"""Commit-backed sources; exact immutable evidence in the pinned snapshot.

The proofs read evidence only from the commit-backed snapshot (source_root), so the
checkout is not pinned: research fronts may legitimately extend their evidence files.
"""
import hashlib,json
from pathlib import Path
from pinned_reference import INPUT_REVISION,CHAIN_REVISION,source_root

def verify():
 import os
 if os.environ.get('RL_REFERENCE_PROFILE')=='chain5':
  document=json.loads(Path(__file__).with_name('chain5-reference-pins.json').read_bytes())
  if document['revision']!=CHAIN_REVISION:raise ValueError('Chain5 reference revision')
  for name,digest in document['sha256'].items():
   if hashlib.sha256((source_root()/name).read_bytes()).hexdigest()!=digest:raise ValueError('Chain5 frozen evidence/source changed: '+name)
  return document
 document=json.loads(Path(__file__).with_name('player-reference-pins.json').read_bytes())
 if document['input_revision']!=INPUT_REVISION:raise ValueError('Input port revision identity')
 for path,digest in document['evidence_sha256'].items():
  if hashlib.sha256((source_root()/path).read_bytes()).hexdigest()!=digest:raise ValueError('Original input evidence changed: '+path)
 return document
