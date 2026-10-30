"""EnginRestaureEtat, BatimentEnleveMatiere, the state-19 cave meal / "nothing found" and SetDechargeCaveEnginSelect
over their original-first captures.

- Both captures (``rotinas``: the routines at their real call sites and in declared cases; ``corpo``: the same
  timeline with the state-19 bodies recorded) are original-only, reproduce the display reference's frames 0/1, leave
  the code unchanged and record the same declared actions.
- MONDE01 facts shown natively: with every food sack removed, unit 12 (walking to a sack) finds nothing and goes back
  to work through EnginRestaureEtat; unit 14 eats at the own cave, which costs one food through
  BatimentEnleveMatiere; with no food at the cave, "nothing found" runs from the cave; tag 19 sends unit 14 to unload
  (state 0x14) and its hunger there reaches EnginRestaureEtat's saved-state-0x14 branch.
- Every recorded call replays without a CPU from the bytes the original read before writing; the bodies replay with
  EnginRestaureEtat/BatimentEnleveMatiere served in-process. Deliberate mutations are caught; providers refuse
  omitted argument registers.
- The committed native differentials are bound to the current translations.
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

import replay_restauracao as rp  # noqa: E402
import restauracao as rs  # noqa: E402
import validar_restauracao as vr  # noqa: E402

RELATORIOS = {m: PASTA / f'validacao-restauracao-{m}-emulada.json' for m in ('rotinas', 'corpo')}
_CAP = {}


def captura(modo):
    if modo not in _CAP:
        _CAP[modo] = json.loads(lzma.decompress(vr.CAPTURAS[modo].read_bytes()))
    return _CAP[modo]


def chamadas(modo, rotina):
    return [r for r in captura(modo)['calls'] if r['routine'] == rotina]


def topo(r):
    return [x[1] for x in r['calls'] if x[0] == 0]


def saved_state(r):
    """The saved state +0xa0 read at entry (from the bytes read before writing)."""
    from replay_ciclo_trabalho import MemoriaEsparsa
    m = MemoriaEsparsa(r['read_before_write'])
    u = int(r['entry_registers']['EAX'], 16) & 0xffff
    return m.u16(m.u32(rs.PONTEIRO_UNIDADES) + rs.PASSO * u + 0xa0)


class Captura(unittest.TestCase):
    def test_original_only_and_reproduced(self):
        for modo in ('rotinas', 'corpo'):
            c = captura(modo)
            self.assertFalse(c['translation_executed'])
            self.assertEqual(c['mode'], modo)
            self.assertEqual(c['reproduction'], dict(load_tail=True, between_frames=True, frame1=True,
                                                     code_unchanged=True))
            self.assertEqual(c['original_sha256'], '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')

    def test_both_modes_share_the_timeline(self):
        a, b = captura('rotinas'), captura('corpo')
        self.assertEqual(a['frames'], b['frames'])
        self.assertEqual([(x['frame'], x['label']) for x in a['actions']], [(x['frame'], x['label']) for x in b['actions']])
        self.assertTrue(a['sacks_removed'])

    def test_real_call_sites(self):
        reais = [r for r in chamadas('rotinas', 'EnginRestaureEtat') if 'action' not in r]
        self.assertTrue(reais)
        self.assertEqual({r['caller_return'] for r in reais}, {'0x45566f'})
        self.assertIn(5, {saved_state(r) for r in reais})
        self.assertIn(0x14, {saved_state(r) for r in reais})
        reais = [r for r in chamadas('rotinas', 'BatimentEnleveMatiere') if 'action' not in r]
        # The cave meal (0x4556d7) and the unload state 20 (CalculDechargeCaveEngin 0x44e565) after tag 19.
        self.assertEqual({r['caller_return'] for r in reais}, {'0x4556dc', '0x44e56a'})
        cave = [r for r in reais if r['caller_return'] == '0x4556dc']
        self.assertEqual(len(cave), 3)
        for r in cave:
            self.assertEqual((int(r['entry_registers']['EAX'], 16) & 0xff, int(r['entry_registers']['EDX'], 16) & 0xffff),
                             (1, 1))

    def test_state19_branches_in_the_bodies(self):
        corpos = chamadas('corpo', 'EnginNextEtape:19')
        caminhos = {tuple(topo(r)[-3:]) for r in corpos}
        self.assertTrue(any('BatimentEnleveMatiere' in topo(r) for r in corpos), caminhos)
        nada = [r for r in corpos if 'ChercheVegetLibre' in topo(r) and topo(r)[-1] == 'EnginRestaureEtat']
        self.assertTrue(nada, caminhos)
        self.assertTrue(any('TestRessource' in topo(r) and 'BatimentEnleveMatiere' not in topo(r) for r in nada))


class Replay(unittest.TestCase):
    def test_every_call_replays(self):
        for modo in ('rotinas', 'corpo'):
            contagem, falhas = rp.replay(captura(modo))
            self.assertEqual([f for f in falhas if f['outcome'] != 'outside_domain'], [],
                             json.dumps(falhas[:5], indent=1))
            for nome in vr.DIRETAS:
                if modo == 'rotinas':
                    self.assertGreater(contagem[nome]['match'], 0, nome)

    def test_every_switch_target_is_exercised(self):
        estados = {saved_state(r) for r in chamadas('rotinas', 'EnginRestaureEtat')}
        self.assertTrue({1, 2, 3, 5, 7, 0xb, 0xd, 0xf, 0x10, 0x11, 0x12, 0x14, 0x18} <= estados, sorted(estados))
        self.assertTrue(estados - {1, 2, 3, 5, 7, 0xb, 0xd, 0xf, 0x10, 0x11, 0x12, 0x14, 0x18})

    def test_mutations_are_detected(self):
        restauros = chamadas('rotinas', 'EnginRestaureEtat')
        matieres = chamadas('rotinas', 'BatimentEnleveMatiere')
        selecoes = chamadas('rotinas', 'SetDechargeCaveEnginSelect')

        class SemDeposito(rs.Restauracao):
            """Saved state 5 without the depot tuple put back."""
            def _estado5(self, rec, si, r, esp, loc):
                antes = self.m.u16(rec + 0x80)
                super()._estado5(rec, si, r, esp, loc)
                self.m.u16(rec + 0x80, antes ^ 1)

        class NivelSemSete(rs.Restauracao):
            def batiment_enleve_matiere(self, regs):
                saida = super().batiment_enleve_matiere(regs)
                o = 6 * (regs['EBX'] & 0xff)
                self.m.u8(rs.INDICADOR + o + 4, self.m.u8(rs.INDICADOR + o + 4) + 1)
                return saida

        class SemVoz(rs.Restauracao):
            def _ext(self, nome, chamada, r, esp, pilha=()):
                if nome == 'EnginAsk':
                    return dict(r)
                return super()._ext(nome, chamada, r, esp, pilha)

        def com(cls):
            def executar(nome, m, resultado):
                rr = vr.Replay(resultado)
                regs = {k: int(resultado['entry_registers'][k], 16) for k in rs.REG7 + ('ESP',)}
                return cls(m, externo=rr(m)).chamar(nome, regs), rr
            return executar

        for cls, casos in ((SemDeposito, [r for r in restauros if saved_state(r) == 5]), (NivelSemSete, matieres),
                           (SemVoz, selecoes)):
            self.assertTrue(casos, cls.__name__)
            resultados = {rp.replay_chamada(r, com(cls))[0] for r in casos}
            self.assertTrue(resultados & {'mismatch', 'error'}, cls.__name__)

    def test_dependencies_raise(self):
        r = next(x for x in chamadas('rotinas', 'EnginRestaureEtat') if saved_state(x) == 5)
        m = rp.MemoriaEsparsa(r['read_before_write'])
        regs = {k: int(v, 16) for k, v in r['entry_registers'].items()}
        with self.assertRaises(rs.DependenciaRestauracao) as ctx:
            rs.Restauracao(m).chamar('EnginRestaureEtat', regs)
        self.assertIn(ctx.exception.chamada, (0x453639, 0x4536d4))

    def test_provider_refuses_omitted_arguments(self):
        from entrada_estruturas import ArgumentoNaoPassado
        r = next(x for x in chamadas('rotinas', 'BatimentEnleveMatiere'))
        m = rp.MemoriaEsparsa(r['read_before_write'])
        externo = rs.provedor_restauracao(rs.Restauracao(m))
        regs = {k: int(r['entry_registers'][k], 16) for k in ('EAX', 'EDX')}
        with self.assertRaises(ArgumentoNaoPassado):
            externo('BatimentEnleveMatiere', 0x4556d7, regs)
        self.assertEqual(m.escritos, {})


class Relatorio(unittest.TestCase):
    def test_native_reports_bound_to_translation(self):
        for modo, caminho in RELATORIOS.items():
            rel = json.loads(caminho.read_text())
            for p, h in rel['translation'].items():
                self.assertEqual(h, hashlib.sha256((PASTA / p).read_bytes()).hexdigest(), (modo, p))
            self.assertEqual((rel['mismatches'], rel['errors']), (0, 0), modo)
            self.assertTrue(rel['rerun_equals_capture'], modo)
            self.assertEqual(rel['compared'], sum(1 for r in captura(modo)['calls'] if r['routine'] in vr.TRADUZIDAS))


if __name__ == '__main__':
    unittest.main()
