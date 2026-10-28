"""Live attack chain on the intact EXE over one shared Core world.

Unpatched native segments: SetAttaqueEngin, the declared EnginNextEtape prelude
head (to the reload store), the state-1/24 branch at 0x456886 to its exit,
CalculAttaqueEngin with emission, ProjectileCalcul with impacts, damage and
SetDyingEngin. Named stops interrupt the CPU before the dependency's body or
call executes. Every mapped page is snapshotted around each segment.
"""
import struct

from bancada_consumo_fisico import BancadaConsumoFisico, INTERVALOS as INTERVALOS_FISICOS, PROJETEIS, TIPOS, MATRIZES
from bancada_animacao import ANIMACAO
from bancada_maquina_projeteis import MAQUINA
from bancada_ordens import OBJETOS, BASE_ESTRUTURAS
from ordens_unidades import BASE_GRUPOS
from emulador import UNIDADES, PILHA, RETORNO, x86

RAMO, SAIDA_RAMO = 0x456886, 0x454ccd
PRELUDIO, FIM_PRELUDIO = 0x45442c, 0x454591
INTERVALOS = INTERVALOS_FISICOS + ANIMACAO + MAQUINA + [
    (0x45673b, 0x4568ad), (PRELUDIO, FIM_PRELUDIO), (0x445a36, 0x445af1),
    (0x41a70b, 0x41a735), (0x41a08c, 0x41a0ab), (0x46d817, 0x46d838)]
# Named dependency stops: the CPU halts before the instruction executes.
PARADAS = {
    0x4567a9: 'iagUnitSendMessage',  # branch call site, invalid target of an AI owner
    0x440c5d: 'EnginGetVolume', 0x48aa79: 'PlaySnd_PostSound', 0x48aacf: 'HandleSnd_Update',
    0x44930c: 'DeplaceEngin', 0x4704dc: 'Random', 0x473510: 'SortilegeEffet',
    0x447b2f: 'AnimBallonStatic', 0x44fb20: 'EnginSetLevelExperience',
}
DIPLOMACIA = 0x46d600  # PlayerAAttaqueSet: a stop only when both owners are 0..3
CHECKPOINT_ATAQUE = 0x451914
OITO_A = 0x8a


class BancadaAtaqueVivo(BancadaConsumoFisico):
    def __init__(self):
        super().__init__()
        import unicorn
        self.escritas_8a = []
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._observar_8a, begin=UNIDADES, end=UNIDADES + 220800 - 1)
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._diplomacia, begin=DIPLOMACIA, end=DIPLOMACIA)
        self.parada_diplomacia = False

    def _observar_8a(self, cpu, acesso, endereco, tamanho, valor, _):
        rel = endereco - UNIDADES
        for k in range(tamanho):
            if (rel + k) % 276 == OITO_A:
                self.escritas_8a.append((cpu.reg_read(x86.UC_X86_REG_EIP), (rel + k) // 276, (valor >> 8 * k) & 255))

    def _diplomacia(self, cpu, endereco, tamanho, _):
        a, d = cpu.reg_read(x86.UC_X86_REG_EAX) & 255, cpu.reg_read(x86.UC_X86_REG_EDX) & 255
        if a < 4 and d < 4:
            self.parada_diplomacia = True
            cpu.emu_stop()

    def preparar_vivo(self, mundo, danos, pool, tipos):
        if len(tipos) != 1300:
            raise ValueError('Loaded type table must hold 26 x 50 bytes')
        self.preparar(mundo, danos, pool)
        self.cpu.mem_write(0x4965ae, bytes(tipos))
        self.cpu.mem_write(self.grades['jogadores'] + 4 * 20 + 6, b'\0')
        self.escritas_8a = []

    def contador(self, valor):
        self.cpu.mem_write(0x508f7c, struct.pack('<I', valor & 0xffffffff))

    def _limpar(self):
        self.eventos_consumo, self.pendentes, self.entradas_consumo = [], [], []
        self.eventos_wrapper, self.retornos_wrapper, self.eventos_morte = [], [], []
        self.random_projectile, self.rand_pendentes, self.impactos_projetil = [], [], []
        self.parada_diplomacia = False

    def _segmento(self, entrada, registradores, saida):
        self._limpar()
        try:
            r = self.executar(entrada, INTERVALOS, registradores, parada={saida, *PARADAS},
                              limite_instrucoes=1000000)
        except RuntimeError:
            if not self.parada_diplomacia:
                raise
            return 'PlayerAAttaqueSet', {'EIP': self.cpu.reg_read(x86.UC_X86_REG_EIP)}
        if r['EIP'] == saida:
            return None, r
        if r['EIP'] in PARADAS:
            return PARADAS[r['EIP']], r
        raise RuntimeError(f'Unexpected native stop 0x{r["EIP"]:08x}')

    def definir_ataque(self, indice, modo, referencia):
        return self._segmento(0x445a36, dict(EAX=indice, EDX=modo, EBX=referencia), RETORNO)

    def preludio(self, indice):
        return self._segmento(PRELUDIO, dict(EAX=indice), FIM_PRELUDIO)

    def ramo(self, indice, checkpoint_ataque=False):
        """Enter at 0x456886 with ESI = record and DI = index, as the state table does."""
        saida = CHECKPOINT_ATAQUE if checkpoint_ataque else SAIDA_RAMO
        nome, r = self._segmento(RAMO, dict(ESI=UNIDADES + indice * 276, EDI=indice), saida)
        if checkpoint_ataque and nome is None:
            return 'CalculAttaqueEngin', r
        return nome, r

    def projeteis(self):
        return self._segmento(0x46fc0f, None, RETORNO)

    # Whole-memory snapshots, page-compared to locate every changed byte.
    def regioes(self):
        return [(inicio, fim - inicio + 1) for inicio, fim, _ in self.cpu.mem_regions()
                if not PILHA <= inicio < PILHA + 0x10000]

    def instantaneo(self):
        return {inicio: bytes(self.cpu.mem_read(inicio, tamanho)) for inicio, tamanho in self.regioes()}

    @staticmethod
    def alteracoes(antes, depois):
        mudancas = []
        for inicio, a in antes.items():
            b = depois[inicio]
            for pagina in range(0, len(a), 4096):
                pa, pb = a[pagina:pagina + 4096], b[pagina:pagina + 4096]
                if pa != pb:
                    mudancas += [inicio + pagina + k for k in range(len(pa)) if pa[k] != pb[k]]
        return mudancas

    def areas(self):
        """Python-modeled areas in native layout (see test_ataque_vivo.areas_mundo)."""
        g = self.grades
        def ler(endereco, tamanho):
            return bytes(self.cpu.mem_read(endereco, tamanho))
        return dict(
            unidades=ler(UNIDADES, 220800), estruturas=ler(BASE_ESTRUTURAS, 276000),
            grupos=ler(BASE_GRUPOS, 3200), objetos=ler(OBJETOS, 65536),
            atributos=ler(g['atributos'], 65536), regioes=ler(g['regioes'], 131072), tiles=ler(g['tiles'], 131072),
            donos_objetos=ler(g['donos_objetos'], 65536), mini_final=ler(g['mini_final'], 65536),
            mini_unidades=ler(g['mini_unidades'], 65536), mini_estruturas=ler(g['mini_estruturas'], 65536),
            descoberto=ler(g['descoberto'], 262144), luz_bordas=ler(g['luz_bordas'], 262144),
            contagem_luz=ler(g['contagem_luz'], 262144), sombra=ler(g['sombra'], 256),
            rotas=ler(g['rotas'], 409600), projeteis=ler(PROJETEIS, 5600),
            busca=ler(0x496304, 2) + ler(0x4e0f36, 2) + ler(0x4e0f3c, 4) + ler(0x496302, 1),
            iteracao=ler(0x51b844, 4) + ler(0x51b848, 2),
            alerta=ler(0x4e19c0, 4) + ler(0x496acc, 2))

    def modelado(self):
        """Address intervals covered by areas(); any other changed byte is unmodeled."""
        g = self.grades
        faixas = [(UNIDADES, 220800), (BASE_ESTRUTURAS, 276000), (BASE_GRUPOS, 3200), (OBJETOS, 65536),
                  (PROJETEIS, 5600), (0x496304, 2), (0x4e0f36, 2), (0x4e0f3c, 4), (0x496302, 1),
                  (0x51b844, 4), (0x51b848, 2), (0x4e19c0, 4), (0x496acc, 2)]
        for nome, tamanho in (('atributos', 65536), ('regioes', 131072), ('tiles', 131072),
                              ('donos_objetos', 65536), ('mini_final', 65536), ('mini_unidades', 65536),
                              ('mini_estruturas', 65536), ('descoberto', 262144), ('luz_bordas', 262144),
                              ('contagem_luz', 262144), ('sombra', 256), ('rotas', 409600)):
            faixas.append((g[nome], tamanho))
        return faixas
