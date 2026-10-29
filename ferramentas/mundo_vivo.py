"""Core's navigation world (``MundoNavegacao``) bound live to a flat original memory.

Missions' ``ligacao_provedores_m1.montar_provedores`` binds the same world to a ``MapaMemoriaM1``
snapshot: it copies the bytes in and serializes them out. This binding instead makes every
buffer of the world a live view of the caller's memory. Every scalar is a property that reads
and writes its original address, so no pull/push is needed, and each frame of a chained Python
run sees and leaves the original layout. It uses the same original addresses as Missions'
mapping:
- the unit pool ``[0x4e19a0]`` and the structures ``0x49a0c8``;
- the terrain grids (``vincular_grades``) and the discovery, light and minimap grids;
- the route buffers ``[[0x4e1924] + 4i]``, the search context ``0x496304``/``0x4e0f36..``;
- the per-player and per-type tables.

The path solver is an explicit argument; using the search without one raises ``EstadoSemEndereco``
(a ``NotImplementedError``), as does ``mascaras_alianca[4]``, which has no original address. The
search result the world keeps per unit is the original's global pair: status u8 ``0x4e0f4c`` and
alternative cell u16 ``0x4e0f4a``, which DeplaceEngin's state 4 reads. The navigation trace is a
write-only Python list, a diagnostic that nothing in the game logic reads. ``memoria`` needs ``u8/u16/u32`` and either ``vista(addr, n)`` or
``segmentos`` of ``(base, end, view)``.
"""
import struct

from grade_u16 import GradeU16
from estruturas_caminhos import CoresEstruturas
from navegacao_unidades import MundoNavegacao
from ordens_unidades import ContextoBusca

PASSO = 276
UNIDADES, BOLSAS, JOGADORES = 0x4e19a0, 0x4e19b8, 0x5080a8
OBJETOS, ATRIBUTOS, TILES, DONOS, REGIOES = 0x507d74, 0x507da8, 0x507d70, 0x507dac, 0x4e0f38
DESCOBERTO, LUZ_BORDAS, CONTAGEM_LUZ = 0x507d78, 0x507d88, 0x507d98
MINIMAPAS = (('mini_final', 0x507d5c), ('mini_unidades', 0x507d60), ('mini_estruturas', 0x507d64))
SOMBRA, MARCADORES, ROTAS, GRADE_CORES = 0x4e24b4, 0x507db0, 0x4e1924, 0x4e156c
# Scalar fields of the world: name -> (address, struct format)
ESCALARES = dict(largura=(0x497168, 'H'), altura=(0x49716a, 'H'), jogador_local=(0x508041, 'B'),
                 semente_caminhos=(0x497164, 'I'), grupo_em_iteracao=(0x51b844, 'I'),
                 unidade_em_iteracao=(0x51b848, 'H'), permitir_aliados_parados=(0x4e1771, 'B'),
                 ultimo_bloqueador=(0x4e1a34, 'H'), ultima_celula_livre=(0x4e1a36, 'H'),
                 objeto_muro=(0x495bf8, 'B'), objeto_portao=(0x495bf9, 'B'))
BUSCA = dict(unidade=(0x496304, 'H'), ocupada=(0x4e0f36, 'B'), sucesso=(0x4e0f37, 'B'),
             ponteiro_rota=(0x4e0f3c, 'I'), concluida=(0x496302, 'B'))
STATUS_BUSCA, DESTINO_ALTERNATIVO = 0x4e0f4c, 0x4e0f4a   # read by DeplaceEngin's state 4 (0x4493f9, 0x449402)


class EstadoSemEndereco(NotImplementedError):
    def __init__(self, nome, motivo):
        super().__init__(f'{nome}: {motivo}; it has no original address in the live world')
        self.nome = nome


def _acesso(m, formato):
    return {'B': m.u8, 'H': m.u16, 'I': m.u32}[formato]


def vista_de(m, endereco, tamanho):
    """Writable live view of ``tamanho`` bytes at ``endereco`` inside one segment of ``m``."""
    if hasattr(m, 'vista'):
        return m.vista(endereco, tamanho)
    for base, fim, view in m.segmentos:
        if base <= endereco and endereco + tamanho <= fim:
            return memoryview(view)[endereco - base:endereco - base + tamanho]
    raise ValueError(f'[0x{endereco:08x},+{tamanho}) is not inside one live segment')


class _Itens:
    """A fixed sequence whose items are scalars at original addresses."""
    def __init__(self, m, enderecos, formato, nome):
        self._m, self._enderecos, self._f, self._nome = m, list(enderecos), formato, nome

    def __len__(self):
        return len(self._enderecos)

    def __getitem__(self, i):
        endereco = self._enderecos[i]
        if endereco is None:
            raise EstadoSemEndereco(f'{self._nome}[{i}]', 'pathfinding-only entry')
        return _acesso(self._m, self._f)(endereco)

    def __setitem__(self, i, valor):
        endereco = self._enderecos[i]
        if endereco is None:
            raise EstadoSemEndereco(f'{self._nome}[{i}]', 'pathfinding-only entry')
        _acesso(self._m, self._f)(endereco, valor)

    def __iter__(self):
        return (self[i] for i in range(len(self)))


class _Rotas:
    """The 800 route buffers ``[[0x4e1924] + 4i]`` (512 bytes each); a stored route is copied in place."""
    def __init__(self, m):
        self._m = m
        tabela = m.u32(ROTAS)
        self._ponteiros = [m.u32(tabela + 4 * i) for i in range(800)]

    def __len__(self):
        return 800

    def __getitem__(self, i):
        return vista_de(self._m, self._ponteiros[i], 512)

    def __setitem__(self, i, valor):
        dados = bytes(valor)
        if len(dados) > 512:
            raise ValueError('A route buffer holds 512 bytes')
        vista_de(self._m, self._ponteiros[i], len(dados))[:] = dados


def _propriedade(enderecos, nome):
    endereco, formato = enderecos[nome]

    def obter(self):
        return _acesso(self._memoria, formato)(endereco)

    def definir(self, valor):
        _acesso(self._memoria, formato)(endereco, valor)
    return property(obter, definir)


def _negada(nome, motivo):
    def falhar(self, *_):
        raise EstadoSemEndereco(nome, motivo)
    return property(falhar, falhar)


class _ResultadosVivos:
    """``resultados_busca[unit]``: the original keeps one global result pair, read back by DeplaceEngin."""
    def __init__(self, m):
        self._m = m

    def __getitem__(self, indice):
        return dict(status=self._m.u8(STATUS_BUSCA), destino_alternativo=self._m.u16(DESTINO_ALTERNATIVO))

    def __setitem__(self, indice, resultado):
        self._m.u8(STATUS_BUSCA, resultado['status'])
        self._m.u16(DESTINO_ALTERNATIVO, resultado['destino_alternativo'])


class BuscaViva(ContextoBusca):
    """The search context at its original scalars."""
    def __init__(self, m):
        object.__setattr__(self, '_memoria', m)


class CoresEstruturasVivas(CoresEstruturas):
    """Structure-colour state: grid ``[0x4e156c]``, free/released tables, u16 stack ``0x4e0732``."""
    largura = _propriedade(ESCALARES, 'largura')
    altura = _propriedade(ESCALARES, 'altura')

    def __init__(self, m):
        self._memoria = m
        self.grade = vista_de(m, m.u32(GRADE_CORES), 65536)
        self.livres = vista_de(m, 0x4e1570, 256)
        self.liberadas = vista_de(m, 0x4e1670, 256)
        self.pilha = GradeU16(vista_de(m, 0x4e0732, 2048), 1024)


class MundoNavegacaoVivo(MundoNavegacao):
    @property
    def solucionador(self):
        if self._solucionador is None:
            raise EstadoSemEndereco('solucionador', 'no path solver was given to mundo_vivo')
        return self._solucionador

    @property
    def tamanho_minimapa(self):
        return self._memoria.u16(0x496fe0), self._memoria.u16(0x496fe2)

    @tamanho_minimapa.setter
    def tamanho_minimapa(self, valor):
        self._memoria.u16(0x496fe0, valor[0])
        self._memoria.u16(0x496fe2, valor[1])


for _n in BUSCA:
    setattr(BuscaViva, _n, _propriedade(BUSCA, _n))
for _n in ESCALARES:
    setattr(MundoNavegacaoVivo, _n, _propriedade(ESCALARES, _n))


def ponteiros_rotas(memoria):
    """The 800 route buffer addresses ``[[0x4e1924] + 4i]`` (the solver's route identifiers)."""
    tabela = memoria.u32(ROTAS)
    return [memoria.u32(tabela + 4 * i) for i in range(800)]


def mundo_vivo(memoria, solucionador=None):
    """A ``MundoNavegacao`` whose state is the caller's live original memory (see the module docstring)."""
    m = memoria
    P = m.u32
    w = MundoNavegacaoVivo.__new__(MundoNavegacaoVivo)
    w._memoria = m
    w._solucionador = solucionador
    w.resultados_busca = _ResultadosVivos(m)
    w.historico_navegacao = []
    w.unidades = vista_de(m, P(UNIDADES), 800 * PASSO)
    w.estruturas = vista_de(m, 0x49a0c8, 1000 * PASSO)
    w.realizaveis_estruturas = vista_de(m, 0x49a070, 88)
    w.selecoes_estruturas = vista_de(m, 0x495be0, 8)
    w.experiencias_unidades = vista_de(m, 0x4e19c4, 40)
    w.selecoes_unidades = vista_de(m, 0x508728, 2048)
    w.bolsas_tipos_unidades = [vista_de(m, P(P(BOLSAS) + 4 * i), 26 * 104) for i in range(4)]
    w.grupos = vista_de(m, 0x51a9e0, 100 * 32)
    w.objetos = vista_de(m, P(OBJETOS), 65536)
    w.vincular_grades(tiles=vista_de(m, P(TILES), 131072), regioes=vista_de(m, P(REGIOES), 131072),
                      atributos=vista_de(m, P(ATRIBUTOS), 65536), objetos=w.objetos,
                      donos_objetos=vista_de(m, P(DONOS), 65536))
    for nome, base in (('descoberto', DESCOBERTO), ('luz_bordas', LUZ_BORDAS), ('contagem_luz', CONTAGEM_LUZ)):
        setattr(w, nome, [vista_de(m, P(base + 4 * i), 65536) for i in range(4)])
    largura_mm, altura_mm = w.tamanho_minimapa
    for nome, slot in MINIMAPAS:
        setattr(w, nome, vista_de(m, P(slot), largura_mm * altura_mm))
    w.cores_jogadores = vista_de(m, 0x4e24dc, 32)
    w.cores_tiles = vista_de(m, 0x509694, 702)
    w.sombra = vista_de(m, P(SOMBRA), 256)
    w.rotas = _Rotas(m)
    w.marcadores_obstaculos_tiles = vista_de(m, P(MARCADORES), 702)
    w.cores_estruturas = CoresEstruturasVivas(m)
    w.busca = BuscaViva(m)
    jogadores = P(JOGADORES)
    w.controle_jogadores = _Itens(m, (jogadores + 20 * j + 1 for j in range(4)), 'B', 'controle_jogadores')
    w.mascaras_alianca = _Itens(m, [jogadores + 20 * j + 6 for j in range(4)] + [None], 'B', 'mascaras_alianca')
    w.limites_fadiga = _Itens(m, (0x4965dc + 50 * t for t in range(26)), 'H', 'limites_fadiga')
    w.bonus_fadiga = [_Itens(m, (0x4dfba0 + 468 * d + 18 * t for t in range(26)), 'H', f'bonus_fadiga[{d}]')
                      for d in range(4)]
    return w
