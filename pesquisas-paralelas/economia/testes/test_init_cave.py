"""Contagem dos 1000 registros, wrap u8, corpus ETA e atualização econômica."""
from collections import Counter
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from construcoes import (BASE_CONSTRUCOES, EconomiaConstrucoes, PASSO_CONSTRUCAO,
                         TOTAL_CONSTRUCOES)


def mundo():
    return EconomiaConstrucoes(estruturas=bytes(TOTAL_CONSTRUCOES * PASSO_CONSTRUCAO),
                               contagens_por_tipo=b'\xa5' * 88, contagens_tipo18=b'\x5a' * 4)


def definir(m, indice, dono=0, estado=1, tipo=3):
    o = indice * PASSO_CONSTRUCAO
    m.estruturas[o + 4] = dono
    m.estruturas[o + 5] = estado
    m.estruturas[o + 8] = tipo


def mundo_eta(arquivo):
    """Fixture de cópia direta dos prefixos de 204 bytes, não o MissionLoad inteiro."""
    dados = arquivo.read_bytes()
    if dados[:4] != b'V0.3':
        raise ValueError('ETA incompatível')
    quantidade, tamanho = struct.unpack_from('<HH', dados, 0x50030)
    if tamanho != 204:
        raise ValueError('Prefixo de estruturas diferente de 204 bytes')
    posicao = 0x50034
    m, registros = mundo(), []
    for _ in range(quantidade):
        indice = struct.unpack_from('<H', dados, posicao)[0]
        posicao += 2
        prefixo = dados[posicao:posicao + tamanho]
        posicao += tamanho
        if indice >= TOTAL_CONSTRUCOES or len(prefixo) != tamanho:
            raise ValueError('Registro de estrutura inválido')
        m.estruturas[indice * PASSO_CONSTRUCAO:indice * PASSO_CONSTRUCAO + tamanho] = prefixo
        registros.append((indice, prefixo))
    return m, registros


class ExemplosInitCave(unittest.TestCase):
    def test_conta_os_22_tipos_para_os_quatro_jogadores(self):
        m = mundo()
        for j in range(4):
            for tipo in range(22):
                definir(m, j * 22 + tipo, j, 1, tipo)
        m.inicializar_armazens()
        self.assertEqual(m.contagens_por_tipo, bytes([1] * 88))
        self.assertEqual(m.contagens_tipo18, bytes([1] * 4))
        self.assertEqual([m.capacidades.parametros(j)[0] for j in range(4)], [1] * 4)

    def test_qualquer_estado_nao_zero_conta_e_donos_externos_sao_ignorados(self):
        m = mundo()
        for i, estado in enumerate((1, 2, 4, 7, 255)):
            definir(m, i, estado=estado)
        definir(m, 5, estado=0, tipo=255)
        for i, dono in enumerate((4, 200, 255), 6):
            definir(m, i, dono, 1, 255)
        m.inicializar_armazens()
        self.assertEqual(m.capacidades.parametros(0)[0], 5)
        self.assertEqual(sum(m.contagens_por_tipo), 5)

    def test_wrap_255_256_257_e_1000_armazens(self):
        for quantidade in (255, 256, 257, 1000):
            with self.subTest(quantidade=quantidade):
                m = mundo()
                for i in range(quantidade):
                    definir(m, i)
                m.inicializar_armazens()
                self.assertEqual(m.capacidades.parametros(0)[0], quantidade & 255)

    def test_recontagem_limpa_contagens_antigas_e_preserva_demais_campos(self):
        m = mundo()
        m.capacidades.memoria[:] = b'\x93' * 24
        antes = bytes(m.estruturas), bytes(m.economia.memoria)
        m.inicializar_armazens()
        self.assertEqual(m.contagens_por_tipo, bytes(88))
        self.assertEqual(m.contagens_tipo18, bytes(4))
        for j in range(4):
            self.assertEqual(m.capacidades.memoria[j * 6:j * 6 + 6], b'\x00\x00' + b'\x93' * 4)
        self.assertEqual((bytes(m.estruturas), bytes(m.economia.memoria)), antes)

    def test_copia_tipo18_tambem_sofre_wrap_de_byte(self):
        m = mundo()
        for i in range(257):
            definir(m, i, 2, 1, 18)
        m.inicializar_armazens()
        self.assertEqual(m.contagens_tipo18, b'\x00\x00\x01\x00')
        self.assertEqual(m.capacidades.parametros(2)[0], 0)

    def test_nao_recalcula_indicador_nem_redefine_capacidade_unitaria(self):
        m = mundo()
        definir(m, 0)
        m.capacidades.configurar(0, 999, 0)
        m.capacidades.escrever_nivel(0, 77)
        m.inicializar_armazens()
        self.assertEqual(m.capacidades.parametros(0), (1, 0))
        self.assertEqual(m.capacidades.nivel(0), 77)
        with self.assertRaises(ZeroDivisionError):
            m.recalcular_recursos(0)

    def test_validacao_de_comprimento_e_tipo_ativo_antes_de_escrever(self):
        with self.assertRaises(ValueError):
            EconomiaConstrucoes().inicializar_armazens()
        m = mundo()
        definir(m, 0, tipo=22)
        antes = bytes(m.contagens_por_tipo), bytes(m.capacidades.memoria)
        with self.assertRaises(ValueError):
            m.inicializar_armazens()
        self.assertEqual((bytes(m.contagens_por_tipo), bytes(m.capacidades.memoria)), antes)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialInitCave(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_init_cave import BancadaInitCave
        cls.b = BancadaInitCave()

    def setUp(self):
        self.rng = random.Random(0x419112)

    def conferir(self, m):
        esperado = dict(economia=bytes(m.economia.memoria), capacidades=bytes(m.capacidades.memoria),
                        estruturas=bytes(m.estruturas), tipos=bytes(m.terreno.tipos),
                        quantidades=bytes(m.terreno.quantidades), semente=m.terreno.semente,
                        contagens_por_tipo=bytes(m.contagens_por_tipo), contagens_tipo18=bytes(m.contagens_tipo18))
        for campo, atual in self.b.estado().items():
            self.assertEqual(atual, esperado[campo], campo)
        self.assertEqual(self.b.guardas(), (b'\xa6' * 16, b'\x6a' * 16))
        self.assertEqual(self.b.guardas_contagens(), (b'\x8b' * 8, b'\x4d' * 4, b'\x9e' * 8))
        guardas = self.b.outras_guardas()
        self.assertEqual(guardas[:2], (b'\xc7' * 8, b'\x7c' * 8))
        self.assertEqual(guardas[-1], 0x12345678)

    def inicializar(self, m, registradores=None):
        self.b.carregar_mundo(m)
        m.inicializar_armazens()
        resultado = self.b.inicializar_armazens(registradores)
        self.conferir(m)
        self.assertEqual(self.b.chamadas, [])
        for nome in ('EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP'):
            self.assertEqual(resultado[nome], (registradores or {}).get(nome, 0))

    def test_32_tabelas_inteiras_com_estados_e_proprietarios_variados(self):
        for n in range(32):
            m = mundo()
            m.estruturas[:] = self.rng.randbytes(TOTAL_CONSTRUCOES * PASSO_CONSTRUCAO)
            m.economia.memoria[:] = self.rng.randbytes(128)
            m.capacidades.memoria[:] = self.rng.randbytes(24)
            m.contagens_por_tipo[:] = self.rng.randbytes(88)
            m.contagens_tipo18[:] = self.rng.randbytes(4)
            for i in range(TOTAL_CONSTRUCOES):
                dono = self.rng.choice((0, 1, 2, 3, 4, 200, 255))
                estado = self.rng.choice((0, 1, 2, 4, 255))
                tipo = self.rng.randrange(22) if dono < 4 and estado else self.rng.randrange(256)
                definir(m, i, dono, estado, tipo)
            regs = {nome: self.rng.getrandbits(32) for nome in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')}
            self.inicializar(m, regs)

    def test_16_limites_de_contagem_de_armazens_e_heliportos(self):
        for ordinal, quantidade in enumerate((0, 1, 255, 256, 257, 511, 512, 1000)):
            for tipo in (3, 18):
                m = mundo()
                dono = ordinal % 4
                for i in range(quantidade):
                    definir(m, i, dono, 255, tipo)
                self.inicializar(m)
                self.assertEqual(m.contagens_por_tipo[dono * 22 + tipo], quantidade & 255)

    def test_prefixos_de_estruturas_dos_38_mapas_eta(self):
        mapas = sorted((PASTA.parents[2] / 'source/cd/WORLD').glob('*.ETA'))
        self.assertEqual(len(mapas), 38)
        for arquivo in mapas:
            m, registros = mundo_eta(arquivo)
            self.inicializar(m)
            # Oracle do arquivo, separado da tabela em memória; o original conta 1000 slots.
            contagens = Counter((p[4], p[8]) for _, p in registros if p[5] and p[4] < 4)
            for j in range(4):
                self.assertEqual(m.capacidades.parametros(j)[0], contagens[j, 3] & 255)
                self.assertEqual(m.contagens_tipo18[j], contagens[j, 18] & 255)

    def test_integracao_contagem_recalculo_e_debito_24_chamadas(self):
        for quantidade in (0, 1, 2, 255, 256, 257, 511, 1000):
            m = mundo()
            for i in range(quantidade):
                definir(m, i)
            m.capacidades.configurar(0, 17, 100)
            m.capacidades.escrever_nivel(0, 123)
            m.economia.atribuir(0, 1, 50)
            m.economia.creditar(0, 1, 100)
            self.inicializar(m)
            m.recalcular_recursos(0)
            self.b.recalcular_recursos(0)
            self.conferir(m)
            m.retirar(0, 1, 40)
            self.b.retirar(0, 1, 40)
            self.conferir(m)
            if quantidade in (0, 256):
                self.assertEqual(m.capacidades.nivel(0), 123)

    def test_troca_de_dono_inativacao_e_reativacao_4_chamadas(self):
        m = mundo()
        definir(m, 0)
        self.inicializar(m)
        for dono, estado in ((1, 1), (1, 0), (3, 255)):
            definir(m, 0, dono, estado)
            self.b.cpu.mem_write(BASE_CONSTRUCOES + 4, bytes([dono, estado]))
            m.inicializar_armazens()
            self.b.inicializar_armazens()
            self.conferir(m)
            self.assertEqual(sum(m.contagens_por_tipo), int(estado != 0))


if __name__ == '__main__':
    unittest.main()
