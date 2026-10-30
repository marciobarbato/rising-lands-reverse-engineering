"""Bounded original-only S1 continuation for Graphics checkpoints; no reconstructed routine is imported."""
import argparse,json,time
from pathlib import Path
import capturar_sondas_graficos_m3 as original

REF='fd56f69'

def main(a):
    original.REF=REF;m=original.modulo_entrada();b,_,start=m.abrir(a.start,Path(a.snapshot) if a.snapshot else None)
    if not 0<a.to-start<=800:raise ValueError('At most800 original frames per native invocation')
    raw=original.remoto(original.PROBE_ROOT+'entradas/S1.json');b.roteiro.quadros=m.carregar_entrada(json.loads(raw))[0]
    t=time.monotonic();changes=[];previous=None;checks=[]
    for k in range(start+1,a.to+1):
        b.roteiro.iniciar_quadro(k);b.executar_entre_quadros(300,k);b.executar_quadro(600,k)
        image=b.imagem();summary=b.resumo_imagem(image);checks.append([k,summary['sha256']])
        pool=bytes(b.cpu.mem_read(0x49a0c8,276000))
        active=[[i,pool[i*276+8],pool[i*276+5],pool[i*276+4]] for i in range(1000) if pool[i*276+5]]
        if active!=previous:changes.append(dict(frame=k,structures=active));previous=active
        b.roteiro.eventos.clear()
        if k%100==0:print('S1',k,'original structure inventory',active,flush=True)
        if time.monotonic()-t>1080:raise RuntimeError('18-minute native budget exhausted')
    path=Path(a.start)/f'S1-{a.to:05d}.pickle';digest=original.seg.salvar(b,path,a.to)
    result=dict(schema='rising-lands/graphics-s1-native-prefix/1',probe_ref=REF,frames=[start+1,a.to],
        executable_sha256=__import__('emulador').HASH_ORIGINAL,input_sha256=original.sha(raw),
        source_sha256=original.sha(Path(__file__).read_bytes()),snapshot=dict(path=str(path),sha256=digest),
        structure_changes=changes,states=checks,elapsed_seconds=round(time.monotonic()-t,3),code_sha256=b.sha256_codigo())
    Path(a.output).write_text(json.dumps(result,indent=1)+'\n');print(result['snapshot'],flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--snapshot');p.add_argument('--to',type=int,required=True);p.add_argument('--output',required=True)
    main(p.parse_args())
