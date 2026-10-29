"""Fast long-run package/continuation rejection checks; no native/game run."""
import base64
import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import zlib

import frame_long_evidence as e
import frame_long_differential as d


class FrameLongTests(unittest.TestCase):
    def test_published_manifest_exact_domain_and_pins(self):
        manifest = e.load_manifest()
        self.assertEqual(sum(p['phases'] for p in manifest['parts']),18401)
        self.assertEqual(manifest['parts'][9]['frames'],[8991,9200])

    def test_phase_order_and_checkpoint_indices(self):
        self.assertEqual(e.phase_names(0,1),['load_tail','between_frames','frame1'])
        self.assertEqual(e.phase_names(8991,8992),['between_frames8991','frame8991','between_frames8992','frame8992'])
        self.assertEqual(e.phase_frame('between_frames'),1)
        self.assertEqual(e.phase_frame('frame9176'),9176)

    def test_allocator_checkpoint_contract_rejects_hidden_activity(self):
        phase=dict(phase='frame1001',entry=dict(allocations=25482),exit=dict(allocations=25482),
                   state_delta=dict(allocated={},released=[]),bindings=[])
        self.assertTrue(e.allocator_invariants(dict(phases=[phase]))['unchanged_after_load_tail'])
        phase['bindings']=[dict(name='KERNEL32.GlobalUnlock')]
        with self.assertRaises(ValueError):
            e.allocator_invariants(dict(phases=[phase]))
        phase['bindings']=[]
        phase['state_delta']['released']=['alloc00001']
        with self.assertRaises(ValueError):
            e.allocator_invariants(dict(phases=[phase]))

    def test_opening_three_hashes_are_required(self):
        state={'dgroup':(0x494000,b'ABCD')}
        mask=e.MascaraEnderecos([['0x494001','0x494002']])
        compared,masked=e.resumos_mascarados(mask,state)
        part=dict(part=0,opening_state=dict(full_state=d.pack_state(state),summary=e.resumo_estado(state),
                                          compared_summary=compared,masked_sha256=masked))
        self.assertEqual(e.opening(part,mask),state)
        bad=copy.deepcopy(part);bad['opening_state']['masked_sha256']='0'*64
        with self.assertRaises(ValueError):
            e.opening(bad,mask)

    def test_actual_serial_state_roundtrip_is_complete(self):
        state={'dgroup':(0x494000,b'\x00ABC\xff'),'alloc00000':(0x40000000,bytes(range(256)))}
        self.assertEqual(d.unpack_state(d.pack_state(state)),state)

    def test_partial_or_dirty_shards_cannot_aggregate(self):
        manifest=e.load_manifest()
        plan=dict(manifest=dict(sha256=e.PINS[e.MANIFEST]),summary=dict(result='verified'))
        paths=[str(n) for n in range(10)]
        reports=[]
        for p in manifest['parts']:
            reports.append(dict(part=dict(number=p['part'],raw_sha256=p['raw_sha256'],first_phase=p['first_phase'],last_phase=p['last_phase'],
                                          opening={k:'same' for k in e.HASH_FIELDS},ending={k:'same' for k in e.HASH_FIELDS}),
                                manifest=dict(sha256=e.PINS[e.MANIFEST]),policy=manifest['policy'],
                                library=dict(sha256='binary'),engine_source_sha256={'source':'hash'},engine_sources_unchanged_during_run=True,
                                source_dirty_paths=[],phases=[{}]*p['phases'],summary=dict(complete_part=True,phases_equal=p['phases'],phases_compared=p['phases']),
                                allocation_records=dict(equal=True),timing=dict(rust_phase_seconds=1,frames_completed=p['frames'][1]-max(1,p['frames'][0])+1),
                                scope='declared_opening_checkpoint'))
        with patch.object(d,'read_json',side_effect=lambda p:reports[int(p)]), patch.object(d,'sha',return_value='report-hash'):
            result=d.aggregate(paths,plan)
            self.assertTrue(result['summary']['complete_proof'])
            reports[9]['summary']['complete_part']=False
            self.assertFalse(d.aggregate(paths,plan)['summary']['complete_proof'])
            reports[9]['summary']['complete_part']=True
            reports[0]['source_dirty_paths']=[' M motor/testes/example.py']
            self.assertFalse(d.aggregate(paths,plan)['summary']['complete_proof'])

    def test_serial_aggregate_requires_actual_checkpoint_chain(self):
        # The real phase proof is expensive; this validates the independent
        # aggregate guard before report I/O, rather than fabricating acceptance.
        manifest=e.load_manifest()
        self.assertEqual(manifest['parts'][0]['first_phase'],'load_tail')
        with self.assertRaises(ValueError):
            d.aggregate([],dict(manifest=dict(sha256=e.PINS[e.MANIFEST]),summary=dict(result='verified')),serial=True)


if __name__=='__main__':
    unittest.main(verbosity=2)
