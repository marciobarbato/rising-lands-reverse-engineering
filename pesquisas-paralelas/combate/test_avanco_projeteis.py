"""Compara memória inteira e sequência de dano, RNG e filhos com o x86."""
import os
import random
import unittest

from projeteis import PoolProjeteis, u16, por16, por32
from avanco_projeteis import animar_projetil, infligir_dano_projetil, avancar_linear, TIPOS_LINEARES


class PoolObservado(PoolProjeteis):
    def definir(self, *args):
        self.trilha.append(('ProjectileSet', args))
        return super().definir(*args)


def modelo(dados):
    p = PoolObservado(bytearray(dados))
    p.trilha = []
    p.efeito_externo = lambda n, a: p.trilha.append((n, a))
    return p


class ContratosAvanco(unittest.TestCase):
    def test_ultimo_passo_nao_produz_dano_ate_proximo_despacho(self):
        p = modelo(bytes(5600))
        p.definir(0, 9, 0, 1, 1, 7, 3, 47, 16, 0)
        p.registro(0)[0x19] = 0  # isola o momento do impacto da emissão secundária
        p.trilha.clear()
        avancar_linear(p, 0)
        self.assertEqual((u16(p.registro(0), 0x34), p.registro(0)[2]), (0, 1))
        self.assertEqual(p.trilha, [])
        avancar_linear(p, 0)
        self.assertEqual(p.trilha, [('InfligeDegat', (1, 1, 7, 3, 0))])
        self.assertEqual(p.registro(0)[2], 0)

    def test_area_ordem_flags_e_modo29(self):
        p = modelo(bytes(5600))
        p.definir(0, 29, 0, 0, 2, 7, 31, 16, 16, 255)
        p.trilha.clear()
        infligir_dano_projetil(p, 0)
        self.assertEqual(p.trilha, [('InfligeDegat', (0, 2, 7, 31, 255)),
            ('InfligeDegat', (1, 4, 7, 29, 0)), ('InfligeDegat', (256, 4, 7, 29, 0)),
            ('InfligeDegat', (257, 4, 7, 29, 0))])

    def test_filho_perdido_sem_repeticao_e_rng_mesmo_sem_espaco(self):
        p = modelo(bytearray([1] * 5600))
        p.definir(37, 1, 0, 1, 1, 7, 3, 16, 16, 0)
        r = p.registro(37)
        r[3] = 14
        p.trilha.clear()
        avancar_linear(p, 37)
        self.assertEqual((r[3], r[0x19]), (15, 0))
        self.assertEqual(p.trilha, [])
        por16(r, 0x34, 0)
        marcadores = []
        avancar_linear(p, 37, lambda n: marcadores.append(n) or 2)
        self.assertEqual(marcadores, [0x30])
        self.assertEqual([x[0] for x in p.trilha], ['InfligeDegat'])
        self.assertEqual(r[2], 0)

    def test_aquecimento_animacao_e_tipo_pendente(self):
        p = modelo(bytes(5600))
        p.definir(0, 29, 0, 1, 1, 7, 3, 16, 16, 0)
        antes = bytes(p.memoria)
        avancar_linear(p, 0)
        self.assertEqual(p.memoria, antes)
        for _ in range(12):
            animar_projetil(p.registro(0), 0)
        self.assertEqual(p.registro(0)[0x18], 12)
        p.registro(0)[0] = 30
        antes = bytes(p.memoria)
        with self.assertRaises(NotImplementedError):
            avancar_linear(p, 0)
        self.assertEqual(p.memoria, antes)

    def test_backend_obrigatorio_preserva_escritas_anteriores(self):
        p = modelo(bytes(5600))
        p.definir(0, 1, 0, 0, 1, 7, 3, 16, 16, 0)
        with self.assertRaises(NotImplementedError):
            avancar_linear(p, 0)
        self.assertEqual((p.registro(0)[2], p.registro(0)[3]), (1, 1))
        self.assertEqual(p.trilha[-1], ('InfligeDegat', (0, 1, 7, 3, 0)))

    def test_deriva_dos_efeitos_e_area_de_dano_distintas(self):
        p = modelo(bytes(5600))
        p.definir(37, 20, 0x100, 0x100, 1, 7, 3, 16, 16, 0)
        p.trilha.clear()
        avancar_linear(p, 37, lambda _: 0)
        self.assertEqual([a[0] for n, a in p.trilha if n == 'InfligeDegat'],
                         [256, 257, 0, 1, 512, 513])
        self.assertEqual([a[2] for n, a in p.trilha if n == 'ProjectileSet'],
                         [0, 1, 255, 256, 510, 511])


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Opcional: RISING_EMULAR=1')
class DiferencialAvanco(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_avanco_projeteis import BancadaAvanco
        cls.b = BancadaAvanco()

    def preparar(self, p, seed=1, incremento=1, dimensoes=(256, 256)):
        self.b.pool(p.memoria)
        self.b.contexto_avanco(seed, incremento, dimensoes)
        p.trilha.clear()

    def conferir_avanco(self, p, indice=37):
        p.trilha.clear()
        self.b.avancar(indice)
        # Oráculo para a CONSULTA externa: o gerador original executa inteiro.
        # Não substitui CALL, retorno ou instrução na CPU; não duplica RNG Python.
        valores = iter(self.b.resultados_random)
        def consultar(marcador):
            valor = next(valores)
            p.trilha.append(('Random', (marcador, valor)))
            return valor
        avancar_linear(p, indice, consultar)
        self.assertEqual(list(valores), [], 'RNG nativo consumiu mais valores')
        self.assertEqual(self.b.trilha, p.trilha)
        self.assertEqual(self.b.ler_pool(), p.memoria)

    def test_animacao_todos_bytes_tipos_quadros_incrementos(self):
        rng = random.Random(0x46e52c)
        p = modelo(rng.randbytes(5600))
        for tipo in range(256):
            for quadro in (0, 1, 3, 7, 11, 12, 19, 20, 31, 32, 254, 255):
                for inc in (0, 1, 2, 255):
                    p.registro(37)[0], p.registro(37)[0x18] = tipo, quadro
                    p.registro(37)[2] = quadro & 1  # animar não filtra registros inativos
                    self.preparar(p, incremento=inc)
                    self.b.animar(37); animar_projetil(p.registro(37), inc)
                    self.assertEqual(self.b.ler_pool(), p.memoria, (tipo, quadro, inc))

    def test_dano_todos_tipos_bordas_e_dimensoes_ignoradas(self):
        rng = random.Random(0x46e5fe)
        for tipo in range(256):
            for alvo in (0, 1, 255, 256, 0x101, 0x80ff, 0xff00, 0xfffe, 0xffff):
                p = modelo(rng.randbytes(5600))
                r = p.registro(37)
                r[0], r[0x1f], r[0x22], r[0x23] = tipo, 1, tipo, tipo
                por16(r, 0x16, alvo); por16(r, 0x20, 7)
                self.preparar(p, dimensoes=(16, 12))
                self.b.infligir(37); infligir_dano_projetil(p, 37)
                self.assertEqual(self.b.trilha, p.trilha, (tipo, alvo))
                self.assertEqual(self.b.ler_pool(), p.memoria)

    def test_avanco_memoria_bruta_filhos_contadores_e_wrap(self):
        rng = random.Random(0x46ef66)
        for tipo in sorted(TIPOS_LINEARES):
            for caso in range(96):
                p = modelo(rng.randbytes(5600))
                for i in range(100):
                    p.registro(i)[2] = 1
                for i in ((), (0,), (99,), (0, 1, 2, 99))[caso % 4]:
                    p.registro(i)[2] = 0
                r = p.registro(37)
                r[0], r[0x1f], r[0x23] = tipo, 1, caso % 3
                r[3] = (0, 254, 255)[caso % 3]
                r[4] = (r[3] + 1) & 255 if caso % 2 else 17
                r[0x19] = caso % 3
                r[0x18] = (0, 11, 12, 19, 255)[caso % 5]
                por16(r, 0x20, 7)
                por16(r, 0x34, (0, 1, 2, 65535)[caso % 4])
                por32(r, 0x24, (0, 0xfffffff0)[caso % 2])
                self.preparar(p, seed=rng.randrange(2**32))
                with self.subTest(tipo=tipo, caso=caso):
                    self.conferir_avanco(p)

    def test_chegada_area_bordas_deriva_e_pool_saturado(self):
        rng = random.Random(0x46f4de)
        for tipo in (1, 20, 22, 29):
            for x in (0, 1, 127, 254, 255):
                for y in (0, 1, 127, 254, 255):
                    for livres in (0, 1, 9):
                        p = modelo(rng.randbytes(5600))
                        for i in range(100):
                            p.registro(i)[2] = int(i >= livres)
                        alvo = x + 256 * y
                        p.definir(37, tipo, alvo, alvo, 1, 7, 31, 16, 16, 1)
                        p.registro(37)[0x18] = 12
                        self.preparar(p, seed=(1, 2, 0xffffffff)[livres % 3])
                        with self.subTest(tipo=tipo, x=x, y=y, livres=livres):
                            self.conferir_avanco(p)

    def test_alias_registro_inativo_reusado_como_filho(self):
        for tipo in sorted(TIPOS_LINEARES):
            p = modelo(bytearray([1] * 5600))
            p.definir(37, tipo, 0x101, 0x105, 1, 7, 3, 16, 16, 0)
            r = p.registro(37)
            r[2], r[3], r[4], r[0x19], r[0x18] = 0, 0, 1, 1, 12
            self.preparar(p)
            self.conferir_avanco(p)
            self.assertEqual(p.trilha[0][0:1], ('ProjectileSet',))
            self.assertEqual(p.trilha[0][1][0:2], (37, tipo + 1))

    def test_sequencias_desde_set_ate_chegada(self):
        for tipo in sorted(TIPOS_LINEARES):
            for alvo in (0x0909, 0x0a0a, 0x0a0c, 0x0c08):
                p = modelo(bytes(5600))
                p.definir(37, tipo, 0x0a0a, alvo, 1, 7, 17, 16, 16, 1)
                self.preparar(p, seed=12345)
                limite = u16(p.registro(37), 0x34) + 14
                for _ in range(limite):
                    self.b.animar(37); animar_projetil(p.registro(37), 1)
                    self.conferir_avanco(p)
                    if not p.registro(37)[2]:
                        break
                else:
                    self.fail(f'Projétil {tipo} não terminou em {limite} despachos')
                self.assertEqual((u16(p.registro(37), 0xc), u16(p.registro(37), 0xe)),
                                 ((alvo & 255) * 32 + 16, (alvo >> 8) * 32 + 16))


if __name__ == '__main__':
    unittest.main()
