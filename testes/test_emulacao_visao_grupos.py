"""Native differential of the structure vision, group selection, minimap and exit-position translations
(RISING_EMULAR=1, about 4 minutes).

Reruns the accepted MONDE01 display path to frame 1's first ProcessInputGame entry, runs the 320 declared cases
(329 measured steps, the windows included) natively and compares each with ``visao_grupos`` over a copy of the
exact step-entry state (``validar_visao_grupos.comparar``) and with the committed capture.
"""
import os
from pathlib import Path
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialVisaoGrupos(unittest.TestCase):
    def test_every_declared_step_matches_the_original(self):
        from validar_visao_grupos import executar
        registros, _, reproducao, _, _, captura = executar()
        self.assertTrue(all(reproducao.values()), reproducao)
        self.assertEqual(len(registros), len(captura['cases']))
        self.assertEqual([r['case'] for r in registros if not r['ok']], [])


if __name__ == '__main__':
    unittest.main()
