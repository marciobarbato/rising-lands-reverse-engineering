"""Replay the bounded original-only Audio/M2.2 access and pump evidence."""
import hashlib
import json
from pathlib import Path
import struct
import sys
import unittest

OWNED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNED))
from ambiente_audio import CD, ORIGINAL_SHA256


def read(name):return json.loads((OWNED/'evidencias'/name).read_text())


class M22AudioSoundnessTests(unittest.TestCase):
    def test_new_original_intervals_match_intact_pe(self):
        raw=(CD/'INSTALHD/RISING.EXE').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),ORIGINAL_SHA256)
        pe=struct.unpack_from('<I',raw,0x3c)[0];optional=struct.unpack_from('<H',raw,pe+20)[0]
        sections=[struct.unpack_from('<IIII',raw,pe+24+optional+i*40+8)
                  for i in range(struct.unpack_from('<H',raw,pe+6)[0])]
        inventory=read('m22-sound-original-inventory.json')
        self.assertEqual(len(inventory['routines']),101)
        for routine in inventory['routines']:
            rva=int(routine['start'],16)-0x400000
            section=next(s for s in sections if s[1]<=rva<s[1]+s[2])
            data=raw[section[3]+rva-section[1]:section[3]+rva-section[1]+routine['bytes']]
            self.assertEqual(hashlib.sha256(data).hexdigest(),routine['sha256'],routine['name'])

    def test_isolated_original_pumps_are_not_all_noops(self):
        report=read('m22-sound-original-pumps.json')
        self.assertEqual(report['coverage']['states'],258)
        self.assertEqual(report['coverage']['distinct_input_range_images'],1)
        manager,play,manage=report['cases']
        self.assertTrue(all(c['returned'] for c in report['cases']))
        self.assertEqual([(w['address'],w['old'],w['value']) for w in manager['writes']],
                         [('0x521f88','00000000','0x0'),('0x498f5c','01000000','0x0')])
        for c in (play,manage):
            self.assertEqual(c['writes'],[])
            self.assertEqual([r['address'] for r in c['reads']],['0x4e2f29'])

    def test_declared_reference_is_reproduced_in_all_257_phases(self):
        report=read('m22-sound-original-accesses.json')
        self.assertEqual(len(report['phases']),257)
        self.assertTrue(all(p['summary_equal'] for p in report['phases']))
        self.assertFalse(report['execute_original_pumps'])
        private={'initialized_sound_scalars','request_waiting_logical_physical_bank_state'}
        self.assertFalse([r for r in report['reads'] if r['range'] in private])

    def test_chained_pumps_keep_the_private_difference_and_no_game_readers(self):
        report=read('m22-sound-original-chained-pumps.json')
        self.assertTrue(report['complete']);self.assertIsNone(report['stop'])
        self.assertEqual(len(report['phases']),257)
        self.assertEqual(report['original_pump_entries'],{'MCICD_Play':130,'PlaySnd_Manage':128,'MCICD_Manage':128})
        self.assertEqual(report['code_sha256_before'],report['code_sha256_after'])
        self.assertEqual(report['memory_width_audit']['hook_backward_prefix'],15)
        self.assertLessEqual(report['memory_width_audit']['max_explicit_memory_operand_bytes'],16)
        self.assertTrue(report['phases'][0]['summary_equal'])
        self.assertTrue(all(p['differences']==[dict(block='dgroup',address='0x498f5c',accepted=1,actual=0)]
                            for p in report['phases'][1:]))
        private={'initialized_sound_scalars','request_waiting_logical_physical_bank_state'}
        self.assertTrue([r for r in report['reads'] if r['range'] in private])
        self.assertFalse([r for r in report['reads'] if r['range'] in private and r['code_owner']=='game-or-display'])

    def test_shared_cd_flags_and_cursor_are_not_classified_private(self):
        report=read('m22-sound-original-chained-pumps.json')
        flags=[r for r in report['reads'] if r['range']=='game_cd_playing_and_mci_initialized_flags' and r['code_owner']=='game-or-display']
        cursor=[r for r in report['writes'] if r['range']=='shared_random_permutation_cursor']
        self.assertTrue(flags);self.assertTrue(cursor)
        self.assertTrue(any(r['routine'].startswith('CalculGame') for r in flags))
        self.assertTrue(any(r['routine'].startswith('CalculGame') for r in cursor))
