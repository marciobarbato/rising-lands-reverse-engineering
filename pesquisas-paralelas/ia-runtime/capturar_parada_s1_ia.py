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
    args = ap.parse_args()
    path = ROOT/args.saida
    if path.exists():
        raise SystemExit('Refusing to overwrite original evidence')
    if args.ate <= args.de:
        raise SystemExit('--ate must be after --de')
    import bancada_s1 as bs
    started = time.monotonic()
    s1 = bs.BancadaS1(args.de)
    reads = Leituras(s1.b.cpu)
    cases = []

    def choose(name, regs, ret, observer):
        if observer.quadro == args.ate and ret == args.chamada+5:
            reads.iniciar()
            return True
        return False

    def close(case, blocks):
        case['read_before_write'] = reads.finalizar()
        cases.append(case)

    # This caller contract takes no pushed words (plain RET).
    obs = bs.Observacao(s1.b, {args.rotina: 0}, escolher=choose, ao_fechar=close)
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
