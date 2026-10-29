"""Extract static player-action evidence from the intact PE; never emulate it.

LLVM decodes a temporary ELF container whose .text is an exact .incbin of the
original BEGTEXT raw bytes. No PE normalization or translation is involved.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import tempfile

OWNED = Path(__file__).resolve().parent
ROOT = OWNED.parents[1]
INTACT_SHA = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
ROUTINES = (
    'WndProc', '_WinMain@16', 'ProgIteration', 'GrabAllInput', 'InputGame',
    'KeyboardInit', 'KeyPressed', 'KeyUnPressed', 'KeyTestRelease', 'MouseInit',
    'MouseZone', 'MouseEstDeplacer', 'Deselection', 'InputReceive', 'InputSend',
    'SetPlayerOrdre', 'ProcessInputGame', 'InitInputPlayer',
    'SetConstruitBatimentSelect', 'SetDeplaceEnginSelect', 'SetAttaqueEnginSelect',
    'SetRecolteEnginSelect', 'SetTransporteEnginSelect', 'SelectionEngin',
    'EnginAddSelection', 'DeSelectionGroupe', 'SelectionAddEngin', 'DeselectionEngin',
    'SetDeplaceEngin', 'SetEnginConstruitBatiment', 'SetRecolteEngin',
    'SetTransporteEngin', 'SetAttaqueEngin', 'ResetOrdre',
    'CalculConstruireBatiment', 'CalculWorkEngin', 'CalculTransporteEngin',
    'CalculAttaqueEngin', 'CalculEnginNextEtape', 'CalculBatimentNextEtape',
    'ConstruitPerso', 'InitRecruteTroupe', 'CalculTroupe', 'TerrainRecolte',
    'MineRecolte', 'BatimentConstruction', 'BatimentAlloc', 'TestFinDeMission',
    'TestFinDeMission6', 'CalculGame', 'MenuInit', 'MissionNext', 'MissionReStart',
    'EnginNextEtape', 'BatimentNextEtape', 'CreerBatiment', 'InitBatimentPlayer',
    'BatimentConstruit', 'BatimentAjouteMatiere', 'TerrainRetireMatiere',
    'SetDepotEnginSelect', 'SetMineEnginSelect', 'SetRamasseEnginSelect',
    'PartieGetResultat', 'BatimentGetTypeName', 'RechercheCalcul', 'CalculMatiere')
LINE = re.compile(r'^\s*([0-9a-f]+):\s+((?:[0-9a-f]{2}\s+)+)\s*([a-z][a-z0-9.]*)\s*(.*)$')


def sha(data): return hashlib.sha256(data).hexdigest()
def hx(value): return f'0x{value:08x}'


class OriginalPE:
    def __init__(self, path):
        self.path = Path(path).resolve()
        self.data = self.path.read_bytes()
        if sha(self.data) != INTACT_SHA: raise ValueError('Intact executable identity mismatch')
        pe = struct.unpack_from('<I', self.data, 0x3c)[0]
        n, opt_size = struct.unpack_from('<H', self.data, pe+6)[0], struct.unpack_from('<H', self.data, pe+20)[0]
        opt = pe+24
        self.base = struct.unpack_from('<I', self.data, opt+28)[0]
        self.sections = []
        for i in range(n):
            name, virtual_size, rva, size, offset = struct.unpack_from('<8sIIII', self.data, opt+opt_size+i*40)
            self.sections.append(dict(name=name.rstrip(b'\0').decode(), rva=rva, raw_size=size, raw_offset=offset))
        self.imports = {}
        rva = struct.unpack_from('<I', self.data, opt+104)[0]
        def string(addr):
            data = bytearray()
            for i in range(4096):
                value = self.read(addr+i, 1)[0]
                if value == 0: return data.decode('ascii')
                data.append(value)
            raise ValueError('Unterminated import string')
        descriptor = self.base+rva
        while True:
            lookup, _, _, name, iat = struct.unpack('<5I', self.read(descriptor, 20))
            if not any((lookup, name, iat)): break
            dll = string(self.base+name)
            index = 0
            while True:
                thunk = struct.unpack('<I', self.read(self.base+(lookup or iat)+4*index, 4))[0]
                if not thunk: break
                symbol = 'ordinal_'+str(thunk & 0xffff) if thunk & 0x80000000 else string(self.base+thunk+2)
                self.imports[self.base+iat+4*index] = dll+'!'+symbol
                index += 1
            descriptor += 20

    def offset(self, address, size=1):
        rva = address-self.base
        for section in self.sections:
            if section['rva'] <= rva and rva+size <= section['rva']+section['raw_size'] and section['raw_offset']:
                return section['raw_offset']+rva-section['rva']
        raise ValueError('Address is not in original file-backed bytes: '+hx(address))

    def read(self, address, size):
        offset = self.offset(address, size)
        return self.data[offset:offset+size]


def symbols():
    rows = [line.split('\t', 1) for line in (ROOT/'relatorios/simbolos-originais.tsv').read_text().splitlines()[1:]]
    return {name: int(address, 16) for address, name in rows}


def decode(obj, address, end, base):
    command = ['xcrun', 'llvm-objdump', '-d', '--x86-asm-syntax=intel', '--adjust-vma='+hx(base),
               '--start-address='+hex(address-base), '--stop-address='+hex(end-base), str(obj)]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    instructions = []
    for line in result.stdout.splitlines():
        match = LINE.match(line)
        if match:
            addr, raw, mnemonic, operands = match.groups()
            a = int(addr, 16)
            if address <= a < end:
                instructions.append(dict(address=hx(a), hex=''.join(raw.split()), mnemonic=mnemonic,
                                         operands=operands.split(' <', 1)[0].strip()))
    return instructions


def direct_target(instruction):
    raw = bytes.fromhex(instruction['hex'])
    if instruction['mnemonic'] == 'call' and len(raw) == 5 and raw[0] == 0xe8:
        return int(instruction['address'], 16)+5+struct.unpack('<i', raw[1:])[0]
    return None


def memory_operands(instructions):
    effects = []
    for ins in instructions:
        operands = ins['operands'].split(', ')
        for index, operand in enumerate(operands):
            if '[' not in operand: continue
            mnemonic = ins['mnemonic']
            if mnemonic == 'lea': mode = 'address_only'
            elif mnemonic.startswith(('cmp', 'test', 'push', 'call', 'j')): mode = 'read'
            elif mnemonic.startswith(('mov', 'set', 'pop')): mode = 'write' if index == 0 else 'read'
            elif index == 0: mode = 'read_write_or_instruction_specific'
            else: mode = 'read'
            width = next((v for k, v in [('qword ptr',8),('dword ptr',4),('word ptr',2),('byte ptr',1)] if k in operand), None)
            effects.append(dict(site=ins['address'], operand=operand, width_bytes=width, access=mode,
                                evidence='byte_proven_operand_encoding', limitation='Effective address and runtime execution not proven'))
    return effects


def command_paths(instructions, pe, names):
    by_address = {int(i['address'],16):i for i in instructions}
    table = struct.unpack('<40I', pe.read(0x45ed20, 160))
    cases = []
    for code, target in enumerate(table):
        todo, seen, calls = [target], set(), []
        while todo:
            site = todo.pop()
            if site in seen or site == 0x45f2de: continue
            seen.add(site)
            if site not in by_address: continue
            ins = by_address[site]; mnemonic = ins['mnemonic']; raw = bytes.fromhex(ins['hex'])
            callee = direct_target(ins)
            if callee is not None: calls.append(dict(site=hx(site),target=hx(callee),callee=names.get(callee, 'unlabeled'),hex=raw.hex()))
            match = re.fullmatch(r'0x([0-9a-f]+)', ins['operands'])
            branch = int(match.group(1),16) if match else None
            if mnemonic.startswith('ret'): continue
            if mnemonic.startswith('j'):
                if branch is not None: todo.append(branch)
                if mnemonic == 'jmp': continue
            todo.append(site+len(raw))
        cases.append(dict(command_u16=code, table_entry=hx(0x45ed20+4*code), branch=hx(target),
                          direct_calls=sorted(calls,key=lambda x:x['site']), evidence='byte_proven_table_and_static_cfg',
                          limitation='No player-input runtime trace; conditional callees are possible paths, not an execution sequence'))
    return cases


def extract(exe, output):
    output = Path(output)
    pe = OriginalPE(exe); syms = symbols(); names = {v:k for k,v in syms.items()}
    addresses = sorted(set(syms.values()))
    routines = []
    section = next(s for s in pe.sections if s['name'] == 'BEGTEXT')
    code_base = pe.base+section['rva']
    with tempfile.TemporaryDirectory(prefix='rising-player-actions-') as directory:
        temp = Path(directory); assembly = temp/'original-text.S'; obj = temp/'original-text.o'
        quoted = str(pe.path).replace('\\','\\\\').replace('"','\\"')
        assembly.write_text(f'.text\n.incbin "{quoted}", {section["raw_offset"]}, {section["raw_size"]}\n')
        subprocess.run(['xcrun','clang','-target','i386-pc-linux-gnu','-c',str(assembly),'-o',str(obj)],check=True,capture_output=True)
        for name in ROUTINES:
            address = syms[name]; end = next(a for a in addresses if a>address)
            raw = pe.read(address,end-address); instructions=decode(obj,address,end,code_base)
            for instruction in instructions:
                actual = pe.read(int(instruction['address'],16),len(bytes.fromhex(instruction['hex'])))
                if actual.hex()!=instruction['hex']: raise ValueError('Disassembler bytes differ from intact PE')
            calls=[]
            for ins in instructions:
                target=direct_target(ins)
                if target is not None:
                    calls.append(dict(site=ins['address'],hex=ins['hex'],target=hx(target),callee=names.get(target,'unlabeled'),kind='direct_e8', evidence='byte_proven_call_encoding'))
                elif ins['mnemonic']=='call':
                    slots=re.findall(r'\[0x([0-9a-f]+)\]',ins['operands'])
                    slot=int(slots[0],16) if slots else None
                    calls.append(dict(site=ins['address'],hex=ins['hex'],target=hx(slot) if slot else None,
                                      callee=pe.imports.get(slot,'unresolved_indirect'),kind='iat_indirect' if slot in pe.imports else 'unresolved_indirect',evidence='byte_proven_instruction_and_import_table' if slot in pe.imports else 'byte_proven_indirect_instruction_only'))
            routines.append(dict(name=name,address=hx(address),end_exclusive=hx(end),
                extent_basis='next imported symbol; not a proven function-return boundary',sha256=sha(raw),hex=raw.hex(),
                instructions=instructions,calls=calls,memory_operands=memory_operands(instructions)))
    process=next(r for r in routines if r['name']=='ProcessInputGame')
    evidence=dict(schema='rising-lands/player-action-static-byte-evidence/1',intact_executable_sha256=INTACT_SHA,
        source=str(pe.path),analysis='Static only; no native execution, no translation, no normalized PE input',
        provenance=dict(symbols='relatorios/simbolos-originais.tsv',symbols_sha256=sha((ROOT/'relatorios/simbolos-originais.tsv').read_bytes()),
                        disassembler='xcrun llvm-objdump --x86-asm-syntax=intel; ELF .text is exact original BEGTEXT .incbin'),
        scope='MONDE01 action and end-condition planning; execution and mission reachability are not inferred',
        imports={hx(k):v for k,v in sorted(pe.imports.items())},routines=routines,
        command_table=dict(address=hx(0x45ed20),hex=pe.read(0x45ed20,160).hex(),cases=command_paths(process['instructions'],pe,names)),
        structure_type_records=[dict(type_u8=t,address=hx(0x495d8c+t*52),bytes=52,
            hex=pe.read(0x495d8c+t*52,52).hex(),name_offset=19,
            name=pe.read(0x495d8c+t*52+19,33).split(b'\0',1)[0].decode('ascii')) for t in (2,3)])
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(dict(output=str(output),routines=len(routines),calls=sum(len(r['calls']) for r in routines),commands=40)))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();extract(args.exe,args.output)
