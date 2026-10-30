"""Run requested S1/D1 evidence as separate <=250-frame native lease jobs.

S1: 11000..12250 (harvester death and its 330-step removal).
D1: 11250..11750 (first deaths), then 15250..15700 (last deaths/defeat).
Interval starts match committed DGROUP and whole-state records, not pickle SHA.
Use on the Mac mini after the scenario's resumo.json and snapshots are present.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from ambiente_combate_raid import ROOT


def parse_interval(value):
    try:
        begin, end = map(int, value.split('-'))
    except ValueError:
        raise argparse.ArgumentTypeError('Use START-END, for example 11250-11750') from None
    if begin < 0 or end <= begin:
        raise argparse.ArgumentTypeError('Require 0 <= START < END')
    return begin, end


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('scenario',choices=('S1','D1'))
    p.add_argument('--snapshot-root',type=Path,default=ROOT/'.local')
    p.add_argument('--inicio',type=Path,default=ROOT/'.local/m3/quadro128')
    p.add_argument('--saida-root',type=Path,default=ROOT/'.local/combat-fatal-20261030')
    p.add_argument('--lease',type=Path)
    p.add_argument('--manifest',type=Path)
    p.add_argument('--intervals',type=parse_interval,nargs='+',metavar='START-END',
                   help='Override scenario windows; each is split into jobs of at most 250 frames')
    a=p.parse_args(argv)
    manifest=a.manifest or ROOT/f'pesquisas-paralelas/missoes/m3/sondas/{a.scenario}/resumo.json'
    data=json.loads(manifest.read_bytes())
    source_input=ROOT/data['input_file']
    if hashlib.sha256(source_input.read_bytes()).hexdigest()!=data['input_sha256']:
        raise RuntimeError('Scenario input hash differs from the published native run')
    if a.lease is None:
        a.lease=next((q/'local-data/coordination/heavy_lease.py' for q in (ROOT,*ROOT.parents)
                      if (q/'local-data/coordination/heavy_lease.py').is_file()),None)
    if a.lease is None or not a.lease.is_file():raise RuntimeError('Supply the machine heavy_lease.py with --lease')
    intervals=a.intervals or (((11000,12250),) if a.scenario=='S1' else ((11250,11750),(15250,15700)))
    records=ROOT/f'pesquisas-paralelas/missoes/m3/sondas/{a.scenario}/quadros.jsonl.xz'
    # The alternate --manifest may describe another serialization of the same run.
    # Always anchor its starting state to this checkout's committed scenario record.
    from capturar_janela_fatal_combate import identidade_registrada
    for i,(begin,end) in enumerate(intervals):
        if i and begin<intervals[i-1][1]:p.error('Intervals must be ordered and nonoverlapping')
        if end>data['last_frame']:raise RuntimeError(f'Native scenario ends at {data["last_frame"]}, before requested {end}')
        if str(begin) not in data['snapshots']:raise RuntimeError(f'No published starting snapshot at frame {begin}')
        identidade_registrada(records,begin)
    for begin,end in intervals:
        snapshot=None;current=begin
        while current<end:
            stop=min(end,current+250)
            out=a.saida_root/a.scenario/f'{current:05d}-{stop:05d}'
            command=[sys.executable,str(a.lease),f'combat-{a.scenario.lower()}-{current}-{stop}','--',
                     sys.executable,'-B',str(ROOT/'pesquisas-paralelas/combate/capturar_janela_fatal_combate.py'),
                     '--inicio',str(a.inicio),'--snapshot-root',str(a.snapshot_root),
                     '--snapshot-frame',str(current),
                     '--entrada',str(source_input),'--ate',str(stop),'--saida',str(out),'--execute-sound-bodies']
            if snapshot is None:
                command.extend(('--snapshot-manifest',str(manifest),'--snapshot-records',str(records)))
            else:
                command.extend(('--snapshot',snapshot,'--snapshot-sha256',digest))
            print(json.dumps(dict(scenario=a.scenario,frames=[current,stop],command=command)),flush=True)
            subprocess.run(command,cwd=ROOT,check=True)
            report=json.loads((out/'manifest.json').read_bytes())
            if report['failures'] or report['completed_frame']!=stop or report['incomplete_leaves']:
                raise RuntimeError('Native segment did not complete; no following segment started')
            snapshot=report['end_snapshot']['path'];digest=report['end_snapshot']['sha256'];current=stop


if __name__=='__main__':main()
