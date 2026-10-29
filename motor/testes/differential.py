"""Compare every selected frozen call: Rust C ABI vs original AND unchanged Python.

Only captured bytes are declared. No entire mission snapshot, zero-filled heap,
original media, optional emulation module, Python simulation or app is needed.
"""
import argparse
from collections import Counter
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys

from pilot_abi import ENGINE, ROOT, Pilot, ROUTINES

ORIGINAL = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
CAPTURES = {
    'evidencias/fundacoes-quadro/captura-chamadas-quadro1.json': {'Random': 16},
    'evidencias/fundacoes-quadro/captura-exibicao-quadro1.json': {'Random': 8, 'LongRand': 12, 'rand': 12},
    'pesquisas-paralelas/economia/evidencias/captura-consultas-economia-exibicao-v2.json': {'IntToBCD': 19, 'BCDToInt': 8},
}


def verify_pins(pins=None):
    pins = pins if pins is not None else json.loads((ENGINE / 'testes/reference-pins.json').read_text())
    for path, expected in pins.items():
        actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError('ReferenceIdentityMismatch: ' + path)
    return pins


def references():
    sys.path.insert(0, str(ROOT / 'ferramentas'))
    sys.path.insert(0, str(ROOT / 'pesquisas-paralelas/economia'))
    core = importlib.import_module('chamadas_quadro_core')
    provider = importlib.import_module('provedores_economia_quadro')
    memory = importlib.import_module('memoria_quadro_core')
    return core, provider.q, memory.MemoriaQuadro


def declared_input(case):
    known = {}
    def declare(address, value):
        address = int(address, 16)
        if value is None or not 0 <= value <= 255:
            raise ValueError('UncapturedInputByte')
        if address in known and known[address] != value:
            raise ValueError('ConflictingCapturedInput')
        known[address] = value
    for address, value, *_ in case['read_before_write']:
        declare(address, value)
    for key in ('changed_bytes', 'caller_stack_changes'):
        for address, old, _ in case.get(key, []):
            declare(address, old)
    for key in ('written_unchanged', 'caller_stack_written_unchanged'):
        for address, value in case.get(key, []):
            declare(address, value)
    blocks = []
    for address, value in sorted(known.items()):
        if blocks and blocks[-1][0] + len(blocks[-1][1]) == address:
            blocks[-1][1].append(value)
        else:
            blocks.append((address, bytearray([value])))
    return [(address, bytes(data)) for address, data in blocks]


def changed_bytes(before, after):
    if [(a, len(b)) for a, b in before] != [(a, len(b)) for a, b in after]:
        raise AssertionError('ProjectionRegionIdentityMismatch')
    return [(address + i, old, new)
            for (address, data), (_, output) in zip(before, after)
            for i, (old, new) in enumerate(zip(data, output)) if old != new]


def expected_changes(case):
    return sorted((int(address, 16), old, new)
                  for key in ('changed_bytes', 'caller_stack_changes')
                  for address, old, new in case.get(key, []))


def python_call(core, economy, memory_type, name, blocks, input_registers):
    buffers = [(address, bytearray(data)) for address, data in blocks]
    memory = memory_type(buffers)
    registers = dict(input_registers)
    if name == 'Random':
        registers.update(core.aleatorio_mundo_memoria(memory))
    elif name in ('LongRand', 'rand'):
        registers.update(core.aleatorio_crt_memoria(memory))
    elif name == 'IntToBCD':
        economy.escrever_bcd(memory, registers['EAX'], registers['EDX'])
        # Python provider is void. Separate original-byte ABI adapter, NOT
        # a fabricated Python-return value: final DIV has AX=0, DX=1.
        registers.update(EAX=0, EDX=1)
    elif name == 'BCDToInt':
        economy.ler_bcd(memory, registers['EAX'], registers['EDX'])
        # Same adapter: original multiplier is10000 after four iterations.
        registers['EDX'] = 10000
    else:
        raise ValueError('UnknownRoutine')
    return [(address, bytes(data)) for address, data in buffers], registers


def run(library=None):
    pins = verify_pins()
    core, economy, memory_type = references()
    pilot = Pilot(library)
    counts, rng_counts = Counter(), Counter()
    records, failures = [], []
    for relative, expected in CAPTURES.items():
        capture = json.loads((ROOT / relative).read_text())
        if capture['original_sha256'] != ORIGINAL or capture['translation_executed'] is not False:
            raise ValueError('OriginalCaptureProvenanceMismatch: ' + relative)
        cases = [c for c in capture['calls'] if c['routine'] in expected]
        if Counter(c['routine'] for c in cases) != Counter(expected):
            raise ValueError('CaptureCoverageMismatch: ' + relative)
        for index, case in enumerate(cases):
            name = case['routine']
            record = dict(capture=relative, selected_index=index, routine=name, phase=case['phase'])
            handle = pilot.create()
            try:
                if not case.get('reached_return', case.get('reached_exit', False)):
                    raise ValueError('CaptureDidNotReturn')
                before = declared_input(case)
                input_registers = {k.upper(): int(case['entry_registers'][k.upper()], 16)
                                   for k in ('eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp')}
                native_registers = {k: int(case['exit_registers'][k], 16) for k in input_registers}
                pilot.load(handle, before)
                if pilot.project(handle) != before:
                    raise AssertionError('LoadProjectRoundTripMismatch')
                rust_registers = pilot.step(handle, name, input_registers)
                after = pilot.project(handle)
                python_after, python_registers = python_call(core, economy, memory_type, name, before, input_registers)
                original_changes = expected_changes(case)
                if changed_bytes(before, after) != original_changes:
                    raise AssertionError('RustOriginalChangedBytesMismatch')
                if changed_bytes(before, python_after) != original_changes:
                    raise AssertionError('PythonOriginalChangedBytesMismatch')
                if after != python_after:
                    raise AssertionError('RustPythonWholeProjectionMismatch')
                if rust_registers != native_registers or python_registers != native_registers:
                    raise AssertionError('ReturnRegisterMismatch: ' + str(dict(rust=rust_registers, python_adapter=python_registers, original=native_registers)))
                if pilot.clock(handle) != (0, 0):
                    raise AssertionError('RoutineAdvancedFrameClock')
                if name in ('Random', 'LongRand', 'rand'):
                    seed_address = 0x497164 if name == 'Random' else memory_type([(a,bytearray(b)) for a,b in before]).u32(0x522244) + 12
                    rust_seed = memory_type([(a,bytearray(b)) for a,b in after]).u32(seed_address)
                    python_seed = memory_type([(a,bytearray(b)) for a,b in python_after]).u32(seed_address)
                    original_after = [(a,bytearray(b)) for a,b in before]
                    native_memory = memory_type(original_after)
                    for address, _, new in original_changes:
                        native_memory.u8(address, new)
                    if not rust_seed == python_seed == native_memory.u32(seed_address):
                        raise AssertionError('RngStateMismatch')
                    rng_counts[name] += 1
                    record['rng_seed'] = hex(rust_seed)
                record.update(passed=True, declared_bytes=sum(len(b) for _,b in before), changed_bytes=len(original_changes), data_registers_checked=7)
                counts[name] += 1
            except Exception as error:
                record.update(passed=False, error=type(error).__name__ + ': ' + str(error))
                failures.append(record)
            finally:
                pilot.free(handle)
            records.append(record)
    return dict(schema='rising-lands/rust-pilot-differential/1', original_sha256=ORIGINAL,
                source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                library=str(pilot.path), library_sha256=hashlib.sha256(pilot.path.read_bytes()).hexdigest(),
                abi_version=hex(pilot.lib.rl_versao()), reference_pins=pins, by_routine=dict(counts),
                rng_checks=dict(rng_counts), comparisons=len(records), mismatches=len(failures), skipped=0,
                passed=not failures, failures=failures, records=records,
                register_scope='Seven data GPRs; original-byte ABI adapter for void Python BCD providers. No EIP/ESP/flags emulation.',
                capture_scope='75 captured records; nested LongRand/rand records are counted separately. No new original execution.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--library', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output and (args.output.exists() or args.output.is_symlink()):
        parser.error('Refusing to overwrite evidence: ' + str(args.output))
    result = run(args.library)
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as destination:
            destination.write(text)
    print(json.dumps({k:result[k] for k in ('passed','comparisons','by_routine','mismatches','skipped')}, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
