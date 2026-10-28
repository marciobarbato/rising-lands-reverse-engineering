"""Verify source binding, generated assets and isolated bundle runtime paths."""
import hashlib
import json
import os
from pathlib import Path
import plistlib
import subprocess


def verify(app):
    payload = app / 'Contents/Resources/preview'
    manifest = json.loads((payload / 'snapshot.json').read_text())
    plist = plistlib.loads((app / 'Contents/Info.plist').read_bytes())
    assert plist['RisingLandsSourceCommit'] == manifest['commit']
    assert plist['CFBundleDisplayName'] == 'RisingLands-ptbr'
    for entry in manifest['files']:
        file = payload / 'source' / entry['path']
        assert file.is_file() and not file.is_symlink(), str(file)
        assert hashlib.sha256(file.read_bytes()).hexdigest() == entry['sha256'], str(file)
    for file in (payload / 'source/apps/macos-preview/src').rglob('*'):
        if file.is_file() and file.suffix in ('.py', '.html', '.css', '.js'):
            assert file.read_bytes() == (payload / file.relative_to(payload / 'source/apps/macos-preview/src')).read_bytes(), str(file)
    assets = json.loads((payload / 'assets/fontes.json').read_text())
    assert assets['commit'] == manifest['commit']
    for entry in assets['outputs']:
        assert hashlib.sha256((payload / 'assets' / entry['path']).read_bytes()).hexdigest() == entry['sha256']
    runtime = app / 'Contents/Resources/Python/bin/python3'
    environment = {k: v for k, v in os.environ.items() if k not in ('RISING_APP_ROOT', 'PYTHONHOME', 'PYTHONPATH')}
    code = """import sys,json,pathlib
root=pathlib.Path(sys.argv[1]);sys.path.insert(0,str(root))
import engine,research_adapter,navegacao_unidades,economia,alvos_alcance
p=engine.Preview();p.reset('jogavel');p.order(0,9,4)
for i in range(4):p.step(200)
assert p.state()['units'][0]['pos']==[9,4]
print(json.dumps({'prefix':sys.prefix,'commit':engine.MANIFEST['commit'],
'modules':[m.__file__ for m in (engine,research_adapter,navegacao_unidades,economia,alvos_alcance)]}))
"""
    result = subprocess.run([str(runtime), '-I', '-B', '-c', code, str(payload)],
                            env=environment, capture_output=True, text=True, timeout=30)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    paths = json.loads(result.stdout)
    assert paths['commit'] == manifest['commit']
    assert Path(paths['prefix']).is_relative_to(app)
    assert all(Path(p).is_relative_to(app) for p in paths['modules'])
    return paths
