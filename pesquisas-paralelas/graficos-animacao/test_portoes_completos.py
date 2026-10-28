"""Original full-return gate captures, independently of the pure renderer."""
import hashlib
import json
import unittest
from extrair_evidencias import RAIZ, imagem_pe
from graficos import Catalogo
from portoes_completos import consultar_portao_completo, compor_portao_completo


def fixture(**changes):
    args=dict(contador_u8=0,orientacao_u16=0,valor_0a_u16=35,jogador=0,camera=0,
        modo_u8=5,visibilidade_u8=0,descoberta_u8=0,x=128,y=128,
        janela_celulas=[10,10],terreno_u16=0,recorte_entrada=[11,13,300,299])
    args.update(changes)
    return args


class FullGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((RAIZ/'validacao/x86-portoes-completos.json').read_text())
        cls.catalog=Catalogo()

    def test_768_original_calls_restore_clip_and_return(self):
        self.assertEqual(self.report['result'],'PASS')
        self.assertEqual(len(self.report['captures']),768)
        for capture in self.report['captures']:
            plan=consultar_portao_completo(**capture['args'])
            self.assertEqual(capture['stop'],'0x3000000')
            self.assertEqual(capture['stack'],0x2008004)
            self.assertTrue(capture['record_preserved'])
            self.assertEqual(capture['clip'],plan['recorte_saida'])
            operations=[event['operation'] for event in capture['events']]
            if plan['camadas']:
                self.assertEqual(operations[:6],['save_clip','set_clip','copy','workshop_guard','restore_clip','habitation_query'])
                self.assertEqual(capture['events'][4]['restored_clip'],capture['args']['recorte_entrada'])
            else:self.assertEqual(operations,[])

    def test_original_selection_and_gauge_guards(self):
        frame_count=gauge_count=0
        for capture in self.report['captures']:
            args=capture['args'];plan=consultar_portao_completo(**args)
            operations=[event['operation'] for event in capture['events']]
            eligible=bool(plan['camadas']) and capture['habitado'] and args['modo_u8']!=3 and args['jogador']==args['camera']
            frame=eligible and capture['selected']
            gauge=eligible and (capture['selected'] or capture['hovered'])
            self.assertEqual(operations.count('selection_guard'),int(frame))
            self.assertEqual(operations.count('gauge_guard'),int(gauge))
            frame_count+=frame;gauge_count+=gauge
        self.assertGreater(frame_count,0);self.assertGreater(gauge_count,0)

    def test_112_original_indexed_buffers_and_inverted_incoming_clip(self):
        self.assertEqual(len(self.report['pixels']),112)
        background=bytes((i*17+23)%256 for i in range(320*320))
        for capture in self.report['pixels']:
            plan=consultar_portao_completo(**capture['args'])
            out,clip=compor_portao_completo(self.catalog,background,320,320,plan)
            self.assertEqual(hashlib.sha256(out).hexdigest(),capture['sha256'])
            self.assertEqual(list(clip),capture['clip'])
        # An inverted caller clip is restored verbatim, but the gate's own
        # temporary rectangle still allows its indexed facade to draw.
        sample=next(item for item in self.report['pixels'] if item['args']['recorte_entrada']==[319,319,0,0]
            and item['args']['x']==128 and item['args']['valor_0a_u16']==35)
        self.assertNotEqual(sample['sha256'],hashlib.sha256(background).hexdigest())

    def test_original_byte_intervals_and_immutable_previous_stage(self):
        evidence=json.loads((RAIZ/'evidencias/portoes-completos.json').read_text())
        base,image=imagem_pe()
        self.assertEqual(evidence['exe_sha256'],self.report['exe_sha256'])
        for region in evidence['regions']:
            data=bytes.fromhex(region['bytes_hex'])
            self.assertEqual(hashlib.sha256(data).hexdigest(),region['sha256'])
            self.assertEqual(data,image[int(region['start'],16)-base:int(region['end'],16)-base])
        for path,digest in evidence['predecessor_sources'].items():
            self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(),digest)

    def test_hidden_plan_preserves_background_and_clip_without_catalog(self):
        class NoCatalog:
            def quadro(self,_):raise AssertionError('Hidden gate queried a sprite')
        plan=consultar_portao_completo(**fixture(descoberta_u8=16))
        before=bytearray([82])*1024
        out,clip=compor_portao_completo(NoCatalog(),before,32,32,plan)
        self.assertEqual(out,bytes(before));self.assertEqual(clip,(11,13,300,299))

    def test_declared_domain_and_required_state(self):
        for value in (0x356,):
            with self.assertRaises(NotImplementedError):consultar_portao_completo(**fixture(terreno_u16=value))
        for changes in [dict(terreno_u16=-1),dict(terreno_u16=65536),dict(terreno_u16=True),
                dict(recorte_entrada=[1,2,3]),dict(recorte_entrada=[0,0,65536,0]),dict(recorte_entrada=[False,0,0,0])]:
            with self.assertRaises(ValueError):consultar_portao_completo(**fixture(**changes))
        with self.assertRaises(TypeError):consultar_portao_completo(terreno_u16=0,recorte_entrada=[0]*4)


if __name__=='__main__':unittest.main()
