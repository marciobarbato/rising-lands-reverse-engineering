"""Animação lógica, pedidos de impacto e ramo linear de ProjectileAvance.

Não desenha sprites nem calcula dano. O avanço cobre tipos 1..5, 9..13,
17, 20..23 e 29, incluindo chegada e emissão secundária. Outros tipos são
recusados antes de alterações; não é substituto completo de ProjectileAvance.
Random é uma consulta externa (valor u32), sem gerador duplicado neste módulo.
"""
import struct

from projeteis import u16, s16, por32, calcular_linha

TIPOS_LINEARES = frozenset((*range(1, 6), *range(9, 14), 17, 20, 21, 22, 23, 29))


def animar_projetil(p, incremento):
    """ProjectileAnim 0x46e52c; incremento é o byte global em 0x508f7c.

Não testa atividade. A passagem inicial de tipos 29/30 até quadro 12 e o
incremento simples dos efeitos não usam a velocidade global de animação.
"""
    tipo, quadro = p[0], p[0x18]
    if tipo in (*range(1, 6), 17):
        p[0x18] = (quadro + (incremento & 255)) & 3
    elif 20 <= tipo <= 23:
        p[0x18] = (quadro + (incremento & 255)) & 7
    elif tipo in (29, 30):
        p[0x18] = quadro + 1 if quadro < 12 else ((quadro + 1) % 20 or 12)
    elif tipo in (6, 7, 8, 14, 15, 16, 18, 19, *range(24, 29), *range(31, 35)):
        p[0x18] = (quadro + 1) & 255


def infligir_dano_projetil(pool, indice):
    """ProjectileInfligeDegat 0x46e5fe: ordena pedidos, não aritmética de dano.

Centro primeiro. Tipos 20/22 expandem com modo/direção originais; tipo 29
usa modo 4 e o tipo como direção. Vizinhos usam flag zero e bordas 0..255.
Releitura dos campos após efeitos preserva o comportamento com callbacks.
"""
    p = pool.registro(indice)
    pool._efeito('InfligeDegat', u16(p, 0x16), p[0x1f], u16(p, 0x20), p[0x22], p[0x23])
    tipo = p[0]  # o original decide a expansão depois do efeito central
    if tipo not in (20, 22, 29):
        return
    for dx, dy in ((-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1),
                   (-1, 1), (0, 1), (1, 1)):
        centro = u16(p, 0x16)
        x, y = centro & 255, centro >> 8
        if not (0 <= x + dx <= 255 and 0 <= y + dy <= 255):
            continue
        modo = 4 if tipo == 29 else p[0x1f]
        # O primeiro vizinho do tipo 29 usa BL salvo; os outros releem +00.
        direcao = (tipo if (dx, dy) == (-1, 0) else p[0]) if tipo == 29 else p[0x22]
        pool._efeito('InfligeDegat', (centro + dx + dy * 256) & 65535,
                     modo, u16(p, 0x20), direcao, 0)


def _aleatorio(consulta, marcador):
    if consulta is None:
        raise NotImplementedError('Consulta externa necessária: Random')
    # EAX na entrada é observado como marcador; Random não o usa como limite.
    return consulta(marcador) & 0xffffffff


def _efeito_chegada(pool, p, origem, tipo):
    return pool.iniciar(tipo, origem & 65535, u16(p, 0x16), p[0x1f],
                        u16(p, 0x20), p[0x22], 0, 0, p[0x23])


def _chegada(pool, indice, aleatorio):
    p = pool.registro(indice)
    tipo = p[0]
    if tipo in (1, 9, 17, 20, 21, 22, 23, 29):
        infligir_dano_projetil(pool, indice)
    if tipo == 1:
        filho = 6 + _aleatorio(aleatorio, 0x30) % 3
        _efeito_chegada(pool, p, u16(p, 0x16), filho)
    elif tipo in (20, 22, 29):
        alvo = u16(p, 0x16)
        x, y = alvo & 255, alvo >> 8
        largura = 3 - int(x in (0, 255))
        altura = 3 - int(y in (0, 255))
        origem = max(0, x - 1) + 256 * max(0, y - 1)
        for _ in range(altura):
            for _ in range(largura):
                filho = 6 + _aleatorio(aleatorio, 0x2f) % 3
                _efeito_chegada(pool, p, origem, filho)
                origem += 1
            # 0x46f587 subtrai ALTURA, não largura. Não corrigir a deriva nas bordas.
            origem += 256 - altura
    elif tipo == 30:
        # Só alcançável por alias artificial: registro inativo reutilizado como
        # filho 30 durante a própria chamada de avanço do tipo 29.
        raise NotImplementedError('Chegada do tipo 30 não traduzida')
    p[2] = 0  # depois do dano, RNG e tentativas de criar todos os filhos


def avancar_linear(pool, indice, aleatorio=None):
    """Ramos lineares de ProjectileAvance 0x46eaf8; um despacho nativo.

Tipo 29 aguarda +18>=12. Incrementa +03 com wrap e tenta filho tipo+1
quando +19!=0 e +03==+04, limpando +19 mesmo com pool cheio. A chegada é
processada somente se +34 JÁ é zero antes do incremento de posição.
Não verifica atividade, não move unidades e não tem colisão intermediária
nos ramos traduzidos. O backend precisa fornecer Random para certas chegadas.
"""
    p = pool.registro(indice)
    if p[0] not in TIPOS_LINEARES:
        raise NotImplementedError(f'Ramo de ProjectileAvance não traduzido: tipo {p[0]}')
    if p[0] == 29 and p[0x18] < 12:
        return
    p[3] = (p[3] + 1) & 255
    if p[0x19] and p[3] == p[4]:
        pool.iniciar((p[0] + 1) & 255, u16(p, 0x14), u16(p, 0x16), p[0x1f],
                     u16(p, 0x20), p[0x22], s16(u16(p, 0x10)), s16(u16(p, 0x12)), p[0x23])
        p[0x19] = 0
    if u16(p, 0x34):
        calcular_linha(p)
        if p[0x23]:
            # ADD usa +28 sem sinal, mesmo quando a preparação escreveu IDIV negativo.
            por32(p, 0x24, struct.unpack_from('<I', p, 0x24)[0] + u16(p, 0x28))
    else:
        _chegada(pool, indice, aleatorio)
