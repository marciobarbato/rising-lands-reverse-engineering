"""Native differential of EteintTerrain at SortieTroupe's abandonment and AvanceEngin (RISING_EMULAR=1, ~6 min).

Reruns Economy's sanctuary abandonment scenario natively and compares every in-situ and declared case with
``fadiga_vegetacao`` (``validar_fadiga_vegetacao``). The hunger scenario (EnginSetFatigue, ChercheVegetLibre,
ChercheTypeBatimentProximite; ~15 min) runs with ``validar_fadiga_vegetacao.py --cenario fome``.
"""
import json
import lzma
import os
from pathlib import Path
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialFadigaVegetacao(unittest.TestCase):
    @unittest.skipUnless((RAIZ / 'pesquisas-paralelas/economia/capturar_abandono_santuario.py').exists(),
                         "Economy's abandonment scenario is not on this tree")
    def test_abandonment_scenario_matches_the_original(self):
        import validar_fadiga_vegetacao as v
        ref = json.loads(lzma.decompress(v.captura_padrao('abandono').read_bytes()))
        ex = v.Execucao('abandono', traduzir=v.traduzir)
        ex.executar()
        self.assertTrue(all(ex.ciclo.reproducao.values()), ex.ciclo.reproducao)
        self.assertEqual([v._sem_comparacao(c) for c in ex.casos], ref['cases'])
        self.assertEqual([c['label'] for c in ex.casos if not c['comparison']['ok']], [])


if __name__ == '__main__':
    unittest.main()
