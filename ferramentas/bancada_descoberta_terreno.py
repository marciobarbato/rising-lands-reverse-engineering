"""Unpatched discovery/light native runs with per-cell entry traces."""
from bancada_colocacao_missao import BancadaColocacaoMissao
from emulador import RETORNO, unicorn, x86

# Exactly the exported DecouvreCase/DecouvreTerrain, IllumineCase/IllumineTerrain,
# Distance, SetMiniMap and its four leaf queries: direct entries reach nothing else.
INTERVALOS_DIRETOS = [(0x47670a, 0x476851), (0x476851, 0x47693a), (0x476968, 0x476adc),
                      (0x476cb3, 0x476e82), (0x47954c, 0x479555), (0x46a388, 0x46a70c),
                      (0x4765f4, 0x476647), (0x46003b, 0x460051), (0x4766f0, 0x47670a),
                      (0x476951, 0x476968)]


class BancadaDescobertaTerreno(BancadaColocacaoMissao):
    # SetMiniMap pixel-loop head: one 128x128 block (1-cell-wide maps) exceeds
    # the one-second segment budget, so it may also resume with CPU/stack intact.
    pontos_retomada = (0x46a388, 0x46a623)

    def __init__(self):
        super().__init__(segmentar=True)
        self.celulas = []
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._observar_celula)

    def _observar_celula(self, cpu, endereco, tamanho, _):
        if endereco in self.paradas or endereco not in (0x47670a, 0x476968):
            return
        eax, edx = (cpu.reg_read(getattr(x86, 'UC_X86_REG_'+r)) for r in ('EAX', 'EDX'))
        self.celulas.append(('discover_cell' if endereco == 0x47670a else 'light_cell',
                             eax & 65535, edx & 255))

    def carregar_saida(self, mundo, tipos=None):
        super().carregar_saida(mundo, tipos)
        self.celulas = []

    def descobrir(self, celula, raio, dono):
        """0x476851: AX cell, DX radius (the body adds one), BL owner."""
        return self.executar(0x476851, INTERVALOS_DIRETOS, dict(EAX=celula, EDX=raio, EBX=dono),
                             parada=RETORNO, limite_instrucoes=1000000)

    def iluminar(self, celula, raio, dono):
        """0x476cb3: AX cell, DX radius, BL owner."""
        return self.executar(0x476cb3, INTERVALOS_DIRETOS, dict(EAX=celula, EDX=raio, EBX=dono),
                             parada=RETORNO, limite_instrucoes=1000000)
