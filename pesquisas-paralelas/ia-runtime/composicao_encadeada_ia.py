"""Chained Python composition of MONDE01 (a) load_tail -> (b) between_frames -> (c) frame1 (M2.1 round 3).

One Missions ``MapaMemoriaM1`` is built from the accepted M1 post-load state and
carried through all three phases. It is never restarted from an original state.
Every routine is an integrated provider, called in original order:
- this front: the frame skeleton, the dispatcher loops, CalculNextReflect,
  AvanceMonstre, iaSolver (via Core ``MaquinaTarefas``), ProcessInputGame,
  MessageBoxCalcul, InputGame, InputSend, CalculIconeAction, MenuInit,
  EnginNextEtape and BatimentNextEtape;
- Core ``chamadas_quadro_core`` and ``fundacoes_quadro``;
- Economy ``quadro_economia``, ``BonusUnidades`` and ``Mercado``;
- Combat ``MaquinaProjeteis``, ``alvos_alcance.encontrar_alvo`` and ``aliados``;
- Missions ``fim_missao`` and ``influencia_missao``.

**Declared stops.** RestoreAll (Graphics), and SetClipping, InitGameZone,
NextAnimTerrain and NextAnimVeget (Core, not yet integrated) are crossed by
``Travessias``, exactly and only when the Python state at the call equals the
original state at that call's entry (all blocks). The original's own effect of
that one call (its return state, return EAX, and the bindings and boundaries it
recorded) is then applied. Every crossing is reported. A state that differs at a
crossing is a divergence, and the phase stops there.

**Checkpoints.** At the listed provider calls the Python state is compared with the
original state at the same call. The first difference localizes a divergence.
"""
import struct
import sys

from ambiente_ia_runtime import CD, ROOT
from composicao_quadro1_ia import Registro as RegistroBase, fase_entre_quadros, mundo  # noqa: F401
from entrada_quadro_ia import calcular_icone_acao, entrada_jogo, enviar_entrada, iniciar_menu
from laco_despachantes import calcular_proxima_etapa_estruturas, calcular_proxima_etapa_unidades
from memoria_composicao_ia import MemoriaMapaM1
from proxima_etapa_quadro import proxima_etapa_estrutura, proxima_etapa_unidade, tabelas_imagem
from quadro_calcul_game import calcular_quadro
from reinicio_ia import DependenciaIA
from rotinas_quadro_ia import (TABELA_COMANDOS, PonteTarefas, avancar_monstros, calcular_caixa_mensagens,
                               processar_entrada, resolver_ia)
from simbolos_ia import ler_rul
from tarefas_ia import MaquinaTarefas

for _pasta in ('pesquisas-paralelas/combate', 'pesquisas-paralelas/economia'):
    if str(ROOT / _pasta) not in sys.path:
        sys.path.append(str(ROOT / _pasta))
from chamadas_quadro_core import provedores_core  # noqa: E402
from fundacoes_quadro import zerar_contadores_carga  # noqa: E402
from fim_missao import consultas_publicadas, evento_em_curso, testar_fim_missao  # noqa: E402
import quadro_economia as economia_quadro  # noqa: E402
from alvos_alcance import aliados, encontrar_alvo  # noqa: E402
from maquina_projeteis import MaquinaProjeteis  # noqa: E402
from projeteis import PoolProjeteis  # noqa: E402

TRAVESSIAS = {'RestoreAll': 'graphics', 'SetClipping': 'core', 'InitGameZone': 'core',
              'NextAnimTerrain': 'core', 'NextAnimVeget': 'core'}
PONTOS = ('MenuInit', 'InputGame', 'InputSend', 'ProcessInputGame', 'MessageBoxCalcul', 'CalculIconeAction',
          'ProjectileCalcul', 'CalculEnginNextEtape', 'EnginNextEtape', 'CalculBatimentNextEtape', 'RechercheCalcul',
          'PlayerInitAllianceCompteur', 'SetUpdateChamp', 'UpdateChamp', 'CalculMatiere', 'CalculCompteurMarche',
          'CalculCompteurProposition', 'PlayerAttaqueCalculSympa', 'TestFinDeMission')


class Divergencia(RuntimeError):
    def __init__(self, fase, rotina, ocorrencia, blocos):
        self.fase, self.rotina, self.ocorrencia, self.blocos = fase, rotina, ocorrencia, blocos
        super().__init__(f'{fase}: state differs from the original at {rotina} #{ocorrencia}: {blocos[:6]}')


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


class ContextoEncadeado(PonteTarefas):
    def __init__(self, imagem):
        super().__init__(MaquinaTarefas(ler_rul((CD / 'INSTALHD/RISING.RUL').read_bytes())))
        self.comandos = imagem.table(TABELA_COMANDOS, 40)
        self.estados = imagem.table(0x42c804, 25)
        self.tabelas = tabelas_imagem(imagem)


class Travessias:
    """Original data for declared stops and checkpoints, keyed (phase, routine, occurrence)."""

    def __init__(self, entradas, retornos, pontos, hashes):
        self.entradas, self.retornos, self.pontos, self.hashes = entradas, retornos, pontos, hashes
        self.contagem, self.feitas, self.verificados = {}, [], []

    def _ocorrencia(self, fase, rotina):
        n = self.contagem.get((fase, rotina), 0)
        self.contagem[(fase, rotina)] = n + 1
        return n

    def comparar(self, fase, rotina, mapa):
        n = self._ocorrencia(fase, rotina)
        esperado = self.pontos.get((fase, rotina, n))
        if esperado is None:
            return n, None
        atual = self.hashes(mapa)
        diferentes = sorted(k for k in set(atual) | set(esperado) if atual.get(k) != esperado.get(k))
        self.verificados.append(dict(phase=fase, routine=rotina, occurrence=n, equal=not diferentes))
        if diferentes:
            raise Divergencia(fase, rotina, n, diferentes)
        return n, esperado

    def atravessar(self, fase, rotina, sitio, mapa, registro):
        n, esperado = self.comparar(fase, rotina, mapa)
        if esperado is None:
            raise DependenciaIA(f'{rotina} ({TRAVESSIAS[rotina]}): no original crossing data', sitio)
        retorno = self.retornos[(fase, rotina, n)]
        carregar_estado(mapa, retorno['blocks'])
        registro.vinculos += retorno['bindings']
        registro.fronteiras += retorno['boundaries']
        self.feitas.append(dict(phase=fase, routine=rotina, owner=TRAVESSIAS[rotina], site=hex(sitio), occurrence=n,
                                state_equal_at_entry=True, bindings=len(retorno['bindings']),
                                boundaries=len(retorno['boundaries']), eax=hex(retorno['eax'])))
        return retorno['eax']


def carregar_estado(mapa, blocos):
    """Write a full original block set into the live map, segment by segment (lists element-wise)."""
    if set(blocos) - {'native_stack'} != set(mapa.blocos):
        raise ValueError('Crossing state has a different block set than the map')
    for s in mapa.segmentos:
        base, dados = blocos[s.bloco]
        fatia = dados[s.base - base:s.fim - base]
        if s.tipo == 'bytes':
            s.vista[:] = fatia
        else:
            s.carregar(fatia)
    mapa.puxar()


def provedores(mapa, prov, mm, ctx, registro, janelas, travessias, fase, regs):
    """Original-name providers for every routine the three phases reach."""
    p = {}
    bonus = lambda jogador, tipo, seletor: prov.bonus.consultar(jogador, tipo, seletor)  # noqa: E731
    p.update(provedores_core(mm, bonus))

    def ponto(nome, funcao):
        def chamar(sitio, **argumentos):
            travessias.comparar(fase, nome, mapa)
            return funcao(sitio=sitio, **argumentos)
        return chamar

    def cruzar(nome):
        return lambda sitio, **argumentos: travessias.atravessar(fase, nome, sitio, mapa, registro)

    def mcicd_play(sitio, faixa, edx):
        indice = mapa.u8(0x4e1d18)
        registro.fronteira('MCICD_Play', sitio + 5, 'CalculGame+0xac5',
                           dict(EAX=faixa, EDX=edx, EBX=(regs['EBX'] & ~0xff) | indice, ECX=2),
                           {'0x4e2f28': mapa.u8(0x4e2f28), '0x4e2f29': mapa.u8(0x4e2f29)})
        return faixa

    def projeteis(sitio):
        ponteiro = mapa.u32(0x5080f0)
        return MaquinaProjeteis(PoolProjeteis(memoria=mapa.vista(ponteiro, 5600))).calcular(mapa.u32(0x508f7c) & 0xff)

    def alvo(sitio, unidade):
        pool = mapa.u32(0x4e19a0)
        unidades = [mapa.ler(pool + 276 * i, 276) for i in range(800)]
        jogadores = mapa.u32(0x5080a8)
        mascaras = bytes(mapa.u8(jogadores + 20 * j + 6) for j in range(5))
        return encontrar_alvo(unidades, unidade, GradeRegioes(prov.mundo.regioes), mascaras)

    def fim(sitio, jogador):
        jogadores = mapa.u32(0x5080a8)
        mascaras = bytes(mapa.u8(jogadores + 20 * j + 6) for j in range(5))
        consultas = consultas_publicadas(
            mapa.vista(0x49a0c8, 276000), prov.economia, mapa.vista(0x496fe4, 1), mapa.vista(0x50c614, 4000),
            celula=lambda j: p['BatimentGetCase'](sitio=0x458a44, estrutura=j),
            invencoes=lambda j: economia_quadro.numero_invencoes(mm, j),
            aliado=lambda a, b: int(aliados(a, b, mascaras)),
            iluminada=lambda c, j: p['CaseEstIlluminee'](sitio=0, caso=c, jogador=j))
        return testar_fim_missao(jogador, mapa.vista(0x4e1d20, 100), mapa.vista(0x4e1d84, 14), mapa.vista(0x4e1a3a, 2),
                                 mapa.vista(0x4e1928, 8), mapa.vista(0x4dfaa8, 16), consultas)

    producao = prov.habitacao.producao
    recursos = recursos_terreno(mapa)
    p.update({
        'EvenementEnCours': lambda sitio: evento_em_curso(mapa.vista(0x4e1b0e, 1)),
        'MCICD_Play': mcicd_play,
        'PlayerGetType': lambda sitio, jogador: prov.mercado.tipo_jogador(jogador),
        'MissionGetNum': lambda sitio: mapa.u8(0x496fe4),
        'InputGame': lambda sitio, jogador: entrada_jogo(mm, jogador, registro, janelas),
        'InputSend': lambda sitio, jogador: enviar_entrada(mm, jogador),
        'AvanceMonstre': lambda sitio, jogador: avancar_monstros(mm, p),
        'iaSolver': lambda sitio, contexto: resolver_ia(mm, ctx, contexto),
        'ProcessInputGame': lambda sitio, jogador: processar_entrada(mm, jogador, ctx.comandos),
        'MessageBoxCalcul': lambda sitio: calcular_caixa_mensagens(mm),
        'CalculIconeAction': lambda sitio: calcular_icone_acao(mm),
        'ProjectileCalcul': projeteis,
        'CalculEnginNextEtape': lambda sitio: calcular_proxima_etapa_unidades(mm, p),
        'EnginNextEtape': lambda sitio, unidade: proxima_etapa_unidade(mm, p, unidade, ctx.tabelas),
        'BonusGetValEngin': lambda sitio, jogador, tipo, seletor, ecx: prov.bonus.consultar(jogador, tipo, seletor,
                                                                                            ecx=ecx),
        'EnginTrouveCible': alvo,
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
    })
    for nome in PONTOS:
        if nome in p:
            p[nome] = ponto(nome, p[nome])
    for nome in TRAVESSIAS:
        p[nome] = cruzar(nome)
    return p


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


def recursos_terreno(mapa):
    from construcoes import TerrenoSacolas
    from extracao import RecursosTerreno
    terreno = TerrenoSacolas()
    terreno.tipos = mapa.vista(mapa.u32(0x507d74), 65536)
    terreno.quantidades = mapa.vista(mapa.u32(0x507dac), 65536)
    recursos = RecursosTerreno(terreno)
    recursos.atributos = mapa.vista(mapa.u32(0x507da8), 65536)
    recursos.mosaicos = MosaicosListados()
    recursos.minas = mapa.vista(0x509954, 80)
    return recursos


def fase_cauda_carga(mapa, prov, ctx, registro, travessias, regs):
    """(a) 0x42d22d .. load-state CalculGame RET: RestoreAll, SetClipping, counter reset, MenuInit,
    InitGameZone, then the frame-0 body."""
    mm = MemoriaMapaM1(mapa)
    janelas = JanelasDeclaradas()
    p = provedores(mapa, prov, mm, ctx, registro, janelas, travessias, 'load_tail', regs)
    p['RestoreAll'](sitio=0x42d27f)
    p['SetClipping'](sitio=0x42d2a6)
    zerar_contadores_carga(mapa.vista(0x508f7c, 12))
    p['MenuInit'] = travessias_ponto(travessias, 'load_tail', 'MenuInit', mapa, lambda sitio, **a: iniciar_menu(
        mm, a['jogador'], a['estado'], a['ecx'], registro, janelas, p, ebx=0, esp=regs['ESP']))
    p['MenuInit'](sitio=0x42d2d0, jogador=mapa.u8(0x508041), estado=0x12, ecx=1)
    p['InitGameZone'](sitio=0x42d2d9)
    return calcular_quadro(mm, p)


def travessias_ponto(travessias, fase, nome, mapa, funcao):
    def chamar(sitio, **argumentos):
        travessias.comparar(fase, nome, mapa)
        return funcao(sitio=sitio, **argumentos)
    return chamar


def fase_quadro(mapa, prov, ctx, registro, travessias, regs):
    """(c) CalculGame 0x42c868 entered from ProgIteration .. return 0x475063."""
    mm = MemoriaMapaM1(mapa)
    janelas = JanelasDeclaradas()
    p = provedores(mapa, prov, mm, ctx, registro, janelas, travessias, 'frame1', regs)
    estado = mapa.u8(0x4e2f78)
    mapa.vista(0x49a010, 2)[:] = struct.pack('<H', 0x1dd8)
    registro.vinculo('USER32.SetCursorPos', (mapa.u16(0x5099a8), mapa.u16(0x5099aa)), 0x42c8a5, 1)
    if estado != 0x12:
        raise DependenciaIA(f'CalculGame state 0x{estado:x}', ctx.estados[estado] if estado <= 0x18 else 0x42d4e2)
    return calcular_quadro(mm, p)
