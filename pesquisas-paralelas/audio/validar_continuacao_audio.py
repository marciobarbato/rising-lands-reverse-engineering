"""Fresh native/Python/frozen Audio continuation differential; run under lease."""
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
    from capturar_continuacao_audio import capture
    original=json.loads((OWNED/'evidencias/captura-continuacao-audio-original-v3.json').read_text());fresh=capture()
    failures=[];original_equal=fresh['cases']==original['cases']
    for case in fresh['cases']:
        try:errors,_=compare(case)
        except Exception as exc:errors=[type(exc).__name__+': '+str(exc)]
        if errors:failures.append(dict(case=case['name'],differences=errors))
    report=dict(schema='rising-lands/audio-continuation-three-way/1',passed=original_equal and not failures,
                original_capture_equal=original_equal,original_native_calls=fresh['native_calls'],scenarios=fresh['scenarios'],
                dependency_stops=sum(c['stop'] is not None for c in fresh['cases']),failures=failures,seconds=fresh['seconds'],
                source_sha256={name:hashlib.sha256((OWNED/name).read_bytes()).hexdigest() for name in
                               ('fila_audio.py','reproduzir_fila_audio.py','capturar_continuacao_audio.py')})
    if not original_equal:report['fresh_original_cases']=fresh['cases']
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as output:json.dump(report,output,indent=2);output.write('\n')
    print(json.dumps({k:v for k,v in report.items() if k!='fresh_original_cases'}))
    if not report['passed']:raise SystemExit(1)


if __name__=='__main__':main()
