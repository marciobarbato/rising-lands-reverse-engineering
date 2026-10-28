"""Composição indexada independente. Nenhuma função depende de x86/Unicorn.

Escopo: cinco tipos validados; corpo normal, máscara de sombra e despacho.
Percentual e ciclos são entradas explícitas: não presumimos estado global.
"""
from graficos import TIPOS, consultar, localizar, compor_indices

SOMBRA_ID = 10784
ROTINAS = {
    'corpo_base': 0x412390, 'ataque_nao_mapeado': 0x41374c,
    'construcao_nao_mapeada': 0x414495, 'trabalho_nao_mapeado': 0x414a8a,
    'morte_nao_mapeada': 0x41559a, 'sem_desenho': None,
}


def _u8(v, nome):
    if type(v) is not int or not 0 <= v <= 255:
        raise ValueError(nome+' deve ser um inteiro em 0..255')


def encaminhamento(tipo, estado_u8, *, auxiliar_8a=None):
    """AffEngin, sem executar os handlers de ataque/trabalho/construção/morte.

    Sem desenho significa retorno desta função, não invisibilidade no jogo.
    A fase bruta +0xa4 não é substituída pela fase de parada pelo renderer.
    """
    if type(tipo) is not int or tipo not in TIPOS:
        raise NotImplementedError('Despacho validado somente para tipos 0,5,6,7,9')
    _u8(estado_u8, 'estado_u8')
    if auxiliar_8a is not None:
        _u8(auxiliar_8a, 'auxiliar_8a')
    estado = estado_u8
    rota = 'sem_desenho'
    if estado in (1, 22, 24):
        if auxiliar_8a is None:
            raise ValueError('Este estado exige o byte +0x8a; não presumir zero')
        if auxiliar_8a == 0:
            rota = 'corpo_base'
        elif auxiliar_8a <= (1 if estado == 22 else 3):
            rota = 'ataque_nao_mapeado'
    elif estado in (2,3,6,7,8,9,13,16,17,18,19,20,21,23,30):
        rota = 'corpo_base'
    elif estado == 4:
        rota = 'morte_nao_mapeada'
    elif estado == 5:
        rota = 'trabalho_nao_mapeado'
    elif estado in (11,15):
        rota = 'construcao_nao_mapeada'
    return dict(tipo=tipo, estado_u8=estado, auxiliar_8a=auxiliar_8a,
                rota=rota, funcao=hex(ROTINAS[rota]) if ROTINAS[rota] else None,
                evidencia='AffEngin 0x41591f..0x415a57',
                confianca='confirmada_codigo_e_comparacao_x86')


def tabela_sombra(paleta, *, percentual, ciclos):
    """CalculOmbrage: alvo RGB, distância quadrática, empate pelo menor índice.

    ciclos: pares inclusivos a excluir da busca (0 continua candidato inicial).
    percentual: DL original, u8; cálculo por componente truncado em u8.
    Exceções 5..15 são constantes originais, não uma operação RGB uniforme.
    """
    if len(paleta) != 768:
        raise ValueError('Paleta RGB deve conter 768 bytes')
    _u8(percentual, 'percentual')
    ciclos = tuple(ciclos)
    if len(ciclos) > 255:
        raise ValueError('Mais de 255 intervalos de ciclo')
    for a, b in ciclos:
        _u8(a, 'início do ciclo'); _u8(b, 'fim do ciclo')
        if a > b:
            raise ValueError('Intervalo de ciclo invertido')
    cores = [tuple(paleta[i:i+3]) for i in range(0,768,3)]
    candidatos = [0]+[i for i in range(1,256) if not any(a <= i <= b for a,b in ciclos)]
    saida = bytearray()
    for i, cor in enumerate(cores):
        if 5 <= i <= 7:
            saida.append(228-i)
        elif 8 <= i <= 15:
            saida.append(167)
        else:
            alvo = tuple((v*percentual//100) & 255 for v in cor)
            distancias = [sum((a-b)**2 for a,b in zip(alvo,c)) for c in cores]
            saida.append(min(candidatos, key=distancias.__getitem__))
    return bytes(saida)


def compor_sombra(destino, largura, altura, quadro, x, y, tabela, recorte=None):
    """PasteOmbreCmp: só a máscara CMP importa; remapeia o índice de destino."""
    if len(destino) != largura*altura or len(tabela) != 256:
        raise ValueError('Superfície ou tabela inválida')
    l,t,r,b = recorte if recorte is not None else (0,0,largura-1,altura-1)
    l,t,r,b = max(l,0),max(t,0),min(r,largura-1),min(b,altura-1)
    saida = bytearray(destino)
    for sy in range(max(0,t-y),min(quadro.altura,b-y+1)):
        for sx in range(max(0,l-x),min(quadro.largura,r-x+1)):
            if quadro.opacidade[sy*quadro.largura+sx]:
                p = (y+sy)*largura+x+sx
                saida[p] = tabela[saida[p]]
    return bytes(saida)


def compor_unidade(catalogo, destino, largura, altura, *, tipo, estado_u8,
                   direcao, fase, x, y, tabela, bolsa_u16=None, auxiliar_8a=None,
                   dx=0, dy=0, recorte=None):
    """Sombra → corpo normal. x/y: origem da célula já projetada em pixels.

    Somente jogador 0, efeitos/indicadores inativos (+0x74=100, +0xba=0).
    Fase é o byte efetivo, inclusive
    em estado 7; use consultar(...,'parado') antes se quiser parada estabelecida.
    Retorna (superfície, plano). Não interpreta pós-processamento ETA.
    """
    rota = encaminhamento(tipo,estado_u8,auxiliar_8a=auxiliar_8a)
    if len(destino) != largura*altura:
        raise ValueError('Superfície inválida')
    plano = dict(**rota,camadas=[])
    if rota['rota'] == 'sem_desenho':
        return bytes(destino), plano
    if rota['rota'] != 'corpo_base':
        raise NotImplementedError('Handler de desenho ainda não mapeado: '+rota['rota'])
    for v in (dx,dy):
        if type(v) is not int or not -128 <= v <= 127:
            raise ValueError('Deslocamentos devem ser i8')
    m = consultar(tipo,'andando',direcao,fase,bolsa_u16=bolsa_u16)
    ax,ay = TIPOS[tipo]['ancora']
    sombra = dict(**localizar(SOMBRA_ID),x=x+dx+2,y=y+dy+26,operacao='remapear_destino')
    corpo = dict(**localizar(m['id_motor']),x=x+dx-ax,y=y+dy-ay,operacao='copiar_opacos')
    saida = compor_sombra(destino,largura,altura,catalogo.quadro(SOMBRA_ID),
                          sombra['x'],sombra['y'],tabela,recorte)
    saida = compor_indices(saida,largura,altura,catalogo.quadro(m['id_motor']),
                           corpo['x'],corpo['y'],recorte)
    plano['camadas'] = [sombra,corpo]
    return saida,plano
