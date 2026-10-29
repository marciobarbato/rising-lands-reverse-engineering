"""ABI 1.1 transactional, version and phase-output contracts."""
import ctypes as C
import struct
import unittest

from frame_abi import Frames, FrameInput, FrameEvent


class FrameContract(unittest.TestCase):
    def setUp(self):
        self.abi=Frames()
        self.world=self.abi.create()
    def tearDown(self):
        self.abi.free(self.world)
    def test_additive_creation_and_invalid_phase(self):
        old=C.c_uint64()
        self.abi.check(self.abi.lib.rl_criar_mundo(0x00010000,20,0,C.byref(old)))
        self.abi.free(old.value)
        self.abi.check(self.abi.lib.rl_criar_mundo(0x00010001,20,0,C.byref(old)))
        self.abi.free(old.value)
        inp=FrameInput()
        inp.registers.eax=0xdeadbeef
        before=bytes(inp)
        self.assertEqual(self.abi.lib.rl_passo_quadro(self.world,99,C.byref(inp)),1)
        self.assertEqual(bytes(inp),before)
        self.assertEqual(self.abi.lib.rl_passo_quadro(self.world,1,None),1)
    def test_failed_phase_preserves_world_clock_input_and_events(self):
        # Phase3 stores the cursor sprite and records SetCursorPos before the
        # unsupported mode is reached. The external transaction publishes none.
        blocks=[(0x49a010,b'\xaa\xbb'),(0x4e2f78,b'\0'),(0x5099a8,struct.pack('<HH',13,17))]
        self.abi.load(self.world,blocks)
        inp=FrameInput()
        inp.registers.eax=0xdeadbeef
        before=bytes(inp)
        self.assertEqual(self.abi.lib.rl_passo_quadro(self.world,3,C.byref(inp)),5)
        self.assertIn('CalculGame game state',self.abi.error())
        self.assertIn('0x0042c868',self.abi.error())
        self.assertEqual(bytes(inp),before)
        self.assertEqual(self.abi.snapshot(self.world),dict(blocks))
        self.assertEqual(self.abi.snapshot(self.world,freed=True),{})
        self.assertEqual(self.abi.events(self.world),[])
        self.assertEqual(self.abi.clock(self.world),(0,0))
    def test_bulk_snapshot_size_errors_copy_no_prefix(self):
        self.abi.load(self.world,[(0x60000000,b'abc')])
        required=C.c_uint32()
        output=(C.c_uint8*2)(0xaa,0xbb)
        self.assertEqual(self.abi.lib.rl_projetar_tudo(self.world,output,2,C.byref(required)),6)
        self.assertEqual(bytes(output),b'\xaa\xbb')
        self.assertEqual(required.value,15)
        self.assertEqual(self.abi.snapshot(self.world),{0x60000000:b'abc'})
        self.assertEqual(C.sizeof(FrameInput),72)
        self.assertEqual(C.sizeof(FrameEvent),72)

if __name__=='__main__':unittest.main()
