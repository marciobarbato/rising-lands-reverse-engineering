"""Bind the integrated provider object graph to the one M1 memory map.

Every provider object is created by its owner's constructor, then each of its
state buffers is bound at the original address and filled in place from the
frozen entry snapshot (``MapaMemoriaM1.vincular``). When two providers model
the same original bytes, the first (Core's world, which most callees use) keeps
its buffer and the other is pointed at it by identity, as the committed
``casos_habitaveis.montar_habitacao`` composition already does. Constructor
state that has no declared original address is *denied*: the object's class is
swapped for a guarded subclass whose attribute access raises
``AtributoNaoMapeadoM1`` naming the attribute, its owner and the reason. Mapped
buffers may not be rebound by a provider either; only declared scalar caches
may be assigned. No value here is a default: an unbound byte cannot be read.
"""
from dataclasses import dataclass, field
import struct

import ambiente_missoes
from pathlib import Path
import sys

_IA = Path(__file__).resolve().parents[1] / 'ia-runtime'
if str(_IA) not in sys.path:
    sys.path.append(str(_IA))

from integracao.providers import load_economy_resources
load_economy_resources()
from economia import Economia                      # noqa: E402
from construcoes import Capacidades, EconomiaConstrucoes  # noqa: E402
from bonus_unidades import BonusUnidades            # noqa: E402
from mercado import Mercado, BUFFERS as BUFFERS_MERCADO  # noqa: E402
from ciclo_mercado import CicloMercado, BUFFERS_CICLO  # noqa: E402
from recrutamento import Recrutamento                # noqa: E402
from producao import Producao                        # noqa: E402
from proprietarios import PropriedadeConstrucoes     # noqa: E402
from aprendizagem import Aprendizagem                # noqa: E402
from construcoes_habitaveis import HabitacaoConstrucoes  # noqa: E402
from cauda_carga import CaudaCargaEconomia           # noqa: E402
from navegacao_unidades import MundoNavegacao        # noqa: E402

UNIDADES, BOLSAS, JOGADORES, JOGADORES_GUARDADOS, PROJETEIS = 0x4e19a0, 0x4e19b8, 0x5080a8, 0x5080ac, 0x5080f0
OBJETOS, ATRIBUTOS, TILES, DONOS, REGIOES = 0x507d74, 0x507da8, 0x507d70, 0x507dac, 0x4e0f38
DESCOBERTO, LUZ_BORDAS, CONTAGEM_LUZ = 0x507d78, 0x507d88, 0x507d98
MINIMAPAS = (('mini_final', 0x507d5c), ('mini_unidades', 0x507d60), ('mini_estruturas', 0x507d64))
SOMBRA, MARCADORES, ROTAS, GRADE_CORES = 0x4e24b4, 0x507db0, 0x4e1924, 0x4e156c
EXCESSO = 0x5c   # poison byte for provider-private bytes beyond a native allocation


class AtributoNaoMapeadoM1(NotImplementedError):
    def __init__(self, dono, atributo, motivo, escrita=False):
        self.dono, self.atributo, self.motivo, self.escrita = dono, atributo, motivo, escrita
        acao = 'assigned' if escrita else 'read'
        super().__init__(f'{dono}.{atributo} {acao}: {motivo}')


SEM_ENDERECO = 'constructor state with no declared original address in the M1 map'


def proteger(objeto, dono, permitidos, escalares=(), motivos=None):
    """Swap ``objeto``'s class for a guarded subclass (identity and isinstance kept).

    Every existing instance attribute outside ``permitidos`` (bound buffers and
    provider-object links) and ``escalares`` (declared scalar caches) is denied:
    any read or write raises with its reason. Writes to permitted attributes
    raise too, because mapped buffers and links must keep their identity.
    """
    classe = type(objeto)
    motivos = motivos or {}
    escalares = frozenset(escalares)
    permitidos = frozenset(permitidos)
    negados = {nome: motivos.get(nome, SEM_ENDERECO) for nome in vars(objeto)
               if nome not in permitidos and nome not in escalares}
    desconhecidos = (permitidos | escalares) - frozenset(vars(objeto))
    if desconhecidos:
        raise ValueError(f'{dono}: declared attributes {sorted(desconhecidos)} do not exist')

    def __getattribute__(self, nome):
        if nome in negados:
            raise AtributoNaoMapeadoM1(dono, nome, negados[nome])
        return classe.__getattribute__(self, nome)

    def __setattr__(self, nome, valor):
        if nome in negados:
            raise AtributoNaoMapeadoM1(dono, nome, negados[nome], escrita=True)
        if nome in permitidos:
            raise AtributoNaoMapeadoM1(dono, nome, 'mapped buffer/object must keep its identity', escrita=True)
        classe.__setattr__(self, nome, valor)

    objeto.__class__ = type(classe.__name__, (classe,), {
        '__getattribute__': __getattribute__, '__setattr__': __setattr__,
        '__module__': classe.__module__, '_m1_negados': negados, '_m1_dono': dono})
    return negados


class MascaraMapeada:
    """Read-only bytes of the live mapped range, read at use (type-20 mask 0x4dfb9c)."""
    def __init__(self, mapa, endereco, tamanho):
        self.mapa, self.endereco, self.tamanho = mapa, endereco, tamanho

    def __bytes__(self):
        return b''.join(self.mapa.ler(a, 1) for a in range(self.endereco, self.endereco + self.tamanho))

    def __len__(self):
        return self.tamanho


@dataclass
class ProvedoresM1:
    mapa: object
    mundo: object
    economia: object
    bonus: object
    mercado: object
    ciclo: object
    habitacao: object
    cauda: object
    vistas: dict = field(default_factory=dict)
    excessos: list = field(default_factory=list)   # (owner, buffer, start) of provider-private tails
    compartilhados: list = field(default_factory=list)  # identity sharing performed (consumer, owner)
    negados: dict = field(default_factory=dict)


def _ponteiro(mapa, slot):
    return struct.unpack('<I', mapa.ler_origem(slot, 4))[0]


def _vincular_alocacao(mapa, endereco, buffer, dono, excessos):
    """Bind a provider buffer at an allocation; an oversized provider buffer exposes only
    the allocation's bytes and its private excess is poisoned (verified unchanged later)."""
    tamanho = mapa.tamanho_bloco(endereco)
    if len(buffer) > tamanho:
        view = memoryview(buffer)
        view[tamanho:] = bytes([EXCESSO]) * (len(buffer) - tamanho)
        excessos.append((dono, buffer, tamanho))
        return mapa.vincular(endereco, view[:tamanho], dono)
    return mapa.vincular(endereco, buffer, dono)


def _cache_campo(mapa, endereco, formato, objeto, nome, dono):
    mapa.cache(endereco, formato, lambda: getattr(objeto, nome), lambda v: setattr(objeto, nome, v), dono)


def _cache_item(mapa, endereco, formato, sequencia, indice, dono):
    def definir(v):
        sequencia[indice] = v
    mapa.cache(endereco, formato, lambda: sequencia[indice], definir, dono)


def montar_provedores(mapa):
    """Create, bind and guard every provider object for one entry snapshot map (before ``fechar``)."""
    P = lambda slot: _ponteiro(mapa, slot)  # noqa: E731
    excessos, compartilhados = [], []
    larg, alt = struct.unpack('<HH', mapa.ler_origem(0x497168, 4))
    # MundoFisico validates 1..256; the cached values are reloaded from the bytes on every pull.
    w = MundoNavegacao(max(1, min(256, larg)), max(1, min(256, alt)))

    # ---- Core world byte buffers ------------------------------------------------
    mapa.vincular(P(UNIDADES), w.unidades, 'core:unidades [0x4e19a0]')
    mapa.vincular(0x49a0c8, w.estruturas, 'core:estruturas 0x49a0c8')
    mapa.vincular(0x49a070, w.realizaveis_estruturas, 'core:realizaveis_estruturas 0x49a070')
    mapa.vincular(0x495be0, w.selecoes_estruturas, 'core:selecoes_estruturas 0x495be0')
    mapa.vincular(0x4e19c4, w.experiencias_unidades, 'core:experiencias_unidades 0x4e19c4')
    mapa.vincular(0x508728, w.selecoes_unidades, 'core:selecoes_unidades 0x508728')
    tabela = P(BOLSAS)
    for i, bolsa in enumerate(w.bolsas_tipos_unidades):
        mapa.vincular(_ponteiro(mapa, tabela + 4 * i), bolsa, f'core:bolsas_tipos_unidades[{i}] [[0x4e19b8]+{4*i}]')
    mapa.vincular(0x51a9e0, w.grupos, 'core:grupos 0x51a9e0')
    mapa.vincular(P(OBJETOS), w.objetos, 'core:objetos [0x507d74]')
    mapa.vincular(P(ATRIBUTOS), w.atributos, 'core:atributos [0x507da8]')
    mapa.vincular_lista(P(REGIOES), w.regioes, 'H', 'core:regioes(list) [0x4e0f38]')
    mapa.vincular_lista(P(TILES), w.tiles, 'H', 'core:tiles(list) [0x507d70]')
    mapa.vincular(P(DONOS), w.donos_objetos, 'core:donos_objetos [0x507dac]')
    for nome, base in (('descoberto', DESCOBERTO), ('luz_bordas', LUZ_BORDAS), ('contagem_luz', CONTAGEM_LUZ)):
        for i, grade in enumerate(getattr(w, nome)):
            mapa.vincular(_ponteiro(mapa, base + 4 * i), grade, f'core:{nome}[{i}] [0x{base + 4*i:x}]')
    for nome, slot in MINIMAPAS:
        _vincular_alocacao(mapa, P(slot), getattr(w, nome), f'core:{nome} [0x{slot:x}]', excessos)
    mapa.vincular(0x4e24dc, w.cores_jogadores, 'core:cores_jogadores 0x4e24dc')
    mapa.vincular(0x509694, w.cores_tiles, 'core:cores_tiles 0x509694')
    mapa.vincular(P(SOMBRA), w.sombra, 'core:sombra [0x4e24b4]')
    rotas = P(ROTAS)
    for i, rota in enumerate(w.rotas):
        mapa.vincular(_ponteiro(mapa, rotas + 4 * i), rota, f'core:rotas[{i}]')
    mapa.vincular(P(MARCADORES), w.marcadores_obstaculos_tiles, 'core:marcadores_obstaculos_tiles [0x507db0]')
    cores = w.cores_estruturas
    mapa.vincular(P(GRADE_CORES), cores.grade, 'core:cores_estruturas.grade [0x4e156c]')
    mapa.vincular(0x4e1570, cores.livres, 'core:cores_estruturas.livres 0x4e1570')
    mapa.vincular(0x4e1670, cores.liberadas, 'core:cores_estruturas.liberadas 0x4e1670')
    mapa.vincular_lista(0x4e0732, cores.pilha, 'H', 'core:cores_estruturas.pilha(list) 0x4e0732')

    # ---- Economy byte buffers ----------------------------------------------------
    economia = Economia()
    mapa.vincular(0x4e2ea8, economia.memoria, 'economy:Economia.memoria 0x4e2ea8')
    bonus = BonusUnidades()
    mapa.vincular(0x4dfba0, bonus.memoria, 'economy:BonusUnidades.memoria 0x4dfba0')
    mapa.vincular(0x4965ae, bonus.tipos_unidades, 'economy:BonusUnidades.tipos_unidades 0x4965ae')
    mercado = Mercado(economia)
    mapa.vincular(P(JOGADORES), mercado.jogadores, 'economy:Mercado.jogadores [0x5080a8]')
    for nome, (endereco, _) in BUFFERS_MERCADO.items():
        mapa.vincular(endereco, getattr(mercado, nome), f'economy:Mercado.{nome} 0x{endereco:x}')
    ciclo = CicloMercado(mercado)
    for nome, (endereco, _) in BUFFERS_CICLO.items():
        mapa.vincular(endereco, getattr(ciclo, nome), f'economy:CicloMercado.{nome} 0x{endereco:x}')
    capacidades = Capacidades()
    mapa.vincular(0x4dfb2c, capacidades.memoria, 'economy:Capacidades.memoria 0x4dfb2c')
    construcoes = EconomiaConstrucoes(economia, capacidades)
    mapa.vincular(0x4dfb4c, construcoes.contagens_tipo18, 'economy:EconomiaConstrucoes.contagens_tipo18 0x4dfb4c')
    for consumidor, alvo in ((('EconomiaConstrucoes.estruturas', construcoes, 'estruturas'), w.estruturas),
                             (('EconomiaConstrucoes.contagens_por_tipo', construcoes, 'contagens_por_tipo'),
                              w.realizaveis_estruturas),
                             (('TerrenoSacolas.tipos', construcoes.terreno, 'tipos'), w.objetos),
                             (('TerrenoSacolas.quantidades', construcoes.terreno, 'quantidades'), w.donos_objetos)):
        setattr(consumidor[1], consumidor[2], alvo)
        compartilhados.append(consumidor[0])
    recrutamento = Recrutamento(construcoes)
    recrutamento.selecoes, recrutamento.unidades = w.selecoes_estruturas, w.unidades
    recrutamento.tipos_unidades = bonus.tipos_unidades
    compartilhados += ['Recrutamento.selecoes', 'Recrutamento.unidades', 'Recrutamento.tipos_unidades']
    mapa.vincular(0x497174, recrutamento.tipos_sortilegios, 'economy:Recrutamento.tipos_sortilegios 0x497174')
    producao = Producao(recrutamento)
    mapa.vincular(0x495d8c, producao.tipos_construcoes, 'economy:Producao.tipos_construcoes 0x495d8c')
    propriedade = PropriedadeConstrucoes(construcoes)
    mapa.vincular(0x4e1a14, propriedade.baloes, 'economy:PropriedadeConstrucoes.baloes 0x4e1a14')
    mapa.vincular(0x4dd6e8, propriedade.pendencias, 'economy:PropriedadeConstrucoes.pendencias 0x4dd6e8')
    mapa.vincular(0x508f30, propriedade.sortilegios, 'economy:PropriedadeConstrucoes.sortilegios 0x508f30')
    aprendizagem = Aprendizagem(producao, propriedade)
    mapa.vincular(0x508f44, aprendizagem.inventados, 'economy:Aprendizagem.inventados 0x508f44')
    # Missions-owned explicit inputs handed to economy by identity (constructor stores them as given).
    unidades_realizaveis = bytearray(104)
    estruturas_realizaveis = bytearray(88)
    rede = bytearray(1)
    guardados = bytearray(80)
    mapa.vincular(0x4e1934, unidades_realizaveis, 'missions:TypeEnginEstRealisable 0x4e1934')
    mapa.vincular(0x4dfad4, estruturas_realizaveis, 'missions:TypeBatimentEstRealisable 0x4dfad4')
    mapa.vincular(0x4e0730, rede, 'missions:ReseauActif byte 0x4e0730')
    mapa.vincular(P(JOGADORES_GUARDADOS), guardados, 'missions:stored players [0x5080ac]')
    habitacao = HabitacaoConstrucoes(aprendizagem, unidades_realizaveis=unidades_realizaveis,
                                     estruturas_realizaveis=estruturas_realizaveis)
    cauda = CaudaCargaEconomia(habitacao, ciclo, rede=rede, jogadores_guardados=guardados)

    # ---- Missions-owned byte views/buffers ---------------------------------------
    guardadas = bytearray(40)
    mapa.vincular(0x4e19ec, guardadas, 'missions:saved experience 0x4e19ec')
    vistas = dict(experiencia_guardada=guardadas)

    # ---- Scalar caches (bytes canonical) ----------------------------------------
    busca = w.busca
    for endereco, formato, nome in ((0x496304, 'H', 'unidade'), (0x4e0f36, 'B', 'ocupada'),
                                    (0x4e0f37, 'B', 'sucesso'), (0x4e0f3c, 'I', 'ponteiro_rota'),
                                    (0x496302, 'B', 'concluida')):
        _cache_campo(mapa, endereco, formato, busca, nome, f'core:busca.{nome}')
    for alvo, rotulo in ((w, 'core:mundo'), (cores, 'core:cores_estruturas')):
        _cache_campo(mapa, 0x497168, 'H', alvo, 'largura', f'{rotulo}.largura')
        _cache_campo(mapa, 0x49716a, 'H', alvo, 'altura', f'{rotulo}.altura')
    _cache_campo(mapa, 0x51b844, 'I', w, 'grupo_em_iteracao', 'core:grupo_em_iteracao')
    _cache_campo(mapa, 0x51b848, 'H', w, 'unidade_em_iteracao', 'core:unidade_em_iteracao')
    mapa.cache(0x496fe0, 'H', lambda: w.tamanho_minimapa[0],
               lambda v: setattr(w, 'tamanho_minimapa', (v, w.tamanho_minimapa[1])), 'core:tamanho_minimapa[0]')
    mapa.cache(0x496fe2, 'H', lambda: w.tamanho_minimapa[1],
               lambda v: setattr(w, 'tamanho_minimapa', (w.tamanho_minimapa[0], v)), 'core:tamanho_minimapa[1]')
    _cache_campo(mapa, 0x508041, 'B', w, 'jogador_local', 'core:jogador_local')
    jogadores = P(JOGADORES)
    for j in range(4):
        _cache_item(mapa, jogadores + 20 * j + 1, 'B', w.controle_jogadores, j, f'core:controle_jogadores[{j}]')
        _cache_item(mapa, jogadores + 20 * j + 6, 'B', w.mascaras_alianca, j, f'core:mascaras_alianca[{j}]')
    # mascaras_alianca has a fifth byte with no original address (pathfinding-only owner 4).
    w.mascaras_alianca[4] = EXCESSO
    excessos.append(('core:mascaras_alianca[4] (no original address)', w.mascaras_alianca, 4))
    for t in range(26):
        _cache_item(mapa, 0x4965dc + 50 * t, 'H', w.limites_fadiga, t, f'core:limites_fadiga[{t}]')
        for d in range(4):
            _cache_item(mapa, 0x4dfba0 + 468 * d + 18 * t, 'H', w.bonus_fadiga[d], t, f'core:bonus_fadiga[{d}][{t}]')
    _cache_campo(mapa, 0x497164, 'I', w, 'semente_caminhos', 'core:semente_caminhos')
    _cache_campo(mapa, 0x497164, 'I', construcoes.terreno, 'semente', 'economy:TerrenoSacolas.semente')
    _cache_campo(mapa, 0x4e1771, 'B', w, 'permitir_aliados_parados', 'core:permitir_aliados_parados')
    _cache_campo(mapa, 0x4e1a34, 'H', w, 'ultimo_bloqueador', 'core:ultimo_bloqueador')
    _cache_campo(mapa, 0x4e1a36, 'H', w, 'ultima_celula_livre', 'core:ultima_celula_livre')
    _cache_campo(mapa, 0x495bf8, 'B', w, 'objeto_muro', 'core:objeto_muro')
    _cache_campo(mapa, 0x495bf9, 'B', w, 'objeto_portao', 'core:objeto_portao')
    _cache_campo(mapa, 0x495bf0, 'H', recrutamento, 'periodo_nova', 'economy:Recrutamento.periodo_nova')
    _cache_campo(mapa, 0x495be8, 'B', producao, 'ajuste_hospital', 'economy:Producao.ajuste_hospital')

    # ---- Guards -------------------------------------------------------------------
    negados = {}
    negados['core:MundoNavegacao'] = proteger(w, 'core:MundoNavegacao', (
        'unidades', 'estruturas', 'realizaveis_estruturas', 'selecoes_estruturas', 'experiencias_unidades',
        'selecoes_unidades', 'bolsas_tipos_unidades', 'grupos', 'objetos', 'busca', 'atributos', 'regioes',
        'tiles', 'donos_objetos', 'descoberto', 'luz_bordas', 'contagem_luz', 'mini_final', 'mini_unidades',
        'mini_estruturas', 'cores_jogadores', 'cores_tiles', 'sombra', 'controle_jogadores', 'limites_fadiga',
        'bonus_fadiga', 'rotas', 'marcadores_obstaculos_tiles', 'mascaras_alianca', 'cores_estruturas'),
        ('largura', 'altura', 'tamanho_minimapa', 'jogador_local', 'grupo_em_iteracao', 'unidade_em_iteracao',
         'semente_caminhos', 'permitir_aliados_parados', 'ultimo_bloqueador', 'ultima_celula_livre',
         'objeto_muro', 'objeto_portao'),
        dict(solucionador='Python path-solver hook; no original state',
             resultados_busca='Python search-result cache; no original state',
             historico_navegacao='Python navigation trace; no original state'))
    negados['core:ContextoBusca'] = proteger(busca, 'core:ContextoBusca', (),
                                            ('unidade', 'ocupada', 'sucesso', 'ponteiro_rota', 'concluida'))
    negados['core:CoresEstruturas'] = proteger(cores, 'core:CoresEstruturas', ('grade', 'livres', 'liberadas', 'pilha'),
                                              ('largura', 'altura'))
    negados['economy:PropriedadeConstrucoes'] = proteger(
        propriedade, 'economy:PropriedadeConstrucoes', ('mundo', 'baloes', 'pendencias', 'sortilegios'), (),
        dict(ordens=('single 10,816-byte buffer (4 x 2,704 owner stride); the original and Core keep four '
                     'distinct 2,704-byte allocations through the pointer table [0x4e19b8], so it cannot '
                     'alias them')))
    negados['economy:TerrenoSacolas'] = proteger(construcoes.terreno, 'economy:TerrenoSacolas',
                                                ('tipos', 'quantidades'), ('semente',))
    negados['economy:Recrutamento'] = proteger(recrutamento, 'economy:Recrutamento', (
        'mundo', 'selecoes', 'tipos_unidades', 'tipos_sortilegios', 'unidades'), ('periodo_nova',))
    negados['economy:Producao'] = proteger(producao, 'economy:Producao', ('recrutamento', 'tipos_construcoes'),
                                          ('ajuste_hospital',))
    for objeto, dono, permitidos in (
            (economia, 'economy:Economia', ('memoria',)),
            (bonus, 'economy:BonusUnidades', ('memoria', 'tipos_unidades')),
            (mercado, 'economy:Mercado', ('economia', 'jogadores') + tuple(BUFFERS_MERCADO)),
            (ciclo, 'economy:CicloMercado', ('mercado',) + tuple(BUFFERS_CICLO)),
            (capacidades, 'economy:Capacidades', ('memoria',)),
            (construcoes, 'economy:EconomiaConstrucoes', ('economia', 'capacidades', 'estruturas', 'terreno',
                                                         'contagens_por_tipo', 'contagens_tipo18')),
            (aprendizagem, 'economy:Aprendizagem', ('producao', 'propriedade', 'inventados')),
            (habitacao, 'economy:HabitacaoConstrucoes', ('aprendizagem', 'producao', 'construcoes', 'propriedade',
                                                        'unidades_realizaveis', 'estruturas_realizaveis')),
            (cauda, 'economy:CaudaCargaEconomia', ('habitacao', 'construcoes', 'ciclo', 'rede',
                                                   'jogadores_guardados'))):
        negados[dono] = proteger(objeto, dono, permitidos)
    return ProvedoresM1(mapa, w, economia, bonus, mercado, ciclo, habitacao, cauda, vistas,
                        excessos, compartilhados, negados)


def verificar_excessos(provedores):
    """Provider-private bytes beyond a native allocation must still hold the poison byte."""
    alterados = []
    for dono, buffer, inicio in provedores.excessos:
        cauda = bytes(buffer[inicio:])
        if cauda != bytes([EXCESSO]) * len(cauda):
            alterados.append(dict(owner=dono, first_offset=inicio + next(
                i for i, b in enumerate(cauda) if b != EXCESSO)))
    return alterados
