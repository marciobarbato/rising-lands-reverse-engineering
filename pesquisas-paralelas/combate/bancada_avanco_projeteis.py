"""Avanço/impacto no x86 original; dano em grade vazia, RNG original observado."""
import struct

from bancada_projeteis import BancadaProjeteis, PROJETEIS, x86

# Escopo menor que a bancada de ataque: dano sem ocupantes só precisa dessas
# consultas. Limite maior de instruções comporta nove buscas de 800 unidades.
AVANCO = [(0x46e4ca, 0x46fc0f), (0x46e208, 0x46e422), (0x46e049, 0x46e17f),
    (0x4704dc, 0x470520), (0x450874, 0x4510dd), (0x4465df, 0x446693),
    (0x4462aa, 0x4462b0), (0x41b54a, 0x41b579)]


class BancadaAvanco(BancadaProjeteis):
    def __init__(self):
        super().__init__()
        import unicorn
        self.trilha = []
        self.resultados_random = []
        self.marcador_random = None
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._observar_avanco)

    def _observar_avanco(self, cpu, endereco, tamanho, _):
        if endereco not in (0x450874, 0x46e208, 0x4704dc, 0x47051c):
            return
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        if endereco == 0x47051c:
            valor = cpu.reg_read(x86.UC_X86_REG_EAX)
            self.resultados_random.append(valor)
            self.trilha.append(('Random', (self.marcador_random, valor)))
            return
        retorno = struct.unpack('<I', cpu.mem_read(esp, 4))[0]
        a, d, b, c = (cpu.reg_read(getattr(x86, 'UC_X86_REG_' + n))
                      for n in ('EAX', 'EDX', 'EBX', 'ECX'))
        if endereco == 0x450874 and 0x46e5fe <= retorno < 0x46eaf8:
            self.trilha.append(('InfligeDegat', (a & 65535, d & 255, b & 65535,
                                                c & 255, cpu.mem_read(esp + 4, 1)[0])))
        elif endereco == 0x46e208 and 0x46eaf8 <= retorno < 0x46fc0f:
            m, at, di, dx, dy, fl = struct.unpack('<6I', cpu.mem_read(esp + 4, 24))
            self.trilha.append(('ProjectileSet', (a & 65535, d & 255, b & 65535, c & 65535,
                m & 255, at & 65535, di & 255, self._s16(dx), self._s16(dy), fl & 255)))
        elif endereco == 0x4704dc:
            if not 0x46eaf8 <= retorno < 0x46fc0f:
                raise RuntimeError('Random fora do chamador delimitado')
            self.marcador_random = a

    def contexto_avanco(self, semente=1, incremento=1, dimensoes=(256, 256)):
        self.cpu.mem_write(0x497164, struct.pack('<I', semente & 0xffffffff))
        self.cpu.mem_write(0x508f7c, bytes([incremento & 255]))
        self.cpu.mem_write(0x497168, struct.pack('<HH', *dimensoes))

    def limpar_trilha(self):
        self.trilha = []
        self.resultados_random = []
        self.marcador_random = None

    def animar(self, indice):
        return self.executar(0x46e52c, AVANCO, dict(EAX=indice | 0xabcd0000))

    def infligir(self, indice):
        self.limpar_trilha()
        return self.executar(0x46e5fe, AVANCO, dict(EAX=PROJETEIS + 56 * indice), limite_instrucoes=500000)

    def avancar(self, indice):
        self.limpar_trilha()
        return self.executar(0x46eaf8, AVANCO, dict(EAX=PROJETEIS + 56 * indice), limite_instrucoes=500000)
