"""Unmodified original leaf calls restored from the real M2.3 part-09 full checkpoints.

No game routine is bridged or skipped. Hooks only record, or halt before a
named dependency. Native stack scratch is a declared zeroed 64-KiB leaf stack;
all checkpoint blocks (including display bytes) are retained without masks.
"""
import base64
import bisect
import hashlib
import json
import struct
import time
import zlib

from ambiente_combate_raid import ROOT

PREFIX = 'pesquisas-paralelas/missoes/evidencias/m2-3/captura-quadros9200-monde01-exibicao-v2'
REGS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP', 'EFLAGS')
# These are stops, never callbacks pretending the original callee returned.
DEPENDENCIES = {
    0x48aa79: 'PlaySnd_PostSound',
    0x48aacf: 'PlaySnd_PostVolume', 0x41a1ac: 'VoixOffAsk',
}


def checkpoints(frames=(9000, 9176)):
    """Use AI's pinned compressed reader and Missions' full-state decoder/summary."""
    from comparar_quadros_ia import carregar_captura
    from delta_estado_missao import _decodificar, resumo
    manifest_path = ROOT / (PREFIX + '.manifest.json')
    manifest = json.loads(manifest_path.read_bytes())
    pin = next(p for p in manifest['parts'] if p['part'] == 9)
    path = ROOT / pin['artifact']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == pin['compressed_sha256']
    part, raw_hash = carregar_captura(path, pin['raw_sha256'])
    states = {}
    for frame in frames:
        phase = next(p for p in part['phases'] if p['phase'] == f'frame{frame}')
        state = {n: (int(b['base'], 16), _decodificar(b)) for n, b in phase['state_after']['full_state'].items()}
        if resumo(state) != phase['state_after']['summary']:
            raise ValueError(f'Checkpoint frame{frame} summary mismatch')
        states[frame] = (state, {k: int(v, 16) for k, v in phase['exit']['registers'].items()})
    provenance = dict(manifest=str(manifest_path.relative_to(ROOT)),
                      manifest_sha256=hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                      artifact=pin['artifact'], compressed_sha256=pin['compressed_sha256'], raw_sha256=raw_hash,
                      checkpoints={str(f): resumo(s[0]) for f, s in states.items()})
    return states, provenance


class BancadaCombateRaid:
    def __init__(self, state):
        from emulador import BancadaX86, mapear_paginas, PILHA, RETORNO, x86, unicorn
        from oraculo_carga_missao import simbolos
        self.x86, self.unicorn, self.stack, self.return_address = x86, unicorn, PILHA, RETORNO
        self.b = BancadaX86()
        self.cpu = self.b.cpu
        for hook in list(self.cpu._callbacks):
            self.cpu.hook_del(hook)
        self.names = {a: n for n, a in simbolos().items()}
        self.symbols = {n: a for a, n in self.names.items()}
        present = {p for a, z, _ in self.cpu.mem_regions() for p in range(a, z + 1, 4096)}
        needed = {p for base, data in state.values() for p in range(base & ~4095, (base + len(data) + 4095) & ~4095, 4096)}
        mapear_paginas(self.cpu, needed - present, unicorn.UC_PROT_READ | unicorn.UC_PROT_WRITE)
        self.layout = {n: (base, len(data)) for n, (base, data) in state.items()}
        self.bases = sorted((base, base + n, name) for name, (base, n) in self.layout.items())
        self.starts = [a for a, _, _ in self.bases]
        self.restore(state)
        self.cpu.mem_protect(0x400000, 0x200000, unicorn.UC_PROT_READ | unicorn.UC_PROT_WRITE)
        self.cpu.mem_protect(0x401000, 0x93000, unicorn.UC_PROT_READ | unicorn.UC_PROT_EXEC)
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._store)
        self.cpu.hook_add(unicorn.UC_HOOK_BLOCK, self._block)
        self.cpu.ctl_flush_tb()
        self.active = False

    def restore(self, state):
        for base, data in state.values():
            self.cpu.mem_write(base, data)

    def read(self, address, n):
        return bytes(self.cpu.mem_read(address, n))

    def u16(self, address):
        return struct.unpack('<H', self.read(address, 2))[0]

    def u32(self, address):
        return struct.unpack('<I', self.read(address, 4))[0]

    def record(self, unit):
        return self.u32(0x4e19a0) + unit * 276

    def snapshot(self):
        return {n: (a, self.read(a, size)) for n, (a, size) in self.layout.items()}

    def _store(self, cpu, access, address, size, value, _):
        if not self.active or self.stack <= address < self.stack + 65536:
            return
        i = bisect.bisect_right(self.starts, address) - 1
        if i < 0 or address + size > self.bases[i][1]:
            self.outside.append([hex(address), size])
        self.stores.append([hex(cpu.reg_read(self.x86.UC_X86_REG_EIP)), hex(address), size,
                            hex(value & ((1 << (8 * size)) - 1))])

    def registers(self):
        return {r: self.cpu.reg_read(getattr(self.x86, 'UC_X86_REG_' + r)) for r in REGS}

    def _block(self, cpu, address, size, _):
        if not self.active:
            return
        if address in self.stops:
            self.stopped = address
            cpu.emu_stop()
            return
        if address in self.names:
            regs = self.registers()
            self.entries.append(dict(routine=self.names[address], address=hex(address),
                                     caller_return=hex(self.u32(regs['ESP'])),
                                     registers={k: hex(v) for k, v in regs.items() if k in ('EAX', 'EDX', 'EBX', 'ECX')}))

    def call(self, name, registers, *, words=(), stops=DEPENDENCIES, seconds=5):
        """Fresh declared leaf stack per call; state persists until explicit restore."""
        from delta_estado_missao import delta, resumo
        regs = dict(EAX=0x13579bdf, EBX=0x2468ace0, ECX=0x31415926, EDX=0x27182818,
                    ESI=0x12345678, EDI=0x23456789, EBP=0x3456789a, ESP=self.stack + 0x8000, EFLAGS=2)
        regs.update(registers)
        self.cpu.mem_write(self.stack, bytes(65536))
        self.cpu.mem_write(regs['ESP'], struct.pack('<' + 'I' * (1 + len(words)), self.return_address, *words))
        for r, v in regs.items():
            self.cpu.reg_write(getattr(self.x86, 'UC_X86_REG_' + r), v & 0xffffffff)
        entry = self.symbols[name]
        self.cpu.reg_write(self.x86.UC_X86_REG_EIP, entry)
        before = self.snapshot()
        self.stores, self.entries, self.outside = [], [], []
        self.stops = set(stops)
        self.stopped = None
        self.active = True
        t0 = time.monotonic()
        try:
            self.cpu.emu_start(entry, self.return_address, timeout=int(seconds * 1e6), count=2000000)
            result = self.registers()
            fault = None
        except self.unicorn.UcError as exc:
            result = self.registers()
            fault = str(exc)
        finally:
            self.active = False
        after = self.snapshot()
        record = dict(routine=name, entry_registers={k: hex(v) for k, v in dict(regs, EIP=entry).items()},
                      exit_registers={k: hex(v) for k, v in result.items()}, stack_words=list(words),
                      reached_return=result['EIP'] == self.return_address,
                      stop=stops.get(result['EIP']) if hasattr(stops, 'get') else None,
                      fault=fault, limit=not fault and result['EIP'] != self.return_address and self.stopped is None,
                      state_before=resumo(before), state_after=resumo(after), delta=delta(before, after),
                      stop_stack_words=list(struct.unpack('<4I', self.read(result['ESP']+4,16))),
                      stores=self.stores, entries=self.entries, writes_outside_checkpoint=self.outside,
                      seconds=round(time.monotonic() - t0, 4))
        return record, before, after
