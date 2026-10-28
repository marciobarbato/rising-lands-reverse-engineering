"""Original selected/sorted index buffers and order-sensitive overlap draws."""
import hashlib
import json
import random
import struct
import time
from bancada_x86 import Bancada, UNIDADE, SUPERFICIE, RETORNO, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, ORDEM, TIPOS
from composicao import compor_unidade
from validar_composicao import BancadaComposicao
from ordem_unidades import selecionar_ordem_unidades, POOL_SIZE, RECORD_SIZE


def sha(data):return hashlib.sha256(data).hexdigest()


def buffers(case):
    pool=bytearray(POOL_SIZE*RECORD_SIZE)
    for item in case['records']:
        offset=item['index']*RECORD_SIZE
        if 'raw_hex' in item:pool[offset:offset+RECORD_SIZE]=bytes.fromhex(item['raw_hex'])
        else:
            pool[offset+2]=item['state'];pool[offset+0xab]=item['priority']
            struct.pack_into('<H',pool,offset+8,item['cell'])
    discovery=bytearray(65536);light=bytearray(65536)
    for item in case.get('discovery',[]):discovery[item[0]]=item[1]
    for item in case.get('light',[]):light[item[0]]=item[1]
    return bytes(pool),bytes(discovery),bytes(light)


class BancadaOrdem(BancadaComposicao):
    def __init__(self):
        super().__init__();self.discovery=self.alocar(65536);self.light=self.alocar(65536)
        self.escrever(0x507d78,struct.pack('<I',self.discovery));self.escrever(0x507d88,struct.pack('<I',self.light))
        self.escrever(0x508041,b'\0')

    def order(self,case):
        pool,discovery,light=buffers(case)
        self.escrever(UNIDADE,pool);self.escrever(self.discovery,discovery);self.escrever(self.light,light)
        self.escrever(0x508724,struct.pack('<HH',*case['window']))
        self.executar(0x416864,[(0x416864,0x416a6c),(0x441fff,0x442025),
            (0x4766f0,0x47670a),(0x47693a,0x476951),(0x4766e8,0x4766f0)],
            dict(EAX=case['origin'][0],EDX=case['origin'][1]),paradas=[0x416946])
        count=self.reg('ESI')&65535;stack=self.reg('ESP')
        selected=list(struct.unpack('<'+'H'*count,self.ler(stack+8,count*2)))
        if count<=128:self.retomar([0x416a6c],limite=1000000)
        else:
            # Preserve original CPU/stack, pause only at outer-loop boundaries.
            self.retomar([0x41697d])
            while self.reg('EIP')!=0x416a6c:
                previous=self.reg('EIP');self.paradas=set();self.execucoes+=1
                self.cpu.emu_start(previous,RETORNO,timeout=2000000,count=1)
                assert self.reg('EIP')!=previous
                self.retomar([0x41697d,0x416a6c],limite=1000000)
        ordered=list(struct.unpack('<'+'H'*count,self.ler(stack+8,count*2)))
        assert self.ler(UNIDADE,len(pool))==pool
        assert self.ler(self.discovery,65536)==discovery and self.ler(self.light,65536)==light
        expected=selecionar_ordem_unidades(pool,discovery,light,origem=case['origin'],janela_celulas=case['window'])
        assert selected==expected['selecionadas'] and ordered==expected['ordenadas'],(case,selected,ordered,expected)
        return dict(selected=selected,ordered=ordered,stop=hex(self.reg('EIP')),
            pool_sha256=sha(pool),discovery_sha256=sha(discovery),light_sha256=sha(light),inputs_preserved=True)


def case(name,records,**changes):
    value=dict(name=name,records=records,origin=[20,20],window=[8,6],discovery=[],light=[])
    value.update(changes);return value


def record(index,cell,priority=0,state=2):
    return dict(index=index,cell=cell,priority=priority,state=state)


def validate():
    exigir_area_editavel();start=time.monotonic();b=BancadaOrdem();c=Catalogo();rng=random.Random(0x416864)
    base,image=imagem_pe();regions=[]
    for name,first,last in [('selection_and_sort',0x416864,0x416a6c),
            ('exists_query',0x441fff,0x442025),('discovery',0x4766f0,0x47670a),
            ('illumination',0x47693a,0x476951)]:
        data=image[first-base:last-base]
        regions.append(dict(name=name,start=hex(first),end=hex(last),bytes_hex=data.hex(),sha256=sha(data)))
    provenance=dict(exe_sha256=HASH_EXE,regions=regions,
        predecessor_sources={path:sha((RAIZ/path).read_bytes()) for path in ('composicao.py','evidencias/00416864.asm')})
    (RAIZ/'evidencias/ordem-unidades.json').write_text(json.dumps(provenance,indent=2)+'\n')
    cases=[case('empty',[]),case('unstable_equal_keys',[record(0,0x1415),record(1,0x1415),record(2,0x1414)])]
    for state in range(256):cases.append(case('state_byte',[record(799,0x1414,state=state)]))
    for axis in ('x','y'):
        values=(19,20,21,28,29,30) if axis=='x' else (19,20,21,34,35,36)
        cases.append(case('window_'+axis,[record(i,20*256+v if axis=='x' else v*256+20) for i,v in enumerate(values)]))
    cells=[(i//16)*256+i%16 for i in range(256)]
    for field in ('discovery','light'):
        cases.append(case('all_flag_bytes_'+field,[record(i,cell) for i,cell in enumerate(cells)],
            origin=[0,0],window=[16,16],**{field:[[cell,i] for i,cell in enumerate(cells)]}))
    cases.append(case('full_800_selected',[record(i,(20+(799-i)//32)*256+20+(799-i)%32,priority=i%7) for i in range(800)],window=[32,25]))
    for ordinal in range(64):
        records=[record(index,rng.randrange(18,38)*256+rng.randrange(18,33),rng.randrange(256),rng.choice((0,1,2,4,7,255)))
            for index in rng.sample(range(800),64)]
        cases.append(case('seeded_'+str(ordinal),records))
    report=dict(exe_sha256=HASH_EXE,unicorn_version=unicorn.__version__,
        limits=dict(instructions_per_segment=1000000,timeout_us=2000000),
        checkpoints=['0x416946: selected buffer before sorting','0x41697d: outer sort boundary for large buffers',
            '0x416a6c: before projectile sort/drawing'],
        substitutions=dict(selection=[],sort=[],overlap_pixels=[],bank_loading=['file IO and allocation']),
        cases=[],overlap=[],unsupported=['rest of AffSprite; projectiles and two-pass traversal','whole-scene/runtime consumer'])
    for item in cases:report['cases'].append(dict(case=item,**b.order(item)))
    print('Selection/sort fixtures:',len(cases),'including all 800 selected',flush=True)
    b.carregar_banco_original({name:c._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM})
    table=bytes(json.loads((RAIZ/'validacao/x86-composicao.json').read_text())['tabelas_sombra'][1]['indices'])
    intervals=[(0x41591f,0x415a57),(0x412390,0x41374c),(0x410fcc,0x41209d),
        (0x4470b9,0x4470c5),(0x442025,0x442065),(0x44fffe,0x45007a),
        (0x467d97,0x467da6),(0x45b247,0x45b4fd)]+b.intervalos_sombra()
    for phase in range(8):
        records=[]
        for index,kind in enumerate(TIPOS):
            raw=bytearray(b.inicializar_tipo(kind));raw[2]=2;raw[0x91]=1+2*index
            raw[0xa4]=phase;raw[0xab]=(4-index)%3
            struct.pack_into('<H',raw,8,0x1414);struct.pack_into('<H',raw,0x74,100)
            records.append(dict(index=index,raw_hex=raw.hex()))
        item=case('overlap_'+str(phase),records);capture=b.order(item)
        background=bytes((i*17+23)%256 for i in range(128*128));b.preparar_superficie(128,128,background,(0,0,127,127),table)
        pool,discovery,light=buffers(item);b.escrever(UNIDADE,pool)
        for index in capture['ordered']:
            b.executar(0x41591f,intervals,dict(EAX=64,EDX=48,EBX=index),limite=300000)
        original=b.ler(SUPERFICIE,128*128)
        planned=selecionar_ordem_unidades(pool,discovery,light,origem=item['origin'],janela_celulas=item['window'])
        out=background
        for index in planned['ordenadas']:
            offset=index*276
            out,_=compor_unidade(c,out,128,128,tipo=pool[offset+1],estado_u8=2,direcao=pool[offset+0x91],
                fase=pool[offset+0xa4],x=64,y=48,tabela=table,bolsa_u16=0)
        assert out==original
        stable=background
        stable_order=sorted(planned['selecionadas'],key=lambda index:(
            struct.unpack_from('<H',pool,index*276+8)[0],pool[index*276+0xab]))
        for index in stable_order:
            offset=index*276
            stable,_=compor_unidade(c,stable,128,128,tipo=pool[offset+1],estado_u8=2,direcao=pool[offset+0x91],
                fase=pool[offset+0xa4],x=64,y=48,tabela=table,bolsa_u16=0)
        report['overlap'].append(dict(case=item,**capture,sha256=sha(original),stable_order=stable_order,
            stable_sha256=sha(stable),stable_diff_pixels=sum(a!=z for a,z in zip(original,stable))))
    report.update(result='PASS',bounded_executions=b.execucoes,instructions=b.instrucoes,
        expected_exceptions=0,expected_limits=0,skips=0,seconds=round(time.monotonic()-start,3))
    (RAIZ/'validacao/x86-ordem-unidades.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',len(report['overlap']),'overlap buffers;',b.execucoes,'bounded segments',flush=True)


if __name__=='__main__':validate()
