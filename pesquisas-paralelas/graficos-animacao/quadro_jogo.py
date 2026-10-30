"""AffGame 0x417698 in-game frame (mode 0x12) through the HUD checkpoint 0x417B1C.

Order: CalculFrame, EvenementEnCours, draw-cadence gate, optional clears,
DDLockSurface, saved-background restore, AffTerrain, AffSprite with the four
renderers, selection box, then the HUD (not composed). Every global write is
returned as an explicit effect; renderers outside committed domains raise
DependenciaQuadro at their original call site with the partial surface.
"""
import struct
import sobreposicoes_entrada_m3 as entrada_m3
import cave_scriptada_m3 as cave_m3
from cache_terreno import resolver_bloco_terreno
from passe_terreno import planejar_passe_terreno, executar_passe_terreno, pixels_bloco_terreno, compor_bloco_terreno
from passe_sprites import planejar_passe_sprites
from sequenciais import consultar_objeto_v6
from objetos import consultar_objeto, compor_passe
from composicao import encaminhamento, compor_unidade
from graficos import TIPOS, localizar, Quadro, compor_indices
from projeteis_graficos import compor_projetil
from construcoes import consultar_santuario, compor_fachada, tabelas_jogador as _tabelas_jogador
from corpo_tipos1_8 import CORPOS as CORPOS_TIPOS1_8, compor_corpo_tipos1_8

CHECKPOINT_HUD = 0x417B1C
MODO_JOGO = 0x12
DDERR_SURFACELOST = 0x887601C2
# (name, address, width): every global the world-view prefix reads or writes.
GLOBAIS_QUADRO = (
    ('rng_u8', 0x4e1d18, 1), ('evento_u8', 0x4e1b0e, 1), ('pitch_u32', 0x4e17a0, 4),
    ('dd_ponteiro_u32', 0x4e17a4, 4), ('dd_travas_u32', 0x4e17a8, 4), ('fps_contador_u16', 0x4e17ae, 2),
    ('fps_ultimo_tick_u32', 0x4e17b0, 4), ('fps_tick_u32', 0x4e17b4, 4), ('caixa_selecao_u8', 0x4e19b0, 1),
    ('forcar_desenho_u8', 0x4e05a2, 1), ('modo_jogo_u8', 0x4e2f78, 1), ('fps_digitos', 0x496394, 3),
    ('paginas_texto', 0x4963b4, 4), ('selecionada_unidade_u16', 0x496ac2, 2),
    ('selecionada_estrutura_u16', 0x496ac4, 2), ('divisor_u8', 0x497284, 1), ('largura_tela_u16', 0x49a018, 2),
    ('altura_tela_u16', 0x49a01a, 2), ('recorte', 0x49a01c, 8), ('recorte_salvo', 0x49a02c, 8),
    ('restaurar_fundo_u8', 0x49a041, 1), ('paginas_u8', 0x49a05b, 1), ('camera_u8', 0x508041, 1),
    ('origem', 0x508720, 4), ('janela', 0x508724, 4), ('superficie_u32', 0x508f70, 4),
    ('quadro_u32', 0x508f7c, 4), ('modo_selecao_u8', 0x508f8f, 1), ('margem_i8', 0x508f90, 1),
    ('limpar_u8', 0x508f92, 1))
LARGURAS = {nome: largura for nome, endereco, largura in GLOBAIS_QUADRO}
ENDERECOS = {nome: endereco for nome, endereco, largura in GLOBAIS_QUADRO}
# AffBatiments terrain switch 0x40F23B..0x40F342; AffVehiculeAtelier 0x402880.
GATILHOS_FACHADA = frozenset((0x2cb, 0x2ed, 0x2fb, 0x30d, 0x326, 0x343, 0x35e, 0x37a, 0x388, 0x390, 0x398,
    0x3b0, 0x3ce, 0x3e1, 0x3f8, 0x406, 0x40e, 0x42a, 0x436))
OFICINA = 0x356
# TypeEnginSeFatigue 0x442C34: jump table 0x442BCC over types 0..25 (type > 25 answers false)
SE_FATIGUE = tuple(int(c) for c in '11111111111000000000000001')
ICONE_FADIGA = 0x1e2b   # bob id = unit word +4 + 0x1E2B (0x41362E / 0x413650)
GATILHO_SANTUARIO = 0x2ed   # type-2 structure facade trigger (terrain switch 0x40F23B)
OBJETO_MURO, OBJETO_PORTAO = 254, 253  # bytes 0x495BF8/0x495BF9
# AffVeget table 0x415A58: codes with a handler; others return at 0x410B38.
CODIGOS_AFFVEGET = frozenset((65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 27, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1))


class DependenciaQuadro(NotImplementedError):
    """Unsupported original branch: address, detail, partial surface and effects so far."""
    def __init__(self, endereco, detalhe, *, superficie=None, chamadas=(), efeitos=()):
        self.endereco, self.detalhe = endereco, detalhe
        self.superficie, self.chamadas, self.efeitos = superficie, list(chamadas), list(efeitos)
        super().__init__(f'AffGame frame dependency at 0x{endereco:08x}: {detalhe}')


class EstadoTela:
    """Mutable globals of the in-game frame, as raw little-endian bytes."""
    def __init__(self, globais):
        if set(globais) != set(LARGURAS):
            raise ValueError('Expected exactly the AffGame prefix globals')
        self._bytes = {}
        for nome, valor in globais.items():
            if not isinstance(valor, (bytes, bytearray)) or len(valor) != LARGURAS[nome]:
                raise ValueError('Global width mismatch: '+nome)
            self._bytes[nome] = bytes(valor)
        self.efeitos = []

    def bruto(self, nome): return self._bytes[nome]
    def u(self, nome): return int.from_bytes(self._bytes[nome], 'little')
    def palavras(self, nome): return struct.unpack('<%dH' % (LARGURAS[nome]//2), self._bytes[nome])

    def gravar(self, nome, valor):
        novo = valor.to_bytes(LARGURAS[nome], 'little') if isinstance(valor, int) else bytes(valor)
        if len(novo) != LARGURAS[nome]: raise ValueError('Global width mismatch: '+nome)
        antigo = self._bytes[nome]; self._bytes[nome] = novo
        if novo != antigo: self.efeitos.append((nome, ENDERECOS[nome], antigo.hex(), novo.hex()))

    def instantaneo(self): return dict(self._bytes)


class MundoQuadro:
    """Read-only world buffers the prefix consumes (camera-indexed visibility)."""
    TAMANHOS = dict(terreno=131072, objetos=65536, auxiliares=65536, regioes=131072, unidades=220800, projeteis=5600)

    def __init__(self, *, terreno, objetos, auxiliares, regioes, unidades, projeteis, descoberta, iluminacao, estruturas=None):
        valores = dict(terreno=terreno, objetos=objetos, auxiliares=auxiliares, regioes=regioes, unidades=unidades, projeteis=projeteis)
        for nome, valor in valores.items():
            if len(valor) != self.TAMANHOS[nome]: raise ValueError('Invalid world buffer: '+nome)
            setattr(self, nome, bytes(valor))
        if len(descoberta) != 4 or len(iluminacao) != 4 or any(len(m) != 65536 for m in list(descoberta)+list(iluminacao)):
            raise ValueError('Expected four 65536-byte discovery and lighting maps')
        self.descoberta, self.iluminacao = [bytes(m) for m in descoberta], [bytes(m) for m in iluminacao]
        if estruturas is not None and len(estruturas) != 1000*276: raise ValueError('Structure pool must be 1000 x 276 bytes')
        self.estruturas = None if estruturas is None else bytes(estruturas)   # DGROUP 0x49A0C8; None = not inherited

    def palavra(self, nome, celula): return struct.unpack_from('<H', getattr(self, nome), celula*2)[0]


def calcular_frame(tela, relogio):
    """CalculFrame 0x43F710: FPS counter/ticks/digits and the page-count text."""
    tela.gravar('fps_contador_u16', (tela.u('fps_contador_u16')+1) & 0xffff)
    if not callable(relogio):
        raise DependenciaQuadro(0x43F71A, 'KERNEL32 GetTickCount binding is not supplied', efeitos=tela.efeitos)
    tick = relogio()
    if type(tick) is not int or not 0 <= tick <= 0xFFFFFFFF: raise ValueError('GetTickCount must return u32')
    tela.gravar('fps_tick_u32', tick)
    if (tick-tela.u('fps_ultimo_tick_u32')) & 0xFFFFFFFF >= 1000:
        tela.gravar('fps_ultimo_tick_u32', tick)
        contador = tela.u('fps_contador_u16')
        if contador > 99: tela.gravar('fps_contador_u16', 99); contador = 99
        tela.gravar('fps_digitos', bytes(((contador//10+0x30) & 255, (contador % 10+0x30) & 255, 0)))
        tela.gravar('fps_contador_u16', 0)
    texto = str(tela.u('paginas_u8')).encode('ascii')+b'\0'  # itoa(byte 0x49A05B, 0x4963B4, 10)
    tela.gravar('paginas_texto', texto+tela.bruto('paginas_texto')[len(texto):])


def travar_superficie(tela, directdraw):
    """DDLockSurface 0x43F3B4 over the IDirectDrawSurface binding."""
    if tela.u('dd_travas_u32') == 0 or tela.u('dd_ponteiro_u32') == 0:
        def metodo(nome, endereco):
            f = getattr(directdraw, nome, None)
            if not callable(f):
                raise DependenciaQuadro(endereco, f'IDirectDrawSurface::{nome} binding is not supplied', efeitos=tela.efeitos)
            return f
        if metodo('is_lost', 0x43F3D7)() == DDERR_SURFACELOST:
            metodo('restore', 0x43F3E4)()
        hresultado, ponteiro = metodo('lock', 0x43F40C)()
        if hresultado != 0:
            return 0
        tela.gravar('pitch_u32', 800); tela.gravar('dd_ponteiro_u32', ponteiro)
    tela.gravar('dd_travas_u32', (tela.u('dd_travas_u32')+1) & 0xFFFFFFFF)
    return tela.u('dd_ponteiro_u32')


class _Composicao:
    def __init__(self, mundo, tela, superficie, catalogo, ciclo, sombra, eclairage):
        self.mundo, self.tela, self.catalogo, self.ciclo = mundo, tela, catalogo, ciclo
        self.sombra, self.eclairage = sombra, eclairage
        self.largura, self.altura = tela.u('pitch_u32'), tela.u('altura_tela_u16')
        self.saida = bytes(superficie); self.chamadas = []
        self.camera = tela.u('camera_u8')
        if self.camera > 3: raise ValueError('camera_u8 must select one of four player maps')
        self.descoberta, self.iluminacao = mundo.descoberta[self.camera], mundo.iluminacao[self.camera]
        self.leitura_entrada = None
        self.habitado = self.relogios_extra = self.selecao_estruturas = self.tabelas_jogador = None

    def recorte(self):
        topo, base, esquerda, direita = self.tela.palavras('recorte')
        return (esquerda, topo, direita, base)

    def parar(self, endereco, detalhe):
        raise DependenciaQuadro(endereco, detalhe, superficie=self.saida, chamadas=self.chamadas, efeitos=self.tela.efeitos)

    # AffTerrain callbacks
    def bloco(self, x, y, celula, fonte):
        self.chamadas.append(['GetNumBob', fonte, celula])
        try:
            plano = resolver_bloco_terreno(self.catalogo, self.ciclo.cache, id_terreno_u16=fonte,
                descoberta_u8=self.descoberta[celula], iluminacao_u8=self.iluminacao[celula], tabela_sombra=self.sombra)
        except NotImplementedError as erro:
            self.parar(0x40FD95, f'GetNumBob source {fonte} at cell {celula}: {erro}')
        self.chamadas.append(['AffBloc'])
        try:
            pixels = pixels_bloco_terreno(self.catalogo, self.ciclo.cache, plano['id_motor'])
        except NotImplementedError as erro:
            self.parar(0x45C72A, f'AffBloc engine ID {plano["id_motor"]}: {erro}')
        self.saida = compor_bloco_terreno(self.saida, self.largura, self.altura, pixels, x, y)

    def vegetacao_terreno(self, x, y, celula):
        self.chamadas.append(['AffVegetTerrain', x, y, celula])
        codigo = self.mundo.objetos[celula]
        if codigo in (0, OBJETO_PORTAO) or self.descoberta[celula] & 31: return
        try:
            plano = consultar_objeto_v6(codigo, auxiliar_u8=self.mundo.auxiliares[celula],
                descoberta_u8=self.descoberta[celula], iluminacao_u8=self.iluminacao[celula])
        except (NotImplementedError, ValueError) as erro:
            self.parar(0x410085, f'AffVegetTerrain code {codigo} at cell {celula}: {erro}')
        self.saida = compor_passe(self.catalogo, self.saida, self.largura, self.altura, plano, 'terreno', x, y,
            tabela_sombra=self.sombra, recorte=self.recorte())

    # AffSprite renderers
    def veget(self, x, y, celula):
        codigo = self.mundo.objetos[celula]
        if codigo not in CODIGOS_AFFVEGET: return
        if not 1 <= codigo <= 11: self.parar(0x415ACF, f'AffVeget handler for object code {codigo} at cell {celula}')
        try:
            plano = consultar_objeto(codigo, auxiliar_u8=self.mundo.auxiliares[celula],
                descoberta_u8=self.descoberta[celula], iluminacao_u8=self.iluminacao[celula])
        except (NotImplementedError, ValueError) as erro:
            self.parar(0x415ACF, f'AffVeget tree {codigo} at cell {celula}: {erro}')
        self.saida = compor_passe(self.catalogo, self.saida, self.largura, self.altura, plano, 'sprites', x, y,
            tabela_sombra=self.sombra, recorte=self.recorte())

    def _estrutura(self, indice, endereco):
        if self.mundo.estruturas is None:
            self.parar(endereco, 'the structure pool is not an inherited input (MundoQuadro.estruturas)')
        if indice >= 1000: self.parar(endereco, f'structure index {indice} is beyond the 1000-record pool')
        return self.mundo.estruturas[indice*276:(indice+1)*276]

    def _consulta_habitada(self, indice, endereco):
        if not callable(self.habitado): self.parar(endereco, 'BatimentEstHabiter provider (economy) is not supplied')
        return bool(self.habitado(indice))

    def batiments(self, x, y, celula):
        """AffBatiments 0x407DD3 for one cell: prefix, terrain switch, facade of the type-2 structure, selection tail."""
        palavra_regiao = self.mundo.palavra('regioes', celula)
        indice = (palavra_regiao & 0x7fe0) >> 5 if palavra_regiao & 0x8000 else 0xffff   # 0x407DEF..0x407E14
        if indice != 0xffff and self.mundo.estruturas is None:   # pinned pre-structure inputs keep their original stop
            self.parar(0x407DEF, f'AffBatiments structure occupancy at cell {celula}')
        if indice != 0xffff:
            r = self._estrutura(indice, 0x407E1E)
            # 0x407E1E..0x407E56: mode 3 skips the check; a foreign owner needs its per-camera visibility byte (+0x110+camera)
            if r[5] != 3 and r[4] != self.camera and r[0x110+self.camera] == 0: return
        if self.descoberta[celula] & 0x10: return  # CaseEstDecouverte false: 0x40F491
        esquerda, topo, direita, base = self.recorte()  # SaveCurrentClipping 0x40F4B7
        self.tela.gravar('recorte_salvo', struct.pack('<4H', esquerda, direita, topo, base))
        codigo = self.mundo.objetos[celula]
        if codigo in (OBJETO_MURO, OBJETO_PORTAO):
            self.parar(0x407EA7 if codigo == OBJETO_MURO else 0x407FB8, f'ChercheIndiceBatiment for object {codigo} at cell {celula}')
        palavra = self.mundo.palavra('terreno', celula)
        if palavra == GATILHO_SANTUARIO and self.mundo.estruturas is None:
            self.parar(0x40F23B, f'building facade for terrain word 0x{palavra:x} at cell {celula}')
        if palavra == GATILHO_SANTUARIO:
            self._fachada_santuario(x, y, celula, indice)
        elif palavra == 0x30d and self.mundo.estruturas is not None:
            cave_m3.facade(self,x,y,celula,indice)
        elif palavra in GATILHOS_FACHADA: self.parar(0x40F23B, f'building facade for terrain word 0x{palavra:x} at cell {celula}')
        if palavra == OFICINA: self.parar(0x40288B, f'workshop facade at cell {celula}')
        salvo = struct.unpack('<4H', self.tela.bruto('recorte_salvo'))  # RestaureClipping 0x40F4E8
        self.tela.gravar('recorte', struct.pack('<4H', salvo[2], salvo[3], salvo[0], salvo[1]))
        self._cauda_batiments(celula, indice)

    def _fachada_santuario(self, x, y, celula, indice):
        """Terrain word 0x2ED (0x408577..0x408ab3): inline lookup, state query, type-2 facade layers."""
        if indice == 0xffff: return   # 0x4085C5 -> 0x40F491: no structure at the trigger, nothing drawn
        r = self._estrutura(indice, 0x4085CB)
        modo = r[5]
        if r[8] != 2: self.parar(0x408606, f'structure type {r[8]}: only the type-2 facade is reconstructed')
        if modo not in (3,4,5):
            cave_m3.facade(self,x,y,celula,indice);return
        habitado = self._consulta_habitada(indice, 0x4087AA)
        if not habitado:
            cave_m3.facade(self,x,y,celula,indice,habitacao=False);return
        auxiliar = struct.unpack_from('<H', r, 6)[0]
        if auxiliar: self.parar(0x4085cb, 'sanctuary damage/fire (+0x06 nonzero): facade provider stops before drawing')
        if self.relogios_extra is None: self.parar(0x4087E3, 'frame clocks 0x508F80/0x508F84 are not supplied')
        relogios = [self.tela.u('quadro_u32'), *self.relogios_extra]
        plano = consultar_santuario(tipo=2, modo=5, habitado=True, jogador=r[4], relogios=relogios,
            celula_mapa=(celula & 0xff, celula >> 8), auxiliar_06=auxiliar)
        self.chamadas.append(['AffBatiments.fachada', indice, modo])
        self.saida = compor_fachada(self.catalogo, self.saida, self.largura, self.altura, plano, x, y,
            tabelas=self.tabelas_jogador, recorte=self.recorte())

    def _cauda_batiments(self, celula, indice):
        """0x40F342: AffVehiculeAtelier, RestaureClipping, selection frame and gauge for the selected structure."""
        if self.mundo.palavra('terreno', celula) == OFICINA: return
        if indice == 0xffff: return
        habitado = self._consulta_habitada(indice, 0x40F378)
        r = self._estrutura(indice, 0x40F399)
        if habitado and self.mundo.objetos[celula] != OBJETO_MURO and r[5] != 3:
            if self.selecao_estruturas is None: self.parar(0x40F3C2, 'per-owner structure selection words 0x495BE0 are not supplied')
            dono = self.selecao_estruturas[r[4]] if r[4] < len(self.selecao_estruturas) else None
            if dono is None: self.parar(0x40F3C2, f'owner {r[4]} is outside the supplied selection words')
            frame = dono == indice and r[4] == self.camera
            gauge = r[4] == self.camera and (self.tela.u('selecionada_estrutura_u16') == indice or dono == indice)
            if frame or gauge:
                if r[8] in (2,3) and self.mundo.palavra('terreno', celula) != {2:GATILHO_SANTUARIO,3:0x30d}[r[8]]: return
                entrada_m3.estrutura(self, r, celula, indice, frame=frame, gauge=gauge)
            return
        if r[8] == 0x11 and r[4] == self.camera and self.tela.u('selecionada_estrutura_u16') == indice:
            self.parar(0x4020EC, 'AffJaugeBatiment is not reconstructed')

    def engin(self, x, y, indice):
        r = self.mundo.unidades[indice*276:(indice+1)*276]; tipo, estado = r[1], r[2]
        if tipo in TIPOS and encaminhamento(tipo, estado, auxiliar_8a=r[0x8a])['rota'] == 'sem_desenho': return
        overlay = bool(r[0xba] or r[0xbd] or self.tela.u('selecionada_unidade_u16') == indice or self.tela.u('modo_selecao_u8'))
        i8 = lambda v: v-256 if v > 127 else v
        px, py = x+i8(r[0x86]), y+i8(r[0x87])
        if overlay:
            if self.leitura_entrada is None: self.parar(0x41591f, 'AffEngin input overlays require the live type-table read view')
            entrada_m3.validar_unidade(self, r)
            entrada_m3.quadro_selecao_unidade(self, r, px, py)
            if estado in (2,7):cave_m3.order_markers(self,r)
        if tipo == 7 and estado in (11,15):
            cave_m3.construction_builder(self,r,x,y,indice);return
        if estado not in (2,7):
            from camadas_exibicao_m3 import normal_extension,work
            if normal_extension(self,r,x,y,indice,overlay):return
            if work(self,r,x,y,indice,overlay):return
        if tipo in CORPOS_TIPOS1_8:   # render API 1.3: AffDeplaceEngin branches 0x412D4C / 0x412962 (native capture)
            try:
                self.saida, _ = compor_corpo_tipos1_8(self.catalogo, self.saida, self.largura, self.altura, r, x=x, y=y,
                    indice_u16=indice, camera_u8=self.camera, indice_selecionado_u16=self.tela.u('selecionada_unidade_u16'),
                    modo_selecao_u8=self.tela.u('modo_selecao_u8'), tabela_sombra=self.sombra, recorte=self.recorte(), sobreposicoes_compostas=overlay)
            except NotImplementedError as erro:
                self.parar(0x41591F, f'AffEngin unit {indice} type {tipo} state {estado}: {erro}')
            i8 = lambda v: v-256 if v > 127 else v
            self._cauda_unidade_m3(r, x, y, indice, overlay)
            return
        if tipo not in TIPOS: self.parar(0x41591F, f'AffEngin unit {indice} type {tipo} has no committed body')
        rota = encaminhamento(tipo, estado, auxiliar_8a=r[0x8a])
        if rota['rota'] == 'sem_desenho': return
        guarda = (rota['rota'] == 'corpo_base' and estado in (2,7) and r[0] == 0 and self.camera == 0
            and (overlay or (r[0xba] == 0 and r[0xbd] == 0
                and self.tela.u('selecionada_unidade_u16') != indice and self.tela.u('modo_selecao_u8') == 0))
            and 1 <= r[0x91] <= 16 and r[0xa4] <= 7)
        if not guarda: self.parar(0x41591F, f'AffEngin unit {indice} type {tipo} state {estado} route {rota["rota"]} outside the validated body domain')
        i8 = lambda v: v-256 if v > 127 else v
        self.saida, _ = compor_unidade(self.catalogo, self.saida, self.largura, self.altura, tipo=tipo, estado_u8=estado,
            direcao=r[0x91], fase=r[0xa4], x=x, y=y, tabela=self.sombra, bolsa_u16=struct.unpack_from('<H', r, 0xa)[0],
            auxiliar_8a=r[0x8a], dx=i8(r[0x86]), dy=i8(r[0x87]), recorte=self.recorte())
        self._cauda_unidade_m3(r, x, y, indice, overlay)

    def _cauda_unidade_m3(self, r, x, y, indice, overlay):
        i8 = lambda v: v-256 if v > 127 else v
        px, py = x+i8(r[0x86]), y+i8(r[0x87])-9
        if overlay and ((r[0] == self.camera and r[0xbd]) or self.tela.u('selecionada_unidade_u16') == indice or self.tela.u('modo_selecao_u8')):
            entrada_m3.info_unidade(self, r, px, py, indice)
        else:
            self._icone_fadiga(r, x, y, indice, i8(r[0x86]), i8(r[0x87]))
            if overlay: entrada_m3.experiencia(self, r, px, py)

    def _icone_fadiga(self, r, x, y, indice, dx, dy):
        """Tail 0x413568..0x413655 of the body routine: the low-life tired icon (life < 100, word +4 == word +0x76)."""
        vida, w4, w76 = struct.unpack_from('<H', r, 0x74)[0], struct.unpack_from('<H', r, 4)[0], struct.unpack_from('<H', r, 0x76)[0]
        if not (w4 == w76 and vida < 100): return
        if (vida//5) % 2: return
        if r[1] > 25 or not SE_FATIGUE[r[1]]: return
        if (dx or dy) and not (r[1]==9 and r[2] in (2,7,13)):
            self.parar(0x4135FA, 'tired icon with a nonzero body shift (+0x86/+0x87): origin not verified')
        self.chamadas.append(['EngineIconeFadiga', indice])
        q = self.catalogo.quadro(localizar(w4+ICONE_FADIGA)['id_motor'])   # drawn at the cell origin - (8, 11): native args of 0x41362E/0x413650
        if r[0] != 0xc8: q = Quadro(q.largura, q.altura, q.pixels.translate(self.tabelas_jogador[r[0]] if r[0] < 5 else self.parar(0x413650, f'owner {r[0]} has no player table')), q.opacidade, 0, b'')
        self.saida = compor_indices(self.saida, self.largura, self.altura, q, x+dx-8, y+dy-11, self.recorte())

    def projetil(self, indice):
        r = self.mundo.projeteis[indice*56:(indice+1)*56]; px, py = struct.unpack_from('<HH', r, 0xc)
        celula = ((py//32)*256+px//32) & 0xffff
        try:
            self.saida, _ = compor_projetil(self.catalogo, self.saida, self.largura, self.altura, r,
                origem=list(self.tela.palavras('origem')), iluminacao_u8=self.iluminacao[celula], tabela_sombra=self.sombra,
                tabela_eclairage=self.eclairage, recorte=self.recorte())
        except (NotImplementedError, ValueError) as erro:
            self.parar(0x46FF70, f'AffProjectile {indice}: {erro}')


def compor_quadro(mundo, tela, *, ciclo_cache, catalogo, tabela_sombra, tabela_eclairage, superficie, relogio, directdraw,
                  habitado=None, relogios_extra=None, selecao_estruturas=None, tabelas_jogador=None, leitura_entrada=None):
    """One AffGame call in mode 0x12, through the HUD checkpoint 0x417B1C.

    mundo: MundoQuadro (read-only). tela: EstadoTela, mutated with original
    writes and returned as ordered effects. ciclo_cache: the persistent
    CicloCacheTerreno after InitCache (GetNumBob mutates it). superficie: the
    locked surface's previous bytes (pitch x screen height). relogio():
    GetTickCount binding. directdraw: is_lost()/restore()/lock() -> (hresult,
    pointer) IDirectDrawSurface binding.
    """
    if not isinstance(mundo, MundoQuadro) or not isinstance(tela, EstadoTela):
        raise ValueError('Expected MundoQuadro and EstadoTela')
    if len(tabela_sombra) != 256 or len(tabela_eclairage) != 256: raise ValueError('Expected 256-byte shadow/lighting tables')
    if tela.u('modo_jogo_u8') != MODO_JOGO:
        raise DependenciaQuadro(0x4176A8, f'AffGame mode 0x{tela.u("modo_jogo_u8"):02x}: only the in-game mode 0x12 is composed')
    calcular_frame(tela, relogio)
    evento = tela.u('evento_u8') != 0  # EvenementEnCours 0x4581B6: consumed by the HUD tail only
    if tela.u('forcar_desenho_u8') == 0:
        divisor = tela.u('divisor_u8')
        if divisor == 0: raise DependenciaQuadro(0x417921, 'draw divisor 0 faults (DIV)', efeitos=tela.efeitos)
        if tela.u('quadro_u32') % divisor:
            return dict(desenhado=False, parada='retorno', superficie=bytes(superficie), chamadas=[['CalculFrame']],
                efeitos=list(tela.efeitos), evento=evento)
    if tela.u('limpar_u8') and tela.u('largura_tela_u16') == 800:
        raise DependenciaQuadro(0x41794B, 'video-surface clear path (DDLockSurfaceVideo) is not composed', efeitos=tela.efeitos)
    ponteiro = travar_superficie(tela, directdraw); tela.gravar('superficie_u32', ponteiro)
    if ponteiro == 0:
        raise DependenciaQuadro(0x4179D4, 'DDLockSurface returned NULL; drawing would fault', efeitos=tela.efeitos)
    if tela.u('restaurar_fundo_u8') and leitura_entrada is None:
        raise DependenciaQuadro(0x4179E1, 'saved-background restore (PasteBob) is not composed', efeitos=tela.efeitos)
    largura, altura = tela.u('pitch_u32'), tela.u('altura_tela_u16')
    if len(superficie) != largura*altura: raise ValueError('Surface must be pitch x screen height bytes')
    c = _Composicao(mundo, tela, superficie, catalogo, ciclo_cache, bytes(tabela_sombra), bytes(tabela_eclairage))
    c.leitura_entrada = leitura_entrada
    c.habitado, c.relogios_extra, c.selecao_estruturas = habitado, relogios_extra, selecao_estruturas
    c.tabelas_jogador = tabelas_jogador if tabelas_jogador is not None else _tabelas_jogador()
    c.chamadas += [['CalculFrame'], ['DDLockSurface']]
    if tela.u('restaurar_fundo_u8'):
        from hud_scriptado_m3 import restore_background
        restore_background(c)
    origem = list(tela.palavras('origem')); janela = list(tela.palavras('janela')); margem = tela.u('margem_i8')
    margem = margem-256 if margem > 127 else margem
    if tela.u('largura_tela_u16') != largura or janela[0]*32 != largura:
        c.parar(0x41068E, 'AffTerrain is reconstructed only with window width x 32 = pitch = screen-width word 0x49A018')
    c.chamadas.append(['AffTerrain']+origem)
    try:
        plano = planejar_passe_terreno(mundo.terreno, c.iluminacao, origem=origem, janela_celulas=janela, margem_i8=margem)
    except (NotImplementedError, ValueError) as erro:
        c.parar(0x41068E, f'AffTerrain viewport outside the reconstructed domain: {erro}')
    executar_passe_terreno(plano, bloco=c.bloco, vegetacao=c.vegetacao_terreno)
    c.chamadas.append(['AffSprite']+origem)
    try:
        plano = planejar_passe_sprites(mundo.unidades, mundo.projeteis, mundo.objetos, c.descoberta, c.iluminacao,
            origem=origem, janela_celulas=janela)
    except (NotImplementedError, ValueError) as erro:
        c.parar(0x416864, f'AffSprite viewport outside the reconstructed domain: {erro}')
    for evento_sprite in plano['eventos']:
        nome = evento_sprite['funcao']
        if nome == 'AffProjectile':
            c.chamadas.append([nome, evento_sprite['indice']]); c.projetil(evento_sprite['indice']); continue
        argumento = evento_sprite['indice'] if nome == 'AffEngin' else evento_sprite['celula']
        c.chamadas.append([nome, evento_sprite['x'], evento_sprite['y'], argumento])
        if nome == 'AffVeget': c.veget(evento_sprite['x'], evento_sprite['y'], argumento)
        elif nome == 'AffBatiments': c.batiments(evento_sprite['x'], evento_sprite['y'], argumento)
        elif nome == 'AffEngin': c.engin(evento_sprite['x'], evento_sprite['y'], argumento)
    if tela.u('caixa_selecao_u8'):
        entrada_m3.drag(c)
    return dict(desenhado=True, parada=CHECKPOINT_HUD, superficie=c.saida, chamadas=c.chamadas,
        efeitos=list(tela.efeitos), evento=evento)
