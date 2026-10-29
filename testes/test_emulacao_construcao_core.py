"""Native differential of the Core construction translations (RISING_EMULAR=1, about 2.5 minutes).

Reruns the accepted MONDE01 display path to frame 1's first ProcessInputGame entry, runs the 153
declared leaf-call cases natively and compares each with ``construcao_core`` over a copy of the exact
case-entry state (``validar_construcao_core.comparar``) and with the committed capture.
"""
import json
import os
from pathlib import Path
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialConstrucaoCore(unittest.TestCase):
    def test_every_declared_case_matches_the_original(self):
        import capturar_construcao_core as ccc
        from validar_construcao_core import CAPTURA, comparar
        por_nome = {c['case']: c for c in json.loads(CAPTURA.read_bytes())['cases']}
        registros = []

        def observador(caso, antes, resultado):
            nativo = dict(resultado, calls=[ccc.chamada_compacta(c) for c in resultado['calls']])
            registros.append(comparar(caso, antes, nativo, por_nome.get(caso['case'])))
        _, casos, _, reproducao, _, _ = ccc.executar('exibicao', observador)
        self.assertTrue(all(reproducao.values()), reproducao)
        self.assertEqual(len(registros), len(por_nome))
        self.assertEqual([r for r in registros if not r['ok']], [])
        self.assertEqual(sorted(r['case'] for r in registros if r['uncertain_bits']),
                         ['move_build_order_at_target', 'move_state3_search'])


if __name__ == '__main__':
    unittest.main()
