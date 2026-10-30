"""Fresh original/adapter comparison at S1's captured detection-handler entry.

The original full handler and every native callee execute unchanged. Compare
all seven registers/ESP, every final byte and ordered non-unit byte stores.
Combat owns its live-record store sequence. Declared register sentinels, the
captured original post-state and a no-battle variant remain separate cases.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente_ia_runtime import ROOT, ORIGINAL_SHA256
from emulador import BancadaX86, PILHA, RETORNO, mapear_paginas
from validar_donos_economia_s1_ia import Memory
from deteccao_conflito_ia import detectar_registradores, REG7

CAPTURE = ROOT/'pesquisas-paralelas/ia-runtime/evidencias/s1-deteccao-conflito-original-v2.json'


class DetectionMemory(Memory):
    """Sparse memory with real aliased complete records for Combat's buffer API."""
    def __init__(self, runs, records):
        super().__init__(runs)
        self.records = [(int(a, 16), bytearray(self.dados[int(a, 16)+i] for i in range(len(h)//2)))
                        for a, h in records]

    def _acesso(self, a, n, v):
        for base, buf in self.records:
            if base <= a and a+n <= base+len(buf):
                if v is None:
                    return int.from_bytes(buf[a-base:a-base+n], 'little')
                self.stores.append((a, n, v & ((1 << (8*n))-1)))
                buf[a-base:a-base+n] = (v & ((1 << (8*n))-1)).to_bytes(n, 'little')
                self.escritos.update(range(a, a+n))
                return v
        return super()._acesso(a, n, v)

    def vista(self, a, n):
        for base, buf in self.records:
            if base <= a and a+n <= base+len(buf):
                return memoryview(buf)[a-base:a-base+n]
        raise KeyError(f'No captured complete live view at {a:#x}+{n}')


def bytes_of(stores):
    return [(a+i, v >> (8*i) & 255) for a, n, v in stores for i in range(n)]


def compare(case, variant, regs, patches=()):
    import unicorn
    from unicorn import x86_const as X
    runs = list(case['read_before_write'])+list(case['adapter_entry_spans'])
    runs += [[a, f'{old:02x}'] for a, old, new in case['changed_bytes']]
    runs += list(patches)
    m = DetectionMemory(runs, case['adapter_entry_spans'][:2])
    original = dict(m.dados)
    out = detectar_registradores(m, regs)
    b = BancadaX86()
    uc = b.cpu
    regions = list(uc.mem_regions())
    addresses = set(original)
    stores_ref = [(int(s[1], 16), s[2], int(s[3], 16)) for s in case['stores']]
    addresses.update(a+i for a, n, v in stores_ref for i in range(n))
    mapear_paginas(uc, {a & ~4095 for a in addresses if not any(lo <= a <= hi for lo, hi, _ in regions)})
    for a, h in runs:
        uc.mem_write(int(a, 16), bytes.fromhex(h))
    stores = []

    def write(cpu, access, a, n, v, extra):
        if not PILHA <= a < PILHA+65536:
            stores.append((a, n, v & ((1 << (n*8))-1)))
    uc.hook_add(unicorn.UC_HOOK_MEM_WRITE, write)
    uc.ctl_flush_tb()
    for k, v in regs.items():
        uc.reg_write(getattr(X, 'UC_X86_REG_'+k), v)
    uc.mem_write(regs['ESP'], RETORNO.to_bytes(4, 'little'))
    native = b.retomar(0x489b5a, [(0x401000, 0x494000)], parada=RETORNO, limite_instrucoes=1000000)
    if native['EIP'] != RETORNO:
        raise RuntimeError('Original detection did not return')
    dif = {k: [hex(out[k]), hex(native[k])] for k in REG7+('ESP',) if out[k] != native[k]}
    is_record = lambda a: any(base <= a < base+len(buf) for base, buf in m.records)
    own_stores = lambda values: [(a, v) for a, v in bytes_of(values) if not is_record(a)]
    byte_stores_equal = own_stores(m.stores) == own_stores(stores)
    addresses = set(original) | set(a for a, v in bytes_of(stores)) | m.escritos
    memory_equal = all(m.u8(a) == uc.mem_read(a, 1)[0] for a in addresses)
    capture_equal = variant != 's1_actual' or (stores == stores_ref and all(
        native[k] == int(case['exit_registers'][k], 16) for k in REG7+('ESP',)))
    return dict(variant=variant, equal=not dif and byte_stores_equal and memory_equal and capture_equal,
                register_differences=dif, ordered_non_unit_byte_stores_equal=byte_stores_equal,
                memory_equal=memory_equal, original_capture_equal=capture_equal,
                native_stores=len(stores), python_stores=len(m.stores),
                first_store_difference=next(([i, a, b] for i, (a, b) in
                    enumerate(zip(own_stores(m.stores), own_stores(stores))) if a != b), None))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--saida', required=True)
    args = ap.parse_args()
    raw = CAPTURE.read_bytes()
    cap = json.loads(raw)
    if cap['original_sha256'] != ORIGINAL_SHA256 or len(cap['cases']) != 1:
        raise ValueError('Expected one real original S1 handler entry')
    case = cap['cases'][0]
    regs = {k: int(v, 16) for k, v in case['entry_registers'].items()}
    regs['ESP'] = int(case['esp'], 16)
    results = [compare(case, 's1_actual', regs)]
    for i in range(32):
        r = {k: v if k in ('EAX', 'EDX', 'ESP') else (v ^ ((i+1)*0x1234567)) & 0xffffffff
             for k, v in regs.items()}
        results.append(compare(case, f'preserved_registers_{i}', r))
    post = [[s[1], int(s[3], 16).to_bytes(s[2], 'little').hex()] for s in case['stores']]
    results.append(compare(case, 'original_post_state_duplicate', regs, post))
    # The actual native group19's battle field, deliberately declared -1.
    results.append(compare(case, 'declared_no_battle', regs, [['0x51ac4c', 'ffffffff']]))
    data = dict(schema='rising-lands/s1-detection-handler-differential/1', original_sha256=ORIGINAL_SHA256,
                capture_sha256=hashlib.sha256(raw).hexdigest(), comparisons=len(results),
                equal=sum(r['equal'] for r in results), cases=results,
                source_revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                source_sha256={n: hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest() for n in
                    ('deteccao_conflito_ia.py', 'validar_deteccao_conflito_ia.py')})
    path = ROOT/args.saida
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1, sort_keys=True)+'\n')
    print(json.dumps({k: data[k] for k in ('comparisons', 'equal')}))
    return 0 if data['equal'] == len(results) else 2


if __name__ == '__main__':
    raise SystemExit(main())
