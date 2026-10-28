"""Comandos de grupos de portões e avanço do estado físico, sem desenho.

Preserva o contador +0x76 e os efeitos sobre colisão/regiões. Sprites, seleção
pelo cursor e frequência global das chamadas permanecem contratos externos.
"""
import struct
from colocacao_estruturas import _objeto


def _registro(mundo, indice):
    indice &= 65535
    if indice >= 1000:
        raise ValueError('Índice de estrutura fora de 0..999')
    return indice,indice*276


def portao_em_transicao(mundo, indice):
    _,p=_registro(mundo,indice)
    return mundo.estruturas[p+0x76] not in (0,15,31)


def portao_na_fase15(mundo, indice):
    _,p=_registro(mundo,indice)
    return mundo.estruturas[p+0x76]==15


def portao_na_fase0_31(mundo, indice):
    _,p=_registro(mundo,indice)
    return mundo.estruturas[p+0x76] in (0,31)


def portao_horizontal(mundo, indice):
    _,p=_registro(mundo,indice)
    return struct.unpack_from('<H',mundo.estruturas,p+0x7c)[0]==0


def _incrementar(mundo, indice):
    _,p=_registro(mundo,indice)
    mundo.estruturas[p+0x76]=(mundo.estruturas[p+0x76]+1)&255


def solicitar_liberacao_portoes(mundo, celula, indice):
    """BaisseTouteHerse, 0x4193d4: incrementa contadores pela grade de regiões.

    Só exige objeto de portão e rótulo de estrutura; não testa dono/tipo/estado.
    Conserva os limites assimétricos da varredura original.
    """
    _registro(mundo,indice)
    celula &= 65535
    horizontal=portao_horizontal(mundo,indice)
    passo=1 if horizontal else 256
    eixo=(lambda c:c&255) if horizontal else (lambda c:c>>8)
    portao=mundo.objeto_portao&255
    for _ in range(256):
        if _objeto(mundo,celula-passo)==portao:
            celula=(celula-passo)&65535
        else:
            break
        if eixo(celula)==0:break
    else:raise NotImplementedError('Varredura de portões excedeu o domínio de uma linha')
    for _ in range(256):
        if _objeto(mundo,celula)!=portao:break
        valor=mundo.regioes[celula]
        if valor&0x8000:_incrementar(mundo,(valor&0x7fe0)>>5)
        celula=(celula+passo)&65535
        if eixo(celula)==255:break
    else:raise NotImplementedError('Varredura de portões excedeu o domínio de uma linha')


def solicitar_bloqueio_portoes(mundo, celula, indice):
    """RemonteTouteHerse, 0x4195ca: lista de 255 posições, recusa se ocupada.

    A atualização procura as origens nos 1.000 registros, sem usar rótulos,
    dono, tipo ou atividade. Slots repetidos causam incrementos repetidos.
    """
    _registro(mundo,indice)
    celula &= 65535
    horizontal=portao_horizontal(mundo,indice)
    passo=1 if horizontal else 256
    portao=mundo.objeto_portao&255
    lista=[0xffff]*255
    lista[0]=celula
    n=0
    # No ramo vertical o teste de parada continua usando x, como no x86.
    x=celula&255
    for _ in range(256):
        atual=lista[n]
        if _objeto(mundo,atual-passo)==portao:
            if n+1>=255:raise NotImplementedError('Grupo excede os 255 slots originais')
            n+=1;lista[n]=(atual-passo)&65535
            if horizontal:x=lista[n]&255
        else:break
        if x==0:break
    else:raise NotImplementedError('Varredura de portões excedeu uma linha')
    lista[0]=lista[n]
    n=0
    for _ in range(256):
        atual=lista[n]
        if _objeto(mundo,atual+passo)==portao:
            if n+1>=255:raise NotImplementedError('Grupo excede os 255 slots originais')
            n+=1;lista[n]=(atual+passo)&65535
        else:break
        eixo=(lista[n]&255) if horizontal else lista[n]>>8
        if eixo==0:break
    else:raise NotImplementedError('Varredura de portões excedeu uma linha')
    if any(c!=0xffff and mundo.atributos[c]&1 for c in lista):return
    for i in range(1000):
        origem=struct.unpack_from('<H',mundo.estruturas,i*276+2)[0]
        for c in lista:
            if c!=0xffff and c==origem:_incrementar(mundo,i)


def alternar_portoes(mundo, celula, indice):
    """ChercheEtatHerse, 0x419917: ignora transição; escolhe pelo contador."""
    if portao_em_transicao(mundo,indice):return
    if portao_na_fase15(mundo,indice):solicitar_bloqueio_portoes(mundo,celula,indice)
    else:solicitar_liberacao_portoes(mundo,celula,indice)


def avancar_estado_portao(mundo, indice):
    """Ramo tipo 12 de BatimentNextEtape, após a entrada opcional de mouse.

    Ao chegar a 15 libera a célula; ao voltar a zero insere o bloqueio. Não
    escolhe quadros visuais nem converte a frequência das chamadas em tempo.
    """
    indice,p=_registro(mundo,indice)
    if mundo.estruturas[p+8]!=12:
        raise ValueError('Avanço específico para estruturas do tipo 12')
    if not portao_em_transicao(mundo,indice):return
    nova=(mundo.estruturas[p+0x76]+1)&255
    if nova>=31:nova=0
    mundo.estruturas[p+0x76]=nova
    celula=struct.unpack_from('<H',mundo.estruturas,p+2)[0]
    if nova==15:
        mundo.atributos[celula]&=254
        mundo.modificar_regiao_estrutura(indice,0,celula,False)
    elif nova==0:
        mundo.atributos[celula]|=1
        mundo.modificar_regiao_estrutura(indice,0,celula,True)
