"""Fresh original/Python/frozen queue comparison. Native execution requires lease."""
import argparse
import hashlib
import json
from pathlib import Path
from ambiente_audio import OWNED
from reproduzir_fila_audio import compare


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();path=args.output
    if path.exists() or path.is_symlink():parser.error('Refusing to overwrite report')
    from capturar_fila_audio import capture
    original=json.loads((OWNED/'evidencias/captura-fila-audio-original-v7.json').read_text())
    fresh=capture()
    if fresh['cases']!=original['cases']:raise ValueError('Fresh original cases differ from frozen v7 evidence')
    failures=[]
    for case in fresh['cases']:
        errors,_=compare(case)
        if errors:failures.append(dict(case=case['name'],differences=errors))
    report=dict(schema='rising-lands/audio-queue-three-way/1',passed=not failures,native_calls=fresh['native_calls'],
                scenarios=fresh['scenario_count'],expected_dependency_stops=sum(c['stop'] is not None for c in fresh['cases']),
                unexpected_failures=failures,original_capture_equal=True,seconds=fresh['seconds'],
                implementation_sha256=hashlib.sha256((OWNED/'fila_audio.py').read_bytes()).hexdigest())
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as output:json.dump(report,output,indent=2);output.write('\n')
    print(json.dumps(report))
    if failures:raise SystemExit(1)


if __name__=='__main__':main()
