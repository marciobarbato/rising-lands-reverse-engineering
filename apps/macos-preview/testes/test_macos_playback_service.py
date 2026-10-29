"""Exercise the real isolated worker and JSON bridge, including errors and close."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'apps/macos-preview/src'))
from macos_playback_client import MacOSPlaybackClient


class PlaybackServiceTests(unittest.TestCase):
    def test_worker_open_step_read_reset_errors_and_close(self):
        client = MacOSPlaybackClient(ROOT, ROOT/'apps/macos-preview/src', 'test-commit')
        self.addCleanup(client.close)
        initial = client.request(dict(id=1, operation='open'))['playback']
        self.assertEqual((initial['verified_phases'], initial['verified_checkpoints']), (257, 11))
        self.assertEqual(initial['commit'], 'test-commit')
        result = client.request(dict(id=2, operation='frame', frame=1))['playback']
        self.assertEqual(result['phase'], 'frame1')
        self.assertEqual(result['render']['code'], 'missing_previous_surface')
        self.assertEqual(client.request(dict(id=3, operation='read', address='0x508f7c', size=4))['playback']['read_hex'], '01000000')
        self.assertFalse(client.request(dict(id=4, operation='unknown'))['ok'])
        self.assertFalse(client.request([])['ok'])
        self.assertFalse(client.request(dict(id=5, operation='phase', phase='unknown'))['ok'])
        self.assertEqual(client.request(dict(id=6, operation='phase', phase='frame1'))['playback']['summary_sha256'], result['summary_sha256'])
        self.assertEqual(client.request(dict(id=7, operation='reset'))['playback']['summary_sha256'], initial['summary_sha256'])
        process = client.process
        client.close()
        self.assertIsNotNone(process.poll())
