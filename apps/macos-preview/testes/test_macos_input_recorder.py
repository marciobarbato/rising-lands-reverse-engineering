from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'apps/macos-preview/src'))
from macos_input_recorder import MacOSInputRecorder,InputContractPending,VKEYS

class RecorderTests(unittest.TestCase):
    def test_ordered_mouse_queue_signed_coordinates_and_poll_sites(self):
        r=MacOSInputRecorder()
        for msg in range(0x200,0x206):r.event(129,dict(kind='mouse',msg=msg,x=-2,y=599,wParam=4))
        self.assertEqual(r.poll(129,0x475044,'GetCursorPos'),dict(x=-2,y=599,result=1))
        first=r.poll(129,0x4601dd,'PeekMessageA',remove=False)
        self.assertEqual(first['message']['lParam'],599<<16|65534)
        self.assertEqual([r.poll(129,0x4601dd,'PeekMessageA')['message']['msg'] for _ in range(6)],list(range(0x200,0x206)))
        self.assertEqual(r.poll(129,0x4601dd,'PeekMessageA')['result'],0)
        self.assertEqual(len(r.journal()['polls']),9)

    def test_held_release_repeat_and_since_last_poll_for_every_declared_key(self):
        for key in VKEYS:
            r=MacOSInputRecorder();r.event(129,dict(kind='key',vkey=key,down=True))
            self.assertEqual(r.poll(129,1,'GetAsyncKeyState',key),0x8001)
            r.event(129,dict(kind='key',vkey=key,down=True))
            self.assertEqual(r.poll(129,1,'GetAsyncKeyState',key),0x8000)
            r.event(130,dict(kind='key',vkey=key,down=False))
            self.assertEqual(r.poll(130,1,'GetAsyncKeyState',key),0)

    def test_short_click_between_polls_and_atomic_bad_event(self):
        r=MacOSInputRecorder();r.event(1,dict(kind='key',vkey=88,down=True));r.event(1,dict(kind='key',vkey=88,down=False))
        self.assertEqual(r.poll(2,1,'GetAsyncKeyState',88),1)
        before=r.journal()
        with self.assertRaises(ValueError):r.event(1,dict(kind='mouse',msg=0x201,x=1,y=2))
        self.assertEqual(r.journal(),before)
        journal=r.journal();journal['events'].clear();self.assertTrue(r.events)

    def test_export_requires_owner_contract(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(InputContractPending):MacOSInputRecorder().export_script(d)

    def test_replay_preserves_interleaving_and_rejects_changed_answers(self):
        r=MacOSInputRecorder()
        r.event(129,dict(kind='key',vkey=88,down=True))
        r.poll(129,0x429278,'GetAsyncKeyState',88)
        r.event(129,dict(kind='key',vkey=88,down=False))
        r.poll(129,0x429278,'GetAsyncKeyState',88)
        r.event(130,dict(kind='mouse',msg=0x201,x=123,y=456,wParam=1))
        r.poll(130,0x4601dd,'PeekMessageA',remove=False)
        r.poll(130,0x4601dd,'PeekMessageA')
        journal=r.journal()
        self.assertEqual(MacOSInputRecorder.replay(journal).journal(),journal)
        journal['polls'][0]['answer']^=1
        with self.assertRaisesRegex(ValueError,'differs on replay'):MacOSInputRecorder.replay(journal)
