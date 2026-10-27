"""Ordens e tarefas executadas com todas as chamadas originais, sem interceptação."""
import os
import random
import struct
import sys
import unittest
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from ordens_unidades import MundoUnidades, ContextoBusca
from tarefas_ia import MaquinaTarefas
from simbolos_ia import Instrucao, ler_rul
from test_tarefas_ia import programa


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialOrdens(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_ordens import BancadaOrdens
        cls.bancada = BancadaOrdens()

    def mundo(self, tipo, estado=7, indice=0, movendo=False, vinculo=0xffff):
        mundo = MundoUnidades()
        rng = random.Random(tipo * 1000 + estado * 800 + indice)
        u = bytearray(rng.randrange(256) for _ in range(276))
        u[0], u[1], u[2] = 3, tipo, estado
        u[0x86], u[0x87] = (254, 1) if movendo else (0, 0)
        struct.pack_into('<H', u, 8, 0x202)
        struct.pack_into('<H', u, 0x7c, 0x303)
        struct.pack_into('<H', u, 0xb8, vinculo)
        struct.pack_into('<H', u, 0xc0, 7 if tipo == 13 else 0xffff)
        mundo.escrever_unidade(indice, u)
        # Uma estrutura sentinela permite verificar os efeitos do construtor.
        mundo.estruturas[7 * 276:8 * 276] = bytes([0x5a]) * 276
        mundo.estruturas[7 * 276 + 0x76] = 15
        mundo.busca = ContextoBusca(indice, 1, 1, 0x12345678, 1)
        return mundo

    def conferir(self, mundo):
        self.assertEqual(self.bancada.conferir_mundo(mundo), [])

    def test_reset_ordem_todos_tipos_animacao_e_vinculo_estrutura(self):
        for tipo in range(26):
            for movendo in (False, True):
                for referencia in (0xffff, 7):
                    mundo = self.mundo(tipo, movendo=movendo)
                    mundo.palavra(0, 0xc0, referencia)
                    self.bancada.carregar_mundo(mundo)
                    mundo.redefinir_ordem(0)
                    self.bancada.chamar('ResetOrdre', (0,))
                    self.conferir(mundo)

    def test_movimento_todos_tipos_estados_caixas_e_busca(self):
        for tipo in range(26):
            for estado in (0, 4, 1, 2, 7):
                for objeto in (0, 0x36, 0x42):
                    mundo = self.mundo(tipo, estado, indice=799, movendo=estado % 2 == 0)
                    mundo.objetos[0x708] = objeto
                    if objeto == 0x42:
                        mundo.busca.unidade = 0  # Trabalho de outra unidade deve continuar intacto.
                    self.bancada.carregar_mundo(mundo)
                    self.assertEqual(mundo.mover_unidade(0x708, 799), self.bancada.chamar('V_DeplacerUnite', (0x708, 799)))
                    self.conferir(mundo)

    def test_todos_os_estados_e_truncamento_u16(self):
        for estado in range(256):
            mundo = self.mundo(0, estado, indice=3)
            self.bancada.carregar_mundo(mundo)
            self.assertEqual(mundo.mover_unidade(0x87654321, 0x12340003),
                             self.bancada.chamar('V_DeplacerUnite', (0x87654321, 0x12340003)))
            self.conferir(mundo)

    def test_construtor_condicoes_do_tuyau_e_limites_da_tabela(self):
        for estrutura in (0, 999):
            for tipo_estrutura in (0, 14, 15, 16):
                for flag in (0, 1, 255):
                    mundo = self.mundo(13)
                    mundo.palavra(0, 0xc0, estrutura)
                    mundo.estruturas[estrutura * 276 + 0x74] = 255
                    mundo.estruturas[estrutura * 276 + 0x75] = flag
                    mundo.estruturas[estrutura * 276 + 0x76] = tipo_estrutura
                    self.bancada.carregar_mundo(mundo)
                    mundo.mover_unidade(0x507, 0)
                    self.bancada.chamar('V_DeplacerUnite', (0x507, 0))
                    self.conferir(mundo)

    def test_ordens_aleatorias_preservam_restante_dos_registros(self):
        rng = random.Random(0x4457d3)
        for _ in range(256):
            tipo, estado, indice = rng.randrange(26), rng.randrange(256), rng.randrange(800)
            mundo = self.mundo(tipo, estado, indice=indice, movendo=bool(rng.randrange(2)))
            destino = rng.randrange(65536)
            mundo.objetos[destino] = rng.randrange(256)
            mundo.busca.unidade = rng.choice([indice, (indice + 1) % 800, 0xffff])
            self.bancada.carregar_mundo(mundo)
            mundo.definir_movimento(indice, destino)
            self.bancada.chamar('SetDeplaceEngin', (indice, destino))
            self.conferir(mundo)

    def test_grupo_vazio_misto_e_26_tipos(self):
        for grupo in (0, 99):
            for tamanho in (0, 1, 26):
                mundo = MundoUnidades()
                indices = list(range(799, 799 - tamanho, -1))
                for n, indice in enumerate(indices):
                    outro = self.mundo(n % 26, (0, 4, 1, 7, 1)[n % 5], indice=indice,
                                       vinculo=12 if n % 5 == 2 else 0xffff)
                    mundo.escrever_unidade(indice, outro.ler_unidade(indice))
                mundo.estruturas[7 * 276 + 0x74:7 * 276 + 0x77] = bytes([9, 1, 15])
                mundo.definir_grupo(grupo, indices)
                mundo.objetos[0x608] = 0x36
                mundo.busca = ContextoBusca(indices[-1] if indices else 0xffff, 1, 1, 123, 1)
                self.bancada.carregar_mundo(mundo)
                self.assertEqual(mundo.mover_grupo(grupo, 0x608), self.bancada.chamar('V_DeplaceGroupe', (grupo, 0x608)))
                self.conferir(mundo)

    def test_consultas_de_tipo_e_estado_sem_efeitos(self):
        for valor in range(256):
            mundo = self.mundo(valor, estado=valor)
            self.bancada.carregar_mundo(mundo)
            for nome in ('I_DonneTypeUnite', 'B_TestUniteFaitRien'):
                self.assertEqual(mundo.executar_operacao(nome, (0,)), self.bancada.chamar(nome, (0,)))
                self.conferir(mundo)

    def conferir_maquina(self, m):
        self.assertEqual(self.bancada.memoria_tarefas(), bytes(m.memoria))
        self.assertEqual(self.bancada.estado_listas(), dict(livres=m.livres, contextos=m.contextos, ativas=m.ativas))
        self.conferir(m.mundo)

    def test_tarefa_consulta_move_espera_e_conclui_sem_callbacks(self):
        ops = [Instrucao('I_DonneTypeUnite', 0x215, 5, 3, 0),
               Instrucao('B_TestUniteFaitRien', 0x210, 6, 3, 0),
               Instrucao('V_DeplacerUnite', 0x2120, 7, 3, 0),
               Instrucao('V_Attendre', 0x10, 1, 3, 2)]
        p = programa(ops)
        for tipo, estado in ((0, 7), (6, 7), (13, 7), (16, 7), (0, 4)):
            mundo = self.mundo(tipo, estado, indice=2)
            mundo.objetos[0x708] = 0x42
            self.bancada.carregar(p)
            self.bancada.carregar_mundo(mundo)
            m = MaquinaTarefas(p, mundo=mundo)
            self.assertEqual(m.postar(1, 1, (0x708, 2)), self.bancada.postar(1, 1, (0x708, 2)))
            self.conferir_maquina(m)
            for _ in range(4):
                self.assertEqual(m.atualizar(1), self.bancada.atualizar(1))
                self.conferir_maquina(m)

    def test_tarefa_de_grupo_sem_callbacks(self):
        p = programa([Instrucao('V_DeplaceGroupe', 0x2120, 1, 3, 0)])
        mundo = MundoUnidades()
        for indice, estado in ((1, 7), (2, 1), (3, 4)):
            mundo.escrever_unidade(indice, self.mundo(0, estado, indice=indice, vinculo=5).ler_unidade(indice))
        mundo.definir_grupo(3, [1, 2, 3])
        self.bancada.carregar(p)
        self.bancada.carregar_mundo(mundo)
        m = MaquinaTarefas(p, mundo=mundo)
        self.assertEqual(m.postar(2, 1, (3, 0x804)), self.bancada.postar(2, 1, (3, 0x804)))
        self.assertEqual(m.atualizar(2), self.bancada.atualizar(2))
        self.conferir_maquina(m)

    def test_instrucao_427_do_rule_original_com_estado_preparado(self):
        from bancada_tarefas import TAREFAS
        p = ler_rul((RAIZ.parent / 'source/cd/INSTALHD/RISING.RUL').read_bytes())
        mundo = self.mundo(0, 7, indice=2)
        self.bancada.carregar(p)
        self.bancada.carregar_mundo(mundo)
        m = MaquinaTarefas(p, mundo=mundo)
        indice = m.postar(0, 16, (2, 0, 0, 0x807))
        self.assertEqual(indice, self.bancada.postar(0, 16, (2, 0, 0, 0x807)))
        # O prefixo espacial 422..426 continua fora deste experimento. Inicia-se
        # na instrução real 427 com suas variáveis já preenchidas, sem alterar RUL.
        m.gravar(indice, 0xc, 427)
        self.bancada.cpu.mem_write(TAREFAS + indice * 96 + 0xc, struct.pack('<I', 427))
        self.assertEqual(m.atualizar(0), self.bancada.atualizar(0))
        self.conferir_maquina(m)
        self.assertEqual(mundo.palavra(2, 0x7e), 0x807)
