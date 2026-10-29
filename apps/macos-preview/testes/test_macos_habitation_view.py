"""Read-only Economy interop; no constructor-synthesized game state."""
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'apps/macos-preview/src'))
from macos_habitation_view import habitation_query
from macos_m22_playback import MacOSM22Playback


class HabitationViewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.player=MacOSM22Playback.open(ROOT)

    def test_existing_economy_query_matches_original_graphics_reference_without_mutation(self):
        image=self.player.reset();identity=image.identity
        expected=json.loads((ROOT/'pesquisas-paralelas/graficos-animacao/evidencias/quadro-original-pixels-m1.json').read_bytes())['habitation']
        query=habitation_query(ROOT,image)
        for index,value in expected.items(): self.assertEqual(query(int(index)),bool(value))
        self.assertEqual(image.identity,identity)
        self.assertIsInstance(image.blocks[0].data,bytes)

    def test_original_provider_rejects_out_of_pool_index(self):
        query=habitation_query(ROOT,self.player.current)
        with self.assertRaises(ValueError):query(1000)
        with self.assertRaises(ValueError):query(-1)

    def test_drawing_memory_is_previous_captured_state_not_ending_counter(self):
        self.player.reset();self.player.step_to_phase('between_frames')
        self.assertEqual(self.player.current.u32(0x508f7c),1)
        self.assertEqual(self.player.drawing_input().u32(0x508f7c),0)
        self.assertEqual(self.player.drawing_input().phase_name,'load_tail')
