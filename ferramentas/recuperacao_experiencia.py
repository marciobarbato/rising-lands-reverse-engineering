"""Original Engin_RetrieveExperimente 0x441623 (MissionLoad+0x2ea tail call).

Intact bytes 0x441623..0x441659 plus shared epilogue 0x440d59..0x440d5e.
Watcom register routine with no consumed register input: it pushes and pops
EBX/ECX/EDX/ESI, never touches EDI/EBP, and returns with RET (no stack
arguments). For owners 0..3 and words 0..4 in ascending order it copies the
u16 at 0x4e19ec+10*owner+2*word (saved queue) to 0x4e19c4+10*owner+2*word
(current queue). No guard or data-dependent branch exists; the 40 copied
bytes are the only non-stack memory effect. On return EAX is 0x28 and the
last CMP ECX,4 leaves ZF=PF=1, CF=AF=SF=OF=0; DF and other bits are kept.
MissionLoad's next call, PlayerRetrieve 0x46df41, begins with XOR EAX,EAX.

Both queues are live 40-byte buffers owned by the caller: the current queue
is the same `experiencias_unidades` bytearray used by EnginSetExperimente,
the saved queue is whatever the session's original producers left in
0x4e19ec (Engin_ResetExperience, Engin_StoreExperimente, Engin_LoadExperimente).
Nothing here creates, resets or defaults either buffer.
"""
from dataclasses import dataclass

ENTRADA = 0x441623
LEITURA_GUARDADA = 0x441645  # first saved-queue read: MOV DX,[EAX+0x4e19ea]
ATUAL, GUARDADA = 0x4e19c4, 0x4e19ec
EAX_RETORNO = 0x28
FLAGS_ARITMETICAS = 0x8d5  # CF|PF|AF|ZF|SF|OF written by the final CMP ECX,4
FLAGS_RESULTADO = 0x44  # PF|ZF after 4-4


class DependenciaExperienciaGuardada(NotImplementedError):
    """The saved queue at 0x4e19ec was not supplied; nothing was written."""
    def __init__(self, endereco=LEITURA_GUARDADA):
        self.endereco = endereco
        super().__init__(f'Live saved experience queue 0x{GUARDADA:x} (40 bytes) required at '
                         f'0x{endereco:x}; current queue unchanged')


@dataclass(frozen=True)
class RetornoRecuperacaoExperiencia:
    """Register state at RET 0x440d5d; EBX/ECX/EDX/ESI/EDI/EBP equal entry."""
    eax: int = EAX_RETORNO

    @staticmethod
    def eflags(eflags_entrada):
        return (eflags_entrada & ~FLAGS_ARITMETICAS & 0xffffffff) | FLAGS_RESULTADO


def recuperar_experiencias(atuais, guardadas):
    """Copy the live saved queue into the live current queue in place.

    `atuais` must be the writable 40-byte bytearray (0x4e19c4); `guardadas` the
    distinct live 40-byte bytes/bytearray (0x4e19ec). Every check happens
    before the first store. A missing saved queue raises the named dependency
    at its original read; malformed buffers raise ValueError. Views are refused
    because the original buffers are adjacent and never overlap.
    """
    if guardadas is None:
        raise DependenciaExperienciaGuardada()
    if type(atuais) is not bytearray or len(atuais) != 40:
        raise ValueError('Current experience queue must be the live 40-byte bytearray at 0x4e19c4')
    if type(guardadas) not in (bytes, bytearray) or len(guardadas) != 40:
        raise ValueError('Saved experience queue must be a live 40-byte bytes/bytearray at 0x4e19ec')
    if guardadas is atuais:
        raise ValueError('Saved and current experience queues are distinct original buffers')
    for dono in range(4):
        for palavra in range(5):
            p = dono*10 + palavra*2
            atuais[p:p+2] = guardadas[p:p+2]
    return RetornoRecuperacaoExperiencia()


def recuperar_experiencia_missao(mundo, guardadas):
    """MissionLoad tail entry over the world's live `experiencias_unidades`."""
    return recuperar_experiencias(mundo.experiencias_unidades, guardadas)
