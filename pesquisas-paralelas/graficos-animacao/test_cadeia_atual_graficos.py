"""Source-frozen complete P3/P6/P7 replay, with the explicit recorded AffText boundary."""
import json,hashlib,unittest
from pathlib import Path

AQUI=Path(__file__).resolve().parent

class CadeiaAtualGraficos(unittest.TestCase):
    def test_every_current_source_probe_frame_is_equal(self):
        d=json.loads((AQUI/'validacao/cadeia-atual-P3P6P7.json').read_text())
        for name,digest in d['sources_sha256'].items():
            self.assertEqual(hashlib.sha256((AQUI/name).read_bytes()).hexdigest(),digest,name)
        self.assertEqual({w['probe']:w['equal'] for w in d['windows']},dict(P3=3001,P6=2272,P7=3572))
        for w in d['windows']:
            self.assertEqual(w['equal'],w['drawn_total']);self.assertIsNone(w['first_stop'])
            self.assertTrue(all(r['equal'] and r['stop'] is None and r['logic_stop'] is None
                and r['pixel_mismatches']==r['argument_mismatches']==0 and not r['effect_mismatches']
                and r['sha256']==r['native_sha256'] for r in w['rows']))
