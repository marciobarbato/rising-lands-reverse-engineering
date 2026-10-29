"""Consumer proof uses the real Rust dylib; missing build is an explicit skip."""
import ctypes as C
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'apps/macos-preview/src'))
from macos_live_session import MacOSLiveSession,masked_summary
from macos_rust_abi import FrameInput,FrameRegisters,FrameEvent,unpack_blocks

class LiveTests(unittest.TestCase):
    def test_copied_layout_and_strict_bulk_decoder(self):
        import struct
        self.assertEqual(C.sizeof(FrameInput),72);self.assertEqual(C.sizeof(FrameEvent),72)
        self.assertEqual(FrameInput.registers.offset,12)
        raw=struct.pack('<III',1,0x100,2)+b'ab'
        self.assertEqual(unpack_blocks(raw),{0x100:b'ab'})
        for bad in (b'',raw[:-1],raw+b'x',struct.pack('<III',1,0x100,0)):
            with self.assertRaises(ValueError):unpack_blocks(bad)

    def test_mask_uses_original_addresses_and_keeps_unmasked_corruption(self):
        s={'b':(100,b'abcdef'),'a':(10,b'xyz')}
        digest=masked_summary(s,[(101,103)])
        self.assertEqual(digest,masked_summary({'b':(100,b'a!!def'),'a':(10,b'xyz')},[(101,103)]))
        self.assertNotEqual(digest,masked_summary({'b':(100,b'a!!deZ'),'a':(10,b'xyz')},[(101,103)]))

    def test_named_abi_failure_latches_without_publishing_or_retry(self):
        live=object.__new__(MacOSLiveSession)
        live.stop=None;live.index=-1;live.current=object();live.handle=7
        live.inputs=object();live.abi=Mock();live.abi.frame.side_effect=RuntimeError('UnsupportedPath CalculWorkEngin 0x44bc74')
        before=live.current
        self.assertIs(live.apply_frame(),before)
        self.assertIn('CalculWorkEngin',live.stop['detail'])
        self.assertEqual(live.index,-1)
        live.apply_frame();self.assertEqual(live.abi.frame.call_count,1)

    def test_failed_fast_render_preserves_published_image_and_full_read_buffer(self):
        from types import SimpleNamespace as NS
        from macos_state_consumer import StateValidationError
        live=object.__new__(MacOSLiveSession)
        before=NS(identity='published');published=Mock()
        candidate=Mock();candidate.update.return_value=candidate
        candidate.masked_summary.return_value='hash'
        live.stop=None;live.index=-1;live.current=before;live.bulk=published
        live.bulks=[candidate,Mock()];live.views=[Mock(),Mock()]
        live.handle=7;live.inputs=object();live.abi=Mock()
        live.names={};live.static={};live.ranges=[];live.expected=['hash']
        live.renderer=NS(api=object(),consume=Mock(side_effect=StateValidationError('surface mismatch')))
        self.assertIs(live.apply_frame(),before)
        self.assertIs(live.bulk,published)
        self.assertEqual(live.index,-1)
        self.assertIn('surface mismatch',live.stop['detail'])
        live.apply_frame();self.assertEqual(live.abi.frame.call_count,1)

    def test_real_rust_s0_three_phases_reset_and_owned_lifetime(self):
        library=Path(os.environ.get('RL_MACOS_ENGINE_LIBRARY',ROOT/'motor/target/release/librising_engine.dylib'))
        executable=Path(os.environ.get('RL_ORIGINAL_EXE','/Users/marcio/git/Rising Lands/source/cd/INSTALHD/RISING.EXE'))
        if not library.is_file() or not executable.is_file():self.skipTest('Native Rust build/original table input unavailable')
        live=MacOSLiveSession(ROOT,library,executable)
        self.addCleanup(live.close)
        identity=live.current.identity
        for _ in range(3):live.apply_frame()
        self.assertIsNone(live.stop,live.stop)
        self.assertEqual(live.current.phase_name,'frame1')
        self.assertEqual([r['state_equal'] for r in live.records],[True]*3)
        self.assertEqual(live.abi.clock(live.handle)[0],2)
        first=live.current.summary_sha256
        old=live.handle;live.reset();self.assertNotEqual(live.handle,old)
        self.assertEqual(live.current.identity,identity)
        for _ in range(3):live.apply_frame()
        self.assertEqual(live.current.summary_sha256,first)
        live.close();self.assertIsNone(live.handle)
