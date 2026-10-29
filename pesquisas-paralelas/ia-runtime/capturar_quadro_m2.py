"""Original-only M2 captures of the AI/runtime frame routines from the M1 post-load state.

    python3 -B pesquisas-paralelas/ia-runtime/capturar_quadro_m2.py \
        --saida pesquisas-paralelas/ia-runtime/evidencias/captura-quadro-m2-pos-carga.json

Input label: **M1 post-load input**. The intact executable runs the original
new-campaign startup and MissionLoad on Missions' committed whole-load bench
(``oraculo_carga_missao.BancadaCargaMissaoOriginal``, same declared Windows
inputs as the accepted v2 capture). The resulting image must equal the frozen
accepted M1 final state (``58a5020e…``) or nothing is captured. From that state,
each capture restores every block, enters one original routine with the
registers its CalculGame call site passes, and runs every callee natively.
No callee is stubbed; only the bench's declared I/O/import bindings answer, and
display, undeclared-import or fault boundaries stop the capture with its state
retained and recorded. Each capture records the SBL entry trace (callee,
return site, EAX/EDX/EBX/ECX), the inherited bytes read before written, every
changed byte and the final registers.

This is not the frame-1 input: the load-entry tail 0x42d22d..0x42d2de and the
frame steps before each routine have not run. Missions' first-frame oracle owns
that input; these captures are re-validated against it when it is published.
A failed run is preserved under ``.local/`` and exits nonzero.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time

from ambiente_ia_runtime import OWNED, ROOT
from inventario_quadro_m2 import M1_CAPTURE_SHA256, M1_FINAL_STATE_SHA256

MISSOES = ROOT / 'pesquisas-paralelas/missoes'
if str(MISSOES) not in sys.path:
    sys.path.insert(0, str(MISSOES))
import ambiente_missoes  # noqa: E402  (bootstraps the Missions bench imports)
from capturar_carga_missao_original import entradas  # noqa: E402
from emulador import HASH_ORIGINAL, unicorn, x86  # noqa: E402
from oraculo_carga_missao import (ARENA, DGROUP, BancadaCargaMissaoOriginal,  # noqa: E402
                                  OraculoInterrompido, RETORNO_MISSION_LOAD)
from vinculos_declarados import ParadaVinculoDeclarado  # noqa: E402

LABEL = 'M1 post-load input'
FILL, CLOCK = 0xa7, 0x00123456          # the accepted v2 capture's declared inputs
MISSION = 1                             # MissionGetNum at the M1 post-load state (byte 0x496fe4)
LIVE_UNITS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
LIVE_STRUCTURES = (0,)
TRACE_LIMIT = 200000
CAPTURE_SECONDS = 60.0
MERGE_GAP = 8


def captures():
    """(label, routine, registers) in CalculGame order, then per actual unit/structure.

    Registers reproduce the call sites: CalculNextReflect 0x42d35d (eax = player,
    edx = MissionGetNum low byte), ProcessInputGame 0x42d3b0 (eax = player byte),
    the dispatcher loops 0x456ead (EnginNextEtape eax = u16 unit), 0x456e65
    (IATestUtilite eax = 1, edx = u16 unit), 0x4282d3/0x4282da (IATestUtilite eax = 3,
    BatimentNextEtape eax = u16 structure).
    """
    result = [(f'calcul_next_reflect_p{p}', 'CalculNextReflect', {'EAX': p, 'EDX': MISSION}) for p in (1, 2, 3, 4)]
    result += [(f'process_input_game_p{p}', 'ProcessInputGame', {'EAX': p}) for p in range(4)]
    result += [('message_box_calcul', 'MessageBoxCalcul', {}), ('game_next_frame', 'GameNextFrame', {}),
               ('calcul_engin_next_etape', 'CalculEnginNextEtape', {}),
               ('calcul_batiment_next_etape', 'CalculBatimentNextEtape', {})]
    for unit in LIVE_UNITS:
        result += [(f'ia_test_utilite_unit{unit}', 'IATestUtilite', {'EAX': 1, 'EDX': unit}),
                   (f'engin_next_etape_unit{unit}', 'EnginNextEtape', {'EAX': unit})]
    for structure in LIVE_STRUCTURES:
        result += [(f'ia_test_utilite_structure{structure}', 'IATestUtilite', {'EAX': 3, 'EDX': structure}),
                   (f'batiment_next_etape_structure{structure}', 'BatimentNextEtape', {'EAX': structure})]
    return result


class Observador:
    """Entry trace and read-before-write footprint, reset before every capture."""

    def __init__(self, bench):
        self.bench = bench
        self.regions = [(DGROUP[0], DGROUP[1] - DGROUP[0]),
                        (ARENA[0], bench.arena.proximo - ARENA[0])]
        self.reset()
        cpu = bench.cpu
        for address in sorted(bench.nomes):
            if 0x401000 <= address < 0x493c00:
                cpu.hook_add(unicorn.UC_HOOK_CODE, self._entry, begin=address, end=address)
        for base, size in self.regions:
            cpu.hook_add(unicorn.UC_HOOK_MEM_READ, self._read, (base, size), begin=base, end=base + size - 1)
            cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._write, (base, size), begin=base, end=base + size - 1)

    def reset(self):
        self.trace, self.entries, self.last = [], 0, None
        self.written = {base: bytearray(size) for base, size in self.regions}
        self.read = {base: bytearray(size) for base, size in self.regions}
        self.reader = {base: {} for base, _ in self.regions}

    def _entry(self, cpu, address, size, _):
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        if self.last == (address, esp, self.entries):
            return                          # same instruction resumed after a segment boundary
        self.entries += 1
        if len(self.trace) < TRACE_LIMIT:
            ret = int.from_bytes(bytes(cpu.mem_read(esp, 4)), 'little')
            regs = [cpu.reg_read(r) for r in (x86.UC_X86_REG_EAX, x86.UC_X86_REG_EDX,
                                              x86.UC_X86_REG_EBX, x86.UC_X86_REG_ECX)]
            caller = self.bench.nome(ret) if 0x401000 <= ret < 0x493c00 else f'0x{ret:x}'
            self.trace.append(f'{self.bench.nomes[address]}@{caller} ' +
                              ' '.join(f'{v:x}' for v in regs))
        self.last = (address, esp, self.entries)

    def _read(self, cpu, access, address, size, value, region):
        base, length = region
        written, read, reader = self.written[base], self.read[base], self.reader[base]
        for offset in range(address - base, min(address - base + size, length)):
            if not written[offset] and not read[offset]:
                read[offset] = 1
                reader[offset] = cpu.reg_read(x86.UC_X86_REG_EIP)

    def _write(self, cpu, access, address, size, value, region):
        base, length = region
        start = address - base
        end = min(start + size, length)
        self.written[base][start:end] = b'\x01' * (end - start)

    def mark_binding_writes(self, events):
        for event in events:
            for write in event['memory_writes']:
                address, size = int(write['address'], 16), write['size']
                for base, length in self.regions:
                    if base <= address < base + length:
                        start = address - base
                        self.written[base][start:min(start + size, length)] = b'\x01' * min(size, length - start)

    def footprint(self):
        ranges = []
        for base, length in self.regions:
            read, reader = self.read[base], self.reader[base]
            i = 0
            while True:
                i = read.find(1, i)
                if i < 0:
                    break
                j = i
                while j < length and read[j]:
                    j += 1
                ranges.append([f'0x{base + i:08x}', j - i, self.bench.nome(reader[i])])
                i = j
        return ranges


def changed(before, after):
    """Changed byte runs (merged across gaps < MERGE_GAP) with original before/after bytes."""
    result = []
    for name in sorted(set(before) | set(after)):
        if name not in before or name not in after:
            result.append(dict(block=name, event='allocated' if name in after else 'released'))
            continue
        base, old = before[name]
        _, new = after[name]
        if old == new:
            continue
        runs, i, n = [], 0, len(old)
        while i < n:
            if old[i] == new[i]:
                i += 1
                continue
            j = i
            while j < n and old[j] != new[j]:
                j += 1
            if runs and i - runs[-1][1] < MERGE_GAP:
                runs[-1][1] = j
            else:
                runs.append([i, j])
            i = j
        for start, end in runs:
            result.append(dict(address=f'0x{base + start:08x}', size=end - start,
                               before=old[start:end].hex(), after=new[start:end].hex()))
    return result


def restore(bench, image):
    if set(image) != {f"alloc{r['index']:05d}" for r in bench.arena.ativos()} | {'dgroup', 'crt_thread_data'}:
        raise RuntimeError('Arena allocation set differs from the M1 post-load state; cannot restore')
    for base, data in image.values():
        bench.cpu.mem_write(base, data)


def registers(values):
    return {k: f'0x{v:x}' for k, v in values.items()}


def run(saida):
    revision = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True,
                              text=True).stdout.strip()
    dirty = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'pesquisas-paralelas/ia-runtime',
                            'pesquisas-paralelas/missoes'], capture_output=True, text=True).stdout
    sources = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (
        OWNED / 'capturar_quadro_m2.py', OWNED / 'inventario_quadro_m2.py', MISSOES / 'oraculo_carga_missao.py',
        MISSOES / 'fronteiras_carga_missao.py', MISSOES / 'capturar_carga_missao_original.py')}
    named = entradas(FILL, CLOCK)
    bench = BancadaCargaMissaoOriginal(named, segundos=120.0)
    report = dict(schema='rising-lands/ai-runtime-m2-capture/1', label=LABEL, original_sha256=HASH_ORIGINAL,
                  translation_executed=False, source_revision=revision, source_dirty_paths=dirty.splitlines(),
                  source_sha256=sources, named_inputs=named.manifesto(),
                  m1_reference=dict(capture='pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json',
                                    capture_sha256=M1_CAPTURE_SHA256, final_state_sha256=M1_FINAL_STATE_SHA256),
                  limits=dict(capture_seconds=CAPTURE_SECONDS, instructions_per_segment=bench.instrucoes_segmento,
                              trace_entries=TRACE_LIMIT),
                  captures=[])
    t0 = time.monotonic()
    phase = 'startup'
    try:
        bench.iniciar_relogio()
        bench.executar_inicio()
        phase = 'missionload'
        regs = bench.executar_mission_load(60.0)
        post = bench.imagem()
        summary = bench.resumo_imagem(post)
        report['m1_post_load'] = dict(real_return=f"0x{regs['EIP']:x}", al=regs['EAX'] & 0xff, summary=summary,
                                      seconds=round(time.monotonic() - t0, 3))
        if regs['EIP'] != RETORNO_MISSION_LOAD or summary['sha256'] != M1_FINAL_STATE_SHA256:
            raise RuntimeError('Replayed post-load state differs from the frozen accepted M1 final state')
        phase = 'capture'
        bench.fase = 'm2-capture'          # any display-boundary skip now stops a capture
        observer = Observador(bench)
        for label, routine, entry in captures():
            restore(bench, post)
            observer.reset()
            first_event = len(bench.vinculos_declarados.eventos)
            bench.limite_segundos = CAPTURE_SECONDS
            bench.iniciar_relogio()
            started = time.monotonic()
            record = dict(label=label, input=LABEL, routine=routine, entry=f'0x{bench.sym[routine]:08x}',
                          registers_in=registers(entry))
            try:
                out = bench.chamar(label, routine, entry)
                record['result'] = 'returned'
                record['registers_out'] = registers(out)
            except (OraculoInterrompido, ParadaVinculoDeclarado, RuntimeError) as error:
                record['result'] = 'stopped'
                record['stop'] = dict(type=type(error).__name__, reason=str(error)[:2000],
                                      detail=getattr(error, 'detalhe', None))
            events = bench.vinculos_declarados.eventos[first_event:]
            observer.mark_binding_writes(events)
            after = bench.imagem()
            record.update(
                seconds=round(time.monotonic() - started, 3), bindings=[
                    dict(name=e['name'], caller_return=e['caller_return'], status=e['status']) for e in events],
                entries=observer.entries, trace_truncated=observer.entries > len(observer.trace),
                trace_sha256=hashlib.sha256('\n'.join(observer.trace).encode()).hexdigest(), trace=observer.trace,
                footprint=observer.footprint(), changes=changed(post, after),
                state_after_sha256=bench.resumo_imagem(after)['sha256'])
            report['captures'].append(record)
            print(f"{label}: {record['result']} entries={record['entries']} changes={len(record['changes'])} "
                  f"{record['seconds']}s", flush=True)
        report['code_integrity'] = dict(exe_code_sha256=bench.sha256_codigo_exe, after=bench.sha256_codigo())
        status = 0
    except (OraculoInterrompido, ParadaVinculoDeclarado, RuntimeError) as error:
        report['stop'] = dict(phase=phase, type=type(error).__name__, reason=str(error)[:2000],
                              detail=getattr(error, 'detalhe', None))
        status = 2
    report['total_seconds'] = round(time.monotonic() - t0, 3)
    if status:
        saida = ROOT / '.local' / ('m2-capture-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as handle:
        json.dump(report, handle, indent=1, sort_keys=True)
        handle.write('\n')
    print(json.dumps(dict(output=str(saida), sha256=hashlib.sha256(saida.read_bytes()).hexdigest(),
                          result='captured' if not status else 'stopped', stop=report.get('stop', {}).get('reason'),
                          captures=len(report['captures']), total_seconds=report['total_seconds']), indent=1))
    return status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--saida', required=True)
    args = parser.parse_args()
    saida = ROOT / args.saida if not args.saida.startswith('/') else __import__('pathlib').Path(args.saida)
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    return run(saida)


if __name__ == '__main__':
    sys.exit(main())
