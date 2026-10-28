"""Independent saved projectile display buffers and exact indexed replays."""
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, Catalogo, compor_indices
from extrair_evidencias import imagem_pe
from ordem_projeteis import consultar_celula_projetil, selecionar_ordem_projeteis


def buffers(case):
    pool=bytearray(5600);discovery=bytearray(65536);light=bytearray(65536)
    for item in case['records']:
        offset=item['index']*56;pool[offset]=item.get('type',0);pool[offset+2]=item['active']
        struct.pack_into('<HH',pool,offset+0xc,item['x'],item['y']);pool[offset+0x18]=item.get('phase',0)
        struct.pack_into('<HH',pool,offset+0x14,0xabcd,0x1234)
    for cell,flag in case['discovery']:discovery[cell]=flag
    for cell,flag in case['light']:light[cell]=flag
    return bytes(pool),bytes(discovery),bytes(light),bytes(range(200))


class ProjectileOrderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads((RAIZ/'validacao/x86-ordem-projeteis.json').read_text())

    def test_581_original_complete_index_buffers_and_untouched_tail(self):
        self.assertEqual(self.report['result'],'PASS');self.assertEqual(len(self.report['cases']),581)
        for capture in self.report['cases']:
            case=capture['case'];inputs=buffers(case)
            plan=selecionar_ordem_projeteis(*inputs,origem=case['origin'],janela_celulas=case['window'])
            self.assertEqual(plan['selecionadas'],capture['selected']);self.assertEqual(plan['ordenadas'],capture['ordered'])
            self.assertEqual(plan['indices_saida'],bytes.fromhex(capture['output_hex']))
            self.assertEqual(plan['indices_saida'][plan['quantidade']*2:],inputs[3][plan['quantidade']*2:])
            self.assertTrue(capture['pool_preserved']);self.assertEqual(capture['stop'],'0x3000000')

    def test_98_original_cell_queries_unsigned_words_and_full_key(self):
        self.assertEqual(len(self.report['cell_queries']),98)
        for capture in self.report['cell_queries']:
            pool=bytearray(5600);struct.pack_into('<HH',pool,capture['index']*56+0xc,capture['x'],capture['y'])
            cell=consultar_celula_projetil(pool,capture['index'])
            self.assertEqual(cell['chave_u32'],capture['value']);self.assertEqual(cell['celula_u16'],capture['value']&65535)
        high=next(item for item in self.report['cell_queries'] if item['x']==65535 and item['y']==65535)
        self.assertEqual(high['value'],526079)

    def test_last_equal_candidate_low_word_sort_and_full_pool(self):
        equal=next(item for item in self.report['cases'] if item['case']['name']=='last_equal')
        self.assertEqual(equal['ordered'],[3,0,1,2])
        wrapped=next(item for item in self.report['cases'] if item['case']['name']=='low_word_wrap')
        self.assertEqual(wrapped['ordered'],[1,0,2])
        full=next(item for item in self.report['cases'] if item['case']['name']=='full100')
        self.assertEqual(len(full['ordered']),100)

    def test_activity_and_both_mask31_predicates_against_original(self):
        active=[item for item in self.report['cases'] if item['case']['name']=='active_byte']
        self.assertEqual(len(active),256)
        for value,capture in enumerate(active):self.assertEqual(capture['selected'],[99] if value else [])
        flags=[item for item in self.report['cases'] if item['case']['name']=='flag_bytes']
        self.assertEqual(len(flags),256)
        self.assertEqual(flags[1]['selected'],[]);self.assertEqual(flags[16]['selected'],[])
        self.assertEqual(flags[32]['selected'],[0,99])

    def test_eight_indexed_original_projectile_replays(self):
        catalog=Catalogo();self.assertEqual(len(self.report['overlap']),8)
        for capture in self.report['overlap']:
            case=capture['case'];plan=selecionar_ordem_projeteis(*buffers(case),origem=case['origin'],janela_celulas=case['window'])
            draws={event['index']:event for event in capture['draws']}
            out=bytes((i*17+23)%256 for i in range(128*128))
            for index in plan['ordenadas']:
                event=draws[index]
                out=compor_indices(out,128,128,catalog.quadro(event['id_motor']),event['x'],event['y'])
            self.assertEqual(hashlib.sha256(out).hexdigest(),capture['sha256'])

    def test_original_byte_intervals_and_predecessors(self):
        evidence=json.loads((RAIZ/'evidencias/ordem-projeteis.json').read_text());base,image=imagem_pe()
        self.assertEqual(evidence['exe_sha256'],self.report['exe_sha256'])
        for region in evidence['regions']:
            data=bytes.fromhex(region['bytes_hex'])
            self.assertEqual(hashlib.sha256(data).hexdigest(),region['sha256'])
            self.assertEqual(data,image[int(region['start'],16)-base:int(region['end'],16)-base])
        for path,digest in evidence['predecessor_sources'].items():
            self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(),digest)

    def test_declared_input_widths_and_preserved_inputs(self):
        pool=bytearray(5600);maps=bytearray(65536);output=bytearray(range(200))
        for index in (-1,100,65535,True):
            with self.assertRaises(ValueError):consultar_celula_projetil(pool,index)
        for data in (b'',bytes(5599)):
            with self.assertRaises(ValueError):consultar_celula_projetil(data,0)
        for args in ((pool,maps[:-1],maps,output),(pool,maps,maps,output[:-1])):
            with self.assertRaises(ValueError):selecionar_ordem_projeteis(*args,origem=[0,0],janela_celulas=[1,1])
        before=(bytes(pool),bytes(maps),bytes(output))
        plan=selecionar_ordem_projeteis(pool,maps,maps,output,origem=[0,0],janela_celulas=[1,1])
        self.assertEqual(plan['quantidade'],0);self.assertEqual(plan['indices_saida'],bytes(output))
        self.assertEqual((bytes(pool),bytes(maps),bytes(output)),before)


if __name__=='__main__':unittest.main()
