"""Sustained real-window benchmark; invoke through heavy_lease.py --exclusive."""
import argparse
import json
from pathlib import Path
import subprocess


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--app',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--mode',choices=('play','test'),default='play')
    p.add_argument('--game-fps',type=float,default=0)
    p.add_argument('--orders',action='store_true',help='Dispatch actual AppKit selection and movement clicks')
    p.add_argument('--orders-selected',action='store_true',help='Reproduce the original selected-actor workload: clicks at 8/8.2 seconds, pointer at 8.5; no deselection')
    p.add_argument('--seconds',type=float,default=65)
    a=p.parse_args()
    if not 60<=a.seconds<=180:p.error('The sustained measurement requires 60..180 seconds')
    if not 0<=a.game_fps<=120:p.error('Game rate must be 0 (unlimited)..120')
    if a.output.exists():p.error('Refusing to overwrite benchmark evidence')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    command=['open','-W','-n',str(a.app),'--args','--inspection','--native-benchmark',str(a.output),
             '--benchmark-mode',a.mode,'--benchmark-seconds',str(a.seconds),'--game-fps',str(a.game_fps)]
    if a.orders and a.orders_selected:p.error('Choose one order workload')
    if a.orders or a.orders_selected:command.append('--benchmark-orders')
    if a.orders_selected:command.append('--benchmark-orders-selected')
    result=subprocess.run(command,capture_output=True,text=True,timeout=a.seconds+90)
    a.output.with_suffix('.launch.log').write_text(result.stdout+result.stderr)
    if result.returncode or not a.output.exists():raise RuntimeError('NativeBenchmarkLaunchFailed: '+str(result.returncode))
    report=json.loads(a.output.read_text())
    if not report.get('passed'):raise RuntimeError('NativeBenchmarkFailed: '+json.dumps(report))
    metrics=report['native_metrics']
    assert metrics['seconds']>=60 and len(metrics['oneSecondPresentations'])>=60
    if a.orders or a.orders_selected:
        assert a.mode=='play' and metrics['humanEvents']>=4 and metrics['declaredFrames']>0
        assert 1 in report['benchmark_order_tags'] and 5 in report['benchmark_order_tags']
    if a.mode=='play':
        assert metrics['proofSeconds']==0
        assert report['verified_phases']==report['verified_checkpoints']==report['verified_surfaces']==0
        assert metrics['displayError'] is None
    else:
        assert report['verified_phases']==257 and report['verified_checkpoints']==11
        assert report['verified_surfaces']>=128
    print(json.dumps({k:v for k,v in report.items() if k not in ('phases','memory')},indent=2))


if __name__=='__main__':main()
