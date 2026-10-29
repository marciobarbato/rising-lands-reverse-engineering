"""Read-only accepted-state consumer, independent of the synthetic preview.

No simulation, rendering, input dispatch or live provider binding occurs here.
"""
from dataclasses import dataclass
import hashlib
import importlib.util
import json
from pathlib import Path
import re

CONTRACT = 'rising-lands/macos-state-consumer/5'
CAPTURE_SHA256 = 'eb7d2303e13e62d4f5692c9cb6ef302b573d138df6a8b51183a6d9b0bd703afc'
EXECUTABLE_SHA256 = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
CAPTURE = 'pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json'
ACCEPTANCE = 'integracao/validacao/cxr-20261028-08-m1-acceptance.json'


class StateValidationError(ValueError):
    """Invalid or unaccepted state; the current consumer image is unchanged."""


class RuntimeContractPending(RuntimeError):
    """Validated M2 delivery/phase/ownership contract is not published."""


def _sha(data):
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class MacOSMemoryBlock:
    name: str
    base: int
    data: bytes
    sha256: str


@dataclass(frozen=True)
class MacOSAcceptedImage:
    contract: str
    source_sha256: str
    blocks: tuple

    @property
    def identity(self):
        # Source identity includes ordered external effects and provenance too.
        return self.contract, self.source_sha256

    def read(self, address, size):
        """Read one captured range; never fabricate bytes across gaps."""
        if type(address) is not int or type(size) is not int or size <= 0:
            raise StateValidationError('Invalid read address or size')
        for block in self.blocks:
            offset = address - block.base
            if 0 <= offset and offset + size <= len(block.data):
                return block.data[offset:offset + size]
        raise StateValidationError('Range is outside the captured blocks')

    def inspect(self):
        return dict(contract=self.contract, source_sha256=self.source_sha256,
                    mode='inspecao-m1', scenario='MONDE01/original-v2/M1-accepted-inspection', blocks=len(self.blocks),
                    bytes=sum(len(b.data) for b in self.blocks),
                    memory=[dict(name=b.name, base=f'0x{b.base:08x}',
                                 bytes=len(b.data), sha256=b.sha256) for b in self.blocks])


def _decode_blocks(records, decoder):
    """Validate structure before invoking the unchanged Missions decoder."""
    if not isinstance(records, dict) or not records:
        raise StateValidationError('Empty or invalid block map')
    try:
        for name, block in records.items():
            if not isinstance(name, str) or not name or not isinstance(block, dict):
                raise ValueError('block')
            if not isinstance(block.get('base'), str) or not re.fullmatch(r'0x[0-9a-fA-F]{1,8}', block['base']):
                raise ValueError('base')
            if type(block.get('bytes')) is not int or not 0 < block['bytes'] <= 16 * 1024 * 1024:
                raise ValueError('size')
            if int(block['base'], 16) + block['bytes'] > 2**32:
                raise ValueError('overflow')
            if not isinstance(block.get('sha256'), str) or not re.fullmatch(r'[0-9a-f]{64}', block['sha256']):
                raise ValueError('sha256')
            if not isinstance(block.get('zlib_base64'), str):
                raise ValueError('encoding')
        decoded = decoder(records)
        blocks = tuple(sorted((MacOSMemoryBlock(name, base, bytes(data), records[name]['sha256'])
                               for name, (base, data) in decoded.items()),
                              key=lambda b: (b.base, b.name)))
        for left, right in zip(blocks, blocks[1:]):
            if left.base + len(left.data) > right.base:
                raise ValueError('overlapping blocks')
        return blocks
    except Exception as exc:
        raise StateValidationError('Invalid memory blocks: ' + str(exc)) from exc



def _source_root(source_root):
    """Resolve an explicit root, declared bundle archive or source checkout.

    A deployed module never guesses a repository from its ancestor directories.
    Bundle manifests must select a relative archive contained in the payload.
    """
    if source_root is not None:
        return Path(source_root)
    module = Path(__file__).resolve()
    payload = module.parent
    manifest_path = payload / 'snapshot.json'
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_bytes())
        snapshot = manifest['snapshot']
        if not isinstance(snapshot, str) or not snapshot:
            raise ValueError('Bundle snapshot must declare a relative source archive')
        relative = Path(snapshot)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Bundle source archive must remain inside the payload')
        root = (payload / relative).resolve()
        if not root.is_relative_to(payload) or root == payload:
            raise ValueError('Bundle source archive must remain inside the payload')
        return root
    if (payload.name == 'src' and payload.parent.name == 'macos-preview'
            and payload.parent.parent.name == 'apps'):
        return payload.parents[2]
    raise ValueError('No source archive declared beside the deployed consumer; '
                     'provide source_root explicitly or a valid bundle snapshot.json')


def load_accepted_m1(source_root=None):
    """Load the exact acceptance-pinned original-v2 capture, not an ETA copy.

    source_root is the same immutable source archive used by the app packager,
    or the checkout root for independent developer inspection. Without an explicit
    root, bundles use only their snapshot.json archive. No CD is read.
    """
    try:
        root = _source_root(source_root)
        acceptance = json.loads((root / ACCEPTANCE).read_bytes())
        reference = acceptance['original_reference']
        if (acceptance['decision'] != 'ACCEPTED' or reference['capture_v2'] != CAPTURE
                or reference['capture_v2_sha256'] != CAPTURE_SHA256):
            raise ValueError('acceptance identity')
        raw = (root / CAPTURE).read_bytes()
        if _sha(raw) != CAPTURE_SHA256:
            raise ValueError('capture SHA-256')
        capture = json.loads(raw)
        oracle = capture['oracle']
        if (capture['schema'] != 'rising-lands/missionload-original-capture/1'
                or capture['original_sha256'] != EXECUTABLE_SHA256
                or oracle['reached_real_return'] is not True or oracle['al'] != 1):
            raise ValueError('MissionLoad schema/return')
        # This provider has only standard-library imports and no initialization.
        path = root / 'pesquisas-paralelas/missoes/mapa_memoria_m1.py'
        spec = importlib.util.spec_from_file_location('_macos_m1_memory_provider', path)
        provider = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(provider)
        blocks = _decode_blocks(oracle['final_state']['blocks'], provider.carregar_blocos)
        if len(blocks) != 881 or sum(len(b.data) for b in blocks) != 2659375:
            raise ValueError('accepted M1 extent')
        return MacOSAcceptedImage(CONTRACT, CAPTURE_SHA256, blocks)
    except StateValidationError:
        raise
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise StateValidationError('Unable to validate M1 state: ' + str(exc)) from exc


class MacOSStateConsumer:
    """Single-threaded inspection slot. No engine-owned mutable memory aliases.

    The shell must serialize calls. Only a successful load publishes an image;
    repeated loads preserve object identity. reset explicitly releases it.
    """
    def __init__(self):
        self._current = None

    @property
    def current(self):
        return self._current

    def load_m1(self, source_root=None):
        candidate = load_accepted_m1(source_root)
        if self._current is None or self._current.identity != candidate.identity:
            self._current = candidate
        return self._current

    def reset(self):
        self._current = None

    def apply_frame(self, frame):
        """Reserved local call boundary; no frame payload schema is invented."""
        raise RuntimeContractPending(
            'M2 contract pending: validated phase, sequence, scenario and buffer ownership')


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Inspect the accepted M1 snapshot')
    parser.add_argument('--source-root', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(load_accepted_m1(args.source_root).inspect(), indent=2))
    except StateValidationError as exc:
        parser.exit(2, str(exc) + '\n')


if __name__ == '__main__':
    main()
