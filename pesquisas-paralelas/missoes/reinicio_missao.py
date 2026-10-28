"""MissionLoad 0x46c2cf / MissionLoadName 0x46c5e3 reset prefixes up to FileOpen.

Missions owns the caller order, the two u16 0xffff stores and the UI leaf
resets IconeReset, MessageBoxInit and BallonInit. Committed providers are
called at their original positions: core BatimentResetAll/EnginResetAll,
combat ProjectileReset, economy SortilegeResetTechnologie. Callees without a
committed provider (TerrainReset, MiniMapReset, and MissionLoadName's
research/experience resets) are supplied explicitly or raise
DependenciaReinicio at their CALL site, keeping every earlier effect.
"""
from dataclasses import dataclass
import struct
import ambiente_missoes
from ciclo_estruturas import resetar_todas_estruturas
from ciclo_unidades import resetar_todas_unidades
from nome_missao import nome_arquivo_missao
from reinicio_projeteis import resetar_projeteis

ICONE=struct.pack('<HHH',0x29b1,1,0)
MODO=b'rb'
DIRETORIO_MUNDO=b'\\WORLD\\'
FILE_OPEN=0x458420
# (callee, MissionLoad CALL, MissionLoadName CALL)
CHAMADAS={'TerrainReset':(0x46b315,0x46c35f,0x46c60f),'MiniMapReset':(0x469f00,0x46c364,0x46c614),
          'SortilegeResetTechnologie':(0x4749f2,None,0x46c687),'RechercheReset':(0x470b46,None,0x46c68c),
          'Engin_ResetExperience':(0x441470,None,0x46c691),'RechercheCheat':(0x4716fe,None,0x46c6a6),
          'RechercheStore':(0x4714f0,None,0x46c6ab)}


class DependenciaReinicio(NotImplementedError):
    def __init__(self,rotina,chamador,caminho=None):
        self.rotina=rotina
        self.endereco=CHAMADAS[rotina][0]
        self.chamada=CHAMADAS[rotina][1 if chamador=='MissionLoad' else 2]
        self.chamador,self.caminho=chamador,caminho
        super().__init__(f'{rotina} 0x{self.endereco:x} has no supplied provider at {chamador} '
                         f'CALL 0x{self.chamada:x}; earlier reset effects retained')


class ForaDoDominioReinicio(ValueError):
    def __init__(self,mensagem,endereco):
        self.endereco=endereco
        super().__init__(f'{mensagem} (original 0x{endereco:x})')


def _vista(memoria,tamanho,nome):
    view=memoryview(memoria)
    if view.readonly or not view.c_contiguous or view.ndim!=1 or view.format!='B' or len(view)!=tamanho:
        raise ValueError(f'{nome} must be a writable contiguous u8 buffer of {tamanho} bytes')
    return view


def resetar_icones(icones,alterados):
    """IconeReset0x45e88f: ten 6-byte records at 0x4e2410; flag u8 0x4e05a2.

    For each record in order, a value other than (0x29b1,1,0) first stores 1
    in the flag; the record is then rewritten. The flag is never cleared.
    """
    view,flag=_vista(icones,60,'icones'),_vista(alterados,1,'icones_alterados')
    for indice in range(10):
        if view[indice*6:indice*6+6]!=ICONE:
            flag[0]=1
        view[indice*6:indice*6+6]=ICONE


def inicializar_caixas_mensagem(mensagens):
    """MessageBoxInit0x469908 over 0x4e7754..0x507d5a (132,614 bytes).

    u16 +0x20600 and +0x20602 = 0, u8 +0x20604 and +0x20605 = 0, then byte 0
    of each of the 256 records of 518 bytes. Other record bytes are kept.
    """
    view=_vista(mensagens,0x20606,'mensagens')
    view[0x20600:0x20606]=bytes(6)
    for indice in range(256):
        view[indice*0x206]=0


def inicializar_baloes(baloes):
    """BallonInit0x441b6c: four 8-byte records at 0x4e1a14; byte +3 is kept."""
    view=_vista(baloes,32,'baloes')
    for indice in range(4):
        p=indice*8
        view[p+4:p+8]=b'\xff\xff\xff\xff'
        view[p:p+3]=bytes(3)


@dataclass(frozen=True)
class MemoriaReinicio:
    """Inherited globals in original widths; core-consumed pools are bytearrays."""
    contadores: object            # 0x4e1a38, two u16
    icones: object                # 0x4e2410, 60
    icones_alterados: object      # 0x4e05a2, 1
    mensagens: object             # 0x4e7754, 132,614
    baloes: object                # 0x4e1a14, 32 (may be economy PropriedadeConstrucoes.baloes)
    estruturas: bytearray         # 0x49a0c8, 276,000
    estruturas_bandeiras: bytearray  # 0x49a070, 88
    estruturas_selecoes: bytearray   # 0x495be0, 8
    unidades: object              # core world exposing .unidades and .bolsas_tipos_unidades
    projeteis: object             # pool reached through 0x5080f0, 5,600
    missao: object                # 0x496fe4, 1


@dataclass(frozen=True)
class MemoriaReinicioNome:
    """MissionLoadName-only globals."""
    unidades_realizaveis: object  # 0x4e1934, 4x26
    estruturas_realizaveis: object  # 0x4dfad4, 4x22
    rede: int                     # inherited u8 0x4e0730 read by ReseauActif 0x42c3b0


@dataclass(frozen=True)
class ProvedoresReinicio:
    """Callables for callees without a committed provider; None raises at the CALL."""
    terreno: object=None
    minimapa: object=None
    tecnologia: object=None
    pesquisa: object=None
    experiencia: object=None
    pesquisa_trapaca: object=None
    pesquisa_guardar: object=None


@dataclass(frozen=True)
class PedidoAbertura:
    """FileOpen 0x458420 arguments; the open itself is the caller's binding."""
    caminho: bytes
    modo: bytes
    nome: bytes
    rotina_seguinte: int=FILE_OPEN


def _validar(memoria):
    for nome,largura in (('contadores',4),('icones',60),('icones_alterados',1),('mensagens',0x20606),
                         ('baloes',32),('projeteis',5600),('missao',1)):
        _vista(getattr(memoria,nome),largura,nome)
    for nome,largura in (('estruturas',276000),('estruturas_bandeiras',88),('estruturas_selecoes',8)):
        if not isinstance(getattr(memoria,nome),bytearray) or len(getattr(memoria,nome))!=largura:
            raise ValueError(f'{nome} must be a bytearray of {largura} bytes')
    u=getattr(memoria.unidades,'unidades',None);tabelas=getattr(memoria.unidades,'bolsas_tipos_unidades',None)
    if (not isinstance(u,bytearray) or len(u)!=220800 or not isinstance(tabelas,(tuple,list)) or len(tabelas)!=4
            or any(not isinstance(t,bytearray) or len(t)!=2704 for t in tabelas) or len({id(t) for t in tabelas})!=4):
        raise ValueError('unidades must expose 800 units and four distinct 2704-byte Bag pools')


def _texto_c(dados,limite,nome):
    dados=bytes(dados)
    fim=dados.find(b'\0')
    if fim<0 or fim>=limite:
        raise ValueError(f'{nome} must be a NUL-terminated string within {limite} bytes')
    return dados[:fim]


def _chamar(provedor,rotina,chamador,caminho=None):
    if provedor is None:
        raise DependenciaReinicio(rotina,chamador,caminho)
    return provedor()


def _resets_comuns(memoria,provedores,chamador,caminho):
    vista=_vista(memoria.contadores,4,'contadores')
    vista[:]=b'\xff\xff\xff\xff'
    resetar_icones(memoria.icones,memoria.icones_alterados)
    _chamar(provedores.terreno,'TerrainReset',chamador,caminho)
    _chamar(provedores.minimapa,'MiniMapReset',chamador,caminho)


def _resets_mundo(memoria):
    """Calls at 0x46c369..0x46c378 / 0x46c619..0x46c628, after MiniMapReset."""
    resetar_todas_estruturas(memoria.estruturas,memoria.estruturas_bandeiras,memoria.estruturas_selecoes)
    resetar_todas_unidades(memoria.unidades)
    resetar_projeteis(memoria.projeteis)
    inicializar_caixas_mensagem(memoria.mensagens)


def continuar_reinicio_missao(memoria,caminho):
    """MissionLoad continuation from 0x46c369 (after MiniMapReset) to the FileOpen stop."""
    _validar(memoria)
    _resets_mundo(memoria)
    inicializar_baloes(memoria.baloes)
    return PedidoAbertura(bytes(caminho),MODO,b'')


def resetar_para_missao(memoria,diretorio,provedores,*,variante_u8=None,simpatia=None):
    """MissionLoad 0x46c2cf..0x46c389.

    The mission number is the inherited u8 at 0x496fe4. diretorio is the
    inherited C string at 0x509594. Path = diretorio + MakeMissionName result,
    built in the 0x100-byte stack local before any global store.
    """
    _validar(memoria)
    if not isinstance(provedores,ProvedoresReinicio):
        raise ValueError('provedores must be a ProvedoresReinicio')
    base=_texto_c(diretorio,256,'diretorio')
    nome=nome_arquivo_missao(_vista(memoria.missao,1,'missao')[0],bytearray(0x2c),
                             variante_u8=variante_u8,simpatia=simpatia)
    caminho=base+nome
    if len(caminho)>=0x100:
        raise ForaDoDominioReinicio('Mission path overflows the 0x100-byte stack local',0x46c333)
    _resets_comuns(memoria,provedores,'MissionLoad',caminho)
    pedido=continuar_reinicio_missao(memoria,caminho)
    return PedidoAbertura(caminho,pedido.modo,nome)


def continuar_reinicio_missao_nome(memoria,extra,nome,diretorios,provedores):
    """MissionLoadName continuation from 0x46c619 (after MiniMapReset) to the FileOpen stop.

    diretorios maps 0x509494 and 0x509594 to their inherited C strings.
    """
    _validar(memoria)
    reais_u=_vista(extra.unidades_realizaveis,104,'unidades_realizaveis')
    reais_e=_vista(extra.estruturas_realizaveis,88,'estruturas_realizaveis')
    nome=_texto_c(nome,0x100,'nome')
    bases={chave:_texto_c(diretorios[chave],256,'diretorio') for chave in (0x509494,0x509594)}
    _resets_mundo(memoria)
    reais_u[:]=bytes(104)
    reais_e[:]=bytes(88)
    _chamar(provedores.tecnologia,'SortilegeResetTechnologie','MissionLoadName')
    _chamar(provedores.pesquisa,'RechercheReset','MissionLoadName')
    _chamar(provedores.experiencia,'Engin_ResetExperience','MissionLoadName')
    _vista(memoria.missao,1,'missao')[0]=0x32
    if extra.rede&255:
        _chamar(provedores.pesquisa_trapaca,'RechercheCheat','MissionLoadName')
        _chamar(provedores.pesquisa_guardar,'RechercheStore','MissionLoadName')
    inicializar_baloes(memoria.baloes)
    if len(nome)<4:
        raise ForaDoDominioReinicio('Name shorter than its 4-byte extension check',0x46c6c5)
    caminho=bases[0x509494 if nome[-4:].lower()==b'.net' else 0x509594]+DIRETORIO_MUNDO+nome
    if len(caminho)>=0x114:
        raise ForaDoDominioReinicio('Mission path overflows the stack local',0x46c742)
    return PedidoAbertura(caminho,MODO,nome)


def resetar_para_missao_nome(memoria,extra,nome,diretorios,provedores):
    """MissionLoadName 0x46c5e3..0x46c75f for an explicit name C string."""
    _validar(memoria)
    if not isinstance(provedores,ProvedoresReinicio):
        raise ValueError('provedores must be a ProvedoresReinicio')
    _vista(extra.unidades_realizaveis,104,'unidades_realizaveis')
    _vista(extra.estruturas_realizaveis,88,'estruturas_realizaveis')
    _texto_c(nome,0x100,'nome')
    for chave in (0x509494,0x509594):
        _texto_c(diretorios[chave],256,'diretorio')
    _resets_comuns(memoria,provedores,'MissionLoadName',None)
    return continuar_reinicio_missao_nome(memoria,extra,nome,diretorios,provedores)
