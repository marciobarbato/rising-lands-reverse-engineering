"""Selective market reset behavior and unmodified original x86 comparisons."""
import os
from pathlib import Path
import random
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from ciclo_mercado import CicloMercado, BUFFERS_CICLO
from mercado import Mercado, BUFFERS


def preparar(rng=None):
    rng = rng or random.Random(0x46634e)
    m = Mercado(jogadores=rng.randbytes(80),
                **{nome:rng.randbytes(tamanho) for nome, (_, tamanho) in BUFFERS.items()})
    m.economia.memoria[:] = rng.randbytes(128)
    return CicloMercado(m, **{nome:rng.randbytes(tamanho)
                             for nome, (_, tamanho) in BUFFERS_CICLO.items()})


def estado(c):
    return {**{nome:bytes(getattr(c, nome)) for nome in BUFFERS_CICLO},
            **{nome:bytes(getattr(c.mercado, nome)) for nome in BUFFERS},
            'jogadores':bytes(c.mercado.jogadores), 'economia':bytes(c.mercado.economia.memoria)}


def conferir_linha(teste, c, j):
    teste.assertEqual((c.bytes_2e7c[j], c.bytes_292c[j], c.bytes_2928[j], c.mercado.contatos[j]), (0, 1, 0, 255))
    for nome, bloco in (('indicadores', c.mercado.indicadores),
                        ('words_2938', c.words_2938), ('words_2940', c.words_2940)):
        teste.assertEqual(bytes(bloco[j*2:j*2+2]), bytes(2), nome)


class ExemplosCicloMercado(unittest.TestCase):
    def test_all_resets_share_market_and_preserve_proposals_prices_players_balances(self):
        c = preparar()
        antes = estado(c)
        contato = c.mercado.contatos
        self.assertIsNone(c.resetar_todos())
        self.assertIs(contato, c.mercado.contatos)
        for j in range(4):
            conferir_linha(self, c, j)
        for nome in BUFFERS.keys() - {'contatos', 'indicadores'} | {'jogadores', 'economia'}:
            self.assertEqual(estado(c)[nome], antes[nome], nome)

    def test_quit_captures_live_contact_before_reset_and_aliases_are_allowed(self):
        c = preparar()
        c.mercado.contatos[0] = 2
        self.assertIsNone(c.sair(0x100))
        conferir_linha(self, c, 0)
        conferir_linha(self, c, 2)
        c.mercado.contatos[3] = 3
        self.assertIsNone(c.sair(0x103))
        conferir_linha(self, c, 3)

    def test_invalid_first_index_has_no_writes(self):
        for indice in (4, 255, -1, 0x104):
            c = preparar()
            antes = estado(c)
            for chamar in (lambda:c.resetar(indice, 0), lambda:c.sair(indice)):
                with self.assertRaises(ValueError):
                    chamar()
                self.assertEqual(estado(c), antes)

    def test_invalid_second_index_retains_first_row_both_pair_and_quit(self):
        for k in (4, 255, -1, 0x104):
            c = preparar()
            esperado = preparar()
            esperado.resetar(1, 1)
            with self.assertRaises(ValueError):
                c.resetar(0x101, k)
            self.assertEqual(estado(c), estado(esperado))
        c = preparar()
        c.mercado.contatos[1] = 255
        with self.assertRaises(ValueError):
            c.sair(1)
        conferir_linha(self, c, 1)

    def test_constructor_copies_only_new_buffers_and_guards_lengths_names(self):
        m = Mercado()
        original = bytearray(b'\x77' * 4)
        c = CicloMercado(m, bytes_2e7c=original)
        self.assertIs(c.mercado, m)
        original[0] = 3
        self.assertEqual(c.bytes_2e7c[0], 0x77)
        self.assertEqual(c.words_2938, bytes(8))  # synthetic default, not loading
        for nome, (_, tamanho) in BUFFERS_CICLO.items():
            with self.assertRaises(ValueError):
                CicloMercado(m, **{nome:bytes(tamanho+1)})
        with self.assertRaises(TypeError):
            CicloMercado(m, unknown=bytes(4))

    def test_pair_keeps_other_players_and_approval_buffer(self):
        from construcoes import EconomiaConstrucoes
        from ordem_mercado import OrdemMercado
        mundo = EconomiaConstrucoes()
        mercado = Mercado(mundo.economia)
        ordem = OrdemMercado(mercado, mundo, aceites=b'\x02\x80\xff\x01')
        c = CicloMercado(mercado)
        mercado.contatos[:] = b'\x01\x00\x03\x02'
        c.bytes_2e7c[:] = b'\x11\x22\x33\x44'
        c.resetar(0, 1)
        self.assertEqual(c.bytes_2e7c[2:], b'\x33\x44')
        self.assertEqual(mercado.contatos, b'\xff\xff\x03\x02')
        self.assertEqual(ordem.aceites, b'\x02\x80\xff\x01')

    def test_second_quit_after_success_is_guarded_after_first_row_writes(self):
        c = preparar()
        c.mercado.contatos[0] = 1
        c.sair(0)
        antes = estado(c)
        with self.assertRaises(ValueError):
            c.sair(0)
        self.assertEqual(estado(c), antes)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional original x86: RISING_EMULAR=1')
class DiferencialCicloMercado(unittest.TestCase):
    bancadas = []

    def setUp(self):
        from bancada_ciclo_mercado import BancadaCicloMercado
        self.b = BancadaCicloMercado()
        type(self).bancadas.append(self.b)
        self.rng = random.Random(0x46027c)
        self.aceites = self.rng.randbytes(4)

    def carregar(self, c):
        # Seed gaps as well as fields. Neither executable nor model may erase them.
        self.b.cpu.mem_write(0x4e2900, self.rng.randbytes(0x700))
        self.b.cpu.mem_write(0x496f84, self.rng.randbytes(20))
        self.b.carregar_ciclo(c, self.aceites)

    def conferir(self, c):
        from bancada_mercado import JOGADORES
        for nome, atual in self.b.estado().items():
            self.assertEqual(atual, bytes(getattr(c.mercado, nome)), nome)
        for nome, atual in self.b.estado_ciclo().items():
            self.assertEqual(atual, bytes(getattr(c, nome)), nome)
        self.assertEqual(self.b.memoria(), bytes(c.mercado.economia.memoria))
        self.assertEqual(self.b.guardas(), (b'\xa6'*16, b'\x6a'*16))
        self.assertEqual(bytes(self.b.cpu.mem_read(JOGADORES - 8, 96)),
                         b'\xc3'*8 + bytes(c.mercado.jogadores) + b'\x3c'*8)
        janela = bytearray(self.b.vizinhos_antes)
        for campos, dono in ((BUFFERS, c.mercado), (BUFFERS_CICLO, c)):
            for nome, (endereco, tamanho) in campos.items():
                if 0x4e2900 <= endereco < 0x4e3000:
                    janela[endereco-0x4e2900:endereco-0x4e2900+tamanho] = getattr(dono, nome)
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4e2900, 0x700)), bytes(janela))
        contatos = bytearray(self.b.contatos_antes)
        contatos[8:12] = c.mercado.contatos
        self.assertEqual(bytes(self.b.cpu.mem_read(0x496f84, 20)), bytes(contatos))
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4e2968, 4)), self.aceites)

    def comparar(self, c, entrada, j=0, k=0, *, carregar=True, invalido=False):
        from emulador import RETORNO, PILHA
        if carregar:
            self.carregar(c)
        def modelo():
            if entrada == 0x46027c:
                return c.resetar_todos()
            if entrada == 0x46634e:
                return c.resetar(j, k)
            return c.sair(j)
        if invalido:
            with self.assertRaises(ValueError):
                modelo()
        else:
            self.assertIsNone(modelo())
        regs = self.b.chamar_ciclo(entrada, j, k, parar_indice=invalido)
        self.assertEqual(regs['EIP'], 0x466395 if invalido else RETORNO)
        if not invalido:
            self.assertEqual(regs['ESP'], PILHA+0x8004)
            for nome, valor in dict(EBX=0x92345678, ECX=0x3456789a,
                                    ESI=0x56789abc, EDI=0x6789abcd, EBP=0x789abcde).items():
                self.assertEqual(regs[nome], valor, nome)
            if entrada != 0x46634e:
                self.assertEqual(regs['EDX'], k & 0xffffffff)
        self.conferir(c)

    def test_32_all_resets_with_seeded_gaps_and_unrelated_buffers(self):
        for _ in range(32):
            self.comparar(preparar(self.rng), 0x46027c)

    def test_96_pairs_all_indices_aliases_and_high_register_bits(self):
        for _ in range(3):
            for j in range(4):
                for k in range(4):
                    for mascara in (0, 0xa5c37f00):
                        self.comparar(preparar(self.rng), 0x46634e, j|mascara, k|mascara)

    def test_32_quit_contacts_and_aliases(self):
        for j in range(4):
            for k in range(4):
                for mascara in (0, 0xfedcba00):
                    c = preparar(self.rng)
                    c.mercado.contatos[j] = k
                    self.comparar(c, 0x4663d6, j|mascara, 0xabcdef89)

    def test_1008_invalid_second_bytes_stop_after_complete_first_row(self):
        for j in range(4):
            for k in range(4, 256):
                self.comparar(preparar(self.rng), 0x46634e, j|0xaabbcc00, k|0xffeedd00, invalido=True)

    def test_8_invalid_quit_contacts_preserve_first_row(self):
        for j in range(4):
            for k in (4, 255):
                c = preparar(self.rng)
                c.mercado.contatos[j] = k
                self.comparar(c, 0x4663d6, j|0xccffaa00, 0x12345678, invalido=True)

    def test_96_persistent_reset_quit_all_sequences(self):
        for n in range(32):
            c = preparar(self.rng)
            j, k = n%4, (n//4)%4
            alvo = (j+1)%4
            c.mercado.contatos[alvo] = alvo
            self.comparar(c, 0x46634e, j, j)
            # Choose a still valid contact; prior native state persists.
            self.assertNotEqual(alvo, j)
            self.comparar(c, 0x4663d6, alvo, k, carregar=False)
            self.comparar(c, 0x46027c, carregar=False)

    def test_3_exact_original_write_orders_including_alias_duplicate_writes(self):
        primeiro = [('bytes_2e7c',0), ('bytes_292c',1), ('bytes_2928',0), ('contatos',255),
                    ('indicadores',0), ('words_2940',0), ('words_2938',0)]
        segundo = [('bytes_2e7c',0), ('contatos',255), ('bytes_292c',1), ('bytes_2928',0),
                   ('words_2938',0), ('words_2940',0), ('indicadores',0)]
        todos = [('bytes_2e7c',0), ('indicadores',0), ('contatos',255), ('bytes_292c',1),
                 ('bytes_2928',0), ('words_2940',0), ('words_2938',0)]
        for entrada, linhas in ((0x46027c, [(j, todos) for j in range(4)]),
                                 (0x46634e, [(2,primeiro),(2,segundo)]),
                                 (0x4663d6, [(2,primeiro),(2,segundo)])):
            c = preparar(self.rng)
            c.mercado.contatos[2] = 2
            observadas = []
            escrever = c._escrever
            def registrar(nome, jogador, valor):
                observadas.append((nome, jogador, valor))
                escrever(nome, jogador, valor)
            c._escrever = registrar
            self.comparar(c, entrada, 2, 2)
            campos = {**BUFFERS, **BUFFERS_CICLO}
            esperado = []
            for j, ordem in linhas:
                for nome, valor in ordem:
                    base, tamanho = campos[nome]
                    largura = tamanho//4
                    esperado.append((base+j*largura, largura, valor))
            self.assertEqual(self.b.escritas, esperado)
            self.assertEqual(observadas, [(nome,j,valor) for j,ordem in linhas for nome,valor in ordem])


if __name__ == '__main__':
    unittest.main()
