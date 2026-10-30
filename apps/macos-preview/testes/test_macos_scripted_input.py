"""Test A answer requests, frame semantics and record-only human export."""
from pathlib import Path
import copy,json,sys,unittest
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'apps/macos-preview/src'));sys.path.insert(0,str(ROOT/'apps/macos-preview/scripts'))
from macos_scripted_input import ScriptedInput,FrameAnswerMapper,MacOSSessionRecorder,VKEYS,owner_contract
from validate_macos_input import compare_probe,PROBES

class ScriptedInputTests(unittest.TestCase):
    def test_all_native_probe_answer_requests_and_canonical_roundtrips(self):
        counts=(7522,9034,45032,33873,53099,7037)
        for name,count in zip(PROBES,counts):
            with self.subTest(probe=name):
                r=compare_probe(ROOT,name);self.assertEqual(r['answers'],count);self.assertTrue(r['equal'],r['first_difference']);self.assertTrue(r['roundtrip_equal']);self.assertEqual(r['actual_answers_sha256'],r['expected_answers_sha256'])

    def test_cursor_holds_keys_reset_and_literal_key_answer_repeats(self):
        s=ScriptedInput(ROOT,dict(schema='rising-lands/monde01-scripted-input/1',start={'frame':128},stop_frame=135,frames=[dict(frame=129,cursor=[45,56],keys={'0x11':-32767})]))
        m=FrameAnswerMapper(s,hwnd=0);m.begin_frame(129)
        for site in (0x4295fc,0x42a042):self.assertEqual(m.poll('key',phase='frame129',site=site,vk=17)['value'],-32767)
        self.assertEqual(m.poll('key',phase='frame129',site=1,vk=0x45)['value'],0)
        m.begin_frame(135);self.assertEqual(m.poll('cursor',phase='between_frames135',site=0x47504b)['x'],45);self.assertEqual(m.poll('key',phase='frame135',site=1,vk=17)['value'],0)

    def test_message_peek_get_translate_dispatch_and_unconsumed_rejection(self):
        s=ScriptedInput(ROOT,json.loads((ROOT/'pesquisas-paralelas/missoes/m3/entradas/P1.json').read_bytes()));m=FrameAnswerMapper(s,hwnd=123)
        m.begin_frame(130);first=m.poll('peek_message',phase='between_frames130',site=1)
        self.assertEqual(first,m.poll('peek_message',phase='between_frames130',site=1))
        with self.assertRaisesRegex(ValueError,'Unconsumed'):m.begin_frame(131)
        self.assertEqual(m.poll('get_message',phase='between_frames130',site=2)['message'],first['message'])
        with self.assertRaisesRegex(ValueError,'Translate'):m.poll('dispatch_message',phase='between_frames130',site=3)
        m.poll('translate_message',phase='between_frames130',site=3)
        self.assertEqual(m.poll('dispatch_message',phase='between_frames130',site=4)['hwnd'],123)
        m.finish()
        with self.assertRaisesRegex(ValueError,'phase/frame'):m.poll('cursor',phase='frame129',site=1)

    def test_human_click_cadence_cursor_hold_ctrl_and_canonical_export(self):
        r=MacOSSessionRecorder(ROOT);r.event(129,dict(kind='key',vkey=17,down=True))
        r.event(130,dict(kind='mouse',msg=0x201,x=400,y=272,wParam=8))
        r.event(131,dict(kind='mouse',msg=0x200,x=500,y=300))
        r.event(132,dict(kind='mouse',msg=0x202,x=400,y=272))
        r.event(140,dict(kind='key',vkey=17,down=False))
        s=r.export_script(stop_frame=145);owner_contract(str(ROOT))[0]['carregar_entrada'](s.export())
        self.assertEqual([s.frames[f][1][0][0] for f in (130,131,133)],[0x200,0x201,0x202])
        self.assertEqual(s.frames[134][0],(500,300));self.assertEqual(s.frames[139][2],{17:-32768});self.assertEqual(s.frames[140][2],{})
        m=FrameAnswerMapper(s,hwnd=0)
        for f in range(129,146):
            m.begin_frame(f)
            if 130<=f<=133:self.assertEqual(m.cursor,(400,272))
            while m.poll('peek_message',phase=f'between_frames{f}',site=1)['message'] is not None:
                for kind in ('get_message','translate_message','dispatch_message'):m.poll(kind,phase=f'between_frames{f}',site=2)
        m.finish();self.assertEqual(s.export_bytes(),ScriptedInput(ROOT,s.export_bytes()).export_bytes())

    def test_all_mac_keys_and_buttons_have_declared_messages_and_rejected_events_are_atomic(self):
        r=MacOSSessionRecorder(ROOT)
        for f,key in enumerate(VKEYS,129):r.event(f,dict(kind='key',vkey=key,down=True))
        for f,key in enumerate(VKEYS,150):r.event(f,dict(kind='key',vkey=key,down=False))
        r.event(170,dict(kind='mouse',msg=0x204,x=10,y=20));r.event(171,dict(kind='mouse',msg=0x203,x=30,y=40))
        s=r.export_script();msgs={m[0] for _,rows,_ in s.frames.values() for m in rows}
        self.assertTrue({0x100,0x101,0x200,0x203,0x204,0x205}.issubset(msgs));before=copy.deepcopy(r.journal())
        for frame,event in [(128,dict(kind='key',vkey=17,down=True)),(180,dict(kind='key',vkey=49,down=True)),(180,dict(kind='mouse',msg=0x201,x=800,y=1))]:
            with self.assertRaises(ValueError):r.event(frame,event)
            self.assertEqual(r.journal(),before)
        with self.assertRaisesRegex(ValueError,'truncates'):r.export_script(stop_frame=171)

    def test_owner_rejects_bad_interchange_and_import_is_independent(self):
        data=json.loads((ROOT/'pesquisas-paralelas/missoes/m3/entradas/P1.json').read_bytes());s=ScriptedInput(ROOT,data);data['frames'].clear();self.assertTrue(s.frames)
        bad=s.export();bad['frames'][0]['messages'][0][0]=0x102
        with self.assertRaises(ValueError):ScriptedInput(ROOT,bad)
        with self.assertRaises(ValueError):FrameAnswerMapper(s,hwnd=None)

    def test_full_missions_harness_module_accepts_human_export_unchanged(self):
        import subprocess,tempfile
        r=MacOSSessionRecorder(ROOT);r.event(129,dict(kind='mouse',msg=0x201,x=400,y=272))
        raw=r.export_script().export_bytes()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'input.json';p.write_bytes(raw)
            code="import runpy,json,sys; owner=runpy.run_path(sys.argv[1],run_name='macos_owner_validator'); rows,end=owner['carregar_entrada'](json.load(open(sys.argv[2]))); assert end==132 and len(rows)==3"
            result=subprocess.run([sys.executable,'-I','-B','-c',code,str(ROOT/'pesquisas-paralelas/missoes/m3/entrada_roteirizada.py'),str(p)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(p.read_bytes(),raw)
