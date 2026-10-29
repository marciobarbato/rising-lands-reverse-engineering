"""Compare game-logic state of the v1 and display-executing MONDE01 captures, phase by phase.

CPU-free, from committed original-only captures only.  The display scenario
allocates bank/AffInit buffers before MissionLoad, so every allocation pointer
moves.  Allocations are matched by their call sequence (the v1 record
sequence of (caller return, size, flags) must be a subsequence of the display
one); pointer words are then normalized: a dword whose v1 value points into a
matched v1 allocation and whose display value is the same offset into its
partner is a relocation, not a difference.  Everything else that differs is
reported byte by byte, per state (MissionLoad entry and return, after
load_tail, between_frames and frame1), with the first state where it appears.
Unmatched display allocations (banks, surfaces' helpers) are listed as
display-only blocks.

    python3 -B pesquisas-paralelas/missoes/comparar_quadros_exibicao.py \
        --relatorio pesquisas-paralelas/missoes/validacao/m2-frame1-v1-vs-exibicao.json
"""
import argparse
from bisect import bisect_right
import hashlib
import json
import struct
import subprocess
import sys

import ambiente_missoes
import cenarios_oraculo as cen
from mapa_memoria_m1 import carregar_blocos, carregar_json, expandir_captura

ESTADOS = ('entry', 's0', 'load_tail', 'between_frames', 'frame1')


def imagens(cenario):
    entrada = carregar_json(cen.caminho(cenario, 'entrada'))
    m1 = expandir_captura(carregar_json(cen.caminho(cenario, 'captura_m1')), entrada)
    quadro = carregar_json(cen.caminho(cenario, 'captura_quadro'))
    e = carregar_blocos(entrada['blocks'])
    e.pop('native_stack', None)
    saida = dict(entry=e, s0=carregar_blocos(m1['oracle']['final_state']['blocks']))
    atual = saida['s0']
    for p in quadro['phases']:
        st = p['state_after']
        novos = carregar_blocos(st['blocks_changed_since_previous'])
        img = {}
        for nome, h in st['block_hashes'].items():
            base, dados = novos[nome] if nome in novos else atual[nome]
            if hashlib.sha256(dados).hexdigest() != h['sha256']:
                raise ValueError(f'{cenario} {p["phase"]} block {nome} does not match its hash')
            img[nome] = (base, dados)
        saida[p['phase']] = atual = img
    return saida, quadro['allocations'], m1['allocations'], entrada


def _chave(r):
    """(GlobalAlloc caller return, size, flags, code return addresses among the eight caller-stack words).

    Every MemAlloc-based GlobalAlloc shares the caller return 0x467ec0, so the
    stack words (which hold MemAlloc's caller and that caller's caller) are
    needed to tell allocations apart.
    """
    pilha = tuple(w for w in r.get('stack') or () if 0x401000 <= int(w, 16) < 0x493c00)
    return (r['caller_return'], r['size'], r['flags'], r.get('kind'), pilha)


def emparelhar(v1, v2):
    """Map v1 allocation records to display records by call-sequence subsequence."""
    chave = _chave
    v1, v2 = sorted(v1, key=lambda r: r['index']), sorted(v2, key=lambda r: r['index'])
    pares, j = {}, 0
    for r in v1:
        while j < len(v2) and chave(v2[j]) != chave(r):
            j += 1
        if j == len(v2):
            raise ValueError(f'v1 allocation {r["index"]} {chave(r)} has no display partner in order')
        pares[r['index']] = v2[j]
        j += 1
    return pares


class Relocacao:
    def __init__(self, v1, pares):
        self.intervalos = sorted((int(r['pointer'], 16), r['size'], int(pares[r['index']]['pointer'], 16))
                                 for r in v1)
        self.inicios = [x[0] for x in self.intervalos]

    def mapear(self, valor):
        i = bisect_right(self.inicios, valor)-1
        if i < 0:
            return None
        p, n, q = self.intervalos[i]
        return q+(valor-p) if p <= valor <= p+n else None


def diferencas(a, b, base, reloc):
    """Byte offsets differing after pointer normalization (relocated dwords removed)."""
    if len(a) != len(b):
        raise ValueError('Matched blocks have different sizes')
    difs = [i for i in range(len(a)) if a[i] != b[i]] if a != b else []
    restantes, relocados = set(difs), set()
    for i in difs:
        if i in relocados:
            continue
        for k in range(max(0, i-3), min(i, len(a)-4)+1):
            va, vb = struct.unpack_from('<I', a, k)[0], struct.unpack_from('<I', b, k)[0]
            if va != vb and reloc.mapear(va) == vb:
                relocados.update(range(k, k+4))
                break
    restantes -= relocados
    return sorted(restantes), len(relocados & set(difs))


def faixas(enderecos, a_val, b_val, limite=400):
    saida, ordem = [], sorted(enderecos)
    for x in ordem:
        if saida and x == saida[-1][1]:
            saida[-1][1] += 1
        else:
            saida.append([x, x+1])
    return [dict(start=hex(s), end=hex(e), v1=a_val(s, e).hex(), display=b_val(s, e).hex()) for s, e in saida[:limite]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--relatorio', required=True)
    args = ap.parse_args()
    saida = ambiente_missoes.ROOT/args.relatorio
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    i1, aloc1_q, aloc1, _ = imagens('v1')
    i2, aloc2_q, aloc2, _ = imagens('exibicao')
    # Frames allocate nothing in either scenario; the MissionLoad captures keep the caller-stack words.
    if [r['index'] for r in aloc1_q] != [r['index'] for r in aloc1] or len(aloc2_q) != len(aloc2):
        raise ValueError('Frame phases created allocations: extend the matching to them')
    pares = emparelhar(aloc1, aloc2)
    reloc = Relocacao(aloc1, pares)
    nome2 = {int(r['pointer'], 16): f"alloc{r['index']:05d}" for r in aloc2}
    estados, primeiro = {}, {}
    for estado in ESTADOS:
        a, b = i1[estado], i2[estado]
        relatorio_estado = dict(blocks_v1=len(a), blocks_display=len(b), relocated_bytes=0, differing={})
        usados = set()
        for nome, (base, dados) in a.items():
            if nome.startswith('alloc'):
                indice = int(nome[5:])
                parceiro = pares[indice]
                nome_b = nome2[int(parceiro['pointer'], 16)]
                if nome_b not in b:
                    relatorio_estado['differing'][nome] = dict(missing_in_display=nome_b)
                    continue
                base_b, dados_b = b[nome_b]
            else:
                nome_b = nome
                base_b, dados_b = b[nome]
            usados.add(nome_b)
            restantes, relocados = diferencas(dados, dados_b, base, reloc)
            relatorio_estado['relocated_bytes'] += relocados
            if restantes:
                enderecos = [base+i for i in restantes]
                relatorio_estado['differing'][nome] = dict(
                    display_block=nome_b, display_base=hex(base_b), v1_base=hex(base), bytes=len(restantes),
                    ranges=faixas(enderecos, lambda s, e: dados[s-base:e-base],
                                  lambda s, e: dados_b[s-base:e-base]))
                for x in enderecos:
                    primeiro.setdefault((nome, x-base), estado)
        so_exibicao = sorted(set(b)-usados)
        relatorio_estado['display_only_blocks'] = dict(count=len(so_exibicao),
                                                       bytes=sum(len(b[n][1]) for n in so_exibicao))
        relatorio_estado['differing_bytes'] = sum(v.get('bytes', 0) for v in relatorio_estado['differing'].values())
        estados[estado] = relatorio_estado
    revisao = subprocess.run(['git', '-C', str(ambiente_missoes.ROOT), 'rev-parse', 'HEAD'],
                             capture_output=True, text=True).stdout.strip()
    rel = dict(schema='rising-lands/monde01-v1-vs-display-logic-state/1', source_revision=revisao, cpu_free=True,
               inputs={f'{c}_{k}': dict(path=str(cen.caminho(c, k).relative_to(ambiente_missoes.ROOT)),
                                        sha256=hashlib.sha256(cen.caminho(c, k).read_bytes()).hexdigest())
                       for c in ('v1', 'exibicao') for k in ('entrada', 'captura_m1', 'captura_quadro')},
               allocation_matching=dict(v1_records=len(aloc1), display_records=len(aloc2), matched=len(pares)),
               states=estados,
               first_state_of_each_difference={f'{n}+0x{o:x}': s for (n, o), s in sorted(primeiro.items())},
               method=__doc__.split('\n\n')[1].replace('\n', ' '))
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(rel, f, indent=1)
        f.write('\n')
    print(json.dumps({e: dict(differing_bytes=v['differing_bytes'], relocated=v['relocated_bytes'],
                              blocks=list(v['differing'])[:12], display_only=v['display_only_blocks'])
                      for e, v in estados.items()}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
