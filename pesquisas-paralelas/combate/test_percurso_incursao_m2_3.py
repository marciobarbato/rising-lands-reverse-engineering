"""Facts of the native MONDE01 raid course (forced counters 9000..12000) that Combat relies on.

Reads `percurso-incursao-m2-3-original.json`; nothing is emulated or
translated.  It pins what the no-input raid reaches: two spawns with their
effect projectiles and orders, empty target queries and no attack, damage or
death routine, so a later Combat translation of those routines is not needed
for this path.
"""
import json
import unittest
from pathlib import Path

CAPTURA = Path(__file__).resolve().parent / 'evidencias/percurso-incursao-m2-3-original.json'


class PercursoIncursaoM23(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(CAPTURA.read_text())
        cls.chaves = [(q['counter'], linha) for q in cls.d['frames'] for linha in q.get('key_entries', ())]

    def entradas(self, rotina):
        return [(c, linha.split()[1:]) for c, linha in self.chaves if linha.split('@')[0] == rotina]

    def test_capture_is_complete(self):
        self.assertIsNone(self.d['stop'])
        self.assertFalse(self.d['translation_executed'])
        self.assertEqual([q['counter'] for q in self.d['frames']], list(range(9000, 12001)))

    def test_no_attack_damage_or_death(self):
        self.assertEqual(self.d['never_entered'], [
            'SetAttaqueEngin', 'CalculAttaqueEngin', 'InfligeDegat', 'iagUnitSendMessage', 'CreerExplosion',
            'EnginInfligeDegat', 'ProjectileInfligeDegat', 'BatimentInfligeDegat', 'SetDyingEngin',
            'DetruireEngin', 'DetruireBatiment'])

    def test_two_spawns_with_effects_and_orders(self):
        self.assertEqual(self.entradas('ConstruitGroupeMonstre'),
                         [(9000, ['3f3f', '0', '1', '0']), (10800, ['3f00', '0', '1', '0'])])
        self.assertEqual([c for c, _ in self.entradas('ProjectileInit')], [9000, 10800])
        self.assertEqual(self.d['combat_totals']['ProjectileInit'], 2)
        self.assertEqual(self.entradas('StockeAction'), [
            (9000, ['2f', '12', '2e03', '3e3e']), (10800, ['2f', '13', '3b22', '3e00']),
            (11101, ['2e', '12', '320e', '2e03'])])

    def test_raid_units_end_idle_at_their_destinations(self):
        ultimo = {}
        for q in self.d['frames']:
            for unidade, estado in q.get('raid_units', {}).items():
                ultimo[unidade] = (q['counter'], estado['cell'], estado['head'])
        self.assertEqual(ultimo, {'16': (11280, '0x320e', '040007a7'), '17': (11580, '0x3b22', '040007a7')})


if __name__ == '__main__':
    unittest.main()
