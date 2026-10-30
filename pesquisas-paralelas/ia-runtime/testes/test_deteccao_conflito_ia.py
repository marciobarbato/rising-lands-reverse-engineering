"""The actual S1 detection entry, live aliases, and raw-register guard."""
import json
import hashlib
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
import ambiente_ia_runtime  # noqa: F401
from deteccao_conflito_ia import detectar_registradores, REG7
from validar_deteccao_conflito_ia import DetectionMemory
from entrada_estruturas import ArgumentoNaoPassado


class NoMemory:
    def __getattr__(self, name):
        raise AssertionError(f'Unexpected access {name}')


class Detection(unittest.TestCase):
    def test_actual_call_all_effects_and_registers(self):
        c = json.loads((OWNED/'evidencias/s1-deteccao-conflito-original-v2.json').read_text())['cases'][0]
        runs = c['read_before_write']+c['adapter_entry_spans']+[[a, f'{v:02x}'] for a, v, new in c['changed_bytes']]
        m = DetectionMemory(runs, c['adapter_entry_spans'][:2])
        regs = {k: int(v, 16) for k, v in c['entry_registers'].items()}
        regs['ESP'] = int(c['esp'], 16)
        self.assertEqual(detectar_registradores(m, regs), {k: int(v, 16) for k, v in c['exit_registers'].items()})
        for a, old, new in c['changed_bytes']:
            self.assertEqual(m.u8(int(a, 16)), new)
        self.assertEqual(m.u8(0x474a9254+2), 1)
        self.assertEqual(m.u16(0x474a9254+0xb8), 8)
        self.assertEqual(m.u16(0x520352), 1)
        self.assertEqual(m.u16(0x520356), 40)

    def test_missing_registers_fail_before_access(self):
        for missing in REG7:
            with self.assertRaises(ArgumentoNaoPassado):
                detectar_registradores(NoMemory(), {k: 0 for k in REG7 if k != missing})

    def test_native_report_has_zero_mismatches(self):
        r = json.loads((OWNED/'validacao/deteccao-conflito-native.json').read_text())
        self.assertEqual(r['comparisons'], 35)
        self.assertEqual(r['equal'], 35)
        self.assertTrue(all(c['equal'] for c in r['cases']))
        for name, expected in r['source_sha256'].items():
            self.assertEqual(hashlib.sha256((OWNED/name).read_bytes()).hexdigest(), expected)


if __name__ == '__main__':
    unittest.main()
