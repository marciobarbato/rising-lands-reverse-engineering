"""VideMatiere 0x4663eb: transferência de recursos de uma linha de proposta.

Sem aceitação, transporte de unidades, limpeza da proposta ou rollback.
Os dois argumentos x86 são AL=jogador da proposta e DL=outro jogador.
"""
import struct

from economia import _jogador


class TransferenciasMercado:
    """Composição do Mercado e EconomiaConstrucoes com o mesmo saldo mutável."""
    def __init__(self, mercado, mundo):
        if mercado.economia is not mundo.economia:
            raise ValueError('Mercado e construções devem compartilhar a mesma Economia')
        self.mercado = mercado
        self.mundo = mundo

    def _creditar_direto(self, jogador, recurso, quantidade, *, total_primeiro):
        # Não usar Economia.creditar: aqui os dois words aumentam, sem teto 9999.
        o = jogador * 32 + recurso * 8
        memoria = self.mundo.economia.memoria
        rmi, total = struct.unpack_from('<HH', memoria, o)
        escritas = ((o + 2, total), (o, rmi)) if total_primeiro else ((o, rmi), (o + 2, total))
        for offset, valor in escritas:
            struct.pack_into('<H', memoria, offset, (valor + quantidade) & 65535)

    def transferir(self, jogador, outro):
        """Debita condicionalmente e credita integralmente, na ordem do x86.

        Usa as duas metades da linha `jogador`; não consulta `contatos`.
        Para IDs 0,1,2: oferecido vai de jogador para outro; depois pedido
        vai de outro para jogador. Cada débito precede seu crédito. Somente
        tipo 1 paga, via BatimentEnleveMatiere, inclusive quando quantidade=0.
        Divisão por zero no recálculo deixa os efeitos anteriores aplicados.
        A API retorna None e protege índices u8 fora de 0..3.
        """
        j, k = _jogador(jogador), _jogador(outro)
        for recurso in range(3):
            q = struct.unpack_from('<H', self.mercado.recursos_oferecidos, j * 6 + recurso * 2)[0]
            if self.mercado.tipo_jogador(j) == 1:
                self.mundo.retirar(j, recurso, q)
            self._creditar_direto(k, recurso, q, total_primeiro=True)
        for recurso in range(3):
            q = struct.unpack_from('<H', self.mercado.recursos_pedidos, j * 6 + recurso * 2)[0]
            if self.mercado.tipo_jogador(k) == 1:
                self.mundo.retirar(k, recurso, q)
            self._creditar_direto(j, recurso, q, total_primeiro=False)
