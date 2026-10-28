"""Independent original lighting tables, expected zero divisor and CMP blits."""
import hashlib
import json
import struct
import time
from bancada_x86 import SUPERFICIE, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, ORDEM, ler_cmp
from validar_composicao import BancadaComposicao
from eclairage import tabela_eclairage, compor_eclairage


def sha(data):return hashlib.sha256(data).hexdigest()


class BancadaEclairage(BancadaComposicao):
    def __init__(self):
        self.record_writes=False;self.writes=[]
        super().__init__()

    def _hook(self,cpu,address,size,data):
        if self.record_writes and address==0x45fb20:self.writes.append(self.reg('EAX'))
        super()._hook(cpu,address,size,data)

    def setup_table(self,palette,percentage,cycles):
        source=self.alocar(768);output=self.alocar(256)
        self.escrever(source,palette);self.escrever(output,bytes(range(256)))
        self.escrever(0x4e24b8,struct.pack('<I',output));self.escrever(0x4e24e1,bytes([len(cycles)]))
        self.escrever(0x4e24e4,b''.join(bytes([low,high,0]) for low,high in cycles))
        self.writes=[];self.record_writes=True
        intervals=[(0x45faf0,0x45fca5),(0x4795af,0x479610)]
        return source,output,intervals,dict(EAX=source,EDX=percentage)

    def calculate(self,palette,percentage,cycles):
        source,output,intervals,registers=self.setup_table(palette,percentage,cycles)
        self.executar(0x45fafc,intervals,registers,paradas=[0x45fb23])
        for _ in range(256):
            self.retomar([0x45fb16]);self.retomar([0x45fb23])
        self.retomar([]);self.record_writes=False
        assert self.writes==list(range(256)) and self.ler(source,768)==palette
        return self.ler(output,256)

    @staticmethod
    def blit_intervals():
        return [(0x45ba23,0x45bcb0),(0x45b4f6,0x45b4fd),(0x45f7d8,0x45f7f6),(0x45f6de,0x45f6e1)]

    def blit(self,ident,x,y,background,clip,table):
        self.preparar_superficie(128,128,background,clip,table)
        pointer=self.alocar(256);self.escrever(pointer,table);self.escrever(0x4e24b8,struct.pack('<I',pointer))
        self.executar(0x45ba23,self.blit_intervals(),dict(EAX=x,EDX=y,EBX=ident,ECX=1))
        return self.ler(SUPERFICIE,128*128)


def validate():
    exigir_area_editavel();start=time.monotonic();b=BancadaEclairage();c=Catalogo();base,image=imagem_pe()
    regions=[]
    for name,first,last in [('CalculEclairage',0x45fafc,0x45fca5),('table_epilogue',0x45faf0,0x45fafc),
            ('PasteEclairCmp',0x45ba23,0x45bcb0),('MemEclairCopy',0x45f7d8,0x45f7f6),
            ('setup_call',0x474f04,0x474f13)]:
        data=image[first-base:last-base]
        regions.append(dict(name=name,start=hex(first),end=hex(last),bytes_hex=data.hex(),sha256=sha(data)))
    (RAIZ/'evidencias/eclairage.json').write_text(json.dumps(dict(exe_sha256=HASH_EXE,regions=regions,
        predecessor_sources={path:sha((RAIZ/path).read_bytes()) for path in ('graficos.py','composicao.py')}),indent=2)+'\n')
    original_palette=c.paleta();synthetic=bytes((index*17)%256 for index in range(768))
    fixtures=[('PLATGAME',original_palette,value,[]) for value in (1,60,100,255)]
    fixtures += [('PLATGAME_cycles',original_palette,60,[(0,0),(160,167),(224,239)]),
        ('black_ties',bytes(768),60,[]),('all_candidates_excluded',synthetic,60,[(0,255)]),
        ('synthetic_cycles',synthetic,100,[(1,2),(15,35)])]
    report=dict(exe_sha256=HASH_EXE,unicorn_version=unicorn.__version__,
        limits=dict(instructions_per_segment=1000000,timeout_us=2000000),
        checkpoints=['0x45fb16 before each output write','0x45fb23 after each write/increment; then native RET'],
        substitutions=dict(table=[],blits=[],bank_loading=['file IO and allocation'],synthetic=['ID1 descriptor replaced only in emulated RAM']),
        tables=[],pixels=[],exceptions=[],unsupported=['CL=0 blitter path','whole initialization/palette cycling','projectile simulation'])
    for name,palette,percentage,cycles in fixtures:
        native=b.calculate(palette,percentage,cycles)
        assert native==tabela_eclairage(palette,percentual=percentage,ciclos=cycles)
        report['tables'].append(dict(name=name,palette_hex=palette.hex(),percentage=percentage,cycles=cycles,
            table_hex=native.hex(),write_indices=b.writes,palette_preserved=True))
        print('Lighting table:',name,percentage,flush=True)
    source,output,intervals,registers=b.setup_table(original_palette,0,[])
    try:b.executar(0x45fafc,intervals,registers)
    except unicorn.UcError as error:
        assert error.errno==unicorn.UC_ERR_EXCEPTION and b.reg('EIP')==0x45fb46
        assert b.writes==[] and b.ler(output,256)==bytes(range(256))
        report['exceptions'].append(dict(percentage=0,expected=True,code=error.errno,address=hex(b.reg('EIP')),output_unchanged=True))
    else:raise AssertionError('Original zero divisor did not fault')
    b.record_writes=False
    load=b.carregar_banco_original({name:c._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM})
    table=bytes.fromhex(report['tables'][1]['table_hex']);pattern=bytes((i*17+23)%256 for i in range(128*128))
    cases=[dict(ident=10784,x=40,y=45,background=index,clip=[0,0,127,127]) for index in range(256)]
    for ident in (10784,10876,11293,11325,11357):
        for x,y,clip in [(-3,-4,(0,0,127,127)),(0,0,(0,0,127,127)),(127,127,(0,0,127,127)),
                (128,128,(0,0,127,127)),(32,48,(40,50,55,52)),(40,45,(42,48,42,48)),
                (0,0,(40,50,55,52)),(110,110,(0,0,127,127))]:
            cases.append(dict(ident=ident,x=x,y=y,background=None,clip=list(clip)))
    for case in cases:
        background=pattern if case['background'] is None else bytes([case['background']])*(128*128)
        native=b.blit(case['ident'],case['x'],case['y'],background,case['clip'],table)
        assert native==compor_eclairage(background,128,128,c.quadro(case['ident']),case['x'],case['y'],table,case['clip'])
        report['pixels'].append(dict(**case,sha256=sha(native)))
    raw=struct.pack('<HHHI',1,4,1,5)+bytes([1,254,0,255,1]);frame=ler_cmp(raw)[0]
    descriptor=b.alocar(12);data=b.alocar(5);b.escrever(data,frame.comprimido)
    b.escrever(descriptor,struct.pack('<HHII',4,1,5,data));b.escrever(load['tabela'],struct.pack('<I',descriptor))
    background=bytes([82])*(128*128);native=b.blit(1,2,3,background,[0,0,127,127],table)
    assert native==compor_eclairage(background,128,128,frame,2,3,table)
    assert native[3*128+2:3*128+6]==bytes([82,table[82],table[82],82])
    report['synthetic']=dict(cmp_hex=raw.hex(),sha256=sha(native),literal_zero_opaque=True,source_colors_ignored=True)
    report.update(result='PASS',bounded_executions=b.execucoes,instructions=b.instrucoes,expected_exceptions=len(report['exceptions']),
        unexpected_exceptions=0,expected_limits=0,skips=0,seconds=round(time.monotonic()-start,3))
    (RAIZ/'validacao/x86-eclairage.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',len(report['tables']),'tables;',len(report['pixels'])+1,'indexed buffers;',b.execucoes,'segments;',len(report['exceptions']),'expected exception',flush=True)


if __name__=='__main__':validate()
