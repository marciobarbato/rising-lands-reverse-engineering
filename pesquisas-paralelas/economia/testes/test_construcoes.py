"""Capacidade/excedentes com memória inteira e sacolas comparadas ao original."""
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from construcoes import (Capacidades, EconomiaConstrucoes, LimiteDeposito, RetiradaColonoPendente,
                         TerrenoSacolas)


def mundo(tipo=3, posicao=0x2020, armazens=1, capacidade=100):
    m = EconomiaConstrucoes(estruturas=bytes(8 * 276))
    m.estruturas[8] = tipo
    struct.pack_into('<H', m.estruturas, 2, posicao)
    m.capacidades.configurar(0, armazens, capacidade)
    return m


class ExemplosConstrucoes(unittest.TestCase):
    def test_capacidade_compartilhada_comida_e_pedra(self):
        m = mundo()
        m.economia.atribuir(0, 1, 100)
        m.economia.creditar(0, 1, 60)
        m.economia.creditar(0, 2, 30)
        resultado = m.adicionar(0, 1, 20, 0)
        self.assertEqual((resultado.credito_enviado, resultado.excedente), (10, 10))
        self.assertEqual(m.economia.consultar(0).comida, 170)
        self.assertEqual(m.economia.consultar_rmi(0).comida, 100)
        self.assertEqual(m.capacidades.nivel(0), 7)
        self.assertEqual(m.terreno.tipos[0x2222], 0x43)
        self.assertEqual(m.terreno.quantidades[0x2222], 10)

    def test_sem_armazem_e_tipo_sem_destino_descarta(self):
        m = mundo(tipo=8, armazens=0)
        m.capacidades.escrever_nivel(0, 99)
        r = m.adicionar(0, 1, 12, 0)
        self.assertEqual((r.credito_enviado, r.excedente, r.descartado), (0, 12, True))
        self.assertEqual(m.capacidades.nivel(0), 99)
        self.assertEqual(sum(m.terreno.quantidades), 0)

    def test_destinos_dos_tipos_2_e_3_e_wrap(self):
        for tipo, recurso, esperado in ((2, 1, 0x0201), (3, 1, 0x0100), (3, 2, 0xff01)):
            m = mundo(tipo, 0xfefe, armazens=0)
            r = m.adicionar(0, recurso, 2, 0)
            self.assertEqual(r.pedido_sacolas.celula, esperado)
            self.assertEqual(m.terreno.quantidades[esperado], 2)

    def test_estoque_acima_da_capacidade_nao_e_corrigido_com_max(self):
        m = mundo(tipo=8)
        m.economia.creditar(0, 1, 150)
        r = m.adicionar(0, 1, 10, 0)
        self.assertEqual((r.credito_enviado, r.excedente), (65486, 60))
        self.assertEqual(m.economia.consultar(0).comida, 100)

    def test_capacidade_e_numerador_truncam_em_16_bits(self):
        m = mundo(tipo=8, armazens=400, capacidade=200)
        r = m.adicionar(0, 1, 20000, 0)
        self.assertEqual((r.credito_enviado, r.excedente), (14464, 5536))
        self.assertEqual(m.economia.consultar(0).comida, 9999)
        self.assertEqual(m.capacidades.nivel(0), 1)  # (14464 // 400 * 7) // 200.

    def test_pecas_passam_pelo_mesmo_limite_comida_pedra(self):
        m = mundo(tipo=8)
        m.economia.creditar(0, 1, 90)
        r = m.adicionar(0, 0, 20, 0)
        self.assertEqual((r.credito_enviado, r.excedente), (10, 10))
        self.assertEqual(m.economia.consultar(0).pecas, 10)
        self.assertEqual(m.capacidades.nivel(0), 7)

    def test_divisao_por_zero_ocorre_depois_do_credito(self):
        m = mundo(tipo=8, capacidade=0)
        m.economia.atribuir(0, 1, 12000)
        with self.assertRaises(ZeroDivisionError):
            m.adicionar(0, 1, 10, 0)
        self.assertEqual(m.economia.consultar(0).comida, 9999)
        self.assertEqual(sum(m.terreno.quantidades), 0)

    def test_tipo_4_contador_saturado_em_5_e_quantidade_ignorada(self):
        m = mundo(tipo=4)
        struct.pack_into('<H', m.estruturas, 0x0e, 5)
        for _ in range(8):
            m.adicionar(0, 2, 60000, 0)
        self.assertEqual(struct.unpack_from('<H', m.estruturas, 0x78)[0], 5)
        self.assertEqual(m.economia.consultar(0), (0, 0, 0, 0))

    def test_tipo_4_sem_alojamento_exige_dependencia_explicita(self):
        m = mundo(tipo=4)
        with self.assertRaises(RetiradaColonoPendente) as ctx:
            m.adicionar(0, 2, 10, 0)
        self.assertEqual(ctx.exception.indice, 0)
        # Exercita só o contrato da dependência; não valida BatimentRetireColon.
        chamados = []
        r = m.adicionar(0, 2, 10, 0, retirar_colono=chamados.append)
        self.assertEqual(chamados, [0])
        self.assertEqual((r.pedido_sacolas.celula, r.pedido_sacolas.recurso, r.pedido_sacolas.quantidade),
                         (0x2220, 1, 1))

    def test_sacolas_recusa_incompatibilidade_e_transbordo_aleatorio(self):
        t = TerrenoSacolas(semente=1)
        t.tipos[0x2020] = 0x43
        t.quantidades[0x2020] = 31
        t.criar(0x2020, 2)
        self.assertEqual(sum(t.quantidades), 31)
        t.criar(0x2020, 1)
        self.assertEqual(t.quantidades[0x2020], 31)
        self.assertEqual(sum(t.quantidades), 32)
        self.assertNotEqual(t.semente, 1)
        # O original compara a 31 por igualdade e incrementa em u8.
        t.quantidades[0x2020] = 255
        t.criar(0x2020, 1)
        self.assertEqual(t.quantidades[0x2020], 0)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialConstrucoes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_construcoes import BancadaConstrucoes
        cls.b = BancadaConstrucoes()

    def setUp(self):
        self.rng = random.Random(0x42340f)
        self.b.sujeira_pilha = None

    def conferir(self, m):
        esperado = dict(economia=bytes(m.economia.memoria), capacidades=bytes(m.capacidades.memoria),
                        estruturas=bytes(m.estruturas), tipos=bytes(m.terreno.tipos),
                        quantidades=bytes(m.terreno.quantidades), semente=m.terreno.semente)
        atual = self.b.estado()
        for nome in esperado:
            self.assertEqual(atual[nome], esperado[nome], nome)
        self.assertEqual(self.b.guardas(), (b'\xa6' * 16, b'\x6a' * 16))
        self.assertEqual(self.b.outras_guardas(), (b'\xc7' * 8, b'\x7c' * 8, b'\xe9' * 8, b'\x9e' * 8, 0x12345678))

    def adicionar(self, m, j, r, q, i):
        self.b.carregar_mundo(m)
        resultado = m.adicionar(j, r, q, i)
        self.b.adicionar(j, r, q, i)
        self.conferir(m)
        creditos = [c for c in self.b.chamadas if c['entrada'] == 0x4678f2]
        if creditos:
            self.assertEqual((creditos[0]['EAX'] & 255, creditos[0]['EDX'] & 65535, creditos[0]['EBX'] & 65535),
                             (r & 255, resultado.credito_enviado, j & 255))
        depositos = [c for c in self.b.chamadas if c['entrada'] == 0x4761a9]
        if resultado.pedido_sacolas:
            p = resultado.pedido_sacolas
            self.assertEqual([(c['EAX'] & 65535, c['EDX'] & 255, c['EBX'] & 65535) for c in depositos],
                             [(p.celula, p.recurso, p.quantidade)])
        else:
            self.assertEqual(depositos, [])

    def test_capacidade_1024_estados_inclusive_pilha_suja(self):
        for n in range(1024):
            j, i = n % 4, n % 8
            m = mundo(tipo=8)
            m.economia.memoria[:] = bytes(self.rng.randrange(256) for _ in range(128))
            m.capacidades.memoria[:] = bytes(self.rng.randrange(256) for _ in range(24))
            # Estes tipos não depositam excedentes: permite q/estoque extremos sem 65 mil sacolas.
            m.estruturas[:] = bytes(self.rng.randrange(256) for _ in range(8 * 276))
            m.estruturas[i * 276 + 8] = (0, 1, 5, 8, 21)[n % 5]
            m.capacidades.configurar(j, self.rng.randrange(1, 65536), self.rng.randrange(1, 65536))
            self.b.sujeira_pilha = (None, 0xa5, 0xff, 0x42)[n % 4]
            self.adicionar(m, j | 0x12340000, n % 4 | 0x12340000,
                           self.rng.getrandbits(32), i | 0xabcd0000)

    def test_destinos_excedentes_384_casos_com_sacolas_originais(self):
        for n in range(384):
            tipo, r, j, i = (2, 3, 8)[n % 3], n % 3, n % 4, n % 8
            m = mundo(tipo)
            m.estruturas[i * 276 + 8] = tipo
            struct.pack_into('<H', m.estruturas, i * 276 + 2, (0, 0xffff, 0x20ff, 0x2020)[n % 4])
            m.capacidades.configurar(j, 0 if n % 5 == 0 else 1, 100)
            m.economia.creditar(j, 1, 45)
            m.economia.creditar(j, 2, 45)
            m.terreno.semente = self.rng.randrange(0x80000000)
            self.adicionar(m, j, r, n % 49, i)

    def test_pilhas_cheias_e_ocupacao_incompativel_96_casos(self):
        for n in range(96):
            m = mundo(3, armazens=0)
            p = 0x2222
            m.terreno.tipos[p] = 0x43 if n % 2 else 0x44
            m.terreno.quantidades[p] = 31
            m.terreno.semente = self.rng.randrange(0x80000000)
            self.adicionar(m, 0, 1, 1 + n % 48, 0)

    def test_sem_lugar_nos_cinco_aneis_usa_ffff_2_casos(self):
        for tipo_ffff in (0, 0x80):
            m = mundo(3, armazens=0)
            for y in range(0x22 - 5, 0x22 + 6):
                for x in range(0x22 - 5, 0x22 + 6):
                    m.terreno.tipos[y * 256 + x] = 0x80
            m.terreno.tipos[0x2222] = 0x43
            m.terreno.quantidades[0x2222] = 31
            m.terreno.tipos[0xffff] = tipo_ffff
            self.adicionar(m, 0, 1, 1, 0)
            self.assertEqual(m.terreno.quantidades[0xffff], 1 if tipo_ffff == 0 else 0)

    def test_tipo_4_aceita_256_casos_e_limite_5(self):
        for n in range(256):
            m = mundo(4)
            limite = self.rng.randrange(1, 65536)
            ocupacao = self.rng.randrange(limite)
            struct.pack_into('<H', m.estruturas, 0x0e, limite)
            struct.pack_into('<H', m.estruturas, 0x72, ocupacao)
            struct.pack_into('<H', m.estruturas, 0x78, n if n % 2 else n % 6)
            self.adicionar(m, n % 4, n % 3, self.rng.getrandbits(32), 0)

    def test_tipo_4_recusa_64_paradas_na_dependencia(self):
        for n in range(64):
            m = mundo(4)
            struct.pack_into('<H', m.estruturas, 0x0e, n)
            struct.pack_into('<H', m.estruturas, 0x72, n)
            self.b.carregar_mundo(m)
            with self.assertRaises(RetiradaColonoPendente):
                m.adicionar(0, 1, 10, 0)
            regs = self.b.adicionar(0, 1, 10, 0)
            self.assertEqual(regs['EIP'], 0x41dde0)
            self.assertEqual(regs['EAX'], 0)
            self.conferir(m)

    def test_procura_512_casos_bordas_ordem_e_semente(self):
        for n in range(512):
            celula = (0, 0xffff, 0x00ff, 0xff00, 0x2020)[n % 5]
            tipo = 0x42 + n % 3
            m = mundo()
            m.terreno.semente = self.rng.randrange(0x80000000)
            x, y = celula & 255, celula >> 8
            for dy in range(-5, 6):
                for dx in range(-5, 6):
                    if 0 <= x + dx < 256 and 0 <= y + dy < 256:
                        p = (y + dy) * 256 + x + dx
                        m.terreno.tipos[p] = self.rng.choice((0, tipo, 0x80))
                        m.terreno.quantidades[p] = self.rng.choice((0, 1, 30, 31, 32, 255))
            self.b.carregar_mundo(m)
            esperado = m.terreno.procurar(celula, tipo)
            self.assertEqual(self.b.procurar(celula, tipo), esperado, n)
            self.conferir(m)

    def test_criar_e_depositar_192_casos(self):
        for n in range(192):
            m = mundo()
            recurso = n % 4
            celula = 0x2020
            m.terreno.semente = self.rng.randrange(0x80000000)
            m.terreno.tipos[celula] = (0, 0x42 + recurso, 0x80)[n % 3]
            m.terreno.quantidades[celula] = (0, 30, 31, 32, 254, 255)[n % 6]
            if m.terreno.tipos[celula] == 0x42 + recurso and 32 <= m.terreno.quantidades[celula] <= 254:
                m.terreno.quantidades[celula] = 31
            self.b.carregar_mundo(m)
            if n % 2:
                m.terreno.criar(celula, recurso)
                self.b.criar(celula, recurso)
            else:
                m.terreno.depositar(celula, recurso, n % 65)
                self.b.depositar(celula, recurso, n % 65)
            self.conferir(m)

    def test_pilhas_corrompidas_3_limites_de_execucao(self):
        for quantidade in (32, 33, 254):
            m = mundo()
            m.terreno.tipos[0x2020] = 0x43
            m.terreno.quantidades[0x2020] = quantidade
            self.b.carregar_mundo(m)
            with self.assertRaises(LimiteDeposito):
                m.terreno.criar(0x2020, 1, limite=10)
            with self.assertRaisesRegex(RuntimeError, 'não alcançou a parada'):
                self.b.criar(0x2020, 1)
            self.b.limites_esperados += 1
            self.conferir(m)

    def test_divisao_zero_8_excecoes_apos_credito(self):
        from bancada_construcoes import BancadaConstrucoes, x86, unicorn
        for n in range(8):
            # Uma CPU nova evita estado interno de exceção pendente do Unicorn.
            anterior = self.b
            type(self).b = BancadaConstrucoes()
            self.b.execucoes = anterior.execucoes
            self.b.excecoes_esperadas = anterior.excecoes_esperadas
            self.b.limites_esperados = anterior.limites_esperados
            m = mundo(8, capacidade=0)
            m.economia.atribuir(0, 1, 12000)
            self.b.carregar_mundo(m)
            with self.assertRaises(ZeroDivisionError):
                m.adicionar(0, 1, n, 0)
            with self.assertRaises(unicorn.UcError) as ctx:
                self.b.adicionar(0, 1, n, 0)
            self.assertEqual(ctx.exception.errno, unicorn.UC_ERR_EXCEPTION)
            self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_EIP), 0x423501)
            self.b.excecoes_esperadas += 1
            self.conferir(m)


if __name__ == '__main__':
    unittest.main()
