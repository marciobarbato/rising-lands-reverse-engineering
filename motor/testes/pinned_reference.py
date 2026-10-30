"""Immutable revision-backed Python references, independent of the integration tree.

The logic revision is the source actually ported by stage 2/3. Only the Graphics
front is overlaid at the explicitly ported 1.7 revision. Both source and fixture
bytes come from Git objects. Original evidence pins additionally check the real
checkout; asset payloads are linked read-only and verified by the frozen catalog.
No imports are swapped, and no working-tree research file is modified.
"""
import fcntl
import functools
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile

REPO = Path(__file__).resolve().parents[2]
LOGIC_REVISION = '7ceeff909b52b7d4f59723f35dfe43a9deda41ff'
INPUT_REVISION = 'a7f5d4939e7826e02a8b348995edb9c793657f4c'
CHAIN_REVISION = '54d148d931cc3420fe256e6fec71462087597293'
CHAIN8_REVISION = '92fab50ccfa14271f6657fc0f6032b6b4b68dd4b'
CHAIN7_REVISION = '89575fad00ad3ee506879b275bdceb8f63423baf'
CHAIN6_GRAPHICS_REVISION = '24f0ec85714dbbfa4645212ca81f8f4145a76143'
GRAPHICS_REVISION = 'ce441852bcada750a8f91da8ed3302f1668c4405'
ROOTS = ('ferramentas', 'integracao', 'pesquisas-paralelas', 'evidencias', 'relatorios')
GRAPHICS = 'pesquisas-paralelas/graficos-animacao'


def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args])


def entries(revision, roots):
    data = git('ls-tree', '-r', '-z', revision, '--', *roots)
    return {name.decode(): (mode.decode(), oid.decode())
            for field in data.split(b'\0') if field
            for head, name in [field.split(b'\t', 1)]
            for mode, kind, oid in [head.split()] if kind == b'blob'}


def archive(revision, roots, target):
    process = subprocess.Popen(['git', '-C', str(REPO), 'archive', revision, *roots], stdout=subprocess.PIPE)
    try:
        with tarfile.open(fileobj=process.stdout, mode='r|') as stream:
            for item in stream:
                relative = Path(item.name)
                if relative.is_absolute() or '..' in relative.parts:
                    raise ValueError('Unsafe reference archive path')
                path = target / relative
                if item.isdir():
                    path.mkdir(parents=True, exist_ok=True)
                elif item.isfile():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with stream.extractfile(item) as source, path.open('wb') as dest:
                        shutil.copyfileobj(source, dest)
                    path.chmod(0o444)
                elif item.issym():
                    raise ValueError('Unexpected tracked reference symlink: ' + item.name)
                else:
                    raise ValueError('Unexpected reference archive entry: ' + item.name)
        if process.wait() != 0:
            raise ValueError('Pinned Git archive failed')
    finally:
        if process.poll() is None:
            process.kill(); process.wait()


def link_missing(path, target):
    if not path.exists() and not path.is_symlink():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(target, target_is_directory=True)


@functools.lru_cache(maxsize=1)
def source_root():
    profile = os.environ.get("RL_REFERENCE_PROFILE", "logic")
    if profile not in ("logic", "input", "chain5", "chain6", "chain7", "chain8"): raise ValueError("Unknown engine reference profile")
    logic_revision = CHAIN8_REVISION if profile=="chain8" else CHAIN7_REVISION if profile == "chain7" else CHAIN_REVISION if profile in ("chain5", "chain6") else INPUT_REVISION if profile == "input" else LOGIC_REVISION
    graphics_revision = CHAIN8_REVISION if profile=="chain8" else CHAIN6_GRAPHICS_REVISION if profile in ("chain6", "chain7", "chain8") else CHAIN_REVISION if profile == "chain5" else GRAPHICS_REVISION
    for revision in (logic_revision, graphics_revision):
        try:
            git('cat-file', '-e', revision + '^{commit}')
        except subprocess.CalledProcessError as error:
            raise RuntimeError('Pinned reference commit unavailable; fetch ' + revision) from error
    expected = entries(logic_revision, ROOTS)
    expected = {p: v for p, v in expected.items() if not p.startswith(GRAPHICS + '/')}
    expected.update(entries(graphics_revision, (GRAPHICS,)))
    identity = hashlib.sha256(json.dumps(expected, sort_keys=True).encode()).hexdigest()
    parent = REPO / '.local/pinned-engine-references' / identity
    parent.mkdir(parents=True, exist_ok=True)
    target = parent / 'tree'
    with (parent / 'prepare.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        ready = parent / 'ready.json'
        if not ready.exists():
            if target.exists(): shutil.rmtree(target)
            target.mkdir()
            archive(logic_revision, ROOTS, target)
            shutil.rmtree(target / GRAPHICS)
            archive(graphics_revision, (GRAPHICS,), target)
            ready.write_text(json.dumps(dict(logic=logic_revision, graphics=graphics_revision, tree_manifest_sha256=identity)) + '\n')
        if json.loads(ready.read_text()) != dict(logic=logic_revision, graphics=graphics_revision, tree_manifest_sha256=identity):
            raise ValueError('Pinned reference cache identity changed')
        # Validate actual cached bytes against the immutable Git tree, including
        # transitive modules and fixtures. A corrupt cache is a hard error.
        for relative, (mode, oid) in expected.items():
            if mode not in ('100644', '100755'): raise ValueError('Reference object mode')
            path = target / relative
            size = path.stat().st_size
            digest = hashlib.sha1(('blob %d\0' % size).encode())
            with path.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1024*1024), b''): digest.update(chunk)
            if digest.hexdigest() != oid:
                raise ValueError('Pinned reference cache corrupt: ' + relative)
        link_missing(parent / 'source', REPO.parent / 'source')
        link_missing(target / '.local/python', REPO / '.local/python')
        link_missing(target / GRAPHICS / 'fontes/cd', REPO / GRAPHICS / 'fontes/cd')
    return target


def reference_file(path):
    path = Path(path)
    relative = path.relative_to(REPO) if path.is_absolute() else path
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Reference path outside repository')
    return source_root() / relative


def pinned_file(path):
    """Source pins read the snapshot; immutable original evidence stays live/exact."""
    path = Path(path)
    return reference_file(path) if path.suffix == '.py' else path


def activate():
    root = source_root()
    paths = [root, root/'ferramentas', root/'pesquisas-paralelas/economia',
             root/'pesquisas-paralelas/combate', root/'pesquisas-paralelas/missoes',
             root/'pesquisas-paralelas/ia-runtime']
    for path in paths:
        text = str(path)
        if text not in sys.path: sys.path.insert(0, text)
    return root


def provenance():
    root = source_root()
    return {**json.loads((root.parent/'ready.json').read_text()), 'source_and_fixtures':'Git objects; no working-tree source hash gate'}
