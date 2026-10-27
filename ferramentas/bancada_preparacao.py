"""Preparação e início dos candidatos originais, com checkpoints delimitados."""
import struct
from emulador import RETORNO
from solucionador_original import BancadaNavegacao


def gravar_preparacao(bancada, preparacao, ponteiro_rota):
    p, cpu = preparacao, bancada.cpu
    for endereco, formato, valor in (
            (0x4e0f34, 'B', p.flag_unidades), (0x4e0f35, 'B', p.flag_estruturas),
            (0x4e0f36, 'B', 1), (0x4e0f37, 'B', p.sucesso),
            (0x496302, 'B', p.concluida), (0x496304, 'H', p.contexto.unidade),
            (0x4e0f3c, 'I', ponteiro_rota), (0x4e0f41, 'B', p.contexto.dono),
            (0x4e0f42, 'B', p.contexto.mascara), (0x4e0f48, 'B', p.contexto.classe),
            (0x4e0f4a, 'H', p.alternativa), (0x4e0f4c, 'B', p.status)):
        cpu.mem_write(endereco, struct.pack('<' + formato, valor))
    cpu.mem_write(ponteiro_rota, b'\0\0')
    if p.registrar_extremos:
        cpu.mem_write(0x4e0f44, struct.pack('<HH', p.inicio, p.destino))


def gravar_inicio_candidatos(bancada, inicio, esp):
    cpu = bancada.cpu
    for endereco in (0x4e116a, 0x4e136a): cpu.mem_write(endereco, b'\0\0')
    cpu.mem_write(0x4e1772, struct.pack('<H', inicio.regiao_origem))
    cpu.mem_write(0x4e0f40, b'\0')
    cpu.mem_write(0x4e0f50, struct.pack('<I', 0x4e0f54))
    cpu.mem_write(0x4e0f54, inicio.registro_ocupantes)
    cpu.mem_write(0x4e0f68, bytes([len(inicio.regioes)]))
    if inicio.regioes:
        cpu.mem_write(0x4e0f6a, struct.pack('<' + 'H' * len(inicio.regioes), *inicio.regioes))
    for offset, formato, valor in ((0xec, 'I', 0), (0x108, 'I', 0), (0xd4, 'I', inicio.inicio),
                                   (0x4c, 'I', inicio.obstaculo_proximo),
                                   (0x3c4, 'B', inicio.todos_bloqueados), (0x2e0, 'B', inicio.direcao)):
        cpu.mem_write(esp + offset, struct.pack('<' + formato, valor))


class BancadaPreparacao(BancadaNavegacao):
    def escolher_original(self, buffers, custos, registros, semente, status=1, flags=(0, 0)):
        for endereco, buffer in zip((0x4e116a, 0x4e136a), buffers): self.cpu.mem_write(endereco, bytes(buffer))
        self.cpu.mem_write(0x4e0f54, b''.join(bytes(r) for r in registros))
        self.cpu.mem_write(0x4e0f34, bytes(flags))
        self.cpu.mem_write(0x4e0f4c, bytes([status]))
        self.cpu.mem_write(0x497164, struct.pack('<I', semente))
        r = self.executar(0x43b073, self.intervalos, parada=0x43b2a9,
                          pilha={0xec: struct.pack('<I', custos[0]), 0x108: struct.pack('<I', custos[1])})
        return dict(escolhido=(r['EDX'] - 0x4e116a) // 512,
                    buffers=tuple(bytes(self.cpu.mem_read(a, 512)) for a in (0x4e116a, 0x4e136a)),
                    status=self.cpu.mem_read(0x4e0f4c, 1)[0],
                    semente=struct.unpack('<I', self.cpu.mem_read(0x497164, 4))[0])

    def preparar_original(self, mundo, indice, inicio, destino, mascara=None, flags=(0, 0)):
        self.carregar_navegacao(mundo)
        rota = self.grades['rotas'] + indice * 512
        mascara = 1 + int(mundo.unidades[indice * 276 + 0xab] != 0) if mascara is None else mascara
        return self.executar(0x43b30b, self.intervalos,
                              dict(EAX=inicio, EDX=destino, EBX=indice, ECX=mascara),
                              pilha={4: struct.pack('<III', rota, *flags)}, limite_instrucoes=1000000)

    def inicio_original(self):
        return self.executar(0x42f214, self.intervalos, parada=(RETORNO, 0x430b7e), limite_instrucoes=1000000)

    def memoria_preparacao(self, indice=0):
        return (bytes(self.cpu.mem_read(0x4e0f34, 26)), bytes(self.cpu.mem_read(0x496302, 4)),
                bytes(self.cpu.mem_read(self.grades['rotas'] + indice * 512, 512)))

    def memoria_inicio(self, esp):
        ler = self.cpu.mem_read
        n = ler(0x4e0f68, 1)[0]
        return dict(regiao=bytes(ler(0x4e1772, 2)), fase=bytes(ler(0x4e0f40, 1)),
                    ponteiro=bytes(ler(0x4e0f50, 4)), registro=bytes(ler(0x4e0f54, 10)),
                    regioes=bytes(ler(0x4e0f68, 2 + n * 2)),
                    contagens=(bytes(ler(0x4e116a, 2)), bytes(ler(0x4e136a, 2))),
                    locais={off: bytes(ler(esp + off, tamanho)) for off, tamanho in
                            ((0xec, 4), (0x108, 4), (0xd4, 2), (0x4c, 2), (0x3c4, 1), (0x2e0, 1))})
