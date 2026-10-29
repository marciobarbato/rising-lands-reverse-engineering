"""The committed M2.2 128-frame equality proof (validacao/m2-2-prova-128-quadros.json)."""
import hashlib
import json
from pathlib import Path
import unittest

OWNED = Path(__file__).resolve().parents[1]
ROOT = OWNED.parents[1]
PROVA = json.loads((OWNED / 'validacao/m2-2-prova-128-quadros.json').read_text())


class Proof128Frames(unittest.TestCase):
    def test_clean_tree_and_committed_inputs(self):
        self.assertEqual(PROVA['source_dirty_paths'], [])
        for chave in ('capture', 'policy'):
            ref = PROVA[chave]
            self.assertEqual(hashlib.sha256((ROOT / ref['path']).read_bytes()).hexdigest(), ref['sha256'], chave)
        self.assertEqual(PROVA['capture']['raw_json_sha256'], PROVA['capture']['raw_json_sha256_pinned'])
        self.assertEqual(PROVA['policy']['format'], 'cumulative')

    def test_every_phase_equal(self):
        self.assertEqual(PROVA['summary']['result'], 'equal')
        self.assertEqual(len(PROVA['phases']), 257)
        for nome, r in PROVA['phases'].items():
            with self.subTest(nome):
                self.assertTrue(r['equal'])
                self.assertTrue(r['reference_integrity']['summary_equal'])
                for chave in ('state', 'rng', 'bindings', 'boundaries', 'allocation_count'):
                    self.assertTrue(r[chave]['equal'], chave)
                self.assertTrue(all(v['equal'] for v in r.get('registers', {}).values()))
                self.assertTrue(all(v['equal'] for v in r.get('carried_entry_registers', {}).values()))
        self.assertTrue(PROVA['allocation_records']['equal'])
        self.assertEqual(len(PROVA['capture']['checkpoint_full_states']), 11)

    def test_no_crossing_and_hud(self):
        self.assertEqual(PROVA['crossings']['writing_compared_bytes'], 0)
        self.assertEqual(len(PROVA['hud_flag']), 128)
        self.assertTrue(all(h['equal'] and not h['masked'] for h in PROVA['hud_flag']))


if __name__ == '__main__':
    unittest.main()
