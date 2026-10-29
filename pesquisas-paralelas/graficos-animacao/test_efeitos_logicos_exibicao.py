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
        for m, sitio in ((estado(d=1), 0x43f191), (estado(origem=(0, 0)), 0x415b77), (estado(pool={3: 3}), 0x407dd3)):
            with self.assertRaises(e.DependenciaExibicao) as c:
                e.desenhar_jogo(m)
            self.assertEqual(c.exception.sitio, sitio)

    def test_dd_init_dimensions(self):
        self.assertEqual(e.inicializar_dimensoes(None).escritas[-1], (0x508726, 2, 17))
        with self.assertRaises(e.DependenciaExibicao):
            e.inicializar_dimensoes(None, False)


if __name__ == '__main__':
    unittest.main()
