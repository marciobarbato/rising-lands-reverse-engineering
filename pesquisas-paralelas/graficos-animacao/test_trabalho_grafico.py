"""Prepared worker work display against independent original captures."""
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, Catalogo
from extrair_evidencias import imagem_pe
from trabalho_grafico import consultar_trabalho_grafico, compor_trabalho_grafico


def selection(v):return dict(indice_u16=v[9],camera_u8=v[11],indice_selecionado_u16=v[12],modo_selecao_u8=v[13])


def record(template,v):
    raw=bytearray(template);raw[0]=0;raw[1]=v[0];raw[2]=5;raw[0x89]=v[1]
    struct.pack_into('<H',raw,0xa,v[2]);raw[0x91]=v[3];raw[0xa4]=v[4]
    raw[0x86]=v[5]&255;raw[0x87]=v[6]&255;raw[0xbd]=v[10];raw[0xdc]=0
    struct.pack_into('<H',raw,0x74,v[14]);raw[0xba]=v[15];return raw


def layers(p):return [[l['id_motor'],l['x'],l['y'],l['operacao']] for l in p['camadas']]


class WorkGraphicsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((RAIZ/'validacao/x86-trabalho-grafico.json').read_text());cls.catalog=Catalogo()
        cls.templates={int(k):bytes.fromhex(v) for k,v in cls.report['initial_records'].items()}
        cls.shadow=bytes.fromhex(cls.report['shadow_table_hex'])

    def test_18516_original_command_captures_and_guard_stops(self):
        self.assertEqual(self.report['result'],'PASS');self.assertEqual(len(self.report['captures']),18516)
        for v,stop,native,supported in self.report['captures']:
            raw=record(self.templates[v[0]],v)
            if supported:
                self.assertEqual(stop,'0x3000000');self.assertEqual(layers(consultar_trabalho_grafico(raw,x=v[7],y=v[8],**selection(v))),native)
            else:
                self.assertIn(stop,('0x414b1f','0x410be4','0x41531c'))
                with self.assertRaises(NotImplementedError):consultar_trabalho_grafico(raw,x=v[7],y=v[8],**selection(v))
        r=self.report
        self.assertEqual(r['complete_capture_returns']+r['selection_prefix_stops']+r['selection_info_stops']+r['indicator_boundary_stops'],18516)

    def test_1179_original_indexed_buffers_and_input_preservation(self):
        self.assertEqual(len(self.report['pixels']),1179)
        for case in self.report['pixels']:
            v=case['input'];raw=record(self.templates[v[0]],v);before=bytes(raw)
            background=bytearray((i*17+23)%256 for i in range(128*128));original=bytes(background);shadow=bytearray(self.shadow)
            out,_=compor_trabalho_grafico(self.catalog,background,128,128,raw,x=v[7],y=v[8],tabela_sombra=shadow,recorte=case['clip'],**selection(v))
            self.assertEqual(hashlib.sha256(out).hexdigest(),case['sha256'])
            self.assertEqual(bytes(raw),before);self.assertEqual(bytes(background),original);self.assertEqual(bytes(shadow),self.shadow)

    def test_task_specific_native_overlay_bypass(self):
        for kind,task in ((6,3),(7,1),(7,2)):
            rows=[row for row in self.report['captures'] if row[0][0:2]==[kind,task] and row[0][10]==255 and row[0][11]==1]
            self.assertEqual(len(rows),256)
            for v,stop,native,supported in rows:
                self.assertEqual(stop,'0x3000000');self.assertEqual(native,[]);self.assertTrue(supported)
                p=consultar_trabalho_grafico(record(self.templates[kind],v),x=64,y=48,**selection(v))
                self.assertTrue(p['pular_pos_corpo'])
        blocked=[row for row in self.report['captures'] if row[0][0:2]==[7,1] and row[0][10]==1 and row[0][11]==0]
        self.assertTrue(blocked);self.assertTrue(all(row[1]=='0x414b1f' and not row[3] for row in blocked))

    def test_fixed_work_variants_and_strides(self):
        for kind,task,bag,expected in ((5,0,0,1602),(5,0,1,1698),(5,1,0,1666),(6,0,0,2978),(6,0,1,3042),(6,2,0,3042),(7,0,0,1346),(7,0,1,1474),(7,12,0,1410)):
            v=[kind,task,bag,1,0,0,0,64,48,0,0,0,65535,0,100,0];raw=record(self.templates[kind],v)
            raw[0xa5]=raw[0xa6]=raw[0xa8]=255
            p=consultar_trabalho_grafico(raw,x=64,y=48,**selection(v))
            self.assertEqual(p['camadas'][1]['id_motor'],expected)
            self.assertEqual([l['operacao'] for l in p['camadas']],['sombra','copiar'])

    def test_no_body_bypass_performs_no_catalog_access(self):
        class NoCatalog:
            def quadro(self,_):raise AssertionError('Bypass task fetched a frame')
        for kind,task in ((6,3),(7,1),(7,2)):
            v=[kind,task,65535,255,255,0,0,64,48,0,255,1,0,255,0,255]
            out,p=compor_trabalho_grafico(NoCatalog(),bytes(16),4,4,record(self.templates[kind],v),x=0,y=0,tabela_sombra=self.shadow,**selection(v))
            self.assertEqual(out,bytes(16));self.assertEqual(p['camadas'],[])

    def test_exact_input_widths_and_unsupported_record_guards(self):
        v=[5,0,0,1,0,0,0,64,48,0,0,0,65535,0,100,0];raw=record(self.templates[5],v)
        for offset,value in ((0,1),(1,13),(2,11),(0xdc,1),(0xba,1),(0x74,99),(0xbd,1)):
            bad=bytearray(raw);bad[offset]=value
            with self.assertRaises(NotImplementedError):consultar_trabalho_grafico(bad,x=0,y=0,**selection(v))
        for key,value in (('indice_u16',800),('camera_u8',256),('modo_selecao_u8',False),('indice_selecionado_u16',65536)):
            args=selection(v);args[key]=value
            with self.assertRaises(ValueError):consultar_trabalho_grafico(raw,x=0,y=0,**args)
        with self.assertRaises(ValueError):consultar_trabalho_grafico(raw[:-1],x=0,y=0,**selection(v))
        with self.assertRaises(TypeError):consultar_trabalho_grafico(raw,x=0,y=0)

    def test_original_bytes_and_unchanged_predecessors(self):
        e=json.loads((RAIZ/'evidencias/trabalho-grafico.json').read_text());base,image=imagem_pe()
        for r in e['regions']:
            data=bytes.fromhex(r['bytes_hex']);self.assertEqual(hashlib.sha256(data).hexdigest(),r['sha256'])
            self.assertEqual(data,image[int(r['start'],16)-base:int(r['end'],16)-base])
        for path,digest in e['predecessor_sources'].items():self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(),digest)


if __name__=='__main__':unittest.main()
