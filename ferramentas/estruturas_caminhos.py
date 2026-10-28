"""Cores auxiliares e observação de estruturas durante CheminCalcul.

As cores representam componentes de obstáculos, não a paleta de desenho.
A ocupação física e a inserção/remoção de edifícios são etapas distintas.
"""
import struct
from caminhos import aliados


def modificar_regiao_estrutura(mundo, indice, subcelula, celula, inserir):
    """Modos 1/3 de Chemin_ModifieZone, 0x43e138.

    Guarda/restaura a região sob a estrutura e atualiza cores. A máscara
    física de terreno é responsabilidade do chamador, como no original.
    """
    if not 0 <= indice < 1000 or not 0 <= subcelula < 32:
        raise ValueError('Estrutura/subcélula fora da codificação da grade')
    celula &= 65535
    tag = 0x8000 | indice << 5 | subcelula
    offset = indice * 276 + 0xcc + subcelula * 2
    if inserir:
        if mundo.regioes[celula] >= 0x4000:
            return False
        struct.pack_into('<H',mundo.estruturas,offset,mundo.regioes[celula])
        mundo.regioes[celula] = tag
        mundo.cores_estruturas.adicionar_muro(celula)
    else:
        if mundo.regioes[celula] != tag:
            return False
        mundo.regioes[celula] = struct.unpack_from('<H',mundo.estruturas,offset)[0]
        mundo.cores_estruturas.retirar_muro(celula)
    return True


class CoresEstruturas:
    def __init__(self, largura, altura):
        self.largura, self.altura = largura, altura
        self.grade = bytearray(65536)
        # Inicialização em Chemin_Remap, 0x42ee52..0x42eea5.
        self.livres = bytearray([255] + list(range(1, 256)))
        self.liberadas = bytearray([1] * 256)
        self.pilha = [0] * 1024

    def alocar(self):
        """AlloueCouleur, 0x43e5a0: devolve zero ao esgotar a pilha."""
        n = self.livres[0]
        if not n:
            return 0
        cor = self.livres[n]
        self.livres[0] -= 1
        self.liberadas[cor] = 0
        return cor

    def liberar(self, cor):
        """LibereCouleur, 0x43e5d5: ignora zero e liberação repetida."""
        cor &= 255
        if self.livres[0] == 255 or self.liberadas[cor] or not cor:
            return
        self.livres[0] += 1
        self.livres[self.livres[0]] = cor
        self.liberadas[cor] = 1

    def _vizinhos(self, celula):
        # As rotinas de cores testam os limites de cada vizinho. Não exigem
        # que a célula recebida já esteja dentro do retângulo jogável.
        x, y = celula & 255, celula >> 8
        return tuple(cx + cy * 256 if 0 <= cx < self.largura and 0 <= cy < self.altura else 0xffff
                     for cx, cy in ((x-1,y),(x,y-1),(x+1,y),(x,y+1)))

    def adicionar_muro(self, celula):
        """MurAjoute, 0x43e616: reúne componentes vizinhos com uma nova cor."""
        celula &= 65535
        vizinhos = self._vizinhos(celula)
        anteriores = [self.grade[c] if c != 0xffff else 0 for c in vizinhos]
        nova = self.alocar()
        for c, antiga in zip(vizinhos, anteriores):
            if c != 0xffff and self.grade[c] and self.grade[c] == antiga:
                self.preencher(c, nova)
        self.grade[celula] = nova
        for antiga in anteriores:
            self.liberar(antiga)

    def retirar_muro(self, celula):
        """MurRetire, 0x43e8b7: separa componentes depois de remover a célula."""
        celula &= 65535
        if not self.grade[celula]:
            return
        vizinhos = self._vizinhos(celula)
        anteriores = [self.grade[c] if c != 0xffff else 0 for c in vizinhos]
        self.grade[celula] = 0
        for c, antiga in zip(vizinhos, anteriores):
            if c != 0xffff and self.grade[c] and self.grade[c] == antiga:
                self.preencher(c, self.alocar())
        for antiga in anteriores:
            self.liberar(antiga)

    def preencher(self, inicio, cor):
        """Remplit, 0x43e464: quatro vizinhos e pilha limitada a 1.023 itens.

        Conserva a cauda da pilha e o término antecipado ao enchê-la. Trocar
        uma cor por ela mesma é recusado: o x86 pode não terminar nesse caso.
        """
        inicio, cor = inicio & 65535, cor & 255
        if not cor:
            return
        antiga = self.grade[inicio]
        if antiga == cor:
            raise ValueError('Remplit requer uma cor diferente da cor de origem')
        topo = 1
        self.pilha[1] = inicio
        while topo:
            celula = self.pilha[topo]
            topo -= 1
            if self.grade[celula] == antiga:
                self.grade[celula] = cor
            for vizinha in self._vizinhos(celula):
                if vizinha != 0xffff and self.grade[vizinha] == antiga and topo < 1023:
                    topo += 1
                    self.pilha[topo] = vizinha
            if topo == 1023:
                return


def observar_estrutura(contexto, valor, celula, registro, fase):
    """Normaliza para 0x8000|cor e registra estruturas do tipo 9.

    A observação ocorre antes da deduplicação: outra estrutura da mesma cor
    ainda pode substituir uma aliada pelo primeiro inimigo encontrado.
    """
    m = contexto.mundo
    indice = (valor & 0x7fe0) >> 5
    if indice >= 1000:
        raise ValueError('Índice de estrutura fora de 0..999')
    p = indice * 276
    inimigo = int(not aliados(m.estruturas[p + 4], contexto.dono, m.mascaras_alianca))
    if m.estruturas[p + 8] == 9 and (not registro[5] or inimigo > registro[7]):
        struct.pack_into('<H', registro, 2, indice)
        registro[5], registro[7], registro[9] = 1, inimigo, fase & 255
    return 0x8000 | m.cores_estruturas.grade[celula & 65535]
