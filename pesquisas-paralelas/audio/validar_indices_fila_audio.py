"""Fresh three-way native/Python/committed queue-index comparison. Use the lease."""
import json
import hashlib
from pathlib import Path
import sys
from ambiente_audio import OWNED
from capturar_indices_fila_audio import capture
sys.path.insert(0,str(OWNED/'testes'))
from test_indices_fila_audio import compare_cases


def main():
    committed=json.loads((OWNED/'evidencias/captura-indices-fila-audio-original.json').read_text())
    fresh=capture()
    if fresh['cases']!=committed['cases']:raise ValueError('Fresh original capture differs from committed evidence')
    compare_cases(fresh)
    path=OWNED/'validacao/indices-fila-audio-native.json'
    if path.exists():raise ValueError('Refusing to overwrite native report')
    report=dict(schema='rising-lands/audio-waiting-slot-three-way/1',passed=True,native_calls=fresh['native_calls'],
                original_capture_equal=True,python_equal=True,seconds=fresh['seconds'],
                capture_commit='679bd00',implementation='indices_fila_audio.py',
                implementation_sha256=hashlib.sha256((OWNED/'indices_fila_audio.py').read_bytes()).hexdigest())
    path.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))


if __name__=='__main__':main()
