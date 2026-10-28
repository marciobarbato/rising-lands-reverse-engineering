"""Regression against independent original type-2 layer and pixel captures."""
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, Catalogo, QUANTIDADES
from extrair_evidencias import imagem_pe
from unidade_tipo2 import consultar_corpo_tipo2, compor_corpo_tipo2


def runtime_record(template,values):
    state,direction,phase,count,dx,dy,_,_,_=values
    raw=bytearray(template);raw[0]=0;raw[1]=2;raw[2]=state
    raw[0x91]=direction;raw[0xa4]=phase;raw[0xa5]=count
    raw[0x86]=dx&255;raw[0x87]=dy&255
    raw[0x99]=raw[0xba]=raw[0xdc]=0;struct.pack_into('<H',raw,0x74,100)
    return raw


def selection(index=0):return dict(indice_u16=index,camera_u8=0,indice_selecionado_u16=65535,modo_selecao_u8=0)


def layers(plan):return [[l['id_motor'],l['x'],l['y'],l['operacao']] for l in plan['camadas']]


class TypeTwoBodyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((RAIZ/'validacao/x86-unidade-tipo2.json').read_text())
        cls.template=bytes.fromhex(cls.report['initial_record_hex'])
        cls.shadow=bytes.fromhex(cls.report['shadow_table_hex']);cls.catalog=Catalogo()

    def test_12564_native_layer_captures_and_raw_catalog_boundary(self):
        self.assertEqual(self.report['result'],'PASS');self.assertEqual(len(self.report['captures']),12564)
        unsupported=0
        for values,native,supported in self.report['captures']:
            raw=runtime_record(self.template,values)
            if supported:self.assertEqual(layers(consultar_corpo_tipo2(raw,x=values[6],y=values[7],**selection(values[8]))),native)
            else:
                unsupported+=1
                self.assertTrue(any(not 1<=l[0]<=sum(QUANTIDADES) for l in native))
                with self.assertRaises(NotImplementedError):consultar_corpo_tipo2(raw,x=values[6],y=values[7],**selection(values[8]))
        self.assertEqual(unsupported,555)

    def test_263_native_indexed_buffers_and_input_preservation(self):
        self.assertEqual(len(self.report['pixels']),263)
        for case in self.report['pixels']:
            values=case['input'];raw=runtime_record(self.template,values);before=bytes(raw)
            background=bytearray((i*17+23)%256 for i in range(128*128));original=bytes(background)
            shadow=bytearray(self.shadow)
            result,_=compor_corpo_tipo2(self.catalog,background,128,128,raw,x=values[6],y=values[7],tabela_sombra=shadow,recorte=case['clip'],**selection(values[8]))
            self.assertEqual(hashlib.sha256(result).hexdigest(),case['sha256'])
            self.assertEqual(bytes(raw),before);self.assertEqual(bytes(background),original);self.assertEqual(bytes(shadow),self.shadow)

    def test_raw_stride_phase_and_direction_zero_are_not_normalized(self):
        for direction,phase,count,expected in ((0,0,8,3194),(1,255,8,3457),(16,7,8,3265),(255,7,0,3209)):
            raw=runtime_record(self.template,[7,direction,phase,count,0,0,64,48,0])
            plan=consultar_corpo_tipo2(raw,x=64,y=48,**selection())
            self.assertEqual(plan['camadas'][1]['id_motor'],expected)
            self.assertEqual([l['operacao'] for l in plan['camadas']],['sombra','copiar'])
            self.assertEqual(plan['camadas'][0]['id_motor'],10784)
        self.assertEqual(self.template[0xa5],8);self.assertEqual(self.template[0x99],0)

    def test_native_unsigned_fatigue_guard_and_ignored_bag(self):
        self.assertEqual(len(self.report['guard_captures']),21)
        for capture in self.report['guard_captures']:
            raw=bytes.fromhex(capture['record_hex'])
            self.assertEqual(layers(consultar_corpo_tipo2(raw,x=64,y=48,**selection())),capture['layers'])
            self.assertEqual(struct.unpack_from('<H',raw,0x74)[0],capture['fatigue_u16'])
            self.assertEqual(struct.unpack_from('<H',raw,0xa)[0],capture['bag_u16'])

    def test_unsupported_preconditions_fail_before_catalog_lookup(self):
        class NoCatalog:
            def quadro(self,_):raise AssertionError('Unsupported state fetched a frame')
        base=runtime_record(self.template,[2,1,0,8,0,0,64,48,0])
        for offset,value in ((0,1),(1,0),(2,1),(2,4),(2,5),(2,14),(0x99,1),(0xdc,1),(0xba,1),(0x74,99)):
            raw=bytearray(base);raw[offset]=value
            with self.assertRaises(NotImplementedError):
                compor_corpo_tipo2(NoCatalog(),bytes(16),4,4,raw,x=0,y=0,tabela_sombra=self.shadow,**selection())

    def test_exact_input_widths(self):
        raw=runtime_record(self.template,[2,1,0,8,0,0,64,48,0])
        for x,y in ((-32769,0),(32768,0),(False,0),(0,32768)):
            with self.assertRaises(ValueError):consultar_corpo_tipo2(raw,x=x,y=y,**selection())
        with self.assertRaises(ValueError):consultar_corpo_tipo2(raw[:-1],x=0,y=0,**selection())
        with self.assertRaises(TypeError):consultar_corpo_tipo2(raw)
        with self.assertRaises(ValueError):compor_corpo_tipo2(self.catalog,bytes(16),4,4,raw,x=0,y=0,tabela_sombra=bytes(255),**selection())

    def test_original_bytes_unchanged_predecessors_and_reviewed_rea(self):
        evidence=json.loads((RAIZ/'evidencias/unidade-tipo2.json').read_text());base,image=imagem_pe()
        for region in evidence['regions']:
            data=bytes.fromhex(region['bytes_hex']);self.assertEqual(hashlib.sha256(data).hexdigest(),region['sha256'])
            self.assertEqual(data,image[int(region['start'],16)-base:int(region['end'],16)-base])
        for path,digest in evidence['predecessor_sources'].items():self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(),digest)
        review=json.loads((RAIZ/'evidencias/rea-unidade-tipo2-review.json').read_text());native=review['instruction_observation']['normalized_result']
        self.assertEqual(native['bytes'],image[0x412f06-base:0x412f0c-base].hex());self.assertEqual(native['mnemonic'],'MOV')
        self.assertEqual(review['original_executable_sha256'],evidence['exe_sha256'])


if __name__=='__main__':unittest.main()
