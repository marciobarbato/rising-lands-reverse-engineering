"""Consulta de recursos e avaliação de propostas do mercado.

EvalueCoutProposition 0x466bac e GetNbRessource 0x462a58, com seus três
acessores de jogadores. Não aceita propostas nem executa transferências.
Índices protegidos nesta API não equivalem a verificações do executável.
"""
import struct

from economia import Economia, _buffer_vivo, _i32, _jogador

JOGADORES = 0x5080a8   # DWORD pointer to the four 20-byte player records

# As quatro linhas pertencem ao jogador da proposta, inclusive as quantidades
# pedidas ao contato. As tabelas de preços são globais, não por jogador.
BUFFERS = {
    'contatos': (0x496f8c, 4),
    'precos_unidades': (0x496fb0, 26),
    'precos_recursos': (0x496fcc, 3),
    'indicadores': (0x4e2930, 8),
    'diferenca': (0x4e2948, 2),
    'unidades_oferecidas': (0x4e29bc, 208),
    'unidades_pedidas': (0x4e2a8c, 208),
    'recursos_oferecidos': (0x4e2cfc, 24),
    'recursos_pedidos': (0x4e2d14, 24),
}


def _idiv(numerador, divisor):
    """IDIV signed32: truncamento para zero, após wrap do produto."""
    numerador, divisor = _i32(numerador), _i32(divisor)
    if divisor == 0:
        raise ZeroDivisionError('IDIV na avaliação da proposta')
    if numerador == -0x80000000 and divisor == -1:
        raise OverflowError('Quociente IDIV fora de signed32')
    q = abs(numerador) // abs(divisor)
    return -q if (numerador < 0) != (divisor < 0) else q


class Mercado:
    """Compartilha Economia; copia buffers do mercado e quatro jogadores × 20.

    jogadores: conteúdo apontado por DWORD 0x5080a8; +1 tipo, +6 bits de
    aliança, +12 quatro simpatias signed16 direcionais. Os demais bytes
    ficam intactos. Valores omitidos são sintéticos (zero), não a carga do jogo.
    The constructor copies (fixture form); ``Mercado.vivo``/``da_memoria`` bind live memory.
    """
    @classmethod
    def vivo(cls, economia, *, jogadores, **buffers):
        """Bind the live player records and every market buffer by identity: no copy.

        ``economia`` must itself be live (``Economia.vivo``); ``jogadores`` is the
        80-byte block [0x5080a8] points to; ``buffers`` are all of BUFFERS. Every
        argument is checked before binding.
        """
        if not isinstance(economia, Economia):
            raise TypeError('economia must be Economia.vivo over the live resource table')
        _buffer_vivo(economia.memoria, 128, 'Live resource table (0x4e2ea8)')
        if set(buffers) != BUFFERS.keys():
            raise TypeError('Every market buffer is required: ' + ', '.join(sorted(BUFFERS)))
        vivos = {n: _buffer_vivo(buffers[n], t, f'Live {n} ({a:#x})') for n, (a, t) in BUFFERS.items()}
        jogadores = _buffer_vivo(jogadores, 80, 'Live player records ([0x5080a8])')
        self = cls.__new__(cls)
        self.economia, self.jogadores = economia, jogadores
        for nome, buffer in vivos.items():
            setattr(self, nome, buffer)
        return self

    @classmethod
    def da_memoria(cls, m):
        """``vivo`` over a live memory map; the player records are read through the pointer at 0x5080a8."""
        registros = struct.unpack('<I', bytes(m.ler(JOGADORES, 4)))[0]
        self = cls.vivo(Economia.da_memoria(m), jogadores=m.vista(registros, 80),
                        **{n: m.vista(a, t) for n, (a, t) in BUFFERS.items()})
        # Bound this way, aliado runs the original PlayerEstAllie over m (quadro_economia.aliado): the
        # allocation holds five records and the original reads record 4; no 0..3 protection.
        self.memoria_viva = m
        return self

    def __init__(self, economia=None, *, jogadores=None, **buffers):
        # Legacy/fixture form: copies. Use Mercado.vivo/da_memoria for the live original memory.
        if set(buffers) - BUFFERS.keys():
            raise TypeError('Buffer de mercado desconhecido')
        self.economia = Economia() if economia is None else economia
        self.jogadores = bytearray(80 if jogadores is None else jogadores)
        if len(self.jogadores) != 80:
            raise ValueError('Jogadores devem ter quatro registros de 20 bytes')
        for nome, (_, tamanho) in BUFFERS.items():
            dados = buffers.get(nome)
            bloco = bytearray(tamanho if dados is None else dados)
            if len(bloco) != tamanho:
                raise ValueError(f'{nome} deve ter {tamanho} bytes')
            setattr(self, nome, bloco)

    def tipo_jogador(self, jogador):
        """PlayerGetType 0x46d817: AL; inválido após u8 devolve 2."""
        j = jogador & 255
        return self.jogadores[j * 20 + 1] if j < 4 else 2

    def aliado(self, jogador, outro):
        """PlayerEstAllie 0x46d838, domínio protegido 0..3, AL e DL.

        É direcional; igualdade retorna 1 sem consultar a máscara.
        Bound by ``da_memoria``, it runs the original over live memory instead (any AL/DL).
        """
        if getattr(self, 'memoria_viva', None) is not None:
            from quadro_economia import aliado
            return aliado(self.memoria_viva, jogador, outro)
        j, k = _jogador(jogador), _jogador(outro)
        return int(j == k or bool(self.jogadores[j * 20 + 6] & (1 << k)))

    def simpatia(self, jogador, outro):
        """PlayerGetSympathie 0x46dc6c: AX reinterpretado como signed16."""
        j, k = _jogador(jogador), _jogador(outro)
        return struct.unpack_from('<h', self.jogadores, j * 20 + 12 + k * 2)[0]

    def quantidade_recurso(self, jogador, recurso):
        """GetNbRessource 0x462a58: AL=recurso, DL=jogador no x86.

        Consulta total, não estoque. IDs 0 peças, 1 comida, 2 pedra;
        qualquer outro byte devolve 65535, inclusive ID 3.
        """
        saldos = self.economia.consultar(jogador)
        r = recurso & 255
        return (saldos.pecas, saldos.comida, saldos.pedra)[r] if r < 3 else 65535

    def _valor(self, jogador, unidades, recursos):
        quantidades = struct.unpack_from('<26H', unidades, jogador * 52)
        materias = struct.unpack_from('<3H', recursos, jogador * 6)
        return (sum(q * p for q, p in zip(quantidades, self.precos_unidades))
                + sum(q * p for q, p in zip(materias, self.precos_recursos)))

    def avaliar(self, jogador):
        """EvalueCoutProposition 0x466bac, jogador em AL; retorna None.

        Escreve somente indicador u16 do jogador e diferença global u16.
        Não consulta suficiência, não debita saldos nem limpa a proposta.
        Uma divisão por zero ocorre antes das duas escritas.
        """
        j = _jogador(jogador)
        contato = _jogador(self.contatos[j])
        oferecido = self._valor(j, self.unidades_oferecidas, self.recursos_oferecidos)
        pedido = self._valor(j, self.unidades_pedidas, self.recursos_pedidos)
        tipo = self.tipo_jogador(j)
        simpatia = self.simpatia(j, contato) if tipo == 2 else self.simpatia(contato, j)
        fator = 80 + simpatia + 40 * self.aliado(contato, j)
        if tipo == 2:
            ajustado = _idiv(pedido * 100, fator)
            indicador = _idiv(ajustado * 100, oferecido) if oferecido else 100
            diferenca = ajustado - oferecido
        else:
            ajustado = _idiv(oferecido * fator, 100)
            indicador = _idiv(ajustado * 100, pedido) if pedido else (200 if ajustado else 0)
            diferenca = ajustado - pedido
        struct.pack_into('<H', self.indicadores, j * 2, indicador & 65535)
        struct.pack_into('<H', self.diferenca, 0, diferenca & 65535)
