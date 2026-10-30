"""Replay native mine-query inputs and check the cross-provider ABI boundary."""
import json
import lzma
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
import ambiente_ia_runtime  # noqa: F401
from entrada_estruturas import ArgumentoNaoPassado
from provedores_entrada_ia import DonosM3
from capturar_consulta_mina_ia import compare


class NoMemory:
    def __getattr__(self, name):
        raise AssertionError(f'Unexpected access: {name}')


class Query(unittest.TestCase):
    def test_native_cases(self):
        data = json.loads(lzma.decompress((OWNED/'evidencias/consulta-mina-original.json.xz').read_bytes()))
        self.assertEqual(len(data['cases']), 101)
        for case in data['cases']:
            with self.subTest(kind=case['kind'], index=case.get('index'), reserve=case.get('reserve')):
                self.assertTrue(compare(case)['equal'])

    def test_missing_uncertain_or_invalid_index_before_memory(self):
        d = DonosM3(NoMemory(), som=None)
        for regs in ({}, dict(EAX=0, _incertos={'EAX': 1})):
            with self.assertRaises(ArgumentoNaoPassado):
                d.externo('MineGetCapacite', 0x44ca17, regs)
        with self.assertRaises(ValueError):
            d.externo('MineGetCapacite', 0x44ca17, dict(EAX=20))

    def test_live_reserve_and_preserved_uncertainty(self):
        from memoria_quadro_core import MemoriaQuadro
        table = bytearray(80)
        m = MemoriaQuadro([(0x509954, table)])
        d = DonosM3(m, som=None)
        regs = dict(EAX=0xabcd0000, EDX=0x12345678,
                    _incertos=dict(EAX=0xffff0000, EDX=0xff000000))
        for reserve in (37, 0):
            m.u16(0x509956, reserve)
            out = d.externo('MineGetCapacite', 0x44ca17, regs)
            self.assertEqual(out['EAX'], reserve)
            self.assertEqual(out['EDX'], regs['EDX'])
            self.assertEqual(out['_incertos']['EDX'], 0xff000000)
            self.assertNotIn('EAX', out['_incertos'])


if __name__ == '__main__':
    unittest.main()
