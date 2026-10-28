"""Original AffProjectile dispatch/copy/shadow/Eclair and public scene adapter."""
import hashlib
import json
import struct
import time
from bancada_x86 import SUPERFICIE, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, ORDEM, QUANTIDADES, png
from composicao import compor_unidade
from objetos import consultar_objeto, compor_passe
from portoes_completos import consultar_portao_completo, compor_portao_completo
from passe_sprites import planejar_passe_sprites, executar_passe_sprites
from projeteis_graficos import consultar_projetil_grafico, compor_projetil
from validar_passe_sprites import BancadaPasse, buffers as scene_buffers


def sha(data):return hashlib.sha256(data).hexdigest()


# [type, phase, direction, displacement, pixel_x, pixel_y, origin_x, origin_y,
#  activity, illumination, native pool index]. Captured vectors are raw inputs.
def fixture(kind=1,phase=0,direction=1,displacement=12800,px=704,py=704,
            ox=20,oy=20,active=1,light=0,index=0):
    return [kind,phase,direction,displacement,px,py,ox,oy,active,light,index]


def runtime_record(values):
    kind,phase,direction,displacement,px,py,_,_,active,_,_=values
    raw=bytearray((index*37+19)%256 for index in range(56))
    raw[0]=kind;raw[2]=active;raw[0x18]=phase;raw[0x22]=direction
    struct.pack_into('<HH',raw,0xc,px,py);struct.pack_into('<I',raw,0x24,displacement)
    return bytes(raw)


def observed(plan):
    return [[layer['id_motor'],layer['x'],layer['y'],layer['operacao']] for layer in plan['camadas']]


class BancadaRenderProjeteis(BancadaPasse):
    def __init__(self):
        self.record_blits=False;self.blits=[];self.previous_light=None
        super().__init__();self.escrever(self.light,bytes(65536))

    def _hook(self,cpu,address,size,data):
        operations={0x45b247:'copiar',0x45b796:'sombra',0x45ba23:'eclairage'}
        if self.record_blits and address in operations:
            assert self.reg('ECX')&255==1
            self.blits.append([self.reg('EBX')&65535,(self.reg('EAX')+32768)%65536-32768,
                (self.reg('EDX')+32768)%65536-32768,operations[address]])
        if self.trace and address==0x45ba23:
            self.layers.append(dict(event=self.current,id_motor=self.reg('EBX')&65535,
                x=(self.reg('EAX')+32768)%65536-32768,y=(self.reg('EDX')+32768)%65536-32768,
                operation='eclairage'))
        super()._hook(cpu,address,size,data)

    def executar(self,entrada,intervalos,*args,**kwargs):
        # Complete native scene runs may now reach Eclair handlers. No original
        # instruction, callback or predecessor source is patched or replaced.
        if entrada==0x416864:
            intervalos=list(intervalos)+[(0x45ba23,0x45bcb0),(0x45f7d8,0x45f7f6),(0x45f6de,0x45f6e1)]
        return super().executar(entrada,intervalos,*args,**kwargs)

    def draw(self,values,*,pixels=False,clip=(0,0,127,127),shadow=None,lighting=None):
        raw=runtime_record(values);px,py=values[4:6];ox,oy=values[6:8];flag,index=values[9:11]
        pool=bytearray(5600);pool[index*56:index*56+56]=raw;self.escrever(self.pool,pool)
        if self.previous_light is not None:self.escrever(self.light+self.previous_light,b'\0')
        key=((py//32)*256+px//32)&65535;self.escrever(self.light+key,bytes([flag]));self.previous_light=key
        self.escrever(0x508720,struct.pack('<HH',ox,oy))
        intervals=[(0x46ff70,0x4704d9),(0x46fc08,0x46fc0f),(0x476951,0x476968),(0x476702,0x47670a)]
        stubs={address:lambda b:b.retornar_stub() for address in (0x45b247,0x45b796,0x45ba23)}
        background=bytes((i*17+23)%256 for i in range(128*128))
        if pixels:
            self.preparar_superficie(128,128,background,clip,shadow)
            self.escrever(0x4e24b8,struct.pack('<I',self.lighting_pointer))
            intervals += [(0x45b247,0x45b4fd),(0x45ba23,0x45bcb0),(0x45f7d8,0x45f7f6)]+self.intervalos_sombra()
            stubs={}
        self.blits=[];self.record_blits=True
        result=self.executar(0x46ff70,intervals,dict(EAX=index),stubs=stubs,limite=1000000)
        self.record_blits=False
        assert result['EIP']==0x3000000 and result['ESP']==0x2008004
        assert self.ler(self.pool,5600)==bytes(pool) and self.ler(self.light+key,1)==bytes([flag])
        return list(self.blits),self.ler(SUPERFICIE,128*128) if pixels else b''


def compose_public_scene(catalog,case,shadow,lighting):
    units,projectiles,objects,discovery,light=scene_buffers(case)
    plan=planejar_passe_sprites(units,projectiles,objects,discovery,light,origem=case['origin'],janela_celulas=case['window'])
    w,h=(v*32 for v in case['window']);out=bytes((i*17+23)%256 for i in range(w*h));clip=(0,0,w-1,h-1)
    auxiliaries=dict(case['auxiliaries'])
    def vegetation(x,y,cell):
        nonlocal out
        if objects[cell]==253:return
        p=consultar_objeto(objects[cell],auxiliar_u8=auxiliaries.get(cell,0),descoberta_u8=discovery[cell],iluminacao_u8=light[cell])
        out=compor_passe(catalog,out,w,h,p,'sprites',x,y,tabela_sombra=shadow,recorte=clip)
    def building(x,y,cell):
        nonlocal out
        gate=case['gate']
        if not gate or cell!=gate['cell']:return
        p=consultar_portao_completo(contador_u8=gate['counter'],orientacao_u16=gate['orientation'],valor_0a_u16=35,
            jogador=0,camera=0,modo_u8=5,visibilidade_u8=0,descoberta_u8=discovery[cell],x=x,y=y,
            janela_celulas=case['window'],terreno_u16=0,recorte_entrada=clip)
        out,_=compor_portao_completo(catalog,out,w,h,p)
    def unit(x,y,index):
        nonlocal out
        offset=index*276
        out,_=compor_unidade(catalog,out,w,h,tipo=units[offset+1],estado_u8=2,direcao=units[offset+0x91],
            fase=units[offset+0xa4],x=x,y=y,tabela=shadow,bolsa_u16=0,recorte=clip)
    def projectile(index):
        nonlocal out
        raw=projectiles[index*56:index*56+56];px,py=struct.unpack_from('<HH',raw,0xc)
        key=((py//32)*256+px//32)&65535
        out,_=compor_projetil(catalog,out,w,h,raw,origem=case['origin'],iluminacao_u8=light[key],
            tabela_sombra=shadow,tabela_eclairage=lighting,recorte=clip)
    executar_passe_sprites(plan,vegetacao=vegetation,construcao=building,unidade=unit,projetil=projectile)
    return out


def write_report(path,report):
    # One compact row per native capture keeps exhaustive byte matrices legible.
    parts=[]
    for name,value in report.items():
        encoded=('[\n'+',\n'.join('    '+json.dumps(row,separators=(',',':')) for row in value)+'\n  ]'
            if name=='captures' else json.dumps(value,indent=2))
        parts.append('  '+json.dumps(name)+': '+encoded)
    path.write_text('{\n'+',\n'.join(parts)+'\n}\n')


def validate():
    exigir_area_editavel();start=time.monotonic();b=BancadaRenderProjeteis();catalog=Catalogo()
    base,image=imagem_pe();regions=[]
    for name,first,last in [('AffProjectile',0x46ff70,0x4704d9),('dispatch_table',0x46fee8,0x46ff70),
            ('shared_epilogue',0x46fc08,0x46fc0f),('illumination',0x476951,0x476968)]:
        data=image[first-base:last-base]
        regions.append(dict(name=name,start=hex(first),end=hex(last),bytes_hex=data.hex(),sha256=sha(data)))
    (RAIZ/'evidencias/projeteis-graficos.json').write_text(json.dumps(dict(exe_sha256=HASH_EXE,regions=regions,
        predecessor_sources={name:sha((RAIZ/name).read_bytes()) for name in ('eclairage.py','passe_sprites.py','ordem_projeteis.py')}),indent=2)+'\n')
    report=dict(exe_sha256=HASH_EXE,unicorn_version=unicorn.__version__,
        limits=dict(instructions_per_execution=1000000,timeout_us=2000000),
        substitutions=dict(captures=['three blitters intercepted'],pixels=[],scenes=[],bank_loading=['file IO and allocation']),
        input_vector=['type','phase','direction','displacement_u32','pixel_x_u16','pixel_y_u16','origin_x_u16','origin_y_u16','activity','illumination','pool_index'],
        capture_row=['input_vector','native_layers[id,x_i16,y_i16,operation]','public_supported'],
        captures=[],pixels=[],scenes=[],unsupported=['raw states selecting IDs outside the catalog','physical projectile updates','full AffGame/real mission'])
    fixtures=[];seen=set()
    def add(values):
        key=tuple(values)
        if key not in seen:seen.add(key);fixtures.append(values)
    for kind in range(256):add(fixture(kind=kind))
    for kind in range(1,35):
        for phase in range(256):add(fixture(kind=kind,phase=phase))
    for kind in (24,25,27):
        for direction in range(256):
            for phase in (0,255):add(fixture(kind=kind,phase=phase,direction=direction,index=99))
    for kind in (2,3,4,5,9,10,11,12,13):
        for displacement in (0,1,255,256,12800,0x7fffffff,0xffffffff):
            for px,py in ((0,0),(65535,65535),(704,704),(31,32)):
                for ox,oy in ((0,0),(20,20),(65535,65535)):
                    add(fixture(kind=kind,displacement=displacement,px=px,py=py,ox=ox,oy=oy,index=99))
    for value in range(256):add(fixture(active=value));add(fixture(light=value))
    for values in fixtures:
        native,_=b.draw(values);raw=runtime_record(values)
        try:plan=consultar_projetil_grafico(raw,origem=values[6:8],iluminacao_u8=values[9])
        except NotImplementedError:
            assert any(not 1<=layer[0]<=sum(QUANTIDADES) for layer in native)
            report['captures'].append([values,native,False])
        else:
            assert native==observed(plan),(values,native,observed(plan))
            report['captures'].append([values,native,True])
    print('Original projectile dispatch captures:',len(fixtures),flush=True)
    b.carregar_banco_original({name:catalog._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM})
    shadow=bytes(json.loads((RAIZ/'validacao/x86-composicao.json').read_text())['tabelas_sombra'][1]['indices'])
    lighting=bytes.fromhex(json.loads((RAIZ/'validacao/x86-eclairage.json').read_text())['tables'][1]['table_hex'])
    b.lighting_pointer=b.alocar(256);b.escrever(b.lighting_pointer,lighting)
    report['shadow_table_hex']=shadow.hex();report['lighting_table_hex']=lighting.hex()
    pixel_fixtures=[]
    for kind in range(1,35):
        for phase in (0,1,3,7,12,19,31,63,255):
            for direction in ((0,1,16) if kind in (24,25,27) else (1,)):
                pixel_fixtures.append((fixture(kind=kind,phase=phase,direction=direction),[0,0,127,127]))
    for kind in (1,9,24,25,27,29,30,31,32,34):
        for px,py,clip in [(640,640,[0,0,127,127]),(65535,65535,[0,0,127,127]),
                (704,704,[50,55,70,80]),(704,704,[64,64,64,64]),(704,704,[100,100,127,127])]:
            pixel_fixtures.append((fixture(kind=kind,phase=3,direction=16,px=px,py=py),clip))
    contact=bytearray(1024*512);contact_count=0
    for values,clip in pixel_fixtures:
        native,pixels=b.draw(values,pixels=True,clip=clip,shadow=shadow,lighting=lighting)
        background=bytes((i*17+23)%256 for i in range(128*128))
        out,plan=compor_projetil(catalog,background,128,128,runtime_record(values),origem=values[6:8],iluminacao_u8=values[9],
            tabela_sombra=shadow,tabela_eclairage=lighting,recorte=clip)
        assert pixels==out and native==observed(plan),(values,clip)
        report['pixels'].append(dict(input=values,clip=clip,sha256=sha(pixels)))
        if values[1]==0 and values[2]==1 and values[0] not in (28,33):
            cx,cy=(contact_count%8)*128,(contact_count//8)*128
            for row in range(128):contact[(cy+row)*1024+cx:(cy+row)*1024+cx+128]=pixels[row*128:row*128+128]
            contact_count+=1
    scene_types=[(1,9),(24,25),(27,29),(30,31),(32,34),(2,3),(6,8),(20,23)]
    old_scenes=json.loads((RAIZ/'validacao/x86-passe-sprites.json').read_text())['pixels']
    for phase,old in enumerate(old_scenes):
        case=json.loads(json.dumps(old['case']));case['name']='public_projectile_scene_'+str(phase)
        for projectile,kind in zip(case['projectiles'],scene_types[phase]):projectile['type']=kind
        b.escrever(0x4e24b8,struct.pack('<I',b.lighting_pointer))
        capture,pixels=b.scene(case,pixels=True,shadow_table=shadow)
        assert pixels==compose_public_scene(catalog,case,shadow,lighting)
        report['scenes'].append(dict(case=case,sha256=sha(pixels),stop=capture['stop'],inputs_preserved=capture['inputs_preserved']))
    palette=catalog.paleta();rgba=bytes(component for index in contact for component in (*palette[index*3:index*3+3],255))
    (RAIZ/'artefatos/projeteis-contato.png').write_bytes(png(1024,512,rgba))
    report.update(result='PASS',bounded_executions=b.execucoes,instructions=b.instrucoes,
        unsupported_raw_captures=sum(not row[2] for row in report['captures']),expected_exceptions=0,expected_limits=0,skips=0,
        seconds=round(time.monotonic()-start,3))
    write_report(RAIZ/'validacao/x86-projeteis-graficos.json',report)
    print('PASS:',len(report['pixels']),'indexed buffers;',len(report['scenes']),'public-composed scenes;',b.execucoes,'native calls',flush=True)


if __name__=='__main__':validate()
