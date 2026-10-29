"""Native differential of the M3.1 input-path translation (``entrada_ordens_ia``) against its original capture.

Reruns the original-first capture (``capturar_entrada_ordens_ia``: Core's frame-1 ProcessInputGame pause and the
same declared cases) and, after each native leaf call, runs the translation over a copy of the exact case-entry
state (every DGROUP/thread/allocation block, as Core's ``MemoriaQuadro``) with the committed owners as providers
(``provedores_entrada_ia``). Per case it compares:
- the native run against the committed capture (registers, stores, changed bytes, calls, boundaries, keys);
- the exit registers EAX..EBP (InputGame's EAX and the single-unit CalculIconeAction's EAX are the leftovers of
  the rain routine and IconeFillContenu, which CalculGame discards: 0x42d340 reloads EAX, 0x42d3f0 does not read
  it; they are not compared);
- the changed bytes of the whole mapped state;
- the sound-library requests (PlaySnd_PostSound/PlaySnd_StopSound) against the native boundary events;
- the GetAsyncKeyState answers consumed against the native declared answers.

Declared inputs handed to the translation, exactly as the bench answered them: the case's key answers (0 when
none, the frame-phase answer), the bench's GetCursorPos answer and, for InitInputPlayer only, the pointers the
native GlobalAlloc+GlobalLock returned inside MemAlloc (the arena is the bench's declared binding). A case that stops at a named dependency is
reported with its dependency (never as equal).

A passing full run also writes ``evidencias/leituras-entrada-ordens-ia.json.xz``: the case-entry bytes each native
leaf call read and the original value of every byte the translation read or wrote (all from the original
case-entry states), as one ``base`` (the union, first recorded value) plus each case's differing bytes, the
inputs of the CPU-free replay in ``testes/test_entrada_ordens_ia.py``.

    python3 -B pesquisas-paralelas/ia-runtime/validar_entrada_ordens_ia.py
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

CAPTURA = AQUI / 'evidencias/captura-entrada-ordens-ia.json'
LEITURAS = AQUI / 'evidencias/leituras-entrada-ordens-ia.json.xz'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
FONTES = ('pesquisas-paralelas/ia-runtime/entrada_ordens_ia.py', 'pesquisas-paralelas/ia-runtime/provedores_entrada_ia.py',
          'pesquisas-paralelas/ia-runtime/validar_entrada_ordens_ia.py',
          'pesquisas-paralelas/ia-runtime/capturar_entrada_ordens_ia.py',
          'pesquisas-paralelas/ia-runtime/casos_entrada_ordens_ia.py', 'ferramentas/selecao_ordens.py',
          'pesquisas-paralelas/economia/ordens_economia.py', 'pesquisas-paralelas/combate/ataque_vivo.py',
          'pesquisas-paralelas/combate/alvos_alcance.py', 'pesquisas-paralelas/economia/extracao.py')


class Janelas:
    """The declared answers of one case: ordered keys (or 0), the bench cursor."""
    def __init__(self, teclas, cursor):
        self.teclas, self.cursor_xy, self.consumidas = [tuple(k) for k in teclas], tuple(cursor), []

    def tecla(self, vk, local=None):
        if not self.teclas:
            return 0
        if self.teclas[0][0] != vk:
            raise ValueError(f'GetAsyncKeyState(0x{vk:x}) is not the next declared key answer {self.teclas[0]}')
        _, valor = self.teclas.pop(0)
        self.consumidas.append([vk, valor])
        return valor & 0xffff

    def cursor(self):
        return self.cursor_xy


class LeiturasMemoria:
    """Wraps a memory and records the original value of every byte read or written through
    u8/u16/u32/vista/ler (the case-entry state of every byte the translation touches)."""
    def __init__(self, m):
        self.m, self.lidos, self.escritos = m, {}, set()

    def _ler(self, a, n):
        for i in range(n):
            if a + i not in self.escritos and a + i not in self.lidos:
                self.lidos[a + i] = self.m.u8(a + i)

    def _acesso(self, n, a, v):
        if v is None:
            self._ler(a, n)
            return getattr(self.m, f'u{8 * n}')(a)
        self._ler(a, n)
        self.escritos.update(range(a, a + n))
        return getattr(self.m, f'u{8 * n}')(a, v)

    def u8(self, a, v=None):
        return self._acesso(1, a, v)

    def u16(self, a, v=None):
        return self._acesso(2, a, v)

    def u32(self, a, v=None):
        return self._acesso(4, a, v)

    def vista(self, a, n):
        self._ler(a, n)                             # the pre-state of the whole range, then treated as written
        self.escritos.update(range(a, a + n))
        return self.m.vista(a, n)

    def ler(self, a, n):
        self._ler(a, n)
        return self.m.ler(a, n)


def comandos_imagem():
    from inventario_ia_runtime import OriginalImage
    from entrada_ordens_ia import TABELA_COMANDOS
    return OriginalImage().table(TABELA_COMANDOS, 40)


def executar_traducao(m, caso, entrada, cursor, alocacoes, comandos):
    """Run the translation of ``caso`` over memory ``m``; returns (exit registers, sound requests, keys)."""
    from entrada_ordens_ia import Entrada
    from provedores_entrada_ia import provedores_vivos
    pedidos = []

    def som(nome, regs, pilha):
        pedidos.append(dict(routine=nome, registers={k: hex(v) for k, v in regs.items()}, stack=[hex(v) for v in pilha]))
        return regs['EAX']
    janelas = Janelas(caso.get('keys', ()), cursor)
    fila = list(alocacoes)
    e = Entrada(m, provedores_vivos(m, janelas=janelas, som=som, alocar=lambda flags, tamanho: fila.pop(0)))
    e.comandos = comandos
    r = dict(entrada)
    nome = caso['routine']
    if nome == 'InputGame':
        e.input_game(r['EAX'])
        saida = dict(r, EAX=None)
    elif nome == 'ProcessInputGame':
        saida = e.process_input_game(r)
    elif nome == 'CalculIconeAction':
        saida = e.calcul_icone_action(r)
    elif nome in ('SetPlayerOrdre', 'WndProc'):
        saida = {'SetPlayerOrdre': e.set_player_ordre, 'WndProc': e.wnd_proc}[nome](r, caso['stack'])
    elif nome in ('BagGetCode', 'BagGetType', 'EnginGetBagOrdre'):
        saida = e.bag_regs(nome, r)
    else:
        saida = {'MouseZone': e.mouse_zone_regs, 'MouseEstDeplacer': e.mouse_est_deplacer,
                 'KeyPressed': e.key_pressed, 'KeyUnPressed': e.key_unpressed, 'KeyTestRelease': e.key_test_release,
                 'IconeGetZone': e.icone_get_zone_regs, 'GrabAllInput': e.grab_all_input,
                 'InitInputPlayer': e.init_input_player, 'MiniMapGetCase': e.mini_map_get_case,
                 'MiniMapGetCenterSelect': e.mini_map_get_center_select}[nome](r)
    if janelas.teclas:
        raise ValueError(f'declared key answers left unconsumed: {janelas.teclas}')
    return saida, pedidos, janelas.consumidas


def fronteiras_nativas(nativo):
    return [dict(routine=b['routine'], registers={k: hex(int(v, 16)) for k, v in b['registers'].items()},
                 stack=b['stack_words'][:1] if b['routine'] == 'PlaySnd_PostSound' else [])
            for b in nativo['boundaries']]


def comparar_resultado(caso, nativo, saida, pedidos, teclas, mudancas_py):
    """One comparison record from the translation's outputs and the native result."""
    regs_nativos = {k: int(nativo['exit_registers'][k], 16) for k in REGISTROS}
    dif = {k: [hex(saida[k]), hex(regs_nativos[k])] for k in REGISTROS
           if saida.get(k) is not None and saida[k] & 0xffffffff != regs_nativos[k]}
    for p in pedidos:
        if p['routine'] == 'PlaySnd_StopSound':
            p['stack'] = []
        elif p['routine'] == 'PlaySnd_PostSound':
            p['stack'] = p['stack'][:1]
    nat_f = fronteiras_nativas(nativo)
    nat_teclas = [[c[1], c[2]] for c in nativo['declared_keys_consumed']]
    r = dict(case=caso['case'], routine=caso['routine'], register_differences=dif,
             changed_equal=mudancas_py == nativo['changed_bytes'], boundaries_equal=pedidos == nat_f,
             keys_equal=teclas == nat_teclas, native_changed=len(nativo['changed_bytes']), boundaries=len(pedidos),
             excluded_registers=[k for k in REGISTROS if saida.get(k) is None])
    r['ok'] = not dif and r['changed_equal'] and r['boundaries_equal'] and r['keys_equal']
    if not r['changed_equal']:
        py, nat = {x[0]: x for x in mudancas_py}, {x[0]: x for x in nativo['changed_bytes']}
        r['changed_differences'] = sorted(([a, py.get(a), nat.get(a)] for a in set(py) | set(nat)
                                           if py.get(a) != nat.get(a)), key=lambda x: int(x[0], 16))[:24]
    if not r['boundaries_equal']:
        r.update(python_boundaries=pedidos, native_boundaries=nat_f)
    if not r['keys_equal']:
        r.update(python_keys=teclas, native_keys=nat_teclas)
    return r


def comparar(caso, antes, nativo, referencia, cursor, comandos):
    """One comparison record over a copy of the case-entry blocks (plus the bytes the translation read)."""
    from reinicio_ia import DependenciaIA
    from validar_selecao_ordens import memoria_de, mudancas
    m, copias = memoria_de(antes)
    lm = LeiturasMemoria(m)
    entrada = {k: int(nativo['entry_registers'][k], 16) for k in REGISTROS}
    alocacoes = [int(c.split('|')[4], 16) for c in nativo['calls'] if c.split('|')[1] == 'MemAlloc']
    iguais = referencia is not None and all(referencia[k] == nativo[k] for k in (
        'exit_registers', 'entry_registers', 'changed_bytes', 'stores', 'calls', 'boundaries', 'reached_return',
        'declared_keys_consumed'))
    try:
        saida, pedidos, teclas = executar_traducao(lm, caso, entrada, cursor, alocacoes, comandos)
    except DependenciaIA as erro:
        return dict(case=caso['case'], routine=caso['routine'], ok=False, native_equals_capture=iguais,
                    dependency=str(erro), python_reads=lm.lidos), None
    except Exception as erro:                       # recorded as a mismatch, never ignored
        return dict(case=caso['case'], routine=caso['routine'], ok=False, native_equals_capture=iguais,
                    python_error=f'{type(erro).__name__}: {erro}'), None
    r = comparar_resultado(caso, nativo, saida, pedidos, teclas, mudancas(antes, copias))
    r['native_equals_capture'] = iguais
    r['ok'] = r['ok'] and iguais
    return r, lm.lidos


def main():
    import capturar_entrada_ordens_ia as cap
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', default='pesquisas-paralelas/ia-runtime/validacao/entrada-ordens-native.json')
    ap.add_argument('--casos', type=int, help='first N cases only (smoke run, output under .local/)')
    ap.add_argument('--nucleo-ref', help='directory holding Core\'s construcao_core.py (a read-only extraction of '
                                         'its committed branch while it is not on main; recorded in the report)')
    a = ap.parse_args()
    nucleo_ref = None
    if a.nucleo_ref:
        caminho = (ROOT / a.nucleo_ref) if not Path(a.nucleo_ref).is_absolute() else Path(a.nucleo_ref)
        sys.path.append(str(caminho))
        nucleo_ref = dict(path=a.nucleo_ref, construcao_core_sha256=hashlib.sha256(
            (caminho / 'construcao_core.py').read_bytes()).hexdigest())
    saida = ROOT / a.saida
    if a.casos is not None and not a.saida.startswith('.local/'):
        raise SystemExit('A --casos smoke run writes under .local/ only')
    captura = json.loads(CAPTURA.read_bytes())
    por_nome = {c['case']: c for c in captura['cases']}
    comandos = comandos_imagem()
    registros, leituras_py = [], {}
    estado = {}

    def observador(caso, antes, resultado):
        nativo = dict(resultado, calls=[cap.chamada_compacta(c) for c in resultado['calls']])
        r, lidos = comparar(caso, antes, nativo, por_nome.get(caso['case']), estado['cursor'], comandos)
        registros.append(r)
        leituras_py[caso['case']] = lidos or r.pop('python_reads', {}) or {}
        print(f"{r['case']}: {'ok' if r['ok'] else 'MISMATCH ' + json.dumps({k: v for k, v in r.items() if k not in ('case', 'routine')})[:600]}",
              file=sys.stderr, flush=True)

    import bancada_selecao_ordens as bso
    teclas = cap.Teclas()

    def casos(b):
        estado['cursor'] = tuple(b.windows.quadro.cursor)
        return teclas.preparar(b, cap.casos_da_bancada(b)[:a.casos])

    def observar(caso, antes, resultado):
        resultado['declared_keys_consumed'] = teclas.depois(caso)
        observador(caso, antes, resultado)
    t0 = time.monotonic()
    b, lista, resultados, reproducao, pausa, segundos = bso.executar('exibicao', casos, observar, leituras=True)
    por_rotina = {}
    for r in registros:
        c = por_rotina.setdefault(r['routine'], dict(cases=0, equal=0, dependency_stops=0, mismatches=0))
        c['cases'] += 1
        c['equal' if r['ok'] else 'dependency_stops' if 'dependency' in r else 'mismatches'] += 1
    relatorio = dict(
        schema='rising-lands/monde01-input-orders-differential/1', original_sha256=HASH_ORIGINAL,
        capture=dict(path=str(CAPTURA.relative_to(ROOT)), sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in FONTES},
        path_reproduction=reproducao, pause=pausa, comparisons=len(registros),
        equal=sum(r['ok'] for r in registros),
        dependency_stops=[dict(case=r['case'], dependency=r['dependency']) for r in registros if 'dependency' in r],
        mismatches=[r for r in registros if not r['ok'] and 'dependency' not in r],
        by_routine=dict(sorted(por_rotina.items())),
        changed_bytes_compared=sum(r.get('native_changed', 0) for r in registros if r['ok']),
        boundary_requests_compared=sum(r.get('boundaries', 0) for r in registros if r['ok']),
        providers='provedores_entrada_ia.provedores_vivos (committed Core/Economy/Combat owners); sound requests '
                  'return the EAX they receive (the frame bench declaration for PlaySnd_*)',
        core_construction_reference=nucleo_ref, seconds=round(time.monotonic() - t0, 3))
    completo = a.casos is None and len(registros) == len(captura['cases'])
    ok = all(reproducao.values()) and not relatorio['mismatches'] and len(registros) == len(lista)
    if not ok:
        saida = ROOT / '.local/entrada' / f'entrada-ordens-falha-{time.strftime("%Y%m%dT%H%M%S")}.json'
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'w') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    evidencia = ok and completo and not a.saida.startswith('.local/')          # test runs never touch evidence
    destino_leituras = LEITURAS if evidencia else ROOT / '.local/entrada/leituras-entrada-ordens-ia.json.xz'
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
    escrever_leituras(destino_leituras, por_caso, dict(
        schema='rising-lands/monde01-input-orders-reads/2', original_sha256=HASH_ORIGINAL,
        capture=relatorio['capture'], cursor=list(estado['cursor']),
        label='case-entry bytes read by each native leaf call and the original value of every byte the '
              'translation read or wrote, recorded by the native differential run; base = union (first recorded '
              'value), cases = each case\'s bytes that differ from base'))
    print(json.dumps(dict(output=str(saida), comparisons=len(registros), equal=relatorio['equal'],
                          dependency_stops=len(relatorio['dependency_stops']), mismatches=len(relatorio['mismatches']),
                          reproduction=reproducao, seconds=relatorio['seconds']), indent=1))
    encerrar_captura(0 if ok else 2, saida, destino_leituras)


def escrever_leituras(destino, por_caso, cabecalho):
    import lzma
    base = {}
    for bytes_ in por_caso.values():
        for a, v in bytes_.items():
            base.setdefault(a, v)
    casos = {nome: _runs({a: v for a, v in bytes_.items() if base[a] != v}) for nome, bytes_ in por_caso.items()}
    texto = json.dumps(dict(cabecalho, base=_runs(base), cases=casos), indent=None, sort_keys=True,
                       separators=(',', ':')) + '\n'
    Path(destino).write_bytes(lzma.compress(texto.encode(), preset=9))


def _runs(bytes_):
    runs = []
    for a in sorted(bytes_):
        if runs and runs[-1][0] + len(runs[-1][1]) // 2 == a:
            runs[-1][1] += f'{bytes_[a]:02x}'
        else:
            runs.append([a, f'{bytes_[a]:02x}'])
    return [[hex(a), v] for a, v in runs]


if __name__ == '__main__':
    main()
