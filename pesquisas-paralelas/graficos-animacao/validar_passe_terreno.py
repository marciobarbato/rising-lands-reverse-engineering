"""Complete native interior AffTerrain traces, opaque blocks and object pixels."""
import hashlib
import json
import struct
import time
from bancada_x86 import RETORNO, SUPERFICIE, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, png
from objetos import compor_passe
from sequenciais import consultar_objeto_v6
from cache_terreno import resolver_bloco_terreno
from validar_cache_terreno import BancadaCache, initial_cache, cache_from_initial
from passe_terreno import (terreno_de_construcao,planejar_passe_terreno,executar_passe_terreno,
    pixels_bloco_terreno,compor_bloco_terreno)


def sha(data):return hashlib.sha256(data).hexdigest()


def make_case(name,origin=(20,20),window=(4,4),inset=0,*,objects=True,uniform=False,clip=None,camera=0):
    ox,oy=origin;w,h=window;terrain=[];flags=[];items=[]
    values=(1,349,701,702,732,762,774,799,819,855,879,899,931,983,1007,1081,1080,300)
    for row in range(h):
        for col in range(w):
            index=row*w+col;cell=(oy+row)*256+ox+col
            terrain.append([cell,1 if uniform else values[index%len(values)]])
            flags.append([cell,0 if uniform else (0,0,1,2,3,4,8,9,12,15,16,224)[index%12],
                0 if uniform else (0,16,0,1,2,4,8,15,224)[index%9]])
    if objects:
        for index,(code,aux) in enumerate(((13,0),(22,0),(54,255),(66,7),(67,14),(68,31),(28,0),(52,0),(253,0))):
            if index>=w*h:break
            cell=(oy+index//w)*256+ox+index%w;items.append([cell,code,aux]);flags[index][1:]=[0,16 if index%2 else 0]
    return dict(name=name,origin=list(origin),window=list(window),inset=inset,camera=camera,terrain=terrain,flags=flags,
        objects=items,clip=clip or [0,0,w*32-1,h*32-1],initial_cache=initial_cache(cursor=255))


def buffers(case):
    terrain=bytearray(struct.pack('<H',1)*65536);objects=bytearray(65536);aux=bytearray(65536)
    discovery=bytearray(65536);light=bytearray(65536)
    for cell,word in case['terrain']:struct.pack_into('<H',terrain,cell*2,word)
    for cell,d,l in case['flags']:discovery[cell]=d;light[cell]=l
    for cell,code,value in case['objects']:objects[cell]=code;aux[cell]=value
    return bytes(terrain),bytes(objects),bytes(aux),bytes(discovery),bytes(light)


def plan_events(plan):
    out=[]
    executar_passe_terreno(plan,bloco=lambda x,y,c,s:out.append(['bloco',x,y,c,s]),
        vegetacao=lambda x,y,c:out.append(['vegetacao',x,y,c]))
    return out


def compose(catalog,case,shadow,*,wrong_order=False):
    terrain,objects,aux,discovery,light=buffers(case)
    plan=planejar_passe_terreno(terrain,light,origem=case['origin'],janela_celulas=case['window'],margem_i8=case['inset'])
    cache=cache_from_initial(case['initial_cache']);w,h=(v*32 for v in case['window'])
    out=bytes((index*17+23)%256 for index in range(w*h));ids=[]
    def block(x,y,cell,source):
        nonlocal out
        selected=resolver_bloco_terreno(catalog,cache,id_terreno_u16=source,descoberta_u8=discovery[cell],
            iluminacao_u8=light[cell],tabela_sombra=shadow)
        ident=selected['id_motor'];ids.append(ident)
        out=compor_bloco_terreno(out,w,h,pixels_bloco_terreno(catalog,cache,ident),x,y)
    def vegetation(x,y,cell):
        nonlocal out
        if objects[cell] in (0,253) or discovery[cell]&31:return
        p=consultar_objeto_v6(objects[cell],auxiliar_u8=aux[cell],descoberta_u8=discovery[cell],iluminacao_u8=light[cell])
        out=compor_passe(catalog,out,w,h,p,'terreno',x,y,tabela_sombra=shadow,recorte=case['clip'])
    if wrong_order:
        for item in plan['celulas']:block(item['x'],item['y'],item['celula'],item['id_terreno_u16'])
        for item in plan['celulas']:vegetation(item['x'],item['y'],item['celula'])
    else:executar_passe_terreno(plan,bloco=block,vegetacao=vegetation)
    return out,cache,ids


class BancadaTerreno(BancadaCache):
    def __init__(self,catalog):
        self.trace=False;self.events=[];self.resolved_ids=[];self.query_input=None;self.width=0
        super().__init__(catalog);self.world={}
        for name,global_pointer,size in [('terrain',0x507d70,131072),('objects',0x507d74,65536),
                ('aux',0x507dac,65536),('attributes',0x507da8,65536)]:
            pointer=self.alocar(size);self.world[name]=pointer;self.escrever(global_pointer,struct.pack('<I',pointer));self.escrever(pointer,bytes(size))

    def _hook(self,cpu,address,size,data):
        if self.trace:
            if address==0x40fd95:self.query_input=(self.reg('EAX')&65535,self.reg('EDX')&65535)
            elif address==0x41077d:self.resolved_ids.append(self.reg('EAX')&65535)
            elif address==0x45c72a:
                offset=self.reg('EAX')-SUPERFICIE;source,cell=self.query_input
                assert self.reg('EBX')&65535==cell
                self.events.append(['bloco',offset%self.width,offset//self.width,cell,source])
            elif address==0x410085:
                self.events.append(['vegetacao',(self.reg('EAX')+32768)%65536-32768,
                    (self.reg('EDX')+32768)%65536-32768,self.reg('EBX')&65535])
        super()._hook(cpu,address,size,data)

    def resume(self,stops):
        self.execucoes+=1;self.paradas=set(stops)|{RETORNO}
        self.cpu.emu_start(self.reg('EIP'),RETORNO,timeout=2000000,count=300000)
        if self.reg('EIP') not in self.paradas:raise RuntimeError('Terrain segment exceeded its declared limit')
        return dict(EIP=self.reg('EIP'),ESP=self.reg('ESP'))

    def draw(self,case,shadow,*,pixels):
        terrain,objects,aux,discovery,light=buffers(case);camera=case['camera']
        for name,payload in [('terrain',terrain),('objects',objects),('aux',aux)]:self.escrever(self.world[name],payload)
        self.escrever(self.world['attributes'],bytes(65536))
        for index,payload in enumerate((discovery,light)):
            self.escrever(self.maps[index][camera],payload);self.expected_maps[index][camera]=bytearray(payload)
        self.escrever(0x508041,bytes([camera]));self.escrever(0x508724,struct.pack('<HH',*case['window']))
        self.escrever(0x508f90,bytes([case['inset']]))
        w,h=(value*32 for value in case['window']);self.width=w
        background=bytes((index*17+23)%256 for index in range(w*h))
        self.preparar_superficie(w,h,background,case['clip'],shadow);self.escrever(0x49a018,struct.pack('<H',w))
        if w*h<0x100000:self.escrever(SUPERFICIE+w*h,bytes([204])*16)
        old_clip=self.ler(0x49a01c,8);self.reset_cache(case['initial_cache'])
        intervals=[(0x410085,0x41087e),(0x410b38,0x410b40),(0x42302d,0x423355),
            (0x40fd95,0x410085),(0x4766d6,0x47670a),(0x47693a,0x476968),
            (0x45c72a,0x45c8df),(0x45f7ba,0x45f7d8),(0x45f6de,0x45f6e1)]
        stubs={0x40fd95:lambda b:b.retornar_stub(1),0x45c72a:lambda b:b.retornar_stub(),0x410085:lambda b:b.retornar_stub()}
        if pixels:intervals += [(0x45b247,0x45b4fd)]+self.intervalos_sombra();stubs={}
        self.events=[];self.resolved_ids=[];self.trace=True
        result=self.executar(0x41068e,intervals,dict(EAX=case['origin'][0],EDX=case['origin'][1]),
            stubs=stubs,paradas=[0x4107ed],limite=300000)
        # Alternate checkpoints preserve original CPU/stack and avoid stopping
        # again at the same instruction before it has executed.
        while result['EIP']!=RETORNO:
            assert result['EIP']==0x4107ed
            result=self.resume([0x4107c9]);assert result['EIP']==0x4107c9
            result=self.resume([0x4107ed])
        self.trace=False;assert result['ESP']==0x2008004
        for name,payload in [('terrain',terrain),('objects',objects),('aux',aux)]:assert self.ler(self.world[name],len(payload))==payload
        assert self.ler(self.world['attributes'],65536)==bytes(65536) and self.ler(0x49a01c,8)==old_clip
        self.verify_read_only_inputs()
        if w*h<0x100000:assert self.ler(SUPERFICIE+w*h,16)==bytes([204])*16
        return dict(events=list(self.events),resolved_ids=list(self.resolved_ids),stop=hex(result['EIP']),
            entries=self.ler(self.entries,1024),raw_blocks=self.ler(self.raw,256*1056),next_index=struct.unpack('<H',self.ler(0x49a04e,2))[0]),self.ler(SUPERFICIE,w*h)


def validate():
    exigir_area_editavel();start=time.monotonic();catalog=Catalogo();b=BancadaTerreno(catalog)
    base,image=imagem_pe();regions=[]
    for name,first,last in [('AffTerrain',0x41068e,0x41087e),('construction_predicate',0x42302d,0x423355),('AffBloc',0x45c72a,0x45c779)]:
        raw=image[first-base:last-base];regions.append(dict(name=name,start=hex(first),end=hex(last),bytes_hex=raw.hex(),sha256=sha(raw)))
    evidence=dict(exe_sha256=HASH_EXE,regions=regions,predecessor_sources={name:sha((RAIZ/name).read_bytes()) for name in ('cache_terreno.py','objetos.py','sequenciais.py','graficos.py')})
    (RAIZ/'evidencias/passe-terreno.json').write_text(json.dumps(evidence,indent=2)+'\n')
    report=dict(exe_sha256=HASH_EXE,unicorn_version=unicorn.__version__,limits=dict(instructions_per_segment=300000,timeout_us=2000000),
        substitutions=dict(traces=['GetNumBob returns fixed validID1; AffBloc and AffVegetTerrain intercepted'],
            pixels=[],bank_loading=['file IO/allocation'],cache_payloads=['guarded explicit synthetic RAM snapshot']),traces=[],pixels=[],blocks=[])
    predicate=bytearray(8192);cell=0x1234
    for word in range(65536):
        b.escrever(b.world['terrain']+cell*2,struct.pack('<H',word))
        result=b.executar(0x42302d,[(0x42302d,0x423355)],dict(EAX=0xdead1234,EBX=0x12345678,EDX=0xabcdef12))
        flag=result['EAX']&255;assert flag in (0,1) and bool(flag)==terreno_de_construcao(word)
        assert result['ESP']==0x2008004 and result['EBX']==0x12345678 and result['EDX']==0xabcdef12
        assert b.ler(b.world['terrain']+cell*2,2)==struct.pack('<H',word)
        if flag:predicate[word//8]|=1<<(word%8)
    report['predicate_bitmap_hex']=predicate.hex();print('Original construction predicate:65536 full returns',flush=True)
    shadow=bytes.fromhex(json.loads((RAIZ/'validacao/x86-cache-terreno.json').read_text())['tables_hex'][0]);report['shadow_table_hex']=shadow.hex()
    cases=[]
    for size in range(1,33):
        cases.append(make_case('row_'+str(size),(256-size,255),(size,1),objects=False))
        cases.append(make_case('column_'+str(size),(255,256-size),(1,size),objects=False))
    cases += [make_case('interior'),make_case('inset',(20,20),(8,6),1),make_case('empty_inset',(20,20),(4,4),2),
        make_case('corner',(252,252),(4,4),camera=3),make_case('large',(224,224),(32,32),objects=False,uniform=True),
        make_case('narrow',(100,100),(31,17),8,objects=False),make_case('small_clip',clip=[50,50,60,60]),
        make_case('hidden_invalid',(20,20),(4,4),objects=False)]
    last=cases[-1];last['terrain'][-1][1]=65535;last['flags'][-1][1]=16
    for case in cases:
        terrain,_,_,_,light=buffers(case);plan=planejar_passe_terreno(terrain,light,origem=case['origin'],janela_celulas=case['window'],margem_i8=case['inset'])
        native,_=b.draw(case,shadow,pixels=False);assert native['events']==plan_events(plan)
        report['traces'].append(dict(case=case,events=native['events'],stop=native['stop']))
    print('Original full terrain traces:',len(cases),flush=True)
    for case in cases[-8:]:
        native,pixels=b.draw(case,shadow,pixels=True);out,cache,ids=compose(catalog,case,shadow)
        assert pixels==out and native['resolved_ids']==ids
        assert native['entries']==bytes(cache.registros) and native['raw_blocks']==bytes(cache.blocos_crus) and native['next_index']==cache.proximo_u16
        wrong,_,_=compose(catalog,case,shadow,wrong_order=True)
        report['pixels'].append(dict(case=case,sha256=sha(pixels),resolved_ids=ids,cache_entries_sha256=sha(native['entries']),
            cache_raw_sha256=sha(native['raw_blocks']),next_index=native['next_index'],stop=native['stop'],wrong_order_changed_pixels=sum(a!=c for a,c in zip(pixels,wrong))))
        if case['name']=='interior':
            palette=catalog.paleta();rgba=bytes(c for index in pixels for c in (*palette[index*3:index*3+3],255))
            (RAIZ/'artefatos/cena-passe-terreno.png').write_bytes(png(128,128,rgba))
    # Standalone AffBloc ignores the clip rectangle and raw row-header values.
    b.reset_cache(initial_cache())
    for ident in (1,300,1081,1090):
        for w,h,x,y in ((32,32,0,0),(64,64,0,0),(64,64,32,32),(96,64,13,17),(128,128,96,96)):
            background=bytes((index*17+23)%256 for index in range(w*h));b.preparar_superficie(w,h,background,(0,0,0,0),shadow)
            ptr=struct.unpack('<I',b.ler(b.bank['tabela']+(ident-1)*4,4))[0];rawptr=struct.unpack('<I',b.ler(ptr+8,4))[0]
            result=b.executar(0x45c72a,[(0x45c72a,0x45c779)],dict(EAX=SUPERFICIE+y*w+x,EDX=rawptr))
            assert result['EIP']==RETORNO and result['ESP']==0x2008004
            out=compor_bloco_terreno(background,w,h,pixels_bloco_terreno(catalog,cache_from_initial(initial_cache()),ident),x,y)
            assert out==b.ler(SUPERFICIE,w*h)
            report['blocks'].append(dict(id=ident,w=w,h=h,x=x,y=y,sha256=sha(out)))
    report.update(result='PASS',predicate_calls=65536,terrain_full_calls=len(report['traces'])+len(report['pixels']),
        standalone_block_calls=len(report['blocks']),bank_calls=2,bounded_segments=b.execucoes,instructions_observed=b.instrucoes,
        expected_exceptions=0,expected_limits=0,skips=0,seconds=round(time.monotonic()-start,3))
    (RAIZ/'validacao/x86-passe-terreno.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',len(report['pixels']),'complete terrain buffers;',len(report['blocks']),'opaque blocks;',b.execucoes,'bounded segments',flush=True)


if __name__=='__main__':validate()
