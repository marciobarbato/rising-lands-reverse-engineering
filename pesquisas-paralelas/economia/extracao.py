"""Extração de minas, coleta e regeneração de campos no terreno original.

Não credita jogadores nem movimenta unidades. Compartilha tipos, quantidades
e RNG com TerrenoSacolas. A grade de atributos é apenas consultada para o
bit 0 que impede o nascimento de plantas; não implementa colisão ou caminhos.
"""
import struct

from construcoes import TerrenoSacolas

BASE_MINAS = 0x509954
TOTAL_MINAS = 20


class RecursosTerreno:
    def __init__(self, terreno=None, *, minas=None, mosaicos=None, atributos=None,
                 linha=1, atualizar=0, periodo=1, tempo=0):
        self.terreno = TerrenoSacolas() if terreno is None else terreno
        self.minas = bytearray(80 if minas is None else minas)
        self.mosaicos = bytearray(131072 if mosaicos is None else mosaicos)
        self.atributos = bytearray(65536 if atributos is None else atributos)
        if len(self.minas) != 80 or len(self.mosaicos) != 131072 or len(self.atributos) != 65536:
            raise ValueError('Esperados 80 bytes de minas, 131072 de mosaicos e 65536 de atributos')
        # Padrões sintéticos da API; não equivalem a executar inicialização do jogo.
        self.linha = linha & 65535
        self.atualizar = atualizar & 255
        self.periodo = periodo & 65535
        self.tempo = tempo & 0xffffffff

    @staticmethod
    def _indice(indice):
        indice &= 65535
        if indice >= TOTAL_MINAS:
            raise ValueError('Índice da mina deve estar em 0..19 depois de truncado')
        return indice

    def indice_mina(self, celula):
        """MineGetIndice 0x47544c: primeira origem não nula que inclui a célula.

        São origem, +1, +256, +257, com somas em 32 bits. Não há teste de
        coordenadas por eixo, reserva ou mosaico; 0xffff significa ausente.
        """
        celula &= 65535
        for i in range(TOTAL_MINAS):
            origem = struct.unpack_from('<H', self.minas, i * 4)[0]
            if origem and celula in (origem, origem + 1, origem + 256, origem + 257):
                return i
        return 65535

    def capacidade_mina(self, indice):
        """MineGetCapacite 0x475541: reserva u16; não recebe uma célula."""
        return struct.unpack_from('<H', self.minas, self._indice(indice) * 4 + 2)[0]

    def _origem_par(self, indice):
        origem = struct.unpack_from('<H', self.minas, self._indice(indice) * 4)[0]
        if origem == 65535:
            # O x86 escreveria na célula seguinte, fora da grade. Guarda da API.
            raise ValueError('Par da mina ultrapassa a grade de 65536 células')
        return origem

    def _trabalho_mina(self, celula, delta):
        i = self.indice_mina(celula)
        if i != 65535:
            origem = self._origem_par(i)
            for c in (origem, origem + 1):
                self.terreno.quantidades[c] = (self.terreno.quantidades[c] + delta) & 255

    def iniciar_trabalho_mina(self, celula):
        """MineSetWork 0x4754a7: incrementa dois bytes, inclusive wrap 255→0."""
        self._trabalho_mina(celula, 1)

    def encerrar_trabalho_mina(self, celula):
        """MineEndWork 0x4754de: decrementa dois bytes, inclusive wrap 0→255."""
        self._trabalho_mina(celula, -1)

    def destruir_mina(self, indice):
        """MineDetruire 0x475515: só grava mosaicos 0x1db/0x1dc; mantém reserva."""
        origem = self._origem_par(indice)
        struct.pack_into('<HH', self.mosaicos, origem * 2, 0x1db, 0x1dc)

    def retirar_mina(self, indice, quantidade):
        """MineRetire 0x47554f: retorna min(DX, reserva), esgota em igualdade.

        Em estado fora do domínio (origem 0xffff com esgotamento), a API
        rejeita antes de escrever; o original gravaria além do fim da grade.
        """
        i = self._indice(indice)
        quantidade &= 65535
        reserva = self.capacidade_mina(i)
        if quantidade >= reserva:
            self._origem_par(i)
            struct.pack_into('<H', self.minas, i * 4 + 2, 0)
            self.destruir_mina(i)
            return reserva
        struct.pack_into('<H', self.minas, i * 4 + 2, reserva - quantidade)
        return quantidade

    def recolher_mina(self, celula):
        """MineRecolte 0x4755a7: tenta retirar uma unidade; ausente retorna zero."""
        indice = self.indice_mina(celula)
        return 0 if indice == 65535 else self.retirar_mina(indice, 1)

    def retirar_sacola(self, celula):
        """TerrainRetireMatiere 0x476662: retira uma unidade sem validar o tipo.

        Retorna (tipo-0x42)&255 se havia quantidade, senão zero. Zero também
        identifica peças; não usar esse retorno como booleano de sucesso.
        Limpa o tipo sempre que a quantidade final é zero.
        """
        celula &= 65535
        recurso = 0
        if self.terreno.quantidades[celula]:
            self.terreno.quantidades[celula] -= 1
            recurso = (self.terreno.tipos[celula] - 0x42) & 255
        if self.terreno.quantidades[celula] == 0:
            self.terreno.tipos[celula] = 0
        return recurso

    def e_campo(self, celula):
        """TerrainEstChampi 0x478247: intervalo inclusivo 0x1d..0x34."""
        return 0x1d <= self.terreno.tipos[celula & 65535] <= 0x34

    def pode_crescer(self, celula):
        """PatateAugmentable 0x47826c: exclui os estágios 0x28 e 0x34."""
        tipo = self.terreno.tipos[celula & 65535]
        return 0x1d <= tipo < 0x28 or 0x29 <= tipo < 0x34

    def recolher_campo(self, celula):
        """TerrainRecolte 0x4781e8: 0x33/34 retrocedem dez; demais campos somem.

        Não altera quantidades ou carteiras e não retorna a quantidade colhida.
        """
        celula &= 65535
        if self.e_campo(celula):
            tipo = self.terreno.tipos[celula]
            self.terreno.tipos[celula] = tipo - 10 if tipo >= 0x33 else 0

    def nova_planta(self, celula):
        """NouvellePatate 0x4782b4: célula vazia, bit 0 livre, um sorteio.

        Não verifica o mosaico. Paridade do Random escolhe 0x1d ou 0x29.
        Quantidades preexistentes são preservadas.
        """
        celula &= 65535
        if self.terreno.tipos[celula] or self.atributos[celula] & 1:
            return False
        self.terreno.tipos[celula] = 0x29 if self.terreno._aleatorio() & 1 else 0x1d
        return True

    def propagar_planta(self, celula):
        """ScanNouvellePatate 0x478319: tenta esquerda/direita/cima/baixo.

        Índices lineares são truncados em u16, inclusive nas bordas. Planta no
        primeiro vizinho vazio sobre mosaico 0x84..86 ou 0x9d..dc e bit 0 livre.
        O AL residual varia entre saídas; esta API não inventa retorno booleano.
        """
        celula &= 65535
        for delta in (-1, 1, -256, 256):
            vizinho = (celula + delta) & 65535
            mosaico = struct.unpack_from('<H', self.mosaicos, vizinho * 2)[0]
            if (0x84 <= mosaico < 0x87 or 0x9d <= mosaico < 0xdd) and self.nova_planta(vizinho):
                return

    def agendar_campos(self):
        """SetUpdateChamp 0x475328: tempo u32 múltiplo de período u16 ativa flag.

        Não limpa flag nos demais ticks. Período zero causa divisão por zero.
        """
        if (self.tempo & 0xffffffff) % (self.periodo & 65535) == 0:
            self.atualizar = 1

    def atualizar_campos(self):
        """UpdateChamp 0x478806: processa uma linha, colunas 1..254, in-place.

        A flag inicia uma passagem; linha>1 a mantém em andamento. Ao terminar
        linha 255, restaura linha=1 e flag=0. Usa o RNG compartilhado de sacolas.
        Linha fora de 0..255 é rejeitada pela API, pois o original pode ler
        além da grade antes de truncar outros acessos.
        """
        linha = self.linha & 65535
        if not self.atualizar & 255 and linha <= 1:
            return
        if linha > 255:
            raise ValueError('Linha ativa deve estar em 0..255')
        for x in range(1, 255):
            celula = linha * 256 + x
            if self.terreno.tipos[celula] == 0x1c and self.terreno._aleatorio() % 5 == 0:
                self.propagar_planta(celula)
            if not self.e_campo(celula) or self.terreno._aleatorio() % 10:
                continue
            tipo = self.terreno.tipos[celula]
            if not self.pode_crescer(celula):
                self.terreno.tipos[celula] = 0
                self.propagar_planta(celula)
            elif 0x24 <= tipo <= 0x27 or 0x30 <= tipo <= 0x33:
                if self.terreno._aleatorio() % 5 == 0:
                    self.terreno.tipos[celula] += 1
                else:
                    self.propagar_planta(celula)
            else:
                self.terreno.tipos[celula] += 1
        self.linha = linha + 1
        if self.linha > 255:
            self.linha = 1
            self.atualizar = 0
