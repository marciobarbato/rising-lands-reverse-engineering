"""Native leaf-call bench for the player selection and order-setter routines (M3 groundwork).

None of these routines runs in the no-input coverage run (docs/M3_PLAN.md §0), so the
game flow cannot pause at them. This bench reruns one of Missions' committed MONDE01
paths (``percurso_quadro1._bancada``: startup, MissionLoad, load_tail, between_frames)
and pauses frame 1 at its first ``ProcessInputGame`` entry, the routine that dispatches
player commands to these setters. That state is accepted real state: the run reproduces
every committed phase summary and the code section afterwards.

At the pause, each declared case runs one routine natively as a leaf call:
- the saved CPU context and every state block (DGROUP+.bss, CRT thread page, active
  allocations, native stack) are restored first;
- the case's declared byte writes and argument registers are applied (other registers keep
  the paused values, which are recorded);
- the return slot holds the bench sentinel 0x100 bytes below the paused ESP, followed by
  the declared pushed words;
- the routine runs under the bench's own frame boundary handling: a ``PlaySnd_*`` call is
  not executed (EAX unchanged, declared stack cleanup) and is logged with its registers and
  stack words, exactly as in the committed frame phases.

Recorded per case: entry and exit registers, every non-stack store in order (instruction,
address, width, value), the changed bytes of every state block (stack excluded), the
nested routine entries (depth, name, argument registers, exit EAX) and the boundary
events. After the last case the exact paused state is restored and frame 1 resumes.

``observador(caso, antes, resultado)`` (optional) runs after each native case with the
state blocks at the case entry (after its writes); the validator compares the Python
translation there. Importing this module executes nothing.
"""
import copy
import struct
import time

CODIGO = (0x401000, 0x493c00)
REGS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP')
FASE_FOLHA = 'frame1'


class Folhas:
    """Recorder of one native leaf call; hooks exist only while a case runs."""
    def __init__(self, b, regioes, pilha):
        self.b, self.regioes, self.pilha = b, regioes, pilha
        self.simbolos = set(b.nomes)

    def armar(self, esp_inicial):
        import unicorn
        cpu = self.b.cpu
        self.escritas, self.chamadas, self.abertas, self.ultimo = [], [], [], None
        self.esp_inicial = esp_inicial
        g = [cpu.hook_add(unicorn.UC_HOOK_BLOCK, self._bloco, begin=CODIGO[0], end=CODIGO[1] - 1)]
        for inicio, fim in self.regioes:
            g.append(cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._escrever, begin=inicio, end=fim - 1))
        cpu.ctl_flush_tb()
        return g

    def _regs(self, cpu):
        from unicorn import x86_const as x86
        return {r: cpu.reg_read(getattr(x86, 'UC_X86_REG_' + r)) for r in REGS}

    def _bloco(self, cpu, endereco, tamanho, _):
        from unicorn import x86_const as x86
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        while self.abertas and endereco == self.abertas[-1]['retorno'] and esp > self.abertas[-1]['esp']:
            f = self.abertas.pop()
            self.chamadas[f['indice']][4] = hex(cpu.reg_read(x86.UC_X86_REG_EAX))
        chave = (endereco, esp)
        repetido, self.ultimo = chave == self.ultimo, chave
        if endereco not in self.simbolos or repetido or esp >= self.esp_inicial:
            return                      # the top-level entry itself is not a nested call
        r = self._regs(cpu)
        retorno = struct.unpack('<I', bytes(cpu.mem_read(esp, 4)))[0]
        self.abertas.append(dict(retorno=retorno, esp=esp, indice=len(self.chamadas)))
        self.chamadas.append([len(self.abertas) - 1, self.b.nomes[endereco],
                              {k: hex(r[k]) for k in ('EAX', 'EDX', 'EBX', 'ECX')}, self.b.nome(retorno), None])

    def _escrever(self, cpu, acesso, endereco, tamanho, valor, _):
        if self.pilha[0] <= endereco < self.pilha[1]:
            return
        from unicorn import x86_const as x86
        self.escritas.append([self.b.nome(cpu.reg_read(x86.UC_X86_REG_EIP)), hex(cpu.reg_read(x86.UC_X86_REG_EIP)),
                              hex(endereco), tamanho, hex(valor & ((1 << 8 * tamanho) - 1))])


def _mudancas(antes, depois):
    saida = []
    for nome, (base, velho) in antes.items():
        if nome == 'native_stack':
            continue
        novo = depois[nome][1]
        if novo != velho:
            saida += [[hex(base + i), velho[i], novo[i]] for i in range(len(velho)) if velho[i] != novo[i]]
    return sorted(saida, key=lambda x: int(x[0], 16))


def executar(cenario, casos, observador=None, quadro_s=1800):
    """Run the declared ``casos`` at frame 1's first ProcessInputGame entry of ``cenario``.

    Returns (bench, cases, results, reproduction, pause, seconds). ``casos``: a list, or a
    callable(bench) evaluated at the pause, of dicts with ``case``, ``routine``,
    ``registers`` {name: value}, optional ``writes`` [(address, bytes)], ``stack`` [u32 words
    pushed above the return slot] and ``ret_imm`` (bytes the routine's RET pops)."""
    import percurso_quadro1 as pq
    from oraculo_carga_missao import BancadaCargaMissaoOriginal, DADOS_THREAD_CRT, DGROUP
    from oraculo_quadro_missao import Isolamento
    from emulador import PILHA, RETORNO
    from unicorn import x86_const as x86
    b, cap = pq._bancada(cenario)
    resultados, estado = [], dict(feito=False, pausa=None)
    t0 = time.monotonic()

    class Pausa(Isolamento):
        def executar(self, regs):
            if estado['feito'] or b.fase != 'frame1':
                return
            estado['feito'] = True
            self.ativo = False
            contexto, blocos = self._salvar()
            rastro, topo, ultimo = copy.deepcopy(b.rastro), getattr(b, '_topo', None), getattr(b, '_ultimo_bloco', None)
            fronteiras = len(b.eventos_fronteira)
            a = b.arena
            regioes = ((DGROUP[0], DGROUP[1]), (DADOS_THREAD_CRT, DADOS_THREAD_CRT + 0x1000), (a.base, a.proximo),
                       (PILHA, PILHA + 0x10000))
            gravador = Folhas(b, regioes, (PILHA, PILHA + 0x10000))
            retorno_pausa = struct.unpack('<I', b.cpu.mem_read(regs['ESP'], 4))[0]
            estado['pausa'] = dict(routine=self.entradas[regs['EIP']], caller_return=hex(retorno_pausa),
                                   caller=b.nome(retorno_pausa), registers={k: hex(v) for k, v in regs.items()},
                                   state_sha256=b.resumo_imagem(blocos))
            estado['casos'] = casos(b) if callable(casos) else list(casos)
            try:
                for caso in estado['casos']:
                    self._restaurar(contexto, blocos)
                    for endereco, dados in caso.get('writes', ()):
                        b.cpu.mem_write(endereco, bytes(dados))
                    esp = regs['ESP'] - 0x100
                    palavras = [RETORNO] + list(caso.get('stack', ()))
                    b.cpu.mem_write(esp, struct.pack(f'<{len(palavras)}I', *palavras))
                    for nome, valor in caso['registers'].items():
                        b.cpu.reg_write(getattr(x86, 'UC_X86_REG_' + nome), valor & 0xffffffff)
                    b.cpu.reg_write(x86.UC_X86_REG_ESP, esp)
                    entrada = b.sym[caso['routine']]
                    antes = self._salvar()[1]
                    regs_entrada = gravador._regs(b.cpu)
                    regs_entrada['EIP'] = entrada
                    ganchos = gravador.armar(esp)
                    inicio = len(b.eventos_fronteira)
                    try:
                        b._retomando = set()
                        saida = BancadaCargaMissaoOriginal._correr(b, 'leaf', entrada, {}, (RETORNO,), retomar=True)
                    finally:
                        for g in ganchos:
                            b.cpu.hook_del(g)
                        b.cpu.ctl_flush_tb()
                    eventos = b.eventos_fronteira[inicio:]
                    del b.eventos_fronteira[inicio:]
                    depois = self._salvar()[1]
                    if gravador.abertas:
                        raise RuntimeError(f'Unclosed nested calls in case {caso["case"]}')
                    resultado = dict(
                        case=caso['case'], routine=caso['routine'], entry=hex(entrada),
                        declared_registers={k: hex(v) for k, v in caso['registers'].items()},
                        writes=[[hex(x), bytes(d).hex()] for x, d in caso.get('writes', ())],
                        stack_words=[hex(v) for v in caso.get('stack', ())],
                        entry_registers={k: hex(v) for k, v in regs_entrada.items()},
                        exit_registers={k: hex(v) for k, v in saida.items()},
                        reached_return=saida['EIP'] == RETORNO and saida['ESP'] == esp + 4 + caso.get('ret_imm', 0),
                        stores=gravador.escritas, changed_bytes=_mudancas(antes, depois), calls=gravador.chamadas,
                        boundaries=[dict(routine=e['routine'], caller=e['caller'], registers=e['registers'],
                                         stack_words=e['stack_words'], declared_eax=e['declared_eax'],
                                         stack_cleanup=e['stack_cleanup']) for e in eventos])
                    resultados.append(resultado)
                    if observador is not None:
                        observador(caso, antes, resultado)
            finally:
                self._restaurar(contexto, blocos)
                del b.eventos_fronteira[fronteiras:]
                b.rastro, b._topo, b._ultimo_bloco = rastro, topo, ultimo
                b.fase = 'frame1'
                b.windows.fase = 'frame1'
                self.ativo = True

    iso = Pausa(b, ('ProcessInputGame',))
    iso.instalar()
    referencia = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(300)),
                         ('frame1', lambda: b.executar_quadro(quadro_s))):
        correr()
        reproducao[nome] = b.resumo_imagem(b.imagem()) == referencia[nome]
    reproducao['code_unchanged'] = b.sha256_codigo() == cap['code_integrity']['after']
    reproducao['paused'] = estado['feito']
    return b, estado.get('casos', []), resultados, reproducao, estado['pausa'], round(time.monotonic() - t0, 3)
