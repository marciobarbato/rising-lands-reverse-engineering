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

Not modeled: CheminCalcul's contour-engine scratch, which the Python solver has no field for. These
are u8 0x4e0f40, the record pointer u32 0x4e0f50, the contour state u8 0x4e0f68 and u16 0x4e1772.
The native differential reports them as remaining differences.
"""
from mundo_vivo import ponteiros_rotas, vista_de
from solucionador_python import SolucionadorCaminhosPython

BUFFERS = (0x4e116a, 0x4e136a)
REGIOES, REGISTROS = 0x4e0f6a, (0x4e0f54, 0x4e0f5e)
INICIO, DESTINO = 0x4e0f44, 0x4e0f46
FLAGS, DONO, MASCARA, CLASSE = (0x4e0f34, 0x4e0f35), 0x4e0f41, 0x4e0f42, 0x4e0f48
NAO_MODELADOS = (0x4e0f40, 0x4e0f50, 0x4e0f68, 0x4e1772)


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
        u = mundo.unidades
        m.u8(DONO, u[indice * 276])
        m.u8(CLASSE, m.u8(0x4962c8 + u[indice * 276 + 1]))
        # DeplaceEngin 0x44937f..0x4493a5 passes mask 1 + (+0xab != 0) in CL and two zero stack flags.
        m.u8(MASCARA, 1 + int(u[indice * 276 + 0xab] != 0))
        for f in FLAGS:
            m.u8(f, 0)

    def iniciar(self, mundo, indice):
        self._carregar()
        resultado = super().iniciar(mundo, indice)
        self._guardar(mundo, indice)
        return resultado
