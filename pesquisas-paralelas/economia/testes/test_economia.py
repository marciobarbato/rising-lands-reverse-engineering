"""Casos explicativos e diferenciais; todas as escritas ficam na pesquisa."""
import json
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from economia import Economia, Recurso, Saldos, custo_ia, custos_construcao, custos_unidade


class Exemplos(unittest.TestCase):
    def test_ids_e_consultas(self):
        e = Economia()
        for r, valor in ((Recurso.COMIDA, 10), (Recurso.PEDRA, 20), (Recurso.PECAS, 30), (3, 40)):
            e.atribuir(0, r, valor)
        self.assertEqual(e.consultar(0), (10, 20, 30, 0))
        self.assertEqual(e.consultar_rmi(0), (10, 20, 0, 0))
        self.assertEqual(e.consultar_estoque(0), (0, 0, 0, 0))

    def test_atribuicao_sem_teto_preserva_byte_7(self):
        e = Economia(b'\xa5' * 128)
        e.atribuir(0, 1, 70000)
        self.assertEqual(e.registro(0, 1), struct.pack('<HHHB', 4464, 4464, 0, 0) + b'\xa5')
        self.assertEqual(e.registro(0, 0), b'\xa5' * 8)

    def test_credito_overflow_antes_do_teto(self):
        e = Economia()
        e.atribuir(0, 1, 65535)
        e.creditar(0, 1, 1)
        self.assertEqual(e.consultar(0).comida, 0)
        self.assertEqual(e.consultar_estoque(0).comida, 1)
        e.creditar(0, 1, 10000)
        self.assertEqual(e.consultar(0).comida, 9999)
        e.atribuir(0, 1, 12000)
        e.creditar(0, 1, 0)
        self.assertEqual(e.consultar(0).comida, 9999)

    def test_debito_consumindo_rmi_primeiro_em_termos_da_diferenca(self):
        e = Economia()
        e.atribuir(0, 1, 100)
        e.creditar(0, 1, 40)
        e.debitar(0, 1, 80)
        self.assertEqual(e.consultar(0).comida, 60)
        self.assertEqual(e.consultar_rmi(0).comida, 20)
        self.assertEqual(e.consultar_estoque(0).comida, 40)
        e.debitar(0, 1, 30)
        self.assertEqual(e.consultar_rmi(0).comida, 0)
        self.assertEqual(e.consultar_estoque(0).comida, 30)
        e.debitar(0, 1, 1000)
        self.assertEqual(e.consultar(0).comida, 0)

    def test_suficiencia_e_falta_de_pecas_no_helper(self):
        e = Economia()
        e.atribuir(0, 1, 10)
        e.atribuir(0, 2, 20)
        self.assertTrue(e.suficiente(0, 10, 20, 0))
        self.assertFalse(e.suficiente(0, 10, 20, 1))
        self.assertEqual(e.recurso_necessario(0, Saldos(10, 20, 999)), 0)
        self.assertEqual(e.recurso_necessario(0, Saldos(11, 21, 999)), 1)
        self.assertEqual(e.recurso_necessario(0, Saldos(10, 21, 999)), 2)

    def test_indices_ia_nao_sao_ids_internos(self):
        e = Economia()
        e.atribuir(0, Recurso.COMIDA, 4)
        self.assertEqual(e.testar_ia(0, 0, 4), 1)
        self.assertEqual(e.testar_ia(0, 1, 4), -1)
        self.assertEqual(e.testar_ia(0, 3, 0), 1)
        self.assertEqual(e.testar_ia(0, 0, 0xffffffff), 1)

    def test_custos_de_unidade_reordenados(self):
        tipo = bytearray(50)
        struct.pack_into('<3H', tipo, 2, 10, 30, 20)
        custos = custos_unidade(tipo)
        self.assertEqual(custos, (10, 20, 30, 0))
        self.assertEqual([custo_ia(custos, i) for i in range(3)], [10, 20, 30])

    def test_indices_truncados_e_validacao_adicional(self):
        e = Economia()
        e.atribuir(0x10000, 0x101, -1)
        self.assertEqual(e.consultar(0).comida, 65535)
        with self.assertRaises(ValueError):
            e.consultar(4)
        with self.assertRaises(ValueError):
            e.atribuir(0, 4, 0)
        with self.assertRaises(ValueError):
            Economia(bytes(127))

    def test_custos_reais_dos_26_tipos(self):
        dados = json.loads((PASTA.parents[1] / 'relatorios/unidades.json').read_text())
        for tipo in dados['unidades']:
            c = custos_unidade(bytes.fromhex(tipo['registro_memoria_hex']))
            self.assertEqual(c, (tipo['custo_comida'], tipo['custo_pedra'], tipo['custo_pecas'], 0))

    def test_recursos_iniciais_dos_38_mapas(self):
        mapas = sorted((PASTA.parents[2] / 'source/cd/WORLD').glob('*.ETA'))
        self.assertEqual(len(mapas), 38)
        # Apenas leitura do leitor existente; o teste confronta os offsets do arquivo.
        sys.path.insert(0, str(PASTA.parents[1] / 'ferramentas'))
        from formatos import ler_eta
        for mapa in mapas:
            dados = mapa.read_bytes()
            recursos = ler_eta(dados)['recursos_por_tipo']
            e = Economia.de_recursos_eta(recursos, b'\xa5' * 128)
            for j in range(4):
                bruto = tuple(struct.unpack_from('<H', dados, o + j * 2)[0]
                              for o in (0x50004, 0x5000c, 0x50014)) + (0,)
                self.assertEqual(e.consultar(j), bruto)
                self.assertEqual(e.consultar_rmi(j), bruto[:2] + (0, 0))
                self.assertEqual(e.consultar_estoque(j), (0, 0, 0, 0))
                self.assertEqual(e.registro(j, 3), b'\xa5' * 8)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class Diferencial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_economia import BancadaEconomia
        cls.b = BancadaEconomia()
        cls.rng = random.Random(0x4678f2)

    def estado(self):
        dados = bytes(self.rng.randrange(256) for _ in range(128))
        self.b.carregar(dados)
        return Economia(dados)

    def conferir_memoria(self, e):
        self.assertEqual(self.b.memoria(), e.memoria)
        self.assertEqual(self.b.guardas(), (b'\xa6' * 16, b'\x6a' * 16))

    def test_mutacoes_1536_casos_mais_limites(self):
        for entrada, nome in ((0x46799c, 'atribuir'), (0x4678f2, 'creditar'), (0x46792c, 'debitar')):
            for n in range(512):
                e = self.estado()
                # Também confere truncamentos AL, BX, DX com bits altos preenchidos.
                j = self.rng.getrandbits(16) << 16 | (n % 4)
                r = self.rng.getrandbits(24) << 8 | (n // 4 % 4)
                q = self.rng.getrandbits(32)
                getattr(e, nome)(j, r, q)
                self.b.mutacao(entrada, j, r, q)
                self.conferir_memoria(e)
        for inicial, q in ((65535, 1), (65530, 10), (9999, 1), (12000, 0), (0, 0xffffffff)):
            e = Economia()
            e.atribuir(0, 1, inicial)
            self.b.carregar(e.memoria)
            e.creditar(0, 1, q)
            self.b.mutacao(0x4678f2, 0, 1, q)
            self.conferir_memoria(e)

    def test_consultas_1536_casos_e_bytes_nao_escritos(self):
        for _ in range(512):
            e = self.estado()
            j = self.rng.getrandbits(24) << 8 | self.rng.randrange(4)
            for entrada, nome in ((0x467670, 'consultar'), (0x467640, 'consultar_rmi'),
                                   (0x46769d, 'consultar_estoque')):
                resultado, bruto = self.b.consulta(entrada, j)
                esperado = getattr(e, nome)(j)
                self.assertEqual(resultado, esperado)
                self.assertEqual(bruto, b''.join(struct.pack('<H', v) + b'\xa5\xa5' for v in esperado))
                self.conferir_memoria(e)

    def test_suficiencia_512_casos_e_igualdade(self):
        for n in range(512):
            e = self.estado()
            j = n % 4
            custos = e.consultar(j)[:3] if n % 5 == 0 else tuple(self.rng.getrandbits(32) for _ in range(3))
            self.assertEqual(self.b.suficiente(j, *custos), e.suficiente(j, *custos))
            self.conferir_memoria(e)

    def test_operacoes_ia_1024_casos_e_limiares_signed(self):
        for n in range(512):
            e = self.estado()
            j, indice = n % 4, n // 4 % 4
            limites = [0, 65535, 65536, 0xffffffff, 0x80000000, self.rng.getrandbits(32)]
            limiar = limites[n % len(limites)]
            for entrada, estoque in ((0x4813b8, True), (0x481400, False)):
                self.assertEqual(self.b.operacao_ia(entrada, j, indice, limiar),
                                 e.testar_ia(j, indice, limiar, estoque=estoque))
                self.conferir_memoria(e)

    def test_riqueza_256_casos(self):
        for n in range(256):
            e = self.estado()
            self.assertEqual(self.b.riqueza(n % 4), e.riqueza_ia(n % 4))
            self.conferir_memoria(e)

    def test_custos_sinteticos_acessores_e_ia_208_chamadas(self):
        for tipo in range(26):
            unidade = bytes(self.rng.randrange(256) for _ in range(50))
            self.b.cpu.mem_write(0x4965ae + tipo * 50, unidade)
            c = custos_unidade(unidade)
            self.assertEqual(self.b.custos(0x4410d2, tipo | 0x12340000), c)
            for i in range(3):
                self.assertEqual(self.b.operacao_ia(0x481372, 0, i, tipo), custo_ia(c, i))
            tabela = bytes(self.rng.randrange(256) for _ in range(52 * 26))
            self.b.cpu.mem_write(0x495d98, tabela)
            c = custos_construcao(tabela, tipo)
            self.assertEqual(self.b.custos(0x41aace, tipo), c)
            for i in range(3):
                self.assertEqual(self.b.operacao_ia(0x481399, 0, i, tipo), custo_ia(c, i))

    def test_helper_necessidade_512_casos(self):
        for n in range(256):
            e = self.estado()
            j, tipo = n % 4, n % 26
            unidade = bytes(self.rng.randrange(256) for _ in range(50))
            self.b.cpu.mem_write(0x4965ae + tipo * 50, unidade)
            self.assertEqual(self.b.necessario(0x45d7cf, j, tipo),
                             e.recurso_necessario(j, custos_unidade(unidade)))
            tabela = bytes(self.rng.randrange(256) for _ in range(26 * 52))
            self.b.cpu.mem_write(0x495d98, tabela)
            self.assertEqual(self.b.necessario(0x45d753, j, tipo),
                             e.recurso_necessario(j, custos_construcao(tabela, tipo)))
            self.conferir_memoria(e)

    def test_sequencia_credito_debito_e_consultas_400_chamadas(self):
        e = Economia()
        self.b.carregar(e.memoria)
        for n in range(100):
            j, r, q = n % 4, n % 3, self.rng.randrange(20000)
            entrada, nome = ((0x4678f2, 'creditar'), (0x46792c, 'debitar'),
                             (0x46799c, 'atribuir'))[n % 3]
            getattr(e, nome)(j, r, q)
            self.b.mutacao(entrada, j, r, q)
            for a, f in ((0x467670, e.consultar), (0x467640, e.consultar_rmi), (0x46769d, e.consultar_estoque)):
                self.assertEqual(self.b.consulta(a, j)[0], f(j))
            self.conferir_memoria(e)

    def test_inicializacao_38_mapas_e_custos_reais_482_chamadas(self):
        sys.path.insert(0, str(PASTA.parents[1] / 'ferramentas'))
        from formatos import ler_eta
        for mapa in sorted((PASTA.parents[2] / 'source/cd/WORLD').glob('*.ETA')):
            recursos = ler_eta(mapa.read_bytes())['recursos_por_tipo']
            antes = bytes(self.rng.randrange(256) for _ in range(128))
            e = Economia.de_recursos_eta(recursos, antes)
            self.b.carregar(antes)
            for r in (1, 2, 0):
                for j, valor in enumerate(recursos[str(r)]):
                    self.b.mutacao(0x46799c, j, r, valor)
            self.conferir_memoria(e)
        dados = json.loads((PASTA.parents[1] / 'relatorios/unidades.json').read_text())
        for tipo in dados['unidades']:
            registro = bytes.fromhex(tipo['registro_memoria_hex'])
            self.b.cpu.mem_write(0x4965ae + tipo['id'] * 50, registro)
            self.assertEqual(self.b.custos(0x4410d2, tipo['id']), custos_unidade(registro))


if __name__ == '__main__':
    unittest.main()
