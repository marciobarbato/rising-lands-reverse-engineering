"""Real accepted-evidence replay and consumer failure/transition coverage."""
from pathlib import Path
import copy
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'apps/macos-preview/src'))
import macos_m22_playback as playback
from macos_state_consumer import StateValidationError, RuntimeContractPending, load_accepted_m1


class M22PlaybackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.player = playback.MacOSM22Playback.open(ROOT)

    def setUp(self): self.player.reset()

    def test_all_real_phase_summaries_and_full_checkpoints(self):
        p = self.player
        self.assertEqual(len(p.integrity), 257)
        self.assertEqual(sum(bool(i.get('checkpoint_full_state_equal')) for i in p.integrity), 11)
        for index, name in enumerate(playback.PHASES):
            image = p.step_to_phase(index)
            self.assertEqual(image.phase_name, name)
            self.assertEqual(image.summary_sha256, p._capture['phases'][index]['state_after']['summary']['sha256'])
        self.assertEqual(p.inspect()['observed']['counter']['value'], 128)

    def test_phase_frame_name_index_read_reset_and_repeat(self):
        p = self.player
        original = p.current
        first = p.step_to_frame('frame1')
        self.assertIs(first, p.step_to_phase('frame1'))
        self.assertIs(first, p.step_to_phase(2))
        self.assertEqual(p.read(0x508f7c, 4), b'\x01\0\0\0')
        self.assertEqual(p.step_to_frame(0), original)
        self.assertEqual(first, p.step_to_frame('1'))
        self.assertEqual(p.step_to_phase('state_s0'), original)
        self.assertEqual(p.step_to_frame(128).observed_words()['counter']['value'], 128)
        self.assertEqual(first, p.step_to_frame(1))

    def test_invalid_selectors_leave_image_unchanged(self):
        p = self.player; first = p.current
        for selector in (-1, 257, True, 'unknown', None):
            with self.assertRaises(StateValidationError): p.step_to_phase(selector)
            self.assertIs(p.current, first)
        for selector in (-1, 129, True, 'frame-1', None):
            with self.assertRaises(StateValidationError): p.step_to_frame(selector)
            self.assertIs(p.current, first)
        with self.assertRaises(StateValidationError): p.read(0, 1)

    def test_phase_failure_publishes_nothing(self):
        p = self.player; first = p.current
        summary = p._capture['phases'][0]['state_after']['summary']
        with patch.dict(summary, sha256='0'*64):
            with self.assertRaises(StateValidationError): p.step_to_phase(0)
        self.assertIs(p.current, first)
        self.assertEqual(p._index, -1)
        self.assertEqual(p.step_to_phase(0).phase_name, 'load_tail')

    def test_checkpoint_failure_publishes_nothing(self):
        p = self.player; first = p.current
        checkpoint = p._capture['phases'][2]['state_after']['full_state']
        key = next(iter(checkpoint))
        with patch.dict(checkpoint, {key: dict(base='0x1', hex='00')}):
            with self.assertRaises(StateValidationError): p.step_to_frame(1)
        self.assertIs(p.current, first)

    def test_missing_wrong_order_and_missing_checkpoint(self):
        phases = [dict(phase=n, state_after={}) for n in playback.PHASES]
        for p in phases:
            if p['phase'] in [f'frame{i}' for i in playback.CHECKPOINTS]: p['state_after']['full_state'] = {}
        playback.MacOSM22Playback._validate_order(dict(phases=phases))
        for changed in (phases[:-1], list(reversed(phases))):
            with self.assertRaises(StateValidationError):
                playback.MacOSM22Playback._validate_order(dict(phases=changed))
        changed = copy.deepcopy(phases); changed[2]['state_after'].clear()
        with self.assertRaises(StateValidationError):
            playback.MacOSM22Playback._validate_order(dict(phases=changed))

    def test_pinned_inputs_missing_and_modified(self):
        # Links point only to read-only committed evidence; mutation targets a new file.
        for missing in playback.PINS:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for relative in playback.PINS:
                    path = root / relative; path.parent.mkdir(parents=True, exist_ok=True)
                    if relative != missing: path.symlink_to(ROOT / relative)
                with self.assertRaises(StateValidationError): playback.MacOSM22Playback.open(root)
                path = root / missing; path.write_bytes(b'tampered input')
                with self.assertRaisesRegex(StateValidationError, 'modified'):
                    playback.MacOSM22Playback.open(root)

    def test_raw_hash_and_reader_summary_rejection(self):
        reader = self.player._reader
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'capture.json'; path.write_text('{}')
            with self.assertRaises(reader.IntegridadeCaptura): reader.carregar_captura(path, playback.RAW_SHA)
        cap = dict(phases=[dict(phase='test', state_delta=dict(released=[], allocated={}, ranges=[]),
                               state_after=dict(summary=dict(blocks=0, bytes=0, sha256='wrong')))])
        with self.assertRaises(reader.IntegridadeCaptura): list(reader.fases_referencia(cap, {}))

    def test_live_frames_reserved_scenarios_distinct_and_immutable(self):
        p = self.player
        self.assertNotEqual(load_accepted_m1(ROOT).inspect()['scenario'], p.inspect()['scenario'])
        with self.assertRaises(RuntimeContractPending): p.apply_frame({})
        with self.assertRaises(AttributeError): p.current.phase_name = 'other'
        self.assertIsInstance(p.current.blocks[0].data, bytes)
        with self.assertRaises(StateValidationError): p.previous_surface()
        p.step_to_phase(0)
        with self.assertRaisesRegex(StateValidationError, 'Missing previous surface'): p.previous_surface()
        with self.assertRaisesRegex(StateValidationError, 'differs'): p.previous_surface(b'incorrect')
