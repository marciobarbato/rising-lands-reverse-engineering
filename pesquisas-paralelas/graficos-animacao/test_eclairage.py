"""Original lighting tables and independent indexed destination buffers."""
import hashlib
import json
import unittest
from graficos import RAIZ, Catalogo, ler_cmp
from extrair_evidencias import imagem_pe
from eclairage import tabela_eclairage, compor_eclairage


class EclairageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((RAIZ/'validacao/x86-eclairage.json').read_text());cls.catalog=Catalogo()

    def test_eight_original_tables_and_sequential_output_writes(self):
        self.assertEqual(self.report['result'],'PASS');self.assertEqual(len(self.report['tables']),8)
        for capture in self.report['tables']:
            actual=tabela_eclairage(bytes.fromhex(capture['palette_hex']),percentual=capture['percentage'],ciclos=capture['cycles'])
            self.assertEqual(actual,bytes.fromhex(capture['table_hex']))
            self.assertEqual(capture['write_indices'],list(range(256)));self.assertTrue(capture['palette_preserved'])

    def test_ties_and_initial_zero_candidate_inside_cycle(self):
        black=next(item for item in self.report['tables'] if item['name']=='black_ties')
        excluded=next(item for item in self.report['tables'] if item['name']=='all_candidates_excluded')
        self.assertEqual(bytes.fromhex(black['table_hex']),bytes(256))
        self.assertEqual(bytes.fromhex(excluded['table_hex']),bytes(256))

    def test_296_original_indexed_buffers_all_destination_indices_and_clips(self):
        self.assertEqual(len(self.report['pixels']),296)
        table=bytes.fromhex(self.report['tables'][1]['table_hex'])
        for capture in self.report['pixels']:
            background=(bytes((i*17+23)%256 for i in range(128*128)) if capture['background'] is None
                else bytes([capture['background']])*(128*128))
            actual=compor_eclairage(background,128,128,self.catalog.quadro(capture['ident']),capture['x'],capture['y'],table,capture['clip'])
            self.assertEqual(hashlib.sha256(actual).hexdigest(),capture['sha256'])

    def test_synthetic_opacity_literal_zero_and_ignored_source_colors(self):
        capture=self.report['synthetic'];frame=ler_cmp(bytes.fromhex(capture['cmp_hex']))[0]
        table=bytes.fromhex(self.report['tables'][1]['table_hex']);background=bytes([82])*(128*128)
        actual=compor_eclairage(background,128,128,frame,2,3,table)
        self.assertEqual(hashlib.sha256(actual).hexdigest(),capture['sha256'])
        self.assertEqual(actual[3*128+2:3*128+6],bytes([82,table[82],table[82],82]))
        self.assertTrue(capture['literal_zero_opaque']);self.assertTrue(capture['source_colors_ignored'])

    def test_original_zero_divisor_is_explicit_expected_exception(self):
        self.assertEqual(self.report['expected_exceptions'],1);self.assertEqual(self.report['unexpected_exceptions'],0)
        exception=self.report['exceptions'][0]
        self.assertEqual(exception['address'],'0x45fb46');self.assertTrue(exception['expected']);self.assertTrue(exception['output_unchanged'])
        with self.assertRaises(ValueError):tabela_eclairage(bytes(768),percentual=0,ciclos=[])

    def test_original_bytes_and_preserved_sources(self):
        evidence=json.loads((RAIZ/'evidencias/eclairage.json').read_text());base,image=imagem_pe()
        self.assertEqual(evidence['exe_sha256'],self.report['exe_sha256'])
        for region in evidence['regions']:
            data=bytes.fromhex(region['bytes_hex'])
            self.assertEqual(hashlib.sha256(data).hexdigest(),region['sha256'])
            self.assertEqual(data,image[int(region['start'],16)-base:int(region['end'],16)-base])
        for path,digest in evidence['predecessor_sources'].items():
            self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(),digest)

    def test_declared_widths_and_immutable_inputs(self):
        palette=bytearray(768)
        for value in (-1,0,256,True):
            with self.assertRaises(ValueError):tabela_eclairage(palette,percentual=value,ciclos=[])
        for cycles in [[(2,1)],[(0,256)],[(True,1)],[(0,1)]*256]:
            with self.assertRaises(ValueError):tabela_eclairage(palette,percentual=60,ciclos=cycles)
        with self.assertRaises(ValueError):tabela_eclairage(palette[:-1],percentual=60,ciclos=[])
        frame=ler_cmp(bytes.fromhex(self.report['synthetic']['cmp_hex']))[0]
        for x,y in ((32768,0),(0,-32769),(True,0)):
            with self.assertRaises(ValueError):compor_eclairage(bytes(16),4,4,frame,x,y,bytes(range(256)))
        self.assertEqual(palette,bytearray(768))


if __name__=='__main__':unittest.main()
