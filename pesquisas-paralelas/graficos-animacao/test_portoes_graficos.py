"""Regressions against separately executed original x86 gate captures."""
import hashlib
import json
import unittest
from graficos import RAIZ, Catalogo, Quadro, localizar
from extrair_evidencias import imagem_pe
from portoes_graficos import consultar_portao, compor_portao


def fixture(**changes):
    args=dict(contador_u8=0,orientacao_u16=0,valor_0a_u16=35,jogador=0,camera=0,
        modo_u8=5,visibilidade_u8=0,descoberta_u8=0,x=128,y=128,janela_celulas=[10,10])
    args.update(changes)
    return args


class GateGraphicsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=Catalogo()
        cls.report=json.loads((RAIZ/'validacao/x86-portoes-graficos.json').read_text())

    def test_original_bytes_and_preserved_predecessors(self):
        evidence=json.loads((RAIZ/'evidencias/portoes-graficos.json').read_text())
        self.assertEqual(evidence['exe_sha256'],self.report['exe_sha256'])
        self.assertEqual(evidence['exe_sha256'],'6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
        base,image=imagem_pe()
        for region in evidence['regions']:
            data=bytes.fromhex(region['bytes_hex'])
            self.assertEqual(len(data),int(region['end'],16)-int(region['start'],16))
            self.assertEqual(hashlib.sha256(data).hexdigest(),region['sha256'])
            self.assertEqual(data,image[int(region['start'],16)-base:int(region['end'],16)-base])
        for name,digest in evidence['predecessor_sources'].items():
            self.assertEqual(hashlib.sha256((RAIZ/name).read_bytes()).hexdigest(),digest)

    def test_1700_original_calls_and_temporary_clip_order(self):
        self.assertEqual(self.report['result'],'PASS')
        self.assertEqual(len(self.report['captures']),1700)
        for capture in self.report['captures']:
            plan=consultar_portao(**capture['args'])
            events=capture['events']
            self.assertTrue(capture['record_preserved'])
            if not plan['camadas']:
                self.assertEqual(events,[])
                self.assertEqual(capture['stop'],'0x40f491')
                continue
            layer=plan['camadas'][0]
            self.assertEqual([event['operation'] for event in events],['save_clip','set_clip','copy'])
            self.assertEqual(events[0]['clip'],[11,13,300,299])
            self.assertEqual(events[1]['clip'],plan['recorte'])
            self.assertEqual(events[2],dict(operation='copy',id_motor=layer['id_motor'],
                x=layer['x'],y=layer['y'],clip=plan['recorte'],clipping=1))
            self.assertEqual(capture['stop'],'0x40f342')

    def test_192_original_indexed_buffers(self):
        self.assertEqual(len(self.report['pixels']),192)
        for capture in self.report['pixels']:
            args=capture['args'];width,height=(value*32 for value in args['janela_celulas'])
            background=bytes((i*17+23)%256 for i in range(width*height))
            out=compor_portao(self.catalog,background,width,height,consultar_portao(**args))
            self.assertEqual(hashlib.sha256(out).hexdigest(),capture['sha256'])

    def test_64_bank_associations_and_opacity(self):
        associations=json.loads((RAIZ/'artefatos/associacoes-portoes.json').read_text())
        self.assertEqual(len(associations),64)
        self.assertEqual([item['id_motor'] for item in associations],list(range(7576,7640)))
        for item in associations:
            for key,value in localizar(item['id_motor']).items():
                self.assertEqual(item[key],value)
            self.assertEqual(item['arquivo_cmp'],'BUILDING.CMP')
            frame=self.catalog.quadro(item['id_motor'])
            self.assertEqual(hashlib.sha256(frame.pixels).hexdigest(),item['sha256_pixels'])
            self.assertEqual(hashlib.sha256(frame.opacidade).hexdigest(),item['sha256_opacity'])
        self.assertEqual((associations[0]['indice_local'],associations[-1]['indice_local']),(547,610))

    def test_raw_counter_crosses_strip_but_public_api_refuses(self):
        self.assertEqual(len(self.report['raw_counter_captures']),896)
        for capture in self.report['raw_counter_captures']:
            args=capture['args']
            with self.assertRaises(NotImplementedError):consultar_portao(**args)
            self.assertEqual(capture['events'][-1]['id_motor'],
                (7608 if args['orientacao_u16'] else 7576)+args['contador_u8'])

    def test_owner_visibility_and_mode3_precede_discovery(self):
        args=fixture(jogador=1,camera=0,descoberta_u8=16)
        self.assertEqual(consultar_portao(**args)['motivo'],'hidden_record')
        args.update(modo_u8=3)
        self.assertEqual(consultar_portao(**args)['motivo'],'undiscovered_cell')
        args.update(descoberta_u8=15)
        self.assertEqual(consultar_portao(**args)['motivo'],'draw')

    def test_signed_anchors_and_low_word_state(self):
        horizontal=consultar_portao(**fixture(contador_u8=31))
        self.assertEqual((horizontal['camadas'][0]['id_motor'],horizontal['recorte']),
            (7607,[128,128,319,319]))
        vertical=consultar_portao(**fixture(orientacao_u16=256,x=32767,y=32767))
        self.assertEqual((vertical['camadas'][0]['x'],vertical['camadas'][0]['y']),(-32764,-32765))
        self.assertEqual(consultar_portao(**fixture(valor_0a_u16=65535))['estado_u16'],56170)

    def test_no_palette_shadow_or_literal_zero_loss(self):
        class Synthetic:
            def quadro(self,ident):
                return Quadro(4,1,bytes([160,160,0,167]),bytes([0,255,255,255]),0,b'')
        plan=consultar_portao(**fixture(x=0,y=0,janela_celulas=[1,1]))
        background=bytes([82])*1024
        out=compor_portao(Synthetic(),background,32,32,plan)
        self.assertEqual(out[:4],bytes([82,160,0,167]))
        self.assertEqual(background,bytes([82])*1024)

    def test_required_runtime_fields_and_failures(self):
        with self.assertRaises(TypeError):consultar_portao(contador_u8=0,orientacao_u16=0)
        for key,value in [('contador_u8',-1),('contador_u8',256),('contador_u8',True),
                ('orientacao_u16',65536),('valor_0a_u16',-1),('camera',4),('jogador',5),
                ('modo_u8',256),('x',32768),('y',-32769),('janela_celulas',[0,10])]:
            with self.assertRaises(ValueError):consultar_portao(**fixture(**{key:value}))
        plan=consultar_portao(**fixture())
        with self.assertRaises(ValueError):compor_portao(self.catalog,b'',320,320,plan)
        with self.assertRaises(ValueError):compor_portao(self.catalog,bytes(64*64),64,64,plan)
        for capture in self.report['missing_occupancy']:
            self.assertEqual(capture['events'],[dict(operation='save_clip',clip=[11,13,300,299])])
            self.assertEqual(capture['stop'],'0x40f491')


if __name__=='__main__':
    unittest.main()
