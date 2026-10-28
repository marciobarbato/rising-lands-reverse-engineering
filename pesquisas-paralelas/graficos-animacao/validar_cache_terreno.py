"""Original GetNumBob graphics-cache state and complete raw-block comparisons."""
import hashlib
import json
import struct
import time
from bancada_x86 import RETORNO, unicorn
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, exigir_area_editavel
from graficos import Catalogo, ORDEM, png
from validar_composicao import BancadaComposicao
from cache_terreno import CacheTerreno, resolver_bloco_terreno, RAW_BLOCK, SLOTS, FIRST_CACHED_ID


def sha(data):return hashlib.sha256(data).hexdigest()


def initial_cache(*,cursor=0,fill=82,overrides=()):
    entries=bytearray(struct.pack('<HBB',65535,255,255)*256)
    for slot,source,light,fog in overrides:struct.pack_into('<HBB',entries,slot*4,source,light,fog)
    return dict(entries_hex=entries.hex(),raw_fill_u8=fill,next_u16=cursor)


def cache_from_initial(value):
    return CacheTerreno(bytes.fromhex(value['entries_hex']),bytes([value['raw_fill_u8']])*(256*1056),proximo_u16=value['next_u16'])


class BancadaCache(BancadaComposicao):
    def __init__(self,catalog):
        self.branch=None;super().__init__();self.catalog=catalog
        self.bank=self.carregar_banco_original({name:catalog._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM})
        self.entries=self.alocar(1024);self.raw_guard=self.alocar(256*RAW_BLOCK+64);self.raw=self.raw_guard+32
        self.escrever(0x49a050,struct.pack('<I',self.entries))
        assert struct.unpack('<H',self.ler(0x495bc4,2))[0]==256
        self.descriptors=[]
        for slot in range(256):
            ident=FIRST_CACHED_ID+slot;ptr=struct.unpack('<I',self.ler(self.bank['tabela']+(ident-1)*4,4))[0]
            assert struct.unpack('<HHI',self.ler(ptr,8))==(32,32,1056)
            self.escrever(ptr+8,struct.pack('<I',self.raw+slot*RAW_BLOCK));self.descriptors.append(ptr)
        self.maps=[];self.expected_maps=[]
        for global_pointer in (0x507d78,0x507d88):
            pointers=[];expected=[]
            for camera in range(4):
                pointer=self.alocar(65536);payload=bytearray([16])*65536
                self.escrever(pointer,payload);pointers.append(pointer);expected.append(payload)
                self.escrever(global_pointer+camera*4,struct.pack('<I',pointer))
            self.maps.append(pointers);self.expected_maps.append(expected)
        self.shadow=self.alocar(256);self.escrever(0x4e24b4,struct.pack('<I',self.shadow))
        self.table_snapshot=self.ler(self.bank['tabela'],self.bank['quantidade']*4)

    def _hook(self,cpu,address,size,data):
        branch={0x40fdb8:'undiscovered',0x40fe06:'direct',0x40fe6c:'hit',0x40fedd:'miss'}.get(address)
        if branch is not None:self.branch=branch
        super()._hook(cpu,address,size,data)

    def reset_cache(self,value):
        self.escrever(self.entries,bytes.fromhex(value['entries_hex']))
        self.escrever(self.raw_guard,bytes([204])*32+bytes([value['raw_fill_u8']])*(256*1056)+bytes([204])*32)
        self.escrever(0x49a04e,struct.pack('<H',value['next_u16']))

    def query(self,values,table):
        source,discovery,light,_,cell,camera=values
        self.escrever(0x508041,bytes([camera]));self.escrever(self.shadow,table)
        for index,flag in enumerate((discovery,light)):
            self.escrever(self.maps[index][camera]+cell,bytes([flag]));self.expected_maps[index][camera][cell]=flag
        preserved=dict(EBX=0xcafebabe,ECX=0x13579bdf,ESI=0x2468ace0,EDI=0x0badf00d,EBP=0x7f112233)
        self.branch=None
        result=self.executar(0x40fd95,[(0x40fd95,0x410085),(0x4766d6,0x4766f0),(0x47693a,0x476968),
            (0x476702,0x47670a),(0x45c779,0x45c8df),(0x45f7ba,0x45f7d8),(0x45f6de,0x45f6e1)],
            dict(EAX=source,EDX=cell,**preserved),limite=300000)
        assert result['EIP']==RETORNO and result['ESP']==0x2008004 and self.branch is not None
        for name,value in preserved.items():assert result[name]==value
        for index in (0,1):assert self.ler(self.maps[index][camera],65536)==bytes(self.expected_maps[index][camera])
        assert self.ler(self.raw_guard,32)==bytes([204])*32 and self.ler(self.raw+256*1056,32)==bytes([204])*32
        assert self.ler(0x495bc4,2)==b'\0\1' and self.ler(0x49a050,4)==struct.pack('<I',self.entries)
        return result['EAX'],self.branch,struct.unpack('<H',self.ler(0x49a04e,2))[0],self.ler(self.entries,1024),self.ler(self.raw,256*1056)

    def pixels_for_id(self,ident):
        if not (1<=ident<=1081 or 1090<=ident<=1345):return None
        ptr=struct.unpack('<I',self.ler(self.bank['tabela']+(ident-1)*4,4))[0]
        rawptr=struct.unpack('<I',self.ler(ptr+8,4))[0];raw=self.ler(rawptr,1056)
        return b''.join(raw[row*33+1:row*33+33] for row in range(32))

    def verify_read_only_inputs(self):
        assert self.ler(self.bank['tabela'],self.bank['quantidade']*4)==self.table_snapshot
        for index in (0,1):
            for camera in range(4):assert self.ler(self.maps[index][camera],65536)==bytes(self.expected_maps[index][camera])


def validate():
    exigir_area_editavel();start=time.monotonic();catalog=Catalogo();b=BancadaCache(catalog)
    base,image=imagem_pe();regions=[]
    for name,first,last in [('GetNumBob',0x40fd95,0x410085),('block_masks_and_copy',0x45c779,0x45c8df),
            ('discovery',0x4766d6,0x4766f0),('lighting',0x47693a,0x476968),('cache_capacity',0x495bc4,0x495bc6)]:
        raw=image[first-base:last-base];regions.append(dict(name=name,start=hex(first),end=hex(last),bytes_hex=raw.hex(),sha256=sha(raw)))
    evidence=dict(exe_sha256=HASH_EXE,regions=regions,predecessor_sources={name:sha((RAIZ/name).read_bytes()) for name in ('graficos.py','composicao.py','passe_sprites.py')})
    (RAIZ/'evidencias/cache-terreno.json').write_text(json.dumps(evidence,indent=2)+'\n')
    real_shadow=bytes.fromhex(json.loads((RAIZ/'validacao/x86-unidade-tipo2.json').read_text())['shadow_table_hex'])
    tables=[real_shadow,bytes(range(256)),bytes((value*37+23)%256 for value in range(256))]
    report=dict(exe_sha256=HASH_EXE,unicorn_version=unicorn.__version__,tables_hex=[table.hex() for table in tables],
        input_vector=['source_u16','discovery_u8','lighting_u8','shadow_table_index','cell_u16','camera_u8'],groups=[],
        limits=dict(instructions_per_call=300000,timeout_us=2000000),substitutions=dict(query=[],bank_loading=['file IO/allocation'],
            cache_payload_binding='256 dynamic payload pointers bound to one guarded synthetic RAM snapshot; original descriptors retain32x32/1056'),
        unsupported=['miss copying a source outside verified static full-literal blocks1..1081','mission/cache initialization','palette lifecycle','complete terrain pass'])
    sources=[]
    for ident in range(1,1082):
        frame=catalog.quadro(ident)
        assert (frame.largura,frame.altura,len(frame.comprimido))==(32,32,1056)
        assert all(frame.comprimido[row*33]==224 for row in range(32))
        sources.append(sha(frame.comprimido))
    report['source_block_sha256']=sha(''.join(sources).encode('ascii'))
    groups=[]
    groups.append(('all_flags',initial_cache(),[(7,d,l,0) for d in range(32) for l in range(32)]+
        [(2,value,0,0) for value in range(256)]+[(3,0,value,0) for value in range(256)]+[(4,value,255-value,0) for value in range(256)]+[(0,16,0,0),(65535,16,255,0),(0,0,0,0),(65535,0,0,0)]))
    groups.append(('all_static_sources',initial_cache(cursor=255),[(ident,1,1,2) for ident in range(1,1082)]))
    groups.append(('masks_and_tables',initial_cache(),[(ident,d,l,table) for table in range(3) for ident in (1,2,17,300,800,1080,1081) for d in range(16) for l in range(16)]))
    groups.append(('duplicates_and_raw_hit',initial_cache(cursor=255,fill=97,overrides=[(5,123,2,1),(77,123,2,1),(3,65535,1,1)]),
        [(123,1,2,0),(123,225,226,2),(65535,1,1,1),(42,3,4,0),(43,3,4,0),(42,3,4,2)]))
    groups.append(('table_staleness',initial_cache(),[(1,1,2,2),(1,1,2,1)]+[(ident,1,2,1) for ident in range(2,262)]+[(1,1,2,1)]))
    contact=bytearray(512*512);case_count=0;branch_counts={name:0 for name in ('undiscovered','direct','hit','miss')}
    for name,initial,cases in groups:
        b.reset_cache(initial);cache=cache_from_initial(initial);group=dict(name=name,initial=initial,captures=[])
        for source,discovery,light,table_index in cases:
            cell=(0,65535,32768,0x1234)[case_count%4];camera=(0,3)[case_count%2]
            values=[source,discovery,light,table_index,cell,camera];table=tables[table_index]
            ident,branch,next_index,entries,raw=b.query(values,table)
            plan=resolver_bloco_terreno(catalog,cache,id_terreno_u16=source,descoberta_u8=discovery,iluminacao_u8=light,tabela_sombra=table)
            assert ident==plan['id_motor'] and branch==plan['motivo']
            assert next_index==cache.proximo_u16 and entries==bytes(cache.registros) and raw==bytes(cache.blocos_crus),(name,values,branch)
            pixels=b.pixels_for_id(ident)
            if 1090<=ident<=1345:assert pixels==cache.pixels(ident-1090)
            elif pixels is not None:assert pixels==catalog.quadro(ident).pixels
            group['captures'].append([values,ident,branch,next_index,sha(entries),sha(raw),sha(pixels) if pixels is not None else None])
            if name=='masks_and_tables' and source==300 and table_index==0:
                for row in range(32):contact[(light*32+row)*512+discovery*32:(light*32+row)*512+discovery*32+32]=pixels[row*32:row*32+32]
            case_count+=1;branch_counts[branch]+=1
        b.verify_read_only_inputs();report['groups'].append(group)
        print('Original terrain cache group:',name,len(cases),flush=True)
    palette=catalog.paleta();rgba=bytes(c for index in contact for c in (*palette[index*3:index*3+3],255))
    (RAIZ/'artefatos/cache-terreno-mascaras.png').write_bytes(png(512,512,rgba))
    report.update(result='PASS',bounded_executions=b.execucoes,instructions=b.instrucoes,cases=case_count,branches=branch_counts,
        expected_exceptions=0,expected_limits=0,skips=0,seconds=round(time.monotonic()-start,3))
    # Keep each independent cache observation on one readable compact row.
    groups_encoded=[]
    for group in report.pop('groups'):
        groups_encoded.append('    {"name":'+json.dumps(group['name'])+',"initial":'+json.dumps(group['initial'])+',"captures":[\n'+
            ',\n'.join('      '+json.dumps(row,separators=(',',':')) for row in group['captures'])+'\n    ]}')
    encoded=json.dumps(report,indent=2)[:-2]+',\n  "groups":[\n'+',\n'.join(groups_encoded)+'\n  ]\n}\n'
    (RAIZ/'validacao/x86-cache-terreno.json').write_text(encoded)
    print('PASS:',case_count,'full-state/raw-block comparisons;',b.execucoes,'native calls',flush=True)


if __name__=='__main__':validate()
