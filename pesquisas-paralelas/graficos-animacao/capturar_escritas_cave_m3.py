"""Two native passes over exact scripted states: AffBatiments changing writers and outside-display readers.

Pass one records every changing non-stack/non-surface byte written in AffBatiments. Pass two restores the same
native checkpoint and watches readers of precisely that set outside AffGame/AffBatiments/RestoreAll. No game
routine is replaced and no state write creates a case. Both passes must reproduce published whole states and
surfaces when available, and must reproduce each other for every frame (including the S1 input prefix).
"""
import argparse,collections,hashlib,json,lzma,struct,time
from pathlib import Path
import capturar_sondas_graficos_m3 as original

AQUI=original.AQUI
REF='fd56f69'
sha=original.sha

class EscritasBatiments:
    def __init__(self,b,targets=None):
        self.b=b;self.targets=targets;self.frame=None;self.stack=[];self.writes={};self.readers={};self.guards={};self.hooks=[]
        roots={b.sym[n]:n for n in ('AffGame','AffBatiments','RestoreAll')};code=bytes(b.cpu.mem_read(0x401000,0x92c00));returns=set()
        pos=0
        while True:
            pos=code.find(b'\xe8',pos)
            if pos<0 or pos+5>len(code):break
            target=(0x401000+pos+5+struct.unpack_from('<i',code,pos+1)[0])&0xffffffff
            if target in roots:returns.add(0x401000+pos+5)
            pos+=1
        def entry(cpu,address,size,user):
            if self.frame is None:return
            esp=cpu.reg_read(original.x86.UC_X86_REG_ESP);ret=int.from_bytes(cpu.mem_read(esp,4),'little')
            while self.stack and esp>=self.stack[-1][1]+4:self.stack.pop()
            self.stack.append((roots[address],esp,ret))
            if roots[address]!='AffBatiments':return
            cell=cpu.reg_read(original.x86.UC_X86_REG_EBX)&65535;m=cpu.mem_read
            u=lambda a,n:int.from_bytes(m(a,n),'little')
            region=u(u(0x4e0f38,4)+2*cell,2)
            if region&0x8000:
                index=(region&0x7fe0)>>5
                if index<1000:
                    r=bytes(m(0x49a0c8+276*index,276));key=(self.frame,index,r[8],r[5],r[4],int.from_bytes(r[6:8],'little'),int.from_bytes(r[10:12],'little'))
                    self.guards[key]=self.guards.get(key,0)+1
        def leave(cpu,address,size,user):
            if self.frame is None:return
            esp=cpu.reg_read(original.x86.UC_X86_REG_ESP)
            while self.stack and self.stack[-1][2]==address and esp>=self.stack[-1][1]+4:self.stack.pop()
        for address in roots:self.hooks.append(b.cpu.hook_add(original.unicorn.UC_HOOK_CODE,entry,begin=address,end=address))
        for address in returns:self.hooks.append(b.cpu.hook_add(original.unicorn.UC_HOOK_CODE,leave,begin=address,end=address))
        self.memhooks=[]
        b.cpu.ctl_flush_tb()

    def start(self,frame):
        self.frame=frame;self.stack=[]
        def write(cpu,access,address,size,value,user):
            if not any(n=='AffBatiments' for n,_,_ in self.stack):return
            old=bytes(cpu.mem_read(address,size));new=(value&((1<<(size*8))-1)).to_bytes(size,'little')
            pc=cpu.reg_read(original.x86.UC_X86_REG_EIP)
            for k,(a,z) in enumerate(zip(old,new)):
                if a==z:continue
                target=address+k;item=self.writes.setdefault(target,dict(count=0,writers={},examples=[]));item['count']+=1
                key=hex(pc);item['writers'][key]=item['writers'].get(key,0)+1
                if len(item['examples'])<3:item['examples'].append([self.frame,self.b.fase,self.b.nome(pc),a,z])
        def read(cpu,access,address,size,value,user):
            if self.targets is None or self.stack:return
            pc=cpu.reg_read(original.x86.UC_X86_REG_EIP)
            for a in range(address,address+size):
                if a not in self.targets:continue
                key=(a,pc,self.b.fase,bytes(cpu.mem_read(a,1))[0]);self.readers[key]=self.readers.get(key,0)+1
        for lo,hi in ((0x494000,0x523000),(0x60000000,0x60001000),(self.b.arena.base,self.b.arena.proximo)):
            self.memhooks.append(self.b.cpu.hook_add(original.unicorn.UC_HOOK_MEM_WRITE,write,begin=lo,end=hi-1))
            if self.targets is not None:self.memhooks.append(self.b.cpu.hook_add(original.unicorn.UC_HOOK_MEM_READ,read,begin=lo,end=hi-1))
        self.b.cpu.ctl_flush_tb()

    def stop(self):
        for hook in self.memhooks:self.b.cpu.hook_del(hook)
        self.memhooks=[];self.frame=None;self.stack=[];self.b.cpu.ctl_flush_tb()

    def finish(self):
        for hook in self.hooks:self.b.cpu.hook_del(hook)
        return dict(changing_bytes={hex(a):v for a,v in sorted(self.writes.items())},
            outside_display_readers=[dict(address=hex(a),pc=hex(pc),routine=self.b.nome(pc),phase=phase,value=value,count=count)
                                     for (a,pc,phase,value),count in sorted(self.readers.items())],
            structure_calls=[dict(frame=k[0],index=k[1],kind=k[2],state=k[3],owner=k[4],damage=k[5],health=k[6],calls=v)
                             for k,v in sorted(self.guards.items())])

def run(a,targets=None):
    original.REF=REF;m=original.modulo_entrada();b,_,start=m.abrir(a.start,Path(a.snapshot))
    if not 0<a.to-start<=1000:raise ValueError('Use bounded native segments of at most1000 frames')
    raw=original.remoto(original.PROBE_ROOT+'entradas/'+a.probe+'.json');b.roteiro.quadros=m.carregar_entrada(json.loads(raw))[0]
    refs={}
    if a.probe!='S1':refs={r['frame']:r for r in map(json.loads,lzma.decompress(original.remoto(original.PROBE_ROOT+'sondas/'+a.probe+'/quadros.jsonl.xz')).splitlines())}
    if refs and b.resumo_imagem(b.imagem())['sha256']!=refs[start]['state_sha256']:raise RuntimeError('Opening state differs')
    obs=EscritasBatiments(b,targets);checks=[];t=time.monotonic()
    for k in range(start+1,a.to+1):
        b.roteiro.iniciar_quadro(k)
        if k in a.observe:obs.start(k)
        b.executar_entre_quadros(300,k);surface=sha(b.directdraw.pixels('offscreen'));b.executar_quadro(600,k)
        after=sha(b.directdraw.pixels('offscreen'));state=b.resumo_imagem(b.imagem())['sha256']
        if refs:
            assert (surface,after,state)==(refs[k]['surfaces_between']['offscreen'],refs[k]['surfaces_frame']['offscreen'],refs[k]['state_sha256']),k
        checks.append(dict(frame=k,between=surface,after=after,state=state))
        if k in a.observe:obs.stop()
        b.roteiro.eventos.clear()
        if k%50==0:print(a.probe,k,'native original phase/state checked',flush=True)
        if time.monotonic()-t>1080:raise RuntimeError('18-minute native budget exhausted')
    return dict(checks=checks,observation=obs.finish(),code_sha256=b.sha256_codigo(),elapsed_seconds=round(time.monotonic()-t,3),
                input_sha256=sha(raw),published_reference=bool(refs))

def main(a):
    first=run(a);targets={int(x,16) for x in first['observation']['changing_bytes']}
    second=run(a,targets)
    assert first['checks']==second['checks'];assert first['observation']['changing_bytes']==second['observation']['changing_bytes']
    result=dict(schema='rising-lands/cave-display-writer-reader/1',method=__doc__,probe_ref=REF,probe=a.probe,observed_frames=a.observe,
        executable_sha256=__import__('emulador').HASH_ORIGINAL,snapshot_sha256=sha(Path(a.snapshot).read_bytes()),
        source_sha256=sha(Path(__file__).read_bytes()),passes=[first,second],passes_equal=True)
    raw=json.dumps(result).encode();z=lzma.compress(raw);Path(a.output).write_bytes(z)
    Path(a.output+'.manifest.json').write_text(json.dumps(dict(raw_sha256=sha(raw),compressed_sha256=sha(z),probe=a.probe,
        observed_frames=a.observe,passes_equal=True,elapsed_seconds=[p['elapsed_seconds'] for p in result['passes']]),indent=1)+'\n')
    print(a.probe,'two passes equal;',len(targets),'changing bytes;',len(second['observation']['outside_display_readers']),'outside-display reader groups',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--snapshot',required=True)
    p.add_argument('--probe',choices=('P3','P6','P7','S1'),required=True);p.add_argument('--to',type=int,required=True)
    p.add_argument('--observe',type=lambda s:list(map(int,s.split(','))),required=True);p.add_argument('--output',required=True)
    main(p.parse_args())
