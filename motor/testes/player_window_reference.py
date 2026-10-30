"""Newly published immutable window evidence, independent of the input source pin."""
import fcntl
import hashlib
import json
from pathlib import Path
from pinned_reference import REPO, INPUT_REVISION, source_root, git


def window_root(probe):
    if probe != 'P6':
        return source_root(), INPUT_REVISION
    pins = json.loads(Path(__file__).with_name('player-window-pins.json').read_bytes())
    revision = pins['revision']
    root = REPO / '.local/pinned-player-windows' / revision / 'tree'
    root.mkdir(parents=True, exist_ok=True)
    with (root.parent / 'prepare.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for relative, expected in pins['evidence_sha256'].items():
            path = Path(relative)
            if path.is_absolute() or '..' in path.parts:
                raise ValueError('Invalid pinned window path')
            original = git('show', revision + ':' + relative)
            if hashlib.sha256(original).hexdigest() != expected:
                raise ValueError('Pinned Git window identity changed: ' + relative)
            if hashlib.sha256((REPO / path).read_bytes()).hexdigest() != expected:
                raise ValueError('Immutable working-tree window changed: ' + relative)
            target = root / path
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                temporary = target.with_name(target.name + '.partial')
                temporary.write_bytes(original)
                temporary.chmod(0o444)
                temporary.replace(target)
            if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                raise ValueError('Pinned window cache changed: ' + relative)
    return root, revision
