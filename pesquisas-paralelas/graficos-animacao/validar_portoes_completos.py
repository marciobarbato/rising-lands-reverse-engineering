"""Execute original AffBatiments through RET for the declared gate domain."""
import hashlib
import itertools
import json
import struct
import time
from bancada_x86 import Bancada, RETORNO, SUPERFICIE, UNIDADE, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, ORDEM
from portoes_completos import consultar_portao_completo, compor_portao_completo


def sha(data):return hashlib.sha256(data).hexdigest()


def fixture(**changes):
    args=dict(contador_u8=0,orientacao_u16=0,valor_0a_u16=35,jogador=0,camera=0,
        modo_u8=5,visibilidade_u8=0,descoberta_u8=0,x=128,y=128,
        janela_celulas=[10,10],terreno_u16=0,recorte_entrada=[11,13,300,299])
    args.update(changes)
    return args


class BancadaPortaoCompleto(Bancada):
    def __init__(self):
        self.capture=False;self.events=[]
        super().__init__();self.ptrs={}
        for name,address,size in [('occupancy',0x4e0f38,131072),('objects',0x507d74,65536),
                ('discovery',0x507d78,65536),('terrain',0x507d70,131072)]:
            ptr=self.alocar(size);self.ptrs[name]=ptr
            self.escrever(address,struct.pack('<I',ptr));self.escrever(ptr,bytes(size))

    def clip(self,address=0x49a01c):
        top,bottom,left,right=struct.unpack('<4H',self.ler(address,8))
        return [left,top,right,bottom]

    def _hook(self,cpu,address,size,data):
        if self.capture:
            operations={0x40f4b7:'save_clip',0x40f519:'set_clip',0x45b247:'copy',
                0x402864:'workshop_guard',0x40f4e8:'restore_clip',
                0x41a5b8:'habitation_query',0x4022c8:'selection_guard',0x4020ec:'gauge_guard'}
            if address in operations:
                event=dict(operation=operations[address])
                if address in (0x40f4b7,0x45b247):event['clip']=self.clip()
                if address==0x40f4e8:
                    left,right,top,bottom=struct.unpack('<4H',self.ler(0x49a02c,8))
                    event['restored_clip']=[left,top,right,bottom]
                if address==0x45b247:
                    event.update(id_motor=self.reg('EBX')&65535,
                        x=(self.reg('EAX')+32768)%65536-32768,
                        y=(self.reg('EDX')+32768)%65536-32768)
                self.events.append(event)
        super()._hook(cpu,address,size,data)

    def draw(self,args,*,habitado=False,selected=False,hovered=False,pixels=False):
        cell=0x0d11;record=0x49a0c8
        raw=bytearray(276)
        struct.pack_into('<H',raw,2,cell)
        raw[4]=args['jogador'];raw[5]=args['modo_u8'];raw[8]=12
        raw[0x76]=args['contador_u8'];raw[0x110+args['camera']]=args['visibilidade_u8']
        struct.pack_into('<H',raw,0x7c,args['orientacao_u16'])
        struct.pack_into('<H',raw,0xa,args['valor_0a_u16'])
        # An independent empty bag or one tagged unit of original type 9.
        # Only original BagContient reads it; the graphics API does not model bags.
        struct.pack_into('<H',raw,0xe,int(habitado))
        raw[0x4e]=1
        self.escrever(UNIDADE,bytes([0,9])+bytes(274));self.escrever(record,raw)
        self.escrever(self.ptrs['occupancy']+cell*2,struct.pack('<H',0x8000))
        self.escrever(self.ptrs['objects']+cell,b'\xfd')
        self.escrever(self.ptrs['terrain']+cell*2,struct.pack('<H',args['terreno_u16']))
        self.escrever(0x508041,bytes([args['camera']]))
        self.escrever(0x507d78+args['camera']*4,struct.pack('<I',self.ptrs['discovery']))
        self.escrever(self.ptrs['discovery']+cell,bytes([args['descoberta_u8']]))
        self.escrever(0x508724,struct.pack('<HH',*args['janela_celulas']))
        self.escrever(0x495be0,b'\xff'*10)
        self.escrever(0x495be0+args['jogador']*2,struct.pack('<H',0 if selected else 0xffff))
        self.escrever(0x496ac4,struct.pack('<H',0 if hovered else 0xffff))
        left,top,right,bottom=args['recorte_entrada']
        self.escrever(0x49a01c,struct.pack('<4H',top,bottom,left,right))
        width,height=(v*32 for v in args['janela_celulas'])
        background=bytes((i*17+23)%256 for i in range(width*height)) if pixels else b''
        if pixels:
            self.escrever(SUPERFICIE,background);self.escrever(0x508f70,struct.pack('<I',SUPERFICIE))
            self.escrever(0x4e17a0,struct.pack('<I',width))
        intervals=[(0x407dd3,0x40f49c),(0x41a6ec,0x41a70b),(0x41a08c,0x41a0ab),
            (0x41b54a,0x41b579),(0x4766d6,0x4766f0),(0x41a8e5,0x41a940),
            (0x40f4b7,0x40f535),(0x402864,0x40288b),(0x402c7a,0x402c82),
            (0x41a5b8,0x41a61c),(0x4471b8,0x44724a),(0x41a4f4,0x41a513),
            (0x4022c8,0x4022f9),(0x402490,0x402497),
            (0x4020ec,0x402122),(0x402268,0x40226f)]
        stubs={0x45b247:lambda b:b.retornar_stub()}
        if pixels:intervals.append((0x45b247,0x45b4fd));stubs={}
        self.events=[];self.capture=True
        result=self.executar(0x407dd3,intervals,dict(EAX=args['x'],EDX=args['y'],EBX=cell),stubs=stubs)
        self.capture=False
        assert result['EIP']==RETORNO
        assert self.ler(record,276)==bytes(raw)
        assert self.clip()==args['recorte_entrada']
        return dict(events=self.events,stop=hex(result['EIP']),clip=self.clip(),
            stack=result['ESP'],record_preserved=True),self.ler(SUPERFICIE,len(background)) if pixels else b''


def compare(args,capture):
    plan=consultar_portao_completo(**args)
    copies=[e for e in capture['events'] if e['operation']=='copy']
    expected=[dict(operation='copy',clip=plan['recorte'],id_motor=layer['id_motor'],
        x=layer['x'],y=layer['y']) for layer in plan['camadas']]
    assert copies==expected,(args,capture,plan)
    assert capture['clip']==plan['recorte_saida']
    assert capture['stack']==0x2008004
    operations=[event['operation'] for event in capture['events']]
    if plan['camadas']:
        assert operations[:6]==['save_clip','set_clip','copy','workshop_guard','restore_clip','habitation_query']
    else:assert not operations
    return plan


def validate():
    exigir_area_editavel();start=time.monotonic();b=BancadaPortaoCompleto();c=Catalogo()
    base,image=imagem_pe()
    regions=[]
    for name,first,last in [('shared_tail',0x40f342,0x40f49c),
            ('workshop_guard',0x402864,0x40288b),('workshop_epilogue',0x402c7a,0x402c82),
            ('selection_guard',0x4022c8,0x4022f9),('selection_epilogue',0x402490,0x402497),
            ('gauge_guard',0x4020ec,0x402122),('gauge_epilogue',0x402268,0x40226f),
            ('habitation_query',0x41a5b8,0x41a61c),('bag_read_dependency',0x4471b8,0x44724a)]:
        data=image[first-base:last-base]
        regions.append(dict(name=name,start=hex(first),end=hex(last),bytes_hex=data.hex(),sha256=sha(data)))
    provenance=dict(exe_sha256=HASH_EXE,regions=regions,
        predecessor_commit='6dcd05564047589e85fac4ba525ac762fedcc24f',
        predecessor_sources={name:sha((RAIZ/name).read_bytes()) for name in (
            'portoes_graficos.py','evidencias/portoes-graficos.json','validacao/x86-portoes-graficos.json')})
    (RAIZ/'evidencias/portoes-completos.json').write_text(json.dumps(provenance,indent=2)+'\n')
    report=dict(exe_sha256=HASH_EXE,unicorn_version=unicorn.__version__,
        limits=dict(facade_instructions=100000,bank_setup_instructions=1000000,timeout_us=2000000),
        substitutions=dict(captures=['PasteBobCmp intercepted'],pixels=[],habitation=[],guards=[],
            bank_loading=['file IO and allocation']),captures=[],pixels=[],
        unsupported=['terrain 0x356: whole-pool workshop lookup','other structure types','whole-scene/runtime consumer'])
    combinations=itertools.product((0,3,5,255),(0,1,4),(0,1),(0,1),(0,16),(False,True),(False,True),(False,True))
    for mode,owner,camera,visible,discovery,inhabited,selected,hovered in combinations:
        args=fixture(modo_u8=mode,jogador=owner,camera=camera,visibilidade_u8=visible,descoberta_u8=discovery)
        capture,_=b.draw(args,habitado=inhabited,selected=selected,hovered=hovered)
        compare(args,capture)
        report['captures'].append(dict(args=args,habitado=inhabited,selected=selected,hovered=hovered,**capture))
    print('Complete gate calls through RET:',len(report['captures']),flush=True)
    b.carregar_banco_original({name:c._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM})
    cases=[fixture(contador_u8=counter,orientacao_u16=orient) for orient in (0,1) for counter in range(32)]
    for value in (0,17,34,35,70,65535):
        for x,y in ((-20,-10),(310,310),(128,128),(0,0)):
            for orient in (0,65535):
                cases.append(fixture(contador_u8=15,valor_0a_u16=value,x=x,y=y,orientacao_u16=orient,
                    terreno_u16=65535,recorte_entrada=[319,319,0,0]))
    for args in cases:
        capture,original=b.draw(args,pixels=True,habitado=True,selected=True,hovered=True)
        plan=compare(args,capture);background=bytes((i*17+23)%256 for i in range(320*320))
        out,clip=compor_portao_completo(c,background,320,320,plan)
        assert original==out and list(clip)==capture['clip']
        report['pixels'].append(dict(args=args,sha256=sha(original),**capture))
    report.update(result='PASS',bounded_executions=b.execucoes,instructions=b.instrucoes,
        expected_exceptions=0,expected_limits=0,skips=0,seconds=round(time.monotonic()-start,3))
    (RAIZ/'validacao/x86-portoes-completos.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',len(report['pixels']),'indexed buffers;',b.execucoes,'bounded executions',flush=True)


if __name__=='__main__':validate()
