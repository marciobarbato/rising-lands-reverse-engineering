"""Subestados de CalculAttaqueEngin (0x451914), sem física, som ou dano.

Muta registros e contexto de busca locais. Efeitos externos são chamadas
explícitas: o chamador deve fornecê-los, inclusive se quiser um ensaio sem
efeitos. Não implementa dano nem avança projéteis. Uma chamada é um passo da
rotina, não uma unidade de tempo calibrada.
"""
from dataclasses import dataclass, field
import json
from pathlib import Path
import struct

from alvos_alcance import (a_portee, a_portee_minimale, linha_de_tiro, palavra,
                           arma_carregada, TIPOS_GRANDES, IGNORAM_LINHA, _consulta)
from mira_angular import angulo_calcul, engin_vise_cible, mira_requerida

DADOS = json.loads((Path(__file__).resolve().parent / 'evidencias/dados-disparo.json').read_text())
TIPOS_ANIMAM = frozenset((0, 1, 2, 3, 4, 8, 11, 14, 15, 18, 19, 20, 21, 22, 23, 24, 25))
VETORES = {1: (-1, 0), 3: (-1, -1), 5: (0, -1), 7: (1, -1),
           9: (1, 0), 11: (1, 1), 13: (0, 1), 15: (-1, 1)}


def guardar(u, off, valor):
    struct.pack_into('<H', u, off, valor & 65535)


def sinal16(v):
    return ((v + 32768) & 65535) - 32768


def animar(u, periodo, quadros):
    """Incremento u8, igualdade de período, (quadro+1) em 32 bits antes do mod."""
    u[0xa9] = (u[0xa9] + 1) & 255
    if u[0xa9] == periodo:
        # Divisor zero provoca erro também no x86; não inventar um quadro.
        novo = (u[0xa4] + 1) % quadros
        u[0xa9], u[0xa4] = 0, novo


def anim_attaque_engin(u):
    """0x4479c4: muitos tipos não animam aqui; subestados 2/3 também não."""
    if u[1] in TIPOS_ANIMAM and u[0x8a] in (0, 1):
        animar(u, u[0xa7] if u[0x8a] == 0 else u[0xa8],
               u[0xa5] if u[0x8a] == 0 else u[0xa6])


def anim_attaque_termine_engin(u):
    """0x447977: só retorna verdadeiro para tipo 2, quadro +a4 igual a 1."""
    return u[1] == 2 and u[0xa4] == 1


def girar(u, torre=False):
    """0x448599/0x4484a7, atualização apenas dos campos de orientação."""
    if torre and u[1] not in (12, 15):
        return
    if not torre and u[1] in (12, 15):
        u[0xda] = ((u[0x90] - 1) * 2 + 1) & 255
    desejada, atual, contador, n = (0xda, 0x94, 0x96, 32) if torre else (0x90, 0x91, 0x92, 16)
    if u[desejada] == u[atual]:
        return
    u[contador] = (u[contador] + 1) & 255
    if u[contador] != u[0x93]:
        return
    d, a = u[desejada], u[atual]
    aumenta = (d > a and d - a < n // 2) or (a > d and a - d > n // 2)
    u[atual] = a % n + 1 if aumenta else (n if a == 1 else (a - 1) & 255)
    u[contador] = 0


def saida_projetil(tipo, orientacao):
    """0x4511a5: offsets u16 somados ao deslocamento de corpo, depois s16."""
    entrada = DADOS['saidas'].get(str(tipo))
    x = y = 0
    if entrada:
        n = len(entrada['pares'])
        d = orientacao & 255
        i = ((d - 1) & 255) if n == 32 else (int((d - 1) / 2) & 255)
        if i >= n:
            raise ValueError('Orientação lê fora da tabela de saída no original')
        x, y = entrada['pares'][i]
    bx, by = DADOS['deslocamento_corpo'][tipo]
    return sinal16(x + bx), sinal16(y + by)


@dataclass
class BuscaAtaque:
    unidade: int = 0xffff
    ocupada: int = 0
    sucesso: int = 0
    ponteiro_rota: int = 0

    def liberar(self, indice):
        if self.unidade == indice:
            self.unidade = 0xffff
            self.ocupada = self.sucesso = self.ponteiro_rota = 0


@dataclass
class ContextoAtaque:
    unidades: list
    recargas: dict = field(default_factory=dict)
    modificadores: dict = field(default_factory=dict)
    terreno: dict = field(default_factory=dict)
    largura: int = 256
    altura: int = 256
    busca: BuscaAtaque = field(default_factory=BuscaAtaque)
    celula_construcao: object = None
    celula_construcao_adjacente: object = None
    adjacente_construcao: object = None
    alcance_magia: object = None
    descoberto: object = None
    efeito_externo: object = None
    chamadas: list = field(default_factory=list)

    def emitir(self, nome, *args):
        self.chamadas.append((nome, tuple(args)))
        return _consulta(self.efeito_externo, nome, nome, tuple(args))

    def alcance(self, i):
        u = self.unidades[i]
        return a_portee(self.unidades, i, u[0xb7], palavra(u, 0xb8),
            self.modificadores.get((u[0], u[1], 4), 0),
            celula_construcao=self.celula_construcao, adjacente_construcao=self.adjacente_construcao,
            alcance_magia=self.alcance_magia)

    def alvo(self, i, centro=False):
        u = self.unidades[i]
        modo, ref = u[0xb7], palavra(u, 0xb8)
        if modo == 1:
            if ref >= 800:
                raise IndexError('Unidade alvo fora de 0..799')
            return palavra(self.unidades[ref], 0x7c)
        if modo == 5:
            return ref
        if modo == 3:
            c = 0xffff
            if not centro and u[0xb0] in (0, 1):
                c = _consulta(self.celula_construcao_adjacente, 'BatimentGetCaseAdjacent', ref, palavra(u, 0x7c)) & 65535
            if c == 0xffff:
                c = _consulta(self.celula_construcao, 'BatimentGetCase', ref) & 65535
            return c
        raise ValueError('Máquina traduzida para modos 1/3/5')

    def mira(self, i):
        return engin_vise_cible(self.unidades, i, celula_construcao=self.celula_construcao,
                                celula_construcao_adjacente=self.celula_construcao_adjacente)

    def vizinha(self, c, d):
        x, y = c & 255, c >> 8
        dx, dy = VETORES.get(d, (0, 0))
        x, y = x + dx, y + dy
        return x + y * 256 if 0 <= x < self.largura and 0 <= y < self.altura else 65535


def direcao_sinais(a, b):
    dx, dy = (b & 255) - (a & 255), (b >> 8) - (a >> 8)
    v = ((dx > 0) - (dx < 0), (dy > 0) - (dy < 0))
    return next((d for d, vetor in VETORES.items() if vetor == v), 0)


def definir_destino(ctx, i, destino, sempre=False):
    u = ctx.unidades[i]
    if sempre or palavra(u, 0x7e) != destino:
        guardar(u, 0x7e, destino)
        ctx.busca.liberar(i)
        u[0x88] = 0


def preparar(ctx, i):
    u = ctx.unidades[i]
    if not u[0x86] and not u[0x87] and ctx.alcance(i) and linha_de_tiro(
            u, ctx.alvo(i, centro=True), ctx.terreno, ctx.largura, ctx.altura):
        definir_destino(ctx, i, palavra(u, 0x7c), sempre=True)
        info = mira_requerida(ctx.unidades, i, celula_construcao=ctx.celula_construcao,
                              celula_construcao_adjacente=ctx.celula_construcao_adjacente)
        if u[1] in (12, 15):
            u[0xda] = info['orientacao_requerida']
            if u[0x94] != u[0xda]:
                girar(u, torre=True)
                return
        else:
            u[0x90] = info['orientacao_requerida']
            if u[0x91] != u[0x90]:
                girar(u)
                return
        base = ctx.recargas[u[1]]
        if not arma_carregada(palavra(u, 0x102), base, ctx.modificadores.get((u[0], u[1], 3), 0)):
            return
        guardar(u, 0x102, 0)
        u[0x8a] = 1
        if u[1] != 16:
            u[0xa4] = u[0xa9] = 0
        if u[1] in (14, 16) and not u[0xda]:
            ctx.emitir('SetDeplaceEngin', i, palavra(u, 0x7c))
        return
    if not u[0x86] and not u[0x87]:
        if not ctx.alcance(i):
            definir_destino(ctx, i, ctx.alvo(i))
        elif not a_portee_minimale(ctx.unidades, i, u[0xb7], palavra(u, 0xb8)):
            destino = ctx.alvo(i)
            atual = palavra(u, 8)
            if destino != atual:
                primeiro = ctx.vizinha(atual, direcao_sinais(destino, atual))
                destino = ctx.vizinha(atual, direcao_sinais(primeiro, atual))
            definir_destino(ctx, i, destino)
        elif u[1] in IGNORAM_LINHA:
            return
        else:
            definir_destino(ctx, i, ctx.alvo(i))
    ctx.emitir('DeplaceEngin', i)


def disparar(ctx, i):
    u = ctx.unidades[i]
    alvo = ctx.alvo(i)
    if u[2] == 24:
        ctx.emitir('SortilegeEffet', i, u[0xf4], palavra(u, 0xb8))
        ctx.emitir('ResetOrdre', i)
    elif u[2] == 1:
        if _consulta(ctx.descoberto, 'TerrainEstDecouvert', palavra(u, 8)):
            volume = ctx.emitir('EnginGetVolume', i)
            u[0xf9] = 0
            if struct.unpack_from('<I', u, 0x104)[0] == 0xffffffff:
                ctx.emitir('PlaySnd_PostSound', 0x50, (u[1] << 16) | 0x2300, 0, volume, i)
        if u[1] in (14, 16) and u[0xda]:
            u[0xda] -= 1
        if not u[0x78]:
            celula = alvo if u[1] in TIPOS_GRANDES else ctx.vizinha(palavra(u, 8), u[0x91])
            if u[1] == 16:
                ctx.emitir('ProjectileInit', 8, celula, celula, 1, i, 0, 0, 0, 0)
            ctx.emitir('InfligeDegat', celula, 1, i, 0, 0)
        else:
            desloc_x = desloc_y = 0
            if u[1] not in (1, 21, 11):
                desloc_x, desloc_y = saida_projetil(u[1], u[0x94] if u[1] in (12, 15) else u[0x91])
            direcao = u[0x91]
            if u[1] == 11:
                origem = palavra(u, 8)
                direcao = angulo_calcul(origem & 255, origem >> 8, alvo & 255, alvo >> 8, 32)
            if u[1] not in (3, 25):
                elevado = int(u[0xb7] == 1 and ctx.unidades[palavra(u, 0xb8)][1] in (16, 17))
                ctx.emitir('ProjectileInit', u[0x79], palavra(u, 8), alvo, 1, i, direcao,
                           desloc_x, desloc_y, elevado)
            if u[1] in (3, 11, 25):
                ctx.emitir('ProjectileInit', 33 if u[1] == 25 else 26, alvo, alvo, 1, i, direcao, 0, 0, 0)


def calcular_ataque(ctx, i):
    """Um despacho completo de 0x451914. Efeitos externos exigem callback.

    Não há atribuição a +8a=2 nem +8a=3 neste corpo. Esses subestados podem
    entrar prontos; a tradução não inventa transições para eles.
    """
    u = ctx.unidades[i]
    subestado = u[0x8a]
    if subestado == 0:
        preparar(ctx, i)
    elif subestado == 1:
        anim_attaque_engin(u)
        if not u[0xa9] and u[0xa4] == u[0x7a]:
            disparar(ctx, i)
        if not u[0xa9] and not u[0xa4]:
            if not u[0x8b]:
                u[0x8a] = 0
                if u[1] != 16:
                    u[0xa4] = 0
                guardar(u, 0x102, 0)
            else:
                u[0x8b] = (u[0x8b] - 1) & 255
                if u[1] in (3, 11):
                    u[0xa4] = 5 if u[1] == 3 else 0
    elif subestado == 2:
        if u[1] == 16:
            animar(u, u[0xa7], u[0xa5])
        elif u[1] == 17:
            ctx.emitir('AnimBallonStatic', i)
        if u[0x8b] == 1 and u[1] != 16:
            u[0xa4] = u[0xa9] = 0
        u[0x8b] = (u[0x8b] - 1) & 255
        if not u[0x8b]:
            u[0x8a] = 1
            if u[1] != 16:
                u[0xa4] = u[0xa9] = 0
            if u[1] in (14, 16):
                if not u[0xda]:
                    ctx.emitir('SetDeplaceEngin', i, palavra(u, 0x7c))
            elif not (ctx.alcance(i) and ctx.mira(i)):
                u[0x8a] = 0
    elif subestado == 3:
        # As chamadas aleatórias em 0x452b8b..0x452bf5 não são alcançáveis
        # pelo despacho válido; o próprio tipo 16 salta por esse código.
        if u[2] not in (0, 4):
            u[2] = 7
            ctx.busca.liberar(i)
        guardar(u, 0xb8, 0xffff)
        u[0xa4] = u[0xa9] = 0
    return ctx.chamadas
