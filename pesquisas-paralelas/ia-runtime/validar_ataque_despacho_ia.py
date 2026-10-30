"""Compare the real S1 attack-transition parent, original x86 versus providers.

Full native entry memory is an ignored, hash-bound input. No game callee is
patched. Compare all final game blocks, the original native return/changes and
the ordered dispatcher handoffs. The semantic parent API discards registers.
Run via heavy_lease.py after the original capture has been committed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import pickle
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente_ia_runtime import ROOT, ORIGINAL_SHA256
from emulador import BancadaX86, PILHA, RETORNO, mapear_paginas
from composicao_quadro1_ia import mundo
from composicao_encadeada_ia import (MemoriaMapaRapida, ContextoEncadeado, Registro,
    JanelasDeclaradas, Travessias, provedores)
from inventario_ia_runtime import OriginalImage

CAPTURE = ROOT/'pesquisas-paralelas/ia-runtime/evidencias/s1-ataque-proxima-etapa-original.json'


def main():
    import unicorn
    from unicorn import x86_const as X
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--captura', default=str(CAPTURE.relative_to(ROOT)))
    args = ap.parse_args()
    raw = (ROOT/args.captura).read_bytes()
    cap = json.loads(raw)
    if cap['original_sha256'] != ORIGINAL_SHA256 or not cap['s1']['code_unchanged']:
        raise ValueError('Expected an unchanged intact original S1 capture')
    case, = cap['cases']
    phase = case['phase']
    path = (ROOT/case['local_entry_state']['path']).resolve()
    if not path.is_relative_to((ROOT/'.local').resolve()):
        raise ValueError('Full original entry inputs must remain ignored')
    state_raw = path.read_bytes()
    if hashlib.sha256(state_raw).hexdigest() != case['local_entry_state']['sha256']:
        raise ValueError('Original entry state hash differs')
    blocks = pickle.loads(state_raw)
    regs = {k: int(v, 16) for k, v in case['entry_registers'].items()}
    regs['ESP'] = int(case['esp'], 16)
    mapa, owner = mundo(blocks)
    m = MemoriaMapaRapida(mapa)
    ctx = ContextoEncadeado(OriginalImage(), 'exibicao', modo='prova')
    p, _ = provedores(mapa, owner, m, ctx, Registro(phase), JanelasDeclaradas(),
                       Travessias({}, {}, lambda m: {}), phase, regs)
    events = []
    for name in ('iagUnitSendMessage', 'EnginNextEtape:state1'):
        if name in p:
            body = p[name]
            def traced(sitio, _body=body, _name=name, **kw):
                events.append(dict(routine=_name, site=hex(sitio), arguments=kw))
                return _body(sitio=sitio, **kw)
            p[name] = traced
    p['EnginNextEtape'](sitio=0x456ead, unidade=regs['EAX'])
    python = mapa.serializar()
    b = BancadaX86()
    uc = b.cpu
    regions = list(uc.mem_regions())
    pages = {a for base, data in blocks.values() for a in range(base & ~4095, (base+len(data)+4095)&~4095, 4096)
             if not any(lo <= a <= hi for lo, hi, _ in regions)}
    mapear_paginas(uc, pages)
    for base, data in blocks.values():
        uc.mem_write(base, data)
    for k, v in regs.items():
        uc.reg_write(getattr(X, 'UC_X86_REG_'+k), v)
    native_events, native_registers = [], []
    def observe(cpu, address, size, extra):
        r = {k: cpu.reg_read(getattr(X, 'UC_X86_REG_'+k)) for k in regs}
        native_registers.append(dict(address=hex(address), registers={k: hex(v) for k, v in r.items()}))
        if address == 0x4829c8:
            ret = int.from_bytes(cpu.mem_read(r['ESP'], 4), 'little')
            native_events.append(dict(routine='iagUnitSendMessage', site=hex(ret-5),
                arguments=dict(unidade=r['EAX'] & 65535, mensagem=r['EDX'] & 255, alvo=r['EBX'])))
        elif address == 0x456886:
            native_events.append(dict(routine='EnginNextEtape:state1', site=hex(address),
                                      arguments=dict(unidade=r['EDI'] & 65535)))
    for address in (0x4829c8, 0x456886, 0x454587):
        uc.hook_add(unicorn.UC_HOOK_CODE, observe, begin=address, end=address)
    uc.ctl_flush_tb()
    # Preserve the actual original caller/stack, stop at its observed return.
    output = b.retomar(0x45442c, [(0x401000, 0x494000)], parada=0x456eb2, limite_instrucoes=1000000)
    changes = []
    differences = []
    for name, (base, data) in blocks.items():
        if name == 'native_stack':
            continue
        native = bytes(uc.mem_read(base, len(data)))
        if native != data:
            changes += [[hex(base+i), old, new] for i, (old, new) in enumerate(zip(data, native)) if old != new]
        pybase, pydata = python[name]
        if pybase != base or pydata != native:
            differences.append(dict(block=name, first_bytes=[hex(base+i) for i, (a, b) in
                               enumerate(zip(pydata, native)) if a != b][:12]))
    reproduced = sorted(changes, key=lambda x: int(x[0], 16)) == case['changed_bytes'] and all(
        output[k] == int(v, 16) for k, v in case['exit_registers'].items())
    handoffs = events == native_events and bool(events)
    passages_equal = all(passage in native_registers for passage in case.get('passages', []))
    result = dict(equal=not differences and reproduced and handoffs and passages_equal, memory_differences=differences,
                  frame=case['frame'], unit=regs['EAX'], passages_equal=passages_equal,
                  native_capture_reproduced=reproduced, handoffs_equal=handoffs, handoffs=events,
                  native_handoff_registers=native_registers,
                  original_changed_bytes=len(changes), game_blocks_compared=len(blocks)-1)
    data = dict(schema='rising-lands/s1-attack-dispatch-differential/1', original_sha256=ORIGINAL_SHA256,
        capture_sha256=hashlib.sha256(raw).hexdigest(), comparisons=1, equal=int(result['equal']), cases=[result],
        capture=args.captura,
        source_revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        source_sha256={n: hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest() for n in
            ('ataque_despacho_ia.py', 'proxima_etapa_quadro.py', 'composicao_encadeada_ia.py',
             'validar_ataque_despacho_ia.py')})
    path = ROOT/args.saida
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1, sort_keys=True)+'\n')
    print(json.dumps(data, indent=1, sort_keys=True))
    return 0 if result['equal'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
