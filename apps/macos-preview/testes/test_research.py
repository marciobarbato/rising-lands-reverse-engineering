from pathlib import Path
import hashlib,json,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from engine import Preview
from research_adapter import RESEARCH

class ResearchTests(unittest.TestCase):
    def test_all_research_files_match_frozen_snapshots(self):
        for m in RESEARCH.values():
            for f in m['files']:self.assertEqual(hashlib.sha256((ROOT/m['path']/f['path']).read_bytes()).hexdigest(),f['sha256'])
            self.assertTrue(m['historicalValidation']['sucesso'])
    def test_credits_and_debits_are_real_and_do_not_recruit(self):
        p=Preview();before=bytes(p.world.unidades)
        p.handle({'action':'economy','operation':'credit','resource':1,'quantity':12})
        self.assertEqual(p.research.economy.consultar(0).comida,42)
        p.handle({'action':'economy','operation':'debit','resource':1,'quantity':50})
        self.assertEqual(p.research.economy.consultar(0).comida,0);self.assertEqual(bytes(p.world.unidades),before)
    def test_capacity_excess_bags_and_recalculation(self):
        p=Preview();p.handle({'action':'economy','operation':'deposit','resource':1,'quantity':150})
        r=p.research.state();self.assertEqual(r['balances'][0]['comida'],130)
        self.assertEqual(sum(b['quantity'] for b in r['bags']),50);self.assertEqual(r['level'],7)
        p.handle({'action':'economy','operation':'withdraw','resource':1,'quantity':10})
        self.assertEqual(p.research.state()['balances'][0]['comida'],120)
    def test_target_query_preserves_live_movement_and_health(self):
        p=Preview();before=bytes(p.world.unidades);p.handle({'action':'combat','unit':0,'target':2})
        r=p.research.last_combat;self.assertTrue(r['enemy']);self.assertFalse(r['damageApplied'])
        self.assertTrue(r['orderAcceptedOnCopy']);self.assertEqual(r['aim']['orientacao_requerida'],13)
        self.assertEqual(bytes(p.world.unidades),before)
    def test_target_selection_reads_updated_spatial_grid(self):
        p=Preview();p.reset('livre');p.order(2,4,4)
        for _ in range(4):p.step(200)
        p.research.combat(p.world,0,2);self.assertEqual(p.research.last_combat['automaticTarget'],2)
    def test_missing_building_callback_is_explicit(self):
        from alvos_alcance import a_portee
        p=Preview();records=[p.world.ler_unidade(i) for i in range(800)]
        with self.assertRaises(NotImplementedError):a_portee(records,0,3,0)
    def test_economy_rejects_unknown_operations_and_bad_inputs(self):
        p=Preview();before=bytes(p.research.economy.memoria)
        for msg in ({'operation':'recruit'},{'operation':'credit','quantity':-1},{'operation':'deposit','resource':3}):
            with self.assertRaises(ValueError):p.research.mutate(msg)
        self.assertEqual(bytes(p.research.economy.memoria),before)
if __name__=='__main__':unittest.main(verbosity=2)
