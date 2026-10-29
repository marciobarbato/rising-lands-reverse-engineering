"""Core construction routines over live original memory (M3 groundwork, Economy's build path).

Translated from the intact bytes (``evidencias/construcao-core/*.asm``) after the native capture
``evidencias/construcao-core/captura-construcao-core-exibicao.json`` was committed (``0a0ff90``).
Routines (entry, then the helpers each reaches):
- PlaceBatiment 0x41c4ac: BatimentModifyTerrain 0x41ba49 (SetTerrain, SetCollision, Chemin_ModifieZone
  mode 3 with MurAjoute/Remplit/AlloueCouleur/LibereCouleur), or for walls ChercheMurCombinaisons and for
  gates ValideHerse. It reaches neither BatimentModifyMap, BatimentAlloc nor any discovery;
- ResetCheminTerrainModify 0x41b78f: BatimentCollision, Chemin_ModifieZone mode 1 with MurRetire;
- BatimentCollision 0x41ab5c (Core's committed ``chamadas_quadro_core.colisao_estrutura``);
- BatimentConstructible 0x41fb12: TerrainEnCollision, EnginOccupeCase, EnginGetPlayer;
- BatimentPosable 0x41fc40: memset, TerrainEstHerbe, EnginGetPlayer, TerrainEstDecouvert,
  TerrainEnCollision, EnginOccupeCase, ValideHerse;
- EnginOccupeCase 0x44246e, TerrainEstHerbe 0x47636a, ValideHerse 0x41ac8b, ChercheMurCombinaisons 0x41c18a;
- DeplaceEngin 0x44930c: M2.3's live navigation world (``mundo_vivo`` with ``SolucionadorCaminhosVivo``)
  makes every store; this module adds the register exit.

Every routine takes EAX..EBP at its entry and returns EAX..EBP as the original leaves them, callee-saved
registers included. Arithmetic flags are not modeled. ``memoria``: ``u8/u16/u32(addr, value=None)`` and
``vista(addr, n)`` (``memoria_quadro_core.MemoriaQuadro``); only DeplaceEngin (M2.3's world) needs ``vista``.
Structure colours (MurAjoute/MurRetire/Remplit) run on Core's ``estruturas_caminhos.CoresEstruturas`` over the
original addresses.

Uncertain register bits. DeplaceEngin's EAX is sometimes the EAX a deep callee leaves (EnginNextCase's
frame dword, CheminCalcul, EnginDebloqueNextCase) and includes native stack residue. Those bits are never
guessed: the returned dict then carries ``_incertos = {'EAX': mask}``, and the masked bits are 0. Every
other register, and every bit of every other routine, is exact.

Named dependencies (never defaulted; without a provider the path raises ``DependenciaRamoCore`` at the
original call, after the stores the original made before it):
- Economy: ``bonus(jogador, tipo, seletor) -> EAX`` for BonusGetValEngin 0x428cc0, which CalculFatigue
  calls at the end of a DeplaceEngin step (AvanceEngin) of a unit of type 0..10 or 25; only its value is
  needed (the world's stores read the same live table 0x4dfba0).
- Audio: CalculNextCase's local-player sound for unit types 11..16 raises ``NotImplementedError`` in M2.3's
  world (``_som_movimento``), as before.
Protected inputs (``ValueError`` before any store): a structure index >= 1000, a structure type > 21.
"""
import struct

from chamadas_quadro_core import (DependenciaRamoCore, colisao_estrutura, definir_colisao, dono_da_unidade,
                                  terreno_esta_descoberto)
from colocacao_estruturas import PRIMEIROS_TILES
from estruturas_caminhos import CoresEstruturas
from incursao_core import memset_crt, terreno_em_colisao

M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
ESTRUTURAS, MAX_ESTRUTURAS = 0x49a0c8, 1000
TIPOS_ESTRUTURA = 0x495d8c           # stride 52: u16 width, u16 height, u32 terrain mask pointer at +8
TILES, OBJETOS, ATRIBUTOS, REGIOES, CORES = 0x507d70, 0x507d74, 0x507da8, 0x4e0f38, 0x4e156c
OBJETO_MURO, OBJETO_PORTAO = 0x495bf8, 0x495bf9
CORES_LIVRES = 0x4e1570
POSAVEL, MATRIZ_POSAVEL = 0x4e05b8, 0x4e05b9   # BatimentPosable's flag and per-cell matrix
BUSCA_OCUPADA, BUSCA_CONCLUIDA, BUSCA_SUCESSO, BUSCA_UNIDADE = 0x4e0f36, 0x496302, 0x4e0f37, 0x496304
STATUS_BUSCA = 0x4e0f4c
LIMITE_FADIGA = 0x4965dc
ROTINAS = {
    'PlaceBatiment': 0x41c4ac, 'ResetCheminTerrainModify': 0x41b78f, 'BatimentCollision': 0x41ab5c,
    'BatimentConstructible': 0x41fb12, 'BatimentPosable': 0x41fc40, 'EnginOccupeCase': 0x44246e,
    'TerrainEstHerbe': 0x47636a, 'ValideHerse': 0x41ac8b, 'ChercheMurCombinaisons': 0x41c18a,
    'DeplaceEngin': 0x44930c,
}
TIPOS_QUATRO_CELULAS = frozenset((3, 11, 12, 13, 14, 15, 16, 25))   # EnginOccupeCase 0x442522


def _baixo(v, b):
    return (v & 0xffffff00) | (b & 0xff)


class _Bytes:
    """``n`` live bytes at ``base`` through ``memoria.u8`` (any memory, sparse ones included)."""
    def __init__(self, memoria, base, largura=1):
        self._m, self._base, self._l = memoria, base, largura
        self._f = memoria.u8 if largura == 1 else memoria.u16

    def __getitem__(self, i):
        return self._f((self._base + self._l * i) & M32)

    def __setitem__(self, i, v):
        self._f((self._base + self._l * i) & M32, v)


class _CoresMemoria(CoresEstruturas):
    """Core's structure-colour state (``estruturas_caminhos.CoresEstruturas``: AlloueCouleur, LibereCouleur,
    MurAjoute, MurRetire, Remplit) at its original addresses: grid ``[0x4e156c]``, free list 0x4e1570,
    released flags 0x4e1670, u16 fill stack 0x4e0732, map size 0x497168. Each LibereCouleur is recorded
    as (count before, released) for the exit EAX of MurAjoute/MurRetire."""
    def __init__(self, memoria):
        self._memoria = memoria
        self.grade = _Bytes(memoria, memoria.u32(CORES))
        self.livres = _Bytes(memoria, CORES_LIVRES)
        self.liberadas = _Bytes(memoria, 0x4e1670)
        self.pilha = _Bytes(memoria, 0x4e0732, 2)
        self.liberacoes = []

    largura = property(lambda self: self._memoria.u16(0x497168))
    altura = property(lambda self: self._memoria.u16(0x49716a))

    def liberar(self, cor):
        antes = self.livres[0]
        super().liberar(cor)
        self.liberacoes.append((antes, self.livres[0] != antes))


class ConstrucaoCore:
    """The routines over one live memory. ``bonus``: Economy's BonusGetValEngin value provider."""

    def __init__(self, memoria, *, bonus=None):
        self.m = memoria
        self.bonus = bonus
        self._mundo = None
        self._cores = None

    # ------------------------------------------------------------ entry point
    def chamar(self, nome, regs, pilha=()):
        """Run routine ``nome`` with entry registers ``regs`` (EAX..EBP; missing keys are an error)."""
        metodo = {'PlaceBatiment': self.place_batiment, 'ResetCheminTerrainModify': self.reset_chemin_terrain_modify,
                  'BatimentCollision': self.batiment_collision, 'BatimentConstructible': self.batiment_constructible,
                  'BatimentPosable': self.batiment_posable, 'EnginOccupeCase': self.engin_occupe_case,
                  'TerrainEstHerbe': self.terrain_est_herbe, 'ValideHerse': self.valide_herse,
                  'ChercheMurCombinaisons': self.cherche_mur_combinaisons, 'DeplaceEngin': self.deplace_engin}[nome]
        r = {k: regs[k] & M32 for k in REG7}
        return metodo(r)

    # ------------------------------------------------------------ helpers
    def _cores_vivas(self):
        if self._cores is None:
            self._cores = _CoresMemoria(self.m)
        return self._cores

    def mundo(self):
        """M2.3's navigation world bound live to this memory, with the live path solver (built on first use)."""
        if self._mundo is None:
            from mundo_vivo import mundo_vivo
            from solucionador_vivo import SolucionadorCaminhosVivo
            self._mundo = mundo_vivo(self.m, SolucionadorCaminhosVivo(self.m))
        return self._mundo

    def _estrutura(self, eax):
        indice = eax & 0xffff
        if indice >= MAX_ESTRUTURAS:
            raise ValueError(f'Structure index {indice} outside 0..999')
        return indice, ESTRUTURAS + indice * PASSO

    def _tamanho(self, tipo):
        return self.m.u16(TIPOS_ESTRUTURA + 52 * tipo), self.m.u16(TIPOS_ESTRUTURA + 52 * tipo + 2)

    def _set_terrain(self, celula, tile):
        """SetTerrain 0x476251: tiles[AX] = DX; EAX = AX."""
        self.m.u16((self.m.u32(TILES) + 2 * (celula & 0xffff)) & M32, tile)

    def _chemin_modifie_zone(self, modo, celula, indice, ecx, sub):
        """Chemin_ModifieZone 0x43e138 modes 3 (insert a structure tag, MurAjoute) and 1 (remove, MurRetire).

        Returns (EAX, EBX, EDX); ESI/EDI/ECX are preserved and the routine pops the pushed ``sub`` (RET 4).
        """
        m = self.m
        celula &= 0xffff
        eax = (indice & 0xffff00ff)
        eax = (eax & 0xffffff00) | (sub & 0xff)
        eax = (eax + (indice << 5)) & M32
        eax = (eax & 0xffff00ff) | ((((eax >> 8) & 0xff) + 0x80) & 0xff) << 8
        marca = eax & 0xffff
        regioes = m.u32(REGIOES)
        endereco = (regioes + 2 * celula) & M32
        antigo = m.u16(endereco)
        if modo == 3:
            if antigo >= 0x4000:
                return endereco & 0xffffff00, 2 * celula, celula
            m.u16(ecx, antigo)
            m.u16((m.u32(REGIOES) + 2 * celula) & M32, marca)
            cores = self._cores_vivas()
            cores.liberacoes = []
            cores.adicionar_muro(celula)
            c3 = cores.liberacoes[3][0]               # the count read before the fourth LibereCouleur
            eax = c3 | (((c3 + 1) & 0xff) << 8 if cores.liberacoes[3][1] else 0)
            return _baixo(eax, 1), 2 * celula, celula
        if modo == 1:
            if antigo != marca:
                return endereco & 0xffffff00, regioes, celula
            salvo = m.u16(ecx)
            m.u16(endereco, salvo)
            cores = self._cores_vivas()
            cores.liberacoes = []
            vazia = not cores.grade[celula]
            cores.retirar_muro(celula)
            eax = 0 if vazia else cores.liberacoes[3][0]
            return _baixo(eax, 1), (regioes & 0xffff0000) | salvo, celula
        raise DependenciaRamoCore('Chemin_ModifieZone', 0x43e138, f'mode {modo} is not part of this slice')

    def _batiment_modify_terrain(self, origem, tile, indice):
        """BatimentModifyTerrain 0x41ba49 (AX origin, DX first tile, BX index): returns the exit EAX."""
        m = self.m
        rec = ESTRUTURAS + (indice & 0xffff) * PASSO
        tipo = m.u8(rec + 8)
        largura, altura = self._tamanho(tipo)
        mascara = m.u32(TIPOS_ESTRUTURA + 52 * tipo + 8)
        eax = origem
        edi = origem
        sub = 0
        for linha in range(altura):
            for coluna in range(largura):
                celula = edi & 0xffff
                self._set_terrain(celula, tile)
                eax = celula
                tile = (tile + 1) & 0xffff
                if m.u8((mascara + linha * largura + coluna) & M32):
                    definir_colisao(m, celula, 1)
                    eax, _, _ = self._chemin_modifie_zone(3, celula, indice & 0xffff, rec + 0xcc + 2 * sub, sub)
                    sub = (sub + 1) & 0xff
                m.u8((m.u32(OBJETOS) + celula) & M32, 0)
                edi += 1
            edi += 0x100 - largura
        return eax

    # ------------------------------------------------------------ PlaceBatiment
    def place_batiment(self, r):
        """PlaceBatiment 0x41c4ac (AX index): terrain, collision, region tags and colours of a prepared record."""
        m = self.m
        indice, rec = self._estrutura(r['EAX'])
        tipo = m.u8(rec + 8)
        if tipo > 0x15:
            raise ValueError(f'Structure type {tipo} outside 0..21')
        origem = m.u16(rec + 2)
        saida = dict(r)
        if tipo not in (9, 12):
            saida['EAX'] = self._batiment_modify_terrain(origem, PRIMEIROS_TILES[tipo], indice)
            return saida
        if tipo == 9:
            combinacao = self.cherche_mur_combinaisons(dict(r, EAX=origem))['EAX'] & 0xff
            m.u16(rec + 0x7c, combinacao)
            m.u8((m.u32(OBJETOS) + origem) & M32, m.u8(OBJETO_MURO))
            definir_colisao(m, origem, 1)
        else:
            orientacao = self.valide_herse(dict(r, EAX=origem))['EAX'] & 0xff
            if orientacao == 0xff:
                saida['EAX'] = 0xff
                return saida
            m.u16(rec + 0x7c, orientacao)
            m.u8((m.u32(OBJETOS) + origem) & M32, m.u8(OBJETO_PORTAO))
            m.u16(rec + 0x86, 0)
            definir_colisao(m, origem, 1)
        saida['EAX'] = self._chemin_modifie_zone(3, origem, indice, rec + 0xcc, 0)[0]
        return saida

    # ------------------------------------------------------------ ResetCheminTerrainModify
    def reset_chemin_terrain_modify(self, r):
        """ResetCheminTerrainModify 0x41b78f (AX index): removes the record's region tags (mode 1) by its
        static collision mask and origin; EAX = the height row count, all others preserved."""
        m = self.m
        indice, rec = self._estrutura(r['EAX'])
        tipo = m.u8(rec + 8)
        if tipo > 0x15:
            raise ValueError(f'Structure type {tipo} outside 0..21')
        largura, altura = self._tamanho(tipo)
        edi = (r['EDI'] & 0xffff0000) | m.u16(rec + 2)
        sub = 0
        for linha in range(altura):
            for k in range(largura):
                if colisao_estrutura(m, tipo, linha * largura + k)['EAX'] & 0xff:
                    self._chemin_modifie_zone(1, edi & 0xffff, indice, rec + 0xcc + 2 * sub, sub)
                    sub = (sub + 1) & 0xff
                edi = (edi + 1) & M32
            edi = (edi + 0x100 - largura) & M32
        return dict(r, EAX=altura)

    # ------------------------------------------------------------ BatimentCollision
    def batiment_collision(self, r):
        """BatimentCollision 0x41ab5c (AL type, DX mask index): Core's committed translation."""
        return dict(r, **colisao_estrutura(self.m, r['EAX'], r['EDX']))

    # ------------------------------------------------------------ queries
    def terrain_est_herbe(self, r):
        """TerrainEstHerbe 0x47636a (AX cell): AL = tile in 0x15d..0x1a4; only EAX changes."""
        eax = r['EAX']
        tile = self.m.u16((self.m.u32(TILES) + 2 * (eax & 0xffff)) & M32)
        if 0x15d <= tile < 0x19d:
            return dict(r, EAX=_baixo(eax, 1))
        return dict(r, EAX=_baixo(tile, int(0x19d <= tile < 0x1a5)))

    def _objeto(self, endereco_linear):
        return self.m.u8((self.m.u32(OBJETOS) + endereco_linear) & M32)

    def _muro_ou_portao(self, v):
        return v == self.m.u8(OBJETO_MURO) or v == self.m.u8(OBJETO_PORTAO)      # the gate byte only on a miss

    def valide_herse(self, r):
        """ValideHerse 0x41ac8b (AX cell): AL 0 horizontal, 1 vertical, 0xff no fitting walls; only EAX changes."""
        celula = r['EAX'] & 0xffff
        x, y = celula & 0xff, celula >> 8
        if x > 0 and self._muro_ou_portao(self._objeto(celula - 1)) and self._muro_ou_portao(self._objeto(celula + 1)):
            return dict(r, EAX=_baixo(y, 0))
        if y > 0 and self._muro_ou_portao(self._objeto(celula - 0x100)):
            abaixo = self._objeto(celula + 0x100)
            eax = (celula & 0xff00) | abaixo
            return dict(r, EAX=_baixo(eax, 1 if self._muro_ou_portao(abaixo) else 0xff))
        return dict(r, EAX=_baixo(y, 0xff))

    def cherche_mur_combinaisons(self, r):
        """ChercheMurCombinaisons 0x41c18a (AX cell): wall bits W=8, S=4, E=2, N=1 minus one; 0 on a gate.
        AH = the gate object byte, EAX's upper half kept; only EAX changes."""
        celula = r['EAX'] & 0xffff
        bits = 0
        for delta, bit in ((-1, 8), (0x100, 4), (1, 2), (-0x100, 1)):
            if self._muro_ou_portao(self._objeto(celula + delta)):
                bits |= bit
        portao = self.m.u8(OBJETO_PORTAO)
        if self._objeto(celula) == portao:
            bits = 0
        elif bits:
            bits -= 1
        return dict(r, EAX=(r['EAX'] & 0xffff0000) | portao << 8 | bits)

    def engin_occupe_case(self, r):
        """EnginOccupeCase 0x44246e (AX unit, DX cell, BL mask): AL = the unit holds the cell (+8 or the
        reserved +0x7c; four cells for the large types). EAX, EBX and EDX change."""
        m = self.m
        eax, ebx, edx = r['EAX'], r['EBX'], r['EDX']
        bh = ebx & 0xff
        rec = (m.u32(PONTEIRO_UNIDADES) + (eax & 0xffff) * PASSO) & M32
        ebx = (ebx & 0xffff0000) | bh << 8 | 1
        sair = lambda eax_, ebx_, edx_: dict(r, EAX=eax_ & M32, EBX=ebx_ & M32, EDX=edx_ & M32)
        cx, ab, si = m.u16(rec + 8), m.u8(rec + 0xab), m.u16(rec + 0x7c)
        if (ab and bh == 1) or (not ab and bh == 2) or m.u8(rec + 2) == 0xe:
            return sair(rec & 0xffffff00, ebx, edx)
        tipo = m.u8(rec + 1)
        eax = _baixo(rec, tipo)
        if tipo > 0x19:
            return sair(_baixo(eax, 1), ebx, edx)
        dx = edx & 0xffff
        if tipo not in TIPOS_QUATRO_CELULAS:
            bl = int(cx == dx or si == dx)
            return sair(_baixo(eax, bl), _baixo(ebx, bl), edx)
        if cx == dx:
            return sair(_baixo(eax, 1), ebx, edx)
        ebx, eax = cx, dx
        if (ebx - 1) & M32 == eax or (ebx - 0x101) & M32 == eax:
            return sair(_baixo(eax, 1), _baixo(ebx, 1), edx)
        ebx = (ebx - 0x100) & M32
        if ebx == eax or si == dx:
            return sair(_baixo(eax, 1), _baixo(ebx, 1), edx)
        edx = si
        for ebx in ((edx - 1) & M32, (edx - 0x101) & M32):
            if ebx == eax:
                return sair(_baixo(eax, 1), _baixo(ebx, 1), edx)
        edx = (edx - 0x100) & M32
        bl = int(edx == eax)
        return sair(_baixo(eax, bl), _baixo(ebx, bl), edx)

    # ------------------------------------------------------------ BatimentConstructible
    def batiment_constructible(self, r):
        """BatimentConstructible 0x41fb12 (AL type, DX reference = bottom-right cell, BX unit): AL = no cell
        of the w x h rectangle has collision bit 0 unless unit BX holds it (EnginOccupeCase, mask 1). Type 12
        instead needs a wall object at DX whose structure tag belongs to the unit's owner. EAX, EBX and EDX
        change; ECX, ESI, EDI and EBP are restored."""
        m = self.m
        unidade = r['EBX'] & 0xffff
        edx = r['EDX']
        tipo = r['EAX'] & 0xff
        largura, altura = self._tamanho(tipo)
        esi = (edx - (largura - 1) - ((altura - 1) << 8)) & M32
        sair = lambda eax_, ebx_, edx_: dict(r, EAX=eax_ & M32, EBX=ebx_ & M32, EDX=edx_ & M32)
        if tipo == 12:
            eax = edx & 0xffff
            ebx = m.u32(OBJETOS)
            objeto = m.u8((ebx + eax) & M32)
            edx = _baixo(edx, objeto)
            if objeto != m.u8(OBJETO_MURO):
                return sair(eax & 0xffffff00, ebx, edx)
            ebx = 2 * eax
            endereco = (m.u32(REGIOES) + ebx) & M32
            eax = (m.u16(endereco) & 0x7fe0) >> 5 if m.u8(endereco + 1) & 0x80 else 0xffff   # TEST high byte first
            if eax == 0xffff:
                return sair(eax & 0xffffff00, ebx, edx)
            ebx = eax * PASSO
            eax = dono_da_unidade(m, unidade)['EAX']
            return sair(_baixo(eax, int(eax & 0xff == m.u8((ebx + ESTRUTURAS + 4) & M32))), ebx, edx)
        ebx, edx = tipo, 0
        linha = 0
        while True:
            if (linha & 0xffff) >= altura:
                return sair(_baixo(linha, 1), ebx, edx)
            for _ in range(largura):
                celula = esi & 0xffff
                edx = 1
                if terreno_em_colisao(m, celula, 1)['EAX'] & 0xff:
                    o = self.engin_occupe_case(dict(r, EAX=unidade, EBX=1, EDX=celula))
                    ebx, edx = o['EBX'], o['EDX']
                    if not o['EAX'] & 0xff:
                        return sair(o['EAX'], ebx, edx)
                esi = (esi + 1) & M32
            esi = (esi + 0x100 - largura) & M32
            linha += 1

    # ------------------------------------------------------------ BatimentPosable
    def batiment_posable(self, r):
        """BatimentPosable 0x41fc40 (AL type, DX centre cell, BX unit): the cursor test. Fills the flag
        0x4e05b8 and the w x h matrix 0x4e05b9 (1 = valid cell), returns AL = the flag. EAX, EBX and EDX change."""
        m = self.m
        unidade = r['EBX'] & 0xffff
        tipo = r['EAX'] & 0xff
        largura, altura = self._tamanho(tipo)
        celula = r['EDX'] & 0xffff
        x, y = celula % 0x100, celula // 0x100
        m.u8(POSAVEL, 1)
        memset_crt(m, MATRIZ_POSAVEL, 1, largura * altura)
        meia_l, meia_a = largura >> 1, altura >> 1
        esi = (celula - meia_l - (meia_a << 8)) & M32
        if meia_l > x or y < meia_a or largura + x - meia_l - 1 > 0x100 or altura + y - meia_a - 1 > 0x100:
            memset_crt(m, MATRIZ_POSAVEL, 0, largura * altura)
            m.u8(POSAVEL, 0)
            return dict(r, EAX=_baixo(MATRIZ_POSAVEL, 0), EBX=largura * altura, EDX=0)

        def invalida(linha, coluna):
            m.u8(MATRIZ_POSAVEL + linha * largura + coluna, 0)
            m.u8(POSAVEL, 0)
        if tipo == 12:                                # 0x41fe27: a gate needs a wall cell that fits
            eax, edx = meia_a, (y - meia_a) & M32
            for linha in range(altura):
                for coluna in range(largura):
                    alvo = esi & 0xffff
                    objeto = self._objeto(alvo)
                    eax = (self.valide_herse(dict(r, EAX=alvo))['EAX'] & 0xffff00ff) | objeto << 8
                    if objeto == m.u8(OBJETO_MURO) and eax & 0xff != 0xff:
                        edx = eax & 0xff
                    else:
                        edx = largura * linha
                        eax &= 0xffffff00
                        invalida(linha, coluna)
                    esi = (esi + 1) & M32
                eax = (0x100 - largura) & M32
                esi = (esi + eax) & M32
            return dict(r, EAX=_baixo(eax, m.u8(POSAVEL)), EBX=altura, EDX=edx)
        ebx = (largura + x - meia_l - 1) & M32         # 0x41fd16, kept when there is no row
        edx = 0
        for linha in range(altura):
            for coluna in range(largura):
                alvo = esi & 0xffff
                valida = False
                if self.terrain_est_herbe(dict(r, EAX=alvo))['EAX'] & 0xff:
                    jogador = dono_da_unidade(m, unidade)['EAX'] & 0xff
                    d = terreno_esta_descoberto(m, alvo, jogador)
                    edx = d['EDX']
                    if d['EAX'] & 0xff:
                        edx = 1
                        if not terreno_em_colisao(m, alvo, 1)['EAX'] & 0xff:
                            valida = True
                        else:
                            o = self.engin_occupe_case(dict(r, EAX=unidade, EBX=1, EDX=alvo))
                            ebx, edx = o['EBX'], o['EDX']
                            valida = bool(o['EAX'] & 0xff)
                if not valida:
                    edx = linha * largura
                    invalida(linha, coluna)
                esi = (esi + 1) & M32
            ebx = linha + 1
            esi = (esi + 0x100 - largura) & M32
        return dict(r, EAX=_baixo(altura, m.u8(POSAVEL)), EBX=ebx, EDX=edx)

    # ------------------------------------------------------------ DeplaceEngin
    def deplace_engin(self, r):
        """DeplaceEngin 0x44930c (AX unit): the path-state switch on +0x88. M2.3's live world makes the stores;
        EBX..EBP are preserved. EAX is exact except the bits marked in ``_incertos`` (see the module docstring)."""
        m = self.m
        unidade = r['EAX'] & 0xffff
        rec = (m.u32(PONTEIRO_UNIDADES) + unidade * PASSO) & M32
        estado = m.u8(rec + 0x88)
        saida = dict(r)
        deslocado = m.u8(rec + 0x86) or m.u8(rec + 0x87)
        if estado > 6 or estado == 2:
            saida['EAX'] = unidade
            return saida
        w = self.mundo()
        if estado == 1:
            w.deslocar(unidade)
            saida['EAX'] = unidade
            return saida
        if estado == 6:
            w.deslocar(unidade)
            saida['EAX'] = 0x14 if m.u8(rec + 0x88) == 3 else m.u8(rec + 0x8b)
            return saida
        if estado in (0, 5) or (estado == 3 and deslocado):
            eax, incerto = self._calcul_next_case(unidade, rec)
        elif estado == 3:
            if m.u8(BUSCA_OCUPADA):
                saida['EAX'] = unidade
                return saida
            w.deslocar(unidade)
            eax, incerto = 0, M32                     # CheminCalcul's EAX
        else:
            eax, incerto = self._estado_busca(unidade, rec)
        saida['EAX'] = eax & ~incerto & M32
        if incerto:
            saida['_incertos'] = {'EAX': incerto}
        return saida

    def _estado_busca(self, unidade, rec):
        """DeplaceEngin's state 4 (0x4493d8): exit EAX from the branch the original takes."""
        m = self.m
        w = self.mundo()
        if not m.u8(BUSCA_CONCLUIDA):
            w.deslocar(unidade)
            return 0, M32                             # CheminCalcul's EAX
        sucesso, status = m.u8(BUSCA_SUCESSO), m.u8(STATUS_BUSCA)
        estado_unidade = m.u8(rec + 2)
        dono_busca = m.u16(BUSCA_UNIDADE) == unidade
        w.deslocar(unidade)
        if sucesso:
            if estado_unidade == 2 and status == 2:
                return rec, 0                         # 0x449414; a release there defeats the check at 0x4494bf
            return (0 if dono_busca else estado_unidade), 0
        if status == 8:
            return (0 if dono_busca else unidade), 0
        return 0, M32                                 # EnginDebloqueNextCase's branch (its EAX, the record or 0)

    def _calcul_next_case(self, unidade, rec):
        """CalculNextCase 0x448f50 through M2.3's world, with its exit EAX: (EAX, uncertain mask)."""
        m = self.m
        w = self.mundo()
        u8 = lambda o: m.u8(rec + o)
        chamada = None
        if not u8(0x86) and not u8(0x87):
            if u8(0x88) == 0:
                w.escolher_direto(unidade)
                chamada = 'EnginNextCase'
            elif u8(0x88) == 5:
                w.escolher_da_rota(unidade)
                chamada = 'EnginNextCaseChemin'
        reservada = m.u16(rec + 0x7c)
        if reservada == m.u16(rec + 8):
            # EAX = the callee's upper half with AX = +0x7c. EnginNextCase leaves its frame dword (stack
            # residue) or the record, except after three blocked tries (+0x88 = 3, EAX = 3).
            if chamada is None or (chamada == 'EnginNextCase' and u8(0x88) == 3):
                return reservada, 0
            return reservada, 0xffff0000
        from movimento import pode_avancar
        w.animar_movimento(unidade)
        if u8(0x91) != u8(0x90):
            w.girar(unidade)
        w._som_movimento(unidade)
        if not pode_avancar(u8(0x90), u8(0x91)):
            return 0, 0
        antes = dict(tipo=u8(1), dono=u8(0), visivel=u8(0x72), contador=m.u16(rec + 0x74),
                     provisoes=m.u16(rec + 4), f8=u8(0xf8))
        w.avancar_passo(unidade)
        return self._saida_avance(unidade, rec, antes), 0

    def _saida_avance(self, unidade, rec, antes):
        """AvanceEngin's exit EAX (0x448ac6..0x448b37): CalculFatigue's for types 0..10 and 25."""
        m = self.m
        estado = m.u8(rec + 2)
        if estado in (0, 4):
            return 0
        tipo = antes['tipo']
        if tipo > 0x19:
            return _baixo(m.u32(PONTEIRO_UNIDADES), tipo)
        if 11 <= tipo <= 24:
            return tipo
        if not antes['visivel']:
            return unidade * PASSO & 0xffffff00
        if self.bonus is None:
            raise DependenciaRamoCore('CalculFatigue', 0x452d48, 'BonusGetValEngin provider (economy) not supplied')
        valor = self.bonus(antes['dono'], tipo, 0) & M32
        limite = (m.u16(LIMITE_FADIGA + 50 * tipo) + antes['f8'] + valor) & 0xffff
        if limite > (antes['contador'] + 1) & 0xffff:
            return valor
        return antes['provisoes']


ROTINAS_ECONOMIA = ('PlaceBatiment', 'BatimentConstructible', 'BatimentCollision', 'ResetCheminTerrainModify',
                    'DeplaceEngin')


def provedor_construcao(core, outros=None):
    """Economy's ``externo(nome, chamada, registradores) -> registradores`` for the five Core routines its
    build path calls (``ROTINAS_ECONOMIA``), run by ``core`` (a ``ConstrucaoCore`` over the same memory).

    Input: EAX..EBP (and ESP, unused) at the callee entry, optionally ``_incertos``. Output: EAX..EBP as the
    callee leaves them, after its stores. ``_incertos`` in the output marks the bits not reconstructed
    (DeplaceEngin's EAX through deep callees; those bits are 0); input masks are carried for the registers
    the callee leaves unchanged. Any other name goes to ``outros`` (same signature) or raises
    ``DependenciaRamoCore`` at its call. Wiring with Core's selection-orders provider:
    ``provedor_core(SelecaoOrdens(m, som=...), provedor_construcao(ConstrucaoCore(m, bonus=...)))``.
    """
    def externo(nome, chamada, regs):
        if nome not in ROTINAS_ECONOMIA:
            if outros is None:
                raise DependenciaRamoCore(nome, chamada, 'no provider for this routine')
            return outros(nome, chamada, regs)
        entrada = {k: regs[k] & M32 for k in REG7}
        saida = core.chamar(nome, entrada)
        resultado = {k: saida[k] & M32 for k in REG7}
        incertos = {k: v for k, v in (regs.get('_incertos') or {}).items() if resultado.get(k) == entrada.get(k)}
        for k, v in (saida.get('_incertos') or {}).items():
            incertos[k] = incertos.get(k, 0) | v
        if incertos:
            resultado['_incertos'] = incertos
        return resultado
    return externo
