"""AffGame tail after the HUD checkpoint: the bottom strip and the cursor (0x417B1C..0x417D30), render API 1.5.

Reconstructed from the intact executable and the native capture ``evidencias/captura-hud-m22-v2.json`` (committed
before this module); the additive M3 branches use captures committed as 5b05e41/5405033.  The order is AffGame's own: three AffCompteurMatiere counters, AffZoneIconeAction, AffTrame,
the blinking target marker, AffMarche, AffMiniMap, AffChrono, AffZoneInfo, AffInfoAide, AffDebug, EvenementAffiche,
MessageBoxAffiche, AffDrapeauAlliance, the mouse-position copy and the cursor bob.  It ends at 0x417D30, the
DDUnlockSurface call after which AffGame no longer writes the offscreen surface.

Only the branches the native capture exercised are composed.  Every other branch raises ``DependenciaQuadro`` at its
original address (``ENDERECOS_PARADA``); nothing is defaulted.  Reads go through ``LeituraHud`` (live memory, with the
AffGame prefix's own writes overlaid); the only writes, the mouse-position copy 0x49A042/44, are returned as effects.
"""
import struct
from graficos import compor_indices, Quadro
from composicao import compor_sombra
from construcoes import tabelas_jogador
from quadro_jogo import DependenciaQuadro
import hud_scriptado_m3 as script_m3

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
    0x417086: 'AffZoneIconeAction: slot kind/value outside 1.5 (kind 0 percent 0..100, 1, 2 value 0..999)',
    0x41729b: 'AffTrame: placement frame mode 0x4E05AE = 3 (BatimentTailleGet, Box, FilledBoxGris)',
    0x417ba2: 'target marker outside the captured animation IDs 0x1E03..0x1E09',
    0x4667a7: 'AffMarche: market state 1..4 for the camera player (InitGameZone, market icons)',
    0x46a70c: 'AffMiniMap outside the captured geometry',
    0x401d18: 'AffChrono: a selected structure (recruitment/time gauge)',
    0x41a5b8: 'AffChrono: actual BatimentEstHabiter dependency is missing',
    0x423f9d: 'AffChrono: recruitment target outside captured unit types',
    0x423ec8: 'AffChrono: zero recruitment duration',
    0x401ef1: 'AffChrono: percentage outside captured clock strip',
    0x401e56: 'AffChrono: margin outside captured zero',
    0x401e11: 'AffChrono: minimap layout outside captured 0/1',
    0x45b796: 'AffChrono: original shadow table dependency is missing',
    0x40f77b: 'AffZoneInfo: cost counter exceeds 9999',
    0x40f8c0: 'AffInfoAide: tooltip text pointer 0x4E060C set (AffTextEncadre)',
    0x417c7f: 'AffDebug enabled (0x4E17AC)',
    0x417c8a: 'EvenementAffiche: an event is in progress',
    0x469c5f: 'MessageBoxAffiche: message queue not empty (AffText)',
    0x417604: 'AffDrapeauAlliance: allied player flag (PastePlayerCmp)',
    0x4175f2: 'AffDrapeauAlliance: player contacting for an alliance (blinking flag)',
    0x417cfc: 'second cursor count outside 0..16',
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
    def __init__(self, leitura, superficie, catalogo, evento, texto=None, tabela_sombra=None, habitado=None):
        self.m, self.catalogo, self.evento = leitura, catalogo, evento
        self.largura, self.altura = leitura.u32(0x4e17a0), 600     # pitch as the blitters read it
        if self.largura != LARGURA_FIXA_MINIMAPA or len(superficie) != self.largura*self.altura:
            raise ValueError('The HUD tail is composed only for the 800 x 600 surface with pitch 800')
        self.saida = bytearray(superficie)
        self.chamadas, self.efeitos = [], []
        self.camera = leitura.u8(0x508041)
        self.texto = texto
        self.tabela_sombra = tabela_sombra
        self.habitado = habitado

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
        selected = None
        def selection():
            nonlocal selected
            if selected is None: selected = self.m.u16(0x496d4a)
            return selected
        left = self.m.u16(0x4e2440)
        self.bob(8, 547, 0x29b5 if left == VAZIO_ICONE else (0x2a39 if selection() == 8 else 0x2a37), False)
        for i in range(4):
            slot, x = 0x4e2410+6*i, 31+60*i
            ident = self.m.u16(slot)
            if ident == VAZIO_ICONE:
                self.bob(x, 547, VAZIO_ICONE+i, False)
                continue
            self.bob(x, 547, 0x29b7, False)
            self.bob(x+2, 549, ident, False)
            kind = self.m.u16(slot+2)
            if kind == 0:
                value = self.m.u16(slot+4)
                if value > 100: self.parar(0x417086, f'slot {i} percent {value}')
                mask = 0x2a1d-value*42//100
                self.chamadas.append(['PasteNoirBlancCmp', x+2, 549, mask, 0])
                table = self.m.ler(self.m.u32(0x4e24bc), 256)
                self.saida[:] = compor_sombra(bytes(self.saida), self.largura, self.altura,
                                              self.catalogo.quadro(mask), x+2, 549, table)
            elif kind == 2:
                value = self.m.u16(slot+4)
                if value > 999: self.parar(0x417086, f'slot {i} counter {value}')
                leading = True
                for j, digit in enumerate((value//100, value//10 % 10, value % 10)):
                    if leading and not digit and j < 2: continue
                    self.bob(x+22+12*j, 582, 0x2a22+2*digit, False)
                    leading = False
            elif kind != 1: self.parar(0x417086, f'slot {i} kind {kind}')
            if selection() == i: self.bob(x+2, 549, 0x2a36, False)
        right = self.m.u16(0x4e2446)
        self.bob(272, 547, 0x29b6 if right == VAZIO_ICONE else (0x2a3a if selection() == 9 else 0x2a38), False)

    def player(self, x, y, ident, owner):
        self.chamadas.append(['PastePlayerCmp', x, y, ident, 1, owner])
        q = self.catalogo.quadro(ident)
        q = Quadro(q.largura, q.altura, q.pixels.translate(tabelas_jogador()[owner]), q.opacidade, 0, b'')
        clip = (self.m.u16(0x49a020), self.m.u16(0x49a01c), self.m.u16(0x49a022), self.m.u16(0x49a01e))
        self.saida[:] = compor_indices(bytes(self.saida), self.largura, self.altura, q, x, y, clip)

    def gravar(self, name, address, value):
        old, new = self.m.ler(address, 2), struct.pack('<H', value)
        if old != new: self.efeitos.append((name, address, old.hex(), new.hex()))
        self.m.sobrepostos.update({address+i:v for i,v in enumerate(new)})

    def alvo(self):
        cell = self.m.u16(0x496204)
        if cell == 0xffff: return
        ident = self.m.u16(0x4e05ac)
        if not 0x1e03 <= ident <= 0x1e09: self.parar(0x417ba2)
        if not self.m.u8(0x508f7c) & 1:
            ident += 1
            self.gravar('alvo_animacao_u16', 0x4e05ac, ident)
        x = (cell % 256-self.m.u16(0x508720))*32+12
        y = (cell//256-self.m.u16(0x508722))*32+12
        i16 = lambda v: (v+32768) % 65536-32768
        self.player(i16(x), i16(y), ident, self.camera)
        if ident == 0x1e0a:
            self.gravar('alvo_animacao_u16', 0x4e05ac, 0x1e03)
            self.gravar('alvo_celula_u16', 0x496204, 0xffff)

    def trama(self):
        """AffTrame 0x41721F (EBX = 0): returns unless the mouse is inside the view and mode 0x4E05AE is 3."""
        mx, my = self.m.u16(0x5099a8), self.m.u16(0x5099aa)
        if mx > self.m.u16(0x508724)*32 or my > self.m.u16(0x508726)*32: return
        if self.m.u16(0x4e05ae) == 3: script_m3.placement(self)

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
        """AffChrono 0x401CC6: no selection, or the captured sanctuary with no recruitment underway."""
        selected = self.m.u16(0x496ac4)
        if selected == 0xffff: selected = self.m.u16(0x495be0+2*self.camera)
        if selected == 0xffff: return
        if selected >= 1000: self.parar(0x401d18)
        record = 0x49a0c8+276*selected
        if self.m.u8(record+4)!=self.camera:return
        if self.m.u8(record+8)==3 and self.m.u8(record+5)==5:return
        if (self.m.u8(record+4) == self.camera == 0 and self.m.u8(record+8) == 2
                and self.m.u8(record+5) == 5 and self.m.u16(record+0x74) == 0): return
        if self.camera == 0 and self.m.u8(record+8) == 2 and self.m.u8(record+5) in (4,5):
            if not callable(self.habitado): self.parar(0x41a5b8,'active recruitment clock requires BatimentEstHabiter')
            if not self.habitado(selected): return
            from cronometro_s1_graficos import compor_cronometro_s1
            return compor_cronometro_s1(self,record)
        self.parar(0x401d18)

    def zona_info(self):
        """AffZoneInfo 0x40F758: panel, then the prioritized cost-counter rows (values 0..9999)."""
        self.bob(0x12a, 0x223, 0x29b8, False)
        def counter(value, y):
            if value > 9999: self.parar(0x40f77b, str(value))
            x, leading = 328, True
            for i, digit in enumerate((value//1000, value//100 % 10, value//10 % 10, value % 10)):
                if leading and not digit and i < 3:
                    if i == 2: self.bob(x, y, 0x2a21, False); x += 12
                    continue
                self.bob(x, y, 0x2a22+2*digit, False)
                x += 12; leading = False
        def row(value, ident, top):
            self.bob(299, top, ident, False)
            self.bob(327, top+4, 0x2a45, False)
            counter(value, top+5)
        value = self.m.u16(0x4e0618)
        if value:
            row(value, 0x2a46, 548); return
        value = self.m.u16(0x4e0612)
        if value: row(value, 0x2a43, 548)
        value = self.m.u16(0x4e0614)
        if value: row(value, 0x2a44, 574)
        else:
            value = self.m.u16(0x4e0616)
            if value: row(value, 0x2a42, 574)

    def info_ajuda(self):
        """AffInfoAide 0x40F8AA: returns while the tooltip text pointer 0x4E060C is NULL."""
        if self.m.u32(0x4e060c): script_m3.tooltip(self)

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
        self.alvo()
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
            second = self.m.u16(0x4e062c)
            if second:
                if second > 16: self.parar(0x417cfc)
                self.bob(self.m.i16(0x5099a8), self.m.i16(0x5099aa), (self.m.u16(0x49a010)+16-second) & 0xffff, True)
        return bytes(self.saida)


def compor_hud(leitura, superficie, *, catalogo, evento, texto=None, tabela_sombra=None, habitado=None):
    """Compose AffGame's tail 0x417B1C..0x417D30 over ``superficie`` (the surface at the checkpoint).

    leitura: LeituraHud over the live memory with the AffGame prefix's writes overlaid. evento: EvenementEnCours as
    read by the prefix (AffGame's local [ebp-4]). Returns dict(superficie, chamadas, efeitos); raises
    DependenciaQuadro (partial surface, calls and effects) at the first branch outside the captured domain.
    """
    h = _Hud(leitura, superficie, catalogo, evento, texto, tabela_sombra, habitado)
    pixels = h.compor()
    return dict(superficie=pixels, chamadas=h.chamadas, efeitos=h.efeitos)
