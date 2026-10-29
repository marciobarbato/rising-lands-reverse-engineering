"""Native differential of the structure-entry, lodging and Bag translations (M3/M4 groundwork).

Reruns the original-first capture (``capturar_entrada_estruturas``: same bench, preparations, cases and windows)
and, after each native measured step, runs ``entrada_estruturas`` over a copy of the exact step-entry state
(every DGROUP/thread/allocation block, as a ``MemoriaQuadro``). Per step it compares:
- the native run against the committed capture (registers, stores, changed bytes, calls, boundary events);
- the Python exit registers EAX..EBP against the native ones, except the bits a result marks in ``_incertos``
  (counted and reported per step);
- the Python changed bytes of the whole mapped state against the native ones;
- the sound-library requests (``som``) against the native boundary events.

Providers used for the comparison (the translation defaults none):
- ``bonus``: Economy's committed ``bonus_unidades.BonusUnidades`` over the live tables 0x4dfba0/0x4965ae;
- ``som``: returns the EAX it receives (the accepted frame bench's declaration for PlaySnd_*), each request
  recorded and compared;
- ``externo`` for other fronts' callees (BatimentLogeEngin, iagUnitSendMessage, PlayerInitPropositionAlliance):
  the original's own nested call replayed, as Economy's validators do. Its name and argument registers are
  checked against the native call, then the stores the original made inside it are applied in order and its
  exit registers returned. Validation scaffolding, not a translation.
A passing full run also writes the bytes each native step read before writing (``leituras-...``), the inputs of
the CPU-free replay in ``testes/test_entrada_estruturas.py``.

    python3 -B ferramentas/validar_entrada_estruturas.py
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import struct
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
CAPTURA = RAIZ / 'evidencias/entrada-estruturas/captura-entrada-estruturas-exibicao.json.xz'
LEITURAS = RAIZ / 'evidencias/entrada-estruturas/leituras-entrada-estruturas-exibicao.json.xz'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
ESTRANGEIRAS = ('BatimentLogeEngin', 'iagUnitSendMessage', 'PlayerInitPropositionAlliance', 'InitBatimentNeutre')
# Declared domain stops: the translation must raise ForaDoDominioEntrada at exactly this original address.
PARADAS_DECLARADAS = {'entre_unit_type_out_of_branch': 0x449c56}
FONTES = ('ferramentas/entrada_estruturas.py', 'ferramentas/validar_entrada_estruturas.py',
          'ferramentas/capturar_entrada_estruturas.py', 'ferramentas/bancada_entrada_estruturas.py',
          'ferramentas/casos_entrada_estruturas.py')


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


def bonus_economia(m):
    """Economy's BonusGetValEngin over the live tables of ``m`` (``bonus(jogador, tipo, seletor) -> EAX``)."""
    sys.path.insert(0, str(RAIZ))
    from integracao.providers import load_economy_bonus
    from mundo_vivo import vista_de
    tabela = load_economy_bonus().BonusUnidades.vivo(bytearray(vista_de(m, 0x4dfba0, 1872)),
                                                     tipos_unidades=bytearray(vista_de(m, 0x4965ae, 1300)))
    return lambda jogador, tipo, seletor: tabela.consultar(jogador, tipo, seletor)


def gravador_atribuido():
    """A ``Folhas`` recorder that also attributes each store to the innermost open nested call and keeps every
    nested call's full exit registers (for the replay of other fronts' callees)."""
    import bancada_selecao_ordens as bso
    from unicorn import x86_const as x86

    class FolhasAtribuidas(bso.Folhas):
        ultimo = None

        def armar(self, esp_inicial):
            self.atribuicao, self.saidas = [], {}
            FolhasAtribuidas.ultimo = self
            return super().armar(esp_inicial)

        def _bloco(self, cpu, endereco, tamanho, _):
            esp = cpu.reg_read(x86.UC_X86_REG_ESP)
            j = len(self.abertas) - 1
            while j >= 0 and endereco == self.abertas[j]['retorno'] and esp > self.abertas[j]['esp']:
                self.saidas[self.abertas[j]['indice']] = self._regs(cpu)
                j -= 1
            super()._bloco(cpu, endereco, tamanho, _)

        def _escrever(self, cpu, acesso, endereco, tamanho, valor, _):
            antes = len(self.escritas)
            super()._escrever(cpu, acesso, endereco, tamanho, valor, _)
            if len(self.escritas) > antes:
                self.atribuicao.append([a['indice'] for a in self.abertas])
    return FolhasAtribuidas


class Replay:
    """``externo`` serving another front's callee from the original's own nested call of this step."""

    def __init__(self, chamadas, escritas, atribuicao, saidas):
        self.chamadas, self.escritas, self.atribuicao, self.saidas = chamadas, escritas, atribuicao, saidas
        self.sequencia = []
        pilha = []
        for i, c in enumerate(chamadas):
            del pilha[c[0]:]
            if c[1] in ESTRANGEIRAS and not any(chamadas[a][1] in ESTRANGEIRAS for a in pilha):
                self.sequencia.append(i)
            pilha.append(i)
        self.i = 0
        self.erros = []

    def __call__(self, m):
        def externo(nome, chamada, regs):
            if self.i >= len(self.sequencia):
                self.erros.append(f'extra call {nome} at {chamada:#x}')
                raise RuntimeError(f'{nome} at {chamada:#x} is not in the original call sequence')
            k = self.sequencia[self.i]
            self.i += 1
            _, nome_n, args, _, _ = self.chamadas[k]
            if nome_n != nome:
                self.erros.append(f'call {nome} where the original called {nome_n}')
                raise RuntimeError(self.erros[-1])
            largura = {'BatimentLogeEngin': {'EAX': 0xffff, 'EDX': 0xffff},
                       'iagUnitSendMessage': {'EAX': 0xffff, 'EDX': 0xff, 'EBX': M32},
                       'PlayerInitPropositionAlliance': {'EAX': 0xff, 'EDX': 0xff},
                       'InitBatimentNeutre': {'EAX': 0xffff, 'EDX': 0xff}}[nome]
            for r, mascara in largura.items():
                if (regs[r] ^ int(args[r], 16)) & mascara:
                    self.erros.append(f'{nome} {r} {regs[r]:#x} != original {args[r]}')
            for (rotina, eip, endereco, tamanho, valor), abertas in zip(self.escritas, self.atribuicao):
                if k in abertas:
                    getattr(m, {1: 'u8', 2: 'u16', 4: 'u32'}[tamanho])(int(endereco, 16), int(valor, 16))
            return dict(self.saidas[k])
        return externo


M32 = 0xffffffff


def comparar(passo, antes, resultado, referencia, gravador):
    """One comparison record (``ok`` plus the differences) for a native measured step ``resultado``."""
    from capturar_entrada_estruturas import chamada_compacta
    from entrada_estruturas import EntradaEstruturas
    compacto = dict(resultado, calls=[chamada_compacta(c) for c in resultado['calls']])
    chamadas = [[p, n, r, ch, sa] for p, n, r, ch, sa in resultado['calls']]
    m, copias = memoria_de(antes)
    pedidos = []

    def som(nome, regs, pilha):
        pedidos.append(dict(routine=nome, registers={k: hex(v) for k, v in regs.items()},
                            stack=[hex(v) for v in pilha]))
        return regs['EAX']
    replay = Replay(chamadas, resultado['stores'], gravador.atribuicao, gravador.saidas)
    t = EntradaEstruturas(m, externo=replay(m), som=som, bonus=bonus_economia(m))
    entrada = {k: int(resultado['entry_registers'][k], 16) for k in REGISTROS}
    registro = dict(case=resultado['case'], routine=resultado['routine'])
    iguais_captura = referencia is not None and all(referencia[k] == compacto[k] for k in (
        'exit_registers', 'entry_registers', 'changed_bytes', 'stores', 'calls', 'boundaries', 'reached_return'))
    registro['native_equals_capture'] = iguais_captura
    try:
        saida = t.chamar(resultado['routine'], entrada, passo.get('stack', ()))
    except Exception as erro:                    # recorded as a mismatch, never ignored
        from entrada_estruturas import ForaDoDominioEntrada
        declarada = PARADAS_DECLARADAS.get(resultado['case'])
        parada = isinstance(erro, ForaDoDominioEntrada) and declarada is not None and erro.endereco == declarada
        registro.update(ok=parada and iguais_captura, python_error=f'{type(erro).__name__}: {erro}',
                        declared_domain_stop=hex(declarada) if parada else None)
        return registro
    incertos = saida.get('_incertos') or {}
    regs_nativos = {k: int(resultado['exit_registers'][k], 16) for k in REGISTROS}
    dif_regs = {k: [hex(saida[k]), hex(regs_nativos[k])] for k in REGISTROS
                if (saida[k] ^ regs_nativos[k]) & ~incertos.get(k, 0) & M32}
    py_mud = mudancas(antes, copias)
    # a sound inside a replayed callee belongs to that replay, not to this translation
    nativos_fronteira = [dict(routine=b['routine'], registers={k: hex(int(v, 16)) for k, v in b['registers'].items()},
                              stack=b['stack_words'][:1] if b['routine'] == 'PlaySnd_PostSound' else [])
                         for b in resultado['boundaries'] if b['caller'].split('+')[0] not in ESTRANGEIRAS]
    replay_ok = not replay.erros and replay.i == len(replay.sequencia)
    if replay.i != len(replay.sequencia):
        replay.erros.append(f'{len(replay.sequencia) - replay.i} original foreign call(s) not made')
    registro.update(
        ok=(not dif_regs and py_mud == resultado['changed_bytes'] and pedidos == nativos_fronteira and
            iguais_captura and replay_ok),
        register_differences=dif_regs, changed_equal=py_mud == resultado['changed_bytes'],
        boundaries_equal=pedidos == nativos_fronteira, native_changed=len(resultado['changed_bytes']),
        boundaries=len(pedidos), uncertain_bits={k: hex(v) for k, v in incertos.items() if v},
        replayed=[chamadas[k][1] for k in replay.sequencia], replay_errors=replay.erros)
    if py_mud != resultado['changed_bytes']:
        py, na = {x[0]: x for x in py_mud}, {x[0]: x for x in resultado['changed_bytes']}
        registro.update(python_only=[py[a] for a in py if py[a] != na.get(a)][:16],
                        native_only=[na[a] for a in na if na[a] != py.get(a)][:16])
    if pedidos != nativos_fronteira:
        registro.update(python_boundaries=pedidos, native_boundaries=nativos_fronteira)
    return registro


def executar(nomes=None, limite=None):
    """Rerun natively and compare; returns (records, results, reproduction, pause, seconds, capture)."""
    import bancada_entrada_estruturas as bee
    import capturar_entrada_estruturas as cee
    captura = carregar_captura()
    por_nome = {c['case']: c for c in captura['cases']}
    Gravador = gravador_atribuido()
    bee.Folhas = Gravador
    registros = []

    def observador(caso, passo, antes, resultado):
        r = comparar(passo, antes, resultado, por_nome.get(resultado['case']), Gravador.ultimo)
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
    ap.add_argument('--saida', default='relatorios/entrada-estruturas-emulada.json')
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
        schema='rising-lands/monde01-structure-entry-differential/1', original_sha256=HASH_ORIGINAL,
        capture=dict(path=str(CAPTURA.relative_to(RAIZ)), sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        path_reproduction=reproducao, pause=pausa, comparisons=len(registros),
        mismatches=[r for r in registros if not r['ok']],
        by_routine={k: dict(steps=v[0], mismatches=v[1]) for k, v in sorted(por_rotina.items())},
        changed_bytes_compared=sum(r.get('native_changed', 0) for r in registros),
        uncertain=[dict(case=r['case'], bits=r['uncertain_bits']) for r in registros if r.get('uncertain_bits')],
        replayed_foreign_calls=sum(len(r.get('replayed', ())) for r in registros),
        providers=dict(bonus='Economy bonus_unidades.BonusUnidades over the live tables 0x4dfba0/0x4965ae',
                       som='returns the received EAX (the frame bench declaration for PlaySnd_*), compared',
                       externo='the original nested call replayed (BatimentLogeEngin, iagUnitSendMessage, '
                               'PlayerInitPropositionAlliance, InitBatimentNeutre): arguments checked, its stores '
                               'applied, its exit registers returned'),
        declared_domain_stops=[dict(case=r['case'], address=r['declared_domain_stop']) for r in registros
                               if r.get('declared_domain_stop')],
        seconds=segundos)
    ok = (all(reproducao.values()) and not relatorio['mismatches'] and
          (a.nomes or len(registros) == len(captura['cases'])))
    if not ok:
        saida = RAIZ / '.local/entrada' / f'entrada-estruturas-falha-{time.strftime("%Y%m%dT%H%M%S")}.json'
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'w') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    escritos = []
    if ok and not a.nomes:
        with lzma.open(LEITURAS, 'wt') as f:
            json.dump(dict(schema='rising-lands/monde01-structure-entry-reads/1', original_sha256=HASH_ORIGINAL,
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
