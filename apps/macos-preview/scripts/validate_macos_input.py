"""Test A's answer half using original requests; never execute orders or WndProc."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import argparse,collections,hashlib,json,lzma
from macos_scripted_input import ScriptedInput,FrameAnswerMapper,owner_contract,canonical
PROBES=('P1','P2','P3','P6','P7','K1')


def compare_probe(root,name):
    folder=root/'pesquisas-paralelas/missoes/m3';summary=json.loads((folder/'sondas'/name/'resumo.json').read_bytes())
    source=root/summary['input_file'];raw=source.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=summary['input_sha256']:raise ValueError('Probe input hash mismatch: '+name)
    original=ScriptedInput(root,raw);exported=original.export_bytes();roundtrip=ScriptedInput(root,exported).export_bytes()
    log=folder/'sondas'/name/'entradas.jsonl.xz';rows=[json.loads(x) for x in lzma.open(log,'rt')]
    # HWND=0 is an explicit scenario declaration, checked against every native
    # dispatch record below. No expected answer/flag bytes enter the mapper.
    mapper=FrameAnswerMapper(ScriptedInput(root,roundtrip),hwnd=0)
    expected_hash=hashlib.sha256();actual_hash=hashlib.sha256();first=None;counts=collections.Counter();polls=collections.Counter();flags=0
    for index,reference in enumerate(rows):
        frame=reference['frame']
        if frame!=mapper.frame:mapper.begin_frame(frame)
        actual=mapper.poll(reference['kind'],phase=reference['phase'],site=reference['site'],vk=reference.get('vk'))
        expected={k:v for k,v in reference.items() if k!='wndproc_flags_after'}
        flags+=int('wndproc_flags_after' in reference);counts[reference['kind']]+=1;polls[(reference['kind'],reference['site'])]+=1
        expected_hash.update(canonical(expected));actual_hash.update(canonical(actual))
        if actual!=expected and first is None:first=dict(index=index,frame=frame,phase=reference['phase'],site=reference['site'],expected=expected,actual=actual)
    mapper.finish()
    return dict(probe=name,frames=summary['last_frame']-128,answers=len(rows),kinds=dict(counts),poll_sites=[dict(kind=k,site=s,count=n) for (k,s),n in sorted(polls.items())],
                equal=first is None,first_difference=first,roundtrip_equal=exported==roundtrip,input_sha256=hashlib.sha256(raw).hexdigest(),export_sha256=hashlib.sha256(exported).hexdigest(),
                native_log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),expected_answers_sha256=expected_hash.hexdigest(),actual_answers_sha256=actual_hash.hexdigest(),wndproc_state_records_deferred=flags)


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[3]);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():p.error('Refusing to replace proof evidence')
    rows=[compare_probe(a.root,n) for n in PROBES]
    result=dict(schema='rising-lands/macos-test-a-answers/1',owner_contract_sha256=owner_contract(str(a.root.resolve()))[1],rows=rows,equal=all(r['equal'] and r['roundtrip_equal'] for r in rows),
                scope='Declared answers on native-recorded requests; reference answers and WndProc flag stores never feed the mapper',state_hash_half='Separate ABI1.5 state proof: validate_macos_player.py; this answer-only tool performs no state comparison',orders_injected=False)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(canonical(result));print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=1));print([(r['probe'],r['answers'],r['equal'],r['roundtrip_equal']) for r in rows]);return int(not result['equal'])
if __name__=='__main__':sys.exit(main())
