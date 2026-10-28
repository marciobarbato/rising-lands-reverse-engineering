"""Projéteis no EXE original, com pool sintético e chamadas não substituídas.

Dano: grade sem ocupantes. Iluminação: dimensões zero, raio pequeno, laços
originais sem células. Observa os argumentos; não valida esses efeitos no mundo.
"""
import struct

from bancada_animacao import BancadaAnimacao, ANIMACAO, PROJETEIS, x86

ROTINAS = ANIMACAO + [(0x46e00a, 0x46e049), (0x46e422, 0x46e44c),
    (0x46e4ca, 0x46e52c), (0x474734, 0x47474f), (0x476851, 0x47693a),
    (0x476cb3, 0x476e82)]


class BancadaProjeteis(BancadaAnimacao):
    def __init__(self):
        super().__init__()
        import unicorn
        self.mundo([bytes(276) for _ in range(800)])
        self.cpu.mem_write(0x497168, bytes(4))
        self.eventos = []
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._observar_projeteis)

    def _observar_projeteis(self, cpu, endereco, tamanho, _):
        nomes = {0x450874: 'InfligeDegat', 0x474734: 'SortilegeGetRayonEffet',
                 0x476851: 'DecouvreTerrain', 0x476cb3: 'IllumineTerrain'}
        if endereco not in nomes:
            return
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        retorno = struct.unpack('<I', cpu.mem_read(esp, 4))[0]
        if not 0x46e208 <= retorno < 0x46e422:
            return
        a, d, b, c = (cpu.reg_read(getattr(x86, 'UC_X86_REG_' + n))
                       for n in ('EAX', 'EDX', 'EBX', 'ECX'))
        if endereco == 0x450874:
            args = (a & 65535, d & 255, b & 65535, c & 255, cpu.mem_read(esp + 4, 1)[0])
        elif endereco == 0x474734:
            args = (a & 255,)
        else:
            args = (a & 65535, d & 65535, b & 255)
        self.eventos.append((nomes[endereco], args))

    def pool(self, dados, raio=3):
        if len(dados) != 5600 or not 0 <= raio <= 10:
            raise ValueError('Pool de 5600 bytes e raio 0..10 para laços delimitados')
        self.cpu.mem_write(PROJETEIS, bytes(dados))
        self.cpu.mem_write(0x497170, struct.pack('<H', raio))
        self.eventos = []

    def ler_pool(self):
        return bytes(self.cpu.mem_read(PROJETEIS, 5600))

    def resetar(self):
        return self.executar(0x46e00a, ROTINAS)

    def existe(self, indice):
        return self.executar(0x46e02c, ROTINAS, dict(EAX=indice))['EAX'] & 255

    def livre(self):
        return self.executar(0x46e422, ROTINAS)['EAX'] & 65535

    @staticmethod
    def _pilha(*valores):
        # Envenena bits altos para confirmar a largura lida em cada argumento.
        return {4: struct.pack('<' + 'I' * len(valores),
                    *((v & 65535) | 0xa5a50000 for v in valores))}

    def definir(self, indice, tipo, origem, alvo, modo, atacante, direcao, dx, dy, flag):
        return self.executar(0x46e208, ROTINAS,
            dict(EAX=indice | 0xa5a50000, EDX=tipo | 0xabcd0000,
                 EBX=origem | 0xface0000, ECX=alvo | 0xcafe0000),
            pilha=self._pilha(modo, atacante, direcao, dx, dy, flag), limite_instrucoes=100000)

    def iniciar(self, tipo, origem, alvo, modo, atacante, direcao, dx, dy, flag):
        return self.executar(0x46e44c, ROTINAS,
            dict(EAX=tipo | 0xabcd0000, EDX=origem | 0xa5a50000,
                 EBX=alvo | 0xface0000, ECX=modo | 0xcafe0000),
            pilha=self._pilha(atacante, direcao, dx, dy, flag), limite_instrucoes=100000)

    def preparar_linha(self, indice=0):
        return self.executar(0x46e049, ROTINAS, dict(EAX=PROJETEIS + indice * 56))

    def calcular_linha(self, indice=0):
        return self.executar(0x46e4ca, ROTINAS, dict(EAX=PROJETEIS + indice * 56))
