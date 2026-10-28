"""Objetos 54/66/67/68: associação gráfica, sem atualização econômica.

As sequências 66..68 têm 16 quadros, escolhidos por auxiliar//2. A origem e
as alterações desse auxiliar são entradas externas. Só biblioteca padrão.
"""
from graficos import localizar
from objetos import CODIGOS, consultar_objeto, ler_objetos_eta, visibilidade

CODIGOS_SEQUENCIAIS = (54, 66, 67, 68)
CODIGOS_V6 = tuple(sorted(CODIGOS + CODIGOS_SEQUENCIAIS))


def consultar_sequencial(codigo, *, auxiliar_u8, descoberta_u8, iluminacao_u8):
    if type(codigo) is not int or codigo not in CODIGOS_SEQUENCIAIS:
        raise NotImplementedError('Somente objetos 54/66/67/68 neste contrato')
    if type(auxiliar_u8) is not int or not 0 <= auxiliar_u8 <= 255:
        raise ValueError('Auxiliar deve ser u8')
    if codigo != 54 and auxiliar_u8 > 31:
        raise ValueError('Sequência validada de 16 quadros: auxiliar 0..31')
    vis = visibilidade(descoberta_u8, iluminacao_u8)
    fase = 0 if codigo == 54 else auxiliar_u8 // 2
    base = 0x2a47 + (0 if codigo == 54 else (codigo - 66) * 16)
    mid = base + fase
    dx = -4 if codigo in (54, 66) else 0
    plano = dict(codigo=codigo, auxiliar_u8=auxiliar_u8,
        descoberta_u8=descoberta_u8, iluminacao_u8=iluminacao_u8, **vis,
        classe_visual={54:'fragmentos_cinzentos',66:'fragmentos_cinzentos',
                       67:'formas_alaranjadas',68:'blocos_cinzentos'}[codigo],
        classificacao_visual='inferência de aparência; sem regra econômica',
        fase=fase, auxiliar_ignorado=codigo == 54, terreno=[], sprites=[])
    if not vis['descoberto']:
        return plano
    for ordem, operacao in enumerate(('copiar',) if vis['iluminado'] else ('copiar','sombra')):
        plano['terreno'].append(dict(**localizar(mid), ordem=ordem, x=dx, y=0,
            operacao=operacao, fase=fase,
            sequencia=[base] if codigo == 54 else list(range(base, base + 16)),
            evidencia='AffVegetTerrain 0x4104af..0x410587; entrada 54 em 0x41053d',
            confianca='codigo_e_comparacao_x86'))
    return plano


def consultar_objeto_v6(codigo, **entradas):
    """União explícita do catálogo v5 com os quatro códigos novos da v6."""
    if type(codigo) is int and codigo in CODIGOS_SEQUENCIAIS:
        return consultar_sequencial(codigo, **entradas)
    return consultar_objeto(codigo, **entradas)


def ler_objetos_eta_v6(dados):
    """Mesma leitura de disco da v5, com cobertura ampliada de códigos."""
    resultado = ler_objetos_eta(dados)
    for registro in resultado['registros']:
        registro['mapeado'] = registro['codigo'] in CODIGOS_V6
        registro['catalogo'] = ('v6' if registro['codigo'] in CODIGOS_SEQUENCIAIS
                               else 'v5' if registro['mapeado'] else None)
    return resultado


def normalizar_inicio(objetos, auxiliares):
    """Somente o laço 0x46c3de..0x46c40a de MissionLoad; não o carregador inteiro.

    Converte código 54 em 66, auxiliar 1; preserva todos os demais bytes.
    Retorna cópias novas e índices das células convertidas.
    """
    if len(objetos) != 65536 or len(auxiliares) != 65536:
        raise ValueError('São exigidas duas camadas de 65536 bytes')
    out = bytearray(objetos)
    aux = bytearray(auxiliares)
    alteradas = []
    for i, codigo in enumerate(objetos):
        if codigo == 54:
            out[i] = 66
            aux[i] = 1
            alteradas.append(i)
    return dict(objetos=bytes(out), auxiliares=bytes(aux), alteradas=alteradas)
