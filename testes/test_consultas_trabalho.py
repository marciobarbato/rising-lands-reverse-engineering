"""TerrainEstGc and SetMiniMap at CalculWorkEngin's calls without a CPU; ``chamar_som``'s call address.

- The capture (``validar_consultas_trabalho.py --capturar``) is original-only and holds the real calls: TerrainEstGc
  at 0x44d8cd (object >= 0x1d) and SetMiniMap mode 4 at 0x44c437 (the builder leaving its mine).
- The committed native differential is bound to Core's own sources, with 0 mismatches.
- ``provedores_core`` serves TerrainEstGc; the flat translation covers every object byte.
- ``chamar_som`` passes the call address to providers that declare ``chamada`` and keeps three-argument ones working.
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


class EvidenciaOriginal(unittest.TestCase):
    def test_capture_holds_the_real_calls(self):
        from validar_consultas_trabalho import CAPTURA
        d = json.loads(lzma.decompress(CAPTURA.read_bytes()))
        self.assertFalse(d['translation_executed'])
        self.assertTrue(all(d['path_reproduction'].values()))
        situ = [c for c in d['cases'] if c['kind'] == 'in_situ']
        gc = [c for c in situ if c['routine'] == 'TerrainEstGc']
        self.assertTrue(gc and all(c['caller_return'] == '0x44d8d2' and c['exit_registers']['EAX'] == '0x1' for c in gc))
        mm = [c for c in situ if c['caller_return'] == '0x44c43c']
        self.assertEqual(len(mm), 1)
        self.assertEqual((mm[0]['frame'], mm[0]['entry_registers']['EDX'], mm[0]['entry_registers']['EAX']),
                         (572, '0x4', '0x0'))


class DiferencialNativo(unittest.TestCase):
    def test_report_is_bound_to_core_sources_and_has_no_mismatch(self):
        from validar_consultas_trabalho import CAPTURA, FONTES, RELATORIO
        rel = json.loads(RELATORIO.read_text())
        self.assertEqual(rel['capture']['sha256'], hashlib.sha256(CAPTURA.read_bytes()).hexdigest())
        self.assertEqual(set(rel['source_sha256']), set(FONTES))
        for caminho, sha in rel['source_sha256'].items():
            self.assertEqual(hashlib.sha256((RAIZ / caminho).read_bytes()).hexdigest(), sha,
                             f'{caminho} changed since the native differential: rerun validar_consultas_trabalho.py')
        self.assertTrue(all(rel['path_reproduction'].values()))
        self.assertEqual(rel['mismatches'], [])
        self.assertEqual(rel['comparisons'], rel['capture_cases'])
        self.assertTrue(all(r['ok'] and r['native_equals_capture'] for r in rel['cases']))


class Traducoes(unittest.TestCase):
    def test_terrain_est_gc_and_its_provider(self):
        from chamadas_quadro_core import provedores_core
        from incursao_core import terreno_esta_gc
        from test_chamadas_quadro_core import MemoriaEsparsa
        grade = 0x10000000
        m = MemoriaEsparsa({**{0x507d74 + i: (grade >> (8 * i)) & 0xff for i in range(4)},
                            **{grade + o: o for o in range(256)}})
        for o in range(256):
            self.assertEqual(terreno_esta_gc(m, 0xabcd0000 | o), dict(EAX=int(0x1d <= o <= 0x34)))
        self.assertEqual(provedores_core(m)['TerrainEstGc'](sitio=0x44d8cd, caso=0x30), 1)


class Som(unittest.TestCase):
    def test_call_address_only_for_providers_that_declare_it(self):
        from selecao_ordens import chamar_som
        vistos = []

        def antigo(nome, regs, pilha):
            vistos.append((nome, pilha))
            return 7

        def novo(nome, regs, pilha, chamada=None):
            vistos.append((nome, pilha, chamada))
            return 8

        def livre(nome, regs, pilha, **extra):
            vistos.append((nome, extra))
            return 9
        regs = dict(EAX=0x50, EDX=0, EBX=0, ECX=0)
        self.assertEqual(chamar_som(antigo, 'PlaySnd_PostSound', regs, [1], 0x440de7), 7)
        self.assertEqual(chamar_som(novo, 'PlaySnd_PostSound', regs, [1], 0x440de7), 8)
        self.assertEqual(chamar_som(livre, 'PlaySnd_StopSound', regs, [], 0x4728e4), 9)
        self.assertEqual(vistos, [('PlaySnd_PostSound', [1]), ('PlaySnd_PostSound', [1], 0x440de7),
                                  ('PlaySnd_StopSound', {'chamada': 0x4728e4})])


if __name__ == '__main__':
    unittest.main()
