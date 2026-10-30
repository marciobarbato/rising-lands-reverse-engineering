"""EnginSetFatigue, ChercheVegetLibre, ChercheTypeBatimentProximite and EteintTerrain without a CPU.

- The captures (``validar_fadiga_vegetacao.py --capturar``) are original-only, reproduce the display path and hold
  the real call sites: EnginSetFatigue (Economy's declared hunger, units 12 and 14), SortieTroupe's EteintTerrain at
  0x421116 (radius 10) and AvanceEngin's.
- The committed native differentials are bound to Core's own sources, with 0 mismatches and no uncertain bits.
  Economy's bench/scenario files are foreign: a report records the versions it ran, informational only.
- ``provedor_fadiga`` refuses a call that omits an argument register or ChercheVegetLibre's pushed unit.
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
CENARIOS = ('fome', 'abandono')
_cache = {}


def captura(cenario):
    if cenario not in _cache:
        from validar_fadiga_vegetacao import captura_padrao
        _cache[cenario] = json.loads(lzma.decompress(captura_padrao(cenario).read_bytes()))
    return _cache[cenario]


class EvidenciaOriginal(unittest.TestCase):
    def test_captures_are_original_only_and_reproduce_the_path(self):
        for cenario in CENARIOS:
            d = captura(cenario)
            self.assertFalse(d['translation_executed'])
            self.assertEqual(d['scenario'], cenario)
            self.assertTrue(all(d['path_reproduction'].values()), d['path_reproduction'])
            for c in d['cases']:
                self.assertIn(c['kind'], ('in_situ', 'variant'))

    def test_hunger_call_sites(self):
        fome = captura('fome')['cases']
        fadiga = [c for c in fome if c['routine'] == 'EnginSetFatigue' and c['kind'] == 'in_situ']
        self.assertEqual({int(c['entry_registers']['EAX'], 16) & 0xffff for c in fadiga}, {12, 14})
        for c in fadiga:
            self.assertEqual(c['caller_return'], '0x454994')               # EnginNextEtape 0x45498f
        # the entering calls (unit 12 at 1100, unit 14 later) find a sack; the repeats return at state 19 (EAX 0x13)
        entradas = [c for c in fadiga if c['changed_bytes']]
        self.assertEqual([int(c['entry_registers']['EAX'], 16) & 0xffff for c in entradas], [12, 14])
        self.assertEqual(entradas[0]['frame'], 1100)
        self.assertTrue(all(c['exit_registers']['EAX'] == '0x13' for c in fadiga if not c['changed_bytes']))
        # the nested food search is ChercheVegetLibre(cell, 20, 0x43, 0x43, push unit)
        cvl = [c for c in fome if c['label'] == 'ChercheVegetLibre: in situ']
        self.assertEqual(len(cvl), 2)
        for c in cvl:
            self.assertEqual([c['entry_registers'][k] for k in ('EDX', 'EBX', 'ECX')], ['0x14', '0x43', '0x43'])

    def test_abandonment_call_site(self):
        sortie = [c for c in captura('abandono')['cases']
                  if c['routine'] == 'EteintTerrain' and c['kind'] == 'in_situ' and c['caller_return'] == '0x42111b']
        self.assertEqual(len(sortie), 1)
        self.assertEqual(int(sortie[0]['entry_registers']['EDX'], 16) & 0xffff, 10)   # the sanctuary's radius
        self.assertTrue(sortie[0]['changed_bytes'])


class DiferencialNativo(unittest.TestCase):
    def test_reports_are_bound_to_core_sources_and_have_no_mismatch(self):
        from validar_fadiga_vegetacao import FONTES, captura_padrao, relatorio_padrao
        for cenario in CENARIOS:
            with self.subTest(cenario=cenario):
                rel = json.loads(relatorio_padrao(cenario).read_text())
                cap = captura_padrao(cenario)
                self.assertEqual(rel['capture']['sha256'], hashlib.sha256(cap.read_bytes()).hexdigest())
                self.assertEqual(set(rel['source_sha256']), set(FONTES))
                for caminho, sha in rel['source_sha256'].items():
                    self.assertEqual(hashlib.sha256((RAIZ / caminho).read_bytes()).hexdigest(), sha,
                                     f'{caminho} changed since the native differential: rerun validar_fadiga_vegetacao')
                self.assertTrue(all(rel['path_reproduction'].values()))
                self.assertEqual(rel['mismatches'], [])
                self.assertEqual(rel['comparisons'], rel['capture_cases'])
                self.assertEqual(rel['comparisons'], len(captura(cenario)['cases']))
                for r in rel['cases']:
                    self.assertTrue(r['ok'] and r['native_equals_capture'], r['label'])
                    self.assertEqual(r['uncertain_bits'], {}, r['label'])

    def test_economy_sources_are_recorded_not_pinned(self):
        """Economy's bench/scenario files are foreign: the report records which versions ran (informational), and
        only Core's files bind it, so an Economy change never blocks either front's gate."""
        from validar_fadiga_vegetacao import relatorio_padrao
        for cenario in CENARIOS:
            rel = json.loads(relatorio_padrao(cenario).read_text())
            self.assertIn('bancada_ciclo_trabalho', rel['economy_sources'])
            self.assertTrue(all(len(v['sha256']) == 64 for v in rel['economy_sources'].values()))


class FormasProvedor(unittest.TestCase):
    def _provedor(self):
        from fadiga_vegetacao import provedor_fadiga
        chamadas = []

        class Falsa:
            def chamar(self, nome, regs, pilha=()):
                chamadas.append((nome, dict(regs), list(pilha)))
                return dict(regs)
        return provedor_fadiga(Falsa()), chamadas

    def test_missing_arguments_raise_before_running(self):
        from entrada_estruturas import ArgumentoNaoPassado
        p, chamadas = self._provedor()
        for nome, regs, falta in (
                ('ChercheVegetLibre', {'EAX': 0x1010, 'EDX': 20, 'EBX': 0x43, '_pilha': [12]}, ('ECX',)),
                ('ChercheVegetLibre', {'EAX': 0x1010, 'EDX': 20, 'EBX': 0x43, 'ECX': 0x43}, ('_pilha',)),
                ('EteintTerrain', {'EAX': 0x1010, 'EDX': 10}, ('EBX',)),
                ('ChercheTypeBatimentProximite', {'EAX': 0x1010, 'EDX': 40, 'EBX': 3}, ('ECX',)),
                ('EnginSetFatigue', {}, ('EAX',))):
            with self.assertRaises(ArgumentoNaoPassado) as ctx:
                p(nome, 0x421116, regs)
            self.assertEqual(ctx.exception.registradores, falta)
        self.assertEqual(chamadas, [])

    def test_unchanged_missing_registers_come_back_uncertain(self):
        p, chamadas = self._provedor()
        r = p('EteintTerrain', 0x421116, {'EAX': 0x1010, 'EDX': 10, 'EBX': 0})
        self.assertEqual(chamadas[-1], ('EteintTerrain', dict(EAX=0x1010, EBX=0, ECX=0, EDX=10, ESI=0, EDI=0, EBP=0),
                                        []))
        self.assertEqual(r['_incertos'], {k: 0xffffffff for k in ('ECX', 'ESI', 'EDI', 'EBP')})
        p('ChercheVegetLibre', 0x455756, {'EAX': 1, 'EDX': 2, 'EBX': 3, 'ECX': 4, '_pilha': [12], 'ESP': 0x2000f00})
        self.assertEqual(chamadas[-1][2], [12])
        self.assertEqual(chamadas[-1][1]['ESP'], 0x2000f00)


if __name__ == '__main__':
    unittest.main()
