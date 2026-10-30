"""Commit-backed sources; exact immutable evidence in both snapshot and checkout."""
import hashlib,json
from pathlib import Path
from pinned_reference import REPO,INPUT_REVISION,source_root

def verify():
 document=json.loads(Path(__file__).with_name('player-reference-pins.json').read_bytes())
 if document['input_revision']!=INPUT_REVISION:raise ValueError('Input port revision identity')
 revision_backed=document.get('revision_backed_evidence',{})
 if set(revision_backed)-set(document['evidence_sha256']):raise ValueError('Unknown revision-backed evidence')
 for path,digest in document['evidence_sha256'].items():
  fixed=revision_backed.get(path)
  if fixed and fixed['revision']!=INPUT_REVISION:raise ValueError('Evidence revision differs from pinned input reference')
  for root in ((source_root(),) if fixed else (REPO,source_root())):
   if hashlib.sha256((root/path).read_bytes()).hexdigest()!=digest:raise ValueError('Original input evidence changed: '+path)
 return document
