"""Original-first S1 sack query, exact provider ABI and native attestation."""
import hashlib
import json
import lzma
from pathlib import Path
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
RAIZ = PASTA.parents[1]
for p in (RAIZ/'ferramentas', PASTA):
    sys.path.insert(0, str(p))
import lacunas_economia_s1 as l
from sondar_lacunas_economia_s1 import caminho, traduzir
from entrada_estruturas import ArgumentoNaoPassado


def captura():
    return json.loads(lzma.decompress(caminho('sac').read_bytes()))


class SacS1(unittest.TestCase):
    def test_original_only_at_inputgame(self):
        c = captura()
        self.assertFalse(c['translation_executed'])
        self.assertTrue(c['reproduction']['code_unchanged'])
        reais = [r for r in c['cases'] if r['kind']=='in_situ']
        self.assertEqual([(r['frame'], r['caller_return']) for r in reais], [(3851, '0x4299df')])
        self.assertEqual(len(c['cases']), 274)
        self.assertTrue(all(not r['stores'] and not r['changed_bytes'] for r in c['cases']))

    def test_all_native_cases_and_provider(self):
        for r in captura()['cases']:
            with self.subTest(label=r.get('label',r['kind'])):
                self.assertTrue(traduzir(r)['ok'])

    def test_missing_registers_rejected_before_memory(self):
        class NaoLer:
            def __getattr__(self, n):
                raise AssertionError('Memory accessed before ABI validation')
        p = l.provedor_lacunas_economia_s1(l.LacunasEconomiaS1(NaoLer()))
        for k in l.REG7:
            with self.subTest(register=k), self.assertRaises(ArgumentoNaoPassado):
                p('SacGetCapacite',0x4299da,{r:0 for r in l.REG7 if r!=k})

    def test_quantity_pointer_upper_half_is_observable(self):
        from replay_ciclo_trabalho import MemoriaEsparsa
        r = next(r for r in captura()['cases'] if r['kind']=='in_situ')
        m = MemoriaEsparsa(r['read_before_write'])
        entrada = {k:int(v,16) for k,v in r['entry_registers'].items()}
        t = l.LacunasEconomiaS1(m)
        saida = t.chamar('SacGetCapacite',entrada)
        self.assertEqual(saida['EAX'] & 0xffff0000,m.u32(0x507dac) & 0xffff0000)
        self.assertNotEqual(saida['EAX'] & 0xffff0000,0)

    def test_native_report_bound_to_owned_sources(self):
        p = PASTA/'validacao-lacunas-s1-sac-emulada.json'
        r = json.loads(p.read_bytes())
        self.assertEqual(r['comparisons'],274)
        self.assertEqual(r['mismatches'],[])
        self.assertTrue(r['rerun_equals_capture'])
        self.assertEqual(r['capture_sha256'],hashlib.sha256(caminho('sac').read_bytes()).hexdigest())
        for nome,h in r['source_sha256'].items():
            self.assertTrue(nome.startswith('pesquisas-paralelas/economia/'))
            self.assertEqual(hashlib.sha256((RAIZ/nome).read_bytes()).hexdigest(),h,nome)


if __name__ == '__main__':
    unittest.main()
