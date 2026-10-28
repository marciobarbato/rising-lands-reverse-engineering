"""Read-only volume and bounded EnginAsk; pending sound insertion is explicit."""
from dataclasses import dataclass
import struct

from movimento import distancia_quadratica
from selecao_unidades import unidade_selecionada


def _registro(mundo, indice):
    indice &= 65535
    if not isinstance(mundo.unidades, bytearray) or len(mundo.unidades) != 220800 or indice >= 800:
        raise ValueError('Unit voice requires live 800-record pool and unit 0..799')
    if not 0 <= mundo.jogador_local < 4:
        raise ValueError('Unit voice requires local camera owner 0..3')
    return indice*276


def consultar_volume_unidade(mundo, indice, janela):
    """Complete 0x440c5d, full EAX 0..256; explicit four u16 viewport words."""
    p = _registro(mundo, indice)
    if not isinstance(janela, (tuple,list)) or len(janela) != 4:
        raise ValueError('Volume requires viewport (x,y,width,height) as four loaded words')
    x, y, largura, altura = (v & 65535 for v in janela)
    celula = struct.unpack_from('<H', mundo.unidades, p+8)[0]
    distancia = distancia_quadratica(x+largura//2, y+altura//2, celula & 255, celula >> 8)
    if distancia >= 0x80000000:
        distancia -= 0x100000000
    volume = 256 if distancia <= 145 else 180 if distancia <= 300 else 100 if distancia < 600 else 0
    if not unidade_selecionada(mundo, mundo.jogador_local, indice):
        volume //= 2
    return volume


@dataclass(frozen=True)
class SolicitacaoSomUnidade:
    unidade: int
    codigo: int
    flag: int
    volume: int
    offset_handle: int
    opcode: int = 0x50


class DependenciaVozUnidade(NotImplementedError):
    def __init__(self, unidade, efeito, endereco, checkpoint, solicitacao=None):
        self.unidade, self.efeito = unidade, efeito
        self.endereco, self.checkpoint, self.solicitacao = endereco, checkpoint, solicitacao
        super().__init__(f'{efeito} required at 0x{endereco:x}; prior live stores retained')


def solicitar_voz_unidade(mundo, indice, modo, flag, *, janela=None):
    """Complete hidden/active-handle EnginAsk; never discard an inactive request."""
    indice, modo, flag = indice & 65535, modo & 65535, flag & 255
    p = _registro(mundo, indice)
    celula = struct.unpack_from('<H', mundo.unidades, p+8)[0]
    if not mundo._visivel(celula):
        return
    if janela is None:
        raise DependenciaVozUnidade(indice, 'EnginGetVolume viewport', 0x440c5d, 0x440d9f)
    volume = consultar_volume_unidade(mundo, indice, janela)
    if modo == 16:
        volume = 256
    handle = struct.unpack_from('<I', mundo.unidades, p+0x104)[0]
    mundo.unidades[p+0xf9] = flag
    if handle != 0xffffffff:
        return
    pedido = SolicitacaoSomUnidade(indice, (mundo.unidades[p+1] << 16) | (modo << 8),
                                  flag, volume, p+0x104)
    raise DependenciaVozUnidade(indice, 'PlaySnd_PostSound/HandlSnd_Insert', 0x48aa79, 0x440de7, pedido)


@dataclass(frozen=True)
class SolicitacaoSaidaTropa:
    indice: int
    unidade: int
    celula: int
    tipo_unidade: int
    destino_ordem: int
    endereco_dependencia: int = 0x420fb7


def retomar_solicitacao_saida(mundo, pedido, *, janela=None):
    """0x420f9e..0x420fb7; only reach cleanup after the supported request returns."""
    if pedido.endereco_dependencia != 0x420f9e:
        raise ValueError('Expected placement/order handoff at 0x420f9e')
    indice, unidade, celula = pedido.indice & 65535, pedido.unidade & 65535, pedido.celula & 65535
    tipo, destino = pedido.tipo_unidade & 255, pedido.destino_ordem & 65535
    _registro(mundo, unidade)
    if not isinstance(mundo.estruturas, bytearray) or len(mundo.estruturas) != 276000 or indice >= 1000:
        raise ValueError('Request continuation requires building 0..999 and writable structure pool')
    if mundo.estruturas[indice*276+4] == mundo.jogador_local:
        solicitar_voz_unidade(mundo, unidade, 6, 0, janela=janela)
    return SolicitacaoSaidaTropa(indice, unidade, celula, tipo, destino)
