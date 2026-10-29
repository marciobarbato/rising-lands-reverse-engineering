"""Project immutable original boundary arguments into stream v1; no emulation."""
import hashlib
import json
import lzma
from pathlib import Path

from ambiente_audio import ROOT, OWNED, ORIGINAL_SHA256
from fluxo_pedidos_audio import AudioRequestStream, from_boundaries


def sha(data): return hashlib.sha256(data).hexdigest()


def export():
    from audio_m22_soundness import CAPTURE, CAPTURE_SHA, RAW_SHA
    manifest_path=ROOT/'pesquisas-paralelas/missoes/evidencias/m2-3/captura-quadros9200-monde01-exibicao-v2.manifest.json'
    manifest=json.loads(manifest_path.read_bytes());sources=[];m23=AudioRequestStream()
    for i,identity in enumerate([dict(artifact=str(CAPTURE.relative_to(ROOT)),compressed_sha256=CAPTURE_SHA,raw_sha256=RAW_SHA)]+manifest['parts']):
        path=ROOT/identity['artifact'];compressed=path.read_bytes();raw=lzma.decompress(compressed)
        if (sha(compressed),sha(raw))!=(identity['compressed_sha256'],identity['raw_sha256']):raise ValueError('Original source identity differs')
        source=from_boundaries(json.loads(raw)['phases'])
        sources.append({k:identity[k] for k in ('artifact','compressed_sha256','raw_sha256')})
        if i==0:m22=source
        else:
            for e in source['events']:m23.append(e['phase'],e['caller_return'],e['routine'],e['registers'],e['stack_words'])
    outputs=[]
    for label,document in (('m22',m22),('m23',m23.document())):
        raw=(json.dumps(document,sort_keys=True,separators=(',',':'))+'\n').encode()
        compressed=lzma.compress(raw,preset=6)
        path=OWNED/f'evidencias/m3-fluxo-{label}-original.json.xz'
        with path.open('xb') as output:output.write(compressed)
        outputs.append(dict(artifact=str(path.relative_to(ROOT)),events=len(document['events']),
                            raw_sha256=sha(raw),compressed_sha256=sha(compressed)))
    result=dict(schema='rising-lands/audio-request-stream-provenance/1',original_sha256=ORIGINAL_SHA256,
                method='Projection of argument registers/words, callsite and order from immutable native boundary logs; no engine translation',
                source_manifest_sha256=sha(manifest_path.read_bytes()),sources=sources,outputs=outputs,
                exporter_sha256=sha(Path(__file__).read_bytes()),projector_sha256=sha((OWNED/'fluxo_pedidos_audio.py').read_bytes()))
    path=OWNED/'evidencias/m3-fluxo-original-proveniencia.json'
    with path.open('x') as output:json.dump(result,output,indent=1);output.write('\n')
    print(json.dumps(outputs))


if __name__=='__main__':export()
