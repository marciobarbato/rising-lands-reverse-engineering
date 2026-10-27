"""Seleção e condições de ataque recuperadas do x86, sem movimento ou dano.

Registros de unidade: bytes/bytearray de 276 bytes; tabela com 800 entradas.
Grade: mapeamento célula u16 -> palavra u16, ausência equivale a 0xffff.
Os callbacks de construções e magia são dependências explícitas, ainda externas.
Não se pressupõe que encontrar alvo, emitir ordem e começar animação coincidam.
"""
import struct

SEM_ALVO = 0xffff
TIPOS_GRANDES = frozenset((3, 11, 12, 13, 14, 15, 16, 25))
IGNORAM_LINHA = frozenset((4, 8, 12, 22, 23))
RECUSAM_ORDEM = frozenset((5, 6, 7, 9, 10, 13))
TIPOS_BUSCA_AUTOMATICA = frozenset((0, 1, 2, 3, 8, 11, 12, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25))


def palavra(registro, offset):
    return struct.unpack_from('<H', registro, offset)[0]


def _consulta(funcao, nome, *args):
    if funcao is None:
        raise NotImplementedError(f'Consulta externa necessária: {nome}')
    return funcao(*args)


def distancia2(a, b):
    """0x479555 aplicado a células de coordenadas u8, resultado u32."""
    return ((a & 255) - (b & 255)) ** 2 + (((a & 65535) >> 8) - ((b & 65535) >> 8)) ** 2


def aliados(origem, destino, mascaras):
    """0x46d838: relação direcional; igualdade é aceita até para ID 200."""
    origem, destino = origem & 255, destino & 255
    if origem == destino:
        return True
    return origem <= 4 and destino <= 4 and bool(mascaras[origem] & (1 << destino))


def engin_est_ennemi(dono_consultante, dono_unidade, mascaras):
    """0x446fbf / predicado embutido no scan: AL da unidade, DL consultante.

    O caso 4 diferente prevalece sobre a exclusão de 200: (4, 200) é inimigo.
    O scan ainda exclui separadamente candidatos de dono 200.
    """
    a, b = dono_consultante & 255, dono_unidade & 255
    if a != b and (a == 4 or b == 4):
        return True
    return a != 200 and b != 200 and a != b and not aliados(a, b, mascaras)


def tipo_pode_atacar(tipo_atacante, tipo_alvo):
    """0x453d7d: filtro do PAR de tipos; não é capacidade global do atacante."""
    tipo_atacante, tipo_alvo = tipo_atacante & 255, tipo_alvo & 255
    if tipo_alvo in (10, 17):
        return False
    return tipo_alvo != 16 or tipo_atacante in (2, 8)


def encontrar_alvo_scan(unidades, indice, mascaras):
    """0x453da2: primeiro ID 0..799 elegível no círculo da visão (+0xbb)."""
    u = unidades[indice]
    for i in range(800):
        alvo = unidades[i]
        if alvo[2] in (0, 4) or not alvo[0x72]:
            continue
        if not engin_est_ennemi(u[0], alvo[0], mascaras) or alvo[0] == 200:
            continue
        if tipo_pode_atacar(u[1], alvo[1]) and distancia2(palavra(u, 8), palavra(alvo, 8)) <= u[0xbb] ** 2:
            return i
    return SEM_ALVO


def encontrar_alvo(unidades, indice, grade, mascaras):
    """0x453f74: tipos 2/8 preferem scan; depois mínimo na grade, empate estável.

    A grade consulta aliados(candidato, atacante), não o sentido do scan.
    Não refaz estado/+0x72; mede a CÉLULA DA GRADE. Distâncias truncadas a u16.
    IDs 800..2047 causam IndexError aqui; o original acessaria fora da tabela.
    """
    u = unidades[indice]
    if u[1] in (2, 8):
        encontrado = encontrar_alvo_scan(unidades, indice, mascaras)
        if encontrado != SEM_ALVO:
            return encontrado
    atual, raio = palavra(u, 8), u[0xbb]
    x, y = atual & 255, atual >> 8
    melhor, menor = SEM_ALVO, 0xffff
    for cy in range(max(0, y - raio), min(256, y + raio + 1)):
        for cx in range(max(0, x - raio), min(256, x + raio + 1)):
            celula = cx + cy * 256
            ocupacao = grade.get(celula, 0xffff) & 0xffff
            if ocupacao & 0xc000 != 0x4000:
                continue
            i = (ocupacao & 0x3ff8) >> 3
            if i >= 800:
                raise IndexError('ID de ocupante fora da tabela original de 800 unidades')
            alvo = unidades[i]
            if alvo[0] == 200 or aliados(alvo[0], u[0], mascaras):
                continue
            if not tipo_pode_atacar(u[1], alvo[1]):
                continue
            d = distancia2(atual, celula) & 0xffff
            if d <= raio * raio and d < menor:
                melhor, menor = i, d
    return melhor


def ocupa_celula(u, celula, filtro=0):
    """0x44246e, tipos 0..25; filtro 1 exclui +ab!=0 e 2 exclui +ab==0."""
    if (u[0xab] and filtro == 1) or (not u[0xab] and filtro == 2) or u[2] == 14:
        return False
    if not 0 <= u[1] <= 25:
        raise ValueError('Tipo fora do domínio reconstruído')
    celula &= 65535
    deslocamentos = (0, 1, 0x101, 0x100) if u[1] in TIPOS_GRANDES else (0,)
    # As subtrações de footprint são u32, não u16: não dar wrap nos -1 etc.
    return any(palavra(u, off) - d == celula for off in (8, 0x7c) for d in deslocamentos)


def celulas_adjacentes(u):
    """Laços de 0x4468e4 / 0x446b0c, incluindo a própria área e bordas x86."""
    if u[0x86] or u[0x87]:
        return
    if not 0 <= u[1] <= 25:
        raise ValueError('Tipo fora do domínio reconstruído')
    w = h = 2 if u[1] in TIPOS_GRANDES else 1
    inicio = (palavra(u, 8) - ((h - 1) * 256 + w - 1)) & 0xffff
    x, y = inicio & 255, inicio >> 8
    if x:
        inicio -= 1
    else:
        w -= 1
    if y:
        inicio -= 256
    else:
        h -= 1
    x, y = inicio & 255, (inicio & 65535) >> 8
    cursor = inicio
    for dy in range(h + 2):
        if y + dy < 256:
            for dx in range(w + 2):
                if x + dx < 256:
                    yield cursor & 65535
                cursor += 1
        cursor += 256 - w - 2


def adjacente_unidade(atacante, alvo):
    """0x4468e4: consulta ocupa_celula no mesmo estrato bruto de +0xab."""
    filtro = 1 + bool(alvo[0xab])
    return any(ocupa_celula(alvo, c, filtro) for c in celulas_adjacentes(atacante))


def a_portee(unidades, indice, modo, referencia, modificador4=0, *,
             celula_construcao=None, adjacente_construcao=None, alcance_magia=None):
    """0x446cb5: AX=atacante, DL=modo, BX=referência. Retorna booleano AL.

    Modificador4 é valor já consultado, somado ao alcance QUADRÁTICO +0xb0.
    Modo 1 usa +0x7c do alvo; 3 consulta construção; 5 usa +0xb8 do atacante.
    Modos fora de 1/3/5 têm local não inicializado no original e são recusados.
    Callbacks não fornecidos falham explicitamente quando o ramo os necessita.
    """
    u = unidades[indice]
    modo &= 255
    if modo not in (1, 3, 5):
        raise ValueError('Modo com célula local indefinida no original')
    if modo == 1:
        destino = palavra(unidades[referencia], 0x7c)
    elif modo == 3:
        destino = _consulta(celula_construcao, 'BatimentGetCase', referencia) & 65535
    else:
        destino = palavra(u, 0xb8)
    if u[2] == 24:
        limite = _consulta(alcance_magia, 'SortilegeGetPortee', u[0xf4]) + modificador4
    else:
        if u[1] == 16:
            return palavra(u, 8) == destino
        if not u[0x78] or u[1] in (1, 4, 21):
            contato = (adjacente_unidade(u, unidades[referencia]) if modo == 1 else
                       _consulta(adjacente_construcao, 'BatimentAdjacent', referencia, palavra(u, 8)) if modo == 3 else
                       (referencia & 65535) in celulas_adjacentes(u))
            if contato:
                return True
        limite = u[0xb0] + modificador4
    return distancia2(palavra(u, 8), destino) <= (limite & 65535)


def a_portee_minimale(unidades, indice, modo, referencia):
    """0x446eed: só contra alvo tipo 16 em modo 1 exige distância² > 4."""
    if modo & 255 != 1 or unidades[referencia][1] != 16:
        return True
    return distancia2(palavra(unidades[indice], 8), palavra(unidades[referencia], 0x7c)) > 4


def linha_de_tiro(u, celula_alvo, terreno, largura=256, altura=256):
    """0x4517a2: passos pelos sinais dx/dy, não Bresenham; testa só montanhas.

    O alvo já foi resolvido pelo chamador. Nenhuma consulta de ocupação/névoa.
    Tipos 4, 8, 12, 22 e 23 retornam True sem ler terreno.
    No domínio suportado origem/alvo são válidos nas dimensões informadas.
    """
    if u[1] in IGNORAM_LINHA:
        return True
    atual = palavra(u, 0x7c)
    tx, ty = celula_alvo & 255, (celula_alvo & 65535) >> 8
    if not (1 <= largura <= 256 and 1 <= altura <= 256 and
            (atual & 255) < largura and (atual >> 8) < altura and tx < largura and ty < altura):
        raise ValueError('Célula fora das dimensões: caminho não delimitado aqui')
    while True:
        x, y = atual & 255, atual >> 8
        x += (tx > x) - (tx < x)
        y += (ty > y) - (ty < y)
        atual = x + 256 * y
        bloqueia = 0x1dd <= (terreno.get(atual, 0) & 65535) < 0x260
        if bloqueia or atual == celula_alvo:
            # Montanha na própria célula alvo é aceita pelo original.
            return atual == celula_alvo


def arma_carregada(atual, recarga_tipo, modificador3=0):
    """0x45173f: comparação assinada de valores promovidos para 32 bits."""
    return (atual & 65535) >= (recarga_tipo & 65535) - (modificador3 & 65535)


def preparar_inicio(u, em_alcance, linha_livre):
    """Portão de 0x451957..0x4519bd, só subestado +0x8a == 0.

    True conduz a parar a navegação/apontar/recarregar; não significa dano.
    """
    if u[0x8a] != 0:
        raise ValueError('Portão exclusivo do subestado zero')
    return not (u[0x86] or u[0x87]) and bool(em_alcance) and bool(linha_livre)


def iniciar_ciclo_apos_mira(u, recarga_tipo, modificador3=0):
    """0x451d4d..0x451e22: após o alinhamento do corpo, verifica torre/recarga.

    Retorna uma cópia do registro e o próximo portão. Não gira nem aplica dano.
    Tipos 12/15 precisam +94==+da. Ao carregar, zera +102 e põe +8a=1.
    """
    resultado = bytearray(u)
    if u[1] in (12, 15) and u[0x94] != u[0xda]:
        return resultado, 'girar_torre'
    if not arma_carregada(palavra(u, 0x102), recarga_tipo, modificador3):
        return resultado, 'aguardar_recarga'
    struct.pack_into('<H', resultado, 0x102, 0)
    resultado[0x8a] = 1
    if u[1] != 16:
        resultado[0xa4] = resultado[0xa9] = 0
    return resultado, 'ciclo_iniciado'


def ordem_apos_reset(u, indice, modo, referencia):
    """0x445a80..0x445af1: efeitos LOCAIS após ResetOrdre já ter ocorrido.

    O chamador deve testar a identidade da ordem ANTES de ResetOrdre. A rotina
    completa o chama até quando depois recusa tipo, modo ou alvo igual a si.
    Não verifica alcance, vida, aliança ou validade da referência.
    """
    r = bytearray(u)
    modo, referencia = modo & 255, referencia & 65535
    aceitou = u[1] not in RECUSAM_ORDEM and modo in (1, 3, 5) and not (modo == 1 and indice == referencia)
    if aceitou:
        r[2], r[0x8a], r[0xb7] = 1, 0, modo
        struct.pack_into('<H', r, 0xb8, referencia)
    return r, aceitou


def ordem_ja_definida(u, modo, referencia):
    """0x445a57..0x445a76: mesma ordem ativa evita inclusive ResetOrdre."""
    return u[2] == 1 and u[0xb7] == (modo & 255) and palavra(u, 0xb8) == (referencia & 65535)


def alvo_ordem_valido(unidades, indice, *, construcao_invalida=None, dono_construcao=None):
    """0x456886..0x45689e, despacho dos estados 1 e 24 em EnginNextEtape.

    Modo 1: referência !=ffff, estado do alvo !=0/4, dono !=200, +72!=0.
    Não refaz alianças, filtro de tipos, distância nem consulta vida +9a.
    Modo 3 delega os dois acessores de construção. Outros modos passam aqui.
    """
    u = unidades[indice]
    referencia = palavra(u, 0xb8)
    if u[0xb7] == 1:
        if referencia == SEM_ALVO:
            return False
        if referencia >= 800:
            raise IndexError('Referência fora da tabela original de 800 unidades')
        alvo = unidades[referencia]
        return alvo[2] not in (0, 4) and alvo[0] != 200 and bool(alvo[0x72])
    if u[0xb7] == 3:
        return (referencia != SEM_ALVO and not _consulta(construcao_invalida, 'BatimentEnDestruction', referencia)
                and _consulta(dono_construcao, 'BatimentGetPlayer', referencia) != 200)
    return True


def elegivel_busca_automatica(u):
    """Portões locais 0x4546bc..0x454794 antes de EnginTrouveCible.

    Esta elegibilidade só vale quando EnginNextEtape já alcançou o trecho.
    Não inclui os portões anteriores do despachante de atualização.
    """
    return (u[1] in TIPOS_BUSCA_AUTOMATICA and u[2] not in (1, 19)
            and (u[1] != 16 or u[0xda] != 0))


def reacao_alvo_automatico(u, tipo_controle):
    """0x4547ad..0x4547e0, assumindo que a busca encontrou alvo !=ffff.

    Controle 2 envia mensagem 0x49; demais só emitem SetAttaqueEngin no estado 7.
    Retorna a ação para o chamador; não envia mensagem nem altera outro sistema.
    """
    return 'mensagem_0x49' if tipo_controle == 2 else 'ordem_modo_1' if u[2] == 7 else 'nenhuma'


def manter_ciclo_apos_espera(tipo, em_alcance, mira_alinhada):
    """0x452b10..0x452b78, somente após expirar +8b; falha volta +8a a 0.

    Tipos 14/16 saltam essa revalidação. Recebe consultas já resolvidas, sem
    afirmar que alcance e mira sejam as únicas condições de manutenção global.
    """
    return tipo in (14, 16) or (bool(em_alcance) and bool(mira_alinhada))
