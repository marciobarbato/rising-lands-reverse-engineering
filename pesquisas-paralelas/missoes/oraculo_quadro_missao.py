"""MONDE01 first-frame original oracle, continuing the accepted M1 bench.

The accepted M1 path is reused unchanged: original startup (AppInit, the
CalculGame menu frames driven by the declared key script) to the real
``CALL MissionLoad`` at 0x42d228, then the intact MissionLoad to 0x42d22d.
This module then runs, still with the intact executable only:

(a) ``load_tail``: the rest of that load-state CalculGame invocation from
    0x42d22d to its real RET (state 0 jumps to 0x42d27f: RestoreAll,
    SetClipping, the three frame counters reset, MenuInit, InitGameZone,
    PlayerAttaqueReset, then the shared frame body).  The bench called the
    load frame directly, as in M1, so that RET returns to the bench's caller
    trampoline instead of ProgIteration 0x475063.
(b) ``between_frames``: what the window loop executes between two CalculGame
    calls, from ProgIteration 0x475063 (the instruction after its CALL
    CalculGame) through AffGame, the flag clears, the RET to _WinMain@16
    0x460212, PlaySnd_Manage, MCICD_Manage, the quit/active-flag tests,
    PeekMessageA, a new ProgIteration (frame counters 0x508f7c/80/84,
    GetCursorPos, cursor stores) up to the CalculGame entry 0x42c868.
(c) ``frame1``: the first game-state CalculGame frame from 0x42c868 to its
    real return 0x475063 inside ProgIteration.

Between (a) and (b) the stack slots ProgIteration and _WinMain@16 own above
the CalculGame return slot are declared (see ``quadro_chamador``): the return
address 0x460212 of the CALL at 0x46020d, saved EBX 0 (_WinMain@16 zeroes EBX
at 0x4601af and uses it as its zero constant), and declared saved ECX/EDX and
carried ESI/EDI/EBP values whose influence is measured by a sensitivity run.

Routines that need the display, the sound library (PlaySnd_InitSoundLib is
never executed) or MCI CD audio (MCICD_Init is never executed) are *not
executed* in these phases.  Each is a declared output boundary
(``FRONTEIRAS_QUADRO``): the bench stops at its entry, records the routine,
caller, EAX/EDX/EBX/ECX and the stack argument words, applies the routine's
own callee stack cleanup and returns to the caller with EAX unchanged or a
declared value.  Any other non-executed routine, undeclared import, fault or
budget exhaustion stops the run with all state retained.  Importing this
module executes nothing.
"""
from bisect import bisect_right
from dataclasses import dataclass, field
import struct

import ambiente_missoes
from emulador import PILHA, RETORNO, unicorn, x86
from vinculos_declarados import ParadaVinculoDeclarado
from fronteiras_carga_missao import WindowsDeclarado
from oraculo_carga_missao import (BancadaCargaMissaoOriginal, DADOS_THREAD_CRT, DGROUP, PULOS_INICIO,
                                  RETORNO_MISSION_LOAD, escritas_estaticas)

CALCUL_GAME = 0x42c868
RETORNO_CALCUL_GAME = 0x475063     # ProgIteration, after CALL CalculGame 0x47505e
RETORNO_PROG_ITERATION = 0x460212  # _WinMain@16, after CALL ProgIteration 0x46020d
SAIDA_LACO = 0x460227              # _WinMain@16 loop exit (quit flag 0x49a059 set)
RNG = (0x497164, 0x498db4)
FASES_QUADRO = ('load_tail', 'between_frames', 'frame1')

# Frame-phase non-executed routines: name -> (declared EAX or None=unchanged,
# callee stack cleanup from the routine's own RET imm16, reason).  The startup
# display/text/bank set (PULOS_INICIO) keeps its M1 declarations: MenuInit
# runs natively in the load tail exactly as in the startup menus.
FRONTEIRAS_QUADRO = {nome: (valor, limpeza, 'startup display/text/bank boundary (M1 PULOS_INICIO)')
                     for nome, (valor, limpeza) in PULOS_INICIO.items()}
FRONTEIRAS_QUADRO.update({
    'AffGame': (None, 0, 'whole-frame display composition (DirectDraw surfaces, sprite banks never loaded)'),
    'PlaySnd_Manage': (None, 0, 'sound library mixer pump; PlaySnd_InitSoundLib never executed'),
    'PlaySnd_PostSound': (None, 4, 'sound request post into the sound library; PlaySnd_InitSoundLib never executed'),
    'PlaySnd_StopSound': (None, 0, 'sound library; PlaySnd_InitSoundLib never executed'),
    'PlaySnd_StopAllSound': (None, 0, 'sound library; PlaySnd_InitSoundLib never executed'),
    'PlaySnd_PostVolume': (None, 0, 'sound library; PlaySnd_InitSoundLib never executed'),
    'PlaySnd_SetGameVolume': (None, 0, 'sound library; PlaySnd_InitSoundLib never executed'),
    'MCICD_Manage': (None, 0, 'MCI CD audio pump; MCICD_Init never executed'),
})
# Guard bytes recorded at each boundary event.  MCICD_Play 0x467a97 and
# MCICD_Manage 0x467bf6 return without any store while [0x4e2f29] (set only by
# MCICD_Init, never executed) is 0; CalculGame ignores MCICD_Play's AL.
GUARDAS_FRONTEIRA = {'MCICD_Play': (0x4e2f29, 0x4e2f28), 'MCICD_Manage': (0x4e2f29, 0x4e2f28),
                     'MCICD_Stop': (0x4e2f29, 0x4e2f28)}
# Routines whose static absolute DGROUP stores are watched for reads during
# the frame phases: every frame boundary plus the sound/CD initializers that
# the startup never ran.
NAO_EXECUTADOS_QUADRO = tuple(sorted(FRONTEIRAS_QUADRO)) + ('PlaySnd_InitSoundLib', 'MCICD_Init',
                                                            'AppWindowInit', 'WndProc')


@dataclass(frozen=True)
class EntradasQuadro:
    """Named inputs of the frame phases, on top of the M1 ``EntradasNomeadas``."""
    base: object                      # EntradasNomeadas of the accepted M1 path
    cursor: tuple                     # GetCursorPos answer (x, y)
    registradores_chamador: dict      # declared saved ECX/EDX and carried ESI/EDI/EBP at (b)
    proveniencia: dict = field(default_factory=dict)

    def __post_init__(self):
        if (len(self.cursor) != 2 or set(self.registradores_chamador) != {'ECX', 'EDX', 'ESI', 'EDI', 'EBP'}):
            raise ValueError('Declare the cursor and every caller register explicitly')

    def manifesto(self):
        return dict(cursor=list(self.cursor),
                    caller_registers={k: hex(v) for k, v in sorted(self.registradores_chamador.items())},
                    get_async_key_state='every frame-phase call answers 0 (not pressed, no transition)',
                    peek_message='PeekMessageA answers 0 (no message queued)',
                    provenance=self.proveniencia)


class WindowsQuadro(WindowsDeclarado):
    """M1 Windows answers plus the declared no-input answers of the frame phases."""
    def __init__(self, entradas, quadro):
        super().__init__(entradas)
        self.quadro = quadro
        self.fase = None

    def tecla(self, chamada):
        if self.teclas or self.fase not in FASES_QUADRO:
            return super().tecla(chamada)
        vk, = chamada.argumentos
        self.consumidos.append(('key', hex(chamada.retorno), vk, 0, self.fase))
        return 0

    def cursor(self, chamada):
        if self.fase not in FASES_QUADRO:
            raise ParadaVinculoDeclarado('GetCursorPos outside the declared frame phases')
        x, y = self.quadro.cursor
        chamada.escrever(chamada.argumentos[0], struct.pack('<ii', x, y))
        self.consumidos.append(('cursor', hex(chamada.retorno), x, y, self.fase))
        return 1

    def mensagem(self, chamada):
        if self.fase not in FASES_QUADRO:
            raise ParadaVinculoDeclarado('PeekMessageA outside the declared frame phases')
        _, hwnd, minimo, maximo, remover = chamada.argumentos
        if (hwnd, minimo, maximo) != (0, 0, 0):
            raise ParadaVinculoDeclarado('PeekMessageA filter outside the declared no-message answer')
        self.consumidos.append(('peek_message', hex(chamada.retorno), remover, 0, self.fase))
        return 0


def retornos_alcancaveis(imagem_codigo, entrada, limite=50000):
    """RET imm16 values reachable from ``entrada`` without following CALLs.

    Intra-procedural walk over the intact bytes: conditional branches go both
    ways, unconditional JMPs (shared epilogues, thunks) and fall-through across
    symbol boundaries are followed.  A switch ``jmp [reg*4+table]`` is
    followed through ``bound+1`` table entries when one of the three preceding
    instructions is ``cmp reg, bound`` on the same register; any other indirect
    JMP is recorded as unresolved, never guessed.  Returns (sorted RET
    immediates, unresolved).
    """
    import capstone
    import re
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    familia = {'eax': ('eax', 'ax', 'al'), 'ebx': ('ebx', 'bx', 'bl'), 'ecx': ('ecx', 'cx', 'cl'),
               'edx': ('edx', 'dx', 'dl'), 'esi': ('esi', 'si'), 'edi': ('edi', 'di'), 'ebp': ('ebp', 'bp')}
    vistos, pilha, rets, abertos = set(), [entrada], set(), []
    while pilha and len(vistos) < limite:
        a = pilha.pop()
        recentes = []
        while 0x401000 <= a < 0x493c00 and a not in vistos:
            vistos.add(a)
            ins = next(md.disasm(imagem_codigo(a, 16), a), None)
            if ins is None:
                abertos.append(hex(a))
                break
            if ins.mnemonic == 'ret':
                rets.add(int(ins.op_str, 16) if ins.op_str else 0)
                break
            if ins.mnemonic == 'jmp':
                if ins.op_str.startswith('0x'):
                    a = int(ins.op_str, 16)
                    continue
                tabela = re.fullmatch(r'dword ptr (?:cs:)?\[(e\w\w)\*4 \+ (0x[0-9a-f]+)\]', ins.op_str)
                limite_tabela = None
                if tabela:
                    for r in reversed(recentes[-3:]):
                        m = re.fullmatch(r'(\w+), (0x[0-9a-f]+|\d+)', r.op_str)
                        if r.mnemonic == 'cmp' and m and m.group(1) in familia.get(tabela.group(1), ()):
                            limite_tabela = int(m.group(2), 0)
                            break
                if limite_tabela is None:
                    abertos.append(f'{ins.address:#x}: jmp {ins.op_str}')
                    break
                base = int(tabela.group(2), 16)
                pilha.extend(struct.unpack('<I', imagem_codigo(base+4*i, 4))[0] for i in range(limite_tabela+1))
                break
            recentes.append(ins)
            if ins.mnemonic.startswith('j') or ins.mnemonic.startswith('loop'):
                if ins.op_str.startswith('0x'):
                    pilha.append(int(ins.op_str, 16))
            a = ins.address + ins.size
    return sorted(rets), abertos


def limpeza_estatica(imagem_codigo, inicio, fim=None):
    """('rets', [imm16...]) reachable from a routine entry, or ('unresolved', [...])."""
    rets, abertos = retornos_alcancaveis(imagem_codigo, inicio)
    return ('rets', rets) if not abertos else ('unresolved', abertos)


def eax_lido_pelo_chamador(imagem_codigo, retorno, maximo=12):
    """Static check after a return: does the caller read EAX before writing it?

    Linear decode from the return address until an instruction writes all of
    EAX, any control transfer, or ``maximo`` instructions.  Returns
    ('read', address, text) / ('overwritten', ...) / ('transfer', ...).
    """
    import capstone
    from capstone import x86_const as X
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True
    familia = {X.X86_REG_EAX, X.X86_REG_AX, X.X86_REG_AL, X.X86_REG_AH}
    for ins in md.disasm(imagem_codigo(retorno, 64), retorno):
        lidos, escritos = ins.regs_access()
        if familia & set(lidos) and not (ins.mnemonic == 'xor' and ins.op_str in ('eax, eax',)):
            return ('read', hex(ins.address), f'{ins.mnemonic} {ins.op_str}')
        if X.X86_REG_EAX in escritos:
            return ('overwritten', hex(ins.address), f'{ins.mnemonic} {ins.op_str}')
        if ins.group(capstone.CS_GRP_JUMP) or ins.group(capstone.CS_GRP_CALL) or ins.group(capstone.CS_GRP_RET):
            return ('transfer', hex(ins.address), f'{ins.mnemonic} {ins.op_str}')
        maximo -= 1
        if not maximo:
            break
    return ('undetermined', hex(retorno), '')


class BancadaQuadroMissaoOriginal(BancadaCargaMissaoOriginal):
    def __init__(self, entradas_quadro, *, fronteiras=FRONTEIRAS_QUADRO, rastrear=True, **kw):
        self.entradas_quadro = entradas_quadro
        super().__init__(entradas_quadro.base, **kw)
        self.fronteiras = {self.sym[n]: (n, (v, l)) for n, (v, l, _) in fronteiras.items()}
        self.razoes_fronteiras = {n: r for n, (_, _, r) in fronteiras.items()}
        self.eventos_fronteira = []
        self.rastrear = rastrear
        self.rastro = {}
        self.fases = []
        self._passar_uma_vez = set()

    # ------------------------------------------------------------ extension points
    def _criar_windows(self, entradas):
        return WindowsQuadro(entradas, self.entradas_quadro)

    def _importacoes_extras(self):
        w = self.windows
        return ((0x523294, 'USER32.GetCursorPos', 1, w.cursor),
                (0x5232b8, 'USER32.PeekMessageA', 5, w.mensagem))

    def _enderecos_pulo(self):
        if self.fase in FASES_QUADRO:
            return set(self.pulos) | set(self.fronteiras)
        return set(self.pulos)

    def _pulo(self, eip):
        if self.fase not in FASES_QUADRO:
            return super()._pulo(eip)
        if eip in self.fronteiras:
            return self.fronteiras[eip]
        if eip in self.pulos:
            self._interromper('undeclared_frame_boundary', callee=self.pulos[eip][0])
        return None

    def _registrar_pulo(self, nome, retorno, valor, limpeza):
        if self.fase not in FASES_QUADRO:
            return super()._registrar_pulo(nome, retorno, valor, limpeza)
        regs = self._registros()
        pilha = struct.unpack('<4I', self.cpu.mem_read(regs['ESP']+4, 16))
        self.eventos_fronteira.append(dict(
            phase=self.fase, routine=nome, caller_return=hex(retorno), caller=self.nome(retorno),
            top_callee=self._topo[0] if self._topo else None,
            registers={k: hex(regs[k]) for k in ('EAX', 'EDX', 'EBX', 'ECX')},
            stack_words=[hex(v) for v in pilha], declared_eax=valor, stack_cleanup=limpeza,
            guards={hex(g): self.cpu.mem_read(g, 1)[0] for g in GUARDAS_FRONTEIRA.get(nome, ())}))

    def _correr(self, rotulo, entrada, registradores, paradas, retomar=False):
        iso = getattr(self, 'isolamento', None)
        if iso is None or not iso.ativo or not retomar:
            return super()._correr(rotulo, entrada, registradores, paradas, retomar)
        while True:
            regs = super()._correr(rotulo, entrada, registradores, tuple(paradas)+tuple(iso.entradas), True)
            if regs['EIP'] not in iso.entradas or regs['EIP'] in paradas:
                return regs
            iso.executar(regs)
            entrada = regs['EIP']
            self._retomando = {entrada}
            # The entry stays a stop address: let its hook pass once so the
            # resumed phase executes the routine instead of stopping again.
            self._passar_uma_vez.add(entrada)

    def _parar_se_pedido(self, cpu, endereco, tamanho, _):
        if endereco in self._passar_uma_vez:
            self._passar_uma_vez.discard(endereco)
            return
        super()._parar_se_pedido(cpu, endereco, tamanho, _)

    # ------------------------------------------------------------ entry trace
    def _ganchar_quadros(self):
        enderecos = set(self.fronteiras) | {CALCUL_GAME, RETORNO_CALCUL_GAME, SAIDA_LACO}
        for a in sorted(enderecos - set(self.pulos)):
            self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._parar_se_pedido, begin=a, end=a)
        self._simbolos = set(self.nomes)
        self._topo, self._ultimo_bloco = None, None
        if self.rastrear:
            self.cpu.hook_add(unicorn.UC_HOOK_BLOCK, self._bloco, begin=0x401000, end=0x493bff)
        # Unicorn instruments hooks when a block is translated: blocks cached
        # during startup/MissionLoad would silently miss hooks added now.
        self.cpu.ctl_flush_tb()

    def iniciar_pegada(self):
        super().iniciar_pegada()
        self.escritas_por_fase = {}

    def _pegada_ler(self, cpu, acesso, endereco, tamanho, valor, r):
        base, escrito, lido, leitor = r
        o = endereco-base
        for i in range(o, min(o+tamanho, len(escrito))):
            if not escrito[i] and not lido[i]:
                lido[i] = 1
                leitor[i] = (cpu.reg_read(x86.UC_X86_REG_EIP), self.fase)

    def pegada(self):
        """Read-before-write byte ranges: [(start, end, first_reader_routine, phase)]."""
        self._marcar_escritas_vinculos()
        faixas = []
        for base, _, lido, leitor in self._pegada:
            i, n = 0, len(lido)
            while True:
                i = lido.find(1, i)
                if i < 0:
                    break
                j = i
                while j < n and lido[j] and leitor[j] == leitor[i]:
                    j += 1
                faixas.append((base+i, base+j, self.nome(leitor[i][0]), leitor[i][1]))
                i = j
        return faixas

    def marcar_escritas_fase(self):
        """Cumulative written-byte counts per footprint region at the end of a phase."""
        self._marcar_escritas_vinculos()
        self.escritas_por_fase[self.fase] = {hex(base): escrito.count(1) for base, escrito, _, _ in self._pegada}

    def _leitura_vigiada(self, cpu, acesso, endereco, tamanho, valor, _):
        if self.fase in FASES_QUADRO:
            eip = cpu.reg_read(x86.UC_X86_REG_EIP)
            self.leituras_vigiadas[(endereco, tamanho, self.nome(eip), self.fase)] += 1

    def _raiz(self, retorno):
        if self.fase == 'between_frames':
            return self.sym['ProgIteration'] <= retorno < 0x47509d or 0x460170 <= retorno < 0x46027c
        return CALCUL_GAME <= retorno < 0x42d4f8

    def _bloco(self, cpu, endereco, tamanho, _):
        if self.fase not in FASES_QUADRO:
            return
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        chave = (endereco, esp)
        repetido = chave == self._ultimo_bloco
        self._ultimo_bloco = chave
        if endereco not in self._simbolos or repetido:
            return
        retorno = struct.unpack('<I', cpu.mem_read(esp, 4))[0]
        nome = self.nomes[endereco]
        fase = self.rastro.setdefault(self.fase, dict(order=[], top=[], top_index={}))
        if self._raiz(retorno):
            self._topo = (nome, retorno)
            if self._topo not in fase['top_index']:
                fase['top_index'][self._topo] = len(fase['top'])
                fase['top'].append(dict(callee=nome, call_return=hex(retorno), calls=0, nested={}))
            fase['top'][fase['top_index'][self._topo]]['calls'] += 1
            alvo = None
        else:
            alvo = fase['top'][fase['top_index'][self._topo]]['nested'] if self._topo in fase['top_index'] else None
        if nome not in fase['order']:
            fase['order'].append(nome)
        fase.setdefault('counts', {})
        fase['counts'][nome] = fase['counts'].get(nome, 0)+1
        if alvo is not None:
            alvo[nome] = alvo.get(nome, 0)+1

    def rastro_json(self):
        saida = {}
        fronteiras = {n for n, _ in self.fronteiras.values()}
        def item(n, c):
            d = dict(routine=n, entries=c)
            if n in fronteiras:
                d['not_executed_boundary'] = True
            return d
        for fase, r in self.rastro.items():
            saida[fase] = dict(
                routines_in_first_entry_order=[item(n, r['counts'][n]) for n in r['order']],
                top_level=[dict(item(t['callee'], t['calls']), call_return=t['call_return'],
                                caller=self.nome(int(t['call_return'], 16)),
                                nested_first_entry_order=[item(n, c) for n, c in t['nested'].items()])
                           for t in r['top']])
        return saida

    # ------------------------------------------------------------ phases
    def _fase(self, nome):
        self.fase = nome
        self.windows.fase = nome
        self._topo = None

    def _estado_fase(self):
        regs = self._registros()
        return dict(registers={k: hex(v) for k, v in regs.items()},
                    rng={hex(a): hex(struct.unpack('<I', self.cpu.mem_read(a, 4))[0]) for a in RNG},
                    bindings=len(self.vinculos_declarados.eventos), boundaries=len(self.eventos_fronteira),
                    windows_answers=len(self.windows.consumidos), allocations=len(self.arena.ordem),
                    segments=self.execucoes)

    def executar_cauda_carga(self, segundos):
        """(a) From the MissionLoad return 0x42d22d to the load-state CalculGame RET."""
        if self.cpu.reg_read(x86.UC_X86_REG_EIP) != RETORNO_MISSION_LOAD or self.fase != 'oracle':
            raise RuntimeError('The load tail starts only at the real MissionLoad return')
        self._ganchar_quadros()
        self._fase('load_tail')
        self.limite_segundos = segundos
        self.iniciar_relogio()
        return self._correr('load_tail', RETORNO_MISSION_LOAD, {}, (RETORNO,), retomar=True)

    def quadro_chamador(self):
        """Declared ProgIteration/_WinMain@16 stack slots above the CalculGame return slot."""
        esp = self.cpu.reg_read(x86.UC_X86_REG_ESP)
        if esp != PILHA+0x8004 or self.cpu.reg_read(x86.UC_X86_REG_EIP) != RETORNO:
            raise RuntimeError('The caller frame is declared only after the load-state CalculGame RET')
        r = self.entradas_quadro.registradores_chamador
        palavras = [(0x8, r['EDX'], 'ProgIteration saved EDX (push edx 0x475010)'),
                    (0xc, r['ECX'], 'ProgIteration saved ECX (push ecx 0x47500f)'),
                    (0x10, 0, 'ProgIteration saved EBX (push ebx 0x47500e): _WinMain@16 EBX is 0 from 0x4601af'),
                    (0x14, RETORNO_PROG_ITERATION, 'return of CALL ProgIteration 0x46020d')]
        for deslocamento, valor, _ in palavras:
            self.cpu.mem_write(esp+deslocamento, struct.pack('<I', valor))
        for nome in ('ESI', 'EDI', 'EBP'):
            self.cpu.reg_write(getattr(x86, 'UC_X86_REG_'+nome), r[nome])
        self.cpu.reg_write(x86.UC_X86_REG_EBX, 0)
        return dict(esp=hex(esp), words=[dict(address=hex(esp+d), value=hex(v), provenance=p) for d, v, p in palavras],
                    untouched=dict(point=[hex(esp), hex(esp+8)], msg=[hex(esp+0x18), hex(esp+0x34)],
                                   note='POINT local (rewritten by GetCursorPos before any read) and _WinMain@16 '
                                        'MSG buffer keep the bench stack bytes; reads are measured by the footprint'),
                    registers=dict(EBX='0x0', **{k: hex(r[k]) for k in ('ESI', 'EDI', 'EBP')}),
                    eax_kept=hex(self.cpu.reg_read(x86.UC_X86_REG_EAX)))

    def executar_entre_quadros(self, segundos):
        """(b) ProgIteration 0x475063 .. window loop .. ProgIteration .. CalculGame entry."""
        self.declaracao_chamador = self.quadro_chamador()
        self._fase('between_frames')
        self.limite_segundos = segundos
        self.iniciar_relogio()
        regs = self._correr('between_frames', RETORNO_CALCUL_GAME, {}, (CALCUL_GAME, SAIDA_LACO), retomar=True)
        if regs['EIP'] != CALCUL_GAME:
            self._interromper('window_loop_exit', eip=hex(regs['EIP']))
        retorno = struct.unpack('<I', self.cpu.mem_read(regs['ESP'], 4))[0]
        if retorno != RETORNO_CALCUL_GAME:
            self._interromper('calculgame_not_entered_from_progiteration', stack_return=hex(retorno))
        return regs

    def executar_quadro(self, segundos):
        """(c) The first game-state CalculGame frame to its real return 0x475063."""
        if self.cpu.reg_read(x86.UC_X86_REG_EIP) != CALCUL_GAME or self.fase != 'between_frames':
            raise RuntimeError('Frame 1 starts only at the CalculGame entry reached from ProgIteration')
        self._fase('frame1')
        self.limite_segundos = segundos
        self.iniciar_relogio()
        self._retomando = {CALCUL_GAME}
        return self._correr('frame1', CALCUL_GAME, {}, (RETORNO_CALCUL_GAME,), retomar=True)

    # ------------------------------------------------------------ evidence helpers
    def conjunto_vigiado_quadro(self):
        """Static absolute DGROUP stores of every frame-phase non-executed routine."""
        ler = lambda a, n: bytes(self.cpu.mem_read(a, n))
        parar = {self.sym['MenuInit'], self.sym['CalculGame']}
        origem = {}
        for nome in NAO_EXECUTADOS_QUADRO:
            for endereco, tamanho, indexado, _ in escritas_estaticas(ler, self._ordenados, self.nomes,
                                                                     self.sym[nome], parar):
                origem.setdefault((endereco, tamanho, indexado), set()).add(nome)
        return {k: sorted(v) for k, v in origem.items()}

    def sitios_escrita(self, lidos):
        """Static store sites (routine, instruction) of non-executed routines covering each read."""
        ler = lambda a, n: bytes(self.cpu.mem_read(a, n))
        parar = {self.sym['MenuInit'], self.sym['CalculGame']}
        saida = {}
        for nome in NAO_EXECUTADOS_QUADRO:
            for endereco, tamanho, indexado, sitio in escritas_estaticas(ler, self._ordenados, self.nomes,
                                                                         self.sym[nome], parar):
                for a, n in lidos:
                    if endereco < a+n and a < endereco+tamanho:
                        saida.setdefault((a, n), set()).add((nome, self.nome(sitio), hex(sitio), indexado))
        return {k: sorted(v) for k, v in saida.items()}

    def politica_fronteiras(self):
        """Static evidence for each boundary: own RET cleanup and caller EAX use."""
        ler = lambda a, n: bytes(self.cpu.mem_read(a, n))
        saida = {}
        for endereco, (nome, (valor, limpeza)) in sorted(self.fronteiras.items(), key=lambda x: x[1][0]):
            rets, abertos = retornos_alcancaveis(ler, endereco)
            estatico = dict(reachable_ret_immediates=rets, unresolved=abertos,
                            cleanup_matches=not abertos and rets == [limpeza])
            saida[nome] = dict(address=hex(endereco), declared_eax=valor, declared_cleanup=limpeza,
                               reason=self.razoes_fronteiras[nome], static=estatico)
        return saida

    def uso_eax_retorno(self):
        ler = lambda a, n: bytes(self.cpu.mem_read(a, n))
        vistos = {}
        for ev in self.eventos_fronteira:
            chave = (ev['routine'], ev['caller_return'])
            if chave not in vistos:
                vistos[chave] = eax_lido_pelo_chamador(ler, int(ev['caller_return'], 16))
        return [dict(routine=r, caller_return=c, caller=self.nome(int(c, 16)), declared_eax=self.fronteiras[self.sym[r]][1][0],
                     after_return=v[0], at=v[1], instruction=v[2]) for (r, c), v in sorted(vistos.items())]


class Isolamento:
    """Pause a phase at routine entries and run each call in isolation.

    At a declared entry the bench saves the CPU context and every state block
    (DGROUP+.bss, CRT thread page, active allocations, native stack), runs the
    intact routine natively to its stack return address under local
    read/write hooks, records AL/EAX, registers, written bytes and the bytes
    read before written (with their entry values), restores the exact saved
    state, and repeats for each declared perturbation.  The phase then resumes
    from the restored entry and executes the routine as usual.  A binding or
    boundary inside an isolated call stops the run.
    """
    def __init__(self, bancada, rotinas, perturbacoes=None, observador=None):
        self.b = bancada
        self.observador = observador   # f(routine, case, blocks before the call, result) after each case
        self.entradas = {bancada.sym[n]: n for n in rotinas}
        self.perturbacoes = perturbacoes or {}
        self.registros = []
        self.ativo = True

    def instalar(self):
        for a in self.entradas:
            self.b.cpu.hook_add(unicorn.UC_HOOK_CODE, self.b._parar_se_pedido, begin=a, end=a)
        self.b.cpu.ctl_flush_tb()
        self.b.isolamento = self

    def _salvar(self):
        blocos = self.b.imagem()
        blocos['native_stack'] = (PILHA, bytes(self.b.cpu.mem_read(PILHA, 0x10000)))
        return self.b.cpu.context_save(), blocos

    def _restaurar(self, contexto, blocos):
        for base, dados in blocos.values():
            self.b.cpu.mem_write(base, dados)
        self.b.cpu.context_restore(contexto)

    def _rastrear(self, blocos):
        lidos, escritos = {}, set()
        def ler(cpu, acesso, endereco, tamanho, valor, _):
            for a in range(endereco, endereco+tamanho):
                if a not in escritos and a not in lidos:
                    lidos[a] = cpu.reg_read(x86.UC_X86_REG_EIP)
        def escrever(cpu, acesso, endereco, tamanho, valor, _):
            escritos.update(range(endereco, endereco+tamanho))
        # Four merged regions (one hook pair per allocation would make every
        # access scan ~1,800 hooks): DGROUP+.bss, CRT thread page, the arena
        # up to its next free page, the native stack.
        a = self.b.arena
        regioes = ((DGROUP[0], DGROUP[1]), (DADOS_THREAD_CRT, DADOS_THREAD_CRT+0x1000), (a.base, a.proximo),
                   (PILHA, PILHA+0x10000))
        ganchos = []
        for inicio, fim in regioes:
            ganchos.append(self.b.cpu.hook_add(unicorn.UC_HOOK_MEM_READ, ler, None, begin=inicio, end=fim-1))
            ganchos.append(self.b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, escrever, None, begin=inicio, end=fim-1))
        self.b.cpu.ctl_flush_tb()
        return lidos, escritos, ganchos

    def _valor(self, blocos, endereco):
        for base, dados in blocos.values():
            if base <= endereco < base+len(dados):
                return dados[endereco-base]
        return None   # freed or unallocated arena page: no declared block holds it

    def executar(self, regs):
        b, entrada = self.b, regs['EIP']
        nome, fase = self.entradas[entrada], b.fase
        retorno = struct.unpack('<I', b.cpu.mem_read(regs['ESP'], 4))[0]
        contexto, blocos = self._salvar()
        casos = [dict(case='captured_inputs', writes=[], registers={})] + list(self.perturbacoes.get(nome, ()))
        resultados = []
        self.ativo = False
        b.fase = 'isolated'
        try:
            for caso in casos:
                self._restaurar(contexto, blocos)
                for endereco, dados in caso['writes']:
                    b.cpu.mem_write(endereco, bytes(dados))
                for registro, valor in caso['registers'].items():
                    b.cpu.reg_write(getattr(x86, 'UC_X86_REG_'+registro), valor)
                antes = {k: v for k, v in self._salvar()[1].items()}
                eventos, fronteiras = len(b.vinculos_declarados.eventos), len(b.eventos_fronteira)
                lidos, escritos, ganchos = self._rastrear(blocos)
                # Stops are address-scoped hooks: the return address needs its own.
                ganchos.append(b.cpu.hook_add(unicorn.UC_HOOK_CODE, b._parar_se_pedido, begin=retorno, end=retorno))
                b.cpu.ctl_flush_tb()
                try:
                    b._retomando = {entrada}
                    saida = BancadaCargaMissaoOriginal._correr(b, 'isolated', entrada, {}, (retorno,), retomar=True)
                finally:
                    for g in ganchos:
                        b.cpu.hook_del(g)
                    b.cpu.ctl_flush_tb()
                if len(b.vinculos_declarados.eventos) != eventos or len(b.eventos_fronteira) != fronteiras:
                    b._interromper('binding_or_boundary_in_isolated_call', routine=nome, case=caso['case'])
                depois = self._salvar()[1]
                mudados = {}
                for n, (base, dados) in depois.items():
                    if n == 'native_stack':
                        continue
                    velho = antes[n][1]
                    if dados != velho:
                        mudados.update({base+i: (velho[i], dados[i]) for i in range(len(dados)) if dados[i] != velho[i]})
                pilha_sp = saida['ESP']
                leituras = sorted(a for a in lidos if not (PILHA <= a < pilha_sp))
                resultados.append(dict(
                    case=caso['case'], perturbation=dict(writes=[[hex(a), bytes(d).hex()] for a, d in caso['writes']],
                                                         registers={k: hex(v) for k, v in caso['registers'].items()}),
                    entry_registers={k: hex(v) for k, v in regs.items()},
                    exit_registers={k: hex(v) for k, v in saida.items()}, al=saida['EAX'] & 0xff,
                    reached_return=saida['EIP'] == retorno,
                    changed_bytes=[[hex(a), v[0], v[1]] for a, v in sorted(mudados.items())],
                    read_before_write=[[hex(a), self._valor(antes, a), b.nome(lidos[a])] for a in leituras]))
                if self.observador is not None:
                    self.observador(nome, fase, caso, antes, resultados[-1])
        finally:
            self._restaurar(contexto, blocos)
            b.fase = fase
            self.ativo = True
        self.registros.append(dict(routine=nome, entry=hex(entrada), phase=fase, caller_return=hex(retorno),
                                   caller=b.nome(retorno), cases=resultados))
