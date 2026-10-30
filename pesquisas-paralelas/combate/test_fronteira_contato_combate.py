"""Real raid-contact regression through the supported AI callback boundary."""
import unittest

from validar_fronteira_contato_combate import comparar_contato


class RaidContactBoundary(unittest.TestCase):
    def test_existing_combat_matches_real_contact_before_ai_message(self):
        report = comparar_contato()
        self.assertEqual(report['summary'], dict(cases=2, mismatches=0))
        self.assertEqual(report['cases'][1]['dependency'], dict(
            name='iagUnitSendMessage', address=0x4829c8, arguments=[0, 0x48, 16]))


if __name__ == '__main__':
    unittest.main()
