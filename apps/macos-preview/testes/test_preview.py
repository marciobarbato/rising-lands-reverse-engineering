import hashlib,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from engine import Preview,MANIFEST

class PreviewTests(unittest.TestCase):
    def test_snapshot_integrity(self):
        snap=ROOT/MANIFEST['snapshot']
        for item in MANIFEST['files']:
            self.assertEqual(hashlib.sha256((snap/item['path']).read_bytes()).hexdigest(),item['sha256'],item['path'])
    def test_asset_integrity_and_cd_provenance(self):
        m=json.loads((ROOT/'assets/fontes.json').read_text())
        self.assertEqual(m['commit'],MANIFEST['commit'])
        for f in m['outputs']:self.assertEqual(hashlib.sha256((ROOT/'assets'/f['path']).read_bytes()).hexdigest(),f['sha256'])
        self.assertEqual(len(m['sources']),4)
    def test_local_detour_reaches_without_crossing_obstacle(self):
        p=Preview();p.order(0,10,4);p.step(200);u=p.state()['units'][0]
        self.assertEqual(u['pos'],[10,4]);self.assertEqual(u['state'],7)
        self.assertNotIn([6,4],u['trail']);self.assertTrue(p.world.colisoes)
        self.assertEqual(u['route'],u['trail'])
    def test_general_solver_missing_is_explicit(self):
        p=Preview();p.reset('parede','local');p.order(0,10,4);p.step(200);u=p.state()['units'][0]
        self.assertIsNotNone(u['blocked']);self.assertIn('SolucionadorOriginal',u['blocked'])
        self.assertNotEqual(u['pos'],u['requested']);self.assertEqual(u['state'],2);self.assertTrue(p.paused)
        position=u['pos'];p.step(100);self.assertEqual(p.state()['units'][0]['pos'],position)
    def test_paused_and_single_step(self):
        p=Preview();p.order(0,10,4);p.handle({'action':'pump'});self.assertEqual(p.tick,0)
        p.handle({'action':'step'});self.assertEqual(p.tick,1);self.assertTrue(p.paused)
    def test_all_speed_factors_have_exact_relative_tick_counts(self):
        for speed in (.25,.5,1,2,4,8):
            p=Preview();p.order(0,15,15);p.handle({'action':'speed','speed':speed});p.handle({'action':'play'})
            for _ in range(4):p.handle({'action':'pump'})
            self.assertEqual(p.tick,int(8*speed),speed)
    def test_forecast_does_not_change_live_world(self):
        p=Preview();p.order(0,10,4);before=bytes(p.world.unidades);events=list(p.world.colisoes)
        p.forecast(0);self.assertEqual(bytes(p.world.unidades),before);self.assertEqual(p.world.colisoes,events)
    def test_blocked_destination_is_not_reported_as_arrival(self):
        p=Preview();p.order(0,6,4);p.step(200);u=p.state()['units'][0]
        self.assertNotEqual(u['pos'],u['requested']);self.assertEqual(u['state'],7)
        self.assertIn('sem alcançar',p.events[-1]['text'])
    def test_units_do_not_share_cells(self):
        p=Preview();p.reset('livre');p.order(0,2,9);p.step(200)
        cells=[u['pos'] for u in p.state()['units']];self.assertEqual(len({tuple(x) for x in cells}),len(cells))
        self.assertTrue(p.world.colisoes)
    def test_new_order_after_missing_function(self):
        p=Preview();p.reset('parede','local');p.order(0,10,4);p.step(200);self.assertTrue(p.blocked)
        p.order(0,2,4);p.step(200);self.assertNotIn(0,p.blocked);self.assertEqual(p.state()['units'][0]['pos'],[2,4])
    def test_mission_is_original_and_read_only(self):
        p=Preview();p.reset('missao');self.assertEqual((p.width,p.height),(64,64));self.assertEqual(len(p.state()['units']),16)
        self.assertEqual(p.state()['units'][0]['pos'],[7,15])
        with self.assertRaises(ValueError):p.order(0,8,15)
        with self.assertRaises(ValueError):p.handle({'action':'play'})
    def test_python_solver_routes_around_wall(self):
        p=Preview();p.reset('parede','python');p.order(0,10,4)
        for _ in range(4):p.step(200)
        u=p.state()['units'][0]
        self.assertEqual(u['pos'],[10,4]);self.assertEqual(u['state'],7);self.assertFalse(u['blocked'])
        self.assertTrue(p.world.historico_navegacao);self.assertIn([6,11],u['trail'])
        for x,y in u['trail']:self.assertFalse(x==6 and y<11)
    def test_python_solver_refuses_missing_structures_grid(self):
        p=Preview();p.reset('parede','python');p.world.regioes[0x808]=0x8000
        p.order(0,10,4);p.step(200);u=p.state()['units'][0]
        self.assertIsNotNone(u['blocked']);self.assertIn('estruturas',u['blocked'])
        self.assertNotEqual(u['pos'],u['requested']);self.assertTrue(p.paused)
    def test_invalid_input_has_no_side_effect(self):
        p=Preview();before=bytes(p.world.unidades)
        for msg in ({'action':'order','x':16,'y':4},{'action':'order','x':True,'y':4},{'action':'select','unit':799},{'action':'speed','speed':100},{'action':'shell'}):
            with self.assertRaises(ValueError):p.handle(msg)
        self.assertEqual(bytes(p.world.unidades),before)
    def test_json_protocol_recovers_after_error(self):
        msgs=[{'id':1,'action':'init'},{'id':2,'action':'select','unit':500},{'id':3,'action':'select','unit':2}]
        proc=subprocess.run([sys.executable,'-I','-B','src/engine.py'],cwd=ROOT,input='\n'.join(json.dumps(x) for x in msgs)+'\n',text=True,capture_output=True,timeout=15)
        self.assertEqual(proc.returncode,0);responses=[json.loads(x) for x in proc.stdout.splitlines()]
        self.assertEqual([r['ok'] for r in responses],[True,False,True]);self.assertEqual(responses[2]['state']['selected'],2)
    def test_no_x86_dependency_loaded(self):
        p=Preview();p.order(0,10,4);p.step(200)
        self.assertNotIn('unicorn',sys.modules);self.assertNotIn('solucionador_original',sys.modules)

if __name__=='__main__':unittest.main(verbosity=2)
