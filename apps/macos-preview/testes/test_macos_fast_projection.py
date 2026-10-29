"""Persistent-buffer proof guards: no copied blocks, stale aliases or masked logic."""
import ctypes as C
from pathlib import Path
import struct
import sys
from types import SimpleNamespace as NS
import unittest
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'apps/macos-preview/src'))
from macos_fast_projection import MacOSBulkProjection,MacOSGraphicsView
from macos_live_session import masked_summary
from macos_state_consumer import StateValidationError


def packed(blocks):
    return struct.pack('<I',len(blocks))+b''.join(struct.pack('<II',a,len(b))+b for a,b in blocks)


class BulkTests(unittest.TestCase):
    def bulk(self,blocks,capacity=1000):
        payload=[packed(blocks)]
        def project(handle,out,size,required):
            C.cast(required,C.POINTER(C.c_uint32))[0]=len(payload[0])
            if size<len(payload[0]):return 6
            C.memmove(out,payload[0],len(payload[0]));return 0
        def check(code):
            if code:raise RuntimeError(str(code))
        abi=NS(lib=NS(rl_projetar_tudo=project),check=check)
        bulk=MacOSBulkProjection(abi,capacity)
        return bulk,payload

    def test_reuses_foreign_buffer_and_hashes_all_bytes_with_original_mask(self):
        state={'z':(100,b'abcdef'),'a':(10,b'xyz')}
        bulk,payload=self.bulk(sorted(state.values()))
        original=bulk.foreign
        bulk.update(1)
        ranges=[(101,103)]
        self.assertEqual(bulk.masked_summary({100:'z',10:'a'},{},ranges),masked_summary(state,ranges))
        payload[0]=packed([(10,b'xyz'),(100,b'a!!def')]);bulk.update(1)
        self.assertIs(bulk.foreign,original)
        self.assertEqual(bulk.allocations,1);self.assertEqual(bulk.calls,2)
        self.assertEqual(bulk.masked_summary({100:'z',10:'a'},{},ranges),masked_summary(state,ranges))
        payload[0]=packed([(10,b'xyZ'),(100,b'a!!def')]);bulk.update(1)
        self.assertNotEqual(bulk.masked_summary({100:'z',10:'a'},{},ranges),masked_summary(state,ranges))

    def test_region_slots_are_isolated_read_only_reused_and_preflighted(self):
        bulk,payload=self.bulk([(100,b'abcdefgh')]);bulk.update(1)
        api=NS(regioes_necessarias=lambda m,hud:[(102,106,'declared')])
        a,b=MacOSGraphicsView('source'),MacOSGraphicsView('source')
        a.capture(bulk,api,0,'load_tail','hash',False)
        slot=a.regions[0][1]
        payload[0]=packed([(100,b'XXXXXXXX')]);bulk.update(1)
        b.capture(bulk,api,1,'between_frames','next',False)
        self.assertEqual(a.read(102,4),b'cdef');self.assertEqual(b.read(102,4),b'XXXX')
        with self.assertRaises(TypeError):a.read(102,1)[0]=0
        with self.assertRaises(StateValidationError):a.read(100,1)
        a.capture(bulk,api,2,'frame1','third',True)
        self.assertIs(a.regions[0][1],slot);self.assertEqual(a.allocations,1)
        with self.assertRaises(StateValidationError):a.capture(bulk,NS(regioes_necessarias=lambda m,hud:[(999,1000,'missing')]),3,'bad','bad',False)

    def test_growth_and_malformed_descriptors_fail_explicitly(self):
        bulk,payload=self.bulk([(100,b'abcdefgh')],capacity=4);bulk.update(1)
        self.assertEqual(bulk.allocations,2);self.assertEqual(bulk.read(100,8),b'abcdefgh')
        for bad in (b'bad',packed([(100,b'abc'),(101,b'z')]),packed([(2**32-1,b'ab')]),packed([(1,b'a')])+b'x'):
            payload[0]=bad
            with self.assertRaises(StateValidationError):bulk.update(1)
