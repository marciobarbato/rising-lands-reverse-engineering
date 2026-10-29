"""Original-only Audio continuation fixtures; native execution requires shared lease."""
import argparse
import hashlib
import json
import signal
import struct
import time
from pathlib import Path
from capturar_fila_audio import QueueNativeBench,globals_from_original,response,ENTRIES
from audio_queue_fixtures import *
from emulador import x86
from vinculos_declarados import ParadaVinculoDeclarado
from ambiente_audio import ORIGINAL_SHA256

ENTRIES.update(replace_physical=0x48abdc,replace_logical=0x48ad3c,find_physical=0x48acd3,
 find_logical=0x48aeb3,destroy_physical=0x48ac53,destroy_only=0x489e35,duplicate=0x48bfb9,
 create_logical=0x48ae5f,clear_list=0x489f96)


def case(name,operation,m,regs=None,com=None,args=None,sequence=None):
    result=dict(name=name,operation=operation,memory=m.snapshot(),regs=regs or {},arguments=args or [],com=com or [])
    if sequence is not None:result['sequence']=sequence
    return result


def table(m,base,counter,count):
    m.w32(counter,count)
    for i in range(count+1):
        r=record(m,i,state=1,slot=base+i*8,kind=int(base==0x52216c),sound_id=ID1 if i==0 else ID2)
        m.w32(base+i*8,COM_BUFFER);m.w32(base+i*8+4,r)


def scenarios():
    original=globals_from_original()
    for logical,base,counter in ((False,0x52211c,0x498f60),(True,0x52216c,0x498f64)):
        suffix='logical' if logical else 'physical'
        for count in (-1,0,1,9):
            for target in sorted({0,max(count,0)}):
                m=fixture_memory(original);table(m,base,counter,count)
                yield case(f'replace-{suffix}-{count}-{target}','replace_'+suffix,m,dict(EAX=base+8*target))
            for sound_id in (ID1,ID2,0xffffffff):
                for bank in (BANK_A,BANK_B):
                    m=fixture_memory(original);table(m,base,counter,count)
                    yield case(f'find-{suffix}-{count}-{sound_id:x}-{bank:x}','find_'+suffix,m,dict(EAX=sound_id,EDX=bank))
    for hresult in (0,0x80004005):
        for output in (0,COM_DUPLICATE):
            for position in (0,0x80004005):
                m=fixture_memory(original)
                plan=[response('DuplicateSoundBuffer',pointer=COM_DEVICE,args=(COM_BUFFER,),value=output,hresult=hresult)]
                if not hresult and output:plan.append(response('SetPosition',pointer=output,args=(0,),hresult=position))
                yield case(f'duplicate-{hresult:x}-{output:x}-{position:x}','duplicate',m,dict(EAX=COM_BUFFER),plan)
                for count in (-1,9):
                    n=QueueFixtureMemory.restore(m.snapshot());table(n,0x52216c,0x498f64,count)
                    yield case(f'create-logical-{count}-{hresult:x}-{output:x}-{position:x}','create_logical',n,
                               dict(EAX=COM_BUFFER,EDX=TABLE+20*44),[] if count==9 else plan)
    for source,device in ((0,COM_DEVICE),(COM_BUFFER,0)):
        m=fixture_memory(original);m.w32(0x522228,device)
        yield case(f'duplicate-null-{source:x}-{device:x}','duplicate',m,dict(EAX=source))
    for count in (0,1,9):
        for status in (0,1,5):
            for hresult in (0,0x80004005):
                m=fixture_memory(original);table(m,0x52211c,0x498f60,count)
                plan=[response('GetStatus',value=status,hresult=hresult)]
                if status&1:plan += [response('GetStatus',value=status),response('Stop',hresult=hresult)]
                plan.append(response('Release',hresult=7))
                yield case(f'destroy-physical-{count}-{status}-{hresult:x}','destroy_physical',m,dict(EAX=0x52211c),plan)
    for count in (0,1):
        for promoted in (False,True):
            m=fixture_memory(original);table(m,0x52211c,0x498f60,count)
            if promoted:
                logical=record(m,10,state=1,slot=0x52216c,kind=1)
                m.w32(0x52216c,COM_DUPLICATE);m.w32(0x522170,logical);m.w32(0x498f64,0)
            plan=[response('GetStatus',value=0),response('GetStatus',value=0),response('Release',hresult=7)]
            yield case(f'destroy-promote-{count}-{int(promoted)}','destroy_only',m,dict(EAX=TABLE),plan)
            n=QueueFixtureMemory.restore(m.snapshot())
            yield case(f'transfer-physical-{count}-{int(promoted)}','transfer_to_waiting',n,dict(EAX=0),[response('GetStatus',value=0),response('Release',hresult=7)])
    for logical,base,counter in ((False,0x52211c,0x498f60),(True,0x52216c,0x498f64)):
        for status in (0,1,5):
            m=fixture_memory(original);table(m,base,counter,0)
            plan=[response('GetStatus',value=status,hresult=0x80004005)]
            if status==0:plan += [response('GetStatus',value=0),response('GetStatus',value=0),response('Release',hresult=7)]
            yield case(f'clear-list-{int(logical)}-{status}','clear_list',m,com=plan)


    yield from request_scenarios(original)


def start_plan(pointer=COM_BUFFER,volume=0):
    return [response('GetStatus',pointer=pointer,value=0),response('SetPosition',pointer=pointer,args=(0,)),
            response('SetVolume',pointer=pointer,args=(volume,)),response('Play',pointer=pointer,args=(0,0,0))]


def fill_plan(m,*,resident=False,compressed=False,pointer=COM_BUFFER,output=EXTERNAL+0x4000,data=None):
    data=data if data is not None else bytes((i*7+3)&255 for i in range(64))
    descriptor=struct.pack('<IIIII',20,0xe0,256 if compressed else 64,0,0).hex()
    wave=struct.pack('<HHIIHH',1,1,22050,44100,2,16).hex()
    plan=[] if resident else [response('_llseek',pointer=0x1234,args=(0,0))]
    plan.append(response('CreateSoundBuffer',pointer=COM_DEVICE,args=(descriptor,wave,0),value=pointer))
    lock=response('Lock',pointer=pointer,args=(0,64,0),value=dict(pointer=output,size=64))
    if not resident:
        plan.append(response('_llseek',pointer=0x1234,args=(0,0)))
        read=response('_hread',pointer=0x1234,args=(EXTERNAL+0x6000 if compressed else output,64),value=data.hex(),hresult=len(data))
        if compressed:plan.extend([read,lock])
        else:plan.extend([lock,read])
    else:plan.append(lock)
    plan.append(response('Unlock',pointer=pointer,args=(output,64,0,0)))
    return plan


def request_scenarios(original):
    for resident in (False,True):
        for compressed in (False,True):
            m=fixture_memory(original);m.w32(INDEX,20);record(m,20)
            data=(struct.pack('<hBB',1000,0,0)+bytes([0x11])*60) if compressed else bytes((i*7+3)&255 for i in range(64))
            m.w8(DATA1+12,4 if compressed else 0);m.w16(DATA1+14,64)
            m.w32(0x52222c,EXTERNAL+0x6000)
            if resident:
                m.w32(BANK_A+16,1);m.w32(BANK_A+20,EXTERNAL+0x8000);m.write(EXTERNAL+0x8000,data)
            plan=fill_plan(m,resident=resident,compressed=compressed,data=data)+start_plan()
            yield case(f'manage-data-{int(resident)}-{int(compressed)}','manage',m,com=plan)
    for duplicate_hresult,duplicate_output in ((0,COM_DUPLICATE),(0,0),(0x80004005,COM_DUPLICATE)):
        m=fixture_memory(original);table(m,0x52211c,0x498f60,0);m.w32(0x498f5c,0);m.w32(TABLE+20,0)
        m.w32(INDEX,20);record(m,20)
        plan=[response('GetStatus',value=1),response('DuplicateSoundBuffer',pointer=COM_DEVICE,args=(COM_BUFFER,),value=duplicate_output,hresult=duplicate_hresult)]
        if not duplicate_hresult and duplicate_output:
            plan.append(response('SetPosition',pointer=COM_DUPLICATE,args=(0,)))
            plan+=start_plan(COM_DUPLICATE)
        yield case(f'manage-reuse-{duplicate_hresult:x}-{duplicate_output:x}','manage',m,com=plan)
    for same_bank in (False,True):
        for count in (2,3):
            m=fixture_memory(original);m.w32(INDEX,19+count)
            for i in range(count):record(m,20+i,bank=BANK_A if same_bank else (BANK_A,BANK_B,BANK_P)[i])
            plan=fill_plan(m)+start_plan()
            for i in range(1,count):
                pointer=COM_DUPLICATE if i==1 else COM_BASE+0x1300
                if same_bank:
                    plan += [response('DuplicateSoundBuffer',pointer=COM_DEVICE,args=(COM_BUFFER,),value=pointer),response('SetPosition',pointer=pointer,args=(0,))]
                else:plan+=fill_plan(m,pointer=pointer,output=EXTERNAL+0x4000+0x400*i)
                plan+=start_plan(pointer)
            yield case(f'manage-concurrent-{count}-{int(same_bank)}','manage',m,com=plan)
    for counter in (0,9):
        m=fixture_memory(original);table(m,0x52211c,0x498f60,counter);table(m,0x52216c,0x498f64,9)
        m.w32(0x498f5c,0)
        for i in range(20):m.w32(TABLE+i*44+20,0)
        m.w32(INDEX,20);record(m,20)
        # Both tables contain live records: each guard query is an explicit answer.
        plan=[response('GetStatus',value=1) for _ in range(10+counter+1)]
        yield case(f'manage-capacity-{counter}-9','manage',m,com=plan)


class ContinuationBench(QueueNativeBench):
    def __init__(self,fixture):
        super().__init__(fixture)
        self.cpu.mem_write(COM_BASE+0x1300,struct.pack('<I',COM_BASE+0x2000))
        if any(a['method']=='DuplicateSoundBuffer' for a in fixture['com']):
            address=COM_BASE+0x4014;self.cpu.mem_write(COM_BASE+0x2014,struct.pack('<I',address))
            def duplicate(call):
                this,source,output=call.argumentos
                answer=self.plan.answer('DuplicateSoundBuffer',this,[source])
                self.raw_com.append(dict(method='DuplicateSoundBuffer',args=list(call.argumentos),answer=answer))
                if 'value' not in answer:raise ParadaVinculoDeclarado('DuplicateSoundBuffer requires explicit output write')
                call.escrever(output,struct.pack('<I',answer['value']));return answer['hresult']
            self.declarar_vinculo(address,'AudioCOM.DuplicateSoundBuffer',(4,8,12),duplicate,desempilhar=12,natureza='backend')


def run_case(fixture):
    b=ContinuationBench(fixture);stop=None;regs={};steps=[]
    try:
        for request in fixture.get('sequence',[fixture]):
            regs=b.executar(ENTRIES[request['operation']],[(0x489dac,0x48c204),(0x48c3b0,0x48c3c8),(0x48d890,0x48d942)],request['regs'],
                           pilha={4+4*i:struct.pack('<I',v) for i,v in enumerate(request['arguments'])},limite_instrucoes=50000)
            if 'sequence' in fixture:steps.append(dict(eax=hex(regs['EAX']),memory=b.snapshot()))
    except Exception as exc:stop=dict(type=type(exc).__name__,detail=str(exc),eip=hex(b.cpu.reg_read(x86.UC_X86_REG_EIP)))
    return dict(name=fixture['name'],operation=fixture['operation'],input=fixture,output=b.snapshot(),eax=hex(regs['EAX']) if regs else None,
                steps=steps,stop=stop,com=b.plan.calls,raw_com=b.raw_com,unused_com=len(b.plan.responses))


def capture():
    def timeout(*_):raise TimeoutError('Ten-minute Audio continuation bound')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(600)
    start=time.monotonic();cases=[]
    for fixture in scenarios():
        if time.monotonic()-start>=600:raise TimeoutError('Audio continuation deadline')
        cases.append(run_case(fixture))
    return dict(schema='rising-lands/audio-continuation-original/1',original_sha256=ORIGINAL_SHA256,translation_executed=False,
                cases=cases,scenarios=len(cases),native_calls=sum(len(c['input'].get('sequence',[None])) for c in cases),seconds=round(time.monotonic()-start,3))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    if args.output.exists() or args.output.is_symlink():parser.error('Refusing to overwrite original evidence')
    report=capture();args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps(dict(native_calls=report['native_calls'],scenarios=report['scenarios'],seconds=report['seconds'],stops=sum(c['stop'] is not None for c in report['cases']))))
