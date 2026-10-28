"""Whole-MissionLoad original oracle started from the original program start.

The bench runs the intact executable on Core's BancadaX86 and its committed
Stage16 binding transport. For speed it replaces Core's per-instruction Python
checker with equivalent native guards (address-scoped stop hooks, data/stack/
arena pages without execute permission, instruction-count segments resumed at
the same instruction). A *startup* phase
executes the original new-campaign path (AppInit/ProgInit, main menu,
campaign menu, research screen and the CalculGame load frame) so that the
state inherited by MissionLoad 0x46c2cf is produced by original code rather
than by fixture constructors. Startup calls whose bodies require DirectDraw,
CD audio, cursor drawing or other display/window semantics are *not executed*:
the bench stops at their entry, records the skip and returns to the caller with
EAX either unchanged or a declared value. Every skipped write set is watched
for reads during MissionLoad.

The *oracle* phase begins at the real CALL from CalculGame 0x42d228 and ends
at the real return 0x42d22d. During it no call may be skipped: reaching a
display boundary, an undeclared import or any fault stops the run with all
state retained. Only the declared external bindings (fronteiras_carga_missao)
answer calls. Importing this module executes nothing.
"""
from bisect import bisect_right
from collections import Counter
import hashlib
import struct
import time
import zlib
import base64

import ambiente_missoes
from emulador import BancadaX86, DESCRITORES, PILHA, RETORNO, TRAMPOLINS_DECLARADOS as TRAMPOLINS, unicorn, x86
from vinculos_declarados import ArgumentoVinculo
from fronteiras_carga_missao import (ArenaAlocacoes, ArquivosCRT, ArquivosWin32, MidiaOriginal,
                                     PerfilWindows, WindowsDeclarado)

DGROUP = (0x494000, 0x523000)
ARENA = (0x40000000, 0x50000000)
ARMADILHAS = 0x3300000
DADOS_THREAD_CRT = 0x3400000   # declared home of the CRT main-thread data block
TAMANHO_DADOS_THREAD = 0xe4     # [0x49945c]=0xe2 rounded to 4 by __WinMain 0x48fe17
MISSION_LOAD, RETORNO_MISSION_LOAD = 0x46c2cf, 0x42d22d

SIMBOLOS = ambiente_missoes.ROOT / 'relatorios/simbolos-originais.tsv'


def simbolos():
    tabela = {}
    for linha in SIMBOLOS.read_text().splitlines()[1:]:
        endereco, nome = linha.split('\t')[:2]
        tabela[nome] = int(endereco, 16)
    return tabela


# Startup-only display/audio/UI routines not executed: name -> (declared EAX or
# None=unchanged, callee stack cleanup in bytes from the routine's own RET imm16:
# FilledBox shares Box's `ret 8` at 0x45caca, AffText ends with `ret 0x10`; all
# others end with a plain RET). Reason: each requires DirectDraw surfaces,
# MCI CD audio, screen drawing or sprite/menu bitmap banks.
PULOS_INICIO = {
    'AffInit': (None, 0), 'DDSetPalette': (None, 0), 'DDLockSurface': (0, 0),
    'DDUnlockSurface': (None, 0), 'DDFlipPage': (None, 0), 'LoadPie': (None, 0),
    'FilledBox': (None, 8), 'ResetMode': (None, 0), 'AffText': (None, 0x10),
    'MCICD_Play': (None, 0), 'MCICD_Stop': (None, 0), 'PlayVideo': (None, 0),
    'CreateCredits': (None, 0), 'FreeCredits': (None, 0),
    # Text resources: InitTextLangue reads TEXTES.TXT with FileReadLine 0x4584a3
    # (CRT fgets), which is not an inventoried I/O boundary; menu text lookups
    # therefore return a declared NULL pointer that only menu UI tables store.
    'InitTextLangue': (None, 0), 'TextGetMessage': (0, 0),
    # Sprite/menu graphic banks (24k allocations of display bitmaps).
    'LoadSTRATBank': (0, 0), 'SetBank': (None, 0), 'LoadBank': (0, 0), 'DeleteBank': (None, 0),
}


# Original routines whose effects are absent from the derived startup state:
# every skipped startup call plus program-start/frame routines that the
# startup driver does not run (window creation, sound/CD init, per-frame
# display and the window procedure). Their static absolute DGROUP write sets
# are watched for reads during the oracle phase.
NAO_EXECUTADOS = tuple(PULOS_INICIO) + ('AppWindowInit', 'DisableIME', 'PlaySnd_InitSoundLib',
                                        'MCICD_Init', 'AffGame', 'WndProc')
# ProgIteration's own per-frame stores (frame counters, cursor position);
# its callees CalculGame/AffGame are handled separately.
ESCRITAS_PROG_ITERATION = ((0x508f7c, 4), (0x508f80, 4), (0x508f84, 4), (0x5099a8, 2), (0x5099aa, 2),
                           (0x5099ae, 1), (0x5099af, 1), (0x5099b1, 1), (0x5099b2, 1))


def escritas_estaticas(imagem_codigo, simbolos_ordenados, nomes, raiz, parar=()):
    """Static absolute DGROUP destinations reachable from ``raiz`` (direct CALLs).

    Diagnostic over-approximation: indexed absolute stores record only their
    base; stores through registers/pointers are not covered (they target
    allocations that skipped routines never created, so a dereference faults).
    """
    import capstone
    from capstone import x86_const as X
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True

    def fim(a):
        i = bisect_right(simbolos_ordenados, a)
        return simbolos_ordenados[i] if i < len(simbolos_ordenados) else a+0x400
    vistos, pilha, saida = set(), [raiz], []
    while pilha:
        a = pilha.pop()
        if a in vistos or not 0x401000 <= a < 0x493c00:
            continue
        vistos.add(a)
        for ins in md.disasm(imagem_codigo(a, fim(a)-a), a):
            if ins.mnemonic == 'call' and ins.operands and ins.operands[0].type == X.X86_OP_IMM:
                alvo = ins.operands[0].imm
                i = bisect_right(simbolos_ordenados, alvo)-1
                if i >= 0 and simbolos_ordenados[i] not in parar:
                    pilha.append(simbolos_ordenados[i])
            for op in ins.operands:
                if (op.type == X.X86_OP_MEM and op.access & capstone.CS_AC_WRITE and op.mem.base == 0
                        and DGROUP[0] <= op.mem.disp < DGROUP[1]):
                    saida.append((op.mem.disp, op.size, op.mem.index != 0, ins.address))
    return saida


class OraculoInterrompido(RuntimeError):
    def __init__(self, motivo, detalhe):
        self.motivo, self.detalhe = motivo, detalhe
        super().__init__(f'{motivo}: {detalhe}')


class BancadaCargaMissaoOriginal(BancadaX86):
    def __init__(self, entradas, *, segundos=300.0, instrucoes_segmento=1000000,
                 segmentos=200000, vinculos=200000, alocacoes=60000, pulos=PULOS_INICIO):
        super().__init__()
        # Core's generic per-instruction Python checker would make a whole
        # program-start run cost minutes per 100M instructions. This bench
        # replaces it by equivalent native guards: address-scoped stop hooks
        # and non-executable data/arena/stack pages (any fetch outside the
        # original code section faults with UC_ERR_FETCH_PROT).
        for handle in list(self.cpu._callbacks):
            self.cpu.hook_del(handle)
        self.sym = simbolos()
        self.nomes = {v: k for k, v in self.sym.items()}
        self._ordenados = sorted(self.nomes)
        self.entradas = entradas
        self.limite_segundos, self.instrucoes_segmento = segundos, instrucoes_segmento
        self.limite_segmentos, self.limite_vinculos_total = segmentos, vinculos
        self.midia = MidiaOriginal(entradas)
        self.arena = ArenaAlocacoes(self.cpu, *ARENA, alocacoes, entradas.preenchimento_alocacao)
        self.arquivos = ArquivosCRT(self.midia)
        self.arquivos_win32 = ArquivosWin32(self.midia)
        self.perfil = PerfilWindows(self.midia)
        self.windows = WindowsDeclarado(entradas)
        self.intervalos = sorted(self.vinculos_declarados.codigo_protegido)
        self._inicios = [a for a, _ in self.intervalos]
        self._fins = [b for _, b in self.intervalos]
        self.pulos = {self.sym[n]: (n, v) for n, v in pulos.items()}
        self.eventos_pulados, self.fase = [], 'startup'
        self.segmentos_retomados = 0
        self.passos, self._pedidas, self._retomando = [], set(), set()
        self._pegada, self._eventos_vistos = None, 0
        self._inicio, self._seg0 = time.monotonic(), 0
        self._declarar()
        self._proteger_e_ganchar()

    # ------------------------------------------------------------ bindings
    def _declarar(self):
        a = self.arena
        w = self.windows
        self.declarar_vinculo(0x48c71f, 'CRT.fopen', ('EAX', 'EDX'), self.arquivos.fopen, natureza='io')
        self.declarar_vinculo(0x48c97b, 'CRT.fread', ('EAX', 'EDX', 'EBX', 'ECX'), self.arquivos.fread,
                              natureza='io')
        self.declarar_vinculo(0x48c80b, 'CRT.fclose', ('EAX',), self.arquivos.fclose, natureza='io')
        self.declarar_vinculo(0x45848b, 'FileSeek', ('EAX', ArgumentoVinculo('EDX', 8)),
                              self.arquivos.file_seek, natureza='io')
        for slot, nome, argc, atender in (
                (0x5231c0, 'KERNEL32.GlobalAlloc', 2, a.alocar),
                (0x5231d0, 'KERNEL32.GlobalLock', 1, a.fixar),
                (0x5231cc, 'KERNEL32.GlobalHandle', 1, a.handle),
                (0x5231d8, 'KERNEL32.GlobalUnlock', 1, a.desfixar),
                (0x5231c8, 'KERNEL32.GlobalFree', 1, a.liberar),
                (0x5231d4, 'KERNEL32.GlobalMemoryStatus', 1, w.estado_memoria),
                (0x5231c4, 'KERNEL32.GlobalCompact', 1, w.constante(0x1000000, 'declared largest free block')),
                (0x5231ac, 'KERNEL32.GetPrivateProfileIntA', 4, self.perfil.inteiro),
                (0x5231b0, 'KERNEL32.GetPrivateProfileStringA', 6, self.perfil.texto),
                (0x5231e4, 'KERNEL32.SetErrorMode', 1, w.constante(0, 'declared previous mode 0')),
                (0x5231a8, 'KERNEL32.GetDriveTypeA', 1, w.tipo_unidade),
                (0x5231bc, 'KERNEL32.GetVolumeInformationA', 8, w.volume),
                (0x5233d4, 'KERNEL32.GetCurrentDirectoryA', 2, w.diretorio),
                (0x5234a4, 'WINMM.timeGetTime', 0, w.tempo),
                (0x5231b8, 'KERNEL32.GetTickCount', 0, w.tempo),
                (0x5233dc, 'KERNEL32.GetCurrentThreadId', 0, w.constante(self.entradas.id_thread, 'declared thread id')),
                (0x5233b4, 'KERNEL32.CreateFileA', 7, self.arquivos_win32.criar),
                (0x52340c, 'KERNEL32.ReadFile', 5, self.arquivos_win32.ler),
                (0x523424, 'KERNEL32.SetFilePointer', 4, self.arquivos_win32.posicionar),
                (0x5233ac, 'KERNEL32.CloseHandle', 1, self.arquivos_win32.fechar),
                (0x5233e8, 'KERNEL32.GetFileType', 1, self.arquivos_win32.tipo),
                (0x5233ec, 'KERNEL32.GetLastError', 0, self.arquivos_win32.erro),
                (0x5233fc, 'KERNEL32.GetStdHandle', 1, w.constante(0, 'declared GUI process: no standard handle')),
                (0x52343c, 'KERNEL32.VirtualAlloc', 4, a.reservar),
                (0x5232d0, 'USER32.ShowCursor', 1, w.constante(0, 'declared display counter 0')),
                (0x5232c8, 'USER32.SetCursorPos', 2, w.constante(1, 'declared success')),
                (0x523290, 'USER32.GetAsyncKeyState', 1, w.tecla)):
            self.declarar_importacao(slot, nome, argc, atender)
        # Every other import slot points at a private trap: reaching it is a
        # visible unsupported boundary, never a call into unmapped hint data.
        declarados = {int(x['iat'], 16) for x in self.importacoes_declaradas}
        self.armadilhas = {}
        self.cpu.mem_map(ARMADILHAS, 0x1000)
        self.cpu.mem_write(ARMADILHAS, b'\xc3'*0x1000)
        for i, (slot, meta) in enumerate(sorted(self.importacoes_originais.items())):
            if slot in declarados:
                continue
            alvo = ARMADILHAS+4*i
            self.armadilhas[alvo] = f"{meta['dll']}.{meta['symbol']}"
            self.cpu.mem_write(slot, struct.pack('<I', alvo))

    # ------------------------------------------------------------ execution
    def nome(self, endereco):
        i = bisect_right(self._ordenados, endereco)-1
        if i < 0:
            return hex(endereco)
        base = self._ordenados[i]
        return self.nomes[base]+('' if base == endereco else f'+0x{endereco-base:x}')

    def _proteger_e_ganchar(self):
        rw = unicorn.UC_PROT_READ | unicorn.UC_PROT_WRITE
        rx = unicorn.UC_PROT_READ | unicorn.UC_PROT_EXEC
        codigo = self.intervalos
        if codigo != [(0x401000, 0x493c00)]:
            raise ValueError('Unexpected original code section layout')
        # Image layout (SizeOfImage 0x12e000): headers R, BEGTEXT R|X (its last
        # page tail is zero padding), DGROUP+.bss RW, .idata RW (IAT slots are
        # data), .reloc/.rsrc R; the mapped tail beyond the image has no access.
        self.cpu.mem_protect(0x400000, 0x1000, unicorn.UC_PROT_READ)
        self.cpu.mem_protect(0x401000, 0x494000-0x401000, rx)
        self.cpu.mem_protect(0x494000, 0x524000-0x494000, rw)
        self.cpu.mem_protect(0x524000, 0x52e000-0x524000, unicorn.UC_PROT_READ)
        self.cpu.mem_protect(0x52e000, 0x600000-0x52e000, unicorn.UC_PROT_NONE)
        for inicio, fim, _ in list(self.cpu.mem_regions()):
            if inicio >= 0x1000000 and inicio not in (RETORNO, ARMADILHAS, TRAMPOLINS):
                self.cpu.mem_protect(inicio, fim-inicio+1, rw)
        self.sha256_codigo_exe = hashlib.sha256(self._bytes_codigo_exe()).hexdigest()
        self.sha256_codigo_inicial = self.sha256_codigo()
        if self.sha256_codigo_inicial != self.sha256_codigo_exe:
            raise ValueError('Mapped code section differs from the intact executable bytes')
        enderecos = set(self.vinculos_declarados.vinculos) | set(self.pulos) | {
            MISSION_LOAD, RETORNO_MISSION_LOAD}
        for a in sorted(enderecos):
            self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._parar_se_pedido, begin=a, end=a)
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._parar_se_pedido, begin=ARMADILHAS, end=ARMADILHAS+0xfff)

    @staticmethod
    def _bytes_codigo_exe():
        dados = (ambiente_missoes.CD/'INSTALHD/RISING.EXE').read_bytes()
        return dados[0x400:0x400+0x92c00]   # BEGTEXT raw offset/size

    def sha256_codigo(self):
        return hashlib.sha256(bytes(self.cpu.mem_read(0x401000, 0x92c00))).hexdigest()

    def _parar_se_pedido(self, cpu, endereco, tamanho, _):
        if endereco in self.paradas or endereco in self.armadilhas:
            cpu.emu_stop()

    def _registros(self):
        return {n: self.cpu.reg_read(getattr(x86, 'UC_X86_REG_'+n))
                for n in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP', 'EFLAGS')}

    def pilha_provavel(self, esp, palavras=512):
        """Diagnostic only: stack words that follow a CALL in original code."""
        achados = []
        try:
            dados = bytes(self.cpu.mem_read(esp, 4*palavras))
        except unicorn.UcError:
            return achados
        for i in range(palavras):
            v = struct.unpack_from('<I', dados, 4*i)[0]
            if 0x401000 <= v < 0x4a0000:
                antes = bytes(self.cpu.mem_read(v-7, 7))
                if antes[2] == 0xe8 or antes[1:3] == b'\xff\x15' or antes[0:2] == b'\x2e\xff':
                    achados.append(f'+{4*i:x}:{self.nome(v)}')
        return achados[:24]

    def _interromper(self, motivo, **detalhe):
        regs = self._registros()
        try:
            retorno = struct.unpack('<I', self.cpu.mem_read(regs['ESP'], 4))[0]
        except unicorn.UcError:
            retorno = 0
        detalhe.update(stack_scan=self.pilha_provavel(regs['ESP']))
        detalhe.update(eip=hex(regs['EIP']), routine=self.nome(regs['EIP']),
                       stack_return=hex(retorno), stack_return_routine=self.nome(retorno),
                       registers={k: hex(v) for k, v in regs.items()}, phase=self.fase)
        raise OraculoInterrompido(motivo, detalhe)

    def _executar_ate_parada(self, entrada, limite_instrucoes):
        if self._pegada is not None:
            self._marcar_escritas_vinculos()
        while True:
            restante = self.limite_segundos-(time.monotonic()-self._inicio)
            if restante <= 0:
                self._interromper('wall_budget_exhausted', seconds=self.limite_segundos)
            if self.execucoes-self._seg0 > self.limite_segmentos:
                self._interromper('segment_budget_exhausted', segments=self.limite_segmentos)
            if entrada in self.paradas and entrada not in self._retomando:
                eip = entrada
            else:
                try:
                    self.cpu.emu_start(entrada, RETORNO, timeout=int(restante*1e6)+1,
                                       count=self.instrucoes_segmento)
                except unicorn.UcError as erro:
                    self._interromper('native_fault', error=str(erro))
                eip = self.cpu.reg_read(x86.UC_X86_REG_EIP)
            self._retomando = set()
            if eip in self.armadilhas:
                self._interromper('undeclared_import', import_name=self.armadilhas[eip])
            if eip in self.pulos and eip not in self._pedidas:
                nome, (valor, limpeza) = self.pulos[eip]
                if self.fase != 'startup':
                    self._interromper('display_boundary_in_oracle', callee=nome)
                esp = self.cpu.reg_read(x86.UC_X86_REG_ESP)
                retorno = struct.unpack('<I', self.cpu.mem_read(esp, 4))[0]
                self.eventos_pulados.append(dict(routine=nome, caller_return=hex(retorno),
                                                 caller=self.nome(retorno), declared_eax=valor,
                                                 stack_cleanup=limpeza))
                if valor is not None:
                    self.cpu.reg_write(x86.UC_X86_REG_EAX, valor)
                self.cpu.reg_write(x86.UC_X86_REG_ESP, esp+4+limpeza)
                self.execucoes += 1
                entrada = retorno
                continue
            if eip in self.paradas:
                return {n: self.cpu.reg_read(getattr(x86, 'UC_X86_REG_'+n))
                        for n in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP')}
            if time.monotonic()-self._inicio >= self.limite_segundos:
                self._interromper('wall_budget_exhausted', seconds=self.limite_segundos)
            # Instruction-count segment end: resume the same instruction with
            # every register, flag and stack byte preserved.
            self.segmentos_retomados += 1
            self.execucoes += 1
            self._retomando = {eip}
            entrada = eip

    def _correr(self, rotulo, entrada, registradores, paradas, retomar=False):
        self._pedidas = set(paradas)
        todas = set(paradas) | set(self.armadilhas) | set(self.pulos)
        if retomar:
            return self.retomar(entrada, self.intervalos, parada=todas,
                                limite_instrucoes=self.instrucoes_segmento,
                                limite_vinculos=self.limite_vinculos_total)
        return self.executar(entrada, self.intervalos, registradores, parada=todas,
                             limite_instrucoes=self.instrucoes_segmento,
                             limite_vinculos=self.limite_vinculos_total)

    # ------------------------------------------------------------ phases
    def iniciar_relogio(self):
        self._inicio = time.monotonic()
        self._seg0 = self.execucoes

    def chamar(self, rotulo, nome, registradores=None, paradas=(RETORNO,)):
        entrada = self.sym[nome]
        regs = self._correr(rotulo, entrada, registradores or {}, paradas)
        self.passos.append(dict(step=rotulo, routine=nome, entry=hex(entrada),
                                registers={k: hex(v) for k, v in (registradores or {}).items()},
                                stop=hex(regs['EIP']), eax=hex(regs['EAX'])))
        return regs

    def preparar_dados_thread_crt(self):
        """Reproduce the CRT main-thread data block setup of __WinMain/__NTInit.

        __WinMain 0x48fe1e..0x48fe2a reserves [0x49945c] bytes rounded to 4 and
        memsets them to zero; __NTInit 0x48e7e9 calls the original
        __InitThreadData on it and stores the result at 0x522244 (0x48e7ee).
        The block lives in a declared page instead of the original main stack.
        The zero fill and the 0x522244 store are documented byte provenance;
        __InitThreadData itself executes natively.
        """
        if struct.unpack('<H', self.cpu.mem_read(0x49945c, 2))[0] != 0xe2:
            raise ValueError('Unexpected CRT thread-data size in the original image')
        self.cpu.mem_map(DADOS_THREAD_CRT, 0x1000)
        self.cpu.mem_write(DADOS_THREAD_CRT, bytes(0x1000))
        regs = self.chamar('crt_thread_data', '__InitThreadData', {'EAX': DADOS_THREAD_CRT})
        if regs['EAX'] != DADOS_THREAD_CRT:
            raise RuntimeError('__InitThreadData did not return the declared block')
        self.cpu.mem_write(0x522244, struct.pack('<I', regs['EAX']))
        self.passos.append(dict(step='crt_thread_pointer_store', documented_store='0x48e7ee',
                                address='0x522244', value=hex(regs['EAX'])))
        # __NTInit 0x48e806 then calls the original file-handle table initializer.
        self.chamar('crt_file_handles', '__NTInitFileHandles')

    def executar_inicio(self, quadros_maximos=8):
        """Original new-campaign path up to the CALL MissionLoad at 0x42d228.

        AppInit runs from WinMain's call (EAX = declared hInstance 0x400000).
        Then CalculGame frames run natively; the declared keyboard script
        (Enter on the default item of menus 2 and 3, Enter on the research
        screen 0x11) drives MenuNewSelect exactly as the original input path.
        ProgIteration/AffGame between frames are not executed (see
        NAO_EXECUTADOS/ESCRITAS_PROG_ITERATION).
        """
        self.preparar_dados_thread_crt()
        self.chamar('appinit', 'AppInit', {'EAX': 0x400000})
        for quadro in range(quadros_maximos):
            estado = self.cpu.mem_read(0x4e2f78, 1)[0]
            regs = self.chamar(f'frame{quadro}_state{estado:#x}', 'CalculGame', {},
                               paradas=(RETORNO, MISSION_LOAD))
            if regs['EIP'] == MISSION_LOAD:
                return regs
        raise RuntimeError('MissionLoad was not reached within the declared frame budget')

    def executar_mission_load(self, segundos, instrucoes_segmento=None):
        """Run the intact MissionLoad from its real caller frame to 0x42d22d."""
        if self.cpu.reg_read(x86.UC_X86_REG_EIP) != MISSION_LOAD:
            raise RuntimeError('The oracle must start at the real MissionLoad entry')
        retorno = struct.unpack('<I', self.cpu.mem_read(self.cpu.reg_read(x86.UC_X86_REG_ESP), 4))[0]
        if retorno != RETORNO_MISSION_LOAD:
            raise RuntimeError('MissionLoad was not entered from CalculGame 0x42d228')
        self.fase, self.limite_segundos = 'oracle', segundos
        if instrucoes_segmento is not None:
            if not 1 <= instrucoes_segmento <= 1000000:
                raise ValueError('Segment size must be within the Core bench bound')
            self.instrucoes_segmento = instrucoes_segmento
        self.iniciar_relogio()
        self.evento_inicio_oraculo = len(self.vinculos_declarados.eventos)
        self.segmentos_inicio_oraculo = self.execucoes
        regs = self._correr('missionload', MISSION_LOAD, {}, (RETORNO_MISSION_LOAD,), retomar=True)
        self.segundos_oraculo = time.monotonic()-self._inicio
        return regs

    def snapshot_entrada(self):
        """First-class MissionLoad entry state: every block, stack, CPU and fixture state."""
        if self.cpu.reg_read(x86.UC_X86_REG_EIP) != MISSION_LOAD or self.fase != 'startup':
            raise RuntimeError('Entry snapshot is defined only at the real MissionLoad entry')
        # ObjectifLoadText 0x47c557 opens the briefing as an existence test and,
        # on success, reopens it at 0x47c5cd without closing the first FILE*:
        # that original leak is recorded, not hidden. No Win32 handle may remain.
        if self.arquivos_win32.abertos:
            raise RuntimeError('A Win32 file handle is still open at MissionLoad entry')
        corrente = struct.unpack('<I', self.cpu.mem_read(0x4e1d1c, 4))[0]
        abertos = [dict(stream=hex(k), path=v['record']['path'], cursor=v['cursor'], reads=v['reads'],
                        referenced_by_0x4e1d1c=k == corrente) for k, v in self.arquivos.abertos.items()]
        regs = self._registros()
        segs = {n: self.cpu.reg_read(getattr(x86, 'UC_X86_REG_'+n)) for n in ('CS', 'DS', 'ES', 'SS', 'FS', 'GS')}
        blocos = self.imagem()
        blocos['native_stack'] = (PILHA, bytes(self.cpu.mem_read(PILHA, 0x10000)))
        return dict(blocks=blocos, registers=regs, segments=segs,
                    gdt=dict(base=hex(DESCRITORES), limit=23,
                             bytes=bytes(self.cpu.mem_read(DESCRITORES, 24)).hex()),
                    arena=dict(base=hex(self.arena.base), limit=hex(self.arena.limite),
                               next_free=hex(self.arena.proximo), fill=self.arena.preenchimento,
                               count_budget=self.arena.maximo, allocations=len(self.arena.ordem),
                               policy='GMEM_FIXED handle==pointer, page-aligned, never reused; '
                                      'ZEROINIT zero else declared fill; VirtualAlloc commit zero'),
                    crt_streams_open=abertos, file_stream_slot_0x4e1d1c=hex(corrente), win32_handles_open=[],
                    crt_next_stream_index=self.arquivos.proximo, win32_next_handle_index=self.arquivos_win32.proximo,
                    remaining_clock=list(self.windows.relogio),
                    remaining_keys=[list(t) for t in self.windows.teclas],
                    stack_return=hex(struct.unpack('<I', self.cpu.mem_read(regs['ESP'], 4))[0]))

    # ------------------------------------------------------------ footprint
    def iniciar_pegada(self):
        """Track inherited bytes read before written during the oracle phase.

        Regions: DGROUP+.bss, the CRT thread page, the native stack and every
        arena byte allocated before MissionLoad. Binding writes (fread etc.)
        mark their destination as written before the next native segment.
        """
        regioes = [(DGROUP[0], DGROUP[1]-DGROUP[0]), (DADOS_THREAD_CRT, 0x1000), (PILHA, 0x10000),
                   (self.arena.base, self.arena.proximo-self.arena.base)]
        self._pegada = []
        for base, tamanho in regioes:
            r = (base, bytearray(tamanho), bytearray(tamanho), {})
            self._pegada.append(r)
            self.cpu.hook_add(unicorn.UC_HOOK_MEM_READ, self._pegada_ler, r, begin=base, end=base+tamanho-1)
            self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._pegada_escrever, r, begin=base, end=base+tamanho-1)
        self._eventos_vistos = len(self.vinculos_declarados.eventos)

    def _pegada_ler(self, cpu, acesso, endereco, tamanho, valor, r):
        base, escrito, lido, leitor = r
        o = endereco-base
        for i in range(o, min(o+tamanho, len(escrito))):
            if not escrito[i] and not lido[i]:
                lido[i] = 1
                leitor[i] = cpu.reg_read(x86.UC_X86_REG_EIP)

    def _pegada_escrever(self, cpu, acesso, endereco, tamanho, valor, r):
        base, escrito = r[0], r[1]
        o = endereco-base
        fim = min(o+tamanho, len(escrito))
        escrito[o:fim] = b'\x01'*(fim-o)

    def _marcar_escritas_vinculos(self):
        eventos = self.vinculos_declarados.eventos
        for ev in eventos[self._eventos_vistos:]:
            for w in ev['memory_writes']:
                a, n = int(w['address'], 16), w['size']
                for base, escrito, _, _ in self._pegada:
                    if base <= a < base+len(escrito):
                        o = a-base
                        escrito[o:min(o+n, len(escrito))] = b'\x01'*(min(o+n, len(escrito))-o)
        self._eventos_vistos = len(eventos)

    def pegada(self):
        """Read-before-write byte ranges: [(start, end, first_reader_routine)]."""
        self._marcar_escritas_vinculos()
        faixas = []
        for base, _, lido, leitor in self._pegada:
            i, n = 0, len(lido)
            while True:
                i = lido.find(1, i)
                if i < 0:
                    break
                j = i
                while j < n and lido[j]:
                    j += 1
                faixas.append((base+i, base+j, self.nome(leitor[i])))
                i = j
        return faixas

    def conjunto_vigiado(self):
        """Byte ranges written by non-executed original routines (see NAO_EXECUTADOS)."""
        ler = lambda a, n: bytes(self.cpu.mem_read(a, n))
        parar = {self.sym['MenuInit'], self.sym['CalculGame']}
        origem = {}
        for nome in NAO_EXECUTADOS:
            for endereco, tamanho, indexado, sitio in escritas_estaticas(
                    ler, self._ordenados, self.nomes, self.sym[nome], parar):
                origem.setdefault((endereco, tamanho, indexado), set()).add(nome)
        for endereco, tamanho in ESCRITAS_PROG_ITERATION:
            origem.setdefault((endereco, tamanho, False), set()).add('ProgIteration')
        return {k: sorted(v) for k, v in origem.items()}

    def vigiar_leituras(self, conjunto):
        intervalos = sorted((a, a+n) for a, n, _ in conjunto)
        unidos = []
        for a, z in intervalos:
            if unidos and a <= unidos[-1][1]:
                unidos[-1][1] = max(unidos[-1][1], z)
            else:
                unidos.append([a, z])
        self.leituras_vigiadas = Counter()
        self.intervalos_vigiados = [tuple(x) for x in unidos]
        for a, z in unidos:
            self.cpu.hook_add(unicorn.UC_HOOK_MEM_READ, self._leitura_vigiada, begin=a, end=z-1)

    def _leitura_vigiada(self, cpu, acesso, endereco, tamanho, valor, _):
        if self.fase == 'oracle':
            eip = cpu.reg_read(x86.UC_X86_REG_EIP)
            self.leituras_vigiadas[(endereco, tamanho, self.nome(eip))] += 1

    def imagem(self):
        blocos = {'dgroup': (DGROUP[0], bytes(self.cpu.mem_read(DGROUP[0], DGROUP[1]-DGROUP[0]))),
                  'crt_thread_data': (DADOS_THREAD_CRT, bytes(self.cpu.mem_read(DADOS_THREAD_CRT,
                                                                                 TAMANHO_DADOS_THREAD)))}
        for r in self.arena.ativos():
            blocos[f"alloc{r['index']:05d}"] = (r['pointer'], bytes(self.cpu.mem_read(r['pointer'], r['size'])))
        return blocos

    @staticmethod
    def serializar(blocos):
        return {nome: dict(base=hex(base), bytes=len(dados), sha256=hashlib.sha256(dados).hexdigest(),
                           zlib_base64=base64.b64encode(zlib.compress(dados, 9)).decode('ascii'))
                for nome, (base, dados) in blocos.items()}

    @staticmethod
    def resumo_imagem(blocos):
        h = hashlib.sha256()
        for nome in sorted(blocos):
            base, dados = blocos[nome]
            h.update(struct.pack('<II', base, len(dados)))
            h.update(dados)
        return dict(blocks=len(blocos), bytes=sum(len(d) for _, d in blocos.values()), sha256=h.hexdigest())
