"""Independent original index buffers, visibility and overlap composition."""
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, Catalogo
from extrair_evidencias import imagem_pe
from composicao import compor_unidade
from ordem_unidades import selecionar_ordem_unidades


def buffers(case):
    pool=bytearray(800*276);discovery=bytearray(65536);light=bytearray(65536)
    for item in case['records']:
        offset=item['index']*276
        if 'raw_hex' in item:pool[offset:offset+276]=bytes.fromhex(item['raw_hex'])
        else:
            pool[offset+2]=item['state'];struct.pack_into('<H',pool,offset+8,item['cell'])
            pool[offset+0xab]=item['priority']
    for cell,flag in case['discovery']:discovery[cell]=flag
    for cell,flag in case['light']:light[cell]=flag
    return bytes(pool),bytes(discovery),bytes(light)


class UnitOrderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((RAIZ/'validacao/x86-ordem-unidades.json').read_text())

    def test_327_original_selected_and_sorted_buffers(self):
        self.assertEqual(self.report['result'],'PASS');self.assertEqual(len(self.report['cases']),327)
        for capture in self.report['cases']:
            case=capture['case'];inputs=buffers(case)
            plan=selecionar_ordem_unidades(*inputs,origem=case['origin'],janela_celulas=case['window'])
            self.assertEqual(plan['selecionadas'],capture['selected']);self.assertEqual(plan['ordenadas'],capture['ordered'])
            self.assertTrue(capture['inputs_preserved']);self.assertEqual(capture['stop'],'0x416a6c')
            for data,key in zip(inputs,('pool_sha256','discovery_sha256','light_sha256')):
                self.assertEqual(hashlib.sha256(data).hexdigest(),capture[key])

    def test_full_800_pool_and_unstable_equal_keys(self):
        full=next(item for item in self.report['cases'] if item['case']['name']=='full_800_selected')
        self.assertEqual(len(full['selected']),800);self.assertEqual(len(full['ordered']),800)
        unstable=next(item for item in self.report['cases'] if item['case']['name']=='unstable_equal_keys')
        self.assertEqual(unstable['selected'],[0,1,2]);self.assertEqual(unstable['ordered'],[2,1,0])

    def test_every_state_and_flag_byte_against_original(self):
        state_cases=[item for item in self.report['cases'] if item['case']['name']=='state_byte']
        self.assertEqual(len(state_cases),256)
        for value,capture in enumerate(state_cases):
            self.assertEqual(capture['selected'],[799] if value else [])
        discovery=next(item for item in self.report['cases'] if item['case']['name']=='all_flag_bytes_discovery')
        light=next(item for item in self.report['cases'] if item['case']['name']=='all_flag_bytes_light')
        self.assertEqual(len(discovery['selected']),8);self.assertEqual(len(light['selected']),128)

    def test_eight_order_sensitive_original_indexed_buffers(self):
        catalog=Catalogo();table=bytes(json.loads((RAIZ/'validacao/x86-composicao.json').read_text())['tabelas_sombra'][1]['indices'])
        self.assertEqual(len(self.report['overlap']),8)
        for capture in self.report['overlap']:
            case=capture['case'];pool,discovery,light=buffers(case)
            plan=selecionar_ordem_unidades(pool,discovery,light,origem=case['origin'],janela_celulas=case['window'])
            out=bytes((i*17+23)%256 for i in range(128*128))
            for index in plan['ordenadas']:
                offset=index*276
                out,_=compor_unidade(catalog,out,128,128,tipo=pool[offset+1],estado_u8=2,
                    direcao=pool[offset+0x91],fase=pool[offset+0xa4],x=64,y=48,tabela=table,bolsa_u16=0)
            self.assertEqual(hashlib.sha256(out).hexdigest(),capture['sha256'])
            self.assertNotEqual(capture['sha256'],capture['stable_sha256'])
            self.assertGreater(capture['stable_diff_pixels'],0)

    def test_original_bytes_and_unchanged_predecessors(self):
        evidence=json.loads((RAIZ/'evidencias/ordem-unidades.json').read_text());base,image=imagem_pe()
        self.assertEqual(evidence['exe_sha256'],self.report['exe_sha256'])
        for region in evidence['regions']:
            data=bytes.fromhex(region['bytes_hex'])
            self.assertEqual(hashlib.sha256(data).hexdigest(),region['sha256'])
            self.assertEqual(data,image[int(region['start'],16)-base:int(region['end'],16)-base])
        for path,digest in evidence['predecessor_sources'].items():
            self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(),digest)

    def test_input_widths_and_read_only_buffers(self):
        pool=bytearray(800*276);discovery=bytearray(65536);light=bytearray(65536)
        for args in [(pool[:-1],discovery,light),(pool,discovery[:-1],light),(pool,discovery,light[:-1])]:
            with self.assertRaises(ValueError):selecionar_ordem_unidades(*args,origem=[0,0],janela_celulas=[1,1])
        for origin,window in [([-1,0],[1,1]),([256,0],[1,1]),([True,0],[1,1]),([0,0],[0,1]),([0,0],[257,1])]:
            with self.assertRaises(ValueError):selecionar_ordem_unidades(pool,discovery,light,origem=origin,janela_celulas=window)
        before=(bytes(pool),bytes(discovery),bytes(light))
        self.assertEqual(selecionar_ordem_unidades(pool,discovery,light,origem=[0,0],janela_celulas=[1,1])['ordenadas'],[])
        self.assertEqual((bytes(pool),bytes(discovery),bytes(light)),before)


if __name__=='__main__':unittest.main()
