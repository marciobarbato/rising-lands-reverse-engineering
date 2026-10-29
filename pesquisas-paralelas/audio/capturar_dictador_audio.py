"""Original-only entry-word256 dictator lifecycle; native execution requires lease."""
import argparse
import json
import signal
import struct
import time
from pathlib import Path
from capturar_continuacao_audio import ContinuationBench,case,fill_plan
from capturar_fila_audio import globals_from_original,response,ENTRIES
from audio_queue_fixtures import *
from ambiente_audio import ORIGINAL_SHA256
from emulador import x86

DICTATOR=0x521f94
DICTATOR_SLOT=EXTERNAL+0x9000
ENTRIES.update(init_dictator=0x489f39,clear_dictator=0x489f04,game_volume=0x48aa45)


def request(operation,regs=None,args=None):return dict(operation=operation,regs=regs or {},arguments=args or [])
def post(reference=REFS+72*4,flags=0):return request('post',dict(EAX=0x41,EDX=ID2,EBX=reference,ECX=flags),[256])
def allocation(pointer=DICTATOR_SLOT):return response('GlobalAlloc',pointer=0,args=(0,8),hresult=pointer)


def initial(original):
    m=fixture_memory(original)
    for i in range(3):m.write(DATA2+i*16,struct.pack('<IIBBHBBH',0,64,1,16,22050,0,0,64))
    for i in (72,73):m.w32(REFS+i*4,0xffffffff)
    return m


def start_plan(flags=0,*,created=COM_BUFFER,position=0,volume=0,play=0):
    if not created:return []
    result=[response('GetStatus',value=0),response('SetPosition',args=(0,),hresult=position)]
    if not position:
        result.append(response('SetVolume',args=(0,),hresult=volume))
        if not volume:result.append(response('Play',args=(0,0,0),hresult=play))
    return result


def create_plan(m,flags=0):return fill_plan(m)+start_plan(flags)


def scenarios():
    original=globals_from_original()
    for pointer in (DICTATOR_SLOT,0):
        m=initial(original)
        yield case(f'init-{pointer:x}','init_dictator',m,com=[allocation(pointer)])
    for flags in (0,1):
        for status in (0,1,5):
            for error in (0,0x80004005):
                m=initial(original);sequence=[request('init_dictator'),post(flags=flags),request('manage'),request('clear_list')]
                plan=[allocation()]+create_plan(m,flags)+[response('GetStatus',value=status,hresult=error)]
                if not status:plan += [response('GetStatus',value=0),response('Release',hresult=7)]
                yield case(f'clear-list-{flags}-{status}-{error:x}','init_dictator',m,com=plan,sequence=sequence)
                sequence=[request('init_dictator'),post(flags=flags),request('manage'),request('clear_dictator')]
                plan=[allocation()]+create_plan(m,flags)+[response('GetStatus',value=status,hresult=error)]
                if status&5:plan.append(response('Stop',hresult=error))
                plan.append(response('Release',hresult=7))
                yield case(f'clear-explicit-{flags}-{status}-{error:x}','init_dictator',m,com=plan,sequence=sequence)
    for game_volume in (0,128,256,257,0xffffffff):
        m=initial(original);sequence=[request('init_dictator'),post(),request('manage'),request('game_volume',dict(EAX=game_volume)),request('manage')]
        effective=0 if game_volume==0xffffffff else min(game_volume,256)
        word=m.u32(GLOBAL_BASE+effective//16*4)
        plan=[allocation()]+create_plan(m)+[response('GetStatus',value=1),response('SetVolume',args=(word,),hresult=0x80004005)]
        yield case(f'volume-active-{game_volume:x}','init_dictator',m,com=plan,sequence=sequence)
    for failure in ('position','volume','play'):
        m=initial(original);sequence=[request('init_dictator'),post(),request('manage')]
        plan=[allocation()]+fill_plan(m)+start_plan(**{failure:0x80004005})
        yield case('start-error-'+failure,'init_dictator',m,com=plan,sequence=sequence)
    m=initial(original)
    sequence=[request('init_dictator'),post(),request('manage'),post(REFS+73*4),request('manage'),request('clear_dictator'),request('manage'),request('clear_list')]
    plan=[allocation()]+create_plan(m)+[response('GetStatus',value=1),response('GetStatus',value=0),response('Release',hresult=7)]
    plan+=create_plan(m)+[response('GetStatus',value=0),response('GetStatus',value=0),response('Release',hresult=7)]
    yield case('active-pending-clear-relaunch','init_dictator',m,com=plan,sequence=sequence)


class DictatorBench(ContinuationBench):
    def __init__(self,fixture):
        super().__init__(fixture)
        def allocate(call):
            args=list(call.argumentos);answer=self.plan.answer('GlobalAlloc',0,args)
            self.raw_com.append(dict(method='GlobalAlloc',args=args,answer=answer))
            return answer['hresult']
        self.declarar_importacao(0x5231c0,'KERNEL32.GlobalAlloc',2,allocate)


def run_case(fixture):
    b=DictatorBench(fixture);stop=None;regs={};steps=[];attempted=0
    try:
        for item in fixture.get('sequence',[fixture]):
            attempted+=1
            regs=b.executar(ENTRIES[item['operation']],[(0x489dac,0x48c241),(0x48c3b0,0x48c3c8),(0x48d890,0x48d942)],item['regs'],
                           pilha={4+4*i:struct.pack('<I',v) for i,v in enumerate(item['arguments'])},limite_instrucoes=50000)
            if 'sequence' in fixture:steps.append(dict(eax=hex(regs['EAX']),memory=b.snapshot()))
    except Exception as exc:stop=dict(type=type(exc).__name__,detail=str(exc),eip=hex(b.cpu.reg_read(x86.UC_X86_REG_EIP)))
    return dict(name=fixture['name'],native_calls=attempted,operation=fixture['operation'],input=fixture,output=b.snapshot(),eax=hex(regs['EAX']) if regs else None,
                steps=steps,stop=stop,com=b.plan.calls,raw_com=b.raw_com,unused_com=len(b.plan.responses))


def capture():
    def timeout(*_):raise TimeoutError('Ten-minute Audio dictator capture bound')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(600)
    start=time.monotonic();cases=[]
    for fixture in scenarios():
        if time.monotonic()-start>=600:raise TimeoutError('Audio dictator deadline')
        cases.append(run_case(fixture))
    return dict(schema='rising-lands/audio-dictator-original/1',original_sha256=ORIGINAL_SHA256,translation_executed=False,
                scenarios=len(cases),native_calls=sum(c['native_calls'] for c in cases),planned_calls=sum(len(c['input'].get('sequence',[None])) for c in cases),cases=cases,seconds=round(time.monotonic()-start,3))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    if args.output.exists() or args.output.is_symlink():parser.error('Refusing to overwrite original evidence')
    result=capture();args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'}));print('stops',sum(c['stop'] is not None for c in result['cases']))
