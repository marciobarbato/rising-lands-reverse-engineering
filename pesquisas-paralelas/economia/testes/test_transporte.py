"""Transport (unit state 18), cave unload (unit state 20) and the state-19 saved-state checks over their original-first
capture.

- The capture is original-only, reproduces the display reference's frames 0/1 and leaves the code unchanged.
- Real call sites: CalculTransporteEngin from EnginNextEtape (return 0x455e2d) after tag 8, CalculDechargeCaveEngin
  (return 0x455d21) after tag 19; the declared hunger in state 18 reaches the saved-state-0x12 check natively.
- Every recorded call replays without a CPU from the bytes the original read before writing; Economy's own callees run
  in-process. Deliberate mutations are caught; the provider refuses an omitted unit register.
- The committed native differential is bound to the current translations.
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
import replay_restauracao as rr  # noqa: E402
import replay_transporte as rp  # noqa: E402
import transporte as tr  # noqa: E402
import validar_transporte as vt  # noqa: E402

RELATORIO = PASTA / 'validacao-transporte-emulada.json'
_CAP = {}


def captura():
    if 'c' not in _CAP:
        _CAP['c'] = json.loads(lzma.decompress(vt.CAPTURA.read_bytes()))
    return _CAP['c']


def chamadas(rotina):
    return [r for r in captura()['calls'] if r['routine'] == rotina]


def topo(r):
    return [x[1] for x in r['calls'] if x[0] == 0]


def campo(r, deslocamento, largura=1):
    m = rr.MemoriaEsparsa(r['read_before_write'])
    if r['routine'] == 'EnginNextEtape:19':
        rec = int(r['entry_registers']['ESI'], 16)
    else:
        rec = m.u32(tr.PONTEIRO_UNIDADES) + tr.PASSO * (int(r['entry_registers']['EAX'], 16) & 0xffff)
    return m.u8(rec + deslocamento) if largura == 1 else m.u16(rec + deslocamento)


class Captura(unittest.TestCase):
    def test_original_only_and_reproduced(self):
        c = captura()
        self.assertFalse(c['translation_executed'])
        self.assertEqual(c['reproduction'], dict(load_tail=True, between_frames=True, frame1=True, code_unchanged=True))
        self.assertEqual(c['original_sha256'], '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')

    def test_real_call_sites(self):
        reais = [r for r in chamadas('CalculTransporteEngin') if 'action' not in r]
        self.assertTrue(reais)
        self.assertEqual({r['caller_return'] for r in reais}, {'0x455e2d'})
        self.assertTrue({1, 2, 3} <= {campo(r, 0x89) for r in reais})
        reais = [r for r in chamadas('CalculDechargeCaveEngin') if 'action' not in r]
        self.assertTrue(reais)
        self.assertEqual({r['caller_return'] for r in reais}, {'0x455d21'})
        self.assertTrue({1, 2, 3} <= {campo(r, 0x89) for r in reais})
        # Goods leave the cave (state 20 phase 1) and reach a depot (phase 3) natively.
        self.assertTrue(any('BatimentEnleveMatiere' in topo(r) for r in reais))
        self.assertTrue(any('BatimentAjouteMatiere' in topo(r) or 'EnginRetireType' in topo(r) for r in reais))

    def test_saved_state_checks_reached(self):
        corpos = chamadas('EnginNextEtape:19')
        estados = {campo(r, 0xa0, 2) for r in corpos}
        self.assertTrue(set(al.VERIFICACOES) <= estados, sorted(estados))
        reais = [r for r in corpos if 'action' not in r]
        self.assertIn(0x12, {campo(r, 0xa0, 2) for r in reais})

    def test_empty_ground_depot_case_does_not_drop_stale_cargo(self):
        # This restored case formerly set count=0 without clearing capacity
        # tags: BagContient found stale food that BagRetire could not remove,
        # and the original EnginRetireType loop never completed.
        r = next(r for r in chamadas('CalculTransporteEngin')
                 if 'phase 3, timer 1, empty, the sack is the depot cell' in r.get('action', ''))
        self.assertIn('BagContient', topo(r))
        self.assertNotIn('EnginRetireType', topo(r))
        self.assertNotIn('BatimentAjouteMatiere', topo(r))

    def test_all_declared_cases_completed(self):
        c = captura()
        self.assertGreaterEqual(c['last_counter'], 1800)
        self.assertEqual(c['cases_pending'], 0)
        self.assertEqual(c['cases'], c['cases_planned'])
        self.assertEqual(c['cases'], sum(a['kind'] == 'case' and
                                        a['label'].startswith(('Calcul', 'EnginNextEtape')) for a in c['actions']))


class Replay(unittest.TestCase):
    def test_every_call_replays(self):
        contagem, falhas = rp.replay(captura())
        self.assertEqual(falhas, [], json.dumps(falhas[:5], indent=1))
        for nome in vt.TRADUZIDAS:
            self.assertGreater(contagem[nome]['match'], 0, nome)

    def test_mutations_are_detected(self):
        class SemRetorno(tr.Transporte):
            """State 20: the unit does not go back to the cave (phase 0) once its bag is empty."""
            def _dc3(self, r, rec, di, desloc):
                antes = self.m.u16(rec + 0xb2)
                self.m.u16(rec + 0xb2, 0xffff)
                try:
                    return super()._dc3(r, rec, di, desloc)
                finally:
                    self.m.u16(rec + 0xb2, antes)

        class TimerOnze(tr.Transporte):
            def _t0(self, r, rec, di, desloc):
                saida = super()._t0(r, rec, di, desloc)
                if self.m.u8(rec + 0x8b) == 0xa:
                    self.m.u8(rec + 0x8b, 0xb)
                return saida

        class SemSoltar(al.Alimentacao):
            def _soltar_alvo(self, r, esi, di):
                return True

        def com(cls):
            def executar(nome, m, resultado):
                rpl = vt.Replay(resultado)
                regs = {k: int(resultado['entry_registers'][k], 16) for k in tr.REG7 + ('ESP',)}
                return cls(m, externo=rpl(m)).chamar(nome, regs), rpl
            return executar

        def com_fome(cls):
            def executar(nome, m, resultado):
                import restauracao as rs
                import validar_restauracao as vr
                rpl = vr.ReplayCorpo(resultado)
                base = rpl(m)
                regs = {k: int(resultado['entry_registers'][k], 16) for k in tr.REG7 + ('ESP',)}
                fome = cls(m, externo=rs.provedor_restauracao(rs.Restauracao(m, externo=base), base))
                return fome.chamar(nome, regs), rpl
            return executar

        casos = ((com(SemRetorno), [r for r in chamadas('CalculDechargeCaveEngin') if campo(r, 0x89) == 3]),
                 (com(TimerOnze), [r for r in chamadas('CalculTransporteEngin') if campo(r, 1) == 5
                                   and campo(r, 0x89) == 0]),
                 (com_fome(SemSoltar), [r for r in chamadas('EnginNextEtape:19') if campo(r, 0xa0, 2) in (1, 0x18)]))
        for executar, rs_ in casos:
            self.assertTrue(rs_)
            resultados = {rr.replay_chamada(r, executar)[0] for r in rs_}
            self.assertTrue(resultados & {'mismatch', 'error'})

    def test_dependencies_raise(self):
        r = next(x for x in chamadas('CalculDechargeCaveEngin') if 'DeplaceEngin' in topo(x))
        m = rr.MemoriaEsparsa(r['read_before_write'])
        regs = {k: int(v, 16) for k, v in r['entry_registers'].items()}
        with self.assertRaises(tr.DependenciaTransporte):
            tr.Transporte(m).chamar('CalculDechargeCaveEngin', regs)

    def test_provider_refuses_omitted_unit(self):
        from entrada_estruturas import ArgumentoNaoPassado
        r = chamadas('CalculTransporteEngin')[0]
        m = rr.MemoriaEsparsa(r['read_before_write'])
        externo = tr.provedor_transporte(tr.Transporte(m))
        for nome in tr.ROTINAS:
            with self.assertRaises(ArgumentoNaoPassado):
                externo(nome, 0x455e28, {'EDX': 0})
        self.assertEqual(m.escritos, {})


class Relatorio(unittest.TestCase):
    def test_native_report_bound_to_translation(self):
        rel = json.loads(RELATORIO.read_text())
        for p, h in rel['translation'].items():
            self.assertEqual(h, hashlib.sha256((PASTA / p).read_bytes()).hexdigest(), p)
        self.assertEqual((rel['mismatches'], rel['errors'], rel['outside_domain']), (0, 0, 0))
        self.assertTrue(rel['rerun_equals_capture'])
        self.assertEqual(rel['compared'], sum(1 for r in captura()['calls'] if r['routine'] in vt.TRADUZIDAS))


if __name__ == '__main__':
    unittest.main()
