"""Scripted M3 surfaces and every CAVE health step against the intact executable's frozen outputs."""
import contextlib,hashlib,io,json,struct,unittest
from pathlib import Path
from graficos import Catalogo
from validar_sondas_graficos_m3 import CapturaSondaGrafica,FronteiraTextoGravada,compare_matrix
from validar_entrada_m3 import ArgumentosRasterM3,CatalogoRastreado,MemoriaEntradaM3

AQUI=Path(__file__).resolve().parent

class CaveScriptadaM3(unittest.TestCase):
    def test_full_native_facade_matrix(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result=compare_matrix(AQUI/'evidencias/matriz-cave-toda-vida-api17.json.xz')
        self.assertEqual((result['cases'],result['mismatches']),(600,0))

    def test_scripted_surfaces_arguments_and_text_dependency(self):
        catalog=CatalogoRastreado()
        for probe,frames in (('P1',(129,131,133,169,170,171,250,400,629)),
                             ('P2',(129,133,218,219,220,300,400,600,729)),
                             ('P3',(129,133,140,141,142,143,144,152,153,154,155,200,220,221,222,245,246,260,280,300))):
            cap=CapturaSondaGrafica(AQUI/f'evidencias/sonda-render-{probe}-api17.json.xz')
            self.assertEqual(cap.d['executable_sha256'],'6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
            self.assertTrue(all(r['surface_equal'] and r['state_equal'] for r in cap.d['checks']))
            self.assertTrue(all(r['after']==r['probe_surface_sha256'] for r in cap.d['rows']))
            for row in cap.d['rows']:
                if row['frame'] not in frames:continue
                with self.subTest(probe=probe,frame=row['frame']):
                    boundary=FronteiraTextoGravada(cap,row)
                    with ArgumentosRasterM3(catalog) as raster:result=cap.render(row,catalog,texto=boundary)
                    self.assertIsNone(result.parada)
                    self.assertEqual(result.pixels,cap.blob(row['after']))
                    self.assertEqual(raster.calls,row['blits'])
                    self.assertFalse(boundary.pending)
                    if row['text_boundaries']:
                        strict=cap.render(row,catalog)
                        self.assertEqual(strict.parada['endereco'],'0x00459454')
                        self.assertEqual(strict.pixels,cap.blob(row['text_boundaries'][0]['surface_before']))

    def test_boundary_adapter_rejects_unattested_pixels_and_arguments(self):
        cap=CapturaSondaGrafica(AQUI/'evidencias/sonda-render-P3-api17.json.xz');row=next(r for r in cap.d['rows'] if r['text_boundaries'])
        native=row['text_boundaries'][0];regs=native['registers']
        request=dict(text=bytes.fromhex(native['text_hex']),x=int(regs['EAX'],16),y=int(regs['EDX'],16),
            right=int(regs['EBX'],16),bottom=int(regs['ECX'],16),font=1,flags=(0,0))
        pixels=cap.blob(native['surface_before'])
        self.assertEqual(FronteiraTextoGravada(cap,row)(request,pixels),pixels)
        with self.assertRaises(AssertionError):FronteiraTextoGravada(cap,row)(request,bytes(len(pixels)))
        with self.assertRaises(AssertionError):FronteiraTextoGravada(cap,row)({**request,'text':b'UNKNOWN'},pixels)

    def test_current_full_comparison_reports(self):
        for path,expected in (('sondas-api17-final.json',(('P1',501),('P2',601),('P3',172))),):
            report=json.loads((AQUI/'validacao'/path).read_text())
            self.assertTrue(report['probe_text_boundary_contract'])
            for source,digest in report['sources_sha256'].items():
                self.assertEqual(hashlib.sha256((AQUI/source).read_bytes()).hexdigest(),digest,source)
            self.assertEqual([(r['probe'],r['frames']) for r in report['probes']],list(expected))
            for probe in report['probes']:
                self.assertIsNone(probe['first_difference'])
                self.assertEqual(probe['surface_equal'],probe['frames'])
                self.assertEqual(probe['chained_equal'],probe['frames'])
                self.assertTrue(all(r['chained']['entry_cache_equal'] and r['chained']['entry_saved_background_equal'] for r in probe['rows']))

    def test_default_renderer_reports_first_glyph_dependency(self):
        report=json.loads((AQUI/'validacao/prefixos-sondas-api17.json').read_text())
        self.assertEqual([(r['probe'],r['chained_equal_prefix'],r['first_stop_frame']) for r in report['probes']],
                         [('P1',41,170),('P2',90,219),('P3',12,141)])
        self.assertTrue(all(r['native_partial_surface_equal'] and r['native_partial_arguments_equal'] for r in report['probes']))

    def test_fresh_128_hud_regression(self):
        report=json.loads((AQUI/'evidencias/verificacao-cadeia-m22-v2-api17-128.json').read_text())
        self.assertEqual((report['frames'],report['render_api_version'],report['hud'],report['chained_equals_recorded_count']),
                         (128,[1,7],True,128))
        self.assertIsNone(report['first_stop']);self.assertIsNone(report['first_chained_difference_frame'])

    def test_uncaptured_cave_construction_variant_stops(self):
        from render_quadro import renderizar_quadro
        cap=CapturaSondaGrafica(AQUI/'evidencias/matriz-cave-toda-vida-api17.json.xz')
        row=next(r for r in cap.d['rows'] if r['name']=='type3_mode0_state100')
        m=cap.memory(row);blocks=[(a,bytearray(d)) for a,d in m.blocks];address=0x49a0c8+276+0x76
        for a,d in blocks:
            if a<=address<a+len(d):d[address-a]=1;break
        result=renderizar_quadro(MemoriaEntradaM3(blocks),superficie_anterior=cap.blob(row['before']),cache=cap.cache_entry(row),
            catalogo=Catalogo(),habitado=lambda i:False,hud=True)
        self.assertEqual(result.parada['endereco'],'0x004099a6')

if __name__=='__main__':unittest.main()
