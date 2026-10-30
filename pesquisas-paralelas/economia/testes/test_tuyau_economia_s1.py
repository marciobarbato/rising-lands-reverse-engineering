"""Exact S1 TuyauEstSortie native capture, sparse replay and required registers."""
import hashlib
import json
import lzma
from pathlib import Path
import sys
import unittest

PASTA=Path(__file__).resolve().parents[1]
RAIZ=PASTA.parents[1]
for p in (RAIZ/'ferramentas',PASTA):sys.path.insert(0,str(p))
import tuyau_economia_s1 as t
from entrada_estruturas import ArgumentoNaoPassado
from sondar_tuyau_economia_s1 import CAPTURA,comparar


def captura():return json.loads(lzma.decompress(CAPTURA.read_bytes()))


class TuyauS1(unittest.TestCase):
    def test_original_real_call_sites(self):
        c=captura();self.assertFalse(c['translation_executed'])
        self.assertTrue(c['reproduction']['code_unchanged'])
        reais=[r for r in c['cases'] if r['kind']=='in_situ']
        self.assertEqual([r['frame'] for r in reais],[1977,1978,1979,1980])
        self.assertTrue(all(r['caller']=='AffBatiments+0x1965' for r in reais))
        self.assertEqual(len(c['cases']),273)

    def test_sparse_native_replay(self):
        for c in captura()['cases']:
            with self.subTest(label=c.get('label',c['kind'])):self.assertTrue(comparar(c)['ok'])

    def test_all_inputs_required_before_memory(self):
        p=t.provedor_tuyau_economia_s1(t.TuyauEconomiaS1(None))
        for omitido in t.REG7:
            with self.subTest(register=omitido),self.assertRaises(ArgumentoNaoPassado):
                p('TuyauEstSortie',0x44357c,{k:0 for k in t.REG7 if k!=omitido})

    def test_protected_structure_range(self):
        for i in (1000,65535):
            with self.assertRaises(ValueError):t.TuyauEconomiaS1(None).chamar('TuyauEstSortie',dict.fromkeys(t.REG7,0)|{'EAX':i})

    def test_native_attestation_only_pins_economy(self):
        r=json.loads((PASTA/'validacao-tuyau-s1-emulada.json').read_bytes())
        self.assertEqual(r['comparisons'],273);self.assertEqual(r['mismatches'],[])
        self.assertTrue(r['rerun_equals_capture'])
        self.assertEqual(r['capture_sha256'],hashlib.sha256(CAPTURA.read_bytes()).hexdigest())
        for p,h in r['source_sha256'].items():
            self.assertTrue(p.startswith('pesquisas-paralelas/economia/'))
            self.assertEqual(hashlib.sha256((RAIZ/p).read_bytes()).hexdigest(),h,p)


if __name__=='__main__':unittest.main()
