"""Native differential of the selection and order-setter translations (RISING_EMULAR=1, about 2 minutes).

Reruns the accepted MONDE01 display path to frame 1's first ProcessInputGame entry, runs the 130
declared leaf-call cases natively and compares each with ``selecao_ordens`` over a copy of the
exact case-entry state (``validar_selecao_ordens.comparar``) and with the committed capture.
"""
import json
import os
from pathlib import Path
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialSelecaoOrdens(unittest.TestCase):
    def test_every_declared_case_matches_the_original(self):
        import capturar_selecao_ordens as cso
        from validar_selecao_ordens import CAPTURA, comparar
        por_nome = {c['case']: c for c in json.loads(CAPTURA.read_bytes())['cases']}
        registros = []

        def observador(caso, antes, resultado):
            nativo = dict(resultado, calls=[cso.chamada_compacta(c) for c in resultado['calls']])
            registros.append(comparar(caso, antes, nativo, por_nome.get(caso['case'])))
        _, casos, _, reproducao, _, _ = cso.executar('exibicao', observador)
        self.assertTrue(all(reproducao.values()), reproducao)
        self.assertEqual(len(registros), len(por_nome))
        self.assertEqual([r for r in registros if not r['ok']], [])


if __name__ == '__main__':
    unittest.main()
