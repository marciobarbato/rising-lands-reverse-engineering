"""EnginViseCible (0x451464) e AngleCalcul (0x4796cb), domínio da mira.

Consulta de alinhamento, sem escrita em unidades e sem integração ao movimento.
O cálculo angular suporta coordenadas 0..255 e as resoluções 8/32 usadas pela
mira. Não pretende reproduzir registradores superiores nem a FPU bit a bit.
"""
import math

from alvos_alcance import palavra, _consulta

# Imediatos 0x400921fb:0x54411744 em 0x479716..0x479728, double do EXE.
# math.pi tem outros bits; conservar a constante original na conversão a graus.
PI_ORIGINAL = float.fromhex('0x1.921fb54411744p+1')
TIPOS_TORRE = frozenset((12, 15))


def angulo_calcul(x1, y1, x2, y2, setores):
    """0x4796cb: orientação 1..N, começando no oeste e seguindo para norte.

    Soma meio setor antes de truncar para inteiro; não usa round() nem a
    direção baseada somente nos sinais. O domínio é o usado por 0x451464.
    Células coincidentes resultam no setor do leste (5 em 8; 17 em 32).
    """
    if setores not in (8, 32):
        raise ValueError('A mira usa somente resoluções de 8 ou 32 setores')
    if any(not 0 <= v <= 255 for v in (x1, y1, x2, y2)):
        raise ValueError('Coordenadas fora do domínio u8 da mira')
    dx, dy = abs(x1 - x2), abs(y1 - y2)
    if not dy:
        graus = 0.0
    elif not dx:
        graus = 90.0
    else:
        graus = math.acos(dx / math.sqrt(dx * dx + dy * dy)) * 180.0 / PI_ORIGINAL
    if x1 > x2:
        graus = graus + 180.0 if y1 >= y2 else 180.0 - graus
    elif y1 > y2:
        graus = 360.0 - graus
    passo = 360.0 / setores
    graus += passo * 0.5
    if graus >= 360.0:
        graus -= 360.0
    # 0x48c43e altera RC para truncamento, restaura CW e 0x47986d converte.
    indice = math.trunc(graus / passo)
    return ((indice % setores + setores - setores // 2) % setores) + 1


def _alvo_unidade(unidades, referencia):
    if referencia >= 800:
        raise IndexError('Referência fora da tabela original de 800 unidades')
    return palavra(unidades[referencia], 0x7c)


def celula_alvo_mira(unidades, indice, *, celula_construcao=None, celula_construcao_adjacente=None):
    """Resolve a célula como 0x451490..0x45165d, incluindo a segunda consulta.

    Modo vem de +b7 e referência de +b8. No modo 3 e alcance +b0=0/1, a
    primeira consulta pede BatimentGetCaseAdjacent(ref, atacante.+7c); ffff
    causa fallback ao centro. Tipos 12/15 depois resolvem o centro novamente,
    mesmo que a primeira consulta tenha encontrado adjacência.
    """
    u = unidades[indice]
    modo, referencia = u[0xb7], palavra(u, 0xb8)
    alvo = 0xffff
    if modo == 1:
        alvo = _alvo_unidade(unidades, referencia)
    elif modo == 3:
        if u[0xb0] in (0, 1):
            alvo = _consulta(celula_construcao_adjacente, 'BatimentGetCaseAdjacent',
                             referencia, palavra(u, 0x7c)) & 65535
        if alvo == 0xffff:
            alvo = _consulta(celula_construcao, 'BatimentGetCase', referencia) & 65535
    elif modo == 5:
        alvo = referencia
    if u[1] in TIPOS_TORRE:
        if modo == 1:
            alvo = _alvo_unidade(unidades, referencia)
        elif modo == 3:
            alvo = _consulta(celula_construcao, 'BatimentGetCase', referencia) & 65535
        elif modo == 5:
            alvo = referencia
        else:
            # 0x451656 salta sem definir EDI: depende do registrador do chamador.
            raise ValueError('Modo de torre com célula dependente de EDI de entrada no x86')
    # Outros modos no ramo de corpo conservam o ffff explícito de 0x451490.
    return alvo


def mira_requerida(unidades, indice, *, celula_construcao=None, celula_construcao_adjacente=None):
    """Retorna célula, campo comparado, orientação requerida e atual.

    Tipos 12/15: AngleCalcul(...,32) versus +94. Demais: 2*AngleCalcul(...,8)-1
    versus +91; tipo 3 aplica (orientação+11)%16+1. Origem é sempre +08.
    """
    u = unidades[indice]
    alvo = celula_alvo_mira(unidades, indice, celula_construcao=celula_construcao,
                            celula_construcao_adjacente=celula_construcao_adjacente)
    origem = palavra(u, 8)
    torre = u[1] in TIPOS_TORRE
    setores = 32 if torre else 8
    orientacao = angulo_calcul(origem & 255, origem >> 8, alvo & 255, alvo >> 8, setores)
    if not torre:
        orientacao = (2 * orientacao - 1) & 255
        if u[1] == 3:
            orientacao = (orientacao + 11) % 16 + 1
    campo = 0x94 if torre else 0x91
    return dict(celula_alvo=alvo, setores=setores, campo_orientacao=campo,
                orientacao_requerida=orientacao, orientacao_atual=u[campo])


def engin_vise_cible(unidades, indice, *, celula_construcao=None, celula_construcao_adjacente=None):
    """0x451464: AX=índice; resultado AL, sem alterar a orientação."""
    mira = mira_requerida(unidades, indice, celula_construcao=celula_construcao,
                          celula_construcao_adjacente=celula_construcao_adjacente)
    return mira['orientacao_atual'] == mira['orientacao_requerida']
