"""Remaining L7 auxiliary readers and the complete original auxiliary chain.

Caller order (both MissionLoad 0x46c57d.. and MissionLoadName 0x46c946..):
LoadMine, IALoadAttaqueIni, LoadBatimentGhost, LoadCadreInfluence,
LoadFinMission, LoadCalculMissionDivers, LoadObjectif, LoadEntrerMonstre,
then FileClose 0x45844c (not executed here). Raw tables only: no ghost,
influence, monster-spawn or AI semantics are interpreted.
"""
from dataclasses import dataclass
import struct
import ambiente_missoes
from candidatos_rota import aleatorio_caminhos
from carregador_auxiliares import _entrada,carregar_minas_e_ataques
from carregador_condicoes import carregar_condicoes_fim,carregar_objetivos
from formatos import Leitor

PERFIL=b'./monstre.ini'
SECAO=b'GENERAL'
# (CALL site, key, nDefault, monster-buffer offset of the stored result or None for HumanOnly)
INTEIROS=((0x47a665,b'HumanOnly',0,None),(0x47a688,b'ProbaCaveJoueur',5,4),
          (0x47a6a5,b'ProbaCaveIA',2,8),(0x47a6c7,b'ProbaEmbuscade',2,12))
_ESPACOS=b' \t\n\v\f\r'


class ForaDoDominioAuxiliar(ValueError):
    """Original continues past the declared buffer or supported CRT form; earlier effects stay."""
    def __init__(self,mensagem,endereco):
        self.endereco=endereco
        super().__init__(f'{mensagem} (original 0x{endereco:x})')


class DependenciaEntradaMonstros(NotImplementedError):
    def __init__(self,endereco):
        self.endereco=endereco
        super().__init__(f'InitEntrerMonstre needs the declared KERNEL32 profile binding at 0x{endereco:x}; '
                         'prior record initialization retained')


@dataclass(frozen=True)
class TabelaAuxiliarCarregada:
    quantidade: int
    tamanho: int
    fim: int
    rotina_seguinte: int
    retorno_al: int=None


@dataclass(frozen=True)
class EntradaMonstrosCarregada:
    quantidade_lida: int
    quantidade_final: int
    tamanho: int
    semente: int
    fim: int
    rotina_seguinte: int=0x45844c


def _leitor(leitor):
    if not isinstance(leitor,Leitor):
        raise ValueError('Leitor auxiliar incompatível')


def carregar_fantasmas_missao(leitor,fantasmas):
    """LoadBatimentGhost0x47bcc7 over 0x50b18c..0x50c612 (5254 bytes).

    +0 u16 count, +2 750 u16 IDs, +1502 two retained bytes, +1504 750 u32
    values, +4504 750 flag bytes. The count is stored by its read, then
    count flags become 0xff, then count (u16,u32) pairs are read in order.
    AL is 0 for an empty table, else 1; callers ignore it.
    """
    view=_entrada(leitor,fantasmas,5254)
    view[0:2]=leitor.ler(2)
    count=struct.unpack_from('<H',view,0)[0]
    for index in range(count):
        if index>=750:
            raise ForaDoDominioAuxiliar('Ghost flag beyond 750 slots',0x47bce1)
        view[4504+index]=255
    for index in range(count):
        view[2+index*2:4+index*2]=leitor.ler(2)
        view[1504+index*4:1508+index*4]=leitor.ler(4)
    return TabelaAuxiliarCarregada(count,6,leitor.posicao,0x47c04a,int(count!=0))


def carregar_influencia_missao(leitor,influencia):
    """LoadCadreInfluence0x47c04a over 0x50c614 (400x10 bytes).

    Words +0..+6 of every slot become 0xffff (+8/+9 retained), then u16
    count and u16 size go to stack locals (size is read even for count 0),
    then each record's size bytes are read at slot*10. Sizes above 10 overlap
    the next slot exactly as the original; writes past 4000 bytes are not
    supported (the original would reach the attack table at 0x50d5b4).
    """
    view=_entrada(leitor,influencia,4000)
    for index in range(400):
        view[index*10:index*10+8]=b'\xff'*8
    count,size=leitor.u16(),leitor.u16()
    for index in range(count):
        if index*10+size>4000:
            raise ForaDoDominioAuxiliar('Influence record beyond 4000-byte table',0x47c0b1)
        view[index*10:index*10+size]=leitor.ler(size)
    return TabelaAuxiliarCarregada(count,size,leitor.posicao,0x458b05)


def consumir_diversos_missao(leitor):
    """LoadCalculMissionDivers0x47c30f: 16 one-byte reads into stack scratch only."""
    _leitor(leitor)
    lidos=bytearray()
    for _ in range(16):
        lidos+=leitor.ler(1)
    return bytes(lidos)


def _sscanf_i(texto):
    """Watcom sscanf(texto,"%i") for the supported decimal subset: (converted, value)."""
    i=0
    while i<len(texto) and texto[i] in _ESPACOS:
        i+=1
    j=i+(texto[i:i+1] in (b'+',b'-'))
    k=j
    while k<len(texto) and 48<=texto[k]<=57:
        k+=1
    if k==j:
        return False,None
    if texto[j]==48 and (k-j>1 or texto[k:k+1] in (b'x',b'X')):
        raise ForaDoDominioAuxiliar('Octal/hexadecimal %i form is outside the supported subset',0x48c41c)
    valor=int(texto[j:k])*(-1 if texto[i:i+1]==b'-' else 1)
    if not -2**31<=valor<2**31:
        raise ForaDoDominioAuxiliar('Overflowing %i value is outside the supported subset',0x48c41c)
    return True,valor


def _iniciar_entrada_monstros(view,grupos,aleatorio,tipos,perfil):
    """InitEntrerMonstre0x47a601; core's Random0x4704dc updates the live state each call."""
    for index in range(100):
        p=20+index*12
        view[p:p+4]=b'\xff\xff\xff\xff'
        view[p+4:p+6]=b'\0\0'
        view[p+8:p+12]=bytes(4)
        semente=aleatorio_caminhos(struct.unpack_from('<I',aleatorio,0)[0])
        struct.pack_into('<I',aleatorio,0,semente)
        view[p+6]=semente&15
    view[0]=0
    for endereco,chave,padrao,destino in INTEIROS:
        if perfil is None:
            raise DependenciaEntradaMonstros(endereco)
        valor=perfil.inteiro(SECAO,chave,padrao,PERFIL)&0xffffffff
        if destino is None:
            if valor:
                view[0]=1
        else:
            struct.pack_into('<I',view,destino,valor)
    grupos[:]=bytes(432)
    for grupo in range(16):
        texto=bytes(perfil.texto(SECAO,b'GROUPE%02d'%grupo,b'',256,PERFIL))
        posicao=0
        while texto:
            virgula=texto.find(b',',posicao)
            convertido,valor=_sscanf_i(texto[posicao:])
            if convertido:
                if not 0<=valor<8:
                    raise ForaDoDominioAuxiliar('Group monster index outside table 0x498400[0..7]',0x47a7c9)
                grupos[416+grupo]=(grupos[416+grupo]+1)&255
                tipo=grupo*26+tipos[valor]
                grupos[tipo]=(grupos[tipo]+1)&255
            if virgula<0:
                break
            posicao=virgula+1


def carregar_entrada_monstros_missao(leitor,monstros,grupos,aleatorio,*,tipos_grupo8,perfil):
    """LoadEntrerMonstre0x47ac30, including its InitEntrerMonstre call.

    monstros: 0x50a9bc..0x50ae80 (1220 bytes): +0 HumanOnly u8, +4/+8/+12
    profile dwords, +18 u16 count, +20 100x12 records. grupos: 0x50af84
    (16x26 type counts, then 16 group counts). aleatorio is the live u32
    Random state at 0x497164 (4 bytes) and tipos_grupo8 the inherited bytes
    0x498400..0x498408; both are explicit inputs, never defaults.
    """
    view=_entrada(leitor,monstros,1220);groups=_entrada(leitor,grupos,432);state=_entrada(leitor,aleatorio,4)
    if not isinstance(tipos_grupo8,(bytes,bytearray)) or len(tipos_grupo8)!=8:
        raise ValueError('InitEntrerMonstre requires the explicit 8-byte type table')
    _iniciar_entrada_monstros(view,groups,state,bytes(tipos_grupo8),perfil)
    view[18:20]=leitor.ler(2)
    count=struct.unpack_from('<H',view,18)[0]
    size=leitor.u16()
    for index in range(count):
        p=20+index*12
        if index>=100 or index*12+size>1200:
            raise ForaDoDominioAuxiliar('Monster entry beyond 100x12 records',0x47ac9b)
        view[p:p+size]=leitor.ler(size)
        struct.pack_into('<H',view,p+4,struct.unpack_from('<H',view,p+4)[0]*30&0xffff)
        mascara,bit=struct.unpack_from('<H',view,p+2)[0],view[p+6]
        view[p+8:p+12]=bytes(4)
        for _ in range(16):
            bit=(bit+1)&15
            if mascara>>bit&1:
                break
        else:
            bit=255
        view[p+6]=bit
    # Backward pass: trailing empty word0 (0xffff) slots drop the count; a used
    # slot moves only its word0 into the highest lower empty slot. No empty slot
    # below a used one ends the pass. Other record bytes are not moved.
    atual=count-1
    while atual>=0:
        origem=20+atual*12
        if struct.unpack_from('<H',view,origem)[0]!=0xffff:
            for vazio in range(atual-1,-1,-1):
                destino=20+vazio*12
                if struct.unpack_from('<H',view,destino)[0]==0xffff:
                    view[destino:destino+2]=view[origem:origem+2]
                    break
            else:
                break
        struct.pack_into('<H',view,18,(struct.unpack_from('<H',view,18)[0]-1)&0xffff)
        atual-=1
    return EntradaMonstrosCarregada(count,struct.unpack_from('<H',view,18)[0],size,
                                    struct.unpack_from('<I',state,0)[0],leitor.posicao)


@dataclass(frozen=True)
class BuffersCadeiaAuxiliar:
    """Writable views of the inherited tables, in original memory widths."""
    minas: object          # 0x509954, 80
    ataques: object        # 0x50d5b4, 1004
    fantasmas: object      # 0x50b18c, 5254
    influencia: object     # 0x50c614, 4000
    condicoes_fim: object  # 0x4e1d20, 114
    objetivos: object      # 0x511ffc, 804
    monstros: object       # 0x50a9bc, 1220
    grupos: object         # 0x50af84, 432
    aleatorio: object      # 0x497164, 4 (live Random state)


@dataclass(frozen=True)
class CadeiaAuxiliarCarregada:
    minas: int
    ataques: int
    fantasmas: TabelaAuxiliarCarregada
    influencia: TabelaAuxiliarCarregada
    condicoes_fim: object
    diversos: bytes
    objetivos: object
    monstros: EntradaMonstrosCarregada
    semente: int
    fim: int
    rotina_seguinte: int=0x45844c


_LARGURAS=(('minas',80),('ataques',1004),('fantasmas',5254),('influencia',4000),('condicoes_fim',114),
           ('objetivos',804),('monstros',1220),('grupos',432),('aleatorio',4))


def carregar_cadeia_auxiliar(leitor,buffers,*,tipos_grupo8,perfil):
    """Complete original L7 order; all shape guards precede the first effect."""
    _leitor(leitor)
    for nome,largura in _LARGURAS:
        _entrada(leitor,getattr(buffers,nome),largura)
    if not isinstance(tipos_grupo8,(bytes,bytearray)) or len(tipos_grupo8)!=8:
        raise ValueError('InitEntrerMonstre requires the explicit 8-byte type table')
    iniciais=carregar_minas_e_ataques(leitor,buffers.minas,buffers.ataques)
    fantasmas=carregar_fantasmas_missao(leitor,buffers.fantasmas)
    influencia=carregar_influencia_missao(leitor,buffers.influencia)
    fim=carregar_condicoes_fim(leitor,buffers.condicoes_fim)
    diversos=consumir_diversos_missao(leitor)
    objetivos=carregar_objetivos(leitor,buffers.objetivos)
    monstros=carregar_entrada_monstros_missao(leitor,buffers.monstros,buffers.grupos,buffers.aleatorio,
                                              tipos_grupo8=tipos_grupo8,perfil=perfil)
    return CadeiaAuxiliarCarregada(iniciais.minas,iniciais.ataques,fantasmas,influencia,fim,diversos,
                                   objetivos,monstros,monstros.semente,leitor.posicao)
