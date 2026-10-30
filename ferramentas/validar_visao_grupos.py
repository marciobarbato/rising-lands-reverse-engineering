"""Native differential of the structure vision, group selection, minimap view and exit-position translations
(M3.1 round 2).

Reruns the original-first capture (``capturar_visao_grupos``: same bench, preparations, cases and windows) and,
after each native measured step, runs ``visao_grupos`` over a copy of the exact step-entry state (every
DGROUP/thread/allocation block, as a ``MemoriaQuadro``). Per step it compares:
- the native run against the committed capture (registers, stores, changed bytes, calls, boundary events);
- the Python exit registers EAX..EBP against the native ones, except the bits a result marks in ``_incertos``
  (counted and reported per step);
- the Python changed bytes of the whole mapped state against the native ones;
- the sound-library requests (``som``) against the native boundary events.

Providers used for the comparison (the translation defaults none): ``som`` returns the EAX it receives (the accepted
frame bench's declaration for PlaySnd_*), each request recorded and compared. No other front's callee is reached.
A passing full run also writes the bytes each native step read before writing (``leituras-...``), the inputs of the
CPU-free replay in ``testes/test_visao_grupos.py``.

    python3 -B ferramentas/validar_visao_grupos.py
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
CAPTURA = RAIZ / 'evidencias/visao-grupos/captura-visao-grupos-exibicao.json.xz'
LEITURAS = RAIZ / 'evidencias/visao-grupos/leituras-visao-grupos-exibicao.json.xz'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
# Declared domain stops: the translation must raise ForaDoDominioEntrada at exactly this original address.
PARADAS_DECLARADAS = {}
FONTES = ('ferramentas/visao_grupos.py', 'ferramentas/validar_visao_grupos.py',
          'ferramentas/capturar_visao_grupos.py', 'ferramentas/bancada_entrada_estruturas.py',
          'ferramentas/casos_visao_grupos.py', 'ferramentas/selecao_ordens.py')


def carregar_captura():
    return json.loads(lzma.decompress(CAPTURA.read_bytes()))


def memoria_de(blocos):
    """A writable ``MemoriaQuadro`` over copies of the step-entry blocks (native stack excluded)."""
    from memoria_quadro_core import MemoriaQuadro
    copias = {n: (base, bytearray(dados)) for n, (base, dados) in blocos.items() if n != 'native_stack'}
    return MemoriaQuadro(copias.values()), copias


def mudancas(blocos, copias):
    saida = []
    for nome, (base, novo) in copias.items():
        velho = blocos[nome][1]
        if novo != velho:
            saida += [[hex(base + i), velho[i], novo[i]] for i in range(len(velho)) if velho[i] != novo[i]]
    return sorted(saida, key=lambda x: int(x[0], 16))


M32 = 0xffffffff


def comparar(passo, antes, resultado, referencia):
    """One comparison record (``ok`` plus the differences) for a native measured step ``resultado``."""
    from capturar_visao_grupos import chamada_compacta
    from visao_grupos import VisaoGrupos
    compacto = dict(resultado, calls=[chamada_compacta(c) for c in resultado['calls']])
    m, copias = memoria_de(antes)
    pedidos = []

    def som(nome, regs, pilha):
        pedidos.append(dict(routine=nome, registers={k: hex(v) for k, v in regs.items()},
                            stack=[hex(v) for v in pilha]))
        return regs['EAX']
    t = VisaoGrupos(m, som=som)
    entrada = {k: int(resultado['entry_registers'][k], 16) for k in REGISTROS}
    registro = dict(case=resultado['case'], routine=resultado['routine'])
    iguais_captura = referencia is not None and all(referencia[k] == compacto[k] for k in (
        'exit_registers', 'entry_registers', 'changed_bytes', 'stores', 'calls', 'boundaries', 'reached_return'))
    registro['native_equals_capture'] = iguais_captura
    try:
        saida = t.chamar(resultado['routine'], entrada, passo.get('stack', ()))
    except Exception as erro:                    # recorded as a mismatch, never ignored
        from visao_grupos import ForaDoDominioVisao
        declarada = PARADAS_DECLARADAS.get(resultado['case'])
        parada = isinstance(erro, ForaDoDominioVisao) and declarada is not None and erro.endereco == declarada
        registro.update(ok=parada and iguais_captura, python_error=f'{type(erro).__name__}: {erro}',
                        declared_domain_stop=hex(declarada) if parada else None)
        return registro
    incertos = saida.get('_incertos') or {}
    regs_nativos = {k: int(resultado['exit_registers'][k], 16) for k in REGISTROS}
    dif_regs = {k: [hex(saida[k]), hex(regs_nativos[k])] for k in REGISTROS
                if (saida[k] ^ regs_nativos[k]) & ~incertos.get(k, 0) & M32}
    py_mud = mudancas(antes, copias)
    nativos_fronteira = [dict(routine=b['routine'], registers={k: hex(int(v, 16)) for k, v in b['registers'].items()},
                              stack=b['stack_words'][:1] if b['routine'] == 'PlaySnd_PostSound' else [])
                         for b in resultado['boundaries']]
    registro.update(
        ok=(not dif_regs and py_mud == resultado['changed_bytes'] and pedidos == nativos_fronteira and
            iguais_captura),
        register_differences=dif_regs, changed_equal=py_mud == resultado['changed_bytes'],
        boundaries_equal=pedidos == nativos_fronteira, native_changed=len(resultado['changed_bytes']),
        boundaries=len(pedidos), uncertain_bits={k: hex(v) for k, v in incertos.items() if v})
    if py_mud != resultado['changed_bytes']:
        py, na = {x[0]: x for x in py_mud}, {x[0]: x for x in resultado['changed_bytes']}
        registro.update(python_only=[py[a] for a in py if py[a] != na.get(a)][:16],
                        native_only=[na[a] for a in na if na[a] != py.get(a)][:16])
    if pedidos != nativos_fronteira:
        registro.update(python_boundaries=pedidos, native_boundaries=nativos_fronteira)
    return registro


def executar(nomes=None, limite=None):
    """Rerun natively and compare; returns (records, results, reproduction, pause, seconds, capture)."""
    import capturar_visao_grupos as cee
    captura = carregar_captura()
    por_nome = {c['case']: c for c in captura['cases']}
    registros = []

    def observador(caso, passo, antes, resultado):
        r = comparar(passo, antes, resultado, por_nome.get(resultado['case']))
        registros.append(r)
        print(f"{r['case']}: {'ok' if r['ok'] else 'MISMATCH'}", file=sys.stderr, flush=True)

    t0 = time.monotonic()
    b, casos, resultados, reproducao, pausa, segundos = cee.executar('exibicao', observador, leituras=True,
                                                                     nomes=nomes, limite=limite)
    return registros, resultados, reproducao, pausa, round(time.monotonic() - t0, 3), captura


def main():
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', default='relatorios/visao-grupos-emulada.json')
    ap.add_argument('--nomes', nargs='*', help='only these cases (smoke run, output under .local/)')
    a = ap.parse_args()
    saida = RAIZ / a.saida
    if a.nomes and not a.saida.startswith('.local/'):
        raise SystemExit('A smoke run writes under .local/ only')
    registros, resultados, reproducao, pausa, segundos, captura = executar(nomes=set(a.nomes) if a.nomes else None)
    por_rotina = {}
    for r in registros:
        por_rotina.setdefault(r['routine'], [0, 0])
        por_rotina[r['routine']][0] += 1
        por_rotina[r['routine']][1] += not r['ok']
    relatorio = dict(
        schema='rising-lands/monde01-vision-groups-differential/1', original_sha256=HASH_ORIGINAL,
        capture=dict(path=str(CAPTURA.relative_to(RAIZ)), sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        path_reproduction=reproducao, pause=pausa, comparisons=len(registros),
        mismatches=[r for r in registros if not r['ok']],
        by_routine={k: dict(steps=v[0], mismatches=v[1]) for k, v in sorted(por_rotina.items())},
        changed_bytes_compared=sum(r.get('native_changed', 0) for r in registros),
        uncertain=[dict(case=r['case'], bits=r['uncertain_bits']) for r in registros if r.get('uncertain_bits')],
        providers=dict(som='returns the received EAX (the frame bench declaration for PlaySnd_*), compared'),
        declared_domain_stops=[dict(case=r['case'], address=r['declared_domain_stop']) for r in registros
                               if r.get('declared_domain_stop')],
        seconds=segundos)
    ok = (all(reproducao.values()) and not relatorio['mismatches'] and
          (a.nomes or len(registros) == len(captura['cases'])))
    if not ok:
        saida = RAIZ / '.local/visao-grupos' / f'visao-grupos-falha-{time.strftime("%Y%m%dT%H%M%S")}.json'
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'w') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    escritos = []
    if ok and not a.nomes:
        with lzma.open(LEITURAS, 'wt') as f:
            json.dump(dict(schema='rising-lands/monde01-vision-groups-reads/1', original_sha256=HASH_ORIGINAL,
                           capture=relatorio['capture'],
                           label='bytes each native measured step read before writing (stack excluded), recorded '
                                 'by the native differential run of the same cases',
                           cases={r['case']: r['read_before_write'] for r in resultados}),
                      f, indent=None, sort_keys=True, separators=(',', ':'))
            f.write('\n')
        escritos.append(LEITURAS)
    print(json.dumps(dict(output=str(saida), comparisons=len(registros), mismatches=len(relatorio['mismatches']),
                          by_routine=relatorio['by_routine'], reproduction=reproducao, seconds=segundos), indent=1))
    encerrar_captura(0 if ok else 2, saida, *escritos)


if __name__ == '__main__':
    main()
