"""Commit-backed sources; exact immutable evidence in the pinned snapshot.

The proofs read evidence only from the commit-backed snapshot (source_root), so the
checkout is not pinned: research fronts may legitimately extend their evidence files.
"""
import hashlib,json
from pathlib import Path
from pinned_reference import INPUT_REVISION,CHAIN_REVISION,CHAIN6_GRAPHICS_REVISION,CHAIN7_REVISION,CHAIN8_REVISION,source_root

def verify():
 import os
 if os.environ.get('RL_REFERENCE_PROFILE')in ('chain5','chain6','chain7','chain8'):
  profile=os.environ['RL_REFERENCE_PROFILE']
  document=json.loads(Path(__file__).with_name(profile+'-reference-pins.json').read_bytes())
  if document['revision']!=(CHAIN8_REVISION if profile=='chain8'else CHAIN7_REVISION if profile=='chain7'else CHAIN_REVISION):raise ValueError('Chain reference revision')
  if profile in ('chain6','chain7','chain8')and document['graphics_revision']!=(CHAIN8_REVISION if profile=='chain8'else CHAIN6_GRAPHICS_REVISION):raise ValueError('Chain6 Graphics revision')
  for name,digest in document['sha256'].items():
   if hashlib.sha256((source_root()/name).read_bytes()).hexdigest()!=digest:raise ValueError('Chain5 frozen evidence/source changed: '+name)
  return document
 document=json.loads(Path(__file__).with_name('player-reference-pins.json').read_bytes())
 if document['input_revision']!=INPUT_REVISION:raise ValueError('Input port revision identity')
 for path,digest in document['evidence_sha256'].items():
  if hashlib.sha256((source_root()/path).read_bytes()).hexdigest()!=digest:raise ValueError('Original input evidence changed: '+path)
 return document
