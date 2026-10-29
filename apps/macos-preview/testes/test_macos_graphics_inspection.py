"""Graphics 1.3 consumer protocol; synthetic pixels only test adapter behavior."""
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
from macos_state_consumer import StateValidationError


class GraphicsInspectionTests(unittest.TestCase):
    def renderer(self, stop=None):
        cache = NS(registros=bytes(1024), blocos_crus=bytes(256*1056), proximo=76)
        next_cache = NS(registros=bytes(1024), blocos_crus=bytes(256*1056), proximo=77)
        result = NS(versao=(1, 3), largura=800, altura=600, rgba=bytes(1920000),
                    pixels=bytes(480000), parada=stop, chamadas=(('AffTerrain',),), efeitos=(), cache=next_cache)
        r = object.__new__(GraphicsInspectionRenderer)
        r.api = NS(VERSAO_RENDER_QUADRO=(1, 3), renderizar_quadro=Mock(return_value=result))
        r.root, r.catalog, r.initial_pixels, r.initial_cache = ROOT, object(), bytes(480000), cache
        r.references = {}; r.phase_hashes = {n:'reference' for n in ('load_tail','between_frames','frame1','between_frames2')}
        r.encode_png = Mock(return_value=b'encoded-by-graphics')
        r.reset()
        return r

    def consume(self, r, index, name):
        with patch('macos_habitation_view.habitation_query', return_value='real-read-provider'):
            return r.consume(NS(phase_index=index, phase_name=name), memory=NS(phase_name='captured-entry',summary_sha256='captured-summary'))

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

    def test_partial_stop_is_retained_in_undrawn_phase(self):
        stop=dict(endereco='0x0041591f',detalhe='type 8 outside the supported overlay domain')
        r=self.renderer(stop);self.consume(r,0,'load_tail')
        self.assertEqual(self.consume(r,1,'between_frames')['status'],'partial')
        self.consume(r,2,'frame1')
        self.assertEqual(r.present()['inherited_stop'],stop)
        self.assertIn('HUD',r.present()['detail'])

    def test_every_other_api_version_refused_without_publication(self):
        for version in ((1,0),(1,1),(1,2),(1,4),(2,0),None):
            with self.assertRaises(GraphicsVersionError): require_version(version)
        r=self.renderer();self.consume(r,0,'load_tail')
        r.api.renderizar_quadro.return_value.versao=(1,4)
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
        r.references={1:dict(chained=dict(sha256='wrong',first_row=1),native_checkpoint_sha256='native')}
        with self.assertRaises(StateValidationError):self.consume(r,1,'between_frames')
        self.assertEqual((r.pixels,r.cache,r.index),before)

    def test_reset_restarts_from_both_initial_artifacts(self):
        r=self.renderer();self.consume(r,0,'load_tail');self.consume(r,1,'between_frames')
        r.reset()
        self.assertIs(r.pixels,r.initial_pixels);self.assertIs(r.cache,r.initial_cache)
        self.assertEqual(r.index,-1)

    def test_real_graphics_api_loads_in_isolated_process_at_version_1_3(self):
        script=('import sys;sys.path.insert(0,sys.argv[1]);'
                'from macos_graphics_inspection import load_graphics;'
                'print(load_graphics(sys.argv[2]).VERSAO_RENDER_QUADRO)')
        result=subprocess.run([sys.executable,'-I','-B','-c',script,str(ROOT/'apps/macos-preview/src'),str(ROOT)],capture_output=True,text=True,timeout=20)
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(result.stdout.strip(),'(1, 3)')

    def test_initial_artifact_modified_or_missing_is_refused_before_asset_load(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            folder=root/'pesquisas-paralelas/graficos-animacao/evidencias';folder.mkdir(parents=True)
            with patch('macos_graphics_inspection.load_graphics', return_value=NS(VERSAO_RENDER_QUADRO=(1,3))):
                with self.assertRaises(FileNotFoundError): GraphicsInspectionRenderer(root)
                (folder/'superficie-inicial-m22-v2.json').write_text('tampered')
                with self.assertRaisesRegex(StateValidationError,'Unpinned Graphics artifact'): GraphicsInspectionRenderer(root)
