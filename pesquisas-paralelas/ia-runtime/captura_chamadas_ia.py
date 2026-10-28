"""Original-only call-order captures on core's x86 bench.

The intact routine runs instruction by instruction on ``emulador.BancadaX86``.
Every declared callee entry is a stop: the capture records the callee and its
register/stack arguments, applies the fixture's declared return (EAX and, for
Win32 stdcall imports, the stack cleanup) and resumes at the original return
address. Callees are therefore *not* executed; a capture claims only the
caller's own order, branches and stores. Routines listed as ``native`` are
executed from the image. Import slots are bound to declared thunk addresses
(the Windows loader's job); no Windows API is emulated.
"""
import struct

import ambiente_ia_runtime  # noqa: F401  (paths)
from emulador import BancadaX86, PILHA, RETORNO

THUNKS = RETORNO + 0x100
STACK_LOW, STACK_HIGH = PILHA, PILHA + 0x10000
CODE_END = 0x494000  # end of BEGTEXT in the intact image


class CaptureStop(RuntimeError):
    """A capture reached an address the fixture does not declare."""


class CallCapture:
    def __init__(self, image, bench=None):
        self.image = image
        self.bench = bench or BancadaX86()
        self.cpu = self.bench.cpu
        self.events, self.writes = [], []
        self.import_thunks = {}
        self._cleanups = {}
        self._hook = None

    # -- memory helpers -------------------------------------------------
    def write(self, address, data):
        self.cpu.mem_write(address, bytes(data))

    def u8(self, address, value=None):
        if value is not None:
            self.write(address, bytes([value & 0xff]))
        return self.cpu.mem_read(address, 1)[0]

    def u16(self, address, value=None):
        if value is not None:
            self.write(address, struct.pack('<H', value & 0xffff))
        return struct.unpack('<H', self.cpu.mem_read(address, 2))[0]

    def u32(self, address, value=None):
        if value is not None:
            self.write(address, struct.pack('<I', value & 0xffffffff))
        return struct.unpack('<I', self.cpu.mem_read(address, 4))[0]

    def reg(self, name, value=None):
        from unicorn import x86_const
        register = getattr(x86_const, 'UC_X86_REG_' + name.upper())
        if value is not None:
            self.cpu.reg_write(register, value & 0xffffffff)
        return self.cpu.reg_read(register)

    def bind_import(self, slot, stack_bytes):
        """Point an IAT slot at a declared thunk; the binding pops ``stack_bytes`` arguments."""
        if slot not in self.image.imports:
            raise ValueError(f'0x{slot:08x} is not an import slot')
        thunk = THUNKS + 0x10 * len(self.import_thunks)
        self.import_thunks[thunk] = (self.image.imports[slot], stack_bytes)
        self.u32(slot, thunk)
        return thunk

    def _record_write(self, _uc, _access, address, size, value, _data):
        if STACK_LOW <= address < STACK_HIGH or RETORNO <= address < RETORNO + 0x1000:
            return
        self.writes.append((self.reg('eip'), address, size, value & ((1 << (8 * size)) - 1)))

    # -- execution ------------------------------------------------------
    def run(self, entry, native, stubs, registers=None, stack=None, limit=400000, max_events=5000):
        """Execute ``entry`` with ``native`` intervals allowed and ``stubs`` as declared callees.

        ``stubs`` maps an address (callee entry or thunk) to a callable ``f(capture, call)``
        returning the EAX value; ``call`` holds the registers, return address and stack words.
        Returns the final registers. Events and writes accumulate on the instance.
        """
        import unicorn
        if self._hook is None:
            self._hook = self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._record_write)
        stops = set(stubs) | {RETORNO}
        result = self.bench.executar(entry, native, registers or {}, parada=stops, pilha=stack, limite_instrucoes=limit)
        while result['EIP'] != RETORNO:
            if len(self.events) >= max_events:
                raise CaptureStop('Capture exceeded its declared event budget')
            target = result['EIP']
            esp = result['ESP']
            ret = self.u32(esp)
            call = dict(target=target, ret=ret, eax=result['EAX'], ebx=result['EBX'], ecx=result['ECX'],
                        edx=result['EDX'], esi=result['ESI'], edi=result['EDI'],
                        stack=[self.u32(esp + 4 * i) for i in range(1, 5)])
            if target in self.import_thunks:
                name, cleanup = self.import_thunks[target]
            else:
                name, cleanup = self.image.name(target) or f'sub_{target:08x}', self._cleanup(target)
            value = stubs[target](self, call)
            event = dict(callee=f'0x{target:08x}', name=name, call_site=self._call_site(ret),
                         eax=f'0x{call["eax"]:08x}', edx=f'0x{call["edx"]:08x}',
                         ebx=f'0x{call["ebx"]:08x}', ecx=f'0x{call["ecx"]:08x}')
            if cleanup:
                event['stack_arguments'] = [f'0x{v:08x}' for v in call['stack'][:cleanup // 4]]
            if value is not None:
                event['declared_return'] = f'0x{value & 0xffffffff:08x}'
                self.reg('eax', value)
            self.events.append(event)
            self.reg('esp', esp + 4 + cleanup)
            result = self.bench.retomar(ret, native, parada=stops, limite_instrucoes=limit)
        return result

    def _cleanup(self, target):
        """A stubbed Watcom callee pops its pushed arguments exactly as its own ``ret N`` does."""
        if target not in self._cleanups:
            cleanup = self.image.stack_cleanup(target)
            if cleanup is None:
                raise CaptureStop(f'Stack cleanup of 0x{target:08x} is not statically determined')
            self._cleanups[target] = cleanup
        return self._cleanups[target]

    def _call_site(self, ret):
        """Address of the call ending at ``ret``; None when the stop was entered by a tail jump."""
        if not self.image.image_base + 0x1000 <= ret - 7 or ret > CODE_END:
            return None  # e.g. the bench's own return address after a tail jump into a stop
        for size in (5, 7, 6, 3, 2, 4):
            try:
                insn = self.image.instruction(ret - size)
            except ValueError:
                continue
            if insn.mnemonic == 'call' and insn.size == size:
                return f'0x{ret - size:08x}'
        return None

    def store_trace(self):
        return [dict(pc=f'0x{pc:08x}', address=f'0x{address:08x}', width=size, value=f'0x{value:0{2 * size}x}')
                for pc, address, size, value in self.writes]


def returns(value):
    """Stub returning a constant EAX."""
    return lambda _capture, _call: value


def returns_by_register(register, table, default=0):
    """Stub returning ``table[register & 0xff]`` (e.g. a per-player declared type)."""
    return lambda _capture, call: table.get(call[register] & 0xff, default)


def summarize_writes(writes, image=None):
    """Collapse a store trace into (address, width) cells with the first and last value.

    With ``image`` each cell names the original routine containing its first store.
    """
    cells = {}
    for entry in writes:
        key = (entry['address'], entry['width'])
        cell = cells.setdefault(key, dict(address=entry['address'], width=entry['width'], stores=0,
                                          first=entry['value'], last=entry['value'], first_pc=entry['pc']))
        if image is not None and 'routine' not in cell:
            cell['routine'] = image.owner(int(entry['pc'], 16))[1]
        cell['stores'] += 1
        cell['last'] = entry['value']
    return sorted(cells.values(), key=lambda c: (int(c['address'], 16), c['width']))


def regions(cells, gap=0x10):
    """Group touched cells into contiguous regions (labels are not inferred)."""
    result = []
    for cell in cells:
        start = int(cell['address'], 16)
        end = start + cell['width']
        if result and start <= result[-1]['end'] + gap:
            region = result[-1]
            region['end'] = max(region['end'], end)
            region['widths'].add(cell['width'])
            region['cells'] += 1
        else:
            region = dict(start=start, end=end, widths={cell['width']}, cells=1, routines=set())
            result.append(region)
        if cell.get('routine'):
            region['routines'].add(cell['routine'])
    return [dict(start=f'0x{r["start"]:08x}', end_exclusive=f'0x{r["end"]:08x}', size=r['end'] - r['start'],
                 widths=sorted(r['widths']), cells=r['cells'], routines=sorted(r['routines'])) for r in result]
