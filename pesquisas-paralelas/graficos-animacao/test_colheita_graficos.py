"""Harvest and scroll domains compared with committed isolated calls and full native probe surfaces."""
import hashlib,json,struct,subprocess,unittest
from pathlib import Path
from validar_janelas_api18 import CapturaLimitada,AQUI
from validar_entrada_m3 import CatalogoRastreado,ArgumentosRasterM3,MemoriaEntradaM3
from validar_sondas_graficos_m3 import FronteiraTextoGravada
from render_quadro import renderizar_quadro
import efeitos_logicos_exibicao as logic
from test_efeitos_logicos_exibicao import estado

class ColheitaGraficos(unittest.TestCase):
    def test_complete_native_container_identity(self):
        paths=list((AQUI/'evidencias').glob('sonda-colheita-P[45]-*.json.xz'))
        self.assertEqual(len(paths),10);frames=0
        for path in paths:
            manifest=json.loads(Path(str(path)+'.manifest.json').read_text())
            self.assertEqual(manifest['status'],'complete')
            self.assertEqual(manifest['executable_sha256'],'6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),manifest['compressed_sha256'])
            self.assertLess(manifest['elapsed_seconds'],1200)
            frames+=manifest['frames'][1]-manifest['frames'][0]+1
        self.assertEqual(frames,6002)

    def test_every_new_origin_has_an_exact_native_case(self):
        report=json.loads((AQUI/'validacao/origens-colheita-final.json').read_text())
        provenance=json.loads((AQUI/'evidencias/origens-colheita-proveniencia.json').read_text())
        expected={tuple(case['origin']) for probe in provenance['cases'].values() for case in probe['new_origins']}
        self.assertEqual(len(expected),35)
        self.assertEqual(set(map(tuple,report['unique_origins'])),expected)
        self.assertEqual((report['cases'],report['mismatches']),(43,0))
        frozen=subprocess.check_output(['git','show','5fcb284:pesquisas-paralelas/graficos-animacao/efeitos_logicos_exibicao.py'],cwd=AQUI)
        self.assertEqual(hashlib.sha256(frozen).hexdigest(),report['graphics_provider_sha256'])
        self.assertEqual(hashlib.sha256((AQUI/'camadas_colheita_m3.json').read_bytes()).hexdigest(),report['layer_data_sha256'])
        self.assertEqual(hashlib.sha256((AQUI/'validar_origens_colheita.py').read_bytes()).hexdigest(),report['comparison_source_sha256'])
        self.assertTrue(all(r['returned'] and r['surface_equal'] and not r['additional_logic_writes'] and not r['crt_changes'] for r in report['rows']))
        for origin in expected:self.assertEqual(logic.desenhar_jogo(estado(origem=origin)).escritas,())

    def test_harvest_pixels_and_arguments_in_representative_native_states(self):
        catalog=CatalogoRastreado()
        for filename,frames in (
            ('sonda-colheita-P4-129-728.json.xz',(422,444,462,484,728)),
            ('sonda-colheita-P5-129-728.json.xz',(572,594,595,610,611,728)),
            ('sonda-colheita-P5-729-1328.json.xz',(760,761,1328)),
            ('sonda-colheita-P4-2529-3129.json.xz',(3129,)),
            ('sonda-colheita-P5-2529-3129.json.xz',(3129,))):
            cap=CapturaLimitada(AQUI/'evidencias'/filename)
            for row in cap.d['rows']:
                if row['frame'] not in frames:continue
                with self.subTest(capture=filename,frame=row['frame']):
                    boundary=FronteiraTextoGravada(cap,row)
                    with ArgumentosRasterM3(catalog) as raster:result=cap.render(row,catalog,texto=boundary)
                    self.assertIsNone(result.parada);self.assertEqual(result.pixels,cap.blob(row['after']))
                    self.assertEqual(raster.calls,row['blits']);self.assertFalse(boundary.pending)
                    if row['text_boundaries']:
                        strict=cap.render(row,catalog)
                        self.assertEqual(strict.parada['endereco'],'0x00459454')
                        self.assertEqual(strict.pixels,cap.blob(row['text_boundaries'][0]['surface_before']))

    def test_frozen_api19_chained_surface_report_and_sources(self):
        report=json.loads((AQUI/'validacao/colheita-graficos-final.json').read_text())
        expected={'K1':501,'P4':3001,'P5':3001}
        self.assertEqual({w['probe']:w['drawn_total'] for w in report['windows']},expected)
        for window in report['windows']:
            self.assertEqual(window['equal'],expected[window['probe']]);self.assertIsNone(window['first_stop'])
            self.assertTrue(all(row['equal'] and not row['logic_stop'] for row in window['rows']))
        for name,digest in report['sources_sha256'].items():
            frozen=subprocess.check_output(['git','show','5fcb284:pesquisas-paralelas/graficos-animacao/'+name],cwd=AQUI)
            self.assertEqual(hashlib.sha256(frozen).hexdigest(),digest,name)

    def test_fresh_128_hud_hashes_preserve_all_prior_versions(self):
        new=json.loads((AQUI/'evidencias/verificacao-cadeia-m22-v2-api19-128.json').read_text())
        self.assertEqual((new['frames'],new['render_api_version'],new['chained_equals_recorded_count']),(128,[1,9],128))
        self.assertIsNone(new['first_stop']);self.assertIsNone(new['first_chained_difference_frame'])
        self.assertTrue(all(row['chain_cache_equals_native_entry_cache'] and row['chain_input_equals_native_previous']
                            and row['over_native_previous']['pixels']==0 for row in new['rows']))
        for version in ('14','15','17','18'):
            old=json.loads((AQUI/f'evidencias/verificacao-cadeia-m22-v2-api{version}-128.json').read_text())
            self.assertEqual([r['chained']['sha256'] for r in new['rows']],[r['chained']['sha256'] for r in old['rows']],version)

    def test_unproved_origins_restoreall_and_builder_tasks_stay_stops(self):
        with self.assertRaises(logic.DependenciaExibicao):logic.desenhar_jogo(estado(origem=(5,5)))
        with self.assertRaises(logic.DependenciaExibicao):logic.restaurar_tudo(estado(origem=(1,0)))
        cap=CapturaLimitada(AQUI/'evidencias/sonda-colheita-P5-129-728.json.xz')
        row=next(r for r in cap.d['rows'] if r['frame']==594);memory=cap.memory(row)
        address=memory.u32(0x4e19a0)+12*276+0x89
        blocks=[(a,bytearray(data)) for a,data in memory.blocks]
        for a,data in blocks:
            if a<=address<a+len(data):data[address-a]=12;break
        result=renderizar_quadro(MemoriaEntradaM3(blocks),superficie_anterior=cap.blob(row['before']),cache=cap.cache_entry(row),
            catalogo=CatalogoRastreado(),habitado=lambda i:True,hud=True)
        self.assertEqual(result.parada['endereco'],'0x00414a8a')

if __name__=='__main__':unittest.main()
