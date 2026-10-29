"""Static artifact reproducibility and bounds, with no native execution."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

OWNED=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('difficulty_static_scan',OWNED/'difficulty_scan.py')
scan=importlib.util.module_from_spec(spec);spec.loader.exec_module(scan)
CD=Path(os.environ.get('RISING_CD_ROOT','/Users/marcio/git/Rising Lands/source/cd'))


class StaticDifficultyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report,cls.asm=scan.collect(CD)
        cls.expected=json.loads((OWNED/'evidence/static-scan-v1.json').read_text())

    def test_all_sources_and_original_instruction_artifacts_reproduce(self):
        self.assertEqual(self.report,self.expected)
        self.assertEqual(self.asm,(OWNED/'evidence/reviewed-routines.asm').read_text())

    def test_missing_mission_corpus_is_refused(self):
        formats,_=scan.read_modules()
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError,'MissionCorpusMismatch'):
                scan.collect_missions(Path(temporary),formats)

    def test_incompatible_executable_is_refused_before_disassembly(self):
        _,reader=scan.read_modules()
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'INSTALHD';path.mkdir();(path/'RISING.EXE').write_bytes(b'wrong original')
            with self.assertRaisesRegex(ValueError,'OriginalIdentityMismatch'):
                scan.collect_code(Path(temporary),reader)

    def test_monster_profile_keys_are_absent_and_stub_bytes_are_exact(self):
        self.assertEqual(self.report['monstre_ini']['missing_profile_keys'],
                         ['HumanOnly','ProbaCaveJoueur','ProbaCaveIA','ProbaEmbuscade'])
        self.assertEqual(self.report['code']['config_getter']['bytes'],'89d8c3')
        refs=self.report['code']['profile_field_references']
        self.assertEqual(sum(r['absolute_field'] for r in refs),19)
        self.assertEqual(sum(not r['absolute_field'] for r in refs),2)
        writers={r['symbol'] for r in refs if r['absolute_field'] and r['access']&2}
        self.assertEqual(writers,{'InitEntrerMonstre','ReadConfigMonstre','ChargeMonstre'})
        self.assertFalse(any(r['target']=='ReadConfigMonstre' for r in self.report['code']['direct_calls']))

    def test_scenario_tuning_is_not_miscounted_as_global_difficulty(self):
        missions=self.report['missions']
        self.assertEqual(len(missions),38)
        self.assertEqual(sum(m['monster_table']['active_cell_records'] for m in missions),436)
        self.assertEqual(len({m['discarded16']['raw_hex'] for m in missions}),5)
        first=next(m for m in missions if m['path']=='WORLD/MONDE01.ETA')
        timed=[r for r in first['monster_table']['records'] if r['disk_period']]
        self.assertEqual([r['loaded_u16_period'] for r in timed],[9000,10800])
        self.assertEqual(len(first['monster_table']['records']),5)
        self.assertEqual(first['conditions']['records'][1]['words'][0],50)


if __name__=='__main__':unittest.main()
