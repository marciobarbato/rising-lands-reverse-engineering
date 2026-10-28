"""Mechanic/builder construction display against independent native captures."""
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, Catalogo
from extrair_evidencias import imagem_pe
from construcao_grafica import consultar_construcao_grafica, compor_construcao_grafica


def selection(v):return dict(indice_u16=v[10],indice_selecionado_u16=v[12],modo_selecao_u8=v[13])


def record(template,v):
    raw=bytearray(template);raw[0]=0;raw[1]=v[0];raw[2]=v[1];raw[0x89]=v[2]
    struct.pack_into('<H',raw,0xa,v[3]);raw[0x91]=v[4];raw[0xa4]=v[5]
    raw[0x86]=v[6]&255;raw[0x87]=v[7]&255;raw[0xbd]=v[11];raw[0xdc]=raw[0xba]=0
    struct.pack_into('<H',raw,0x74,100);return raw


def layers(p):return [[l['id_motor'],l['x'],l['y'],l['operacao']] for l in p['camadas']]


class ConstructionGraphicsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((RAIZ/'validacao/x86-construcao-grafica.json').read_text());cls.catalog=Catalogo()
        cls.templates={int(k):bytes.fromhex(v) for k,v in cls.report['initial_records'].items()}
        cls.shadow=bytes.fromhex(cls.report['shadow_table_hex'])

    def test_30780_original_route_and_layer_captures(self):
        self.assertEqual(self.report['result'],'PASS');self.assertEqual(len(self.report['captures']),30780)
        for v,stop,native,supported in self.report['captures']:
            raw=record(self.templates[v[0]],v)
            if supported:
                self.assertEqual(stop,'0x3000000');self.assertEqual(layers(consultar_construcao_grafica(raw,x=v[8],y=v[9],**selection(v))),native)
            else:
                self.assertIn(stop,('0x41451d','0x410be4'))
                with self.assertRaises(NotImplementedError):consultar_construcao_grafica(raw,x=v[8],y=v[9],**selection(v))
        r=self.report;self.assertEqual(r['complete_capture_returns']+r['selection_prefix_stops']+r['selection_info_stops'],30780)

    def test_1554_original_indexed_buffers_and_immutability(self):
        self.assertEqual(len(self.report['pixels']),1554)
        for case in self.report['pixels']:
            v=case['input'];raw=record(self.templates[v[0]],v);before=bytes(raw)
            background=bytearray((i*17+23)%256 for i in range(128*128));original=bytes(background);shadow=bytearray(self.shadow)
            out,_=compor_construcao_grafica(self.catalog,background,128,128,raw,x=v[8],y=v[9],tabela_sombra=shadow,recorte=case['clip'],**selection(v))
            self.assertEqual(hashlib.sha256(out).hexdigest(),case['sha256'])
            self.assertEqual(bytes(raw),before);self.assertEqual(bytes(background),original);self.assertEqual(bytes(shadow),self.shadow)

    def test_fixed_strides_bag_variants_and_layer_order(self):
        for kind,task,bag,expected in ((7,0,0,1346),(7,0,1,1474),(7,1,0,1410),(6,0,0,2978),(6,0,1,3042),(6,1,0,3170)):
            v=[kind,11,task,bag,1,0,0,0,64,48,0,0,65535,0,0];raw=record(self.templates[kind],v)
            raw[0xa5]=raw[0xa6]=raw[0xa8]=255
            p=consultar_construcao_grafica(raw,x=64,y=48,**selection(v))
            self.assertEqual(p['camadas'][1]['id_motor'],expected)
            self.assertEqual([l['operacao'] for l in p['camadas']],['sombra','copiar'])
        v=[6,15,1,65535,16,255,0,0,64,48,799,0,65535,0,255]
        raw=record(self.templates[6],v);self.assertEqual(consultar_construcao_grafica(raw,x=64,y=48,**selection(v))['camadas'][1]['id_motor'],3453)

    def test_task_above_one_has_no_body_or_asset_lookup(self):
        class NoCatalog:
            def quadro(self,_):raise AssertionError('No-body task fetched an asset')
        for kind in (6,7):
            for task in (2,255):
                v=[kind,11,task,65535,255,255,0,0,64,48,0,0,65535,0,0];raw=record(self.templates[kind],v)
                out,p=compor_construcao_grafica(NoCatalog(),bytes(16),4,4,raw,x=0,y=0,tabela_sombra=self.shadow,**selection(v))
                self.assertEqual(out,bytes(16));self.assertEqual(p['camadas'],[])

    def test_selection_prefix_does_not_depend_on_camera(self):
        rows=[row for row in self.report['captures'] if row[0][11]!=0]
        self.assertTrue(rows)
        self.assertEqual({row[0][14] for row in rows},{0,1})
        self.assertTrue(all(row[1]=='0x41451d' and not row[3] for row in rows))

    def test_input_widths_and_preflight_guards(self):
        v=[7,11,0,0,1,0,0,0,64,48,0,0,65535,0,0];raw=record(self.templates[7],v)
        for offset,value in ((0,1),(1,5),(2,2),(0xdc,1),(0xba,1),(0x74,99),(0xbd,1)):
            bad=bytearray(raw);bad[offset]=value
            with self.assertRaises(NotImplementedError):consultar_construcao_grafica(bad,x=0,y=0,**selection(v))
        for key,value in (('indice_u16',800),('indice_u16',False),('indice_selecionado_u16',65536),('modo_selecao_u8',256)):
            args=selection(v);args[key]=value
            with self.assertRaises(ValueError):consultar_construcao_grafica(raw,x=0,y=0,**args)
        with self.assertRaises(ValueError):consultar_construcao_grafica(raw,x=32768,y=0,**selection(v))
        with self.assertRaises(TypeError):consultar_construcao_grafica(raw,x=0,y=0)

    def test_original_bytes_and_unchanged_predecessors(self):
        e=json.loads((RAIZ/'evidencias/construcao-grafica.json').read_text());base,image=imagem_pe()
        for r in e['regions']:
            data=bytes.fromhex(r['bytes_hex']);self.assertEqual(hashlib.sha256(data).hexdigest(),r['sha256'])
            self.assertEqual(data,image[int(r['start'],16)-base:int(r['end'],16)-base])
        for path,digest in e['predecessor_sources'].items():self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(),digest)


if __name__=='__main__':unittest.main()
