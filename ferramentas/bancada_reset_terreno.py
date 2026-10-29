"""Unpatched TerrainReset, MiniMapReset and BatimentModifyMap native runs."""
from bancada_descoberta_terreno import BancadaDescobertaTerreno, INTERVALOS_DIRETOS
from emulador import RETORNO, unicorn, x86

MINAS, ALEATORIO = 0x509954, 0x497164
INTERVALOS_TERRENO = [(0x46b315, 0x46b38f), (0x4704dc, 0x470520)]
INTERVALOS_MINIMAPA = [(0x469f00, 0x469f68), (0x48c3b0, 0x48c3c8), (0x48d890, 0x48d933)]
INTERVALOS_ESTRUTURA = [(0x419e97, 0x419fc8), (0x42399a, 0x4239a0)] + INTERVALOS_DIRETOS


class BancadaResetTerreno(BancadaDescobertaTerreno):
    # TerrainReset's per-cell loop head: 65,536 cells with one Random call each
    # exceed a single segment, so it may also resume with CPU/stack intact.
    pontos_retomada = BancadaDescobertaTerreno.pontos_retomada + (0x46b327,)

    def __init__(self):
        super().__init__()
        self.chamadas_aleatorio = 0
        self.memsets = []
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._observar_reset)

    def _observar_reset(self, cpu, endereco, tamanho, _):
        if endereco in self.paradas or endereco not in (0x4704dc, 0x48c3b0):
            return
        if endereco == 0x4704dc:
            self.chamadas_aleatorio += 1
            return
        eax, edx, ebx = (cpu.reg_read(getattr(x86, 'UC_X86_REG_'+r)) for r in ('EAX', 'EDX', 'EBX'))
        nomes = {self.grades[n]: n for n in ('mini_final', 'mini_unidades', 'mini_estruturas')}
        self.memsets.append((nomes.get(eax, hex(eax)), edx & 255, ebx))

    def carregar_reset(self, mundo, minas, aleatorio):
        self.carregar_saida(mundo)
        self.cpu.mem_write(MINAS, bytes(minas))
        self.cpu.mem_write(ALEATORIO, bytes(aleatorio))
        self.chamadas_aleatorio = 0
        self.memsets = []

    def ler_reset(self):
        return bytes(self.cpu.mem_read(MINAS, 80)), bytes(self.cpu.mem_read(ALEATORIO, 4))

    def conferir_reset(self, mundo, minas, aleatorio):
        erros = self.conferir_saida(mundo)
        atual_minas, atual_aleatorio = self.ler_reset()
        if atual_minas != bytes(minas):
            erros.append(dict(regiao='minas'))
        if atual_aleatorio != bytes(aleatorio):
            erros.append(dict(regiao='aleatorio', atual=atual_aleatorio.hex(), esperado=bytes(aleatorio).hex()))
        return erros

    def resetar_terreno(self):
        return self.executar(0x46b315, INTERVALOS_TERRENO, {}, parada=RETORNO, limite_instrucoes=1000000)

    def resetar_minimapa(self):
        return self.executar(0x469f00, INTERVALOS_MINIMAPA, {}, parada=RETORNO, limite_instrucoes=1000000)

    def modificar_minimapa_estrutura(self, indice, ativo):
        """0x419e97: AX structure index, DL nonzero -> SetMiniMap mode 6, zero -> mode 7."""
        return self.executar(0x419e97, INTERVALOS_ESTRUTURA, dict(EAX=indice, EDX=ativo),
                             parada=RETORNO, limite_instrucoes=1000000)
