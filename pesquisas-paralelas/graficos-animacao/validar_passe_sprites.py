"""Complete native AffSprite traces and a bounded native indexed sprite scene."""
import hashlib
import json
import random
import struct
import time
from bancada_x86 import UNIDADE, SUPERFICIE, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, ORDEM, TIPOS, png
from validar_ordem_projeteis import BancadaProjeteis
from passe_sprites import planejar_passe_sprites
from objetos import consultar_objeto, compor_passe
from composicao import compor_unidade
from portoes_completos import consultar_portao_completo, compor_portao_completo


def sha(data):return hashlib.sha256(data).hexdigest()


def buffers(case):
    units=bytearray(800*276);projectiles=bytearray(5600);objects=bytearray(65536)
    discovery=bytearray(65536);light=bytearray(65536)
    for item in case['units']:
        offset=item['index']*276
        if 'raw_hex' in item:units[offset:offset+276]=bytes.fromhex(item['raw_hex'])
        else:
            units[offset+2]=item['state'];units[offset+0xab]=item['priority']
            struct.pack_into('<H',units,offset+8,item['cell'])
    for item in case['projectiles']:
        offset=item['index']*56;projectiles[offset]=item.get('type',0);projectiles[offset+2]=item['active']
        struct.pack_into('<HH',projectiles,offset+0xc,item['x'],item['y']);projectiles[offset+0x18]=item.get('phase',0)
    for cell,value in case['objects']:objects[cell]=value
    for cell,value in case['discovery']:discovery[cell]=value
    for cell,value in case['light']:light[cell]=value
    return bytes(units),bytes(projectiles),bytes(objects),bytes(discovery),bytes(light)


def fixture(name,**changes):
    case=dict(name=name,origin=[20,20],window=[4,4],units=[],projectiles=[],objects=[],discovery=[],light=[],auxiliaries=[],gate=None)
    case.update(changes);return case


class BancadaPasse(BancadaProjeteis):
    def __init__(self):
        self.trace=False;self.calls=[];self.layers=[];self.phase=1;self.current=-1
        super().__init__();self.world={}
        for name,address,size in [('objects',0x507d74,65536),('terrain',0x507d70,131072),
                ('occupancy',0x4e0f38,131072),('auxiliaries',0x507dac,65536),('attributes',0x507da8,65536)]:
            ptr=self.alocar(size);self.world[name]=ptr;self.escrever(address,struct.pack('<I',ptr))

    def _hook(self,cpu,address,size,data):
        if self.trace:
            if address==0x416c64:self.phase=2
            names={0x415acf:'AffVeget',0x407dd3:'AffBatiments',0x40f49b:'AffBatimentOmbre',
                0x41591f:'AffEngin',0x46ff70:'AffProjectile'}
            if address in names:
                name=names[address]
                direct=address!=0x40f49b or struct.unpack('<I',self.ler(self.reg('ESP'),4))[0]==0x416bd7
                if direct:
                    event=dict(funcao=name,passe=self.phase)
                    if name=='AffProjectile':event['indice']=self.reg('EAX')&65535
                    else:
                        event.update(x=(self.reg('EAX')+32768)%65536-32768,y=(self.reg('EDX')+32768)%65536-32768)
                        event['indice' if name=='AffEngin' else 'celula']=self.reg('EBX')&65535
                    self.calls.append(event);self.current=len(self.calls)-1
            if address in (0x45b247,0x45b796):
                self.layers.append(dict(event=self.current,id_motor=self.reg('EBX')&65535,
                    x=(self.reg('EAX')+32768)%65536-32768,y=(self.reg('EDX')+32768)%65536-32768,
                    operation='copy' if address==0x45b247 else 'shadow'))
        super()._hook(cpu,address,size,data)

    def scene(self,case,*,pixels=False,shadow_table=None):
        inputs=buffers(case);units,projectiles,objects,discovery,light=inputs
        self.escrever(UNIDADE,units);self.escrever(self.pool,projectiles)
        self.escrever(self.world['objects'],objects);self.escrever(self.discovery,discovery);self.escrever(self.light,light)
        for name,size in [('terrain',131072),('occupancy',131072),('auxiliaries',65536),('attributes',65536)]:
            self.escrever(self.world[name],bytes(size))
        for cell,value in case['auxiliaries']:self.escrever(self.world['auxiliaries']+cell,bytes([value]))
        raw=bytearray(276)
        if case['gate']:
            gate=case['gate'];raw[8]=12;raw[5]=5
            raw[0x76]=gate['counter'];struct.pack_into('<H',raw,0x7c,gate['orientation']);struct.pack_into('<H',raw,0xa,35)
            struct.pack_into('<H',raw,2,gate['cell'])
            self.escrever(self.world['occupancy']+gate['cell']*2,struct.pack('<H',0x8000))
        self.escrever(0x49a0c8,raw);self.escrever(0x495be0,b'\xff'*10);self.escrever(0x496ac4,b'\xff\xff')
        self.escrever(0x508720,struct.pack('<HH',*case['origin']));self.escrever(0x508724,struct.pack('<HH',*case['window']))
        w,h=(v*32 for v in case['window']);background=bytes((i*17+23)%256 for i in range(w*h)) if pixels else b''
        intervals=[(0x416864,0x416e41),(0x410878,0x41087e),(0x441fff,0x442025),
            (0x4766d6,0x47670a),(0x47693a,0x476968),(0x46fc8b,0x46fee5),(0x46fc08,0x46fc0f)]
        stubs={address:lambda b:b.retornar_stub() for address in (0x415acf,0x407dd3,0x40f49b,0x41591f,0x46ff70)}
        if pixels:
            self.preparar_superficie(w,h,background,(0,0,w-1,h-1),shadow_table)
            intervals += [(0x415acf,0x416864),(0x410b38,0x410b40),(0x407dd3,0x40f535),
                (0x41a6ec,0x41a70b),(0x41a08c,0x41a0ab),(0x41b54a,0x41b579),
                (0x41a8e5,0x41a940),(0x402864,0x40288b),(0x402c7a,0x402c82),
                (0x41a5b8,0x41a61c),(0x4471b8,0x44724a),(0x41a4f4,0x41a513),
                (0x41591f,0x415a57),(0x412390,0x41374c),(0x410fcc,0x41209d),
                (0x4470b9,0x4470c5),(0x442025,0x442065),(0x44fffe,0x45007a),(0x467d97,0x467da6),
                (0x46ff70,0x4704d9),(0x45b247,0x45b4fd)]+self.intervalos_sombra()
            stubs={}
        self.calls=[];self.layers=[];self.phase=1;self.current=-1;self.trace=True
        result=self.executar(0x416864,intervals,dict(EAX=case['origin'][0],EDX=case['origin'][1]),stubs=stubs,limite=1000000)
        self.trace=False
        plan=planejar_passe_sprites(*inputs,origem=case['origin'],janela_celulas=case['window'])
        assert self.calls==plan['eventos'],(case,self.calls,plan['eventos'])
        assert self.ler(UNIDADE,len(units))==units and self.ler(self.pool,5600)==projectiles
        assert self.ler(self.world['objects'],65536)==objects and self.ler(self.discovery,65536)==discovery and self.ler(self.light,65536)==light
        assert self.ler(0x49a0c8,276)==bytes(raw)
        assert result['ESP']==0x2008004
        return dict(calls=self.calls,layers=self.layers,stop=hex(result['EIP']),stack=result['ESP'],inputs_preserved=True),self.ler(SUPERFICIE,len(background)) if pixels else b''


def compose_demo(catalog,case,capture,table):
    inputs=buffers(case);units,projectiles,objects,discovery,light=inputs
    plan=planejar_passe_sprites(*inputs,origem=case['origin'],janela_celulas=case['window'])
    w,h=(v*32 for v in case['window']);out=bytes((i*17+23)%256 for i in range(w*h));clip=(0,0,w-1,h-1)
    auxiliaries=dict(case['auxiliaries'])
    projectile_layers={}
    for layer in capture['layers']:
        event=capture['calls'][layer['event']]
        if event['funcao']=='AffProjectile':projectile_layers.setdefault(event['indice'],[]).append(layer)
    from graficos import compor_indices
    for event in plan['eventos']:
        name=event['funcao']
        if name=='AffVeget' and objects[event['celula']]!=253:
            cell=event['celula'];p=consultar_objeto(objects[cell],auxiliar_u8=auxiliaries.get(cell,0),descoberta_u8=discovery[cell],iluminacao_u8=light[cell])
            out=compor_passe(catalog,out,w,h,p,'sprites',event['x'],event['y'],tabela_sombra=table,recorte=clip)
        elif name=='AffBatiments' and case['gate'] and event['celula']==case['gate']['cell']:
            gate=case['gate'];p=consultar_portao_completo(contador_u8=gate['counter'],orientacao_u16=gate['orientation'],valor_0a_u16=35,
                jogador=0,camera=0,modo_u8=5,visibilidade_u8=0,descoberta_u8=discovery[gate['cell']],
                x=event['x'],y=event['y'],janela_celulas=case['window'],terreno_u16=0,recorte_entrada=clip)
            out,_=compor_portao_completo(catalog,out,w,h,p)
        elif name=='AffEngin':
            offset=event['indice']*276
            out,_=compor_unidade(catalog,out,w,h,tipo=units[offset+1],estado_u8=2,direcao=units[offset+0x91],
                fase=units[offset+0xa4],x=event['x'],y=event['y'],tabela=table,bolsa_u16=0,recorte=clip)
        elif name=='AffProjectile':
            for layer in projectile_layers[event['indice']]:
                assert layer['operation']=='copy'
                out=compor_indices(out,w,h,catalog.quadro(layer['id_motor']),layer['x'],layer['y'],clip)
    return out


def validate():
    exigir_area_editavel();start=time.monotonic();b=BancadaPasse();c=Catalogo();rng=random.Random(0x416a6c)
    base,image=imagem_pe();raw=image[0x416864-base:0x416e41-base]
    (RAIZ/'evidencias/passe-sprites.json').write_text(json.dumps(dict(exe_sha256=HASH_EXE,start='0x416864',end='0x416e41',
        bytes_hex=raw.hex(),sha256=sha(raw),predecessor_sources={name:sha((RAIZ/name).read_bytes()) for name in (
            'ordem_unidades.py','ordem_projeteis.py','portoes_completos.py')}),indent=2)+'\n')
    cases=[fixture('empty'),fixture('priority_and_row_margins',units=[dict(index=i,cell=y*256+x,priority=p,state=2) for i,(x,y,p) in enumerate(
        ((20,20,0),(20,20,1),(20,20,255),(20,28,0),(20,29,0),(20,29,1),(25,20,0),(26,20,0)))]),
        fixture('minimum_window',window=[1,1]),fixture('maximum_interior_window',origin=[216,214],window=[32,32])]
    for code in (0,1,66,253,255):
        for flag in (0,1,15,16,31,32,255):cases.append(fixture('object_visibility',objects=[[0x1515,code]],discovery=[[0x1515,flag]]))
    for ordinal in range(16):
        cases.append(fixture('seeded_'+str(ordinal),units=[dict(index=i,cell=rng.randrange(19,35)*256+rng.randrange(19,34),
            priority=rng.choice((0,1,2,255)),state=rng.choice((0,2,4,7,255))) for i in rng.sample(range(800),24)],
            projectiles=[dict(index=i,x=rng.randrange(19*32,34*32),y=rng.randrange(19*32,35*32),active=rng.choice((0,1,2))) for i in range(8)],
            objects=[[(20+i//4)*256+20+i%4,rng.choice((0,1,12,66,253,255))] for i in range(16)]))
    report=dict(exe_sha256=HASH_EXE,unicorn_version=unicorn.__version__,limits=dict(instructions_per_call=1000000,timeout_us=2000000),
        substitutions=dict(traces=['four renderer callbacks captured; original no-op shadow captured'],pixels=[],
            sorts=[],predicates=[],bank_loading=['file IO and allocation']),cases=[],pixels=[],
        unsupported=['margin wraparound/negative origins','general renderer handlers and side effects','AffTerrain, full AffGame and real-mission consumer',
            'public projectile sprite mapping; demo replays captured type1 layers'])
    for case in cases:
        capture,_=b.scene(case);report['cases'].append(dict(case=case,**capture))
    print('Complete AffSprite callback fixtures:',len(cases),flush=True)
    b.carregar_banco_original({name:c._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM})
    table=bytes(json.loads((RAIZ/'validacao/x86-composicao.json').read_text())['tabelas_sombra'][1]['indices'])
    for phase in range(8):
        units=[]
        for index,kind in enumerate(TIPOS):
            raw=bytearray(b.inicializar_tipo(kind));raw[2]=2;raw[0xab]=index%2;raw[0x91]=1+2*index;raw[0xa4]=phase
            struct.pack_into('<H',raw,8,0x1616);struct.pack_into('<H',raw,0x74,100)
            units.append(dict(index=index,raw_hex=raw.hex()))
        case=fixture('indexed_scene_'+str(phase),units=units,objects=[[0x1615,1],[0x1516,253]],auxiliaries=[[0x1615,phase%4]],
            gate=dict(cell=0x1516,counter=phase*4,orientation=phase%2),
            projectiles=[dict(index=i,x=20*32+64+i,y=20*32+64+i,type=1,active=1,phase=(phase+i)%4) for i in range(2)])
        capture,original=b.scene(case,pixels=True,shadow_table=table)
        assert original==compose_demo(c,case,capture,table)
        report['pixels'].append(dict(case=case,**capture,sha256=sha(original)))
        if phase==0:
            palette=c.paleta();rgba=bytes(value for index in original for value in (*palette[index*3:index*3+3],255))
            (RAIZ/'artefatos/cena-passe-sprites.png').write_bytes(png(128,128,rgba))
    report.update(result='PASS',bounded_executions=b.execucoes,instructions=b.instrucoes,expected_exceptions=0,expected_limits=0,skips=0,
        seconds=round(time.monotonic()-start,3))
    (RAIZ/'validacao/x86-passe-sprites.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',len(report['pixels']),'native complete sprite-pass buffers;',b.execucoes,'bounded calls',flush=True)


if __name__=='__main__':validate()
