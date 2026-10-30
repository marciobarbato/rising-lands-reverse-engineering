"""Keep the input reference's flat imports isolated from the older logic port."""
import os,subprocess,sys,unittest
from pathlib import Path
class PlayerChecks(unittest.TestCase):
 def test_declared_input_contracts(self):
  p=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('player_contract_checks.py'))],env=dict(os.environ,RL_REFERENCE_PROFILE='input'),capture_output=True,text=True,timeout=120)
  self.assertEqual(p.returncode,0,p.stdout+p.stderr)
 def test_original_input_routine_effects(self):
  import json,tempfile
  root=Path(__file__).resolve().parents[2]
  with tempfile.TemporaryDirectory(prefix='player-leaves-',dir=root/'.local') as tmp:
   output=Path(tmp)/'proof.json'
   p=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('player_leaf_proof.py')),'--binary',str(root/'motor/target/debug/player_fixtures'),'--output',str(output)],env=dict(os.environ,RL_REFERENCE_PROFILE='input'),capture_output=True,text=True,timeout=1140)
   self.assertEqual(p.returncode,0,p.stdout+p.stderr)
   r=json.loads(output.read_bytes());self.assertEqual((r['cases'],r['completed'],r['completed_state_equal'],r['mismatches']),(463,452,452,[]))
   self.assertEqual(len(r['stops']),11);self.assertEqual(len(r['skips']),2)
   for stop in r['stops']:self.assertNotIn('UndeclaredAccess',stop['stop'])
