"""Capture original gate facade calls, temporary clips and indexed buffers."""
import hashlib
import json
import struct
import time
from bancada_x86 import Bancada, SUPERFICIE, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, ORDEM, localizar, ler_paleta, png
from portoes_graficos import consultar_portao, compor_portao


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fixture(**changes):
    args = dict(contador_u8=0,orientacao_u16=0,valor_0a_u16=35,jogador=0,
        camera=0,modo_u8=5,visibilidade_u8=0,descoberta_u8=0,
        x=128,y=128,janela_celulas=[10,10])
    args.update(changes)
    return args


class BancadaPortoes(Bancada):
    def __init__(self):
        self.events = []; self.capture = False
        super().__init__()
        self.ptrs = {}
        for name,address,size in [('occupancy',0x4e0f38,131072),
                ('objects',0x507d74,65536),('discovery',0x507d78,65536)]:
            ptr = self.alocar(size); self.ptrs[name] = ptr
            self.escrever(address,struct.pack('<I',ptr))
            self.escrever(ptr,bytes(size))

    def clip(self):
        top,bottom,left,right = struct.unpack('<4H',self.ler(0x49a01c,8))
        return [left,top,right,bottom]

    def _hook(self,cpu,address,size,data):
        if self.capture:
            if address == 0x40f4b7:
                self.events.append(dict(operation='save_clip',clip=self.clip()))
            elif address == 0x40f519:
                self.events.append(dict(operation='set_clip',clip=[
                    self.reg(r)&65535 for r in ('EAX','EDX','EBX','ECX')]))
            elif address == 0x45b247:
                def i16(v):return (v+32768)%65536-32768
                self.events.append(dict(operation='copy',id_motor=self.reg('EBX')&65535,
                    x=i16(self.reg('EAX')),y=i16(self.reg('EDX')),clip=self.clip(),
                    clipping=self.reg('ECX')&255))
        super()._hook(cpu,address,size,data)

    def draw(self,args,*,pixels=False,index=0,occupancy=True,incoming=(11,13,300,299)):
        cell = 0x0d11; record = 0x49a0c8+index*276
        raw = bytearray((i*13+7)%256 for i in range(276))
        raw[4]=args['jogador'];raw[5]=args['modo_u8'];raw[8]=12
        raw[0x76]=args['contador_u8'];raw[0x110+args['camera']]=args['visibilidade_u8']
        struct.pack_into('<H',raw,0x7c,args['orientacao_u16'])
        struct.pack_into('<H',raw,0x0a,args['valor_0a_u16'])
        self.escrever(record,raw)
        self.escrever(self.ptrs['occupancy']+cell*2,struct.pack('<H',0x8000+index*32 if occupancy else 0))
        self.escrever(self.ptrs['objects']+cell,b'\xfd')
        self.escrever(0x508041,bytes([args['camera']]))
        self.escrever(0x507d78+args['camera']*4,struct.pack('<I',self.ptrs['discovery']))
        self.escrever(self.ptrs['discovery']+cell,bytes([args['descoberta_u8']]))
        self.escrever(0x508724,struct.pack('<HH',*args['janela_celulas']))
        left,top,right,bottom=incoming
        self.escrever(0x49a01c,struct.pack('<4H',top,bottom,left,right))
        width,height=(v*32 for v in args['janela_celulas'])
        background=bytes((i*17+23)%256 for i in range(width*height)) if pixels else b''
        if pixels:
            self.escrever(SUPERFICIE,background)
            self.escrever(0x508f70,struct.pack('<I',SUPERFICIE))
            self.escrever(0x4e17a0,struct.pack('<I',width))
        intervals=[(0x407dd3,0x40f49c),(0x41a6ec,0x41a70b),
            (0x41a08c,0x41a0ab),(0x41b54a,0x41b579),(0x4766d6,0x4766f0),
            (0x41a8e5,0x41a940),(0x40f4b7,0x40f535)]
        stubs={0x45b247:lambda b:b.retornar_stub()}
        if pixels:
            intervals.append((0x45b247,0x45b4fd));stubs={}
        self.events=[];self.capture=True
        result=self.executar(0x407dd3,intervals,dict(EAX=args['x'],EDX=args['y'],EBX=cell),
            paradas=[0x40f342,0x40f491],stubs=stubs)
        self.capture=False
        assert self.ler(record,276)==bytes(raw), 'Renderer mutated the gate record'
        assert self.ler(self.ptrs['occupancy']+cell*2,2)==struct.pack('<H',0x8000+index*32 if occupancy else 0)
        assert self.ler(self.ptrs['objects']+cell,1)==b'\xfd'
        assert self.ler(self.ptrs['discovery']+cell,1)==bytes([args['descoberta_u8']])
        return dict(events=self.events,stop=hex(result['EIP']),clip=self.clip(),
            record_preserved=True),self.ler(SUPERFICIE,len(background)) if pixels else b''


def compare(args,capture):
    plan=consultar_portao(**args)
    if plan['camadas']:
        layer=plan['camadas'][0]
        assert capture['events']==[
            dict(operation='save_clip',clip=[11,13,300,299]),
            dict(operation='set_clip',clip=plan['recorte']),
            dict(operation='copy',id_motor=layer['id_motor'],x=layer['x'],y=layer['y'],
                clip=plan['recorte'],clipping=1)],(args,capture,plan)
        assert capture['stop']=='0x40f342'
    else:
        assert capture['events']==[] and capture['stop']=='0x40f491',(args,capture)
    return plan


def validate():
    exigir_area_editavel();start=time.monotonic();b=BancadaPortoes();c=Catalogo()
    base,image=imagem_pe()
    regions=[]
    for name,first,last in [('AffBatiments_prefix',0x407dd3,0x407fa7),
            ('AffBatiments_HERSE',0x407fa7,0x4080e8),('copy_join',0x408412,0x408422),
            ('BatimentGetEtat',0x41a8e5,0x41a940),('clip_helpers',0x40f4b7,0x40f535),
            ('gate_type',0x495ffc,0x496030),('object_codes',0x495bf8,0x495bfa)]:
        data=image[first-base:last-base]
        regions.append(dict(name=name,start=hex(first),end=hex(last),bytes_hex=data.hex(),sha256=sha(data)))
    predecessors={name:sha((RAIZ/name).read_bytes()) for name in (
        'construcoes.py','graficos.py','composicao.py','evidencias/proveniencia-v6.json')}
    (RAIZ/'evidencias/portoes-graficos.json').write_text(json.dumps(dict(
        exe_sha256=HASH_EXE,regions=regions,predecessor_sources=predecessors),indent=2)+'\n')
    report=dict(exe_sha256=HASH_EXE,baseline_commit='6634be3af2d255846a847d8aa21ad4edf1cdb589',
        unicorn_version=unicorn.__version__,
        limits=dict(facade_instructions=100000,bank_setup_instructions=1000000,timeout_us=2000000),
        stops=['0x40f342: before AffVehiculeAtelier/shared tail','0x40f491: early return epilogue'],
        substitutions=dict(captures=['PasteBobCmp intercepted'],pixels=[],bank_loading=['file IO and allocation']),
        unsupported=['shared tail, selection, gauges, workshop callback, global scene ordering',
            'physical simulation, allocation, disk-to-runtime loading','public counters 32..255'],
        captures=[],raw_counter_captures=[],pixels=[],missing_occupancy=[])
    for orient in (0,1,256,65535):
        for counter in range(256):
            args=fixture(contador_u8=counter,orientacao_u16=orient)
            capture,_=b.draw(args)
            if counter<=31:
                compare(args,capture);report['captures'].append(dict(args=args,**capture))
            else:
                event=capture['events'][-1]
                assert event['id_motor']==(7576 if orient==0 else 7608)+counter
                report['raw_counter_captures'].append(dict(args=args,**capture))
    for mode in (0,3,5,255):
        for owner in range(5):
            for camera in range(4):
                for visible in (0,1,255):
                    for discovery in (0,1,15,16,31,255):
                        args=fixture(modo_u8=mode,jogador=owner,camera=camera,
                            visibilidade_u8=visible,descoberta_u8=discovery)
                        capture,_=b.draw(args);compare(args,capture)
                        report['captures'].append(dict(args=args,**capture))
    for value in (0,1,17,34,35,36,69,70,22937,22938,65535):
        for x,y in ((-32768,-32768),(-20,-10),(0,0),(128,128),(319,319),(32767,32767)):
            for orient in (0,65535):
                args=fixture(valor_0a_u16=value,x=x,y=y,orientacao_u16=orient)
                capture,_=b.draw(args,index=999);compare(args,capture)
                report['captures'].append(dict(args=args,**capture))
    for index in (0,999):
        capture,_=b.draw(fixture(),index=index,occupancy=False)
        assert capture['events']==[dict(operation='save_clip',clip=[11,13,300,299])]
        assert capture['stop']=='0x40f491'
        report['missing_occupancy'].append(dict(index=index,**capture))
    print('Gate calls and temporary clips captured:',len(report['captures']),flush=True)
    b.carregar_banco_original({name:c._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM})
    cases=[fixture(contador_u8=counter,orientacao_u16=orient) for orient in (0,1) for counter in range(32)]
    for value in (0,1,17,34,35,36,70,65535):
        for x,y in ((-20,-10),(0,0),(310,310),(128,128)):
            for orient in (0,65535):
                cases.append(fixture(contador_u8=15,valor_0a_u16=value,x=x,y=y,orientacao_u16=orient))
    cases += [fixture(contador_u8=counter,orientacao_u16=orient,x=8,y=4,
        janela_celulas=[2,2]) for orient in (0,1) for counter in range(32)]
    contact=bytearray(512*512)
    for args in cases:
        capture,original=b.draw(args,pixels=True);plan=compare(args,capture)
        width,height=(value*32 for value in args['janela_celulas'])
        background=bytes((i*17+23)%256 for i in range(width*height))
        assert original==compor_portao(c,background,width,height,plan),(args,capture)
        report['pixels'].append(dict(args=args,sha256=sha(original)))
        if width==64:
            ordinal=args['orientacao_u16']*32+args['contador_u8']
            cx,cy=(ordinal%8)*64,(ordinal//8)*64
            for row in range(64):
                contact[(cy+row)*512+cx:(cy+row)*512+cx+64]=original[row*64:row*64+64]
    associations=[]
    for ident in range(7576,7640):
        frame=c.quadro(ident)
        associations.append(dict(**localizar(ident),width=frame.largura,height=frame.altura,
            sha256_pixels=sha(frame.pixels),sha256_opacity=sha(frame.opacidade),
            opaque_pixels=sum(bool(v) for v in frame.opacidade),
            opaque_literal_zero=sum(p==0 and bool(mask) for p,mask in zip(frame.pixels,frame.opacidade))))
    report.update(result='PASS',bounded_executions=b.execucoes,instructions=b.instrucoes,
        expected_exceptions=0,expected_limits=0,skips=0,seconds=round(time.monotonic()-start,3))
    (RAIZ/'artefatos/associacoes-portoes.json').write_text(json.dumps(associations,indent=2)+'\n')
    palette=ler_paleta(c._ler('cd/INSTALHD/PLATGAME.PIE'))
    rgba=bytes(value for index in contact for value in (*palette[index*3:index*3+3],255))
    (RAIZ/'artefatos/portoes-contato.png').write_bytes(png(512,512,rgba))
    report['contact_sheet']=dict(path='artefatos/portoes-contato.png',
        indexed_sha256=sha(contact),palette_sha256=sha(palette),
        layout='8 columns; orientation 0 then 1; counter 0..31 row-major; each tile 64x64')
    (RAIZ/'validacao/x86-portoes-graficos.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',len(report['pixels']),'indexed buffers;',b.execucoes,'bounded executions',flush=True)


if __name__=='__main__':
    validate()
