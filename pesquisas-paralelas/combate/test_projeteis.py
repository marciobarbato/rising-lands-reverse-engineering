"""Contratos e comparação dos 5600 bytes do pool com o x86 original."""
import os
import random
import struct
import unittest

from projeteis import PoolProjeteis, preparar_linha, calcular_linha, u16, por16, por32


def modelo(dados, raio=3):
    eventos = []
    def consultar(n):
        eventos.append(('SortilegeGetRayonEffet', (n,)))
        return raio
    p = PoolProjeteis(bytearray(dados), lambda n, a: eventos.append((n, a)), consultar)
    return p, eventos


class ContratosProjeteis(unittest.TestCase):
    def test_pool_cheio_reset_e_reuso(self):
        p = PoolProjeteis(bytearray([173] * 5600))
        self.assertEqual(p.livre(), 100)
        self.assertEqual(p.existe(99), 173)
        self.assertEqual(p.iniciar(26, 1, 2, 1, 7, 3, 16, 16, 0), 100)
        self.assertEqual(p.chamadas, [])
        p.resetar()
        self.assertEqual(p.livre(), 0)
        self.assertTrue(all(v == (0 if i % 56 == 2 else 173) for i, v in enumerate(p.memoria)))
        self.assertEqual(p.iniciar(5, 0, 1, 1, 7, 3, 16, 16, 0), 0)
        self.assertEqual(p.livre(), 1)
        self.assertEqual(p.registro(0)[4], 173)  # limiar não inicializado por tipo 5

    def test_efeitos_exigem_backend_e_preservam_ordem(self):
        p = PoolProjeteis(bytearray(5600))
        with self.assertRaises(NotImplementedError):
            p.iniciar(26, 1, 2, 1, 7, 3, 0, 0, 0)
        self.assertEqual(p.existe(0), 1)  # exceção Python não desfaz escritas anteriores
        eventos, raios = [], iter((65535, 7))
        def consultar(n):
            eventos.append(('raio', n))
            return next(raios)
        p.efeito_externo = lambda n, a: eventos.append((n, a))
        p.raio_magia = consultar
        p.definir(0, 28, 0, 0x1234, 255, 0xabcd, 31, 0, 0, 0)
        self.assertEqual(eventos, [('raio', 0), ('DecouvreTerrain', (0x1234, 1, 205)),
                                  ('raio', 0), ('IllumineTerrain', (0x1234, 7, 205))])

    def test_zero_distancia_e_limites_da_api(self):
        p = PoolProjeteis(bytearray(5600))
        p.definir(0, 1, 0x1234, 0x1234, 1, 7, 3, 16, 16, 1)
        r = p.registro(0)
        self.assertEqual((u16(r, 0x34), u16(r, 0x28)), (0, 12800))
        antes = bytes(r)
        calcular_linha(r)
        self.assertEqual(r, antes)
        for indice in (-1, 100, 65535):
            with self.assertRaises(ValueError):
                p.registro(indice)
        with self.assertRaises(ValueError):
            PoolProjeteis(bytearray(56))

    def test_passo_independe_de_atividade_e_campo04(self):
        r = bytearray(56)
        por16(r, 0xc, 16); por16(r, 0xe, 16); por16(r, 0x16, 1)
        preparar_linha(r)
        calcular_linha(r)
        self.assertEqual((u16(r, 0xc), u16(r, 0xe), u16(r, 0x34)), (17, 16, 31))
        self.assertEqual((r[2], r[4]), (0, 0))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Opcional: RISING_EMULAR=1')
class DiferencialProjeteis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_projeteis import BancadaProjeteis
        cls.b = BancadaProjeteis()

    def setUp(self):
        self.b.mundo([bytes(276) for _ in range(800)])

    def test_cadeia_ataque_emissao_pool_e_ultimo_slot(self):
        from animacao_disparo import calcular_ataque, TIPOS_ANIMAM
        from inicializacao_ataque import PROJETIL_POR_TIPO
        from test_animacao_disparo import contexto
        from bancada_combate import RETORNO
        rng = random.Random(0x451914)
        for tipo in range(26):
            for modo in (1, 5):
                for alvo_aereo in (False, True):
                    for livre in (0, 99, 100):
                        ctx = contexto(tipo, 1, modo)
                        u = ctx.unidades[0]
                        u[0x79] = PROJETIL_POR_TIPO.get(tipo, 1)
                        u[0xa4], u[0xa9], u[0x7a], u[0xa8] = (1 if tipo in TIPOS_ANIMAM else 2), 0, 2, 1
                        ctx.unidades[7][1] = 16 if alvo_aereo else 0
                        dados = bytearray(rng.randbytes(5600))
                        for i in range(100):
                            dados[i * 56 + 2] = int(i < livre)
                        p, eventos = modelo(dados)
                        def emitir(nome, args):
                            if nome != 'ProjectileInit':
                                self.fail(f'Efeito inesperado nesta cadeia: {nome}')
                            p.iniciar(*args)
                        ctx.efeito_externo = emitir
                        self.b.mundo(ctx.unidades)
                        self.b.preparar_busca(ctx.busca)
                        self.b.pool(dados)
                        r = self.b.passo_ataque(0)
                        calcular_ataque(ctx, 0)
                        with self.subTest(tipo=tipo, modo=modo, alvo_aereo=alvo_aereo, livre=livre):
                            self.assertEqual(r['EIP'], RETORNO)
                            self.assertEqual(self.b.ler_pool(), p.memoria)
                            self.assertEqual(self.b.ler_unidade(), ctx.unidades[0])
                            self.assertEqual(self.b.ler_busca(), ctx.busca)
                            self.assertEqual(self.b.chamadas, ctx.chamadas)
                            self.assertEqual(self.b.eventos, eventos)

    def test_reset_existe_livre_todas_posicoes(self):
        rng = random.Random(0x46e00a)
        dados = bytearray(rng.randbytes(5600))
        for i in range(100):
            dados[i * 56 + 2] = 255
        for livre in range(101):
            p, _ = modelo(dados)
            if livre < 100:
                p.registro(livre)[2] = 0
            self.b.pool(p.memoria)
            self.assertEqual(self.b.livre(), p.livre())
            if livre < 100:
                self.assertEqual(self.b.existe(livre | 0xabcd0000), p.existe(livre))
            self.assertEqual(self.b.ler_pool(), p.memoria)
        for ativo in range(256):
            p.registro(99)[2] = ativo
            self.b.pool(p.memoria)
            self.assertEqual(self.b.existe(99), ativo)
        self.b.resetar(); p.resetar()
        self.assertEqual(self.b.ler_pool(), p.memoria)

    def test_set_todos_tipos_flags_offsets_registro_inteiro(self):
        rng = random.Random(0x46e208)
        for tipo in range(256):
            for flag in (0, 1, 255):
                for dx, dy in ((16, 16), (-32768, 32767), (32767, -32768),
                               (rng.randrange(65536), rng.randrange(65536))):
                    p, eventos = modelo(rng.randbytes(5600), raio=tipo % 11)
                    self.b.pool(p.memoria, raio=tipo % 11)
                    args = (rng.choice((0, 7, 99)), tipo, rng.randrange(65536), rng.randrange(65536),
                            rng.randrange(256), rng.randrange(800), rng.randrange(256), dx, dy, flag)
                    self.b.definir(*args); p.definir(*args)
                    with self.subTest(args=args):
                        self.assertEqual(self.b.ler_pool(), p.memoria)
                        self.assertEqual(self.b.eventos, eventos)

    def test_init_todos_tipos_posicoes_e_pool_cheio(self):
        rng = random.Random(0x46e44c)
        for tipo in range(256):
            for livre in (0, 7, 99, 100):
                dados = bytearray(rng.randbytes(5600))
                for i in range(100):
                    dados[i * 56 + 2] = 255
                if livre < 100:
                    dados[livre * 56 + 2] = 0
                p, eventos = modelo(dados)
                self.b.pool(dados)
                args = (tipo, rng.randrange(65536), rng.randrange(65536), 255, 799, 255,
                        rng.randrange(65536), rng.randrange(65536), tipo % 3)
                self.b.iniciar(*args)
                with self.subTest(tipo=tipo, livre=livre):
                    self.assertEqual(p.iniciar(*args), livre)
                    self.assertEqual(self.b.ler_pool(), p.memoria)
                    self.assertEqual(self.b.eventos, eventos)

    def test_linha_limites_assinados_e_aleatorios(self):
        rng = random.Random(0x46e049)
        # Deltas para alvo central (16,16), incluindo ABS(-32768) e overflow.
        deltas = (-32768, -32767, -16385, -1, 0, 1, 16384, 32767)
        casos = [(16 - x, 16 - y, 0, f) for x in deltas for y in deltas for f in (0, 1, 255)]
        casos += [(rng.randrange(65536), rng.randrange(65536), rng.randrange(65536),
                   rng.randrange(256)) for _ in range(2048)]
        for x, y, alvo, flag in casos:
            p, _ = modelo(rng.randbytes(5600))
            r = p.registro(7)
            por16(r, 0xc, x); por16(r, 0xe, y); por16(r, 0x16, alvo); r[0x23] = flag
            self.b.pool(p.memoria)
            self.b.preparar_linha(7); preparar_linha(r)
            with self.subTest(x=x, y=y, alvo=alvo, flag=flag):
                self.assertEqual(self.b.ler_pool(), p.memoria)
            for _ in range(2):
                self.b.calcular_linha(7); calcular_linha(r)
                self.assertEqual(self.b.ler_pool(), p.memoria)

    def test_incremento_bruto_wrap_e_sinal_erro(self):
        rng = random.Random(0x46e4ca)
        for erro in (0, 1, 32767, 32768, 65535):
            for restante in (0, 1, 32768, 65535):
                for pos in (0, 0xffffffff, 0x7fffffff, 0x80000000):
                    p, _ = modelo(rng.randbytes(5600))
                    r = p.registro(99)
                    por16(r, 0x2e, erro); por16(r, 0x34, restante); por32(r, 8, pos)
                    self.b.pool(p.memoria)
                    self.b.calcular_linha(99); calcular_linha(r)
                    self.assertEqual(self.b.ler_pool(), p.memoria)

    def test_trajetos_completos_quadrantes_diagonal_e_empate(self):
        for tx in (8, 10, 12):
            for ty in (8, 10, 12):
                p, _ = modelo(bytes(5600))
                p.definir(0, 1, 0x0a0a, tx + ty * 256, 1, 7, 0, 16, 16, 1)
                self.b.pool(p.memoria)
                r = p.registro(0)
                passos = u16(r, 0x34)
                for _ in range(passos + 2):
                    self.b.calcular_linha(); calcular_linha(r)
                    self.assertEqual(self.b.ler_pool(), p.memoria)
                self.assertEqual((u16(r, 0xc), u16(r, 0xe)), (tx * 32 + 16, ty * 32 + 16))
                self.assertEqual((u16(r, 0x34), r[2]), (0, 1))


if __name__ == '__main__':
    unittest.main()
