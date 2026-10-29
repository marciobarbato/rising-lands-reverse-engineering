"""Explicit Stage 15 fixtures: actual MONDE01 records and synthetic edge worlds.

Only inherited buffers are built here. Nothing economic or physical is
computed, so the same cases feed original-only captures and comparisons.
"""
from dataclasses import dataclass
from pathlib import Path
import random
import struct
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _caminho in (RAIZ/'ferramentas', PASTA):
    if str(_caminho) not in sys.path:
        sys.path.insert(0, str(_caminho))
# Bind economy's flat module names before the missions bootstrap adds the
# graphics folder (which has a different 'construcoes') to the search path.
import construcoes  # noqa: F401
from construcoes import Capacidades
from economia import Economia
from bonus_unidades import BonusUnidades
from navegacao_unidades import MundoNavegacao
from ordens_unidades import ContextoBusca

PASSO = 276
TIPOS_SEM_VISAO = (9, 12, 17)


@dataclass
class CasoHabitavel:
    nome: str
    origem: str
    indice: int
    mundo: object
    economia: Economia
    capacidades: Capacidades
    pendencias: bytearray            # 0x4dd6e8: 4 owners x 22 types x 104-byte Bags
    sortilegios: bytearray           # 0x508f30: SortilegeEstRealisable bytes
    inventados: bytearray            # 0x508f44: SortilegeEstInvente bytes
    unidades_realizaveis: bytearray  # 0x4e1934: TypeEnginEstRealisable, 4 x 26
    estruturas_realizaveis: bytearray  # 0x4dfad4: TypeBatimentEstRealisable, 4 x 22
    rede: int                        # 0x4e0730: read by ReseauActif, result discarded


def _tabelas(rng, padrao):
    if padrao == 'zero':
        return bytearray(104), bytearray(88), bytearray(20), bytearray(20)
    if padrao == 'um':
        return bytearray([1]*104), bytearray([1]*88), bytearray([1]*20), bytearray([1]*20)
    escolha = lambda n: bytearray(rng.choice((0, 0, 1, 2, 0x80, 255)) for _ in range(n))
    return escolha(104), escolha(88), escolha(20), escolha(20)


def _economia(rng, caso_economia=None):
    economia = caso_economia or Economia(bytearray(rng.randbytes(128)))
    capacidades = Capacidades(bytearray(rng.randbytes(24)))
    return economia, capacidades


def _grades_semeadas(mundo, rng):
    for dono in range(4):
        for celula in range(65536):
            if rng.random() < 0.08:
                mundo.descoberto[dono][celula] = rng.randrange(32)
                mundo.luz_bordas[dono][celula] = rng.randrange(32)
                mundo.contagem_luz[dono][celula] = rng.choice((0, 1, 2, 254, 255))


def caso_monde01(nome='MONDE01', *, padrao='zero', semear_grades=False, semente=0x41cc70,
                 classe=MundoNavegacao, local=0):
    """Actual MONDE01 header, structure record 0 and 16 units via committed loaders.

    Physical grids, technology/spell tables, Bags and pools outside the
    loaded records are explicit synthetic inherited inputs, not load results.
    """
    missoes = str(RAIZ/'pesquisas-paralelas/missoes')
    if missoes not in sys.path:
        sys.path.append(missoes)  # after economy, so flat economy names stay bound
    import ambiente_missoes
    from formatos import Leitor, ler_eta
    from carregador_cabecalho import continuar_cabecalho
    from carregador_estruturas import carregar_estruturas_missao
    from carregador_unidades import carregar_unidades_missao
    from entradas import tipos_originais, bloco_unidades
    rng = random.Random(semente)
    dados = (ambiente_missoes.CD/'WORLD/MONDE01.ETA').read_bytes()
    meta = ler_eta(dados)
    mundo = classe(meta['largura'], meta['altura'])
    mundo.jogador_local = local
    economia = Economia(bytearray(rng.randbytes(128)))
    camadas = [bytearray(65536), bytearray(131072), bytearray(65536), bytearray(65536)]
    continuar_cabecalho(Leitor(dados, 0), *camadas, economia, bytearray(4), bytearray(4), 0)
    mundo.atributos[:] = camadas[0]
    mundo.tiles[:] = struct.unpack('<65536H', camadas[1])
    mundo.objetos[:] = camadas[2]
    mundo.donos_objetos[:] = camadas[3]
    mundo.regioes[:] = [1]*65536
    mundo.busca = ContextoBusca(7, 1, 1, 0x12345678, 77)
    mundo.unidades[:] = b'\xa5'*220800
    for i in range(800):
        mundo.unidades[i*PASSO+2] = 0
    tipos = tipos_originais()
    bonus = BonusUnidades(b'\x31'*1872)
    carregar_unidades_missao(Leitor(dados, bloco_unidades(dados)['offset']), mundo.unidades,
                             bytearray(b'\x11\x22\x33\x44'), tipos, mundo.selecoes_unidades,
                             modificador12=lambda dono, tipo: bonus.consultar(dono, tipo, 12))
    mundo.estruturas[:] = bytes((i*29+0x3b) & 255 for i in range(276000))
    for i in range(1000):
        mundo.estruturas[i*PASSO+5] = 0
    bloco = next(b for b in meta['blocos'] if b['nome'] == 'estruturas')
    carregar_estruturas_missao(Leitor(dados, bloco['offset']), mundo.estruturas)
    if semear_grades:
        _grades_semeadas(mundo, rng)
    _, capacidades = _economia(rng, economia)
    ur, er, so, inv = _tabelas(rng, padrao)
    return CasoHabitavel(nome, 'MONDE01 disk header/structure/units; synthetic inherited tables and grids',
                         0, mundo, economia, capacidades, bytearray(rng.randbytes(9152)), so, inv, ur, er,
                         rng.randrange(256))


def registro_estrutura(rng, tipo, dono, origem, *, unidades=(), etiquetas=None, capacidade=None, estado=5):
    r = bytearray(rng.randbytes(PASSO))
    r[4], r[5], r[8] = dono, estado, tipo
    struct.pack_into('<H', r, 2, origem)
    etiquetas = [1]*len(unidades) if etiquetas is None else list(etiquetas)
    capacidade = len(unidades) if capacidade is None else capacidade
    struct.pack_into('<HH', r, 0x0c, len(unidades), capacidade)
    for slot in range(30):
        valor = unidades[slot] if slot < len(unidades) else rng.randrange(800)
        struct.pack_into('<H', r, 0x12+2*slot, valor)
        r[0x4e+slot] = etiquetas[slot] if slot < len(etiquetas) else rng.choice((0, 2, 6))
    return r


def caso_sintetico(nome, tipo, dono, origem, *, largura=256, altura=256, unidades=(), tipos_unidades=(),
                   etiquetas=None, capacidade=None, padrao='aleatorio', semear_grades=False,
                   armazens=None, semente=0, indice=None, local=0, classe=MundoNavegacao):
    """One structure on an explicit synthetic world; units carry given type bytes."""
    rng = random.Random(f'{nome}:{semente}')
    mundo = classe(largura, altura)
    mundo.jogador_local = local
    mundo.unidades[:] = rng.randbytes(220800)
    for u, t in zip(unidades, tipos_unidades):
        mundo.unidades[u*PASSO+1] = t
    mundo.estruturas[:] = rng.randbytes(276000)
    for i in range(1000):
        mundo.estruturas[i*PASSO+5] = 0
    indice = rng.choice((0, 1, 517, 998, 999)) if indice is None else indice
    mundo.estruturas[indice*PASSO:(indice+1)*PASSO] = registro_estrutura(
        rng, tipo, dono, origem, unidades=unidades, etiquetas=etiquetas, capacidade=capacidade)
    for celula in range(65536):
        mundo.tiles[celula] = rng.randrange(702)
    mundo.objetos[:] = rng.randbytes(65536)
    mundo.regioes[:] = [1]*65536
    if semear_grades:
        _grades_semeadas(mundo, rng)
    economia, capacidades = _economia(rng)
    if armazens is not None:
        for j in range(4):
            struct.pack_into('<HH', capacidades.memoria, j*6, *armazens)
    ur, er, so, inv = _tabelas(rng, padrao)
    return CasoHabitavel(nome, 'synthetic', indice, mundo, economia, capacidades,
                         bytearray(rng.randbytes(9152)), so, inv, ur, er, rng.randrange(256))


def montar_habitacao(caso, *, ordens=None):
    """Compose existing economy classes over the case buffers, by identity.

    ``ordens``: the four per-owner unit-order pools for PropriedadeConstrucoes
    (None keeps its four fresh zero pools)."""
    from construcoes import EconomiaConstrucoes
    from recrutamento import Recrutamento
    from producao import Producao
    from proprietarios import PropriedadeConstrucoes
    from aprendizagem import Aprendizagem
    from construcoes_habitaveis import HabitacaoConstrucoes
    m = caso.mundo
    construcoes = EconomiaConstrucoes(caso.economia, caso.capacidades)
    construcoes.estruturas = m.estruturas
    recrutamento = Recrutamento(construcoes)
    recrutamento.unidades = m.unidades
    propriedade = PropriedadeConstrucoes(construcoes, ordens=ordens)
    propriedade.pendencias, propriedade.sortilegios = caso.pendencias, caso.sortilegios
    aprendizagem = Aprendizagem(Producao(recrutamento), propriedade)
    aprendizagem.inventados = caso.inventados
    return HabitacaoConstrucoes(aprendizagem, unidades_realizaveis=caso.unidades_realizaveis,
                                estruturas_realizaveis=caso.estruturas_realizaveis)
