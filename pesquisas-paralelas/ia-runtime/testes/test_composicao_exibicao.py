"""The committed M2.1 round-4 reports: chained composition on the display reference and the v1 regression."""
import json
from pathlib import Path
import unittest

OWNED = Path(__file__).resolve().parents[1]
EXIBICAO = json.loads((OWNED / 'validacao/m2-quadro1-exibicao-ia.json').read_text())
V1 = json.loads((OWNED / 'validacao/m2-quadro1-v1-r4-ia.json').read_text())
FASES = ('load_tail', 'between_frames', 'frame1')


class DisplayReferenceReports(unittest.TestCase):
    def verificar(self, relatorio):
        self.assertTrue(relatorio['path_reproduction']['passed'])
        self.assertNotIn('note', relatorio['path_reproduction'])          # not a cached collection
        for fase in FASES:
            r = relatorio['phases'][fase]
            self.assertEqual(r['result'], 'returned', fase)
            self.assertTrue(r['state_equal'] and r['rng_equal'], fase)
            self.assertTrue(r['bindings']['equal'] and r['boundaries']['equal'], fase)
            self.assertTrue(all(c['equal'] for c in r['checkpoints']), fase)
            self.assertTrue(all(c['state_equal_at_entry'] for c in r['crossings']), fase)
        self.assertTrue(all(relatorio['phases']['between_frames']['registers_equal'].values()))

    def test_display_reference_equal_chained(self):
        self.verificar(EXIBICAO)
        self.assertEqual(EXIBICAO['scenario'], 'exibicao')
        self.assertEqual(EXIBICAO['source_dirty_paths'], [])
        cruzadas = [(f, c['routine'], c['owner']) for f in FASES for c in EXIBICAO['phases'][f]['crossings']]
        self.assertEqual(cruzadas, [
            ('load_tail', 'RestoreAll', 'graphics'), ('load_tail', 'DDLockSurface', 'graphics'),
            ('load_tail', 'DeleteBank', 'graphics'), ('load_tail', 'FilledBox', 'graphics'),
            ('load_tail', 'DDUnlockSurface', 'graphics'), ('load_tail', 'DDFlipPage', 'graphics'),
            ('load_tail', 'NextAnimTerrain', 'core'), ('load_tail', 'NextAnimVeget', 'core'),
            ('between_frames', 'AffGame', 'graphics'),
            ('frame1', 'NextAnimTerrain', 'core'), ('frame1', 'NextAnimVeget', 'core')])

    def test_graphics_crossings_write_no_logic_dgroup_byte(self):
        exibicao = {0x496394, 0x496395, 0x496396, 0x4963b5, 0x49a02e, 0x49a02f, 0x49a032, 0x49a033, 0x49a042,
                    0x49a043, 0x49a044, 0x49a045, 0x4e17b0, 0x4e17b1, 0x4e17b2, 0x4e17b4, 0x4e17b5, 0x4e17b6,
                    0x49a04e, 0x4e17a6, 0x4e17a7, 0x4e17a8}
        for f in FASES:
            for c in EXIBICAO['phases'][f]['crossings']:
                if c['owner'] == 'graphics':
                    escritos = {int(a, 16) for a, _, _ in c['changed_bytes'].get('dgroup', [])}
                    self.assertLessEqual(escritos, exibicao, (f, c['routine']))

    def test_v1_regression_with_the_same_code(self):
        self.verificar(V1)
        self.assertEqual(V1['scenario'], 'v1')
        self.assertEqual([(f, c['routine']) for f in FASES for c in V1['phases'][f]['crossings']],
                         [('load_tail', 'RestoreAll')])


if __name__ == '__main__':
    unittest.main()
