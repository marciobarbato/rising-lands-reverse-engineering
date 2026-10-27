"""Original x86 para animação/controle e chamadas de emissão delimitadas.

Projéteis usam pool cheio, dano usa células sem ocupantes e magia ID inválido
nos testes de despacho. Isso executa os ramos originais de insucesso/ausência,
sem trocar CALLs por mocks. Movimento, balão e áudio param em entradas nomeadas.
"""
import struct

from bancada_combate import BancadaCombate, MIRA, LINHA, UNIDADES, RETORNO, x86

VISIBILIDADE, PROJETEIS = 0x1160000, 0x1170000
ANIMACAO = MIRA + LINHA + [(0x451914, 0x452c91), (0x447977, 0x4479b4),
    (0x4479c4, 0x447acf), (0x4484a7, 0x448699), (0x4511a5, 0x4513c7),
    (0x410fcc, 0x4110bf), (0x46e44c, 0x46e4ca), (0x4766f0, 0x47670a),
    (0x473510, 0x473692), (0x44357c, 0x443688), (0x450874, 0x4510dd),
    (0x41b54a, 0x41b579), (0x4465df, 0x446693), (0x46e208, 0x46e422),
    (0x4462aa, 0x4462b0), (0x46e049, 0x46e17f), (0x46fc09, 0x46fc0f)]
EFEITOS = {0x46e44c: 'ProjectileInit', 0x450874: 'InfligeDegat',
    0x473510: 'SortilegeEffet', 0x44357c: 'ResetOrdre',
    0x4457d3: 'SetDeplaceEngin', 0x44930c: 'DeplaceEngin',
    0x447b2f: 'AnimBallonStatic', 0x440c5d: 'EnginGetVolume', 0x48aa79: 'PlaySnd_PostSound'}
PENDENTES = {0x4457d3, 0x44930c, 0x447b2f, 0x440c5d, 0x48aa79}


class BancadaAnimacao(BancadaCombate):
    def __init__(self):
        super().__init__()
        import unicorn
        self.cpu.mem_map(VISIBILIDADE, 0x20000)
        self.cpu.mem_write(0x507d78, struct.pack('<I', VISIBILIDADE))
        self.cpu.mem_write(VISIBILIDADE, b'\1' * 65536)
        self.cpu.mem_write(0x508041, b'\0')
        self.cpu.mem_write(0x5080f0, struct.pack('<I', PROJETEIS))
        pool = bytearray(100 * 56)
        for i in range(100):
            pool[i * 56 + 2] = 1
        self.cpu.mem_write(PROJETEIS, bytes(pool))
        self.chamadas = []
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._registrar)

    def mundo(self, unidades, grade=None, mascaras=(0, 0, 0, 0, 0), terreno=None):
        super().mundo(unidades, grade, mascaras, terreno)
        if grade is None:
            # ffff tem bit 15 e seria interpretado como construção por
            # ChercheIndiceBatiment. Região natural zero é vazia para ambos.
            self.cpu.mem_write(0x1100000, bytes(0x20000))

    def _registrar(self, cpu, endereco, tamanho, _):
        if endereco not in EFEITOS:
            return
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        retorno = struct.unpack('<I', cpu.mem_read(esp, 4))[0]
        if not 0x451914 <= retorno < 0x452c91:
            return
        r = {nome: cpu.reg_read(getattr(x86, 'UC_X86_REG_' + nome)) for nome in ('EAX', 'EDX', 'EBX', 'ECX')}
        nome = EFEITOS[endereco]
        if nome == 'ProjectileInit':
            extras = struct.unpack('<5I', cpu.mem_read(esp + 4, 20))
            args = (r['EAX'] & 255, r['EDX'] & 65535, r['EBX'] & 65535, r['ECX'] & 255,
                    extras[0] & 65535, extras[1] & 255, self._s16(extras[2]), self._s16(extras[3]), extras[4] & 255)
        elif nome == 'InfligeDegat':
            args = (r['EAX'] & 65535, r['EDX'] & 255, r['EBX'] & 65535, r['ECX'] & 255,
                    cpu.mem_read(esp + 4, 1)[0])
        elif nome == 'SortilegeEffet':
            args = (r['EAX'] & 65535, r['EDX'] & 255, r['EBX'] & 65535)
        elif nome == 'SetDeplaceEngin':
            args = (r['EAX'] & 65535, r['EDX'] & 65535)
        elif nome == 'PlaySnd_PostSound':
            args = (r['EAX'], r['EDX'], r['ECX'], struct.unpack('<I', cpu.mem_read(esp + 4, 4))[0],
                    (r['EBX'] - UNIDADES - 0x104) // 276)
        else:
            args = (r['EAX'] & 65535,)
        self.chamadas.append((nome, args))

    @staticmethod
    def _s16(v):
        return ((v + 32768) & 65535) - 32768

    def preparar_busca(self, busca):
        for end, formato, valor in ((0x496304, 'H', busca.unidade), (0x4e0f36, 'B', busca.ocupada),
                (0x4e0f37, 'B', busca.sucesso), (0x4e0f3c, 'I', busca.ponteiro_rota)):
            self.cpu.mem_write(end, struct.pack('<' + formato, valor))

    def ler_busca(self):
        from animacao_disparo import BuscaAtaque
        return BuscaAtaque(struct.unpack('<H', self.cpu.mem_read(0x496304, 2))[0],
            self.cpu.mem_read(0x4e0f36, 1)[0], self.cpu.mem_read(0x4e0f37, 1)[0],
            struct.unpack('<I', self.cpu.mem_read(0x4e0f3c, 4))[0])

    def passo_ataque(self, indice):
        self.chamadas = []
        r = self.executar(0x451914, ANIMACAO, dict(EAX=indice),
                         parada={RETORNO, *PENDENTES}, limite_instrucoes=100000)
        # O gancho de limites para antes dos demais hooks no checkpoint.
        if r['EIP'] in PENDENTES:
            self._registrar(self.cpu, r['EIP'], 0, None)
        return r
