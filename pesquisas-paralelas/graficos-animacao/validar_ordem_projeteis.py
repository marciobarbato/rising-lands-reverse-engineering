"""Original projectile display-list/GetCase buffers and indexed replay demo."""
import hashlib
import json
import random
import struct
import time
from bancada_x86 import SUPERFICIE, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, ORDEM, compor_indices
from validar_composicao import BancadaComposicao
from ordem_projeteis import consultar_celula_projetil, selecionar_ordem_projeteis


def sha(data):return hashlib.sha256(data).hexdigest()


def buffers(case):
    pool=bytearray(5600);discovery=bytearray(65536);light=bytearray(65536)
    for item in case['records']:
        offset=item['index']*56;pool[offset]=item.get('type',0);pool[offset+2]=item['active']
        struct.pack_into('<HH',pool,offset+0xc,item['x'],item['y']);pool[offset+0x18]=item.get('phase',0)
        struct.pack_into('<HH',pool,offset+0x14,0xabcd,0x1234)
    for cell,flag in case['discovery']:discovery[cell]=flag
    for cell,flag in case['light']:light[cell]=flag
    return bytes(pool),bytes(discovery),bytes(light),bytes(range(200))


def record(index,x,y,active=1,**values):return dict(index=index,x=x,y=y,active=active,**values)


def case(name,records,**changes):
    item=dict(name=name,records=records,origin=[20,20],window=[8,6],discovery=[],light=[])
    item.update(changes);return item


class BancadaProjeteis(BancadaComposicao):
    def __init__(self):
        self.capture=False;self.events=[];self.index=0
        super().__init__();self.pool=self.alocar(5600);self.discovery=self.alocar(65536)
        self.light=self.alocar(65536);self.output=self.alocar(200)
        self.escrever(0x5080f0,struct.pack('<I',self.pool));self.escrever(0x507d78,struct.pack('<I',self.discovery))
        self.escrever(0x507d88,struct.pack('<I',self.light));self.escrever(0x508041,b'\0')

    def _hook(self,cpu,address,size,data):
        if self.capture and address==0x45b247:
            self.events.append(dict(index=self.index,id_motor=self.reg('EBX')&65535,
                x=(self.reg('EAX')+32768)%65536-32768,y=(self.reg('EDX')+32768)%65536-32768))
        super()._hook(cpu,address,size,data)

    def prepare(self,case):
        pool,discovery,light,output=buffers(case)
        self.escrever(self.pool,pool);self.escrever(self.discovery,discovery);self.escrever(self.light,light)
        self.escrever(self.output,output);self.escrever(0x508720,struct.pack('<HH',*case['origin']))
        self.escrever(0x508724,struct.pack('<HH',*case['window']))
        return pool,discovery,light,output

    def order(self,case):
        inputs=self.prepare(case)
        self.executar(0x46fc8b,[(0x46fc8b,0x46fe9a),(0x46fc08,0x46fc0f),
            (0x4766f0,0x47670a),(0x476951,0x476968)],dict(EAX=self.output),paradas=[0x46fd9c])
        count=struct.unpack('<H',self.ler(self.reg('ESP')+8,2))[0]
        selected=list(struct.unpack('<'+'H'*count,self.ler(self.output,count*2)))
        self.retomar([],limite=1000000)
        output=self.ler(self.output,200)
        expected=selecionar_ordem_projeteis(*inputs,origem=case['origin'],janela_celulas=case['window'])
        assert self.reg('EAX')&65535==count==expected['quantidade']
        assert selected==expected['selecionadas'] and output==expected['indices_saida'],(case,selected,expected)
        assert self.ler(self.pool,5600)==inputs[0] and self.ler(self.discovery,65536)==inputs[1] and self.ler(self.light,65536)==inputs[2]
        return dict(selected=selected,ordered=list(struct.unpack('<'+'H'*count,output[:count*2])),
            output_hex=output.hex(),pool_preserved=True,stop=hex(self.reg('EIP')))

    def get_cell(self,pool,index):
        self.escrever(self.pool,pool)
        result=self.executar(0x46fe9a,[(0x46fe9a,0x46fee5)],dict(EAX=index))
        assert self.ler(self.pool,5600)==pool
        return result['EAX']


def validate():
    exigir_area_editavel();start=time.monotonic();b=BancadaProjeteis();c=Catalogo();rng=random.Random(0x46fc8b)
    base,image=imagem_pe();regions=[]
    for name,first,last in [('display_sort',0x46fc8b,0x46fe9a),('cell_query',0x46fe9a,0x46fee5),
            ('shared_epilogue',0x46fc08,0x46fc0f),('illumination',0x476951,0x476968),
            ('demo_type1_guard_dispatch',0x46ff70,0x4704d9)]:
        data=image[first-base:last-base]
        regions.append(dict(name=name,start=hex(first),end=hex(last),bytes_hex=data.hex(),sha256=sha(data)))
    (RAIZ/'evidencias/ordem-projeteis.json').write_text(json.dumps(dict(exe_sha256=HASH_EXE,regions=regions,
        predecessor_sources={name:sha((RAIZ/name).read_bytes()) for name in ('ordem_unidades.py','composicao.py')}),indent=2)+'\n')
    report=dict(exe_sha256=HASH_EXE,unicorn_version=unicorn.__version__,
        limits=dict(instructions_per_segment=1000000,timeout_us=2000000),
        checkpoint='0x46fd9c before sort, then complete native return',
        substitutions=dict(selection=[],sort=[],cell_query=[],demo_pixels=[],bank_loading=['file IO and allocation']),
        cases=[],cell_queries=[],overlap=[],unsupported=['full AffSprite traversal','public AffProjectile mapping; demo type1 only',
            'negative or out-of-map camera origins','physical projectile simulation'])
    cases=[case('empty',[]),case('last_equal',[record(i,640,640) for i in range(4)]),
        case('low_word_wrap',[record(0,0,8192),record(1,0,0),record(2,8192,0)],origin=[0,0],window=[256,256]),
        case('full100',[record(i,640+32*((99-i)%10),640+32*((99-i)//10)) for i in range(100)],window=[12,12])]
    for active in range(256):cases.append(case('active_byte',[record(99,640,640,active)]))
    for flag in range(256):
        cases.append(case('flag_bytes',[record(0,640,640),record(99,672,640)],
            discovery=[[0x1414,flag]],light=[[0x1415,flag]]))
    cases.append(case('window_edges',[record(i,x*32,y*32) for i,(x,y) in enumerate(
        ((19,20),(20,20),(29,20),(30,20),(20,19),(20,35),(20,36)))]))
    for ordinal in range(64):
        cases.append(case('seeded_'+str(ordinal),[record(i,rng.randrange(18*32,34*32),rng.randrange(18*32,39*32),rng.choice((0,1,2,255)))
            for i in rng.sample(range(100),32)]))
    for item in cases:report['cases'].append(dict(case=item,**b.order(item)))
    for x in (0,1,31,32,8191,8192,65535):
        for y in (0,1,31,32,8191,8192,65535):
            for index in (0,99):
                pool=bytearray(5600);struct.pack_into('<HH',pool,index*56+0xc,x,y)
                original=b.get_cell(pool,index);expected=consultar_celula_projetil(pool,index)
                assert original==expected['chave_u32']
                report['cell_queries'].append(dict(index=index,x=x,y=y,value=original))
    print('Display lists:',len(cases),'cell queries:',len(report['cell_queries']),flush=True)
    b.carregar_banco_original({name:c._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM})
    intervals=[(0x46ff70,0x4704d9),(0x46fc08,0x46fc0f),(0x476951,0x476968),
        (0x476702,0x47670a),(0x45b247,0x45b4fd)]
    for phase in range(8):
        item=case('indexed_replay_'+str(phase),[record(i,64+i%2,64+i//2,type=1,phase=(i+phase)%4)
            for i in range(4)],origin=[0,0],window=[4,4])
        capture=b.order(item);inputs=b.prepare(item);background=bytes((i*17+23)%256 for i in range(128*128))
        b.escrever(SUPERFICIE,background);b.escrever(0x508f70,struct.pack('<I',SUPERFICIE));b.escrever(0x4e17a0,struct.pack('<I',128))
        b.escrever(0x49a01c,struct.pack('<4H',0,127,0,127));b.events=[];b.capture=True
        for index in capture['ordered']:
            b.index=index;b.executar(0x46ff70,intervals,dict(EAX=index),limite=300000)
        b.capture=False;original=b.ler(SUPERFICIE,128*128)
        assert b.ler(b.pool,5600)==inputs[0]
        planned=selecionar_ordem_projeteis(*inputs,origem=item['origin'],janela_celulas=item['window'])
        draws={event['index']:event for event in b.events};out=background
        for index in planned['ordenadas']:
            event=draws[index];out=compor_indices(out,128,128,c.quadro(event['id_motor']),event['x'],event['y'])
        assert original==out
        report['overlap'].append(dict(case=item,**capture,draws=b.events,sha256=sha(original)))
    report.update(result='PASS',bounded_executions=b.execucoes,instructions=b.instrucoes,
        expected_exceptions=0,expected_limits=0,skips=0,seconds=round(time.monotonic()-start,3))
    (RAIZ/'validacao/x86-ordem-projeteis.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',len(report['overlap']),'indexed buffers;',b.execucoes,'bounded segments',flush=True)


if __name__=='__main__':validate()
