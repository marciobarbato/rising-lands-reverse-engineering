"""Original-only render inputs and drawing calls from pinned Missions scripted probes.

Reads remote source/input/evidence with git-show; never checks out or merges the Missions branch. Native WndProc
and all display routines execute under the probe's declared boundary contract (AffText remains a recorded boundary).
A frame-128 snapshot and optional resumable checkpoints are local task data, never tracked evidence.
"""
import argparse, base64, hashlib, json, lzma, struct, subprocess, sys, time, types, zlib
from pathlib import Path

AQUI=Path(__file__).resolve().parent
ROOT=AQUI.parents[1]
sys.path.insert(0,str(AQUI.parent/'missoes'))
import ambiente_missoes
import segmentos_quadros_missao as seg
from emulador import x86, unicorn

REF='f0588447b6cea3cc10701233a55bbcd16551e5e5'
PROBE_ROOT='pesquisas-paralelas/missoes/m3/'
sha=lambda d:hashlib.sha256(bytes(d)).hexdigest()
def remoto(path):return subprocess.check_output(['git','-C',str(ROOT),'show',REF+':'+path])
def modulo_entrada():
    name='entrada_roteirizada';m=types.ModuleType(name)
    m.__file__=str(AQUI.parent/'missoes/m3/entrada_roteirizada.py')
    sys.modules[name]=m
    exec(compile(remoto(PROBE_ROOT+'entrada_roteirizada.py'),f'git:{REF}:{PROBE_ROOT}entrada_roteirizada.py','exec'),m.__dict__)
    return m

BLOCOS=(('terrain',0x507d70,131072),('objects',0x507d74,65536),('aux',0x507dac,65536),('regions',0x4e0f38,131072),
        ('units',0x4e19a0,220800),('projectiles',0x5080f0,5600),
        *((f'discovery{i}',0x507d78+4*i,65536) for i in range(4)),
        *((f'lighting{i}',0x507d88+4*i,65536) for i in range(4)),('players',0x5080a8,100),('gray',0x4e24bc,256),('gray_effect',0x4e24c4,256),('tooltip_shadow',0x4e24b4,256))
BLITS={0x45b247:'PasteBobCmp',0x45b796:'PasteOmbreCmp',0x45c455:'PastePlayerCmp',0x45ba23:'PasteEclairCmp',
       0x45bf3d:'PasteNoirBlancCmp',0x45bcb0:'PasteGrisCmp',0x45c912:'Box',0x45cacd:'FilledBox',
       0x45cc35:'FilledBoxOmbre',0x45cd91:'FilledBoxGris',0x45aec2:'GetBob',0x45adf3:'PasteBob'}

class CapturadorSondasGraficos:
    def __init__(self,b):
        self.b=b;self.blobs={};self.rows=[];self.current=None;self.phase_frame=None
        cpu=b.cpu
        self.hooks=[cpu.hook_add(unicorn.UC_HOOK_CODE,self.entry,begin=0x417698,end=0x417698),
                    cpu.hook_add(unicorn.UC_HOOK_CODE,self.end,begin=0x417d30,end=0x417d30)]
        self.hooks += [cpu.hook_add(unicorn.UC_HOOK_CODE,self.blit,begin=a,end=a) for a in BLITS]
        self.hooks += [cpu.hook_add(unicorn.UC_HOOK_BLOCK,self.text,begin=b.sym['AffText'],end=b.sym['AffText'])]
        cpu.ctl_flush_tb()
    def blob(self,data):
        key=sha(data)
        if key not in self.blobs:self.blobs[key]=base64.b64encode(zlib.compress(bytes(data),6)).decode()
        return key
    def read(self,a,n):return bytes(self.b.cpu.mem_read(a,n))
    def u(self,a,n):return int.from_bytes(self.read(a,n),'little')
    def entry(self,c,a,n,_):
        if self.phase_frame is None:return
        if self.current is not None:raise RuntimeError('Nested AffGame')
        regions=[('dgroup',0x494000,0x8f000)]
        regions += [(name,self.u(slot,4),size) for name,slot,size in BLOCOS]
        regions += [('minimap',self.u(0x507d5c,4),self.u(0x496fe0,2)*self.u(0x496fe2,2))]
        if self.u(0x49a041,1):
            regions.append(('saved_background',self.u(0x49a03c,4),self.u(0x49a04a,2)*self.u(0x49a04c,2)))
        image=self.b.imagem()
        self.current=dict(frame=self.phase_frame,phase=self.b.fase,
            entry={name:[hex(base),self.blob(self.read(base,size))] for name,base,size in regions},
            before=self.blob(self.b.directdraw.pixels('offscreen')),
            cache=dict(keys=self.blob(self.read(self.u(0x49a050,4),1024)),cursor=self.u(0x49a04e,2),
                       payloads=self.blob(b''.join(image[f'alloc{2196+2*i:05d}'][1] for i in range(256)))),
            blits=[],text_boundaries=[])
    def blit(self,c,a,n,_):
        if self.current is None:return
        r=lambda k:c.reg_read(getattr(x86,'UC_X86_REG_'+k))&0xffffffff
        i16=lambda v:(v&65535)-65536 if v&32768 else v&65535
        name=BLITS[a];ev=[name,i16(r('EAX')),i16(r('EDX')),r('EBX')&65535,r('ECX')&255]
        if name=='PastePlayerCmp':ev.append(struct.unpack('<I',c.mem_read(r('ESP')+4,4))[0])
        if name in ('FilledBox','Box'):
            ev=[name,i16(r('EAX')),i16(r('EDX')),i16(r('EBX')),i16(r('ECX')),
                *struct.unpack('<2I',c.mem_read(r('ESP')+4,8))]
        if name in ('FilledBoxGris','FilledBoxOmbre'):
            ev=[name,i16(r('EAX')),i16(r('EDX')),i16(r('EBX')),i16(r('ECX')),struct.unpack('<I',c.mem_read(r('ESP')+4,4))[0]]
        if name in ('GetBob','PasteBob'):
            ev=[name,i16(r('EAX')),i16(r('EDX')),r('EBX')&65535,r('ECX')&65535,struct.unpack('<I',c.mem_read(r('ESP')+4,4))[0]]
        self.current['blits'].append(ev)
    def text(self,c,a,n,_):
        if self.current is None:return
        r=lambda k:c.reg_read(getattr(x86,'UC_X86_REG_'+k))&0xffffffff
        ptr=struct.unpack('<I',self.read(r('ESP')+4,4))[0]
        data=bytearray()
        for i in range(128):
            value=self.read(ptr+i,1)[0]
            if not value:break
            data.append(value)
        self.current['text_boundaries'].append(dict(text_hex=bytes(data).hex(),registers={k:hex(r(k)) for k in ('EAX','EBX','ECX','EDX','ESI','EDI')},
            stack=self.read(r('ESP'),24).hex(),surface_before=self.blob(self.b.directdraw.pixels('offscreen')),
            blits_before=len(self.current['blits']),address=hex(a)))
    def end(self,c,a,n,_):
        if self.current is None:return
        self.current.update(after=self.blob(self.b.directdraw.pixels('offscreen')),
                            exit_dgroup=self.blob(self.read(0x494000,0x8f000)))
        self.rows.append(self.current);self.current=None
    def detach(self):
        for h in self.hooks:self.b.cpu.hook_del(h)
        self.b.cpu.ctl_flush_tb()

def prepare(args,m):
    start=Path(args.start);start.mkdir(parents=True,exist_ok=False)
    b=m.bancada_fresca(1_000_000);b.iniciar_relogio();b.executar_inicio();b.executar_mission_load(60)
    for phase,_ in b.executar_quadros(128,600):pass
    expected=json.loads(lzma.decompress((AQUI.parent/'missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz').read_bytes()))
    expected=next(p['state_after']['summary'] for p in expected['phases'] if p['phase']=='frame128')
    summary=b.resumo_imagem(b.imagem())
    if summary!=expected:raise RuntimeError(('Frame128 differs',summary,expected))
    path=start/'instantaneo-00128.pickle';digest=seg.salvar(b,path,128)
    manifest=dict(ticks=1_000_000,snapshot=path.name,snapshot_sha256=digest,frame128_summary=summary,probe_ref=REF)
    (start/'manifesto.json').write_text(json.dumps(manifest,indent=1)+'\n')
    print(json.dumps(manifest),flush=True)

def capture(args,m):
    t=time.monotonic();b,at,k0=m.abrir(args.start,Path(args.resume) if args.resume else None)
    raw=remoto(PROBE_ROOT+'entradas/'+args.probe+'.json');schedule=json.loads(raw)
    frames,stop=m.carregar_entrada(schedule);b.roteiro.quadros=frames
    stop=min(args.to or stop,stop)
    if stop-k0>1000:raise ValueError('At most 1000 native frames per MacBook invocation; route longer jobs to Mac mini')
    refraw=remoto(PROBE_ROOT+'sondas/'+args.probe+'/quadros.jsonl.xz')
    references={r['frame']:r for r in map(json.loads,lzma.decompress(refraw).splitlines())}
    recorder=CapturadorSondasGraficos(b);checks=[]
    checkpoints={int(k) for k in args.checkpoint_frames.split(',') if k};requested_stop=stop;status='complete'
    for k in range(k0+1,stop+1):
        b.roteiro.iniciar_quadro(k);recorder.phase_frame=k
        b.executar_entre_quadros(300,k)
        drawn=recorder.rows[-1] if recorder.rows and recorder.rows[-1]['frame']==k else None
        actual=sha(b.directdraw.pixels('offscreen'));expected=references[k]['surfaces_between']['offscreen']
        if actual!=expected:raise RuntimeError(f'{args.probe} frame {k}: native surface differs from pinned probe')
        b.executar_quadro(600,k)
        if sha(b.directdraw.pixels('offscreen'))!=references[k]['surfaces_frame']['offscreen']:
            raise RuntimeError(f'{args.probe} frame {k}: frame surface differs')
        if b.resumo_imagem(b.imagem())['sha256']!=references[k]['state_sha256']:
            raise RuntimeError(f'{args.probe} frame {k}: whole native state differs')
        if drawn:drawn['probe_surface_sha256']=expected
        checks.append(dict(frame=k,drawn=bool(drawn),surface_equal=True,state_equal=True))
        b.roteiro.eventos.clear()
        if k%50==0:print(args.probe,k,'native surface/state equal',flush=True)
        if k in checkpoints:
            path=Path(args.start)/f'{args.probe}-{k:05d}.pickle'
            if not path.exists():seg.salvar(b,path,k)
        if time.monotonic()-t>1080:
            status='budget_stop';stop=k;break
    recorder.phase_frame=None;recorder.detach()
    checkpoint=Path(args.start)/f'{args.probe}-{stop:05d}.pickle'
    if not checkpoint.exists():digest=seg.salvar(b,checkpoint,stop)
    else:digest=sha(checkpoint.read_bytes())
    out=dict(schema='rising-lands/m3-probe-render-native/1',method=__doc__,probe=args.probe,probe_ref=REF,
             input_sha256=sha(raw),probe_records_sha256=sha(refraw),frames=[k0+1,stop],
             snapshot=dict(path=str(checkpoint),sha256=digest),elapsed_seconds=round(time.monotonic()-t,3),
             requested_stop=requested_stop,status=status,executable_sha256=__import__('emulador').HASH_ORIGINAL,
             producing_revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
             source_sha256=sha(Path(__file__).read_bytes()),boundary_contract='Missions display v2: AffText declared boundary (not native glyph drawing)',
             checks=checks,rows=recorder.rows,blobs=recorder.blobs,code_sha256=b.sha256_codigo())
    Path(args.output).write_text(json.dumps(out));print(json.dumps({k:v for k,v in out.items() if k not in ('rows','blobs','checks','method')}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--prepare',action='store_true')
    p.add_argument('--probe',choices=('P1','P2','P3','K1'));p.add_argument('--to',type=int);p.add_argument('--resume')
    p.add_argument('--checkpoint-frames',default='');p.add_argument('--output');args=p.parse_args();m=modulo_entrada()
    if args.prepare:prepare(args,m)
    else:capture(args,m)
