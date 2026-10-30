"""Original-first real-contact matrix for fight composition and corpse removal."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import signal
import struct

from bancada_luta_fatal_combate import BancadaLutaFatal, estado_contato, json_bytes

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / 'evidencias/captura-folhas-luta-fatal-original-v1.json'


def main():
    if OUTPUT.exists():
        raise SystemExit(f'Refusing to overwrite {OUTPUT}')
    def budget(*_):
        raise TimeoutError('1100-second whole native job budget')
    signal.signal(signal.SIGALRM, budget); signal.alarm(1100)
    state, pin = estado_contato(); b = BancadaLutaFatal(state); records = []
    def byte(a, v): return [hex(a), bytes([v & 255]).hex()]
    def word(a, v): return [hex(a), struct.pack('<H', v & 65535).hex()]
    def dword(a, v): return [hex(a), struct.pack('<I', v & 0xffffffff).hex()]
    def run(label, name, regs, writes=(), *, parent='contact', restore=True, words=(), stops=None):
        if restore: b.restore(state)
        for a, data in writes: b.cpu.mem_write(int(a, 16), bytes.fromhex(data))
        c, _, _ = b.call(name, regs, words=words, stops=stops)
        c.update(case=label, state_ref=parent, declared_writes=list(writes))
        records.append(c)
        if c['fault'] or c['limit']: print(json.dumps(dict(case=label, fault=c['fault'], limit=c['limit'])), flush=True)
        return c
    for u in (0, 13, 16):
        for message in (0x48, 0x44, 0x4a):
            run(f'message-u{u}-{message:x}', 'iagUnitSendMessage', dict(EAX=0xabcd0000|u, EDX=0x12340000|message, EBX=0))
    for target in (0, 1, 13, 0xffff):
        run(f'message48-raider-target-{target}', 'iagUnitSendMessage', dict(EAX=16, EDX=0x48, EBX=target))
    for a, d in ((0,0), (0,1), (1,0), (0,4), (4,0), (4,4), (200,0)):
        run(f'break-alliance-{a}-{d}', 'PlayerResetAllie', dict(EAX=0xabcd0000|a, EDX=0x12340000|d))
        run(f'attacked-{a}-{d}', 'PlayerAAttaqueSet', dict(EAX=0xabcd0000|a, EDX=0x12340000|d))
    for action in (0,1,6,8,10):
        run(f'sympathy-actual-{action}', 'MAJSympathie', dict(EAX=0, EDX=1, EBX=action))
        base=0x497288+16*action
        for mode, change in ((0,100), (0,-100), (1,100), (1,-100)):
            run(f'sympathy-trigger-{action}-{mode}-{change}', 'MAJSympathie', dict(EAX=0, EDX=1, EBX=action),
                [byte(base+4, mode), dword(base, change), dword(base+8, 0), dword(base+12, 1)])
    for a,d in ((0,0),(0,4),(4,0),(200,0)):
        run(f'sympathy-guard-{a}-{d}', 'MAJSympathie', dict(EAX=a, EDX=d, EBX=10))
    for code in (0,99,100,406,502,999,1000,65535):
        run(f'message-box-{code}', 'MessageBoxSet', dict(EAX=0xabcd000a, EDX=code))
    run('message-box-full', 'MessageBoxSet', dict(EAX=10, EDX=406), [byte(0x507d58,1)])
    run('message-box-wrap-full', 'MessageBoxSet', dict(EAX=10, EDX=406), [word(0x507d56,255),word(0x507d54,0),byte(0x507d58,0)])
    for u in (0,16):
        for level in range(6):
            run(f'level-u{u}-{level}', 'EnginSetLevelExperience', dict(EAX=u, EDX=level))
    for u in (0,13,16):
        run(f'dying-u{u}', 'SetDyingEngin', dict(EAX=0xabcd0000|u), [word(b.record(u)+0x9a,0)])
    # Sequential corpse animation is the actual output of original SetDyingEngin,
    # not a constructed state-4 fixture. Three full 330-step original windows.
    for u in (0,13,16):
        previous=f'corpse-u{u}-dying'
        c=run(previous, 'SetDyingEngin', dict(EAX=u), [word(b.record(u)+0x9a,0)])
        if not c['reached_return']: continue
        for tick in range(1,332):
            label=f'corpse-u{u}-t{tick}'
            c=run(label, 'EnginNextEtape', dict(EAX=u), [dword(0x508f7c,10683+tick)], parent=previous, restore=False)
            previous=label
            if not c['reached_return'] or b.read(b.record(u)+2,1)==b'\0': break
        run(f'corpse-u{u}-recount', 'CalculEnginNextEtape', {}, parent=previous, restore=False)
    # Full native damage, including imports and lethal variants. No game callback is skipped.
    for victim, mode, source in ((0,1,16), (16,1,0), (13,1,16)):
        for life in (100,1,0):
            run(f'unit-damage-{victim}-{source}-life{life}', 'EnginInfligeDegat', dict(EAX=victim,EDX=mode,EBX=source,ECX=0),
                [word(b.record(victim)+0x9a,life)])
    # Exact first impact input and a declared one-life victim variation.
    for life in (100,1,0):
        run(f'impact-contact-life{life}', 'InfligeDegat', dict(EAX=0x2d05,EDX=1,EBX=16,ECX=0),
            [word(b.record(0)+0x9a,life)], words=(0,))
    signal.alarm(0)
    output=dict(schema='rising-lands/combat-fatal-leaves-original/1', translation_executed=False,
                original_sha256='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
                provenance=pin, external_binding='Missions PerfilWindows over original media; Core stdcall transport; no game substitution',
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                bench_sha256=hashlib.sha256((HERE/'bancada_luta_fatal_combate.py').read_bytes()).hexdigest(), cases=records)
    OUTPUT.write_text(json.dumps(output,indent=1,default=json_bytes)+'\n')
    counts=Counter(c['routine'] for c in records)
    print(json.dumps(dict(cases=dict(counts), returns=sum(c['reached_return'] for c in records),
                         faults=sum(bool(c['fault']) for c in records),limits=sum(c['limit'] for c in records),
                         outside=sum(bool(c['writes_outside_checkpoint']) for c in records))),flush=True)


if __name__=='__main__': main()
