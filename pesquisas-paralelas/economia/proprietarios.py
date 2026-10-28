"""Efeitos de InitBatimentPlayer e InitBatimentNeutre, sem mudar dono/estado.

Chegada/saída de balão que exige criação ou movimento é dependência explícita.
Os ramos econômicos, listas de ordens e resets locais são traduções diretas.
"""
import ctypes
import struct

from construcoes import EconomiaConstrucoes, PASSO_CONSTRUCAO

PASSO_BAG = 104
PASSO_PENDENCIAS_JOGADOR = 22 * PASSO_BAG
# One owner's unit-order pool: 26 unit-type Bags of 104 bytes (2,704 bytes).
PASSO_ORDENS_JOGADOR = 26 * PASSO_BAG
# Pointer table of the four per-owner unit-order pools. The original fills it
# with four separate page-aligned GlobalAlloc allocations (MONDE01:
# 0x41781000, 0x41782000, 0x41783000, 0x41784000), so the pools are NOT one
# contiguous array: [[0x4e19b8]+4*owner] + 104*type is owner/type's Bag.
BASE_TABELA_ORDENS = 0x4e19b8
BASE_PENDENCIAS = 0x4dd6e8
BASE_BIBLIOTECAS = 0x4dfb48
BASE_BALOES = 0x4e1a14
BASE_NUMEROS_UNIDADES = 0x4e1a3c
BASE_SORTILEGIOS = 0x508f30
BASE_JOGADOR_DEPOSITO = 0x4dfab8


class DependenciaBalaoPendente(RuntimeError):
    def __init__(self, endereco, jogador):
        self.endereco, self.jogador = endereco, jogador
        super().__init__(f'Dependência de balão 0x{endereco:08x}, jogador {jogador}')


def _word(memoria, offset):
    return struct.unpack_from('<H', memoria, offset)[0]


def _escrever_word(memoria, offset, valor):
    struct.pack_into('<H', memoria, offset, valor & 65535)


def inicializar_bag(memoria, offset, capacidade):
    """BagInit 0x447148: limpa cabeçalho/30 valores/30 tags; preserva +0x60..65."""
    if offset < 0 or offset + PASSO_BAG > len(memoria):
        raise ValueError('Bag fora do buffer')
    memoria[offset:offset + 0x60] = bytes(0x60)
    _escrever_word(memoria, offset + 0x66, 0)
    _escrever_word(memoria, offset + 2, capacidade)


def bag_contem_modo6(memoria, offset, valor):
    """Ramo DL=6 de BagContient: busca tag 6 e ID, retorna 0/1."""
    capacidade = _word(memoria, offset + 2)
    if capacidade > 30:
        raise ValueError('Capacidade de BagContient fora dos 30 slots protegidos')
    return any(memoria[offset + 0x42 + i] == 6 and _word(memoria, offset + 6 + i * 2) == (valor & 65535)
               for i in range(capacidade))


def _endereco_gravavel(bolsa):
    """Address of a writable, contiguous unsigned-byte buffer (no copy)."""
    if isinstance(bolsa, memoryview):
        if bolsa.readonly or bolsa.ndim != 1 or bolsa.format not in ('B', 'b') or not bolsa.c_contiguous:
            raise ValueError('Unit-order pool views must be writable, one-dimensional and contiguous bytes')
    elif not isinstance(bolsa, bytearray):
        raise ValueError('Unit-order pools must be writable bytearray or memoryview buffers')
    if len(bolsa) != PASSO_ORDENS_JOGADOR:
        raise ValueError(f'Each unit-order pool must have {PASSO_ORDENS_JOGADOR} bytes')
    janela = (ctypes.c_char * PASSO_ORDENS_JOGADOR).from_buffer(bolsa)
    try:
        return ctypes.addressof(janela)
    finally:
        del janela  # release the buffer export at once


def validar_ordens(ordens):
    """Validate the four live per-owner unit-order pools of [0x4e19b8].

    ``ordens`` is a list or tuple of exactly four distinct, writable,
    non-overlapping 2,704-byte buffers (owner 0..3). Returns a tuple holding the
    SAME four buffer objects; nothing is copied. Raises ValueError otherwise.
    A single contiguous buffer is rejected: use ``ordens_contiguas`` for it.
    """
    if not isinstance(ordens, (list, tuple)) or len(ordens) != 4:
        raise ValueError('Unit-order Bags must be a sequence of four per-owner pools ([0x4e19b8])')
    bolsas = tuple(ordens)
    if len({id(b) for b in bolsas}) != 4:
        raise ValueError('The four per-owner unit-order pools must be distinct objects')
    faixas = sorted(_endereco_gravavel(b) for b in bolsas)
    if any(b - a < PASSO_ORDENS_JOGADOR for a, b in zip(faixas, faixas[1:])):
        raise ValueError('The four per-owner unit-order pools must not overlap')
    return bolsas


def ordens_contiguas(memoria):
    """Legacy/fixture form: four owner views over ONE 10,816-byte buffer.

    The native benches lay the pools out contiguously (owner stride 2,704);
    this returns the four non-overlapping writable views of that buffer, so
    writes through ``PropriedadeConstrucoes.ordens`` land in ``memoria``.
    It is not the original layout (see BASE_TABELA_ORDENS).
    """
    if not isinstance(memoria, (bytearray, memoryview)) or len(memoria) != 4 * PASSO_ORDENS_JOGADOR:
        raise ValueError('Contiguous unit-order fixture must be a writable 10,816-byte buffer')
    vista = memoryview(memoria)
    if vista.readonly:
        raise ValueError('Contiguous unit-order fixture must be writable')
    return tuple(vista[j * PASSO_ORDENS_JOGADOR:(j + 1) * PASSO_ORDENS_JOGADOR] for j in range(4))


def juntar_ordens(ordens):
    """Bytes of the four per-owner pools in owner order (contiguous bench layout)."""
    return b''.join(bytes(b) for b in validar_ordens(ordens))


class PropriedadeConstrucoes:
    def __init__(self, mundo=None, *, bibliotecas=None, baloes=None, numeros_unidades=None,
                 pendencias=None, ordens=None, sortilegios=None, jogador_deposito=0):
        """``ordens``: the four live per-owner unit-order pools of [0x4e19b8], used by
        identity (e.g. core's ``MundoUnidades.bolsas_tipos_unidades``); owner j's
        unit-type t Bag is ``self.ordens[j]`` at ``t*104``. None allocates four
        fresh zero pools. Validation precedes every other effect.
        """
        ordens = validar_ordens([bytearray(PASSO_ORDENS_JOGADOR) for _ in range(4)]
                                if ordens is None else ordens)
        self.mundo = EconomiaConstrucoes() if mundo is None else mundo
        self.bibliotecas = bytearray(4 if bibliotecas is None else bibliotecas)
        self.baloes = bytearray(32 if baloes is None else baloes)
        self.numeros_unidades = bytearray(208 if numeros_unidades is None else numeros_unidades)
        self.pendencias = bytearray(4 * PASSO_PENDENCIAS_JOGADOR if pendencias is None else pendencias)
        self.ordens = ordens
        self.sortilegios = bytearray(20 if sortilegios is None else sortilegios)
        esperados = ((self.bibliotecas, 4), (self.baloes, 32), (self.numeros_unidades, 208),
                     (self.pendencias, 9152), (self.sortilegios, 20))
        if any(len(memoria) != tamanho for memoria, tamanho in esperados):
            raise ValueError('Comprimento de buffer de propriedade incompatível')
        self.jogador_deposito = jogador_deposito & 255
        if self.jogador_deposito >= 4:
            raise ValueError('Jogador do depósito deve estar em 0..3')

    def _entrada(self, indice, jogador):
        indice, jogador = indice & 65535, jogador & 255
        offset = indice * PASSO_CONSTRUCAO
        if jogador >= 4 or offset + PASSO_CONSTRUCAO > len(self.mundo.estruturas):
            raise ValueError('Jogador ou construção fora do domínio protegido')
        return indice, jogador, offset, self.mundo.estruturas[offset + 8]

    @staticmethod
    def _pendencia(jogador):
        return jogador * PASSO_PENDENCIAS_JOGADOR + 0x750

    def _chegada_balao(self, jogador, callback):
        offset = jogador * 8
        quantidade = _word(self.baloes, offset)
        if quantidade:
            _escrever_word(self.baloes, offset, quantidade + 1)
        elif callback is None:
            raise DependenciaBalaoPendente(0x441baa, jogador)
        else:
            callback(jogador)  # Deve executar a dependência inteira, com seus efeitos reais.

    def _saida_balao(self, jogador, callback):
        offset = jogador * 8
        quantidade = _word(self.baloes, offset)
        if quantidade == 1:
            if callback is None:
                raise DependenciaBalaoPendente(0x441d4f, jogador)
            callback(jogador)
        elif quantidade:
            _escrever_word(self.baloes, offset, quantidade - 1)

    def _dono_unidades(self, offset):
        dono = self.mundo.estruturas[offset + 4]
        if dono >= 4:
            raise ValueError('Dono usado na consulta de unidades fora de 0..3')
        return dono

    def inicializar_jogador(self, indice, jogador, *, preparar_chegada=None):
        """InitBatimentPlayer 0x41be88: AX=índice, DL=jogador; não atribui o dono."""
        _, jogador, offset, tipo = self._entrada(indice, jogador)
        if tipo == 3:
            o = jogador * 6
            quantidade = (_word(self.mundo.capacidades.memoria, o) + 1) & 65535
            _escrever_word(self.mundo.capacidades.memoria, o, quantidade)
            if quantidade:
                self.mundo.recalcular_recursos(jogador)
        elif tipo == 6:
            self.bibliotecas[jogador] = (self.bibliotecas[jogador] + 1) & 255
        elif tipo == 18:
            dono = self._dono_unidades(offset)
            self._chegada_balao(jogador, preparar_chegada)
            contagens = self.mundo.contagens_tipo18
            contagens[jogador] = (contagens[jogador] + 1) & 255
            if contagens[dono] > _word(self.numeros_unidades, dono * 52 + 16 * 2):
                bag = self._pendencia(jogador)
                if not bag_contem_modo6(self.pendencias, bag, 16):
                    inicializar_bag(self.pendencias, bag, 1)
                    _escrever_word(self.pendencias, bag + 0x66, 1)
                    self.pendencias[bag + 0x42] = 6
                    _escrever_word(self.pendencias, bag + 6, 16)
                    _escrever_word(self.pendencias, bag, 1)

    def _depositar_materia_neutralizada(self, indice, celula, modo):
        """TerrainDeposeMatiere 0x41bb8a, domínio usado pelo chamador: flag de pilha=0.

        O jogador vem de 0x4dfab8, não do argumento de InitBatimentNeutre.
        Modo 0 é comida; modo 1 é pedra, com uma divisão adicional do depósito.
        """
        jogador = self.jogador_deposito
        saldos = self.mundo.economia.consultar_estoque(jogador)
        recurso, quantidade = (1, saldos.comida) if modo == 0 else (2, saldos.pedra)
        if quantidade:
            armazens, _ = self.mundo.capacidades.parametros(jogador)
            if armazens:
                quantidade = (quantidade // armazens) >> 1
            self.mundo.economia.debitar(jogador, recurso, quantidade)
            if armazens:
                self.mundo.recalcular_recursos(jogador)
        pedido = quantidade if modo == 0 else quantidade >> 1
        self.mundo.terreno.depositar(celula, recurso, pedido)

    def inicializar_neutro(self, indice, jogador, *, preparar_saida=None):
        """InitBatimentNeutre 0x41c017: AX=índice, DL=jogador; não muda dono/estado."""
        indice, jogador, offset, tipo = self._entrada(indice, jogador)
        if tipo == 3:
            o = jogador * 6
            _escrever_word(self.mundo.capacidades.memoria, o, _word(self.mundo.capacidades.memoria, o) - 1)
            if self.mundo.estruturas[offset + 5] != 3:
                celula = (_word(self.mundo.estruturas, offset + 2) + 0x202) & 65535
                self._depositar_materia_neutralizada(indice, celula, 0)
                self._depositar_materia_neutralizada(indice, celula, 1)
        elif tipo == 6:
            self.bibliotecas[jogador] = (self.bibliotecas[jogador] - 1) & 255
            if self.bibliotecas[jogador] == 0:
                self.sortilegios[jogador * 5:jogador * 5 + 5] = bytes(5)
                inicializar_bag(self.ordens[jogador], 4 * PASSO_BAG, 5)
        elif tipo == 18:
            dono = self._dono_unidades(offset)
            self._saida_balao(jogador, preparar_saida)
            contagens = self.mundo.contagens_tipo18
            contagens[jogador] = (contagens[jogador] - 1) & 255
            if contagens[dono] <= _word(self.numeros_unidades, dono * 52 + 16 * 2):
                # BagInit esvazia a lista; o BagRetire DL=6 subsequente encontra zero itens.
                inicializar_bag(self.pendencias, self._pendencia(jogador), 1)
        elif tipo == 20:
            self.mundo.estruturas[offset + 0x7a] = 0
            self.mundo.estruturas[offset + 0x104] = 0
            struct.pack_into('<I', self.mundo.estruturas, offset + 0x108, 1)
