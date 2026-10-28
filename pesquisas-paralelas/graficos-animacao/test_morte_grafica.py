"""Original corpse copy/fade layers, indexed pixels and ignored-field guards."""
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, Catalogo
from extrair_evidencias import imagem_pe
from morte_grafica import consultar_morte_grafica, compor_morte_grafica


def runtime_record(template,v):
    raw=bytearray(template);raw[0]=0;raw[1]=v[0];raw[2]=4;raw[0xdc]=0
    struct.pack_into('<H',raw,0xc2,v[1]);raw[0x91]=v[2];raw[0xa4]=v[3];raw[0xdb]=v[4]
    raw[0x86]=v[5]&255;raw[0x87]=v[6]&255
    return raw


def layers(p):return [[l['id_motor'],l['x'],l['y'],l['operacao']] for l in p['camadas']]


class CorpseGraphicsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((RAIZ/'validacao/x86-morte-grafica.json').read_text());cls.catalog=Catalogo()
        cls.templates={int(k):bytes.fromhex(v) for k,v in cls.report['initial_records'].items()}
        cls.shadow=bytes.fromhex(cls.report['shadow_table_hex'])

    def test_17502_original_full_return_layer_captures(self):
        self.assertEqual(self.report['result'],'PASS');self.assertEqual(len(self.report['captures']),17502)
        unsupported=0
        for v,native,supported in self.report['captures']:
            raw=runtime_record(self.templates[v[0]],v)
            if supported:self.assertEqual(layers(consultar_morte_grafica(raw,x=v[7],y=v[8])),native)
            else:
                unsupported+=1
                with self.assertRaises(NotImplementedError):consultar_morte_grafica(raw,x=v[7],y=v[8])
        self.assertEqual(unsupported,1068);self.assertEqual(self.report['expected_dependency_stops'],0)

    def test_1210_original_indexed_buffers_and_immutability(self):
        self.assertEqual(len(self.report['pixels']),1210)
        for case in self.report['pixels']:
            v=case['input'];raw=runtime_record(self.templates[v[0]],v);before=bytes(raw)
            background=bytearray((i*17+23)%256 for i in range(128*128));original=bytes(background);shadow=bytearray(self.shadow)
            out,_=compor_morte_grafica(self.catalog,background,128,128,raw,x=v[7],y=v[8],tabela_sombra=shadow,recorte=case['clip'])
            self.assertEqual(hashlib.sha256(out).hexdigest(),case['sha256'])
            self.assertEqual(bytes(raw),before);self.assertEqual(bytes(background),original);self.assertEqual(bytes(shadow),self.shadow)

    def test_native_counter_boundaries_copy_before_mask_and_no_footprint_shadow(self):
        expected={0:['copiar'],299:['copiar'],300:['copiar'],304:['copiar'],305:['copiar','sombra'],
            310:['copiar','sombra','sombra'],314:['copiar','sombra','sombra'],315:['copiar']+['sombra']*3,
            316:['sombra']*3,319:['sombra']*3,320:['sombra']*2,325:['sombra'],329:['sombra'],330:[],65535:[]}
        for kind in self.templates:
            rows={v[1]:native for v,native,supported in self.report['captures'] if supported and v[0]==kind and v[2]==1 and v[3]==0 and v[9]==0}
            for counter,ops in expected.items():
                self.assertEqual([l[3] for l in rows[counter]],ops)
                self.assertTrue(all(l[0]!=10784 for l in rows[counter]))
                self.assertLessEqual(len({l[0] for l in rows[counter]}),1)

    def test_12_native_ignored_selection_fatigue_bag_and_other_stride_fields(self):
        self.assertEqual(len(self.report['ignored_field_captures']),12)
        for case in self.report['ignored_field_captures']:
            raw=bytes.fromhex(case['record_hex'])
            self.assertEqual(raw[0xbd],255);self.assertEqual(raw[0xba],255)
            self.assertEqual(layers(consultar_morte_grafica(raw,x=64,y=48)),case['layers'])

    def test_finished_counter_does_not_fetch_even_raw_catalog_overflow(self):
        class NoCatalog:
            def quadro(self,_):raise AssertionError('Finished corpse fetched a frame')
        for counter in (330,65535):
            raw=runtime_record(self.templates[2],[2,counter,255,255,255,0,0,64,48,0])
            out,p=compor_morte_grafica(NoCatalog(),bytes([82])*16,4,4,raw,x=0,y=0,tabela_sombra=self.shadow)
            self.assertEqual(out,bytes([82])*16);self.assertEqual(p['camadas'],[])

    def test_input_widths_and_unsupported_records(self):
        raw=runtime_record(self.templates[0],[0,0,1,0,8,0,0,64,48,0])
        for offset,value in ((0,1),(1,11),(2,2),(0xdc,1)):
            bad=bytearray(raw);bad[offset]=value
            with self.assertRaises(NotImplementedError):consultar_morte_grafica(bad,x=0,y=0)
        for x,y in ((32768,0),(False,0),(0,-32769)):
            with self.assertRaises(ValueError):consultar_morte_grafica(raw,x=x,y=y)
        with self.assertRaises(ValueError):consultar_morte_grafica(raw[:-1],x=0,y=0)
        with self.assertRaises(TypeError):consultar_morte_grafica(raw)
        with self.assertRaises(ValueError):compor_morte_grafica(self.catalog,bytes(16),4,4,raw,x=0,y=0,tabela_sombra=bytes(255))

    def test_original_bytes_predecessors_and_reviewed_rea(self):
        e=json.loads((RAIZ/'evidencias/morte-grafica.json').read_text());base,image=imagem_pe()
        for r in e['regions']:
            data=bytes.fromhex(r['bytes_hex']);self.assertEqual(hashlib.sha256(data).hexdigest(),r['sha256'])
            self.assertEqual(data,image[int(r['start'],16)-base:int(r['end'],16)-base])
        for path,digest in e['predecessor_sources'].items():self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(),digest)
        review=json.loads((RAIZ/'evidencias/rea-morte-grafica-review.json').read_text());native=review['instruction_observation']['normalized_result']
        self.assertEqual(native['address'],'0x415639');self.assertEqual(native['bytes'],image[0x415639-base:0x415640-base].hex())


if __name__=='__main__':unittest.main()
