"""M3 provider and request-stream replay, with optional fresh native leaves.

Trace-driven stream validation does not reconstruct game emitters or accept M3.
The source remains the immutable Missions boundary events, not a new oracle.
"""
import argparse
from collections import Counter
import hashlib
import json
import lzma
from pathlib import Path

import ambiente_audio
from ambiente_audio import ROOT, OWNED
from audio_queue_fixtures import QueueFixtureMemory
from provedor_pedidos_m3_audio import SoundRequestProvider, OPERATIONS
from fluxo_pedidos_audio import AudioRequestStream, from_boundaries, compare_streams


def sha(data): return hashlib.sha256(data).hexdigest()


def provider_replay():
    original=json.loads((OWNED/'evidencias/m3-pedidos-original-v1.json').read_bytes())
    failures=[]; count=0
    for case in original['cases']:
        f=case['input']; m=QueueFixtureMemory.restore(f['memory'])
        p=SoundRequestProvider(m,domain='unopened-display')
        name=next(k for k,v in OPERATIONS.items() if v==f['operation'])
        value=p(name,f['regs'],f['arguments']); count+=1
        if value!=int(case['eax'],16) or m.snapshot()!=case['output']:
            failures.append(dict(case=case['name'],field='EAX or full memory'))
    initialized=0; scenarios=0
    for artifact in ('captura-fila-audio-original-v9.json','captura-continuacao-audio-original-v3.json',
                     'captura-dictador-audio-original-v3.json'):
        document=json.loads((OWNED/'evidencias'/artifact).read_bytes())
        for case in document['cases']:
            f=case['input']; requests=f.get('sequence',[f])
            if case['stop'] or requests[0]['operation'] not in OPERATIONS.values(): continue
            m=QueueFixtureMemory.restore(f['memory'])
            p=SoundRequestProvider(m,domain='captured-initialized',capture=(artifact,case['name']))
            scenarios+=1
            for i,request in enumerate(requests):
                if request['operation'] not in OPERATIONS.values(): break
                name=next(k for k,v in OPERATIONS.items() if v==request['operation'])
                value=p(name,request['regs'],request['arguments']); initialized+=1
                expected=case['steps'][i] if 'sequence' in f else dict(eax=case['eax'],memory=case['output'])
                if value!=int(expected['eax'],16) or m.snapshot()!=expected['memory']:
                    failures.append(dict(artifact=artifact,case=case['name'],step=i,field='EAX or full memory'))
                if i==len(requests)-1 and (p.plan.calls!=case['com'] or len(p.plan.responses)!=case['unused_com']):
                    failures.append(dict(artifact=artifact,case=case['name'],field='platform transcript'))
    return dict(display_calls=count,initialized_calls=initialized,initialized_scenarios=scenarios,
                mismatches=len(failures),failures=failures)


def stream_replay(phases):
    expected=from_boundaries(phases)
    f=json.loads((OWNED/'evidencias/m3-pedidos-original-v1.json').read_bytes())['cases'][0]['input']
    m=QueueFixtureMemory.restore(f['memory']);stream=AudioRequestStream()
    p=SoundRequestProvider(m,domain='unopened-display',stream=stream)
    returns=Counter()
    for phase in phases:
        for e in phase['boundaries']:
            if e['routine'] not in OPERATIONS: continue
            count=1 if e['routine']=='PlaySnd_PostSound' else 0
            p.phase,p.caller_return=phase['phase'],e['caller_return']
            # The accepted no-input windows contain no post/stop. If a future
            # artifact adds one, its live caller-state capture is required.
            if e['routine']!='PlaySnd_Manage': raise ValueError('Window needs captured live caller handle state')
            returns[p(e['routine'],{k:int(v,16) for k,v in e['registers'].items()},
                      [int(v,16) for v in e['stack_words'][:count]])]+=1
    result=compare_streams(expected,stream.document())
    result.pop('differences')
    return result,stream.document(),dict(returns)


def validate_windows():
    paths=[ROOT/'pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz']
    manifest_path=ROOT/'pesquisas-paralelas/missoes/evidencias/m2-3/captura-quadros9200-monde01-exibicao-v2.manifest.json'
    manifest=json.loads(manifest_path.read_bytes())
    result=[]; whole=AudioRequestStream()
    for index,path in enumerate(paths+[ROOT/p['artifact'] for p in manifest['parts']]):
        compressed=path.read_bytes(); raw=lzma.decompress(compressed)
        if index:
            identity=manifest['parts'][index-1]
            if (sha(compressed),sha(raw))!=(identity['compressed_sha256'],identity['raw_sha256']):
                raise ValueError('M2.3 part identity differs')
        doc=json.loads(raw); comparison,stream,returns=stream_replay(doc['phases'])
        result.append(dict(artifact=str(path.relative_to(ROOT)),compressed_sha256=sha(compressed),raw_sha256=sha(raw),
                           phases=len(doc['phases']),comparison=comparison,provider_return_counts=returns,
                           routine_counts=dict(Counter(e['routine'] for e in stream['events']))))
        if index:
            for e in stream['events']:
                whole.append(e['phase'],e['caller_return'],e['routine'],e['registers'],e['stack_words'])
        else: m22=stream
    # Independent source prefix check: the M2.3 stream starts with exactly the
    # accepted M2.2 events, despite the different capture packaging.
    prefix=dict(schema=whole.document()['schema'],events=whole.events[:len(m22['events'])])
    golden=json.loads((OWNED/'evidencias/m3-fluxo-original-proveniencia.json').read_bytes())
    golden_checks=[]
    for identity,actual in zip(golden['outputs'],(m22,whole.document())):
        compressed=(ROOT/identity['artifact']).read_bytes();raw=lzma.decompress(compressed)
        if (sha(compressed),sha(raw))!=(identity['compressed_sha256'],identity['raw_sha256']):
            raise ValueError('Committed original stream identity differs')
        golden_checks.append(compare_streams(json.loads(raw),actual))
    return dict(method='Trace-driven raw Missions boundaries -> provider recorder -> exact semantic stream comparator',
                m22=result[0],m23_parts=result[1:],m23_events=len(whole.events),
                m22_prefix_comparison=compare_streams(m22,prefix),
                committed_stream_comparisons=golden_checks,
                raid_window=result[-1],
                limitation='No PostSound occurs in either accepted no-input window. Emitter logic is not rerun by this transport test.')


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--native',action='store_true')
    a=p.parse_args()
    if a.output.exists(): raise ValueError('Refusing report overwrite')
    report=dict(schema='rising-lands/audio-m3-validation/1',provider=provider_replay(),windows=validate_windows())
    if a.native:
        from capturar_pedidos_m3_audio import leaves
        frozen=json.loads((OWNED/'evidencias/m3-pedidos-original-v1.json').read_bytes())
        frozen.pop('seconds')
        fresh=leaves()
        report['fresh_native_display']=dict(cases=len(fresh['cases']),equal=fresh==frozen)
    report['source_sha256']={name:sha((OWNED/name).read_bytes()) for name in
        ('fila_audio.py','provedor_pedidos_m3_audio.py','fluxo_pedidos_audio.py','validar_pedidos_m3_audio.py')}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=1)+'\n')
    print(json.dumps(dict(provider=report['provider'],m23_events=report['windows']['m23_events'],
                         native=report.get('fresh_native_display'))),flush=True)
    if report['provider']['mismatches'] or any(not v['comparison']['equal'] for v in [report['windows']['m22']]+report['windows']['m23_parts']):
        raise SystemExit(1)
    if any(not v['equal'] for v in report['windows']['committed_stream_comparisons']):raise SystemExit(1)
    if a.native:
        from encerramento_captura import encerrar_captura
        encerrar_captura(0 if report['fresh_native_display']['equal'] else 1,a.output)


if __name__=='__main__': main()
