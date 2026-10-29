"""Fresh intact native vs Python differential of the Core frame-0/frame-1 callees (RISING_EMULAR=1)."""
import os
from pathlib import Path
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
sys.path.insert(0, str(RAIZ))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialChamadasQuadro1(unittest.TestCase):
    def test_exact_frame_inputs_and_perturbations(self):
        from validar_chamadas_quadro_core import diferencial
        r = diferencial()
        self.assertTrue(r['path_reproduction']['passed'], r['path_reproduction'])
        self.assertEqual(r['mismatches'], [])
        self.assertEqual(r['dependencies'], [])
        self.assertEqual(r["calls"], 678 + 61)
        self.assertGreater(r['comparisons'], 678)
        # Perturbations reach the non-captured outcomes: positive visibility exits, region inserts.
        for nome in ('BatimentEstDecouvert', 'BatimentContourEstIllumine', 'CaseEstDecouverte', 'CaseEstIlluminee'):
            self.assertIn('1', r['al_by_routine'][nome], nome)
        self.assertIn('1', r['al_by_routine']['Chemin_ModifieZone'])
        self.assertIn('SetEnginCollision', r['cases_with_stores'])

    def test_display_scenario_exact_inputs_and_perturbations(self):
        from validar_chamadas_quadro_core import diferencial
        r = diferencial(cenario='exibicao')
        self.assertTrue(r['path_reproduction']['passed'], r['path_reproduction'])
        self.assertEqual((r['mismatches'], r['dependencies']), ([], []))
        self.assertEqual(r['calls'], 124)
        for nome in ('NextAnimTerrain', 'NextAnimVeget', 'NextAnimVegetFullMap', 'rand', 'LongRand', 'InitGameZone'):
            self.assertIn(nome, r['cases_with_stores'], nome)
        for nome in ('TerrainEstDecouvert', 'TerrainEstIllumine', 'ExisteEngin', 'EnginGetType', 'EnginGetPlayer',
                     'EnginEstArmure', 'EnginEstMiroir', 'EnginEstTerreur', 'TypeEnginSeFatigue', 'MissionGetNum'):
            self.assertIn(nome, r['by_routine'], nome)


if __name__ == '__main__':
    unittest.main()
