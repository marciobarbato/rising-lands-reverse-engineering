"""The native UI frame driver uses real ABI1.6 worlds; no replayed future states."""
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
        engine=Path(os.environ.get('RL_MACOS_ENGINE_LIBRARY',ROOT/'apps/macos-preview/build/abi16-target/release/librising_engine.dylib'))
        inputs=Path(os.environ.get('RL_MACOS_NATIVE_INPUTS',ROOT/'apps/macos-preview/build/native-inputs-v2'))
        if not all(p.exists() for p in (driver,engine,inputs)):self.skipTest('Explicit ABI1.6/native input build unavailable')
        return driver,engine,inputs
    def test_real_phase_order_surface_proof_and_recreate_identity(self):
        d,e,i=self.paths();native=NativeDriver(d,e,i);self.addCleanup(native.close)
        engine=C.CDLL(str(e));engine.rl_versao.restype=C.c_uint32;engine.rl_render_contrato.restype=C.c_uint32
        self.assertEqual(engine.rl_versao(),0x10006);self.assertEqual(engine.rl_render_contrato(),0x10007)
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

    def test_play_mode_has_identical_state_and_pixels_without_proof_or_observers(self):
        import hashlib
        from macos_rust_abi import Frames
        d,e,i=self.paths()
        play=NativeDriver(d,e,i);proof=NativeDriver(d,e,i)
        self.addCleanup(play.close);self.addCleanup(proof.close)
        self.assertEqual(play.lib.macos_live_validation(play.handle,0),0)
        f=Frames(e)
        mode=C.c_uint32()
        for native,expected in ((play,1),(proof,0)):
            self.assertEqual(f.lib.rl_execucao_modo(native.status().world,C.byref(mode)),0)
            self.assertEqual(mode.value,expected)
        calls=[]
        for _ in range(129):
            self.assertEqual(play.advance(lambda *args:(calls.append(args) or 1)),0)
            self.assertEqual(proof.advance(),0)
            self.assertEqual(play.pixels(),proof.pixels())
            self.assertEqual(play.palette(),proof.palette())
        s=play.status();self.assertEqual((s.frames,s.phases_equal,s.surfaces_equal,s.checkpoints_equal,s.proof_ns),(128,0,0,0,0))
        self.assertEqual(calls,[])
        self.assertNotEqual(play.lib.macos_live_validation(play.handle,1),0)
        f=Frames(e)
        def projection(world):
            n=C.c_uint32();f.lib.rl_projetar_tudo(world,None,0,C.byref(n))
            out=(C.c_uint8*n.value)()
            self.assertEqual(f.lib.rl_projetar_tudo(world,out,n.value,C.byref(n)),0)
            return hashlib.sha256(bytes(out)).hexdigest()
        self.assertEqual(projection(s.world),projection(proof.status().world))

    def test_native_human_mapper_matches_script_mapper_on_every_phase(self):
        from macos_scripted_input import MacOSSessionRecorder,FrameAnswerMapper
        from macos_rust_abi import Frames
        d,e,i=self.paths();human=NativeDriver(d,e,i);scripted=NativeDriver(d,e,i)
        self.addCleanup(human.close);self.addCleanup(scripted.close)
        for driver in (human,scripted):
            self.assertEqual(driver.lib.macos_live_validation(driver.handle,0),0)
            for _ in range(129):self.assertEqual(driver.advance(),0)
        events=[(130,dict(kind='mouse',msg=0x201,x=560,y=528,wParam=0)),
                (131,dict(kind='mouse',msg=0x202,x=560,y=528,wParam=0)),
                (134,dict(kind='mouse',msg=0x200,x=400,y=272,wParam=0)),
                (136,dict(kind='key',vkey=17,down=True)),(138,dict(kind='key',vkey=17,down=False)),
                (139,dict(kind='mouse',msg=0x204,x=400,y=272,wParam=0)),
                (140,dict(kind='mouse',msg=0x205,x=400,y=272,wParam=0))]
        recorder=MacOSSessionRecorder(ROOT)
        for frame,event in events:recorder.event(frame,event)
        mapper=FrameAnswerMapper(recorder.export_script(stop_frame=148),hwnd=0)
        f=Frames(e)
        for frame in range(129,149):
            for stamp,event in events:
                if stamp==frame:self.assertEqual(human.event(event),0)
            # This independent mapper supplies exactly the recorded descriptor.
            # Poll draining below concerns only the schedule, not expected answers.
            mapper.begin_frame(frame);answers=mapper.declared_answers()
            for phase in (2,3):
                self.assertEqual(human.lib.macos_live_human_phase(human.handle,phase),0)
                self.assertEqual(scripted.input_phase(phase,answers),0)
                self.assertEqual(f.snapshot(human.status().world),f.snapshot(scripted.status().world))
                self.assertEqual(bytes(human.context()),bytes(scripted.context()))
            mapper.queue.clear()  # This test compares complete states; Test A compares actual polls.
        self.assertEqual(human.status().frames,148)
        import struct
        blocks=f.snapshot(human.status().world)
        base,data=next((b,v) for b,v in blocks.items() if b<=0x508728< b+len(v))
        self.assertEqual(struct.unpack_from('<H',data,0x508728-base)[0],0)
        self.assertEqual(human.status().proof_ns,0)
