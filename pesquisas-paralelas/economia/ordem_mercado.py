"""Resource-only MarcheOrdreEchange and its two original transfer callers.

Nonzero unit rows stop at the original unit-loop checkpoints. No world unit
transfer/allocation is fabricated. Unlike VideMatiere, zero resources are
skipped and each transferred row entry is cleared between total/RMI writes.
"""
import struct

from economia import _jogador

BASE_ACEITES = 0x4e2968


class TrocaUnidadesMercadoPendente(RuntimeError):
    """Earlier caller/resource mutations remain applied at this unit checkpoint."""
    def __init__(self, fase, jogador, proponente, tipo_unidade, quantidade):
        self.fase = fase
        self.jogador = jogador
        self.proponente = proponente
        self.tipo_unidade = tipo_unidade
        self.quantidade = quantidade
        self.endereco = 0x46166b if fase == 'prend' else 0x4618df
        super().__init__(f'Unit market exchange pending at 0x{self.endereco:08x}')


class OrdemMercado:
    def __init__(self, mercado, mundo, *, aceites=None):
        if mercado.economia is not mundo.economia:
            raise ValueError('Market callers and buildings must share the same Economy')
        self.mercado, self.mundo = mercado, mundo
        self.aceites = bytearray(4 if aceites is None else aceites)
        if len(self.aceites) != 4:
            raise ValueError('Market approval buffer must contain four bytes')

    def _unidades(self, fase, jogador, proponente, bloco):
        for tipo in range(26):
            quantidade = struct.unpack_from('<H', bloco, proponente * 52 + tipo * 2)[0]
            if quantidade:
                raise TrocaUnidadesMercadoPendente(fase, jogador, proponente, tipo, quantidade)

    def _recursos(self, origem, destino, proponente, bloco):
        for recurso in range(3):
            pos = proponente * 6 + recurso * 2
            quantidade = struct.unpack_from('<H', bloco, pos)[0]
            if not quantidade:
                continue
            if self.mercado.tipo_jogador(origem) == 1:
                self.mundo.retirar(origem, recurso, quantidade)
            # Original callers: write destination total, consume proposal, write
            # destination RMI. No capacity check or clamp on these direct credits.
            offset = destino * 32 + recurso * 8
            rmi, total = struct.unpack_from('<HH', self.mundo.economia.memoria, offset)
            struct.pack_into('<H', self.mundo.economia.memoria, offset + 2, (total + quantidade) & 65535)
            struct.pack_into('<H', bloco, pos, 0)
            struct.pack_into('<H', self.mundo.economia.memoria, offset, (rmi + quantidade) & 65535)

    def receber(self, jogador, proponente):
        """MarcheEchangePrend 0x461621: AL=recipient, DL=proposal-row owner.

        Check offered units first, then transfer nonzero offered resources from
        proponente to jogador and clear each successful entry in that row.
        """
        j, p = _jogador(jogador), _jogador(proponente)
        self._unidades('prend', j, p, self.mercado.unidades_oferecidas)
        self._recursos(p, j, p, self.mercado.recursos_oferecidos)

    def entregar(self, jogador, proponente):
        """MarcheEchangeDonne 0x46189a: AL=donor, DL=proposal-row owner.

        Check requested units first, then transfer nonzero requested resources
        from jogador to proponente and clear each successful row entry.
        """
        j, p = _jogador(jogador), _jogador(proponente)
        self._unidades('donne', j, p, self.mercado.unidades_pedidas)
        self._recursos(j, p, p, self.mercado.recursos_pedidos)

    def ordenar(self, jogador, proponente):
        """MarcheOrdreEchange 0x461bea, low AL/DL, protected players 0..3.

        Toggle jogador's byte: zero -> 1, any nonzero -> 0. If proponente's
        current approval is nonzero OR jogador has type 2, execute Prend then
        Donne, then clear both approvals. Do not test the new jogador approval,
        indicator, contacts, prices, alliance or sufficiency. Aliasing players
        therefore observes the freshly toggled byte. Failure preserves earlier
        toggles/transfers/row clearing and does not clear both approvals.

        Returns a new Python diagnostic bool (executed), not an original AL
        success flag. Nonzero unit rows raise an explicit pending checkpoint.
        """
        j, p = _jogador(jogador), _jogador(proponente)
        self.aceites[j] = int(self.aceites[j] == 0)
        if self.aceites[p] == 0 and self.mercado.tipo_jogador(j) != 2:
            return False
        self.receber(j, p)
        self.entregar(j, p)
        self.aceites[j] = 0
        self.aceites[p] = 0
        return True
