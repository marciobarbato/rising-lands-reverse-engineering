"""Original-only record/COM/queue captures. Execute only through the heavy lease."""
import argparse
import hashlib
import json
import signal
import struct
import time
from pathlib import Path

import ambiente_audio
from ambiente_audio import ROOT,OWNED,CD,ORIGINAL_SHA256
from analisar import dependencias
from emulador import BancadaX86,RETORNO,x86
from vinculos_declarados import ParadaVinculoDeclarado
from audio_queue_fixtures import *

ENTRIES={'is_playing':0x48be90,'is_stopped':0x48beb9,'is_looped':0x48bedb,'stop_buffer':0x48bf74,
 'compact':0x48af1b,'destroy_waiting':0x48b11d,'permute':0x48b317,'sort':0x48a664,
 'transfer_to_playing':0x48b1e9,'transfer_to_waiting':0x48b01b,'post':0x48aa79,'insert':0x48a218,
 'destroy_logical':0x48adb3,'stop_handle':0x48a438,'set_volume':0x48a14a,'manage':0x48aaca}


def globals_from_original():
    pefile,_=dependencias();raw=(CD/'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=ORIGINAL_SHA256:raise ValueError('Intact executable identity differs')
    return pefile.PE(data=raw).get_data(GLOBAL_BASE-0x400000,GLOBAL_SIZE)


def response(method,*,value=None,hresult=0,args=(),pointer=COM_BUFFER):
    item=dict(method=method,object=pointer,args=list(args),hresult=hresult)
    if value is not None:item['value']=value
    return item


def scenarios():
    original=globals_from_original()
    for operation in ('is_playing','is_stopped','is_looped','stop_buffer'):
        m=fixture_memory(original)
        yield dict(name=operation+'-null',operation=operation,regs=dict(EAX=0),arguments=[],memory=m.snapshot(),com=[])
        for status in (0,1,2,4,5,0xffffffff):
            for hresult in (0,0x80004005):
                plan=[response('GetStatus',value=status,hresult=hresult)]
                if operation=='stop_buffer' and status&5:
                    plan.append(response('Stop',hresult=hresult))
                yield dict(name=f'{operation}-{status:x}-{hresult:x}',operation=operation,regs=dict(EAX=COM_BUFFER),arguments=[],memory=m.snapshot(),com=plan)
    for maximum in (19,20,21,69,70):
        for target in sorted({20,maximum}):
            for clear in (0,1):
                m=fixture_memory(original);m.w32(INDEX,maximum)
                for i in range(20,max(21,maximum+1)):record(m,i)
                yield dict(name=f'compact-{maximum}-{target}-{clear}',operation='compact',
                    regs=dict(EAX=TABLE+target*44,EDX=clear),arguments=[],memory=m.snapshot(),com=[])
                yield dict(name=f'destroy-{maximum}-{target}-{clear}',operation='destroy_waiting',
                    regs=dict(EAX=target),arguments=[],memory=m.snapshot(),com=[])
    for a,b in ((20,21),(20,20),(0,20),(69,70)):
        m=fixture_memory(original)
        for i in {a,b}:record(m,i,slot=0x52211c+(i%10)*8)
        yield dict(name=f'permute-{a}-{b}',operation='permute',regs=dict(EAX=TABLE+a*44,EDX=TABLE+b*44),arguments=[],memory=m.snapshot(),com=[])
    for dirty in (0,1,2,0xffffffff):
        m=fixture_memory(original);m.w32(0x521f84,dirty)
        yield dict(name=f'sort-{dirty:x}',operation='sort',regs={},arguments=[],memory=m.snapshot(),com=[])
    for maximum,target in ((20,20),(21,20),(21,21),(69,20),(70,20)):
        m=fixture_memory(original);m.w32(INDEX,maximum)
        for i in range(20,maximum+1):record(m,i)
        m.w32(TABLE+target*44+32,0x52211c);m.w32(0x52211c,COM_BUFFER)
        yield dict(name=f'to-playing-{maximum}-{target}',operation='transfer_to_playing',regs=dict(EAX=target),arguments=[],memory=m.snapshot(),com=[])
    for maximum in (19,20,69,70):
        m=fixture_memory(original);m.w32(INDEX,maximum)
        for i in range(20,max(21,maximum+1)):record(m,i)
        record(m,0,state=1,slot=0x52216c,kind=1);m.w32(0x52216c,COM_BUFFER);m.w32(0x522170,TABLE);m.w32(0x498f64,0)
        yield dict(name=f'to-waiting-{maximum}',operation='transfer_to_waiting',regs=dict(EAX=0),arguments=[],memory=m.snapshot(),
                   com=[] if maximum==70 else [response('GetStatus',value=0),response('Release')])
    for counter in (0,1,9):
        for target in sorted({0,counter}):
            for status in (0,1):
                m=fixture_memory(original);m.w32(0x498f64,counter)
                for i in range(counter+1):
                    r=record(m,i,state=1,slot=0x52216c+i*8,kind=1)
                    m.w32(0x52216c+i*8,COM_BUFFER);m.w32(0x522170+i*8,r)
                plan=[response('GetStatus',value=status)]
                if status:plan += [response('GetStatus',value=1),response('Stop')]
                plan += [response('Release')]
                yield dict(name=f'destroy-logical-{counter}-{target}-{status}',operation='destroy_logical',
                           regs=dict(EAX=0x52216c+target*8),arguments=[],memory=m.snapshot(),com=plan)
    for selector in (0,0x40,0x41,0x42,0x50,0x51,0x10041):
        for sound_id in (ID1,ID2,0xffffffff):
            for maximum in (19,69,70):
                m=fixture_memory(original);m.w32(INDEX,maximum)
                yield dict(name=f'post-{selector:x}-{sound_id:x}-{maximum}',operation='post',
                    regs=dict(EAX=selector,EDX=sound_id,EBX=REFS+4*72,ECX=0x102),arguments=[255],memory=m.snapshot(),com=[])
    for maximum in (20,21,69):
        for volume in (0,128):
            for identity in (ID1,ID2):
                m=fixture_memory(original);m.w32(INDEX,maximum)
                for i in range(20,maximum+1):record(m,i)
                yield dict(name=f'insert-existing-{maximum}-{volume}-{identity:x}',operation='insert',
                  regs=dict(EAX=identity,EDX=BANK_A,EBX=REFS+20*4,ECX=3),arguments=[volume],memory=m.snapshot(),com=[])
    for volume in (0,64,256,0xffffffff):
        m=fixture_memory(original);record(m,20)
        yield dict(name=f'set-volume-{volume}',operation='set_volume',regs=dict(EAX=REFS+20*4,EDX=volume),arguments=[],memory=m.snapshot(),com=[])
    for maximum in (20,21):
        m=fixture_memory(original);m.w32(INDEX,maximum)
        for i in range(20,maximum+1):record(m,i)
        yield dict(name=f'stop-handle-{maximum}',operation='stop_handle',regs=dict(EAX=REFS+20*4),arguments=[],memory=m.snapshot(),com=[])
    for status in (0,1,5):
        for hresult in (0,0x80004005):
            m=fixture_memory(original)
            record(m,0,state=1,slot=0x52216c,kind=1)
            m.w32(0x52216c,COM_BUFFER);m.w32(0x522170,TABLE);m.w32(0x498f64,0)
            plan=[response('GetStatus',value=status,hresult=hresult)]
            if status&5:
                plan.append(response('SetVolume',args=(m.u32(GLOBAL_BASE+16*4),),hresult=hresult))
            else:
                plan += [response('GetStatus',value=0),response('GetStatus',value=0),response('Release')]
            yield dict(name=f'manage-active-{status}-{hresult:x}',operation='manage',regs={},arguments=[],memory=m.snapshot(),com=plan)
    m=fixture_memory(original)
    yield dict(name='manage-empty',operation='manage',regs={},arguments=[],memory=m.snapshot(),com=[])
    m=fixture_memory(original);m.w32(INDEX,20);record(m,20)
    yield dict(name='manage-pending-provider',operation='manage',regs={},arguments=[],memory=m.snapshot(),
               com=[response('_llseek',pointer=0x1234,args=(0,0))])


class QueueNativeBench(BancadaX86):
    def __init__(self,fixture):
        super().__init__();self.fixture=fixture;self.plan=ScriptedCOM(fixture['com']);self.raw_com=[]
        self.cpu.mem_map(EXTERNAL,EXTERNAL_SIZE);self.cpu.mem_map(COM_BASE,COM_SIZE)
        for region in fixture['memory']:self.cpu.mem_write(int(region['base'],16),decode(region['zlib_base64']))
        for pointer in (COM_BUFFER,COM_DUPLICATE,COM_DEVICE):self.cpu.mem_write(pointer,struct.pack('<I',COM_BASE+0x2000))
        for slot in range(32):
            offset=slot*4;address=COM_BASE+0x5000+offset
            self.cpu.mem_write(COM_BASE+0x2000+offset,struct.pack('<I',address))
            def unavailable(call,number=offset):
                raise ParadaVinculoDeclarado(f'Undeclared DirectSound slot +0x{number:x} at caller 0x{call.retorno:x}')
            self.declarar_vinculo(address,'AudioCOM.Unbound'+hex(offset),(),unavailable,natureza='backend')
        for method,offset,nargs in (('GetStatus',0x24,2),('Stop',0x48,1),('SetPosition',0x34,2),('SetVolume',0x3c,2),('Play',0x30,4),('Release',8,1)):
            address=COM_BASE+0x4000+offset
            self.cpu.mem_write(COM_BASE+0x2000+offset,struct.pack('<I',address))
            def handler(call,name=method):
                args=call.argumentos;normalized=[] if name=='GetStatus' else list(args[1:])
                answer=self.plan.answer(name,args[0],normalized)
                self.raw_com.append(dict(method=name,args=list(args),answer=answer))
                if name=='GetStatus':
                    if 'value' not in answer:raise ParadaVinculoDeclarado('GetStatus requires an explicit written status')
                    call.escrever(args[1],struct.pack('<I',answer['value']))
                return answer['hresult']
            self.declarar_vinculo(address,'AudioCOM.'+method,tuple(range(4,4*(nargs+1),4)),handler,desempilhar=4*nargs,natureza='backend')
        def seek(call):
            args=call.argumentos
            answer=self.plan.answer('_llseek',args[0],list(args[1:]))
            self.raw_com.append(dict(method='_llseek',args=list(args),answer=answer))
            return answer['hresult']
        self.declarar_importacao(0x5231f8,'KERNEL32._llseek',3,seek)
        self.calls=0

    def snapshot(self):
        return [dict(base=r['base'],zlib_base64=encode(self.cpu.mem_read(int(r['base'],16),len(decode(r['zlib_base64'])))),
                     sha256=hashlib.sha256(self.cpu.mem_read(int(r['base'],16),len(decode(r['zlib_base64'])))).hexdigest()) for r in self.fixture['memory']]


def run_case(fixture):
    b=QueueNativeBench(fixture);stop=None;regs={}
    try:
        regs=b.executar(ENTRIES[fixture['operation']],[(0x489dac,0x48c204),(0x48c3b0,0x48c3c8),(0x48d890,0x48d942)],fixture['regs'],
                       pilha={4+4*i:struct.pack('<I',v) for i,v in enumerate(fixture['arguments'])},limite_instrucoes=20000)
    except Exception as exc:stop=dict(type=type(exc).__name__,detail=str(exc),eip=hex(b.cpu.reg_read(x86.UC_X86_REG_EIP)))
    return dict(name=fixture['name'],operation=fixture['operation'],input=fixture,output=b.snapshot(),
                eax=hex(regs['EAX']) if regs else None,stop=stop,com=b.plan.calls,raw_com=b.raw_com,unused_com=len(b.plan.responses))


def capture():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('Ten-minute Audio queue capture limit')));signal.alarm(600)
    start=time.monotonic();cases=[run_case(f) for f in scenarios()]
    return dict(schema='rising-lands/audio-queue-original-capture/1',original_sha256=ORIGINAL_SHA256,
                translation_executed=False,declared_com='Exact ordered HRESULT/status answers; no hardware/default status semantics',
                cases=cases,native_calls=len(cases),seconds=round(time.monotonic()-start,3))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    if args.output.exists():raise ValueError('Refusing to overwrite original queue evidence')
    report=capture();args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as output:json.dump(report,output,indent=2);output.write('\n')
    print(json.dumps(dict(native_calls=report['native_calls'],seconds=report['seconds'],stops=sum(c['stop'] is not None for c in report['cases']))))
