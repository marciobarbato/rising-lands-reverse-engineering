#!/usr/bin/env python3
"""Compare inventoried inputs directly with original MODE2/2352 BIN sectors.

Reuse the existing legacy CDROM reader, without invoking its writing CLI.
Writes source-proof.json only beside this script; media remain read-only.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def hash_file(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bin-image', required=True, type=Path)
    parser.add_argument('--cue', required=True, type=Path)
    parser.add_argument('--cd-root', required=True, type=Path)
    parser.add_argument('--cdrom-reader', required=True, type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('campaign_existing_cdrom', args.cdrom_reader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data = json.loads((HERE / 'inventory.json').read_text())
    inputs = {r['path']: r for r in data['original_sources']}
    for mission in data['maps']:
        for record in (mission['source'], mission['briefing_source']):
            if record:
                inputs[record['path']] = record
    cd = module.CDROM(args.bin_image)
    try:
        entries = {r['path']: r for r in cd.walk()}
        proof = []
        for name, record in sorted(inputs.items()):
            entry = entries[name]
            original = cd.read(entry['sector'], entry['size'])
            assert original == (args.cd_root / name).read_bytes(), name
            assert hashlib.sha256(original).hexdigest() == record['sha256'], name
            assert len(original) == record['size'], name
            proof.append({'path': name, 'sector': entry['sector'], 'size': len(original),
                          'sha256': record['sha256'], 'bin_equals_extracted': True})
    finally:
        cd.file.close()
    report = {'schema': 'rising-lands/campaign-original-sector-proof/1',
              'bin': {'filename': args.bin_image.name, 'size': args.bin_image.stat().st_size,
                      'sha256': hash_file(args.bin_image)},
              'cue': {'filename': args.cue.name, 'sha256': hash_file(args.cue)},
              'reader': {'workspace_relative_path': 'legacy-prototype/tools/cdrom.py',
                         'sha256': hash_file(args.cdrom_reader), 'entrypoint': 'CDROM.walk/read'},
              'verified_input_count': len(proof), 'files': proof}
    encoded = (json.dumps(report, indent=2, sort_keys=True) + '\n').encode()
    output = HERE / 'source-proof.json'
    if args.check:
        assert output.read_bytes() == encoded, 'Sector proof changed'
    else:
        output.write_bytes(encoded)
    print(f'Verified {len(proof)} original files byte-for-byte against BIN sectors.')


if __name__ == '__main__':
    main()
