"""Cave structure body, habitation and sanctuary recruitment over the original-first multi-frame capture.

- The capture is original-only, reproduces the display reference's frames 0/1 and leaves the code unchanged; its
  listings are the intact bytes.
- MONDE01 facts shown natively: the cave body runs on the 0xc8 cave (no colonist: BagContient only), the colonist's
  lodging hands it to player 0 (InitBatimentPlayer: cave count 0 -> 1), the sanctuary recruits one unit at a time
  for its food cost, and each completion converts one colonist.
- Every recorded call of a translated routine replays without a CPU from the bytes the original read before
  writing: exit registers, the final value of every changed byte, and each call into another front (name and
  argument bits). Deliberate mutations are caught; named dependencies raise instead of defaulting.
- The committed native differential is bound to the current translation.
- RISING_EMULAR=1 reruns the native differential (about 10 minutes).
"""
import hashlib
import json
import lzma
import os
from pathlib import Path
import struct
import subprocess
import sys
import unittest
from unittest import mock

PASTA = Path(__file__).resolve().parents[1]
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import caverna_recrutamento as cr  # noqa: E402
import replay_caverna_recrutamento as rp  # noqa: E402
from validar_caverna_recrutamento import CAPTURA  # noqa: E402

RELATORIO = PASTA / 'validacao-caverna-recrutamento-emulada.json'
_CAP = {}


def captura():
    if 'c' not in _CAP:
        _CAP['c'] = json.loads(lzma.decompress(CAPTURA.read_bytes()))
    return _CAP['c']


def comida(quadro):
    return struct.unpack_from('<H', bytes.fromhex(quadro['resources_p0']), 8 + 2)[0]


class Captura(unittest.TestCase):
    def test_original_only_and_reproduced(self):
        c = captura()
        self.assertFalse(c['translation_executed'])
        self.assertEqual(c['reproduction'], dict(load_tail=True, between_frames=True, frame1=True, code_unchanged=True))
        self.assertEqual(c['original_sha256'], '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')

    def test_listings_are_the_intact_bytes(self):
        from extrair_ordens_economia import ler_pe
        try:
            ler = ler_pe()
        except (OSError, ValueError):
            self.skipTest('original executable not available')
        manifesto = json.loads((PASTA / 'evidencias/caverna-recrutamento/manifesto.json').read_text())
        for t in manifesto['intervals']:
            a, b = int(t['start'], 16), int(t['end_exclusive'], 16)
            self.assertEqual(hashlib.sha256(ler(a, b - a)).hexdigest(), t['sha256'], t['name'])

    def test_cave_and_recruitment_facts(self):
        c = captura()
        cave = str(c['cave'])
        q = c['frames']
        self.assertEqual(q[0]['structures'][cave]['owner'], 0xc8)
        corpos = [r for r in c['calls'] if r['routine'] == 'BatimentNextEtape' and r.get('action') is None]
        sem_colono = [r for r in corpos if r['frame'] < 100]
        self.assertTrue(sem_colono)
        for r in sem_colono:       # the uninhabited cave: one BagContient, nothing written
            self.assertEqual([x[1] for x in r['calls']], ['BagContient'])
            self.assertEqual(r['changed_bytes'], [])
        dono = next(f for f in q if f['structures'][cave]['owner'] == 0)
        self.assertEqual(dono['cave_words_p0'][:4], '0100')
        # Recruitment: each completion leaves the request cleared and one colonist fewer in the sanctuary.
        self.assertGreaterEqual(len(c['recruit_completions']), 3)
        inicios = [r for r in c['calls'] if r['routine'] == 'InitRecruteTroupe' and r.get('action', '').startswith('tag 17')]
        aceitos = [r for r in inicios if int(r['exit_registers']['EAX'], 16) & 0xff == 1]
        self.assertGreaterEqual(len(aceitos), 4)


class Replay(unittest.TestCase):
    def test_every_translated_call_replays(self):
        contagem, falhas = rp.replay(captura())
        self.assertEqual(falhas, [], json.dumps(falhas[:5], indent=1))
        self.assertGreater(sum(c['match'] for c in contagem.values()), 0)

    def test_mutations_are_detected(self):
        c = captura()
        alvos = {}
        for r in c['calls']:
            alvos.setdefault(r['routine'], r)

        class CorpoSemLimite(cr.CavernaRecrutamento):
            def corpo_caverna(self, estrutura):
                e = self._est(estrutura)
                if self.m.u8(e + 0x75) and self.m.u8(e + 0x76) >= 15:
                    self.m.u8(e + 0x76, 16)
                return super().corpo_caverna(estrutura)

        class NivelErrado(cr.CavernaRecrutamento):
            def _nivel(self, p, rotina, endereco):
                saida = super()._nivel(p, rotina, endereco)
                self.m.u8(cr.INDICADOR + 6 * p + 4, saida[0] + 1)
                return saida

        class RecrutaSemPendencia(cr.CavernaRecrutamento):
            def _InitRecruteTroupe(self, regs):
                saida = super()._InitRecruteTroupe(regs)
                p = regs['EDX'] & 0xff
                e = self._est(self.m.u16(cr.SELECOES_ESTRUTURA + 2 * p))
                if saida['EAX'] & 0xff:
                    self.m.u8(e + 0x74, 0)
                return saida

        class TempoErrado(cr.CavernaRecrutamento):
            def _EnginGetTimeRecrute(self, regs):
                saida = super()._EnginGetTimeRecrute(regs)
                return dict(saida, EAX=saida['EAX'] + 1)

        for cls, rotina in ((NivelErrado, 'InitBatimentPlayer'), (RecrutaSemPendencia, 'InitRecruteTroupe'),
                            (TempoErrado, 'CalculTroupe')):
            casos = [r for r in c['calls'] if r['routine'] == rotina]
            resultados = {rp.replay_chamada(r, cls)[0] for r in casos}
            self.assertIn('mismatch', resultados | ({'mismatch'} if 'error' in resultados else set()), (cls, rotina))
        # The case +0x75 = 1, +0x76 = 15 with bit 0 of 0x508f80 clear: the counter stays at its limit (EAX = 15).
        limite = [r for r in c['calls'] if r['routine'] == 'BatimentNextEtape' and r.get('action')
                  and int(r['exit_registers']['EAX'], 16) == 15]
        self.assertTrue(limite)
        self.assertEqual(rp.replay_chamada(limite[0], CorpoSemLimite)[0], 'mismatch')

    def test_dependencies_raise(self):
        r = next(r for r in captura()['calls'] if r['routine'] == 'BatimentNextEtape')
        m = rp.MemoriaEsparsa(r['read_before_write'])
        regs = {k: int(v, 16) for k, v in r['entry_registers'].items()}
        with self.assertRaises(cr.DependenciaCavernaRecrutamento) as ctx:
            cr.CavernaRecrutamento(m)._BatimentNextEtape(regs)
        self.assertEqual((ctx.exception.rotina, ctx.exception.chamada), ('BagContient', 0x426b8d))


class Relatorio(unittest.TestCase):
    def test_native_report_bound_to_translation(self):
        rel = json.loads(RELATORIO.read_text())
        self.assertEqual(rel['translation'], hashlib.sha256((PASTA / 'caverna_recrutamento.py').read_bytes()).hexdigest())
        self.assertEqual((rel['mismatches'], rel['errors']), (0, 0))
        self.assertTrue(rel['rerun_equals_capture'])

    @unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'native differential (RISING_EMULAR=1)')
    def test_native_differential(self):
        saida = RAIZ / '.local/caverna/validacao-teste.json'
        saida.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run([sys.executable, '-B', str(PASTA / 'validar_caverna_recrutamento.py'),
                            '--captura', str(CAPTURA.relative_to(RAIZ)), '--saida', str(saida.relative_to(RAIZ))],
                           cwd=RAIZ, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-2000:])


if __name__ == '__main__':
    unittest.main()
