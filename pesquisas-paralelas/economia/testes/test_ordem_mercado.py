"""Market handshake and consuming resource calls compared to original x86."""
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from construcoes import EconomiaConstrucoes
from economia import BASE_RECURSOS
from mercado import Mercado, BUFFERS
from ordem_mercado import OrdemMercado, TrocaUnidadesMercadoPendente, BASE_ACEITES


def w(b, o, v):
    struct.pack_into('<H', b, o, v & 65535)


def proposta(o, p=1, oferta=(3, 5, 7), pedido=(11, 13, 17)):
    struct.pack_into('<3H', o.mercado.recursos_oferecidos, p * 6, *oferta)
    struct.pack_into('<3H', o.mercado.recursos_pedidos, p * 6, *pedido)


def preparar(j=0, p=1, tipo_j=1, tipo_p=1):
    m = EconomiaConstrucoes()
    o = OrdemMercado(Mercado(m.economia), m)
    o.mercado.jogadores[j * 20 + 1] = tipo_j
    o.mercado.jogadores[p * 20 + 1] = tipo_p
    o.aceites[p] = 1
    for jogador in range(4):
        for recurso in range(4):
            struct.pack_into('<HH', m.economia.memoria, jogador * 32 + recurso * 8, 100, 100)
    proposta(o, p)
    return o


def pares(o, jogador):
    return [struct.unpack_from('<HH', o.mundo.economia.memoria, jogador * 32 + recurso * 8) for recurso in range(4)]


class ExemplosOrdemMercado(unittest.TestCase):
    def test_wait_toggle_without_transfer_then_second_approval_executes(self):
        o = preparar()
        o.aceites[1] = 0
        antes = bytes(o.mundo.economia.memoria)
        self.assertFalse(o.ordenar(0x100, 0x101))
        self.assertEqual(o.aceites, bytes((1, 0, 0, 0)))
        self.assertEqual(bytes(o.mundo.economia.memoria), antes)
        o.aceites[1] = 255
        self.assertTrue(o.ordenar(0, 1))  # New own approval is zero, but still executes.
        self.assertEqual(o.aceites, bytes(4))

    def test_second_argument_row_is_consumed_contacts_and_indicator_ignored(self):
        o = preparar()
        proposta(o, 0, (600, 600, 600), (700, 700, 700))
        o.mercado.contatos[:] = b'\xff' * 4
        o.mercado.indicadores[:] = bytes(8)
        o.ordenar(0, 1)
        self.assertEqual(pares(o, 0), [(92, 92), (92, 92), (90, 90), (100, 100)])
        self.assertEqual(pares(o, 1), [(108, 108), (108, 108), (110, 110), (100, 100)])
        self.assertEqual(bytes(o.mercado.recursos_oferecidos[6:12]), bytes(6))
        self.assertEqual(bytes(o.mercado.recursos_pedidos[6:12]), bytes(6))
        self.assertEqual(struct.unpack_from('<3H', o.mercado.recursos_oferecidos), (600, 600, 600))

    def test_type_two_executes_without_peer_approval(self):
        o = preparar(tipo_j=2)
        o.aceites[:] = bytes(4)
        self.assertTrue(o.ordenar(0, 1))
        self.assertEqual(pares(o, 0)[0], (103, 103))  # Requested debit skipped for type 2.
        self.assertEqual(pares(o, 1)[0], (108, 108))

    def test_zero_resources_skip_debit_and_recalculation(self):
        o = preparar()
        proposta(o, oferta=(0, 0, 0), pedido=(0, 0, 0))
        for j in (0, 1):
            o.mundo.capacidades.configurar(j, 1, 0)
            o.mundo.capacidades.escrever_nivel(j, 99)
        self.assertTrue(o.ordenar(0, 1))
        self.assertEqual((o.mundo.capacidades.nivel(0), o.mundo.capacidades.nivel(1)), (99, 99))

    def test_alias_reads_freshly_toggled_approval(self):
        o = preparar(j=0, p=0)
        o.aceites[0] = 1
        self.assertFalse(o.ordenar(0, 0))
        self.assertTrue(o.ordenar(0, 0))
        self.assertEqual(pares(o, 0), [(100, 100)] * 4)

    def test_first_unit_checkpoint_preserves_toggle_and_all_resources(self):
        o = preparar()
        w(o.mercado.unidades_oferecidas, 52 + 7 * 2, 65535)
        antes = bytes(o.mundo.economia.memoria)
        with self.assertRaises(TrocaUnidadesMercadoPendente) as ctx:
            o.ordenar(0, 1)
        self.assertEqual((ctx.exception.endereco, ctx.exception.tipo_unidade, ctx.exception.quantidade),
                         (0x46166b, 7, 65535))
        self.assertEqual(o.aceites[:2], bytes((1, 1)))
        self.assertEqual(bytes(o.mundo.economia.memoria), antes)

    def test_second_unit_checkpoint_keeps_completed_offered_resource_leg(self):
        o = preparar()
        w(o.mercado.unidades_pedidas, 52 + 2 * 2, 1)
        with self.assertRaises(TrocaUnidadesMercadoPendente) as ctx:
            o.ordenar(0, 1)
        self.assertEqual(ctx.exception.endereco, 0x4618df)
        self.assertEqual(pares(o, 0)[:3], [(103, 103), (105, 105), (107, 107)])
        self.assertEqual(bytes(o.mercado.recursos_oferecidos[6:12]), bytes(6))
        self.assertEqual(struct.unpack_from('<3H', o.mercado.recursos_pedidos, 6), (11, 13, 17))

    def test_divide_failure_keeps_earlier_leg_row_consumption_and_approvals(self):
        o = preparar()
        o.mundo.capacidades.configurar(0, 1, 0)
        with self.assertRaises(ZeroDivisionError):
            o.ordenar(0, 1)
        self.assertEqual(bytes(o.mercado.recursos_oferecidos[6:12]), bytes(6))
        self.assertEqual(struct.unpack_from('<3H', o.mercado.recursos_pedidos, 6), (11, 13, 17))
        self.assertEqual(pares(o, 0)[0], (92, 92))
        self.assertEqual(pares(o, 1)[0], (97, 97))  # No credit for failed requested debit.
        self.assertEqual(o.aceites[:2], bytes((1, 1)))

    def test_direct_callers_do_not_toggle_or_clear_approvals(self):
        o = preparar()
        o.aceites[:] = bytes((8, 7, 6, 5))
        self.assertIsNone(o.receber(0, 1))
        self.assertIsNone(o.entregar(0, 1))
        self.assertEqual(o.aceites, bytes((8, 7, 6, 5)))

    def test_protected_domains_and_shared_economy(self):
        o = preparar()
        with self.assertRaises(ValueError):
            OrdemMercado(Mercado(), o.mundo)
        with self.assertRaises(ValueError):
            OrdemMercado(o.mercado, o.mundo, aceites=bytes(5))
        for j, p in ((4, 0), (0, 255), (-1, 0)):
            antes = bytes(o.aceites)
            with self.assertRaises(ValueError):
                o.ordenar(j, p)
            self.assertEqual(bytes(o.aceites), antes)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional original x86: RISING_EMULAR=1')
class DiferencialOrdemMercado(unittest.TestCase):
    bancadas = []

    def setUp(self):
        self.nova_bancada()
        self.rng = random.Random(0x461bea)

    def nova_bancada(self):
        from bancada_ordem_mercado import BancadaOrdemMercado
        self.b = BancadaOrdemMercado()
        type(self).bancadas.append(self.b)

    def conferir(self, o):
        from bancada_mercado import JOGADORES
        m = o.mundo
        esperado = dict(economia=bytes(m.economia.memoria), capacidades=bytes(m.capacidades.memoria),
                        estruturas=bytes(m.estruturas), tipos=bytes(m.terreno.tipos),
                        quantidades=bytes(m.terreno.quantidades), semente=m.terreno.semente)
        for k, v in self.b.estado().items():
            self.assertTrue(v == esperado[k], k)
        self.assertEqual(self.b.aceites(), bytes(o.aceites))
        self.assertEqual(self.b.guardas(), (b'\xa6' * 16, b'\x6a' * 16))
        self.assertEqual(self.b.outras_guardas(), (b'\xc7' * 8, b'\x7c' * 8, b'\xe9' * 8, b'\x9e' * 8, 0x12345678))
        self.assertEqual(bytes(self.b.cpu.mem_read(JOGADORES - 8, 96)), b'\xc3' * 8 + bytes(o.mercado.jogadores) + b'\x3c' * 8)
        janela = bytearray(self.b.vizinhos_antes)
        for nome, (endereco, tamanho) in BUFFERS.items():
            atual = bytes(getattr(o.mercado, nome))
            self.assertEqual(self.b.buffers_mercado()[nome], atual, nome)
            if 0x4e2900 <= endereco < 0x4e3000:
                janela[endereco - 0x4e2900:endereco - 0x4e2900 + tamanho] = atual
        janela[BASE_ACEITES - 0x4e2900:BASE_ACEITES - 0x4e2900 + 4] = o.aceites
        janela[BASE_RECURSOS - 0x4e2900:BASE_RECURSOS - 0x4e2900 + 128] = m.economia.memoria
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4e2900, 0x700)), bytes(janela))

    def comparar(self, o, j=0, p=1, entrada=0x461bea, carregar=True):
        from emulador import RETORNO, PILHA
        if carregar:
            self.b.carregar_ordem(o)
        {0x461bea:o.ordenar, 0x461621:o.receber, 0x46189a:o.entregar}[entrada](j, p)
        regs = self.b.chamar_ordem(entrada, j | 0xabcd0000, p | 0xface0000)
        self.assertEqual((regs['EIP'], regs['ESP']), (RETORNO, PILHA + 0x8004))
        self.conferir(o)

    def test_1024_noncanonical_approval_and_type_gates(self):
        for flag in range(256):
            for outro in (0, 255):
                for tipo in (1, 2):
                    o = preparar(tipo_j=tipo)
                    o.aceites[0], o.aceites[1] = flag, outro
                    self.comparar(o)

    def test_512_alias_gates(self):
        for flag in range(256):
            for tipo in (1, 2):
                o = preparar(j=0, p=0, tipo_j=tipo, tipo_p=tipo)
                o.aceites[0] = flag
                self.comparar(o, 0, 0)

    def test_384_seeded_buffers_and_all_player_pairs(self):
        for n in range(384):
            j, p = n % 4, n // 4 % 4
            o = preparar(j, p)
            for nome, (_, tamanho) in BUFFERS.items():
                getattr(o.mercado, nome)[:] = self.rng.randbytes(tamanho)
            o.mercado.unidades_oferecidas[p * 52:(p + 1) * 52] = bytes(52)
            o.mercado.unidades_pedidas[p * 52:(p + 1) * 52] = bytes(52)
            o.mundo.economia.memoria[:] = self.rng.randbytes(128)
            o.mundo.estruturas[:] = self.rng.randbytes(276)
            o.mercado.jogadores[:] = self.rng.randbytes(80)
            for jogador in range(4):
                o.mercado.jogadores[jogador * 20 + 1] = (0, 1, 2, 255)[(n + jogador) % 4]
                o.mundo.capacidades.configurar(jogador, n % 3, 1 + n % 100)
            o.aceites[:] = self.rng.randbytes(4)
            self.comparar(o, j, p)

    def test_256_direct_callers(self):
        for entrada in (0x461621, 0x46189a):
            for n in range(128):
                j, p = n % 4, n // 4 % 4
                o = preparar(j, p, n % 5, n % 3)
                proposta(o, p, (n, 65535 - n, n % 2), (n % 2, 65535 - n, n))
                o.aceites[:] = self.rng.randbytes(4)
                self.comparar(o, j, p, entrada)

    def test_104_pending_unit_paths_preserve_prior_effects(self):
        for fase in ('prend', 'donne'):
            for tipo in range(26):
                for quantidade in (1, 65535):
                    o = preparar()
                    bloco = o.mercado.unidades_oferecidas if fase == 'prend' else o.mercado.unidades_pedidas
                    w(bloco, 52 + tipo * 2, quantidade)
                    self.b.carregar_ordem(o)
                    with self.assertRaises(TrocaUnidadesMercadoPendente) as ctx:
                        o.ordenar(0, 1)
                    regs = self.b.chamar_ordem(0x461bea, 0, 1)
                    self.assertEqual(regs['EIP'], ctx.exception.endereco)
                    self.assertEqual(regs['EDX'], quantidade)
                    self.conferir(o)

    def test_12_divide_exceptions_and_prior_consumed_entries(self):
        from emulador import unicorn, x86
        for fase in ('prend', 'donne'):
            for recurso in range(3):
                for armazens in (1, 65535):
                    if self.b.execucoes:
                        self.nova_bancada()
                    o = preparar()
                    origem = 1 if fase == 'prend' else 0
                    o.mundo.capacidades.configurar(origem, armazens, 0)
                    q = tuple(3 if i >= recurso else 0 for i in range(3))
                    proposta(o, oferta=q if fase == 'prend' else (3, 5, 7), pedido=q)
                    self.b.carregar_ordem(o)
                    with self.assertRaises(ZeroDivisionError):
                        o.ordenar(0, 1)
                    with self.assertRaises(unicorn.UcError) as ctx:
                        self.b.chamar_ordem(0x461bea, 0, 1)
                    self.assertEqual(ctx.exception.errno, unicorn.UC_ERR_EXCEPTION)
                    self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_EIP), 0x423635)
                    self.b.excecoes_esperadas += 1
                    self.conferir(o)

    def test_exact_total_row_clear_rmi_write_order_and_debit_calls(self):
        o = preparar()
        self.comparar(o)
        escritas = [(ip, a, tam) for ip,a,tam,v in self.b.escritas if 0x461621 <= ip < 0x461c4f]
        esperado = [(0x461c04, BASE_ACEITES, 1)]
        for r in range(3):
            esperado += [(0x46187e, BASE_RECURSOS + r * 8 + 2, 2),
                         (0x461886, 0x4e2cfc + 6 + r * 2, 2),
                         (0x46188d, BASE_RECURSOS + r * 8, 2)]
        for r in range(3):
            esperado += [(0x461bc6, BASE_RECURSOS + 32 + r * 8 + 2, 2),
                         (0x461bce, 0x4e2d14 + 6 + r * 2, 2),
                         (0x461bd5, BASE_RECURSOS + 32 + r * 8, 2)]
        esperado += [(0x461c40, BASE_ACEITES, 1), (0x461c46, BASE_ACEITES + 1, 1)]
        self.assertEqual(escritas, esperado)
        self.assertEqual([(e['EBX'] & 255, e['EAX'] & 255, e['EDX'] & 65535)
                          for e in self.b.eventos if e['entrada'] == 0x4235bd],
                         [(1,0,3), (1,1,5), (1,2,7), (0,0,11), (0,1,13), (0,2,17)])

    def test_64_repeat_calls_consume_once(self):
        for n in range(16):
            o = preparar(tipo_j=2)
            for repeticao in range(4):
                self.comparar(o, carregar=repeticao == 0)
                self.assertEqual(sum(e['entrada'] == 0x4235bd for e in self.b.eventos), 3 if repeticao == 0 else 0)


if __name__ == '__main__':
    unittest.main()
