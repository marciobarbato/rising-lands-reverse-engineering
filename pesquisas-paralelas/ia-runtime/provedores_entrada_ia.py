"""Committed owners wired as the named providers of ``entrada_ordens_ia`` over one live memory.

Nothing here is defaulted. Each name is bound to the owning front's committed translation, imported (never
copied or edited), over the same memory object ``m`` (``u8/u16/u32`` and ``vista``, e.g. Core's
``memoria_quadro_core.MemoriaQuadro`` or the composition's map):

- Core ``selecao_ordens.SelecaoOrdens``: SelectionEngin, DeSelectionGroupe, BatimentDeselectionner,
  BatimentSelection, EnginAddSelection, EnginAsk, SetDeplaceEnginSelect, SetAttaqueEnginSelect,
  SetConstruitBatimentSelect, SetRecolteEnginSelect, SetTransporteEnginSelect, EnginSelectionnable (its SetAttaqueEngin through
  Combat's ``ataque_vivo.definir_ataque``, as Core's own validator binds it);
- Core ``construcao_core.ConstrucaoCore`` (when present on the import path): BatimentPosable;
- Core ``entrada_estruturas.EntradaEstruturas`` (when present on the import path): EnginSelectPeutEntrer;
- Core ``chamadas_quadro_core.iniciar_zonas_jogo``: InitGameZone;
- Economy ``ordens_economia.OrdensEconomia`` (its Core callees through ``provedor_core``):
  EnginTravailSelectionne, TestRessource, SetMineEnginSelect, SetDepotEnginSelect, SetRamasseEnginSelect;
- Economy ``extracao.RecursosTerreno`` over the live mine table 0x509954: MineGetIndice, MineGetCapacite;
- Combat ``alvos_alcance.ocupa_celula`` over the live unit record: EnginOccupeCase;
- this front's ``entrada_quadro_ia.proximas_gotas``: NextGouttes;
- the caller's declared input answers (``janelas``): GetAsyncKeyState, GetCursorPos; its allocator
  (``alocar``) for MemAlloc's GlobalAlloc/GlobalLock; and the sound-library boundary (``som``) for PlaySnd_PostSound/PlaySnd_StopSound.

Not provided (named dependencies, raised at their original call): SetDechargeCaveEnginSelect,
InitRecruteTroupe, BatimentInitAttaqueSelect, BatimentPeutAttaquer (Combat), SacGetCapacite, MiniMapSetPos
(MiniMapRecentre), and BatimentPosable/EnginSelectPeutEntrer while Core's ``construcao_core``/``entrada_estruturas``
are not importable.
"""
import sys

from ambiente_ia_runtime import ROOT
from entrada_ordens_ia import M32, PASSO, POOL, Provedores, REG7

for _pasta in ('pesquisas-paralelas/economia', 'pesquisas-paralelas/combate'):
    if str(ROOT / _pasta) not in sys.path:
        sys.path.append(str(ROOT / _pasta))

CORE = ('SelectionEngin', 'DeSelectionGroupe', 'BatimentDeselectionner', 'BatimentSelection', 'EnginAddSelection',
        'EnginAsk', 'SetDeplaceEnginSelect', 'SetAttaqueEnginSelect', 'SetConstruitBatimentSelect',
        'SetRecolteEnginSelect', 'SetTransporteEnginSelect', 'EnginSelectionnable')
ECONOMIA = ('EnginTravailSelectionne', 'SetMineEnginSelect', 'SetDepotEnginSelect', 'SetRamasseEnginSelect')
ESP_CHAMADA = 0x2007e00               # nominal ESP handed to Economy (its Core callees ignore it)


def _modulo_economia(nome):
    """Economy's module ``nome`` imported with Economy's own siblings: ``extracao`` imports ``construcoes`` and
    ``economia`` by bare name, and Graphics has a different ``construcoes`` that may already be loaded. The
    sibling entries are swapped in for the import only and the previous ones restored."""
    import importlib
    if nome in _ECONOMIA_CARREGADOS:
        return _ECONOMIA_CARREGADOS[nome]
    pasta = str(ROOT / 'pesquisas-paralelas/economia')
    irmaos = ('construcoes', 'economia', nome)
    anteriores = {k: sys.modules.pop(k) for k in irmaos if k in sys.modules}
    sys.path.insert(0, pasta)
    try:
        modulo = importlib.import_module(nome)
    finally:
        sys.path.remove(pasta)
        for k in irmaos:
            sys.modules.pop(k, None)
        sys.modules.update(anteriores)
    _ECONOMIA_CARREGADOS[nome] = modulo
    return modulo


_ECONOMIA_CARREGADOS = {}


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


def entrada_estruturas(m, *, som=None, bonus=None, externo=None):
    """Core's ``entrada_estruturas.EntradaEstruturas`` over ``m``, or None when it is not importable yet (it is on
    ``feat/re-core``; a run may add a read-only extraction of it to the import path, recorded by the caller)."""
    try:
        from entrada_estruturas import EntradaEstruturas
    except ImportError:
        return None
    return EntradaEstruturas(m, externo=externo, som=som, bonus=bonus)


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

    import inspect
    som_sitio = 'chamada' in inspect.signature(som).parameters

    def externo(nome, sitio, regs):
        if nome == 'PlaySnd_PostSound' and som_sitio:
            # The boundary with its declared call address (``sitio``) and pushed words.
            return dict(EAX=som('PlaySnd_PostSound', {k: regs[k] & M32 for k in ('EAX', 'EDX', 'EBX', 'ECX')},
                                list(regs['pilha']), chamada=sitio))
        f = funcoes.get(nome)
        if f is None:
            raise DependenciaIA(nome, sitio)
        return f(regs)

    def calcul(regs):
        return economia.calcul_construire_batiment(dict({k: (regs.get(k) or 0) & M32 for k in REG7},
                                                        ESP=ESP_CHAMADA))
    return ConstrucaoEntrada(m, externo, calcul)


def provedores_vivos(m, *, janelas, som, alocar=None, construcao=None, estruturas=None, donos=None):
    """``Provedores`` for ``entrada_ordens_ia.Entrada`` over ``m``.

    ``janelas.tecla(vk, sitio) -> u16 answer`` (``sitio``: the poll's return address) and ``janelas.cursor() -> (x, y)`` are the declared input answers;
    ``som(nome, registradores, pilha) -> EAX`` is the sound-library boundary (also handed to Core's EnginAsk);
    ``alocar(flags, tamanho) -> pointer`` binds MemAlloc's GlobalAlloc+GlobalLock (InitInputPlayer only); ``construcao`` (default: Core's
    ``construcao_core`` when importable) provides BatimentPosable; ``estruturas`` (default: Core's
    ``entrada_estruturas`` when importable) provides EnginSelectPeutEntrer (mode 3)."""
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
        RecursosTerreno = _modulo_economia('extracao').RecursosTerreno
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
    ee = entrada_estruturas(m, som=som) if estruturas is None else estruturas
    if ee is not None:
        funcoes['EnginSelectPeutEntrer'] = lambda regs: ee.chamar(
            'EnginSelectPeutEntrer', {k: regs.get(k, 0) & M32 for k in REG7})
    def recrutamento():
        """Economy's ``recrutamento.Recrutamento`` over snapshots of the bytes its queries read (selection
        0x495be0, unit types 0x4965ae, spell types 0x497174, the unit pool, the structure pool): read-only."""
        modulo = _modulo_economia('recrutamento')
        mundo = modulo.EconomiaConstrucoes(estruturas=bytes(m.vista(0x49a0c8, 276000)))
        return modulo.Recrutamento(mundo, selecoes=bytes(m.vista(0x495be0, 8)), tipos_unidades=bytes(m.vista(0x4965ae, 1300)),
                            tipos_sortilegios=bytes(m.vista(0x497174, 230)),
                            unidades=bytes(m.vista(m.u32(POOL), 220800)))
    from entrada_ordens_ia import batiment_peut_attaquer_prefixo
    funcoes['BatimentPeutAttaquer'] = lambda regs: batiment_peut_attaquer_prefixo(
        m, {k: regs.get(k, 0) & M32 for k in REG7})
    funcoes['GetStatusRecrute'] = lambda tipo, jogador: recrutamento().status(tipo, jogador)
    if donos is not None:
        # The M3 owners (``DonosM3``): group selection and view (tags 0xb/0xc, the group key), the minimap
        # press, entry into a structure (tag 0x10 sub 3) and the colonist release (tag 0x21).
        for nome in ('SauveSelectionGroupe', 'RestaureSelectionGroupe', 'EnginGetCentreGroupe',
                     'SetEnginSelectRentreBatiment', 'BatimentRetireColon'):
            funcoes[nome] = donos.registros(nome)
        funcoes['EnginSelectPeutEntrer'] = donos.registros('EnginSelectPeutEntrer')
        # Tag 17 (0x45f1a9): Economy's InitRecruteTroupe (AL unit type, DL player), its callees through DonosM3.
        funcoes['InitRecruteTroupe'] = lambda regs: {k: v for k, v in donos.caverna.chamar(
            'InitRecruteTroupe', dict({k: regs.get(k, 0) & M32 for k in REG7}, ESP=0)).items() if k != 'ESP'}
        funcoes['MiniMapSetPos'] = lambda x, y: donos.visao.chamar(
            'MiniMapSetPos', dict(dict.fromkeys(REG7, 0), EAX=x & M32, EDX=y & M32, EBX=0, ECX=1))
    if alocar is not None:
        funcoes['GlobalAlloc'] = lambda flags, tamanho: alocar(flags, tamanho)
    return Provedores(funcoes)


class DonosM3:
    """The committed M3 owners past frame 220 over one live memory, wired to each other (one instance each):

    - Core ``entrada_estruturas.EntradaEstruturas`` (``ee``): Bag primitives, structure entry and lodging, unit
      state 13's body, SetEnginSelectRentreBatiment, BatimentRetireColon, and the Core routines Economy calls
      (``ROTINAS_ECONOMIA`` through ``provedor_entrada``);
    - Economy ``caverna_recrutamento.CavernaRecrutamento`` (``caverna``): the type-3 body, BatimentHabitable,
      InitBatimentPlayer/InitBatimentNeutre, ...;
    - Economy ``ciclo_trabalho.CicloTrabalho`` (``ciclo``): CalculWorkEngin (unit state 5), BatimentLogeEngin,
      BatimentAjouteMatiere, the mine/field leaves;
    - Core ``visao_grupos.VisaoGrupos`` (``visao``): BatimentIllumine/BatimentDecouvre, the group selection,
      MiniMapSetPos/MiniMapRecentre, CalculPosition and RechercheDecalageSortie.

    Every named dependency one of them raises goes through ``externo(nome, chamada, regs)``: the routine of the
    module that owns it, ``bonus(jogador, tipo, seletor)`` for BonusGetValEngin, ``mensagem_unidade(regs,
    chamada) -> regs`` (this front's iagUnitSendMessage) when given; any other name raises
    ``DependenciaIA`` at its original call (never defaulted)."""

    def __init__(self, m, *, som, bonus=None, mensagem_unidade=None):
        from entrada_estruturas import EntradaEstruturas, ROTINAS_ECONOMIA, provedor_entrada
        from visao_grupos import VisaoGrupos, provedor_saida
        caverna_recrutamento = _modulo_economia('caverna_recrutamento')
        ciclo_trabalho = _modulo_economia('ciclo_trabalho')
        self.m, self.bonus, self.mensagem_unidade, self.som = m, bonus, mensagem_unidade, som
        self.ee = EntradaEstruturas(m, externo=self.externo, som=som, bonus=bonus)
        # (bonus None: BonusGetValEngin stays a named dependency)
        self.visao = VisaoGrupos(m, som=som)
        self.caverna = caverna_recrutamento.CavernaRecrutamento(m, externo=self.externo)
        self.ciclo = ciclo_trabalho.CicloTrabalho(m, externo=self.externo)
        self._core = provedor_entrada(self.ee)
        self._saida = provedor_saida(self.visao)
        self._caverna = caverna_recrutamento.provedor_caverna(self.caverna)
        self.nomes_core = frozenset(ROTINAS_ECONOMIA)
        self.nomes_caverna = frozenset(caverna_recrutamento.ROTINAS)
        self.nomes_ciclo = frozenset(ciclo_trabalho.ROTINAS)
        self.chamadas = []                       # (name, original call) of every cross-module call, in order

    def externo(self, nome, chamada, regs):
        from reinicio_ia import DependenciaIA
        self.chamadas.append((nome, chamada))
        if nome in self.nomes_core:
            return self._core(nome, chamada, regs)
        if nome in ('CalculPosition', 'RechercheDecalageSortie'):
            return self._saida(nome, chamada, regs)
        if nome in self.nomes_caverna:
            return self._caverna(nome, chamada, regs)
        if nome in self.nomes_ciclo:
            entrada = {k: regs.get(k, 0) & M32 for k in REG7}
            entrada['ESP'] = 0
            saida = getattr(self.ciclo, '_' + nome)(entrada)
            return {k: v for k, v in saida.items() if k != 'ESP'}
        if nome == 'BonusGetValEngin' and self.bonus is not None:
            return dict(EAX=self.bonus(regs['EAX'] & 0xff, regs['EBX'] & 0xff, regs['EDX'] & 0xff))
        if nome in ('PlaySnd_PostSound', 'PlaySnd_StopSound') and self.som is not None:
            # The sound-library boundary, with the caller's declared call address and pushed words.
            pilha = list(regs.get('_pilha') or ())
            import inspect
            argumentos = {'chamada': chamada} if 'chamada' in inspect.signature(self.som).parameters else {}
            return dict(EAX=self.som(nome, {k: regs.get(k, 0) & M32 for k in ('EAX', 'EDX', 'EBX', 'ECX')}, pilha,
                                     **argumentos) & M32)
        if nome == 'iagUnitSendMessage' and self.mensagem_unidade is not None:
            return self.mensagem_unidade(regs, chamada)
        raise DependenciaIA(nome, chamada)

    def registros(self, nome):
        """``f(regs) -> regs`` running Core's/visao's routine ``nome`` (the ``Provedores`` register shape)."""
        alvo = self.visao if nome in ('SauveSelectionGroupe', 'RestaureSelectionGroupe', 'EnginGetCentreGroupe',
                                      'MiniMapSetPos', 'MiniMapRecentre', 'BatimentIllumine',
                                      'BatimentDecouvre') else self.ee
        return lambda regs: alvo.chamar(nome, {k: regs.get(k, 0) & M32 for k in REG7})
