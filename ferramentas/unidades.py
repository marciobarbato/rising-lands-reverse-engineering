"""Campos das instâncias recuperados no Ghidra e conferidos no assembly x86.

Não simula o jogo. Estado 14 e proprietário 200 continuam como códigos, sem
inventar regras de visibilidade ou nomes de clãs. As coordenadas são células.
"""
import hashlib
import struct

TAMANHO_DISCO = 784
TAMANHO_SERIALIZADO = 272
PASSO_MEMORIA = 276


def coordenadas(celula):
    if not 0 <= celula <= 65535:
        raise ValueError('Célula fora do intervalo uint16')
    return dict(x=celula & 255, y=celula >> 8)


def recompor_memoria(bruto):
    if len(bruto) != TAMANHO_DISCO:
        raise ValueError('Registro de unidade deve ter 784 bytes nesta edição')
    # 0x46ad2e: copia 140; 0x46ad3d: pula 512; 0x46ad62: copia os 132 restantes.
    return bruto[:0x8c] + bruto[0x28c:]


def interpretar_unidade(indice, bruto):
    if not 0 <= indice < 800:
        raise ValueError('Índice excede a tabela alocada de 800 unidades')
    memoria = recompor_memoria(bruto)

    def u16(offset):
        return struct.unpack_from('<H', memoria, offset)[0]

    return dict(indice=indice, tipo=memoria[1], proprietario_id=memoria[0],
                byte_estado=memoria[2], ativa_no_predicado_441fff=memoria[2] != 0,
                celula_atual=u16(8), posicao=coordenadas(u16(8)),
                celula_passo=u16(0x7c), celula_destino=u16(0x7e),
                destino=coordenadas(u16(0x7e)), estado_caminho=memoria[0x88],
                vida_no_arquivo=u16(0x9a), raio_visao_no_arquivo=memoria[0xbb],
                alcance_quadrado_u8_no_arquivo=memoria[0xb0],
                recarga_no_arquivo=u16(0x102), grupo_no_arquivo=memoria[0xbc],
                tamanho_memoria_serializada=len(memoria),
                sha256_registro=hashlib.sha256(bruto).hexdigest())


def atributos_apos_carga(unidade, tipo):
    """Só os efeitos confirmados de 0x46acbf, não o estado completo da RAM.

    O carregador também chama outras rotinas; não modelamos esses efeitos aqui.
    """
    if not unidade['ativa_no_predicado_441fff']:
        return dict(proprietario_id=unidade['proprietario_id'],
                    vida=unidade['vida_no_arquivo'],
                    raio_visao=unidade['raio_visao_no_arquivo'],
                    alcance_quadrado_u8=unidade['alcance_quadrado_u8_no_arquivo'],
                    recarga=unidade['recarga_no_arquivo'], grupo=unidade['grupo_no_arquivo'])
    proprietario = unidade['proprietario_id']
    if unidade['tipo'] == 16:
        proprietario = 0  # 0x46afdc..0x46afe1.
    elif 20 <= unidade['tipo'] <= 24:
        proprietario = 4  # 0x4422dd e 0x46b015.
    return dict(proprietario_id=proprietario, vida=100,
                raio_visao=tipo['raio_visao'] & 255,
                alcance_quadrado_u8=tipo['alcance_ataque_quadrado_u16'] & 255,
                recarga=tipo['recarga'] & 65535, grupo=255)


def curar_com_limite(vida, acrescimo, maximo):
    """Reconstrução de 0x457122: aritmética uint16 antes da comparação.

    Retorna (vida, excedeu_maximo). O booleano é estrito: alcançar exatamente
    o máximo não dispara o retorno verdadeiro dessa função.
    """
    nova = (vida + acrescimo) & 65535
    limite = maximo & 65535
    return (limite, True) if nova > limite else (nova, False)
