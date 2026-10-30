"""Original-first SortieTroupe owner calls: Economy fixtures, verified S1, declared leaves.

Run through heavy_lease.py. --capturar imports no new adapter and refuses replacement.
Comparison requires a committed capture and reexecutes the same unpatched native calls.
"""
import argparse
from collections import Counter
import hashlib
import json
import lzma
from pathlib import Path
import struct
import subprocess
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / 'ferramentas'))
import bancada_s1 as bs

ROTINAS = {'EnginSetType': (0x457b87, 0x420f69), 'EnginAddVie': (0x457122, 0x420f75),
           'EnginResetFatigue': (0x4530fd, 0x420f7c), 'EnginSetExperimente': (0x44fe42, 0x420f85),
           'SetSortEngin': (0x445fbc, 0x420f8c)}
CAPTURA = RAIZ / 'evidencias/recrutamento-core/original.json.xz'
RELATORIO = RAIZ / 'relatorios/recrutamento-core-emulada.json'
ECONOMY = 'pesquisas-paralelas/economia/evidencias/caverna-recrutamento/captura-caverna-recrutamento-exibicao.json.xz'
FONTES = tuple('ferramentas/' + n + '.py' for n in (
    'recrutamento_core', 'validar_recrutamento_core', 'bancada_s1', 'incursao_core',
    'chamadas_quadro_core', 'conversao_unidades', 'unidades', 'experiencia_unidades',
    'mundo_vivo', 'visao_grupos', 'visao_movimento', 'memoria_quadro_core', 'insercao_unidades'))
REG7 = bs.REGISTROS


def comparar(c, blocos):
    from validar_fadiga_vegetacao import memoria_caso, mudancas
    from recrutamento_core import RecrutamentoCore, provedor_recrutamento, bonus_recrutamento
    m, copias = memoria_caso(blocos)
    r = {k: int(v, 16) for k, v in c['entry_registers'].items()}
    r['ESP'] = int(c['esp'], 16)
    try:
        t = RecrutamentoCore(m, bonus=bonus_recrutamento(m))
        out = t.chamar(c['routine'], r)
        dif = {k: [hex(out[k]), v] for k, v in c['exit_registers'].items() if out[k] != int(v, 16)}
        changed = mudancas(blocos, copias)
        # Recreate entry memory for the partial-register consumer protocol.
        p, pc = memoria_caso(blocos)
        provider = provedor_recrutamento(RecrutamentoCore(p, bonus=bonus_recrutamento(p)))
        full = provider(c['routine'], ROTINAS[c['routine']][1], r)
        provider_ok = all(full[k] == int(c['exit_registers'][k], 16) for k in REG7)
        partial = {k: r[k] for k in t.argumentos(c['routine'])}
        p, pc2 = memoria_caso(blocos)
        sparse = provedor_recrutamento(RecrutamentoCore(p, bonus=bonus_recrutamento(p)))(
            c['routine'], ROTINAS[c['routine']][1], partial)
        uncertain = sparse.get('_incertos', {})
        sparse_ok = all(not ((sparse[k] ^ int(c['exit_registers'][k], 16)) & ~uncertain.get(k, 0) & 0xffffffff)
                        for k in REG7)
        return dict(ok=not dif and changed == c['changed_bytes'] and provider_ok and sparse_ok and
                    mudancas(blocos, pc2) == c['changed_bytes'] and not c['boundaries'],
                    register_differences=dif, changed_equal=changed == c['changed_bytes'],
                    provider_equal=provider_ok, partial_known_bits_equal=sparse_ok,
                    python_changed=changed[:15] if changed != c['changed_bytes'] else [])
    except Exception as e:
        return dict(ok=False, python_error=f'{type(e).__name__}: {e}')


def variantes(nome, regs, pool):
    u = pool + (regs['EAX'] & 65535) * 276
    def w(a, v, n=1):
        return a, v.to_bytes(n, 'little')
    yield 'upper register bits', {k: v ^ (0x12340000 + i * 0x110000) for i, (k, v) in enumerate(regs.items())}, []
    if nome == 'EnginSetType':
        for tipo in range(26):
            for dono in (0, 200):
                yield f'type {tipo} owner {dono}', dict(regs, ECX=tipo, EBX=255 - tipo), [w(u, dono), w(0x496304, regs['EAX'] & 65535, 2)]
    elif nome == 'EnginAddVie':
        for tipo in range(26):
            for vida, delta in ((0, 1), (100, 1000), (65530, 20)):
                yield f'type {tipo} life {vida} delta {delta}', dict(regs, EDX=delta), [w(u+1, tipo), w(u+0x9a, vida, 2)]
    elif nome == 'EnginResetFatigue':
        for i in (0, 4, 799):
            for fatigue in (0, 65535):
                yield f'unit {i} fatigue {fatigue}', dict(regs, EAX=i), [w(pool+i*276+0x76, fatigue, 2)]
    elif nome == 'EnginSetExperimente':
        for dono in range(4):
            for tipo in (0, 4, 7):
                for nivel in range(8):
                    fila = bytes((tipo, (nivel << 5) | 3, 1, 0x23, 2, 0x43, 3, 0x63, 4, 0x83))
                    yield f'owner {dono} type {tipo} level {nivel}', regs, [w(u, dono), w(u+1, tipo), (0x4e19c4+dono*10, fila)]
        yield 'nonmatching first pair', regs, [(0x4e19c4, bytes((255, 32)))]
        yield 'empty first pair', regs, [(0x4e19c4, bytes((7, 0)))]
    elif nome == 'SetSortEngin':
        for dono in (0, 1, 2, 3, 4, 200):
            for estado in (0, 4, 14):
                yield f'owner {dono} state {estado}', regs, [w(u, dono), w(u+2, estado), w(u+0xbb, 10), w(u+0xf5, 1), w(0x496304, regs['EAX'] & 65535, 2)]


def executar(traduzir=False):
    from emulador import BancadaX86, PILHA, RETORNO, mapear_paginas, HASH_ORIGINAL
    from unicorn import x86_const as X
    casos = []
    t0 = time.monotonic()
    def registrar(c, blocks):
        if traduzir:
            c['comparison'] = comparar(c, blocks)
        casos.append(c)
    # Replay the committed complete producer fixtures, stopping at the actual owner call sites.
    raw = (RAIZ / ECONOMY).read_bytes()
    fixture = json.loads(lzma.decompress(raw))
    if fixture['original_sha256'] != HASH_ORIGINAL:
        raise ValueError('Economy fixture executable identity')
    selected = [c for c in fixture['calls'] if c['routine'] == 'CalculTroupe' and c['frame'] in (297, 869, 1363)]
    if len(selected) != 3:
        raise ValueError('Expected three complete producer fixtures')
    for f in selected:
        b = BancadaX86()
        uc = b.cpu
        regions = list(uc.mem_regions())
        pages = {a & ~4095 for s, h in f['read_before_write'] for a in range(int(s, 16), int(s, 16)+len(h)//2)
                 if not any(lo <= a <= hi for lo, hi, _ in regions)}
        pages |= {int(store[2], 16) & ~4095 for store in f['stores']
                  if not any(lo <= int(store[2], 16) <= hi for lo, hi, _ in regions)}
        mapear_paginas(uc, pages)
        for s, h in f['read_before_write']:
            uc.mem_write(int(s, 16), bytes.fromhex(h))
        uc.reg_write(X.UC_X86_REG_FPCW, 0x127f)
        regs = {k: int(f['entry_registers'][k], 16) for k in REG7}
        out = b.executar(0x4259e6, [(0x401000, 0x494000)], regs,
                         parada=ROTINAS['EnginSetType'][0], limite_instrucoes=1000000)
        for nome, (entry, call) in ROTINAS.items():
            if out['EIP'] != entry or struct.unpack('<I', uc.mem_read(out['ESP'], 4))[0] != call+5:
                raise RuntimeError('Original missed the real SortieTroupe call site')
            ref = next(c for c in f['calls'] if c[1] == nome)
            if any(out[k] != int(ref[2][k], 16) for k in ref[2]):
                raise RuntimeError('Native entry differs from the committed Economy capture')
            before = {str(i): (lo, bytes(uc.mem_read(lo, hi-lo+1))) for i, (lo, hi, _) in enumerate(uc.mem_regions())
                      if lo != PILHA}
            r = dict(out)
            out = b.retomar(entry, [(0x401000, 0x494000)], parada=call+5, limite_instrucoes=1000000)
            if out['EIP'] != call+5 or out['ESP'] != r['ESP']+4:
                raise RuntimeError('Owner routine did not return')
            if any(out[k] != int(ref[5][k], 16) for k in REG7):
                raise RuntimeError('Owner exit differs from committed Economy capture')
            from validar_selecao_ordens import mudancas
            after = {n: (a, bytes(uc.mem_read(a, len(h)))) for n, (a, h) in before.items()}
            c = dict(routine=nome, kind='economy_fixture', frame=f['frame'], caller_return=hex(call+5),
                     entry_registers={k: hex(r[k]) for k in REG7}, esp=hex(r['ESP']),
                     exit_registers={k: hex(out[k]) for k in REG7+('ESP',)},
                     changed_bytes=mudancas(before, after), boundaries=[])
            registrar(c, before)
            if nome != 'SetSortEngin':
                nxt = list(ROTINAS)[list(ROTINAS).index(nome)+1]
                out = b.retomar(call+5, [(0x401000, 0x494000)], parada=ROTINAS[nxt][0], limite_instrucoes=1000000)
        print(f'Economy frame {f["frame"]} captured', file=sys.stderr, flush=True)
    # Real S1 trajectory; every frame's full state agrees with the committed original record.
    s1 = bs.BancadaS1(2500)
    seeds = []
    def fechar(c, blocks):
        registrar(c, blocks)
        seeds.append((c, blocks))
    obs = bs.Observacao(s1.b, {n: 0 for n in ROTINAS},
                         escolher=lambda n, r, ret, o: ret == ROTINAS[n][1]+5, ao_fechar=fechar)
    while s1.k < 2547:
        s1.avancar(obs)
    if obs.erros or len(seeds) != 5:
        raise RuntimeError(f'Expected five actual S1 calls: {len(seeds)}, {obs.erros}')
    obs.remover()
    saved, context = bs.imagem(s1.b), s1.b.cpu.context_save()
    try:
        for seed, blocks in seeds:
            regs = {k: int(v, 16) for k, v in seed['entry_registers'].items()}
            pool = struct.unpack('<I', s1.b.cpu.mem_read(0x4e19a0, 4))[0]
            for label, r, writes in variantes(seed['routine'], regs, pool):
                bs.restaurar(s1.b, blocks)
                c, before = bs.folha(s1.b, seed['routine'], r, escritas=writes, rotulo=label, quadro=2547)
                registrar(c, before)
            print(f'{seed["routine"]} leaves complete ({len(casos)} total)', file=sys.stderr, flush=True)
    finally:
        bs.restaurar(s1.b, saved)
        s1.b.cpu.context_restore(context)
    if bs.imagem(s1.b) != saved:
        raise RuntimeError('Declared leaves changed the S1 state')
    return dict(original_sha256=HASH_ORIGINAL, economy_fixture=ECONOMY,
                economy_fixture_sha256=hashlib.sha256(raw).hexdigest(), s1=s1.reproducao(),
                source_revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=RAIZ, text=True).strip(),
                cases=casos, by_routine=dict(Counter(c['routine'] for c in casos)), seconds=round(time.monotonic()-t0, 2))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--capturar', action='store_true')
    a = ap.parse_args()
    if a.capturar:
        if CAPTURA.exists():
            raise SystemExit('Refusing capture replacement')
        d = executar()
        if 'recrutamento_core' in sys.modules:
            raise RuntimeError('Original-first capture imported translation')
        d.update(schema='rising-lands/core-recruit-capture/1', translation_executed=False)
        CAPTURA.parent.mkdir(parents=True, exist_ok=True)
        CAPTURA.write_bytes(lzma.compress((json.dumps(d, sort_keys=True)+'\n').encode()))
        output = CAPTURA
    else:
        raw = CAPTURA.read_bytes()
        committed = subprocess.check_output(['git', 'show', f'HEAD:{CAPTURA.relative_to(RAIZ)}'], cwd=RAIZ)
        if raw != committed:
            raise SystemExit('Commit the original-only capture before comparing')
        ref = json.loads(lzma.decompress(raw))
        d = executar(True)
        results = []
        for i, c in enumerate(d.pop('cases')):
            cmp = c.pop('comparison')
            cmp['native_equals_capture'] = c == ref['cases'][i]
            cmp['ok'] &= cmp['native_equals_capture']
            results.append(dict(routine=c['routine'], kind=c['kind'], label=c.get('label'), **cmp))
        d.update(schema='rising-lands/core-recruit-differential/1', comparisons=len(results),
                 capture_cases=len(ref['cases']), cases=results, mismatches=[c for c in results if not c['ok']],
                 source_sha256={p: hashlib.sha256((RAIZ/p).read_bytes()).hexdigest() for p in FONTES},
                 capture_sha256=hashlib.sha256(raw).hexdigest())
        output = RELATORIO if not d['mismatches'] else RAIZ / '.local/recrutamento-core-falha.json'
        output.write_text(json.dumps(d, indent=1, sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(output), by_routine=d['by_routine'], seconds=d['seconds'],
                         mismatches=len(d.get('mismatches', []))), indent=1), flush=True)
    from encerramento_captura import encerrar_captura
    encerrar_captura(2 if d.get('mismatches') else 0, output)


if __name__ == '__main__':
    main()
