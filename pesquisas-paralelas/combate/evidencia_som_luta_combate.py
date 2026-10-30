"""Lossless shared-anchor encoding for the original S1 sound parent states.

The raw original capture is retained unchanged under .local. This creates a
new artifact; each parent's exact entry bytes are rebuilt and checked before
writing. No native state, request or historical evidence is changed.
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path

from ambiente_combate_raid import ROOT
from delta_estado_missao import _decodificar, aplicar, delta, resumo


def decode(blocks):
    return {n:(int(v['base'],16),_decodificar(v)) for n,v in blocks.items()}


def compact(source, destination):
    source,destination=Path(source),Path(destination)
    if destination.exists(): raise ValueError('Refusing to overwrite original evidence')
    raw=source.read_bytes()
    data=json.loads(lzma.decompress(raw))
    anchor=decode(data['cases'][0]['full_state_before'])
    data['state_anchor']=data['cases'][0]['full_state_before']
    for i,case in enumerate(data['cases']):
        before=decode(case.pop('full_state_before'))
        case['entry_delta']=delta(anchor,before)
        rebuilt=aplicar(anchor,case['entry_delta'],f'case{i}')
        if rebuilt!=before: raise ValueError(f'Lossy entry encoding: {i}')
        case['state_before']=resumo(before)
    data['schema']='rising-lands/combat-s1-sound-original/2'
    data['lossless_encoding']=dict(raw_capture_sha256=hashlib.sha256(raw).hexdigest(),
                                  method='one exact full-state anchor and per-parent exact entry deltas',
                                  encoder_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    with lzma.open(destination,'xt',preset=6) as f: json.dump(data,f,sort_keys=True)
    return dict(path=str(destination),cases=len(data['cases']),bytes=destination.stat().st_size,
                sha256=hashlib.sha256(destination.read_bytes()).hexdigest())


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source',type=Path);ap.add_argument('destination',type=Path)
    args=ap.parse_args();print(json.dumps(compact(args.source,args.destination)))
