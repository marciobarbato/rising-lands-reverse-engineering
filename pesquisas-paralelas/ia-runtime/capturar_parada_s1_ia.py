"""Observe an exact S1 owner handoff without replacing the original routine.

The snapshot and every resumed frame must reproduce the committed original
trajectory. Output is new evidence; existing files are never overwritten.
Run through heavy_lease.py. This is a bounded observation, not a chain proof.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente_ia_runtime import ROOT, ORIGINAL_SHA256
from capturar_mensagem_cidade_ia import Leituras


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rotina', required=True)
    ap.add_argument('--chamada', type=lambda v: int(v, 0), required=True)
    ap.add_argument('--de', type=int, required=True)
    ap.add_argument('--ate', type=int, required=True)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--unidade', type=int, help='select the actual zero-extended EAX unit at entry')
    ap.add_argument('--estado-local', help='save full original entry blocks under ignored .local only')
    ap.add_argument('--entrada-deteccao', action='store_true',
                    help='also capture complete live records needed by Combat\'s public message adapter')
    args = ap.parse_args()
    path = ROOT/args.saida
    if path.exists():
        raise SystemExit('Refusing to overwrite original evidence')
    if args.ate <= args.de:
        raise SystemExit('--ate must be after --de')
    state_path = ROOT/args.estado_local if args.estado_local else None
    if state_path and (not state_path.resolve().is_relative_to((ROOT/'.local').resolve()) or state_path.exists()):
        raise SystemExit('--estado-local must be a new ignored .local path')
    import bancada_s1 as bs
    from inventario_ia_runtime import OriginalImage
    instruction = OriginalImage().instruction(args.chamada)
    if instruction.mnemonic != 'call':
        raise ValueError('--chamada must identify an original CALL instruction')
    caller_return = args.chamada + instruction.size
    started = time.monotonic()
    s1 = bs.BancadaS1(args.de)
    reads = Leituras(s1.b.cpu)
    cases = []
    stores = []
    if args.entrada_deteccao:
        import unicorn
        from unicorn import x86_const as X
        def write(cpu, access, address, size, value, extra):
            if reads.ativo and not bs.PILHA_NATIVA <= address < bs.PILHA_NATIVA+bs.TAMANHO_PILHA:
                stores.append([hex(cpu.reg_read(X.UC_X86_REG_EIP)), hex(address), size,
                               hex(value & ((1 << (8*size))-1))])
        s1.b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, write)
        s1.b.cpu.ctl_flush_tb()

    def choose(name, regs, ret, observer):
        if (observer.quadro == args.ate and ret == caller_return
                and (args.unidade is None or regs['EAX'] == args.unidade)):
            stores.clear()
            reads.iniciar()
            return True
        return False

    def close(case, blocks):
        case['read_before_write'] = reads.finalizar()
        if state_path:
            import pickle
            state_path.parent.mkdir(parents=True, exist_ok=True)
            raw_state = pickle.dumps(blocks, protocol=4)
            with state_path.open('xb') as f:
                f.write(raw_state)
            case['local_entry_state'] = dict(path=str(state_path.relative_to(ROOT)),
                sha256=hashlib.sha256(raw_state).hexdigest(), blocks=len(blocks))
        if args.entrada_deteccao:
            def get(address, size):
                for base, raw in blocks.values():
                    if base <= address and address+size <= base+len(raw):
                        return raw[address-base:address-base+size]
                raise ValueError(f'Unmapped original entry span {address:#x}+{size}')
            u32 = lambda address: int.from_bytes(get(address, 4), 'little')
            unit, target = (int(case['entry_registers'][k], 16) for k in ('EAX', 'EDX'))
            pool = u32(0x4e19a0)
            record = pool+276*unit
            group = 0x51a9e0+32*u32(record+0x10c)
            behavior = get(group+27, 1)[0]
            pointer = 0x498e94+4*behavior
            spans = [(record, 276),
                     (0x49a0c8+276*(target&0x7fff), 276) if target&0x8000 else (pool+276*target, 276),
                     (group, 32), (pointer, 4), (u32(pointer), 20)]
            case['adapter_entry_spans'] = [[hex(a), get(a, n).hex()] for a, n in spans]
            case['stores'] = list(stores)
        cases.append(case)

    # This caller contract takes no pushed words (plain RET).
    obs = bs.Observacao(s1.b, {args.rotina: 0}, escolher=choose, ao_fechar=close,
                        retornos_extra={args.rotina: [caller_return]})
    while s1.k < args.ate:
        s1.avancar(obs)
    obs.remover()
    if obs.erros or not cases:
        raise RuntimeError(f'Exact routine/site not observed: {obs.erros}')
    reproduction = s1.reproducao()
    if not reproduction['code_unchanged']:
        raise RuntimeError('Original code changed')
    if 'provedores_entrada_ia' in sys.modules:
        raise RuntimeError('Consumer translation imported in original-only capture')
    data = dict(schema='rising-lands/ai-runtime-s1-next-stop-original/1',
                original_sha256=ORIGINAL_SHA256, routine=args.rotina,
                entry=hex(s1.b.sym[args.rotina]), call=hex(args.chamada),
                caller_return=hex(caller_return),
                translation_executed=False, s1=reproduction, cases=cases,
                source_revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                recorder_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                seconds=round(time.monotonic()-started, 3))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as f:
        f.write(json.dumps(data, indent=1, sort_keys=True)+'\n')
    print(json.dumps(data, indent=1, sort_keys=True))


if __name__ == '__main__':
    main()
