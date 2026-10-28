"""Complete original attack display, raw dispatch routes and indexed buffers."""
import hashlib
import json
import struct
import time
from bancada_x86 import UNIDADE, SUPERFICIE, RETORNO, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, ORDEM, QUANTIDADES, png
from validar_unidade_tipo2 import BancadaTipo2, observed
from ataque_grafico import consultar_ataque_grafico, compor_ataque_grafico


def sha(data):return hashlib.sha256(data).hexdigest()


def fixture(kind=0,state=1,aux=1,direction=1,phase=0,count=8,dx=0,dy=0,x=64,y=48,index=0,selected=0,camera=0,hover=65535,mode=0):
    return [kind,state,aux,direction,phase,count,dx,dy,x,y,index,selected,camera,hover,mode]


def selection(v):return dict(indice_u16=v[10],camera_u8=v[12],indice_selecionado_u16=v[13],modo_selecao_u8=v[14])


def runtime_record(template,v):
    raw=bytearray(template);raw[0]=0;raw[1]=v[0];raw[2]=v[1];raw[0x8a]=v[2]
    raw[0x91]=v[3];raw[0xa4]=v[4];raw[0xa6]=v[5];raw[0x86]=v[6]&255;raw[0x87]=v[7]&255
    raw[0xbd]=v[11];raw[0xdc]=raw[0xba]=0;struct.pack_into('<H',raw,0x74,100)
    return bytes(raw)


class BancadaAtaque(BancadaTipo2):
    def draw_attack(self,raw,v,*,pixels=False,shadow=None,clip=(0,0,127,127)):
        pool=bytearray(800*276);index=v[10];pool[index*276:index*276+276]=raw;self.escrever(UNIDADE,pool)
        self.escrever(0x508041,bytes([v[12]]));self.escrever(0x496ac2,struct.pack('<H',v[13]));self.escrever(0x508f8f,bytes([v[14]]))
        intervals=[(0x41591f,0x415a57),(0x41374c,0x414495),(0x410fcc,0x41209d),
            (0x442025,0x442065),(0x44fffe,0x45007a),(0x467d97,0x467da6)]
        stubs={address:lambda b:b.retornar_stub() for address in (0x45b247,0x45b796)}
        if pixels:
            background=bytes((i*17+23)%256 for i in range(128*128));self.preparar_superficie(128,128,background,clip,shadow)
            intervals += [(0x45b247,0x45b4fd)]+self.intervalos_sombra();stubs={}
        self.layers=[]
        result=self.executar(0x41591f,intervals,dict(EAX=v[8],EDX=v[9],EBX=index),
            stubs=stubs,paradas=[0x412390,0x4137db,0x410be4],limite=300000)
        assert self.ler(UNIDADE,len(pool))==bytes(pool)
        assert self.ler(0x508041,1)==bytes([v[12]]) and self.ler(0x496ac2,2)==struct.pack('<H',v[13]) and self.ler(0x508f8f,1)==bytes([v[14]])
        if result['EIP']==RETORNO:assert result['ESP']==0x2008004
        return result,list(self.layers),self.ler(SUPERFICIE,128*128) if pixels else b''


def validate():
    exigir_area_editavel();start=time.monotonic();b=BancadaAtaque();catalog=Catalogo()
    templates={kind:b.inicializar_tipo(kind) for kind in (0,2)}
    base,image=imagem_pe();regions=[]
    for name,first,last in [('type0_branch',0x413a04,0x413a58),('type2_branch',0x413bc7,0x413c14),
            ('body_join',0x413971,0x413a04),('attack_dispatch',0x4136e4,0x41374c),
            ('prefix',0x41374c,0x4137db),('tail',0x414320,0x414495),('caller',0x41591f,0x415a57)]:
        data=image[first-base:last-base];regions.append(dict(name=name,start=hex(first),end=hex(last),bytes_hex=data.hex(),sha256=sha(data)))
    evidence=dict(exe_sha256=HASH_EXE,regions=regions,predecessor_sources={name:sha((RAIZ/name).read_bytes()) for name in ('graficos.py','composicao.py','unidade_tipo2.py')})
    (RAIZ/'evidencias/ataque-grafico.json').write_text(json.dumps(evidence,indent=2)+'\n')
    report=dict(exe_sha256=HASH_EXE,unicorn_version=unicorn.__version__,initial_records={kind:raw.hex() for kind,raw in templates.items()},
        input_vector=['type','state','aux_8a','direction','phase','attack_count','dx_i8','dy_i8','x_i16','y_i16','pool_index','selection_bd','camera','selected_index','mode'],
        capture_row=['input_vector','stop','native_layers','public_supported'],captures=[],pixels=[],
        substitutions=dict(captures=['copy/shadow blitters intercepted'],pixels=[],bank_loading=['file IO/allocation']),
        limits=dict(instructions_per_call=300000,timeout_us=2000000))
    fixtures=[];seen=set()
    def add(v):
        if tuple(v) not in seen:seen.add(tuple(v));fixtures.append(v)
    for kind in (0,2):
        count=templates[kind][0xa6]
        for direction in range(1,17):
            for phase in range(256):add(fixture(kind=kind,direction=direction,phase=phase,count=count))
        for state in (1,22,24):
            for aux in range(256):add(fixture(kind=kind,state=state,aux=aux,count=count))
        for count in range(256):
            for direction in (0,1,2,15,16,255):
                for phase in (0,255):add(fixture(kind=kind,count=count,direction=direction,phase=phase,index=799))
        for direction in range(256):
            for count in (0,1,8,255):add(fixture(kind=kind,state=24,aux=3,count=count,direction=direction,phase=7,index=799))
        for x,y in ((-32768,-32768),(32767,32767),(0,0),(127,127)):
            for dx,dy in ((-128,-128),(127,127),(-1,1),(0,0)):add(fixture(kind=kind,dx=dx,dy=dy,x=x,y=y,index=799))
        for selected,camera,hover,mode in ((1,0,65535,0),(255,1,65535,0),(0,0,0,0),(0,0,65535,1),(0,0,65535,255)):
            add(fixture(kind=kind,selected=selected,camera=camera,hover=hover,mode=mode))
    for v in fixtures:
        raw=runtime_record(templates[v[0]],v);native,layers,_=b.draw_attack(raw,v)
        try:plan=consultar_ataque_grafico(raw,x=v[8],y=v[9],**selection(v))
        except NotImplementedError:
            supported=False
            if native['EIP']==RETORNO and layers:assert any(not 1<=l[0]<=sum(QUANTIDADES) for l in layers)
        else:
            supported=True;assert native['EIP']==RETORNO and observed(plan)==layers,(v,layers,observed(plan))
        report['captures'].append([v,hex(native['EIP']),layers,supported])
    print('Original attack display captures:',len(fixtures),flush=True)
    b.carregar_banco_original({name:catalog._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM})
    shadow=bytes.fromhex(json.loads((RAIZ/'validacao/x86-unidade-tipo2.json').read_text())['shadow_table_hex']);report['shadow_table_hex']=shadow.hex()
    pixel_cases=[]
    for kind in (0,2):
        count=templates[kind][0xa6]
        for state in (1,22,24):
            for direction in range(1,17):
                for phase in range(count):pixel_cases.append((fixture(kind=kind,state=state,direction=direction,phase=phase,count=count),[0,0,127,127]))
        for dx,dy,x,y,clip in [(-128,-128,64,48,[0,0,127,127]),(127,127,64,48,[0,0,127,127]),
                (-5,-6,20,20,[5,6,17,18]),(0,0,64,48,[40,40,40,40]),(0,0,64,48,[100,100,127,127]),
                (127,127,32767,32767,[0,0,127,127]),(-128,-128,-32768,-32768,[0,0,127,127])]:
            pixel_cases.append((fixture(kind=kind,direction=16,phase=count-1,count=count,dx=dx,dy=dy,x=x,y=y,index=799),clip))
    contact=bytearray(1024*256)
    for v,clip in pixel_cases:
        raw=runtime_record(templates[v[0]],v);native,layers,pixels=b.draw_attack(raw,v,pixels=True,shadow=shadow,clip=clip)
        background=bytes((i*17+23)%256 for i in range(128*128))
        out,plan=compor_ataque_grafico(catalog,background,128,128,raw,x=v[8],y=v[9],tabela_sombra=shadow,recorte=clip,**selection(v))
        assert native['EIP']==RETORNO and out==pixels and observed(plan)==layers,(v,clip)
        report['pixels'].append(dict(input=v,clip=clip,sha256=sha(pixels)))
        if v[1]==1 and v[3]%2 and v[4]==0 and v[6:10]==[0,0,64,48]:
            cx=v[3]//2*128;cy=(v[0]==2)*128
            for row in range(128):contact[(cy+row)*1024+cx:(cy+row)*1024+cx+128]=pixels[row*128:row*128+128]
    palette=catalog.paleta();rgba=bytes(c for index in contact for c in (*palette[index*3:index*3+3],255))
    (RAIZ/'artefatos/ataque-tipos0-2.png').write_bytes(png(1024,256,rgba))
    report.update(result='PASS',bounded_executions=b.execucoes,instructions=b.instrucoes,
        supported_capture_returns=sum(row[3] for row in report['captures']),
        normal_handler_stops=sum(row[1]=='0x412390' for row in report['captures']),
        selection_prefix_stops=sum(row[1]=='0x4137db' for row in report['captures']),
        selection_info_stops=sum(row[1]=='0x410be4' for row in report['captures']),
        no_draw_route_returns=sum(row[1]==hex(RETORNO) and not row[2] for row in report['captures']),
        raw_catalog_rejections=sum(row[1]==hex(RETORNO) and bool(row[2]) and not row[3] for row in report['captures']),
        expected_exceptions=0,expected_limits=0,skips=0,seconds=round(time.monotonic()-start,3))
    parts=[]
    for key,value in report.items():
        encoded=('[\n'+',\n'.join('    '+json.dumps(v,separators=(',',':')) for v in value)+'\n  ]' if key=='captures' else json.dumps(value,indent=2))
        parts.append('  '+json.dumps(key)+': '+encoded)
    (RAIZ/'validacao/x86-ataque-grafico.json').write_text('{\n'+',\n'.join(parts)+'\n}\n')
    print('PASS:',len(report['pixels']),'indexed buffers;',b.execucoes,'native calls',flush=True)


if __name__=='__main__':validate()
