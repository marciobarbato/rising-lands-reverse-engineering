"""AffBatiments logic-effect domain from corrected native writer/reader evidence."""
import hashlib,json,lzma,unittest
from pathlib import Path
from validar_janelas_api18 import CapturaLimitada,AQUI
from validar_efeitos_cave_sondas import EntradaEfeitos
from efeitos_logicos_exibicao import desenhar_jogo,restaurar_tudo,DependenciaExibicao

class CaveLogicaM3(unittest.TestCase):
    def test_corrected_native_writer_reader_passes(self):
        states=set();bytes_written=set()
        for name in ('criacao-v2','completa','p6','p7','s1'):
            path=AQUI/f'evidencias/cave-escritas-{name}.json.xz';d=json.loads(lzma.decompress(path.read_bytes()))
            self.assertIn('0x3400000',d['watched_regions']);self.assertTrue(d['passes_equal'])
            self.assertEqual(d['passes'][0]['checks'],d['passes'][1]['checks'])
            self.assertEqual(d['passes'][0]['observation']['changing_bytes'],d['passes'][1]['observation']['changing_bytes'])
            self.assertFalse(d['passes'][1]['observation']['outside_display_readers'])
            self.assertEqual(d['executable_sha256'],'6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
            bytes_written.update(d['passes'][0]['observation']['changing_bytes'])
            states.update((r['kind'],r['state'],r['owner']) for r in d['passes'][0]['observation']['structure_calls'])
        self.assertEqual(bytes_written,{'0x49a01c','0x49a01d','0x49a01e','0x49a01f','0x49a020','0x49a021'})
        self.assertTrue({(2,4,0),(2,5,0),(3,2,200),(3,5,200),(3,5,0)}<=states)

    def test_current_structure_domain_report_and_origins(self):
        d=json.loads((AQUI/'validacao/cave-dominio-atual.json').read_text())
        self.assertEqual(d['probes'],{'P3':3001,'P6':2272,'P7':3572});self.assertEqual(d['mismatches'],0)
        self.assertEqual([(r['probe'],r['frame'],r['origin'],r['passed']) for r in d['origins']],
            [('K1',141,[1,0],True),('P4',422,[10,16],True),('P5',572,[31,0],True)])
        self.assertEqual(hashlib.sha256((AQUI/'efeitos_logicos_exibicao.py').read_bytes()).hexdigest(),d['provider_sha256'])

    def test_unproved_cave_domain_stays_stopped(self):
        cap=CapturaLimitada(AQUI/'evidencias/janela-P6-2001-2400-api18.json.xz');row=next(r for r in cap.d['rows'] if r['frame']==2179)
        good=EntradaEfeitos(cap,row);self.assertEqual(desenhar_jogo(good).escritas,())
        for offset,value in ((5,b'\3'),(4,b'\1'),(6,b'\1\0')):
            memory=EntradaEfeitos(cap,row);dg=bytearray(memory.dg);address=0x49a0c8+276+offset;dg[address-0x494000:address-0x494000+len(value)]=value;memory.dg=bytes(dg)
            with self.assertRaises(DependenciaExibicao):desenhar_jogo(memory)
        with self.assertRaises(DependenciaExibicao):restaurar_tudo(good)

    def test_p4_484_original_text_boundary_has_no_glyph_execution(self):
        d=json.loads((AQUI/'evidencias/p4-texto-484-auditoria.json').read_text())
        self.assertEqual(len(d['checks']),356)
        self.assertTrue(all(r['surface_equal'] and r['state_equal'] for r in d['checks']))
        self.assertEqual([r['routine'] for r in d['calls']],['AffText','TextGetMessage'])
        self.assertEqual(d['calls'][0]['entry_eax'],d['calls'][0]['return_eax'])
        self.assertEqual(d['calls'][1]['return_eax'],'0x0')
        self.assertEqual(d['body_instructions'],[])
        self.assertTrue(all(r['surface_before']==r['surface_after'] for r in d['calls']))
        self.assertFalse(any(r['address']=='0x5099a4' for r in d['pointer_overlap_reads']))

    def test_original_complete_projectile15_cycle_and_guard(self):
        path=AQUI/'evidencias/projetil15-escritas-ciclo-p3.json.xz';d=json.loads(lzma.decompress(path.read_bytes()))
        self.assertTrue(d['passes_equal']);self.assertEqual(d['passes'][0]['checks'],d['passes'][1]['checks'])
        for p in d['passes']:
            self.assertEqual(p['observation']['changing_bytes'],{})
            self.assertEqual(p['observation']['outside_display_readers'],[])
            self.assertEqual([(r['index'],r['kind'],r['state'],r['phase']) for r in p['observation']['projectile_calls']],
                [(0,15,1,phase) for phase in range(16)])
        cap=CapturaLimitada(AQUI/'evidencias/sonda-render-P3-api17.json.xz');row=next(r for r in cap.d['rows'] if r['frame']==245)
        good=EntradaEfeitos(cap,row);self.assertEqual(desenhar_jogo(good).escritas,())
        for offset,value in ((0x18,16),(2,2)):
            m=EntradaEfeitos(cap,row);raw=bytearray(m.proj);raw[offset]=value;m.proj=bytes(raw)
            with self.assertRaises(DependenciaExibicao):desenhar_jogo(m)

    def test_fresh_native_128_hud_retains_every_prior_hash(self):
        d=json.loads((AQUI/'validacao/regressao-hud-cadeia-atual-128.json').read_text())
        self.assertEqual((d['frames'],d['chained_equals_recorded_count']),(128,128))
        self.assertIsNone(d['first_stop']);self.assertIsNone(d['first_chained_difference_frame'])
        hashes=[r['chained']['sha256'] for r in d['rows']]
        for name in ('verificacao-cadeia-m22-v2-api14-128.json','verificacao-cadeia-m22-v2-api15-128.json',
                     'verificacao-cadeia-m22-v2-api17-128.json','verificacao-cadeia-m22-v2-api18-128.json',
                     'verificacao-cadeia-m22-v2-api19-128.json'):
            old=json.loads((AQUI/'evidencias'/name).read_text())
            self.assertEqual(hashes,[r['chained']['sha256'] for r in old['rows']],name)
