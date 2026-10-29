"""Chained Python composition of MONDE01 (a) load_tail -> (b) between_frames -> (c) frame1.

One Missions ``MapaMemoriaM1`` is built from a scenario's MissionLoad final state
and carried through all three phases. It is never restarted from an original
state. Two scenarios are supported:
- ``exibicao``: the M2 reference since round 4. The display path is executed,
  the viewport is 25x17 and the real window loop runs.
- ``v1``: historical; display routines are declared boundaries.

Every routine is an integrated provider, called in original order:
- this front: the frame skeleton, the dispatcher loops, CalculNextReflect,
  AvanceMonstre, ProcessInputGame, MessageBoxCalcul, InputGame (edge scroll and
  map hover), InputSend, CalculIconeAction, MenuInit, EnginNextEtape and
  BatimentNextEtape;
- Core ``chamadas_quadro_core`` (now including SetClipping, InitGameZone with
  MouseSetZone, and NextAnim*) and the live task VM ``MaquinaTarefasViva``
  (iaSolver);
- Economy ``quadro_economia``, ``BonusUnidades`` and ``Mercado``;
- Combat ``MaquinaProjeteis``, ``encontrar_alvo``, ``aliados`` and ``ocupa_celula``;
- Missions ``fim_missao`` and ``influencia_missao``.

**Crossings.** A routine without a Python provider is crossed by ``Travessias``,
exactly and only when the Python state at the call equals the original state at
that call's entry (all blocks). The original's own effect of that one call (its
changed, allocated and released blocks, its return EAX, and the bindings and
boundaries it recorded) is then applied. Crossings are keyed by phase, routine,
call-return site and occurrence, and every one is reported. Two kinds exist:
- Graphics' display routines: RestoreAll and AffGame, plus, on the display path,
  MenuInit's DDLockSurface, DeleteBank, FilledBox, DDUnlockSurface and DDFlipPage.
- A Core provider that raises ``DependenciaRamoCore``, reported with its own
  address and then crossed.

A state that differs at a crossing or a checkpoint is a divergence, and the phase
stops there.
"""
import bisect
import struct
import sys

from ambiente_ia_runtime import CD, ROOT
from composicao_quadro1_ia import Registro as RegistroBase
from entrada_quadro_ia import calcular_icone_acao, entrada_jogo, enviar_entrada, iniciar_menu
from laco_despachantes import calcular_proxima_etapa_estruturas, calcular_proxima_etapa_unidades
from proxima_etapa_quadro import proxima_etapa_estrutura, proxima_etapa_unidade, tabelas_imagem
from quadro_calcul_game import calcular_quadro
from reinicio_ia import DependenciaIA
from rotinas_quadro_ia import TABELA_COMANDOS, avancar_monstros, calcular_caixa_mensagens, processar_entrada
from simbolos_ia import ler_rul
from tarefas_ia import MaquinaTarefasViva

for _pasta in ('pesquisas-paralelas/combate', 'pesquisas-paralelas/economia'):
    if str(ROOT / _pasta) not in sys.path:
        sys.path.append(str(ROOT / _pasta))
import chamadas_quadro_core as core  # noqa: E402
from fundacoes_quadro import zerar_contadores_carga  # noqa: E402
from fim_missao import consultas_publicadas, evento_em_curso, testar_fim_missao  # noqa: E402
import quadro_economia as economia_quadro  # noqa: E402
from alvos_alcance import aliados, encontrar_alvo, ocupa_celula  # noqa: E402
from maquina_projeteis import MaquinaProjeteis  # noqa: E402
from projeteis import PoolProjeteis  # noqa: E402

GRAFICOS_EXIBICAO = ('RestoreAll', 'AffGame', 'DDLockSurface', 'DeleteBank', 'FilledBox', 'DDUnlockSurface',
                     'DDFlipPage')
NUCLEO = ('SetClipping', 'InitGameZone', 'NextAnimTerrain', 'NextAnimVeget')
PONTOS = ('MenuInit', 'InputGame', 'InputSend', 'ProcessInputGame', 'MessageBoxCalcul', 'CalculIconeAction',
          'ProjectileCalcul', 'CalculEnginNextEtape', 'EnginNextEtape', 'CalculBatimentNextEtape', 'RechercheCalcul',
          'PlayerInitAllianceCompteur', 'SetUpdateChamp', 'UpdateChamp', 'CalculMatiere', 'CalculCompteurMarche',
          'CalculCompteurProposition', 'PlayerAttaqueCalculSympa', 'TestFinDeMission') + NUCLEO
DONOS = dict({n: 'graphics' for n in GRAFICOS_EXIBICAO}, **{n: 'core' for n in NUCLEO})


class Divergencia(RuntimeError):
    def __init__(self, fase, rotina, chave, blocos):
        self.fase, self.rotina, self.chave, self.blocos = fase, rotina, chave, blocos
        super().__init__(f'{fase}: state differs from the original at {rotina} {chave}: {blocos[:6]}')


class Registro(RegistroBase):
    def fronteira(self, rotina, retorno, chamador, registros, guardas=None, palavras=None, declarado=None,
                  limpeza=0, topo=None):
        super().fronteira(rotina, retorno, chamador, registros, guardas, None)
        e = self.fronteiras[-1]
        e.update(declared_eax=declarado, stack_cleanup=limpeza, top_callee=topo or rotina)
        if palavras is not None:
            e['stack_words'] = [None if p is None else hex(p) for p in palavras]


class JanelasDeclaradas:
    """The capture's named frame inputs: no key pressed, ShowCursor 0, SetCursorPos 1."""
    def tecla(self, vk):
        return 0

    def mostrar_cursor(self, mostrar):
        return 0


class MemoriaMapaRapida:
    """u8/u16/u32/s8/vista/ler over ``MapaMemoriaM1`` with a bisect segment index (25k-block maps).

    List-backed u16 segments (Core grids) are served element-wise, as in ``MemoriaMapaM1``.
    ``reindexar`` must follow any block allocation/release.
    """
    def __init__(self, mapa):
        self.mapa = mapa
        self.reindexar()

    def reindexar(self):
        self.segmentos = list(self.mapa.segmentos)
        self.bases = [s.base for s in self.segmentos]

    def _segmento(self, endereco, tamanho):
        i = bisect.bisect_right(self.bases, endereco) - 1
        if i >= 0:
            s = self.segmentos[i]
            if endereco + tamanho <= s.fim:
                return s
        return self.mapa._segmento(endereco, tamanho)      # the map raises its own error

    def vista(self, endereco, tamanho):
        s = self._segmento(endereco, tamanho)
        if s.tipo != 'bytes':
            raise ValueError(f'{s.dono}: 0x{endereco:08x} is list-backed (no byte view)')
        return s.vista[endereco - s.base:endereco - s.base + tamanho]

    def ler(self, endereco, tamanho):
        s = self._segmento(endereco, tamanho)
        if s.tipo == 'bytes':
            return bytes(s.vista[endereco - s.base:endereco - s.base + tamanho])
        return s.bytes()[endereco - s.base:endereco - s.base + tamanho]

    def _acesso(self, largura, endereco, valor):
        endereco &= 0xffffffff
        s = self._segmento(endereco, largura)
        formato = {1: '<B', 2: '<H', 4: '<I'}[largura]
        o = endereco - s.base
        if s.tipo == 'bytes':
            if valor is None:
                return struct.unpack_from(formato, s.vista, o)[0]
            valor &= (1 << 8 * largura) - 1
            struct.pack_into(formato, s.vista, o, valor)
            return valor
        primeiro, ultimo = o // 2, (o + largura - 1) // 2
        dados = bytearray(b''.join(struct.pack('<H', s.lista[i]) for i in range(primeiro, ultimo + 1)))
        d = o - 2 * primeiro
        if valor is None:
            return struct.unpack_from(formato, dados, d)[0]
        valor &= (1 << 8 * largura) - 1
        struct.pack_into(formato, dados, d, valor)
        for k, i in enumerate(range(primeiro, ultimo + 1)):
            s.lista[i] = struct.unpack_from('<H', dados, 2 * k)[0]
        return valor

    def u8(self, endereco, valor=None):
        return self._acesso(1, endereco, valor)

    def u16(self, endereco, valor=None):
        return self._acesso(2, endereco, valor)

    def u32(self, endereco, valor=None):
        return self._acesso(4, endereco, valor)

    def s8(self, endereco):
        v = self.u8(endereco)
        return v - 0x100 if v & 0x80 else v


class ContextoEncadeado:
    """``modo``: 'cruzamentos' (rounds 3/4: crossings allowed) or 'prova' (round 5: no crossing; Graphics'
    logic-effects provider for RestoreAll/AffGame, display roots not executed, DeleteBank on the arena)."""
    def __init__(self, imagem, cenario, modo='cruzamentos', arena=None, superficie=None):
        self.cenario, self.modo, self.arena, self.superficie = cenario, modo, arena, superficie
        self.raizes_nao_executadas = []
        self.programa = ler_rul((CD / 'INSTALHD/RISING.RUL').read_bytes())
        self.comandos = imagem.table(TABELA_COMANDOS, 40)
        self.estados = imagem.table(0x42c804, 25)
        self.tabelas = tabelas_imagem(imagem)


class Travessias:
    """Original data keyed (phase, routine, call-return site, occurrence): checkpoint hashes and crossing effects."""

    def __init__(self, pontos, retornos, hashes):
        self.pontos, self.retornos, self.hashes = pontos, retornos, hashes
        self.contagem, self.feitas, self.verificados, self.paradas_nucleo = {}, [], [], []

    def comparar(self, fase, rotina, retorno, mapa):
        k = (fase, rotina, retorno)
        n = self.contagem.get(k, 0)
        self.contagem[k] = n + 1
        chave = k + (n,)
        esperado = self.pontos.get(chave)
        if esperado is None:
            return chave, None
        atual = self.hashes(mapa)
        diferentes = sorted(b for b in set(atual) | set(esperado) if atual.get(b) != esperado.get(b))
        self.verificados.append(dict(phase=fase, routine=rotina, caller_return=hex(retorno), occurrence=n,
                                     equal=not diferentes))
        if diferentes:
            raise Divergencia(fase, rotina, chave, diferentes)
        return chave, esperado

    def atravessar(self, fase, rotina, sitio, mapa, mm, registro, motivo, verificado=None):
        chave = verificado or self.comparar(fase, rotina, sitio + 5, mapa)[0]
        if chave not in self.retornos:
            raise DependenciaIA(f'{rotina} ({DONOS.get(rotina)}): no original crossing data', sitio)
        efeito = self.retornos[chave]
        aplicar_efeito(mapa, efeito)
        mm.reindexar()
        registro.vinculos += efeito['bindings']
        registro.fronteiras += efeito['boundaries']
        self.feitas.append(dict(phase=fase, routine=rotina, owner=DONOS.get(rotina), site=hex(sitio),
                                occurrence=chave[3], reason=motivo, state_equal_at_entry=True,
                                bindings=len(efeito['bindings']), boundaries=len(efeito['boundaries']),
                                changed_blocks=sorted(efeito['changed']), released=len(efeito['released']),
                                allocated=sorted(efeito['allocated']), eax=hex(efeito['eax']),
                                changed_bytes=efeito.get('changed_bytes', {})))
        return efeito['eax']


def aplicar_efeito(mapa, efeito):
    """Apply one crossed call's original block changes to the live map (segments in place)."""
    for nome in efeito['released']:
        mapa.remover_bloco(nome)
    for nome, (base, dados) in efeito['allocated'].items():
        mapa.adicionar_bloco(nome, base, bytearray(dados), f'crossed allocation {nome}')
    for nome, (base, dados) in efeito['changed'].items():
        for s in mapa.segmentos:
            if s.bloco != nome:
                continue
            fatia = dados[s.base - base:s.fim - base]
            if s.tipo == 'bytes':
                s.vista[:] = fatia
            else:
                s.carregar(fatia)
    mapa.puxar()


class GradeRegioes:
    """Combat's grid query interface over Core's live u16 region list [0x4e0f38] (no copy)."""
    def __init__(self, lista):
        self.lista = lista

    def get(self, celula, padrao=None):
        return self.lista[celula]


class MosaicosListados:
    """[0x507d70] is Core's u16 list in the map; Economy's RecursosTerreno wants bytes. Any use is a named stop."""
    def __getattr__(self, nome):
        raise DependenciaIA('UpdateChamp tile grid [0x507d70]: Core list vs Economy bytes contract', 0x478806)

    def __getitem__(self, k):
        raise DependenciaIA('UpdateChamp tile grid [0x507d70]: Core list vs Economy bytes contract', 0x478806)

    def __len__(self):
        return 131072


def recursos_terreno(mm):
    from construcoes import TerrenoSacolas
    from extracao import RecursosTerreno
    terreno = TerrenoSacolas()
    terreno.tipos = mm.vista(mm.u32(0x507d74), 65536)
    terreno.quantidades = mm.vista(mm.u32(0x507dac), 65536)
    recursos = RecursosTerreno(terreno)
    recursos.atributos = mm.vista(mm.u32(0x507da8), 65536)
    recursos.mosaicos = MosaicosListados()
    recursos.minas = mm.vista(0x509954, 80)
    return recursos


def provedores(mapa, prov, mm, ctx, registro, janelas, travessias, fase, regs):
    """Original-name providers for every routine the three phases reach."""
    p = {}
    bonus = lambda jogador, tipo, seletor: prov.bonus.consultar(jogador, tipo, seletor)  # noqa: E731
    p.update(core.provedores_core(mm, bonus))
    maquina = MaquinaTarefasViva(ctx.programa, mm.vista(0x512320, 0x25e8))
    estado_regs = dict(EBX=regs['EBX'])

    def ponto(nome, funcao):
        def chamar(sitio, **argumentos):
            travessias.comparar(fase, nome, sitio + 5, mapa)
            return funcao(sitio=sitio, **argumentos)
        return chamar

    def cruzar(nome):
        return lambda sitio, **argumentos: travessias.atravessar(fase, nome, sitio, mapa, mm, registro,
                                                                 'display routine (Graphics)')

    def nucleo(nome, chamada):
        """Core's provider; a DependenciaRamoCore is reported and the call is crossed."""
        def chamar(sitio, **argumentos):
            chave, _ = travessias.comparar(fase, nome, sitio + 5, mapa)
            try:
                resultado = chamada(**argumentos)
            except core.DependenciaRamoCore as erro:
                if ctx.modo == 'prova':
                    raise DependenciaIA(f'{nome} (Core): {erro}', erro.endereco) from erro
                travessias.paradas_nucleo.append(dict(phase=fase, routine=nome, site=hex(sitio),
                                                      core_address=hex(erro.endereco), message=str(erro)))
                return travessias.atravessar(fase, nome, sitio, mapa, mm, registro,
                                             f'Core provider stop at 0x{erro.endereco:x}', verificado=chave)
            if nome == 'InitGameZone':
                estado_regs['EBX'] = resultado['EBX']
            return resultado
        return chamar

    def fronteira_menu(nome):
        """v1: MenuInit's display calls are declared boundaries (DDLockSurface answers EAX 0)."""
        def chamar(sitio, registros, palavras, limpeza):
            guardas = {'0x4e2f28': mm.u8(0x4e2f28), '0x4e2f29': mm.u8(0x4e2f29)} if nome == 'MCICD_Play' else None
            declarado = 0 if nome == 'DDLockSurface' else None
            registro.fronteira(nome, sitio + 5, f'MenuInit+0x{sitio + 5 - 0x4682bb:x}', registros, guardas, palavras,
                               declarado=declarado, limpeza=limpeza, topo='MenuInit')
            return registros['EAX'] if declarado is None else declarado
        return chamar

    def mcicd_play(sitio, faixa, edx):
        indice = mm.u8(0x4e1d18)
        registro.fronteira('MCICD_Play', sitio + 5, 'CalculGame+0xac5',
                           dict(EAX=faixa, EDX=edx, EBX=(estado_regs['EBX'] & ~0xff) | indice, ECX=2),
                           {'0x4e2f28': mm.u8(0x4e2f28), '0x4e2f29': mm.u8(0x4e2f29)})
        return faixa

    def projeteis(sitio):
        ponteiro = mm.u32(0x5080f0)
        return MaquinaProjeteis(PoolProjeteis(memoria=mm.vista(ponteiro, 5600))).calcular(mm.u32(0x508f7c) & 0xff)

    def unidades():
        pool = mm.u32(0x4e19a0)
        return [mm.ler(pool + 276 * i, 276) for i in range(800)]

    def mascaras():
        jogadores = mm.u32(0x5080a8)
        return bytes(mm.u8(jogadores + 20 * j + 6) for j in range(5))

    def fim(sitio, jogador):
        consultas = consultas_publicadas(
            mm.vista(0x49a0c8, 276000), prov.economia, mm.vista(0x496fe4, 1), mm.vista(0x50c614, 4000),
            celula=lambda j: p['BatimentGetCase'](sitio=0x458a44, estrutura=j),
            invencoes=lambda j: economia_quadro.numero_invencoes(mm, j),
            aliado=lambda a, b: int(aliados(a, b, mascaras())),
            iluminada=lambda c, j: p['CaseEstIlluminee'](sitio=0, caso=c, jogador=j))
        return testar_fim_missao(jogador, mm.vista(0x4e1d20, 100), mm.vista(0x4e1d84, 14), mm.vista(0x4e1a3a, 2),
                                 mm.vista(0x4e1928, 8), mm.vista(0x4dfaa8, 16), consultas)

    producao = prov.habitacao.producao
    recursos = recursos_terreno(mm)
    p.update({
        'EvenementEnCours': lambda sitio: evento_em_curso(mm.vista(0x4e1b0e, 1)),
        'MCICD_Play': mcicd_play,
        'PlayerGetType': lambda sitio, jogador: prov.mercado.tipo_jogador(jogador),
        'MissionGetNum': lambda sitio: mm.u8(0x496fe4),
        'InputGame': lambda sitio, jogador: entrada_jogo(mm, jogador, registro, janelas, p),
        'InputSend': lambda sitio, jogador: enviar_entrada(mm, jogador),
        'EnginOccupeCase': lambda sitio, unidade, celula, filtro: int(ocupa_celula(
            mm.ler(mm.u32(0x4e19a0) + 276 * unidade, 276), celula, filtro)),
        'AvanceMonstre': lambda sitio, jogador: avancar_monstros(mm, p),
        'iaSolver': lambda sitio, contexto: maquina.atualizar((contexto - 0x5148b0) // 16) & 0xffffffff,
        'ProcessInputGame': lambda sitio, jogador: processar_entrada(mm, jogador, ctx.comandos),
        'MessageBoxCalcul': lambda sitio: calcular_caixa_mensagens(mm),
        'CalculIconeAction': lambda sitio: calcular_icone_acao(mm),
        'ProjectileCalcul': projeteis,
        'CalculEnginNextEtape': lambda sitio: calcular_proxima_etapa_unidades(mm, p),
        'EnginNextEtape': lambda sitio, unidade: proxima_etapa_unidade(mm, p, unidade, ctx.tabelas),
        'BonusGetValEngin': lambda sitio, jogador, tipo, seletor, ecx: prov.bonus.consultar(jogador, tipo, seletor,
                                                                                            ecx=ecx),
        'EnginTrouveCible': lambda sitio, unidade: encontrar_alvo(unidades(), unidade, GradeRegioes(prov.mundo.regioes),
                                                                  mascaras()),
        'EnginNextEtape:state7': lambda sitio, unidade: economia_quadro.estado_parado_unidade(mm, unidade),
        'CalculBatimentNextEtape': lambda sitio: calcular_proxima_etapa_estruturas(mm, p),
        'ResetTableauHangar': lambda sitio: economia_quadro.resetar_tabela_hangar(mm),
        'BatimentNextEtape': lambda sitio, estrutura: proxima_etapa_estrutura(mm, p, estrutura, ctx.tabelas),
        'BatimentNextEtape:production': lambda sitio, estrutura: economia_quadro.ramo_producao_estrutura(
            producao, estrutura, producao.calcular_tropa),
        'RechercheCalcul': lambda sitio: economia_quadro.calcular_pesquisa(mm),
        'PlayerInitAllianceCompteur': lambda sitio: economia_quadro.contar_aliancas(mm),
        'SetUpdateChamp': lambda sitio: economia_quadro.agendar_campos(mm, recursos),
        'UpdateChamp': lambda sitio: economia_quadro.atualizar_campos(mm, recursos),
        'CalculMatiere': lambda sitio: economia_quadro.calcular_materia(mm),
        'CalculCompteurMarche': lambda sitio, jogador: economia_quadro.calcular_contador_mercado(mm, jogador),
        'CalculCompteurProposition': lambda sitio, jogador, edx: economia_quadro.calcular_contador_proposicao(
            mm, jogador, edx),
        'PlayerAttaqueCalculSympa': lambda sitio: economia_quadro.calcular_simpatia_ataques(mm),
        'TestFinDeMission': fim,
        'SetClipping': nucleo('SetClipping', lambda eax, edx, ebx, ecx: core.definir_recorte(mm, eax, edx, ebx, ecx)),
        'InitGameZone': nucleo('InitGameZone', lambda eax, edx, ecx=0: core.iniciar_zonas_jogo(mm, eax, edx)),
        'NextAnimTerrain': nucleo('NextAnimTerrain', lambda x, y: core.animar_terreno(mm, x, y)),
        'NextAnimVeget': nucleo('NextAnimVeget', lambda x, y: core.animar_vegetacao(mm, x, y)),
    })
    for nome in PONTOS:
        if nome in p and nome not in NUCLEO:
            p[nome] = ponto(nome, p[nome])
    if ctx.modo == 'prova':
        import efeitos_logicos_exibicao as graficos
        from bancos_quadro_ia import liberar_banco

        def efeitos(nome, funcao):
            def chamar(sitio, **argumentos):
                travessias.comparar(fase, nome, sitio + 5, mapa)
                resultado = funcao(mm)
                for endereco, largura, valor in resultado.escritas:
                    {1: mm.u8, 2: mm.u16, 4: mm.u32}[largura](endereco, valor)
                ctx.raizes_nao_executadas.append(dict(phase=fase, routine=nome, site=hex(sitio),
                                                      provider='graficos efeitos_logicos_exibicao',
                                                      writes=list(resultado.escritas),
                                                      guards=[list(g) for g in resultado.verificacoes]))
                return 0
            return chamar

        def raiz(nome, eax=None):
            def chamar(sitio, registros, palavras, limpeza):
                travessias.comparar(fase, nome, sitio + 5, mapa)
                ctx.raizes_nao_executadas.append(dict(phase=fase, routine=nome, site=hex(sitio), provider=None,
                                                      eax=None if eax is None else hex(eax)))
                return registros['EAX'] if eax is None else eax
            return chamar

        def banco(sitio, registros, palavras, limpeza):
            travessias.comparar(fase, 'DeleteBank', sitio + 5, mapa)
            liberar_banco(mm, ctx.arena, registro, registros['EAX'])
            mm.reindexar()
            return 0

        p['RestoreAll'] = efeitos('RestoreAll', graficos.restaurar_tudo)
        p['AffGame'] = efeitos('AffGame', graficos.desenhar_jogo)
        p['DDLockSurface'] = raiz('DDLockSurface', ctx.superficie)
        for nome in ('FilledBox', 'DDUnlockSurface', 'DDFlipPage'):
            p[nome] = raiz(nome)
        p['DeleteBank'] = banco
        p['LoadPie'] = fronteira_menu('LoadPie')
        p['MCICD_Play:menu'] = fronteira_menu('MCICD_Play')
    elif ctx.cenario == 'exibicao':
        for nome in GRAFICOS_EXIBICAO:
            p[nome] = cruzar(nome)
        p['LoadPie'] = fronteira_menu('LoadPie')
        p['MCICD_Play:menu'] = fronteira_menu('MCICD_Play')
    else:
        p['RestoreAll'] = cruzar('RestoreAll')
        for nome in ('DDLockSurface', 'FilledBox', 'LoadPie', 'DDUnlockSurface', 'DDFlipPage', 'DeleteBank'):
            p[nome] = fronteira_menu(nome)
        p['MCICD_Play:menu'] = fronteira_menu('MCICD_Play')
    return p, estado_regs


def fase_cauda_carga(mapa, prov, ctx, registro, travessias, regs):
    """(a) 0x42d22d .. load-state CalculGame return: RestoreAll, SetClipping, counter reset, MenuInit,
    InitGameZone, then the frame-0 body."""
    mm = MemoriaMapaRapida(mapa)
    janelas = JanelasDeclaradas()
    p, estado_regs = provedores(mapa, prov, mm, ctx, registro, janelas, travessias, 'load_tail', regs)
    p['RestoreAll'](sitio=0x42d27f)
    p['SetClipping'](sitio=0x42d2a6, eax=0, edx=0, ebx=((mm.u16(0x508724) << 5) - 1) & 0xffff,
                     ecx=((mm.u16(0x508726) << 5) - 1) & 0xffff)
    zerar_contadores_carga(mm.vista(0x508f7c, 12))
    menu = dict(p)
    menu['MCICD_Play'] = p['MCICD_Play:menu']

    def menu_init(sitio, jogador, estado, ecx):
        travessias.comparar('load_tail', 'MenuInit', sitio + 5, mapa)
        return iniciar_menu(mm, jogador, estado, ecx, registro, janelas, menu, ebx=0, esp=regs['ESP'])
    menu_init(sitio=0x42d2d0, jogador=mm.u8(0x508041), estado=0x12, ecx=1)
    p['InitGameZone'](sitio=0x42d2d9, eax=1, edx=0)
    return calcular_quadro(mm, p)


def fase_entre_quadros_exibicao(mapa, prov, ctx, registro, travessias, regs, entradas):
    """(b) on the display path: the real ProgIteration tail from 0x475063, AffGame (crossed), the
    _WinMain@16 loop and a new ProgIteration up to the CalculGame entry. Returns the register file."""
    from fundacoes_quadro import avancar_contadores_iteracao
    mm = MemoriaMapaRapida(mapa)
    r = dict(regs)
    if ctx.modo == 'prova':
        p, _ = provedores(mapa, prov, mm, ctx, registro, JanelasDeclaradas(), travessias, 'between_frames', regs)
        p['AffGame'](sitio=0x475063)
    else:
        travessias.atravessar('between_frames', 'AffGame', 0x475063, mapa, mm, registro, 'display routine (Graphics)')
    if mm.u8(0x5099af):
        mm.u8(0x5099af, 0)
        mm.u8(0x5099ae, 0)
    if mm.u8(0x5099b2):
        mm.u8(0x5099b1, 0)
        mm.u8(0x5099b2, 0)
    point = r['ESP']
    r['EDX'], r['ECX'], r['EBX'] = entradas['salvo_edx'], entradas['salvo_ecx'], entradas['salvo_ebx']
    r['ESP'] = point + 8 + 12 + 4
    msg = r['ESP']
    for rotina, retorno, chamador in (('PlaySnd_Manage', 0x460220, '_WinMain@16+0xb0'),
                                      ('MCICD_Manage', 0x460225, '_WinMain@16+0xb5')):
        guardas = {'0x4e2f28': mm.u8(0x4e2f28), '0x4e2f29': mm.u8(0x4e2f29)} if rotina == 'MCICD_Manage' else {}
        registro.fronteira(rotina, retorno, chamador, {k: r[k] for k in ('EAX', 'EDX', 'EBX', 'ECX')}, guardas,
                           palavras=entradas['msg'])
    if r['EBX'] & 0xff != mm.u8(0x49a059):
        raise DependenciaIA('_WinMain@16 quit path', 0x460227)
    registro.vinculo('USER32.PeekMessageA', (msg, r['EBX'], r['EBX'], r['EBX'], r['EBX']), 0x4601d8,
                     entradas['peek_message'])
    r['EAX'] = entradas['peek_message']
    if r['EAX']:
        raise DependenciaIA('_WinMain@16 GetMessageA/DispatchMessageA path', 0x4601dc)
    if r['EBX'] & 0xff == mm.u8(0x49a058):
        raise DependenciaIA('_WinMain@16 WaitMessage path', 0x460214)
    r['ESP'] = msg - 4 - 12 - 8
    avancar_contadores_iteracao(mm.vista(0x508f7c, 12))
    r['EBX'] = 3
    r['EDX'] = r['ESP']
    x, y = entradas['cursor']
    registro.vinculo('USER32.GetCursorPos', (r['ESP'],), 0x47504b, 1, escritas=((r['ESP'], struct.pack('<ii', x, y)),))
    mm.u16(0x5099a8, x)
    mm.u16(0x5099aa, y)
    r['EAX'] = y & 0xffffffff
    r['ESP'] -= 4
    return r


def fase_quadro(mapa, prov, ctx, registro, travessias, regs):
    """(c) CalculGame 0x42c868 entered from ProgIteration .. return 0x475063."""
    mm = MemoriaMapaRapida(mapa)
    janelas = JanelasDeclaradas()
    p, _ = provedores(mapa, prov, mm, ctx, registro, janelas, travessias, 'frame1', regs)
    estado = mm.u8(0x4e2f78)
    mm.u16(0x49a010, 0x1dd8)
    registro.vinculo('USER32.SetCursorPos', (mm.u16(0x5099a8), mm.u16(0x5099aa)), 0x42c8a5, 1)
    if estado != 0x12:
        raise DependenciaIA(f'CalculGame state 0x{estado:x}', ctx.estados[estado] if estado <= 0x18 else 0x42d4e2)
    return calcular_quadro(mm, p)
