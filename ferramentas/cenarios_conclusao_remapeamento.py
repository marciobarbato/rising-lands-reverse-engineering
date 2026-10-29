"""Small explicit Stage17 inputs; no region-label implementation or native run."""
from cenarios_classificacao_remapeamento import preparar_classificacao

CASOS_CONCLUSAO = ('MONDE01', 'uniform_zero_edge', 'diagonal_one', 'diagonal_zero',
                  'component_lock_unavailable', 'component_lock_null', 'cleanup_unavailable')


def preparar_conclusao(nome):
    if nome not in CASOS_CONCLUSAO:
        raise ValueError('Unknown original-only completion fixture')
    mundo, _, _, fonte = preparar_classificacao('MONDE01' if nome == 'MONDE01' else 'zero')
    if nome != 'MONDE01':
        mundo.largura = mundo.altura = 256
        fonte = dict(kind='Explicit synthetic whole-grid classification/connectivity/resource fixture', case=nome)
    if nome == 'uniform_zero_edge':
        mundo.largura = mundo.altura = 1
    elif nome == 'diagonal_one':
        for celula in (257, 514):
            mundo.atributos[celula] = mundo.objetos[celula] = 1
    elif nome == 'diagonal_zero':
        mundo.atributos[:] = b'\x01'*65536
        mundo.objetos[:] = b'\x01'*65536
        for celula in (257, 514):
            mundo.atributos[celula] = mundo.objetos[celula] = 0
    return mundo, fonte
