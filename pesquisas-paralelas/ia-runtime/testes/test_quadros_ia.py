"""M2.2 preparation: AffGame's HUD flag store, the N-frame phase names, the address mask, the static display
context and the event alignment of the N-frame comparator."""
import json
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
import ambiente_ia_runtime  # noqa: E402,F401
from affgame_hud_ia import BANDEIRA_HUD, affgame_hud  # noqa: E402
from proxima_etapa_quadro import TIPOS_VARREDURA  # noqa: E402
from reinicio_ia import DependenciaIA  # noqa: E402

ROOT = OWNED.parents[1]


class Memoria:
    def __init__(self, valores):
        self.b = {}
        for endereco, largura, valor in valores:
            for i in range(largura):
                self.b[endereco + i] = (valor >> 8 * i) & 0xff

    def _ler(self, endereco, largura):
        return int.from_bytes(bytes(self.b.get(endereco + i, 0) for i in range(largura)), 'little')

    def u8(self, a):
        return self._ler(a, 1)

    def u16(self, a):
        return self._ler(a, 2)

    def u32(self, a):
        return self._ler(a, 4)


def estado(contador, bandeira=1, divisor=1, evento=0, modo=0x12, paleta=0x3600400, marcador=0xffff, extra=()):
    return Memoria([(0x4e2f78, 1, modo), (0x4e1b0e, 1, evento), (BANDEIRA_HUD, 1, bandeira),
                    (0x508f7c, 4, contador), (0x497284, 1, divisor), (0x4e179c, 4, paleta),
                    (0x496204, 2, marcador)] + list(extra))


class AffGameHud(unittest.TestCase):
    def test_multiple_of_five_sets_the_flag_and_eax_is_dd_ok(self):
        chamadas = []
        e = affgame_hud(estado(10), chamadas.append)
        self.assertTrue(e.desenhou)
        self.assertEqual(len(chamadas), 1)
        self.assertEqual(e.escritas, ((BANDEIRA_HUD, 1, 0), (BANDEIRA_HUD, 1, 1)))
        self.assertEqual(e.eax, 0)

    def test_other_counters_clear_the_flag_and_leave_the_quotient(self):
        e = affgame_hud(estado(0x1003), lambda m: None)
        self.assertEqual(e.escritas, ((BANDEIRA_HUD, 1, 0),))
        self.assertEqual(e.eax, (0x1003 // 5) & ~0xff)

    def test_frame_one_net_unchanged(self):
        # between_frames(1): counter 0, flag 1 -> stored 0 then 1, as Graphics' frame-1 capture observed
        self.assertEqual(affgame_hud(estado(0), lambda m: None).escritas[-1], (BANDEIRA_HUD, 1, 1))

    def test_early_return_draws_and_stores_nothing(self):
        e = affgame_hud(estado(7, bandeira=0, divisor=2), lambda m: self.fail('body must not run'))
        self.assertFalse(e.desenhou)
        self.assertEqual(e.escritas, ())
        self.assertEqual(e.eax, 3)

    def test_named_stops(self):
        for m, sitio in ((estado(5, evento=1), 0x417905), (estado(5, bandeira=0, divisor=0), 0x417921),
                         (estado(5, modo=0x16), 0x4176a8), (estado(5, marcador=0x1234), 0x417ba2),
                         (estado(5, paleta=0), 0x43ee95), (estado(5, extra=[(0x508f92, 1, 1)]), 0x417938)):
            with self.subTest(sitio=hex(sitio)), self.assertRaises(DependenciaIA) as erro:
                affgame_hud(m, lambda m: None)
            self.assertEqual(erro.exception.sitio, sitio)


class Varredura(unittest.TestCase):
    def test_scan_type_classifier(self):
        self.assertEqual(sorted(TIPOS_VARREDURA), [0, 1, 2, 3, 8, 11, 12, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25])


class MascaraEContexto(unittest.TestCase):
    def test_both_policy_formats(self):
        from comparar_quadros_ia import MascaraEnderecos
        for faixas in ([['0x1002', '0x1004'], ['0x2000', '0x2001']],
                       [dict(block='x', start='0x1002', end='0x1004'), dict(block='y', start='0x2000', end='0x2001')]):
            m = MascaraEnderecos(faixas)
            self.assertEqual(m.bytes, 3)
            self.assertEqual(m.aplicar(0x1000, b'\x01' * 8), (b'\x01\x01\x00\x00\x01\x01\x01\x01', 2))
            self.assertTrue(m.mascarado(0x2000) and not m.mascarado(0x2001))

    def test_shared_issuer_aligned_with_python_or_reported(self):
        from comparar_quadros_ia import eventos_logicos
        from comparar_quadro1_encadeado_ia import VINCULO
        from contexto_exibicao_ia import ContextoAmbiguo
        ev = lambda nome, ret: dict(name=nome, arguments=[], caller_return=ret, results={}, memory_writes=[])  # noqa
        ref = [ev('A', '0x1'), ev('DD', '0x2'), ev('S', '0x3'), ev('S2', '0x3')]

        def classe(e):
            if e['name'] == 'DD':
                return 'display'
            if e['name'].startswith('S'):
                raise ContextoAmbiguo('MemFree', 3)
            return 'logic'
        saida, exibicao, resolvidos, sem_par = eventos_logicos(ref, [ev('A', '0x1'), ev('S', '0x3')], classe, VINCULO)
        self.assertEqual([e['name'] for e in saida], ['A', 'S'])
        self.assertEqual((exibicao, len(resolvidos), [x['event'] for x in sem_par]), ([1], 1, ['S2']))

    def test_static_display_context_reproduces_m2_1(self):
        """The issuer classification gives M2.1's natively tracked display counts on the -v2 frame capture."""
        try:
            from inventario_ia_runtime import OriginalImage
            imagem = OriginalImage()
        except (FileNotFoundError, OSError) as erro:
            self.skipTest(f'intact executable not available: {erro}')
        from contexto_exibicao_ia import ContextoAmbiguo, ContextoExibicao
        politica = json.loads((ROOT / 'pesquisas-paralelas/missoes/validacao/'
                                      'm2-politica-comparacao-quadro1.json').read_bytes())
        cap = json.loads((ROOT / 'pesquisas-paralelas/missoes/evidencias/'
                                 'captura-quadro1-monde01-exibicao-v2.json').read_bytes())
        prova = json.loads((OWNED / 'validacao/m2-1-prova-quadro1.json').read_bytes())
        c = ContextoExibicao(imagem, politica['display_roots'])

        def classes(eventos, f):
            saida = []
            for e in eventos:
                try:
                    saida.append(f(e))
                except ContextoAmbiguo as erro:
                    saida.append('shared:' + erro.rotina)
            return saida
        for fase in cap['phases']:
            v = classes(fase['bindings'], c.vinculo)
            b = classes(fase['boundaries'], c.fronteira)
            esperado = prova['phases'][fase['phase']]
            self.assertEqual(v.count('display'), esperado['bindings']['display_context_not_modeled'], fase['phase'])
            self.assertEqual([e['routine'] + ' @ ' + e['caller'] for e, k in zip(fase['boundaries'], b)
                              if k == 'display'], esperado['boundaries']['display_context_not_modeled'])
            self.assertTrue(set(v + b) <= {'display', 'logic', 'shared:MenuInit', 'shared:MemFree'})


class CapturaDelta(unittest.TestCase):
    """The M2.2 delta form: replay from s0, summary hashes, checkpoint full states, failures named."""

    def captura(self, resumo=None, completo=None):
        import base64
        import zlib
        from comparar_quadros_ia import resumo_estado
        s0 = {'dgroup': (0x494000, bytes(16)), 'alloc00001': (0x40000000, b'\x01' * 8)}
        depois = {'dgroup': (0x494000, bytes(4) + b'\xaa\xbb' + bytes(10)), 'alloc00002': (0x40001000, b'\x07' * 4)}
        fase = dict(phase='load_tail', state_delta=dict(
            released=['alloc00001'],
            allocated={'alloc00002': dict(base='0x40001000', zlib_base64=base64.b64encode(
                zlib.compress(b'\x07' * 4)).decode())},
            ranges=[dict(address='0x494004', hex='aabb')]),
            state_after=dict(summary=resumo or resumo_estado(depois)))
        if completo is not None:
            fase['state_after']['full_state'] = completo
        return dict(phases=[fase]), s0, depois

    def test_replay_and_checkpoint(self):
        import base64
        import zlib
        from comparar_quadros_ia import fases_referencia
        _, _, depois = self.captura()
        completo = {n: dict(base=hex(b), zlib_base64=base64.b64encode(zlib.compress(d)).decode())
                    for n, (b, d) in depois.items()}
        cap, s0, depois = self.captura(completo=completo)
        [(fase, estado, integridade)] = list(fases_referencia(cap, s0))
        self.assertEqual(estado, depois)
        self.assertEqual(integridade, dict(form='delta', summary_equal=True, checkpoint_full_state_equal=True))

    def test_integrity_failures_are_named(self):
        from comparar_quadros_ia import IntegridadeCaptura, fases_referencia
        cap, s0, _ = self.captura(resumo=dict(blocks=2, bytes=20, sha256='0' * 64))
        with self.assertRaises(IntegridadeCaptura):
            list(fases_referencia(cap, s0))
        cap, s0, _ = self.captura()
        cap['phases'][0]['state_delta']['ranges'] = [dict(address='0x49400f', hex='aabb')]   # crosses the block end
        with self.assertRaises(IntegridadeCaptura):
            list(fases_referencia(cap, s0))
        cap, s0, _ = self.captura(completo={'dgroup': dict(base='0x494000', hex='00' * 16)})
        with self.assertRaises(IntegridadeCaptura):
            list(fases_referencia(cap, s0))


class Fases(unittest.TestCase):
    def test_phase_names_follow_missions(self):
        from composicao_quadros_ia import fases_quadros
        self.assertEqual(fases_quadros(3), ['load_tail', 'between_frames', 'frame1', 'between_frames2', 'frame2',
                                            'between_frames3', 'frame3'])


if __name__ == '__main__':
    unittest.main()
