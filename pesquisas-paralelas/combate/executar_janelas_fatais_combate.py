"""Run requested S1/D1 evidence as separate <=250-frame native lease jobs.

S1: 11000..12250 (harvester death and its 330-step removal).
D1: 11000..12000 (raider death), then 17000..17500 (last deaths/recount).
Only existing, SHA-verified Missions snapshots and their input prefix are used.
Use on the Mac mini after the scenario's resumo.json and snapshots are present.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from ambiente_combate_raid import ROOT


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('scenario',choices=('S1','D1'))
    p.add_argument('--snapshot-root',type=Path,default=ROOT/'.local')
    p.add_argument('--inicio',type=Path,default=ROOT/'.local/m3/quadro128')
    p.add_argument('--saida-root',type=Path,default=ROOT/'.local/combat-fatal-20261030')
    p.add_argument('--lease',type=Path)
    p.add_argument('--manifest',type=Path)
    a=p.parse_args()
    manifest=a.manifest or ROOT/f'pesquisas-paralelas/missoes/m3/sondas/{a.scenario}/resumo.json'
    data=json.loads(manifest.read_bytes())
    source_input=ROOT/data['input_file']
    if hashlib.sha256(source_input.read_bytes()).hexdigest()!=data['input_sha256']:
        raise RuntimeError('Scenario input hash differs from the published native run')
    if a.lease is None:
        a.lease=next((q/'local-data/coordination/heavy_lease.py' for q in (ROOT,*ROOT.parents)
                      if (q/'local-data/coordination/heavy_lease.py').is_file()),None)
    if a.lease is None or not a.lease.is_file():raise RuntimeError('Supply the machine heavy_lease.py with --lease')
    intervals=((11000,12250),) if a.scenario=='S1' else ((11000,12000),(17000,17500))
    for begin,end in intervals:
        if end>data['last_frame']:raise RuntimeError(f'Native scenario ends at{data["last_frame"]}, before requested{end}')
        digest=data['snapshots'][str(begin)]['sha256'];snapshot=None;current=begin
        while current<end:
            stop=min(end,current+250)
            out=a.saida_root/a.scenario/f'{current:05d}-{stop:05d}'
            command=[sys.executable,str(a.lease),f'combat-{a.scenario.lower()}-{current}-{stop}','--',
                     sys.executable,'-B',str(ROOT/'pesquisas-paralelas/combate/capturar_janela_fatal_combate.py'),
                     '--inicio',str(a.inicio),'--snapshot-root',str(a.snapshot_root),
                     '--snapshot-frame',str(current),'--snapshot-sha256',digest,
                     '--entrada',str(source_input),'--ate',str(stop),'--saida',str(out),'--execute-sound-bodies']
            if snapshot is not None:command.extend(('--snapshot',snapshot))
            print(json.dumps(dict(scenario=a.scenario,frames=[current,stop],command=command)),flush=True)
            subprocess.run(command,cwd=ROOT,check=True)
            report=json.loads((out/'manifest.json').read_bytes())
            if report['failures'] or report['completed_frame']!=stop or report['incomplete_leaves']:
                raise RuntimeError('Native segment did not complete; no following segment started')
            snapshot=report['end_snapshot']['path'];digest=report['end_snapshot']['sha256'];current=stop


if __name__=='__main__':main()
