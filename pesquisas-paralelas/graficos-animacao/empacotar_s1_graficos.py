"""Losslessly partition a new native S1 capture for Git transport; preserve its original archive.

Rows and zlib payload strings are copied verbatim. The original capture and manifest
are moved unchanged to the requested local archive only after all parts are verified.
Historical or tracked evidence is never rewritten.
"""
import argparse
import hashlib
import json
import lzma
import re
import shutil
import subprocess
from pathlib import Path

sha = lambda b: hashlib.sha256(b).hexdigest()


def hashes(value):
    if isinstance(value, str):
        if re.fullmatch('[0-9a-f]{64}', value):
            yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from hashes(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from hashes(v)


def empacotar(path, archive, count=128):
    path, archive = Path(path), Path(archive)
    tracked = subprocess.run(['git', 'ls-files', '--error-unmatch', str(path)], capture_output=True).returncode == 0
    if tracked:
        raise ValueError('Only a new, untracked native capture can be partitioned')
    raw = path.read_bytes()
    parent = json.loads(lzma.decompress(raw))
    assert parent['probe'] == 'S1' and parent['status'] == 'complete'
    parent_manifest = Path(str(path) + '.manifest.json')
    metadata = json.loads(parent_manifest.read_text())
    assert metadata['compressed_sha256'] == sha(raw)
    assert metadata['raw_sha256'] == sha(lzma.decompress(raw))
    archive.mkdir(parents=True, exist_ok=True)
    if (archive / path.name).exists() or (archive / parent_manifest.name).exists():
        raise FileExistsError('Native archive already exists')
    rows = parent['rows']
    result = []
    copied = []
    for start in range(0, len(rows), count):
        selected = rows[start:start + count]
        lo, hi = selected[0]['frame'], selected[-1]['frame']
        output = path.with_name(f's1-render-part-{lo}-{hi}.json.xz')
        if output.exists():
            raise FileExistsError(output)
        part = {k: v for k, v in parent.items() if k not in ('rows', 'blobs', 'checks')}
        part['frames'] = [lo, hi]
        part['rows'] = selected
        part['checks'] = [r for r in parent['checks'] if lo <= r['frame'] <= hi]
        needed = set(hashes(selected)) & parent['blobs'].keys()
        part['blobs'] = {k: parent['blobs'][k] for k in sorted(needed)}
        part['derived_partition'] = dict(native_capture_file=path.name, native_capture_sha256=sha(raw),
            native_frames=parent['frames'], row_slice=[start, start + len(selected)],
            snapshot_frame=parent['frames'][1],
            packaging_source_sha256=sha(Path(__file__).read_bytes()),
            rule='Original rows and referenced encoded payloads copied verbatim; native snapshot belongs to parent end frame.')
        output.write_bytes(lzma.compress(json.dumps(part).encode(), preset=3))
        saved = json.loads(lzma.decompress(output.read_bytes()))
        assert saved['rows'] == selected and saved['checks'] == part['checks']
        assert all(saved['blobs'][k] == parent['blobs'][k] for k in needed)
        assert output.stat().st_size < 100 * 1024 * 1024, 'Split into smaller parts before delivery'
        copied.extend(saved['rows'])
        result.append(dict(path=output.name, frames=[lo, hi], sha256=sha(output.read_bytes()), bytes=output.stat().st_size))
    assert copied == parent['rows']
    # The native manifest remains public provenance even though the large original archive is local.
    ledger = dict(schema='rising-lands/graphics-s1-native-lossless-partition/1',
        native_capture_sha256=sha(raw), native_manifest=metadata, parts=result,
        complete_native_rows_equal=True, encoded_payloads_unchanged=True)
    path.with_name(path.name + '.partitions.json').write_text(json.dumps(ledger, indent=2) + '\n')
    shutil.move(str(path), str(archive / path.name))
    shutil.move(str(parent_manifest), str(archive / parent_manifest.name))
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('capture')
    p.add_argument('--archive', required=True)
    p.add_argument('--rows', type=int, default=128)
    a = p.parse_args()
    if not 1 <= a.rows <= 256:
        raise ValueError('Require 1..256 rows per transport part')
    print(empacotar(a.capture, a.archive, a.rows), flush=True)
