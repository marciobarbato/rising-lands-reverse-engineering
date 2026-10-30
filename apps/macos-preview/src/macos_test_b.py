"""Test B hash contract shared by the app validator and original-only observer.

No game writes. The published P6 cumulative mask is consumed verbatim; it is
never expanded to make a new session equal. Input streams and order effects are
reported independently. Unknown layouts remain differences, never dropped.
"""
import ast
import bisect
import hashlib
import json
import struct
from pathlib import Path
from macos_scripted_input import canonical
from macos_live_session import masked_summary

ORIGINAL = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
MASK = 'pesquisas-paralelas/missoes/m3/sondas/P6/mascara-janela.json'
REQUIRED_ORDERS = {'select': 1, 'move': 5, 'build_cave': 4, 'lodge_colonist': 16, 'ctrl_depot': 7, 'recruit': 17}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class Memory:
    def __init__(self, blocks):
        self.blocks = blocks
        self.bases = sorted(blocks)

    def read(self, address, size):
        i = bisect.bisect_right(self.bases, address) - 1
        if i < 0:
            raise ValueError(f'Unmapped address {address:#x}')
        base = self.bases[i]
        out = self.blocks[base][address-base:address-base+size]
        if len(out) != size:
            raise ValueError(f'Short read {address:#x}/{size}')
        return out

    def u8(self, a): return self.read(a, 1)[0]
    def u16(self, a): return struct.unpack('<H', self.read(a, 2))[0]
    def u32(self, a): return struct.unpack('<I', self.read(a, 4))[0]


class HashContract:
    def __init__(self, root):
        self.root = Path(root)
        mask = json.loads((self.root/MASK).read_bytes())
        policy = mask['window_policy']
        if not policy['passed'] or sha(self.root/policy['path']) != policy['sha256']:
            raise ValueError('Published P6 mask policy integrity failed')
        self.ranges = sorted((int(a, 16), int(z, 16)) for a, z in mask['cumulative']['exclusion_mask'])
        # Execute the owner's unchanged pure indicator reader, without importing
        # its simulator/provider namespace. Full mapped memory is hashed separately.
        path = self.root/'pesquisas-paralelas/ia-runtime/provar_entrada_ia.py'
        tree = ast.parse(path.read_text())
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'indicadores']
        if len(nodes) != 1:
            raise ValueError('Indicator contract unavailable')
        ns = dict(struct=struct, hashlib=hashlib, UNIDADES=(11, 12, 13, 14, 15))
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), ns)
        self.indicators = ns['indicadores']
        self.identity = dict(mask_path=MASK, mask_sha256=sha(self.root/MASK),
                             indicator_reader_sha256=sha(path), original_sha256=ORIGINAL,
                             scope='All mapped game blocks, names/base/length preserved; published P6 cumulative exclusion mask, zeroed verbatim. Static executable tables and native stack excluded as in Test A. No session-specific mask additions.')

    def sample(self, frame, state):
        indicators = self.indicators(Memory({a: b for a, b in state.values()}))
        return dict(frame=frame, state_sha256=masked_summary(state, self.ranges),
                    indicator_sha256=hashlib.sha256(canonical(indicators)).hexdigest(),
                    blocks=len(state), bytes=sum(len(b) for a, b in state.values()),
                    indicators=indicators)


def load_rows(path):
    import lzma
    path = Path(path)
    opener = lzma.open if path.suffix == '.xz' else open
    with opener(path, 'rt') as f:
        rows = [json.loads(line) for line in f if line.strip()]
    frames = [r['frame'] for r in rows]
    if len(frames) != len(set(frames)) or frames != sorted(frames):
        raise ValueError('Duplicate or unordered frame records')
    return {r['frame']: r for r in rows}


def compare(app, original, stop_frame=None):
    """Every requested frame appears, including missing frames after a stop."""
    app, original = Path(app), Path(original)
    manifests = [json.loads((p/'manifest.json').read_text()) for p in (app, original)]
    for key in ('input_sha256', 'hash_contract'):
        if manifests[0][key] != manifests[1][key]:
            raise ValueError('Incompatible comparison identity: '+key)
    stop = min(m['stop_frame'] for m in manifests) if stop_frame is None else stop_frame
    if not 129 <= stop <= min(m['stop_frame'] for m in manifests):
        raise ValueError('Comparison range outside replay range')
    aa, oo = [load_rows(p/'states.jsonl') for p in (app, original)]
    results = []
    for frame in range(129, stop+1):
        a, o = aa.get(frame), oo.get(frame)
        dif = {}
        for key in ('state_sha256', 'indicator_sha256', 'blocks', 'bytes'):
            av, ov = a.get(key) if a else None, o.get(key) if o else None
            if a is None or o is None or av != ov:
                dif[key] = dict(app=av, original=ov)
        if a and o and a['indicators'] != o['indicators']:
            dif['indicator_fields'] = {k: dict(app=a['indicators'].get(k), original=o['indicators'].get(k))
                                       for k in a['indicators'].keys() | o['indicators'].keys()
                                       if a['indicators'].get(k) != o['indicators'].get(k)}
        results.append(dict(frame=frame, equal=not dif, differences=dif,
                            app_sha256=a['state_sha256'] if a else None,
                            original_sha256=o['state_sha256'] if o else None))
    differences = [r for r in results if not r['equal']]
    return dict(schema='rising-lands/macos-test-b-comparison/1', input_sha256=manifests[0]['input_sha256'],
                hash_contract=manifests[0]['hash_contract'], frames_requested=stop-128,
                frames_equal=len(results)-len(differences), differences=differences, results=results,
                passed=not differences and all(m['status'] == 'completed' for m in manifests),
                replay_manifests=manifests)
