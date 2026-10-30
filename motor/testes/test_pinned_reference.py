"""Legitimate live-source updates do not alter the explicitly ported reference."""
import hashlib
from pathlib import Path
import unittest
from unittest.mock import patch
from pinned_reference import REPO,reference_file,source_root,provenance
from differential import verify_pins
from frame_differential import assert_pins,M1_CAPTURE

class PinnedReferenceTests(unittest.TestCase):
 def test_source_bytes_are_revision_backed_even_if_working_source_changes(self):
  source='ferramentas/estruturas_caminhos.py';actual=REPO/source;fixed=reference_file(source);digest=hashlib.sha256(fixed.read_bytes()).hexdigest();read=Path.read_bytes
  def changed(path):return b'# legitimate subsequent front update\n' if path==actual else read(path)
  with patch.object(Path,'read_bytes',changed):verify_pins({source:digest})
  self.assertNotEqual(fixed,actual)
 def test_original_evidence_corruption_still_fails_exact_pin(self):
  read=Path.read_bytes
  def changed(path):return read(path)+b'\n' if path==M1_CAPTURE else read(path)
  with patch.object(Path,'read_bytes',changed),self.assertRaises(ValueError):assert_pins([M1_CAPTURE])
 def test_snapshot_source_corruption_is_not_accepted(self):
  source='ferramentas/estruturas_caminhos.py';fixed=reference_file(source);digest=hashlib.sha256(fixed.read_bytes()).hexdigest();read=Path.read_bytes
  def changed(path):return b'# changed frozen source\n' if path==fixed else read(path)
  with patch.object(Path,'read_bytes',changed),self.assertRaises(ValueError):verify_pins({source:digest})
 def test_reference_imports_share_the_pinned_root(self):
  import chamadas_quadro_core,estruturas_caminhos
  for module in (chamadas_quadro_core,estruturas_caminhos):self.assertTrue(Path(module.__file__).is_relative_to(source_root()))
  self.assertEqual(provenance()['graphics'],'ce441852bcada750a8f91da8ed3302f1668c4405')

if __name__=='__main__':unittest.main()
