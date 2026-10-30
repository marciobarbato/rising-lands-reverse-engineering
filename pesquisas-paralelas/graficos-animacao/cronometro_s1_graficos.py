"""AffChrono's selected type-2 recruitment clock, original S1 frame2014 onward.

Consumes live progress and the live unit-table duration: the read-only type-2
CalculStatusRecrute contract (Economy, 0x423F9D). No recruitment state is advanced.
"""
import composicao


def compor_cronometro_s1(h, record):
    m = h.m
    if m.u8(record + 8) != 2 or m.u8(record + 5) not in (4, 5) or h.camera != 0:
        h.parar(0x401d18, 'clock outside the captured owner-0 sanctuary domain')
    if not m.u8(record + 0x74):
        return
    kind = m.u8(record + 0x7b)
    if kind not in (5,7):
        h.parar(0x423f9d, 'recruitment clock target outside captured S1 unit types')
    duration = m.u16(0x4965ae + 50 * kind)
    if not duration:
        h.parar(0x423ec8, 'zero original recruitment duration')
    percent = m.u32(record + 0x8c) // duration
    if not 0 <= percent <= 100:
        h.parar(0x401ef1, 'recruitment clock percentage outside captured strip')
    margin = m.u8(0x508f90)
    if margin:
        h.parar(0x401e56, 'recruitment clock margin outside captured zero')
    enabled = m.u8(0x497285)
    if enabled not in (0, 1):
        h.parar(0x401e11, 'recruitment clock minimap mode outside captured 0/1')
    x = y = 0
    if enabled:
        # 0x46A1F8 returns the minimap origin, not the current mouse position.
        width = h.catalogo.quadro(0x1e6c).largura
        if m.u16(0x507d68) <= m.u16(0x49a018) // 2:
            x = m.u16(0x49a018) - width
    if h.tabela_sombra is None:
        h.parar(0x45b796, 'recruitment clock requires the actual original shadow table')
    clip = tuple(m.u16(a) for a in (0x49a020, 0x49a01c, 0x49a022, 0x49a01e))
    h.chamadas.append(['PasteOmbreCmp', x, y, 0x1e6c, 1])
    h.saida[:] = composicao.compor_sombra(bytes(h.saida), h.largura, h.altura,
        h.catalogo.quadro(0x1e6c), x, y, h.tabela_sombra, clip)
    h.bob(x, y, 0x1e4b + (percent * 32 // 100), True)
