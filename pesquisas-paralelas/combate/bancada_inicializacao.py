"""Entradas x86 originais e observação das escritas nos quatro campos."""
import struct

from bancada_animacao import BancadaAnimacao
from bancada_combate import UNIDADES, RETORNO, x86

INICIALIZACAO = [(0x457350, 0x457e0c), (0x4570f0, 0x4570f4),
                (0x4475ac, 0x4475ef), (0x4474c5, 0x4474c7), (0x428cc0, 0x428e71)]


class BancadaInicializacao(BancadaAnimacao):
    def __init__(self):
        super().__init__()
        import unicorn
        self.escritas_campos = []
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._escrita)

    def _escrita(self, cpu, acesso, endereco, tamanho, valor, _):
        if UNIDADES <= endereco < UNIDADES + 800 * 276:
            indice, offset = divmod(endereco - UNIDADES, 276)
            campos = [c for c in (0x79, 0x7a, 0x8a, 0x8b) if offset <= c < offset + tamanho]
            for campo in campos:
                self.escritas_campos.append((cpu.reg_read(x86.UC_X86_REG_EIP), indice,
                    campo, (valor >> (8 * (campo - offset))) & 255))

    def parametros_tipo(self, tipo, caracteristicas, dono=0, mod1=0, mod12=0):
        for base, valor in ((0x4965d8, caracteristicas.visao),
                            (0x4965da, caracteristicas.alcance_quadrado),
                            (0x4965de, caracteristicas.recarga)):
            self.cpu.mem_write(base + tipo * 50, struct.pack('<H', valor & 65535))
        if dono not in (4, 200):
            base = 0x4dfba0 + dono * 468 + tipo * 18
            self.cpu.mem_write(base + 11, bytes([mod1 & 255]))
            self.cpu.mem_write(base + 16, bytes([mod12 & 255]))

    def caracterizar(self, indice):
        self.escritas_campos = []
        return self.executar(0x457350, INICIALIZACAO, dict(EAX=indice))

    def definir(self, indice, celula, direcao, tipo):
        self.escritas_campos = []
        return self.executar(0x457b87, INICIALIZACAO,
            dict(EAX=indice, EDX=celula, EBX=direcao, ECX=tipo))

    def pedido_leitura(self, indice):
        # Fragmento começa no XOR EAX imediatamente após a leitura do ID.
        return self.executar(0x479d47, [(0x479d47, 0x479d65)],
            parada=0x458461, pilha={4: struct.pack('<I', indice & 65535)},
            registradores={'ESP': 0x2008004})

    def pos_carga_missao(self, indice):
        self.escritas_campos = []
        return self.executar(0x46ad8b, INICIALIZACAO + [(0x46ad8b, 0x46b01e),
            (0x441fff, 0x442045), (0x4422da, 0x4422eb)], parada=0x46acff,
            pilha={12: struct.pack('<I', indice)}, registradores={'ESP': 0x2008004})

    def pos_carga_game(self, indice):
        self.escritas_campos = []
        return self.executar(0x46b08f, [(0x46b08f, 0x46b0e3)], parada=0x46b0e3,
            pilha={4: struct.pack('<I', indice)}, registradores={'ESP': 0x2008004})

    def pedido_leitura_game(self, indice, tamanho):
        return self.executar(0x46b06f, [(0x46b06f, 0x46b08f)], parada=0x458461,
            pilha={4: struct.pack('<I', indice), 12: struct.pack('<I', tamanho)},
            registradores={'ESP': 0x2008004})
