"""Backend compatível: executa Chemin_Verouille/CheminCalcul no EXE original.

É explícito porque requer Unicorn/JIT. Nenhum algoritmo auxiliar é apresentado
como tradução do solucionador; a parte Python cobre consultas, desvios locais
e o controle dos estados de caminho.
"""
import struct
from bancada_avanco import BancadaAvanco
from bancada_caminhos import INTERVALOS as INTERVALOS_CAMINHOS
from emulador import UNIDADES
from ordens_unidades import PASSO


class BancadaNavegacao(BancadaAvanco):
    intervalos = BancadaAvanco.intervalos + INTERVALOS_CAMINHOS + [
        (0x448d08, 0x448f37), (0x4770ee, 0x4772ec), (0x446693, 0x4467a1), (0x440d55, 0x440d5e),
        (0x449176, 0x4492f0), (0x44330c, 0x443470), (0x44930c, 0x449526),
    ]

    def __init__(self):
        super().__init__()
        self.cpu.mem_map(0x1800000, 0x120000)

    def carregar_navegacao(self, mundo):
        self.carregar_fisica(mundo)
        self.cpu.mem_write(0x507db0, struct.pack('<I', self.grades['sombra'] + 0x200))
        self.cpu.mem_write(self.grades['sombra'] + 0x200, bytes(mundo.marcadores_obstaculos_tiles))
        self.cpu.mem_write(0x497164, struct.pack('<I', mundo.semente_caminhos))
        self.cpu.mem_write(0x4e1771, bytes([mundo.permitir_aliados_parados]))
        for dono, mascara in enumerate(mundo.mascaras_alianca):
            self.cpu.mem_write(self.grades['jogadores'] + dono * 20 + 6, bytes([mascara]))

    def consultar(self, indice, celula, mascara):
        buffer = self.grades['sombra'] + 0x100
        self.cpu.mem_write(buffer, b'\xff' * 8)
        r = self.executar(0x442668, self.intervalos, dict(EAX=indice, EDX=celula, EBX=mascara, ECX=buffer), limite_instrucoes=1000000)
        return bool(r['EAX'] & 255), list(struct.unpack('<4H', self.cpu.mem_read(buffer, 8)))

    def direto(self, indice):
        self.executar(0x448d08, self.intervalos, dict(EAX=indice), limite_instrucoes=1000000)

    def componente(self, classes, inicio, rotulo):
        self.cpu.mem_write(0x1800000, bytes(classes))
        self.cpu.mem_write(self.grades['regioes'], bytes(131072))
        self.executar(0x42efd9, [(0x42efd9, 0x42f11d)],
                      dict(EAX=0x1810000, EDX=inicio, ESI=0x1800000), parada=0x42ef4d,
                      pilha={8: struct.pack('<I', rotulo), 0x10: struct.pack('<I', 0x1810000),
                             0x1c: struct.pack('<I', inicio)}, limite_instrucoes=1000000)
        return list(struct.unpack('<65536H', self.cpu.mem_read(self.grades['regioes'], 131072)))

    def preparar_busca(self, mundo, indice):
        self.carregar_navegacao(mundo)
        rota = self.grades['rotas'] + indice * 512
        mascara = 1 + int(mundo.unidades[indice * PASSO + 0xab] != 0)
        self.executar(0x43b30b, self.intervalos,
                      dict(EAX=mundo.palavra(indice, 8), EDX=mundo.palavra(indice, 0x7e), EBX=indice, ECX=mascara),
                      pilha={4: struct.pack('<III', rota, 0, 0)}, limite_instrucoes=1000000)
        return self.calcular(mundo, indice)

    def calcular(self, mundo, indice):
        self.executar(0x42f214, self.intervalos, limite_instrucoes=1000000)
        return self.resultado(indice)

    def resultado(self, indice):
        def ler(a, formato):
            return struct.unpack('<' + formato, self.cpu.mem_read(a, struct.calcsize(formato)))[0]
        return dict(buffer_rota=bytes(self.cpu.mem_read(self.grades['rotas'] + indice * 512, 512)),
                    contexto=dict(unidade=ler(0x496304, 'H'), ocupada=ler(0x4e0f36, 'B'),
                                  sucesso=ler(0x4e0f37, 'B'), ponteiro_rota=ler(0x4e0f3c, 'I'), concluida=ler(0x496302, 'B')),
                    status=ler(0x4e0f4c, 'B'), destino_alternativo=ler(0x4e0f4a, 'H'),
                    destino_calculado=ler(0x4e0f46, 'H'), semente=ler(0x497164, 'I'))

    def copiar_efeitos_ordens(self, mundo):
        mundo.unidades[:] = self.cpu.mem_read(UNIDADES, len(mundo.unidades))
        mundo.estruturas[:] = self.cpu.mem_read(0x49a0c8, len(mundo.estruturas))
        r = self.resultado(0)['contexto']
        for nome, valor in r.items():
            setattr(mundo.busca, nome, valor)

    def pulso_navegacao(self, indice):
        """Sequência original de caminho/física; exclui animação contínua e som."""
        from movimento import pode_avancar
        def unidade():
            return self.ler_unidade(indice)
        u = unidade()
        if u[2] == 2:
            r = self.concluir(indice)
            if r['EIP'] == 0x455a6f:
                self.girar(indice)
            elif r['EIP'] == 0x4555a7:
                estado = u[0x88]
                fisica = False
                if estado in (0, 5):
                    if not u[0x86] and not u[0x87]:
                        self.direto(indice) if estado == 0 else self.escolher_proximo(indice)
                    fisica = True
                else:
                    r = self.executar(0x44930c, self.intervalos, dict(EAX=indice),
                                      parada=(0x3000000, 0x448f50), limite_instrucoes=1000000)
                    fisica = r['EIP'] == 0x448f50
                u = unidade()
                if fisica and struct.unpack_from('<H', u, 8)[0] != struct.unpack_from('<H', u, 0x7c)[0]:
                    if u[0x90] != u[0x91]:
                        self.girar(indice)
                    u = unidade()
                    if pode_avancar(u[0x90], u[0x91]):
                        self.avancar(indice)
        self.notificar(indice)


class SolucionadorOriginal:
    def __init__(self):
        self.bancada = BancadaNavegacao()

    @staticmethod
    def _validar(mundo):
        if any(v & 0x8000 for v in mundo.regioes):
            raise NotImplementedError('Busca com estruturas codificadas requer a grade auxiliar de estruturas, ainda não reconstruída')

    def iniciar(self, mundo, indice):
        self._validar(mundo)
        return self.bancada.preparar_busca(mundo, indice)

    def continuar(self, mundo, indice):
        self._validar(mundo)
        self.bancada.carregar_navegacao(mundo)
        return self.bancada.calcular(mundo, indice)

    def desbloquear(self, mundo, indice):
        b = self.bancada
        b.carregar_navegacao(mundo)
        r = b.executar(0x449176, b.intervalos, dict(EAX=indice), limite_instrucoes=1000000)
        b.copiar_efeitos_ordens(mundo)
        return dict(desbloqueou=bool(r['EAX'] & 255))
