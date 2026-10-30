"""Test A state half through the app mapper and production C phase entry.

Simulation proof deliberately omits rendering; UI render stops are separate.
World starts at S0 and is never replaced with frame128 or any later oracle state.
"""
from pathlib import Path
import argparse,ctypes as C,hashlib,json,lzma,os,sys,time,signal
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from macos_native_driver import NativeDriver
from macos_scripted_input import ScriptedInput,FrameAnswerMapper,canonical


def proof(a):
    os.environ['RL_REFERENCE_PROFILE']='input'
    sys.path.insert(0,str(a.root/'motor/testes'))
    from player_proof import SOURCE,Memory,estado_quadro128,indicadores,comparar_quadro,eventos_referencia,canonical_orders
    from player_abi import Player,inputs,orders
    from player_pins import verify
    from player_state_evidence import WholeState
    from pinned_reference import provenance
    verify()
    base=SOURCE/'pesquisas-paralelas/missoes/m3';raw=(base/'entradas'/f'{a.probe}.json').read_bytes()
    script=ScriptedInput(a.root,raw);mapper=FrameAnswerMapper(ScriptedInput(a.root,script.export_bytes()),hwnd=0)
    rows=lambda name:[json.loads(x) for x in lzma.open(base/'sondas'/a.probe/name,'rt')]
    reference={r['frame']:r for r in rows('quadros.jsonl.xz')};ref_inputs=rows('entradas.jsonl.xz');ref_orders=rows('comandos.jsonl.xz')
    _,original128,_=estado_quadro128()
    whole=WholeState(a.probe,original128) if a.probe in ('P1','P2','P6') else None
    driver=NativeDriver(a.driver,a.library,a.inputs);engine=Player(a.library);engine_inputs=[];out=[];stop=None;difference=None;started=time.perf_counter()
    try:
        assert driver.lib.macos_live_validation(driver.handle,0)==0
        # Input proof requires complete consumed-poll observations. The UI itself
        # uses mode 1; mode 2 is the identical persistent backend with audits.
        engine.lib.rl_execucao_definir.argtypes=[C.c_uint64,C.c_uint32]
        assert engine.lib.rl_execucao_definir(driver.status().world,2)==0
        for _ in range(129):
            if driver.advance():raise RuntimeError(bytes(driver.status().message).decode())
        initial=engine.snapshot(driver.status().world)
        original_bases={base for name,(base,data) in original128.items() if name!='native_stack'}
        static={b:v for b,v in initial.items() if b not in original_bases}
        for frame in range(129,max(reference)+1):
            mapper.begin_frame(frame);answers=mapper.declared_answers();events=[]
            for phase in (2,3):
                code=driver.input_phase(phase,answers);s=driver.status();consumed=engine.consumed(s.world);events+=consumed
                # Requests come only from the actual engine; answers remain script-derived.
                for e in consumed:
                    if e.kind not in range(1,7):continue
                    kind={1:'peek_message',2:'get_message',3:'translate_message',4:'dispatch_message',5:'cursor',6:'key'}[e.kind]
                    mapped=mapper.poll(kind,phase=('between_frames' if phase==2 else 'frame')+str(frame),site=e.site,vk=e.values[0] if e.kind==6 else None)
                    actual=inputs([e])[0];actual['phase']=mapped['phase']
                    if kind=='dispatch_message':actual.pop('wndproc_flags_after');actual['hwnd']=e.values[3];actual['wndproc']='0x4181a1'
                    if mapped!=actual:raise AssertionError(dict(frame=frame,phase=phase,mapper=mapped,engine=actual))
                if code:
                    stop=dict(frame=frame,phase=phase,code=code,detail=bytes(s.message).split(b'\0')[0].decode(),inputs_before_stop=inputs(events),orders_before_stop=orders(events));break
                if whole:
                    result=whole.compare(('between_frames' if phase==2 else 'frame')+str(frame),engine.snapshot(s.world),static,driver.context().registers.values())
                    if not result['equal']:difference=dict(frame=frame,phase=phase,whole_state=result);break
            if stop or difference:break
            actual=indicadores(Memory(engine.snapshot(driver.status().world)));expected=reference[frame]
            dif=comparar_quadro(frame,actual,expected)
            if inputs(events)!=eventos_referencia(ref_inputs,frame):dif['consumed_inputs']=dict(actual=inputs(events),expected=eventos_referencia(ref_inputs,frame))
            if canonical_orders(orders(events))!=canonical_orders([r for r in ref_orders if r['frame']==frame]):dif['orders']=dict(actual=orders(events),expected=[r for r in ref_orders if r['frame']==frame])
            # Hash exactly the indicator comparator's declared fields, never DGROUP.
            fields={k:expected[k] for k in actual};fields['objective']={k:expected['objective'][k] for k in actual['objective']}
            hashes=[hashlib.sha256(canonical(value)).hexdigest() for value in (actual,fields)]
            out.append(dict(frame=frame,equal=not dif,actual_sha256=hashes[0],expected_sha256=hashes[1]))
            if dif:difference=dict(frame=frame,differences=dif);break
        return dict(schema='rising-lands/macos-test-a-state/1',probe=a.probe,world_source='S0 plus original static tables; 128 real no-input frames; no oracle state reload',driver_sha256=hashlib.sha256(a.driver.read_bytes()).hexdigest(),library_sha256=hashlib.sha256(a.library.read_bytes()).hexdigest(),input_sha256=hashlib.sha256(raw).hexdigest(),canonical_roundtrip=ScriptedInput(a.root,script.export_bytes()).export_bytes()==script.export_bytes(),reference=provenance(),frames_equal=sum(r['equal'] for r in out),frames_compared=len(out),frames_requested=len(reference),frame_hash_scope='Exact engine indicator comparator fields, including unit record hashes and objective/UI bytes; DGROUP excluded',whole_state=whole.report() if whole else None,first_difference=difference,first_engine_stop=stop,results=out,rendering_executed=False,seconds=time.perf_counter()-started)
    finally:driver.close()


def main():
    signal.alarm(1140)  # Every native proof is bounded below the 20-minute lease.
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('root','driver','library','inputs','output'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--probe',choices=('P1','P2','P3','P6','P7','K1'),required=True);a=p.parse_args()
    if a.output.exists():p.error('Refusing to overwrite proof')
    report=proof(a);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(canonical(report))
    print(json.dumps({k:v for k,v in report.items() if k not in ('results','whole_state')},indent=1))
    if report['whole_state']:print('Whole phases',report['whole_state']['phases_equal'],report['whole_state']['phases_compared'])
    return int(report['first_difference'] is not None)


if __name__=='__main__':raise SystemExit(main())
