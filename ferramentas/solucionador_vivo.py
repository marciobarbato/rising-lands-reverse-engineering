"""Core's Python path solver with its work state at the original globals (M2.3, path search at 9177).

``SolucionadorCaminhosPython`` keeps the search scratch inside the object. Its result (unit +0x88,
route buffer, search context, status 0x4e0f4c and alternative cell 0x4e0f4a) equals the original's
at the raid's first search (counter 9177; ``validar_movimento_incursao``). This subclass loads the
scratch from the original globals before each search and stores it back afterwards, so a chained run
sees the original layout. The original layout:
- Chemin_Verouille 0x43b30b: flags u8 0x4e0f34/0x4e0f35 (stack arguments), owner u8 0x4e0f41,
  mask u8 0x4e0f42, size class u8 0x4e0f48, start/destination u16 0x4e0f44/0x4e0f46 (only when the
  search was not already concluded);
- CheminCalcul 0x42f214: the two 512-byte candidate buffers 0x4e116a/0x4e136a, the 510-byte region
  table 0x4e0f6a, the two 10-byte records 0x4e0f54/0x4e0f5e.

- CheminCalcul's contour state, when it traces contours (the search was not already concluded):
  - u16 0x4e1772: the unit's region backup +0xfa at entry (0x42f26c);
  - u8 0x4e0f40: the step count of the last traced side (reset per side, 0x42f332/0x4355c3, +1 per
    step, 0x432658/0x4355a5), the contour result's ``fase``;
  - u8 0x4e0f68: the region-list count (each add stores 0x4e0f6a + 2*count, 0x42fd9b), the
    contour result's ``quantidade_regioes``;
  - u32 0x4e0f50: the current record, 0x4e0f54, then 0x4e0f5e from the second side (0x4355e1),
    unless every start was blocked.
"""
from mundo_vivo import ponteiros_rotas, vista_de
from solucionador_python import SolucionadorCaminhosPython

BUFFERS = (0x4e116a, 0x4e136a)
REGIOES, REGISTROS = 0x4e0f6a, (0x4e0f54, 0x4e0f5e)
INICIO, DESTINO = 0x4e0f44, 0x4e0f46
FLAGS, DONO, MASCARA, CLASSE = (0x4e0f34, 0x4e0f35), 0x4e0f41, 0x4e0f42, 0x4e0f48
PASSOS, REGISTRO_ATUAL, QUANTIDADE_REGIOES, REGIAO_ORIGEM = 0x4e0f40, 0x4e0f50, 0x4e0f68, 0x4e1772


class SolucionadorCaminhosVivo(SolucionadorCaminhosPython):
    def __init__(self, memoria):
        super().__init__(ponteiros_rotas(memoria))
        self._m = memoria

    def _carregar(self):
        m = self._m
        self.buffers = tuple(bytes(vista_de(m, b, 512)) for b in BUFFERS)
        self.regioes = bytes(vista_de(m, REGIOES, 510))
        self.registros = tuple(bytes(vista_de(m, r, 10)) for r in REGISTROS)
        self.inicio_calculado, self.destino_calculado = m.u16(INICIO), m.u16(DESTINO)

    def _guardar(self, mundo, indice):
        m = self._m
        for base, dados in zip(BUFFERS, self.buffers):
            vista_de(m, base, 512)[:] = dados
        vista_de(m, REGIOES, 510)[:] = self.regioes
        for base, dados in zip(REGISTROS, self.registros):
            vista_de(m, base, 10)[:] = dados
        p = self.preparacoes_python[-1]
        if not p['concluida']:
            m.u16(INICIO, self.inicio_calculado)
            m.u16(DESTINO, self.destino_calculado)
        if self.ultimo_contorno is not None:
            c = self.ultimo_contorno
            m.u16(REGIAO_ORIGEM, self.ultima_regiao_origem)
            m.u8(PASSOS, c.fase)
            m.u8(QUANTIDADE_REGIOES, c.quantidade_regioes)
            m.u32(REGISTRO_ATUAL, REGISTROS[0] if c.status_falha == 8 and not c.passos else REGISTROS[1])
        u = mundo.unidades
        m.u8(DONO, u[indice * 276])
        m.u8(CLASSE, m.u8(0x4962c8 + u[indice * 276 + 1]))
        # DeplaceEngin 0x44937f..0x4493a5 passes mask 1 + (+0xab != 0) in CL and two zero stack flags.
        m.u8(MASCARA, 1 + int(u[indice * 276 + 0xab] != 0))
        for f in FLAGS:
            m.u8(f, 0)

    def iniciar(self, mundo, indice):
        self.ultimo_contorno = None
        self._carregar()
        resultado = super().iniciar(mundo, indice)
        self._guardar(mundo, indice)
        return resultado

    def verrouiller(self, mundo, indice, inicio, destino, mascara, rota, flag1, flag2):
        """Chemin_Verouille 0x43b30b (AX start, DX destination, BX unit, CL mask; stack: route pointer and
        two flags): prepares the search context at the original globals (``preparar_destino``)."""
        from preparacao_destino import preparar_destino
        m, u = self._m, mundo.unidades
        p = preparar_destino(mundo, indice, inicio, destino, mascara, flag1, flag2)
        m.u8(FLAGS[0], flag1)
        m.u8(FLAGS[1], flag2)
        m.u8(0x4e0f36, 1)
        m.u8(0x4e0f37, p.sucesso)
        m.u8(0x496302, p.concluida)
        m.u32(0x4e0f3c, rota)
        m.u16(0x496304, indice)
        m.u8(MASCARA, mascara)
        m.u8(CLASSE, m.u8(0x4962c8 + u[indice * 276 + 1]))
        m.u8(DONO, u[indice * 276])
        m.u16(rota, 0)
        m.u16(0x4e0f4a, p.alternativa)
        m.u8(0x4e0f4c, p.status)
        if p.registrar_extremos:
            m.u16(INICIO, p.inicio)
            m.u16(DESTINO, p.destino)
        return p

    def calcular(self, mundo):
        """CheminCalcul 0x42f214 on the prepared context: nothing unless a search is open (0x4e0f36 set,
        0x4e0f37 and 0x496302 clear); else the contours, choice and optimization, applied to the world."""
        m = self._m
        if not m.u8(0x4e0f36) or m.u8(0x4e0f37) or m.u8(0x496302):
            return None
        indice = m.u16(0x496304)
        resultado = self.iniciar(mundo, indice)
        mundo._aplicar_resultado(indice, resultado)
        return resultado