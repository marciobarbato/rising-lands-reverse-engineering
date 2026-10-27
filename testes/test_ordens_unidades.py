"""Propriedades observáveis das ordens e integração com o programa de tarefas."""
import struct
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ferramentas'))
from ordens_unidades import MundoUnidades, ContextoBusca
from tarefas_ia import MaquinaTarefas
from simbolos_ia import Instrucao
from test_tarefas_ia import programa


class OrdensUnidades(unittest.TestCase):
    def test_tarefa_move_unidade_de_outro_dono_sem_alterar_posicao(self):
        mundo = MundoUnidades()
        unidade = bytearray(276)
        unidade[0], unidade[1], unidade[2] = 3, 0, 7
        struct.pack_into('<H', unidade, 8, 0x102)
        struct.pack_into('<H', unidade, 0x7c, 0x102)
        mundo.escrever_unidade(2, unidade)
        m = MaquinaTarefas(programa([Instrucao('V_DeplacerUnite', 0x2120, 1, 3, 0)]), mundo=mundo)
        m.postar(0, 1, (0x608, 2))
        m.atualizar(0)
        self.assertEqual(mundo.palavra(2, 8), 0x102)
        self.assertEqual(mundo.palavra(2, 0x7e), 0x608)
        self.assertEqual(mundo.ler_unidade(2)[2], 2)
        self.assertEqual(mundo.ler_unidade(2)[0], 3)
        self.assertEqual(m.ativas, 0)

    def test_unidade_inativa_retorna_sucesso_sem_mudanca(self):
        mundo = MundoUnidades()
        antes = bytes(mundo.unidades)
        self.assertEqual(mundo.mover_unidade(0x100, 0), 1)
        self.assertEqual(bytes(mundo.unidades), antes)

    def test_libera_apenas_busca_da_mesma_unidade(self):
        mundo = MundoUnidades()
        mundo.unidades[2] = 7
        mundo.busca = ContextoBusca(1, 1, 1, 123, 1)
        mundo.mover_unidade(0x101, 0)
        self.assertEqual(mundo.busca, ContextoBusca(1, 1, 1, 123, 1))
        mundo.busca.unidade = 0
        mundo.mover_unidade(0x101, 0)
        self.assertEqual(mundo.busca, ContextoBusca(concluida=1))

    def test_mundo_ausente_nao_descarta_a_ordem(self):
        m = MaquinaTarefas(programa([Instrucao('V_DeplacerUnite', 0x2120, 1, 3, 0)]))
        m.postar(0, 1, (0x101, 0))
        with self.assertRaises(NotImplementedError): m.atualizar(0)

    def test_grupo_preserva_vinculo_em_estado_1(self):
        mundo = MundoUnidades()
        for i in range(3):
            mundo.unidades[i * 276 + 2] = 1
            mundo.palavra(i, 0xb8, 12 if i == 1 else 0xffff)
        mundo.definir_grupo(0, [0, 1, 2])
        antes = mundo.ler_unidade(1)
        mundo.mover_grupo(0, 0x505)
        self.assertEqual(mundo.ler_unidade(1), antes)
        self.assertEqual(mundo.palavra(0, 0x7e), 0x505)
        self.assertEqual(mundo.palavra(2, 0x7e), 0x505)
