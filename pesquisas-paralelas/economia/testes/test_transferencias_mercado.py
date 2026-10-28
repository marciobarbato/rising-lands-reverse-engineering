"""Transferências com estado parcial, créditos diretos e dependências reais."""
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(PASTA))
import test_retirada_recalculo as _comparacoes
from construcoes import EconomiaConstrucoes
from economia import BASE_RECURSOS
from mercado import Mercado, BUFFERS
from transferencias_mercado import TransferenciasMercado


def par(t, j, r, rmi, total):
    struct.pack_into('<HH', t.mundo.economia.memoria, j * 32 + r * 8, rmi, total)


def ler_par(t, j, r):
    return struct.unpack_from('<HH', t.mundo.economia.memoria, j * 32 + r * 8)


def proposta(t, j, oferta=(3, 5, 7), pedido=(11, 13, 17)):
    struct.pack_into('<3H', t.mercado.recursos_oferecidos, j * 6, *oferta)
    struct.pack_into('<3H', t.mercado.recursos_pedidos, j * 6, *pedido)


def preparar(j=0, k=1, tipo_j=1, tipo_k=1):
    mundo = EconomiaConstrucoes()
    mercado = Mercado(mundo.economia)
    mercado.jogadores[j * 20 + 1] = tipo_j
    mercado.jogadores[k * 20 + 1] = tipo_k
    t = TransferenciasMercado(mercado, mundo)
    for jogador in range(4):
        for r in range(4):
            par(t, jogador, r, 100, 100)
    proposta(t, j)
    return t


class ExemplosTransferenciasMercado(unittest.TestCase):
    def test_dois_sentidos_ordem_dos_ids_e_saldos_rmi(self):
        t = preparar()
        self.assertIsNone(t.transferir(0, 1))
        self.assertEqual([ler_par(t, 0, r) for r in range(3)], [(108, 108), (108, 108), (110, 110)])
        self.assertEqual([ler_par(t, 1, r) for r in range(3)], [(92, 92), (92, 92), (90, 90)])
        self.assertEqual((ler_par(t, 0, 3), ler_par(t, 1, 3)), ((100, 100), (100, 100)))

    def test_credito_sem_teto_aumenta_rmi_e_nao_estoque(self):
        t = preparar(tipo_j=0, tipo_k=0)
        proposta(t, 0, (10000, 65535, 1), (0, 0, 0))
        par(t, 1, 0, 1, 2)
        par(t, 1, 1, 1, 1)
        par(t, 1, 2, 65535, 65535)
        antes = t.mundo.economia.consultar_estoque(1)
        t.transferir(0, 1)
        self.assertEqual([ler_par(t, 1, r) for r in range(3)], [(10001, 10002), (0, 0), (0, 0)])
        self.assertEqual(t.mundo.economia.consultar_estoque(1), antes)

    def test_insuficiencia_nao_reduz_credito_ao_que_foi_debitado(self):
        t = preparar()
        proposta(t, 0, (50, 0, 0), (0, 0, 0))
        par(t, 0, 0, 2, 3)
        t.transferir(0, 1)
        self.assertEqual(ler_par(t, 0, 0), (0, 0))
        self.assertEqual(ler_par(t, 1, 0), (150, 150))

    def test_so_tipo1_e_debitado(self):
        for tipo in (0, 1, 2, 3, 255):
            t = preparar(tipo_j=tipo, tipo_k=tipo)
            t.transferir(0, 1)
            self.assertEqual(ler_par(t, 0, 0), (108, 108) if tipo == 1 else (111, 111))
            self.assertEqual(ler_par(t, 1, 0), (92, 92) if tipo == 1 else (103, 103))

    def test_usa_argumentos_e_linha_da_proposta_sem_consultar_contato(self):
        t = preparar(j=2, k=3)
        t.mercado.contatos[:] = b'\xff' * 4
        proposta(t, 3, (65535, 65535, 65535), (65535, 65535, 65535))
        t.transferir(0x102, 0x103)
        self.assertEqual(ler_par(t, 2, 0), (108, 108))
        self.assertEqual(ler_par(t, 3, 0), (92, 92))
        self.assertEqual(ler_par(t, 0, 0), (100, 100))

    def test_credito_independe_da_capacidade_e_nao_recalcula_destino(self):
        t = preparar(tipo_j=0, tipo_k=0)
        t.mundo.capacidades.configurar(0, 1, 0)
        t.mundo.capacidades.configurar(1, 1, 0)
        t.mundo.capacidades.escrever_nivel(0, 77)
        t.mundo.capacidades.escrever_nivel(1, 88)
        t.transferir(0, 1)
        self.assertEqual((t.mundo.capacidades.nivel(0), t.mundo.capacidades.nivel(1)), (77, 88))
        self.assertEqual(ler_par(t, 1, 2), (107, 107))

    def test_quantidade_zero_ainda_debita_e_recalcula(self):
        t = preparar()
        proposta(t, 0, (0, 0, 0), (0, 0, 0))
        par(t, 0, 1, 0, 100)
        t.mundo.capacidades.configurar(0, 1, 100)
        t.mundo.capacidades.escrever_nivel(0, 99)
        t.transferir(0, 1)
        self.assertEqual(t.mundo.capacidades.nivel(0), 7)
        self.assertEqual(ler_par(t, 0, 1), (0, 100))

    def test_falha_na_oferta_deixa_primeiro_debito_sem_credito(self):
        t = preparar()
        t.mundo.capacidades.configurar(0, 1, 0)
        with self.assertRaises(ZeroDivisionError):
            t.transferir(0, 1)
        self.assertEqual(ler_par(t, 0, 0), (97, 97))
        self.assertEqual(ler_par(t, 0, 1), (100, 100))
        self.assertEqual([ler_par(t, 1, r) for r in range(3)], [(100, 100)] * 3)

    def test_falha_no_pedido_preserva_oferta_inteira_e_debito_parcial(self):
        t = preparar()
        t.mundo.capacidades.configurar(1, 1, 0)
        with self.assertRaises(ZeroDivisionError):
            t.transferir(0, 1)
        self.assertEqual([ler_par(t, 0, r) for r in range(3)], [(97, 97), (95, 95), (93, 93)])
        self.assertEqual([ler_par(t, 1, r) for r in range(3)], [(92, 92), (105, 105), (107, 107)])

    def test_nao_limpa_proposta_repetir_repete_efeitos(self):
        t = preparar(tipo_j=0, tipo_k=0)
        antes = {n: bytes(getattr(t.mercado, n)) for n in BUFFERS}
        t.transferir(0, 1)
        t.transferir(0, 1)
        self.assertEqual(ler_par(t, 0, 0), (122, 122))
        self.assertEqual(ler_par(t, 1, 0), (106, 106))
        self.assertEqual({n: bytes(getattr(t.mercado, n)) for n in BUFFERS}, antes)

    def test_mesmo_jogador_nao_e_retorno_sem_efeito(self):
        t = preparar(j=0, k=0)
        par(t, 0, 0, 0, 1)
        t.transferir(0, 0)
        self.assertEqual(ler_par(t, 0, 0), (11, 11))

    def test_guardas_e_identidade_do_saldo_compartilhado(self):
        t = preparar()
        with self.assertRaises(ValueError):
            TransferenciasMercado(Mercado(), t.mundo)
        antes = bytes(t.mundo.economia.memoria)
        for j, k in ((4, 0), (0, 255), (-1, 1)):
            with self.assertRaises(ValueError):
                t.transferir(j, k)
        self.assertEqual(t.mundo.economia.memoria, antes)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: usar --emular')
class DiferencialTransferenciasMercado(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_transferencias_mercado import BancadaTransferenciasMercado
        cls.b = BancadaTransferenciasMercado()

    def setUp(self):
        self.rng = random.Random(0x4663eb)
        self.b.sujeira_pilha = None

    def conferir(self, t):
        from bancada_mercado import JOGADORES
        _comparacoes.DiferencialRetiradaRecalculo.conferir(self, t.mundo)
        for nome, atual in self.b.buffers_mercado().items():
            self.assertEqual(atual, bytes(getattr(t.mercado, nome)), nome)
        self.assertEqual(bytes(self.b.cpu.mem_read(JOGADORES - 8, 96)),
                         b'\xc3' * 8 + bytes(t.mercado.jogadores) + b'\x3c' * 8)
        esperado = bytearray(self.b.vizinhos_antes)
        for nome, (endereco, tamanho) in BUFFERS.items():
            if 0x4e2900 <= endereco < 0x4e3000:
                esperado[endereco - 0x4e2900:endereco - 0x4e2900 + tamanho] = getattr(t.mercado, nome)
        esperado[BASE_RECURSOS - 0x4e2900:BASE_RECURSOS - 0x4e2900 + 128] = t.mundo.economia.memoria
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4e2900, 0x700)), esperado)

    def transferir(self, t, j, k, *, carregar=True):
        from emulador import RETORNO, PILHA
        if carregar:
            self.b.carregar_transferencia(t)
        t.transferir(j, k)
        regs = {n: self.rng.getrandbits(32) for n in ('EBX', 'ECX', 'ESI', 'EDI', 'EBP')}
        atual = self.b.chamar(0x4663eb, (j & 255) | self.rng.getrandbits(24) << 8,
                              (k & 255) | self.rng.getrandbits(24) << 8, regs)
        self.assertEqual((atual['EIP'], atual['ESP']), (RETORNO, PILHA + 0x8004))
        for nome, valor in regs.items():
            self.assertEqual(atual[nome], valor, nome)
        self.conferir(t)
        j, k = j & 255, k & 255
        esperado, debitos = [], []
        for pagador, tabela in ((j, t.mercado.recursos_oferecidos), (k, t.mercado.recursos_pedidos)):
            for r in range(3):
                esperado.append(0x46d817)
                if t.mercado.tipo_jogador(pagador) == 1:
                    esperado += [0x4235bd, 0x46792c]
                    if t.mundo.capacidades.parametros(pagador)[0]:
                        esperado.append(0x46769d)
                    debitos.append((pagador, r, struct.unpack_from('<H', tabela, j * 6 + r * 2)[0]))
        self.assertEqual([e['entrada'] for e in self.b.eventos], esperado)
        self.assertEqual([(e['EBX'] & 255, e['EAX'] & 255, e['EDX'] & 65535)
                          for e in self.b.eventos if e['entrada'] == 0x4235bd], debitos)
        creditos = [(eip, endereco, tamanho) for eip, endereco, tamanho, _ in self.b.escritas
                    if 0x4663eb <= eip < 0x466533]
        self.assertEqual(creditos,
                         [(eip, BASE_RECURSOS + k * 32 + r * 8 + off, 2)
                          for r in range(3) for eip, off in ((0x46643f, 2), (0x466449, 0))]
                         + [(eip, BASE_RECURSOS + j * 32 + r * 8 + off, 2)
                            for r in range(3) for eip, off in ((0x4664cd, 0), (0x4664dc, 2))])
        permitidas = {(BASE_RECURSOS + p * 32 + r * 8 + o, 2)
                      for p in (j, k) for r in range(3) for o in (0, 2)}
        permitidas.update((0x4dfb30 + p * 6, 1) for p in (j, k))
        self.assertTrue(all((a, tam) in permitidas for _, a, tam, _ in self.b.escritas))

    def test_1024_estados_arbitrarios_e_pilha_suja(self):
        for n in range(1024):
            j, k = n % 4, n // 4 % 4
            t = preparar(j, k)
            t.mundo.economia.memoria[:] = self.rng.randbytes(128)
            t.mundo.capacidades.memoria[:] = self.rng.randbytes(24)
            t.mundo.estruturas[:] = self.rng.randbytes(276)
            t.mundo.terreno.tipos[:] = b'\xa5' * 65536
            t.mundo.terreno.quantidades[:] = b'\x5a' * 65536
            for nome, (_, tamanho) in BUFFERS.items():
                getattr(t.mercado, nome)[:] = self.rng.randbytes(tamanho)
            t.mercado.jogadores[:] = self.rng.randbytes(80)
            t.mercado.jogadores[j * 20 + 1] = (0, 1, 2, 3, 255)[n % 5]
            t.mercado.jogadores[k * 20 + 1] = (1, 0, 1, 255)[n % 4]
            for p in range(4):
                count = (0, 1, 2, 255, 65535)[(n + p) % 5]
                t.mundo.capacidades.configurar(p, count, (1, 2, 100, 65535)[(n + p) % 4] if count else 0)
            self.b.sujeira_pilha = (None, 0xa5, 0xff, 0x42)[n % 4]
            self.transferir(t, j, k)

    def test_512_tipos_em_cada_lado(self):
        for tipo in range(256):
            for lado in range(2):
                t = preparar(tipo_j=tipo if lado == 0 else 1, tipo_k=tipo if lado == 1 else 1)
                t.mundo.capacidades.configurar(0, 1, 100)
                t.mundo.capacidades.configurar(1, 2, 100)
                self.transferir(t, 0, 1)

    def test_255_tipos_sem_debito_ignoram_capacidade_zero(self):
        for tipo in range(256):
            if tipo == 1:
                continue
            t = preparar(tipo_j=tipo, tipo_k=tipo)
            t.mundo.capacidades.configurar(0, 1, 0)
            t.mundo.capacidades.configurar(1, 65535, 0)
            self.transferir(t, 0, 1)

    def test_128_limites_de_saldo_quantidade_e_tipo(self):
        for tj, tk in ((0, 0), (0, 1), (1, 0), (1, 1)):
            for q in (0, 1, 100, 9999, 10000, 32768, 65534, 65535):
                for saldo in (0, 1, 9999, 65535):
                    t = preparar(tipo_j=tj, tipo_k=tk)
                    proposta(t, 0, (q, q, q), (65535 - q,) * 3)
                    for p in range(2):
                        for r in range(3):
                            par(t, p, r, 65535 - saldo, saldo)
                    self.transferir(t, 0, 1)

    def test_64_casos_mesmo_jogador(self):
        for j in range(4):
            for tipo in (0, 1, 2, 255):
                for q in (0, 1, 10000, 65535):
                    t = preparar(j, j, tipo, tipo)
                    proposta(t, j, (q, q, q), (65535 - q,) * 3)
                    t.mundo.capacidades.configurar(j, 1, 100)
                    self.transferir(t, j, j)

    def test_32_sequencias_repetidas_sem_limpar(self):
        for n in range(32):
            j, k = n % 4, n // 4 % 4
            t = preparar(j, k, n % 2, n // 2 % 2)
            self.transferir(t, j, k)
            self.transferir(t, j, k, carregar=False)

    def test_32_ciclos_avaliacao_transferencia_consultas(self):
        for n in range(32):
            j, k = n % 4, n // 4 % 4
            t = preparar(j, k, n % 3, n // 3 % 3)
            t.mercado.contatos[j] = k
            t.mercado.precos_recursos[:] = bytes((2, 1, 1))
            self.b.carregar_transferencia(t)
            t.mercado.avaliar(j)
            self.b.chamar(0x466bac, j)
            self.conferir(t)
            avaliado = bytes(t.mercado.indicadores), bytes(t.mercado.diferenca)
            self.transferir(t, j, k, carregar=False)
            for p in (j, k):
                for r in range(3):
                    atual = self.b.chamar(0x462a58, r, p)
                    self.assertEqual(atual['EAX'], t.mercado.quantidade_recurso(p, r))
                    self.conferir(t)
            t.mercado.avaliar(j)
            self.b.chamar(0x466bac, j)
            self.conferir(t)
            self.assertEqual((t.mercado.indicadores, t.mercado.diferenca), avaliado)

    def test_56_falhas_primeiro_ou_segundo_sentido_inclusive_zero(self):
        from bancada_transferencias_mercado import BancadaTransferenciasMercado
        from emulador import unicorn, x86
        for j in range(4):
            for k in range(4):
                for fase in (0, 1):
                    if j == k and fase == 1:
                        continue  # Mesmo jogador falha já na primeira fase.
                    for zero in (False, True):
                        t = preparar(j, k)
                        t.mundo.capacidades.configurar(j if fase == 0 else k, 1, 0)
                        if zero:
                            proposta(t, j, (0, 0, 0), (0, 0, 0))
                        anterior = self.b
                        type(self).b = BancadaTransferenciasMercado()
                        self.b.execucoes = anterior.execucoes
                        self.b.excecoes_esperadas = anterior.excecoes_esperadas
                        self.b.carregar_transferencia(t)
                        with self.assertRaises(ZeroDivisionError):
                            t.transferir(j, k)
                        with self.assertRaises(unicorn.UcError) as erro:
                            self.b.chamar(0x4663eb, j, k)
                        self.assertEqual(erro.exception.errno, unicorn.UC_ERR_EXCEPTION)
                        self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_EIP), 0x423635)
                        self.b.excecoes_esperadas += 1
                        self.conferir(t)
                        creditos = [e for e in self.b.escritas if 0x4663eb <= e[0] < 0x466533]
                        self.assertEqual(len(creditos), 0 if fase == 0 else 6)
                        debitos = [e for e in self.b.eventos if e['entrada'] == 0x4235bd]
                        self.assertEqual(len(debitos), 1 if fase == 0 else 4)
        anterior = self.b
        type(self).b = BancadaTransferenciasMercado()
        self.b.execucoes = anterior.execucoes
        self.b.excecoes_esperadas = anterior.excecoes_esperadas
