"""Observe TextGetMessage's declared return and absent native body reads in one reproduced P7 frame."""
import argparse,json,lzma,struct
from pathlib import Path
from capturar_janelas_graficas_m3 import original,REF,sha,AQUI

def main(a):
    original.REF=REF;m=original.modulo_entrada();b,_,k=m.abrir(a.start,Path(a.snapshot))
    if k!=2850:raise ValueError('Requires native P7 frame 2850')
    raw=original.remoto(original.PROBE_ROOT+'entradas/P7.json');b.roteiro.quadros=m.carregar_entrada(json.loads(raw))[0]
    ref=list(map(json.loads,lzma.decompress(original.remoto(original.PROBE_ROOT+'sondas/P7/quadros.jsonl.xz')).splitlines()))
    ref=next(r for r in ref if r['frame']==2851)
    cpu=b.cpu;uc=original.unicorn;x86=original.x86;target=b.sym['TextGetMessage']
    end=min(v for v in b.sym.values() if v>target);calls=[];pending=[];body=[];reads=[]
    r=lambda name:cpu.reg_read(getattr(x86,'UC_X86_REG_'+name))&0xffffffff
    def block(c,address,size,_):
        if address==target:
            ret=struct.unpack('<I',c.mem_read(r('ESP'),4))[0]
            pending.append((ret,len(calls)));calls.append(dict(phase=b.fase,argument_eax=hex(r('EAX')),caller_return=hex(ret)))
        if pending and address==pending[-1][0]:
            _,index=pending.pop();calls[index]['returned_eax']=hex(r('EAX'))
    def instruction(c,address,size,_):
        if target<address<end:body.append(hex(address))
    def read(c,access,address,size,value,_):reads.append(dict(address=hex(address),size=size,eip=hex(r('EIP')),phase=b.fase))
    cpu.hook_add(uc.UC_HOOK_BLOCK,block)
    cpu.hook_add(uc.UC_HOOK_CODE,instruction,begin=target+1,end=end-1)
    cpu.hook_add(uc.UC_HOOK_MEM_READ,read,begin=0x5099a4,end=0x5099a7);cpu.ctl_flush_tb()
    b.roteiro.iniciar_quadro(2851);b.executar_entre_quadros(300,2851)
    between=sha(b.directdraw.pixels('offscreen'));b.executar_quadro(600,2851)
    image=b.resumo_imagem(b.imagem())['sha256'];surface=sha(b.directdraw.pixels('offscreen'))
    assert calls and not pending and all(c['returned_eax']=='0x0' for c in calls)
    assert not body and not any(int(c['address'],16)==0x5099a4 for c in reads)
    assert between==ref['surfaces_between']['offscreen'] and surface==ref['surfaces_frame']['offscreen'] and image==ref['state_sha256']
    result=dict(schema='rising-lands/text-boundary-native-return/1',probe_ref=REF,frame=2851,
        executable_sha256=__import__('emulador').HASH_ORIGINAL,source_sha256=sha(Path(__file__).read_bytes()),
        snapshot_sha256=sha(Path(a.snapshot).read_bytes()),address=hex(target),calls=calls,body_instructions=body,pointer_overlap_reads=reads,
        native_surface_equal=True,native_whole_state_equal=True,code_sha256=b.sha256_codigo())
    Path(a.output).write_text(json.dumps(result,indent=1)+'\n');print(json.dumps(result))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--snapshot',required=True);p.add_argument('--output',required=True);main(p.parse_args())
