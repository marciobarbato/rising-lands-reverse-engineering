"""Native P4 frame484 AffText/TextGetMessage boundary audit, with no glyph substitution."""
import argparse,json,lzma,struct,time
from pathlib import Path
from capturar_escritas_cave_m3 import original,REF,sha

def main(a):
    original.REF=REF;m=original.modulo_entrada();b,_,start=m.abrir(a.start,None);assert start==128
    raw=original.remoto(original.PROBE_ROOT+'entradas/P4.json');b.roteiro.quadros=m.carregar_entrada(json.loads(raw))[0]
    refs={r['frame']:r for r in map(json.loads,lzma.decompress(original.remoto(original.PROBE_ROOT+'sondas/P4/quadros.jsonl.xz')).splitlines())}
    cpu=b.cpu;uc=original.unicorn;x86=original.x86;targets={b.sym[n]:n for n in ('AffText','TextGetMessage')}
    calls=[];pending=[];body=[];reads=[];checks=[];active=False;t=time.monotonic()
    r=lambda name:cpu.reg_read(getattr(x86,'UC_X86_REG_'+name))&0xffffffff
    def block(c,address,size,_):
        if not active:return
        if address in targets:
            ret=struct.unpack('<I',c.mem_read(r('ESP'),4))[0]
            pending.append((ret,len(calls)));calls.append(dict(routine=targets[address],phase=b.fase,
                entry_eax=hex(r('EAX')),entry_esp=hex(r('ESP')),return_address=hex(ret),surface_before=sha(b.directdraw.pixels('offscreen'))))
        if pending and address==pending[-1][0]:
            _,index=pending.pop();calls[index].update(return_eax=hex(r('EAX')),return_esp=hex(r('ESP')),
                surface_after=sha(b.directdraw.pixels('offscreen')))
    def instruction(c,address,size,_):
        if active:body.append(hex(address))
    def read(c,access,address,size,value,_):
        if active:reads.append(dict(address=hex(address),size=size,eip=hex(r('EIP')),phase=b.fase))
    cpu.hook_add(uc.UC_HOOK_BLOCK,block)
    for target in targets:
        end=min(v for v in b.sym.values() if v>target)
        cpu.hook_add(uc.UC_HOOK_CODE,instruction,begin=target+1,end=end-1)
    cpu.hook_add(uc.UC_HOOK_MEM_READ,read,begin=0x5099a4,end=0x5099a7);cpu.ctl_flush_tb()
    for k in range(start+1,485):
        active=k==484;b.roteiro.iniciar_quadro(k);b.executar_entre_quadros(300,k)
        between=sha(b.directdraw.pixels('offscreen'));b.executar_quadro(600,k)
        state=b.resumo_imagem(b.imagem())['sha256'];surface=sha(b.directdraw.pixels('offscreen'))
        assert between==refs[k]['surfaces_between']['offscreen'] and surface==refs[k]['surfaces_frame']['offscreen'] and state==refs[k]['state_sha256']
        checks.append(dict(frame=k,surface_equal=True,state_equal=True));b.roteiro.eventos.clear()
        if k%100==0:print('P4 original',k,flush=True)
        if time.monotonic()-t>1080:raise RuntimeError('18-minute native budget exhausted')
    assert calls and not pending and not body
    assert all(c['surface_before']==c['surface_after'] for c in calls)
    assert all(c['return_eax']=='0x0' for c in calls if c['routine']=='TextGetMessage')
    assert not any(c['address']=='0x5099a4' for c in reads)
    result=dict(schema='rising-lands/p4-afftext-boundary-audit/1',probe_ref=REF,frame=484,
        executable_sha256=__import__('emulador').HASH_ORIGINAL,source_sha256=sha(Path(__file__).read_bytes()),
        snapshot_sha256=sha(Path(a.snapshot).read_bytes()),input_sha256=sha(raw),code_sha256=b.sha256_codigo(),
        calls=calls,body_instructions=body,pointer_overlap_reads=reads,checks=checks,elapsed_seconds=time.monotonic()-t)
    Path(a.output).write_text(json.dumps(result,indent=1)+'\n');print('audited original boundary',len(calls),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--snapshot',required=True);p.add_argument('--output',required=True);main(p.parse_args())
