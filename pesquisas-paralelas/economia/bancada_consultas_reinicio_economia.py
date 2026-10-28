"""Fresh direct native comparisons on the original-only capture inputs."""
import hashlib
from emulador import BancadaX86, RETORNO, unicorn
from casos_consultas_reinicio_economia import PESQUISA, ESTRUTURAS
from capturar_consultas_reinicio_economia_original import LIMITES, PADRAO_REGS


class BancadaConsultasReinicioEconomia(BancadaX86):
    def __init__(self):
        super().__init__()
        self.escritas = []
        self.retornos = 0
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._observar)

    def _observar(self, cpu, acesso, endereco, tamanho, valor, dados):
        if (PESQUISA-16 <= endereco < PESQUISA+80
                or ESTRUTURAS-16 <= endereco < ESTRUTURAS+276016):
            self.escritas.append(dict(endereco=hex(endereco), tamanho=tamanho, valor=valor))

    def carregar(self, caso):
        self.cpu.mem_write(PESQUISA-16, b'\xa6'*16+caso['pesquisa']+b'\x6a'*16)
        self.cpu.mem_write(ESTRUTURAS-16, b'\xc7'*16+caso['estruturas']+b'\x7c'*16)

    def estado(self):
        return dict(pesquisa=bytes(self.cpu.mem_read(PESQUISA, 64)).hex(),
                    estruturas_sha256=hashlib.sha256(bytes(self.cpu.mem_read(ESTRUTURAS, 276000))).hexdigest(),
                    guardas=[bytes(self.cpu.mem_read(a,n)).hex() for a,n in
                             ((PESQUISA-16,16),(PESQUISA+64,16),(ESTRUTURAS-16,16),(ESTRUTURAS+276000,16))])

    def chamar(self, chamada):
        self.escritas.clear()
        regs = self.executar(chamada['entrada'], list(LIMITES), dict(PADRAO_REGS, **chamada['regs']))
        self.retornos += regs['EIP'] == RETORNO
        return dict(entrada=hex(chamada['entrada']), entrada_regs=chamada['regs'],
                    saida_regs=regs, escritas=list(self.escritas), estado=self.estado())
