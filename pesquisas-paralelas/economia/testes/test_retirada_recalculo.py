"""Débito e recálculo: memória inteira, argumentos, bordas e exceções do x86."""
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from construcoes import EconomiaConstrucoes


def saldo(mundo, jogador, recurso, rmi, total):
    """Prepara também estados inconsistentes; não executa uma regra econômica."""
    struct.pack_into('<HH', mundo.economia.memoria, jogador * 32 + recurso * 8, rmi, total)


class ExemplosRetiradaRecalculo(unittest.TestCase):
    def test_retirada_reduz_rmi_e_total_antes_de_atualizar_nivel(self):
        m = EconomiaConstrucoes()
        m.capacidades.configurar(0, 1, 100)
        saldo(m, 0, 1, 100, 140)
        m.retirar(0, 1, 80)
        self.assertEqual((m.economia.consultar_rmi(0).comida, m.economia.consultar(0).comida), (20, 60))
        self.assertEqual(m.capacidades.nivel(0), 2)
        m.retirar(0, 1, 30)
        self.assertEqual((m.economia.consultar_rmi(0).comida, m.economia.consultar(0).comida), (0, 30))
        self.assertEqual(m.capacidades.nivel(0), 2)
        m.retirar(0, 1, 1000)
        self.assertEqual(m.economia.consultar(0).comida, 0)
        self.assertEqual(m.capacidades.nivel(0), 0)

    def test_sem_armazem_preserva_indicador_mas_nao_evitaria_debito(self):
        m = EconomiaConstrucoes()
        m.capacidades.configurar(0, 0, 0)
        m.capacidades.escrever_nivel(0, 99)
        saldo(m, 0, 1, 40, 60)
        m.retirar(0, 1, 10)
        self.assertEqual((m.economia.consultar_rmi(0).comida, m.economia.consultar(0).comida), (30, 50))
        self.assertEqual(m.capacidades.nivel(0), 99)
        m.recalcular_recursos(0)
        self.assertEqual(m.capacidades.nivel(0), 99)

    def test_recalculo_nao_muda_saldos_e_nao_limita_nivel_em_sete(self):
        m = EconomiaConstrucoes()
        m.capacidades.configurar(0, 1, 1)
        saldo(m, 0, 1, 0, 65535)
        antes = bytes(m.economia.memoria)
        m.recalcular_recursos(0)
        self.assertEqual(m.economia.memoria, antes)
        self.assertEqual(m.capacidades.nivel(0), 249)  # (65535 * 7) & 255.

    def test_duas_divisoes_e_soma_de_estoque_u16(self):
        m = EconomiaConstrucoes()
        m.capacidades.configurar(0, 2, 100)
        saldo(m, 0, 1, 0, 29)
        m.recalcular_recursos(0)
        self.assertEqual(m.capacidades.nivel(0), 0)  # (29//2 * 7)//100; 29*7//200 daria 1.
        saldo(m, 0, 1, 0, 65535)
        saldo(m, 0, 2, 0, 10)
        m.recalcular_recursos(0)
        self.assertEqual(m.capacidades.nivel(0), 0)  # Numerador = 9, não 65545.

    def test_debito_de_pecas_recalcula_somente_comida_e_pedra(self):
        m = EconomiaConstrucoes()
        m.capacidades.configurar(0, 1, 100)
        saldo(m, 0, 1, 0, 30)
        saldo(m, 0, 2, 0, 20)
        saldo(m, 0, 0, 0, 100)
        m.retirar(0, 0, 10)
        self.assertEqual(m.economia.consultar(0).pecas, 90)
        self.assertEqual(m.capacidades.nivel(0), 3)

    def test_jogador_invalido_do_recalculo_e_noop_apos_truncar_al(self):
        m = EconomiaConstrucoes()
        antes = bytes(m.capacidades.memoria)
        for j in (4, 255, -1, 0x104):
            self.assertIsNone(m.recalcular_recursos(j))
            self.assertEqual(m.capacidades.memoria, antes)
        m.capacidades.configurar(0, 1, 100)
        saldo(m, 0, 1, 0, 100)
        m.recalcular_recursos(0x100)
        self.assertEqual(m.capacidades.nivel(0), 7)

    def test_divisao_zero_preserva_debito_ja_feito(self):
        for retirar in (False, True):
            with self.subTest(retirar=retirar):
                m = EconomiaConstrucoes()
                m.capacidades.configurar(0, 1, 0)
                m.capacidades.escrever_nivel(0, 89)
                saldo(m, 0, 1, 100, 150)
                with self.assertRaises(ZeroDivisionError):
                    if retirar:
                        m.retirar(0, 1, 80)
                    else:
                        m.recalcular_recursos(0)
                self.assertEqual((m.economia.consultar_rmi(0).comida, m.economia.consultar(0).comida),
                                 (20, 70) if retirar else (100, 150))
                self.assertEqual(m.capacidades.nivel(0), 89)

    def test_retirada_trunca_bl_al_dx_e_rejeita_indices_inseguros(self):
        m = EconomiaConstrucoes()
        saldo(m, 1, 2, 20, 30)
        m.retirar(0x101, 0x102, 0x1000a)
        self.assertEqual(m.economia.consultar(1).pedra, 20)
        with self.assertRaises(ValueError):
            m.retirar(4, 1, 0)
        with self.assertRaises(ValueError):
            m.retirar(0, 4, 0)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialRetiradaRecalculo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_construcoes import BancadaConstrucoes
        cls.b = BancadaConstrucoes()

    def setUp(self):
        self.rng = random.Random(0x4235bd)
        self.b.sujeira_pilha = None

    def estado(self, n):
        m = EconomiaConstrucoes(estruturas=bytes(self.rng.getrandbits(8) for _ in range(4 * 276)))
        m.economia.memoria[:] = bytes(self.rng.getrandbits(8) for _ in range(128))
        m.capacidades.memoria[:] = bytes(self.rng.getrandbits(8) for _ in range(24))
        j = n % 4
        armazens = (0, 1, 2, 255, 256, 65535, self.rng.randrange(1, 65536))[n % 7]
        capacidade = (1, 2, 3, 100, 65535, self.rng.randrange(1, 65536))[n % 6]
        m.capacidades.configurar(j, armazens, 0 if armazens == 0 else capacidade)
        m.terreno.tipos[:] = b'\xa5' * 65536
        m.terreno.quantidades[:] = b'\x5a' * 65536
        m.terreno.semente = self.rng.randrange(0x80000000)
        return m

    def conferir(self, m):
        esperado = dict(economia=bytes(m.economia.memoria), capacidades=bytes(m.capacidades.memoria),
                        estruturas=bytes(m.estruturas), tipos=bytes(m.terreno.tipos),
                        quantidades=bytes(m.terreno.quantidades), semente=m.terreno.semente)
        for campo, atual in self.b.estado().items():
            self.assertEqual(atual, esperado[campo], campo)
        self.assertEqual(self.b.guardas(), (b'\xa6' * 16, b'\x6a' * 16))
        self.assertEqual(self.b.outras_guardas(), (b'\xc7' * 8, b'\x7c' * 8, b'\xe9' * 8, b'\x9e' * 8, 0x12345678))

    def conferir_consulta(self, j, esperada):
        consultas = [c for c in self.b.chamadas if c['entrada'] == 0x46769d]
        self.assertEqual([c['jogador_pilha'] for c in consultas], [j] if esperada else [])

    def test_recalculo_1024_estados_e_pilha_suja(self):
        for n in range(1024):
            m = self.estado(n)
            j = n % 4 | self.rng.getrandbits(24) << 8
            self.b.sujeira_pilha = (None, 0xa5, 0xff, 0x42)[n % 4]
            self.b.carregar_mundo(m)
            m.recalcular_recursos(j)
            self.b.recalcular_recursos(j)
            self.conferir(m)
            self.conferir_consulta(j & 255, m.capacidades.parametros(j)[0] != 0)
            self.assertFalse(any(c['entrada'] == 0x46792c for c in self.b.chamadas))

    def test_retirada_1024_estados_e_argumentos_truncados(self):
        for n in range(1024):
            m = self.estado(n)
            j = n % 4 | self.rng.getrandbits(24) << 8
            r = n // 4 % 4 | self.rng.getrandbits(24) << 8
            q = self.rng.getrandbits(32)
            self.b.sujeira_pilha = (None, 0xa5, 0xff, 0x42)[n % 4]
            self.b.carregar_mundo(m)
            m.retirar(j, r, q)
            self.b.retirar(j, r, q)
            self.conferir(m)
            self.conferir_consulta(j & 255, m.capacidades.parametros(j)[0] != 0)
            debitos = [c for c in self.b.chamadas if c['entrada'] == 0x46792c]
            self.assertEqual([(c['EAX'], c['EDX'], c['EBX']) for c in debitos],
                             [(r & 255, q & 65535, j & 255)])

    def test_recalculo_252_jogadores_invalidos_nao_le_tabelas(self):
        for j in range(4, 256):
            m = self.estado(j)
            argumento = j | self.rng.getrandbits(24) << 8
            self.b.carregar_mundo(m)
            m.recalcular_recursos(argumento)
            self.b.recalcular_recursos(argumento)
            self.conferir(m)
            self.assertEqual(self.b.chamadas, [])

    def test_limites_numericos_168_chamadas(self):
        for armazens in (1, 2, 3, 65535):
            for capacidade in (1, 100, 65535):
                for estoque in (0, 1, 29, 100, 9999, 32768, 65535):
                    m = EconomiaConstrucoes()
                    m.capacidades.configurar(0, armazens, capacidade)
                    saldo(m, 0, 1, 0, estoque)
                    saldo(m, 0, 2, 65535, 10)  # Underflow independente no estoque de pedra.
                    self.b.carregar_mundo(m)
                    m.recalcular_recursos(0)
                    self.b.recalcular_recursos(0)
                    self.conferir(m)
                    m.retirar(0, 1, 1)
                    self.b.retirar(0, 1, 1)
                    self.conferir(m)

    def test_sequencia_deposito_retirada_recalculo_384_chamadas(self):
        m = EconomiaConstrucoes()
        m.estruturas[8] = 8  # Tipo sem depósito de excedente; não envolve unidades.
        for j in range(4):
            m.capacidades.configurar(j, 2, 100)
            m.economia.atribuir(j, 1, 100)
            m.economia.atribuir(j, 2, 50)
        self.b.carregar_mundo(m)
        for n in range(128):
            j, r = n % 4, n % 3
            entrada, saida = self.rng.randrange(250), self.rng.randrange(250)
            m.adicionar(j, r, entrada, 0)
            self.b.adicionar(j, r, entrada, 0)
            self.conferir(m)
            m.retirar(j, r, saida)
            self.b.retirar(j, r, saida)
            self.conferir(m)
            m.recalcular_recursos(j)
            self.b.recalcular_recursos(j)
            self.conferir(m)

    def test_divisao_zero_16_excecoes_e_ordem_dos_efeitos(self):
        from bancada_construcoes import BancadaConstrucoes, x86, unicorn
        for retirar in (False, True):
            for n in range(8):
                anterior = self.b
                type(self).b = BancadaConstrucoes()
                self.b.execucoes = anterior.execucoes
                self.b.excecoes_esperadas = anterior.excecoes_esperadas
                self.b.limites_esperados = anterior.limites_esperados
                m = EconomiaConstrucoes()
                j = n % 4
                m.capacidades.configurar(j, 1 + n % 3, 0)
                m.capacidades.escrever_nivel(j, 89)
                saldo(m, j, 1, 100, 150)
                self.b.carregar_mundo(m)
                with self.assertRaises(ZeroDivisionError):
                    if retirar:
                        m.retirar(j, 1, 80)
                    else:
                        m.recalcular_recursos(j)
                with self.assertRaises(unicorn.UcError) as ctx:
                    if retirar:
                        self.b.retirar(j, 1, 80)
                    else:
                        self.b.recalcular_recursos(j)
                self.assertEqual(ctx.exception.errno, unicorn.UC_ERR_EXCEPTION)
                self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_EIP), 0x423635 if retirar else 0x4233cb)
                self.b.excecoes_esperadas += 1
                self.conferir(m)
                self.assertEqual((m.economia.consultar_rmi(j).comida, m.economia.consultar(j).comida),
                                 (20, 70) if retirar else (100, 150))


if __name__ == '__main__':
    unittest.main()
