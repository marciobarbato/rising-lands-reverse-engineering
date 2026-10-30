"""Bundle-source regression tests without native tools or generated game assets."""
import importlib.util
import json
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

APP = Path(__file__).resolve().parents[1]
ROOT = APP.parents[1]


def load_script(name, filename):
    spec = importlib.util.spec_from_file_location(name, APP / 'scripts' / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load_script('_test_macos_bundle_builder', 'build.py')
verifier = load_script('_test_macos_bundle_verifier', 'playable_verify.py')


class MacOSBundleTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.app = Path(self.directory.name) / 'RisingLands-ptbr.app'
        self.payload = self.app / 'Contents/Resources/preview'
        self.payload.mkdir(parents=True)
        source = self.payload / 'source/apps/macos-preview/src'
        shutil.copytree(APP / 'src', source)
        builder.copy_preview_sources(source, self.payload)
        (self.payload / 'snapshot.json').write_text(json.dumps(dict(
            snapshot='source', commit='fixture', files=[])))
        (self.app / 'Contents/Info.plist').write_bytes(plistlib.dumps(dict(
            RisingLandsSourceCommit='fixture', CFBundleDisplayName='RisingLands-ptbr')))
        (self.payload / 'assets').mkdir()
        (self.payload / 'assets/fontes.json').write_text(json.dumps(dict(commit='fixture', outputs=[])))
        # Explicit soundless audio payload; verify() re-hashes every listed file.
        (self.payload / 'audio').mkdir()
        (self.payload / 'audio/manifest.json').write_text(json.dumps(dict(files={}, audio=dict(status='absent'))))

    def verify_sources(self):
        # Only the unrelated game-runtime navigation subprocess is substituted.
        # verify() performs its actual source-inventory and byte checks first.
        runtime = dict(commit='fixture', prefix=str(self.app / 'Contents/Resources/Python'),
                       modules=[str(self.payload / 'macos_state_consumer.py')])
        with patch.object(verifier.subprocess, 'run', return_value=subprocess.CompletedProcess(
                [], 0, json.dumps(runtime), '')):
            return verifier.verify(self.app)

    def run_consumer(self, code):
        script = 'import sys; sys.path.insert(0, sys.argv[1]); import macos_state_consumer as c; ' + code
        return subprocess.run([sys.executable, '-I', '-B', '-c', script, str(self.payload)],
                              capture_output=True, text=True, timeout=15)

    def add_evidence(self):
        for name in ('integracao/validacao/cxr-20261028-08-m1-acceptance.json',
                     'pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json',
                     'pesquisas-paralelas/missoes/mapa_memoria_m1.py'):
            destination = self.payload / 'source' / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, destination)

    def test_shared_packager_satisfies_real_verifier(self):
        self.assertTrue((self.payload / 'macos_state_consumer.py').is_file())
        self.assertTrue((self.payload / 'playable_session.py').is_file())
        self.assertFalse((self.payload / 'native/main.swift').exists())
        self.assertEqual(self.verify_sources()['commit'], 'fixture')

    def test_real_verifier_detects_modified_audio_payload(self):
        (self.payload / 'audio/A.HED').write_bytes(b'ABCD')
        (self.payload / 'audio/manifest.json').write_text(json.dumps(dict(files={'A.HED': '0' * 64}, audio=dict(status='absent'))))
        with self.assertRaises(AssertionError):
            self.verify_sources()

    def test_real_verifier_detects_original_missing_consumer_regression(self):
        (self.payload / 'macos_state_consumer.py').unlink()
        with self.assertRaises(FileNotFoundError):
            self.verify_sources()

    def test_real_verifier_still_detects_modified_mirrored_source(self):
        path = self.payload / 'macos_state_consumer.py'
        path.write_bytes(path.read_bytes() + b'\n# modified\n')
        with self.assertRaises(AssertionError):
            self.verify_sources()

    def test_bundled_default_reads_declared_archive(self):
        self.add_evidence()
        result = self.run_consumer('print(len(c.load_accepted_m1().blocks))')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), '881')

    def test_deployed_module_without_manifest_refuses_ancestor_guess(self):
        (self.payload / 'snapshot.json').unlink()
        result = self.run_consumer('c.load_accepted_m1()')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('No source archive declared', result.stderr)
        # An explicit archive root remains supported for developer inspection.
        self.add_evidence()
        result = self.run_consumer('print(len(c.load_accepted_m1(__import__("pathlib").Path(sys.argv[1])/"source").blocks))')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), '881')

    def test_bundle_cannot_select_external_or_malformed_archive(self):
        outside = Path(self.directory.name) / 'external'
        outside.mkdir()
        (self.payload / 'external-link').symlink_to(outside, target_is_directory=True)
        for snapshot in ('../outside', str(outside), 'external-link', '.', '', None):
            with self.subTest(snapshot=snapshot):
                (self.payload / 'snapshot.json').write_text(json.dumps(dict(snapshot=snapshot)))
                result = self.run_consumer('c.load_accepted_m1()')
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Unable to validate M1 state', result.stderr)
        (self.payload / 'snapshot.json').write_text('{')
        result = self.run_consumer('c.load_accepted_m1()')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Unable to validate M1 state', result.stderr)

    def test_declared_archive_missing_evidence_does_not_fall_back(self):
        result = self.run_consumer('c.load_accepted_m1()')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Unable to validate M1 state', result.stderr)
