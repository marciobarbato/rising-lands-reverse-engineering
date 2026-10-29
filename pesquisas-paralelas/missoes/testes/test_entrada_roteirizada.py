"""M3 scripted-input harness: input-file schema, click timing and the committed probe inputs.

CPU-free. The native runs themselves are recorded under m3/sondas and checked by their replay comparisons.
"""
import json
from pathlib import Path
import sys
import unittest

M3 = Path(__file__).resolve().parents[1] / 'm3'
sys.path.insert(0, str(M3))
import entrada_roteirizada as er  # noqa: E402


def entrada(**kw):
    return dict(dict(schema=er.ESQUEMA, start=dict(frame=128), stop_frame=200, frames=[]), **kw)


class TestEsquema(unittest.TestCase):
    def test_vazio(self):
        self.assertEqual(er.carregar_entrada(entrada()), ({}, 200))

    def test_quadro_completo(self):
        q, _ = er.carregar_entrada(entrada(frames=[dict(frame=130, cursor=[1, 2], messages=[['0x201', 1, 5]],
                                                        keys={'0x10': -32768})]))
        self.assertEqual(q[130], ((1, 2), ((0x201, 1, 5),), {0x10: -32768}))

    def test_recusas(self):
        for ruim in (dict(schema='x'), dict(start=dict(frame=1)), dict(frames=[dict(frame=128)]),
                     dict(frames=[dict(frame=201)]), dict(frames=[dict(frame=130), dict(frame=130)]),
                     dict(frames=[dict(frame=130, cursor=[800, 0])]),
                     dict(frames=[dict(frame=130, messages=[[0x102, 0, 0]])]),
                     dict(frames=[dict(frame=130, keys={'0': 0})]),
                     dict(frames=[dict(frame=130, keys={'16': 0x8000})]),
                     dict(checkpoint_frames=[128])):
            with self.subTest(ruim=ruim), self.assertRaises(ValueError):
                er.carregar_entrada(entrada(**ruim))

    def test_mensagens_sem_defwindowproc(self):
        # WndProc 0x4181a1 handles exactly these without DefWindowProcA (encodings 0x4181b5..0x41857d).
        self.assertEqual(sorted(er.MENSAGENS), [0x100, 0x101, 0x200, 0x201, 0x202, 0x203, 0x204, 0x205])


class TestClique(unittest.TestCase):
    def test_tempos_do_plano(self):
        # M3_PLAN §2: WM_MOUSEMOVE at k, DOWN at k+1, UP at k+3, cursor held from k.
        c = er.clique(140, 560, 528)
        lp = 528 << 16 | 560
        self.assertEqual(c, [dict(frame=140, cursor=[560, 528], messages=[[0x200, 0, lp]]),
                             dict(frame=141, messages=[[0x201, 1, lp]]), dict(frame=143, messages=[[0x202, 0, lp]])])
        self.assertEqual(er.clique(140, 1, 2, 'right')[1]['messages'][0][0], 0x204)

    def test_juntar(self):
        q = er.juntar_quadros(er.clique(140, 1, 2), er.clique(143, 3, 4))
        self.assertEqual([x['frame'] for x in q], [140, 141, 143, 144, 146])
        self.assertEqual([m[0] for m in q[2]['messages']], [0x202, 0x200])
        with self.assertRaises(ValueError):
            er.juntar_quadros(er.clique(140, 1, 2), er.clique(140, 3, 4))


class TestEntradasPublicadas(unittest.TestCase):
    def test_validas(self):
        arquivos = sorted((M3 / 'entradas').glob('*.json'))
        self.assertTrue(arquivos)
        for caminho in arquivos:
            with self.subTest(caminho=caminho.name):
                er.carregar_entrada(json.loads(caminho.read_text()))


if __name__ == '__main__':
    unittest.main()
