"""App audio mapper replays recorded original request logs; no sound card used.

The original boundary logs of the Missions probes (S1: the complete MONDE01
run, P6) hold every PlaySnd_PostSound/StopSound/Manage call with its exact
registers and stack volume. They are fed, in order, to the app's C mapper and to
Audio's validated Python queue reference (fila_audio.AudioQueue) over the same
private initialized-library image. Both talk to the same deterministic device
model; their ordered device commands must be identical, and every scheduled
sample must be a catalogued, GetDataHeader-reachable original sound.
"""
import ctypes as C
import hashlib
import json
import lzma
import math
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
import base64

ROOT = Path(__file__).resolve().parents[3]
AUDIO = ROOT / 'pesquisas-paralelas/audio'
NATIVE = ROOT / 'apps/macos-preview/src/native'
PROBES = ROOT / 'pesquisas-paralelas/missoes/m3/sondas'
sys.path.insert(0, str(AUDIO))
sys.path.insert(0, str(ROOT / 'apps/macos-preview/src'))

GLB, BSS, HDR, HDR_STRIDE, DICT, DEVICE_POINTER = 0x498f14, 0x521358, 0x10000000, 0x10000, 0x0f000000, 0x0e000000
BANKS = {0x41: 0x521fc8, 0x42: 0x521fe4, 0x50: 0x522000}
LETTERS = {0x41: 'A', 0x42: 'B', 0x50: 'P'}
ROUTINES = {'PlaySnd_Manage': 0, 'PlaySnd_PostSound': 1, 'PlaySnd_StopSound': 2}
FPS = 60  # Device model: a played sample ends after its decoded length at 60 game frames/s.


class SoundEvent(C.Structure):
    _fields_ = [(n, C.c_uint32) for n in ('kind', 'frame', 'phase', 'site', 'eax', 'edx', 'ebx', 'ecx', 'volume', 'has_volume')]


class Command(C.Structure):
    _fields_ = [('op', C.c_uint32), ('buffer', C.c_uint32), ('source', C.c_uint32), ('volume', C.c_int32),
                ('loop', C.c_uint32), ('frame', C.c_uint32), ('phase', C.c_uint32), ('sequence', C.c_uint32)]


class Stats(C.Structure):
    _fields_ = [(n, C.c_uint64) for n in ('requests', 'posts', 'stops', 'manages', 'absent', 'unsupported_selector', 'commands',
                                          'dropped_commands', 'plays', 'domain_faults', 'handle_overflow', 'buffer_overflow')]


def mapper_library(directory):
    """The built app driver dylib when supplied, otherwise a fresh compile of the same source."""
    supplied = os.environ.get('RL_MACOS_NATIVE_LIBRARY')
    if supplied and Path(supplied).exists():
        lib = C.CDLL(supplied)
        if hasattr(lib, 'macos_audio_create'):
            return lib
    out = Path(directory) / 'libmacos_audio_mapper.dylib'
    subprocess.run(['xcrun', 'clang', '-O2', '-Wall', '-Werror', '-dynamiclib', '-arch', 'arm64',
                    str(NATIVE / 'macos_audio_mapper.c'), '-o', str(out)], check=True, capture_output=True)
    return C.CDLL(str(out))


def sound_directory():
    candidates = []
    if os.environ.get('RL_ORIGINAL_EXE'):
        candidates.append(Path(os.environ['RL_ORIGINAL_EXE']).parent / 'SOUND')
    if os.environ.get('RISING_INPUTS_ROOT'):
        candidates.append(Path(os.environ['RISING_INPUTS_ROOT']) / 'source/cd/INSTALHD/SOUND')
    candidates += [parent / 'source/cd/INSTALHD/SOUND' for parent in ROOT.parents]
    for path in candidates:
        if (path / 'P.HED').is_file():
            return path
    return None


def probe_log(name):
    rows = [json.loads(line) for line in lzma.open(PROBES / name / 'fronteiras.jsonl.xz', 'rt')]
    return [row for row in rows if row['routine'].startswith('PlaySnd_')]


def event(row):
    r = {k: int(v, 16) for k, v in row['registers'].items()}
    return SoundEvent(ROUTINES[row['routine']], row['frame'], 2 if row['phase'].startswith('between') else 3,
                      int(row['caller_return'], 16), r['EAX'], r['EDX'], r['EBX'], r['ECX'],
                      int(row['stack_words'][0], 16) if row['routine'] == 'PlaySnd_PostSound' else 0,
                      int(row['routine'] == 'PlaySnd_PostSound'))


class ShadowMemory:
    """The mapper's private image at the original addresses; game handles default to -1."""
    def __init__(self, globals_bytes, heds):
        self.regions = [(GLB, bytearray(globals_bytes)), (BSS, bytearray(3804)), (DICT, bytearray(8))]
        for i, selector in enumerate((0x41, 0x42, 0x50)):
            hed = heds[selector]
            self.regions.append((HDR + i * HDR_STRIDE, bytearray(hed[16:])))
            bank = BANKS[selector]
            self.w32(bank, 1); self.write(bank + 4, struct.pack('<H', struct.unpack_from('<I', hed, 12)[0]))
            self.w32(bank + 12, HDR + i * HDR_STRIDE)
        self.handles = {}
    def _view(self, address, size):
        for base, data in self.regions:
            if base <= address and address + size <= base + len(data):
                return data, address - base
        return None, None
    def view(self, address, size):
        data, offset = self._view(address, size)
        if data is None:
            raise ValueError(f'Undeclared view 0x{address:08x}')
        return memoryview(data)[offset:offset + size]
    def read(self, address, size):
        data, offset = self._view(address, size)
        if data is None:
            if size == 4:
                return struct.pack('<I', self.handles.get(address, 0xffffffff))
            raise ValueError(f'Undeclared read 0x{address:08x}')
        return bytes(data[offset:offset + size])
    def write(self, address, value):
        data, offset = self._view(address, len(value))
        if data is None:
            if len(value) != 4:
                raise ValueError(f'Undeclared write 0x{address:08x}')
            self.handles[address] = struct.unpack('<I', value)[0]
            return
        data[offset:offset + len(value)] = value
    def u8(self, a): return self.read(a, 1)[0]
    def u16(self, a): return struct.unpack('<H', self.read(a, 2))[0]
    def u32(self, a): return struct.unpack('<I', self.read(a, 4))[0]
    def w8(self, a, v): self.write(a, bytes([v & 255]))
    def w32(self, a, v): self.write(a, struct.pack('<I', v & 0xffffffff))


def signed(value):
    return value - 0x100000000 if value & 0x80000000 else value


class ReferenceDevice:
    """Explicit DirectSound answers for fila_audio, normalized to the mapper's commands."""
    def __init__(self):
        self.status, self.next, self.log, self.positioned, self.stash = {}, 1, [], set(), {}
    def new(self):
        value = self.next; self.next += 1; self.status[value] = 0; return value
    def answer(self, method, pointer, args):
        if method == 'GlobalAlloc':
            return {'hresult': DICT}
        if method == 'GetStatus':
            return {'hresult': 0, 'value': self.status.get(pointer, 0)}
        if method == 'CreateSoundBuffer':
            value = self.new(); self.log.append(('create', value, args[0])); return {'hresult': 0, 'value': value}
        if method == 'DuplicateSoundBuffer':
            value = self.new(); self.log.append(('duplicate', value, args[0])); return {'hresult': 0, 'value': value}
        if method == 'SetPosition':
            self.positioned.add(pointer); return {'hresult': 0}
        if method == 'SetVolume':
            if pointer in self.positioned:
                self.stash[pointer] = signed(args[0])
            else:
                self.log.append(('volume', pointer, signed(args[0])))
            return {'hresult': 0}
        if method == 'Play':
            self.positioned.discard(pointer); loop = args[2] & 1
            self.log.append(('play', pointer, self.stash.pop(pointer), loop)); self.status[pointer] = 1 | (4 if loop else 0)
            return {'hresult': 0}
        if method == 'Stop':
            self.status[pointer] = 0; self.log.append(('stop', pointer)); return {'hresult': 0}
        if method == 'Release':
            self.status.pop(pointer, None); self.log.append(('release', pointer)); return {'hresult': 0}
        raise ValueError('Unexpected device call ' + method)


def reference_queue(globals_bytes, heds):
    from fila_audio import AudioQueue
    device = ReferenceDevice()
    memory = ShadowMemory(globals_bytes, heds)
    memory.w32(0x522228, DEVICE_POINTER)
    queue = AudioQueue(memory, device)
    queue.init_dictator()
    def create_sound(r):
        # Stage-1 criar_superficie_som creates a buffer for formats 0/4 only; its
        # decoded bytes are the asset, so the model answers with the sample key.
        header = memory.u32(r + 28); bank = list(BANKS.values()).index(memory.u32(r + 4))
        if memory.u8(header + 12) not in (0, 4):
            return 0
        key = (bank << 24) | (header - HDR - bank * HDR_STRIDE)
        return queue.call('CreateSoundBuffer', memory.u32(0x522228), (key,), 0x48b834)['value']
    queue.create_sound = create_sound
    return queue, device


OPS = {1: 'create', 2: 'duplicate', 3: 'play', 4: 'volume', 5: 'stop', 6: 'release'}


def normalize(command):
    op = OPS[command.op]
    if op in ('create', 'duplicate'):
        return (op, command.buffer, command.source)
    if op == 'play':
        return (op, command.buffer, command.volume, command.loop)
    if op == 'volume':
        return (op, command.buffer, command.volume)
    return (op, command.buffer)


class AudioMapperReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.lib = lib = mapper_library(cls.temporary.name)
        lib.macos_audio_create.restype = C.c_void_p
        lib.macos_audio_free.argtypes = [C.c_void_p]
        lib.macos_audio_load_bank.argtypes = [C.c_void_p, C.c_uint32, C.c_char_p, C.c_uint32]
        lib.macos_audio_request.argtypes = [C.c_void_p, C.POINTER(SoundEvent)]; lib.macos_audio_request.restype = C.c_uint32
        lib.macos_audio_device_stopped.argtypes = [C.c_void_p, C.c_uint32]
        lib.macos_audio_commands.argtypes = [C.c_void_p, C.POINTER(Command), C.c_uint32]; lib.macos_audio_commands.restype = C.c_uint32
        lib.macos_audio_sample.argtypes = [C.c_void_p, C.c_uint32] + [C.POINTER(C.c_uint32)] * 3; lib.macos_audio_sample.restype = C.c_int32
        lib.macos_audio_stats.argtypes = [C.c_void_p, C.POINTER(Stats)]
        lib.macos_audio_volume_table.restype = C.c_int32
        directory = sound_directory()
        if directory is None:
            raise unittest.SkipTest('Original CD SOUND/*.HED inputs unavailable')
        catalogue = json.loads((AUDIO / 'catalogo-amostras.json').read_bytes())
        cls.heds = {}
        for selector, letter in LETTERS.items():
            data = (directory / (letter + '.HED')).read_bytes()
            expected = catalogue['banks'][letter + '.HED']
            if (len(data), hashlib.sha256(data).hexdigest()) != (expected['bytes'], expected['sha256']):
                raise AssertionError('Original HED identity mismatch: ' + letter)
            cls.heds[selector] = data
        cls.sounds = {(s['bank'], int(s['id'], 16), s['variant']): s for s in catalogue['sounds']}
        capture = json.loads((AUDIO / 'evidencias/m3-pedidos-original-v1.json').read_bytes())
        region = next(r for r in capture['cases'][0]['input']['memory'] if r['base'] == '0x498f14')
        cls.globals = zlib.decompress(base64.b64decode(region['zlib_base64']))
        assert hashlib.sha256(cls.globals).hexdigest() == region['sha256']

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def mapper(self):
        handle = self.lib.macos_audio_create(); self.addCleanup(self.lib.macos_audio_free, handle)
        for selector, data in self.heds.items():
            self.assertEqual(self.lib.macos_audio_load_bank(handle, selector, data, len(data)), 0)
        return handle

    def identity(self, handle, key):
        bank, index, variant = C.c_uint32(), C.c_uint32(), C.c_uint32()
        self.assertEqual(self.lib.macos_audio_sample(handle, key, C.byref(bank), C.byref(index), C.byref(variant)), 0, hex(key))
        letter = 'ABP'[bank.value]
        sound_id = struct.unpack_from('<I', self.heds[[0x41, 0x42, 0x50][bank.value]], 16 + 12 * index.value)[0]
        return letter, sound_id, variant.value

    def duration(self, handle, key):
        sound = self.sounds[self.identity(handle, key)]
        return math.ceil(sound['decoded_bytes'] / 2 / sound['sample_rate'] * FPS)

    def replay(self, rows, finishing):
        """Feeds the log to both implementations; returns their command logs and outcomes."""
        native, (queue, device) = self.mapper(), reference_queue(self.globals, self.heds)
        commands, results, buffer = [], [], (Command * 2048)()
        ends = {'native': {}, 'reference': {}}
        samples = {'native': {}, 'reference': {}}
        def finish(side, frame, stop):
            for buffer_id, end in list(ends[side].items()):
                if end is not None and end <= frame:
                    stop(buffer_id); del ends[side][buffer_id]
        def schedule(side, entries, frame):
            for entry in entries:
                if entry[0] == 'create':
                    samples[side][entry[1]] = entry[2]
                elif entry[0] == 'duplicate':
                    samples[side][entry[1]] = samples[side][entry[2]]
                elif entry[0] == 'play':
                    ends[side][entry[1]] = None if entry[3] or not finishing else frame + self.duration(native, samples[side][entry[1]])
                elif entry[0] in ('stop', 'release'):
                    ends[side].pop(entry[1], None)
        for row in rows:
            e = event(row)
            if e.kind == 0:
                finish('native', e.frame, lambda b: self.lib.macos_audio_device_stopped(native, b))
                finish('reference', e.frame, lambda b: device.status.__setitem__(b, 0))
            before = len(device.log)
            if e.kind == 0:
                reference = queue.manage()
            elif e.kind == 1:
                reference = queue.post(e.eax, e.edx, e.ebx, e.ecx, e.volume)
            else:
                reference = queue.stop_handle(e.eax)
            actual = self.lib.macos_audio_request(native, C.byref(e))
            n = self.lib.macos_audio_commands(native, buffer, len(buffer))
            emitted = [normalize(buffer[i]) for i in range(n)]
            self.assertEqual(emitted, device.log[before:], (row, emitted, device.log[before:]))
            self.assertEqual(actual, reference, row)
            schedule('native', emitted, e.frame); schedule('reference', device.log[before:], e.frame)
            commands += [(e.frame, e.phase) + c for c in emitted]
            results.append((row['routine'], actual))
        stats = Stats(); self.lib.macos_audio_stats(native, C.byref(stats))
        return native, commands, results, stats

    def check_log(self, name, expected_posts, expected_plays):
        full = [json.loads(line) for line in lzma.open(PROBES / name / 'fronteiras.jsonl.xz', 'rt')]
        rows = [row for row in full if row['routine'] in ROUTINES]
        unsupported = [row for row in full if row['routine'].startswith('PlaySnd_') and row['routine'] not in ROUTINES]
        # PlaySnd_StopAllSound (victory) is an open Audio stop, not translated.
        self.assertTrue(all(row['routine'] == 'PlaySnd_StopAllSound' for row in unsupported))
        posts = [row for row in rows if row['routine'] == 'PlaySnd_PostSound']
        self.assertEqual(len(posts), expected_posts)
        for finishing in (True, False):
            with self.subTest(probe=name, device='finishing' if finishing else 'holding'):
                native, commands, results, stats = self.replay(rows, finishing)
                # The mapper consumed exactly the recorded request sequence, in order.
                self.assertEqual([r[0] for r in results], [row['routine'] for row in rows])
                self.assertEqual((stats.requests, stats.posts, stats.stops, stats.manages),
                                 (len(rows), len(posts), sum(r['routine'] == 'PlaySnd_StopSound' for r in rows),
                                  sum(r['routine'] == 'PlaySnd_Manage' for r in rows)))
                self.assertEqual((stats.domain_faults, stats.handle_overflow, stats.buffer_overflow, stats.dropped_commands,
                                  stats.unsupported_selector, stats.absent), (0, 0, 0, 0, 0, 0))
                # Every created sample is an original, catalogued, reachable variant
                # of an ID the log actually posted, created no earlier than its post.
                posted = {}
                for row in posts:
                    r = {k: int(v, 16) for k, v in row['registers'].items()}
                    posted.setdefault((LETTERS[r['EAX']], r['EDX']), row['frame'])
                plays = [c for c in commands if c[2] == 'play']
                for frame, phase, op, buffer_id, key in [c for c in commands if c[2] == 'create']:
                    identity = self.identity(native, key)
                    self.assertTrue(self.sounds[identity]['reachable_by_get_data_header'], identity)
                    self.assertLessEqual(posted[identity[:2]], frame)
                self.assertTrue(all(-10000 <= c[4] <= 0 for c in plays))
                self.assertEqual(len(plays), expected_plays[finishing])

    def test_volume_table_is_the_original_initialized_bytes(self):
        table = [struct.unpack_from('<i', self.globals, 4 * i)[0] for i in range(17)]
        self.assertEqual([self.lib.macos_audio_volume_table(i) for i in range(17)], table)
        self.assertEqual(struct.unpack_from('<5i', self.globals, 68), (256, 1, -1, -1, 19))

    def test_s1_complete_mission_log(self):
        self.check_log('S1', 177, {True: 138, False: 57})

    def test_p6_log(self):
        self.check_log('P6', 59, {True: 56, False: 7})

    def test_handles_repost_volume_zero_stop_and_unknown_selector(self):
        native = self.mapper(); buffer = (Command * 64)()
        def send(kind, eax=0, edx=0, ebx=0, ecx=0, volume=0):
            result = self.lib.macos_audio_request(native, C.byref(SoundEvent(kind, 200, 3, 0, eax, edx, ebx, ecx, volume, int(kind == 1))))
            return result, [normalize(buffer[i]) for i in range(self.lib.macos_audio_commands(native, buffer, 64))]
        unit = 0x474a8df4
        self.assertEqual(send(1, 0x50, 0x70800, unit, 0, 256), (1, []))
        self.assertEqual(send(1, 0x50, 0x70800, unit, 0, 128), (1, []))  # same ID on the busy handle: volume only
        result, commands = send(0)
        self.assertEqual([c[0] for c in commands], ['create', 'play'])
        self.assertEqual(commands[1][2:], (-1250, 0))  # (128*256*256)>>20 = 8 -> table[8]
        self.assertEqual(send(1, 0x50, 0x70800, unit, 0, 0), (1, [('stop', 1), ('release', 1)]))  # volume 0 cancels
        self.assertEqual(send(1, 0x44, 0x1234, unit, 0, 256), (0x1234, []))  # bad selector returns EDX
        self.assertEqual(send(1, 0x50, 0x1700, unit, 1, 256)[0], 1)  # flags byte 1 loops
        self.assertEqual(send(0)[1][-1][3], 1)
        self.assertEqual(send(2, unit)[1][0], ('stop', 2))


class EngineSoundTransportTests(unittest.TestCase):
    """The production C phase entry copies the engine's own kind-10 requests."""
    def test_p2_requests_from_the_engine_equal_the_original_log(self):
        driver = Path(os.environ.get('RL_MACOS_NATIVE_LIBRARY', ROOT / 'apps/macos-preview/build/librising_macos_live.dylib'))
        engine = Path(os.environ.get('RL_MACOS_ENGINE_LIBRARY', ROOT / 'apps/macos-preview/build/abi16-target/release/librising_engine.dylib'))
        inputs = Path(os.environ.get('RL_MACOS_NATIVE_INPUTS', ROOT / 'apps/macos-preview/build/native-inputs-v2'))
        if not all(p.exists() for p in (driver, engine, inputs)):
            self.skipTest('Explicit ABI1.6/native input build unavailable')
        from macos_native_driver import NativeDriver
        from macos_scripted_input import ScriptedInput, FrameAnswerMapper
        native = NativeDriver(driver, engine, inputs); self.addCleanup(native.close)
        if not hasattr(native.lib, 'macos_live_sound_capture'):
            self.skipTest('Supplied driver predates the sound transport')
        self.assertEqual(native.lib.macos_live_validation(native.handle, 0), 0)
        for _ in range(129):
            self.assertEqual(native.advance(), 0)
        self.assertEqual(native.lib.macos_live_sound_capture(native.handle, 1), 0)
        script = ScriptedInput(ROOT, (ROOT / 'pesquisas-paralelas/missoes/m3/entradas/P2.json').read_bytes())
        mapper = FrameAnswerMapper(script, hwnd=0)
        last = 150
        for frame in range(129, last + 1):
            mapper.begin_frame(frame); answers = mapper.declared_answers()
            for phase in (2, 3):
                self.assertEqual(native.input_phase(phase, answers), 0, bytes(native.status().message))
            mapper.queue.clear()
        events = native.sound_events()
        self.assertEqual(native.lib.macos_live_sound_dropped(native.handle), 0)
        # The engine names the CALL rel32 instruction; the log names its return address.
        requests = [(e.kind, e.frame, e.phase, e.site + 5, e.eax, e.edx, e.ebx, e.ecx, e.volume) for e in events if e.kind]
        expected = [event(row) for row in probe_log('P2') if row['routine'] != 'PlaySnd_Manage' and row['frame'] <= last]
        self.assertEqual(requests, [(e.kind, e.frame, e.phase, e.site, e.eax, e.edx, e.ebx, e.ecx, e.volume) for e in expected])
        self.assertEqual(len(requests), 3)
        # One Manage tick opens every play phase 2, frames 129..150.
        self.assertEqual(sorted({e.frame for e in events if e.kind == 0}), list(range(129, last + 1)))


if __name__ == '__main__':
    unittest.main()
