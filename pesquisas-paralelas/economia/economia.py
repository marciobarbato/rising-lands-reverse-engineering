"""Tradução das primitivas econômicas do RISING.EXE brasileiro identificado.

Fatos de instruções: consultas 0x467640..0x467718; mutações
0x4678f2..0x4679d0. Não implementa produção, transporte ou filas.
As validações de índices são proteção desta API, ausente no x86 original.
"""
from enum import IntEnum
import struct
from typing import NamedTuple

BASE_RECURSOS = 0x4e2ea8
TAMANHO_TABELA = 128
PASSO_JOGADOR = 32
PASSO_RECURSO = 8


class Recurso(IntEnum):
    PECAS = 0
    COMIDA = 1
    PEDRA = 2
    SLOT_3 = 3  # O quarto registro existe; sem nome econômico confirmado.


class Saldos(NamedTuple):
    """Ordem das saídas de GetRessource e dos índices das operações da IA."""
    comida: int
    pedra: int
    pecas: int
    quarto: int = 0


def _jogador(jogador):
    jogador &= 0xff
    if jogador >= 4:
        raise ValueError('Jogador truncado deve estar em 0..3')
    return jogador


def _offset(jogador, recurso, *, mutacao=False):
    # Mutações recebem recurso em AL e jogador em BX; consultas usam jogador u8.
    jogador &= 0xffff if mutacao else 0xff
    recurso &= 0xff if mutacao else 0xffff
    if jogador >= 4:
        raise ValueError('Jogador truncado deve estar em 0..3')
    if recurso >= 4:
        raise ValueError('Recurso truncado deve estar em 0..3')
    return jogador * PASSO_JOGADOR + recurso * PASSO_RECURSO


def _i32(valor):
    valor &= 0xffffffff
    return valor - 0x100000000 if valor & 0x80000000 else valor


def _buffer_vivo(buffer, tamanho, nome):
    """Return ``buffer`` itself if it is a writable contiguous byte buffer of ``tamanho`` bytes."""
    if isinstance(buffer, memoryview):
        if buffer.readonly or buffer.ndim != 1 or buffer.format not in ('B', 'b') or not buffer.c_contiguous:
            raise ValueError(f'{nome} view must be writable, one-dimensional and contiguous bytes')
    elif not isinstance(buffer, bytearray):
        raise ValueError(f'{nome} must be a writable bytearray or memoryview (live memory, not a copy)')
    if len(buffer) != tamanho:
        raise ValueError(f'{nome} must have {tamanho} bytes')
    return buffer


class Economia:
    """Cópia mutável dos 128 bytes salvos por SauveRessource (0x46ab33).

    Registro: +0 saldo RMI, +2 total, +4 valor exibido, +6 flags de
    animação, +7 byte preservado. RMI é o nome original da consulta;
    seu significado no jogo ainda requer validação em partida.
    """

    @classmethod
    def vivo(cls, memoria):
        """Bind the live resource table 0x4e2ea8 (128 bytes) by identity: no copy."""
        memoria = _buffer_vivo(memoria, TAMANHO_TABELA, 'Live resource table (0x4e2ea8)')
        self = cls.__new__(cls)
        self.memoria = memoria
        return self

    @classmethod
    def da_memoria(cls, m):
        """``vivo`` over a live memory map: ``m.vista(0x4e2ea8, 128)``."""
        return cls.vivo(m.vista(BASE_RECURSOS, TAMANHO_TABELA))

    def __init__(self, memoria=None):
        # Legacy/fixture form: copies. Use Economia.vivo/da_memoria for the live original table.
        self.memoria = bytearray(TAMANHO_TABELA if memoria is None else memoria)
        if len(self.memoria) != TAMANHO_TABELA:
            raise ValueError('Tabela econômica deve ter 128 bytes')

    def registro(self, jogador, recurso):
        """Retorna os oito bytes do registro, incluindo o byte sem semântica."""
        o = _offset(jogador, recurso)
        return bytes(self.memoria[o:o + PASSO_RECURSO])

    @classmethod
    def de_recursos_eta(cls, recursos_por_tipo, memoria=None):
        """Adapta a saída de formatos.ler_eta; usa SetMatiere 12 vezes.

        O ETA fornece quatro jogadores para cada tipo, na ordem 1, 2, 0.
        Não lê arquivos, não limpa o quarto registro nem o byte +7.
        """
        e = cls(memoria)
        for recurso in (Recurso.COMIDA, Recurso.PEDRA, Recurso.PECAS):
            valores = recursos_por_tipo[str(int(recurso))]
            if len(valores) != 4:
                raise ValueError('Cada recurso ETA deve ter quatro jogadores')
            for jogador, valor in enumerate(valores):
                e.atribuir(jogador, recurso, valor)
        return e

    def atribuir(self, jogador, recurso, valor):
        """SetMatiere 0x46799c: define RMI/total, zera mostrador e flags.

        Não aplica o teto de 9.999 e preserva o byte +7.
        """
        struct.pack_into('<HHHB', self.memoria, _offset(jogador, recurso, mutacao=True),
                         valor & 0xffff, valor & 0xffff, 0, 0)

    def creditar(self, jogador, recurso, quantidade):
        """AjouteMatiere 0x4678f2: total = min((total + DX) & 65535, 9999)."""
        o = _offset(jogador, recurso, mutacao=True) + 2
        total = struct.unpack_from('<H', self.memoria, o)[0]
        struct.pack_into('<H', self.memoria, o, min((total + quantidade) & 0xffff, 9999))

    def debitar(self, jogador, recurso, quantidade):
        """EnleveMatiere 0x46792c: subtrai DX, com piso zero em cada saldo.

        Não testa disponibilidade nem informa sucesso; a autorização de uma
        compra deve ser conferida antes pelo chamador, como no recrutamento.
        """
        o = _offset(jogador, recurso, mutacao=True)
        rmi, total = struct.unpack_from('<HH', self.memoria, o)
        quantidade &= 0xffff
        struct.pack_into('<HH', self.memoria, o,
                         max(rmi - quantidade, 0), max(total - quantidade, 0))

    def consultar(self, jogador):
        """GetRessource 0x467670: três totais u16 e quarta saída zero."""
        j = _jogador(jogador)
        return Saldos(*(struct.unpack_from('<H', self.memoria, _offset(j, r) + 2)[0]
                        for r in (Recurso.COMIDA, Recurso.PEDRA, Recurso.PECAS)))

    def consultar_rmi(self, jogador):
        """GetRessourceRMI 0x467640: RMI comida/pedra; peças e quarto = 0."""
        j = _jogador(jogador)
        return Saldos(*(struct.unpack_from('<H', self.memoria, _offset(j, r))[0]
                        for r in (Recurso.COMIDA, Recurso.PEDRA)), 0)

    def consultar_estoque(self, jogador):
        """GetRessourceStock 0x46769d: diferenças u16, inclusive underflow."""
        j = _jogador(jogador)
        return Saldos(*((total - rmi) & 0xffff
                        for rmi, total in (struct.unpack_from('<HH', self.memoria, _offset(j, r))
                                           for r in (Recurso.COMIDA, Recurso.PEDRA, Recurso.PECAS))))

    def suficiente(self, jogador, comida, pedra, pecas):
        """TestRessource 0x4676e5: comparações unsigned, aceita igualdade."""
        return all((custo & 0xffff) <= saldo
                   for custo, saldo in zip((comida, pedra, pecas), self.consultar(jogador)))

    def testar_ia(self, jogador, indice, limiar, *, estoque=False):
        """B_TestRessource/B_TestStock: 1 ou -1; limiar é signed int32.

        Índice 0=comida, 1=pedra, 2=peças, 3=zero: difere dos IDs Recurso.
        """
        if not 0 <= indice < 4:
            raise ValueError('Índice de consulta da IA deve estar em 0..3')
        saldos = self.consultar_estoque(jogador) if estoque else self.consultar(jogador)
        return 1 if saldos[indice] >= _i32(limiar) else -1

    def riqueza_ia(self, jogador):
        """iagRessGetPlayerWealth 0x485fb9: soma das três diferenças u16."""
        return sum(self.consultar_estoque(jogador))

    def recurso_necessario(self, jogador, custos):
        """Núcleo comum 0x45d78f de Troupe/BatimentRessourceNecessaire.

        Retorna ID 1 por falta de comida, 2 por falta de pedra ou 0.
        O original não verifica peças neste helper; 0 também é o ID de peças.
        """
        saldos = self.consultar(jogador)
        if (custos[0] & 0xffff) > saldos.comida:
            return 1
        if (custos[1] & 0xffff) > saldos.pedra:
            return 2
        return 0


def custos_unidade(registro):
    """EnginGetRessource 0x4410d2; recebe um registro de tipo de 50 bytes."""
    if len(registro) != 50:
        raise ValueError('Tipo de unidade deve ter 50 bytes')
    comida, pecas, pedra = struct.unpack_from('<3H', registro, 2)
    return Saldos(comida, pedra, pecas)


def custos_construcao(tabela_desde_495d98, tipo):
    """BatimentGetRessource 0x41aace, custos a cada 52 bytes.

    A origem da vista deve ser 0x495d98, o primeiro custo lido pelo acessor;
    não se presume que esse endereço seja o início da estrutura de tipo.
    """
    o = (tipo & 0xff) * 52
    if o + 6 > len(tabela_desde_495d98):
        raise ValueError('Tipo de construção fora da tabela fornecida')
    return Saldos(*struct.unpack_from('<3H', tabela_desde_495d98, o))


def custo_ia(custos, indice):
    """I_CombienCoute*: índice 0 comida, 1 pedra, 2 peças (não IDs Recurso)."""
    if not 0 <= indice < 3:
        raise ValueError('Índice de custo da IA deve estar em 0..2')
    return custos[indice] & 0xffff
