"""Accepted M2.2 evidence playback. No frame composition or live frame delivery."""
import ast
from dataclasses import dataclass
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import types
from macos_state_consumer import (MacOSAcceptedImage, MacOSMemoryBlock, StateValidationError,
                                  RuntimeContractPending, _source_root, _sha)

CONTRACT = 'rising-lands/macos-state-consumer/3'
SCENARIO = 'MONDE01/display-v2/M2.2-accepted-evidence'
MISSIONS = 'pesquisas-paralelas/missoes/'
EVIDENCE = MISSIONS + 'evidencias/'
CAPTURE = EVIDENCE + 'captura-quadros128-monde01-exibicao-v2.json.xz'
MANIFEST = EVIDENCE + 'captura-quadros128-monde01-exibicao-v2.manifest.json'
ACCEPTANCE = 'integracao/validacao/cxr-20261029-m2r6-m2-2-acceptance.json'
ENTRY = EVIDENCE + 'entrada-carga-missao-exibicao-v2.json'
M1_DISPLAY = EVIDENCE + 'captura-carga-missao-exibicao-v2.json'
RAW_SHA = '1ad031b96300e5c632fd5b6b7857ae30792f78e86531e4f17d1bf7124c6dd930'
PINS = {
    CAPTURE: '4c8f5c14a9623131dd019eafcdc49ea63054ee358f9defde58c12cb949f59ff3',
    MANIFEST: 'b0e49d1f820faa49db44c007e576c2b78ae8c230675e31e96b77dda17b147380',
    ACCEPTANCE: 'cebbe9b33d7d15a83990d794d3f5143d54696b71faa328710b2cc2c3814bbf57',
    ENTRY: '0bfbe98a7fbdb73e3c1f0c8510095e259a127bcfb842edf161ae072cde13c03a',
    M1_DISPLAY: 'a71351ed3b74bf7f8327910f8d06459327c10e6a97dc4e272f9a95ee237bca7e',
}
CHECKPOINTS = (1, 31, 32, 45, 50, 51, 52, 64, 100, 101, 128)
PHASES = ('load_tail', 'between_frames', 'frame1') + tuple(
    name for i in range(2, 129) for name in (f'between_frames{i}', f'frame{i}'))
WORDS = (('counter', 0x508f7c, 4), ('view_x', 0x508720, 2), ('view_y', 0x508722, 2),
         ('rng_game', 0x497164, 4), ('rng_crt', 0x498db4, 4),
         ('rng_permutation_cursor', 0x4e1d18, 4), ('hud_flag', 0x4e05a2, 1))


def load_path(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    # These leaf providers declare no dataclasses; no global module swap occurs.
    spec.loader.exec_module(module)
    return module


def reference_reader(root):
    """Load the unchanged CPU-only reader definitions by path.

    The complete comparator imports the simulation, Unicorn and the original PE.
    Compile only these existing pure reader definitions, without executing its
    unrelated top-level imports. Never substitute a missing simulation provider.
    """
    path = root / 'pesquisas-paralelas/ia-runtime/comparar_quadros_ia.py'
    tree = ast.parse(path.read_text(), filename=str(path))
    names = {'IntegridadeCaptura', 'resumo_estado', '_dados', 'aplicar_delta',
             'fases_referencia', 'carregar_captura'}
    selected = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    if {n.name for n in selected} != names:
        raise StateValidationError('Committed reference reader definitions are unavailable')
    import base64, bisect, zlib
    module = types.ModuleType('_macos_m22_reference_reader')
    module.__dict__.update(base64=base64, bisect=bisect, zlib=zlib, hashlib=hashlib,
                           json=json, struct=struct)
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(path), 'exec'), module.__dict__)
    return module


@dataclass(frozen=True)
class MacOSPlaybackImage(MacOSAcceptedImage):
    phase_index: int
    phase_name: str
    summary_sha256: str
    checkpoint: bool

    @property
    def identity(self):
        return self.contract, self.source_sha256, self.phase_name, self.summary_sha256

    def observed_words(self):
        return {name: dict(address=hex(address), bytes=size,
                           value=int.from_bytes(self.read(address, size), 'little'))
                for name, address, size in WORDS}

    def inspect(self):
        result = super().inspect()
        result.update(mode='accepted-evidence-playback', scenario=SCENARIO,
                      phase_index=self.phase_index, phase=self.phase_name,
                      summary_sha256=self.summary_sha256, summary_verified=True,
                      checkpoint_verified=self.checkpoint, observed=self.observed_words())
        return result

    def ler_mundo(self, address, size):
        return self.read(address, size)

    def u8(self, address): return self.read(address, 1)[0]
    def u16(self, address): return int.from_bytes(self.read(address, 2), 'little')
    def u32(self, address): return int.from_bytes(self.read(address, 4), 'little')


class MacOSM22Playback:
    """Serial cursor. Publication happens only after complete candidate validation."""
    def __init__(self, root, capture, s0, decoder, reader, integrity):
        self.root, self._capture, self._s0 = root, capture, s0
        self._delta, self._reader, self.integrity = decoder, reader, tuple(integrity)
        self._state = s0
        self._previous = None
        self._index = -1
        self._current = self._image(s0, -1)

    @classmethod
    def open(cls, source_root=None):
        try:
            root = _source_root(source_root)
            for path, expected in PINS.items():
                if _sha((root / path).read_bytes()) != expected:
                    raise StateValidationError('Unpinned or modified M2.2 input: ' + path)
            reader = reference_reader(root)
            delta = load_path(root / MISSIONS / 'delta_estado_missao.py', '_macos_delta_state')
            memory = load_path(root / MISSIONS / 'mapa_memoria_m1.py', '_macos_display_memory')
            manifest = json.loads((root / MANIFEST).read_bytes())
            acceptance = json.loads((root / ACCEPTANCE).read_bytes())
            if acceptance['decision'] != 'ACCEPTED' or manifest['raw_json']['sha256'] != RAW_SHA:
                raise StateValidationError('M2.2 acceptance or manifest identity differs')
            capture, _ = reader.carregar_captura(root / CAPTURE, RAW_SHA)
            cls._validate_order(capture)
            m1 = memory.expandir_captura(json.loads((root / M1_DISPLAY).read_bytes()),
                                        json.loads((root / ENTRY).read_bytes()))
            s0 = memory.carregar_blocos(m1['oracle']['final_state']['blocks'])
            if delta.resumo(s0) != capture['state_s0']['summary']:
                raise StateValidationError('M2.2 opening state is not the accepted display-v2 state')
            # Reuse the runtime reader, including exact checkpoint equality.
            integrity = [dict(phase=phase['phase'], **checked)
                         for phase, _, checked in reader.fases_referencia(capture, s0)]
            # Retain only playback inputs, not binding traces or simulation metadata.
            capture = dict(state_s0=capture['state_s0'], opening_display=m1['display_state'], phases=[
                {k: p[k] for k in ('phase', 'state_delta', 'state_after', 'display_state')}
                for p in capture['phases']])
            return cls(root, capture, s0, delta, reader, integrity)
        except StateValidationError:
            raise
        except Exception as exc:
            raise StateValidationError('Unable to open accepted M2.2 playback: ' + str(exc)) from exc

    @staticmethod
    def _validate_order(capture):
        if tuple(p['phase'] for p in capture['phases']) != PHASES:
            raise StateValidationError('M2.2 phases are missing, duplicated or out of order')
        checkpoints = tuple(p['phase'] for p in capture['phases'] if 'full_state' in p['state_after'])
        if checkpoints != tuple(f'frame{i}' for i in CHECKPOINTS):
            raise StateValidationError('M2.2 checkpoint sequence differs from acceptance')

    def _image(self, state, index):
        blocks = tuple(MacOSMemoryBlock(name, base, data, _sha(data))
                       for name, (base, data) in sorted(state.items(), key=lambda p: (p[1][0], p[0])))
        for left, right in zip(blocks, blocks[1:]):
            if left.base + len(left.data) > right.base:
                raise StateValidationError('Overlapping playback blocks')
        name = PHASES[index] if index >= 0 else 'state_s0'
        return MacOSPlaybackImage(CONTRACT, PINS[CAPTURE], blocks, index, name,
                                  self._delta.resumo(state)['sha256'],
                                  index >= 0 and 'full_state' in self._capture['phases'][index]['state_after'])

    @property
    def current(self): return self._current

    def reset(self):
        image = self._image(self._s0, -1)
        self._state, self._index, self._current = self._s0, -1, image
        self._previous = None
        return image

    def step_to_phase(self, phase):
        if phase == 'state_s0': return self.reset()
        if isinstance(phase, str):
            try: index = PHASES.index(phase)
            except ValueError: raise StateValidationError('Unknown M2.2 phase: ' + phase)
        elif type(phase) is int and 0 <= phase < len(PHASES): index = phase
        else: raise StateValidationError('Phase index must be an integer in 0..256')
        if index == self._index: return self.current
        state = self._state if index > self._index else self._s0
        start = self._index + 1 if index > self._index else 0
        try:
            for i in range(start, index + 1):
                p = self._capture['phases'][i]
                previous = state
                state = self._delta.aplicar(state, p['state_delta'], p['phase'])
                if self._delta.resumo(state) != p['state_after']['summary']:
                    raise StateValidationError('Playback summary mismatch: ' + p['phase'])
                if 'full_state' in p['state_after']:
                    full = {n: (int(b['base'], 16), self._reader._dados(b))
                            for n, b in p['state_after']['full_state'].items()}
                    if full != state:
                        raise StateValidationError('Playback checkpoint mismatch: ' + p['phase'])
            candidate = self._image(state, index)
        except Exception as exc:
            raise StateValidationError('Unable to publish playback phase: ' + str(exc)) from exc
        self._state, self._index, self._current = state, index, candidate
        self._previous = previous
        return candidate

    def step_to_frame(self, frame):
        if isinstance(frame, str) and frame.startswith('frame'): frame = frame[5:]
        if isinstance(frame, str) and frame.isdecimal(): frame = int(frame)
        if type(frame) is not int or not 0 <= frame <= 128:
            raise StateValidationError('Frame must be an integer in 0..128 or a frame name')
        return self.reset() if frame == 0 else self.step_to_phase(f'frame{frame}')

    def read(self, address, size): return self.current.read(address, size)
    def inspect(self): return self.current.inspect()
    def apply_frame(self, frame):
        raise RuntimeContractPending('Live frame delivery remains reserved; use accepted-evidence playback')

    def fork(self):
        """Independent cursor over the same verified immutable evidence inputs."""
        return MacOSM22Playback(self.root, self._capture, self._s0, self._delta, self._reader, self.integrity)

    def drawing_input(self):
        """AffGame entry memory: previous frame/load-tail return, before loop counters.

        between_frames ends at the NEXT CalculGame entry; its ending counter is
        already incremented. Rendering must read the preceding captured state.
        """
        if not self.current.phase_name.startswith('between_frames'):
            raise StateValidationError('Only between_frames phases have an AffGame input')
        return self._image(self._previous, self._index - 1)

    def previous_surface(self, supplied=None):
        """Exact preceding offscreen bytes, from memory or hash-bound external evidence.

        The accepted M2.2 capture publishes surface hashes, not their pixels.
        A future pluggable source must match the preceding captured hash.
        No files or alternate pixel artifacts are consulted by this consumer.
        """
        index = self._index
        if index < 0: raise StateValidationError('Select a playback phase before rendering')
        display = (self._capture['phases'][index - 1]['display_state'] if index > 0
                   else self._capture['opening_display'])
        surface = next(s for s in display['surfaces'] if s['role'] == 'offscreen')
        address, size = int(surface['pixels'], 16), surface['width'] * surface['height']
        data = supplied
        for base, buffer in self._previous.values():
            if base <= address and address + size <= base + len(buffer):
                data = buffer[address - base:address - base + size]
                break
        if data is None:
            raise StateValidationError('Missing previous surface: ' + self.current.phase_name
                                       + ', 480000 bytes, SHA-256 ' + surface['sha256'])
        if len(data) != size or _sha(data) != surface['sha256']:
            raise StateValidationError('Previous surface differs from accepted evidence')
        return data
