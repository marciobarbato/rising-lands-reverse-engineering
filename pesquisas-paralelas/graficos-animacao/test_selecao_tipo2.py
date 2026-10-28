"""Original type-2 selection branches and explicit API preflight boundaries."""
import hashlib
import json
import unittest
from graficos import RAIZ, Catalogo
from extrair_evidencias import imagem_pe
from unidade_tipo2 import consultar_corpo_tipo2, compor_corpo_tipo2


def selection(values):
    return dict(indice_u16=values[4],camera_u8=values[2],indice_selecionado_u16=values[5],modo_selecao_u8=values[3])


def raw_record(template,values):
    raw=bytearray(template);raw[0]=0;raw[1]=2;raw[2]=values[0];raw[0xbd]=values[1]
    raw[0x91]=16;raw[0xa4]=7;raw[0xa5]=8;raw[0x74]=100
    raw[0x99]=raw[0xdc]=raw[0xba]=0
    return raw


class TypeTwoSelectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((RAIZ/'validacao/x86-selecao-tipo2.json').read_text())
        cls.template=bytes.fromhex(cls.report['initial_record_hex']);cls.catalog=Catalogo()
        cls.shadow=bytes.fromhex(cls.report['shadow_table_hex'])

    def test_5136_original_branches_and_expected_dependency_stops(self):
        r=self.report;self.assertEqual(r['result'],'PASS');self.assertEqual(len(r['captures']),5136)
        self.assertEqual(r['full_capture_returns'],3596);self.assertEqual(r['expected_selection_prefix_stops'],514)
        self.assertEqual(r['expected_selection_info_stops'],1026)
        for values,stop,layers,esp in r['captures']:
            raw=raw_record(self.template,values)
            if stop=='0x3000000':
                p=consultar_corpo_tipo2(raw,x=64,y=48,**selection(values))
                self.assertEqual([[l['id_motor'],l['x'],l['y'],l['operacao']] for l in p['camadas']],layers)
                self.assertEqual(esp,0x2008004)
            else:
                self.assertIn(stop,('0x4124c4','0x410be4'))
                with self.assertRaises(NotImplementedError):consultar_corpo_tipo2(raw,x=64,y=48,**selection(values))

    def test_16_original_indexed_buffers_with_other_camera_selected_records(self):
        self.assertEqual(len(self.report['pixels']),16)
        for case in self.report['pixels']:
            values=case['input'];raw=raw_record(self.template,values);before=bytes(raw)
            background=bytes((i*17+23)%256 for i in range(128*128))
            out,_=compor_corpo_tipo2(self.catalog,background,128,128,raw,x=64,y=48,tabela_sombra=self.shadow,**selection(values))
            self.assertEqual(hashlib.sha256(out).hexdigest(),case['sha256']);self.assertEqual(bytes(raw),before)

    def test_overlay_rejections_precede_any_asset_or_surface_effect(self):
        class NoCatalog:
            def quadro(self,_):raise AssertionError('Selection preflight fetched an asset')
        for values in ([2,1,0,0,0,65535],[2,0,0,0,0,0],[7,0,0,1,799,65535]):
            raw=raw_record(self.template,values);surface=bytearray(16);before=bytes(raw)
            with self.assertRaises(NotImplementedError):compor_corpo_tipo2(NoCatalog(),surface,4,4,raw,x=0,y=0,tabela_sombra=self.shadow,**selection(values))
            self.assertEqual(bytes(raw),before);self.assertEqual(surface,bytes(16))

    def test_selection_inputs_are_required_and_exact_widths(self):
        raw=raw_record(self.template,[2,0,0,0,0,65535]);args=selection([2,0,0,0,0,65535])
        for key,value in (('indice_u16',800),('indice_u16',False),('indice_selecionado_u16',65536),('camera_u8',256),('modo_selecao_u8',-1)):
            bad=dict(args);bad[key]=value
            with self.assertRaises(ValueError):consultar_corpo_tipo2(raw,x=0,y=0,**bad)
        for key in args:
            bad=dict(args);del bad[key]
            with self.assertRaises(TypeError):consultar_corpo_tipo2(raw,x=0,y=0,**bad)

    def test_original_bytes_and_unchanged_stage_eight_reports(self):
        e=json.loads((RAIZ/'evidencias/selecao-tipo2.json').read_text());base,image=imagem_pe()
        for region in e['regions']:
            data=bytes.fromhex(region['bytes_hex']);self.assertEqual(hashlib.sha256(data).hexdigest(),region['sha256'])
            self.assertEqual(data,image[int(region['start'],16)-base:int(region['end'],16)-base])
        for path,digest in e['unchanged_reports'].items():self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(),digest)


if __name__=='__main__':unittest.main()
