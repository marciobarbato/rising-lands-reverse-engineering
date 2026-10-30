"""Original-first MineGetCapacite ABI at S1's first missing work-cycle route.

Capture before binding; comparison must reproduce committed native evidence.
Run through heavy_lease.py. No native callee is replaced or skipped.
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
from emulador import BancadaX86, RETORNO
from capturar_mensagem_cidade_ia import Leituras

ENTRY, CALL, MINES = 0x475541, 0x44ca17, 0x509954
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
CAPTURE = ROOT / 'pesquisas-paralelas/ia-runtime/evidencias/consulta-mina-original.json.xz'


def capture():
    import bancada_s1 as bs
    s1 = bs.BancadaS1(3250)
    reads = Leituras(s1.b.cpu)
    cases, seeds = [], []

    def choose(name, regs, ret, observer):
        if ret == CALL + 5:
            reads.iniciar()
            return True
        return False

    def close(case, blocks):
        case['read_before_write'] = reads.finalizar()
        case['mines'] = bytes(s1.b.cpu.mem_read(MINES, 80)).hex()
        if reads.escritos or case['changed_bytes'] or case['boundaries']:
            raise RuntimeError('MineGetCapacite must return without stores/boundaries')
        cases.append(case)
        seeds.append(case)

    obs = bs.Observacao(s1.b, {'MineGetCapacite': 0}, escolher=choose, ao_fechar=close)
    while s1.k < 3277:
        s1.avancar(obs)
    obs.remover()
    if obs.erros or len(seeds) != 1 or seeds[0]['frame'] != 3277:
        raise RuntimeError(f'Expected one real frame-3277 call: {obs.erros}, {len(seeds)}')
    seed = seeds[0]
    b = BancadaX86()
    uc = b.cpu
    reads_v = Leituras(uc)
    from unicorn import x86_const as X
    regs_seed = {k: int(v, 16) for k, v in seed['entry_registers'].items()}
    for index in range(20):
        for reserve in (0, 1, 0x7fff, 0x8000, 0xffff):
            mines = bytearray.fromhex(seed['mines'])
            mines[4*index+2:4*index+4] = reserve.to_bytes(2, 'little')
            uc.mem_write(MINES, bytes(mines))
            regs = {k: (v ^ (0x98760000 + i*0x110000)) & 0xffffffff
                    for i, (k, v) in enumerate(regs_seed.items())}
            regs['EAX'] = (regs['EAX'] & 0xffff0000) | index
            reads_v.iniciar()
            out = b.executar(ENTRY, [(0x401000, 0x494000)], regs,
                             parada=RETORNO, limite_instrucoes=100)
            rbw = reads_v.finalizar()
            if out['EIP'] != RETORNO or reads_v.escritos:
                raise RuntimeError('Declared mine query did not return without stores')
            cases.append(dict(kind='declared_index_reserve', index=index, reserve=reserve,
                              entry_registers={k: hex(v) for k, v in regs.items()},
                              exit_registers={k: hex(out[k]) for k in REG7},
                              read_before_write=rbw, mines=bytes(mines).hex(), changed_bytes=[]))
    reproduction = s1.reproducao()
    if not reproduction['code_unchanged']:
        raise RuntimeError('Original code changed')
    return dict(original_sha256=ORIGINAL_SHA256, entry=hex(ENTRY), call=hex(CALL),
                s1=reproduction, cases=cases)


def compare(case):
    from memoria_quadro_core import MemoriaQuadro
    from provedores_entrada_ia import DonosM3
    mines = bytearray.fromhex(case['mines'])
    m = MemoriaQuadro([(MINES, mines)])
    d = DonosM3(m, som=None)
    regs = {k: int(v, 16) for k, v in case['entry_registers'].items()}
    out = d.externo('MineGetCapacite', CALL, regs)
    dif = {k: [hex(out[k]), case['exit_registers'][k]] for k in REG7
           if out[k] != int(case['exit_registers'][k], 16)}
    partial = d.externo('MineGetCapacite', CALL, dict(EAX=regs['EAX'], _incertos={'EAX': 0xffff0000}))
    partial_ok = (partial['EAX'] == int(case['exit_registers']['EAX'], 16)
                  and partial.get('_incertos') == {k: 0xffffffff for k in REG7 if k != 'EAX'})
    unchanged = mines.hex() == case['mines']
    return dict(equal=not dif and partial_ok and unchanged, register_differences=dif,
                partial_registers_equal=partial_ok, mines_unchanged=unchanged)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--comparar', action='store_true')
    ap.add_argument('--saida')
    a = ap.parse_args()
    if not a.comparar and CAPTURE.exists():
        raise SystemExit('Refusing to replace original evidence')
    reference = None
    if a.comparar:
        raw = CAPTURE.read_bytes()
        committed = subprocess.check_output(['git', 'show', f'HEAD:{CAPTURE.relative_to(ROOT)}'], cwd=ROOT)
        if committed != raw:
            raise SystemExit('Commit original evidence before translation/comparison')
        reference = json.loads(lzma.decompress(raw))
    t0 = time.monotonic()
    data = capture()
    data.update(source_revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                seconds=round(time.monotonic()-t0, 3))
    if not a.comparar:
        if 'provedores_entrada_ia' in sys.modules:
            raise RuntimeError('Consumer translation imported during original-only capture')
        data.update(schema='rising-lands/ai-runtime-mine-query-original/1', translation_executed=False)
        CAPTURE.write_bytes(lzma.compress((json.dumps(data, sort_keys=True)+'\n').encode()))
        print(json.dumps(dict(cases=len(data['cases']), s1=data['s1'])))
        return 0
    if not a.saida:
        raise SystemExit('--comparar requires --saida')
    if data['s1'] != reference['s1'] or data['cases'] != reference['cases']:
        raise RuntimeError('Native evidence did not reproduce exactly')
    results = [dict(kind=c['kind'], index=c.get('index'), reserve=c.get('reserve'),
                    frame=c.get('frame'), **compare(c)) for c in data.pop('cases')]
    sources = ('capturar_consulta_mina_ia.py', 'provedores_entrada_ia.py')
    data.update(schema='rising-lands/ai-runtime-mine-query-differential/1', native_equals_capture=True,
                capture_sha256=hashlib.sha256(raw).hexdigest(), comparisons=len(results),
                equal=sum(c['equal'] for c in results), cases=results,
                source_sha256={p: hashlib.sha256((Path(__file__).parent/p).read_bytes()).hexdigest() for p in sources})
    path = ROOT/a.saida
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1, sort_keys=True)+'\n')
    print(json.dumps(dict(comparisons=len(results), equal=data['equal'], s1=data['s1'])))
    return 0 if data['equal'] == len(results) else 2


if __name__ == '__main__':
    raise SystemExit(main())
