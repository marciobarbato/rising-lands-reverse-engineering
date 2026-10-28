"""Complete original interior terrain-pass captures and opaque block buffers."""
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, Catalogo
from extrair_evidencias import imagem_pe
from cache_terreno import CacheTerreno, resolver_bloco_terreno
from sequenciais import consultar_objeto_v6
from objetos import compor_passe
from passe_terreno import (terreno_de_construcao,planejar_passe_terreno,executar_passe_terreno,
    pixels_bloco_terreno,compor_bloco_terreno)


def sha(data):return hashlib.sha256(data).hexdigest()


def buffers(case):
    terrain=bytearray(struct.pack('<H',1)*65536);objects=bytearray(65536);aux=bytearray(65536)
    discovery=bytearray(65536);light=bytearray(65536)
    for cell,word in case['terrain']:struct.pack_into('<H',terrain,cell*2,word)
    for cell,d,l in case['flags']:discovery[cell]=d;light[cell]=l
    for cell,code,value in case['objects']:objects[cell]=code;aux[cell]=value
    return terrain,objects,aux,discovery,light


def make_cache(value):
    return CacheTerreno(bytes.fromhex(value['entries_hex']),bytes([value['raw_fill_u8']])*(256*1056),proximo_u16=value['next_u16'])


class TerrainPassTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((RAIZ/'validacao/x86-passe-terreno.json').read_text());cls.catalog=Catalogo()
        cls.shadow=bytes.fromhex(cls.report['shadow_table_hex'])

    def test_all_65536_original_construction_predicate_values(self):
        bitmap=bytes.fromhex(self.report['predicate_bitmap_hex']);self.assertEqual(len(bitmap),8192)
        for word in range(65536):self.assertEqual(terreno_de_construcao(word),bool(bitmap[word//8]&(1<<(word%8))))
        self.assertEqual(sum(bin(value).count('1') for value in bitmap),380)

    def test_72_original_complete_callback_traces_and_input_preservation(self):
        self.assertEqual(len(self.report['traces']),72)
        for capture in self.report['traces']:
            case=capture['case'];terrain,_,_,_,light=buffers(case);before=(bytes(terrain),bytes(light));events=[]
            plan=planejar_passe_terreno(terrain,light,origem=case['origin'],janela_celulas=case['window'],margem_i8=case['inset'])
            count=executar_passe_terreno(plan,bloco=lambda x,y,c,s:events.append(['bloco',x,y,c,s]),
                vegetacao=lambda x,y,c:events.append(['vegetacao',x,y,c]))
            self.assertEqual(events,capture['events']);self.assertEqual(count,len(events));self.assertEqual(capture['stop'],'0x3000000')
            self.assertEqual((bytes(terrain),bytes(light)),before)

    def test_eight_original_terrain_object_buffers_and_cache_states(self):
        self.assertEqual(len(self.report['pixels']),8)
        for capture in self.report['pixels']:
            case=capture['case'];terrain,objects,aux,discovery,light=buffers(case);cache=make_cache(case['initial_cache'])
            plan=planejar_passe_terreno(terrain,light,origem=case['origin'],janela_celulas=case['window'],margem_i8=case['inset'])
            w,h=(v*32 for v in case['window']);surface=[bytes((i*17+23)%256 for i in range(w*h))];ids=[]
            def block(x,y,cell,source):
                p=resolver_bloco_terreno(self.catalog,cache,id_terreno_u16=source,descoberta_u8=discovery[cell],
                    iluminacao_u8=light[cell],tabela_sombra=self.shadow)
                ident=p['id_motor'];ids.append(ident)
                surface[0]=compor_bloco_terreno(surface[0],w,h,pixels_bloco_terreno(self.catalog,cache,ident),x,y)
            def vegetation(x,y,cell):
                if objects[cell] in (0,253) or discovery[cell]&31:return
                p=consultar_objeto_v6(objects[cell],auxiliar_u8=aux[cell],descoberta_u8=discovery[cell],iluminacao_u8=light[cell])
                surface[0]=compor_passe(self.catalog,surface[0],w,h,p,'terreno',x,y,tabela_sombra=self.shadow,recorte=case['clip'])
            executar_passe_terreno(plan,bloco=block,vegetacao=vegetation)
            self.assertEqual(sha(surface[0]),capture['sha256']);self.assertEqual(ids,capture['resolved_ids'])
            self.assertEqual(sha(cache.registros),capture['cache_entries_sha256']);self.assertEqual(sha(cache.blocos_crus),capture['cache_raw_sha256'])
            self.assertEqual(cache.proximo_u16,capture['next_index']);self.assertEqual(capture['stop'],'0x3000000')
            if case['name']=='small_clip':
                l,t,r,b=case['clip'];background=bytes((i*17+23)%256 for i in range(w*h))
                self.assertTrue(any(surface[0][y*w+x]!=background[y*w+x] for y in range(h) for x in range(w)
                    if not (l<=x<=r and t<=y<=b)))

    def test_20_original_opaque_blocks_include_unaligned_positions_and_ignore_clip(self):
        self.assertEqual(len(self.report['blocks']),20)
        cache=make_cache(self.report['traces'][0]['case']['initial_cache'])
        for capture in self.report['blocks']:
            w,h,x,y=(capture[key] for key in ('w','h','x','y'));background=bytearray((i*17+23)%256 for i in range(w*h));before=bytes(background)
            out=compor_bloco_terreno(background,w,h,pixels_bloco_terreno(self.catalog,cache,capture['id']),x,y)
            self.assertEqual(sha(out),capture['sha256']);self.assertEqual(bytes(background),before)
        self.assertTrue(any(c['x']==13 and c['y']==17 for c in self.report['blocks']))

    def test_callback_failures_preserve_prior_effects_and_preflight_noncallables(self):
        case=next(capture['case'] for capture in self.report['traces'] if capture['case']['name']=='interior');terrain,_,_,_,light=buffers(case)
        plan=planejar_passe_terreno(terrain,light,origem=case['origin'],janela_celulas=case['window'],margem_i8=case['inset']);events=[]
        def block(*args):events.append('block')
        def vegetation(*args):events.append('vegetation');raise RuntimeError('fixture failure')
        with self.assertRaises(RuntimeError):executar_passe_terreno(plan,bloco=block,vegetacao=vegetation)
        self.assertEqual(events,['block','vegetation']);events.clear()
        with self.assertRaises(ValueError):executar_passe_terreno(plan,bloco=block,vegetacao=None)
        self.assertEqual(events,[])
        with self.assertRaises(TypeError):executar_passe_terreno(plan,bloco=block)

    def test_protected_viewport_and_block_domains(self):
        terrain=struct.pack('<H',1)*65536;light=bytes(65536)
        for origin,window,inset in (([255,255],[2,2],0),([0,0],[4,4],-1),([0,0],[4,4],3)):
            with self.assertRaises(NotImplementedError):planejar_passe_terreno(terrain,light,origem=origin,janela_celulas=window,margem_i8=inset)
        with self.assertRaises(ValueError):planejar_passe_terreno(terrain,light,origem=[False,0],janela_celulas=[4,4],margem_i8=0)
        with self.assertRaises(ValueError):terreno_de_construcao(65536)
        with self.assertRaises(NotImplementedError):compor_bloco_terreno(bytes(64*64),64,64,bytes(1024),33,0)
        with self.assertRaises(NotImplementedError):pixels_bloco_terreno(self.catalog,None,1082)

    def test_original_bytes_and_unchanged_predecessors(self):
        e=json.loads((RAIZ/'evidencias/passe-terreno.json').read_text());base,image=imagem_pe()
        for region in e['regions']:
            data=bytes.fromhex(region['bytes_hex']);self.assertEqual(sha(data),region['sha256'])
            self.assertEqual(data,image[int(region['start'],16)-base:int(region['end'],16)-base])
        for path,digest in e['predecessor_sources'].items():self.assertEqual(sha((RAIZ/path).read_bytes()),digest)


if __name__=='__main__':unittest.main()
