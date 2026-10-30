"""Native multi-frame bench for the economy work and transport cycles (M3/M4 economy row).

Missions' accepted MONDE01 display path (startup, MissionLoad, load_tail, between_frames, frame1) is
rerun and must reproduce its committed summaries. Then the real loop keeps running (between_frames,
frame) with the reference's declared no-input answers; its display clock is extended by the same
rule, as Core's coverage run does (``ferramentas/cobrir_quadros_exibicao.py``).

Declared orders. At the CalculGame entry of chosen frames the bench calls ORIGINAL routines natively
(setters, DecouvreTerrain) from that exact state, as leaf calls whose return lands on the bench
trampoline; their stores stay, the CPU context is restored, and the frame then runs. Each such call
is recorded (registers, changed bytes). A declared byte write (for example the player's cave count)
is recorded the same way. Nothing else differs from the reference loop.

Isolated calls. At the entries of ``rotinas`` a selector decides per call whether to record it. A
recorded call runs natively from its exact entry state to its return under recording hooks (every
non-stack store with the nested call it happened in, every nested routine entry with its argument and
exit registers, the bytes read before written, the frame-boundary events), its changed bytes are
taken over the whole mapped state, an optional observer sees it (the translation validator), the
entry state is restored, and the frame resumes and executes the routine as usual (Missions'
``Isolamento`` method). A binding (declared I/O) inside a recorded call stops the run. ``pseudo`` adds inline bodies
recorded the same way, from an entry address to an exit address reached with the entry ESP.

Importing this module executes nothing.
"""
import copy
import json
from pathlib import Path
import struct
import sys
import time

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

REGS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP')
CONTADOR = 0x508f7c


def _mudancas(antes, depois, estrito=True):
    saida = []
    for nome, (base, velho) in antes.items():
        if nome == 'native_stack':
            continue
        novo = depois[nome][1] if nome in depois else None
        if novo is None:
            if not estrito:
                continue
            raise RuntimeError(f'Block {nome} disappeared inside a recorded call')
        if novo != velho:
            saida += [[hex(base + i), velho[i], novo[i]] for i in range(len(velho)) if velho[i] != novo[i]]
    for nome in depois:
        if nome not in antes and estrito:
            raise RuntimeError(f'Block {nome} appeared inside a recorded call')
    return sorted(saida, key=lambda x: int(x[0], 16))


class Ciclo:
    """The bench. ``ordens(b, k, ler)`` returns the declared actions at frame k's CalculGame entry:
    [dict(kind='call', label, routine, registers) | dict(kind='write', label, address, bytes)].
    ``escolher(nome, regs, ler)`` decides whether a call of ``nome`` is recorded.
    ``observador(nome, regs, antes, resultado)`` sees every recorded call.
    ``gravar_acoes``: a declared call runs through the isolation-aware runner, so the recorded routines it
    enters (itself included) are recorded like the frame's own calls, each tagged with the action label."""

    def __init__(self, rotinas, escolher, ordens, observador=None, amostra=None, ticks=60000, gravar_acoes=False,
                 pseudo=None):
        import percurso_quadro1  # noqa: F401  (puts Missions on sys.path)
        import cenarios_oraculo
        from oraculo_exibicao_missao import BancadaExibicaoOriginal
        self.cap_caminho = cenarios_oraculo.caminho('exibicao', 'captura_quadro')
        self.cap = json.loads(self.cap_caminho.read_bytes())
        ni = self.cap['named_inputs']['m1']
        ticks = tuple(0x123456 + 40 * k for k in range(1, ticks + 1))
        if ticks[:len(cenarios_oraculo.TICKS_EXIBICAO)] != cenarios_oraculo.TICKS_EXIBICAO:
            raise SystemExit('Display clock rule differs from cenarios_oraculo.TICKS_EXIBICAO')
        self.b = BancadaExibicaoOriginal(cenarios_oraculo.entradas_exibicao(ni['allocation_fill'], ni['clock_ms'][0],
                                                                            ticks=ticks), segundos=300, rastrear=False)
        self.rotinas, self.escolher, self.ordens = rotinas, escolher, ordens
        self.observador, self.amostra = observador, amostra
        self.registros, self.acoes, self.quadros = [], [], []
        self.reproducao = {}
        self.gravar_acoes, self.acao_atual = gravar_acoes, None
        # Inline bodies recorded like calls: {entry address: (name, exit address)}. The body runs from its entry to
        # the exit with ESP unchanged (e.g. a unit-state body of EnginNextEtape up to its common exit).
        self.pseudo = dict(pseudo or {})

    # ------------------------------------------------------------ memory helpers
    def ler(self, endereco, n):
        return bytes(self.b.cpu.mem_read(endereco, n))

    def u8(self, a):
        return self.ler(a, 1)[0]

    def u16(self, a):
        return struct.unpack('<H', self.ler(a, 2))[0]

    def u32(self, a):
        return struct.unpack('<I', self.ler(a, 4))[0]

    # ------------------------------------------------------------ declared actions
    def _acao(self, k, acao):
        """One declared action. ``kind='case'`` runs its ``steps`` (calls/writes) from the current state,
        records each step, then restores the whole state (CPU context, every block, native stack)."""
        if acao['kind'] != 'case':
            return self._passo(k, acao)
        from emulador import PILHA
        b = self.b
        contexto = b.cpu.context_save()
        blocos = b.imagem()
        pilha = bytes(b.cpu.mem_read(PILHA, 0x10000))
        inicio = len(self.acoes)
        try:
            for passo in acao['steps']:
                self._passo(k, passo)
        finally:
            passos = self.acoes[inicio:]
            del self.acoes[inicio:]
            for base, dados in blocos.values():
                b.cpu.mem_write(base, dados)
            b.cpu.mem_write(PILHA, pilha)
            b.cpu.context_restore(contexto)
        if b.imagem() != blocos:
            raise RuntimeError(f'Case {acao["label"]} did not restore the state')
        self.acoes.append(dict(frame=k, counter=self.u32(CONTADOR), kind='case', label=acao['label'], steps=passos))

    def _passo(self, k, acao):
        from oraculo_carga_missao import BancadaCargaMissaoOriginal
        from emulador import RETORNO
        from unicorn import x86_const as x86
        b = self.b
        antes = b.imagem()
        contexto = b.cpu.context_save()
        registro = dict(frame=k, counter=self.u32(CONTADOR), **{c: acao[c] for c in acao if c not in ('registers',)})
        if acao['kind'] == 'write':
            b.cpu.mem_write(acao['address'], bytes(acao['bytes']))
            registro.update(address=hex(acao['address']), bytes=bytes(acao['bytes']).hex())
        else:
            esp = b.cpu.reg_read(x86.UC_X86_REG_ESP) - 0x100
            b.cpu.mem_write(esp, struct.pack('<I', RETORNO))
            for nome, valor in acao['registers'].items():
                b.cpu.reg_write(getattr(x86, 'UC_X86_REG_' + nome), valor & 0xffffffff)
            b.cpu.reg_write(x86.UC_X86_REG_ESP, esp)
            fase, eventos, fronteiras = b.fase, len(b.vinculos_declarados.eventos), len(b.eventos_fronteira)
            b._retomando = set()
            if self.gravar_acoes:
                # A stop on the very first instruction leaves EIP unwritten: set it, so the isolation-aware
                # runner sees the routine's entry and records it.
                b.cpu.reg_write(x86.UC_X86_REG_EIP, b.sym[acao['routine']])
                self.acao_atual = acao['label']
                try:
                    saida = b._correr('leaf', b.sym[acao['routine']], {}, (RETORNO,), retomar=True)
                finally:
                    self.acao_atual = None
            else:
                saida = BancadaCargaMissaoOriginal._correr(b, 'leaf', b.sym[acao['routine']], {}, (RETORNO,), retomar=True)
            b.fase = fase
            if saida['EIP'] != RETORNO or saida['ESP'] != esp + 4:
                raise RuntimeError(f'Declared call {acao["label"]} did not return: EIP {saida["EIP"]:#x} '
                                   f'({b.nome(saida["EIP"])}), ESP {saida["ESP"]:#x} (expected {esp + 4:#x})')
            if len(b.vinculos_declarados.eventos) != eventos:
                raise RuntimeError(f'Declared call {acao["label"]} reached a binding')
            registro.update(registers={c: hex(v) for c, v in acao['registers'].items()},
                            exit_registers={c: hex(saida[c]) for c in REGS[:7]},
                            boundaries=[dict(routine=e['routine'], caller=e['caller'], registers=e['registers'])
                                        for e in b.eventos_fronteira[fronteiras:]])
            del b.eventos_fronteira[fronteiras:]
        b.cpu.context_restore(contexto)
        depois = b.imagem()
        registro['changed_bytes'] = _mudancas(antes, depois, estrito=False)
        registro['blocks_added'] = sorted(n for n in depois if n not in antes)
        registro['blocks_removed'] = sorted(n for n in antes if n not in depois)
        self.acoes.append(registro)
        return registro

    # ------------------------------------------------------------ isolation
    def _isolamento(self):
        from oraculo_carga_missao import BancadaCargaMissaoOriginal, DADOS_THREAD_CRT, DGROUP
        from oraculo_quadro_missao import Isolamento
        from emulador import PILHA
        import bancada_ordens_economia as boe
        import unicorn
        ciclo = self

        class IsolamentoCiclo(Isolamento):
            def executar(self, regs):
                b, entrada = self.b, regs['EIP']
                nome = self.entradas[entrada]
                if not ciclo.escolher(nome, regs, ciclo):
                    return
                if entrada in ciclo.pseudo:
                    retorno, esp_saida = ciclo.pseudo[entrada][1], regs['ESP']
                else:
                    retorno, esp_saida = struct.unpack('<I', b.cpu.mem_read(regs['ESP'], 4))[0], regs['ESP'] + 4
                contexto, blocos = self._salvar()
                fase = b.fase
                self.ativo = False   # the frame phase name stays: frame boundaries (PlaySnd_*) are declared there
                a = b.arena
                regioes = ((DGROUP[0], DGROUP[1]), (DADOS_THREAD_CRT, DADOS_THREAD_CRT + 0x1000), (a.base, a.proximo),
                           (PILHA, PILHA + 0x10000))
                gravador = boe._gravador(b, regioes, (PILHA, PILHA + 0x10000), True)
                eventos, fronteiras = len(b.vinculos_declarados.eventos), len(b.eventos_fronteira)
                try:
                    ganchos = gravador.armar(regs['ESP'])
                    ganchos.append(b.cpu.hook_add(unicorn.UC_HOOK_CODE, b._parar_se_pedido, begin=retorno, end=retorno))
                    b.cpu.ctl_flush_tb()
                    try:
                        b._retomando = {entrada}
                        saida = BancadaCargaMissaoOriginal._correr(b, 'isolated', entrada, {}, (retorno,), retomar=True)
                    finally:
                        for g in ganchos:
                            b.cpu.hook_del(g)
                        b.cpu.ctl_flush_tb()
                    if saida['EIP'] != retorno or saida['ESP'] != esp_saida:
                        raise RuntimeError(f'Recorded call {nome} did not reach its return')
                    if len(b.vinculos_declarados.eventos) != eventos:
                        raise RuntimeError(f'Binding inside the recorded call {nome}')
                    if gravador.abertas:
                        raise RuntimeError(f'Unclosed nested calls in {nome}')
                    depois = self._salvar()[1]
                    resultado = dict(
                        routine=nome, entry=hex(entrada), frame=ciclo.k, counter=ciclo.u32(CONTADOR),
                        caller_return=hex(retorno), caller=b.nome(retorno),
                        entry_registers={c: hex(regs[c]) for c in REGS},
                        exit_registers={c: hex(saida[c]) for c in REGS},
                        changed_bytes=_mudancas(blocos, depois), stores=gravador.escritas, calls=gravador.chamadas,
                        read_before_write=gravador.leituras_em_runs(),
                        boundaries=[dict(routine=e['routine'], caller=e['caller'], registers=e['registers'],
                                         stack_words=e['stack_words'], declared_eax=e['declared_eax'],
                                         stack_cleanup=e['stack_cleanup']) for e in b.eventos_fronteira[fronteiras:]])
                    if ciclo.acao_atual is not None:
                        resultado['action'] = ciclo.acao_atual
                    if ciclo.observador is not None:
                        ciclo.observador(nome, regs, blocos, resultado)
                    ciclo.registros.append(resultado)
                finally:
                    self._restaurar(contexto, blocos)
                    del b.eventos_fronteira[fronteiras:]
                    b.fase = fase
                    self.ativo = True

        iso = IsolamentoCiclo(self.b, self.rotinas)
        for entrada, (nome, _saida) in self.pseudo.items():
            iso.entradas[entrada] = nome
        return iso

    # ------------------------------------------------------------ run
    def executar(self, ate, progresso=None):
        """Run frames 0/1 (reproduced), then frames 2..``ate`` (counter) with the declared actions."""
        b = self.b
        t0 = time.monotonic()
        b.iniciar_relogio()
        b.executar_inicio()
        b.executar_mission_load(60)
        referencia = {p['phase']: p['state_after']['summary'] for p in self.cap['phases']}
        for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                             ('between_frames', lambda: b.executar_entre_quadros(300)),
                             ('frame1', lambda: b.executar_quadro(600))):
            correr()
            self.reproducao[nome] = b.resumo_imagem(b.imagem()) == referencia[nome]
        if not all(self.reproducao.values()):
            raise RuntimeError(f'Frames 0/1 do not reproduce the display reference: {self.reproducao}')
        iso = self._isolamento()
        iso.instalar()
        self.k = 2
        while True:
            b.executar_entre_quadros(300)
            for acao in self.ordens(self, self.k):
                self._acao(self.k, acao)
            b.executar_quadro(600)
            if self.amostra is not None:
                self.quadros.append(dict(frame=self.k, counter=self.u32(CONTADOR), **self.amostra(self)))
            if progresso is not None:
                progresso(self.k, time.monotonic() - t0)
            if self.u32(CONTADOR) >= ate:
                break
            self.k += 1
        self.reproducao['code_unchanged'] = b.sha256_codigo() == self.cap['code_integrity']['after']
        return round(time.monotonic() - t0, 3)
