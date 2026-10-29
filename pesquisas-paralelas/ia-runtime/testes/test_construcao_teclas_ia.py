"""M3.1 round 2 (state 11, construction progress, keys): CPU-free replay of every captured case.

The replay runs ``validar_construcao_teclas_ia.executar_traducao`` (``construcao_entrada_ia`` and
``entrada_ordens_ia`` with the committed owners) over a sparse memory holding the case-entry bytes recorded by the
native differential (``evidencias/leituras-construcao-teclas-ia.json.xz``). Every other address is absent, so a
translation that touches an unrecorded byte fails. Each case must reproduce the captured exit registers, changed
bytes, sound requests and key answers, or stop at the dependency the native differential reported. Without Core's
``construcao_core`` on the import path, the cases whose native run reaches DeplaceEngin or BatimentConstructible
must stop at a named dependency.
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

CAPTURA = OWNED / 'evidencias/captura-construcao-teclas-ia.json'
LEITURAS = OWNED / 'evidencias/leituras-construcao-teclas-ia.json.xz'
RELATORIO = OWNED / 'validacao/construcao-teclas-native.json'


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
        from provedores_entrada_ia import construcao_core
        from validar_construcao_teclas_ia import REGISTROS, executar_traducao
        from validar_entrada_ordens_ia import comparar_resultado
        dependencias = {d['case']: d['dependency'] for d in self.relatorio['dependency_stops']}
        sem_nucleo = construcao_core(None) is None
        nucleo = {c['case'] for c in self.captura['cases']
                  if any(f'|{n}|' in x for x in c['calls'] for n in ('DeplaceEngin', 'BatimentConstructible'))}
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
                    with self.assertRaises(DependenciaIA):
                        executar_traducao(m, declarado, entrada, self.leituras['cursor'], self.comandos)
                    continue
                saida, pedidos, teclas = executar_traducao(m, declarado, entrada, self.leituras['cursor'],
                                                           self.comandos)
                r = comparar_resultado(declarado, caso, saida, pedidos, teclas, m.mudancas())
                self.assertTrue(r['ok'], {k: v for k, v in r.items() if k not in ('case', 'routine')})


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'native differential: set RISING_EMULAR=1')
class Nativo(unittest.TestCase):
    def test_native_differential(self):
        import subprocess
        raiz = OWNED.parents[1]
        saida = '.local/entrada/teste-nativo-construcao.json'
        argumentos = [sys.executable, '-B', str(OWNED / 'validar_construcao_teclas_ia.py'), '--saida', saida]
        nucleo = os.environ.get('RISING_NUCLEO_REF')
        if nucleo:
            argumentos += ['--nucleo-ref', nucleo]
        p = subprocess.run(argumentos, cwd=raiz, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-2000:] + p.stderr[-2000:])
        r = json.loads((raiz / saida).read_bytes())
        self.assertEqual((r['mismatches'], r['comparisons']), ([], len(json.loads(CAPTURA.read_bytes())['cases'])))


if __name__ == '__main__':
    unittest.main()
