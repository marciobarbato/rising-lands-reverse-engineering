"""Fresh bounded original leaf comparisons of the live S1 Economy routes.

Consumes committed original-first owner fixtures, never pins foreign source
hashes. All native game callees execute; the technology getters use live
translated owners in Python, not recorded callback returns. Run under lease.
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente_ia_runtime import ROOT, ORIGINAL_SHA256
from emulador import BancadaX86, PILHA, RETORNO, mapear_paginas
from capturar_mensagem_cidade_ia import MemoriaCapturada
from provedores_entrada_ia import DonosM3, _modulo_economia, REG7

FILES = ('captura-sac-v2', 'captura-tuyau', 'captura-tecnologia')
_SYMBOLS = None


def call_site(label):
    global _SYMBOLS
    if _SYMBOLS is None:
        from inventario_ia_runtime import OriginalImage
        _SYMBOLS = {n: a for a, names in OriginalImage().names.items() for n in names}
    name, offset = label.rsplit('+', 1)
    return _SYMBOLS[name]+int(offset, 16)-5


def same_calls(actual, expected):
    return len(actual) == len(expected) and all(a[0:2] == e[0:2] and
        all(a[2][k] == v for k, v in e[2].items()) for a, e in zip(actual, expected))


class Memory(MemoriaCapturada):
    def __init__(self, reads):
        super().__init__(reads)
        self.stores = []

    def _acesso(self, a, n, v):
        if v is not None:
            self.stores.append((a, n, v & ((1 << (n*8))-1)))
        return super()._acesso(a, n, v)


def compare(case, native=False):
    regs = {k: int(v, 16) for k, v in case['entry_registers'].items()}
    regs['ESP'] = int(case['esp'], 16)
    m = Memory(case['read_before_write'])
    d = DonosM3(m, som=None)
    calls = []
    getter = d.tecnologia_s1.externo

    def observe(name, call, r):
        calls.append((name, call, {k: r[k] for k in REG7}))
        return getter(name, call, r)
    d.tecnologia_s1.externo = observe
    out = d.externo(case['routine'], int(case.get('caller_return', '0'), 16)-5, regs)
    expected = {k: int(case['exit_registers'][k], 16) for k in REG7}
    stores = [(int(s[2], 16), s[3], int(s[4], 16)) for s in case['stores']]
    foreign = [(c[1], call_site(c[3]), {k: int(v, 16) for k, v in c[2].items()})
               for c in case['calls'] if c[1] in ('MissionGetNum', 'PlayerGetType')]
    dif = {k: [hex(out[k]), hex(v)] for k, v in expected.items() if out[k] != v}
    result = dict(routine=case['routine'], frame=case['frame'], registers_equal=not dif,
                  register_differences=dif, stores_equal=m.stores == stores,
                  live_foreign_calls_equal=same_calls(calls, foreign), foreign_calls=len(calls))
    if case['routine'] == 'SacGetCapacite':
        result['scalar_projection_equal'] = d.capacidade_saco(regs['EAX']) == expected['EAX']
    if native:
        import unicorn
        from unicorn import x86_const as X
        b = BancadaX86()
        uc = b.cpu
        regions = list(uc.mem_regions())
        addresses = {int(a, 16)+i for a, h in case['read_before_write'] for i in range(len(h)//2)}
        addresses.update(a+i for a, n, v in stores for i in range(n))
        pages = {a & ~4095 for a in addresses if not any(lo <= a <= hi for lo, hi, _ in regions)}
        mapear_paginas(uc, pages)
        for a, h in case['read_before_write']:
            uc.mem_write(int(a, 16), bytes.fromhex(h))
        native_stores, native_calls = [], []

        def write(cpu, access, a, n, v, extra):
            if not PILHA <= a < PILHA+65536:
                native_stores.append((a, n, v & ((1 << (n*8))-1)))

        def call(cpu, a, n, name):
            esp = cpu.reg_read(X.UC_X86_REG_ESP)
            site = int.from_bytes(cpu.mem_read(esp, 4), 'little')-5
            native_calls.append((name, site, {k: cpu.reg_read(getattr(X, 'UC_X86_REG_'+k)) for k in REG7}))
        uc.hook_add(unicorn.UC_HOOK_MEM_WRITE, write)
        for name, entry in (('MissionGetNum', 0x46c11a), ('PlayerGetType', 0x46d817)):
            uc.hook_add(unicorn.UC_HOOK_CODE, call, user_data=name, begin=entry, end=entry)
        uc.ctl_flush_tb()
        for k, v in regs.items():
            uc.reg_write(getattr(X, 'UC_X86_REG_'+k), v)
        uc.reg_write(X.UC_X86_REG_FPCW, 0x127f)
        uc.reg_write(X.UC_X86_REG_FPSW, 0)
        uc.reg_write(X.UC_X86_REG_FPTAG, 0xffff)
        uc.mem_write(regs['ESP'], RETORNO.to_bytes(4, 'little'))
        modules = ('lacunas_economia_s1', 'tuyau_economia_s1', 'tecnologia_economia_s1')
        entries = {k: v for module in modules for k, v in _modulo_economia(module).ROTINAS.items()}
        nout = b.retomar(entries[case['routine']], [(0x401000, 0x494000)],
                        parada=RETORNO, limite_instrucoes=1000000)
        if nout['EIP'] != RETORNO:
            raise RuntimeError('Native leaf did not return')
        result.update(native_registers_equal=all(nout[k] == v for k, v in expected.items()),
                      native_esp_equal=nout['ESP'] == int(case['exit_registers']['ESP'], 16),
                      native_stores_equal=native_stores == stores,
                      native_foreign_calls_equal=same_calls(native_calls, foreign),
                      native_all_seven_callback_inputs_equal=native_calls == calls)
        if '_x87_push' in out:
            top = (uc.reg_read(X.UC_X86_REG_FPSW) >> 11) & 7
            result['native_x87_equal'] = top == 7 and tuple(uc.reg_read(getattr(X, f'UC_X86_REG_FP{top}'))) == out['_x87_push']
    result['equal'] = all(v for k, v in result.items() if k.endswith('_equal'))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--native', action='store_true')
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    start = time.monotonic()
    results, sources = [], {}
    for name in FILES:
        path = ROOT/'pesquisas-paralelas/economia/evidencias/lacunas-s1'/f'{name}.json.xz'
        raw = path.read_bytes()
        cap = json.loads(lzma.decompress(raw))
        if cap['original_sha256'] != ORIGINAL_SHA256:
            raise RuntimeError('Wrong original identity')
        sources[str(path.relative_to(ROOT))] = hashlib.sha256(raw).hexdigest()
        for case in cap['cases']:
            results.append(compare(case, a.native))
        print(name, len(cap['cases']), 'done', flush=True)
    data = dict(schema='rising-lands/ai-runtime-s1-economy-routes/1', original_sha256=ORIGINAL_SHA256,
                source_revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                native=a.native, fixtures=sources, comparisons=len(results),
                equal=sum(r['equal'] for r in results), cases=results,
                source_sha256={n: hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest()
                               for n in ('validar_donos_economia_s1_ia.py', 'provedores_entrada_ia.py')},
                seconds=round(time.monotonic()-start, 3))
    path = ROOT/a.saida
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1, sort_keys=True)+'\n')
    print(json.dumps({k: data[k] for k in ('comparisons', 'equal', 'seconds')}))
    return 0 if data['equal'] == len(results) else 2


if __name__ == '__main__':
    raise SystemExit(main())
