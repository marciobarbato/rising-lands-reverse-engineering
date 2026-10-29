"""Native differential of the Core construction translations (M3 groundwork, Economy's build path).

Reruns the original-first capture (``capturar_construcao_core``: the selection-orders bench, pause and
declared cases) and, after each native leaf call, runs ``construcao_core`` over a copy of the exact
case-entry state (every DGROUP/thread/allocation block, as a ``MemoriaQuadro``). Per case it compares:
- the native run against the committed capture (registers, stores, changed bytes, calls and boundary
  events: the original is deterministic);
- the Python exit registers EAX..EBP against the native ones, except the bits a result marks in
  ``_incertos`` (DeplaceEngin's EAX through deep callees; counted and reported per case);
- the Python changed bytes of the whole mapped state against the native ones.
A passing full run also writes the bytes each native case read before writing
(``evidencias/construcao-core/leituras-construcao-core-exibicao.json``), the inputs of the CPU-free
replay in ``testes/test_construcao_core.py``.

Provider used for the comparison (the translation itself defaults none): ``bonus`` is Economy's committed
``bonus_unidades.BonusUnidades`` over the live bonus table 0x4dfba0 and unit-type table 0x4965ae.

    python3 -B ferramentas/validar_construcao_core.py
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
CAPTURA = RAIZ / 'evidencias/construcao-core/captura-construcao-core-exibicao.json'
LEITURAS = RAIZ / 'evidencias/construcao-core/leituras-construcao-core-exibicao.json'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
FONTES = ('ferramentas/construcao_core.py', 'ferramentas/validar_construcao_core.py',
          'ferramentas/capturar_construcao_core.py', 'ferramentas/bancada_selecao_ordens.py',
          'ferramentas/casos_construcao_core.py')


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


def bonus_economia(m):
    """Economy's BonusGetValEngin over the live tables of ``m`` (``bonus(jogador, tipo, seletor) -> EAX``)."""
    sys.path.insert(0, str(RAIZ))
    from integracao.providers import load_economy_bonus
    from mundo_vivo import vista_de
    tabela = load_economy_bonus().BonusUnidades.vivo(bytearray(vista_de(m, 0x4dfba0, 1872)),
                                                     tipos_unidades=bytearray(vista_de(m, 0x4965ae, 1300)))
    return lambda jogador, tipo, seletor: tabela.consultar(jogador, tipo, seletor)


def comparar(caso, antes, nativo, referencia):
    """One comparison record (``ok`` plus the differences)."""
    from construcao_core import ConstrucaoCore
    m, copias = memoria_de(antes)
    t = ConstrucaoCore(m, bonus=bonus_economia(m))
    entrada = {k: int(nativo['entry_registers'][k], 16) for k in REGISTROS}
    registro = dict(case=caso['case'], routine=caso['routine'])
    try:
        saida = t.chamar(caso['routine'], entrada, caso.get('stack', ()))
    except Exception as erro:                    # recorded as a mismatch, never ignored
        registro.update(ok=False, python_error=f'{type(erro).__name__}: {erro}')
        return registro
    incertos = saida.get('_incertos') or {}
    regs_nativos = {k: int(nativo['exit_registers'][k], 16) for k in REGISTROS}
    dif_regs = {k: [hex(saida[k]), hex(regs_nativos[k])] for k in REGISTROS
                if (saida[k] ^ regs_nativos[k]) & ~incertos.get(k, 0) & 0xffffffff}
    py_mud = mudancas(antes, copias)
    iguais_captura = referencia is not None and all(referencia[k] == nativo[k] for k in (
        'exit_registers', 'entry_registers', 'changed_bytes', 'stores', 'calls', 'boundaries', 'reached_return'))
    registro.update(
        ok=not dif_regs and py_mud == nativo['changed_bytes'] and not nativo['boundaries'] and iguais_captura,
        native_equals_capture=iguais_captura, register_differences=dif_regs,
        changed_equal=py_mud == nativo['changed_bytes'], native_changed=len(nativo['changed_bytes']),
        uncertain_bits={k: hex(v) for k, v in incertos.items()})
    if py_mud != nativo['changed_bytes']:
        registro.update(python_changed=py_mud[:24], native_changed_bytes=nativo['changed_bytes'][:24])
    return registro


def main():
    import capturar_construcao_core as ccc
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', default='relatorios/construcao-core-emulada.json')
    ap.add_argument('--casos', type=int, help='first N cases only (smoke run, output under .local/)')
    a = ap.parse_args()
    saida = RAIZ / a.saida
    if a.casos is not None and not a.saida.startswith('.local/'):
        raise SystemExit('A --casos smoke run writes under .local/ only')
    captura = json.loads(CAPTURA.read_bytes())
    por_nome = {c['case']: c for c in captura['cases']}
    registros = []

    def observador(caso, antes, resultado):
        nativo = dict(resultado, calls=[ccc.chamada_compacta(c) for c in resultado['calls']])
        registros.append(comparar(caso, antes, nativo, por_nome.get(caso['case'])))
        r = registros[-1]
        print(f"{r['case']}: {'ok' if r['ok'] else 'MISMATCH'}", file=sys.stderr, flush=True)

    t0 = time.monotonic()
    b, casos, resultados, reproducao, pausa, segundos = ccc.executar('exibicao', observador, a.casos, leituras=True)
    por_rotina = {}
    for r in registros:
        por_rotina.setdefault(r['routine'], [0, 0])
        por_rotina[r['routine']][0] += 1
        por_rotina[r['routine']][1] += not r['ok']
    relatorio = dict(
        schema='rising-lands/monde01-construction-core-differential/1', original_sha256=HASH_ORIGINAL,
        capture=dict(path=str(CAPTURA.relative_to(RAIZ)), sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        path_reproduction=reproducao, pause=pausa, comparisons=len(registros),
        mismatches=[r for r in registros if not r['ok']],
        by_routine={k: dict(cases=v[0], mismatches=v[1]) for k, v in sorted(por_rotina.items())},
        changed_bytes_compared=sum(r.get('native_changed', 0) for r in registros),
        uncertain=[dict(case=r['case'], bits=r['uncertain_bits']) for r in registros if r.get('uncertain_bits')],
        providers=dict(bonus='Economy bonus_unidades.BonusUnidades over the live tables 0x4dfba0/0x4965ae'),
        seconds=round(time.monotonic() - t0, 3))
    ok = all(reproducao.values()) and not relatorio['mismatches'] and len(registros) == len(captura['cases'][:a.casos])
    if not ok:
        saida = RAIZ / '.local/construcao' / f'construcao-core-falha-{time.strftime("%Y%m%dT%H%M%S")}.json'
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'w') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    if ok and a.casos is None:
        with open(LEITURAS, 'w') as f:
            json.dump(dict(schema='rising-lands/monde01-construction-core-reads/1', original_sha256=HASH_ORIGINAL,
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
