"""Bundle the original sound banks' decoded samples for play-mode audio.

Inputs: the original HED indexes from the read-only CD (hash-checked against
Audio's catalogue) and the decoded WAV samples of the pinned asset release
(assets/ORIGIN.json). A present asset checkout must be exactly that release,
clean, with every sample matching its manifest hash; otherwise the build stops.
An absent checkout yields an explicit soundless bundle ("ausente"), never
replacement audio.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def asset_root(workspace):
    explicit = os.environ.get('RISING_ASSETS_ROOT')
    return Path(explicit) if explicit else Path(workspace) / 'rising-lands-assets'


def prepare_audio(source, workspace, output):
    source, workspace, output = Path(source), Path(workspace), Path(output)
    output.mkdir(parents=True, exist_ok=False)
    catalogue = json.loads((source / 'pesquisas-paralelas/audio/catalogo-amostras.json').read_bytes())
    files = {}
    for letter in 'ABP':
        hed = workspace / 'source/cd/INSTALHD/SOUND' / (letter + '.HED')
        expected = catalogue['banks'][letter + '.HED']
        data = hed.read_bytes()
        if (len(data), hashlib.sha256(data).hexdigest()) != (expected['bytes'], expected['sha256']):
            raise ValueError('Original sound index hash differs: ' + str(hed))
        (output / (letter + '.HED')).write_bytes(data)
        files[letter + '.HED'] = expected['sha256']
    origin = json.loads((source / 'assets/ORIGIN.json').read_bytes())
    root = asset_root(workspace)
    report = {'status': 'absent', 'assetsRoot': str(root), 'release': origin['release_tag'], 'samples': 0, 'bytes': 0}
    if not (root / 'manifest.json').is_file():
        (output / 'manifest.json').write_text(json.dumps({'files': files, 'audio': report}, indent=1) + '\n')
        return report
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()
    if git('rev-parse', 'HEAD') != origin['release_commit']:
        raise ValueError('Asset checkout is not the pinned release ' + origin['release_tag'])
    if git('status', '--porcelain', '--', 'manifest.json', 'data/audio'):
        raise ValueError('Asset checkout has local audio/manifest changes')
    if _sha(root / 'manifest.json') != origin['manifest_sha256']:
        raise ValueError('Asset manifest differs from ORIGIN')
    manifest = json.loads((root / 'manifest.json').read_bytes())
    samples = [o for o in manifest['outputs'] if o['category'] == 'decoded_audio_sample']
    catalogued = {(s['bank'], s['index'], s['variant']) for s in catalogue['sounds']}
    for entry in samples:
        path = Path(entry['path'])
        if path.parts[0] != 'audio' or len(path.parts) != 3 or (entry['bank'], entry['index'], int(path.stem.split('-v')[1])) not in catalogued:
            raise ValueError('Unexpected sample path ' + entry['path'])
        data = (root / manifest['content_root'] / path).read_bytes()
        if hashlib.sha256(data).hexdigest() != entry['sha256'] or len(data) != entry['bytes']:
            raise ValueError('Sample hash differs: ' + entry['path'])
        target = output / path.relative_to('audio')
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(data)
        files[str(path.relative_to('audio'))] = entry['sha256']
        report['bytes'] += len(data)
    if len(samples) != len(catalogue['sounds']):
        raise ValueError('Asset release does not hold every catalogued sound')
    report.update(status='bundled', samples=len(samples), releaseCommit=origin['release_commit'])
    (output / 'manifest.json').write_text(json.dumps({'files': files, 'audio': report}, indent=1) + '\n')
    return report

