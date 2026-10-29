"""Crédito, débito, recálculo de capacidade e excedentes de construções.

Traduz o corpo econômico, BagAccepte, sacolas e sua procura de lugar.
BatimentRetireColon não é traduzido: exige callback explícito no ramo tipo 4
sem alojamento. Não se executa nem se simula criação/movimento de unidades.
"""
from dataclasses import dataclass
import struct

from economia import Economia, _buffer_vivo

BASE_CAPACIDADES = 0x4dfb2c
BASE_CONSTRUCOES = 0x49a0c8
PASSO_CONSTRUCAO = 276
BASE_CONTAGENS_TIPOS = 0x49a070
BASE_CONTAGENS_TIPO18 = 0x4dfb4c
TOTAL_CONSTRUCOES = 1000
TOTAL_TIPOS_CONSTRUCAO = 22


class RetiradaColonoPendente(RuntimeError):
    """Parada equivalente à entrada em BatimentRetireColon, não a um sucesso."""
    def __init__(self, indice):
        self.indice = indice
        super().__init__(f'BatimentRetireColon(0x41dde0) necessário para construção {indice}')


class LimiteDeposito(RuntimeError):
    """Limite funcional da tradução; o x86 também pode não terminar nesse estado."""


@dataclass(frozen=True)
class PedidoSacolas:
    celula: int
    recurso: int
    quantidade: int


@dataclass(frozen=True)
class ResultadoDeposito:
    """Diagnóstico novo da API; não representa registradores de retorno do x86.

    credito_enviado é DX entregue à primitiva, não a variação efetiva do saldo.
    descartado indica excedente sem chamada ao terreno, não falhas ao criar sacolas.
    """
    credito_enviado: int
    excedente: int
    pedido_sacolas: object = None
    descartado: bool = False


class Capacidades:
    """Quatro registros de seis bytes: armazéns u16, capacidade u16, nível u8, byte.

    A inicialização sintética padrão usa capacidade 100, como BatimentAlloc.
    A contagem real é reconstruída por EconomiaConstrucoes.inicializar_armazens.
    """
    def __init__(self, memoria=None):
        self.memoria = bytearray(24 if memoria is None else memoria)
        if len(self.memoria) != 24:
            raise ValueError('Capacidades devem ter 24 bytes')
        if memoria is None:
            for j in range(4):
                struct.pack_into('<H', self.memoria, j * 6 + 2, 100)

    @staticmethod
    def _offset(jogador):
        jogador &= 0xff
        if jogador >= 4:
            raise ValueError('Jogador deve estar em 0..3 depois de truncado')
        return jogador * 6

    def parametros(self, jogador):
        return struct.unpack_from('<HH', self.memoria, self._offset(jogador))

    def configurar(self, jogador, armazens, por_armazem):
        """Preparação de estado da API, não tradução de uma rotina de inicialização."""
        struct.pack_into('<HH', self.memoria, self._offset(jogador), armazens & 65535, por_armazem & 65535)

    def nivel(self, jogador):
        return self.memoria[self._offset(jogador) + 4]

    def escrever_nivel(self, jogador, valor):
        self.memoria[self._offset(jogador) + 4] = valor & 255


class TerrenoSacolas:
    """Grades de 256x256 de tipo e quantidade, sem mapa de movimento.

    Ponteiros originais: 0x507d74 (tipo), 0x507dac (quantidade).
    O estado aleatório corresponde a 0x497164; não altera o gerador 0x498db4.
    """
    @classmethod
    def vivo(cls, tipos, quantidades, semente=1):
        """Bind the live type [0x507d74] and quantity [0x507dac] grids (65,536 bytes each) by identity."""
        tipos = _buffer_vivo(tipos, 65536, 'Live type grid ([0x507d74])')
        quantidades = _buffer_vivo(quantidades, 65536, 'Live quantity grid ([0x507dac])')
        if tipos is quantidades:
            raise ValueError('The type and quantity grids are different allocations')
        if not 0 <= semente <= 0x7fffffff:
            raise ValueError('Semente deve estar em 0..0x7fffffff')
        self = cls.__new__(cls)
        self.tipos, self.quantidades, self.semente = tipos, quantidades, semente
        return self

    def __init__(self, tipos=None, quantidades=None, semente=1):
        # Legacy/fixture form: copies. Use TerrenoSacolas.vivo for the live grids.
        self.tipos = bytearray(65536 if tipos is None else tipos)
        self.quantidades = bytearray(65536 if quantidades is None else quantidades)
        if len(self.tipos) != 65536 or len(self.quantidades) != 65536:
            raise ValueError('Cada grade de sacolas deve ter 65536 bytes')
        if not 0 <= semente <= 0x7fffffff:
            raise ValueError('Semente deve estar em 0..0x7fffffff')
        self.semente = semente

    def _aleatorio(self):
        # 0x4704dc, Park–Miller/Schrage; EAX de entrada é ignorado pelo original.
        quociente, resto = divmod(self.semente, 127773)
        novo = resto * 16807 - quociente * 2836
        if novo <= 0:
            novo += 0x7fffffff
        self.semente = novo
        return novo

    def aceita(self, celula, tipo_sacola):
        """TerrainAccepteSac 0x475763: tipo codificado, não ID do recurso.

        A recusa de quantidade é por igualdade a 31, não por >=31.
        """
        celula &= 65535
        tipo_sacola &= 255
        atual = self.tipos[celula]
        return atual in (0, tipo_sacola) and (atual != tipo_sacola or self.quantidades[celula] != 31)

    def procurar(self, celula, tipo_sacola):
        """SacCherchePlace 0x4757af: cinco anéis, sem teste de caminho.

        Sorteia um ordinal com resto 8*r; a contagem começa em 1. Resto zero,
        ou ordinal maior que a quantidade de candidatos, faz avançar o anel.
        """
        celula &= 65535
        tipo_sacola &= 255
        if self.aceita(celula, tipo_sacola):
            return celula
        x, y = celula & 255, celula >> 8
        for raio in range(1, 6):
            ordinal = self._aleatorio() % (8 * raio)
            encontrados = 0
            for d in range(-raio, raio + 1):
                candidatos = [(x - raio, y + d), (x + raio, y + d)]
                if d not in (-raio, raio):
                    candidatos += [(x + d, y - raio), (x + d, y + raio)]
                for cx, cy in candidatos:
                    if not (0 <= cx < 256 and 0 <= cy < 256):
                        continue
                    candidato = (cy * 256 + cx) & 65535
                    if self.aceita(candidato, tipo_sacola):
                        encontrados += 1
                        if encontrados == ordinal:
                            return candidato
        return 65535

    def criar(self, celula, recurso, *, limite=10000):
        """CreerSac 0x47605d; pode recusar silenciosamente tipos incompatíveis.

        Uma pilha normal comporta 31 sacolas. Ao exceder, desfaz o incremento,
        procura outra célula e tenta novamente. Não testa colisão do terreno.
        """
        celula &= 65535
        tipo_sacola = (recurso + 0x42) & 255
        for _ in range(limite):
            atual = self.tipos[celula]
            if atual not in (0, tipo_sacola):
                return
            if atual == 0:
                self.quantidades[celula] = 1
                self.tipos[celula] = tipo_sacola
                return
            nova = (self.quantidades[celula] + 1) & 255
            self.quantidades[celula] = nova
            if nova <= 31:
                return
            self.quantidades[celula] = (nova - 1) & 255
            celula = self.procurar(celula, tipo_sacola)
        raise LimiteDeposito('CreerSac não terminou no limite funcional de tentativas')

    def depositar(self, celula, recurso, quantidade):
        """TerrainDeposeSac 0x4761a9: chama CreerSac quantidade u16 vezes."""
        for _ in range(quantidade & 65535):
            self.criar(celula, recurso)


def bag_aceita_colono(registro):
    """Ramo DL=1 de BagAccepte 0x4470d2: ocupação + 1 <= limite."""
    if len(registro) != PASSO_CONSTRUCAO:
        raise ValueError('Registro de construção deve ter 276 bytes')
    limite = struct.unpack_from('<H', registro, 0x0e)[0]
    ocupacao = struct.unpack_from('<H', registro, 0x72)[0]
    return ocupacao + 1 <= limite


class EconomiaConstrucoes:
    def __init__(self, economia=None, capacidades=None, estruturas=None, terreno=None,
                 *, contagens_por_tipo=None, contagens_tipo18=None):
        self.economia = Economia() if economia is None else economia
        self.capacidades = Capacidades() if capacidades is None else capacidades
        self.estruturas = bytearray(PASSO_CONSTRUCAO if estruturas is None else estruturas)
        if not self.estruturas or len(self.estruturas) % PASSO_CONSTRUCAO or len(self.estruturas) > 1000 * PASSO_CONSTRUCAO:
            raise ValueError('Estruturas devem conter 1..1000 registros de 276 bytes')
        self.terreno = TerrenoSacolas() if terreno is None else terreno
        self.contagens_por_tipo = bytearray(88 if contagens_por_tipo is None else contagens_por_tipo)
        self.contagens_tipo18 = bytearray(4 if contagens_tipo18 is None else contagens_tipo18)
        if len(self.contagens_por_tipo) != 88 or len(self.contagens_tipo18) != 4:
            raise ValueError('Contagens devem ter 88 bytes por tipo e quatro bytes do tipo 18')

    def inicializar_armazens(self):
        """BatimentInitCave 0x419112: reconta os 1000 registros para jogadores 0..3.

        Conta qualquer estado +5 diferente de zero, agrupando dono +4 e tipo +8.
        As contagens são u8, inclusive armazéns e heliportos. O número de CAVE
        é depois copiado para o word das capacidades; capacidade unitária e
        indicador não são alterados. Não faz o recálculo do indicador.

        A API rejeita tipos ativos fora de 0..21 antes de escrever: o original
        pode incrementar memória vizinha por não verificar esse limite.
        """
        if len(self.estruturas) != TOTAL_CONSTRUCOES * PASSO_CONSTRUCAO:
            raise ValueError('BatimentInitCave exige exatamente 1000 registros de 276 bytes')
        for o in range(0, len(self.estruturas), PASSO_CONSTRUCAO):
            if self.estruturas[o + 5] and self.estruturas[o + 4] < 4 and self.estruturas[o + 8] >= TOTAL_TIPOS_CONSTRUCAO:
                raise ValueError('Construção ativa de jogador 0..3 tem tipo fora de 0..21')
        for jogador in range(4):
            base = jogador * TOTAL_TIPOS_CONSTRUCAO
            self.contagens_por_tipo[base:base + TOTAL_TIPOS_CONSTRUCAO] = bytes(TOTAL_TIPOS_CONSTRUCAO)
            for o in range(0, len(self.estruturas), PASSO_CONSTRUCAO):
                if self.estruturas[o + 5] and self.estruturas[o + 4] == jogador:
                    pos = base + self.estruturas[o + 8]
                    self.contagens_por_tipo[pos] = (self.contagens_por_tipo[pos] + 1) & 255
            self.contagens_tipo18[jogador] = self.contagens_por_tipo[base + 18]
            struct.pack_into('<H', self.capacidades.memoria, jogador * 6, self.contagens_por_tipo[base + 3])

    def recalcular_recursos(self, jogador):
        """BatimentCalculResource 0x423355: atualiza apenas o indicador u8.

        AL >= 4 ou ausência de armazéns são retornos sem alteração no original.
        A soma de estoque é u16 e há duas divisões inteiras sucessivas.
        Não limita estoque à capacidade nem satura o indicador em sete.
        """
        jogador &= 255
        if jogador >= 4:
            return
        armazens, por_armazem = self.capacidades.parametros(jogador)
        if armazens == 0:
            return
        saldos = self.economia.consultar_estoque(jogador)
        estoque = (saldos.comida + saldos.pedra) & 65535
        nivel = (estoque // armazens * 7) // por_armazem
        self.capacidades.escrever_nivel(jogador, nivel)

    def retirar(self, jogador, recurso, quantidade):
        """BatimentEnleveMatiere 0x4235bd: debita e depois recalcula o nível.

        AL=recurso, DX=quantidade, BL=jogador; não recebe índice de construção.
        O débito sempre ocorre, mesmo sem armazéns ou quando o recálculo falha.
        O compartilhamento do método Python não representa uma chamada entre
        as duas rotinas originais: seus corpos x86 repetem a mesma fórmula.
        """
        jogador &= 255
        recurso &= 255
        quantidade &= 65535
        self.economia.debitar(jogador, recurso, quantidade)
        self.recalcular_recursos(jogador)

    def adicionar(self, jogador, recurso, quantidade, indice, *, retirar_colono=None):
        """BatimentAjouteMatiere: AL=recurso, DX=quantidade, BL=jogador, CX=índice.

        O dono em estrutura+4 não substitui o jogador recebido pelo argumento.
        Capacidade usa estoque comida+pedra, inclusive ao creditar peças.
        """
        jogador &= 255
        recurso &= 255
        quantidade &= 65535
        indice &= 65535
        if jogador >= 4 or recurso >= 4:
            raise ValueError('Jogador/recurso fora da tabela econômica protegida')
        o = indice * PASSO_CONSTRUCAO
        if o + PASSO_CONSTRUCAO > len(self.estruturas):
            raise ValueError('Construção fora da tabela fornecida')
        tipo = self.estruturas[o + 8]
        credito, excesso = 0, 0
        if tipo != 4:
            armazens, por_armazem = self.capacidades.parametros(jogador)
            if armazens == 0:
                excesso = quantidade
            else:
                saldos = self.economia.consultar_estoque(jogador)
                estoque = (saldos.comida + saldos.pedra) & 65535
                capacidade = (armazens * por_armazem) & 65535
                credito = quantidade
                if estoque + quantidade > capacidade:
                    excesso = (quantidade + estoque - capacidade) & 65535
                    credito = (capacidade - estoque) & 65535
                self.economia.creditar(jogador, recurso, credito)
                # DIV word usa DX:AX, com DX=0: o numerador também é u16.
                # A falha de divisão por unidade zero ocorre DEPOIS do crédito.
                nivel = (((estoque + credito) & 65535) // armazens * 7) // por_armazem
                self.capacidades.escrever_nivel(jogador, nivel)
        elif bag_aceita_colono(self.estruturas[o:o + PASSO_CONSTRUCAO]):
            contador = struct.unpack_from('<H', self.estruturas, o + 0x78)[0]
            if contador < 5:
                struct.pack_into('<H', self.estruturas, o + 0x78, contador + 1)
        else:
            if retirar_colono is None:
                raise RetiradaColonoPendente(indice)
            retirar_colono(indice)
            posicao = struct.unpack_from('<H', self.estruturas, o + 2)[0]
            # ADD AH,2 difere de somar 0x202 nos outros ramos.
            celula = (posicao & 255) | ((((posicao >> 8) + 2) & 255) << 8)
            pedido = PedidoSacolas(celula, 1, 1)
            self.terreno.depositar(celula, 1, 1)
            return ResultadoDeposito(0, 0, pedido)
        if excesso:
            posicao = struct.unpack_from('<H', self.estruturas, o + 2)[0]
            if tipo == 3:
                celula = (posicao + (0x202 if recurso == 1 else 3)) & 65535
            elif tipo == 2:
                celula = (posicao + 0x303) & 65535
            else:
                return ResultadoDeposito(credito, excesso, descartado=True)
            pedido = PedidoSacolas(celula, recurso, excesso)
            self.terreno.depositar(celula, recurso, excesso)
            return ResultadoDeposito(credito, excesso, pedido)
        return ResultadoDeposito(credito, excesso)
