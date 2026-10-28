"""Selective original market reset/quit operations on shared Mercado buffers."""
import struct

from economia import _jogador
from mercado import Mercado

# Raw names deliberately avoid assigning an unproved gameplay meaning.
BUFFERS_CICLO = {
    'bytes_2e7c': (0x4e2e7c, 4),
    'bytes_292c': (0x4e292c, 4),
    'bytes_2928': (0x4e2928, 4),
    'words_2938': (0x4e2938, 8),
    'words_2940': (0x4e2940, 8),
}


class CicloMercado:
    """Shares Mercado; copies five additional loaded buffers (zero if omitted).

    First/second indices truncate to u8 then require 0..3. The second guard
    occurs AFTER the first player's original writes. Errors retain those
    writes. The native executable itself has no corresponding index guards.
    No callbacks, proposal transfers, approval changes or world effects occur.
    """
    def __init__(self, mercado=None, **buffers):
        if set(buffers) - BUFFERS_CICLO.keys():
            raise TypeError('Buffer de ciclo do mercado desconhecido')
        self.mercado = Mercado() if mercado is None else mercado
        for nome, (_, tamanho) in BUFFERS_CICLO.items():
            dados = buffers.get(nome)
            bloco = bytearray(tamanho if dados is None else dados)
            if len(bloco) != tamanho:
                raise ValueError(f'{nome} deve ter {tamanho} bytes')
            setattr(self, nome, bloco)

    def _escrever(self, nome, jogador, valor):
        bloco = getattr(self.mercado, nome) if nome in ('contatos', 'indicadores') else getattr(self, nome)
        if nome in ('indicadores', 'words_2938', 'words_2940'):
            struct.pack_into('<H', bloco, jogador * 2, valor)
        else:
            bloco[jogador] = valor

    def resetar_todos(self):
        """MarcheResetAll 0x46027c: seven writes per player in ascending order."""
        for j in range(4):
            for nome, valor in (('bytes_2e7c', 0), ('indicadores', 0), ('contatos', 255),
                                ('bytes_292c', 1), ('bytes_2928', 0),
                                ('words_2940', 0), ('words_2938', 0)):
                self._escrever(nome, j, valor)

    def resetar(self, jogador, outro):
        """ResetMarche 0x46634e: first row then protected second row."""
        j = _jogador(jogador)
        for nome, valor in (('bytes_2e7c', 0), ('bytes_292c', 1), ('bytes_2928', 0),
                            ('contatos', 255), ('indicadores', 0),
                            ('words_2940', 0), ('words_2938', 0)):
            self._escrever(nome, j, valor)
        k = _jogador(outro)
        for nome, valor in (('bytes_2e7c', 0), ('contatos', 255), ('bytes_292c', 1),
                            ('bytes_2928', 0), ('words_2938', 0),
                            ('words_2940', 0), ('indicadores', 0)):
            self._escrever(nome, k, valor)

    def sair(self, jogador):
        """MarcheQuitte 0x4663d6: capture contact BEFORE first reset writes."""
        j = _jogador(jogador)
        outro = self.mercado.contatos[j]
        self.resetar(j, outro)
