"""DeleteBank 0x418a12 and MemFree 0x467ecb as reached by MenuInit on the MONDE01 display path.

Translated from the executed blocks recorded inside MenuInit's call in
``evidencias/captura-entradas-quadro1-ia-exibicao.json`` (commit ``ad27649``):

- DeleteBank (EAX = bank header, or 0, which returns at once): for each of the
  u16 ``[bank]`` entries of the u32 table ``[bank+4]``, a nonzero entry first
  frees its u32 ``[entry+8]`` buffer when that is nonzero, then the entry.
  Then the count is cleared, the table (when nonzero) is freed, and finally
  the header itself is freed.
- MemFree (EAX = pointer): ``GlobalHandle(ptr)``, ``GlobalUnlock(h)``,
  ``GlobalHandle(ptr)``, ``GlobalFree(h)``, with no DGROUP store.

The heap is Missions' committed ``ArenaComposicaoM1`` (GMEM_FIXED, handle ==
pointer, exact allocation records). ``ArenaQuadro`` adopts the allocations that
are live at the scenario's MissionLoad return, so that frames 0/1 can free them.
Every request is also recorded in the composition's binding log, in the
capture's fields.
"""
import sys

from ambiente_ia_runtime import ROOT

MISSOES = ROOT / 'pesquisas-paralelas/missoes'
if str(MISSOES) not in sys.path:
    sys.path.insert(0, str(MISSOES))
from arena_composicao_m1 import ArenaComposicaoM1, PAGINA  # noqa: E402

RETORNOS_MEMFREE = (0x467ed8, 0x467ee0, 0x467ee8, 0x467ef0)   # return sites of its four imports


class ArenaQuadro(ArenaComposicaoM1):
    """The committed arena continued from a MissionLoad *return* state (records and live blocks adopted)."""

    def __init__(self, mapa, arena_entrada, alocacoes):
        ultimo = max(int(a['pointer'], 16) + a['size'] for a in alocacoes)
        arena = dict(arena_entrada, allocations=len(alocacoes), next_free=hex((ultimo + PAGINA - 1) & ~(PAGINA - 1)))
        super().__init__(mapa, arena, alocacoes, [])
        for registro in self.registros:
            if not registro['active']:
                continue
            nome = f"alloc{registro['index']:05d}"
            segmentos = [s for s in mapa.segmentos if s.bloco == nome]
            if len(segmentos) == 1 and segmentos[0].tipo == 'bytes':
                ponteiro = int(registro['pointer'], 16)
                self.vivos[ponteiro] = (registro, segmentos[0].buffer, nome)
                self.por_buffer[id(segmentos[0].buffer)] = ponteiro


def liberar_memoria(arena, registro, ponteiro):
    """MemFree 0x467ecb (EAX = pointer)."""
    ponteiro &= 0xffffffff
    if ponteiro not in arena.vivos:
        raise KeyError(f'MemFree 0x{ponteiro:08x}: not a live adopted arena block')
    buffer = arena.vivos[ponteiro][1]
    h = arena.obter_handle(buffer)
    registro.vinculo('KERNEL32.GlobalHandle', (ponteiro,), RETORNOS_MEMFREE[0], h)
    registro.vinculo('KERNEL32.GlobalUnlock', (h,), RETORNOS_MEMFREE[1], arena.desfixar(h))
    h = arena.obter_handle(buffer)
    registro.vinculo('KERNEL32.GlobalHandle', (ponteiro,), RETORNOS_MEMFREE[2], h)
    registro.vinculo('KERNEL32.GlobalFree', (h,), RETORNOS_MEMFREE[3], arena.liberar(h))


def liberar_banco(m, arena, registro, banco):
    """DeleteBank 0x418a12 (EAX = bank header pointer)."""
    banco &= 0xffffffff
    if banco == 0:
        return
    quantidade = m.u16(banco)
    for i in range(quantidade):
        entrada = m.u32(m.u32(banco + 4) + 4 * i)
        if entrada and m.u32(entrada + 8):
            liberar_memoria(arena, registro, m.u32(entrada + 8))
        if entrada:
            liberar_memoria(arena, registro, entrada)
    m.u16(banco, 0)
    tabela = m.u32(banco + 4)
    if tabela:
        liberar_memoria(arena, registro, tabela)
    liberar_memoria(arena, registro, banco)
