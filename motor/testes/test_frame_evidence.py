from pinned_reference import reference_file
"""Fast tests of frame ABI layout and the offline evidence comparator (no game run)."""
import ast
import ctypes as C
from pathlib import Path
import struct
import unittest

from frame_abi import FrameInput, FrameEvent, unpack_blocks
from frame_differential import (ROOT, PINS, FIRST_POLICY, assert_pins, check_mutation_detection,
                                normalize_events)
from frame_evidence import MascaraEnderecos, comparar_estado


class FrameHarnessTests(unittest.TestCase):
    def test_frame_abi_layout(self):
        self.assertEqual(C.sizeof(FrameInput), 72)
        self.assertEqual(FrameInput.registers.offset, 12)
        self.assertEqual(FrameInput.saved.offset, 44)
        self.assertEqual(FrameInput.msg.offset, 56)
        self.assertEqual(C.sizeof(FrameEvent), 72)
        self.assertEqual(FrameEvent.stack_mask.offset, 68)

    def test_bulk_snapshot_strict(self):
        raw = struct.pack('<III', 1, 0x497164, 4) + b'abcd'
        self.assertEqual(unpack_blocks(raw), {0x497164: b'abcd'})
        for bad in (b'', raw[:-1], raw + b'x', struct.pack('<III', 1, 0, 0),
                    struct.pack('<I', 2) + raw[4:] + raw[4:]):
            with self.subTest(raw=bad), self.assertRaises(ValueError):
                unpack_blocks(bad)

    def test_actual_compared_byte_corruption_detected(self):
        state = {'test': (0x1000, b'abcd')}
        mask = MascaraEnderecos([['0x1000', '0x1002']])
        self.assertEqual(check_mutation_detection(mask, state), dict(address='0x1002', detected=True))
        self.assertTrue(comparar_estado(mask, {'test': (0x1000, b'XXcd')}, state)['equal'])
        self.assertFalse(comparar_estado(mask, {'test': (0x1000, b'abXd')}, state)['equal'])

    def test_unknown_event_rejected(self):
        event = FrameEvent()
        event.kind = 99
        with self.assertRaises(ValueError):
            normalize_events([event], 'frame1', (0, 0))

    def test_exact_frozen_reference_pins(self):
        assert_pins(list(PINS))
        self.assertIn(FIRST_POLICY, PINS)

    def test_copied_comparison_definitions_unchanged(self):
        sources = {
            'pesquisas-paralelas/ia-runtime/comparar_quadro1_encadeado_ia.py': ['comparar_eventos'],
            'pesquisas-paralelas/ia-runtime/comparar_quadros_ia.py': [
                'MascaraEnderecos', 'IntegridadeCaptura', 'resumo_estado', 'resumos_mascarados',
                '_dados', 'aplicar_delta', 'fases_referencia', 'carregar_captura', 'comparar_estado',
                'eventos_logicos', 'comparar_eventos_fase', 'comparar_alocacoes', 'ler_estado'],
        }
        def definitions(path):
            return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(path.read_text()).body
                    if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
        copied = definitions(Path(__file__).with_name('frame_evidence.py'))
        for path, names in sources.items():
            original = definitions(reference_file(ROOT / path))
            for name in names:
                with self.subTest(definition=name):
                    self.assertEqual(copied[name], original[name])


if __name__ == '__main__':
    unittest.main(verbosity=2)
