"""Native differential of the frame-125 lodging discovery, light and structure minimap (RISING_EMULAR=1, ~3 min).

Reruns Economy's work-cycle bench to frame 125's BatimentLogeEngin, runs the declared cases natively from the
snapshots of the call's DecouvreTerrain/IllumineTerrain/BatimentModifyMap entries and compares each with Core's
``entrada_estruturas`` over a copy of the exact entry state (``validar_minimapa_quadro125``).
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
class DiferencialMinimapaQuadro125(unittest.TestCase):
    def test_every_case_matches_the_original(self):
        import validar_minimapa_quadro125 as v
        captura = json.loads(lzma.decompress(v.CAPTURA.read_bytes()))
        registro, snapshots, casos, reproducao, _ = v.executar_nativo()
        self.assertTrue(all(reproducao.values()), reproducao)
        self.assertTrue(v.comparar_economia(registro)['equal'])
        self.assertEqual(casos, captura['cases'])
        falhas = [n for n, c in casos.items()
                  if not v.comparar_caso(n, c, v._sem_pilha(snapshots[v.CASOS[n][1]][1]))['ok']]
        self.assertEqual(falhas, [])
        self.assertTrue(all(f['ok'] for f in v.comparar_formas_provedor(casos, snapshots)))


if __name__ == '__main__':
    unittest.main()
