"""M3.1 round 3 (Ctrl deposit mode, help pages 9/0xc/0xb/2/7, the structure under the cursor with troops, their
leaves): CPU-free replay of every captured case.

The replay runs ``validar_paginas_deposito_ia.executar_traducao`` (``entrada_ordens_ia`` with the committed
owners) over a sparse memory holding the case-entry bytes recorded by the native differential
(``evidencias/leituras-paginas-deposito-ia.json.xz``). Every other address is absent, so a translation that
touches an unrecorded byte fails. Each case must reproduce the captured exit registers, changed bytes, boundary
requests and key answers, or stop at the dependency the native differential reported. Core's
``entrada_estruturas`` (EnginSelectPeutEntrer) is not on main yet: ``RISING_NUCLEO_REF`` may name a directory
holding its read-only extraction; without it, the cases whose native run reaches EnginSelectPeutEntrer must stop
at that named dependency.
"""
import json
import os
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
sys.path.insert(0, str(OWNED / 'testes'))
import ambiente_ia_runtime  # noqa: E402,F401
from reinicio_ia import DependenciaIA  # noqa: E402
from test_entrada_ordens_ia import MemoriaEsparsa, _bytes  # noqa: E402

CAPTURA = OWNED / 'evidencias/captura-paginas-deposito-ia.json'
LEITURAS = OWNED / 'evidencias/leituras-paginas-deposito-ia.json.xz'
RELATORIO = OWNED / 'validacao/paginas-deposito-native.json'
if os.environ.get('RISING_NUCLEO_REF'):
    sys.path.append(os.environ['RISING_NUCLEO_REF'])


@unittest.skipUnless(LEITURAS.exists() and RELATORIO.exists(), 'native differential not recorded yet')
class ReplayCasos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import lzma
        from validar_entrada_ordens_ia import comandos_imagem
        cls.captura = json.loads(CAPTURA.read_bytes())
        cls.leituras = json.loads(lzma.decompress(LEITURAS.read_bytes()))
        cls.base = _bytes(cls.leituras['base'])
        cls.relatorio = json.loads(RELATORIO.read_bytes())
        cls.comandos = comandos_imagem()

    def test_report(self):
        self.assertEqual(self.relatorio['mismatches'], [])
        self.assertEqual(self.relatorio['comparisons'], len(self.captura['cases']))
        self.assertEqual(self.leituras['capture']['sha256'], self.relatorio['capture']['sha256'])

    def test_every_case(self):
        from provedores_entrada_ia import entrada_estruturas
        from validar_paginas_deposito_ia import REGISTROS, executar_traducao, texto_so_eax
        from validar_entrada_ordens_ia import comparar_resultado
        dependencias = {d['case']: d['dependency'] for d in self.relatorio['dependency_stops']}
        sem_nucleo = entrada_estruturas(None) is None
        nucleo = {c['case'] for c in self.captura['cases']
                  if any(x.startswith('0|EnginSelectPeutEntrer|') for x in c['calls'])}
        for caso in self.captura['cases']:
            with self.subTest(caso=caso['case']):
                declarado = dict(caso, keys=[[c[1], c[2]] for c in caso['declared_keys_consumed']],
                                 stack=[int(w, 16) for w in caso['stack_words']])
                m = MemoriaEsparsa(_bytes(self.leituras['cases'][caso['case']], dict(self.base)))
                entrada = {k: int(caso['entry_registers'][k], 16) for k in REGISTROS}
                if caso['case'] in dependencias:
                    with self.assertRaises(DependenciaIA) as erro:
                        executar_traducao(m, declarado, entrada, self.leituras['cursor'], self.comandos)
                    self.assertEqual(str(erro.exception), dependencias[caso['case']])
                    continue
                if sem_nucleo and caso['case'] in nucleo:
                    with self.assertRaises(DependenciaIA) as erro:
                        executar_traducao(m, declarado, entrada, self.leituras['cursor'], self.comandos)
                    self.assertIn('EnginSelectPeutEntrer', str(erro.exception))
                    continue
                saida, pedidos, teclas = executar_traducao(m, declarado, entrada, self.leituras['cursor'],
                                                           self.comandos)
                r = comparar_resultado(declarado, texto_so_eax(caso), saida, pedidos, teclas, m.mudancas())
                self.assertTrue(r['ok'], {k: v for k, v in r.items() if k not in ('case', 'routine')})


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'native differential: set RISING_EMULAR=1')
class Nativo(unittest.TestCase):
    def test_native_differential(self):
        import subprocess
        raiz = OWNED.parents[1]
        saida = '.local/entrada/teste-nativo-paginas.json'
        argumentos = [sys.executable, '-B', str(OWNED / 'validar_paginas_deposito_ia.py'), '--saida', saida]
        nucleo = os.environ.get('RISING_NUCLEO_REF')
        if nucleo:
            argumentos += ['--nucleo-ref', nucleo]
        p = subprocess.run(argumentos, cwd=raiz, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-2000:] + p.stderr[-2000:])
        r = json.loads((raiz / saida).read_bytes())
        self.assertEqual((r['mismatches'], r['comparisons']), ([], len(json.loads(CAPTURA.read_bytes())['cases'])))


if __name__ == '__main__':
    unittest.main()
