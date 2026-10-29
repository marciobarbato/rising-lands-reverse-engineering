"""The committed M2.1 first-frame equality proof (validacao/m2-1-prova-quadro1.json)."""
import hashlib
import json
from pathlib import Path
import unittest

OWNED = Path(__file__).resolve().parents[1]
ROOT = OWNED.parents[1]
PROVA = json.loads((OWNED / 'validacao/m2-1-prova-quadro1.json').read_text())


class FirstFrameProof(unittest.TestCase):
    def test_fresh_native_clean_tree(self):
        self.assertTrue(PROVA['path_reproduction']['passed'])
        self.assertNotIn('note', PROVA['path_reproduction'])
        self.assertEqual(PROVA['source_dirty_paths'], [])

    def test_references_and_policy_are_the_committed_files(self):
        for k, ref in PROVA['references'].items():
            self.assertEqual(hashlib.sha256((ROOT / ref['path']).read_bytes()).hexdigest(), ref['sha256'], k)
        self.assertEqual(hashlib.sha256((ROOT / PROVA['policy']['path']).read_bytes()).hexdigest(),
                         PROVA['policy']['sha256'])

    def test_every_phase_equal(self):
        self.assertEqual(PROVA['summary']['result'], 'equal')
        for fase in ('load_tail', 'between_frames', 'frame1'):
            r = PROVA['phases'][fase]
            with self.subTest(fase):
                self.assertTrue(r['equal'])
                for chave in ('state', 'rng', 'bindings', 'boundaries', 'allocation_records'):
                    self.assertTrue(r[chave]['equal'], chave)
                self.assertEqual(r['checkpoints']['total'], r['checkpoints']['equal'])
        self.assertTrue(all(v['equal'] for v in PROVA['phases']['between_frames']['registers'].values()))

    def test_no_crossing_and_display_roots_proved(self):
        self.assertEqual(PROVA['crossings']['count'], 0)
        self.assertEqual(PROVA['crossings']['writing_compared_bytes'], 0)
        self.assertTrue(PROVA['display_roots_not_executed']['all_restored'])


if __name__ == '__main__':
    unittest.main()
