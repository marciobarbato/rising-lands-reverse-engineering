"""Prepared attack rendering against independent original layer/pixel captures."""
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, Catalogo
from extrair_evidencias import imagem_pe
from ataque_grafico import consultar_ataque_grafico, compor_ataque_grafico


def selection(v):return dict(indice_u16=v[10],camera_u8=v[12],indice_selecionado_u16=v[13],modo_selecao_u8=v[14])


def record(template,v):
    raw=bytearray(template);raw[0]=0;raw[1]=v[0];raw[2]=v[1];raw[0x8a]=v[2]
    raw[0x91]=v[3];raw[0xa4]=v[4];raw[0xa6]=v[5];raw[0x86]=v[6]&255;raw[0x87]=v[7]&255
    raw[0xbd]=v[11];raw[0xdc]=raw[0xba]=0;struct.pack_into('<H',raw,0x74,100)
    return raw


def layers(p):return [[l['id_motor'],l['x'],l['y'],l['operacao']] for l in p['camadas']]


class AttackGraphicsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((RAIZ/'validacao/x86-ataque-grafico.json').read_text());cls.catalog=Catalogo()
        cls.templates={int(k):bytes.fromhex(v) for k,v in cls.report['initial_records'].items()}
        cls.shadow=bytes.fromhex(cls.report['shadow_table_hex'])

    def test_17960_original_capture_routes_and_layers(self):
        self.assertEqual(self.report['result'],'PASS');self.assertEqual(len(self.report['captures']),17960)
        for values,stop,native,supported in self.report['captures']:
            raw=record(self.templates[values[0]],values)
            if supported:
                self.assertEqual(stop,'0x3000000')
                self.assertEqual(layers(consultar_ataque_grafico(raw,x=values[8],y=values[9],**selection(values))),native)
            else:
                with self.assertRaises(NotImplementedError):consultar_ataque_grafico(raw,x=values[8],y=values[9],**selection(values))

    def test_974_original_indexed_buffers_and_immutability(self):
        self.assertEqual(len(self.report['pixels']),974)
        for capture in self.report['pixels']:
            v=capture['input'];raw=record(self.templates[v[0]],v);before=bytes(raw)
            background=bytearray((i*17+23)%256 for i in range(128*128));original=bytes(background);shadow=bytearray(self.shadow)
            out,_=compor_ataque_grafico(self.catalog,background,128,128,raw,x=v[8],y=v[9],tabela_sombra=shadow,recorte=capture['clip'],**selection(v))
            self.assertEqual(hashlib.sha256(out).hexdigest(),capture['sha256'])
            self.assertEqual(bytes(raw),before);self.assertEqual(bytes(background),original);self.assertEqual(bytes(shadow),self.shadow)

    def test_routes_stops_and_raw_catalog_rejections_are_separate(self):
        expected={'supported_capture_returns':15341,'normal_handler_stops':6,'selection_prefix_stops':2,
            'selection_info_stops':6,'no_draw_route_returns':1516,'raw_catalog_rejections':1089}
        for key,count in expected.items():self.assertEqual(self.report[key],count)
        self.assertEqual(sum(expected.values()),len(self.report['captures']))
        for values,stop,native,supported in self.report['captures']:
            if values[1]==22 and values[2] in (2,3):self.assertEqual(stop,'0x3000000');self.assertEqual(native,[]);self.assertFalse(supported)
            if values[2]==0:self.assertEqual(stop,'0x412390');self.assertFalse(supported)

    def test_raw_attack_stride_and_phase_do_not_use_walk_stride(self):
        v=[2,1,1,16,9,10,0,0,64,48,0,0,0,65535,0]
        raw=record(self.templates[2],v);raw[0xa5]=255
        plan=consultar_ataque_grafico(raw,x=64,y=48,**selection(v))
        self.assertEqual(plan['camadas'][1]['id_motor'],3345)
        self.assertEqual([l['operacao'] for l in plan['camadas']],['sombra','copiar'])
        self.assertEqual(self.templates[0][0xa6],10);self.assertEqual(self.templates[2][0xa6],10)

    def test_unsupported_guards_preflight_before_asset_access(self):
        class NoCatalog:
            def quadro(self,_):raise AssertionError('Unsupported attack fetched an asset')
        v=[0,1,1,1,0,10,0,0,64,48,0,0,0,65535,0];base=record(self.templates[0],v)
        for offset,value in ((0,1),(1,1),(2,2),(0x8a,0),(0xdc,1),(0xba,1),(0x74,99),(0xbd,1)):
            raw=bytearray(base);raw[offset]=value
            with self.assertRaises(NotImplementedError):compor_ataque_grafico(NoCatalog(),bytes(16),4,4,raw,x=0,y=0,tabela_sombra=self.shadow,**selection(v))

    def test_exact_input_widths_and_required_selection_inputs(self):
        v=[0,1,1,1,0,10,0,0,64,48,0,0,0,65535,0];raw=record(self.templates[0],v);args=selection(v)
        for key,value in (('indice_u16',800),('camera_u8',256),('modo_selecao_u8',False),('indice_selecionado_u16',65536)):
            bad=dict(args);bad[key]=value
            with self.assertRaises(ValueError):consultar_ataque_grafico(raw,x=0,y=0,**bad)
        with self.assertRaises(ValueError):consultar_ataque_grafico(raw,x=32768,y=0,**args)
        with self.assertRaises(ValueError):consultar_ataque_grafico(raw[:-1],x=0,y=0,**args)
        with self.assertRaises(TypeError):consultar_ataque_grafico(raw,x=0,y=0)

    def test_original_bytes_predecessors_and_reviewed_rea(self):
        evidence=json.loads((RAIZ/'evidencias/ataque-grafico.json').read_text());base,image=imagem_pe()
        for region in evidence['regions']:
            data=bytes.fromhex(region['bytes_hex']);self.assertEqual(hashlib.sha256(data).hexdigest(),region['sha256'])
            self.assertEqual(data,image[int(region['start'],16)-base:int(region['end'],16)-base])
        for path,digest in evidence['predecessor_sources'].items():self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(),digest)
        review=json.loads((RAIZ/'evidencias/rea-ataque-grafico-review.json').read_text());native=review['instruction_observation']['normalized_result']
        self.assertEqual(native['bytes'],image[0x413bff-base:0x413c05-base].hex());self.assertEqual(native['mnemonic'],'MOV')


if __name__=='__main__':unittest.main()
