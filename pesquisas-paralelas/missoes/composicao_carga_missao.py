"""Whole ``MissionLoad 0x46c2cf`` composed in Python from the frozen entry snapshot.

Order follows ``evidencias/0046c2cf.asm`` exactly. Every effect is produced by
an integrated provider (or by the small Missions-owned caller code that has no
other owner: the 0x4e1a38/0x4e1a3a stores inside the reset prefix, FileOpen
0x458420 and FileClose 0x45844c) over the one shared memory map. External
inputs are read from the read-only original media through the same resolution
as the oracle's declared handlers; the ordered requests (files, cursor
positions, profile keys, allocations) are logged for comparison with the
original binding log and are never replayed from it.

Any provider exception stops the composition at its original CALL site with
every earlier effect retained, and is reported as a named stop. The result is
evidence only when the run reaches the return and the whole state compares
equal (see ``comparacao_carga_missao``).
"""
from dataclasses import dataclass, field
import hashlib
import struct
import traceback

import ambiente_missoes
from formatos import Leitor
from fronteiras_carga_missao import EntradasNomeadas, MidiaOriginal, PerfilWindows
from mapa_memoria_m1 import MapaMemoriaM1, carregar_blocos
from arena_composicao_m1 import ArenaComposicaoM1
from ligacao_provedores_m1 import (AtributoNaoMapeadoM1, MascaraMapeada, montar_provedores,
                                   verificar_excessos)
from reinicio_missao import MemoriaReinicio, ProvedoresReinicio, resetar_para_missao
from reset_terreno import resetar_terreno, resetar_minimapa
from carregador_cabecalho import continuar_cabecalho
from conclusao_remapeamento import remapear_mundo
from carregador_estruturas import carregar_estruturas_missao
from carregador_unidades import carregar_unidades_missao
from carregador_auxiliares import carregar_minas_missao, carregar_ataques_missao
from carregador_cadeia_auxiliar import (carregar_fantasmas_missao, carregar_influencia_missao,
                                        consumir_diversos_missao, carregar_entrada_monstros_missao)
from carregador_condicoes import carregar_condicoes_fim, carregar_objetivos
from terreno_unidades import ProvedoresTerrenoUnidades, provedores_terreno_core
from terreno_estruturas_missao import (ProvedoresTerrenoEstruturas, preparar_terreno_missao,
                                       provedores_terreno_estruturas_core)
from recuperacao_experiencia import recuperar_experiencia_missao

ENTRADA, RETORNO_REAL = 0x46c2cf, 0x42d22d
FILE_SLOT, BASE_FLUXO = 0x4e1d1c, 0x7f000000
MODO = 0x494b3b


@dataclass(frozen=True)
class Passo:
    nome: str
    rotina: int        # original callee (or inline range start)
    chamada: int       # original CALL site (or first instruction of inline code)
    dono: str


PASSOS = {p.nome: p for p in (
    Passo('MakeMissionName', 0x46c1b8, 0x46c2fd, 'missions'),
    Passo('MissionPathBuild', 0x46c302, 0x46c302, 'missions'),
    Passo('ResetCounters', 0x46c34c, 0x46c34c, 'missions'),
    Passo('IconeReset', 0x45e88f, 0x46c35a, 'missions'),
    Passo('TerrainReset', 0x46b315, 0x46c35f, 'core'),
    Passo('MiniMapReset', 0x469f00, 0x46c364, 'core'),
    Passo('BatimentResetAll', 0x41a75c, 0x46c369, 'core'),
    Passo('EnginResetAll', 0x441659, 0x46c36e, 'core'),
    Passo('ProjectileReset', 0x46e00a, 0x46c373, 'combat'),
    Passo('MessageBoxInit', 0x469908, 0x46c378, 'missions'),
    Passo('BallonInit', 0x441b6c, 0x46c37d, 'missions'),
    Passo('FileOpen', 0x458420, 0x46c389, 'missions'),
    Passo('HeaderPrelude', 0x46c396, 0x46c396, 'missions'),
    Passo('Chemin_Remap', 0x42ee1c, 0x46c512, 'core'),
    Passo('StructureCopy', 0x46c517, 0x46c517, 'missions'),
    Passo('LoadEngin', 0x46acbf, 0x46c578, 'missions'),
    Passo('LoadMine', 0x47534a, 0x46c57d, 'missions'),
    Passo('IALoadAttaqueIni', 0x47c24d, 0x46c582, 'missions'),
    Passo('LoadBatimentGhost', 0x47bcc7, 0x46c587, 'missions'),
    Passo('LoadCadreInfluence', 0x47c04a, 0x46c58c, 'missions'),
    Passo('LoadFinMission', 0x458b05, 0x46c591, 'missions'),
    Passo('LoadCalculMissionDivers', 0x47c30f, 0x46c596, 'missions'),
    Passo('LoadObjectif', 0x47c404, 0x46c59b, 'missions'),
    Passo('LoadEntrerMonstre', 0x47ac30, 0x46c5a0, 'missions'),
    Passo('FileClose', 0x45844c, 0x46c5a5, 'missions'),
    Passo('MissionPlaceTerrain', 0x46c122, 0x46c5aa, 'missions'),
    Passo('EnginInitTechnologie', 0x441459, 0x46c5af, 'economy'),
    Passo('BatimentInitCave', 0x419112, 0x46c5b4, 'economy'),
    Passo('Engin_RetrieveExperimente', 0x441623, 0x46c5b9, 'core'),
    Passo('PlayerRetrieve', 0x46df41, 0x46c5be, 'economy'),
    Passo('IaReset', 0x47f36e, 0x46c5cc, 'ai-runtime'),
    Passo('MarcheResetAll', 0x46027c, 0x46c5d1, 'economy'),
)}
# Function names inside resetar_para_missao, for attributing a stop to its original CALL.
_PREFIXO = (('nome_arquivo_missao', 'MakeMissionName'), ('resetar_icones', 'IconeReset'),
            ('resetar_terreno', 'TerrainReset'), ('resetar_minimapa', 'MiniMapReset'),
            ('resetar_todas_estruturas', 'BatimentResetAll'), ('resetar_todas_unidades', 'EnginResetAll'),
            ('resetar_projeteis', 'ProjectileReset'), ('inicializar_caixas_mensagem', 'MessageBoxInit'),
            ('inicializar_baloes', 'BallonInit'))


def _sha(dados):
    return hashlib.sha256(bytes(dados)).hexdigest()


class ParadaComposicaoM1(RuntimeError):
    def __init__(self, passo, erro):
        self.passo, self.erro = passo, erro
        super().__init__(f'{passo.nome} 0x{passo.rotina:x} at CALL 0x{passo.chamada:x} ({passo.dono}): '
                         f'{type(erro).__name__}: {erro}')


class LeitorRegistradoM1(Leitor):
    """The committed Leitor over the media bytes; logs every fread/FileSeek request."""
    def __init__(self, dados, registro, fluxo):
        super().__init__(dados, 0)
        self.registro, self.fluxo = registro, fluxo

    def ler(self, tamanho):
        cursor = self.posicao
        dados = super().ler(tamanho)
        self.registro.append(dict(name='CRT.fread', args=(tamanho, 1), result=1, cursor=cursor,
                                  sha256=_sha(dados), stream=self.fluxo))
        return dados

    def buscar(self, deslocamento, origem):
        if origem not in (0, 1):
            raise ValueError(f'FileSeek origin {origem} outside the composed reader')
        alvo = (0 if origem == 0 else self.posicao) + deslocamento
        if alvo < 0:
            raise ValueError('FileSeek before file start')
        self.posicao = alvo
        self.registro.append(dict(name='FileSeek', args=(deslocamento, origem), result=0, cursor=alvo,
                                  stream=self.fluxo))


class PerfilComposicaoM1:
    """GetPrivateProfileIntA/StringA answered from the media exactly as the oracle's handler parses it."""
    def __init__(self, midia, registro):
        self.windows = PerfilWindows(midia)
        self.registro = registro

    def inteiro(self, secao, chave, padrao, arquivo):
        valor = self.windows._valor(bytes(secao), bytes(chave), bytes(arquivo))
        if valor is None:
            resultado = padrao & 0xffffffff
        elif valor.isdigit():
            resultado = int(valor) & 0xffffffff
        else:
            raise ValueError(f'Profile integer {secao!r}/{chave!r}={valor!r} outside the decimal subset')
        self.registro.append(dict(name='KERNEL32.GetPrivateProfileIntA',
                                  args=(bytes(secao), bytes(chave), padrao & 0xffffffff, bytes(arquivo)),
                                  result=resultado))
        return resultado

    def texto(self, secao, chave, padrao, tamanho, arquivo):
        valor = self.windows._valor(bytes(secao), bytes(chave), bytes(arquivo))
        if valor is None:
            valor = bytes(padrao)
        if len(valor) >= 2 and valor[:1] == valor[-1:] and valor[:1] in (b'"', b"'"):
            valor = valor[1:-1]
        resultado = valor[:tamanho - 1]
        self.registro.append(dict(name='KERNEL32.GetPrivateProfileStringA',
                                  args=(bytes(secao), bytes(chave), bytes(padrao), tamanho, bytes(arquivo)),
                                  result=len(resultado), written_sha256=_sha(resultado + b'\0')))
        return resultado


@dataclass
class ResultadoComposicaoM1:
    al: object = None                 # AL at the return, or None when stopped
    retornou: bool = False
    parada: dict = None
    passos: list = field(default_factory=list)
    registro: list = field(default_factory=list)
    detalhes: dict = field(default_factory=dict)
    composicao: object = None


def entradas_nomeadas(entrada):
    n = entrada['named_inputs']
    return EntradasNomeadas(
        diretorio_instalacao=n['install_directory'].encode('latin-1'), unidade_cd=n['cd_drive'].encode(),
        rotulo_cd=n['cd_volume_label'].encode('latin-1'), relogio_ms=tuple(n['clock_ms']),
        preenchimento_alocacao=n['allocation_fill'], estado_memoria=bytes.fromhex(n['memory_status_hex']),
        teclas=tuple(tuple(t) for t in n['async_keys']), id_thread=n['thread_id'],
        proveniencia=n.get('provenance', {}))


PONTES = {
    'ordens': ('DIAGNOSTIC ONLY, not M1 evidence: around EnginInitTechnologie 0x46c5af, copy the four live '
               'Core Bag allocations [[0x4e19b8]+4j] into Economy PropriedadeConstrucoes.ordens (its own '
               '10,816-byte buffer), call the provider, then copy the 4 x 2,704 bytes back. Needed only '
               'because Economy cannot alias the four distinct allocations.'),
}


class ComposicaoCargaMissaoM1:
    def __init__(self, entrada, *, cd_dir=None, pontes=()):
        """``pontes``: named diagnostic bridges (see PONTES). The default strict run uses none."""
        desconhecidas = set(pontes) - set(PONTES)
        if desconhecidas:
            raise ValueError(f'Unknown diagnostic bridges {sorted(desconhecidas)}')
        self.pontes = tuple(pontes)
        self.pontes_usadas = []
        self.entrada = entrada
        self.mapa = MapaMemoriaM1(carregar_blocos(entrada['blocks']))
        self.provedores = montar_provedores(self.mapa)
        self.mapa.fechar()
        self.registro = []
        self.arena = ArenaComposicaoM1(self.mapa, entrada['arena'], entrada['allocations'], self.registro)
        self.midia = MidiaOriginal(entradas_nomeadas(entrada), cd_dir)
        self.proximo_fluxo = entrada['crt_next_stream_index']
        self.passos = []
        self.atual = None

    # -- helpers ---------------------------------------------------------
    def _sinc(self, funcao):
        """Wrap a provider callable: pull cached scalars, call, push them back."""
        def chamada(*argumentos):
            self.mapa.puxar()
            resultado = funcao(*argumentos)
            self.mapa.empurrar()
            return resultado
        return chamada

    def _passo(self, nome, funcao, **detalhes):
        self.atual = PASSOS[nome]
        try:
            resultado = self._sinc(funcao)()
        except Exception as erro:
            raise ParadaComposicaoM1(PASSOS[nome], erro) from erro
        self.passos.append(dict(step=nome, **{k: v for k, v in detalhes.items()}))
        return resultado

    def _vista(self, endereco, tamanho):
        return self.mapa.vista(endereco, tamanho)

    # -- Missions caller code without another owner ------------------------
    def _file_open(self, caminho):
        """FileOpen 0x458420: fopen(path, "rb") -> [0x4e1d1c]; AL = FILE* != 0."""
        modo = self.mapa.ler(MODO, 3)
        if modo != b'rb\0':
            raise ValueError('FileOpen mode string at 0x494b3b is not "rb"')
        arquivo, dados = self.midia.ler(caminho)
        if arquivo is None:
            fluxo = 0
        else:
            self.proximo_fluxo += 1
            fluxo = BASE_FLUXO + 0x100 * self.proximo_fluxo
        self.registro.append(dict(name='CRT.fopen', args=(bytes(caminho), b'rb'), result=fluxo,
                                  file=None if arquivo is None else self.midia.lidos[str(arquivo)]))
        self._vista(FILE_SLOT, 4)[:] = struct.pack('<I', fluxo)
        return fluxo, dados

    def _file_close(self):
        """FileClose 0x45844c: fclose([0x4e1d1c]) then [0x4e1d1c] = 0."""
        fluxo = self.mapa.u32(FILE_SLOT)
        self.registro.append(dict(name='CRT.fclose', args=(fluxo,), result=0))
        self._vista(FILE_SLOT, 4)[:] = bytes(4)

    # -- the whole load --------------------------------------------------
    def _prefixo(self, w, p):
        memoria = MemoriaReinicio(
            contadores=self._vista(0x4e1a38, 4), icones=self._vista(0x4e2410, 60),
            icones_alterados=self._vista(0x4e05a2, 1), mensagens=self._vista(0x4e7754, 0x20606),
            baloes=p.habitacao.propriedade.baloes, estruturas=w.estruturas,
            estruturas_bandeiras=w.realizaveis_estruturas, estruturas_selecoes=w.selecoes_estruturas,
            unidades=w, projeteis=self._vista(self.mapa.u32(0x5080f0), 5600), missao=self._vista(0x496fe4, 1))

        def terreno():
            self.atual = PASSOS['TerrainReset']
            return resetar_terreno(w, self._vista(0x509954, 80), self._vista(0x497164, 4))

        def minimapa():
            self.atual = PASSOS['MiniMapReset']
            return resetar_minimapa(w)
        diretorio = self.mapa.ler(0x509594, 0x100)
        self.atual = PASSOS['MakeMissionName']
        try:
            self.mapa.puxar()
            pedido = resetar_para_missao(memoria, diretorio, ProvedoresReinicio(
                terreno=self._sinc(terreno), minimapa=self._sinc(minimapa)))
            self.mapa.empurrar()
        except Exception as erro:
            nomes = [q.name for q in traceback.extract_tb(erro.__traceback__)]
            passo = self.atual
            for funcao, nome in _PREFIXO:
                if funcao in nomes:
                    passo = PASSOS[nome]
            raise ParadaComposicaoM1(passo, erro) from erro
        for nome in ('MakeMissionName', 'MissionPathBuild', 'ResetCounters', 'IconeReset', 'TerrainReset',
                     'MiniMapReset', 'BatimentResetAll', 'EnginResetAll', 'ProjectileReset',
                     'MessageBoxInit', 'BallonInit'):
            self.passos.append(dict(step=nome))
        self.passos[-11]['name_bytes'] = pedido.nome.decode('latin-1')
        self.passos[-10]['path'] = pedido.caminho.decode('latin-1')
        return pedido

    def executar(self):
        w, p = self.provedores.mundo, self.provedores
        resultado = ResultadoComposicaoM1(composicao=self, registro=self.registro, passos=self.passos)
        copia_missao = self.mapa.u8(0x496fe4)   # 0x46c2da..0x46c2e6: AL copied to [esp+0x128]
        try:
            pedido = self._prefixo(w, p)
            fluxo, dados = self._passo('FileOpen', lambda: self._file_open(pedido.caminho))
            if not fluxo:
                resultado.al, resultado.retornou = 0, True   # je 0x46c5d8 with AL=0
                return self._fechar(resultado)
            leitor = LeitorRegistradoM1(dados, self.registro, fluxo)
            tiles = self.mapa._segmento(self.mapa.u32(0x507d70), 2)

            def cabecalho():
                bruto = bytearray(tiles.bytes())     # list-backed tile allocation staged as bytes
                cab = continuar_cabecalho(leitor, w.atributos, bruto, w.objetos, w.donos_objetos, p.economia,
                                          self._vista(0x497168, 4), self._vista(0x508720, 4),
                                          self.mapa.u8(0x508041))
                tiles.carregar(bytes(bruto))
                return cab
            cab = self._passo('HeaderPrelude', cabecalho)
            self.passos[-1].update(width=cab.largura, height=cab.altura, viewer=cab.jogador_visualizacao,
                                   cursor=cab.fim)
            a = self.arena
            al_remap = self._passo('Chemin_Remap', lambda: remapear_mundo(
                w, alocar=a.alocar, fixar=a.fixar, obter_handle=a.obter_handle, desfixar=a.desfixar,
                liberar=a.liberar))
            self.passos[-1]['al'] = int(bool(al_remap))
            carga = self._passo('StructureCopy', lambda: carregar_estruturas_missao(leitor, w.estruturas))
            self.passos[-1].update(count=carga.quantidade, indices=list(carga.indices))
            bonus = p.bonus
            carga = self._passo('LoadEngin', lambda: carregar_unidades_missao(
                leitor, w.unidades, self._vista(0x4e19bc, 4), bonus.tipos_unidades, w.selecoes_unidades,
                modificador12=lambda dono, tipo: bonus.consultar(dono, tipo, 12)))
            self.passos[-1].update(count=carga.quantidade, indices=list(carga.indices))
            perfil = PerfilComposicaoM1(self.midia, self.registro)
            self._passo('LoadMine', lambda: carregar_minas_missao(leitor, self._vista(0x509954, 80)))
            self._passo('IALoadAttaqueIni', lambda: carregar_ataques_missao(leitor, self._vista(0x50d5b4, 1004)))
            self._passo('LoadBatimentGhost', lambda: carregar_fantasmas_missao(leitor, self._vista(0x50b18c, 5254)))
            self._passo('LoadCadreInfluence', lambda: carregar_influencia_missao(leitor, self._vista(0x50c614, 4000)))
            self._passo('LoadFinMission', lambda: carregar_condicoes_fim(leitor, self._vista(0x4e1d20, 114)))
            self._passo('LoadCalculMissionDivers', lambda: consumir_diversos_missao(leitor))
            self._passo('LoadObjectif', lambda: carregar_objetivos(leitor, self._vista(0x511ffc, 804)))
            self._passo('LoadEntrerMonstre', lambda: carregar_entrada_monstros_missao(
                leitor, self._vista(0x50a9bc, 1220), self._vista(0x50af84, 432), self._vista(0x497164, 4),
                tipos_grupo8=self.mapa.ler(0x498400, 8), perfil=perfil))
            self._passo('FileClose', self._file_close)
            self.passos[-1]['cursor'] = leitor.posicao

            def terreno_missao():
                u = provedores_terreno_core(w, bonus_unidades=bonus)
                e = provedores_terreno_estruturas_core(w, habitacao=p.habitacao,
                                                       mascara_tipo20=MascaraMapeada(self.mapa, 0x4dfb9c, 20))
                return preparar_terreno_missao(
                    ProvedoresTerrenoUnidades(*(self._sinc(f) for f in (u.existe, u.visibilidade, u.colocar,
                                                                         u.capacidades))),
                    ProvedoresTerrenoEstruturas(*(None if f is None else self._sinc(f) for f in (
                        e.existe, e.colocar, e.habitada, e.habitar, e.modificar_mapa))))
            terreno = self._passo('MissionPlaceTerrain', terreno_missao)
            self.passos[-1].update(units_placed=list(terreno.unidades.colocadas),
                                   structures_placed=list(terreno.estruturas.colocadas),
                                   structures_inhabited=list(terreno.estruturas.habitadas))
            cauda = p.cauda
            if 'ordens' in self.pontes and not p.ordens_por_dono:
                self._passo('EnginInitTechnologie', lambda: self._ponte_ordens(cauda.inicializar_tecnologia_unidades))
            else:
                self._passo('EnginInitTechnologie', cauda.inicializar_tecnologia_unidades)
            self._passo('BatimentInitCave', lambda: cauda.inicializar_cavernas(w))
            self._passo('Engin_RetrieveExperimente', lambda: recuperar_experiencia_missao(
                w, p.vistas['experiencia_guardada']))
            self._passo('PlayerRetrieve', cauda.recuperar_jogadores)

            def ia_reset():
                from reinicio_ia import REGIOES_REINICIO
                from reinicio_ia_compartilhado import ReinicioIACompartilhado
                unidades, jogadores = self.mapa.u32(0x4e19a0), self.mapa.u32(0x5080a8)
                regioes = REGIOES_REINICIO + ((unidades, unidades + 220800, 'unit pool 800x276'),
                                              (jogadores, jogadores + 80, 'player table 4x20'))
                adaptador = ReinicioIACompartilhado(self.mapa.memoria_declarada(regioes), w, p.mercado,
                                                    self._vista(0x496fe4, 1), pesquisa64=self._vista(0x5080f4, 64))
                eax = adaptador()
                return eax, adaptador.chamadas
            eax, chamadas = self._passo('IaReset', ia_reset)
            self.passos[-1].update(al_argument_unused=copia_missao, eax=eax, provider_calls=len(chamadas))
            self._passo('MarcheResetAll', cauda.resetar_mercado)
            resultado.al, resultado.retornou = 1, True    # 0x46c5d6 mov al, 1
        except ParadaComposicaoM1 as parada:
            erro = parada.erro
            resultado.parada = dict(
                step=parada.passo.nome, routine=hex(parada.passo.rotina), call_site=hex(parada.passo.chamada),
                owner=parada.passo.dono, exception=type(erro).__name__, message=str(erro),
                unmapped_attribute=(dict(owner=erro.dono, attribute=erro.atributo, reason=erro.motivo,
                                         write=erro.escrita) if isinstance(erro, AtributoNaoMapeadoM1) else None),
                traceback=[f'{q.filename.rsplit("/", 1)[-1]}:{q.lineno} {q.name}'
                           for q in traceback.extract_tb(erro.__traceback__)][-8:],
                completed_steps=[q['step'] for q in self.passos])
        return self._fechar(resultado)

    def _ponte_ordens(self, funcao):
        """Diagnostic copy-in/copy-out bridge for Economy's single Bag buffer (PONTES['ordens'])."""
        propriedade = self.provedores.habitacao.propriedade
        negados = type(propriedade)._m1_negados
        motivo = negados.pop('ordens')
        ordens = vars(propriedade)['ordens']
        bolsas = self.provedores.mundo.bolsas_tipos_unidades
        try:
            ordens[:] = b''.join(bytes(b) for b in bolsas)
            resultado = funcao()
            for j, bolsa in enumerate(bolsas):
                bolsa[:] = ordens[j * 2704:(j + 1) * 2704]
        finally:
            negados['ordens'] = motivo
        self.pontes_usadas.append(dict(bridge='ordens', step='EnginInitTechnologie', description=PONTES['ordens']))
        return resultado

    def _fechar(self, resultado):
        resultado.detalhes = dict(
            ordens_contract='per-owner [0x4e19b8] pools' if self.provedores.ordens_por_dono
            else 'legacy single 10,816-byte buffer',
            diagnostic_bridges=list(self.pontes_usadas),
            bridges_not_needed=[b for b in self.pontes
                                if b == 'ordens' and self.provedores.ordens_por_dono],
            excess_changed=verificar_excessos(self.provedores),
            live_arena_allocations=len(self.arena.vivos), next_free=hex(self.arena.proximo),
            identity_sharing=self.provedores.compartilhados,
            denied_attributes={k: sorted(v) for k, v in self.provedores.negados.items() if v})
        return resultado
