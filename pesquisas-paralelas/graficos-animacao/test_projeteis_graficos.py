"""Original projectile layers, indexed buffers and fully public scene draws."""
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, Catalogo, QUANTIDADES
from extrair_evidencias import imagem_pe
from composicao import compor_unidade
from objetos import consultar_objeto, compor_passe
from portoes_completos import consultar_portao_completo, compor_portao_completo
from passe_sprites import planejar_passe_sprites, executar_passe_sprites
from projeteis_graficos import consultar_projetil_grafico, compor_projetil


def runtime_record(values):
    kind,phase,direction,displacement,px,py,_,_,active,_,_=values
    raw=bytearray((index*37+19)%256 for index in range(56))
    raw[0]=kind;raw[2]=active;raw[0x18]=phase;raw[0x22]=direction
    struct.pack_into('<HH',raw,0xc,px,py);struct.pack_into('<I',raw,0x24,displacement)
    return bytes(raw)


def plan_layers(plan):return [[layer['id_motor'],layer['x'],layer['y'],layer['operacao']] for layer in plan['camadas']]


def scene_buffers(case):
    units=bytearray(800*276);projectiles=bytearray(5600);objects=bytearray(65536)
    discovery=bytearray(65536);light=bytearray(65536)
    for item in case['units']:units[item['index']*276:item['index']*276+276]=bytes.fromhex(item['raw_hex'])
    for item in case['projectiles']:
        offset=item['index']*56;projectiles[offset]=item['type'];projectiles[offset+2]=item['active']
        struct.pack_into('<HH',projectiles,offset+0xc,item['x'],item['y']);projectiles[offset+0x18]=item['phase']
    for cell,value in case['objects']:objects[cell]=value
    for cell,value in case['discovery']:discovery[cell]=value
    for cell,value in case['light']:light[cell]=value
    return bytes(units),bytes(projectiles),bytes(objects),bytes(discovery),bytes(light)


class ProjectileGraphicsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((RAIZ/'validacao/x86-projeteis-graficos.json').read_text());cls.catalog=Catalogo()
        cls.shadow=bytes.fromhex(cls.report['shadow_table_hex']);cls.lighting=bytes.fromhex(cls.report['lighting_table_hex'])

    def test_11728_original_dispatch_captures(self):
        self.assertEqual(self.report['result'],'PASS');self.assertEqual(len(self.report['captures']),11728)
        unsupported=0
        for values,native,supported in self.report['captures']:
            raw=runtime_record(values)
            if supported:
                plan=consultar_projetil_grafico(raw,origem=values[6:8],iluminacao_u8=values[9])
                self.assertEqual(plan_layers(plan),native)
            else:
                unsupported+=1
                self.assertTrue(any(not 1<=layer[0]<=sum(QUANTIDADES) for layer in native))
                with self.assertRaises(NotImplementedError):consultar_projetil_grafico(raw,origem=values[6:8],iluminacao_u8=values[9])
        self.assertEqual(unsupported,172)

    def test_410_original_indexed_buffers(self):
        self.assertEqual(len(self.report['pixels']),410)
        for capture in self.report['pixels']:
            values=capture['input'];raw=bytearray(runtime_record(values));before=bytes(raw)
            background=bytes((i*17+23)%256 for i in range(128*128))
            out,_=compor_projetil(self.catalog,background,128,128,raw,origem=values[6:8],iluminacao_u8=values[9],
                tabela_sombra=self.shadow,tabela_eclairage=self.lighting,recorte=capture['clip'])
            self.assertEqual(hashlib.sha256(out).hexdigest(),capture['sha256']);self.assertEqual(bytes(raw),before)

    def test_native_layer_order_and_raw_phase_behavior(self):
        cases=self.report['captures']
        for kind,operations in [(9,['sombra','copiar']),(29,['eclairage']*3),(30,['eclairage']*3),
                (31,['sombra']*2),(32,['eclairage']*2)]:
            native=next(row[1] for row in cases if row[0][0]==kind and row[0][1]==0)
            self.assertEqual([layer[3] for layer in native],operations)
        normal=next(row[1] for row in cases if row[0][0]==1 and row[0][1]==255)
        self.assertEqual(normal[0][0],0x2a7c+255)
        bullet0=next(row[1] for row in cases if row[0][0]==9 and row[0][1]==0)
        bullet255=next(row[1] for row in cases if row[0][0]==9 and row[0][1]==255)
        self.assertEqual(bullet0,bullet255)

    def test_no_draw_paths_do_not_access_catalog(self):
        class NoCatalog:
            def quadro(self,_):raise AssertionError('No-draw projectile fetched a frame')
        for kind,active,light in ((0,1,0),(28,1,0),(33,1,0),(255,1,0),(1,0,0),(1,1,1)):
            values=[kind,255,255,0xffffffff,65535,65535,0,0,active,light,0]
            out,plan=compor_projetil(NoCatalog(),bytes([82])*16,4,4,runtime_record(values),origem=[0,0],iluminacao_u8=light,
                tabela_sombra=self.shadow,tabela_eclairage=self.lighting)
            self.assertEqual(out,bytes([82])*16);self.assertEqual(plan['camadas'],[])

    def test_eight_original_scenes_without_captured_projectile_commands(self):
        self.assertEqual(len(self.report['scenes']),8)
        for capture in self.report['scenes']:
            case=capture['case'];units,projectiles,objects,discovery,light=scene_buffers(case)
            plan=planejar_passe_sprites(units,projectiles,objects,discovery,light,origem=case['origin'],janela_celulas=case['window'])
            w,h=(v*32 for v in case['window']);surface=[bytes((i*17+23)%256 for i in range(w*h))]
            clip=(0,0,w-1,h-1);auxiliaries=dict(case['auxiliaries'])
            def vegetation(x,y,cell):
                if objects[cell]==253:return
                p=consultar_objeto(objects[cell],auxiliar_u8=auxiliaries.get(cell,0),descoberta_u8=discovery[cell],iluminacao_u8=light[cell])
                surface[0]=compor_passe(self.catalog,surface[0],w,h,p,'sprites',x,y,tabela_sombra=self.shadow,recorte=clip)
            def building(x,y,cell):
                gate=case['gate']
                if not gate or cell!=gate['cell']:return
                p=consultar_portao_completo(contador_u8=gate['counter'],orientacao_u16=gate['orientation'],valor_0a_u16=35,
                    jogador=0,camera=0,modo_u8=5,visibilidade_u8=0,descoberta_u8=discovery[cell],x=x,y=y,
                    janela_celulas=case['window'],terreno_u16=0,recorte_entrada=clip)
                surface[0],_=compor_portao_completo(self.catalog,surface[0],w,h,p)
            def unit(x,y,index):
                offset=index*276
                surface[0],_=compor_unidade(self.catalog,surface[0],w,h,tipo=units[offset+1],estado_u8=2,direcao=units[offset+0x91],
                    fase=units[offset+0xa4],x=x,y=y,tabela=self.shadow,bolsa_u16=0,recorte=clip)
            def projectile(index):
                raw=projectiles[index*56:index*56+56];px,py=struct.unpack_from('<HH',raw,0xc)
                key=((py//32)*256+px//32)&65535
                surface[0],_=compor_projetil(self.catalog,surface[0],w,h,raw,origem=case['origin'],iluminacao_u8=light[key],
                    tabela_sombra=self.shadow,tabela_eclairage=self.lighting,recorte=clip)
            executar_passe_sprites(plan,vegetacao=vegetation,construcao=building,unidade=unit,projetil=projectile)
            self.assertEqual(hashlib.sha256(surface[0]).hexdigest(),capture['sha256'])
            self.assertEqual(capture['stop'],'0x3000000');self.assertTrue(capture['inputs_preserved'])

    def test_original_bytes_predecessors_and_rea_flow_caveat(self):
        evidence=json.loads((RAIZ/'evidencias/projeteis-graficos.json').read_text());base,image=imagem_pe()
        for region in evidence['regions']:
            data=bytes.fromhex(region['bytes_hex'])
            self.assertEqual(hashlib.sha256(data).hexdigest(),region['sha256'])
            self.assertEqual(data,image[int(region['start'],16)-base:int(region['end'],16)-base])
        for path,digest in evidence['predecessor_sources'].items():self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(),digest)
        review=json.loads((RAIZ/'evidencias/rea-projeteis-review.json').read_text())
        instruction=review['instruction_observation']['normalized_result']
        self.assertEqual(instruction['bytes'],image[0x46ffe7-base:0x46ffec-base].hex())
        self.assertEqual(instruction['mnemonic'],'JMP');self.assertEqual(instruction['flow']['kind'],'call')

    def test_input_widths_and_catalog_overflow_are_explicit(self):
        raw=runtime_record([1,0,1,0,0,0,0,0,1,0,0])
        for origin,light in (([0],0),([65536,0],0),([True,0],0),([0,0],256),([0,0],False)):
            with self.assertRaises(ValueError):consultar_projetil_grafico(raw,origem=origin,iluminacao_u8=light)
        with self.assertRaises(ValueError):consultar_projetil_grafico(raw[:-1],origem=[0,0],iluminacao_u8=0)
        with self.assertRaises(ValueError):compor_projetil(self.catalog,bytes(16),4,4,raw,origem=[0,0],iluminacao_u8=0,
            tabela_sombra=b'',tabela_eclairage=self.lighting)
        with self.assertRaises(TypeError):consultar_projetil_grafico(raw)


if __name__=='__main__':unittest.main()
