"""Original structure habitation on core's physical harness, without replacement.

Core's segmented minimap resumptions are reused unchanged; every original
DecouvreTerrain/IllumineTerrain/SetMiniMap instruction executes natively.
"""
import hashlib
import struct

from bancada_colocacao_saida import BancadaColocacaoSaida
from emulador import RETORNO, UNIDADES, unicorn, x86

BASE_ESTRUTURAS = 0x49a0c8
BASE_PENDENCIAS = 0x4dd6e8
BASE_ESTRUTURAS_REALIZAVEIS = 0x4dfad4
BASE_CAPACIDADES = 0x4dfb2c
BASE_RECURSOS = 0x4e2ea8
BASE_UNIDADES_REALIZAVEIS = 0x4e1934
BASE_SORTILEGIOS = 0x508f30
BASE_INVENCOES = 0x508f44
REDE = 0x4e0730
INTERVALOS_HABITAVEIS = [
    (0x46c16d, 0x46c1b8), (0x41a5b8, 0x41a61c), (0x41cc70, 0x41cde0), (0x41db1d, 0x41db24),
    (0x41c76c, 0x41cb9a), (0x41aee2, 0x41aff8), (0x41ab5c, 0x41ac8b),
    (0x447148, 0x447197), (0x447483, 0x4474a6), (0x4471b8, 0x44724a), (0x44724a, 0x4472d3),
    (0x44228e, 0x4422b0), (0x42c3b0, 0x42c3b6), (0x474958, 0x474974), (0x474991, 0x4749ad),
    (0x467640, 0x4676e5)]
ENTRADAS = {0x41c76c: 'BatimentSetTechnologie', 0x41aee2: 'BatimentGetCase',
            0x46769d: 'GetRessourceStock', 0x41a5b8: 'BatimentEstHabiter', 0x41cc70: 'BatimentHabitable'}
# Guard bytes beside the economy tables detect any write outside them.
GUARDAS = ((BASE_PENDENCIAS+9152, 8), (BASE_ESTRUTURAS_REALIZAVEIS-8, 8), (BASE_CAPACIDADES+24, 4),
           # 0x4e199c..0x4e19a0 only: 0x4e19a0 holds the harness unit-pool pointer.
           (BASE_UNIDADES_REALIZAVEIS-8, 8), (BASE_UNIDADES_REALIZAVEIS+104, 4), (BASE_SORTILEGIOS-8, 8),
           (BASE_INVENCOES+20, 8), (BASE_RECURSOS-8, 8), (BASE_RECURSOS+128, 8))


class BancadaHabitaveis(BancadaColocacaoSaida):
    intervalos = BancadaColocacaoSaida.intervalos + INTERVALOS_HABITAVEIS

    def __init__(self):
        super().__init__(segmentar=True)
        self.entradas = {'predicado': 0, 'habitavel': 0, 'chamador': 0, 'tecnologia': 0, 'celula': 0}
        self.falhas = 0
        self.resultados = {}
        self.chamadas = []
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._chamada)

    def _chamada(self, cpu, endereco, tamanho, _):
        if endereco not in ENTRADAS or endereco in self.paradas:
            return
        eax, edx, ebx = (cpu.reg_read(getattr(x86, 'UC_X86_REG_'+r)) for r in ('EAX', 'EDX', 'EBX'))
        if endereco == 0x41c76c:
            self.chamadas.append((ENTRADAS[endereco], eax & 255, edx & 255))
        elif endereco == 0x46769d:
            dono = cpu.mem_read(cpu.reg_read(x86.UC_X86_REG_ESP)+4, 1)[0]
            self.chamadas.append((ENTRADAS[endereco], dono))
        else:
            self.chamadas.append((ENTRADAS[endereco], eax & 65535))

    def carregar(self, caso):
        m = caso.mundo
        self.carregar_saida(m)
        for base, tamanho in GUARDAS:
            self.cpu.mem_write(base, bytes(((base >> 2) + i) & 255 | 0x41 for i in range(tamanho)))
        for base, valor in ((BASE_PENDENCIAS, caso.pendencias), (BASE_ESTRUTURAS_REALIZAVEIS, caso.estruturas_realizaveis),
                            (BASE_CAPACIDADES, caso.capacidades.memoria), (BASE_RECURSOS, caso.economia.memoria),
                            (BASE_UNIDADES_REALIZAVEIS, caso.unidades_realizaveis), (BASE_SORTILEGIOS, caso.sortilegios),
                            (BASE_INVENCOES, caso.inventados), (REDE, bytes([caso.rede]))):
            self.cpu.mem_write(base, bytes(valor))
        self.guardas_iniciais = self.guardas()
        self.efeitos, self.chamadas = [], []

    def guardas(self):
        return [bytes(self.cpu.mem_read(b, n)) for b, n in GUARDAS]

    def estado(self):
        ler = lambda b, n: bytes(self.cpu.mem_read(b, n))
        return dict(estruturas=ler(BASE_ESTRUTURAS, 276000), unidades=ler(UNIDADES, 220800),
                    pendencias=ler(BASE_PENDENCIAS, 9152), estruturas_realizaveis=ler(BASE_ESTRUTURAS_REALIZAVEIS, 88),
                    capacidades=ler(BASE_CAPACIDADES, 24), economia=ler(BASE_RECURSOS, 128),
                    unidades_realizaveis=ler(BASE_UNIDADES_REALIZAVEIS, 104), sortilegios=ler(BASE_SORTILEGIOS, 20),
                    inventados=ler(BASE_INVENCOES, 20), rede=ler(REDE, 1))

    def resumo(self):
        """Whole mapped economic/physical buffers as hashes, plus ordered traces."""
        s = {k: hashlib.sha256(v).hexdigest() for k, v in self.estado().items()}
        for nome in ('atributos', 'donos_objetos', 'mini_final', 'mini_unidades', 'mini_estruturas', 'sombra'):
            s[nome] = hashlib.sha256(bytes(self.cpu.mem_read(self.grades[nome], 65536 if nome != 'sombra' else 4096))).hexdigest()
        for nome in ('regioes', 'tiles'):
            s[nome] = hashlib.sha256(bytes(self.cpu.mem_read(self.grades[nome], 131072))).hexdigest()
        for nome in ('descoberto', 'luz_bordas', 'contagem_luz'):
            s[nome] = hashlib.sha256(bytes(self.cpu.mem_read(self.grades[nome], 262144))).hexdigest()
        s['guardas_intactas'] = self.guardas() == self.guardas_iniciais
        return dict(sha256=s, chamadas=[list(c) for c in self.chamadas], efeitos=[list(e) for e in self.efeitos])

    def _resultado(self, rotulo, regs):
        chave = (rotulo, hex(regs['EIP']))
        self.resultados[chave] = self.resultados.get(chave, 0) + 1
        return regs

    def executar_ou_falhar(self, metodo, *args, **kwargs):
        """Return registers, or None after an original CPU exception (e.g. #DE)."""
        try:
            return metodo(*args, **kwargs)
        except unicorn.UcError:
            self.falhas += 1
            self.resultados[('falha', hex(self.cpu.reg_read(x86.UC_X86_REG_EIP)))] = (
                self.resultados.get(('falha', hex(self.cpu.reg_read(x86.UC_X86_REG_EIP))), 0) + 1)
            return None

    def definir_tecnologia(self, jogador, tipo):
        self.entradas['tecnologia'] += 1
        return self._resultado('tecnologia', self.executar(
            0x41c76c, self.intervalos, dict(EAX=jogador, EDX=tipo), limite_instrucoes=1000000))

    def celula_central(self, indice, *, edx=0x1234abcd, ebx=0x5eed0bb5):
        self.entradas['celula'] += 1
        return self._resultado('celula', self.executar(
            0x41aee2, self.intervalos, dict(EAX=indice, EDX=edx, EBX=ebx), limite_instrucoes=1000000))

    def esta_habitada(self, indice):
        self.entradas['predicado'] += 1
        return self._resultado('predicado', self.executar(
            0x41a5b8, self.intervalos, dict(EAX=indice), limite_instrucoes=1000000))

    def tornar_habitavel(self, indice, *, edi=0x5a5a5a5a, paradas=()):
        """Entry 0x41cc70; optional declared stops at 0x476851/0x476cb3."""
        self.entradas['habitavel'] += 1
        return self._resultado('habitavel', self.executar(
            0x41cc70, self.intervalos, dict(EAX=indice, EDI=edi), parada={RETORNO, *paradas},
            limite_instrucoes=1000000))

    def varrer_estrutura(self, indice, *, paradas=()):
        """MissionPlaceTerrain 0x46c195..0x46c1a7, after PlaceBatiment, before BatimentModifyMap."""
        self.entradas['chamador'] += 1
        return self._resultado('chamador', self.executar(
            0x46c195, self.intervalos, dict(EAX=indice, EDX=indice, EBX=indice, EDI=0x5a5a5a5a),
            parada={0x46c1a7, *paradas}, limite_instrucoes=1000000))
