"""Native differential of the selection and order-setter translations (M3 groundwork).

Reruns the original-first capture (``capturar_selecao_ordens``: the same bench, pause and
declared cases) and, after each native leaf call, runs ``selecao_ordens`` over a copy of the
exact case-entry state (every DGROUP/thread/allocation block, as a ``MemoriaQuadro``). Per case
it compares:
- the native run against the committed capture (registers, stores, changed bytes, calls and
  boundary events: the original is deterministic);
- the Python exit registers EAX..EBP against the native ones;
- the Python changed bytes of the whole mapped state against the native ones;
- the sound-library requests the translation hands to its ``som`` provider against the native
  frame-boundary events (routine, EAX/EDX/EBX/ECX and the pushed volume).
A passing full run also writes the bytes each native case read before writing
(``evidencias/selecao-ordens/leituras-selecao-ordens-exibicao.json``), the inputs of the CPU-free
replay in ``testes/test_selecao_ordens.py``.

Providers used for the comparison (the translation itself defaults none):
- ``som`` returns the EAX it receives, the accepted frame bench's declaration for PlaySnd_*;
- ``definir_ataque`` is Combat's committed ``ataque_vivo.definir_ataque`` over the live unit
  records, with Core's ResetOrdre; its registers follow SetAttaqueEngin 0x445a36's bytes
  (EAX = 1 when the same order is already active, otherwise the unit type; EDX = the record).

    python3 -B ferramentas/validar_selecao_ordens.py
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
CAPTURA = RAIZ / 'evidencias/selecao-ordens/captura-selecao-ordens-exibicao.json'
LEITURAS = RAIZ / 'evidencias/selecao-ordens/leituras-selecao-ordens-exibicao.json'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
FONTES = ('ferramentas/selecao_ordens.py', 'ferramentas/validar_selecao_ordens.py',
          'ferramentas/capturar_selecao_ordens.py', 'ferramentas/bancada_selecao_ordens.py',
          'ferramentas/casos_selecao_ordens.py')


def memoria_de(blocos):
    """A writable ``MemoriaQuadro`` over copies of the case-entry blocks (native stack excluded)."""
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


def ataque_combate(m, traducao):
    """SetAttaqueEngin through Combat's committed translation over live records (see the module docstring)."""
    sys.path.insert(0, str(RAIZ / 'pesquisas-paralelas/combate'))
    from alvos_alcance import ordem_ja_definida
    from ataque_vivo import definir_ataque

    class Registros:
        def __getitem__(self, i):
            return m.vista(traducao._rec(i), 276)

    def provedor(unidade, modo, referencia):
        rec = traducao._rec(unidade)
        mesma = ordem_ja_definida(m.vista(rec, 276), modo, referencia)
        definir_ataque(Registros(), unidade, modo, referencia, lambda i: traducao.reset_ordre(dict(EAX=i)))
        return dict(EAX=1 if mesma else m.u8(rec + 1), EDX=rec)
    return provedor


def comparar(caso, antes, nativo, referencia):
    """One comparison record (``ok`` plus the differences)."""
    from selecao_ordens import SelecaoOrdens
    m, copias = memoria_de(antes)
    pedidos = []

    def som(nome, regs, pilha):
        pedidos.append(dict(routine=nome, registers={k: hex(v) for k, v in regs.items()},
                            stack=[hex(v) for v in pilha]))
        return regs['EAX']
    t = SelecaoOrdens(m, som=som)
    t.definir_ataque = ataque_combate(m, t)
    entrada = {k: int(nativo['entry_registers'][k], 16) for k in REGISTROS}
    registro = dict(case=caso['case'], routine=caso['routine'])
    try:
        saida = t.chamar(caso['routine'], entrada, caso.get('stack', ()))
    except Exception as erro:                    # recorded as a mismatch, never ignored
        registro.update(ok=False, python_error=f'{type(erro).__name__}: {erro}')
        return registro
    regs_nativos = {k: int(nativo['exit_registers'][k], 16) for k in REGISTROS}
    dif_regs = {k: [hex(saida[k]), hex(regs_nativos[k])] for k in REGISTROS if saida[k] & 0xffffffff != regs_nativos[k]}
    py_mud = mudancas(antes, copias)
    nativos_fronteira = [dict(routine=b['routine'], registers={k: hex(int(v, 16)) for k, v in b['registers'].items()},
                              stack=b['stack_words'][:1] if b['routine'] == 'PlaySnd_PostSound' else [])
                         for b in nativo['boundaries']]
    iguais_captura = referencia is not None and all(referencia[k] == nativo[k] for k in (
        'exit_registers', 'entry_registers', 'changed_bytes', 'stores', 'calls', 'boundaries', 'reached_return'))
    registro.update(
        ok=not dif_regs and py_mud == nativo['changed_bytes'] and pedidos == nativos_fronteira and iguais_captura,
        native_equals_capture=iguais_captura, register_differences=dif_regs,
        changed_equal=py_mud == nativo['changed_bytes'], boundaries_equal=pedidos == nativos_fronteira,
        native_changed=len(nativo['changed_bytes']), boundaries=len(pedidos))
    if py_mud != nativo['changed_bytes']:
        registro.update(python_changed=py_mud[:24], native_changed_bytes=nativo['changed_bytes'][:24])
    if pedidos != nativos_fronteira:
        registro.update(python_boundaries=pedidos, native_boundaries=nativos_fronteira)
    return registro


def main():
    import capturar_selecao_ordens as cso
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', default='relatorios/selecao-ordens-emulada.json')
    ap.add_argument('--casos', type=int, help='first N cases only (smoke run, output under .local/)')
    a = ap.parse_args()
    saida = RAIZ / a.saida
    if a.casos is not None and not a.saida.startswith('.local/'):
        raise SystemExit('A --casos smoke run writes under .local/ only')
    captura = json.loads(CAPTURA.read_bytes())
    por_nome = {c['case']: c for c in captura['cases']}
    registros = []

    def observador(caso, antes, resultado):
        nativo = dict(resultado, calls=[cso.chamada_compacta(c) for c in resultado['calls']])
        registros.append(comparar(caso, antes, nativo, por_nome.get(caso['case'])))
        r = registros[-1]
        print(f"{r['case']}: {'ok' if r['ok'] else 'MISMATCH'}", file=sys.stderr, flush=True)

    t0 = time.monotonic()
    b, casos, resultados, reproducao, pausa, segundos = cso.executar('exibicao', observador, a.casos, leituras=True)
    por_rotina = {}
    for r in registros:
        por_rotina.setdefault(r['routine'], [0, 0])
        por_rotina[r['routine']][0] += 1
        por_rotina[r['routine']][1] += not r['ok']
    relatorio = dict(
        schema='rising-lands/monde01-selection-orders-differential/1', original_sha256=HASH_ORIGINAL,
        capture=dict(path=str(CAPTURA.relative_to(RAIZ)), sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        path_reproduction=reproducao, pause=pausa, comparisons=len(registros),
        mismatches=[r for r in registros if not r['ok']],
        by_routine={k: dict(cases=v[0], mismatches=v[1]) for k, v in sorted(por_rotina.items())},
        boundary_requests_compared=sum(r.get('boundaries', 0) for r in registros),
        changed_bytes_compared=sum(r.get('native_changed', 0) for r in registros),
        providers=dict(som='returns the received EAX (the frame bench declaration for PlaySnd_*)',
                       definir_ataque='Combat ataque_vivo.definir_ataque with Core ResetOrdre'),
        seconds=round(time.monotonic() - t0, 3))
    ok = all(reproducao.values()) and not relatorio['mismatches'] and len(registros) == len(captura['cases'][:a.casos])
    if not ok:
        saida = RAIZ / '.local/selecao' / f'selecao-ordens-falha-{time.strftime("%Y%m%dT%H%M%S")}.json'
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'w') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    if ok and a.casos is None:
        # CPU-free replay inputs (testes/test_selecao_ordens.py): the bytes each native case read before writing.
        with open(LEITURAS, 'w') as f:
            json.dump(dict(schema='rising-lands/monde01-selection-orders-reads/1', original_sha256=HASH_ORIGINAL,
                           capture=relatorio['capture'],
                           label='bytes each native leaf call read before writing (stack excluded), recorded by '
                                 'the native differential run of the same cases',
                           cases={r['case']: r['read_before_write'] for r in resultados}),
                      f, indent=None, sort_keys=True, separators=(',', ':'))
            f.write('\n')
    print(json.dumps(dict(output=str(saida), comparisons=len(registros), mismatches=len(relatorio['mismatches']),
                          reproduction=reproducao, seconds=relatorio['seconds']), indent=1))
    encerrar_captura(0 if ok else 2, saida, *([LEITURAS] if ok and a.casos is None else []))


if __name__ == '__main__':
    main()
