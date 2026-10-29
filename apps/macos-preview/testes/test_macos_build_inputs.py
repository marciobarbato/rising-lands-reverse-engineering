"""Launcher preflight must fail precisely and keep outputs local to the clone."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]


class MacOSBuildInputTests(unittest.TestCase):
    def test_explicit_missing_inputs_fail_before_creating_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'compilar-jogável'),
                                     '--development-ref', 'HEAD', '--inputs-root', str(root/'inputs'),
                                     '--data-root', str(root/'outputs')], cwd=ROOT,
                                    env={k:v for k,v in os.environ.items() if k != 'RISING_PYTHON_RUNTIME'},
                                    capture_output=True, text=True, timeout=15)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('RISING_PYTHON_RUNTIME', result.stderr)
            self.assertIn(str(root/'inputs/source/cd/INSTALHD/PLATGAME.PIE'), result.stderr)
            self.assertFalse((root/'outputs').exists())
