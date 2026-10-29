"""Graphics 1.5 consumer protocol; synthetic pixels only test adapter behavior."""
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace as NS
import unittest
import tempfile
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'apps/macos-preview/src'))
from macos_graphics_inspection import GraphicsInspectionRenderer, GraphicsVersionError, require_version
from macos_state_consumer import StateValidationError, _sha


class GraphicsInspectionTests(unittest.TestCase):
    def test_15_no_input_reference_preserves_all_14_surface_hashes(self):
        import json
        from macos_graphics_inspection import RENDER_PINS
        folder=ROOT/'pesquisas-paralelas/graficos-animacao/evidencias'
        filename='verificacao-cadeia-m22-v2-api15-128.json'
        self.assertEqual(_sha((folder/filename).read_bytes()),RENDER_PINS[filename])
        old=json.loads((folder/'verificacao-cadeia-m22-v2-api14-128.json').read_bytes())['rows']
        new=json.loads((folder/filename).read_bytes())['rows']
        self.assertEqual(len(new),128)
        self.assertEqual([(r['frame'],r['chained']['sha256'],r['native_full_surface_sha256']) for r in old],
                         [(r['frame'],r['chained']['sha256'],r['native_full_surface_sha256']) for r in new])

    def renderer(self, stop=None):
        cache = NS(registros=bytes(1024), blocos_crus=bytes(256*1056), proximo=76)
        next_cache = NS(registros=bytes(1024), blocos_crus=bytes(256*1056), proximo=77)
        result = NS(versao=(1, 5), largura=800, altura=600, rgba=bytes(1920000),
                    pixels=bytes(480000), parada=stop, chamadas=(('AffTerrain',),), efeitos=(), cache=next_cache)
        r = object.__new__(GraphicsInspectionRenderer)
        r.api = NS(VERSAO_RENDER_QUADRO=(1, 5), renderizar_quadro=Mock(return_value=result),
                   regioes_necessarias=Mock(return_value=[(0x100,0x104,'minimapa'),(0x200,0x264,'jogadores')]))
        r.root, r.catalog, r.initial_pixels, r.initial_cache = ROOT, object(), bytes(480000), cache
        r.references = {}; r.phase_hashes = {n:_sha(bytes(480000)) for n in ('load_tail','between_frames','frame1','between_frames2')}
        r.encode_png = Mock(return_value=b'encoded-by-graphics')
        r.reset()
        return r

    def consume(self, r, index, name):
        with patch('macos_habitation_view.habitation_query', return_value='real-read-provider'):
            return r.consume(NS(phase_index=index, phase_name=name), memory=NS(phase_name='captured-entry',summary_sha256='captured-summary',
                    ler_mundo=Mock(side_effect=lambda address,size: bytes(size))))

    def test_raw_indexed_transfer_keeps_exact_pixels_palette_without_png(self):
        import base64
        r=self.renderer();r.palette=bytes(range(256))*3
        self.consume(r,0,'load_tail');self.consume(r,1,'between_frames')
        wire=r.present(raw=True)
        self.assertNotIn('image',wire)
        self.assertEqual(base64.b64decode(wire['frame']['pixels']),r.pixels)
        self.assertEqual(base64.b64decode(wire['frame']['palette']),r.palette)
        self.assertEqual(wire['frame']['pixels_sha256'],_sha(r.pixels))
        r.encode_png.assert_not_called()

    def test_pixels_and_cache_chain_with_undrawn_frame(self):
        r=self.renderer(); self.consume(r,0,'load_tail')
        self.assertEqual(self.consume(r,1,'between_frames')['status'],'full')
        first_cache=r.cache
        self.assertEqual(self.consume(r,2,'frame1')['status'],'undrawn')
        self.assertIs(r.cache,first_cache)
        self.consume(r,3,'between_frames2')
        args=r.api.renderizar_quadro.call_args.kwargs
        self.assertIs(args['cache'],first_cache)
        self.assertEqual(args['superficie_anterior'],bytes(480000))
        self.assertEqual(r.api.renderizar_quadro.call_count,2)
        self.assertIs(args['hud'],True)
        self.assertIs(r.api.regioes_necessarias.call_args.kwargs['hud'],True)
        self.assertEqual([v['name'] for v in r.records[-1]['required_regions']],['minimapa','jogadores'])
        self.assertNotIn('HUD rows >= 544 not drawn',r.records[-1]['limitations'])

    def test_partial_stop_is_retained_in_undrawn_phase(self):
        stop=dict(endereco='0x00417f6e',detalhe='HUD resource counter outside supported domain')
        r=self.renderer(stop);self.consume(r,0,'load_tail')
        self.assertEqual(self.consume(r,1,'between_frames')['status'],'partial')
        self.consume(r,2,'frame1')
        self.assertEqual(r.present()['inherited_stop'],stop)
        self.assertIn('HUD',r.present()['detail'])

    def test_every_other_api_version_refused_without_publication(self):
        for version in ((1,0),(1,1),(1,2),(1,3),(1,4),(1,6),(2,0),None):
            with self.assertRaises(GraphicsVersionError): require_version(version)
        r=self.renderer();self.consume(r,0,'load_tail')
        r.api.renderizar_quadro.return_value.versao=(1,6)
        with self.assertRaises(GraphicsVersionError):self.consume(r,1,'between_frames')
        self.assertEqual(r.index,0)

    def test_wrong_order_missing_memory_and_bad_extent_refused(self):
        r=self.renderer()
        with self.assertRaises(StateValidationError):self.consume(r,1,'between_frames')
        self.consume(r,0,'load_tail')
        with self.assertRaises(StateValidationError):r.consume(NS(phase_index=1,phase_name='between_frames'))
        r.api.renderizar_quadro.return_value.altura=1
        with self.assertRaises(StateValidationError):self.consume(r,1,'between_frames')
        self.assertEqual(r.index,0)

    def test_checkpoint_failure_keeps_previous_pixels_cache_and_index(self):
        r=self.renderer();self.consume(r,0,'load_tail');before=r.pixels,r.cache,r.index
        r.references={1:dict(chained=dict(sha256='wrong',first_row=1),native_full_surface_sha256='native')}
        with self.assertRaises(StateValidationError):self.consume(r,1,'between_frames')
        self.assertEqual((r.pixels,r.cache,r.index),before)

    def test_missing_or_short_hud_region_is_refused_before_render(self):
        for reader in (Mock(side_effect=StateValidationError('Missing minimap')),
                       Mock(return_value=b'')):
            r=self.renderer();self.consume(r,0,'load_tail');before=r.pixels,r.cache,r.index
            memory=NS(ler_mundo=reader)
            with self.assertRaises(StateValidationError):
                r.consume(NS(phase_index=1,phase_name='between_frames'),memory)
            self.assertEqual((r.pixels,r.cache,r.index),before)
            r.api.renderizar_quadro.assert_not_called()

    def test_full_phase_end_mismatch_is_atomic_even_when_chain_hash_matches(self):
        r=self.renderer();self.consume(r,0,'load_tail');before=r.pixels,r.cache,r.index
        digest=_sha(bytes(480000))
        r.references={1:dict(chained=dict(sha256=digest,first_row=None),native_full_surface_sha256=digest)}
        r.phase_hashes['between_frames']='incorrect-phase-end'
        with self.assertRaisesRegex(StateValidationError,'Native phase-end surface mismatch'):
            self.consume(r,1,'between_frames')
        self.assertEqual((r.pixels,r.cache,r.index),before)

    def test_reset_restarts_from_both_initial_artifacts(self):
        r=self.renderer();self.consume(r,0,'load_tail');self.consume(r,1,'between_frames')
        r.reset()
        self.assertIs(r.pixels,r.initial_pixels);self.assertIs(r.cache,r.initial_cache)
        self.assertEqual(r.index,-1)

    def test_real_graphics_api_loads_in_isolated_process_at_version_1_5(self):
        script=('import sys;sys.path.insert(0,sys.argv[1]);'
                'from macos_graphics_inspection import load_graphics;'
                'print(load_graphics(sys.argv[2]).VERSAO_RENDER_QUADRO)')
        result=subprocess.run([sys.executable,'-I','-B','-c',script,str(ROOT/'apps/macos-preview/src'),str(ROOT)],capture_output=True,text=True,timeout=20)
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(result.stdout.strip(),'(1, 5)')

    def test_initial_artifact_modified_or_missing_is_refused_before_asset_load(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            folder=root/'pesquisas-paralelas/graficos-animacao/evidencias';folder.mkdir(parents=True)
            with patch('macos_graphics_inspection.load_graphics', return_value=NS(VERSAO_RENDER_QUADRO=(1,5))):
                with self.assertRaises(FileNotFoundError): GraphicsInspectionRenderer(root)
                (folder/'superficie-inicial-m22-v2.json').write_text('tampered')
                with self.assertRaisesRegex(StateValidationError,'Unpinned Graphics artifact'): GraphicsInspectionRenderer(root)
