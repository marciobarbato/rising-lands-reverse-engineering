"""As três rotinas de terreno originais, sem substituição de chamadas internas."""
import struct
from solucionador_original import BancadaNavegacao


class BancadaTerrenoEstruturas(BancadaNavegacao):
    intervalos = BancadaNavegacao.intervalos + [
        (0x41b78f, 0x41b9d6), (0x41ba49, 0x41bb8a), (0x41ab5c, 0x41ac8b),
        (0x41db1d, 0x41db24), (0x41fd56, 0x41fd5e), (0x42399a, 0x4239a0),
        (0x476251, 0x476263),
    ]

    def aplicar_terreno(self, indice, origem, primeiro_tile, mascara_tipo20=None):
        if mascara_tipo20 is not None:
            if len(mascara_tipo20) != 20:
                raise ValueError('São necessários 20 bytes para a máscara em RAM')
            self.cpu.mem_write(0x4dfb9c, bytes(mascara_tipo20))
        return self.executar(0x41ba49, self.intervalos, dict(EAX=origem, EDX=primeiro_tile, EBX=indice),
                              limite_instrucoes=1000000)

    def resetar_terreno(self, indice, modo):
        return self.executar(0x41b888, self.intervalos, dict(EAX=indice, EDX=modo), limite_instrucoes=1000000)

    def remover_regioes(self, indice):
        return self.executar(0x41b78f, self.intervalos, dict(EAX=indice), limite_instrucoes=1000000)

    def conferir_terreno(self, mundo):
        erros = self.conferir_fisica(mundo)
        c = mundo.cores_estruturas
        for nome, endereco, esperado in (
                ('cores', self.grades['cores_estruturas'], bytes(c.grade)),
                ('alocador_cores', 0x4e1570, bytes(c.livres + c.liberadas)),
                ('pilha_cores', 0x4e0732, struct.pack('<1024H', *c.pilha))):
            atual = bytes(self.cpu.mem_read(endereco, len(esperado)))
            if atual != esperado:
                diferentes = [i for i, (a,b) in enumerate(zip(atual, esperado)) if a != b]
                erros.append(dict(regiao=nome, total=len(diferentes), primeiros_offsets=diferentes[:10]))
        return erros
