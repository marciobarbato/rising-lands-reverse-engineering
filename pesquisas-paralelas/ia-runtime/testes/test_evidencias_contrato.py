"""Exported intervals and static inventories reproduce the intact executable's bytes."""
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
from ambiente_ia_runtime import ANALYSIS_SHA256, EVIDENCE, EXE, ORIGINAL_SHA256  # noqa: E402

LINE = re.compile(r'^([0-9a-f]{8})  (?:\.byte ([0-9a-f]+)$|([0-9a-f]+)\s)')
INTERVAL = re.compile(r'^; interval 0x([0-9a-f]{8})\.\.0x([0-9a-f]{8})')


def listing_parts(text):
    """(start, end, bytes) for every interval section of an exported listing."""
    parts = []
    for line in text.splitlines():
        header = INTERVAL.match(line)
        if header:
            parts.append([int(header.group(1), 16), int(header.group(2), 16), bytearray(), None])
            continue
        row = LINE.match(line)
        if row:
            address = int(row.group(1), 16)
            part = parts[-1]
            expected = part[0] + len(part[2])
            if address != expected:
                raise AssertionError(f'Listing gap at 0x{address:08x}, expected 0x{expected:08x}')
            part[2] += bytes.fromhex(row.group(2) or row.group(3))
    return [(start, end, bytes(data)) for start, end, data, _ in parts]


def without_snapshot_fields(inventory):
    """Drop fields that reflect other owners' later changes rather than original bytes."""
    clone = json.loads(json.dumps(inventory))
    for record in clone['operations']['records']:
        record.pop('core_status')
    return clone


@unittest.skipUnless(EXE.is_file(), 'intact RISING.EXE is not linked into this worktree (run workstream.py start)')
class ExportedIntervals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from inventario_ia_runtime import OriginalImage
        cls.image = OriginalImage()
        cls.manifest = json.loads((EVIDENCE / 'manifesto.json').read_text(encoding='utf-8'))
        cls.inventory = json.loads((EVIDENCE / 'inventario.json').read_text(encoding='utf-8'))

    def test_identities(self):
        self.assertEqual(hashlib.sha256(EXE.read_bytes()).hexdigest(), ORIGINAL_SHA256)
        self.assertEqual(self.manifest['original_sha256'], ORIGINAL_SHA256)
        self.assertEqual(self.manifest['analysis_sha256'], ANALYSIS_SHA256)
        self.assertNotEqual(ORIGINAL_SHA256, ANALYSIS_SHA256)

    def test_every_interval_hash_matches_the_original_bytes(self):
        records = self.manifest['intervals'] + self.manifest['data_tables']
        records += [tail for record in self.manifest['intervals'] for tail in record.get('shared_tails', [])]
        self.assertEqual(len(self.manifest['intervals']), 171)
        for record in records:
            start, end = int(record['start'], 16), int(record['end_exclusive'], 16)
            data = self.image.read(start, end)
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()), (record['size'], record['sha256']),
                             record['name'])

    def test_listings_reproduce_the_interval_bytes(self):
        files = [r for r in self.manifest['intervals'] if r.get('file')]
        self.assertEqual(len(files), 35)
        for record in files:
            parts = listing_parts((EVIDENCE / record['file']).read_text(encoding='utf-8'))
            expected = [(int(record['start'], 16), int(record['end_exclusive'], 16))]
            expected += [(int(t['start'], 16), int(t['end_exclusive'], 16)) for t in record['shared_tails']]
            self.assertEqual([(s, e) for s, e, _ in parts], expected, record['file'])
            for start, end, data in parts:
                self.assertEqual(data, self.image.read(start, end), f'{record["file"]} 0x{start:08x}')

    def test_data_tables_hold_the_listed_values(self):
        for table in self.manifest['data_tables']:
            values = self.image.table(int(table['start'], 16), table['entries'])
            self.assertEqual([f'0x{v:08x}' for v in values], table['values'], table['name'])

    def test_regeneration_from_the_original_is_identical(self):
        from extrair_contrato_ia import build
        manifest, inventory, listings = build()
        manifest.pop('core_inputs')
        committed = dict(self.manifest)
        committed.pop('core_inputs')
        self.assertEqual(manifest, committed)
        self.assertEqual(without_snapshot_fields(inventory), without_snapshot_fields(self.inventory))
        for name, text in listings.items():
            self.assertEqual(text, (EVIDENCE / name).read_text(encoding='utf-8'), name)


class ContractFacts(unittest.TestCase):
    """Facts the manual states, read back from the committed inventory."""

    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((EVIDENCE / 'inventario.json').read_text(encoding='utf-8'))
        cls.dispatch = cls.inventory['dispatch']

    def test_unit_state_table(self):
        states = self.dispatch['engin_next_etape']['states']
        self.assertEqual(len(states), 25)
        direct_exit = [s['state'] for s in states if s['target'] == '0x00454ccd']
        self.assertEqual(direct_exit, [0, 8, 9, 10, 12, 14])
        calls = {s['state']: {c['name'] for c in s['calls']} for s in states}
        self.assertIn('CalculAttaqueEngin', calls[1])
        self.assertEqual(calls[1], calls[24])
        self.assertIn('CalculWorkEngin', calls[5])
        self.assertIn('CalculTransporteEngin', calls[18])
        self.assertEqual(calls[7], {'AnimBallonStatic', 'Random'})
        self.assertEqual(calls[14], set())

    def test_structure_type_table(self):
        types = {t['type']: {c['name'] for c in t['calls']} for t in self.dispatch['batiment_next_etape']['types']}
        self.assertEqual(len(types), 21)
        self.assertEqual(types[2], {'BagContient', 'BagContientTroupe', 'CalculTroupe'})
        self.assertIn('BaisseTouteHerse', types[12])
        self.assertEqual(types[9], set())
        self.assertEqual(types[21], set())

    def test_uncalled_routines(self):
        callers = self.inventory['callers']
        for address in ('0x00453062', '0x0047f328', '0x0047c162'):  # CalculEnginStatic, iaInit, IAResetAttaque
            self.assertEqual(callers[address]['sites'], [], callers[address]['name'])
        self.assertEqual([s['routine'] for s in callers['0x0047f36e']['sites']], ['MissionLoad', 'MissionLoadName'])
        self.assertEqual([s['routine'] for s in callers['0x0047fb15']['sites']], ['ProgInit'])

    def test_operations_cover_the_rule_program(self):
        operations = self.inventory['operations']
        self.assertEqual((operations['names'], operations['addresses'], operations['instructions']), (140, 136, 1157))
        self.assertEqual(operations['unresolved_names'], [])
        names = [n for r in operations['records'] for n in r['names']]
        self.assertEqual(len(names), 140)
        self.assertTrue(all(r['provider_families'] for r in operations['records']))
        self.assertFalse([r for r in operations['records'] if 'unclassified' in r['provider_families']])

    def test_message_tables(self):
        unit = self.inventory['messages']['iagUnitSendMessage']
        self.assertEqual([b['message'] for b in unit['branches']], [f'0x{m:02x}' for m in range(0x41, 0x4d)])
        city = self.inventory['messages']['iagVilleSendMessage']
        self.assertEqual([b['message'] for b in city['branches']], ['0x01', '0x02', '0x03', '0x04'])
        behaviors = self.inventory['messages']['behaviors']['records']
        self.assertEqual(len(behaviors), 12)
        self.assertIsInstance(behaviors[0]['handlers'], str)  # record outside initialized data


if __name__ == '__main__':
    unittest.main()
