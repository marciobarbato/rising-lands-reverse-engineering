"""Exercise the exact native state machine with a controlled monotonic clock."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

APP=Path(__file__).resolve().parents[1]
ROOT=APP.parents[1]


class SmokeReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        output=Path(os.environ.get('RISING_APP_ROOT',str(ROOT/'.local/smoke-tests')))/'build/tmp'
        output.mkdir(parents=True,exist_ok=True)
        cls.directory=tempfile.TemporaryDirectory(dir=output)
        folder=Path(cls.directory.name)
        harness=folder/'main.swift'
        harness.write_text('''import Foundation
let scenario=CommandLine.arguments[1]
var s=SmokeReadiness(launched:100)
func check(_ value:Bool) { if !value { fatalError("readiness invariant") } }
switch scenario {
case "late-ready":
 s.windowVisible(101);s.documentLoaded(102)
 check(s.timeout(149)==nil);check(s.phase=="initializing")
 s.ready(155);check(s.startChecks(155));check(s.timeout(199)==nil)
 check(s.timeout(200)=="checks_timeout")
case "hung-initialization":
 s.windowVisible(101);s.documentLoaded(102)
 check(!s.startChecks(110));check(s.timeout(189)==nil)
 check(s.timeout(190)=="initialization_timeout")
case "no-window":
 check(s.timeout(145)=="window_timeout");s.windowVisible(146)
 check(s.timeout(146)=="window_timeout")
case "ready-before-document":
 s.windowVisible(101);s.ready(102);check(!s.startChecks(103))
 s.documentLoaded(104);check(s.startChecks(104));check(!s.startChecks(105))
case "late-ready-refused":
 s.windowVisible(101);s.documentLoaded(102);s.ready(191)
 check(!s.startChecks(191));check(s.timeout(191)=="initialization_timeout")
default: fatalError("unknown scenario")
}
print("passed")
''')
        cls.binary=folder/'readiness-test'
        result=subprocess.run(['xcrun','swiftc','-module-cache-path',str(folder/'module-cache'),
                                str(APP/'src/native/SmokeReadiness.swift'),str(harness),'-o',str(cls.binary)],
                               capture_output=True,text=True,timeout=60)
        if result.returncode: raise RuntimeError(result.stdout+result.stderr)

    @classmethod
    def tearDownClass(cls):cls.directory.cleanup()

    def scenario(self,name):
        result=subprocess.run([str(self.binary),name],capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(result.stdout.strip(),'passed')

    def test_loaded_initialization_does_not_spend_check_budget(self):self.scenario('late-ready')
    def test_visible_hung_app_still_fails_bounded_initialization(self):self.scenario('hung-initialization')
    def test_missing_window_fails_earlier(self):self.scenario('no-window')
    def test_checks_require_document_and_ready_and_start_once(self):self.scenario('ready-before-document')
    def test_late_ready_cannot_extend_initialization_deadline(self):self.scenario('late-ready-refused')


class NativeSmokeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('macos_native_smoke_test',APP/'scripts/native_smoke.py')
        cls.tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.tool)

    def test_retry_preserves_failure_json_and_paired_images(self):
        with tempfile.TemporaryDirectory() as directory:
            report=Path(directory)/'smoke.json';image=report.with_suffix('.png')
            report.write_text('{"passed":false,"error":"old failure"}')
            for p in (image,image.with_suffix('.before.png'),image.with_suffix('.after.png')):p.write_bytes(b'old snapshot')
            archive=self.tool.preserve_evidence(report,image)
            self.assertFalse(report.exists())
            self.assertEqual(json.loads((archive/report.name).read_text())['error'],'old failure')
            self.assertEqual(len(list(archive.iterdir())),4)

    def test_outer_timeout_keeps_specific_app_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            report=Path(directory)/'smoke.json'
            def timeout(*args,**kwargs):
                report.write_text('{"passed":false,"error":"initialization_timeout"}')
                raise subprocess.TimeoutExpired(args[0],165)
            with patch.object(self.tool.subprocess,'run',side_effect=timeout):
                code,result,_,_=self.tool.run_native_smoke(Path(directory)/'app',report,report.with_suffix('.png'),{})
            self.assertEqual(code,-1);self.assertEqual(result['error'],'initialization_timeout')

    def test_missing_native_output_has_failure_json(self):
        with tempfile.TemporaryDirectory() as directory:
            report=Path(directory)/'smoke.json'
            with patch.object(self.tool.subprocess,'run',side_effect=subprocess.TimeoutExpired('open',165)):
                code,result,_,_=self.tool.run_native_smoke(Path(directory)/'app',report,report.with_suffix('.png'),{})
            self.assertEqual(code,-1);self.assertFalse(result['passed']);self.assertTrue(report.is_file())

    def test_checks_cannot_pass_without_paired_native_screenshots(self):
        with tempfile.TemporaryDirectory() as directory:
            report=Path(directory)/'smoke.json'
            def success(*args,**kwargs):
                report.write_text('{"passed":true}')
                return subprocess.CompletedProcess(args[0],0,'','')
            with patch.object(self.tool.subprocess,'run',side_effect=success):
                _,result,_,_=self.tool.run_native_smoke(Path(directory)/'app',report,report.with_suffix('.png'),{})
            self.assertFalse(result['passed']);self.assertTrue(result['appResultPassed'])
            self.assertEqual(len(result['missingCaptures']),3)
