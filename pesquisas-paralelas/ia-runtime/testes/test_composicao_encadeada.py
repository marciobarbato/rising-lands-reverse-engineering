"""The committed M2.1 round-3 chained composition report (validacao/m2-quadro1-encadeado-ia.json)."""
import json
from pathlib import Path
import unittest

OWNED = Path(__file__).resolve().parents[1]
REPORT = json.loads((OWNED / 'validacao/m2-quadro1-encadeado-ia.json').read_text())


class ChainedCompositionReport(unittest.TestCase):
    def test_native_path_reproduced_from_a_clean_tree(self):
        self.assertTrue(REPORT['path_reproduction']['passed'])
        self.assertNotIn('note', REPORT['path_reproduction'])          # not a cached collection
        self.assertEqual(REPORT['source_dirty_paths'], [])

    def test_every_phase_equal_chained_from_python(self):
        for fase in ('load_tail', 'between_frames', 'frame1'):
            with self.subTest(fase):
                r = REPORT['phases'][fase]
                self.assertEqual(r['result'], 'returned')
                self.assertTrue(r['state_equal'] and r['rng_equal'])
                self.assertTrue(r['bindings']['equal'] and r['boundaries']['equal'])
                self.assertTrue(all(c['equal'] for c in r['checkpoints']))
        self.assertTrue(all(REPORT['phases']['between_frames']['registers_equal'].values()))

    def test_only_declared_stops_are_crossed(self):
        cruzadas = [(f, c['routine'], c['owner']) for f, r in REPORT['phases'].items() for c in r['crossings']]
        self.assertEqual(cruzadas, [
            ('load_tail', 'RestoreAll', 'graphics'), ('load_tail', 'SetClipping', 'core'),
            ('load_tail', 'InitGameZone', 'core'), ('load_tail', 'InitGameZone', 'core'),
            ('load_tail', 'NextAnimTerrain', 'core'), ('load_tail', 'NextAnimVeget', 'core'),
            ('frame1', 'NextAnimTerrain', 'core'), ('frame1', 'NextAnimVeget', 'core')])
        self.assertTrue(all(c['state_equal_at_entry'] for r in REPORT['phases'].values() for c in r['crossings']))


if __name__ == '__main__':
    unittest.main()
