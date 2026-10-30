"""Observe S1's real screen dependencies, preserving the original benchmark boundaries.

Adds entry/return arguments for LoadPie, direct bitmap text, width queries and result statistics.
The retained frame17000 checkpoint drives the same fifty original frames; no translated renderer is imported.
Each isolated screen's complete leaf sequence must equal its ordinary execution as well as the prior full-state,
surface and raster checks. Historical screen evidence and its original producer are unchanged.
"""
import argparse,json,lzma,struct
from pathlib import Path
import capturar_telas_finais_s1 as native

LEAVES={0x4799c4:'LoadPie',0x4591c8:'AffString',0x458f5c:'TextGetLargeur',
        0x47150f:'RechercheCalculNew',
        0x4717c2:'RechercheGetNiveau',0x4717a2:'RechercheGetEtat',0x4717b1:'RechercheGetBranche',
        0x470c3d:'InventionGetCout',0x46003b:'PlayerGetColor'}

class DependancesS1(native.TelasS1):
    def __init__(self,b):
        super().__init__(b)
        for pc in LEAVES:
            b.cpu.hook_add(native.original.unicorn.UC_HOOK_BLOCK,self.leaf,begin=pc,end=pc)

    def leaf(self,c,pc,size,user):
        target=self.cap.current
        if target is None:
            target=getattr(self,'phasecap',None)
            target=target.current if target is not None and self.ativo else None
        if target is None:return
        r=lambda n:c.reg_read(getattr(native.original.x86,'UC_X86_REG_'+n))&0xffffffff
        item=dict(routine=LEAVES[pc],registers={n:r(n) for n in ('EAX','EDX','EBX','ECX')},
                  surface_before=native.sha(self.b.directdraw.pixels('offscreen')))
        if pc in self.b.fronteiras:
            name,(value,cleanup)=self.b.fronteiras[pc]
            item['declared_nonexecution']=dict(routine=name,eax=value,stack_cleanup=cleanup)
        if pc==0x4717a2:
            item['query_f64_hex']=bytes(c.mem_read(0x5080fc+16*(r('EAX')&255),8)).hex()
        if pc in (0x4799c4,0x4591c8,0x458f5c):
            ptr=r('EBX') if pc==0x4591c8 else r('EAX');raw=bytearray()
            for i in range(65536):
                value=bytes(c.mem_read(ptr+i,1))[0]
                if not value:break
                raw.append(value)
            else:raise ValueError('Screen dependency string has no bounded terminator')
            item['text_hex']=raw.hex()
        target.setdefault('leaf_calls',[]).append(item)
        ret=struct.unpack('<I',c.mem_read(r('ESP'),4))[0];stack=r('ESP')
        def returned(cpu,address,n,unused):
            if r('ESP')<stack+4:return
            item['return_eax']=r('EAX');item['surface_after']=native.sha(self.b.directdraw.pixels('offscreen'))
            cpu.hook_del(hook)
        hook=c.hook_add(native.original.unicorn.UC_HOOK_CODE,returned,begin=ret,end=ret)

    def executar(self,regs):
        count=len(self.registros);phase=self.phasecap.current;start=len(phase.get('leaf_calls',[]))
        ret=struct.unpack('<I',self.b.cpu.mem_read(regs['ESP'],4))[0]
        super().executar(regs)
        if len(self.registros)==count:return
        row=self.registros[-1]
        def ordinary(cpu,pc,size,user):
            row['dependency_arguments_equal']=row.get('leaf_calls',[])==phase.get('leaf_calls',[])[start:]
            assert row['dependency_arguments_equal'],(row['frame'],row['routine'],'native dependency sequence differs')
            cpu.hook_del(hook)
        hook=self.b.cpu.hook_add(native.original.unicorn.UC_HOOK_CODE,ordinary,begin=ret,end=ret)

def main(a):
    if Path(a.output).exists():raise FileExistsError('Native evidence output already exists; choose a new output')
    native.TelasS1=DependancesS1
    native.main(a)
    path=Path(a.output);d=json.loads(lzma.decompress(path.read_bytes()))
    assert all(r['dependency_arguments_equal'] for r in d['rows'])
    d['dependency_observer']=dict(method=__doc__,source_sha256=native.sha(Path(__file__).read_bytes()),
        original_entries={hex(pc):name for pc,name in LEAVES.items()})
    path.write_bytes(lzma.compress(json.dumps(d).encode()))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--snapshot',required=True)
    p.add_argument('--ref',default=native.REF);p.add_argument('--probe-records');p.add_argument('--to',type=int,default=17050)
    p.add_argument('--output',required=True);main(p.parse_args())
