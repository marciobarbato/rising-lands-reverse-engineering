"""MissionPlaceTerrain structure habitation: BatimentEstHabiter and BatimentHabitable.

Economy owns the technology Bags, the type-3 level and the footprint-centre
query. Core owns DecouvreTerrain/IllumineTerrain; they are called directly on
the shared physical world under core's published radius gates.
"""
from dataclasses import dataclass
import importlib
from pathlib import Path
import struct
import sys

from limpeza_saida import bag_contient_troupe
from proprietarios import PASSO_BAG, PASSO_PENDENCIAS_JOGADOR, inicializar_bag

PASSO_ESTRUTURA = 276
# Jump table 0x41cc18 (types 0..21). Types 9/12 point at the shared exit
# without a store, but both return before the switch, like type 17.
RAIOS = (20, 8, 10, 8, 5, 8, 8, 8, 8, None, 7, 7, None, 8, 8, 8, 8, 4, 8, 4, 8, 4)
TIPOS_SEM_VISAO = (17, 9, 12)
# BatimentSetTechnologie 0x41c76c: type -> (BagInit capacity, unit types
# appended with tag 6 when TypeEnginEstRealisable). Types 6/15/20 add more.
TECNOLOGIA = {1: (4, (0, 1, 2, 8)), 2: (4, (5, 6, 7)), 3: (3, ()), 5: (5, (11, 12, 13, 14, 15)),
              13: (2, (3, 25)), 15: (2, (4,)), 16: (1, (10,)), 18: (1, (16,)), 20: (2, (4,))}


class DependenciaHabitacao(NotImplementedError):
    """Original call reached outside core's published domain; earlier effects stay."""
    def __init__(self, indice, endereco, chamada, argumentos, motivo):
        self.indice, self.endereco, self.chamada = indice, endereco, chamada
        self.argumentos, self.motivo = argumentos, motivo
        super().__init__(f'BatimentHabitable({indice}) needs 0x{endereco:08x} from 0x{chamada:08x} '
                         f'with {argumentos}: {motivo}')


@dataclass(frozen=True)
class HabitacaoAplicada:
    indice: int
    tipo: int
    dono: int
    celula: object  # BatimentGetCase result; None for types 17/9/12
    raio: object    # jump-table radius; None for types 17/9/12


def _core(nome):
    """Import a committed core module from this checkout only."""
    pasta = Path(__file__).resolve().parents[2]/'ferramentas'
    atual = sys.modules.get(nome)
    if atual is not None and Path(atual.__file__).resolve() != pasta/f'{nome}.py':
        raise ImportError(f'Structure habitation requires committed core {nome} from this checkout')
    sys.path.insert(0, str(pasta))
    try:
        return importlib.import_module(nome)
    finally:
        sys.path.remove(str(pasta))


def limites_visao():
    """Core's direct-call DX maxima; 10/8 is the committed domain before they exist."""
    visao = _core('visao_movimento')
    return (getattr(visao, 'RAIO_DESCOBERTA_MAXIMO_VALIDADO', 10),
            getattr(visao, 'RAIO_LUZ_MAXIMO_VALIDADO', 8))


def bag_prend(memoria, offset, etiqueta, valor):
    """BagPrend 0x447483: +66 then tag/value at slot word +0, then +0 increments.

    The original never checks capacity; slots beyond 30 overlap the header
    and are outside the protected domain.
    """
    slot = struct.unpack_from('<H', memoria, offset)[0]
    if slot >= 30:
        raise ValueError('BagPrend protected slot is 0..29')
    total = struct.unpack_from('<H', memoria, offset+0x66)[0]
    struct.pack_into('<H', memoria, offset+0x66, (total+1) & 65535)
    memoria[offset+0x42+slot] = etiqueta & 255
    struct.pack_into('<H', memoria, offset+6+2*slot, valor & 65535)
    struct.pack_into('<H', memoria, offset, slot+1)


def celula_central_estrutura(estruturas, indice):
    """BatimentGetCase 0x41aee2: AX index; EDX/EBX are neither read nor changed.

    Centre of the collision-mask bounding box: origin word +2 plus
    (minrow + (maxrow-minrow)/2)*256 + mincol + (maxcol-mincol)/2, as u16.
    Protected domain: index 0..999 and type byte +8 0..21 (core's masks).
    """
    indice &= 65535
    if indice >= 1000 or len(estruturas) != 1000*PASSO_ESTRUTURA:
        raise ValueError('BatimentGetCase protected index is 0..999 in a 1,000-record pool')
    o = indice*PASSO_ESTRUTURA
    origem, tipo = struct.unpack_from('<H', estruturas, o+2)[0], estruturas[o+8]
    if tipo >= 22:
        raise ValueError('BatimentGetCase protected structure type is 0..21')
    pegadas = _core('pegadas_estruturas')
    largura, altura = pegadas.tamanho_estrutura(tipo)
    celulas = [(linha, coluna) for linha in range(altura) for coluna in range(largura)
               if pegadas.colisao_estrutura(tipo, linha*largura+coluna)]
    linhas, colunas = [c[0] for c in celulas], [c[1] for c in celulas]
    linha = min(linhas) + (max(linhas)-min(linhas))//2
    coluna = min(colunas) + (max(colunas)-min(colunas))//2
    return (origem + linha*256 + coluna) & 65535


def estrutura_habitada(producao, indice):
    """BatimentEstHabiter 0x41a5b8: AX index, AL 1/0.

    Type 21 uses only BagContientTroupe 0x44724a; type 2 tries it and then
    BagContient(tag 1, unit type 9); other types use only BagContient.
    """
    r = producao.recrutamento
    tipo = r.mundo.estruturas[r._offset(indice)+8]
    if tipo in (2, 21) and bag_contient_troupe(r, indice):
        return 1
    if tipo == 21:
        return 0
    return int(producao.contar_unidades(indice, 9) != 0)


class HabitacaoConstrucoes:
    """Shared-state provider for 0x41a5b8 and 0x41cc70.

    Buffers are used by identity: technology Bags 0x4dd6e8 and spells via
    aprendizagem.propriedade/inventados, unit realizability 0x4e1934 (104
    bytes) and structure realizability 0x4dfad4 (88 bytes), never copied.
    """
    def __init__(self, aprendizagem, *, unidades_realizaveis, estruturas_realizaveis):
        self.aprendizagem = aprendizagem
        self.producao = aprendizagem.producao
        self.construcoes = self.producao.recrutamento.mundo
        self.propriedade = aprendizagem.propriedade
        self.unidades_realizaveis = unidades_realizaveis
        self.estruturas_realizaveis = estruturas_realizaveis
        for bloco, tamanho in ((self.propriedade.pendencias, 9152), (self.propriedade.sortilegios, 20),
                               (aprendizagem.inventados, 20), (unidades_realizaveis, 104),
                               (estruturas_realizaveis, 88), (self.construcoes.capacidades.memoria, 24),
                               (self.construcoes.estruturas, 276000), (self.producao.recrutamento.unidades, 220800)):
            if len(bloco) != tamanho:
                raise ValueError(f'Structure habitation buffer must have {tamanho} bytes')
        if self.propriedade.mundo is not self.construcoes:
            raise ValueError('Technology Bags and structures must share one economy world')

    def estrutura_habitada(self, indice):
        return estrutura_habitada(self.producao, indice)

    def unidade_realizavel(self, jogador, tipo):
        """TypeEnginEstRealisable 0x44228e: byte 0x4e1934 + 26*AL + DL."""
        jogador, tipo = jogador & 255, tipo & 255
        if jogador >= 4 or tipo >= 26:
            raise ValueError('TypeEnginEstRealisable protected owner/type is 0..3/0..25')
        return self.unidades_realizaveis[jogador*26+tipo]

    def definir_tecnologia(self, jogador, tipo):
        """Complete BatimentSetTechnologie 0x41c76c: AL owner, DL type.

        AL >= 4 and types without a branch return unchanged. Each branch
        resets that owner/type Bag (BagInit) and appends in original order.
        Type 15 calls ReseauActif 0x42c3b0 and discards it before reading
        0x4dfad4+22*owner+20. Type 20 always appends tag 4 value 5.
        """
        jogador, tipo = jogador & 255, tipo & 255
        if jogador >= 4:
            return
        if tipo == 6:
            return self.aprendizagem.atualizar_pesquisas_biblioteca(jogador)
        if tipo not in TECNOLOGIA:
            return
        capacidade, unidades = TECNOLOGIA[tipo]
        memoria = self.propriedade.pendencias
        bag = jogador*PASSO_PENDENCIAS_JOGADOR + tipo*PASSO_BAG
        inicializar_bag(memoria, bag, capacidade)
        for unidade in unidades:
            if self.unidade_realizavel(jogador, unidade):
                bag_prend(memoria, bag, 6, unidade)
        if tipo == 15 and self.estruturas_realizaveis[jogador*22+20]:
            bag_prend(memoria, bag, 3, 20)
        elif tipo == 20:
            bag_prend(memoria, bag, 4, 5)

    def tornar_habitavel(self, mundo, indice):
        """BatimentHabitable 0x41cc70 for AX index; returns HabitacaoAplicada.

        Order: technology Bag; types 17/9/12 store +84=200 and return; type 4
        clears word +78; type 3 with owner<4 recomputes the warehouse level
        (division fault when per-warehouse capacity is 0, after the Bag);
        BatimentGetCase; DecouvreTerrain(cell, R+3, owner); IllumineTerrain
        (cell, R, owner); word +84=200. Owners >= 4 alias core grids in the
        original and raise at 0x476851; radii beyond core's gates raise at
        their call. Type bytes above 21 are rejected before any effect.
        """
        indice &= 65535
        s = self.construcoes.estruturas
        if indice >= 1000:
            raise ValueError('BatimentHabitable protected index is 0..999')
        if getattr(mundo, 'estruturas', None) is not s or getattr(mundo, 'unidades', None) is not self.producao.recrutamento.unidades:
            raise ValueError('Structure habitation requires the identical shared structure/unit pools')
        o = indice*PASSO_ESTRUTURA
        if s[o+8] >= 22:
            raise ValueError('BatimentHabitable protected structure type is 0..21 (above reads inherited EDI)')
        self.definir_tecnologia(s[o+4], s[o+8])
        tipo = s[o+8]
        if tipo in TIPOS_SEM_VISAO:
            struct.pack_into('<H', s, o+0x84, 200)
            return HabitacaoAplicada(indice, tipo, s[o+4], None, None)
        if tipo == 4:
            struct.pack_into('<H', s, o+0x78, 0)
        elif tipo == 3:
            self.construcoes.recalcular_recursos(s[o+4])
        raio = RAIOS[tipo]
        celula = celula_central_estrutura(s, indice)
        dono = s[o+4]
        descoberta, luz = limites_visao()
        if dono >= 4:
            raise DependenciaHabitacao(indice, 0x476851, 0x41cdb9, (celula, raio+3, dono),
                                       'owner grids exist only for owners 0..3')
        if raio+3 > descoberta:
            raise DependenciaHabitacao(indice, 0x476851, 0x41cdb9, (celula, raio+3, dono),
                                       f'discovery radius above core-validated {descoberta}')
        mundo.descobrir_area(celula, raio+3, dono)
        dono = s[o+4]
        if raio > luz:
            raise DependenciaHabitacao(indice, 0x476cb3, 0x41cdca, (celula, raio, dono),
                                       f'light radius above core-validated {luz}')
        mundo.iluminar_area(celula, raio, dono)
        struct.pack_into('<H', s, o+0x84, 200)
        return HabitacaoAplicada(indice, tipo, dono, celula, raio)
