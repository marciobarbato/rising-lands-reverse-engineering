"""AffGame 0x417698, mode 0x12: its store to the HUD refresh flag 0x4e05a2 and its leftover EAX (M2.2).

Translated from the intact code (static disassembly of the mode-0x12 body,
``0x4178f7..0x417ec1``). Graphics' ``efeitos_logicos_exibicao.desenhar_jogo``
still guards the drawing domain. This module adds the two effects of AffGame
that the frame sequence observes outside display: the flag and EAX.

Order in the original, with no event in progress:

1. ``+0x25f`` CalculFrame (display ticks), then ``+0x264`` EvenementEnCours
   (``al = [0x4e1b0e]``). A nonzero value sets the local event flag
   ``[ebp-4]``.
2. ``+0x271``: if ``[0x4e05a2] == 0`` and ``counter [0x508f7c] mod u8
   [0x497284] != 0``, the routine returns at once (``+0x28d``) with
   EAX = counter div divisor. Nothing is drawn and nothing is stored.
3. Otherwise the HUD is drawn. ``+0x3ef`` stores 1 when ``[0x49a041]`` is set.
   DDFlipPage receives the flag in AL (``+0x6a4``). Then ``+0x7f2`` stores 0
   and ``+0x7fa`` divides the counter by 5.
4. When the remainder is 0 and ``[ebp-4]`` is 0 (``+0x804``), or when
   ``[ebp-4]`` is set and a second EvenementEnCours returns 0 (``+0x80c``),
   ``+0x815`` sets CL = 1 and calls Cyclage. Cyclage saves and restores ECX,
   and its last call is DDSetPalette, which returns the backend's IDirectDrawPalette
   SetEntries result in EAX. ``+0x81c`` stores CL = 1.
5. ``+0x822`` EvenementEnCours replaces AL with ``[0x4e1b0e]``. When that is
   nonzero, ``+0x82f`` stores mode 0x16. The routine returns through
   ``0x4171f1``, which restores EBX, ECX, EDX, ESI, EDI and EBP.

Domain and named stops:
- Mode 0x12 only.
- No event in progress at entry. EvenementAffiche, the ``[ebp-4]`` paths and
  the mode-0x16 store are not modelled.
- A divisor of 0 would raise #DE at ``+0x289``.
- ``[0x508f92]`` set: the ``+0x2b5`` store and the video-surface clear.
- ``[0x496204]`` not 0xffff: the ``+0x54a`` marker animation and its
  ``0x4e05ac`` and ``0x496204`` stores.
- The palette object ``[0x4e179c]`` must exist: DDSetPalette then takes the
  SetEntries path, whose declared result is DD_OK = 0
  (``fronteiras_exibicao``).

The ``+0x3ef`` store is always overwritten by ``+0x7f2`` before the routine
returns. Only DDFlipPage reads the value in between, and DDFlipPage is a
display call.
"""
from dataclasses import dataclass

from reinicio_ia import DependenciaIA

AFFGAME = 0x417698
BANDEIRA_HUD = 0x4e05a2
CONTADOR, DIVISOR, MODO, EVENTO = 0x508f7c, 0x497284, 0x4e2f78, 0x4e1b0e
PALETA_OBJETO = 0x4e179c
DD_OK = 0          # Graphics' declared backend: every supported call returns DD_OK


@dataclass(frozen=True)
class EfeitoHud:
    desenhou: bool        # the HUD body ran (False: the +0x28d early return)
    escritas: tuple       # (address, width, value) in original order: the net stores to 0x4e05a2
    eax: int              # leftover EAX at AffGame's RET
    leituras: tuple       # (name, value) read, in order


def affgame_hud(m, desenhar):
    """Effects of one AffGame call in mode 0x12 on the flag and EAX.

    ``m`` provides u8/u16/u32. ``desenhar(m)`` is Graphics' drawing-domain
    provider. It is called only when the original runs the body, and it raises
    its own stop outside the proved domain.
    """
    lidas = []

    def ler(nome, valor):
        lidas.append((nome, valor))
        return valor
    if ler('mode', m.u8(MODO)) != 0x12:
        raise DependenciaIA(f'AffGame mode 0x{m.u8(MODO):x} (only the 0x12 body is modelled)', AFFGAME + 0x10)
    if ler('event', m.u8(EVENTO)):
        raise DependenciaIA('AffGame with an event in progress (EvenementAffiche, [ebp-4] paths)', AFFGAME + 0x26d)
    bandeira, contador = ler('flag', m.u8(BANDEIRA_HUD)), ler('counter', m.u32(CONTADOR))
    if bandeira == 0:
        divisor = ler('divisor', m.u8(DIVISOR))
        if divisor == 0:
            raise DependenciaIA('AffGame draw divisor 0 (#DE at div)', AFFGAME + 0x289)
        if contador % divisor:
            return EfeitoHud(False, (), contador // divisor, tuple(lidas))
    if ler('[0x508f92]', m.u8(0x508f92)):
        raise DependenciaIA('AffGame [0x508f92] video-surface clear path', AFFGAME + 0x2a0)
    if ler('[0x496204]', m.u16(0x496204)) != 0xffff:
        raise DependenciaIA('AffGame marker animation (0x4e05ac/0x496204 stores)', AFFGAME + 0x50a)
    desenhar(m)
    escritas = [(BANDEIRA_HUD, 1, 0)]                                  # +0x7f2
    if contador % 5 == 0:
        if not ler('palette object', m.u32(PALETA_OBJETO)):
            raise DependenciaIA('Cyclage -> DDSetPalette without a palette object (CreatePalette path)',
                                0x43ee95)
        escritas.append((BANDEIRA_HUD, 1, 1))                         # +0x81c, CL = 1 kept by Cyclage
        eax = DD_OK                                                    # DDSetPalette -> SetEntries
    else:
        eax = contador // 5                                            # +0x7fa quotient
    eax = (eax & ~0xff) | m.u8(EVENTO)                                 # +0x822 EvenementEnCours (AL)
    return EfeitoHud(True, tuple(escritas), eax & 0xffffffff, tuple(lidas))
