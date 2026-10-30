"""Frame-125 lodging minimap (Economy's composition divergence) without a CPU.

- The capture (``validar_minimapa_quadro125.py --capturar``) is original-only, reproduces the display path, equals
  Economy's committed work-cycle record of the call, and holds the declared cases.
- The cause, from the original alone: BatimentModifyMap with DL = 0 (what Economy's composition handed Core) leaves
  196 bytes different from the in-situ DL = 1, the first at 0x47933a26 (the composition's report).
- The committed native differential is bound to the current sources, with 0 mismatches.
- ``provedor_entrada`` refuses a call that omits an argument register the routine depends on.
"""
import hashlib
import json
import lzma
from pathlib import Path
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'ferramentas', RAIZ / 'testes'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
CAPTURA = RAIZ / 'evidencias/minimapa-quadro125/captura-minimapa-quadro125.json.xz'
RELATORIO = RAIZ / 'relatorios/minimapa-quadro125-emulada.json'
_cache = {}


def captura():
    if 'c' not in _cache:
        _cache['c'] = json.loads(lzma.decompress(CAPTURA.read_bytes()))
    return _cache['c']


class EvidenciaOriginal(unittest.TestCase):
    def test_capture_is_original_only_and_reproduces_economys_record(self):
        from validar_minimapa_quadro125 import CASOS
        d = captura()
        self.assertFalse(d['translation_executed'])
        self.assertTrue(all(d['path_reproduction'].values()), d['path_reproduction'])
        self.assertTrue(d['economy_record']['equal'])
        self.assertEqual((d['frame'], d['routine']), (125, 'BatimentLogeEngin'))
        self.assertEqual(set(d['cases']), set(CASOS))
        for nome, (rotina, origem, trocas) in CASOS.items():
            c = d['cases'][nome]
            self.assertEqual((c['routine'], c['snapshot']), (rotina, origem))
            self.assertEqual(c['boundaries'], [])
            esperado = dict(d['snapshot_registers'][origem], **{k: hex(v) for k, v in trocas.items()})
            esperado.pop('ESP')
            self.assertEqual(c['entry_registers'], esperado, nome)
        # the in-situ calls are the ones the original made: DecouvreTerrain(0xa14, 11, 0), IllumineTerrain(0xa14, 8, 0),
        # BatimentModifyMap(1, DL=1)
        r = d['snapshot_registers']
        self.assertEqual([r['DecouvreTerrain'][k] for k in ('EAX', 'EDX', 'EBX')], ['0xa14', '0xb', '0x0'])
        self.assertEqual([r['IllumineTerrain'][k] for k in ('EAX', 'EDX', 'EBX')], ['0xa14', '0x8', '0x0'])
        self.assertEqual([r['BatimentModifyMap'][k] for k in ('EAX', 'EDX')], ['0x1', '0x1'])

    def test_dl0_reproduces_the_composition_divergence_natively(self):
        from validar_minimapa_quadro125 import diferenca
        d = captura()
        dif = diferenca(d['cases']['modify_map_dl0_composition_input'], d['cases']['modify_map_in_situ'])
        self.assertEqual((len(dif), dif[0]), (196, '0x47933a26'))
        self.assertEqual(d['dl0_vs_in_situ'], 196)
        final = {a: n for a, _, n in d['cases']['modify_map_in_situ']['changed_bytes']}
        antes = {a: v for a, v, _ in d['cases']['modify_map_in_situ']['changed_bytes']}
        self.assertEqual((antes['0x47933a26'], final['0x47933a26']), (32, 162))   # the report's 32 -> 162


class DiferencialNativo(unittest.TestCase):
    """Every committed native differential is strictly bound to Core's own files. Economy's bench files are foreign:
    the current ones must equal the files one committed report actually ran, so a new Economy bench version needs a
    native rerun committed here (``validar_minimapa_quadro125.py --bancada-economia``), never a re-pin."""

    def _verificar(self, rel):
        from validar_minimapa_quadro125 import CASOS, FONTES, FONTES_ECONOMIA
        self.assertEqual(rel['capture']['sha256'], hashlib.sha256(CAPTURA.read_bytes()).hexdigest())
        self.assertEqual(set(rel['source_sha256']), set(FONTES))
        for caminho, sha in rel['source_sha256'].items():
            self.assertEqual(hashlib.sha256((RAIZ / caminho).read_bytes()).hexdigest(), sha,
                             f'{caminho} changed since the native differential: rerun validar_minimapa_quadro125.py')
        self.assertEqual(set(rel['economy_source_sha256']), set(FONTES_ECONOMIA))
        self.assertTrue(all(rel['path_reproduction'].values()))
        self.assertTrue(rel['economy_record']['equal'])
        self.assertEqual((rel['comparisons'], rel['mismatches']), (len(CASOS), []))
        self.assertTrue(all(r['ok'] and r['native_equals_capture'] for r in rel['cases']))
        self.assertTrue(all(f['ok'] for f in rel['provider_shapes']))
        self.assertEqual(rel['dl0_vs_in_situ']['bytes'], 196)

    def test_reports_are_bound_to_core_sources_and_have_no_mismatch(self):
        from validar_minimapa_quadro125 import RELATORIOS_VERIFICADOS
        for caminho in RELATORIOS_VERIFICADOS:
            with self.subTest(report=caminho):
                self._verificar(json.loads((RAIZ / caminho).read_text()))

    def test_current_economy_bench_was_run_natively(self):
        from validar_minimapa_quadro125 import FONTES_ECONOMIA, RELATORIOS_VERIFICADOS
        atuais = {c: hashlib.sha256((RAIZ / c).read_bytes()).hexdigest() for c in FONTES_ECONOMIA}
        verificados = [json.loads((RAIZ / c).read_text())['economy_source_sha256'] for c in RELATORIOS_VERIFICADOS]
        self.assertIn(atuais, verificados, 'Economy changed its work-cycle bench: rerun validar_minimapa_quadro125.py '
                      '--bancada-economia <that file> and add the report to RELATORIOS_VERIFICADOS')


class FormasProvedor(unittest.TestCase):
    def _provedor(self):
        from entrada_estruturas import provedor_entrada
        chamadas = []

        class Entrada:
            def chamar(self, nome, regs):
                chamadas.append((nome, dict(regs)))
                return dict(regs)
        return provedor_entrada(Entrada()), chamadas

    def test_missing_behaviour_argument_raises_before_running(self):
        from entrada_estruturas import ArgumentoNaoPassado
        p, chamadas = self._provedor()
        for nome, regs, falta in (('BatimentModifyMap', {'EAX': 1}, ('EDX',)),
                                  ('DecouvreTerrain', {'EAX': 0xa14, 'EDX': 11}, ('EBX',)),
                                  ('IllumineTerrain', {'EAX': 0xa14}, ('EDX', 'EBX')),
                                  ('TerrainEstDecouvert', {'EAX': 5}, ('EDX',))):
            with self.assertRaises(ArgumentoNaoPassado) as ctx:
                p(nome, 0x41fa88, regs)
            self.assertEqual(ctx.exception.registradores, falta)
        self.assertEqual(chamadas, [])

    def test_passed_arguments_and_other_routines_keep_the_contract(self):
        p, chamadas = self._provedor()
        r = p('BatimentModifyMap', 0x41fa88, {'EAX': 1, 'EDX': 1})
        self.assertEqual(chamadas[-1], ('BatimentModifyMap', dict(EAX=1, EBX=0, ECX=0, EDX=1, ESI=0, EDI=0, EBP=0)))
        self.assertEqual(r['_incertos'], {k: 0xffffffff for k in ('EBX', 'ECX', 'ESI', 'EDI', 'EBP')})
        p('EnginGetType', 0x41f99e, {'EAX': 3})       # one argument register: unchanged contract
        self.assertEqual(chamadas[-1][0], 'EnginGetType')


if __name__ == '__main__':
    unittest.main()
