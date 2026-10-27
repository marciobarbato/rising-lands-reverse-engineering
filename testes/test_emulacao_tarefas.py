"""Comparação da máquina com funções originais, incluindo todas as chamadas usadas."""
import os
import random
import struct
import sys
import unittest
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from tarefas_ia import MaquinaTarefas, u32
from simbolos_ia import Instrucao, ler_rul
from test_tarefas_ia import programa


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialTarefas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_tarefas import BancadaTarefas
        cls.bancada = BancadaTarefas()

    def conferir(self, maquina):
        self.assertEqual(self.bancada.memoria_tarefas(), bytes(maquina.memoria))
        self.assertEqual(self.bancada.estado_listas(), dict(livres=maquina.livres, contextos=maquina.contextos, ativas=maquina.ativas))

    def iniciar(self, p):
        self.bancada.carregar(p)
        m = MaquinaTarefas(p)
        self.conferir(m)
        return m

    def postar(self, m, jogador, tipo, argumentos=()):
        i = m.postar(jogador, tipo, argumentos)
        self.assertEqual(self.bancada.postar(jogador, tipo, argumentos), i)
        self.conferir(m)
        return i

    def atualizar(self, m, jogador):
        esperado = m.atualizar(jogador)
        self.assertEqual(self.bancada.atualizar(jogador), esperado)
        self.conferir(m)

    def test_espera_criacao_conclusao_e_reutilizacao(self):
        for tempo in (0, 1, 2, 20, 0xffffffff, 0x80000000):
            m = self.iniciar(programa([Instrucao('V_Attendre', 0x111, 1, 3, 0)]))
            self.postar(m, 2, 1, (tempo, 123))
            for _ in range(24): self.atualizar(m, 2)
            self.postar(m, 2, 1, (1, 456))
            for _ in range(3): self.atualizar(m, 2)

    def test_reservatorio_100_e_jogadores(self):
        m = self.iniciar(programa([Instrucao('B_Bidon', 0, 1, 3, 0)]))
        for i in range(101): self.postar(m, i % 5, 1, (i,))
        for j in range(5): self.atualizar(m, j)
        self.assertEqual(m.ativas, 0)
        self.assertEqual(m.livres[1], 100)
        for i in range(10): self.postar(m, 4, 1)
        self.atualizar(m, 4)

    def test_subtarefa_suspende_pai_e_propaga_resultado(self):
        for resultado_filho in (1, 2, 3):
            ops = [Instrucao(2, 0x110, 5, 6, 0), Instrucao('I_Affecte', 0x12, 1, 3, 111),
                   Instrucao('I_Affecte', 0x12, 1, 3, 222), Instrucao('V_Attendre', 0x110, resultado_filho, 3, 0)]
            m = self.iniciar(programa(ops, (0, 4, 7)))
            pai = self.postar(m, 0, 1, (2,))
            for _ in range(7): self.atualizar(m, 0)
            self.assertEqual(m.ativas, 0)
            # Caso 3 preserva o retorno anterior (zero na memória inicial).
            self.assertEqual(m.ler(pai, 0x1c), 222 if resultado_filho == 2 else 111)

    def test_tipo_invalido_e_subtarefa_sem_entrada(self):
        m = self.iniciar(programa([Instrucao(2, 0, 1, 3, 0)], (0, 4, 0)))
        for tipo in (0, 2, 63, 64): self.postar(m, 1, tipo)
        self.postar(m, 1, 1)
        self.atualizar(m, 1)

    def test_operacoes_aritmeticas_com_sinal_e_truncamento(self):
        rng = random.Random(0x481280)
        nomes = ('B_Egalite', 'B_Superieur', 'I_Addition', 'I_Soustraction', 'I_PourcentageAB', 'I_Divise')
        casos = [(50, 100), (100, 50), (0, 0), (0xffffffff, 2), (0x7fffffff, 2), (0x80000000, 1)]
        casos += [(rng.getrandbits(32), rng.getrandbits(32)) for _ in range(64)]
        for nome in nomes:
            for a, b in casos:
                if nome == 'I_PourcentageAB' and b == 0: continue
                m = self.iniciar(programa([Instrucao(nome, 0x2123, 1, 2, 0)]))
                self.postar(m, 0, 1, (a, b))
                self.atualizar(m, 0)

    def test_regra_14_do_arquivo_original(self):
        p = ler_rul((RAIZ.parent / 'source/cd/INSTALHD/RISING.RUL').read_bytes())
        m = self.iniciar(p)
        self.postar(m, 0, 14)
        self.atualizar(m, 0)
        self.assertEqual(m.ativas, 0)

    def test_missao_aliases_constantes_e_valor_zero(self):
        for nome in ('I_NumMission', 'I_Affecte', 'B_AccessibiliteChemin', 'B_AccessibiliteBatiment',
                     'B_GicleUniteAmieDeZone', 'B_TestUniteAmieSurZone', 'B_TestUniteEnnemieSurZone'):
            for missao in (0, 13, 255, 256):
                p = programa([Instrucao(nome, 0x11, 1, 2, 0)])
                self.bancada.carregar(p, missao)
                m = MaquinaTarefas(p, missao=missao)
                self.postar(m, 1, 1)
                self.atualizar(m, 1)

    def test_resolucao_nativa_dos_140_nomes(self):
        from simbolos_ia import ler_sbl, enderecar_simbolos
        simbolos = ler_sbl((RAIZ.parent / 'source/cd/INSTALHD/RISING.SBL').read_bytes())
        base, nomes = enderecar_simbolos(simbolos)
        por_nome = {}
        for s in simbolos: por_nome.setdefault(s.nome, s)
        endereco = 0x1200000
        self.bancada.cpu.mem_map(endereco, 0x1000)
        self.bancada.cpu.mem_write(0x522234, struct.pack('<I', endereco))
        # Uma entrada real por vez mantém o teste sob 20.000 instruções.
        def tabela(nome):
            s = por_nome[nome]
            dados = struct.pack('<4I', s.deslocamento, 16, 0xffffffff, 0) + nome.encode('cp1252') + b' \0'
            self.bancada.cpu.mem_write(endereco, dados)
        tabela('_debugGetPC')
        self.bancada.executar(0x48d74b, [(0x48d74b, 0x48d78d), (0x48d4c0, 0x48d561)])
        self.assertEqual(struct.unpack('<I', self.bancada.cpu.mem_read(0x522238, 4))[0], base)
        p = ler_rul((RAIZ.parent / 'source/cd/INSTALHD/RISING.RUL').read_bytes())
        for nome in sorted({op.operacao for op in p.instrucoes if isinstance(op.operacao, str)}):
            tabela(nome)
            self.bancada.cpu.mem_write(endereco + 0x200, nome.encode('cp1252') + b'\0')
            r = self.bancada.executar(0x48d6fe, [(0x48d6fe, 0x48d74b), (0x48d78d, 0x48d7f4),
                                              (0x48ff83, 0x490041)], dict(EAX=endereco + 0x200))
            self.assertEqual(r['EAX'], nomes[nome])
