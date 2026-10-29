"""Committed owners wired as the named providers of ``entrada_ordens_ia`` over one live memory.

Nothing here is defaulted. Each name is bound to the owning front's committed translation, imported (never
copied or edited), over the same memory object ``m`` (``u8/u16/u32`` and ``vista``, e.g. Core's
``memoria_quadro_core.MemoriaQuadro`` or the composition's map):

- Core ``selecao_ordens.SelecaoOrdens``: SelectionEngin, DeSelectionGroupe, BatimentDeselectionner,
  BatimentSelection, EnginAddSelection, EnginAsk, SetDeplaceEnginSelect, SetAttaqueEnginSelect,
  SetConstruitBatimentSelect, SetRecolteEnginSelect, SetTransporteEnginSelect (its SetAttaqueEngin through
  Combat's ``ataque_vivo.definir_ataque``, as Core's own validator binds it);
- Core ``construcao_core.ConstrucaoCore`` (when present on the import path): BatimentPosable;
- Core ``chamadas_quadro_core.iniciar_zonas_jogo``: InitGameZone;
- Economy ``ordens_economia.OrdensEconomia`` (its Core callees through ``provedor_core``):
  EnginTravailSelectionne, TestRessource, SetMineEnginSelect, SetDepotEnginSelect, SetRamasseEnginSelect;
- Economy ``extracao.RecursosTerreno`` over the live mine table 0x509954: MineGetIndice, MineGetCapacite;
- Combat ``alvos_alcance.ocupa_celula`` over the live unit record: EnginOccupeCase;
- this front's ``entrada_quadro_ia.proximas_gotas``: NextGouttes;
- the caller's declared input answers (``janelas``): GetAsyncKeyState, GetCursorPos; its allocator
  (``alocar``) for MemAlloc's GlobalAlloc/GlobalLock; and the sound-library boundary (``som``) for PlaySnd_PostSound/PlaySnd_StopSound.

Not provided (named dependencies, raised at their original call): SetDechargeCaveEnginSelect,
InitRecruteTroupe, BatimentInitAttaqueSelect, SacGetCapacite, MiniMapSetPos (MiniMapRecentre), and
BatimentPosable while Core's ``construcao_core`` is not importable.
"""
import sys

from ambiente_ia_runtime import ROOT
from entrada_ordens_ia import M32, PASSO, POOL, Provedores, REG7

for _pasta in ('pesquisas-paralelas/economia', 'pesquisas-paralelas/combate'):
    if str(ROOT / _pasta) not in sys.path:
        sys.path.append(str(ROOT / _pasta))

CORE = ('SelectionEngin', 'DeSelectionGroupe', 'BatimentDeselectionner', 'BatimentSelection', 'EnginAddSelection',
        'EnginAsk', 'SetDeplaceEnginSelect', 'SetAttaqueEnginSelect', 'SetConstruitBatimentSelect',
        'SetRecolteEnginSelect', 'SetTransporteEnginSelect')
ECONOMIA = ('EnginTravailSelectionne', 'SetMineEnginSelect', 'SetDepotEnginSelect', 'SetRamasseEnginSelect')
ESP_CHAMADA = 0x2007e00               # nominal ESP handed to Economy (its Core callees ignore it)


def _ataque_combate(m, core):
    """SetAttaqueEngin through Combat's committed translation (Core's validator binding, ``validar_selecao_ordens``)."""
    from alvos_alcance import ordem_ja_definida
    from ataque_vivo import definir_ataque

    class Registros:
        def __getitem__(self, i):
            return m.vista(core._rec(i), 276)

    def provedor(unidade, modo, referencia):
        rec = core._rec(unidade)
        mesma = ordem_ja_definida(m.vista(rec, 276), modo, referencia)
        definir_ataque(Registros(), unidade, modo, referencia, lambda i: core.reset_ordre(dict(EAX=i)))
        return dict(EAX=1 if mesma else m.u8(rec + 1), EDX=rec)
    return provedor


def construcao_core(m, bonus=None):
    """Core's ConstrucaoCore over ``m``, or None when ``construcao_core`` is not importable yet."""
    try:
        from construcao_core import ConstrucaoCore
    except ImportError:
        return None
    return ConstrucaoCore(m, bonus=bonus)


class _MundoMinimapa:
    """Core's live world (``mundo_vivo``) for Core's ``minimapa_estruturas.modificar_minimapa_estrutura``, with the
    structure pool handed as an immutable snapshot taken at the call (the routine reads it and writes none of it;
    a write would raise). Every other attribute is the live world's."""

    def __init__(self, mundo, m):
        self._mundo = mundo
        self.estruturas = bytes(m.vista(0x49a0c8, 276000))

    def __getattr__(self, nome):
        return getattr(self._mundo, nome)


def construcao_viva(m, *, som, bonus, provedores_nucleo=None):
    """``construcao_entrada_ia.ConstrucaoEntrada`` over ``m`` with the committed owners:
    - Economy ``ordens_economia.OrdensEconomia.calcul_construire_batiment`` with Core's ``selecao_ordens`` and
      ``construcao_core`` callees (``provedor_core(..., provedor_construcao(...))``; without ``construcao_core`` the
      walk stops at DeplaceEngin, a named dependency);
    - Core ``chamadas_quadro_core.provedores_core`` (or ``provedores_nucleo``, the caller's same-named dict):
      RotateEngin, SetDeplaceEngin, CalculDirCase, Random, TerrainEstDecouvert; Core ``selecao_ordens``:
      EnginGetVolume, BatimentGetVolume; Core ``minimapa_estruturas``: BatimentModifyMap over the live world;
    - Combat ``projeteis.PoolProjeteis.iniciar`` over the live pool [0x5080f0]: ProjectileInit;
    - ``som(nome, registradores, pilha) -> EAX``: the sound-library boundary (PlaySnd_PostSound).
    ``bonus(jogador, tipo, seletor) -> value`` is Economy's BonusGetValEngin (Core's CalculFatigue in DeplaceEngin).
    Not provided (named dependencies): BatimentHabitable, SetMurAllentour."""
    from chamadas_quadro_core import provedores_core
    from construcao_entrada_ia import ConstrucaoEntrada
    from ordens_economia import OrdensEconomia, provedor_core
    from projeteis import PoolProjeteis
    from reinicio_ia import DependenciaIA
    from selecao_ordens import SelecaoOrdens
    core = SelecaoOrdens(m, som=som)
    nucleo = provedores_nucleo if provedores_nucleo is not None else provedores_core(m, bonus)
    cc = construcao_core(m, bonus=bonus)
    outros = None
    if cc is not None:
        from construcao_core import provedor_construcao
        outros = provedor_construcao(cc)
    economia = OrdensEconomia(m, externo=provedor_core(core, outros))
    estado = {}

    def mundo():
        if 'mundo' not in estado:
            from mundo_vivo import mundo_vivo
            from solucionador_vivo import SolucionadorCaminhosVivo
            estado['mundo'] = mundo_vivo(m, SolucionadorCaminhosVivo(m))
        return estado['mundo']

    def modificar_mapa(r):
        from minimapa_estruturas import modificar_minimapa_estrutura
        modificar_minimapa_estrutura(_MundoMinimapa(mundo(), m), r['EAX'] & 0xffff, r['EDX'] & 0xff)
        return dict(EAX=None)

    def projetil(r):
        PoolProjeteis(memoria=m.vista(m.u32(0x5080f0), 5600)).iniciar(
            r['EAX'] & 0xff, r['EDX'] & 0xffff, r['EBX'] & 0xffff, r['ECX'] & 0xff, *r['pilha'])
        return dict(EAX=None, EBX=None, ECX=None, EDX=None)

    funcoes = {
        'RotateEngin': lambda r: dict(EAX=nucleo['RotateEngin'](sitio=0, unidade=r['EAX'] & 0xffff)),
        'SetDeplaceEngin': lambda r: dict(EAX=nucleo['SetDeplaceEngin'](sitio=0, unidade=r['EAX'] & 0xffff,
                                                                          destino=r['EDX'] & 0xffff)),
        'CalculDirCase': lambda r: dict(EAX=nucleo['CalculDirCase'](sitio=0, caso=r['EAX'] & 0xffff,
                                                                      direcao=r['EDX'] & 0xff)),
        'Random': lambda r: dict(EAX=nucleo['Random'](sitio=0)),
        'TerrainEstDecouvert': lambda r: dict(EAX=nucleo['TerrainEstDecouvert'](sitio=0, caso=r['EAX'],
                                                                                  jogador=r['EDX'])),
        'EnginGetVolume': lambda r: dict(EAX=core._volume_unidade(r['EAX'] & 0xffff)),
        'BatimentGetVolume': lambda r: dict(EAX=core._volume_estrutura(r['EAX'] & 0xffff)),
        'BatimentModifyMap': modificar_mapa,
        'ProjectileInit': projetil,
        'PlaySnd_PostSound': lambda r: dict(EAX=som('PlaySnd_PostSound', {k: r[k] & M32 for k in
                                                                          ('EAX', 'EDX', 'EBX', 'ECX')},
                                                    list(r['pilha']))),
    }

    def externo(nome, sitio, regs):
        f = funcoes.get(nome)
        if f is None:
            raise DependenciaIA(nome, sitio)
        return f(regs)

    def calcul(regs):
        return economia.calcul_construire_batiment(dict({k: (regs.get(k) or 0) & M32 for k in REG7},
                                                        ESP=ESP_CHAMADA))
    return ConstrucaoEntrada(m, externo, calcul)


def provedores_vivos(m, *, janelas, som, alocar=None, construcao=None):
    """``Provedores`` for ``entrada_ordens_ia.Entrada`` over ``m``.

    ``janelas.tecla(vk, sitio) -> u16 answer`` (``sitio``: the poll's return address) and ``janelas.cursor() -> (x, y)`` are the declared input answers;
    ``som(nome, registradores, pilha) -> EAX`` is the sound-library boundary (also handed to Core's EnginAsk);
    ``alocar(flags, tamanho) -> pointer`` binds MemAlloc's GlobalAlloc+GlobalLock (InitInputPlayer only); ``construcao`` (default: Core's
    ``construcao_core`` when importable) provides BatimentPosable."""
    from chamadas_quadro_core import iniciar_zonas_jogo
    from entrada_quadro_ia import proximas_gotas
    from ordens_economia import OrdensEconomia, provedor_core
    from selecao_ordens import SelecaoOrdens
    from alvos_alcance import ocupa_celula
    core = SelecaoOrdens(m, som=som)
    core.definir_ataque = _ataque_combate(m, core)
    economia = OrdensEconomia(m, externo=provedor_core(core))
    construcao = construcao_core(m) if construcao is None else construcao

    def nucleo(nome):
        def chamar(regs):
            return core.chamar(nome, {k: regs.get(k, 0) & M32 for k in REG7})
        return chamar

    def economia_regs(nome):
        def chamar(regs):
            return economia.chamar(nome, dict({k: regs.get(k, 0) & M32 for k in REG7}, ESP=ESP_CHAMADA))
        return chamar

    def teste(regs, pilha):
        return economia.chamar('TestRessource', dict({k: regs.get(k, 0) & M32 for k in REG7}, ESP=ESP_CHAMADA),
                               pilha)

    def minas():
        from extracao import RecursosTerreno
        r = RecursosTerreno.__new__(RecursosTerreno)
        r.minas = m.vista(0x509954, 80)
        return r

    funcoes = {nome: nucleo(nome) for nome in CORE}
    funcoes.update({nome: economia_regs(nome) for nome in ECONOMIA})
    funcoes.update(
        TestRessource=teste,
        GetAsyncKeyState=lambda vk, local: janelas.tecla(vk, local),
        GetCursorPos=lambda: janelas.cursor(),
        EnginOccupeCase=lambda unidade, celula, filtro: int(ocupa_celula(
            m.vista((m.u32(POOL) + unidade * PASSO) & M32, PASSO), celula, filtro)),
        MineGetIndice=lambda celula: minas().indice_mina(celula),
        MineGetCapacite=lambda indice: minas().capacidade_mina(indice),
        NextGouttes=lambda: proximas_gotas(m),
        InitGameZone=lambda eax, edx: iniciar_zonas_jogo(m, eax, edx),
        PlaySnd_StopSound=lambda regs: som('PlaySnd_StopSound', {k: regs[k] for k in ('EAX', 'EDX', 'EBX', 'ECX')},
                                           []),
    )
    if construcao is not None:
        funcoes['BatimentPosable'] = lambda regs: construcao.chamar(
            'BatimentPosable', {k: regs.get(k, 0) & M32 for k in REG7})
    if alocar is not None:
        funcoes['GlobalAlloc'] = lambda flags, tamanho: alocar(flags, tamanho)
    return Provedores(funcoes)
