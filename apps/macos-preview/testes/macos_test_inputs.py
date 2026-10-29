"""Explicit read-only asset inputs for consumer integration tests."""
import json
import os
from pathlib import Path
import shutil
import tempfile


def graphics_inputs(test, root):
    declared = os.environ.get('RISING_APP_ROOT')
    if declared and (Path(declared)/'graphics-inputs/manifesto.json').is_file():
        return Path(declared)/'graphics-inputs'
    inputs = os.environ.get('RISING_INPUTS_ROOT')
    if not inputs:
        raise RuntimeError('Declare RISING_INPUTS_ROOT containing source/cd for Graphics integration tests')
    directory = tempfile.TemporaryDirectory()
    test.addCleanup(directory.cleanup)
    target = Path(directory.name)
    shutil.copy2(root/'pesquisas-paralelas/graficos-animacao/fontes/manifesto.json', target/'manifesto.json')
    (target/'cd').symlink_to(Path(inputs)/'source/cd', target_is_directory=True)
    return target
