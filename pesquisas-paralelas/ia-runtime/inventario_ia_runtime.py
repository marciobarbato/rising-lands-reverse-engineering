"""Static inventory of the intact executable for the AI/runtime contract.

Everything here reads original bytes only: routine intervals come from the
original SBL symbols decoded by core's ``simbolos_ia``, control flow is followed
instruction by instruction, and jump tables are read from the image. Nothing is
executed and no behavior is inferred from names; names only label addresses.
"""
import bisect
import hashlib
from pathlib import Path
import struct

from ambiente_ia_runtime import EXE, SBL, ORIGINAL_SHA256
from analisar import dependencias
from simbolos_ia import enderecar_simbolos, ler_sbl

READ, WRITE = 1, 2
CONDITIONAL = frozenset(('ja', 'jae', 'jb', 'jbe', 'je', 'jne', 'jg', 'jge', 'jl', 'jle', 'jo', 'jno',
                         'js', 'jns', 'jp', 'jnp', 'jcxz', 'jecxz', 'loop', 'loope', 'loopne'))


class OriginalImage:
    """Intact RISING.EXE mapped by its section table, plus its original SBL names."""

    def __init__(self, executable=EXE, symbols=SBL):
        self.raw = Path(executable).read_bytes()
        if hashlib.sha256(self.raw).hexdigest() != ORIGINAL_SHA256:
            raise ValueError('Original EXE SHA-256 mismatch')
        pefile, capstone = dependencias()
        self.pe = pefile.PE(data=self.raw)
        self.image_base = self.pe.OPTIONAL_HEADER.ImageBase
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        self.md.detail = True
        self.capstone = capstone
        base, _ = enderecar_simbolos(ler_sbl(Path(symbols).read_bytes()))
        self.names = {}
        for symbol in ler_sbl(Path(symbols).read_bytes()):
            self.names.setdefault(base + symbol.deslocamento, []).append(symbol.nome)
        self.starts = sorted(self.names)
        self.imports = {}
        for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
            for item in entry.imports:
                name = item.name.decode() if item.name else f'#{item.ordinal}'
                self.imports[item.address] = f'{entry.dll.decode()}!{name}'
        self._cache = {}

    def read(self, start, end):
        if not self.image_base <= start < end:
            raise ValueError('Invalid interval')
        data = self.pe.get_data(start - self.image_base, end - start)
        if len(data) != end - start:
            raise ValueError(f'Interval 0x{start:x}..0x{end:x} is outside the mapped image')
        return data

    def dword(self, address):
        return struct.unpack('<I', self.read(address, address + 4))[0]

    def table(self, address, count):
        return [self.dword(address + 4 * i) for i in range(count)]

    def name(self, address):
        names = self.names.get(address)
        return names[0] if names else None

    def symbol_end(self, address):
        """Next SBL symbol; past the last one (unnamed runtime code), the end of its section."""
        index = bisect.bisect_right(self.starts, address)
        if index < len(self.starts):
            return self.starts[index]
        for section in self.pe.sections:
            start = self.image_base + section.VirtualAddress
            if start <= address < start + max(section.Misc_VirtualSize, section.SizeOfRawData):
                return start + max(section.Misc_VirtualSize, section.SizeOfRawData)
        raise ValueError(f'0x{address:08x} is outside every section')

    def owner(self, address):
        index = bisect.bisect_right(self.starts, address) - 1
        start = self.starts[index]
        return start, self.names[start][0]

    def instruction(self, address):
        if address not in self._cache:
            found = next(self.md.disasm(self.read(address, address + 16), address, 1), None)
            if found is None:
                raise ValueError(f'Undecodable instruction at 0x{address:08x}')
            self._cache[address] = found
        return self._cache[address]

    def decode(self, start, end, strict=True):
        """Linear decoding of [start, end); non-strict decoding stops before padding/data."""
        result, address = [], start
        while address < end:
            try:
                insn = self.instruction(address)
            except ValueError:
                if strict:
                    raise
                break
            if address + insn.size > end:
                break
            result.append(insn)
            address += insn.size
        if strict and address != end:
            raise ValueError(f'Interval 0x{start:x}..0x{end:x} does not end on an instruction boundary')
        return result

    def code_end(self, walked, start, end):
        """End of the last reached instruction inside [start, end); the rest is padding or data."""
        reached = [a + self.instruction(a).size for a in walked['visited'] if start <= a < end]
        return max(reached) if reached else start

    def listing(self, start, end, title, code_end=None):
        code_end = end if code_end is None else code_end
        lines = [f'; {title}; intact original SHA-256 {ORIGINAL_SHA256}',
                 f'; interval 0x{start:08x}..0x{end:08x} (end exclusive); labels are original SBL names']
        for insn in self.decode(start, code_end):
            label = ' ; ' + ' / '.join(self.names[insn.address]) if insn.address in self.names and insn.address != start else ''
            target = self.direct_target(insn)
            note = ''
            if target is not None and self.name(target):
                note = ' ; -> ' + self.name(target)
            elif self.import_slot(insn) is not None:
                note = ' ; -> ' + self.imports[self.import_slot(insn)]
            lines.append(f'{insn.address:08x}  {insn.bytes.hex():<24} {insn.mnemonic} {insn.op_str}'.rstrip() + note + label)
        if code_end < end:
            tail = self.read(code_end, end)
            lines.append(f'; 0x{code_end:08x}..0x{end:08x} not reached by any static path (padding or data):')
            lines.extend(f'{code_end + i:08x}  .byte {tail[i:i + 16].hex()}' for i in range(0, len(tail), 16))
        return '\n'.join(lines) + '\n'

    @staticmethod
    def direct_target(insn):
        if insn.mnemonic in ('call', 'jmp') or insn.mnemonic in CONDITIONAL:
            if len(insn.operands) == 1 and insn.operands[0].type == 2:  # X86_OP_IMM
                return insn.operands[0].imm & 0xffffffff
        return None

    def import_slot(self, insn):
        if insn.mnemonic in ('call', 'jmp') and len(insn.operands) == 1 and insn.operands[0].type == 3:
            mem = insn.operands[0].mem
            if mem.base == 0 and mem.index == 0 and (mem.disp & 0xffffffff) in self.imports:
                return mem.disp & 0xffffffff
        return None

    def jump_table(self, insn, linear):
        """Return (table, count) for ``jmp [reg*4 + table]`` bounded by the preceding cmp/ja."""
        if insn.mnemonic != 'jmp' or len(insn.operands) != 1 or insn.operands[0].type != 3:
            return None
        mem = insn.operands[0].mem
        if mem.base != 0 or mem.index == 0 or mem.scale != 4:
            return None
        position = linear.index(insn.address)
        for back in range(1, 8):
            if position - back - 1 < 0:
                break
            compare = self.instruction(linear[position - back - 1])
            follow = self.instruction(linear[position - back])
            if compare.mnemonic == 'cmp' and compare.operands[1].type == 2 and follow.mnemonic == 'ja':
                return mem.disp & 0xffffffff, (compare.operands[1].imm & 0xff) + 1
        raise ValueError(f'Unbounded jump table at 0x{insn.address:08x}')

    def walk(self, entry, inside, stops=()):
        """Follow every static path from ``entry`` until ``ret``, a stop or a tail call.

        ``inside`` is a list of (start, end) intervals belonging to the routine. A jump
        leaving them to an unnamed address is a shared Watcom tail and is followed; a
        jump to a named routine is a tail call. Calls do not end a path.
        """
        stops = set(stops)
        linear = []
        for start, end in inside:
            linear.extend(i.address for i in self.decode(start, end, strict=False))
        linear.sort()
        seen, work = set(), [entry]
        calls, imports, indirect, tails, reached, tables, shared, returns = {}, {}, [], {}, set(), {}, set(), []
        while work:
            address = work.pop()
            while True:
                if address in stops:
                    reached.add(address)
                    break
                if address in seen:
                    break
                seen.add(address)
                within = any(start <= address < end for start, end in inside)
                if not within:
                    if address in self.names:
                        tails[address] = self.name(address)
                        break
                    shared.add(address)
                insn = self.instruction(address)
                target = self.direct_target(insn)
                following = address + insn.size
                if insn.mnemonic == 'call':
                    if target is not None:
                        calls.setdefault(target, []).append(address)
                    elif self.import_slot(insn) is not None:
                        imports.setdefault(self.imports[self.import_slot(insn)], []).append(address)
                    else:
                        indirect.append(address)
                    address = following
                elif insn.mnemonic in CONDITIONAL:
                    work.append(target)
                    address = following
                elif insn.mnemonic == 'jmp':
                    if target is not None:
                        address = target
                        continue
                    if self.import_slot(insn) is not None:  # import thunk: jmp [IAT slot]
                        imports.setdefault(self.imports[self.import_slot(insn)], []).append(address)
                        break
                    found = self.jump_table(insn, linear) if within else None
                    if found is None:
                        indirect.append(address)
                        break
                    table, count = found
                    targets = self.table(table, count)
                    tables[address] = dict(table=table, count=count, targets=targets)
                    work.extend(targets)
                    break
                elif insn.mnemonic in ('ret', 'retf', 'iret'):
                    returns.append(address)
                    break
                else:
                    address = following
        return dict(entry=entry, instructions=len(seen), visited=sorted(seen), calls=calls, imports=imports, indirect_calls=sorted(indirect),
                    tail_calls=tails, stops_reached=sorted(reached), jump_tables=tables, returns=sorted(returns),
                    shared_addresses=sorted(shared))

    def stack_cleanup(self, entry, _seen=None):
        """Bytes a callee pops on return (``ret N``), read from its own reachable returns."""
        _seen = _seen or set()
        if entry in _seen:
            return None
        _seen.add(entry)
        walked = self.walk(entry, [(entry, self.symbol_end(entry))])
        sizes = {(self.instruction(r).operands[0].imm if self.instruction(r).operands else 0) for r in walked['returns']}
        for target in walked['tail_calls']:
            tail = self.stack_cleanup(target, _seen)
            if tail is not None:
                sizes.add(tail)
        if len(sizes) > 1:
            raise ValueError(f'Inconsistent stack cleanup for 0x{entry:08x}: {sorted(sizes)}')
        return sizes.pop() if sizes else None

    def shared_chunks(self, walked):
        """Group the shared-tail instruction addresses of ``walk`` into exported intervals."""
        chunks = []
        for address in walked['shared_addresses']:
            end = address + self.instruction(address).size
            if chunks and chunks[-1][1] == address:
                chunks[-1][1] = end
            else:
                chunks.append([address, end])
        return [tuple(c) for c in chunks]

    def absolute_accesses(self, start, end, visited=None):
        """Global memory operands (absolute displacement) with width and access kind.

        With ``visited`` only statically reached instructions are inspected.
        """
        result = []
        decoded = ([self.instruction(a) for a in sorted(visited) if start <= a < end] if visited is not None
                   else self.decode(start, end))
        for insn in decoded:
            if insn.mnemonic == 'lea':
                continue
            for operand in insn.operands:
                if operand.type != 3:
                    continue
                mem = operand.mem
                disp = mem.disp & 0xffffffff
                if disp < self.image_base or disp >= 0x600000 or self.import_slot(insn) is not None:
                    continue
                if insn.mnemonic == 'jmp' and mem.index:
                    continue
                access = ('r' if operand.access & READ else '') + ('w' if operand.access & WRITE else '')
                result.append(dict(instruction=insn.address, address=disp, width=operand.size, access=access,
                                   base=insn.reg_name(mem.base) if mem.base else None,
                                   index=insn.reg_name(mem.index) if mem.index else None,
                                   scale=mem.scale if mem.index else None))
        return result

    def immediate_before(self, call, register='edx', lookback=10):
        """Value loaded into ``register`` (or its low parts) before ``call`` in the same routine."""
        start, _ = self.owner(call)
        aliases = {'edx': ('edx', 'dx', 'dl'), 'eax': ('eax', 'ax', 'al'), 'ebx': ('ebx', 'bx', 'bl')}[register]
        linear = [i.address for i in self.decode(start, call + self.instruction(call).size, strict=False)]
        position = linear.index(call)
        for address in reversed(linear[max(0, position - lookback):position]):
            insn = self.instruction(address)
            written = [insn.reg_name(r) for r in insn.regs_access()[1]]
            if not any(alias in written for alias in aliases):
                if insn.mnemonic in ('call', 'ret', 'jmp'):
                    return None
                continue
            if insn.mnemonic == 'mov' and insn.operands[1].type == 2:
                return insn.operands[1].imm & 0xffffffff
            return None
        return None


def interval_record(image, name, start, end, kind='code'):
    data = image.read(start, end)
    return dict(name=name, kind=kind, start=f'0x{start:08x}', end_exclusive=f'0x{end:08x}', size=end - start,
                sha256=hashlib.sha256(data).hexdigest())
