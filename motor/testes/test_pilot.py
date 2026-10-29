"""ABI safety contracts, error boundaries and capture-oracle sensitivity."""
import ctypes as C
from concurrent.futures import ThreadPoolExecutor
import unittest
from unittest.mock import patch

import differential as diff
from pilot_abi import Block, Pilot, Registers, VERSION


class PilotAbiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pilot = Pilot()

    def setUp(self):
        self.world = self.pilot.create()

    def tearDown(self):
        self.pilot.free(self.world)

    def test_version_rate_and_null_output_refuse_creation(self):
        output = C.c_uint64(123)
        self.assertEqual(self.pilot.lib.rl_criar_mundo(VERSION + 1, 20, 0, C.byref(output)), 10)
        self.assertEqual(output.value, 123)
        self.assertEqual(self.pilot.lib.rl_criar_mundo(VERSION, 0, 0, C.byref(output)), 1)
        self.assertEqual(self.pilot.lib.rl_criar_mundo(VERSION, 20, 0, None), 1)

    def test_stale_handles_double_free_and_nonreused_identity(self):
        other = self.pilot.create()
        self.pilot.free(other)
        self.assertEqual(self.pilot.lib.rl_liberar_mundo(other), 2)
        self.assertEqual(self.pilot.lib.rl_avancar_ticks(other, 1), 2)
        newer = self.pilot.create()
        self.assertNotEqual(newer, other)
        self.pilot.free(newer)

    def test_load_and_project_copy_sorted_owned_bytes(self):
        data = (C.c_uint8 * 4)(1, 2, 3, 4)
        blocks = (Block * 1)(Block(100, 4, data))
        self.pilot.check(self.pilot.lib.rl_carregar_blocos(self.world, blocks, 1))
        data[0] = 99
        self.assertEqual(self.pilot.project(self.world), [(100, b'\x01\x02\x03\x04')])
        self.pilot.load(self.world, [(200, b'hi'), (0, b'a')])
        self.assertEqual(self.pilot.project(self.world), [(0, b'a'), (200, b'hi')])
        self.pilot.load(self.world, [])
        self.assertEqual(self.pilot.project(self.world), [])

    def test_malformed_load_is_atomic_with_named_errors(self):
        self.pilot.load(self.world, [(100, b'abc')])
        before = self.pilot.project(self.world)
        with self.assertRaisesRegex(RuntimeError, 'OverlappingRegions'):
            self.pilot.load(self.world, [(100, b'aa'), (101, b'bb')])
        self.assertEqual(self.pilot.project(self.world), before)
        with self.assertRaisesRegex(RuntimeError, 'IncompleteField'):
            self.pilot.load(self.world, [(0x497164, b'aa')])
        self.assertEqual(self.pilot.project(self.world), before)
        self.assertEqual(self.pilot.lib.rl_carregar_blocos(self.world, None, 1), 1)
        self.assertEqual(self.pilot.lib.rl_carregar_blocos(self.world, None, 65537), 9)
        with self.assertRaisesRegex(RuntimeError, 'AddressOverflow'):
            self.pilot.load(self.world, [(0xffffffff, b'aa')])
        self.assertEqual(self.pilot.project(self.world), before)

    def test_unknown_missing_and_unsupported_steps_preserve_registers_and_state(self):
        registers = Registers(1, 2, 3, 4, 5, 6, 7)
        original = bytes(registers)
        self.assertEqual(self.pilot.lib.rl_executar_rotina(self.world, 999, C.byref(registers)), 4)
        self.assertEqual(self.pilot.lib.rl_executar_rotina(self.world, 1, C.byref(registers)), 3)
        self.assertIn('UndeclaredAccess', self.pilot.error())
        self.assertEqual(bytes(registers), original)
        self.pilot.load(self.world, [(0x4990cc, (1).to_bytes(4, 'little'))])
        before = self.pilot.project(self.world)
        self.assertEqual(self.pilot.lib.rl_executar_rotina(self.world, 3, C.byref(registers)), 5)
        self.assertIn('UnsupportedThreadGetter', self.pilot.error())
        self.assertEqual(bytes(registers), original)
        self.assertEqual(self.pilot.project(self.world), before)
        self.assertEqual(self.pilot.lib.rl_executar_rotina(self.world, 1, None), 1)

    def test_failed_bcd_writes_do_not_publish_prefix(self):
        self.pilot.load(self.world, [(100, b'abc')])
        before = self.pilot.project(self.world)
        registers = Registers(eax=100, edx=1234)
        original = bytes(registers)
        self.assertEqual(self.pilot.lib.rl_executar_rotina(self.world, 4, C.byref(registers)), 3)
        self.assertEqual(self.pilot.project(self.world), before)
        self.assertEqual(bytes(registers), original)

    def test_projection_capacity_query_preserves_output_buffer(self):
        self.pilot.load(self.world, [(100, b'abcd')])
        address, required = C.c_uint32(), C.c_uint32()
        output = (C.c_uint8 * 2)(0xaa, 0xbb)
        self.assertEqual(self.pilot.lib.rl_projetar_bloco(self.world, 0, C.byref(address), output, 2, C.byref(required)), 6)
        self.assertEqual((address.value, required.value), (100, 4))
        self.assertEqual(bytes(output), b'\xaa\xbb')
        self.assertEqual(self.pilot.lib.rl_projetar_bloco(self.world, 1, C.byref(address), output, 2, C.byref(required)), 1)
        self.assertEqual(self.pilot.lib.rl_quantidade_blocos(self.world, None), 1)

    def test_error_message_query_is_repeatable_and_thread_local(self):
        self.pilot.lib.rl_liberar_mundo(0)
        self.assertEqual(self.pilot.error(), 'InvalidHandle')
        self.assertEqual(self.pilot.error(), 'InvalidHandle')
        def task():
            self.pilot.lib.rl_executar_rotina(0, 999, C.byref(Registers()))
            return self.pilot.error()
        with ThreadPoolExecutor(max_workers=1) as executor:
            self.assertEqual(executor.submit(task).result(), 'UnknownRoutine')
        self.assertEqual(self.pilot.error(), 'InvalidHandle')

    def test_clock_ticks_and_memory_load_are_separate(self):
        self.pilot.check(self.pilot.lib.rl_avancar_ticks(self.world, 100))
        self.assertEqual(self.pilot.clock(self.world), (100, 5000))
        self.pilot.load(self.world, [(0x497164, (1).to_bytes(4, 'little'))])
        self.assertEqual(self.pilot.clock(self.world), (100, 5000))
        self.pilot.step(self.world, 'Random', dict.fromkeys(('EAX','EBX','ECX','EDX','ESI','EDI','EBP'), 0))
        self.assertEqual(self.pilot.clock(self.world), (100, 5000))

    def test_independent_worlds_repeat_under_concurrent_callers(self):
        def task():
            h = self.pilot.create()
            try:
                self.pilot.load(h, [(0x497164, (123).to_bytes(4, 'little'))])
                result = []
                for _ in range(100):
                    result.append(self.pilot.step(h, 'Random', dict.fromkeys(('EAX','EBX','ECX','EDX','ESI','EDI','EBP'), 0))['EAX'])
                return result
            finally:
                self.pilot.free(h)
        with ThreadPoolExecutor(max_workers=2) as executor:
            a, b = executor.map(lambda _: task(), range(2))
        self.assertEqual(a, b)


class CaptureHarnessTests(unittest.TestCase):
    def test_all_committed_calls_match_original_and_python(self):
        result = diff.run()
        self.assertTrue(result['passed'], result['failures'])
        self.assertEqual(result['comparisons'], 75)
        self.assertEqual(result['skipped'], 0)
        self.assertEqual(result['by_routine'], dict(Random=24, LongRand=12, rand=12, IntToBCD=19, BCDToInt=8))

    def test_tampered_reference_identity_is_refused(self):
        with self.assertRaisesRegex(ValueError, 'ReferenceIdentityMismatch'):
            diff.verify_pins({'ferramentas/chamadas_quadro_core.py': '0' * 64})

    def test_sparse_input_refuses_unknown_conflicting_bytes(self):
        with self.assertRaisesRegex(ValueError, 'UncapturedInputByte'):
            diff.declared_input(dict(read_before_write=[['0x1', None, 'unknown']]))
        with self.assertRaisesRegex(ValueError, 'ConflictingCapturedInput'):
            diff.declared_input(dict(read_before_write=[['0x1', 1, 'a']], changed_bytes=[['0x1', 2, 3]]))

    def test_harness_detects_a_real_rust_return_register_mutation(self):
        original = Pilot.step
        def mutate(pilot, *args):
            result = original(pilot, *args)
            result['EDX'] ^= 1
            return result
        with patch.object(Pilot, 'step', mutate):
            result = diff.run()
        self.assertFalse(result['passed'])
        self.assertEqual(result['mismatches'], 75)
        self.assertTrue(all('ReturnRegisterMismatch' in f['error'] for f in result['failures']))

    def test_harness_detects_a_real_rust_projected_byte_mutation(self):
        original = Pilot.project
        calls = {}
        def mutate(pilot, handle):
            result = original(pilot, handle)
            calls[handle] = calls.get(handle, 0) + 1
            if calls[handle] == 2:
                address, data = result[0]
                result[0] = (address, bytes([data[0] ^ 1]) + data[1:])
            return result
        with patch.object(Pilot, 'project', mutate):
            result = diff.run()
        self.assertFalse(result['passed'])
        self.assertEqual(result['mismatches'], 75)
        self.assertTrue(all('RustOriginalChangedBytesMismatch' in f['error'] for f in result['failures']))

    def test_bcd_alias_and_width_edges_match_unchanged_python(self):
        _, economy, memory_type = diff.references()
        pilot = Pilot()
        for offset in range(-3, 5):
            h = pilot.create()
            try:
                before = [(100, bytes([9, 8, 7, 6, 255, 254, 253, 252, 251, 250, 249, 248]))]
                registers = dict(EAX=103 + offset, EDX=103, EBX=1, ECX=2, ESI=3, EDI=4, EBP=5)
                pilot.load(h, before)
                result = pilot.step(h, 'BCDToInt', registers)
                expected, expected_regs = diff.python_call(None, economy, memory_type, 'BCDToInt', before, registers)
                self.assertEqual(pilot.project(h), expected)
                self.assertEqual(result, expected_regs)
            finally:
                pilot.free(h)
        for value in (0, 1, 999, 1000, 9999, 10000, 65535, 0xffffffff):
            h = pilot.create()
            try:
                before = [(100, b'abcd')]
                registers = dict(EAX=100, EDX=value, EBX=1, ECX=2, ESI=3, EDI=4, EBP=5)
                pilot.load(h, before)
                result = pilot.step(h, 'IntToBCD', registers)
                expected, expected_regs = diff.python_call(None, economy, memory_type, 'IntToBCD', before, registers)
                self.assertEqual(pilot.project(h), expected)
                self.assertEqual(result, expected_regs)
            finally:
                pilot.free(h)


if __name__ == '__main__':
    unittest.main()
