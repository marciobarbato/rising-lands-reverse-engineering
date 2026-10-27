"""Contornos de CheminCalcul: dois sentidos, regiões e saída por linha direta.

Tradução do corpo para as classes de ocupação 1, 2 e 3, incluindo
normalização das estruturas pela grade auxiliar de cores.
"""
import struct
from dataclasses import dataclass
from caminhos import aliados, testar_mascara_celula
from movimento import VETORES
from estruturas_caminhos import observar_estrutura
from otimizacao_caminhos import direcao_busca, passagem_da_busca


@dataclass(frozen=True)
class PassoContorno:
    celula: int
    anterior: int
    direcao: int
    tentativas: tuple


@dataclass(frozen=True)
class ResultadoContornos:
    custos: tuple
    buffers: tuple
    registros: tuple
    regioes: bytes
    quantidade_regioes: int
    fase: int
    status_falha: object
    passos: tuple


def vizinha_contorno(mundo, celula, direcao):
    dx, dy = VETORES.get(direcao & 15, (0, 0))
    x, y = (celula & 255) + dx, (celula >> 8) + dy
    return x + y * 256 if 0 <= x < mundo.largura and 0 <= y < mundo.altura else 0xffff


def escolher_passo_contorno(contexto, atual, obstaculo, sentido):
    """0x430bc5..0x431ec8 e espelho: gira dois índices, no máximo dez testes."""
    if sentido not in (-1, 1):
        raise ValueError('Sentido deve ser -1 ou 1')
    d = direcao_busca(atual, obstaculo)
    candidato = vizinha_contorno(contexto.mundo, atual, d)
    anterior, tentativas = candidato, []
    for _ in range(10):
        tentativas.append(candidato)
        if passagem_da_busca(contexto, candidato, d):
            return PassoContorno(candidato, anterior, d, tuple(tentativas))
        anterior = candidato
        d = (d + sentido * 2) & 15
        candidato = vizinha_contorno(contexto.mundo, atual, d)
        if candidato == obstaculo:
            break
    return PassoContorno(0xffff, anterior, d, tuple(tentativas))


class _RegioesContorno:
    def __init__(self, contexto, inicio, residuos):
        self.contexto, self.origem = contexto, inicio.regiao_origem
        self.dados = bytearray(residuos)
        if len(self.dados) != 510:
            raise ValueError('Lista original de regiões tem 255 palavras')
        self.quantidade = 0
        for valor in inicio.regioes:
            self._adicionar(valor)

    def _adicionar(self, valor):
        if self.quantidade < 255:
            struct.pack_into('<H', self.dados, self.quantidade * 2, valor)
            self.quantidade += 1

    def contem(self, valor):
        return valor in struct.unpack_from('<' + 'H' * self.quantidade, self.dados)

    def registrar(self, valor, registro, fase, deduplicar=True, celula=0):
        if valor in (0, self.origem):
            return
        if valor & 0x8000:
            normalizado = observar_estrutura(self.contexto, valor, celula, registro, fase)
            if not deduplicar or not self.contem(normalizado):
                self._adicionar(normalizado)
            return
        if deduplicar and self.contem(valor):
            return
        if not valor & 0x4000:
            self._adicionar(valor)
            return
        outro = (valor & 0x3ff8) >> 3
        c = self.contexto
        if outro == c.unidade:
            return
        inimigo = int(not aliados(c.mundo.unidades[outro * 276], c.dono, c.mundo.mascaras_alianca))
        if not registro[4] or inimigo > registro[6]:
            struct.pack_into('<H', registro, 0, outro)
            registro[4], registro[6], registro[8] = 1, inimigo, fase & 255
        if valor & 4:
            if self.quantidade < 0xfb:
                for j in range(4): self._adicionar((valor & 0xfffc) + j)
        else:
            self._adicionar(valor)


def _linha_sai_do_contorno(contexto, atual, destino, regioes, registro, fase):
    """Permite sair quando a linha não encontra região já contornada."""
    d = direcao_busca(atual, destino)
    primeira = vizinha_contorno(contexto.mundo, atual, d)
    if not passagem_da_busca(contexto, primeira, d):
        encontrou = False
        for delta in _subcelulas(contexto, primeira):
            valor = contexto.mundo.regioes[(primeira - delta) & 65535]
            if valor & 0xc000 == 0x4000:
                regioes.registrar(valor, registro, fase, deduplicar=False)
                encontrou = True
        if encontrou:
            return False
    for _ in range(255):
        if atual == destino:
            return True
        if not passagem_da_busca(contexto, atual, d):
            for delta in _subcelulas(contexto, atual):
                valor = contexto.mundo.regioes[(atual - delta) & 65535]
                if valor != regioes.origem:
                    if valor & 0x8000:
                        valor = observar_estrutura(contexto, valor, (atual - delta) & 65535, registro, fase)
                    if regioes.contem(valor):
                        return False
        d = direcao_busca(atual, destino)
        atual = vizinha_contorno(contexto.mundo, atual, d)
        if atual == 0xffff:
            return False
    return True


def _subcelulas(contexto, celula):
    if contexto.classe == 1:
        return (0,)
    return (0,) + ((1,) if celula & 255 else ()) + ((256,) if celula > 255 else ()) + ((257,) if celula & 255 and celula > 256 else ())


def _regiao_deixada(contexto, anterior, escolhida):
    m = contexto.mundo
    if contexto.classe == 1:
        return m.regioes[anterior], anterior
    for direcao in (None, 1, 3, 5):
        c = anterior if direcao is None else vizinha_contorno(m, anterior, direcao)
        if (testar_mascara_celula(m.objetos[c], m.atributos[c], contexto.mascara) and
                escolhida - c not in (0, 1, 257, 256)):
            return m.regioes[c], c
    return 0, anterior


def construir_contornos(contexto, inicio, buffers=None, residuos_regioes=None, registros_anteriores=None):
    """Traduz os dois percursos das classes 1..3, preservando caudas dos buffers.

    As rotas param quando a linha até o destino deixa o conjunto de regiões
    contornadas; podem ser parciais. Não há promessa de caminho mínimo.
    """
    if contexto.classe not in (1, 2, 3):
        raise NotImplementedError('Contorno exige classe de ocupação 1, 2 ou 3')
    buffers = buffers or (bytes(512), bytes(512))
    if len(buffers) != 2 or any(len(b) != 512 for b in buffers):
        raise ValueError('São necessários dois buffers de 512 bytes')
    saidas = [bytearray(b) for b in buffers]
    for b in saidas: struct.pack_into('<H', b, 0, 0)
    regioes = _RegioesContorno(contexto, inicio, residuos_regioes or bytes(510))
    registros = [bytearray(inicio.registro_ocupantes), bytearray(registros_anteriores[1] if registros_anteriores else bytes(10))]
    custos, historico, fase = [0, 0], [], 0
    if inicio.todos_bloqueados:
        return ResultadoContornos(tuple(custos), tuple(bytes(b) for b in saidas), tuple(bytes(r) for r in registros),
                                   bytes(regioes.dados), regioes.quantidade, 0, 8, ())
    for lado, sentido in enumerate((-1, 1)):
        if lado == 1: registros[1][:] = bytes(10)
        atual, obstaculo = inicio.inicio, inicio.obstaculo_proximo
        regioes.quantidade, fase = len(inicio.regioes), 0
        quantidade = 0
        while True:
            passo = escolher_passo_contorno(contexto, atual, obstaculo, sentido)
            historico.append(dict(lado=lado, atual=atual, obstaculo=obstaculo,
                                   celula=passo.celula, anterior=passo.anterior))
            if passo.celula == 0xffff or passo.anterior == 0xffff:
                custos[lado] = 0xffff
            else:
                valor, celula_obstaculo = _regiao_deixada(contexto, passo.anterior, passo.celula)
                regioes.registrar(valor, registros[lado], fase, celula=celula_obstaculo)
                obstaculo, atual = passo.anterior, passo.celula
                fase = (fase + 1) & 255
                custos[lado] = (custos[lado] + 1) & 65535
                quantidade += 1
                struct.pack_into('<H', saidas[lado], quantidade * 2, atual)
            saiu = _linha_sai_do_contorno(contexto, atual, inicio.destino, regioes, registros[lado], fase)
            if saiu or custos[lado] == 0xffff or quantidade >= 255 or passo.celula == inicio.destino:
                break
        if atual != inicio.destino:
            d = direcao_busca(atual, inicio.destino)
            proxima = vizinha_contorno(contexto.mundo, atual, d)
            if (passagem_da_busca(contexto, proxima, d) and custos[lado] != 0xffff and
                    quantidade < 255 and proxima != inicio.destino):
                quantidade += 1
                struct.pack_into('<H', saidas[lado], quantidade * 2, proxima)
                fase = (fase + 1) & 255
        struct.pack_into('<H', saidas[lado], 0, quantidade)
    falha = (8 if all(struct.unpack_from('<H', b)[0] == 0 for b in saidas) else 6) if custos == [0xffff,0xffff] else None
    return ResultadoContornos(tuple(custos), tuple(bytes(b) for b in saidas), tuple(bytes(r) for r in registros),
                               bytes(regioes.dados), regioes.quantidade, fase, falha, tuple(historico))
