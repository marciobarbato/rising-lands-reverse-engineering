"""Read-only accepted-state consumer, independent of the synthetic preview.

No simulation, rendering, input dispatch or live provider binding occurs here.
"""
from dataclasses import dataclass
import hashlib
import importlib.util
import json
from pathlib import Path
import re

CONTRACT = 'rising-lands/macos-state-consumer/1'
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
            raise StateValidationError('Endereço/tamanho de leitura inválido')
        for block in self.blocks:
            offset = address - block.base
            if 0 <= offset and offset + size <= len(block.data):
                return block.data[offset:offset + size]
        raise StateValidationError('Intervalo fora dos blocos capturados')

    def inspect(self):
        return dict(contract=self.contract, source_sha256=self.source_sha256,
                    mode='inspecao-m1', blocks=len(self.blocks),
                    bytes=sum(len(b.data) for b in self.blocks),
                    memory=[dict(name=b.name, base=f'0x{b.base:08x}',
                                 bytes=len(b.data), sha256=b.sha256) for b in self.blocks])


def _decode_blocks(records, decoder):
    """Validate structure before invoking the unchanged Missions decoder."""
    if not isinstance(records, dict) or not records:
        raise StateValidationError('Mapa de blocos vazio ou inválido')
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
        raise StateValidationError('Blocos de memória inválidos: ' + str(exc)) from exc


def load_accepted_m1(source_root=None):
    """Load the exact acceptance-pinned original-v2 capture, not an ETA copy.

    source_root is the same immutable source archive used by the app packager,
    or the checkout root for independent developer inspection. No CD is read.
    """
    root = Path(source_root) if source_root is not None else Path(__file__).resolve().parents[3]
    try:
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
        raise StateValidationError('Não foi possível validar o estado M1: ' + str(exc)) from exc


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
            'Contrato M2 pendente: fase validada, sequência, cenário e propriedade dos buffers')


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Inspecionar o snapshot M1 aceito')
    parser.add_argument('--source-root', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(load_accepted_m1(args.source_root).inspect(), indent=2))
    except StateValidationError as exc:
        parser.exit(2, str(exc) + '\n')


if __name__ == '__main__':
    main()
