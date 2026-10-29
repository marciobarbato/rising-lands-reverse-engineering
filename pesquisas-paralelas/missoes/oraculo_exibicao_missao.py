"""Display-executing MONDE01 oracle: startup, MissionLoad and frames 0/1 with the display path run.

Same phases and checks as ``oraculo_quadro_missao``, but the original display
code is *executed* instead of skipped: AffInit/DDInit, LoadPalette,
DDSetPalette, DDLockSurface/DDUnlockSurface, DDFlipPage, FilledBox,
ResetMode, the bank loaders (LoadSTRATBank, SetBank, LoadBank, DeleteBank),
RestoreAll and AffGame.  DirectDraw is Graphics' integrated declared backend
``fronteiras_exibicao.ExibicaoDeclarada`` (DirectDrawCreate and MessageBeep
imports plus COM vtables), installed after the bench's own imports so every
earlier trampoline keeps its address; its surfaces live at 0x60000000.  Still
not executed, each a declared boundary with recorded arguments:

* text resources (InitTextLangue, TextGetMessage, AffText): TEXTES.TXT is read
  with CRT ``fgets`` 0x48ce96, which is not an inventoried I/O boundary;
* LoadPie pictures: ReadLZSImage calls CRT ``fseek`` 0x48cda2, also not
  inventoried;
* video and credits (PlayVideo, CreateCredits, FreeCredits);
* MCI CD audio and the sound library (MCICD_*, PlaySnd_*), never initialized.

Clock answers are declared per call site: the IaAlloc ``iaRandom(0)`` call
(return 0x48978e) keeps the accepted M1 value, so the game RNG seed equals the
v1 scenario; every other timeGetTime/GetTickCount call takes the next value of
the declared display tick sequence.  Importing this module executes nothing.
"""
from dataclasses import dataclass, field
import struct

import ambiente_missoes
from emulador import unicorn, x86
from vinculos_declarados import ParadaVinculoDeclarado
from fronteiras_exibicao import ExibicaoDeclarada
from oraculo_carga_missao import MISSION_LOAD, RETORNO_MISSION_LOAD
from oraculo_quadro_missao import (BancadaQuadroMissaoOriginal, CALCUL_GAME, RETORNO_CALCUL_GAME, SAIDA_LACO,
                                   WindowsQuadro, nomes_fases)

RELOGIO_IA = 0x48978e   # return of the timeGetTime call in iaRandom(0) from IaAlloc
LACO = 0x4601c0         # _WinMain@16 message-loop head (quit-flag test)
SOM = 'sound library; PlaySnd_InitSoundLib never executed'
CD = 'MCI CD audio; MCICD_Init never executed'

TEXTO = 'text resource: TEXTES.TXT needs CRT fgets 0x48ce96, not an inventoried I/O boundary (Core)'
PIE = 'picture loader: ReadLZSImage calls CRT fseek 0x48cda2, not an inventoried I/O boundary (Core)'
PULOS_EXIBICAO = {
    'InitTextLangue': (None, 0), 'TextGetMessage': (0, 0), 'AffText': (None, 0x10),
    'LoadPie': (None, 0), 'PlayVideo': (None, 0), 'CreateCredits': (None, 0), 'FreeCredits': (None, 0),
    'MCICD_Play': (None, 0), 'MCICD_Stop': (None, 0), 'MCICD_Manage': (None, 0),
    'PlaySnd_Manage': (None, 0), 'PlaySnd_PostSound': (None, 4), 'PlaySnd_StopSound': (None, 0),
    'PlaySnd_StopAllSound': (None, 0), 'PlaySnd_PostVolume': (None, 0), 'PlaySnd_SetGameVolume': (None, 0),
}
FRONTEIRAS_EXIBICAO = {
    'InitTextLangue': (None, 0, TEXTO), 'TextGetMessage': (0, 0, TEXTO), 'AffText': (None, 0x10, TEXTO),
    'LoadPie': (None, 0, PIE), 'PlayVideo': (None, 0, 'video playback'), 'CreateCredits': (None, 0, 'credits'),
    'FreeCredits': (None, 0, 'credits'),
    'MCICD_Play': (None, 0, 'MCI CD audio; MCICD_Init never executed'),
    'MCICD_Stop': (None, 0, 'MCI CD audio; MCICD_Init never executed'),
    'MCICD_Manage': (None, 0, 'MCI CD audio pump; MCICD_Init never executed'),
    'PlaySnd_Manage': (None, 0, 'sound library; PlaySnd_InitSoundLib never executed'),
    'PlaySnd_PostSound': (None, 4, 'sound library; PlaySnd_InitSoundLib never executed'),
    'PlaySnd_StopSound': (None, 0, 'sound library; PlaySnd_InitSoundLib never executed'),
    'PlaySnd_StopAllSound': (None, 0, 'sound library; PlaySnd_InitSoundLib never executed'),
    'PlaySnd_PostVolume': (None, 0, 'sound library; PlaySnd_InitSoundLib never executed'),
    'PlaySnd_SetGameVolume': (None, 0, 'sound library; PlaySnd_InitSoundLib never executed'),
}


BASE_COM, BASE_SUPERFICIES, TAMANHO_SUPERFICIES = 0x3600000, 0x60000000, 0x200000
# v3 (prepared, not a reference): LoadPie runs over CRT fseek. Text still needs
# CRT ftell 0x48cf11 (FileSize from LoadFonteExterieur), not inventoried yet.
EXECUTADOS_V3 = ('LoadPie',)
NUNCA_EXECUTADOS = ('AppWindowInit', 'DisableIME', 'PlaySnd_InitSoundLib', 'MCICD_Init', 'WndProc')


@dataclass(frozen=True)
class EntradasExibicao:
    quadro: object                 # EntradasQuadro (M1 inputs + frame inputs)
    ticks: tuple                   # declared display clock answers, in call order
    preenchimento_superficie: int  # initial byte of declared surfaces
    proveniencia: dict = field(default_factory=dict)

    def manifesto(self):
        return dict(display_ticks=list(self.ticks), surface_fill=self.preenchimento_superficie,
                    ia_random_clock_site=hex(RELOGIO_IA), provenance=self.proveniencia)


class WindowsExibicao(WindowsQuadro):
    """Frame answers also in startup: the real window loop runs from AppInit on."""
    def __init__(self, entradas, quadro, ticks):
        super().__init__(entradas, quadro)
        self.ticks = list(ticks)

    def cursor(self, chamada):
        x, y = self.quadro.cursor
        chamada.escrever(chamada.argumentos[0], struct.pack('<ii', x, y))
        self.consumidos.append(('cursor', hex(chamada.retorno), x, y, self.fase))
        return 1

    def mensagem(self, chamada):
        _, hwnd, minimo, maximo, remover = chamada.argumentos
        if (hwnd, minimo, maximo) != (0, 0, 0):
            raise ParadaVinculoDeclarado('PeekMessageA filter outside the declared no-message answer')
        self.consumidos.append(('peek_message', hex(chamada.retorno), remover, 0, self.fase))
        return 0

    def tempo(self, chamada):
        if chamada.retorno == RELOGIO_IA:
            return super().tempo(chamada)
        if not self.ticks:
            raise ParadaVinculoDeclarado('Declared display tick sequence exhausted')
        valor = self.ticks.pop(0)
        self.consumidos.append(('display_clock', hex(chamada.retorno), valor, self.fase))
        return valor


class BancadaExibicaoOriginal(BancadaQuadroMissaoOriginal):
    def __init__(self, entradas_exibicao, *, pulos=None, fronteiras=None, v3=False, **kw):
        """``v3``: bind Core's CRT fseek/fgets boundaries and execute LoadPie (branch-local preparation)."""
        self.entradas_exibicao, self.v3 = entradas_exibicao, v3
        if v3:
            pulos = pulos or {k: v for k, v in PULOS_EXIBICAO.items() if k not in EXECUTADOS_V3}
            fronteiras = fronteiras or {k: v for k, v in FRONTEIRAS_EXIBICAO.items() if k not in EXECUTADOS_V3}
        super().__init__(entradas_exibicao.quadro, pulos=pulos or PULOS_EXIBICAO,
                         fronteiras=fronteiras or FRONTEIRAS_EXIBICAO, **kw)
        # Base protection makes every high region RW without execute; the COM
        # trampolines must stay fetchable (they stop at their hooks).
        inicio, fim = self.directdraw.regiao_executavel
        self.cpu.mem_protect(inicio, fim-inicio, unicorn.UC_PROT_READ | unicorn.UC_PROT_EXEC)
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._parar_se_pedido, begin=SAIDA_LACO, end=SAIDA_LACO)

    def _nao_executados(self):
        # ProgIteration and AffGame run here; only the declared boundaries and
        # the window/sound/CD initializers stay unexecuted.
        return tuple(sorted(PULOS_EXIBICAO)) + NUNCA_EXECUTADOS, ()

    def _nao_executados_quadro(self):
        return tuple(sorted(FRONTEIRAS_EXIBICAO)) + NUNCA_EXECUTADOS

    def _criar_windows(self, entradas):
        return WindowsExibicao(entradas, self.entradas_quadro, self.entradas_exibicao.ticks)

    def _declarar(self):
        super()._declarar()
        if self.v3:
            self.declarar_vinculo(0x48cda2, 'CRT.fseek', ('EAX', 'EDX', 'EBX'), self.arquivos.fseek_crt, natureza='io')
            self.declarar_vinculo(0x48ce96, 'CRT.fgets', ('EAX', 'EDX', 'EBX'), self.arquivos.fgets_crt, natureza='io')
        # After every bench import: earlier trampolines keep their addresses.
        self.directdraw = ExibicaoDeclarada(base=BASE_COM, base_superficies=BASE_SUPERFICIES,
                                            tamanho_superficies=TAMANHO_SUPERFICIES).instalar(self)
        # Declared initial surface bytes (DirectDraw leaves them undefined).
        self.cpu.mem_write(BASE_SUPERFICIES, bytes([self.entradas_exibicao.preenchimento_superficie])*TAMANHO_SUPERFICIES)

    def chamadas_exibicao(self):
        return self.directdraw.eventos

    def estado_exibicao(self):
        """Declared display state (surfaces, COM objects): output, not game state."""
        import hashlib
        m = self.directdraw.manifesto()
        for s in m['surfaces']:
            s['sha256'] = hashlib.sha256(self.directdraw.pixels(s['role'])).hexdigest()
        return m

    # ------------------------------------------------------------ phases
    def executar_inicio(self):
        """AppInit as in M1, then the real _WinMain@16 loop to the original CALL MissionLoad.

        Declared loop frame (``executar``): ESP = bench stack + 0x8000, EBX = 0
        (_WinMain@16 zeroes EBX at 0x4601af and uses it as its zero constant);
        the MSG buffer at [ESP] keeps the bench stack bytes (PeekMessageA
        answers no message, so nothing reads it; measured by the footprint).
        """
        self.preparar_dados_thread_crt()
        self.chamar('appinit', 'AppInit', {'EAX': 0x400000})
        regs = self._correr('window_loop', LACO, {'EBX': 0}, (MISSION_LOAD, SAIDA_LACO))
        self.passos.append(dict(step='window_loop', entry=hex(LACO), registers={'EBX': '0x0'},
                                stop=hex(regs['EIP']), eax=hex(regs['EAX'])))
        if regs['EIP'] != MISSION_LOAD:
            self._interromper('window_loop_exit_before_missionload', eip=hex(regs['EIP']))
        return regs

    def executar_cauda_carga(self, segundos):
        """(a) From 0x42d22d to the load-state CalculGame's real return in ProgIteration 0x475063."""
        if self.cpu.reg_read(x86.UC_X86_REG_EIP) != RETORNO_MISSION_LOAD or self.fase != 'oracle':
            raise RuntimeError('The load tail starts only at the real MissionLoad return')
        self._ganchar_quadros()
        self._fase('load_tail')
        self.limite_segundos = segundos
        self.iniciar_relogio()
        return self._correr('load_tail', RETORNO_MISSION_LOAD, {}, (RETORNO_CALCUL_GAME,), retomar=True)

    def executar_entre_quadros(self, segundos, k=1):
        """(b) The real ProgIteration tail and window loop to the CalculGame entry of frame k."""
        if self.cpu.reg_read(x86.UC_X86_REG_EIP) != RETORNO_CALCUL_GAME:
            raise RuntimeError('between_frames starts at ProgIteration 0x475063')
        entre, _ = nomes_fases(k)
        self.declaracao_chamador = None
        self._fase(entre)
        self.limite_segundos = segundos
        self.iniciar_relogio()
        self._retomando = {RETORNO_CALCUL_GAME}
        self._passar_uma_vez.add(RETORNO_CALCUL_GAME)
        regs = self._correr(entre, RETORNO_CALCUL_GAME, {}, (CALCUL_GAME, SAIDA_LACO), retomar=True)
        if regs['EIP'] != CALCUL_GAME:
            self._interromper('window_loop_exit', eip=hex(regs['EIP']))
        return regs

    def executar_quadros(self, n, segundos=600):
        """Phases of N consecutive frames after MissionLoad: yields (phase, registers) in order.

        load_tail, then for k = 1..n: between_frames(k) and frame(k); each
        phase ends at its real stop (the next CalculGame entry, the frame's
        RET into ProgIteration 0x475063).
        """
        yield 'load_tail', self.executar_cauda_carga(segundos)
        for k in range(1, n+1):
            entre, quadro = nomes_fases(k)
            yield entre, self.executar_entre_quadros(segundos, k)
            yield quadro, self.executar_quadro(segundos, k)
