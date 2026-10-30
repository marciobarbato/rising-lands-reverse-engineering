"""Comparison must expose divergent, absent and incompatible replay frames."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'apps/macos-preview/src'))
from macos_test_b import compare, load_rows


class TestBComparisonTests(unittest.TestCase):
    def prepare(self, directory):
        dirs=[Path(directory)/p for p in ('app','original')]
        for p in dirs:
            p.mkdir()
            (p/'manifest.json').write_text(json.dumps(dict(input_sha256='input',hash_contract={'mask':'same'},stop_frame=131,status='completed')))
            (p/'states.jsonl').write_text(''.join(json.dumps(dict(frame=k,state_sha256=str(k),indicator_sha256=str(k),blocks=2,bytes=100,indicators={'counter':k}))+'\n' for k in range(129,132)))
        return dirs

    def test_all_frames_equal_and_prefix(self):
        with tempfile.TemporaryDirectory() as d:
            aa,oo=self.prepare(d)
            self.assertTrue(compare(aa,oo)['passed'])
            self.assertEqual(compare(aa,oo,130)['frames_equal'],2)

    def test_every_divergence_and_missing_frame_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            aa,oo=self.prepare(d)
            rows=load_rows(aa/'states.jsonl');rows[130]['state_sha256']='wrong'
            (aa/'states.jsonl').write_text('\n'.join(json.dumps(rows[k]) for k in (129,130)))
            r=compare(aa,oo)
            self.assertFalse(r['passed']);self.assertEqual([v['frame'] for v in r['differences']],[130,131])
            self.assertEqual(r['frames_equal'],1)

    def test_identity_and_duplicate_frames_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            aa,oo=self.prepare(d)
            m=json.loads((aa/'manifest.json').read_text());m['input_sha256']='other'
            (aa/'manifest.json').write_text(json.dumps(m))
            with self.assertRaisesRegex(ValueError,'identity'):compare(aa,oo)
            text=(oo/'states.jsonl').read_text();(oo/'states.jsonl').write_text(text+text.splitlines()[0]+'\n')
            with self.assertRaisesRegex(ValueError,'Duplicate'):load_rows(oo/'states.jsonl')
