"""Static write-set closure of AffGame 0x417698 (and other ProgIteration display callees) from the intact bytes.

Recursive-descent x86-32 disassembly of the intact RISING.EXE image (identity checked by imagem_pe). Collects the
call graph and every memory store. No execution. Usage: python3 fechamento_escritas_affgame.py out.json  (mode-0x12 closure report)
"""
import json, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_OP_MEM, CS_OP_IMM, CS_OP_REG, CS_AC_WRITE
from capstone.x86 import X86_REG_ESP, X86_REG_EBP
from extrair_evidencias import imagem_pe

base, imagem = imagem_pe()
CODIGO = (0x401000, 0x493c00); DADOS = (0x494000, 0x523000)
md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail = True
def ler(a, n=16): return bytes(imagem[a-base:a-base+n])
def u32(a): return struct.unpack_from('<I', imagem, a-base)[0]


def varrer(entrada):
    """Recursive descent from a routine entry. Returns (instrucoes dict, chamadas diretas, indiretas, tabelas)."""
    insns, filas = {}, [entrada]; diretas, indiretas, saltos_ind = set(), [], []
    while filas:
        a = filas.pop()
        while CODIGO[0] <= a < CODIGO[1] and a not in insns:
            i = next(md.disasm(ler(a), a), None)
            if i is None: insns[a] = None; break
            insns[a] = i; m = i.mnemonic
            if m == 'call':
                o = i.operands[0]
                if o.type == CS_OP_IMM: diretas.add(o.imm)
                else: indiretas.append((a, i.op_str))
                a += i.size; continue
            if m == 'jmp':
                o = i.operands[0]
                if o.type == CS_OP_IMM: a = o.imm; continue
                saltos_ind.append((a, i.op_str, o))
                break
            if m.startswith('j') or m.startswith('loop') or m == 'jecxz':
                filas.append(i.operands[0].imm)
            if m in ('ret', 'retn', 'hlt', 'int3', 'ud2'): break
            a += i.size
    return insns, diretas, indiretas, saltos_ind


def tabela_salto(o, insns):
    """Resolve 'jmp [reg*4 + abs]' tables: read dwords while they point into code."""
    if o.mem.base or o.mem.scale != 4 or not o.mem.disp: return None
    t, alvos = o.mem.disp & 0xffffffff, []
    while CODIGO[0] <= t < 0x523000 and len(alvos) < 512:
        v = u32(t)
        if not CODIGO[0] <= v < CODIGO[1]: break
        alvos.append(v); t += 4
    return alvos


def escritas(i):
    saida = []
    if i is None: return saida
    if i.mnemonic.startswith(('stos', 'movs', 'rep stos', 'rep movs')) or 'stos' in i.mnemonic or 'movs' in i.mnemonic and i.mnemonic not in ('movsx', 'movsxd', 'movss', 'movsd'):
        saida.append(('cadeia', i.mnemonic+' '+i.op_str))
    for o in i.operands:
        if o.type == CS_OP_MEM and o.access & CS_AC_WRITE:
            mem = o.mem
            if i.mnemonic == 'lea': continue
            base_r = i.reg_name(mem.base) if mem.base else None; idx = i.reg_name(mem.index) if mem.index else None
            saida.append(('mem', dict(base=base_r, indice=idx, escala=mem.scale, disp=mem.disp & 0xffffffff, tamanho=o.size, seg=i.reg_name(mem.segment) if mem.segment else None)))
    if i.mnemonic in ('push', 'call'): return []
    if i.mnemonic in ('xchg', 'cmpxchg', 'xadd'):
        pass
    return saida


def fechar(raiz):
    visitadas, fila, grafo, todas, desconhecidos = {}, [raiz], {}, {}, []
    while fila:
        f = fila.pop()
        if f in visitadas or not CODIGO[0] <= f < CODIGO[1]: continue
        insns, d, ind, saltos = varrer(f)
        alvos_salto = []
        for a, txt, o in saltos:
            t = tabela_salto(o, insns)
            if t is None: desconhecidos.append(dict(rotina=f, endereco=a, tipo='jmp-indireto', operando=txt))
            else:
                # re-descend into each table target within this routine
                for v in t:
                    ins2, d2, ind2, s2 = varrer(v)
                    insns.update(ins2); d |= d2; ind += ind2
                    for a2, txt2, o2 in s2:
                        t2 = tabela_salto(o2, insns)
                        if t2 is None: desconhecidos.append(dict(rotina=f, endereco=a2, tipo='jmp-indireto', operando=txt2))
        for a, txt in ind: desconhecidos.append(dict(rotina=f, endereco=a, tipo='call-indireto', operando=txt))
        visitadas[f] = sorted(insns); grafo[f] = sorted(d); todas.update({a: (f, i) for a, i in insns.items()})
        fila += list(d)
    return visitadas, grafo, todas, desconhecidos


ALVOS = (0x4e2f78, 0x4e1b0e, 0x4e060c, 0x4e0610, 0x507d54, 0x50a9b4, 0x50a9b6, 0x4e1d18)
ENTRADA_MODO12 = 0x4178f7  # AffGame body for [0x4e2f78] == 0x12 (dispatch 0x4176a8..0x4176af)


def _abs_dgroup(i):
    for o in i.operands:
        if o.type == CS_OP_MEM and not o.mem.base and not o.mem.index and DADOS[0] <= (o.mem.disp & 0xffffffff) < DADOS[1]:
            yield o.mem.disp & 0xffffffff, o.size, bool(o.access & CS_AC_WRITE)


def modo12():
    """Closure of the mode-0x12 path of AffGame: body + every direct callee; absolute DGROUP stores, pointer stores,
    and the overlap with absolute reads in the game-logic closure of CalculGame 0x42C868 (routines outside the closure)."""
    corpo, d, ind, saltos = varrer(ENTRADA_MODO12)
    for a, txt, o in saltos:
        for v in tabela_salto(o, corpo) or []:
            i2, d2, ind2, s2 = varrer(v); corpo.update(i2); d |= d2; ind += ind2
    vis, grafo, todas = {}, {}, {a: (0x417698, i) for a, i in corpo.items()}
    desconhecidos = [dict(rotina=0x417698, endereco=a, operando=t) for a, t in ind]
    for c in sorted(d):
        v, g, t, dd = fechar(c); vis.update(v); grafo.update(g); todas.update(t); desconhecidos += dd
    escritos = {}
    ponteiros = []
    for a, (f, i) in sorted(todas.items()):
        if i is None: continue
        for ad, sz, w in _abs_dgroup(i):
            if w: escritos.setdefault(ad, []).append((a, f, i.mnemonic+' '+i.op_str))
        for tp, w in escritas(i):
            if tp == 'mem' and (w['base'] or w['indice']) and w['base'] not in ('esp', 'ebp'):
                ponteiros.append((a, f, i.mnemonic+' '+i.op_str))
    visL, grL, todasL, _ = fechar(0x42c868)
    leitores = {}
    for a, (f, i) in todasL.items():
        if i is None or f in vis: continue
        for ad, sz, w in _abs_dgroup(i):
            if not w: leitores.setdefault(ad, []).append((a, f))
    inter = {ad: dict(stores=[hex(a) for a, f, t in escritos[ad]], leitores_logica=[hex(a) for a, f in leitores[ad]][:8])
        for ad in sorted(escritos) if ad in leitores}
    hx = lambda x: hex(x)
    return dict(entrada=hx(ENTRADA_MODO12), rotinas=[hx(x) for x in sorted(vis)], chamadas_diretas_corpo=[hx(x) for x in sorted(d)],
        indiretos_nao_resolvidos=len(desconhecidos), escritas_absolutas={hx(k): [[hx(a), hx(f), t] for a, f, t in v] for k, v in sorted(escritos.items())},
        escritas_por_ponteiro_nao_pilha=[[hx(a), hx(f), t] for a, f, t in ponteiros],
        interseccao_com_leitores_da_logica={hx(k): v for k, v in inter.items()},
        alvos={hx(a): [[hx(x), hx(f), t] for x, f, t in escritos.get(a, [])] for a in ALVOS if a not in (0x4e1d18,)} | {'0x4e1d18': len(escritos[0x4e1d18])})


def principal(saida):
    r = modo12(); json.dump(r, open(saida, 'w'), indent=1)
    print(len(r['rotinas']), 'routines', len(r['escritas_absolutas']), 'distinct absolute DGROUP store addresses',
        len(r['interseccao_com_leitores_da_logica']), 'also read by game logic;', r['indiretos_nao_resolvidos'], 'unresolved indirect transfers')


if __name__ == '__main__': principal(sys.argv[1])
