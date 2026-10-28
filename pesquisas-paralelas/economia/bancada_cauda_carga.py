"""Original economy load tails on the Stage 15 shared-world harness."""
import hashlib
import struct

from bancada_habitaveis import BancadaHabitaveis
from casos_cauda_carga import MERCADO
from emulador import RETORNO

TABELA_ORDENS = 0x1800000
ORDENS = 0x1801000
GUARDADOS = 0x1804000
CONTAGENS = 0x49a070
TIPO18 = 0x4dfb4c
INTERVALOS_CAUDA = [
    (0x46c5a5, 0x46c5d8), (0x441459, 0x441470), (0x4411e1, 0x441459), (0x440d58, 0x440d5e),
    (0x418a93, 0x418ad3), (0x419112, 0x4191c9), (0x46df41, 0x46dfa0), (0x46dad6, 0x46dadb),
    (0x46027c, 0x4602cd), (0x46c969, 0x46c99a)]
# Guard bytes: before the counts (structures follow them directly), after the
# type-18 counts, around the order Bags and the stored players.
GUARDAS_CAUDA = ((CONTAGENS-8, 8), (TIPO18+4, 4), (ORDENS-8, 8), (ORDENS+10816, 8),
                 (GUARDADOS-8, 8), (GUARDADOS+80, 8))


class BancadaCaudaCarga(BancadaHabitaveis):
    intervalos = BancadaHabitaveis.intervalos + INTERVALOS_CAUDA

    def __init__(self):
        super().__init__()
        self.cpu.mem_map(TABELA_ORDENS, 0x10000)
        self.cpu.mem_write(0x4e19b8, struct.pack('<I', TABELA_ORDENS))
        self.cpu.mem_write(TABELA_ORDENS, struct.pack('<4I', *(ORDENS+j*2704 for j in range(4))))
        self.cpu.mem_write(0x5080ac, struct.pack('<I', GUARDADOS))
        self.entradas.update(tecnologia_cavernas=0, tecnologia_cavernas_nome=0, jogadores=0, mercado=0,
                             tecnologia_unidades=0, realizavel=0)

    def carregar(self, caso):
        super().carregar(caso)
        for base, n in GUARDAS_CAUDA:
            self.cpu.mem_write(base, bytes(((base >> 3)+i) & 255 | 0x21 for i in range(n)))
        self.cpu.mem_write(ORDENS, bytes(caso.ordens))
        self.cpu.mem_write(CONTAGENS, bytes(caso.mundo.realizaveis_estruturas))
        self.cpu.mem_write(TIPO18, bytes(caso.contagens_tipo18))
        self.cpu.mem_write(self.grades['jogadores'], bytes(caso.jogadores))
        self.cpu.mem_write(GUARDADOS, bytes(caso.jogadores_guardados))
        for nome, (base, _) in MERCADO.items():
            self.cpu.mem_write(base, bytes(caso.mercado[nome]))
        self.guardas_cauda = self.guardas_extra()

    def guardas_extra(self):
        return [bytes(self.cpu.mem_read(b, n)) for b, n in GUARDAS_CAUDA]

    def estado(self):
        e = super().estado()
        ler = lambda b, n: bytes(self.cpu.mem_read(b, n))
        e.update(ordens=ler(ORDENS, 10816), contagens=ler(CONTAGENS, 88), contagens_tipo18=ler(TIPO18, 4),
                 jogadores=ler(self.grades['jogadores'], 80), jogadores_guardados=ler(GUARDADOS, 80),
                 **{f'mercado_{n}': ler(b, t) for n, (b, t) in MERCADO.items()})
        return e

    def resumo(self):
        r = super().resumo()
        r['sha256'].update({k: hashlib.sha256(v).hexdigest() for k, v in self.estado().items()
                            if k.startswith('mercado_') or k in ('ordens', 'contagens', 'contagens_tipo18',
                                                                  'jogadores', 'jogadores_guardados')})
        r['sha256']['guardas_cauda_intactas'] = self.guardas_extra() == self.guardas_cauda
        return r

    def _fragmento(self, rotulo, inicio, fim):
        self.entradas[rotulo] += 1
        return self._resultado(rotulo, self.executar(inicio, self.intervalos, dict(EDI=0x5a5a5a5a),
                                                     parada=fim, limite_instrucoes=1000000))

    def cauda_tecnologia_cavernas(self):
        """MissionLoad 0x46c5af..0x46c5b9: EnginInitTechnologie then BatimentInitCave."""
        return self._fragmento('tecnologia_cavernas', 0x46c5af, 0x46c5b9)

    def cauda_nome_tecnologia_cavernas(self):
        """MissionLoadName 0x46c978..0x46c982: the same pair before RechercheCalculNew."""
        return self._fragmento('tecnologia_cavernas_nome', 0x46c978, 0x46c982)

    def cauda_jogadores(self):
        """MissionLoad 0x46c5be..0x46c5c3: PlayerRetrieve."""
        return self._fragmento('jogadores', 0x46c5be, 0x46c5c3)

    def cauda_mercado(self):
        """MissionLoad 0x46c5d1..0x46c5d6: MarcheResetAll."""
        return self._fragmento('mercado', 0x46c5d1, 0x46c5d6)

    def tecnologia_unidades(self, jogador):
        self.entradas['tecnologia_unidades'] += 1
        return self._resultado('tecnologia_unidades', self.executar(
            0x4411e1, self.intervalos, dict(EAX=jogador), limite_instrucoes=1000000))

    def estrutura_realizavel(self, jogador, tipo):
        self.entradas['realizavel'] += 1
        return self._resultado('realizavel', self.executar(
            0x418a93, self.intervalos, dict(EAX=jogador, EDX=tipo, EBX=0x13572468), limite_instrucoes=100000))
