"""Reconstrução parcial do carregador de unidades: 0x441792 e 0x44188b.

Não implementa combate: recupera dados de entrada e o layout escrito em RAM.
Tempos permanecem nas unidades originais, ainda sem conversão para segundos.
"""
import configparser
import struct

BASE_TIPOS = 0x4965ae
PASSO_TIPO = 0x32
TOTAL_TIPOS = 26
# Chave INI: (nome português, valor padrão da API, offset, formato em memória).
CAMPOS = {
    'TMPSRECRUTE': ('tempo_recrutamento', 120, 0x00, 'H'),
    'COUTPATATE': ('custo_comida', 1, 0x02, 'H'),
    'COUTPIECE': ('custo_pecas', 1, 0x04, 'H'),
    'COUTROCHE': ('custo_pedra', 1, 0x06, 'H'),
    'BLINDAGE': ('blindagem', 5, 0x0b, 'B'),
    'RAYON': ('raio_visao', 5, 0x2a, 'H'),
    'PORTEE': ('alcance_ataque', 1, 0x2c, 'H'),
    'FATIGUE': ('fadiga', 3000, 0x2e, 'H'),
    'RECHARGE': ('recarga', 100, 0x30, 'H'),
}


def ler_ini(dados):
    ini = configparser.ConfigParser(interpolation=None, strict=True)
    ini.read_string(dados.decode('cp1252').replace('\x1a', ''))
    return ini


def reconstruir_tipo(secao, ini, registro_original):
    """Espelha truncamentos de AL/AX e o quadrado de PORTEE.

    A validação de INI é mais estrita que a API Windows: valores malformados
    são rejeitados, não se tenta imitar entradas inválidas do sistema legado.
    """
    if len(registro_original) != PASSO_TIPO:
        raise ValueError('Registro de tipo deve ter 50 bytes')
    memoria = bytearray(registro_original)
    valores = {}
    for chave, (nome, padrao, offset, formato) in CAMPOS.items():
        valor = int(ini.get(secao, chave, fallback=str(padrao)))
        valores[nome] = valor
        armazenado = valor * valor if chave == 'PORTEE' else valor
        limite = 0xff if formato == 'B' else 0xffff
        struct.pack_into('<' + formato, memoria, offset, armazenado & limite)
    nome = ini.get(secao, 'NAME', fallback=secao)
    # GetPrivateProfileStringA recebe capacidade 30: até 29 bytes + NUL.
    texto = nome.encode('cp1252')[:29] + b'\0'
    memoria[12:12+len(texto)] = texto
    valores['alcance_ataque_quadrado_u16'] = struct.unpack_from('<H', memoria, 0x2c)[0]
    return dict(secao_original=secao, nome=nome, **valores,
                registro_memoria_hex=memoria.hex())


def ler_danos(ini, secao):
    danos = [int(v.strip()) for v in ini.get(secao, 'DEGAT').split(',')]
    if len(danos) != 27 or any(not 0 <= v <= 255 for v in danos):
        raise ValueError(f'Matriz DEGAT inválida em {secao}')
    return danos


def extrair_regras(imagem, base_imagem, dados_ini):
    ini = ler_ini(dados_ini)
    unidades = []
    for indice in range(TOTAL_TIPOS):
        offset = BASE_TIPOS - base_imagem + indice * PASSO_TIPO
        registro = imagem[offset:offset + PASSO_TIPO]
        if len(registro) != PASSO_TIPO:
            raise ValueError('Tabela de unidades fora da imagem')
        secao = registro[12:42].split(b'\0')[0].decode('cp1252')
        if not ini.has_section(secao):
            raise ValueError(f'Seção {secao!r} ausente; executável incompatível')
        unidade = reconstruir_tipo(secao, ini, registro)
        unidade.update(id=indice, endereco=f'0x{BASE_TIPOS + indice * PASSO_TIPO:08x}',
                       danos_por_alvo=ler_danos(ini, secao))
        unidades.append(unidade)
    return dict(unidades=unidades,
                ordem_alvos=[u['secao_original'] for u in unidades] + ['CONSTRUCAO'],
                danos_mina=ler_danos(ini, 'MINE'),
                bonus_capitao=int(ini.get('DIVERS', 'BONUSCAPITAINE', fallback='2')),
                observacao='Matriz de valores carregados; fórmula final de combate não reconstruída.')
