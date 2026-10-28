"""Unpatched physical exit and joined recruitment-prefix native execution."""
from collections import Counter
from bisect import bisect_right
from bancada_avanco import BancadaAvanco
from bancada_experiencia_unidades import BancadaExperienciaUnidades
from bancada_posicao_saida import REGISTROS
from emulador import RETORNO, unicorn, x86


class BancadaColocacaoSaida(BancadaAvanco):
    intervalos = BancadaAvanco.intervalos + list(BancadaExperienciaUnidades.intervalos) + [
        (0x445fbc, 0x446189), (0x4431fb, 0x443203), (0x420f8a, 0x420f9e)]
    # Preserved-state resume points: SetMiniMap entry; subclasses may add loop heads.
    pontos_retomada = (0x46a388,)

    def __init__(self, segmentar=False):
        super().__init__()
        self.segmentar = segmentar
        self.retomadas_minimapa = 0
        self.retomadas_laco = 0
        self.entradas_originais = Counter()
        self.paradas_atingidas = Counter()
        self.efeitos = []
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._observar)

    def _observar(self, cpu, endereco, tamanho, _):
        if endereco in self.paradas or endereco not in (0x442cb4, 0x476851, 0x476cb3, 0x46a388, 0x4457d3):
            return
        eax, edx, ebx = (cpu.reg_read(getattr(x86, 'UC_X86_REG_'+r)) for r in ('EAX','EDX','EBX'))
        if endereco == 0x442cb4:
            self.efeitos.append(('collision', eax & 65535, edx & 65535))
        elif endereco in (0x476851, 0x476cb3):
            self.efeitos.append(('discovery' if endereco == 0x476851 else 'light',
                                eax & 65535, edx & 65535, ebx & 255))
        elif endereco == 0x46a388:
            self.efeitos.append(('minimap', eax & 255, ebx & 65535, edx & 255))
        elif endereco == 0x4457d3:
            self.efeitos.append(('move', eax & 65535, edx & 65535))

    def _executar_ate_parada(self, entrada, limite_instrucoes):
        # Preserve the exact declared interval union while avoiding a linear
        # scan through duplicate inherited ranges at every native instruction.
        uniao = []
        for inicio, fim in sorted(self.permitidos):
            if uniao and inicio < uniao[-1][1]:
                uniao[-1] = (uniao[-1][0], max(fim, uniao[-1][1]))
            else:
                uniao.append((inicio, fim))
        self._inicios = [a for a, b in uniao]
        self._fins = [b for a, b in uniao]
        finais = set(self.paradas)
        self.entradas_originais[hex(entrada)] += 1
        while True:
            self.instrucoes_atuais = 0
            self._pausa_minimapa = False
            try:
                regs = super()._executar_ate_parada(entrada, limite_instrucoes)
            except RuntimeError:
                self.ultima_falha = dict(eip=hex(self.cpu.reg_read(x86.UC_X86_REG_EIP)),
                                        instructions=self.instrucoes_atuais)
                raise
            self.maximo_instrucoes = max(getattr(self,'maximo_instrucoes',0), self.instrucoes_atuais)
            self.paradas_atingidas[hex(regs['EIP'])] += 1
            if not self._pausa_minimapa:
                return regs
            # Stop before a real SetMiniMap entry (or declared loop head), then
            # execute that same instruction with every register, flag and stack
            # byte preserved. No CALL/RET or native instruction is replaced.
            # Each resume counts separately.
            if regs['EIP'] == 0x46a388:
                self.retomadas_minimapa += 1
            else:
                self.retomadas_laco += 1
            self.execucoes += 1
            self.paradas = set(finais)
            entrada = regs['EIP']

    def _conferir_endereco(self, cpu, endereco, tamanho, _):
        self.instrucoes_atuais += 1
        if endereco in self.paradas:
            cpu.emu_stop()
            return
        if self.segmentar and endereco in self.pontos_retomada and self.instrucoes_atuais >= 50000:
            self._pausa_minimapa = True
            self.paradas.add(endereco)
            cpu.emu_stop()
            return
        i = bisect_right(self._inicios, endereco)-1
        if i < 0 or endereco+tamanho > self._fins[i]:
            raise RuntimeError(f'Execution outside declared original intervals: 0x{endereco:x}')

    def carregar_saida(self, mundo, tipos=None):
        self.carregar_fisica(mundo)
        if tipos is not None:
            self.cpu.mem_write(0x4965ae, bytes(tipos))
        self.cpu.mem_write(0x4e19c4, bytes(mundo.experiencias_unidades))
        self.cpu.mem_write(0x4dfba0, bytes(1872))
        self.efeitos = []

    def colocar(self, indice, celula, parada=RETORNO):
        return self.executar(0x445fbc, self.intervalos, dict(EAX=indice, EDX=celula),
                             parada=parada, limite_instrucoes=1000000)

    def retomar_colocacao(self, pedido, parada=0x420f9e):
        return self.executar(0x420f8a, self.intervalos,
                             dict(ESI=pedido.unidade, EDX=pedido.celula,
                                  EDI=REGISTROS+(pedido.indice & 65535)*276),
                             parada=parada, limite_instrucoes=1000000)

    def retomar_saida(self, pedido, parada=0x420f9e):
        return self.executar(0x420f5a, self.intervalos,
                             dict(EAX=pedido.indice, EBX=pedido.direcao, ESI=pedido.unidade,
                                  EDI=REGISTROS+(pedido.indice & 65535)*276),
                             parada=parada, limite_instrucoes=1000000)

    def conferir_saida(self, mundo):
        erros = self.conferir_fisica(mundo)
        if bytes(self.cpu.mem_read(0x4e19c4, 40)) != bytes(mundo.experiencias_unidades):
            erros.append(dict(region='experience_queue'))
        return erros
