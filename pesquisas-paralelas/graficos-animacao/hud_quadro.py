"""AffGame tail after the HUD checkpoint: the bottom strip and the cursor (0x417B1C..0x417D30), render API 1.4.

Reconstructed from the intact executable and the native capture ``evidencias/captura-hud-m22-v2.json`` (committed
before this module).  The order is AffGame's own: three AffCompteurMatiere counters, AffZoneIconeAction, AffTrame,
the blinking target marker, AffMarche, AffMiniMap, AffChrono, AffZoneInfo, AffInfoAide, AffDebug, EvenementAffiche,
MessageBoxAffiche, AffDrapeauAlliance, the mouse-position copy and the cursor bob.  It ends at 0x417D30, the
DDUnlockSurface call after which AffGame no longer writes the offscreen surface.

Only the branches the native capture exercised are composed.  Every other branch raises ``DependenciaQuadro`` at its
original address (``ENDERECOS_PARADA``); nothing is defaulted.  Reads go through ``LeituraHud`` (live memory, with the
AffGame prefix's own writes overlaid); the only writes, the mouse-position copy 0x49A042/44, are returned as effects.
"""
import struct
from graficos import compor_indices
from quadro_jogo import DependenciaQuadro

FIM_HUD = 0x417D30
LARGURA_FIXA_MINIMAPA = 800      # AffMiniMap 0x46A737..0x46A749: destination row stride is the constant 25*32
# AffCompteurMatiere 0x417F38 (x, y) per resource k = 0..2 (call sites 0x417B32..0x417B7E); y = 0x22D
CONTADORES = ((0x1ec, 0x22d), (0x21c, 0x22d), (0x24c, 0x22d))
BOB_ALGARISMO = 0x2a22           # + 2*digit + highlight bit (0x417FF1..0x417FFC)
BOB_ALGARISMO_VAZIO = 0x2a21     # leading blank (0x4180BA)
BOB_MILHAR = 0x2a3c              # one icon per thousand, at y - 9 (0x417F91)
VAZIO_ICONE = 0x29b1             # empty action slot word (AffZoneIconeAction)
ENDERECOS_PARADA = {
    0x417f6e: 'AffCompteurMatiere: counter value above 9999 (outside the captured domain)',
    0x416f64: 'AffZoneIconeAction: first slot word 0x4E2440 is not the empty icon 0x29B1',
    0x417086: 'AffZoneIconeAction: action slot holds an icon (digits, PasteNoirBlancCmp, selection frame)',
    0x4171be: 'AffZoneIconeAction: last slot word 0x4E2446 is not the empty icon 0x29B1',
    0x41729b: 'AffTrame: placement frame mode 0x4E05AE = 3 (BatimentTailleGet, Box, FilledBoxGris)',
    0x417ba2: 'target marker 0x496204 set (PastePlayerCmp blink, writes 0x4E05AC)',
    0x4667a7: 'AffMarche: market state 1..4 for the camera player (InitGameZone, market icons)',
    0x46a70c: 'AffMiniMap outside the captured geometry',
    0x401d18: 'AffChrono: a selected structure (recruitment/time gauge)',
    0x40f77b: 'AffZoneInfo: cost counters 0x4E0612..0x4E0618 nonzero (AffCompteurCoutMatiere)',
    0x40f8c0: 'AffInfoAide: tooltip text pointer 0x4E060C set (AffTextEncadre)',
    0x417c7f: 'AffDebug enabled (0x4E17AC)',
    0x417c8a: 'EvenementAffiche: an event is in progress',
    0x469c5f: 'MessageBoxAffiche: message queue not empty (AffText)',
    0x417604: 'AffDrapeauAlliance: allied player flag (PastePlayerCmp)',
    0x4175f2: 'AffDrapeauAlliance: player contacting for an alliance (blinking flag)',
    0x417cfc: 'second cursor bob 0x4E062C nonzero',
}


class LeituraHud:
    """Read view: ``memoria`` (MemoriaDeclarada: u8/u16/u32/ler_mundo) with byte overrides {address: value}."""
    def __init__(self, memoria, sobrepostos=None):
        self.memoria, self.sobrepostos = memoria, dict(sobrepostos or {})

    def ler(self, endereco, n):
        if any(endereco+i in self.sobrepostos for i in range(n)):
            return bytes(self.sobrepostos[a] if a in self.sobrepostos else self.memoria.ler_mundo(a, 1)[0]
                         for a in range(endereco, endereco+n))
        return bytes(self.memoria.ler_mundo(endereco, n))

    def u8(self, a): return self.ler(a, 1)[0]
    def u16(self, a): return struct.unpack('<H', self.ler(a, 2))[0]
    def i16(self, a): return struct.unpack('<h', self.ler(a, 2))[0]
    def u32(self, a): return struct.unpack('<I', self.ler(a, 4))[0]


class _Hud:
    def __init__(self, leitura, superficie, catalogo, evento):
        self.m, self.catalogo, self.evento = leitura, catalogo, evento
        self.largura, self.altura = leitura.u32(0x4e17a0), 600     # pitch as the blitters read it
        if self.largura != LARGURA_FIXA_MINIMAPA or len(superficie) != self.largura*self.altura:
            raise ValueError('The HUD tail is composed only for the 800 x 600 surface with pitch 800')
        self.saida = bytearray(superficie)
        self.chamadas, self.efeitos = [], []
        self.camera = leitura.u8(0x508041)

    def parar(self, endereco, extra=''):
        raise DependenciaQuadro(endereco, ENDERECOS_PARADA[endereco] + (f': {extra}' if extra else ''),
                                superficie=bytes(self.saida), chamadas=self.chamadas, efeitos=self.efeitos)

    # PasteBobCmp 0x45B247: clip flag 0 -> the fixed screen box (0, 0, 0x31F, 0x257); nonzero -> the clip words 0x49A01C..
    def bob(self, x, y, id_motor, recorte):
        if recorte:
            topo, base, esquerda, direita = (self.m.u16(0x49a01c), self.m.u16(0x49a01e), self.m.u16(0x49a020), self.m.u16(0x49a022))
            caixa = (esquerda, topo, direita, base)
        else:
            caixa = (0, 0, 0x31f, 0x257)
        self.chamadas.append(['PasteBobCmp', x, y, id_motor, int(bool(recorte))])
        self.saida[:] = compor_indices(bytes(self.saida), self.largura, self.altura, self.catalogo.quadro(id_motor), x, y, caixa)

    # Box 0x45C912 (x0, y0, x1, y1, color, clip flag): outline, clipped to the screen or the clip words
    def caixa(self, x0, y0, x1, y1, cor, recorte):
        self.chamadas.append(['Box', x0, y0, x1, y1, cor, int(bool(recorte))])
        if recorte:
            topo, base, esquerda, direita = (self.m.u16(0x49a01c), self.m.u16(0x49a01e), self.m.u16(0x49a020), self.m.u16(0x49a022))
        else:
            topo, esquerda, direita, base = 0, 0, self.m.u16(0x49a018)-1, self.m.u16(0x49a01a)-1
        if x0 > direita or y0 > base or x1 < esquerda or y1 < topo: return
        x0, y0 = max(x0, esquerda), max(y0, topo)
        x1, y1 = min(x1, direita), min(y1, base)
        if x1 < x0: x0, x1 = x1, x0
        if y1 < y0: y0, y1 = y1, y0
        p, s = self.largura, self.saida
        s[y0*p+x0:y0*p+x1+1] = bytes([cor])*(x1-x0+1)
        s[y1*p+x0:y1*p+x1+1] = bytes([cor])*(x1-x0+1)
        for y in range(y0, y1+1):
            s[y*p+x0] = cor; s[y*p+x1] = cor

    # ------------------------------------------------------------------ routines, in AffGame's order
    def contador(self, k, x, y):
        """AffCompteurMatiere 0x417F38: four BCD positions; thousands as icons, leading blanks, highlight bits."""
        base = 0x4e2eac + 8*(4*self.camera+k)
        valor, brilho = self.m.u16(base), self.m.u8(base+2)
        self.chamadas.append(['AffCompteurMatiere', k, valor, brilho])
        if valor > 9999: self.parar(0x417f6e, f'resource {k} value {valor}')
        digitos = (valor//1000, valor//100 % 10, valor//10 % 10, valor % 10)   # IntToBCD 0x467CD1, most significant first
        inicial = True
        for i in range(4):
            bit = (brilho >> (3-i)) & 1                                          # GetBit 0x467D97
            if digitos[i] == 0 and inicial and i != 3 and not bit:
                if i: self.bob(x, y, BOB_ALGARISMO_VAZIO, False)
                x += 12; continue
            if i == 0:
                for j in range(min(digitos[0], 4)):
                    self.bob(x+12+8*j, y-9, BOB_MILHAR, False)
            else:
                self.bob(x, y, BOB_ALGARISMO + 2*digitos[i] + bit, False)
            inicial = False
            x += 12

    def zona_icone_acao(self):
        """AffZoneIconeAction 0x416F29: redrawn only while the force flag 0x4E05A2 is set."""
        if not self.m.u8(0x4e05a2): return
        self.chamadas.append(['AffZoneIconeAction'])
        if self.m.u16(0x4e2440) != VAZIO_ICONE: self.parar(0x416f64)
        self.bob(8, 0x223, 0x29b5, False)
        for i in range(4):
            if self.m.u16(0x4e2410+6*i) != VAZIO_ICONE: self.parar(0x417086, f'slot {i}')
            self.bob(0x1f+0x3c*i, 0x223, VAZIO_ICONE+i, False)
        if self.m.u16(0x4e2446) != VAZIO_ICONE: self.parar(0x4171be)
        self.bob(0x110, 0x223, 0x29b6, False)

    def trama(self):
        """AffTrame 0x41721F (EBX = 0): returns unless the mouse is inside the view and mode 0x4E05AE is 3."""
        mx, my = self.m.u16(0x5099a8), self.m.u16(0x5099aa)
        if mx > self.m.u16(0x508724)*32 or my > self.m.u16(0x508726)*32: return
        if self.m.u16(0x4e05ae) == 3: self.parar(0x41729b)

    def marcha(self):
        """AffMarche 0x46677D: market state byte 0x4E2E7C[camera]; 0 and > 4 return."""
        estado = self.m.u8(0x4e2e7c+self.camera)
        if 1 <= estado <= 4: self.parar(0x4667a7, f'state {estado}')

    def minimapa(self):
        """AffMiniMap 0x46A70C: frame box, row copy of the minimap buffer, view box (both boxes clipped)."""
        mx, my = self.m.u16(0x507d68), self.m.u16(0x507d6a)
        w, h = self.m.u16(0x496fe0), self.m.u16(0x496fe2)
        cw, ch = self.m.u16(0x497168), self.m.u16(0x49716a)
        if not (0 < w and 0 < h and mx+1+w <= self.largura and my+1+h <= self.altura and cw and ch):
            self.parar(0x46a70c, f'position ({mx},{my}) size {w}x{h} map {cw}x{ch}')
        self.chamadas.append(['AffMiniMap', mx, my, w, h])
        self.caixa(mx, my, mx+w+1, my+h+1, 0x14, True)
        dados = self.m.ler(self.m.u32(0x507d5c), w*h)
        for y in range(h):
            o = (my+1+y)*LARGURA_FIXA_MINIMAPA + mx+1
            self.saida[o:o+w] = dados[y*w:(y+1)*w]
        ox, oy = self.m.u16(0x508720), self.m.u16(0x508722)
        jx, jy = self.m.u16(0x508724), self.m.u16(0x508726)
        self.caixa(ox*w//cw+mx+1, oy*h//ch+my+1, (ox+jx)*w//cw+mx+1, (oy+jy)*h//ch+my+1, 1, True)

    def cronometro(self):
        """AffChrono 0x401CC6: only the no-selection exit (selected structure 0x496AC4 and 0x495BE0[camera] = 0xFFFF)."""
        if self.m.u16(0x496ac4) != 0xffff or self.m.u16(0x495be0+2*self.camera) != 0xffff: self.parar(0x401d18)

    def zona_info(self):
        """AffZoneInfo 0x40F758: the info panel bob, then cost counters (only all-zero is composed)."""
        self.bob(0x12a, 0x223, 0x29b8, False)
        if any(self.m.u16(a) for a in (0x4e0618, 0x4e0612, 0x4e0614, 0x4e0616)): self.parar(0x40f77b)

    def info_ajuda(self):
        """AffInfoAide 0x40F8AA: returns while the tooltip text pointer 0x4E060C is NULL."""
        if self.m.u32(0x4e060c): self.parar(0x40f8c0)

    def drapeau_alliance(self):
        """AffDrapeauAlliance 0x417581: no flag while no other player 0..3 is allied or contacting the camera player."""
        jogadores = self.m.u32(0x5080a8)
        for i in range(4):
            if i == self.camera: continue
            if self.camera <= 4 and self.m.u8(jogadores+20*self.camera+6) & (1 << i):   # PlayerEstAllie 0x46D838
                self.parar(0x417604, f'player {i}')
            if self.m.u32(0x5080b0+16*self.camera+4*i):                                   # PlayerEstContacterPourAlliance 0x46DA1E
                self.parar(0x4175f2, f'player {i}')

    def compor(self):
        for k, (x, y) in enumerate(CONTADORES): self.contador(k, x, y)
        self.zona_icone_acao()
        self.trama()
        if self.m.u16(0x496204) != 0xffff: self.parar(0x417ba2)
        self.marcha()
        if self.m.u8(0x497285): self.minimapa()
        self.cronometro()
        self.zona_info()
        self.info_ajuda()
        if self.m.u8(0x4e17ac): self.parar(0x417c7f)
        if self.evento: self.parar(0x417c8a)
        if self.m.u16(0x507d56) != self.m.u16(0x507d54): self.parar(0x469c5f)
        self.drapeau_alliance()
        mx, my = self.m.u16(0x5099a8), self.m.u16(0x5099aa)
        for nome, endereco, valor in (('mouse_x_copia_u16', 0x49a042, mx), ('mouse_y_copia_u16', 0x49a044, my)):
            antigo, novo = self.m.ler(endereco, 2), struct.pack('<H', valor)     # 0x417CA0..0x417CB2
            if novo != antigo: self.efeitos.append((nome, endereco, antigo.hex(), novo.hex()))
        if self.m.u8(0x49a054) == 0:
            self.bob(self.m.i16(0x5099a8), self.m.i16(0x5099aa), (self.m.u16(0x49a010)+self.m.u16(0x49a014)) & 0xffff, True)
            if self.m.u16(0x4e062c): self.parar(0x417cfc)
        return bytes(self.saida)


def compor_hud(leitura, superficie, *, catalogo, evento):
    """Compose AffGame's tail 0x417B1C..0x417D30 over ``superficie`` (the surface at the checkpoint).

    leitura: LeituraHud over the live memory with the AffGame prefix's writes overlaid. evento: EvenementEnCours as
    read by the prefix (AffGame's local [ebp-4]). Returns dict(superficie, chamadas, efeitos); raises
    DependenciaQuadro (partial surface, calls and effects) at the first branch outside the captured domain.
    """
    h = _Hud(leitura, superficie, catalogo, evento)
    pixels = h.compor()
    return dict(superficie=pixels, chamadas=h.chamadas, efeitos=h.efeitos)
