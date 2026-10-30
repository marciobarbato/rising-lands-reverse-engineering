"""The native UI frame driver uses real ABI1.4 worlds; no replayed future states."""
import ctypes as C
import os
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'apps/macos-preview/src'))
from macos_native_driver import NativeDriver,NativeStatus

class NativeDriverTests(unittest.TestCase):
    def paths(self):
        driver=Path(os.environ.get('RL_MACOS_NATIVE_LIBRARY',ROOT/'apps/macos-preview/build/librising_macos_live.dylib'))
        engine=Path(os.environ.get('RL_MACOS_ENGINE_LIBRARY',ROOT/'apps/macos-preview/build/abi14-target/release/librising_engine.dylib'))
        inputs=Path(os.environ.get('RL_MACOS_NATIVE_INPUTS',ROOT/'apps/macos-preview/build/native-inputs-v2'))
        if not all(p.exists() for p in (driver,engine,inputs)):self.skipTest('Explicit ABI1.4/native input build unavailable')
        return driver,engine,inputs
    def test_real_phase_order_surface_proof_and_recreate_identity(self):
        d,e,i=self.paths();native=NativeDriver(d,e,i);self.addCleanup(native.close)
        engine=C.CDLL(str(e));engine.rl_versao.restype=C.c_uint32;engine.rl_render_contrato.restype=C.c_uint32
        self.assertEqual(engine.rl_versao(),0x10004);self.assertEqual(engine.rl_render_contrato(),0x10007)
        observed=[]
        callback=lambda ctx,world,index,phase:(observed.append((index,phase)) or 0)
        self.assertEqual(native.advance(callback),0);self.assertEqual(native.status().phases_equal,1)
        self.assertEqual(native.advance(callback),0)
        s=native.status();self.assertEqual((s.frames,s.counter,s.phases_equal,s.surfaces_equal,s.checkpoints_equal),(1,1,3,1,1))
        self.assertEqual(observed,[(0,1),(1,2),(2,3)])
        pixels=native.pixels();self.assertEqual(len(pixels),480000);self.assertEqual(len(native.palette()),768)
        native.close();native.close()
        other=NativeDriver(d,e,i);self.addCleanup(other.close);other.advance();other.advance()
        self.assertEqual(other.pixels(),pixels)
    def test_observer_failure_is_named_and_latches_without_retry(self):
        d,e,i=self.paths();native=NativeDriver(d,e,i);self.addCleanup(native.close)
        self.assertNotEqual(native.advance(lambda *args:1),0)
        before=native.status();self.assertIn(b'PhaseObserverRejected',bytes(before.message))
        native.advance();self.assertEqual(native.status().frames,before.frames)
    def test_missing_inputs_fail_without_a_fabricated_world(self):
        import tempfile
        d,e,i=self.paths()
        with tempfile.TemporaryDirectory() as empty:
            with self.assertRaisesRegex(RuntimeError,'Missing S0'):NativeDriver(d,e,empty)
