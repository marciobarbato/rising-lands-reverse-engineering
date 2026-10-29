"""M2.2 delta form: exact state deltas round-trip and the replay check rejects inconsistencies (CPU-free)."""
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ambiente_missoes  # noqa: F401
import delta_estado_missao as d


def estados():
    rnd = random.Random(7)
    s0 = {'dgroup': (0x495000, bytes(rnd.randrange(256) for _ in range(5000))),
          'alloc00001': (0x1000000, b'\xa7'*300), 'alloc00002': (0x1001000, b'\x00'*64),
          'native_stack': (0x2000000, b'\x11'*16)}
    dg = bytearray(s0['dgroup'][1])
    for o in (0, 1, 2, 9, 70, 71, 200, 4999):
        dg[o] ^= 0xff
    dg[1000:1400] = bytes(400)
    s1 = {'dgroup': (0x495000, bytes(dg)), 'alloc00002': (0x1001000, b'\x00'*60+b'\x01\x02\x03\x04'),
          'alloc00003': (0x1002000, b'\x05'*40), 'native_stack': (0x2000000, b'\x22'*16)}
    return s0, s1


class TestDelta(unittest.TestCase):
    def test_delta_rebuilds_the_next_state_exactly(self):
        s0, s1 = estados()
        delta = d.delta(s0, s1)
        self.assertEqual(delta['released'], ['alloc00001'])
        self.assertEqual(sorted(delta['allocated']), ['alloc00003'])
        novo = d.aplicar(s0, delta, 'x')
        self.assertEqual({n: v for n, v in novo.items() if n != 'native_stack'},
                         {n: v for n, v in s1.items() if n != 'native_stack'})
        self.assertEqual(d.resumo(novo), d.resumo(s1))

    def test_ranges_cover_every_difference_and_merge_close_runs(self):
        velho, novo = bytes(200), bytearray(200)
        for o in (3, 5, 100, 199):
            novo[o] = 1
        faixas = d.faixas_diferentes(velho, bytes(novo))
        self.assertEqual(faixas, [(3, 6), (100, 101), (199, 200)])

    def test_resized_block_is_released_and_allocated_again(self):
        s0 = {'alloc00001': (0x1000, b'ab')}
        s1 = {'alloc00001': (0x1000, b'abc')}
        delta = d.delta(s0, s1)
        self.assertEqual(delta['released'], ['alloc00001'])
        self.assertEqual(list(delta['allocated']), ['alloc00001'])
        self.assertEqual(d.aplicar(s0, delta, 'x'), s1)

    def test_replay_check_accepts_a_consistent_capture_and_rejects_a_tampered_one(self):
        s0, s1 = estados()
        captura = dict(state_s0=dict(summary=d.resumo(s0)), phases=[
            dict(phase='load_tail', state_delta=d.delta(s0, s1),
                 state_after=dict(summary=d.resumo(s1), full_state=d.estado_completo(s1)))])
        self.assertEqual(d.verificar_replay(captura, s0),
                         [dict(phase='load_tail', summary_equal=True, checkpoint_full_state_equal=True)])
        captura['phases'][0]['state_delta']['ranges'][0]['hex'] = '00'
        with self.assertRaises(d.ReplayDivergente):
            d.verificar_replay(captura, s0)


class TestEventosCompactos(unittest.TestCase):
    def test_logical_indices_survive_dropping_written_events(self):
        e = d.EventosCompactos([0, 1, 2])
        e.append(3)
        e.descartar_ate(2)
        self.assertEqual((len(e), e[2:4], e[-1], e[-5:], e[4:4]), (4, [2, 3], 3, [2, 3], []))
        with self.assertRaises(IndexError):
            e[1:3]
        with self.assertRaises(IndexError):
            e[1]
        with self.assertRaises(TypeError):
            list(e)


if __name__ == '__main__':
    unittest.main()
