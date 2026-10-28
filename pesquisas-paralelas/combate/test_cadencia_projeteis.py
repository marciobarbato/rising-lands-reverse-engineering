"""Compara portões e apresentação isolada com instruções x86 originais."""
import os
import random
import sys
import unittest
from pathlib import Path

from cadencia_projeteis import (continuar_apos_menu, continuar_apos_evento,
    permitir_bloco_projeteis, preparar_apresentacao_impacto)
from maquina_projeteis import MaquinaProjeteis
from projeteis import PoolProjeteis

# Reutilização somente leitura: não duplicar os contadores já reconstruídos.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'ferramentas'))
from cadencia import avancar_contadores, deve_desenhar


class ContratosCadenciaProjeteis(unittest.TestCase):
    def test_portoes_sao_locais_e_releem_estado(self):
        self.assertTrue(continuar_apos_menu(16, 18, 1))
        self.assertFalse(continuar_apos_menu(18, 18, 1))
        self.assertFalse(continuar_apos_menu(16, 18, 0))
        self.assertTrue(permitir_bloco_projeteis(18, 0))
        self.assertTrue(permitir_bloco_projeteis(16, 255))
        self.assertFalse(permitir_bloco_projeteis(16, 0))
        self.assertFalse(permitir_bloco_projeteis(22, 255))
        self.assertTrue(continuar_apos_evento(0))
        self.assertFalse(continuar_apos_evento(128))

    def test_impacto_zero_nao_consulta_tabela(self):
        r = preparar_apresentacao_impacto(0, 255, 2, None, 640, 0, 20, 15)
        self.assertEqual((r.campo_4dfb44, r.indice_4e1d18, r.deslocamento_y), (0, 255, 0))
        self.assertEqual(r.retangulo_origem, (0, 0, 640, 480))
        with self.assertRaises(NotImplementedError):
            preparar_apresentacao_impacto(1, 0, 0, None, 640, 0, 20, 15)

    def test_modulo_usa_valor_anterior_ao_decremento(self):
        r = preparar_apresentacao_impacto(15, 255, 2, bytes([29] * 256), 640, 0, 20, 15)
        self.assertEqual((r.campo_4dfb44, r.indice_4e1d18, r.deslocamento_y), (14, 0, 14))
        self.assertEqual(r.retangulo_origem, (0, 14, 640, 480))

    def test_geometria_preserva_byte_alto_assinado(self):
        r = preparar_apresentacao_impacto(0, 0, 0, None, 800, 0xffabcdef, 25, 19)
        self.assertEqual(r.retangulo_origem, (-32, -32, 832, 640))
        r = preparar_apresentacao_impacto(0, 0, 0, None, 801, 0xffabcdef, 25, 19)
        self.assertEqual(r.retangulo_origem, (0, 0, 800, 608))

    def test_decremento_por_apresentacao_e_paridade(self):
        campo, indice = 3, 0
        for ciclo in (1, 3, 5, 7):
            r = preparar_apresentacao_impacto(campo, indice, ciclo, bytes(256), 640, 0, 20, 15)
            campo, indice = r.campo_4dfb44, r.indice_4e1d18
        self.assertEqual((campo, indice), (3, 4))
        for _ in range(3):
            r = preparar_apresentacao_impacto(campo, indice, 8, bytes(256), 640, 0, 20, 15)
            campo, indice = r.campo_4dfb44, r.indice_4e1d18
        self.assertEqual((campo, indice), (0, 7))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Opcional: RISING_EMULAR=1')
class DiferencialCadenciaProjeteis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_cadencia_projeteis import BancadaCadenciaProjeteis
        cls.b = BancadaCadenciaProjeteis()

    def test_portoes_bytes_e_estado_salvo(self):
        for estado in range(256):
            self.assertEqual(self.b.portao_evento(estado), continuar_apos_evento(estado))
            for flag in (0, 1, 2, 255):
                self.assertEqual(self.b.portao_bloco(estado, flag), permitir_bloco_projeteis(estado, flag))
                for entrada in (16, 18, 255):
                    self.assertEqual(self.b.portao_menu(entrada, estado, flag),
                                     continuar_apos_menu(entrada, estado, flag))
            for atual in (16, 18):
                for flag in (0, 1):
                    self.assertEqual(self.b.portao_menu(estado, atual, flag),
                                     continuar_apos_menu(estado, atual, flag))

    def test_apresentacao_modulo_e_indice_todos_bytes(self):
        for campo in range(256):
            for valor in (0, 1, 15, 20, 127, 255):
                tabela = bytes([valor] * 256)
                for ciclo in (0, 1, 254, 255):
                    for indice in (0, 255):
                        self.b.contexto_apresentacao(campo, indice, ciclo, tabela)
                        self.assertEqual(self.b.preparar_apresentacao(),
                            preparar_apresentacao_impacto(campo, indice, ciclo, tabela, 640, 0, 20, 15))
                        self.assertEqual(bytes(self.b.cpu.mem_read(0x4e1c18, 256)), tabela)

    def test_retangulo_leitura_desalinhada_e_extremos(self):
        rng = random.Random(0x43f14f)
        tabela = rng.randbytes(256)
        for alto in range(256):
            bruto = (alto << 24) | rng.getrandbits(24)
            for largura in (640, 800, 801):
                for campo in (0, 15):
                    dimensoes = rng.choice(((0, 0), (20, 15), (25, 19), (65535, 65535)))
                    self.b.contexto_apresentacao(campo, alto, 2, tabela, largura, bruto, *dimensoes)
                    self.assertEqual(self.b.preparar_apresentacao(),
                        preparar_apresentacao_impacto(campo, alto, 2, tabela, largura, bruto, *dimensoes))

    def test_contador_global_alimenta_calcul_antes_unidades(self):
        for inicial in (0, 1, 254, 255, 0xfffffffe, 0xffffffff):
            pool = PoolProjeteis(bytearray(5600))
            pool.definir(37, 2, 0, 0xffff, 1, 7, 3, 16, 16, 0)
            pool.registro(37)[0x19] = 0
            pool.registro(0)[0], pool.registro(99)[0] = 1, 20
            m = MaquinaProjeteis(pool)
            self.b.pool(pool.memoria)
            contadores = (inicial, 0xffffffff, 0xfffffffe)
            self.b.contadores(*contadores)
            for _ in range(4):
                contadores = avancar_contadores(*contadores)
                self.assertEqual(self.b.incrementar_contadores(), contadores)
                r = self.b.calcular_no_chamador()
                self.assertEqual(r['EIP'], 0x42d3f5)
                m.calcular(contadores[0] & 255)
                self.assertEqual(self.b.ler_pool(), pool.memoria)
            if inicial == 0:
                self.assertEqual((pool.registro(0)[0x18], pool.registro(99)[0x18]), (2, 2))

    def test_impacto30_ate_preparacao_apresentacao(self):
        from test_maquina_projeteis import modelo
        m = modelo(bytearray([1] * 5600))
        m.pool.definir(37, 30, 0, 0, 1, 7, 3, 16, 16, 0)
        m.pool.registro(37)[0x18] = 12
        self.b.pool(m.pool.memoria)
        self.b.contexto_maquina(campo=173)
        self.b.avancar_completo(37)
        valores = iter(self.b.resultados_random)
        m.aleatorio = lambda _: next(valores)
        m.avancar(37)
        self.assertEqual(list(valores), [])
        self.assertEqual(self.b.ler_pool(), m.pool.memoria)
        self.assertEqual((self.b.campo_tipo30(), m.campo_4dfb44), (15, 15))
        tabela = bytes(range(256))
        self.b.contexto_apresentacao(self.b.campo_tipo30(), 254, 2, tabela, 800, 0x01000000, 25, 19)
        r = preparar_apresentacao_impacto(m.campo_4dfb44, 254, 2, tabela, 800, 0x01000000, 25, 19)
        self.assertEqual(self.b.preparar_apresentacao(), r)
        self.assertEqual((r.campo_4dfb44, r.deslocamento_y), (14, 14))

    def test_apresentacoes_encadeadas_paridade_e_divisor(self):
        tabela = bytes((i * 31 + 7) & 255 for i in range(256))
        for divisor in (1, 2, 3, 4):
            campo, indice, contadores = 15, 255, (0, 0, 0)
            self.b.contexto_apresentacao(campo, indice, 0, tabela)
            self.b.contadores(*contadores)
            for _ in range(120):
                contadores = avancar_contadores(*contadores)
                self.assertEqual(self.b.incrementar_contadores(), contadores)
                if deve_desenhar(contadores[0], divisor):
                    r = preparar_apresentacao_impacto(campo, indice, contadores[0], tabela, 640, 0, 20, 15)
                    self.assertEqual(self.b.preparar_apresentacao(), r)
                    campo, indice = r.campo_4dfb44, r.indice_4e1d18
                self.assertEqual(self.b.campo_tipo30(), campo)
                self.assertEqual(self.b.cpu.mem_read(0x4e1d18, 1)[0], indice)


if __name__ == '__main__':
    unittest.main()
