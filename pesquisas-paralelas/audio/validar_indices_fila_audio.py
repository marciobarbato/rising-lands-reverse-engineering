"""Fresh three-way native/Python/committed queue-index comparison. Use the lease."""
import argparse
import json
import hashlib
from pathlib import Path
import sys
from ambiente_audio import OWNED
sys.path.insert(0,str(OWNED/'testes'))
from test_indices_fila_audio import compare_cases


def original_capture():
    # Keep --help and output preflight independent of optional native imports.
    from capturar_indices_fila_audio import capture
    return capture()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path,
                        help='Fresh report path; relative paths use the current working directory.')
    args=parser.parse_args(argv)
    path=args.output
    if path.exists() or path.is_symlink():
        parser.error('Refusing to overwrite native report: '+str(path))
    path.parent.mkdir(parents=True,exist_ok=True)
    committed=json.loads((OWNED/'evidencias/captura-indices-fila-audio-original.json').read_text())
    fresh=original_capture()
    if fresh['cases']!=committed['cases']:raise ValueError('Fresh original capture differs from committed evidence')
    compare_cases(fresh)
    report=dict(schema='rising-lands/audio-waiting-slot-three-way/1',passed=True,native_calls=fresh['native_calls'],
                original_capture_equal=True,python_equal=True,seconds=fresh['seconds'],
                capture_commit='679bd00',implementation='indices_fila_audio.py',
                implementation_sha256=hashlib.sha256((OWNED/'indices_fila_audio.py').read_bytes()).hexdigest())
    with path.open('x') as output:
        output.write(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':main()
