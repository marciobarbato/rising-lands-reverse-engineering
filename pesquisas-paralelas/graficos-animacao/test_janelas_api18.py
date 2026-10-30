"""API 1.8 chained windows and data-driven layers against committed intact-executable recordings."""
import contextlib,hashlib,io,json,struct,subprocess,unittest
from pathlib import Path
from render_quadro import renderizar_quadro
from validar_entrada_m3 import ArgumentosRasterM3,CatalogoRastreado,MemoriaEntradaM3
from validar_janelas_api18 import CapturaLimitada,AQUI
from validar_sondas_graficos_m3 import FronteiraTextoGravada
from validar_camadas_api18 import validar as comparar_camadas

class SemPonteiroTexto(MemoriaEntradaM3):
    def ler_mundo(self,address,size):
        if address<=0x5099a4<address+size:raise AssertionError('Renderer read the unavailable TextGetMessage pointer')
        return super().ler_mundo(address,size)

class JanelasAPI18(unittest.TestCase):
    def test_native_capture_container_identity(self):
        paths=list((AQUI/'evidencias').glob('janela-*-api18.json.xz'))
        self.assertEqual(len(paths),9)
        frames=0
        for path in paths:
            manifest=json.loads(Path(str(path)+'.manifest.json').read_text())
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),manifest['compressed_sha256'])
            self.assertEqual(manifest['executable_sha256'],'6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
            self.assertEqual(manifest['status'],'complete')
            self.assertLess(manifest['elapsed_seconds'],1200)
            frames+=manifest['frames'][1]-manifest['frames'][0]+1
        self.assertEqual(frames,5030)
        boundary=json.loads((AQUI/'evidencias/fronteira-texto-api18.json').read_text())
        self.assertEqual(boundary['source_sha256'],hashlib.sha256((AQUI/'capturar_fronteira_texto18.py').read_bytes()).hexdigest())
        self.assertTrue(boundary['native_surface_equal'] and boundary['native_whole_state_equal'])
        self.assertFalse(boundary['body_instructions'])
        self.assertTrue(boundary['calls'])
        self.assertTrue(all(call['returned_eax']=='0x0' for call in boundary['calls']))
        self.assertTrue(all(read['address']=='0x5099a6' and read['eip']=='0x417ce2' for read in boundary['pointer_overlap_reads']))

    def test_all_515_inhabited_layer_cases(self):
        with contextlib.redirect_stdout(io.StringIO()):result=comparar_camadas()
        self.assertEqual((result['cases'],result['mismatches']),(515,0))

    def test_representative_new_phases_and_no_message_pointer_read(self):
        catalog=CatalogoRastreado()
        samples=(('janela-P3-2551-3129-api18.json.xz',(2936,3129)),
                 ('janela-P6-2001-2400-api18.json.xz',(2016,2032,2064,2074,2179,2400)),
                 ('janela-P7-2401-2850-api18.json.xz',(2414,2784,2803,2850)),
                 ('janela-P7-2851-3275-api18.json.xz',(3211,3229,3275)),
                 ('janela-P7-3276-3700-api18.json.xz',(3555,3604,3605,3606,3700)),
                 ('janela-K1-129-629-api18.json.xz',(141,180,200,629)))
        for filename,frames in samples:
            cap=CapturaLimitada(AQUI/'evidencias'/filename)
            for row in cap.d['rows']:
                if row['frame'] not in frames:continue
                with self.subTest(capture=filename,frame=row['frame']):
                    m=cap.memory(row);blocks=[(a,bytearray(d)) for a,d in m.blocks]
                    for a,d in blocks:
                        if a<=0x5099a4<a+len(d):struct.pack_into('<I',d,0x5099a4-a,0xdead0000);break
                    memory=SemPonteiroTexto(blocks)
                    inhabited=lambda i:memory.u16(0x49a0c8+276*i+0xc)>0
                    boundary=FronteiraTextoGravada(cap,row)
                    with ArgumentosRasterM3(catalog) as raster:
                        result=renderizar_quadro(memory,superficie_anterior=cap.blob(row['before']),cache=cap.cache_entry(row),
                            catalogo=catalog,habitado=inhabited,hud=True,texto=boundary,
                            relogio=lambda:struct.unpack_from('<I',cap.blob(row['exit_dgroup']),0x4e17b4-0x494000)[0])
                    self.assertIsNone(result.parada)
                    self.assertEqual(result.pixels,cap.blob(row['after']))
                    self.assertEqual(raster.calls,row['blits'])
                    self.assertFalse(boundary.pending)

    def test_frozen_api18_chained_window_report(self):
        report=json.loads((AQUI/'validacao/janelas-api18-final.json').read_text())
        expected={'P3':3001,'P6':2272,'P7':3572,'K1':501}
        self.assertEqual({r['probe']:r['drawn_total'] for r in report['windows']},expected)
        for window in report['windows']:
            self.assertEqual(window['equal'],expected[window['probe']]);self.assertIsNone(window['first_stop'])
            self.assertTrue(all(r['equal'] for r in window['rows']))
        for path,digest in report['sources_sha256'].items():
            frozen=subprocess.check_output(['git','show','85dd278:pesquisas-paralelas/graficos-animacao/'+path],cwd=AQUI)
            self.assertEqual(hashlib.sha256(frozen).hexdigest(),digest,path)

    def test_128_hud_regression_and_prior_hashes(self):
        new=json.loads((AQUI/'evidencias/verificacao-cadeia-m22-v2-api18-128.json').read_text())
        self.assertEqual((new['frames'],new['render_api_version'],new['hud'],new['chained_equals_recorded_count']),(128,[1,8],True,128))
        self.assertIsNone(new['first_stop']);self.assertIsNone(new['first_chained_difference_frame'])
        for version in ('14','15','17'):
            old=json.loads((AQUI/f'evidencias/verificacao-cadeia-m22-v2-api{version}-128.json').read_text())
            self.assertEqual([row['chained']['sha256'] for row in new['rows']],
                             [row['chained']['sha256'] for row in old['rows']],version)

    def test_uncaptured_cave_flags_and_worker_tasks_stay_stops(self):
        for filename,frame,address,value,stop in (
            ('janela-P6-2001-2400-api18.json.xz',2179,0x4dfb30,b'\1','0x0040958e'),
            ('janela-P7-2401-2850-api18.json.xz',2850,None,b'\x0c','0x00414a8a')):
            cap=CapturaLimitada(AQUI/'evidencias'/filename);row=next(r for r in cap.d['rows'] if r['frame']==frame);m=cap.memory(row)
            address=address if address is not None else m.u32(0x4e19a0)+13*276+0x89
            blocks=[(a,bytearray(d)) for a,d in m.blocks]
            for a,d in blocks:
                if a<=address<a+len(d):d[address-a:address-a+len(value)]=value;break
            result=renderizar_quadro(MemoriaEntradaM3(blocks),superficie_anterior=cap.blob(row['before']),cache=cap.cache_entry(row),
                catalogo=CatalogoRastreado(),habitado=lambda i:True,hud=True)
            self.assertEqual(result.parada['endereco'],stop)

if __name__=='__main__':unittest.main()
