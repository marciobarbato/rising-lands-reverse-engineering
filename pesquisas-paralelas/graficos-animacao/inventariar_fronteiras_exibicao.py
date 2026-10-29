"""Inventory of the display boundaries, bank files and RestoreAll's static DGROUP effects, from the intact bytes.

Static only (capstone recursive descent + PE import table + media sizes). Usage: python3 inventariar_fronteiras_exibicao.py out.json
"""
import collections, hashlib, json, re, struct, sys
from pathlib import Path
from capstone import CS_OP_IMM, CS_OP_MEM, CS_AC_WRITE
from extrair_evidencias import imagem_pe
from fechamento_escritas_affgame import base, imagem, fechar, varrer, u32, _abs_dgroup, DADOS
from graficos import RAIZ

sys.path.insert(0, str(RAIZ.parents[1]/'ferramentas'))
from vinculos_declarados import importacoes_pe  # noqa: E402

SIMBOLOS = RAIZ.parents[1]/'relatorios/simbolos-originais.tsv'
MIDIA = RAIZ.parents[2].parent/'source/cd'
RAIZES = ('ProgInit', 'MenuInit', 'RestoreAll', 'CalculGame', 'AffGame', 'ResetMode')
ENVOLTORIOS_DD = ('DDInit', 'DDExit', 'DDSetPalette', 'DDLockSurface', 'DDUnlockSurface', 'DDLockSurfaceVideo', 'DDUnlockSurfaceVideo',
    'DDFlipPage', 'DDFlipToGDISurface', 'DDRestoreAll', 'DDGetDC', 'DDReleaseDC', 'DDLockSurfaceTemp', 'DDUnlockSurfaceTemp',
    'DDUtil_TreatError', 'ResetMode', 'AffInit', 'AffExit', 'RestoreAll', 'SetClipping')
# Object globals of the wrappers (from DDInit 0x43F50B): IDirectDraw, primary, offscreen 800x600, palette.
OBJETOS = {0x4e1788: 'IDirectDraw', 0x4e178c: 'primary surface', 0x4e1790: 'offscreen surface (system memory)', 0x4e179c: 'palette'}


def simbolos():
    t = {}
    for linha in SIMBOLOS.read_text().splitlines()[1:]:
        a, n = linha.split('\t')[:2]; t.setdefault(int(a, 16), n)
    return t


def cstr(a):
    o = bytearray()
    while imagem[a-base]: o.append(imagem[a-base]); a += 1
    return bytes(o).decode('latin-1')


def principal(saida):
    sym = simbolos(); porNome = {n: a for a, n in sym.items()}
    imp = importacoes_pe(Path(MIDIA/'INSTALHD/RISING.EXE').read_bytes(), base)
    resultado = dict(exe_sha256=hashlib.sha256(Path(MIDIA/'INSTALHD/RISING.EXE').read_bytes()).hexdigest())
    # 1. Wrappers: COM vtable calls and IAT calls (own bodies, direct callees listed separately).
    wrappers = {}
    for n in ENVOLTORIOS_DD:
        insns, d, ind, saltos = varrer(porNome[n]); com, iat = [], []
        for a, t in ind:
            m = re.search(r'\[(e[a-z]{2}) \+ (0x[0-9a-f]+)\]', t)
            if m: com.append(dict(site=hex(a), vtable_offset=m.group(2)))
            else:
                m = re.search(r'cs:\[(0x[0-9a-f]+)\]', t)
                if m: iat.append(dict(site=hex(a), slot=m.group(1), **imp.get(int(m.group(1), 16), {})))
        rets = sorted({i.op_str for i in insns.values() if i and i.mnemonic in ('ret', 'retn')})
        wrappers[n] = dict(address=hex(porNome[n]), ret_operand=rets, com_calls=com, iat_calls=iat,
            direct_callees=[sym.get(c, hex(c)) for c in sorted(d)])
    resultado['wrappers'] = wrappers
    # 2. IAT slots reached from each root's closure (all routines).
    alcance = {}
    for r in RAIZES:
        vis, g, todas, desc = fechar(porNome[r]); cont = collections.Counter(); com = collections.Counter()
        for dd in desc:
            t = dd['operando']
            m = re.search(r'cs:\[(0x[0-9a-f]+)\]', t)
            if m:
                s = imp.get(int(m.group(1), 16)); cont[f"{s['dll']}.{s['symbol']}@{m.group(1)}" if s else 'unresolved@'+m.group(1)] += 1
            m = re.search(r'\[(e[a-z]{2}) \+ (0x[0-9a-f]+)\]$', t)
            if m: com[m.group(2)] += 1
        alcance[r] = dict(routines=len(vis), iat_sites=dict(sorted(cont.items())), register_offset_indirect_sites=dict(sorted(com.items())))
    resultado['alcance_por_raiz'] = alcance
    # 3. Bank/media inventory.
    arquivos = []
    nomes = [cstr(u32(0x495bc8+4*i)) for i in range(6)]
    candidatos = [(n, 'LoadSTRATBank name table 0x495bc8') for n in nomes]
    candidatos += [(cstr(a), f'string 0x{a:x}') for a in (0x494a76, 0x494ac5, 0x494ad8, 0x494a4d, 0x494a5b, 0x494a69, 0x494a8e, 0x494a9b,
        0x494ab7, 0x494d44, 0x494d88, 0x494d96, 0x4941b4, 0x494d52, 0x494d67, 0x494d6f, 0x494d7c, 0x494daa, 0x494df8)]
    install = MIDIA/'INSTALHD'
    for nome, origem in candidatos:
        alvo = nome.replace('\\', '/').lstrip('/')
        cand = [p for p in (install/alvo, install/alvo.upper(), install/Path(alvo).name, install/Path(alvo).name.upper(), install/'WORLD'/Path(alvo).name.upper()) if p.exists()]
        # case-insensitive lookup
        if not cand:
            for p in install.rglob('*'):
                if p.is_file() and p.name.lower() == Path(alvo).name.lower(): cand.append(p); break
        e = dict(path=nome, origin=origem, media=None)
        if cand:
            dados = cand[0].read_bytes(); e['media'] = dict(file=str(cand[0].relative_to(MIDIA)), bytes=len(dados), sha256=hashlib.sha256(dados).hexdigest())
        arquivos.append(e)
    resultado['arquivos'] = arquivos
    resultado['chamadas_de_banco'] = {}
    for raiz in ('ProgInit', 'MenuInit', 'RestoreAll', 'ResetMode'):
        vis, g, todas, desc = fechar(porNome[raiz]); alvos = {porNome[n]: n for n in ('LoadBank', 'LoadSTRATBank', 'SetBank', 'DeleteBank', 'LoadPie', 'LoadFonteExterieur', 'AffInit', 'DDInit', 'PaletteAlloc', 'CacheAlloc')}
        sites = [[hex(a), sym.get(f, hex(f)), alvos[i.operands[0].imm]] for a, (f, i) in sorted(todas.items())
            if i and i.mnemonic == 'call' and i.operands[0].type == CS_OP_IMM and i.operands[0].imm in alvos and sym.get(f) not in ('LoadBank', 'LoadSTRATBank')]
        resultado['chamadas_de_banco'][raiz] = sites
    # 4. RestoreAll: absolute DGROUP stores, own body and closure (pixel destinations are surface bytes, not DGROUP).
    vis, g, todas, desc = fechar(porNome['RestoreAll'])
    proprio = {a for a in varrer(porNome['RestoreAll'])[0]}
    por_rotina = collections.defaultdict(set)
    for a, (f, i) in sorted(todas.items()):
        if i is None: continue
        for ad, sz, w in _abs_dgroup(i):
            if w: por_rotina[ad].add(sym.get(f, hex(f)))
    resultado['restoreall'] = dict(rotinas=len(vis), chamadas_na_ordem=[[hex(a), sym.get(i.operands[0].imm, hex(i.operands[0].imm))]
        for a, i in sorted(varrer(porNome['RestoreAll'])[0].items()) if i and i.mnemonic == 'call' and i.operands[0].type == CS_OP_IMM],
        stores_dgroup_absolutos={hex(k): sorted(v) for k, v in sorted(por_rotina.items())}, indiretos_nao_resolvidos=len(desc))
    json.dump(resultado, open(saida, 'w'), indent=1)
    print({k: (len(v) if hasattr(v, '__len__') else v) for k, v in resultado.items()})
    for r, v in alcance.items(): print(r, v['iat_sites'])


if __name__ == '__main__': principal(sys.argv[1])
