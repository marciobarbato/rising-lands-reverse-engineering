"""Propostas: direções da diplomacia, IDIV, wraps e memória integral."""
import json
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(PASTA))
from mercado import Mercado, BUFFERS


def w(bloco, offset, valor):
    struct.pack_into('<H', bloco, offset, valor & 65535)


def preparar(tipo=1, simpatia=0, aliado=False, oferecido=100, pedido=100, jogador=0):
    m = Mercado()
    j, c = jogador, (jogador + 1) % 4
    m.contatos[j] = c
    m.jogadores[j * 20 + 1] = tipo
    m.jogadores[c * 20 + 6] = (1 << j) if aliado else 0
    a, b = (j, c) if tipo == 2 else (c, j)
    w(m.jogadores, a * 20 + 12 + b * 2, simpatia)
    m.precos_recursos[:] = bytes((1, 1, 1))
    w(m.recursos_oferecidos, j * 6, oferecido)
    w(m.recursos_pedidos, j * 6, pedido)
    return m


def resultado(m, jogador=0):
    return (struct.unpack_from('<H', m.indicadores, jogador * 2)[0],
            struct.unpack_from('<H', m.diferenca)[0])


class ExemplosMercado(unittest.TestCase):
    def test_consulta_totais_por_id_e_nao_estoque(self):
        m = Mercado()
        for recurso, quantidade in enumerate((17, 23, 42, 99)):
            m.economia.atribuir(0, recurso, quantidade)
        self.assertEqual([m.quantidade_recurso(0, r) for r in range(5)],
                         [17, 23, 42, 65535, 65535])
        self.assertEqual(m.economia.consultar_estoque(0)[:3], (0, 0, 0))
        self.assertEqual(m.quantidade_recurso(0x100, 0x102), 42)

    def test_fator80_120_e_sentido_da_avaliacao(self):
        for tipo, alianca, esperado in ((1, False, (80, 65516)), (1, True, (120, 20)),
                                      (2, False, (125, 25)), (2, True, (83, 65519))):
            m = preparar(tipo=tipo, aliado=alianca)
            self.assertIsNone(m.avaliar(0))
            self.assertEqual(resultado(m), esperado)

    def test_proposta_vazia_e_denominador_ausente_nao_sao_simetria(self):
        for tipo, oferta, pedido, esperado in (
                (1, 0, 0, (0, 0)), (2, 0, 0, (100, 0)),
                (1, 100, 0, (200, 80)), (2, 0, 100, (100, 125)),
                (1, 0, 100, (0, 65436)), (2, 100, 0, (0, 65436))):
            m = preparar(tipo=tipo, oferecido=oferta, pedido=pedido)
            m.avaliar(0)
            self.assertEqual(resultado(m), esperado)

    def test_simpatia_inverte_mas_alianca_mantem_direcao(self):
        m = preparar()
        w(m.jogadores, 1 * 20 + 12, 10)  # Contato -> jogador.
        w(m.jogadores, 12 + 2, -20)       # Jogador -> contato.
        m.jogadores[6] = 1 << 1          # Aliança inversa não participa.
        m.avaliar(0)
        self.assertEqual(resultado(m), (90, 65526))
        m.jogadores[1] = 2
        m.avaliar(0)
        self.assertEqual(resultado(m), (166, 66))

    def test_truncamento_negativo_e_indicador_sem_clamp(self):
        m = preparar(simpatia=-81, oferecido=199, pedido=3)
        m.avaliar(0)
        self.assertEqual(resultado(m), (65503, 65532))  # -1, depois -100/3 -> -33.
        m = preparar(oferecido=65535, pedido=1)
        m.avaliar(0)
        self.assertEqual(resultado(m), (65456, 52427))  # 5.242.800 truncado para u16.

    def test_somas_pesadas_e_produtos_signed32_com_wrap(self):
        m = preparar(simpatia=32767)
        m.precos_unidades[:] = b'\xff' * 26
        m.precos_recursos[:] = b'\xff' * 3
        m.unidades_oferecidas[:52] = b'\xff' * 52
        m.recursos_oferecidos[:6] = b'\xff' * 6
        m.avaliar(0)
        # Valor 484.631.325; pedido 100×255; produto wrapped = 1.536.333.299.
        # Expectativa calculada sem os helpers da tradução e conferida no x86.
        self.assertEqual(resultado(m), (60248, 2408))

    def test_divisor_zero_mesmo_vazio_nao_altera_saidas(self):
        for alianca, simpatia in ((False, -80), (True, -120)):
            m = preparar(tipo=2, simpatia=simpatia, aliado=alianca, oferecido=0, pedido=0)
            m.indicadores[:] = b'\xa5' * 8
            m.diferenca[:] = b'\x5a' * 2
            with self.assertRaises(ZeroDivisionError):
                m.avaliar(0)
            self.assertEqual((m.indicadores, m.diferenca), (b'\xa5' * 8, b'\x5a' * 2))

    def test_preco_global_independe_de_saldo_e_outras_propostas(self):
        m = preparar(oferecido=0, pedido=10, jogador=3)
        m.precos_unidades[25] = 7
        w(m.unidades_oferecidas, 3 * 52 + 25 * 2, 5)
        m.unidades_oferecidas[:52] = b'\xff' * 52
        m.economia.memoria[:] = b'\xa5' * 128
        antes = bytes(m.economia.memoria)
        m.avaliar(3)
        self.assertEqual(resultado(m, 3), (280, 18))
        self.assertEqual(m.economia.memoria, antes)

    def test_diferenca_global_sobrescrita_indicadores_por_jogador(self):
        m = preparar()
        m.contatos[1] = 0
        w(m.recursos_oferecidos, 6, 10)
        w(m.recursos_pedidos, 6, 20)
        m.avaliar(0)
        m.avaliar(1)
        self.assertEqual(struct.unpack('<4H', m.indicadores), (80, 40, 0, 0))
        self.assertEqual(resultado(m, 1)[1], 65524)

    def test_guardas_adicionais_e_tipo_invalido_original(self):
        m = Mercado()
        self.assertEqual(m.tipo_jogador(0x1ff), 2)
        self.assertEqual(m.aliado(0x101, 1), 1)
        for chamada in (lambda: m.avaliar(4), lambda: m.aliado(4, 4),
                        lambda: m.simpatia(0, 255), lambda: m.quantidade_recurso(4, 255)):
            with self.assertRaises(ValueError):
                chamada()
        m.contatos[0] = 255
        with self.assertRaises(ValueError):
            m.avaliar(0)
        with self.assertRaises(ValueError):
            Mercado(jogadores=bytes(79))
        with self.assertRaises(ValueError):
            Mercado(precos_unidades=bytes(25))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: usar --emular')
class DiferencialMercado(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_mercado import BancadaMercado
        cls.b = BancadaMercado()

    def setUp(self):
        self.rng = random.Random(0x466bac)

    def conferir(self, m):
        from bancada_mercado import JOGADORES
        for nome, atual in self.b.estado().items():
            self.assertEqual(atual, bytes(getattr(m, nome)), nome)
        self.assertEqual(bytes(self.b.cpu.mem_read(JOGADORES - 8, 96)),
                         b'\xc3' * 8 + bytes(m.jogadores) + b'\x3c' * 8)
        self.assertEqual(self.b.memoria(), bytes(m.economia.memoria))
        self.assertEqual(self.b.guardas(), (b'\xa6' * 16, b'\x6a' * 16))
        esperado = bytearray(self.b.antes)
        for nome in ('indicadores', 'diferenca'):
            endereco, tamanho = BUFFERS[nome]
            esperado[endereco - 0x4e2900:endereco - 0x4e2900 + tamanho] = getattr(m, nome)
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4e2900, 0x600)), esperado)

    def avaliar(self, m, j):
        from emulador import RETORNO, PILHA
        self.b.carregar_mercado(m)
        m.avaliar(j)
        regs = {n: self.rng.getrandbits(32) for n in ('EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')}
        atual = self.b.chamar(0x466bac, (j & 255) | self.rng.getrandbits(24) << 8,
                              regs['EDX'], regs)
        self.assertEqual((atual['EIP'], atual['ESP']), (RETORNO, PILHA + 0x8004))
        for nome, valor in regs.items():
            self.assertEqual(atual[nome], valor, nome)
        self.conferir(m)
        j &= 255
        c = m.contatos[j]
        a, b = (j, c) if m.tipo_jogador(j) == 2 else (c, j)
        self.assertEqual([(e, x, y) if e != 0x46d817 else (e, x, None)
                          for e, x, y in self.b.acessos],
                         [(0x46d817, j, None), (0x46dc6c, a, b), (0x46d838, c, j)])
        self.assertEqual(self.b.escritas,
                         [(0x4e2930 + 2 * j, 2, resultado(m, j)[0]),
                          (0x4e2948, 2, resultado(m, j)[1])])

    def test_consulta_1024_ids_e_jogadores(self):
        from emulador import RETORNO
        m = Mercado()
        m.economia.memoria[:] = self.rng.randbytes(128)
        for j in range(4):
            for r in range(256):
                self.b.carregar_mercado(m)
                atual = self.b.chamar(0x462a58, r | self.rng.getrandbits(24) << 8,
                                      j | self.rng.getrandbits(24) << 8)
                self.assertEqual(atual['EIP'], RETORNO)
                self.assertEqual(atual['EAX'], m.quantidade_recurso(j, r))
                self.assertEqual([e for e, _, _ in self.b.acessos], [0x467670])
                self.assertEqual(self.b.escritas, [])
                self.conferir(m)

    def test_acessores_256_tipos_1024_aliancas_112_simpatias(self):
        m = Mercado(jogadores=self.rng.randbytes(80))
        for j in range(256):
            self.b.carregar_mercado(m)
            atual = self.b.chamar(0x46d817, j | 0xabcdef00)
            self.assertEqual(atual['EAX'] & 255, m.tipo_jogador(j))
            self.conferir(m)
        for mask in range(256):
            for j in range(4):
                c = (j + 1) % 4
                m.jogadores[j * 20 + 6] = mask
                self.b.carregar_mercado(m)
                atual = self.b.chamar(0x46d838, j | 0xabcdef00, c | 0x12345600)
                self.assertEqual(atual['EAX'] & 255, m.aliado(j, c))
                self.conferir(m)
        for j in range(4):
            for c in range(4):
                for v in (-32768, -120, -80, -1, 0, 100, 32767):
                    w(m.jogadores, j * 20 + 12 + c * 2, v)
                    self.b.carregar_mercado(m)
                    atual = self.b.chamar(0x46dc6c, j | 0xabcdef00, c | 0x12345600)
                    self.assertEqual(atual['EAX'] & 65535, m.simpatia(j, c) & 65535)
                    self.conferir(m)

    def test_232_componentes_com_precos_originais(self):
        dados = json.loads((PASTA / 'evidencias/parametros-mercado.json').read_text())
        for j in range(4):
            for tipo in (1, 2):
                for item in range(29):
                    m = preparar(tipo=tipo, jogador=j, oferecido=0, pedido=0)
                    m.precos_unidades[:] = bytes.fromhex(dados['precos_unidades']['bytes_hex'])
                    m.precos_recursos[:] = bytes.fromhex(dados['precos_recursos']['bytes_hex'])
                    if item < 26:
                        w(m.unidades_oferecidas, j * 52 + item * 2, 13)
                        w(m.unidades_pedidas, j * 52 + item * 2, 17)
                    else:
                        w(m.recursos_oferecidos, j * 6 + (item - 26) * 2, 13)
                        w(m.recursos_pedidos, j * 6 + (item - 26) * 2, 17)
                    self.avaliar(m, j)

    def test_fronteiras_de_tipo_simpatia_alianca_e_lados_vazios(self):
        for tipo in (0, 1, 2, 3, 255):
            for s in (-32768, -121, -120, -119, -81, -80, -79, -1, 0, 1, 32767):
                for aliado in (False, True):
                    if tipo == 2 and 80 + s + 40 * aliado == 0:
                        continue  # Casos de exceção isolados no teste abaixo.
                    for oferta, pedido in ((0, 0), (0, 1), (1, 0), (1, 1), (65535, 1), (65535, 65535)):
                        self.avaliar(preparar(tipo, s, aliado, oferta, pedido), 0)

    def test_1024_estados_arbitrarios_com_overflow_e_contato_proprio(self):
        for n in range(1024):
            m = Mercado(jogadores=self.rng.randbytes(80),
                        **{nome: self.rng.randbytes(tamanho) for nome, (_, tamanho) in BUFFERS.items()})
            m.economia.memoria[:] = self.rng.randbytes(128)
            j, c = n % 4, n // 4 % 4
            m.contatos[j] = c
            m.jogadores[j * 20 + 1] = (0, 1, 2, 3, 255)[n % 5]
            if m.tipo_jogador(j) == 2 and 80 + m.simpatia(j, c) + 40 * m.aliado(c, j) == 0:
                w(m.jogadores, j * 20 + 12 + c * 2, 0)
            self.avaliar(m, j)

    def test_wrap_explicito_maximos_e_sinais(self):
        m = preparar(simpatia=32767)
        m.precos_unidades[:] = b'\xff' * 26
        m.precos_recursos[:] = b'\xff' * 3
        m.unidades_oferecidas[:52] = b'\xff' * 52
        m.recursos_oferecidos[:6] = b'\xff' * 6
        self.avaliar(m, 0)
        self.assertEqual(resultado(m), (60248, 2408))
        for tipo in (1, 2):
            for s in (-32768, -81, -79, 0, 32767):
                for pedida in (1, 65535):
                    m = preparar(tipo=tipo, simpatia=s)
                    m.precos_unidades[:] = b'\xff' * 26
                    m.precos_recursos[:] = b'\xff' * 3
                    m.unidades_oferecidas[:52] = b'\xff' * 52
                    m.recursos_oferecidos[:6] = b'\xff' * 6
                    m.unidades_pedidas[:52] = struct.pack('<26H', *([pedida] * 26))
                    m.recursos_pedidos[:6] = struct.pack('<3H', *([pedida] * 3))
                    self.avaliar(m, 0)

    def test_16_divisoes_zero_preservam_toda_memoria(self):
        from bancada_mercado import BancadaMercado
        from emulador import unicorn, x86
        for j in range(4):
            for aliado in (False, True):
                for pedido in (0, 65535):
                    m = preparar(tipo=2, simpatia=-120 if aliado else -80,
                                 aliado=aliado, pedido=pedido, jogador=j)
                    m.indicadores[:] = b'\xa5' * 8
                    m.diferenca[:] = b'\x5a' * 2
                    # Unicorn conserva estado após UC_ERR_EXCEPTION; CPU nova por caso.
                    anterior = self.b
                    type(self).b = BancadaMercado()
                    self.b.execucoes = anterior.execucoes
                    self.b.excecoes_esperadas = anterior.excecoes_esperadas
                    self.b.carregar_mercado(m)
                    with self.assertRaises(ZeroDivisionError):
                        m.avaliar(j)
                    with self.assertRaises(unicorn.UcError) as erro:
                        self.b.chamar(0x466bac, j)
                    self.assertEqual(erro.exception.errno, unicorn.UC_ERR_EXCEPTION)
                    self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_EIP), 0x466d94)
                    self.b.excecoes_esperadas += 1
                    self.assertEqual(self.b.escritas, [])
                    self.conferir(m)
        anterior = self.b
        type(self).b = BancadaMercado()
        self.b.execucoes = anterior.execucoes
        self.b.excecoes_esperadas = anterior.excecoes_esperadas
