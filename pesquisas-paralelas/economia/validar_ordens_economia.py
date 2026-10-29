"""Native differential of the economy order setters and construction gates (M3 groundwork).

Reruns the original-first capture (``capturar_ordens_economia``: same bench, pause and declared
cases) and, after each native leaf call, runs ``ordens_economia`` over a copy of the exact
case-entry state (every DGROUP/thread/allocation block, as a ``MemoriaQuadro``). Per case it
compares:
- the native run against the committed capture (registers, stores, changed bytes, calls and
  boundary events: the original is deterministic);
- the Python exit registers EAX..EBP and ESP against the native ones;
- the Python changed bytes of the whole mapped state against the native ones;
- every call into another front, in order: name and EAX/EDX/EBX/ECX at the callee entry against
  the native call (bits the original leaves as uninitialized frame bytes are masked, see
  ``ordens_economia``), and the sound requests against the native frame-boundary events.
Cases in ``FORA_DO_DOMINIO`` must raise ``ForaDoDominioOrdem`` at the declared address with no
store made.

Providers for the comparison (the translation itself defaults none):
- Core's committed ``selecao_ordens.SelecaoOrdens`` over the same memory for EnginEstVivant,
  ResetOrdre (Core's live navigation world), EnginAsk and BatimentGetDecalageConstruction
  (``ordens_economia.provedor_core``); its ``som`` returns the EAX it receives, the frame bench's
  declaration for PlaySnd_*;
- every other front's callee (DeplaceEngin, PlaceBatiment, BatimentConstructible,
  BatimentCollision, ResetCheminTerrainModify) is the original's own call replayed: the stores the
  original made inside that call (and its callees) in order, and its exit registers. It checks the
  translation's arguments and lets the economy code after it be compared; it is not a translation.

A passing full run also writes the bytes each native case read before writing
(``evidencias/ordens-economia/leituras-ordens-economia-exibicao.json``), the input of the CPU-free
replay in ``testes/test_ordens_economia.py``.

    python3 -B pesquisas-paralelas/economia/validar_ordens_economia.py
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
CAPTURA = PASTA / 'evidencias/ordens-economia/captura-ordens-economia-exibicao.json'
LEITURAS = PASTA / 'evidencias/ordens-economia/leituras-ordens-economia-exibicao.json'
RELATORIO = PASTA / 'validacao-ordens-economia-emulada.json'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP')
FONTES = ('pesquisas-paralelas/economia/ordens_economia.py', 'pesquisas-paralelas/economia/validar_ordens_economia.py',
          'pesquisas-paralelas/economia/capturar_ordens_economia.py',
          'pesquisas-paralelas/economia/bancada_ordens_economia.py',
          'pesquisas-paralelas/economia/casos_ordens_economia.py', 'ferramentas/selecao_ordens.py')
CORE = frozenset(('EnginEstVivant', 'ResetOrdre', 'EnginAsk', 'BatimentGetDecalageConstruction'))
REPRODUZIDAS = frozenset(('DeplaceEngin', 'PlaceBatiment', 'BatimentConstructible', 'BatimentCollision',
                          'ResetCheminTerrainModify'))
EXTERNAS = CORE | REPRODUZIDAS
FORA_DO_DOMINIO = {'build_tick_gate_type9': 0x44abbf, 'build_tick_state15': 0x44b15d,
                   'build_tick_progress_byte1': 0x44b1c1}


def chamadas(nativo):
    """Parsed native calls: dicts with depth, name, entry registers, exit registers (or None)."""
    saida = []
    for c in nativo['calls']:
        p, nome, regs, chamador, eax, fim = c.split('|')
        e = dict(zip(('EAX', 'EDX', 'EBX', 'ECX'), (int(x, 16) for x in regs.split(','))))
        s = dict(zip(('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP'), (int(x, 16) for x in fim.split(',')))) \
            if fim else None
        saida.append(dict(depth=int(p), name=nome, entry=e, exit=s, caller=chamador))
    return saida


def externas(lista):
    """[index, subtree indices] of each outermost call into another front, in call order."""
    pilha, saida = [], []                       # pilha: (depth, owning entry of ``saida`` or None)
    for i, c in enumerate(lista):
        while pilha and pilha[-1][0] >= c['depth']:
            pilha.pop()
        dono = next((e for _, e in reversed(pilha) if e is not None), None)
        if dono is not None:
            saida[dono][1].add(i)
        elif c['name'] in EXTERNAS:
            saida.append([i, {i}])
            dono = len(saida) - 1
        pilha.append((c['depth'], dono))
    return saida


def chamadores_reproduzidos(nativo):
    """Names of the routines inside replayed calls (their frame-boundary events are part of the replay)."""
    lista = chamadas(nativo)
    return {lista[j]['name'] for i, sub in externas(lista) if lista[i]['name'] in REPRODUZIDAS for j in sub}


class Reproducao:
    """Validator ``externo``: Core's translations for Core's leaf callees, the original's own call replayed
    for the other fronts; both checked against the native call sequence."""

    def __init__(self, m, nativo, core):
        from ordens_economia import provedor_core
        self.m, self.lista = m, chamadas(nativo)
        self.fila = externas(self.lista)
        self.lojas = nativo['stores']
        self.core = provedor_core(core)
        self.erros, self.pos, self.subarvores = [], 0, set()

    def __call__(self, nome, chamada, regs):
        if self.pos >= len(self.fila):
            self.erros.append(f'extra call {nome} at 0x{chamada:x}')
            raise RuntimeError(self.erros[-1])
        i, sub = self.fila[self.pos]
        self.pos += 1
        nat = self.lista[i]
        incertos = regs.get('_incertos') or {}
        dif = {k: [hex(regs[k]), hex(nat['entry'][k])] for k in ('EAX', 'EDX', 'EBX', 'ECX')
               if (regs[k] ^ nat['entry'][k]) & ~incertos.get(k, 0) & 0xffffffff}
        if nat['name'] != nome or dif:
            self.erros.append(dict(call=self.pos - 1, python=nome, native=nat['name'], at=hex(chamada), registers=dif))
            raise RuntimeError(f'call mismatch {self.erros[-1]}')
        if nome in CORE:
            return self.core(nome, chamada, regs)
        self.subarvores |= sub
        for loja in self.lojas:
            if loja[5] in sub:
                largura, valor = loja[3], int(loja[4], 16)
                getattr(self.m, {1: 'u8', 2: 'u16', 4: 'u32'}[largura])(int(loja[2], 16), valor)
        if nat['exit'] is None:
            raise RuntimeError(f'{nome} did not return natively')
        return dict(nat['exit'])

    def completo(self):
        return self.pos == len(self.fila)


class Gravadora:
    """Memory wrapper recording the final value of every byte the translation stores."""

    def __init__(self, m):
        self.m, self.finais = m, {}

    def vista(self, a, n):
        return self.m.vista(a, n)

    def _w(self, n, a, v):
        if v is None:
            return getattr(self.m, f'u{8 * n}')(a)
        v &= (1 << 8 * n) - 1
        for i in range(n):
            self.finais[(a + i) & 0xffffffff] = v >> 8 * i & 0xff
        return getattr(self.m, f'u{8 * n}')(a, v)

    def u8(self, a, v=None):
        return self._w(1, a, v)

    def u16(self, a, v=None):
        return self._w(2, a, v)

    def u32(self, a, v=None):
        return self._w(4, a, v)


def finais_nativos(nativo):
    finais = {}
    for loja in nativo['stores']:
        a, n, v = int(loja[2], 16), loja[3], int(loja[4], 16)
        for i in range(n):
            finais[(a + i) & 0xffffffff] = v >> 8 * i & 0xff
    return finais


def traduzir(caso, nativo, memoria):
    """Run the translation for ``caso`` over ``memoria`` (its entry state); returns (record, memory, exit
    registers or None). A case outside the domain must raise before any store: the caller compares the
    state change, which must then be empty."""
    from ordens_economia import ForaDoDominioOrdem, OrdensEconomia
    from selecao_ordens import SelecaoOrdens
    pedidos = []

    def som(nome, regs, pilha):
        pedidos.append(dict(routine=nome, registers={k: hex(v) for k, v in regs.items()},
                            stack=[hex(v) for v in pilha]))
        return regs['EAX']
    m = memoria
    rep = Reproducao(m, nativo, SelecaoOrdens(m, som=som))
    t = OrdensEconomia(m, externo=rep)
    entrada = {k: int(nativo['entry_registers'][k], 16) for k in REGISTROS}
    registro = dict(case=caso['case'], routine=caso['routine'])
    esperado = FORA_DO_DOMINIO.get(caso['case'])
    try:
        saida = t.chamar(caso['routine'], entrada, caso.get('stack', ()))
    except ForaDoDominioOrdem as erro:
        registro.update(ok=esperado == erro.endereco and rep.pos == 0, raised=f'0x{erro.endereco:x}')
        return registro, m, None
    except Exception as erro:                     # recorded as a mismatch, never ignored
        registro.update(ok=False, python_error=f'{type(erro).__name__}: {erro}', call_errors=rep.erros)
        return registro, m, None
    if esperado is not None:
        registro.update(ok=False, python_error=f'expected ForaDoDominioOrdem at 0x{esperado:x}')
        return registro, m, None
    regs_nativos = {k: int(nativo['exit_registers'][k], 16) for k in REGISTROS}
    dif_regs = {k: [hex(saida[k]), hex(regs_nativos[k])] for k in REGISTROS if saida[k] & 0xffffffff != regs_nativos[k]}
    nativos_fronteira = [dict(routine=b['routine'], registers={k: hex(int(v, 16)) for k, v in b['registers'].items()},
                              stack=b['stack_words'][:1] if b['routine'] == 'PlaySnd_PostSound' else [])
                         for b in nativo['boundaries'] if b['caller'] not in chamadores_reproduzidos(nativo)]
    registro.update(ok=not dif_regs and pedidos == nativos_fronteira and rep.completo(),
                    register_differences=dif_regs, boundaries_equal=pedidos == nativos_fronteira,
                    other_front_calls=rep.pos, all_calls_consumed=rep.completo(), boundaries=len(pedidos))
    if pedidos != nativos_fronteira:
        registro.update(python_boundaries=pedidos, native_boundaries=nativos_fronteira)
    return registro, m, saida


def memoria_de(blocos):
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


def comparar(caso, antes, nativo, referencia):
    """One comparison record (``ok`` plus the differences)."""
    m, copias = memoria_de(antes)
    registro, _, saida = traduzir(caso, nativo, m)
    iguais_captura = referencia is not None and all(referencia[k] == nativo[k] for k in (
        'exit_registers', 'entry_registers', 'changed_bytes', 'stores', 'calls', 'boundaries', 'reached_return'))
    registro['native_equals_capture'] = iguais_captura
    registro['native_changed'] = len(nativo['changed_bytes'])
    py_mud = mudancas(antes, copias)
    if saida is None and 'raised' in registro and py_mud:
        registro.update(ok=False, python_changed=py_mud[:24])
    if saida is not None:
        registro['changed_equal'] = py_mud == nativo['changed_bytes']
        if py_mud != nativo['changed_bytes']:
            registro.update(ok=False, python_changed=py_mud[:24], native_changed_bytes=nativo['changed_bytes'][:24])
    registro['ok'] = registro['ok'] and iguais_captura
    return registro


def main():
    import capturar_ordens_economia as coe
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', default=str(RELATORIO.relative_to(RAIZ)))
    ap.add_argument('--casos', type=int, help='first N cases only (smoke run, output under .local/)')
    a = ap.parse_args()
    saida = RAIZ / a.saida
    if a.casos is not None and not a.saida.startswith('.local/'):
        raise SystemExit('A --casos smoke run writes under .local/ only')
    captura = json.loads(CAPTURA.read_bytes())
    por_nome = {c['case']: c for c in captura['cases']}
    registros = []

    def observador(caso, antes, resultado):
        nativo = dict(resultado, calls=[coe.chamada_compacta(c) for c in resultado['calls']])
        registros.append(comparar(caso, antes, nativo, por_nome.get(caso['case'])))
        r = registros[-1]
        print(f"{r['case']}: {'ok' if r['ok'] else 'MISMATCH'}", file=sys.stderr, flush=True)

    t0 = time.monotonic()
    b, casos, resultados, reproducao, pausa, segundos = coe.executar('exibicao', observador, a.casos, leituras=True)
    por_rotina = {}
    for r in registros:
        por_rotina.setdefault(r['routine'], [0, 0])
        por_rotina[r['routine']][0] += 1
        por_rotina[r['routine']][1] += not r['ok']
    relatorio = dict(
        schema='rising-lands/monde01-economy-orders-differential/1', original_sha256=HASH_ORIGINAL,
        capture=dict(path=str(CAPTURA.relative_to(RAIZ)), sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        path_reproduction=reproducao, pause=pausa, comparisons=len(registros),
        mismatches=[r for r in registros if not r['ok']],
        by_routine={k: dict(cases=v[0], mismatches=v[1]) for k, v in sorted(por_rotina.items())},
        outside_domain=sorted(FORA_DO_DOMINIO),
        other_front_calls_compared=sum(r.get('other_front_calls', 0) for r in registros),
        boundary_requests_compared=sum(r.get('boundaries', 0) for r in registros),
        changed_bytes_compared=sum(r.get('native_changed', 0) for r in registros if 'raised' not in r),
        providers=dict(core='selecao_ordens.SelecaoOrdens via ordens_economia.provedor_core (EnginEstVivant, '
                            'ResetOrdre, EnginAsk, BatimentGetDecalageConstruction); som returns the received EAX',
                       other_fronts='the original call replayed (its stores and exit registers) after checking '
                                    'its name and EAX/EDX/EBX/ECX: ' + ', '.join(sorted(REPRODUZIDAS))),
        seconds=round(time.monotonic() - t0, 3))
    ok = all(reproducao.values()) and not relatorio['mismatches'] and len(registros) == len(captura['cases'][:a.casos])
    if not ok:
        saida = RAIZ / '.local/ordens-economia' / f'validacao-falha-{time.strftime("%Y%m%dT%H%M%S")}.json'
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'w') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    if ok and a.casos is None:
        with open(LEITURAS, 'w') as f:
            json.dump(dict(schema='rising-lands/monde01-economy-orders-reads/1', original_sha256=HASH_ORIGINAL,
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
