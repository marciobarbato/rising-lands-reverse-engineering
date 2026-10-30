"""ABI and declared-schema regression checks isolated from older reference profiles."""
import os
os.environ['RL_REFERENCE_PROFILE']='input'
import ctypes as C,unittest
from player_proof import Player,FrameInput,FrameRegisters,estado_quadro128,Memory
from player_abi import Event,inputs,Declared,Key

class InputContracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.cap,cls.state,cls.regs=estado_quadro128();cls.native=Player()
 def setUp(self):
  self.h=self.native.create();self.native.load(self.h,sorted((a,b) for name,(a,b) in self.state.items() if name!='native_stack'))
  self.inp=FrameInput(0,0,0,FrameRegisters.from_values({k:int(v,16) for k,v in self.regs.items()}),(C.c_uint32*3)(0,0,0),(C.c_uint32*4)(0x3000000,0,0,0))
 def tearDown(self):self.native.free(self.h)
 def test_stop_is_atomic_and_attempt_diagnostics_are_queryable(self):
  before=self.native.snapshot(self.h);clock=self.native.clock(self.h);raw=bytes(self.inp)
  code=self.native.input(self.h,3,self.inp,keys={27:-32768});error=self.native.error()
  self.assertEqual(code,5);self.assertIn('InputGame Escape held',error);self.assertIn('0x00429305',error)
  self.assertEqual(self.native.snapshot(self.h),before);self.assertEqual(self.native.clock(self.h),clock);self.assertEqual(bytes(self.inp),raw)
  log=inputs(self.native.consumed(self.h));self.assertEqual([(r['vk'],r['value']) for r in log],[(27,-32768)])
  n=C.c_uint32();self.assertEqual(self.native.lib.rl_eventos_entrada(self.h,None,0,C.byref(n)),6);self.assertEqual(n.value,1)
  event=Event();C.memset(C.byref(event),0xa5,C.sizeof(event));old=bytes(event)
  self.assertEqual(self.native.lib.rl_eventos_entrada(self.h,C.byref(event),0,C.byref(n)),6);self.assertEqual(bytes(event),old)
  self.assertEqual(inputs(self.native.consumed(self.h)),log)
  invalid=Declared();invalid.size=0
  self.assertEqual(self.native.lib.rl_passo_quadro_entrada(self.h,3,C.byref(self.inp),C.byref(invalid)),1)
  self.assertEqual(inputs(self.native.consumed(self.h)),log)
 def test_invalid_descriptor_does_not_enter_game(self):
  before=self.native.snapshot(self.h);d=Declared();d.size=C.sizeof(d)-1
  self.assertEqual(self.native.lib.rl_passo_quadro_entrada(self.h,2,C.byref(self.inp),C.byref(d)),1)
  d.size=C.sizeof(d);d.flags=1;d.cursor_x=800
  self.assertEqual(self.native.lib.rl_passo_quadro_entrada(self.h,2,C.byref(self.inp),C.byref(d)),1)
  d.flags=0;ks=(Key*2)(Key(1,0),Key(1,-32768));d.keys=ks;d.key_count=2
  self.assertEqual(self.native.lib.rl_passo_quadro_entrada(self.h,2,C.byref(self.inp),C.byref(d)),1)
  self.assertEqual(self.native.snapshot(self.h),before);self.assertEqual(self.native.consumed(self.h),[])
 def test_multiple_messages_are_consumed_in_order_and_cursor_is_held(self):
  messages=[[0x200,0,0x001401e0],[0x201,1,0x001401e0],[0x202,0,0x001401e0]]
  self.native.check(self.native.input(self.h,2,self.inp,cursor=(400,272),messages=messages))
  ev=inputs(self.native.consumed(self.h));self.assertEqual([e['message'] for e in ev if e['kind']=='get_message'],messages)
  self.assertEqual([e['message'] for e in ev if e['kind']=='peek_message'],messages+[None])
  self.assertEqual(ev[-1]['kind'],'cursor');self.assertEqual((ev[-1]['x'],ev[-1]['y']),(400,272))
  self.native.check(self.native.input(self.h,2,self.inp))
  ev=inputs(self.native.consumed(self.h));self.assertEqual((ev[-1]['x'],ev[-1]['y']),(400,272))
 def test_actual_sound_manage_clears_the_original_dirty_word(self):
  self.native.check(self.native.input(self.h,2,self.inp,cursor=(400,272),sound_boundary=False))
  after=Memory(self.native.snapshot(self.h));self.assertEqual(after.u32(0x498f5c),0)
 def test_all_previous_creation_versions_remain_supported(self):
  for v in range(0x10000,0x10006):
   h=C.c_uint64();self.native.check(self.native.lib.rl_criar_mundo(v,20,0,C.byref(h)));self.native.free(h.value)

if __name__=='__main__':unittest.main()
