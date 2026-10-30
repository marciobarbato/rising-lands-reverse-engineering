"""Native differential of M3.1 round 3 (InputGame's Ctrl deposit mode, help pages 9/0xc/0xb/2/7, page 8 over a
field or mine, the structure under the cursor with troops selected, and the selection/structure leaves of
``entrada_ordens_ia``) against ``evidencias/captura-paginas-deposito-ia.json``.

Reruns the original-first capture (``capturar_paginas_deposito_ia``: Core's frame-1 ProcessInputGame pause and
the same declared cases) and, after each native leaf call, runs the translation over a copy of the exact case-entry
state with the committed owners as providers (``provedores_entrada_ia.provedores_vivos``; Core's
``entrada_estruturas`` for EnginSelectPeutEntrer when ``--nucleo-ref`` adds its read-only extraction). Per case it compares, as ``validar_entrada_ordens_ia`` does: the native run against the
committed capture; the exit registers EAX..EBP (a register the translation returns as ``None`` is a value left
by a callee it does not reconstruct and is listed as excluded); the changed bytes of the whole mapped state; the
sound-library requests; the GetAsyncKeyState answers consumed. A named-dependency stop is reported with its
dependency, never as equal.

Leaf routines run ``entrada_ordens_ia.Entrada.chamar_folha``; InputGame's EAX is excluded as in rounds 1 and 2.
TextGetMessage is a display boundary of the bench (EAX 0, never executed); the translation binds it the same way
as the frame chain and the comparison checks its message number (EAX) only.

A passing full run also writes ``evidencias/leituras-paginas-deposito-ia.json.xz`` (the CPU-free replay inputs of
``testes/test_paginas_deposito_ia.py``).

    python3 -B pesquisas-paralelas/ia-runtime/validar_paginas_deposito_ia.py --nucleo-ref .local/entrada/nucleo-ref-r3
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))
from ambiente_ia_runtime import ROOT  # noqa: E402

CAPTURA = AQUI / 'evidencias/captura-paginas-deposito-ia.json'
LEITURAS = AQUI / 'evidencias/leituras-paginas-deposito-ia.json.xz'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
FONTES = ('pesquisas-paralelas/ia-runtime/entrada_ordens_ia.py', 'pesquisas-paralelas/ia-runtime/provedores_entrada_ia.py',
          'pesquisas-paralelas/ia-runtime/validar_paginas_deposito_ia.py',
          'pesquisas-paralelas/ia-runtime/capturar_paginas_deposito_ia.py',
          'pesquisas-paralelas/ia-runtime/casos_paginas_deposito_ia.py', 'ferramentas/selecao_ordens.py',
          'pesquisas-paralelas/economia/ordens_economia.py')


def executar_traducao(m, caso, entrada, cursor, comandos):
    """Run the translation of ``caso`` over memory ``m``; returns (exit registers, sound requests, keys)."""
    from entrada_ordens_ia import Entrada
    from provedores_entrada_ia import DonosM3, provedores_vivos
    from validar_entrada_ordens_ia import Janelas
    pedidos = []

    def som(nome, regs, pilha):
        pedidos.append(dict(routine=nome, registers={k: hex(v) for k, v in regs.items()}, stack=[hex(v) for v in pilha]))
        return regs['EAX']
    janelas = Janelas(caso.get('keys', ()), cursor)
    donos = DonosM3(m, som=som)
    vivos = provedores_vivos(m, janelas=janelas, som=som, estruturas=donos.ee, donos=donos)

    def texto(n, local):
        """TextGetMessage as the bench's display boundary (Missions' ``FRONTEIRAS_EXIBICAO``: EAX 0, body never
        executed), the same binding as the frame chain; logged with its message number."""
        pedidos.append(dict(routine='TextGetMessage', registers={'EAX': hex(n)}, stack=[]))
        return 0
    vivos.funcoes['TextGetMessage'] = texto
    e = Entrada(m, vivos)
    e.comandos = comandos
    r = dict(entrada)
    nome = caso['routine']
    if nome == 'InputGame':
        e.input_game(r['EAX'])
        saida = dict(r, EAX=None)
    else:
        saida = e.chamar_folha(nome, r)
    if janelas.teclas:
        raise ValueError(f'declared key answers left unconsumed: {janelas.teclas}')
    return saida, pedidos, janelas.consumidas


def texto_so_eax(nativo):
    """``nativo`` with each TextGetMessage boundary reduced to its EAX (the message number, the only register the
    routine reads); EBX/ECX/EDX there are InputGame's scratch values, not reconstructed and not consumed."""
    fronteiras = [dict(b, registers={'EAX': b['registers']['EAX']}) if b['routine'] == 'TextGetMessage' else b
                  for b in nativo['boundaries']]
    return dict(nativo, boundaries=fronteiras)


def comparar(caso, antes, nativo, referencia, cursor, comandos):
    """One comparison record over a copy of the case-entry blocks (plus the bytes the translation read)."""
    from reinicio_ia import DependenciaIA
    from validar_entrada_ordens_ia import LeiturasMemoria, comparar_resultado
    from validar_selecao_ordens import memoria_de, mudancas
    m, copias = memoria_de(antes)
    lm = LeiturasMemoria(m)
    entrada = {k: int(nativo['entry_registers'][k], 16) for k in REGISTROS}
    iguais = referencia is not None and all(referencia[k] == nativo[k] for k in (
        'exit_registers', 'entry_registers', 'changed_bytes', 'stores', 'calls', 'boundaries', 'reached_return',
        'declared_keys_consumed'))
    try:
        saida, pedidos, teclas = executar_traducao(lm, caso, entrada, cursor, comandos)
    except DependenciaIA as erro:
        return dict(case=caso['case'], routine=caso['routine'], ok=False, native_equals_capture=iguais,
                    dependency=str(erro), python_reads=lm.lidos), None
    except Exception as erro:                       # recorded as a mismatch, never ignored
        import traceback
        return dict(case=caso['case'], routine=caso['routine'], ok=False, native_equals_capture=iguais,
                    python_error=f'{type(erro).__name__}: {erro}', traceback=traceback.format_exc()[-1500:]), None
    r = comparar_resultado(caso, texto_so_eax(nativo), saida, pedidos, teclas, mudancas(antes, copias))
    r['native_equals_capture'] = iguais
    r['ok'] = r['ok'] and iguais
    return r, lm.lidos


def main():
    import capturar_paginas_deposito_ia as cap
    from capturar_entrada_ordens_ia import chamada_compacta, Teclas
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    from validar_entrada_ordens_ia import comandos_imagem, escrever_leituras
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', default='pesquisas-paralelas/ia-runtime/validacao/paginas-deposito-native.json')
    ap.add_argument('--casos', type=int, help='first N cases only (smoke run, output under .local/)')
    ap.add_argument('--nucleo-ref', help='directory holding Core\'s entrada_estruturas.py (a read-only extraction of '
                                         'its committed branch while it is not on main; recorded)')
    a = ap.parse_args()
    nucleo_ref = None
    if a.nucleo_ref:
        caminho = (ROOT / a.nucleo_ref) if not Path(a.nucleo_ref).is_absolute() else Path(a.nucleo_ref)
        sys.path.append(str(caminho))
        nucleo_ref = dict(path=a.nucleo_ref, entrada_estruturas_sha256=hashlib.sha256(
            (caminho / 'entrada_estruturas.py').read_bytes()).hexdigest())
    saida = ROOT / a.saida
    if a.casos is not None and not a.saida.startswith('.local/'):
        raise SystemExit('A --casos smoke run writes under .local/ only')
    captura = json.loads(CAPTURA.read_bytes())
    por_nome = {c['case']: c for c in captura['cases']}
    comandos = comandos_imagem()
    registros, leituras_py, estado = [], {}, {}
    teclas = Teclas()

    def casos(b):
        estado['cursor'] = tuple(b.windows.quadro.cursor)
        return teclas.preparar(b, cap.casos_da_bancada(b)[:a.casos])

    def observar(caso, antes, resultado):
        resultado['declared_keys_consumed'] = teclas.depois(caso)
        nativo = dict(resultado, calls=[chamada_compacta(c) for c in resultado['calls']])
        r, lidos = comparar(caso, antes, nativo, por_nome.get(caso['case']), estado['cursor'], comandos)
        registros.append(r)
        leituras_py[caso['case']] = lidos or r.pop('python_reads', {}) or {}
        print(f"{r['case']}: {'ok' if r['ok'] else 'MISMATCH ' + json.dumps({k: v for k, v in r.items() if k not in ('case', 'routine', 'python_reads')}, default=str)[:900]}",
              file=sys.stderr, flush=True)

    import bancada_selecao_ordens as bso
    t0 = time.monotonic()
    b, lista, resultados, reproducao, pausa, segundos = bso.executar('exibicao', casos, observar, leituras=True)
    por_rotina = {}
    for r in registros:
        c = por_rotina.setdefault(r['routine'], dict(cases=0, equal=0, dependency_stops=0, mismatches=0))
        c['cases'] += 1
        c['equal' if r['ok'] else 'dependency_stops' if 'dependency' in r else 'mismatches'] += 1
    relatorio = dict(
        schema='rising-lands/monde01-input-pages-deposit-differential/1', original_sha256=HASH_ORIGINAL,
        capture=dict(path=str(CAPTURA.relative_to(ROOT)), sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in FONTES},
        path_reproduction=reproducao, pause=pausa, comparisons=len(registros),
        equal=sum(r['ok'] for r in registros),
        dependency_stops=[dict(case=r['case'], dependency=r['dependency']) for r in registros if 'dependency' in r],
        mismatches=[r for r in registros if not r['ok'] and 'dependency' not in r],
        excluded_registers={r['case']: r['excluded_registers'] for r in registros
                            if r.get('ok') and r.get('excluded_registers')},
        by_routine=dict(sorted(por_rotina.items())),
        changed_bytes_compared=sum(r.get('native_changed', 0) for r in registros if r['ok']),
        boundary_requests_compared=sum(r.get('boundaries', 0) for r in registros if r['ok']),
        providers='provedores_entrada_ia.provedores_vivos (committed Core/Economy/Combat owners; Core '
                  'entrada_estruturas for EnginSelectPeutEntrer from --nucleo-ref); sound requests return the EAX '
                  'they receive (the frame bench declaration for PlaySnd_*)',
        core_structure_entry_reference=nucleo_ref, seconds=round(time.monotonic() - t0, 3))
    completo = a.casos is None and len(registros) == len(captura['cases'])
    ok = all(reproducao.values()) and not relatorio['mismatches'] and len(registros) == len(lista)
    if not ok:
        saida = ROOT / '.local/entrada' / f'paginas-deposito-falha-{time.strftime("%Y%m%dT%H%M%S")}.json'
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'w') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    evidencia = ok and completo and not a.saida.startswith('.local/')
    destino = LEITURAS if evidencia else ROOT / '.local/entrada/leituras-paginas-deposito-ia.json.xz'
    por_caso = {}
    for r in resultados:
        bytes_ = {}
        for inicio, dados in r['read_before_write']:
            base = int(inicio, 16)
            for i in range(len(dados) // 2):
                bytes_[base + i] = int(dados[2 * i:2 * i + 2], 16)
        for endereco, valor in leituras_py.get(r['case'], {}).items():
            bytes_.setdefault(endereco, valor)
        por_caso[r['case']] = bytes_
    escrever_leituras(destino, por_caso, dict(
        schema='rising-lands/monde01-input-pages-deposit-reads/1', original_sha256=HASH_ORIGINAL,
        capture=relatorio['capture'], cursor=list(estado['cursor']),
        label='case-entry bytes read by each native leaf call and the original value of every byte the '
              'translation read or wrote, recorded by the native differential run; base = union (first recorded '
              'value), cases = each case\'s bytes that differ from base'))
    print(json.dumps(dict(output=str(saida), comparisons=len(registros), equal=relatorio['equal'],
                          dependency_stops=len(relatorio['dependency_stops']), mismatches=len(relatorio['mismatches']),
                          reproduction=reproducao, seconds=relatorio['seconds']), indent=1))
    encerrar_captura(0 if ok else 2, saida, destino)


if __name__ == '__main__':
    main()
