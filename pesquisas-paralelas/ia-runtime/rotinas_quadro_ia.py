"""AI/runtime frame callees reached by MONDE01 frames 0 and 1, over an explicit MemoriaDeclarada.

Translated after the original isolated captures at the exact frame-0/1 entries
(``evidencias/captura-isolada-ia-quadro1.json``, commit ``3b4d227``):

- ``calcular_caixa_mensagens``: MessageBoxCalcul 0x469dce (whole routine);
- ``processar_entrada``: ProcessInputGame 0x45edc0, the no-command path
  (command word 0, or above 0x27, goes through table 0x45ed20 to 0x45f2de and
  clears the 10-byte record). Any other command raises DependenciaIA at its
  table target;
- ``avancar_monstros``: AvanceMonstre 0x47b283, now delegated to ``incursao_ia`` (M2.3). Formerly: the first-call
  stamp, the mission-0x17 test and the monster-spec period scan. The
  ConstruitGroupeMonstre branch (0x47b349), the group-action loop (0x47b3ad),
  the pending-attack branch (0x47b44c) and the mission-0x17 branch (0x47b2d3)
  are unreached at MONDE01 frames 0/1; each raises DependenciaIA at its
  address;
- ``resolver_ia``: iaSolver 0x47d314 by Core's ``tarefas_ia.MaquinaTarefas.atualizar``.
  The live task pool and list headers are loaded into the machine and written
  back afterwards (``PonteTarefas``). Only the empty-context path is validated
  at the original so far.
"""
from memoria_ia_runtime import s32
from reinicio_ia import DependenciaIA

FILA_ENTRADA = 0x4e2458          # four u32 pointers to 10-byte input records
TABELA_COMANDOS = 0x45ed20        # 40 jump targets; 0x45f2de is the clear-only path
LIMPAR_COMANDO = 0x45f2de
MONSTROS, CONTAGEM_MONSTROS, REGISTROS_MONSTROS = 0x50a9cc, 0x50a9ce, 0x50a9d0
ACOES_MONSTROS, ATAQUES_MONSTROS, CONTADOR = 0x50ae80, 0x50b134, 0x508f7c
POOL_TAREFAS, LIVRES, CONTEXTOS, ATIVAS = 0x512320, 0x5148a0, 0x5148b0, 0x514904
REGIOES_ROTINAS = (
    (0x4e2458, 0x4e2468, 'input record pointers'),
    (0x4e7858, 0x4e7858 + 256 * 518, 'message box records'),
    (0x507d54, 0x507d59, 'message box head/tail/flag'),
    (0x50a9bc, 0x50af84, 'monster spec, records and actions'),
    (0x50b134, 0x50b178, 'monster attack stack'),
    (0x508f7c, 0x508f80, 'frame counter'),
    (0x512320, 0x514908, 'task pool, free list, contexts and active count'),
)


def _chamar(provedores, rotina, sitio, **argumentos):
    provedor = provedores.get(rotina)
    if provedor is None:
        raise DependenciaIA(rotina, sitio)
    return provedor(sitio=sitio, **argumentos)


def calcular_caixa_mensagens(m):
    """MessageBoxCalcul 0x469dce: count down the head message; advance the head (mod 256) at zero."""
    cauda, cabeca = m.u16(0x507d56), m.u16(0x507d54)
    if cauda == cabeca:
        return
    endereco = 0x4e7858 + 2 * 259 * cabeca
    restante = (m.u16(endereco) - 1) & 0xffff
    m.u16(endereco, restante)
    if restante:
        return
    m.u16(0x507d54, (cabeca + 1) % 256)
    m.u8(0x507d58, 0)


def processar_entrada(m, jogador, comandos):
    """ProcessInputGame 0x45edc0 (AL = player); ``comandos`` is the jump table 0x45ed20 read from the image."""
    registro = m.u32(FILA_ENTRADA + 4 * (jogador & 0xff))
    comando = m.u16(registro)
    alvo = LIMPAR_COMANDO if comando > 0x27 else comandos[comando]
    if alvo != LIMPAR_COMANDO:
        raise DependenciaIA(f'ProcessInputGame command 0x{comando:x}', alvo)
    for deslocamento in (0, 2, 4, 6, 8):
        m.u16(m.u32(FILA_ENTRADA + 4 * (jogador & 0xff)) + deslocamento, 0)
    return m.u32(FILA_ENTRADA + 4 * (jogador & 0xff))


def avancar_monstros(m, provedores):
    """AvanceMonstre 0x47b283 (player 4): the whole routine is ``incursao_ia.avancar_monstros`` since M2.3."""
    from incursao_ia import avancar_monstros as avancar
    return avancar(m, provedores)


class PonteTarefas:
    """Load/store bridge between the live task memory and Core's MaquinaTarefas."""

    def __init__(self, maquina):
        self.maquina = maquina

    def carregar(self, m):
        mq = self.maquina
        mq.memoria[:] = bytes(m.u8(POOL_TAREFAS + i) for i in range(len(mq.memoria)))
        mq.livres = [s32(m.u32(LIVRES)), m.u32(LIVRES + 4)]
        mq.contextos = [[s32(m.u32(CONTEXTOS + 16 * k)), m.u32(CONTEXTOS + 16 * k + 4)] for k in range(5)]
        mq.ativas = m.u32(ATIVAS)

    def guardar(self, m):
        mq = self.maquina
        for i, valor in enumerate(mq.memoria):
            if m.u8(POOL_TAREFAS + i) != valor:
                m.u8(POOL_TAREFAS + i, valor)
        for endereco, valor in ((LIVRES, mq.livres[0]), (LIVRES + 4, mq.livres[1]), (ATIVAS, mq.ativas)):
            if m.u32(endereco) != valor & 0xffffffff:
                m.u32(endereco, valor)
        for k, (cabeca, contagem) in enumerate(mq.contextos):
            for endereco, valor in ((CONTEXTOS + 16 * k, cabeca), (CONTEXTOS + 16 * k + 4, contagem)):
                if m.u32(endereco) != valor & 0xffffffff:
                    m.u32(endereco, valor)


def resolver_ia(m, ponte, contexto):
    """iaSolver 0x47d314 (EAX = context address 0x5148b0 + 16p) by Core's MaquinaTarefas.atualizar."""
    jogador, resto = divmod(contexto - CONTEXTOS, 16)
    if resto or not 0 <= jogador < 5:
        raise ValueError(f'iaSolver context 0x{contexto:x} is not one of the five list headers')
    ponte.carregar(m)
    try:
        return ponte.maquina.atualizar(jogador) & 0xffffffff
    finally:
        ponte.guardar(m)
