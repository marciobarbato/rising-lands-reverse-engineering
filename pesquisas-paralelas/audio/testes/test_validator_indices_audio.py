"""CLI/output preflight regression tests; no original instruction is executed."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

OWNED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNED))
SPEC=importlib.util.spec_from_file_location('_test_audio_slot_validator',OWNED/'validar_indices_fila_audio.py')
validator=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(validator)


class QueueValidatorCLITests(unittest.TestCase):
    def test_help_exposes_output_and_missing_argument_refuses(self):
        script=str(OWNED/'validar_indices_fila_audio.py')
        help_result=subprocess.run([sys.executable,'-B',script,'--help'],capture_output=True,text=True)
        self.assertEqual(help_result.returncode,0,help_result.stderr)
        self.assertIn('--output',help_result.stdout)
        missing=subprocess.run([sys.executable,'-B',script],capture_output=True,text=True)
        self.assertEqual(missing.returncode,2)
        self.assertIn('--output',missing.stderr)

    def test_existing_file_or_dangling_link_refuses_before_capture(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            existing=root/'existing.json';existing.write_text('preserved evidence')
            link=root/'dangling.json';link.symlink_to(root/'missing-target')
            for target in (existing,link):
                with self.subTest(target=target),patch.object(validator,'original_capture') as capture:
                    with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit) as raised:
                        validator.main(['--output',str(target)])
                    self.assertEqual(raised.exception.code,2)
                    capture.assert_not_called()
            self.assertEqual(existing.read_text(),'preserved evidence')
            self.assertFalse((root/'missing-target').exists())

    def test_fresh_output_path_works_without_native_execution(self):
        # Exercise actual comparison/report generation; only the capture is a mock.
        original=json.loads((OWNED/'evidencias/captura-indices-fila-audio-original.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'new/repeat.json'
            with patch.object(validator,'original_capture',return_value=original) as capture:
                with contextlib.redirect_stdout(io.StringIO()):validator.main(['--output',str(output)])
            capture.assert_called_once_with()
            report=json.loads(output.read_text())
            self.assertTrue(report['passed'])
            self.assertEqual(report['native_calls'],133)

    def test_late_output_race_keeps_the_other_report(self):
        original=json.loads((OWNED/'evidencias/captura-indices-fila-audio-original.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'race.json'
            def competing_capture():
                output.write_text('another completed report')
                return original
            with patch.object(validator,'original_capture',side_effect=competing_capture):
                with self.assertRaises(FileExistsError):validator.main(['--output',str(output)])
            self.assertEqual(output.read_text(),'another completed report')
