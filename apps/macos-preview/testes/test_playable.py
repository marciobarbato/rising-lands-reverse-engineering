"""Consumer integration tests over real committed providers, without x86 claims."""
import os
from pathlib import Path
import struct
import sys
import unittest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP / 'src'))
from engine import Preview, MANIFEST, SNAP


class PlayableTests(unittest.TestCase):
    def setUp(self):
        self.preview = Preview()
        self.preview.reset('jogavel')

    def move(self, index, x, y):
        self.preview.order(index, x, y)
        for _ in range(4):
            self.preview.step(200)
        self.assertEqual(self.preview.state()['units'][index]['pos'], [x, y])

    def test_live_navigation_resource_delivery_and_repeated_combat(self):
        p = self.preview
        initial = p.research.economy.consultar(0).comida
        self.move(1, 4, 9)
        p.session.interact('collect', 1, 2)
        self.assertEqual(p.session.state()['remaining'], 7)
        self.assertEqual(p.research.economy.consultar(0).comida, initial)
        self.move(1, 2, 12)
        p.session.interact('deposit', 1, 2)
        self.assertEqual(p.research.economy.consultar(0).comida, initial + 1)
        self.assertEqual(p.session.delivered, 1)
        self.move(0, 9, 4)
        self.assertTrue(p.world.historico_navegacao)
        p.session.interact('attack', 0, 2)
        p.step(100)
        self.assertGreaterEqual(p.session.hits, 2)
        self.assertLess(p.world.palavra(2, 0x9a), 100)
        self.assertGreater(p.world.palavra(2, 0x9a), 0)

    def test_lethal_boundary_preserves_life_and_never_retries(self):
        p = self.preview
        self.move(0, 9, 4)
        p.session.interact('attack', 0, 2)
        p.step(200)
        self.assertIsNotNone(p.session.boundary)
        self.assertEqual(p.world.palavra(2, 0x9a), 20)
        self.assertEqual(p.session.hits, 4)
        before = bytes(p.world.unidades)
        p.step(200)
        self.assertEqual(bytes(p.world.unidades), before)
        self.assertTrue(p.paused)

    def test_move_interrupts_attack_without_replaying_damage(self):
        p = self.preview
        self.move(0, 9, 4)
        p.session.interact('attack', 0, 2)
        p.step(20)
        self.move(0, 8, 4)
        hits = p.session.hits
        p.step(100)
        self.assertEqual(p.session.hits, hits)

    def test_foreign_unit_and_bad_actions_preserve_live_state(self):
        p = self.preview
        before = bytes(p.world.unidades), bytes(p.research.economy.memoria)
        for message in ({'action':'order','unit':2,'x':8,'y':8},
                        {'action':'interact','operation':'attack','unit':0,'target':2},
                        {'action':'interact','operation':'collect','unit':1},
                        {'action':'interact','operation':'deposit','unit':1},
                        {'action':'interact','operation':'unknown','unit':1}):
            with self.assertRaises(ValueError):
                p.handle(message)
        self.assertEqual((bytes(p.world.unidades), bytes(p.research.economy.memoria)), before)

    def test_message_adapter_rejects_nonempty_ai_group(self):
        p = self.preview
        p.world.controle_jogadores[0] = 2
        struct.pack_into('<I', p.world.unidades, 0x10c, 0)
        with self.assertRaises(NotImplementedError):
            p.session.effect('iagUnitSendMessage', (0, 0x48, 2))

    def test_same_revision_for_every_runtime_provider(self):
        import economia, animacao_disparo, consumo_dano, navegacao_unidades
        for module in (economia, animacao_disparo, consumo_dano, navegacao_unidades):
            self.assertTrue(Path(module.__file__).resolve().is_relative_to(SNAP.resolve()))
        self.assertNotIn('unicorn', sys.modules)
        self.assertEqual(self.preview.state()['commit'], MANIFEST['commit'])


if __name__ == '__main__':
    unittest.main()
