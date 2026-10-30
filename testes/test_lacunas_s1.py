"""S1's Core gaps (work-cycle searches, path-search blocking, first-fight queries) without a CPU.

- The captures (``validar_lacunas_s1.py --janela <w> --capturar``) are original-only, taken on the S1 trajectory
  itself: every frame of each window was checked against the replay-checked S1 record.
- Each committed native differential is bound to Core's own sources, with 0 mismatches.
- The captures hold no read sets, so they do not replay without a CPU; synthetic checks below pin the
  translations' tables, ring order, list splicing and the sound dependency.
"""
import hashlib
import json
import lzma
from pathlib import Path
import struct
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'ferramentas', RAIZ / 'testes'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

JANELAS = ('a', 'b', 'c')


class EvidenciaOriginal(unittest.TestCase):
    def test_captures_are_original_only_on_the_s1_trajectory(self):
        from validar_lacunas_s1 import JANELAS as FRAMES, captura_padrao
        for j in JANELAS:
            with self.subTest(window=j):
                if not captura_padrao(j).exists():
                    continue                      # window c: capture not run yet (see docs/core/S1_GAPS.md)
                d = json.loads(lzma.decompress(captura_padrao(j).read_bytes()))
                self.assertFalse(d['translation_executed'])
                self.assertEqual(d['frames'], list(FRAMES[j]))
                r = d['reproduction']
                self.assertTrue(r['code_unchanged'])
                self.assertEqual((r['last_frame'], r['frames_checked']), (FRAMES[j][1], FRAMES[j][1] - FRAMES[j][0] + 1))
                self.assertTrue(any(c['kind'] == 'in_situ' for c in d['cases']))


class DiferencialNativo(unittest.TestCase):
    def test_reports_are_bound_to_core_sources_and_have_no_mismatch(self):
        from validar_lacunas_s1 import FONTES, captura_padrao, relatorio_padrao
        for j in JANELAS:
            with self.subTest(window=j):
                if not relatorio_padrao(j).exists():
                    continue                      # native differential not run yet (see docs/core/S1_GAPS.md)
                rel = json.loads(relatorio_padrao(j).read_text())
                self.assertEqual(rel['capture']['sha256'], hashlib.sha256(captura_padrao(j).read_bytes()).hexdigest())
                self.assertEqual(set(rel['source_sha256']), set(FONTES))
                for caminho, sha in rel['source_sha256'].items():
                    self.assertEqual(hashlib.sha256((RAIZ / caminho).read_bytes()).hexdigest(), sha,
                                     f'{caminho} changed since the native differential: rerun validar_lacunas_s1.py')
                self.assertTrue(rel['reproduction']['code_unchanged'])
                self.assertEqual(rel['mismatches'], [])
                self.assertEqual(rel['comparisons'], rel['capture_cases'])
                self.assertTrue(all(r['ok'] and r['native_equals_capture'] for r in rel['cases']))


class Traducoes(unittest.TestCase):
    def _memoria(self, extra=()):
        from test_chamadas_quadro_core import MemoriaEsparsa
        return MemoriaEsparsa(dict(extra))

    def test_crushing_tables(self):
        from buscas_bloqueios import _ecrasable, _peut_ecraser
        self.assertEqual([t for t in range(256) if _peut_ecraser(t)], [0x0c, 0x0f])
        ecrasaveis = [t for t in range(26) if _ecrasable(t)]
        self.assertEqual(ecrasaveis, [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 18, 19, 22])
        self.assertTrue(all(_ecrasable(t) for t in range(0x1a, 256)))

    def test_cherche_veget_ring_order_and_registers(self):
        from buscas_bloqueios import BuscasBloqueios
        grade = 0x10000000
        mem = {0x507d74 + i: (grade >> (8 * i)) & 0xff for i in range(4)}
        mem.update({0x497168: 64, 0x497169: 0, 0x49716a: 64, 0x49716b: 0})
        mem.update({grade + c: 0 for c in range(65536)})
        cel = 20 * 256 + 20
        mem[grade + cel + 2 * 256 - 2] = 0x40       # ring 2, check 1 at i = +2: (y+2, x-2)
        m = self._memoria(mem)
        r = dict(EAX=0xabcd0000 | cel, EBX=0x40, ECX=0x41, EDX=5, ESI=1, EDI=2, EBP=3)
        s = BuscasBloqueios(m).chamar('ChercheVeget', r)
        self.assertEqual(s['EAX'], ((2 << 8) + (0xabcd0000 | cel) - 2) & 0xffffffff)
        self.assertEqual((s['EBX'], s['EDX'], s['ECX'] & 0xff00), (grade + cel + 2 * 256 - 2, 2, 0x4000))
        s = BuscasBloqueios(m).chamar('ChercheVeget', dict(r, EDX=1))
        self.assertEqual((s['EAX'], s['EBX'], s['EDX']), (0xffff, 1, 2))

    def test_task_list_helpers(self):
        from consultas_luta import ConsultasLuta
        lista, base = 0x20000000, 0x20001000
        mem = {}
        for o, v in ((0, 3), (4, 3), (8, 8), (0xc, base)):
            mem.update({lista + o + i: (v >> (8 * i)) & 0xff for i in range(4)})
        for e, prox in ((3, 1), (1, 0), (0, 0xffffffff)):          # 3 -> 1 -> 0
            mem.update({base + 8 * e + i: (prox >> (8 * i)) & 0xff for i in range(4)})
        m = self._memoria(mem)
        c = ConsultasLuta(m)
        r = dict(EAX=lista, EBX=0, ECX=0, EDX=1, ESI=0, EDI=0, EBP=0)
        self.assertEqual(c.chamar('listUnlinkElem', r)['EAX'], 1)
        self.assertEqual((m.u32(base + 24), m.u32(lista + 4)), (0, 2))      # 3 -> 0
        self.assertEqual(c.chamar('listUnlinkElem', r)['EAX'], 0xffffffff)
        self.assertEqual(c.chamar('listDeleteElem', r)['EAX'], 1)
        self.assertEqual((m.u32(lista), m.u32(base + 8), m.u32(lista + 4)), (1, 3, 3))

    def test_voice_needs_its_sound_provider(self):
        from consultas_luta import ConsultasLuta, DependenciaLuta
        with self.assertRaises(DependenciaLuta):
            ConsultasLuta(self._memoria()).chamar('VoixOffAsk', dict(EAX=0, EBX=0, ECX=0, EDX=1, ESI=0, EDI=0, EBP=0))
        pedidos = []
        s = ConsultasLuta(self._memoria(), som=lambda n, r, p: pedidos.append((n, r['EBX'], r['EDX'], p)) or 5) \
            .chamar('VoixOffAsk', dict(EAX=2, EBX=0x77, ECX=0x1100, EDX=5, ESI=0, EDI=0, EBP=0))
        canal = 0x49a0c8 + 2 * 276 + 0x100
        self.assertEqual(pedidos, [('PlaySnd_StopSound', 0, 5, []), ('PlaySnd_PostSound', canal, 0x20100, [0x100])])
        self.assertEqual((s['EAX'], s['EBX'], s['ECX'], s['EDX']), (5, canal, 0x1100, 0x20100))


if __name__ == '__main__':
    unittest.main()
