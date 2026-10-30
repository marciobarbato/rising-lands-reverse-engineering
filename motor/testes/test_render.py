"""Run Graphics' flat-import reference in a fresh consumer process."""
from pathlib import Path
import subprocess
import sys
import unittest

class NativeRendererTests(unittest.TestCase):
    def test_graphics_15_contract_original_pixels_and_explicit_stops(self):
        script=Path(__file__).with_name('render_contract_checks.py')
        result=subprocess.run([sys.executable,'-B',str(script),'-v'])
        self.assertEqual(result.returncode,0)

if __name__=='__main__':unittest.main()
