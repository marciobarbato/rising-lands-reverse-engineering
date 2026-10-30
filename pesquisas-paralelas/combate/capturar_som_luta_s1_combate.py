"""Passive original-first S1 fight sound requests and bounded parent cases.

Run via heavy_lease.py. Snapshots stay read-only in their supplied directory;
every resumed frame must match Missions' committed S1 trajectory. The inherited
scenario sound boundary remains installed. No Combat translation is imported.
"""
import argparse
from collections import Counter
import hashlib
import json
import lzma
from pathlib import Path
import struct
import subprocess

from extrair_evidencias import HASH, ler_imagem, Cs, CS_ARCH_X86, CS_MODE_32
from rastrear_ataque_vivo import simbolos, chamadores
from ambiente_combate_raid import ROOT

HERE = Path(__file__).resolve().parent
PARENTS = {'CalculAttaqueEngin': 0, 'ProjectileCalcul': 0,
           'EnginInfligeDegat': 0, 'InfligeDegat': 4,
           'SetDyingEngin': 0, 'BatimentInfligeDegat': 0}


def inventory():
    image = ler_imagem()
    name, limits = simbolos()
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    result = []
    for target, routine in ((0x48aa79, 'PlaySnd_PostSound'), (0x48aac0, 'PlaySnd_StopSound')):
        for address in chamadores(image, target):
            owner = name(address)
            if any(n in owner for n in ('Attaque', 'Projectile', 'Degat', 'Dying', 'Retire', 'NextEtape')):
                start = max(a for a in limits if a <= address)
                end = min(a for a in limits if a > address)
                # Decode from the symbol start, avoiding arbitrary instruction alignment.
                instructions = list(cs.disasm(bytes(image[start-0x400000:end-0x400000]), start))
                context = [i for i in instructions if address-64 <= i.address <= address]
                result.append(dict(call=hex(address), return_address=hex(address+5),
                    routine=routine, owner=owner,
                    context=[f'{i.address:#x} {i.mnemonic} {i.op_str}' for i in context],
                    context_sha256=hashlib.sha256(bytes(image[address-64-0x400000:address+5-0x400000])).hexdigest()))
    # Projectile code has no direct request: damage/alert/death are its emitters.
    direct = {hex(a) for t in (0x48aa79, 0x48aac0) for a in chamadores(image, t)
              if 0x46dfa0 <= a < 0x46fc8b}
    assert not direct, direct
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--snapshot-root', type=Path, required=True)
    ap.add_argument('--inicio', type=Path, required=True)
    ap.add_argument('--de', type=int, default=11750)
    ap.add_argument('--ate', type=int, default=12000)
    ap.add_argument('--saida', type=Path, default=ROOT/'.local/som-luta-s1-raw-original-v1.json.xz')
    a = ap.parse_args()
    if a.saida.exists(): raise SystemExit('Refusing to overwrite original evidence')
    if not 1 <= a.ate-a.de <= 250: raise SystemExit('Require 1..250 frames')
    import bancada_s1 as bs
    from delta_estado_missao import estado_completo
    from emulador import x86, unicorn
    bs.INICIO, bs.INSTANTANEOS = a.inicio, a.snapshot_root
    s1 = bs.BancadaS1(a.de)
    b = s1.b
    requests, cases, starts, seen = [], [], [], set()
    all_sites = {addr: name for target, name in ((0x48aa79, 'PlaySnd_PostSound'), (0x48aac0, 'PlaySnd_StopSound'))
                 for addr in chamadores(ler_imagem(), target)}
    frame = a.de

    def on_call(cpu, address, size, _):
        name = all_sites[address]
        regs = {r: cpu.reg_read(getattr(x86, 'UC_X86_REG_'+r)) for r in bs.REGISTROS+('ESP',)}
        words = [struct.unpack('<I', cpu.mem_read(regs['ESP'], 4))[0]] if name == 'PlaySnd_PostSound' else []
        requests.append(dict(frame=frame, phase=b.fase, routine=name, call=hex(address),
                             return_address=hex(address+5), registers={k:hex(v) for k,v in regs.items()},
                             stack_words=words))

    def choose(name, regs, ret, obs):
        starts.append(len(requests))
        return True

    def close(case, blocks):
        events = requests[starts.pop():]
        if not events: return
        key = (case['routine'], int(case['entry_registers']['EAX'],16)&65535,
               tuple(e['call'] for e in events))
        if key in seen or len(cases) >= 40: return
        seen.add(key)
        case['sound_requests'] = events
        case['full_state_before'] = estado_completo({n:v for n,v in blocks.items() if n!='native_stack'})
        cases.append(case)

    hooks = [b.cpu.hook_add(unicorn.UC_HOOK_CODE,on_call,begin=addr,end=addr) for addr in all_sites]
    obs = bs.Observacao(b, PARENTS, escolher=choose, ao_fechar=close)
    try:
        while s1.k < a.ate:
            frame = s1.k+1
            s1.avancar(obs)
            if frame%25 == 0: print(json.dumps(dict(frame=frame,requests=len(requests),cases=len(cases))),flush=True)
    finally:
        obs.remover()
        for h in hooks: b.cpu.hook_del(h)
    if obs.erros or starts: raise RuntimeError(str(obs.erros))
    target = [r for r in requests if r['frame']==11753 and r['call']=='0x4525a1']
    if a.de==11750 and (len(target)!=1 or target[0]['stack_words']!=[90]):
        raise RuntimeError('Exact frame-11753 target not observed')
    if any(n in __import__('sys').modules for n in ('combate_raid_vivo','luta_fatal_viva_combate')):
        raise RuntimeError('Combat translation imported into original-only capture')
    data = dict(schema='rising-lands/combat-s1-sound-original/1', original_sha256=HASH,
                translation_executed=False, sound_domain='inherited S1 scenario boundary',
                s1=s1.reproducao(), inventory=inventory(), requests=requests, cases=cases,
                counts=dict(Counter(r['call'] for r in requests)),
                source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                recorder_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    a.saida.parent.mkdir(parents=True,exist_ok=True)
    with lzma.open(a.saida,'xt',preset=6) as f: json.dump(data,f,sort_keys=True)
    print(json.dumps(dict(s1=data['s1'],counts=data['counts'],cases=len(cases))),flush=True)


if __name__=='__main__': main()
