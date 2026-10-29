"""Measure Unicorn teardown (``uc_close``) time against the number of mapped regions.

Every measurement runs in its own child interpreter with a wall-clock bound, so
a superlinear teardown cannot hold the heavy lease past the bound (the child is
killed and the case recorded as ``exceeded``). Three layouts are measured:

* ``synthetic``: N disjoint 4 KiB regions (one page gap between them);
* ``display``: the region layout of Missions' display-reference bench after
  MissionLoad (``percurso_quadro1._bancada('exibicao')``), captured live and
  then replayed by prefix in a bare engine: same bases, sizes and protections;
* ``display_bench``: the real display bench itself. The child times its own
  engine finalizer (``uc_close``) and then uses the fast exit;
* ``display_pages``: every 4 KiB page of the display post-load blocks
  (Missions' display MissionLoad capture, DGROUP excluded), mapped one region
  per page as Economy's ``capturar_quadro_m2_original.Captura`` does, by prefix,
  and then coalesced into contiguous runs (``emulador.mapear_paginas``).

    python3 -B ferramentas/medir_encerramento_unicorn.py --saida relatorios/encerramento-unicorn.json
"""
import argparse
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
SINTETICO = (250, 500, 1000, 2000, 3000, 4000)
LIMITE_S = 120

_CABECALHO = '''
import json, os, sys, time
sys.path.insert(0, {ferramentas!r}); sys.path.insert(0, {local!r})
import unicorn
from encerramento_captura import descarregar_saidas_padrao


def _fechar(cpu):
    # The binding's weakref.finalize (Uc.release_handle -> uc_close), the call interpreter shutdown makes.
    fim = cpu._Uc__finalizer
    t = time.perf_counter()
    fim()
    return time.perf_counter() - t
'''

# argv: layout JSON [[base, size, perms], ...]. Prints one JSON line, then leaves without finalization.
_REPLAY = '''
regioes = json.load(open(sys.argv[1]))
cpu = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
t = time.perf_counter()
for base, tamanho, prot in regioes:
    cpu.mem_map(base, tamanho, prot)
mapear = time.perf_counter() - t
n = len(list(cpu.mem_regions()))
fechar = _fechar(cpu)
print(json.dumps(dict(regions=n, map_s=round(mapear, 3), close_s=round(fechar, 3))))
descarregar_saidas_padrao()
os._exit(0)
'''

_BANCADA = '''
import percurso_quadro1 as pq
t = time.perf_counter()
b, _ = pq._bancada('exibicao')
construir = time.perf_counter() - t
regioes = [[a, z - a + 1, p] for a, z, p in b.cpu.mem_regions()]
with open(sys.argv[1], 'x') as f:
    json.dump(regioes, f)
print(json.dumps(dict(stage='built', regions=len(regioes), build_s=round(construir, 3))), flush=True)
print(json.dumps(dict(stage='closed', close_s=round(_fechar(b.cpu), 3))))
descarregar_saidas_padrao()
os._exit(0)
'''


def _filho(corpo, argumentos, limite):
    programa = _CABECALHO.format(ferramentas=str(RAIZ / 'ferramentas'), local=str(RAIZ / '.local/python')) + corpo
    t = time.monotonic()
    p = subprocess.Popen([sys.executable, '-B', '-c', programa, *map(str, argumentos)], stdout=subprocess.PIPE,
                         text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    try:
        saida, _ = p.communicate(timeout=limite)
        estado = 'returned' if p.returncode == 0 else f'status {p.returncode}'
    except subprocess.TimeoutExpired:
        p.kill()
        saida, _ = p.communicate()
        estado = 'exceeded'
    linhas = [json.loads(x) for x in saida.splitlines() if x.startswith('{')]
    return dict(outcome=estado, wall_s=round(time.monotonic() - t, 3), lines=linhas)


def _replay(regioes, pasta, nome, limite):
    caminho = Path(pasta) / f'{nome}.json'
    caminho.write_text(json.dumps(regioes))
    r = _filho(_REPLAY, [caminho], limite)
    return dict(requested=len(regioes), outcome=r['outcome'], wall_s=r['wall_s'], **(r['lines'][0] if r['lines'] else {}))


def resumo_layout(regioes):
    contiguas = sum(1 for (a, n, p), (b, _, q) in zip(regioes, regioes[1:]) if a + n == b and p == q)
    tamanhos = {}
    for _, n, _ in regioes:
        tamanhos[n] = tamanhos.get(n, 0) + 1
    return dict(regions=len(regioes), bytes=sum(n for _, n, _ in regioes),
                contiguous_same_permission_pairs=contiguas,
                coalesced_regions=len(regioes) - contiguas,
                commonest_sizes=sorted(tamanhos.items(), key=lambda kv: -kv[1])[:6])


def paginas_exibicao():
    """Sorted 4 KiB pages of the display post-load blocks (DGROUP excluded), as Economy's capture bench maps them."""
    sys.path.insert(0, str(RAIZ / 'pesquisas-paralelas/missoes'))
    import cenarios_oraculo as cen
    from mapa_memoria_m1 import carregar_blocos, carregar_json, expandir_captura
    captura = expandir_captura(carregar_json(cen.caminho('exibicao', 'captura_m1')),
                               carregar_json(cen.caminho('exibicao', 'entrada')))
    paginas = set()
    for nome, (inicio, dados) in carregar_blocos(captura['oracle']['final_state']['blocks']).items():
        if nome != 'dgroup':
            paginas.update(range(inicio & ~0xfff, (inicio + len(dados) + 0xfff) & ~0xfff, 0x1000))
    return sorted(paginas), len(captura['oracle']['final_state']['blocks'])


def coalescer(regioes):
    """Merge runs of contiguous regions with the same permissions (the layout ``mapear_coalescido`` would map)."""
    saida = []
    for base, n, p in regioes:
        if saida and saida[-1][0] + saida[-1][1] == base and saida[-1][2] == p:
            saida[-1][1] += n
        else:
            saida.append([base, n, p])
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--limite', type=int, default=LIMITE_S, help='seconds per child measurement')
    ap.add_argument('--sem-bancada', action='store_true', help='synthetic layouts only (no original executable)')
    a = ap.parse_args()
    saida = RAIZ / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    pasta = RAIZ / '.local/teardown'
    pasta.mkdir(parents=True, exist_ok=True)
    from emulador import unicorn
    rel = dict(schema='rising-lands/unicorn-teardown-measurement/1', unicorn=unicorn.__version__,
               python=platform.python_version(), machine=platform.machine(), bound_s=a.limite,
               method='each case runs in a child interpreter; close_s times the binding finalizer '
                      '(Uc.release_handle -> uc_close), the call interpreter shutdown makes; children leave '
                      'with os._exit')
    rel['synthetic'] = []
    for n in SINTETICO:
        r = _replay([[0x1000000 + 0x2000 * i, 0x1000, 7] for i in range(n)], pasta, f'synthetic-{n}', a.limite)
        rel['synthetic'].append(r)
        print(json.dumps(r), flush=True)
        if r['outcome'] != 'returned':
            break
    if not a.sem_bancada:
        layout = pasta / f'display-layout-{time.strftime("%Y%m%dT%H%M%S")}.json'
        r = _filho(_BANCADA, [layout], 3 * a.limite + 600)
        rel['display_bench'] = r
        print(json.dumps(r), flush=True)
        regioes = json.loads(layout.read_text())
        rel['display_layout'] = dict(path=str(layout.relative_to(RAIZ)), **resumo_layout(regioes))
        rel['display'] = []
        for n in sorted({len(regioes) * k // 8 for k in (1, 2, 4, 8)}):
            r = _replay(regioes[:n], pasta, f'display-{n}', a.limite)
            rel['display'].append(r)
            print(json.dumps(r), flush=True)
            if r['outcome'] != 'returned':
                break
        r = _replay(coalescer(regioes), pasta, 'display-coalesced', a.limite)
        rel['display_coalesced'] = r
        print(json.dumps(r), flush=True)
        paginas, nblocos = paginas_exibicao()
        por_pagina = [[p, 0x1000, 7] for p in paginas]
        rel['display_pages_layout'] = dict(blocks=nblocos, **resumo_layout(por_pagina))
        rel['display_pages'] = []
        for n in (1000, 2000, 4000, 8000, len(por_pagina)):
            r = _replay(por_pagina[:n], pasta, f'display-pages-{n}', a.limite)
            rel['display_pages'].append(r)
            print(json.dumps(r), flush=True)
            if r['outcome'] != 'returned':
                break
        r = _replay(coalescer(por_pagina), pasta, 'display-pages-coalesced', a.limite)
        rel['display_pages_coalesced'] = r
        print(json.dumps(r), flush=True)
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(rel, f, indent=1, sort_keys=True)
        f.write('\n')
    print(saida)
    return 0


if __name__ == '__main__':
    sys.exit(main())
