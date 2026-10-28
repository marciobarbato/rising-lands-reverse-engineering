"""Original prepared mechanic/builder construction calls and indexed pixels."""
import hashlib
import json
import struct
import time
from bancada_x86 import UNIDADE, SUPERFICIE, RETORNO, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, ORDEM, png
from validar_unidade_tipo2 import BancadaTipo2, observed
from construcao_grafica import consultar_construcao_grafica, compor_construcao_grafica


def sha(data):return hashlib.sha256(data).hexdigest()


def fixture(kind=7,state=11,task=0,bag=0,direction=1,phase=0,dx=0,dy=0,x=64,y=48,index=0,selected=0,hover=65535,mode=0,camera=0):
    return [kind,state,task,bag,direction,phase,dx,dy,x,y,index,selected,hover,mode,camera]


def selection(v):return dict(indice_u16=v[10],indice_selecionado_u16=v[12],modo_selecao_u8=v[13])


def runtime_record(template,v):
    raw=bytearray(template);raw[0]=0;raw[1]=v[0];raw[2]=v[1];raw[0x89]=v[2]
    struct.pack_into('<H',raw,0xa,v[3]);raw[0x91]=v[4];raw[0xa4]=v[5]
    raw[0x86]=v[6]&255;raw[0x87]=v[7]&255;raw[0xbd]=v[11];raw[0xdc]=raw[0xba]=0
    struct.pack_into('<H',raw,0x74,100);return bytes(raw)


class BancadaConstrucao(BancadaTipo2):
    def draw_construction(self,raw,v,*,pixels=False,shadow=None,clip=(0,0,127,127)):
        index=v[10];pool=bytearray(800*276);pool[index*276:index*276+276]=raw;self.escrever(UNIDADE,pool)
        self.escrever(0x508041,bytes([v[14]]));self.escrever(0x496ac2,struct.pack('<H',v[12]));self.escrever(0x508f8f,bytes([v[13]]))
        intervals=[(0x41591f,0x415a57),(0x414495,0x414a8a),(0x410fcc,0x41209d),
            (0x442025,0x442065),(0x44fffe,0x45007a),(0x467d97,0x467da6),(0x4470b9,0x4470c5)]
        stubs={a:lambda b:b.retornar_stub() for a in (0x45b247,0x45b796)}
        if pixels:
            background=bytes((i*17+23)%256 for i in range(128*128));self.preparar_superficie(128,128,background,clip,shadow)
            intervals += [(0x45b247,0x45b4fd)]+self.intervalos_sombra();stubs={}
        self.layers=[]
        result=self.executar(0x41591f,intervals,dict(EAX=v[8],EDX=v[9],EBX=index),
            stubs=stubs,paradas=[0x41451d,0x410be4],limite=300000)
        assert self.ler(UNIDADE,len(pool))==bytes(pool)
        assert self.ler(0x508041,1)==bytes([v[14]]) and self.ler(0x496ac2,2)==struct.pack('<H',v[12]) and self.ler(0x508f8f,1)==bytes([v[13]])
        if result['EIP']==RETORNO:assert result['ESP']==0x2008004
        return result,list(self.layers),self.ler(SUPERFICIE,128*128) if pixels else b''


def validate():
    exigir_area_editavel();start=time.monotonic();b=BancadaConstrucao();catalog=Catalogo()
    templates={kind:b.inicializar_tipo(kind) for kind in (6,7)};base,image=imagem_pe();regions=[]
    for name,first,last in [('construction_handler',0x414495,0x414a8a),('bag_query',0x4470b9,0x4470c5),('caller',0x41591f,0x415a57)]:
        data=image[first-base:last-base];regions.append(dict(name=name,start=hex(first),end=hex(last),bytes_hex=data.hex(),sha256=sha(data)))
    evidence=dict(exe_sha256=HASH_EXE,regions=regions,predecessor_sources={name:sha((RAIZ/name).read_bytes()) for name in ('graficos.py','composicao.py','unidade_tipo2.py','ataque_grafico.py','morte_grafica.py')})
    (RAIZ/'evidencias/construcao-grafica.json').write_text(json.dumps(evidence,indent=2)+'\n')
    report=dict(exe_sha256=HASH_EXE,unicorn_version=unicorn.__version__,initial_records={kind:raw.hex() for kind,raw in templates.items()},
        input_vector=['type','state','task89','bag_u16','direction','phase','dx_i8','dy_i8','x_i16','y_i16','pool_index','selection_bd','selected_index','mode','camera'],
        capture_row=['input_vector','stop','native_layers','public_supported'],captures=[],pixels=[],
        substitutions=dict(captures=['copy/shadow blitters intercepted'],pixels=[],bank_loading=['file IO/allocation']),
        limits=dict(instructions_per_call=300000,timeout_us=2000000))
    fixtures=[];seen=set()
    def add(v):
        if tuple(v) not in seen:seen.add(tuple(v));fixtures.append(v)
    for kind in (6,7):
        for task,bag in ((0,0),(0,1),(1,0)):
            for direction in range(1,17):
                for phase in range(256):add(fixture(kind=kind,task=task,bag=bag,direction=direction,phase=phase))
            for direction in range(256):
                for phase in (0,255):add(fixture(kind=kind,state=15,task=task,bag=bag,direction=direction,phase=phase,index=799))
        for task in range(256):
            for state in (11,15):add(fixture(kind=kind,state=state,task=task))
        for bag in (0,1,255,256,32767,32768,65535):
            for task in (0,1):add(fixture(kind=kind,bag=bag,task=task,index=799))
        for selected in range(256):
            for camera in (0,1):add(fixture(kind=kind,selected=selected,camera=camera))
        for mode in range(256):add(fixture(kind=kind,mode=mode))
        for camera in range(256):add(fixture(kind=kind,camera=camera))
        for index in (0,799):
            for hover in (0,799,800,65535):add(fixture(kind=kind,index=index,hover=hover))
        for x,y in ((-32768,-32768),(32767,32767),(0,0),(127,127)):
            for dx,dy in ((-128,-128),(127,127),(-1,1),(0,0)):add(fixture(kind=kind,task=1,dx=dx,dy=dy,x=x,y=y,index=799))
    for v in fixtures:
        raw=runtime_record(templates[v[0]],v);native,layers,_=b.draw_construction(raw,v)
        try:plan=consultar_construcao_grafica(raw,x=v[8],y=v[9],**selection(v))
        except NotImplementedError:supported=False;assert native['EIP'] in (0x41451d,0x410be4)
        else:supported=True;assert native['EIP']==RETORNO and observed(plan)==layers,(v,layers,observed(plan))
        report['captures'].append([v,hex(native['EIP']),layers,supported])
    print('Original construction captures:',len(fixtures),flush=True)
    b.carregar_banco_original({name:catalog._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM})
    shadow=bytes.fromhex(json.loads((RAIZ/'validacao/x86-unidade-tipo2.json').read_text())['shadow_table_hex']);report['shadow_table_hex']=shadow.hex()
    pixel_cases=[]
    for kind in (6,7):
        for state in (11,15):
            for task,bag in ((0,0),(0,1),(1,0)):
                for direction in range(1,17):
                    for phase in range(8):pixel_cases.append((fixture(kind=kind,state=state,task=task,bag=bag,direction=direction,phase=phase),[0,0,127,127]))
        for task in (2,255):pixel_cases.append((fixture(kind=kind,task=task),[0,0,127,127]))
        for dx,dy,x,y,clip in [(-128,-128,64,48,[0,0,127,127]),(127,127,64,48,[0,0,127,127]),
                (-5,-6,20,20,[5,6,17,18]),(0,0,64,48,[40,40,40,40]),(0,0,64,48,[100,100,127,127]),
                (127,127,32767,32767,[0,0,127,127]),(-128,-128,-32768,-32768,[0,0,127,127])]:
            pixel_cases.append((fixture(kind=kind,task=1,direction=16,phase=7,dx=dx,dy=dy,x=x,y=y,index=799),clip))
    contact=bytearray(1024*768)
    for v,clip in pixel_cases:
        raw=runtime_record(templates[v[0]],v);native,layers,pixels=b.draw_construction(raw,v,pixels=True,shadow=shadow,clip=clip)
        background=bytes((i*17+23)%256 for i in range(128*128))
        out,plan=compor_construcao_grafica(catalog,background,128,128,raw,x=v[8],y=v[9],tabela_sombra=shadow,recorte=clip,**selection(v))
        assert native['EIP']==RETORNO and out==pixels and observed(plan)==layers,(v,clip)
        report['pixels'].append(dict(input=v,clip=clip,sha256=sha(pixels)))
        if v[1]==11 and v[2] in (0,1) and v[4]%2 and v[5]==0 and v[6:10]==[0,0,64,48]:
            row=(0 if v[0]==6 else 3)+(2 if v[2]==1 else v[3]);cx=v[4]//2*128;cy=row*128
            for yy in range(128):contact[(cy+yy)*1024+cx:(cy+yy)*1024+cx+128]=pixels[yy*128:yy*128+128]
    palette=catalog.paleta();rgba=bytes(c for index in contact for c in (*palette[index*3:index*3+3],255))
    (RAIZ/'artefatos/construcao-tipos6-7.png').write_bytes(png(1024,768,rgba))
    report.update(result='PASS',bounded_executions=b.execucoes,instructions=b.instrucoes,
        complete_capture_returns=sum(row[1]==hex(RETORNO) for row in report['captures']),
        empty_body_returns=sum(row[1]==hex(RETORNO) and not row[2] for row in report['captures']),
        selection_prefix_stops=sum(row[1]=='0x41451d' for row in report['captures']),selection_info_stops=sum(row[1]=='0x410be4' for row in report['captures']),
        expected_exceptions=0,expected_limits=0,skips=0,seconds=round(time.monotonic()-start,3))
    parts=[]
    for key,value in report.items():
        encoded=('[\n'+',\n'.join('    '+json.dumps(v,separators=(',',':')) for v in value)+'\n  ]' if key=='captures' else json.dumps(value,indent=2))
        parts.append('  '+json.dumps(key)+': '+encoded)
    (RAIZ/'validacao/x86-construcao-grafica.json').write_text('{\n'+',\n'.join(parts)+'\n}\n')
    print('PASS:',len(report['pixels']),'indexed buffers;',b.execucoes,'native calls',flush=True)


if __name__=='__main__':validate()
