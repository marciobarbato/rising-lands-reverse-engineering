import json, struct, unittest
from pathlib import Path

import efeitos_logicos_exibicao as e

EVIDENCIA = Path(__file__).resolve().parent/'evidencias/efeitos-logicos-exibicao.json'


class Memoria:
    def __init__(self, **valores):
        self.d = {}
        for a, (n, v) in valores.items():
            self.d[int(a, 16)] = (n, v)

    def _ler(self, a, n):
        return self.d.get(a, (n, 0))[1]
    u8 = lambda self, a: self._ler(a, 1)
    u16 = lambda self, a: self._ler(a, 2)


class Pool(Memoria):
    def __init__(self, estados, **kw):
        super().__init__(**kw)
        self.estados = estados

    def u8(self, a):
        if e.ESTRUTURAS <= a < e.ESTRUTURAS+1000*e.ESTRUTURA_PASSO and (a-e.ESTRUTURAS) % e.ESTRUTURA_PASSO == 5:
            return self.estados.get((a-e.ESTRUTURAS)//e.ESTRUTURA_PASSO, 0)
        return super().u8(a)


def estado(origem=(4, 6), pool=None, d=0):
    return Pool(pool or {5: 5}, **{'0x4dfb44': (1, d), '0x508724': (2, 25), '0x508726': (2, 17),
                                  '0x508720': (2, origem[0]), '0x508722': (2, origem[1])})


class CapturaTest(unittest.TestCase):
    def test_capture_found_no_logic_read_of_display_writes(self):
        d = json.loads(EVIDENCIA.read_text())
        self.assertTrue(all(all(r.values()) for r in d['reproduced']))
        logic = {k: v for k, v in d['logic_read_bytes_by_class'].items() if k.startswith('heap') or k == 'dgroup'}
        for k, v in d['dgroup_and_logic_read_bytes'].items():
            for _, leitor in v['logic_readers']:
                self.assertTrue(leitor.startswith('DD'), (k, leitor))   # display wrappers only
        self.assertEqual({k: v for k, v in logic.items() if k.startswith('heap')}, {k: 0 for k in logic if k.startswith('heap')})

    def test_provider_accepts_every_captured_entry_guard(self):
        d = json.loads(EVIDENCIA.read_text())
        for g in d['guards_at_root_entry']:
            if g['phase'] == 'startup':
                continue
            pool = {i: 5 for i in range(g['structure_states']['5'])}
            m = estado(tuple(g['view_origin']), pool, g['dfb44'])
            fn = e.restaurar_tudo if g['root'] == 'RestoreAll' else e.desenhar_jogo
            r = fn(m)
            self.assertEqual(r.escritas, ())


class DominioTest(unittest.TestCase):
    def test_named_stops(self):
        for m, sitio in ((estado(d=1), 0x43f191), (estado(origem=(5, 5)), 0x415b77), (estado(pool={3: 3}), 0x407dd3)):
            with self.assertRaises(e.DependenciaExibicao) as c:
                e.desenhar_jogo(m)
            self.assertEqual(c.exception.sitio, sitio)

    def test_dd_init_dimensions(self):
        self.assertEqual(e.inicializar_dimensoes(None).escritas[-1], (0x508726, 2, 17))
        with self.assertRaises(e.DependenciaExibicao):
            e.inicializar_dimensoes(None, False)


CHAMADAS = Path(__file__).resolve().parent/'evidencias/chamadas-menuinit-exibicao.json'
ISOLADO = [Path(__file__).resolve().parent/'evidencias'/n for n in ('dominio-exibicao-isolado.json', 'dominio-exibicao-visivel.json')]


class Plana:
    def __init__(self, u32=None, u16=None):
        self._u32, self._u16 = u32 or {}, u16 or {}
    u32 = lambda self, a: self._u32.get(a, 0)
    u16 = lambda self, a: self._u16.get(a, 0)
    u8 = lambda self, a: self._u32.get(a, 0)


class MenuInitTest(unittest.TestCase):
    def chamadas(self):
        return {c['root']: c for c in json.loads(CHAMADAS.read_text())['calls']
                if c['phase'] == 'load_tail' and c['caller'].startswith('MenuInit')}

    def test_lock_unlock_match_the_native_bytes(self):
        c = self.chamadas()
        ponteiro = int(c['DDLockSurface']['eax_out'], 16)
        r = e.ddlocksurface(Plana(), ponteiro)
        final = {}
        for a, n, v in r.escritas:
            for k in range(n):
                final[a+k] = (v >> 8*k) & 0xff
        obs = {int(a, 16): v['final_writes'][1] for a, v in c['DDLockSurface']['dgroup_writes'].items()}
        self.assertEqual(final, obs)
        self.assertEqual(r.eax, ponteiro)
        u = e.ddunlocksurface(Plana({0x4e17a8: 1}))
        obs = {int(a, 16): v['final_writes'][1] for a, v in c['DDUnlockSurface']['dgroup_writes'].items()}
        self.assertEqual({a+k: 0 for a, n, _ in u.escritas for k in range(n)}, obs)
        self.assertEqual(int(c['DDUnlockSurface']['eax_out'], 16), u.eax)
        with self.assertRaises(e.DependenciaExibicao):
            e.ddlocksurface(Plana({0x4e17a8: 1}), 1)

    def test_calls_without_dgroup_effect(self):
        c = self.chamadas()
        for nome in ('DeleteBank', 'FilledBox', 'DDFlipPage'):
            self.assertEqual(c[nome]['dgroup_writes'], {})
        self.assertEqual(e.ddflippage(Plana()).eax, int(c['DDFlipPage']['eax_out'], 16))
        self.assertEqual(e.filledbox(None).escritas, ())
        with self.assertRaises(e.DependenciaExibicao):
            e.ddflippage(Plana({0x4dfb44: 1}))

    def test_deletebank_order_and_native_free_sequence(self):
        d = self.chamadas()['DeleteBank']
        self.assertEqual(d['bank_walk']['free_order'], d['freed_pointers'])      # native GlobalHandle sequence
        self.assertEqual(d['other_memory_writes'][0][:3], ['0x47ac6000', 72, 0])  # the zeroed count
        m = Plana({0x1004: 0x2000, 0x2000: 0x3000, 0x2004: 0, 0x2008: 0x3100, 0x3008: 0x4000, 0x3108: 0},
                  {0x1000: 3})
        m._u32.update({0x2000: 0x3000, 0x2004: 0, 0x2008: 0x3100})
        r = e.deletebank(m, 0x1000)
        self.assertEqual(r.liberacoes, (0x4000, 0x3000, 0x3100, 0x2000, 0x1000))
        self.assertEqual(r.escritas, ((0x1000, 2, 0),))
        self.assertEqual(e.deletebank(m, 0).liberacoes, ())


class DominioIsoladoTest(unittest.TestCase):
    def test_every_proved_origin_has_a_native_clean_case(self):
        vistos = set()
        for f in ISOLADO:
            for r in json.loads(f.read_text())['records']:
                for c in r['cases']:
                    if c['case'].startswith('origin_'):
                        _, x, y = c['case'].split('_')
                        vistos.add((int(x), int(y)))
                    elif c['case'].startswith('visible') and c['case'].endswith('_state_5'):
                        p = c['case'].split('_')
                        vistos.add((int(p[1]), int(p[2])))
        self.assertEqual(vistos | {(4, 6)}, set(e.ORIGENS_PROVADAS))

    def test_origin_provider_domain(self):
        self.assertEqual(e.desenhar_jogo(estado(origem=(39, 47))).escritas, ())
        with self.assertRaises(e.DependenciaExibicao):
            e.desenhar_jogo(estado(origem=(5, 5)))


if __name__ == '__main__':
    unittest.main()
