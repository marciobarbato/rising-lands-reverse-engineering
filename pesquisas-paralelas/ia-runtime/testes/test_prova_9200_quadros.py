"""The committed M2.3 9,200-frame equality proof (validacao/m2-3-prova-9200-quadros.json) and its table helpers."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
ROOT = OWNED.parents[1]
sys.path.insert(0, str(OWNED))
import ambiente_ia_runtime  # noqa: E402,F401
import provar_quadros_9200_ia as pq  # noqa: E402

PROVA = json.loads((OWNED / 'validacao/m2-3-prova-9200-quadros.json').read_text())


def sha(caminho):
    return hashlib.sha256((ROOT / caminho).read_bytes()).hexdigest()


class Proof9200Frames(unittest.TestCase):
    def test_clean_tree_and_committed_inputs(self):
        self.assertEqual(PROVA['source_dirty_paths'], [])
        self.assertEqual(PROVA['capture']['manifest']['sha256'], pq.SHA_MANIFESTO)
        self.assertEqual(sha(pq.MANIFESTO), pq.SHA_MANIFESTO)
        self.assertEqual(sha(PROVA['policy']['path']), PROVA['policy']['sha256'])
        for parte in PROVA['capture']['parts']:
            self.assertEqual(sha(parte['artifact']), parte['compressed_sha256'], parte['part'])

    def test_every_phase_equal(self):
        s = PROVA['summary']
        self.assertEqual(s['result'], 'equal')
        self.assertEqual((s['phases'], s['phases_equal'], s['parts_equal']), (18401, 18401, 10))
        e = PROVA['equality']
        for chave in ('state', 'compared_summary', 'rng', 'bindings_outside_display', 'boundaries_outside_display',
                      'allocation_count'):
            self.assertEqual(e[chave], dict(equal=18401, checked=18401), chave)
        self.assertEqual(e['between_frames_exit_registers'], dict(equal=9200, checked=9200))
        self.assertEqual(e['carried_entry_registers']['equal'], e['carried_entry_registers']['checked'])
        self.assertEqual(e['hud_flag'], dict(equal=9200, checked=9200))
        self.assertEqual(e['reference_integrity']['compared_summary'], 18401)
        self.assertEqual(e['reference_integrity']['masked_sha256'], 18401)
        self.assertEqual(e['reference_integrity']['full_states'], ['frame8999', 'frame9000', 'frame9176'])
        self.assertTrue(PROVA['allocation_records']['final']['equal'])
        self.assertEqual(PROVA['allocation_records']['final']['reference'], 25482)
        self.assertFalse(PROVA['problems'])

    def test_phase_table_covers_every_phase_equal(self):
        t = PROVA['phase_table']
        self.assertEqual(sum(r[2] for r in t['runs']), 9200)
        self.assertEqual([t['runs'][0][0], t['runs'][-1][1]], [1, 9200])
        self.assertTrue(all(b[1] == a[0] - 1 for b, a in zip(t['runs'], t['runs'][1:])))
        igual = t['columns'].index('equal')
        self.assertTrue(t['load_tail'][igual])
        self.assertTrue(all(r[3][igual] and r[4][igual] for r in t['runs']))

    def test_no_crossing_and_raid_phases_kept(self):
        self.assertEqual((PROVA['crossings']['count'], PROVA['crossings']['writing_compared_bytes']), (0, 0))
        for nome in ('frame9000', 'frame9176', 'frame9177', 'frame9178', 'frame9179'):
            self.assertTrue(PROVA['phases'][nome]['equal'], nome)

    def test_parts_ran_the_same_code(self):
        self.assertEqual(len({json.dumps(p['machine'], sort_keys=True) for p in PROVA['parts']}), 1)
        self.assertIn('pesquisas-paralelas/ia-runtime/comparar_quadros_ia.py', PROVA['code_sha256'])


class Helpers(unittest.TestCase):
    def fase(self, igual=True, bytes_=10):
        return dict(equal=igual, state=dict(compared_bytes=bytes_, equal=igual),
                    compared_summary=dict(python='a', equal=igual), rng=dict(python={'0x497164': '0x1'}, equal=True),
                    bindings=dict(equal=True, display_context_not_modeled=1, shared_issuers_matched=[]),
                    boundaries=dict(equal=True, display_context_not_modeled=[], shared_issuers_matched=[]),
                    allocation_count=dict(python=3, equal=True), reference_integrity=dict(form='delta',
                                                                                        summary_equal=True))

    def test_run_length_table(self):
        fases = {'load_tail': self.fase(), 'between_frames': self.fase(), 'frame1': self.fase(),
                 'between_frames2': self.fase(), 'frame2': self.fase(), 'between_frames3': self.fase(),
                 'frame3': self.fase(bytes_=11), 'between_frames4': self.fase(), 'frame4': self.fase(bytes_=11)}
        t = pq.tabela_rle(fases, {})
        self.assertEqual([r[:3] for r in t['runs']], [[1, 2, 2], [3, 4, 2]])
        self.assertIn('load_tail', t)
        t = pq.tabela_rle({'between_frames2': self.fase(), 'frame2': self.fase(), 'between_frames3': self.fase(),
                           'frame3': self.fase(igual=False)}, {})
        self.assertEqual([r[:3] for r in t['runs']], [[2, 2, 1], [3, 3, 1]])

    def test_phase_chain_depends_on_every_phase(self):
        a = {'frame1': self.fase(), 'frame2': self.fase()}
        b = {'frame1': self.fase(), 'frame2': dict(self.fase(), compared_summary=dict(python='b'))}
        self.assertNotEqual(pq.cadeia_fases(a), pq.cadeia_fases(b))
        self.assertEqual(pq.cadeia_fases(a), pq.cadeia_fases(dict(a)))


if __name__ == '__main__':
    unittest.main()
