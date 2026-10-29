"""Exercise the real isolated worker and JSON bridge, including errors and close."""
from pathlib import Path
import sys
import unittest
import tempfile
from macos_test_inputs import graphics_inputs

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'apps/macos-preview/src'))
from macos_playback_client import MacOSPlaybackClient


class PlaybackServiceTests(unittest.TestCase):
    def test_worker_open_step_read_reset_errors_and_close(self):
        client = MacOSPlaybackClient(ROOT, ROOT/'apps/macos-preview/src', 'test-commit', graphics_inputs(self, ROOT))
        self.addCleanup(client.close)
        response = client.request(dict(id=1, operation='open'))
        self.assertTrue(response.get('ok'), response)
        initial = response['playback']
        self.assertEqual((initial['verified_phases'], initial['verified_checkpoints']), (257, 11))
        self.assertEqual(initial['commit'], 'test-commit')
        result = client.request(dict(id=2, operation='frame', frame=1))['playback']
        self.assertEqual(result['phase'], 'frame1')
        self.assertEqual(result['render']['status'], 'undrawn')
        self.assertIsNone(result['render']['stop'])
        self.assertNotIn('inherited_stop', result['render'])
        self.assertEqual(result['render']['version'], [1, 4])
        self.assertIn('image', result['render'])
        self.assertTrue(result['render']['hud'])
        self.assertTrue(result['render']['equals_native_phase_end'])
        drawing=client.request(dict(id=20,operation='phase',phase='between_frames'))['playback']['render']
        regions={v['name']:v for v in drawing['required_regions']}
        self.assertEqual(regions['minimapa']['bytes'],128*128)
        self.assertEqual(regions['jogadores']['bytes'],100)
        self.assertTrue(drawing['equals_native_full_surface'])
        self.assertTrue(drawing['equals_native_phase_end'])
        self.assertEqual(client.request(dict(id=3, operation='read', address='0x508f7c', size=4))['playback']['read_hex'], '01000000')
        self.assertFalse(client.request(dict(id=4, operation='unknown'))['ok'])
        self.assertFalse(client.request([])['ok'])
        self.assertFalse(client.request(dict(id=5, operation='phase', phase='unknown'))['ok'])
        self.assertEqual(client.request(dict(id=6, operation='phase', phase='frame1'))['playback']['summary_sha256'], result['summary_sha256'])
        self.assertEqual(client.request(dict(id=7, operation='reset'))['playback']['summary_sha256'], initial['summary_sha256'])
        process = client.process
        client.close()
        self.assertIsNotNone(process.poll())

    def test_unsupported_api_returns_explicit_error_not_a_playback_key(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            folder=root/'pesquisas-paralelas/graficos-animacao';folder.mkdir(parents=True)
            (folder/'render_quadro.py').write_text('VERSAO_RENDER_QUADRO = (1, 5)\n')
            client=MacOSPlaybackClient(root, ROOT/'apps/macos-preview/src','test')
            self.addCleanup(client.close)
            response=client.request(dict(id=1,operation='open'))
            self.assertFalse(response['ok'])
            self.assertNotIn('playback',response)
            self.assertEqual(response['error_type'],'GraphicsVersionError')
            self.assertIn('expected (1, 4)',response['error'])
