"""Hunger state (unit state 19) over its original-first capture.

- The capture is original-only, reproduces the display reference's frames 0/1 and leaves the code unchanged.
- MONDE01 facts shown natively: after the declared hunger, units 12 and 14 walk to a food sack, eat it
  (TerrainRetireMatiere, provisions refilled to +0x76), and EnginRestaureEtat sends them back to work.
- Every recorded state-19 body replays without a CPU from the bytes the original read before writing. Deliberate
  mutations are caught; named dependencies raise instead of defaulting.
- The committed native differential is bound to the current translation.
"""
import hashlib
import json
import lzma
from pathlib import Path
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import alimentacao as al  # noqa: E402
import replay_alimentacao as rp  # noqa: E402
from validar_alimentacao import CAPTURA  # noqa: E402

RELATORIO = PASTA / 'validacao-alimentacao-emulada.json'
_CAP = {}


def captura():
    if 'c' not in _CAP:
        _CAP['c'] = json.loads(lzma.decompress(CAPTURA.read_bytes()))
    return _CAP['c']


def corpos():
    return [r for r in captura()['calls'] if r['routine'] == 'EnginNextEtape:19']


class Captura(unittest.TestCase):
    def test_original_only_and_reproduced(self):
        c = captura()
        self.assertFalse(c['translation_executed'])
        self.assertEqual(c['reproduction'], dict(load_tail=True, between_frames=True, frame1=True, code_unchanged=True))
        self.assertEqual(c['original_sha256'], '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')

    def test_both_units_eat_a_sack_and_go_back_to_work(self):
        comidas = [r for r in corpos() if 'TerrainRetireMatiere' in [x[1] for x in r['calls']]]
        self.assertEqual(sorted(int(r['entry_registers']['EDI'], 16) & 0xffff for r in comidas), [12, 14])
        for r in comidas:
            nomes = [x[1] for x in r['calls'] if x[0] == 0]
            self.assertEqual(nomes[-1], 'EnginRestaureEtat')
        ultimo = captura()['frames'][-1]['units']
        for u in ('12', '14'):
            self.assertEqual((ultimo[u]['state'], ultimo[u]['provisions']), (5, 4))


class Replay(unittest.TestCase):
    def test_every_state19_body_replays(self):
        contagem, falhas = rp.replay(captura())
        self.assertEqual(falhas, [], json.dumps(falhas[:5], indent=1))
        self.assertEqual(contagem['EnginNextEtape:19']['match'], len(corpos()))

    def test_mutations_are_detected(self):
        comidas = [r for r in corpos() if 'TerrainRetireMatiere' in [x[1] for x in r['calls']]]
        andando = [r for r in corpos() if [x[1] for x in r['calls'] if x[0] == 0][-1:] == ['DeplaceEngin']][:20]

        class SemReabastecer(al.Alimentacao):
            def _reabastecer(self, r, esi, di, cave=False):
                super()._reabastecer(r, esi, di, cave)
                self.m.u16(esi + 4, 0)

        class SacoErrado(al.Alimentacao):
            def _TerrainRetireMatiere(self, regs):
                saida = super()._TerrainRetireMatiere(regs)
                c = regs['EAX'] & 0xffff
                q = self.m.u32(al.GRADE_TRABALHO) + c
                self.m.u8(q, self.m.u8(q) + 1)
                return saida

        class ChegadaErrada(al.Alimentacao):
            """A walking unit treated as arrived (destination := its cell)."""
            def _refeicao(self, r, esi, di):
                self.m.u16(esi + 0x7e, self.m.u16(esi + 8))
                return super()._refeicao(r, esi, di)

        for cls, casos in ((SemReabastecer, comidas), (SacoErrado, comidas), (ChegadaErrada, andando)):
            resultados = {rp.replay_chamada(r, cls)[0] for r in casos}
            self.assertTrue(resultados & {'mismatch', 'error'}, cls.__name__)

    def test_dependencies_raise(self):
        r = corpos()[0]
        m = rp.MemoriaEsparsa(r['read_before_write'])
        regs = {k: int(v, 16) for k, v in r['entry_registers'].items()}
        with self.assertRaises(al.DependenciaFome) as ctx:
            al.Alimentacao(m).chamar('EnginNextEtape:19', regs)
        self.assertEqual(ctx.exception.chamada, 0x4550e8)

    def test_saved_states_outside_the_domain_raise_before_any_store(self):
        r = corpos()[0]
        m = rp.MemoriaEsparsa(r['read_before_write'])
        regs = {k: int(v, 16) for k, v in r['entry_registers'].items()}
        m.bytes[regs['ESI'] + 0xa0], m.bytes[regs['ESI'] + 0xa1] = 0x12, 0
        with self.assertRaises(al.ForaDoDominioFome) as ctx:
            al.Alimentacao(m).chamar('EnginNextEtape:19', regs)
        self.assertEqual(ctx.exception.endereco, 0x454fad)
        self.assertEqual(m.escritos, {})


class Relatorio(unittest.TestCase):
    def test_native_report_bound_to_translation(self):
        rel = json.loads(RELATORIO.read_text())
        self.assertEqual(rel['translation'], hashlib.sha256((PASTA / 'alimentacao.py').read_bytes()).hexdigest())
        self.assertEqual((rel['mismatches'], rel['errors'], rel['outside_domain']), (0, 0, 0))
        self.assertTrue(rel['rerun_equals_capture'])


if __name__ == '__main__':
    unittest.main()
