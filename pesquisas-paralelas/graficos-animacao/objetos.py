"""Objetos 1..22 e 28..52: dois passes de desenho, fases das árvores e associação ETA.

Biblioteca padrão; sem execução x86. Os nomes árvores/pedras são descrições
visuais, não classificações econômicas nem regras de coleta.
"""
import hashlib
import struct
from graficos import localizar, compor_indices
from composicao import compor_sombra

# (base CMP, dx, dy, operação), em ordem original: corpo e depois sombra.
ARVORES = {
 1: [(0x291d,2,-27,'copiar'),(0x2939,9,13,'sombra')],
 2: [(0x2919,-4,-36,'copiar'),(0x2935,6,21,'sombra')],
 3: [(0x2915,-3,-83,'copiar'),(0x2931,16,6,'sombra')],
 4: [(0x2915,3,-89,'copiar'),(0x2931,22,0,'sombra'),(0x291d,-3,-19,'copiar'),(0x2939,4,21,'sombra')],
 5: [(0x2915,-4,-91,'copiar'),(0x2931,15,-2,'sombra'),(0x291d,-7,-24,'copiar'),(0x2939,0,16,'sombra'),(0x2919,15,-34,'copiar'),(0x2935,25,23,'sombra')],
 6: [(0x2929,-4,-25,'copiar'),(0x2945,9,16,'sombra')],
 7: [(0x2925,-7,-43,'copiar'),(0x2941,14,14,'sombra')],
 8: [(0x2921,-11,-65,'copiar'),(0x293d,12,13,'sombra')],
 9: [(0x2921,-15,-75,'copiar'),(0x293d,8,3,'sombra'),(0x2929,7,-17,'copiar'),(0x2945,20,24,'sombra')],
 10:[(0x2921,-7,-74,'copiar'),(0x293d,16,4,'sombra'),(0x2925,-18,-40,'copiar'),(0x2941,3,17,'sombra'),(0x2929,11,-17,'copiar'),(0x2945,24,24,'sombra')],
 11:[(0x292d,-5,-36,'copiar'),(0x2949,14,14,'sombra')],
}
BAIXOS = {12:(0,0),13:(16,16),14:(0,0),15:(18,11),16:(18,0),
          17:(18,25),18:(0,25),19:(0,0),20:(0,0),21:(-3,-5),22:(-1,-1)}

CODIGOS = tuple(range(1,23))+tuple(range(28,53))


def _u8(v,n):
    if type(v) is not int or not 0<=v<=255:raise ValueError(n+' deve ser u8')


def visibilidade(descoberta_u8,iluminacao_u8):
    _u8(descoberta_u8,'descoberta');_u8(iluminacao_u8,'iluminação')
    return dict(descoberto=(descoberta_u8&31)==0,iluminado=(iluminacao_u8&16)==0)


def consultar_objeto(codigo,*,auxiliar_u8,descoberta_u8,iluminacao_u8):
    """Retorna cada passe separadamente. Não autoriza reordenar toda a cena.

    Auxiliar 0..3 nas árvores é o índice de fase; nos objetos de solo ele é ignorado.
    Para árvore fora dessa faixa, recusa associação em vez de invadir outra sequência.
    Flags são bytes das camadas do jogador (não atributos de colisão do ETA).
    """
    if type(codigo) is not int or codigo not in CODIGOS:
        raise NotImplementedError('Somente objetos 1..22 e 28..52 validados')
    _u8(auxiliar_u8,'auxiliar')
    if codigo in ARVORES and auxiliar_u8>3:raise ValueError('Fase de árvore validada somente em 0..3')
    vis=visibilidade(descoberta_u8,iluminacao_u8)
    p=dict(codigo=codigo,auxiliar_u8=auxiliar_u8,descoberta_u8=descoberta_u8,iluminacao_u8=iluminacao_u8,
           **vis,classe_visual='arvore' if codigo in ARVORES else ('vegetacao_baixa' if codigo in BAIXOS else 'objeto_de_solo'),
           classificacao_visual='inferência de aparência; sem regra econômica',terreno=[],sprites=[])
    if not vis['descoberto']:return p
    if codigo in ARVORES:
        for ordem,(base,x,y,op) in enumerate(ARVORES[codigo]):
            if op=='copiar' and not vis['iluminado']:base+=92
            p['sprites'].append(dict(**localizar(base+auxiliar_u8),ordem=ordem,x=x,y=y,operacao=op,
                sequencia=list(range(base,base+4)),fase=auxiliar_u8,
                evidencia='AffVeget 0x415acf, ramos 0x415f55..0x416864',confianca='codigo_e_comparacao_x86'))
    else:
        x,y=BAIXOS.get(codigo,(0,0));mid=(0x2941 if codigo in BAIXOS else 0x293c)+codigo+(0 if vis['iluminado'] else 64)
        p['terreno'].append(dict(**localizar(mid),ordem=0,x=x,y=y,operacao='copiar',sequencia=[mid],fase=None,
            evidencia='AffVegetTerrain 0x410085..0x41068e',confianca='codigo_e_comparacao_x86'))
    return p


def compor_passe(catalogo,destino,largura,altura,plano,passe,x,y,*,tabela_sombra,recorte=None):
    """Compor somente 'terreno' ou 'sprites', na ordem capturada do respectivo passe."""
    if passe not in ('terreno','sprites'):raise ValueError('Passe inválido')
    if len(destino)!=largura*altura or len(tabela_sombra)!=256:raise ValueError('Buffer/tabela inválidos')
    out=bytes(destino)
    for q in plano[passe]:
        frame=catalogo.quadro(q['id_motor']);xx=x+q['x'];yy=y+q['y']
        if q['operacao']=='sombra':out=compor_sombra(out,largura,altura,frame,xx,yy,tabela_sombra,recorte)
        elif q['operacao']=='copiar':out=compor_indices(out,largura,altura,frame,xx,yy,recorte)
        else:raise NotImplementedError('Operação não validada')
    return out


def avancar_arvore(*,fase_u8,relogio_u32,indice_aleatorio_u8,tabela_aleatoria):
    """NextAnimVeget para uma árvore 1..11; ordem da varredura vem do consumidor.

    Tabela e cursor são entradas, pois a rotina consome estado aleatório global.
    Não pressupõe probabilidade nem inventa sequência aleatória. Aceita fase u8
    bruta para comparação do avanço; o renderer só aceita fases resultantes 0..3.
    """
    _u8(fase_u8,'fase');_u8(indice_aleatorio_u8,'cursor')
    if type(relogio_u32) is not int or not 0<=relogio_u32<=0xffffffff:raise ValueError('Relógio deve ser u32')
    if len(tabela_aleatoria)!=256:raise ValueError('Tabela aleatória deve ter 256 bytes')
    for v in tabela_aleatoria:_u8(v,'valor aleatório')
    if relogio_u32&3:return dict(fase=fase_u8,indice=indice_aleatorio_u8,consumiu=False)
    valor=tabela_aleatoria[indice_aleatorio_u8]
    return dict(fase=(fase_u8+1)&3 if valor&3==0 else fase_u8,
                indice=(indice_aleatorio_u8+1)&255,consumiu=True)


def ler_objetos_eta(dados):
    """Lê as duas camadas serializadas de V0.3; sem pós-processamento de MissionLoad."""
    if len(dados)<0x50004 or dados[:4]!=b'V0.3':raise ValueError('ETA V0.3 truncado/inválido')
    objetos=dados[0x30004:0x40004];aux=dados[0x40004:0x50004]
    return dict(sha256_objetos=hashlib.sha256(objetos).hexdigest(),sha256_auxiliares=hashlib.sha256(aux).hexdigest(),
        registros=[dict(celula=i,x=i%256,y=i//256,codigo=v,auxiliar_u8=aux[i],
            offset_objeto=0x30004+i,offset_auxiliar=0x40004+i,
            id_terreno=struct.unpack_from('<H',dados,0x10004+i*2)[0],mapeado=v in CODIGOS)
            for i,v in enumerate(objetos) if v])
