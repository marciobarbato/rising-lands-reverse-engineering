"""Original-only call-order captures: committed facts, core consistency and native replay."""
import json
import os
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
from ambiente_ia_runtime import EVIDENCE, EXE, ORIGINAL_SHA256  # noqa: E402

FRAME_BODY = ['MessageBoxCalcul', 'GameNextFrame', 'CalculIconeAction', 'ProjectileCalcul', 'CalculEnginNextEtape',
              'CalculBatimentNextEtape', 'RechercheCalcul', 'PlayerInitAllianceCompteur', 'SetUpdateChamp',
              'UpdateChamp', 'CalculMatiere', 'CalculCompteurMarche', 'CalculCompteurProposition', 'NextAnimTerrain']
INPUT_LOOP = ['PlayerGetType', 'InputGame', 'InputSend', 'PlayerGetType', 'MissionGetNum', 'CalculNextReflect',
              'PlayerGetType', 'PlayerGetType', 'InputReceive', 'PlayerGetType', 'MissionGetNum', 'CalculNextReflect',
              'ProcessInputGame', 'ProcessInputGame', 'ProcessInputGame', 'ProcessInputGame']
PREFIX = ['USER32.dll!SetCursorPos', 'PlayerAttaqueReset', 'EvenementEnCours']


def load():
    return json.loads((EVIDENCE / 'capturas-originais.json').read_text(encoding='utf-8'))


class CommittedCaptures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = load()
        cls.scenarios = {s['scenario']: s for s in cls.document['scenarios']}

    def names(self, scenario):
        return [row[0] for row in self.scenarios[scenario]['calls']]

    def test_identity_and_count(self):
        self.assertEqual(self.document['original_sha256'], ORIGINAL_SHA256)
        self.assertEqual(len(self.scenarios), 57)

    def test_single_player_frame_order(self):
        names = self.names('frame_single_player')
        self.assertEqual(names, PREFIX + ['MCICD_Play'] + INPUT_LOOP + FRAME_BODY +
                         ['NextAnimVeget', 'PlayerAttaqueCalculSympa', 'TestFinDeMission'])
        self.assertEqual(self.scenarios['frame_single_player']['flag_5099b0_after'], 0)
        self.assertEqual(self.names('frame_music_flag_set_skips_cd_play'),
                         PREFIX + INPUT_LOOP + FRAME_BODY + ['NextAnimVeget', 'PlayerAttaqueCalculSympa', 'TestFinDeMission'])

    def test_three_gates(self):
        gate2 = self.scenarios['gate2_event_in_progress']
        self.assertEqual(self.names('gate2_event_in_progress'), PREFIX)
        self.assertEqual(gate2['flag_5099b0_after'], 1)  # exit 0x42d4ea keeps 0x5099b0
        self.assertEqual(self.names('gate3_state_left_during_input'), PREFIX + ['MCICD_Play'] + INPUT_LOOP)
        self.assertEqual(self.scenarios['gate3_state_left_during_input']['flag_5099b0_after'], 0)
        single = self.names('gate1_single_player_state_0x10')
        self.assertEqual(single[-1], 'MouseZone')
        self.assertNotIn('EvenementEnCours', single)
        network = self.names('gate1_network_state_0x10')
        self.assertEqual(network[network.index('PlayerAttaqueReset'):network.index('MCICD_Play')],
                         ['PlayerAttaqueReset', 'EvenementEnCours'])
        self.assertEqual(network[-2:], ['NextAnimVegetFullMap', 'PlayerAttaqueCalculSympa'])
        self.assertNotIn('TestFinDeMission', network)
        self.assertEqual(network.count('PlayerGetType'), 4)  # network input loop covers players 0..3

    def test_load_path_falls_through_into_the_first_frame(self):
        names = self.names('load_state0_then_first_frame')
        self.assertEqual(names[:9], ['USER32.dll!SetCursorPos', 'MouseInit', 'InitCache', 'InitGouttes', 'MissionLoad',
                                     'RestoreAll', 'SetClipping', 'MenuInit', 'InitGameZone'])
        self.assertEqual(names[9:], ['PlayerAttaqueReset', 'EvenementEnCours', 'MCICD_Play'] + INPUT_LOOP + FRAME_BODY +
                         ['NextAnimVeget', 'PlayerAttaqueCalculSympa', 'TestFinDeMission'])
        menu = [row for row in self.scenarios['load_state0_then_first_frame']['calls'] if row[0] == 'MenuInit'][0]
        self.assertEqual((menu[3], menu[4], menu[6]), ('0x00000000', '0x00000012', '0x00000001'))
        self.assertIn('MissionLoadName', self.names('load_state0_network_by_name'))

    def test_end_condition_tail(self):
        self.assertEqual(self.scenarios['end_condition_counting']['end_counter_after'], 6)
        self.assertEqual(self.names('end_condition_mission6_first_frame')[-1], 'MessageBoxSet')
        reached = self.scenarios['end_condition_reached']
        self.assertEqual(self.names('end_condition_reached')[-2:], ['PlaySnd_StopAllSound', 'MenuInit'])
        self.assertEqual((reached['end_counter_after'], reached['state_after']), (100, 0x13))

    def test_unit_loop(self):
        scenario = self.scenarios['unit_loop_monde01']
        names = self.names('unit_loop_monde01')
        dispatched = [int(row[3], 16) for row in scenario['calls'] if row[0] == 'EnginNextEtape']
        tested = [int(row[4], 16) for row in scenario['calls'] if row[0] == 'IATestUtilite']
        self.assertEqual(dispatched, list(range(20)))  # unit 20 (state 0) is skipped
        self.assertEqual(tested, [i for i in range(20) if i != 18])  # state 4 is dispatched but not counted
        self.assertEqual(names[:2], ['IATestUtilite', 'EnginNextEtape'])
        cells = {(row[0], row[1]): row[4] for row in scenario['stores']}
        self.assertEqual(cells[('0x004e1928', 2)], '0x000e')  # owner 0: 16 MONDE01 units minus two type-5
        self.assertEqual(cells[('0x004e1a3a', 2)], '0x0010')  # local (owner 0) units, type != 17

    def test_monde01_unit_states(self):
        self.assertEqual(self.names('unit_state_monde01_type9_state14'),
                         ['BonusGetValEngin', 'GetBit', 'GetBit', 'CalculFatigue', 'GetBit', 'GetBit'])
        self.assertEqual(self.names('unit_state_monde01_type0_state7'),
                         ['BonusGetValEngin', 'PlayerGetType', 'EnginTrouveCible', 'GetBit', 'GetBit', 'CalculFatigue',
                          'GetBit', 'GetBit', 'Random'])
        self.assertIn('SetAttaqueEngin', self.names('unit_state_type0_state7_target_found_human'))
        ai = self.scenarios['unit_state_type0_state7_target_found_ai']['calls']
        self.assertIn(['iagUnitSendMessage', '0x00000049'], [[row[0], row[4]] for row in ai])
        self.assertEqual(self.names('unit_state_state0_direct_entry'), [])

    def test_structure_dispatch(self):
        names = self.names('structure_loop')
        self.assertEqual(names[:3], ['ResetTableauHangar', 'IATestUtilite', 'BatimentNextEtape'])
        self.assertIn('DemonteBatiment', names)
        cells = {(row[0], row[1]): row[4] for row in self.scenarios['structure_loop']['stores']}
        self.assertEqual([cells[(f'0x{0x4dfaa8 + 4 * p:08x}', 4)] for p in range(4)],
                         ['0x00000002', '0x00000000', '0x00000000', '0x00000000'])
        self.assertEqual(self.names('structure_type2_bag1'), ['BagContientTroupe', 'CalculTroupe'])

    def test_core_orchestration_reproduces_ia_calcul_player(self):
        """Core's committed ia.atualizar_ia against the original-only captures (no copy, no change)."""
        from ia import EstadoIA, atualizar_ia
        for name, scenario in self.scenarios.items():
            if not name.startswith('ia_calcul_player_'):
                continue
            fixture = scenario['fixture']
            player = fixture['registers']['eax']
            state = fixture['state']
            declared = {n: int(v, 16) for n, v in fixture['declared_returns'].items() if n != 'other callbacks'}
            addresses = {'iagUnitNoyau': 0x482936, 'iagVilleNoyau': 0x48453c, 'iagRessNoyau': 0x485183,
                         'iagWarNoyau': 0x4866d7, 'iaSolver': 0x47d314, 'AvanceMonstre': 0x47b283,
                         'iagUnitDeleteAllGroups': 0x483d95}
            by_address = {addresses[n]: v for n, v in declared.items()}
            calls = []

            def chamar(address, *args):
                calls.append((address,) + args)
                return by_address.get(address, 0)
            estado = EstadoIA(inativo=state.get('inactive', 0), ciclos_sem_efetivo=state.get('cycles', 0))
            result = atualizar_ia(player, 1, estado, state.get('structures', 0), state.get('units', 0), chamar)
            expected = []
            for row in scenario['calls']:
                address, eax, edx = int(row[1], 16), int(row[3], 16), int(row[4], 16)
                expected.append((address, eax, edx) if address == 0x4866d7 else (address, eax))
            self.assertEqual(calls, expected, name)
            self.assertEqual(f'0x{result:08x}', scenario['final_eax'], name)
            if player < 4:
                self.assertEqual((estado.inativo, estado.ciclos_sem_efetivo),
                                 (scenario['inactive_after'], scenario['cycles_after']), name)

    def test_ai_tables_written_by_reset(self):
        reset = self.scenarios['ia_reset_empty_world']
        routines = {r for region in reset['store_regions'] for r in region['routines']}
        self.assertTrue({'listInit', 'iagUnitReset', 'iagVilleReset', 'iagRessReset', 'iagWarReset',
                         'InitMissionMonstre', 'IaReset'} <= routines)
        starts = {region['start'] for region in reset['store_regions']}
        self.assertTrue({'0x005148a0', '0x00512320'} <= starts)
        alloc = self.scenarios['ia_alloc_program_start']
        self.assertEqual([row[0] for row in alloc['calls']],
                         ['WINMM.dll!timeGetTime', 'debugSymLoad', 'iaProbLoadBinaryRules', 'debugSymUnload'])

    def test_messages(self):
        handlers = {m: self.names(f'unit_message_0x{m:02x}_owner_type2')[1:] for m in range(0x41, 0x4d)}
        self.assertEqual(handlers[0x47], [])
        self.assertEqual(handlers[0x49], ['iabDetection_AjouteEnnemiSaufCivilOuAlerteConflit'])
        self.assertEqual(handlers[0x4b], ['iabFaim_TricheFaim'])
        self.assertEqual(self.names('unit_message_0x41_owner_type1'), ['PlayerGetType'])
        self.assertEqual(self.names('city_message_4')[-1], 'iaProbPost')
        self.assertEqual(self.names('city_message_0'), ['BatimentGetPlayer', 'PlayerGetType'])


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'native replay runs only with RISING_EMULAR=1')
@unittest.skipUnless(EXE.is_file(), 'intact RISING.EXE is not linked into this worktree')
class FreshNativeReplay(unittest.TestCase):
    def test_fresh_native_captures_equal_the_committed_document(self):
        from capturar_contrato_ia import build, dump
        fresh = json.loads(dump(build()))
        committed = load()
        self.assertEqual(len(fresh['scenarios']), len(committed['scenarios']))
        for new, old in zip(fresh['scenarios'], committed['scenarios']):
            self.assertEqual(new, old, new['scenario'])
        self.assertEqual(fresh, committed)
        print(f"\nnative replay: {len(fresh['scenarios'])} scenarios, "
              f"{sum(len(s['calls']) for s in fresh['scenarios'])} declared stops, "
              f"{sum(s['bench_segments'] for s in fresh['scenarios'])} bench segments", file=sys.stderr)


if __name__ == '__main__':
    unittest.main()
