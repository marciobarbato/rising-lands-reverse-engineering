"""Core structure-entry, lodging and Bag translations without a CPU (M3/M4 groundwork).

- The committed native differential (505 measured steps, whole touched state) is bound to the current sources:
  editing the translation or the harness requires rerunning ``validar_entrada_estruturas.py``.
- Every captured step whose routine does not run on M2.3's live world replays exactly from the bytes the original
  read before writing (``leituras-entrada-estruturas-exibicao.json.xz``, written by that native run): registers
  EAX..EBP (except the declared uncertain bits) and every changed byte, and the translation reads no byte the
  original did not read. Deliberate mutations are caught.
- The steps on the live world (``NATIVAS``: the world is built from pointers the original never reads) stay with the
  native differential (``test_emulacao_entrada_estruturas``).
"""
import hashlib
import json
import lzma
from pathlib import Path
import sys
import unittest
from unittest import mock

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'ferramentas', RAIZ / 'testes'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
PASTA = RAIZ / 'evidencias/entrada-estruturas'
CAPTURA = PASTA / 'captura-entrada-estruturas-exibicao.json.xz'
LEITURAS = PASTA / 'leituras-entrada-estruturas-exibicao.json.xz'
RELATORIO = RAIZ / 'relatorios/entrada-estruturas-emulada.json'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
M32 = 0xffffffff
NATIVAS = frozenset(('RetireEngin', 'SetDeplaceEngin', 'EnginPeutPasser', 'DecouvreTerrain', 'IllumineTerrain',
                     'BatimentModifyMap', 'CalculEntreBatiment', 'EnginNextEtape:state13', 'BatimentRetireColon'))
_cache = {}


def capturados():
    if 'c' not in _cache:
        _cache['c'] = json.loads(lzma.decompress(CAPTURA.read_bytes()))['cases']
    return _cache['c']


def leituras():
    if 'l' not in _cache:
        _cache['l'] = json.loads(lzma.decompress(LEITURAS.read_bytes()))['cases']
    return _cache['l']


def replay(teste, caso):
    from entrada_estruturas import EntradaEstruturas
    from test_visao_grupos import memoria_replay
    m = memoria_replay(leituras()[caso['case']])
    pedidos = []

    def som(nome, regs, pilha):
        pedidos.append(nome)
        return regs['EAX']

    def externo(nome, chamada, regs):
        raise AssertionError(f'{caso["case"]}: other front callee {nome} at {chamada:#x}')
    entrada = {k: int(caso['entry_registers'][k], 16) for k in REGISTROS}
    saida = EntradaEstruturas(m, externo=externo, som=som).chamar(caso['routine'], entrada)
    incertos = saida.get('_incertos') or {}
    teste.assertEqual({k: hex(saida[k] & ~incertos.get(k, 0) & M32) for k in REGISTROS},
                      {k: hex(int(caso['exit_registers'][k], 16) & ~incertos.get(k, 0) & M32) for k in REGISTROS})
    m.conferir(teste, caso['changed_bytes'])
    teste.assertEqual(pedidos, [b['routine'] for b in caso['boundaries']])


class DiferencialNativoComprometido(unittest.TestCase):
    def test_report_has_no_mismatch_and_is_bound_to_the_current_sources(self):
        r = json.loads(RELATORIO.read_bytes())
        self.assertEqual(r['mismatches'], [])
        self.assertEqual(r['comparisons'], len(capturados()))
        self.assertTrue(all(r['path_reproduction'].values()))
        self.assertEqual(r['capture']['sha256'], hashlib.sha256(CAPTURA.read_bytes()).hexdigest())
        for caminho, h in r['source_sha256'].items():
            self.assertEqual(hashlib.sha256((RAIZ / caminho).read_bytes()).hexdigest(), h,
                             f'{caminho} changed since the native differential: rerun validar_entrada_estruturas.py')

    def test_capture_is_original_only(self):
        d = json.loads(lzma.decompress(CAPTURA.read_bytes()))
        self.assertFalse(d['translation_executed'])
        self.assertTrue(all(d['path_reproduction'].values()))
        self.assertEqual(len(d['cases']), 505)
        self.assertEqual(set(leituras()), {c['case'] for c in d['cases']})


class ReplaySemCPU(unittest.TestCase):
    def test_every_step_off_the_live_world_replays_exactly(self):
        replayed = {}
        for caso in capturados():
            if caso['routine'] in NATIVAS:
                continue
            with self.subTest(case=caso['case']):
                replay(self, caso)
                replayed[caso['routine']] = replayed.get(caso['routine'], 0) + 1
        self.assertEqual(sum(replayed.values()), 340)
        self.assertEqual(replayed['EnginSelectPeutEntrer'], 111)
        self.assertEqual(replayed['SetEnginSelectRentreBatiment'], 30)

    def test_deliberate_mutations_are_detected(self):
        import entrada_estruturas as ee
        por_nome = {c['case']: c for c in capturados()}
        mutacoes = (('troupe_quad_types', mock.patch.object(ee, 'NAO_TROPAS', frozenset((3,)))),
                    ('select_rentre_colonist_cave', mock.patch.object(ee, 'SELECOES', ee.SELECOES + 2)),
                    ('placelibre_type8_limit', mock.patch.object(ee, 'LIMITE_CASERNA', ee.LIMITE_HOSPITAL)))
        for nome, mutacao in mutacoes:
            with self.subTest(case=nome), mutacao, self.assertRaises((AssertionError, LookupError)):
                replay(self, por_nome[nome])


if __name__ == '__main__':
    unittest.main()
