"""S1 result-screen Economy bodies: native writes/order/calls, exact ABI and x87."""
import copy
import hashlib
import json
import lzma
from pathlib import Path
import sys
import unittest
from unittest import mock

PASTA=Path(__file__).resolve().parents[1];RAIZ=PASTA.parents[1]
for p in (RAIZ/'ferramentas',PASTA):sys.path.insert(0,str(p))
import tecnologia_economia_s1 as t
import replay_tecnologia_economia_s1 as replay
from entrada_estruturas import ArgumentoNaoPassado


def captura():return json.loads(lzma.decompress(replay.CAPTURA.read_bytes()))


class TecnologiaS1(unittest.TestCase):
    def test_original_first_complete_s1_segment(self):
        c=captura();self.assertFalse(c['translation_executed'])
        self.assertEqual(len(c['cases']),511)
        self.assertEqual(set(c['by_routine']),set(t.ROTINAS))
        self.assertTrue(c['reproduction']['code_unchanged'])
        self.assertEqual(c['reproduction']['last_frame'],17044)
        self.assertEqual(c['reproduction']['frames_checked'],45)
        self.assertTrue(all(r['kind']=='in_situ' for r in c['cases']))
        self.assertEqual(sum(r['frame']==17043 for r in c['cases']),510)
        self.assertEqual([(r['frame'],r['routine']) for r in c['cases'] if r['frame']!=17043],
                         [(17044,'RechercheGetBranche')])

    def test_every_native_case_registers_memory_store_order_calls_and_provider(self):
        counts,bad=replay.replay()
        self.assertEqual(sum(x['cases'] for x in counts.values()),511)
        self.assertEqual(bad,[])

    def test_every_provider_register_required_before_reads(self):
        provider=t.provedor_tecnologia_economia_s1(t.TecnologiaEconomiaS1(None))
        for n in t.ROTINAS:
            for missing in t.REG7:
                with self.subTest(routine=n,register=missing),self.assertRaises(ArgumentoNaoPassado):
                    provider(n,t.ROTINAS[n],{k:0 for k in t.REG7 if k!=missing})

    def test_missing_foreign_dependency_retains_prior_reset_and_copy_writes(self):
        c=next(c for c in captura()['cases'] if c['routine']=='RechercheCalculNew')
        m=replay.MemoriaGravada(c['read_before_write'])
        r={k:int(v,16) for k,v in c['entry_registers'].items()};r['ESP']=int(c['esp'],16)
        with self.assertRaises(t.DependenciaTecnologiaS1) as e:t.TecnologiaEconomiaS1(m).chamar(c['routine'],r)
        self.assertEqual(e.exception.rotina,'MissionGetNum')
        self.assertEqual(e.exception.chamada,0x47165f)
        self.assertGreater(len(m.lojas),1200)
        self.assertEqual(m.u8(0x4dfad4),0)
        self.assertEqual(m.u8(0x5080f4),m.u8(0x508134))

    def test_unknown_effect_is_named_and_never_becomes_an_empty_callback(self):
        c=next(c for c in captura()['cases'] if c['routine']=='InventionSetEffet')
        m=replay.MemoriaGravada(c['read_before_write'])
        r={k:int(v,16) for k,v in c['entry_registers'].items()}
        a=t.TABELA+360*(r['EBX']&65535)+12*(r['EDX']&65535)
        m.bytes[a+6]=1
        with self.assertRaises(t.ForaDoDominioTecnologiaS1):t.TecnologiaEconomiaS1(m).chamar(c['routine'],r)
        self.assertEqual(m.lojas,[])

    def test_store_order_and_callback_argument_mutations_are_detected(self):
        c=next(c for c in captura()['cases'] if c['routine']=='RechercheCalculNew')
        modified=copy.deepcopy(c)
        modified['stores'][0],modified['stores'][1]=modified['stores'][1],modified['stores'][0]
        self.assertFalse(replay.comparar(modified)['ok'])
        modified=copy.deepcopy(c)
        call=next(x for x in modified['calls'] if x[1]=='MissionGetNum')
        call[2]['EDX']=hex(int(call[2]['EDX'],16)^1)
        self.assertFalse(replay.comparar(modified)['ok'])
        with mock.patch.object(t.TecnologiaEconomiaS1,'_BonusReset',lambda self,r:dict(r,EAX=4)):
            self.assertFalse(replay.comparar(c)['ok'])

    def test_x87_values_and_one_push_including_signed_zero(self):
        path=PASTA/'evidencias/lacunas-s1/captura-recherche-get-etat-x87.json.xz'
        c=json.loads(lzma.decompress(path.read_bytes()));self.assertFalse(c['translation_executed'])
        self.assertEqual(len(c['cases']),9)
        for row in c['cases']:
            regs={k:int(v,16) for k,v in row['entry_registers'].items()}
            m=replay.MemoriaGravada(row['read_before_write'])
            r=t.TecnologiaEconomiaS1(m).chamar('RechercheGetEtat',regs)
            top=(row['x87_after']['FPSW']>>11)&7
            self.assertEqual(top,(((row['x87_before']['FPSW']>>11)-1)&7))
            self.assertEqual(tuple(row['x87_after'][f'FP{top}']),r['_x87_push'])
            self.assertEqual(m.lojas,[])
        self.assertEqual(t.double_para_x87(1<<63),(0,0x8000))
        with self.assertRaises(t.ForaDoDominioTecnologiaS1):t.double_para_x87(0x7ff0000000000000)

    def test_native_reports_bind_only_owned_sources(self):
        for name,n in (('validacao-tecnologia-s1-emulada.json',511),('validacao-recherche-get-etat-x87-emulada.json',9)):
            r=json.loads((PASTA/name).read_bytes())
            self.assertEqual(r['comparisons'],n);self.assertEqual(r['mismatches'],[])
            self.assertTrue(r['rerun_equals_capture'])
            for path,h in r['source_sha256'].items():
                self.assertTrue(path.startswith('pesquisas-paralelas/economia/'))
                self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(),h,path)


if __name__=='__main__':unittest.main()
