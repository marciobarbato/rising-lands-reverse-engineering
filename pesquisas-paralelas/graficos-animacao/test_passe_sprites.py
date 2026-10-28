"""Complete original callback traces and captured indexed scene buffers."""
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, Catalogo, compor_indices
from extrair_evidencias import imagem_pe
from composicao import compor_sombra
from passe_sprites import planejar_passe_sprites, executar_passe_sprites


def buffers(case):
    units=bytearray(800*276);projectiles=bytearray(5600);objects=bytearray(65536)
    discovery=bytearray(65536);light=bytearray(65536)
    for item in case['units']:
        offset=item['index']*276
        if 'raw_hex' in item:units[offset:offset+276]=bytes.fromhex(item['raw_hex'])
        else:
            units[offset+2]=item['state'];units[offset+0xab]=item['priority'];struct.pack_into('<H',units,offset+8,item['cell'])
    for item in case['projectiles']:
        offset=item['index']*56;projectiles[offset]=item.get('type',0);projectiles[offset+2]=item['active']
        struct.pack_into('<HH',projectiles,offset+0xc,item['x'],item['y']);projectiles[offset+0x18]=item.get('phase',0)
    for cell,value in case['objects']:objects[cell]=value
    for cell,value in case['discovery']:discovery[cell]=value
    for cell,value in case['light']:light[cell]=value
    return bytes(units),bytes(projectiles),bytes(objects),bytes(discovery),bytes(light)


class SpritePassTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads((RAIZ/'validacao/x86-passe-sprites.json').read_text())

    def test_55_original_complete_callback_traces(self):
        self.assertEqual(self.report['result'],'PASS');self.assertEqual(len(self.report['cases']),55)
        for capture in self.report['cases']+self.report['pixels']:
            case=capture['case'];plan=planejar_passe_sprites(*buffers(case),origem=case['origin'],janela_celulas=case['window'])
            self.assertEqual(plan['eventos'],capture['calls'])
            self.assertEqual(capture['stop'],'0x3000000');self.assertEqual(capture['stack'],0x2008004)
            self.assertTrue(capture['inputs_preserved'])

    def test_different_row_margins_priority_passes_and_relative_projection(self):
        capture=next(item for item in self.report['cases'] if item['case']['name']=='priority_and_row_margins')
        units={event['indice']:event for event in capture['calls'] if event['funcao']=='AffEngin'}
        self.assertEqual(units[0]['passe'],1);self.assertEqual(units[1]['passe'],2);self.assertEqual(units[2]['passe'],2)
        self.assertEqual((units[3]['x'],units[3]['y'],units[3]['passe']),(0,256,1))
        self.assertNotIn(4,units);self.assertEqual(units[5]['passe'],2)
        self.assertEqual(units[6]['x'],160);self.assertNotIn(7,units)

    def test_callback_execution_matches_original_and_skips_literal_ret(self):
        capture=self.report['pixels'][0];case=capture['case']
        plan=planejar_passe_sprites(*buffers(case),origem=case['origin'],janela_celulas=case['window']);calls=[]
        count=executar_passe_sprites(plan,
            vegetacao=lambda x,y,cell:calls.append(('AffVeget',x,y,cell)),
            construcao=lambda x,y,cell:calls.append(('AffBatiments',x,y,cell)),
            unidade=lambda x,y,index:calls.append(('AffEngin',x,y,index)),
            projetil=lambda index:calls.append(('AffProjectile',index)))
        expected=[]
        for event in capture['calls']:
            if event['funcao']=='AffBatimentOmbre':continue
            if event['funcao']=='AffProjectile':expected.append((event['funcao'],event['indice']))
            else:expected.append((event['funcao'],event['x'],event['y'],event.get('indice',event.get('celula'))))
        self.assertEqual(calls,expected);self.assertEqual(count,len(expected))

    def test_callback_error_preserves_prior_effects_and_stops(self):
        case=self.report['cases'][0]['case'];plan=planejar_passe_sprites(*buffers(case),origem=case['origin'],janela_celulas=case['window'])
        called=[]
        def building(x,y,cell):
            called.append(cell)
            if len(called)==3:raise RuntimeError('declared consumer failure')
        with self.assertRaisesRegex(RuntimeError,'declared consumer failure'):
            executar_passe_sprites(plan,vegetacao=lambda *args:None,construcao=building,unidade=lambda *args:None,projetil=lambda *args:None)
        self.assertEqual(called,[0x1414,0x1415,0x1416])
        with self.assertRaises(ValueError):
            executar_passe_sprites(plan,vegetacao=None,construcao=building,unidade=lambda *args:None,projetil=lambda *args:None)
        self.assertEqual(len(called),3)

    def test_eight_original_indexed_scenes_replay_in_planned_order(self):
        catalog=Catalogo();table=bytes(json.loads((RAIZ/'validacao/x86-composicao.json').read_text())['tabelas_sombra'][1]['indices'])
        self.assertEqual(len(self.report['pixels']),8)
        for capture in self.report['pixels']:
            case=capture['case'];plan=planejar_passe_sprites(*buffers(case),origem=case['origin'],janela_celulas=case['window'])
            out=bytes((i*17+23)%256 for i in range(128*128));layers={}
            for layer in capture['layers']:layers.setdefault(layer['event'],[]).append(layer)
            for index,event in enumerate(plan['eventos']):
                self.assertEqual(event,capture['calls'][index])
                for layer in layers.get(index,[]):
                    frame=catalog.quadro(layer['id_motor'])
                    if layer['operation']=='shadow':out=compor_sombra(out,128,128,frame,layer['x'],layer['y'],table)
                    else:out=compor_indices(out,128,128,frame,layer['x'],layer['y'])
            self.assertEqual(hashlib.sha256(out).hexdigest(),capture['sha256'])
        image=(RAIZ/'artefatos/cena-passe-sprites.png').read_bytes()
        self.assertEqual(struct.unpack_from('>II',image,16),(128,128))

    def test_exact_original_caller_bytes_and_predecessors(self):
        evidence=json.loads((RAIZ/'evidencias/passe-sprites.json').read_text());base,image=imagem_pe()
        data=bytes.fromhex(evidence['bytes_hex'])
        self.assertEqual(hashlib.sha256(data).hexdigest(),evidence['sha256'])
        self.assertEqual(data,image[int(evidence['start'],16)-base:int(evidence['end'],16)-base])
        for path,digest in evidence['predecessor_sources'].items():
            self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(),digest)

    def test_input_domain_and_immutable_frame_snapshot(self):
        inputs=buffers(self.report['cases'][0]['case'])
        for origin,window,error in [([250,20],[1,1],NotImplementedError),([20,250],[1,1],NotImplementedError),
                ([0,0],[33,1],ValueError),([True,0],[1,1],ValueError),([-1,0],[1,1],ValueError)]:
            with self.assertRaises(error):planejar_passe_sprites(*inputs,origem=origin,janela_celulas=window)
        changed=list(inputs);changed[2]=b''
        with self.assertRaises(ValueError):planejar_passe_sprites(*changed,origem=[20,20],janela_celulas=[4,4])
        mutable=[bytearray(data) for data in inputs];before=[bytes(data) for data in mutable]
        planejar_passe_sprites(*mutable,origem=[20,20],janela_celulas=[4,4])
        self.assertEqual([bytes(data) for data in mutable],before)


if __name__=='__main__':unittest.main()
