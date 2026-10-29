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
    u32 = lambda self, a: self._ler(a, 4)


class Pool(Memoria):
    def __init__(self, estados, **kw):
        super().__init__(**kw)
        self.estados, self.tipos = estados, {}

    def u8(self, a):
        if e.ESTRUTURAS <= a < e.ESTRUTURAS+1000*e.ESTRUTURA_PASSO:
            i, campo = divmod(a-e.ESTRUTURAS, e.ESTRUTURA_PASSO)
            if campo == 5:
                return self.estados.get(i, 0)
            if campo == 8 and i in self.estados:
                return self.tipos.get(i, e.TIPO_ESTRUTURA_PROVADO)
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
        for m, sitio in ((estado(origem=(5, 5)), 0x415b77), (estado(pool={3: 3, 4: 5}), 0x407dd3)):
            with self.assertRaises(e.DependenciaExibicao) as c:
                e.desenhar_jogo(m)
            self.assertEqual(c.exception.sitio, sitio)

    def test_dd_init_dimensions(self):
        self.assertEqual(e.inicializar_dimensoes(None).escritas[-1], (0x508726, 2, 17))
        with self.assertRaises(e.DependenciaExibicao):
            e.inicializar_dimensoes(None, False)


CHAMADAS = Path(__file__).resolve().parent/'evidencias/chamadas-menuinit-exibicao.json'
ISOLADO = [Path(__file__).resolve().parent/'evidencias'/n for n in ('dominio-exibicao-isolado.json', 'dominio-exibicao-visivel.json', 'dominio-exibicao-origens-m22.json')]


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
        self.assertEqual(e.ddflippage(Plana({0x4dfb44: 1, 0x508f7c: 2})).escritas, ((0x4e1d18, 1, 1), (0x4dfb44, 1, 0)))

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


FLIPS = Path(__file__).resolve().parent/'evidencias/dominio-exibicao-flips.json'
ESTADOS = Path(__file__).resolve().parent/'evidencias/dominio-exibicao-estados.json'


class VoltasTest(unittest.TestCase):
    def test_shake_model_equals_every_native_case(self):
        for r in json.loads(FLIPS.read_text())['records']:
            fn = e.restaurar_tudo if r['routine'] == 'RestoreAll' else e.desenhar_jogo
            for c in r['cases']:
                if c['case'] == 'captured_inputs':
                    continue
                w = {int(a, 16): bytes.fromhex(v) for a, v in c['writes']}
                m = estado()
                m.d[0x4dfb44] = (1, w[0x4dfb44][0])
                m.d[0x49a05b] = (1, w.get(0x49a05b, b'\0')[0])
                m.d[0x4e1d18] = (1, 4 if r['routine'] == 'AffGame' else 0)
                m.d[0x508f7c] = (1, w[0x508f7c][0])
                for x in c['calls']:
                    obs = {a: (o, n) for a, o, n in x['changed'].get('dgroup', []) if a in ('0x4e1d18', '0x4dfb44')}
                    efeitos = fn(m)
                    prev = {0x4e1d18: m.d[0x4e1d18][1], 0x4dfb44: m.d[0x4dfb44][1]}
                    prev_tab = {k: v for k, v in prev.items()}
                    pred = {hex(a): (prev_tab[a], v) for a, n, v in efeitos.escritas}
                    self.assertEqual(pred, obs, (r['routine'], c['case']))
                    for a, n, v in efeitos.escritas:
                        m.d[a] = (1, v)

    def test_structure_modes_are_accepted_only_for_one_type_2_record(self):
        for estado_ in range(8):
            self.assertEqual(e.desenhar_jogo(estado(pool={0: estado_})).escritas, ())
        with self.assertRaises(e.DependenciaExibicao):
            e.desenhar_jogo(estado(pool={0: 5, 1: 5}))
        m = estado(pool={0: 5})
        m.tipos[0] = 3
        with self.assertRaises(e.DependenciaExibicao):
            e.desenhar_jogo(m)

    def test_structure_matrix_native_cases_are_clean(self):
        for r in json.loads(ESTADOS.read_text())['records']:
            self.assertEqual(len(r['cases']), 41)
            for c in r['cases']:
                self.assertTrue(c['calls'][0]['returned'] and not c['calls'][0]['stopped'])
                sitios = {hex(int(a, 16)) for a, *_ in json.loads((Path(__file__).resolve().parent/'evidencias/fechamento-escritas-affgame-modo12.json').read_text())['escritas_absolutas']['0x4e1d18']}
                self.assertEqual({k for k in c['coverage'] if k != 'readers_of_record_head'} & sitios, set())


INCURSAO = Path(__file__).resolve().parent/'evidencias/dominio-exibicao-incursao.json'


class IncursaoTest(unittest.TestCase):
    def test_native_raid_frames_are_clean_and_projectile_drawn(self):
        d = json.loads(INCURSAO.read_text())
        self.assertEqual([r['phase'] for r in d['records']], ['between_frames3', 'between_frames4', 'between_frames10', 'between_frames33'])
        for r in d['records']:
            self.assertEqual(r['probe']['monsters'], 1)
            self.assertEqual([p[1] for p in r['probe']['projectiles']], [31])
            vistos = [c for c in r['cases'] if c['case'].startswith('projectile_type_')]
            self.assertEqual(len(vistos), 2)
            for c in r['cases']:
                self.assertTrue(c['calls'][0]['returned'] and not c['calls'][0]['stopped'])
            for c in vistos:
                self.assertEqual(c['coverage']['0x46ff70'], 1)    # AffProjectile ran

    def test_projectile_and_monster_guards(self):
        m = estado()
        m.d[0x50b178] = (1, 1)
        m.d[0x5080f0] = (4, 0x9000)
        m.d[0x9002] = (1, 1)
        m.d[0x9000] = (1, 31)
        self.assertEqual(e.desenhar_jogo(m).escritas, ())
        m.d[0x9000] = (1, 9)
        with self.assertRaises(e.DependenciaExibicao) as c:
            e.desenhar_jogo(m)
        self.assertEqual(c.exception.sitio, 0x46ff70)
        m.d[0x9000] = (1, 31)
        m.d[0x50b178] = (1, 2)
        with self.assertRaises(e.DependenciaExibicao) as c:
            e.restaurar_tudo(m)
        self.assertEqual(c.exception.sitio, 0x41591f)


class UnidadeTest(unittest.TestCase):
    def test_raid_unit_walk_and_visible_unit_cases_are_clean(self):
        base = Path(__file__).resolve().parent/'evidencias'
        d = json.loads((base/'dominio-exibicao-incursao-unidade.json').read_text())
        self.assertEqual([r['phase'] for r in d['records']], ['between_frames300', 'between_frames450', 'between_frames620', 'between_frames700'])
        for r in d['records']:
            self.assertTrue(r['probe']['unit16']['cell'])
            for c in r['cases']:
                self.assertTrue(c['calls'][0]['returned'] and not c['calls'][0]['stopped'])
        v = json.loads((base/'dominio-exibicao-incursao-unidade-visivel.json').read_text())
        casos = [c for r in v['records'] for c in r['cases'] if c['case'].startswith('unit16_')]
        self.assertEqual(len(casos), 2)
        for c in casos:
            self.assertEqual(c['coverage']['0x41591f'], 17)      # AffEngin drew the 16 M1 units plus unit 16
            self.assertTrue(c['calls'][0]['returned'] and not c['calls'][0]['stopped'])


class CamposTest(unittest.TestCase):
    def test_guards_are_in_verificacoes_and_never_in_liberacoes(self):
        for fn in (e.restaurar_tudo, e.desenhar_jogo):
            r = fn(estado())
            self.assertEqual(len(r.verificacoes), 6)
            self.assertEqual([n for n, _ in r.verificacoes][:2], ['[0x4dfb44]', '[0x508724]'])
            self.assertEqual(r.liberacoes, ())
        efeitos = [e.inicializar_dimensoes(None), e.ddunlocksurface(Plana({0x4e17a8: 1})), e.ddlocksurface(Plana(), 1),
                   e.ddflippage(Plana()), e.filledbox(None), e.deletebank(Plana(), 0)]
        for r in efeitos:
            self.assertEqual((r.liberacoes, r.verificacoes), ((), ()))

    def test_deletebank_frees_are_in_liberacoes(self):
        m = Plana({0x1004: 0x2000, 0x2000: 0x3000, 0x3008: 0x4000}, {0x1000: 1})
        r = e.deletebank(m, 0x1000)
        self.assertEqual(r.liberacoes, (0x4000, 0x3000, 0x2000, 0x1000))
        self.assertEqual(r.verificacoes, ())


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

    def test_m22_origins_accepted(self):
        for o in ((3, 5), (2, 4), (1, 3), (0, 2), (0, 1)):
            for fn in (e.desenhar_jogo, e.restaurar_tudo):
                self.assertEqual(fn(estado(origem=o)).escritas, ())

    def test_origin_provider_domain(self):
        self.assertEqual(e.desenhar_jogo(estado(origem=(39, 47))).escritas, ())
        with self.assertRaises(e.DependenciaExibicao):
            e.desenhar_jogo(estado(origem=(5, 5)))


if __name__ == '__main__':
    unittest.main()
