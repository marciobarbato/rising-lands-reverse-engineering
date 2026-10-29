"""Logic-state effects of the original display path (DDInit, RestoreAll 0x474b08, AffGame 0x417698).

Original-first.  ``evidencias/efeitos-logicos-exibicao.json`` records every value-changing write made inside the
dynamic extent of RestoreAll and AffGame in Missions' ``exibicao`` scenario (load tail, between frames) and every
read of those bytes by code outside the extents.  Result: **no byte that logic code reads is written by either
routine in the captured domain**.  The providers therefore return an empty write list, but only inside the domain
the capture proves; every other state raises a named stop instead of assuming the same.  No pixel, surface, bank
or stack byte is produced (display output).

The providers take ``memoria`` with ``u8/u16/u32(address)`` reads (``MemoriaDeclarada`` fits) and never write.
"""
from dataclasses import dataclass

ROTINAS = {'RestoreAll': 0x474b08, 'AffGame': 0x417698, 'DDInit': 0x43f50b}
ESTRUTURAS, ESTRUTURA_PASSO, ESTRUTURA_ESTADO = 0x49a0c8, 276, 5
ESTADOS_ESTRUTURA_PROVADOS = frozenset({0, 5})      # captured pool: 999 free + the Santuario (state 5)
ORIGENS_PROVADAS = frozenset({(4, 6)})              # view origin at the native RestoreAll/AffGame entries
VIEWPORT, TELA = (25, 17), (800, 600)               # DDInit hi-res values (0x508724/26, 0x49a018/1a)
CURSOR_RNG_SITIOS = (0x407dd3, 0x411147, 0x412392, 0x415b77, 0x415c19, 0x43f191)   # display-side 0x4e1d18 writers


class DependenciaExibicao(Exception):
    """A display-path branch whose logic-state effect the capture did not prove."""
    def __init__(self, rotina, sitio, motivo):
        super().__init__(f'{rotina} @0x{sitio:x}: {motivo}')
        self.rotina, self.sitio, self.motivo = rotina, sitio, motivo


@dataclass(frozen=True)
class EfeitosExibicao:
    rotina: str
    escritas: tuple = ()          # (address, width, value): logic-state stores; empty for the proved domain
    verificacoes: tuple = ()      # (name, observed) guard values read, in order


def _guardas(memoria, rotina):
    lidas = []
    def ler(nome, valor):
        lidas.append((nome, valor))
        return valor
    if ler('[0x4dfb44]', memoria.u8(0x4dfb44)) != 0:
        raise DependenciaExibicao(rotina, 0x43f191, 'DDFlipPage shake path would advance the RNG cursor 0x4e1d18 '
                                  'and 0x4dfb44; not captured')
    viewport = (ler('[0x508724]', memoria.u16(0x508724)), ler('[0x508726]', memoria.u16(0x508726)))
    if viewport != VIEWPORT:
        raise DependenciaExibicao(rotina, 0x4178f7, f'viewport {viewport} is not the captured {VIEWPORT}')
    origem = (ler('[0x508720]', memoria.u16(0x508720)), ler('[0x508722]', memoria.u16(0x508722)))
    if origem not in ORIGENS_PROVADAS:
        raise DependenciaExibicao(rotina, CURSOR_RNG_SITIOS[3], f'view origin {origem}: vegetation/terrain handlers '
                                  '(0x411147, 0x412392, 0x415b77/0x415c19) only proved native for (4, 6)')
    estados = {memoria.u8(ESTRUTURAS + i*ESTRUTURA_PASSO + ESTRUTURA_ESTADO) for i in range(1000)}
    lidas.append(('structure states', tuple(sorted(estados))))
    if not estados <= ESTADOS_ESTRUTURA_PROVADOS:
        raise DependenciaExibicao(rotina, CURSOR_RNG_SITIOS[0], f'structure states {sorted(estados)}: AffBatiments '
                                  'advances 0x4e1d18 for state 3 (69 sites); only states {0,5} captured')
    return tuple(lidas)


def restaurar_tudo(memoria):
    """RestoreAll 0x474b08 in the captured domain: no logic-state write (the DGROUP stores are display bookkeeping)."""
    return EfeitosExibicao('RestoreAll', (), _guardas(memoria, 'RestoreAll'))


def desenhar_jogo(memoria):
    """AffGame 0x417698 (mode 0x12 body) in the captured domain: no logic-state write."""
    return EfeitosExibicao('AffGame', (), _guardas(memoria, 'AffGame'))


def inicializar_dimensoes(memoria, alta_resolucao=True):
    """DDInit 0x43f50b stores read by logic: screen 800x600 and the 25x17 viewport (hi-res path only)."""
    if not alta_resolucao:
        raise DependenciaExibicao('DDInit', 0x43f50b, 'low-resolution path not captured')
    escritas = ((0x49a018, 2, TELA[0]), (0x49a01a, 2, TELA[1]), (0x508724, 2, VIEWPORT[0]), (0x508726, 2, VIEWPORT[1]))
    return EfeitosExibicao('DDInit', escritas, ())
