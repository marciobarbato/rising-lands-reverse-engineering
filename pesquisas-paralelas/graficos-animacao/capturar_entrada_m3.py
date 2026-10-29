"""Original-only M3 input-time display cases at Core's accepted frame-1 leaf-call pause.

Native setup routines create selections and action icons. Declared writes explore display globals and record fields.
All cases restore CPU, mapped state, stack, DirectDraw metadata and surface bytes. Hooks only record blitter/Box
arguments; the intact AffGame executes to DDUnlockSurface, with no substituted game routines.
"""
import argparse, base64, copy, hashlib, json, struct, subprocess, sys, time, zlib
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent/'missoes'))
import ambiente_missoes
import percurso_quadro1 as pq
from oraculo_quadro_missao import Isolamento, BancadaCargaMissaoOriginal
from emulador import RETORNO, x86
import unicorn
from extrair_proveniencia_hud import EXE, ler

sha = lambda d: hashlib.sha256(bytes(d)).hexdigest()
BLOBS = {}
def blob(d):
    k = sha(d); BLOBS.setdefault(k, base64.b64encode(zlib.compress(bytes(d), 9)).decode()); return k

def casos(base, read):
    w = lambda a,v,n=2: (a, int(v).to_bytes(n,'little'))
    out = [dict(name='baseline', setup=[], writes=[])]
    for i in (0, 11, 12, 13, 15):
        setup = [('EnginAddSelection', dict(EAX=i, EDX=0)), ('CalculIconeAction', {})]
        out.append(dict(name=f'selected_unit_{i}', setup=setup, writes=[]))
        out.append(dict(name=f'hover_unit_{i}', setup=[], writes=[w(0x496ac2,i)]))
    for mode in (1,2,3):
        out.append(dict(name=f'selection_mode_{mode}_unit12', setup=[], writes=[w(0x496ac2,12),w(0x508f8f,mode,1)]))
    for level in (1,3,7):
        for counter in (4,5):
            out.append(dict(name=f'experience_builder_{level}_frame{counter}', setup=[],
                            writes=[w(base+12*276+0xba,1,1),w(base+12*276+0xaf,level<<5,1),w(0x508f7c,counter,4)]))
    for slot in (0,2,8,9):
        out.append(dict(name=f'builder_action_slot_{slot}', setup=[('EnginAddSelection',dict(EAX=12,EDX=0)),('CalculIconeAction',{})],
                        writes=[w(0x496d4a,slot)]))
    for values in ((10,6,0,0),(0,0,7,0),(1,0,0,0),(0,0,0,1234)):
        out.append(dict(name='cost_'+'_'.join(map(str,values)),setup=[],
                        writes=[w(a,v) for a,v in zip((0x4e0612,0x4e0614,0x4e0616,0x4e0618),values)]))
    for rect in ((100,100,300,250),(300,250,100,100),(780,530,840,580)):
        out.append(dict(name='drag_'+'_'.join(map(str,rect)),setup=[],
                        writes=[w(0x4e19b0,1,1),(0x49a024,struct.pack('<4h',*rect))]))
    for counter, icon in ((4,0x1e03),(5,0x1e03),(4,0x1e09)):
        out.append(dict(name=f'target_frame{counter}_icon{icon}',setup=[],writes=[w(0x496204,4113),w(0x4e05ac,icon),w(0x508f7c,counter,4)]))
    for value in (1,4,16):
        out.append(dict(name=f'second_cursor_{value}',setup=[],writes=[w(0x4e062c,value)]))
    out.append(dict(name='selected_sanctuary',setup=[('BatimentSelection',dict(EAX=0)),('CalculIconeAction',{})],writes=[]))
    builder=[('EnginAddSelection',dict(EAX=12,EDX=0)),('CalculIconeAction',{})]
    maximum=int.from_bytes(read(0x4965b6+50*7,2),'little')
    for percent in (0,1,35,36,75,76,99,100):
        out.append(dict(name=f'builder_health_{percent}',setup=builder,
                        writes=[w(base+12*276+0x9a,maximum*percent//100)]))
    out.append(dict(name='builder_selected_cave_cost',setup=builder,
                    writes=[w(0x4e0612,10),w(0x4e0614,6),w(0x496d4a,2)]))
    for level in (2,4,5,6):
        out.append(dict(name=f'builder_selected_experience_{level}',setup=builder,
                        writes=[w(base+12*276+0xaf,level<<5,1)]))
    for value in (0,7,10,99,100,999):
        out.append(dict(name=f'action_counter_{value}',setup=builder,
                        writes=[w(0x4e2412,2),w(0x4e2414,value)]))
    for value in (0,1,50,99,100):
        out.append(dict(name=f'action_disabled_{value}',setup=builder,
                        writes=[w(0x4e2412,0),w(0x4e2414,value)]))
    for slot in (0,8,9):
        out.append(dict(name=f'action_scroll_{slot}',setup=builder,
                        writes=[w(0x4e2440,1),w(0x4e2446,1),w(0x496d4a,slot)]))
    for value in (10,99,100,999,1000,9999):
        out.append(dict(name=f'cost_counter_{value}',setup=[],writes=[w(0x4e0618,value)]))
    return out


def capturar(saida):
    t0=time.monotonic(); b, cap=pq._bancada('exibicao'); dd=b.directdraw
    rows=[]; reproduction={}; pause={}
    class Pausa(Isolamento):
        def executar(self,regs):
            if rows or b.fase!='frame1': return
            self.ativo=False
            ctx, blocks=self._salvar(); surfaces=bytes(b.cpu.mem_read(dd.base_superficies,dd.tamanho_superficies))
            states=copy.deepcopy(dd.superficies); trace=copy.deepcopy(b.rastro)
            lens=(len(dd.eventos),len(b.eventos_pulados),len(b.eventos_fronteira))
            pause.update(registers={k:hex(v) for k,v in regs.items()},state_sha256=b.resumo_imagem(blocks))
            cpu=b.cpu; read=lambda a,n:bytes(cpu.mem_read(a,n)); u=lambda a,n:int.from_bytes(read(a,n),'little')
            esp=regs['ESP']-0x100
            def call(name,r,stops=(RETORNO,)):
                cpu.mem_write(esp,struct.pack('<I',RETORNO)); cpu.reg_write(x86.UC_X86_REG_ESP,esp)
                for k,v in r.items():cpu.reg_write(getattr(x86,'UC_X86_REG_'+k),v)
                b._retomando=set()
                return BancadaCargaMissaoOriginal._correr(b,'leaf',b.sym[name],{},stops,retomar=True)
            def restore():
                self._restaurar(ctx,blocks); cpu.mem_write(dd.base_superficies,surfaces)
                dd.superficies=copy.deepcopy(states); b.rastro=copy.deepcopy(trace)
                del dd.eventos[lens[0]:], b.eventos_pulados[lens[1]:], b.eventos_fronteira[lens[2]:]
            finish=0x417d30
            stophook=cpu.hook_add(unicorn.UC_HOOK_CODE,b._parar_se_pedido,begin=finish,end=finish)
            try:
                for case in casos(u(0x4e19a0,4),read):
                    restore(); setup=[]
                    for name,r in case['setup']:
                        result=call(name,r); assert result['EIP']==RETORNO,(name,result)
                        setup.append(dict(routine=name,registers=r,returned=True))
                    for a,d in case['writes']:cpu.mem_write(a,bytes(d))
                    # Save only consumer-visible buffers plus the bag arena. Banks are read-only original assets.
                    regions=[('dgroup',0x494000,0x523000-0x494000)]
                    for name,slot,n in (('terrain',0x507d70,131072),('objects',0x507d74,65536),('aux',0x507dac,65536),
                            ('regions',0x4e0f38,131072),('units',0x4e19a0,220800),('projectiles',0x5080f0,5600),
                            *((f'discovery{i}',0x507d78+4*i,65536) for i in range(4)),
                            *((f'lighting{i}',0x507d88+4*i,65536) for i in range(4)),
                            ('minimap',0x507d5c,u(0x496fe0,2)*u(0x496fe2,2)),('players',0x5080a8,100),('noir_blanc',0x4e24bc,256)):
                        regions.append((name,u(slot,4),n))
                    entry={name:[hex(a),blob(read(a,n))] for name,a,n in regions}
                    before=blob(dd.pixels('offscreen'))
                    image=b.imagem()
                    cache=dict(keys=blob(read(u(0x49a050,4),1024)),cursor=u(0x49a04e,2),
                               payloads=blob(b''.join(image[f'alloc{2196+2*i:05d}'][1] for i in range(256))))
                    blits=[]
                    names={0x45b247:'PasteBobCmp',0x45b796:'PasteOmbreCmp',0x45c455:'PastePlayerCmp',0x45ba23:'PasteEclairCmp',0x45bf3d:'PasteNoirBlancCmp',0x45c912:'Box',0x45cacd:'FilledBox'}
                    def record(c,a,n,_):
                        r=lambda k:c.reg_read(getattr(x86,'UC_X86_REG_'+k))&0xffffffff
                        s16=lambda v:(v&65535)-65536 if v&32768 else v&65535
                        ev=[names[a],s16(r('EAX')),s16(r('EDX')),r('EBX')&65535,r('ECX')&255]
                        if names[a]=='PastePlayerCmp':ev.append(struct.unpack('<I',c.mem_read(r('ESP')+4,4))[0])
                        if names[a] in ('Box','FilledBox'):
                            ev=[names[a],s16(r('EAX')),s16(r('EDX')),s16(r('EBX')),s16(r('ECX')),*struct.unpack('<2I',c.mem_read(r('ESP')+4,8))]
                        blits.append(ev)
                    hooks=[cpu.hook_add(unicorn.UC_HOOK_CODE,record,begin=a,end=a) for a in names]
                    try:r=call('AffGame',{},(finish,))
                    finally:
                        for h in hooks:cpu.hook_del(h)
                        cpu.ctl_flush_tb()
                    assert r['EIP']==finish,r
                    rows.append(dict(name=case['name'],setup=setup,writes=[[hex(a),bytes(d).hex()] for a,d in case['writes']],
                                     entry=entry,cache=cache,before=before,after=blob(dd.pixels('offscreen')),blits=blits,
                                     exit_dgroup=blob(read(0x494000,0x523000-0x494000))))
                    print(case['name'],len(blits),flush=True)
            finally:
                cpu.hook_del(stophook);restore();self.ativo=True;b.fase='frame1';b.windows.fase='frame1'
    iso=Pausa(b,('ProcessInputGame',));iso.instalar()
    ref={p['phase']:p['state_after']['summary'] for p in cap['phases']}
    for phase,run in (('load_tail',lambda:b.executar_cauda_carga(600)),('between_frames',lambda:b.executar_entre_quadros(300)),('frame1',lambda:b.executar_quadro(600))):
        run();reproduction[phase]=b.resumo_imagem(b.imagem())==ref[phase]
    reproduction['code_unchanged']=b.sha256_codigo()==cap['code_integrity']['after']
    intervals=[(0x412390,0x412637),(0x412923,0x412962),(0x413568,0x4136e4),(0x41087e,0x410f64),(0x441004,0x4410b7),
               (0x441108,0x44113e),(0x44f9a6,0x44f9cc),(0x4422b0,0x4422cc),(0x416f29,0x4171f8),(0x40f758,0x40f8aa),
               (0x4180d8,0x418186),(0x417ac8,0x417d30)]
    exe=EXE.read_bytes()
    out=dict(schema='rising-lands/m3-input-render-native/1',executable_sha256=sha(exe),producing_revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
             command='python3 -B pesquisas-paralelas/graficos-animacao/capturar_entrada_m3.py --saida ' + str(saida),pause=pause,reproduction=reproduction,
             method=__doc__,elapsed_seconds=round(time.monotonic()-t0,3),cases=rows,blobs=BLOBS,
             intervals=[dict(start=hex(a),end=hex(z),sha256=sha(ler(exe,a,z))) for a,z in intervals])
    Path(saida).write_text(json.dumps(out));print(json.dumps(dict(cases=len(rows),reproduction=reproduction,seconds=out['elapsed_seconds'])))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--saida',required=True);capturar(p.parse_args().saida)
