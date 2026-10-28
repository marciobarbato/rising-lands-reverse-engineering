"""Original six-type corpse display through complete AffEngin returns."""
import hashlib
import json
import struct
import time
from bancada_x86 import UNIDADE, SUPERFICIE, RETORNO, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, ORDEM, QUANTIDADES, png
from validar_unidade_tipo2 import BancadaTipo2, observed
from morte_grafica import consultar_morte_grafica, compor_morte_grafica


KINDS=(0,2,5,6,7,9)
def sha(data):return hashlib.sha256(data).hexdigest()


def fixture(kind=0,counter=0,direction=1,phase=0,count=8,dx=0,dy=0,x=64,y=48,index=0):
    return [kind,counter,direction,phase,count,dx,dy,x,y,index]


def runtime_record(template,v):
    raw=bytearray(template);raw[0]=0;raw[1]=v[0];raw[2]=4;raw[0xdc]=0
    struct.pack_into('<H',raw,0xc2,v[1]);raw[0x91]=v[2];raw[0xa4]=v[3];raw[0xdb]=v[4]
    raw[0x86]=v[5]&255;raw[0x87]=v[6]&255
    return bytes(raw)


class BancadaMorte(BancadaTipo2):
    def draw_death(self,raw,v,*,pixels=False,shadow=None,clip=(0,0,127,127)):
        index=v[9];pool=bytearray(800*276);pool[index*276:index*276+276]=raw;self.escrever(UNIDADE,pool)
        intervals=[(0x41591f,0x415a57),(0x415496,0x41591f),(0x410fcc,0x41209d),
            (0x442025,0x442065),(0x44fffe,0x45007a),(0x467d97,0x467da6)]
        stubs={a:lambda b:b.retornar_stub() for a in (0x45b247,0x45b796)}
        if pixels:
            background=bytes((i*17+23)%256 for i in range(128*128));self.preparar_superficie(128,128,background,clip,shadow)
            intervals += [(0x45b247,0x45b4fd)]+self.intervalos_sombra();stubs={}
        self.layers=[]
        result=self.executar(0x41591f,intervals,dict(EAX=v[7],EDX=v[8],EBX=index),stubs=stubs,limite=300000)
        assert result['EIP']==RETORNO and result['ESP']==0x2008004
        assert self.ler(UNIDADE,len(pool))==bytes(pool)
        return list(self.layers),self.ler(SUPERFICIE,128*128) if pixels else b''


def validate():
    exigir_area_editavel();start=time.monotonic();b=BancadaMorte();catalog=Catalogo()
    templates={kind:b.inicializar_tipo(kind) for kind in KINDS};base,image=imagem_pe();regions=[]
    for name,first,last in [('sprite_query',0x415496,0x41559a),('death_handler',0x41559a,0x41591f),('caller',0x41591f,0x415a57)]:
        data=image[first-base:last-base];regions.append(dict(name=name,start=hex(first),end=hex(last),bytes_hex=data.hex(),sha256=sha(data)))
    evidence=dict(exe_sha256=HASH_EXE,regions=regions,predecessor_sources={name:sha((RAIZ/name).read_bytes()) for name in ('graficos.py','composicao.py','unidade_tipo2.py','ataque_grafico.py')})
    (RAIZ/'evidencias/morte-grafica.json').write_text(json.dumps(evidence,indent=2)+'\n')
    report=dict(exe_sha256=HASH_EXE,unicorn_version=unicorn.__version__,initial_records={kind:raw.hex() for kind,raw in templates.items()},
        input_vector=['type','counter_c2_u16','direction','phase','corpse_count_db','dx_i8','dy_i8','x_i16','y_i16','pool_index'],
        capture_row=['input_vector','native_layers','public_supported'],captures=[],ignored_field_captures=[],pixels=[],
        substitutions=dict(captures=['copy/shadow blitters intercepted'],pixels=[],bank_loading=['file IO/allocation']),
        limits=dict(instructions_per_call=300000,timeout_us=2000000))
    fixtures=[];seen=set()
    def add(v):
        if tuple(v) not in seen:seen.add(tuple(v));fixtures.append(v)
    for kind in KINDS:
        count=templates[kind][0xdb]
        for counter in (*range(341),32767,32768,65535):add(fixture(kind=kind,counter=counter,count=count))
        for phase in range(256):
            for counter in (0,315,330):add(fixture(kind=kind,counter=counter,phase=phase,count=count))
        for direction in range(256):
            for phase in (0,255):
                for counter in (0,329):add(fixture(kind=kind,counter=counter,direction=direction,phase=phase,count=count,index=799))
        for count in range(256):
            for direction in (0,16,255):add(fixture(kind=kind,counter=315,count=count,direction=direction,phase=7,index=799))
        for x,y in ((-32768,-32768),(32767,32767),(0,0),(127,127)):
            for dx,dy in ((-128,-128),(127,127),(-1,1),(0,0)):add(fixture(kind=kind,counter=315,dx=dx,dy=dy,x=x,y=y,index=799))
    for v in fixtures:
        raw=runtime_record(templates[v[0]],v);native,_=b.draw_death(raw,v)
        try:plan=consultar_morte_grafica(raw,x=v[7],y=v[8])
        except NotImplementedError:
            supported=False;assert any(not 1<=l[0]<=sum(QUANTIDADES) for l in native)
        else:
            supported=True;assert observed(plan)==native,(v,native,observed(plan))
        report['captures'].append([v,native,supported])
    print('Original corpse captures:',len(fixtures),flush=True)
    # The death handler does not use normal/attack selection or fatigue guards.
    for kind in KINDS:
        for counter in (0,315):
            v=fixture(kind=kind,counter=counter,count=templates[kind][0xdb]);raw=bytearray(runtime_record(templates[kind],v))
            raw[0xbd]=raw[0xba]=raw[0x99]=raw[0xa5]=raw[0xa6]=255
            struct.pack_into('<H',raw,0x74,0);struct.pack_into('<H',raw,0xa,65535)
            b.escrever(0x508041,b'\0');b.escrever(0x496ac2,b'\0\0');b.escrever(0x508f8f,b'\xff')
            native,_=b.draw_death(raw,v)
            assert observed(consultar_morte_grafica(raw,x=64,y=48))==native
            assert b.ler(0x508041,1)==b'\0' and b.ler(0x496ac2,2)==b'\0\0' and b.ler(0x508f8f,1)==b'\xff'
            report['ignored_field_captures'].append(dict(input=v,record_hex=raw.hex(),layers=native,
                camera_u8=0,selected_index_u16=0,mode_u8=255))
    b.escrever(0x508041,b'\0');b.escrever(0x496ac2,b'\xff\xff');b.escrever(0x508f8f,b'\0')
    b.carregar_banco_original({name:catalog._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM})
    shadow=bytes.fromhex(json.loads((RAIZ/'validacao/x86-unidade-tipo2.json').read_text())['shadow_table_hex']);report['shadow_table_hex']=shadow.hex()
    pixel_cases=[];pixel_seen=set()
    def pixel_add(v,clip=(0,0,127,127)):
        key=tuple(v)+tuple(clip)
        if key not in pixel_seen:pixel_seen.add(key);pixel_cases.append((v,list(clip)))
    for kind in KINDS:
        count=templates[kind][0xdb]
        for direction in range(1,17,2):
            for phase in range(count):pixel_add(fixture(kind=kind,direction=direction,phase=phase,count=count))
            for phase in (0,count-1):
                for counter in (304,305,314,315,316,320,325,330):pixel_add(fixture(kind=kind,counter=counter,direction=direction,phase=phase,count=count))
        for dx,dy,x,y,clip in [(-128,-128,64,48,[0,0,127,127]),(127,127,64,48,[0,0,127,127]),
                (-5,-6,20,20,[5,6,17,18]),(0,0,64,48,[40,40,40,40]),(0,0,64,48,[100,100,127,127]),
                (127,127,32767,32767,[0,0,127,127]),(-128,-128,-32768,-32768,[0,0,127,127])]:
            pixel_add(fixture(kind=kind,counter=315,direction=16,phase=count-1,count=count,dx=dx,dy=dy,x=x,y=y,index=799),clip)
    contact=bytearray(1024*768);contact_counters=(0,304,305,314,315,316,325,330)
    for v,clip in pixel_cases:
        raw=runtime_record(templates[v[0]],v);native,pixels=b.draw_death(raw,v,pixels=True,shadow=shadow,clip=clip)
        background=bytes((i*17+23)%256 for i in range(128*128))
        out,plan=compor_morte_grafica(catalog,background,128,128,raw,x=v[7],y=v[8],tabela_sombra=shadow,recorte=clip)
        assert out==pixels and observed(plan)==native,(v,clip)
        report['pixels'].append(dict(input=v,clip=clip,sha256=sha(pixels)))
        if v[1] in contact_counters and v[2]==1 and v[3]==0 and v[5:9]==[0,0,64,48]:
            cx=contact_counters.index(v[1])*128;cy=KINDS.index(v[0])*128
            for row in range(128):contact[(cy+row)*1024+cx:(cy+row)*1024+cx+128]=pixels[row*128:row*128+128]
    palette=catalog.paleta();rgba=bytes(c for index in contact for c in (*palette[index*3:index*3+3],255))
    (RAIZ/'artefatos/morte-contadores.png').write_bytes(png(1024,768,rgba))
    report.update(result='PASS',bounded_executions=b.execucoes,instructions=b.instrucoes,
        raw_catalog_rejections=sum(not row[2] for row in report['captures']),expected_dependency_stops=0,
        expected_exceptions=0,expected_limits=0,skips=0,seconds=round(time.monotonic()-start,3))
    parts=[]
    for key,value in report.items():
        encoded=('[\n'+',\n'.join('    '+json.dumps(v,separators=(',',':')) for v in value)+'\n  ]' if key=='captures' else json.dumps(value,indent=2))
        parts.append('  '+json.dumps(key)+': '+encoded)
    (RAIZ/'validacao/x86-morte-grafica.json').write_text('{\n'+',\n'.join(parts)+'\n}\n')
    print('PASS:',len(report['pixels']),'indexed buffers;',b.execucoes,'native calls',flush=True)


if __name__=='__main__':validate()
