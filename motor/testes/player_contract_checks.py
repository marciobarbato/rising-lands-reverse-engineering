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
  from player_proof import static_inputs,OriginalImage,ambiente_ia_runtime
  from pathlib import Path
  image=OriginalImage(ambiente_ia_runtime.EXE,Path(ambiente_ia_runtime.EXE).with_suffix('.SBL'))
  cls.static=static_inputs(image,cls.state);cls.static[0x45ed20]=image.read(0x45ed20,0x45edc0)
 def setUp(self):
  self.h=self.native.create();self.native.load(self.h,sorted([(a,b) for name,(a,b) in self.state.items() if name!='native_stack']+list(self.static.items())))
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
 def test_persistent_modes_preserve_state_registers_clock_and_trace_policy(self):
  from player_proof import static_inputs,OriginalImage,ambiente_ia_runtime
  from pathlib import Path
  image=OriginalImage(ambiente_ia_runtime.EXE,Path(ambiente_ia_runtime.EXE).with_suffix('.SBL'))
  static=static_inputs(image,self.state);static[0x45ed20]=image.read(0x45ed20,0x45edc0)
  blocks=sorted([(a,b)for name,(a,b)in self.state.items()if name!='native_stack']+list(static.items()))
  for mode in (1,2):
   with self.subTest(mode=mode):
    other=self.native.create()
    try:
     self.native.free(self.h);self.h=self.native.create()
     self.native.load(self.h,blocks);self.native.load(other,blocks);self.native.execution(self.h,0);self.native.execution(other,mode)
     left=FrameInput.from_buffer_copy(bytes(self.inp));right=FrameInput.from_buffer_copy(bytes(self.inp))
     for _ in range(5):
      for phase in (2,3):
       self.native.check(self.native.input(self.h,phase,left));self.native.check(self.native.input(other,phase,right))
       self.assertEqual(bytes(left),bytes(right));self.assertEqual(self.native.snapshot(self.h),self.native.snapshot(other));self.assertEqual(self.native.clock(self.h),self.native.clock(other))
       events=self.native.consumed(other)
       if mode==2:self.assertEqual([bytes(e)for e in events],[bytes(e)for e in self.native.consumed(self.h)])
       else:self.assertTrue(all(e.kind>=7 for e in events))
    finally:self.native.free(other)
 def test_late_input_stop_rolls_back_every_write_and_retains_diagnostics_in_play(self):
  blocks=[]
  for name,(base,data)in self.state.items():
   if name=='native_stack':continue
   data=bytearray(data)
   if base<=0x495be0<base+len(data):data[0x495be0-base:0x495be2-base]=bytes(2)
   blocks.append((base,bytes(data)))
  for mode in (0,1,2):
   with self.subTest(mode=mode):
    self.native.load(self.h,sorted(blocks+list(self.static.items())));self.native.execution(self.h,mode)
    before=self.native.snapshot(self.h);clock=self.native.clock(self.h);raw=bytes(self.inp)
    code=self.native.input(self.h,3,self.inp);error=self.native.error()
    self.assertEqual(code,5,error);self.assertIn('CalculIconeAction structure selected',error)
    self.assertEqual(self.native.snapshot(self.h),before);self.assertEqual(self.native.clock(self.h),clock);self.assertEqual(bytes(self.inp),raw)
    self.assertTrue(inputs(self.native.consumed(self.h)))
 def test_isolated_rng_and_complete_reload_preserve_execution_policy(self):
  for mode in (1,2):
   self.native.execution(self.h,mode)
   before=self.native.snapshot(self.h);seed=Memory(before).u32(0x497164)
   self.native.step(self.h,'Random',{k:0 for k in ('EAX','EBX','ECX','EDX','ESI','EDI','EBP')})
   after=self.native.snapshot(self.h)
   expected=seed%127773*16807-(seed//127773)*2836
   if expected<=0:expected+=0x7fffffff
   self.assertEqual(Memory(after).u32(0x497164),expected)
   current=C.c_uint32();self.native.lib.rl_execucao_modo.argtypes=[C.c_uint64,C.POINTER(C.c_uint32)]
   self.native.check(self.native.lib.rl_execucao_modo(self.h,C.byref(current)));self.assertEqual(current.value,mode)
   self.native.load(self.h,sorted(before.items()))
   self.native.check(self.native.lib.rl_execucao_modo(self.h,C.byref(current)));self.assertEqual(current.value,mode)
   self.assertEqual(self.native.snapshot(self.h),before)
 def test_execution_policy_rejects_invalid_mode_without_mutation(self):
  before=self.native.snapshot(self.h);clock=self.native.clock(self.h)
  self.assertEqual(self.native.lib.rl_execucao_definir(self.h,3),1)
  self.assertEqual(self.native.snapshot(self.h),before);self.assertEqual(self.native.clock(self.h),clock)
 def test_all_previous_creation_versions_remain_supported(self):
  for v in range(0x10000,0x10007):
   h=C.c_uint64();self.native.check(self.native.lib.rl_criar_mundo(v,20,0,C.byref(h)));self.native.free(h.value)

if __name__=='__main__':unittest.main()
