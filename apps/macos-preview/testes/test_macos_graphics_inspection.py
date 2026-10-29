"""Consumer protocol tests; synthetic pixel fixtures do not claim real rendering."""
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'apps/macos-preview/src'))
from macos_graphics_inspection import GraphicsInspectionRenderer, GraphicsVersionError
from macos_state_consumer import StateValidationError


class GraphicsInspectionTests(unittest.TestCase):
    def renderer(self, stop=None):
        result = SimpleNamespace(versao=(1, 0), largura=800, altura=600,
                                 rgba=bytes(1920000), pixels=bytes(480000), parada=stop,
                                 chamadas=(), efeitos=())
        renderer = object.__new__(GraphicsInspectionRenderer)
        renderer.api = SimpleNamespace(VERSAO_RENDER_QUADRO=(1, 0),
                                       renderizar_quadro=Mock(return_value=result), Catalogo=Mock())
        renderer.catalog, renderer.graphics_sources, renderer.surface_source = object(), None, None
        renderer.encode_png = Mock(return_value=b'synthetic-encoding-test')
        return renderer

    def player(self):
        return SimpleNamespace(current=object(), previous_surface=Mock(return_value=bytes(480000)))

    def test_full_and_partial_are_distinct_and_provider_only(self):
        for stop in (None, dict(endereco='0x0040f378', detalhe='habitation provider required')):
            r = self.renderer(stop); p = self.player()
            value = r.render(p)
            self.assertEqual(value['status'], 'partial' if stop else 'full')
            self.assertEqual(value['stop'], stop)
            r.api.renderizar_quadro.assert_called_once_with(p.current, superficie_anterior=bytes(480000), catalogo=r.catalog)
            self.assertTrue(value['api_called'])
            self.assertIn('image', value)

    def test_missing_surface_never_calls_graphics_or_encodes_an_image(self):
        r = self.renderer(); p = self.player()
        p.previous_surface.side_effect = StateValidationError('Missing previous surface: accepted bytes unavailable')
        result = r.render(p)
        self.assertEqual((result['status'], result['code'], result['api_called']), ('stop', 'missing_previous_surface', False))
        self.assertNotIn('image', result)
        r.api.renderizar_quadro.assert_not_called(); r.encode_png.assert_not_called()

    def test_missing_assets_and_invalid_surface_are_explicit(self):
        r = self.renderer(); r.catalog = None
        r.api.Catalogo.side_effect = FileNotFoundError('PLATGAME.PIE')
        result = r.render(self.player())
        self.assertEqual(result['stage'], 'graphics-input')
        self.assertFalse(result['api_called'])
        p = self.player(); p.previous_surface.side_effect = StateValidationError('Previous surface differs')
        self.assertEqual(r.render(p)['code'], 'invalid_previous_surface')

    def test_api_and_returned_version_mismatch_refused(self):
        r = self.renderer(); r.api.VERSAO_RENDER_QUADRO = (1, 1)
        with self.assertRaises(GraphicsVersionError): r.render(self.player())
        r.api.renderizar_quadro.assert_not_called()
        r = self.renderer(); r.api.renderizar_quadro.return_value.versao = (2, 0)
        with self.assertRaises(GraphicsVersionError): r.render(self.player())

    def test_extent_validation_and_pluggable_source(self):
        r = self.renderer(); r.surface_source = Mock(return_value=b'explicit-source')
        p = self.player(); r.render(p)
        p.previous_surface.assert_called_once_with(b'explicit-source')
        r.api.renderizar_quadro.return_value.altura = 1
        self.assertEqual(r.render(p)['status'], 'stop')

    def test_real_graphics_api_loads_in_isolated_process_at_version_1_0(self):
        script = ('import sys;sys.path.insert(0,sys.argv[1]);'
                  'from macos_graphics_inspection import load_graphics;'
                  'print(load_graphics(sys.argv[2]).VERSAO_RENDER_QUADRO)')
        result = subprocess.run([sys.executable, '-I', '-B', '-c', script,
                                 str(ROOT/'apps/macos-preview/src'), str(ROOT)],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), '(1, 0)')
