"""Independent complete original AffEngin checks for prepared type-2 bodies."""
import hashlib
import json
import struct
import time
from bancada_x86 import UNIDADE, SUPERFICIE, RETORNO, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, ORDEM, QUANTIDADES, png
from validar_composicao import BancadaComposicao
from unidade_tipo2 import consultar_corpo_tipo2, compor_corpo_tipo2


def sha(data):return hashlib.sha256(data).hexdigest()


def record(template,values):
    # [state,direction,phase,count,dx_i8,dy_i8,x_i16,y_i16,pool_index]
    state,direction,phase,count,dx,dy,_,_,_=values
    raw=bytearray(template);raw[0]=0;raw[1]=2;raw[2]=state
    raw[0x91]=direction;raw[0xa4]=phase;raw[0xa5]=count
    raw[0x86]=dx&255;raw[0x87]=dy&255
    raw[0x99]=raw[0xba]=raw[0xdc]=0;struct.pack_into('<H',raw,0x74,100)
    return bytes(raw)


def observed(plan):return [[l['id_motor'],l['x'],l['y'],l['operacao']] for l in plan['camadas']]


class BancadaTipo2(BancadaComposicao):
    def __init__(self):self.layers=[];super().__init__()

    def _hook(self,cpu,address,size,data):
        if address in (0x45b247,0x45b796):
            assert self.reg('ECX')&255==1
            self.layers.append([self.reg('EBX')&65535,(self.reg('EAX')+32768)%65536-32768,
                (self.reg('EDX')+32768)%65536-32768,'copiar' if address==0x45b247 else 'sombra'])
        super()._hook(cpu,address,size,data)

    def draw(self,raw,values,*,pixels=False,clip=(0,0,127,127),shadow=None):
        x,y,index=values[6:9];pool=bytearray(800*276);pool[index*276:index*276+276]=raw
        self.escrever(UNIDADE,pool);self.layers=[]
        intervals=[(0x41591f,0x415a57),(0x412390,0x41374c),(0x410fcc,0x41209d),
            (0x442025,0x442065),(0x44fffe,0x45007a),(0x467d97,0x467da6)]
        stubs={address:lambda b:b.retornar_stub() for address in (0x45b247,0x45b796)}
        if pixels:
            background=bytes((i*17+23)%256 for i in range(128*128))
            self.preparar_superficie(128,128,background,clip,shadow)
            intervals += [(0x45b247,0x45b4fd)]+self.intervalos_sombra();stubs={}
        result=self.executar(0x41591f,intervals,dict(EAX=x,EDX=y,EBX=index),stubs=stubs,limite=300000)
        assert result['EIP']==RETORNO and result['ESP']==0x2008004
        assert self.ler(UNIDADE,len(pool))==bytes(pool)
        return list(self.layers),self.ler(SUPERFICIE,128*128) if pixels else b''


def validate():
    exigir_area_editavel();start=time.monotonic();b=BancadaTipo2();catalog=Catalogo()
    template=b.inicializar_tipo(2)
    assert template[0xa5]==8 and template[0x99]==0
    base,image=imagem_pe();regions=[]
    for name,first,last in [('body_branch',0x412ece,0x412f1c),('body_join',0x412cb8,0x412cfe),
            ('body_dispatch_slot',0x412330,0x412334),('anchor_dispatch_slot',0x410f6c,0x410f70),
            ('anchor',0x410ff8,0x411001),('type_init',0x4576ca,0x457727),
            ('normal_caller',0x41591f,0x415a57),('type_identity',0x496612,0x496644)]:
        data=image[first-base:last-base]
        regions.append(dict(name=name,start=hex(first),end=hex(last),bytes_hex=data.hex(),sha256=sha(data)))
    evidence=dict(exe_sha256=HASH_EXE,regions=regions,
        predecessor_sources={name:sha((RAIZ/name).read_bytes()) for name in ('graficos.py','composicao.py')})
    (RAIZ/'evidencias/unidade-tipo2.json').write_text(json.dumps(evidence,indent=2)+'\n')
    report=dict(exe_sha256=HASH_EXE,unicorn_version=unicorn.__version__,initial_record_hex=template.hex(),
        limits=dict(instructions_per_execution=300000,timeout_us=2000000),
        input_vector=['state','direction','phase','count','dx_i8','dy_i8','x_i16','y_i16','pool_index'],
        capture_row=['input_vector','native_layers[id,x_i16,y_i16,operation]','public_supported'],
        substitutions=dict(captures=['copy and shadow blitters intercepted'],pixels=[],bank_loading=['file IO and allocation']),
        captures=[],guard_captures=[],pixels=[],unsupported=['other states/players/effects','physical phase production','raw out-of-catalog IDs','real mission'])
    fixtures=[];seen=set()
    def add(values):
        key=tuple(values)
        if key not in seen:seen.add(key);fixtures.append(values)
    for state in (2,7):
        for direction in range(1,17):
            for phase in range(256):add([state,direction,phase,8,0,0,64,48,0])
    for count in range(256):
        for direction in (0,1,2,15,16,255):
            for phase in (0,255):add([2,direction,phase,count,0,0,64,48,799])
    for direction in range(256):
        for count in (0,1,8,255):add([7,direction,7,count,0,0,64,48,799])
    for shift in range(-128,128):
        add([2,1,0,8,shift,127-shift if shift>=0 else -1-shift,32767,-32768,799])
    for x,y in ((-32768,-32768),(32767,32767),(-1,-1),(0,0),(127,127)):
        for dx,dy in ((-128,-128),(127,127),(-1,1),(0,0)):add([2,16,255,8,dx,dy,x,y,799])
    for values in fixtures:
        raw=record(template,values);native,_=b.draw(raw,values)
        try:plan=consultar_corpo_tipo2(raw,x=values[6],y=values[7])
        except NotImplementedError:
            assert any(not 1<=l[0]<=sum(QUANTIDADES) for l in native)
            report['captures'].append([values,native,False])
        else:
            assert native==observed(plan),(values,native,observed(plan))
            report['captures'].append([values,native,True])
    print('Original type-2 captures:',len(fixtures),flush=True)
    values=[2,1,7,8,0,0,64,48,799]
    for fatigue in (100,101,255,256,32767,32768,65535):
        for bag in (0,1,65535):
            raw=bytearray(record(template,values));struct.pack_into('<H',raw,0x74,fatigue);struct.pack_into('<H',raw,0xa,bag)
            native,_=b.draw(raw,values)
            assert observed(consultar_corpo_tipo2(raw,x=64,y=48))==native
            report['guard_captures'].append(dict(fatigue_u16=fatigue,bag_u16=bag,record_hex=raw.hex(),layers=native))
    b.carregar_banco_original({name:catalog._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM})
    shadow=bytes(json.loads((RAIZ/'validacao/x86-composicao.json').read_text())['tabelas_sombra'][1]['indices'])
    report['shadow_table_hex']=shadow.hex();contact=bytearray(1024*256)
    pixel_cases=[]
    for state in (2,7):
        for direction in range(1,17):
            for phase in range(8):pixel_cases.append(([state,direction,phase,8,0,0,64,48,0],[0,0,127,127]))
    for dx,dy,x,y,clip in [(-128,-128,64,48,[0,0,127,127]),(127,127,64,48,[0,0,127,127]),
            (-5,-6,20,20,[5,6,17,18]),(0,0,64,48,[40,40,40,40]),(0,0,64,48,[100,100,127,127]),
            (127,127,32767,32767,[0,0,127,127]),(-128,-128,-32768,-32768,[0,0,127,127])]:
        pixel_cases.append(([2,16,7,8,dx,dy,x,y,799],clip))
    for values,clip in pixel_cases:
        raw=record(template,values);native,pixels=b.draw(raw,values,pixels=True,clip=clip,shadow=shadow)
        background=bytes((i*17+23)%256 for i in range(128*128))
        out,plan=compor_corpo_tipo2(catalog,background,128,128,raw,x=values[6],y=values[7],tabela_sombra=shadow,recorte=clip)
        assert out==pixels and observed(plan)==native,(values,clip)
        report['pixels'].append(dict(input=values,clip=clip,sha256=sha(pixels)))
        if values[0]==2 and values[1]%2 and values[2] in (0,7) and values[4:8]==[0,0,64,48]:
            slot=(values[2]==7)*8+values[1]//2;cx,cy=slot%8*128,slot//8*128
            for row in range(128):contact[(cy+row)*1024+cx:(cy+row)*1024+cx+128]=pixels[row*128:row*128+128]
    palette=catalog.paleta();rgba=bytes(c for index in contact for c in (*palette[index*3:index*3+3],255))
    (RAIZ/'artefatos/unidade-tipo2-contato.png').write_bytes(png(1024,256,rgba))
    report.update(result='PASS',bounded_executions=b.execucoes,instructions=b.instrucoes,
        unsupported_raw_captures=sum(not row[2] for row in report['captures']),expected_exceptions=0,expected_limits=0,skips=0,
        seconds=round(time.monotonic()-start,3))
    # Compact each exhaustive capture on one line, preserving every observation.
    parts=[]
    for key,value in report.items():
        encoded=('[\n'+',\n'.join('    '+json.dumps(v,separators=(',',':')) for v in value)+'\n  ]'
            if key=='captures' else json.dumps(value,indent=2))
        parts.append('  '+json.dumps(key)+': '+encoded)
    (RAIZ/'validacao/x86-unidade-tipo2.json').write_text('{\n'+',\n'.join(parts)+'\n}\n')
    print('PASS:',len(report['pixels']),'indexed buffers;',b.execucoes,'native calls',flush=True)


if __name__=='__main__':validate()
