"""Santuário tipo 2: fachada habitada, modo 5, sem indicadores auxiliares.

API Python independente. Não implementa ocupação, produção, dano ou IA.
"""
import struct
import hashlib
from graficos import Catalogo, Quadro, localizar, compor_indices

TIPO = 2
BASE_TERRENO = 732
TAMANHO = (6,5)
GATILHO = (5,2)
ANCORA_GATILHO = (150,93)
# Original 0x496d4c: apenas três faixas de oito índices são usadas.
FAIXAS_JOGADORES = ((144,145,146,148,149,150,253,254),
                   (136,137,138,139,140,141,142,143),
                   (48,50,52,54,56,58,59,61))


def _inteiro(v, minimo, maximo, nome):
    if type(v) is not int or not minimo <= v <= maximo:
        raise ValueError(f'{nome} deve estar em {minimo}..{maximo}')


def avancar_relogios(relogios):
    """Prefixo de ProgIteration: três dwords; não pressupõe taxa em segundos."""
    if len(relogios)!=3:raise ValueError('Três relógios esperados')
    for v in relogios:_inteiro(v,0,0xffffffff,'relógio')
    a,b,c=relogios;a=(a+1)&0xffffffff
    if a%2==0:b=(b+1)&0xffffffff
    if a%3==0:c=(c+1)&0xffffffff
    return a,b,c


def tabelas_jogador(faixas=FAIXAS_JOGADORES):
    """CalculTabPlayer: paletas 0..4, com faixas 1..3 transcritas do EXE.

    O consumidor recebe faixas de identidade-construcoes.json na entrega.
    A tabela 0 é identidade; 1..3 mudam somente 160..167; 4 usa índice 47.
    """
    if len(faixas)!=3 or any(len(f)!=8 for f in faixas):
        raise ValueError('Três faixas de oito índices esperadas')
    for f in faixas:
        for v in f:_inteiro(v,0,255,'índice')
    tabelas=[bytearray(range(256)) for _ in range(5)]
    for jogador,f in enumerate(faixas,1):tabelas[jogador][160:168]=bytes(f)
    tabelas[4][160:168]=bytes([47])*8
    return tuple(bytes(t) for t in tabelas)


def consultar_santuario(*, tipo=2, modo=5, habitado, jogador, relogios, celula_mapa,
                        auxiliar_06=0):
    """Plano da fachada até 0x40f342; sem fogo, seleção, barras ou ordem global.

    habitado é resultado externo de BatimentEstHabiter, não uma regra inferida.
    Relógios: dwords 0x508f7c, 0x508f80, 0x508f84, nessa ordem.
    celula_mapa é a coordenada absoluta (x,y) do gatilho no mapa 256×256.
    Posições relativas à origem da célula que dispara o desenho (5,2 no terreno).
    """
    if type(tipo) is not int or tipo!=2 or type(modo) is not int or modo!=5:
        raise NotImplementedError('Somente Santuário tipo 2, modo 5')
    if habitado is not True:
        raise NotImplementedError('Fachada não habitada ainda depende do efeito cinza')
    if type(auxiliar_06) is not int or auxiliar_06!=0:
        raise NotImplementedError('Camada auxiliar +0x06 diferente de zero não validada')
    _inteiro(jogador,0,4,'jogador')
    if len(relogios)!=3:raise ValueError('Três relógios esperados')
    for v in relogios:_inteiro(v,0,0xffffffff,'relógio')
    if len(celula_mapa)!=2:raise ValueError("Célula deve ter x,y")
    for v in celula_mapa:_inteiro(v,0,255,"coordenada da célula")
    celula=celula_mapa[1]*256+celula_mapa[0]
    a,b,c=relogios
    # [esp] preserva EBX de entrada: célula y*256+x, não o jogador.
    # Ordem e offsets em 0x4087bf..0x408923.
    defs=[('corpo',7032,0,0,'jogador',None,1),
          ('detalhe_alto',7049+((c+celula)&7),74,5,'jogador',2,8),
          ('detalhe_central',7033+((a+celula)&7),89,95,'copiar',0,8),
          ('detalhe_direito',7041+((b+celula)&7),151,131,'copiar',1,8),
          ('bandeira_esquerda',7059+(a&7),48,64,'jogador',0,8),
          ('bandeira_direita',7067+(a&7),144,74,'jogador',0,8),
          ('detalhe_esquerdo',7057+((a+celula)&1),18,63,'copiar',0,2)]
    camadas=[]
    for ordem,(papel,ident,x,y,op,rel,qtd) in enumerate(defs):
        camadas.append(dict(ordem=ordem,papel=papel,**localizar(ident),
            x=x-150,y=y-93,operacao=op,jogador=jogador if op=='jogador' else None,
            relogio=rel,quantidade_quadros=qtd,
            confianca='confirmada_codigo_e_comparacao_x86',evidencia='0x4087bf..0x408923'))
    return dict(tipo=2,chave_ini='SANCTUAIRE',nome='SANTUÁRIO',modo=5,habitado=True,
                jogador=jogador,relogios=list(relogios),celula_mapa=list(celula_mapa),
                celula_gatilho=list(GATILHO),
                terreno_base=BASE_TERRENO,dimensoes_celulas=list(TAMANHO),
                ancoragem_gatilho=list(ANCORA_GATILHO),camadas=camadas)


def compor_fachada(catalogo,destino,largura,altura,plano,x_gatilho,y_gatilho,*,tabelas,recorte=None):
    """Camadas da fachada, sobre fundo fornecido; não compõe a cena inteira."""
    saida=bytes(destino)
    if len(tabelas)!=5 or any(len(t)!=256 for t in tabelas):raise ValueError('Cinco tabelas de 256 bytes esperadas')
    for camada in plano['camadas']:
        q=catalogo.quadro(camada['id_motor'])
        if camada['operacao']=='jogador':
            q=Quadro(q.largura,q.altura,q.pixels.translate(tabelas[camada['jogador']]),q.opacidade,0,b'')
        elif camada['operacao']!='copiar':raise NotImplementedError('Operação não validada')
        saida=compor_indices(saida,largura,altura,q,x_gatilho+camada['x'],y_gatilho+camada['y'],recorte)
    return saida


def ler_estruturas_eta(dados):
    """Bloco 0 de V0.3, estritamente tamanho 204; preserva bytes e hashes."""
    if dados[:4]!=b'V0.3' or len(dados)<0x50034:raise ValueError('ETA inválido')
    n,t=struct.unpack_from('<HH',dados,0x50030)
    if t!=204 or len(dados)<0x50034+n*(t+2):raise ValueError('Bloco de estruturas não suportado')
    out=[]
    for i in range(n):
        p=0x50034+i*(t+2);indice=struct.unpack_from('<H',dados,p)[0];raw=dados[p+2:p+2+t]
        if indice>=1000:raise ValueError('Índice de estrutura fora do pool')
        out.append(dict(indice=indice,offset_registro=p+2,bytes=raw,
            sha256=hashlib.sha256(raw).hexdigest(),tipo=raw[8],modo=raw[5],jogador=raw[4],
            origem_celula=(raw[2],raw[3]),auxiliar_06=struct.unpack_from('<H',raw,6)[0]))
    return out
