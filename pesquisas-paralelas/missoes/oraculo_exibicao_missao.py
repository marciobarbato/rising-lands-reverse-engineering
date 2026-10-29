"""Display-executing MONDE01 oracle: startup, MissionLoad and frames 0/1 with the display path run.

Same phases and checks as ``oraculo_quadro_missao``, but the original display
code is *executed* instead of skipped: AffInit/DDInit, LoadPalette,
DDSetPalette, DDLockSurface/DDUnlockSurface, DDFlipPage, FilledBox,
ResetMode, the bank loaders (LoadSTRATBank, SetBank, LoadBank, DeleteBank),
RestoreAll and AffGame.  DirectDraw is the declared backend of
``exibicao_declarada`` (DirectDrawCreate import plus COM vtables).  Still not
executed, each a declared boundary with recorded arguments:

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
from exibicao_declarada import DirectDrawDeclarado, REGIAO_COM
from oraculo_carga_missao import MISSION_LOAD, RETORNO_MISSION_LOAD
from oraculo_quadro_missao import (BancadaQuadroMissaoOriginal, CALCUL_GAME, RETORNO_CALCUL_GAME, SAIDA_LACO,
                                   WindowsQuadro)

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
    def __init__(self, entradas_exibicao, *, pulos=None, fronteiras=None, **kw):
        self.entradas_exibicao = entradas_exibicao
        super().__init__(entradas_exibicao.quadro, pulos=pulos or PULOS_EXIBICAO,
                         fronteiras=fronteiras or FRONTEIRAS_EXIBICAO, **kw)
        # Base protection makes every high region RW without execute; the COM
        # trampolines must stay fetchable (they stop at their hooks).
        self.cpu.mem_protect(REGIAO_COM, 0x10000, unicorn.UC_PROT_READ | unicorn.UC_PROT_EXEC)
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._parar_se_pedido, begin=SAIDA_LACO, end=SAIDA_LACO)

    def _nao_executados(self):
        # ProgIteration and AffGame run here; only the declared boundaries and
        # the window/sound/CD initializers stay unexecuted.
        return tuple(sorted(PULOS_EXIBICAO)) + NUNCA_EXECUTADOS, ()

    def _nao_executados_quadro(self):
        return tuple(sorted(FRONTEIRAS_EXIBICAO)) + NUNCA_EXECUTADOS

    def _criar_windows(self, entradas):
        return WindowsExibicao(entradas, self.entradas_quadro, self.entradas_exibicao.ticks)

    def _importacoes_extras(self):
        self.directdraw = DirectDrawDeclarado(self, preenchimento_superficie=
                                              self.entradas_exibicao.preenchimento_superficie)
        return tuple(super()._importacoes_extras()) + (
            (0x5234c4, 'DDRAW.DirectDrawCreate', 3, self.directdraw.criar),)

    def estado_exibicao(self):
        """Declared display state (surfaces, COM objects): output, not game state."""
        import hashlib
        saida = {}
        for p, o in self.directdraw.objetos.items():
            if o['interface'] == 'IDirectDrawSurface':
                pixels = bytes(self.cpu.mem_read(o['pixels'], o['largura']*o['altura']))
                saida[o['papel']] = dict(object=hex(p), pixels=hex(o['pixels']), width=o['largura'],
                                         height=o['altura'], sha256=hashlib.sha256(pixels).hexdigest())
        return dict(surfaces=saida, directdraw=self.directdraw.resumo())

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

    def executar_entre_quadros(self, segundos):
        """(b) The real ProgIteration tail and window loop to the next CalculGame entry (no declared frame)."""
        if self.cpu.reg_read(x86.UC_X86_REG_EIP) != RETORNO_CALCUL_GAME:
            raise RuntimeError('between_frames starts at ProgIteration 0x475063')
        self.declaracao_chamador = None
        self._fase('between_frames')
        self.limite_segundos = segundos
        self.iniciar_relogio()
        self._retomando = {RETORNO_CALCUL_GAME}
        self._passar_uma_vez.add(RETORNO_CALCUL_GAME)
        regs = self._correr('between_frames', RETORNO_CALCUL_GAME, {}, (CALCUL_GAME, SAIDA_LACO), retomar=True)
        if regs['EIP'] != CALCUL_GAME:
            self._interromper('window_loop_exit', eip=hex(regs['EIP']))
        return regs
