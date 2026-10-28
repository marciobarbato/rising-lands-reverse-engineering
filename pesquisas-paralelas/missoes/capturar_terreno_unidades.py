"""Original-only captures; preserve the pre-orchestration v1 output observations."""
import hashlib
import json
import struct
from ambiente_missoes import CD,OWNED
from analisar import HASH_ESTUDADO
from entradas import tipos_originais,bloco_unidades
from formatos import ler_eta
from navegacao_unidades import MundoNavegacao
from ordens_unidades import ContextoBusca
from sequenciais import normalizar_inicio


def preparar_caso(name,classe=MundoNavegacao):
    mission=name=='MONDE01'
    data=(CD/'WORLD/MONDE01.ETA').read_bytes() if mission else None
    metadata=ler_eta(data) if mission else None
    world=classe(metadata['largura'] if mission else 16,metadata['altura'] if mission else 16)
    world.unidades[:]=b'\xa5'*220800
    for index in range(800):
        world.unidades[index*276+2]=0
    world.regioes[:]=[1]*65536
    world.selecoes_unidades[:]=bytes((i*23+0x53)&255 for i in range(2048))
    world.busca=ContextoBusca(7,1,1,0x12345678,77)
    if mission:
        world.atributos[:]=data[4:0x10004]
        world.tiles[:]=struct.unpack('<65536H',data[0x10004:0x30004])
        normalized=normalizar_inicio(data[0x30004:0x40004],data[0x40004:0x50004])
        world.objetos[:]=normalized['objetos'];world.donos_objetos[:]=normalized['auxiliares']
        types=tipos_originais();offset=bloco_unidades(data)['offset']
    else:
        types=bytes(1300)
        record=bytearray(784)
        record[0]=200 if name=='state4_neutral' else 0
        record[1]=0
        record[2]=4 if name=='state4_neutral' else 14 if name=='hidden14' else 7
        record[0x72]=255
        struct.pack_into('<H',record,8,0x505)
        struct.pack_into('<H',record,0x7c,0x505)
        data=struct.pack('<HHH',1,784,7)+record
        offset=0
    return world,data,offset,types,b'\x31'*1872,bytearray(b'\x11\x22\x33\x44')


def resumo_original(native):
    from emulador import UNIDADES
    buffers={}
    for name in ('atributos','regioes','tiles','mini_final','mini_unidades','mini_estruturas',
                 'descoberto','luz_bordas','contagem_luz','donos_objetos'):
        size=262144 if name in ('descoberto','luz_bordas','contagem_luz') else 131072 if name in ('regioes','tiles') else 65536
        buffers[name]=hashlib.sha256(bytes(native.cpu.mem_read(native.grades[name],size))).hexdigest()
    return dict(unit_pool_sha256=hashlib.sha256(bytes(native.cpu.mem_read(UNIDADES,220800))).hexdigest(),
                physical_sha256=buffers,selection_sha256=hashlib.sha256(native.selecoes()).hexdigest(),
                search=native.busca_original(),parent_calls=[list(e) for e in native.parent_calls],
                physical_effect_count=len(native.efeitos),
                physical_effect_sha256=hashlib.sha256(json.dumps(native.efeitos,separators=(',',':')).encode()).hexdigest())


def capturar():
    from bancada_terreno_unidades import BancadaTerrenoUnidades
    native=BancadaTerrenoUnidades();cases=[]
    for name in ('ordinary','state4_neutral','hidden14','MONDE01'):
        args=preparar_caso(name)
        native.carregar_caso(*args)
        before=resumo_original(native)
        regs=native.prefixo()
        cases.append(dict(name=name,source_sha256=hashlib.sha256(args[1]).hexdigest(),
                          input_after_native_unit_load=before,output=resumo_original(native),checkpoint=hex(regs['EIP'])))
    report=dict(original_sha256=HASH_ESTUDADO,unit_loader_entries=native.loads,
                placement_prefix_entries=native.prefixes,bounded_segments=native.execucoes,
                preserved_cpu_minimap_resumes=native.retomadas_minimapa,cases=cases,
                scope='Original-only unit-load plus MissionPlaceTerrain unit/capacity prefix; actual MONDE01 unit bytes with explicitly synthetic inherited physical/region/color/search state. No complete reset/remap/startup, intervening auxiliary effects, structure insertion or mission execution.')
    report['correction']='Freeze input parent-call trace before the prefix; v1 retained its live list and later serialized output calls. Original output observations and buffer hashes are unchanged.'
    old_path=OWNED/'evidencias/captura-terreno-unidades-original.json'
    if old_path.exists():
        old=json.loads(old_path.read_text())
        for prior,current in zip(old['cases'],report['cases']):
            if prior['output']!=current['output']:
                raise ValueError('Original output changed during trace-freezing recapture')
    (OWNED/'evidencias/captura-terreno-unidades-original-v2.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    r=capturar();print('Original placement prefixes:',r['placement_prefix_entries'],'segments:',r['bounded_segments'])
