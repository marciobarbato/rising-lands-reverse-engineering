"""Production delegates for IaReset over explicit, aliased live allocations.

No original observations supply callback returns or stores. Missing owner
primitives remain named stops at their original CALL; controls are inherited.
"""
import ctypes
import importlib
from pathlib import Path
import sys

from ambiente_ia_runtime import ROOT
for pasta in (ROOT, ROOT / 'pesquisas-paralelas/economia', ROOT / 'pesquisas-paralelas/missoes',
              ROOT / 'pesquisas-paralelas/combate'):
    if str(pasta) not in sys.path:
        sys.path.append(str(pasta))
from integracao.providers import load_economy_resources
load_economy_resources()
from economia import Economia
from mercado import Mercado
from ordens_unidades import MundoUnidades
from consultas_unidades import tipo_unidade, tipo_unidade_monstro
from consultas_missao import numero_missao, existe_estrutura
from ataque_vivo import batiment_get_player
from memoria_ia_runtime import MemoriaDeclarada
from reinicio_ia import DependenciaIA, GRUPOS, JOGADORES, UNIDADES, reiniciar_ia


def _endereco_buffer(buffer):
    view = memoryview(buffer)
    if view.readonly or view.ndim != 1 or not view.c_contiguous or view.format != 'B' or not len(view):
        raise ValueError('Alias validation requires a nonempty writable contiguous B buffer')
    return ctypes.addressof(ctypes.c_ubyte.from_buffer(view)), len(view)


def _alias(memoria, endereco, tamanho, buffer, nome):
    view, offset = memoria._local(endereco, tamanho, declarado=False)
    if _endereco_buffer(view[offset:offset+tamanho]) != _endereco_buffer(buffer):
        raise ValueError(f'{nome} must alias the exact mapped host range at 0x{endereco:08x}')


class _MemoriaComIteradores(MemoriaDeclarada):
    """Keep the two existing Core scalar attributes and their raw slots coherent."""
    def __init__(self, original, mundo):
        super().__init__([(a, view) for a, _, view in original.segmentos], original.regioes)
        self.mundo = mundo
        if (super().u32(0x51b844) != mundo.grupo_em_iteracao
                or super().u16(0x51b848) != mundo.unidade_em_iteracao):
            raise ValueError('Core iterator attributes and inherited AI slots must initially agree')

    def u32(self, endereco, valor=None):
        resultado = super().u32(endereco, valor)
        if (endereco & 0xffffffff) == 0x51b844:
            if valor is None and resultado != self.mundo.grupo_em_iteracao:
                raise ValueError('Core group iterator diverged from its live mapped slot')
            if valor is not None:
                self.mundo.grupo_em_iteracao = resultado
        return resultado

    def u16(self, endereco, valor=None):
        resultado = super().u16(endereco, valor)
        if (endereco & 0xffffffff) == 0x51b848:
            if valor is None and resultado != self.mundo.unidade_em_iteracao:
                raise ValueError('Core unit iterator diverged from its live mapped slot')
            if valor is not None:
                self.mundo.unidade_em_iteracao = resultado
        return resultado


class ReinicioIACompartilhado:
    """Callable IaReset provider for one actual Core/economy/mission state.

    The caller creates all state and the original-address registry. This
    constructor never rebinds/copies a world/player/resource/group allocation.
    ``pesquisa64`` is optional only until an actual research call reaches it.
    """
    def __init__(self, memoria, mundo, mercado, missao_u8, *, pesquisa64=None):
        if not isinstance(memoria, MemoriaDeclarada) or not isinstance(mundo, MundoUnidades):
            raise ValueError('Expected declared memory and the actual Core world')
        if not isinstance(mercado, Mercado) or not isinstance(mercado.economia, Economia):
            raise ValueError('Expected the actual Mercado and its shared Economia')
        faixas = sorted((a, b) for a, b, _ in memoria.segmentos)
        if any(b > c for (_, b), (c, _) in zip(faixas, faixas[1:])):
            raise ValueError('Mapped segments must not overlap or hide shadow allocations')
        for endereco, tamanho, buffer, nome in (
            (memoria.u32(UNIDADES), 220800, mundo.unidades, 'Core units'),
            (memoria.u32(JOGADORES), 80, mercado.jogadores, 'Live player table'),
            (0x49a0c8, 276000, mundo.estruturas, 'Core structures'),
            (GRUPOS, 3200, mundo.grupos, 'Core AI groups'),
            (0x4e2ea8, 128, mercado.economia.memoria, 'Shared resources'),
            (0x496fe4, 1, missao_u8, 'Mission number')):
            _alias(memoria, endereco, tamanho, buffer, nome)
        if pesquisa64 is not None:
            _alias(memoria, 0x5080f4, 64, pesquisa64, 'Research state')
        self.memoria = _MemoriaComIteradores(memoria, mundo)
        self.mundo, self.mercado, self.missao, self.pesquisa = mundo, mercado, missao_u8, pesquisa64
        self.chamadas = []

    def __call__(self):
        return reiniciar_ia(self.memoria, self)

    def _anotar(self, nome, sitio, *args):
        self.chamadas.append((nome, sitio, tuple(args)))

    def _economia(self, nome, simbolo, sitio, *args):
        caminho = ROOT / 'pesquisas-paralelas/economia/consultas_reinicio_economia.py'
        if not caminho.is_file():
            raise DependenciaIA(nome, sitio)
        modulo = importlib.import_module('consultas_reinicio_economia')
        if Path(modulo.__file__).resolve() != caminho.resolve():
            raise ImportError('Foreign economy reset-query module is already bound')
        return getattr(modulo, simbolo)(*args)

    def PlayerGetType(self, jogador, *, sitio):
        self._anotar('PlayerGetType', sitio, jogador)
        return Mercado.tipo_jogador(self.mercado, jogador)

    def EnginEstVivant(self, unidade, *, sitio):
        self._anotar('EnginEstVivant', sitio, unidade)
        return MundoUnidades.viva(self.mundo, unidade)

    def EnginGetType(self, unidade, *, sitio):
        self._anotar('EnginGetType', sitio, unidade)
        return tipo_unidade(self.mundo, unidade)

    def TypeEnginEstMonstre(self, tipo, *, sitio):
        self._anotar('TypeEnginEstMonstre', sitio, tipo)
        return tipo_unidade_monstro(tipo)

    def MissionGetNum(self, *, sitio):
        self._anotar('MissionGetNum', sitio)
        return numero_missao(self.missao)

    def GetRessource(self, jogador, *, sitio):
        self._anotar('GetRessource', sitio, jogador)
        return Economia.consultar(self.mercado.economia, jogador)

    def BatimentExiste(self, estrutura, *, sitio):
        self._anotar('BatimentExiste', sitio, estrutura)
        return existe_estrutura(self.mundo.estruturas, estrutura)

    def BatimentGetPlayer(self, estrutura, *, sitio):
        self._anotar('BatimentGetPlayer', sitio, estrutura)
        return batiment_get_player(self.mundo.estruturas, estrutura)

    def BatimentGetType(self, estrutura, *, sitio):
        self._anotar('BatimentGetType', sitio, estrutura)
        return self._economia('BatimentGetType', 'tipo_estrutura', sitio, self.mundo.estruturas, estrutura)

    def RechercheGetNiveau(self, jogador, ramo, *, sitio):
        self._anotar('RechercheGetNiveau', sitio, jogador, ramo)
        if self.pesquisa is None:
            raise DependenciaIA('RechercheGetNiveau', sitio)
        return self._economia('RechercheGetNiveau', 'nivel_pesquisa', sitio, self.pesquisa, jogador, ramo)

    def RechercheSetBranche(self, jogador, ramo, *, sitio):
        self._anotar('RechercheSetBranche', sitio, jogador, ramo)
        if self.pesquisa is None:
            raise DependenciaIA('RechercheSetBranche', sitio)
        return self._economia('RechercheSetBranche', 'definir_ramo_pesquisa', sitio, self.pesquisa, jogador, ramo)

    def EnginGetEtat(self, unidade, *, sitio):
        self._anotar('EnginGetEtat', sitio, unidade)
        raise DependenciaIA('EnginGetEtat', sitio)

    def EnginSetPlayer(self, unidade, jogador, *, sitio):
        self._anotar('EnginSetPlayer', sitio, unidade, jogador)
        raise DependenciaIA('EnginSetPlayer', sitio)
