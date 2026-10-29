"""Frame leaf tests: frozen original captures and perturbed-state Python comparisons.

No original execution is started here. The sparse native corpus contains only
inactive AI-player calls and message-queue calls, whose complete declared input
is present in the committed read-before-write capture. Dispatcher equality is
covered by the separate whole-phase comparison, where all unchanged stores are
observable through the complete mission projection.
"""
import ctypes as C
import hashlib
import importlib
import json
import random
import struct
import sys
import unittest

from differential import ORIGINAL, changed_bytes, declared_input, expected_changes
from pilot_abi import ROOT, Pilot

CAPTURE = 'pesquisas-paralelas/ia-runtime/evidencias/captura-isolada-ia-quadro1.json'
PINS = {'pesquisas-paralelas/ia-runtime/evidencias/captura-isolada-ia-quadro1.json': 'fb493e8ea608b071bfa2d07753e5213d7704d6dd4a86a65c98c0b516390b3d3b', 'pesquisas-paralelas/ia-runtime/rotinas_quadro_ia.py': 'd07cd44cc6844138d8e084e3d35f347be95101642114e5acc594d1be4398ca05', 'pesquisas-paralelas/ia-runtime/proxima_etapa_quadro.py': 'd9a3c39db33703c43d0cc16de2446b6cf860f894aa2d875a1828bbfda3f11f80', 'pesquisas-paralelas/ia-runtime/laco_despachantes.py': '709fd162a21fe0b5c76a617fe5ed353fbf513a9a3ac241c49fc82ae9eddebcf9', 'pesquisas-paralelas/ia-runtime/quadro_calcul_game.py': '1634bed75de495041871540bf33176e3aad607e1cf2c843f96453df623c540d7', 'pesquisas-paralelas/ia-runtime/incursao_ia.py': '2e6bc1cce71dcf589ce162902795e6dfd05ae99c607cf8e92840abcebb1cbffc', 'ferramentas/ia.py': '6df1848a0c372d239bb1430040f4c42c8bd402dde0a77855222469c1f66decff', 'pesquisas-paralelas/combate/alvos_alcance.py': 'b0006a64869041997ab85d51f2758c7bd4c1d602e0f7bc6de3bb7ba75878dc17'}


def references():
    for folder in ('ferramentas', 'pesquisas-paralelas/ia-runtime', 'pesquisas-paralelas/combate'):
        path = str(ROOT / folder)
        if path not in sys.path:
            sys.path.insert(0, path)
    return (importlib.import_module('rotinas_quadro_ia'),
            importlib.import_module('quadro_calcul_game'),
            importlib.import_module('alvos_alcance'),
            importlib.import_module('memoria_quadro_core').MemoriaQuadro)


class FrameAiUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for path, expected in PINS.items():
            if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
                raise ValueError('FrameReferenceIdentityMismatch: ' + path)
        cls.pilot = Pilot()
        cls.routines, cls.frame, cls.targets, cls.memory_type = references()
        fn = cls.pilot.lib.rl_executar_rotina_quadro
        fn.argtypes = [C.c_uint64, C.c_uint32, C.POINTER(C.c_uint32), C.c_uint32, C.POINTER(C.c_uint32)]
        fn.restype = C.c_int32

    def rust(self, routine, arguments, blocks):
        handle = self.pilot.create()
        try:
            self.pilot.load(handle, blocks)
            argv = (C.c_uint32 * len(arguments))(*arguments)
            output = C.c_uint32(0xbadc0de)
            self.pilot.check(self.pilot.lib.rl_executar_rotina_quadro(handle, routine, argv, len(argv), C.byref(output)))
            self.assertEqual(self.pilot.clock(handle), (0, 0))
            return output.value, self.pilot.project(handle)
        finally:
            self.pilot.free(handle)

    def python_memory(self, blocks):
        buffers = [(a, bytearray(b)) for a, b in blocks]
        return self.memory_type(buffers), buffers

    def test_frozen_original_inactive_ai_and_message_calls(self):
        capture = json.loads((ROOT / CAPTURE).read_bytes())
        self.assertEqual(capture['original_sha256'], ORIGINAL)
        self.assertFalse(capture['translation_executed'])
        count = 0
        for call in capture['calls']:
            if call['routine'] not in ('CalculNextReflect', 'MessageBoxCalcul'):
                continue
            for case in call['cases']:
                regs = {k: int(v, 16) for k, v in case['entry_registers'].items()}
                if call['routine'] == 'CalculNextReflect' and regs['EAX'] & 255 == 4:
                    continue  # p4's same-value writes are absent in this historical sparse capture
                before = declared_input(case)
                memory, buffers = self.python_memory(before)
                with self.subTest(phase=call['phase'], routine=call['routine'], player=regs['EAX']):
                    if call['routine'] == 'CalculNextReflect':
                        value, after = self.rust(104, [regs['EAX'], regs['EDX']], before)
                        expected = self.frame.Quadro(memory, {}).calcul_next_reflect(regs['EAX'], regs['EDX'])
                        self.assertEqual(value, expected)
                        self.assertEqual(value & 255, case['al'])
                    else:
                        _, after = self.rust(100, [], before)
                        self.routines.calcular_caixa_mensagens(memory)
                    self.assertEqual(changed_bytes(before, after), expected_changes(case))
                    self.assertEqual(after, [(a, bytes(b)) for a, b in buffers])
                    count += 1
        self.assertEqual(count, 8)

    def test_message_timer_and_no_command_perturbations_against_python(self):
        rng = random.Random(0x469dce)
        for index in range(96):
            head = rng.randrange(256)
            tail = head if index % 3 == 0 else rng.randrange(256)
            duration = (0, 1, 2, 0xffff)[index % 4]
            blocks = [(0x507d54, struct.pack('<HHB', head, tail, 0xa7)),
                      (0x4e7858 + 518 * head, struct.pack('<H', duration))]
            blocks.sort()
            memory, buffers = self.python_memory(blocks)
            self.routines.calcular_caixa_mensagens(memory)
            _, after = self.rust(100, [], blocks)
            self.assertEqual(after, [(a, bytes(b)) for a, b in buffers])
            player = rng.randrange(4)
            command = 0 if index % 2 else rng.randrange(40, 65536)
            data = bytearray(rng.randbytes(10))
            struct.pack_into('<H', data, 0, command)
            blocks = [(0x45ed20, struct.pack('<40I', *([0x45f2de] * 40))),
                      (0x4e2458 + 4 * player, struct.pack('<I', 0x60000000)), (0x60000000, bytes(data))]
            memory, buffers = self.python_memory(blocks)
            expected = self.routines.processar_entrada(memory, player, [0x45f2de] * 40)
            value, after = self.rust(101, [player], blocks)
            self.assertEqual(value, expected)
            self.assertEqual(after, [(a, bytes(b)) for a, b in buffers])

    def test_monster_initialization_and_action_timers_against_python(self):
        from incursao_ia import avancar_monstros
        rng = random.Random(0x47b283)
        for index in range(64):
            data = bytearray(rng.randbytes(0x50b17c - 0x50a9bc))
            origin = 0x50a9bc
            def setv(fmt, addr, value):
                struct.pack_into(fmt, data, addr - origin, value)
            setv('<B', 0x50a9cc, index % 2)
            setv('<H', 0x50a9ce, 3)
            now = rng.randrange(500)
            for i in range(3):
                setv('<H', 0x50a9d0 + 12 * i + 4, 1000)
                setv('<I', 0x50a9d0 + 12 * i + 8, 0)
            setv('<I', 0x50ae80, 2)
            for i in range(2):
                setv('<H', 0x50ae84 + 16 * i + 14, 0x31 if i else 0)
                setv('<I', 0x50ae84 + 16 * i + 8, rng.randrange(2, 1000))
            setv('<B', 0x50b134, 0)
            blocks = [(0x496fe4, b'\x01'), (0x508f7c, struct.pack('<I', now)), (origin, bytes(data))]
            memory, buffers = self.python_memory(blocks)
            avancar_monstros(memory, {'MissionGetNum': lambda sitio: memory.u8(0x496fe4)})
            _, after = self.rust(102, [], blocks)
            self.assertEqual(after, [(a, bytes(b)) for a, b in buffers])

    def test_target_scan_and_occupancy_perturbations_against_python(self):
        rng = random.Random(0x453f74)
        for index in range(48):
            pool = bytearray(rng.randbytes(276 * 800))
            players = bytearray(rng.randbytes(100))
            grid = bytearray(b'\xff\xff' * 65536)
            for i in range(800):
                p = 276 * i
                pool[p] = rng.choice((0, 1, 2, 3, 4, 200))
                pool[p+1] = rng.randrange(26)
                pool[p+2] = rng.choice((0, 4, 7, 14))
                pool[p+0xbb] = rng.randrange(6)
                cell = rng.randrange(65536)
                struct.pack_into('<H', pool, p+8, cell)
                struct.pack_into('<H', grid, 2*cell, 0x4000 | i << 3)
            unit = rng.randrange(800)
            p = unit * 276
            kind, cell, filt = pool[p+1], struct.unpack_from('<H', pool, p+8)[0], index % 3
            masks = bytes(players[20*i+6] for i in range(5))
            units = [bytes(pool[276*i:276*(i+1)]) for i in range(800)]
            class Grid:
                def get(self, cell, default):
                    return struct.unpack_from('<H', grid, 2*cell)[0]
            expected = self.targets.encontrar_alvo(units, unit, Grid(), masks)
            blocks = [(0x4e0f38, struct.pack('<I', 0x61000000)),
                      (0x4e19a0, struct.pack('<I', 0x60000000)),
                      (0x5080a8, struct.pack('<I', 0x62000000)),
                      (0x60000000, bytes(pool)), (0x61000000, bytes(grid)), (0x62000000, bytes(players))]
            value, after = self.rust(154, [unit], blocks)
            self.assertEqual(value, expected, (index, kind))
            self.assertEqual(after, blocks)
            expected = self.targets.ocupa_celula(units[unit], cell, filt)
            value, after = self.rust(157, [unit, cell, filt], blocks)
            self.assertEqual(value, int(expected))
            self.assertEqual(after, blocks)

    def test_active_task_is_named_atomic_dependency_stop(self):
        task=bytearray(96)
        struct.pack_into('<I',task,0,0xffffffff)
        blocks=[(0x512320,bytes(task)),(0x5148b0,struct.pack('<4I',0,1,96,0x512320)),
                (0x514910,struct.pack('<5I',0x401234,0,0,0,0))]
        handle = self.pilot.create()
        try:
            self.pilot.load(handle, blocks)
            argv = (C.c_uint32 * 1)(0x5148b0)
            output = C.c_uint32(0xaabbccdd)
            code = self.pilot.lib.rl_executar_rotina_quadro(handle, 103, argv, 1, C.byref(output))
            self.assertEqual(code, 5)
            self.assertIn('iaSolver unported rule', self.pilot.error())
            self.assertIn('0x00401234', self.pilot.error())
            self.assertEqual(output.value, 0xaabbccdd)
            self.assertEqual(self.pilot.project(handle), blocks)
        finally:
            self.pilot.free(handle)


if __name__ == '__main__':
    unittest.main()
