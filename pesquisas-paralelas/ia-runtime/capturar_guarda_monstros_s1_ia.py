"""One native S1 display entry documenting Graphics' multi-monster guard.

Snapshot 11500 is the nearest available original input after the first guard
at 10801. This records 11501, not an invented entry register file for 10801.
Run through heavy_lease.py. No translation, binding or skipped game body.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente_ia_runtime import ROOT, ORIGINAL_SHA256


def main():
    import bancada_s1 as bs
    import unicorn
    from unicorn import x86_const as X
    path = ROOT/'pesquisas-paralelas/ia-runtime/evidencias/s1-guarda-monstros-original.json'
    if path.exists():
        raise SystemExit('Refusing to replace original evidence')
    s1 = bs.BancadaS1(11500)
    entries = []

    def entry(cpu, a, n, extra):
        esp = cpu.reg_read(X.UC_X86_REG_ESP)
        ret = int.from_bytes(cpu.mem_read(esp, 4), 'little')
        if ret == 0x475068:
            entries.append(dict(frame=11501, phase='between_frames11501', entry=hex(a),
                                call='0x475063', registers={k: hex(cpu.reg_read(getattr(X, 'UC_X86_REG_'+k)))
                                                           for k in bs.REGISTROS+('ESP',)},
                                monster_count_u8=int.from_bytes(cpu.mem_read(0x50b178, 1), 'little'),
                                monster_count_u32=int.from_bytes(cpu.mem_read(0x50b178, 4), 'little'),
                                mode=int.from_bytes(cpu.mem_read(0x4e2f78, 1), 'little'),
                                view=[int.from_bytes(cpu.mem_read(g, 2), 'little') for g in (0x508720, 0x508722)]))
    hook = s1.b.cpu.hook_add(unicorn.UC_HOOK_CODE, entry, begin=0x417698, end=0x417698)
    s1.b.cpu.ctl_flush_tb()
    s1.avancar()
    s1.b.cpu.hook_del(hook)
    if len(entries) != 1 or not s1.reproducao()['code_unchanged']:
        raise RuntimeError('Exact native display entry/code did not reproduce')
    data = dict(original_sha256=ORIGINAL_SHA256, schema='rising-lands/s1-graphics-guard-entry/1',
                source_revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                recorder_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                entries=entries, s1=s1.reproducao(), translation_executed=False)
    with path.open('x') as f:
        f.write(json.dumps(data, indent=1, sort_keys=True)+'\n')
    print(json.dumps(data, indent=1))


if __name__ == '__main__':
    main()
