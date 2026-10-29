"""Compare the isolated economy calls of two oracle scenarios (v1 vs exibicao) call by call.

Reads only committed captures (no execution). Calls are matched by phase,
routine and order within that pair. Every allocation moved between the
scenarios (the display path allocates banks before MissionLoad), so v1
allocation addresses are mapped to their display partners with Missions'
CPU-free allocation matching (``comparar_quadros_exibicao.emparelhar``):
an address inside a matched allocation, a register value pointing into one,
and a little-endian dword of read bytes whose v1 value relocates to the
display value are relocations, not differences. Native stack addresses and
register values are compared relative to the entry ESP. Every remaining
difference is listed with both values; nothing else is filtered out.

    python3 -B pesquisas-paralelas/economia/comparar_quadro1_economia_cenarios.py
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
sys.path.insert(0, str(PASTA / 'testes'))
PILHA = (0x2000000, 0x2010000)   # emulador.PILHA .. +0x10000, the Missions bench native stack


def relocacao():
    """v1 -> display address map over the matched MissionLoad allocations (Missions' matching)."""
    # ambiente_missoes reorders sys.path (other fronts first); restore it after the imports.
    caminho = list(sys.path)
    sys.path.insert(0, str(RAIZ / 'pesquisas-paralelas/missoes'))
    try:
        import cenarios_oraculo as cen
        from comparar_quadros_exibicao import Relocacao, emparelhar
        from mapa_memoria_m1 import carregar_json
    finally:
        sys.path[:] = caminho
    # The frozen display captures were recorded on Missions' Stage17 artifacts (``exibicao_interino``).
    aloc = {c: carregar_json(cen.caminho(c, 'captura_m1'))['allocations'] for c in ('v1', 'exibicao_interino')}
    return Relocacao(aloc['v1'], emparelhar(aloc['v1'], aloc['exibicao_interino']))


class Normalizador:
    def __init__(self, reloc, esp, v1):
        self.reloc, self.esp, self.v1 = reloc, esp, v1

    def __call__(self, valor):
        if PILHA[0] <= valor < PILHA[1]:
            return ('stack', valor - self.esp)
        if self.v1:
            mapeado = self.reloc.mapear(valor)
            if mapeado is not None and mapeado != valor:
                return mapeado
        return valor


def lidos_relocados(lidos, normalizar, v1):
    """Read bytes keyed by normalized address; v1 dwords that relocate take their display value."""
    saida = {normalizar(a): v for a, v in lidos.items()}
    if not v1:
        return saida
    for a in sorted(lidos):
        if all(a + i in lidos for i in range(4)):
            valor = int.from_bytes(bytes(lidos[a + i] for i in range(4)), 'little')
            novo = normalizar.reloc.mapear(valor)
            if novo is not None and novo != valor:
                for i, b in enumerate(novo.to_bytes(4, 'little')):
                    saida[normalizar(a + i)] = b
    return saida


def chamada_normalizada(c, reloc, v1):
    n = Normalizador(reloc, int(c['entry_registers']['ESP'], 16), v1)
    return dict(
        entry_registers={k: n(int(v, 16)) for k, v in c['entry_registers'].items()},
        exit_registers={k: n(int(v, 16)) for k, v in c['exit_registers'].items()},
        reached_exit=c['reached_exit'],
        changed_bytes={n(int(a, 16)): (v, m) for a, v, m in c['changed_bytes']},
        read_before_write=lidos_relocados({int(a, 16): v for a, v, _ in c['read_before_write']}, n, v1),
        written_unchanged={n(int(a, 16)): v for a, v in c['written_unchanged']})


def chave_json(k):
    return k if isinstance(k, str) else (f'ESP{k[1]:+#x}' if isinstance(k, tuple) else hex(k))


def valor_json(v):
    return f'ESP{v[1]:+#x}' if isinstance(v, tuple) else v


def diferencas(a, b):
    saida = {}
    for campo in a:
        x, y = a[campo], b[campo]
        if x == y:
            continue
        if isinstance(x, dict):
            chaves = sorted(set(x) | set(y), key=lambda k: (isinstance(k, tuple), k[1] if isinstance(k, tuple) else k))
            saida[campo] = {chave_json(k): [valor_json(x.get(k)), valor_json(y.get(k))] for k in chaves
                            if x.get(k) != y.get(k)}
        else:
            saida[campo] = [x, y]
    return saida


def comparar(a='v1', b='exibicao'):
    import test_quadro1_economia as t1
    ca, cb = t1.evidencia(a), t1.evidencia(b)
    reloc = relocacao()

    def agrupar(c):
        grupos = {}
        for r in c['calls']:
            grupos.setdefault((r['phase'], r['routine']), []).append(r)
        return grupos
    ga, gb = agrupar(ca), agrupar(cb)
    linhas, alterados = [], []
    for chave in sorted(set(ga) | set(gb)):
        xa, xb = ga.get(chave, []), gb.get(chave, [])
        difs = []
        for i, (ra, rb) in enumerate(zip(xa, xb)):
            d = diferencas(chamada_normalizada(ra, reloc, True), chamada_normalizada(rb, reloc, False))
            if d:
                difs.append(dict(index=i, differences=d))
        linha = dict(phase=chave[0], routine=chave[1], calls=[len(xa), len(xb)],
                     identical_after_pool_normalization=len(xa) == len(xb) and not difs, differing_calls=difs)
        linhas.append(linha)
        if not linha['identical_after_pool_normalization']:
            alterados.append(f'{chave[0]}:{chave[1]}')
    return dict(
        scenarios=[a, b], captures={s: dict(path=str(t1.CAPTURAS[s].relative_to(RAIZ)),
                                            sha256=hashlib.sha256(t1.CAPTURAS[s].read_bytes()).hexdigest())
                                    for s in (a, b)},
        calls=[len(ca['calls']), len(cb['calls'])],
        method='calls matched by (phase, routine, order); v1 addresses, register values and read dwords inside '
               'matched MissionLoad allocations relocated to their display partners (Missions\' matching); '
               'native stack addresses relative to the entry ESP; everything else raw',
        changed=alterados, routines=linhas)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--saida', default=str(PASTA / 'validacao-quadro1-economia-v1-vs-exibicao.json'))
    relatorio = comparar()
    Path(ap.parse_args().saida).write_text(json.dumps(relatorio, indent=1) + '\n')
    print(json.dumps(dict(calls=relatorio['calls'], changed=relatorio['changed']),
                     indent=1))


if __name__ == '__main__':
    main()
