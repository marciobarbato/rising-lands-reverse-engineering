"""Pool e preparação linear de projéteis, independentes do mundo do jogo.

Registros brutos de 56 bytes, pool de 100 posições. Efeitos imediatos de dano
e iluminação são callbacks explícitos. O avanço linear e os pedidos de impacto
estão em avanco_projeteis; maquina_projeteis completa o despacho e a expiração.
Não implementa aritmética de dano, desenho nem uma duração de tick.
"""
from dataclasses import dataclass, field
import struct

TAMANHO, QUANTIDADE = 56, 100


def u16(p, off):
    return struct.unpack_from('<H', p, off)[0]


def s16(v):
    return ((v + 32768) & 65535) - 32768


def por16(p, off, v):
    struct.pack_into('<H', p, off, v & 65535)


def por32(p, off, v):
    struct.pack_into('<I', p, off, v & 0xffffffff)


def preparar_linha(p):
    """ProjectileLineaire, 0x46e049: Bresenham com palavras assinadas.

    Entrada: +0c/+0e posição em pixels u16, +16 célula alvo, +23 flag.
    O alvo é o centro da célula (32*x+16, 32*y+16). A posição compactada
    em +08 é s16(y)*8192+s16(x), em 32 bits. Conserva o caso -32768.
    """
    x, y, alvo = u16(p, 0xc), u16(p, 0xe), u16(p, 0x16)
    dx, dy = s16((alvo & 255) * 32 + 16 - x), s16((alvo >> 8) * 32 + 16 - y)
    sx, sy = (-1 if dx < 0 else 1), (-8192 if dy < 0 else 8192)
    ax, ay = abs(dx), abs(dy)
    if s16(ax) > s16(ay):  # CMP CX,DX / JLE; 0x8000 não é positivo
        maior, menor, axial = ax, ay, sx
    else:
        maior, menor, axial = ay, ax, sy
    por16(p, 0x34, maior)
    por16(p, 0x2c, axial)
    por16(p, 0x32, menor * 2)
    por16(p, 0x2a, sx + sy)
    por16(p, 0x30, 2 * menor - 2 * maior)
    por32(p, 8, (s16(y) << 13) + s16(x))
    por16(p, 0x2e, 2 * menor - maior)
    if p[0x23]:
        divisor = s16(maior)
        passo = (12800 // abs(divisor)) * (-1 if divisor < 0 else 1) if divisor else 12800
        por16(p, 0x28, passo)
        por32(p, 0x24, 0)


def calcular_linha(p):
    """ProjectileCalculLineaire, 0x46e4ca: um incremento, não um tick inteiro.

    Não verifica +02 (atividade), +04 ou colisão. +34=0 é no-op.
    A extração de y usa SHR lógico, inclusive para posições compactadas negativas.
    """
    restante = u16(p, 0x34)
    if not restante:
        return
    erro = s16(u16(p, 0x2e))
    deslocamento, correcao = (0x2a, 0x30) if erro >= 0 else (0x2c, 0x32)
    pos = (struct.unpack_from('<I', p, 8)[0] + s16(u16(p, deslocamento))) & 0xffffffff
    por32(p, 8, pos)
    por16(p, 0x2e, erro + u16(p, correcao))
    por16(p, 0xc, pos & 8191)
    por16(p, 0xe, pos >> 13)
    por16(p, 0x34, restante - 1)


@dataclass
class PoolProjeteis:
    """Memória fornecida explicitamente: não presume que MemAlloc zere o pool.

    efeito_externo(nome, args) aplica InfligeDegat/DecouvreTerrain/IllumineTerrain.
    raio_magia(id) consulta SortilegeGetRayonEffet; só tipo 28 precisa dela.
    Os callbacks podem modificar a memória, e a lista de chamadas é cumulativa.
    """
    memoria: bytearray
    efeito_externo: object = None
    raio_magia: object = None
    chamadas: list = field(default_factory=list)

    def __post_init__(self):
        if len(self.memoria) != TAMANHO * QUANTIDADE:
            raise ValueError('Pool deve conter exatamente 100 registros de 56 bytes')

    def registro(self, indice):
        if not 0 <= indice < QUANTIDADE:
            raise ValueError('Índice de projétil fora de 0..99')
        return memoryview(self.memoria)[indice * TAMANHO:(indice + 1) * TAMANHO]

    def resetar(self):
        """0x46e00a: limpa somente +02 dos 100 registros."""
        for i in range(QUANTIDADE):
            self.memoria[i * TAMANHO + 2] = 0

    def existe(self, indice):
        """0x46e02c: byte bruto em AL, sem normalização booleana."""
        return self.registro(indice)[2]

    def livre(self):
        """0x46e422: primeiro +02==0; pool cheio retorna 100, não ffff."""
        return next((i for i in range(QUANTIDADE) if not self.memoria[i * TAMANHO + 2]), QUANTIDADE)

    def _efeito(self, nome, *args):
        self.chamadas.append((nome, args))
        if self.efeito_externo is None:
            raise NotImplementedError(f'Efeito externo necessário: {nome}')
        self.efeito_externo(nome, args)

    def definir(self, indice, tipo, origem, alvo, modo, atacante, direcao, dx, dy, flag):
        """ProjectileSet 0x46e208, incluindo pedidos de efeitos dos tipos 26/28.

        Não limpa o registro inteiro. Fonte/destino/atacante u16; tipo, modo,
        direção e flag u8; offsets s16. Permite sobrescrever um slot ativo.
        """
        p = self.registro(indice)
        tipo, modo, direcao, flag = (v & 255 for v in (tipo, modo, direcao, flag))
        origem, alvo, atacante = (v & 65535 for v in (origem, alvo, atacante))
        dx, dy = s16(dx), s16(dy)
        p[0], p[1], p[2], p[3] = tipo, 1, 1, 0
        por16(p, 0x14, origem)
        por16(p, 0x16, alvo)
        p[0x23] = flag
        por16(p, 0xc, (origem & 255) * 32 + dx)
        por16(p, 0xe, (origem >> 8) * 32 + dy)
        por16(p, 0x10, dx)
        por16(p, 0x12, dy)
        por32(p, 0x24, 0)
        por16(p, 0x28, 0)
        p[0x18], p[0x19] = 0, 0
        por16(p, 0x1a, 12)
        por16(p, 0x1c, 0)
        p[0x1f], p[0x22] = modo, direcao
        por16(p, 0x20, atacante)
        if tipo in (1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 17, 20, 21, 22, 23, 29, 30):
            if tipo in (1, 9, 17, 20, 21, 22, 23):
                p[1] = 0
            limites_contador = {1: 15, 2: 10, 3: 8, 4: 4, 9: 2, 10: 2, 11: 2,
                           12: 2, 13: 2, 17: 15, 20: 15, 21: 15, 22: 15, 23: 15}
            if tipo in limites_contador:
                p[4] = limites_contador[tipo]
            if tipo in (9, 10, 11, 12, 13):
                por16(p, 0x1a, 5)
            p[0x19] = int(tipo in (1, 2, 3, 4, 9, 10, 11, 12))
            preparar_linha(p)
            if tipo == 9:
                por16(p, 0x1c, 5)
            elif tipo in (1, 17, 20, 21, 22, 23):
                por16(p, 0x1c, 10)
            if tipo in (20, 21, 22, 23, 29, 30):
                por16(p, 0x1a, 20)
        elif tipo in (15, 16) and flag:
            por32(p, 0x24, 12800)
        elif tipo == 26:
            self._efeito('InfligeDegat', alvo, modo, atacante, direcao, 0)
        elif tipo == 28:
            if self.raio_magia is None:
                raise NotImplementedError('Consulta externa necessária: SortilegeGetRayonEffet')
            raio = self.raio_magia(0) & 65535
            self._efeito('DecouvreTerrain', alvo, (raio + 2) & 65535, atacante & 255)
            raio = self.raio_magia(0) & 65535  # consulta repetida no original
            self._efeito('IllumineTerrain', alvo, raio, atacante & 255)

    def iniciar(self, tipo, origem, alvo, modo, atacante, direcao, dx, dy, flag):
        """ProjectileInit 0x46e44c: primeiro livre; pool cheio não emite efeitos.

        Retorna o índice escolhido ou 100 como conveniência da API Python.
        Não atribui esse contrato a EAX, que o original deixa clobberado por Set.
        """
        indice = self.livre()
        if indice < QUANTIDADE:
            self.definir(indice, tipo, origem, alvo, modo, atacante, direcao, dx, dy, flag)
        return indice
