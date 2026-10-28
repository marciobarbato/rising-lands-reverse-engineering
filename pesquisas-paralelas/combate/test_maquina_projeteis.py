"""Despacho completo e varreduras, com efeitos sintéticos explícitos e x86 real."""
import os
import random
import unittest

from projeteis import por16, u16
from maquina_projeteis import MaquinaProjeteis
from test_avanco_projeteis import PoolObservado


class MaquinaObservada(MaquinaProjeteis):
    def avancar(self, indice):
        self.indice_atual = indice
        self.avancos.append(indice)
        return super().avancar(indice)


def modelo(dados, tempo=32, raio=3):
    p = PoolObservado(bytearray(dados))
    p.trilha = []
    m = MaquinaObservada(p, campo_4dfb44=173)
    m.avancos, m.atividades, m.indice_atual = [], [], 37
    m.explosoes, m.quadros = bytearray(65536), bytearray([173] * 65536)
    def consulta(nome, valor):
        def ler(i):
            p.trilha.append((nome, (i,)))
            return valor
        return ler
    m.tempo_magia = consulta('SortilegeGetTempsFin', tempo)
    p.raio_magia = consulta('SortilegeGetRayonEffet', raio)
    def efeito(nome, args):
        p.trilha.append((nome, args))
        if nome in ('CreerExplosion', 'EteintTerrain'):
            m.atividades.append((nome, p.registro(m.indice_atual)[2]))
        if nome == 'CreerExplosion':
            # Backend apenas de teste; mesmos dois buffers sintéticos do x86.
            celula, tipo = args
            if not m.explosoes[celula]:
                m.explosoes[celula], m.quadros[celula] = tipo, 0
    p.efeito_externo = efeito
    return m


class ContratosMaquina(unittest.TestCase):
    def test_circulo30_sem_dano_central_duplicado(self):
        m = modelo(bytearray([1] * 5600))
        m.pool.definir(37, 30, 0x8080, 0x8080, 1, 7, 3, 16, 16, 255)
        m.pool.registro(37)[0x18] = 12
        m.pool.trilha.clear()
        consultas = []
        m.aleatorio = lambda n: consultas.append(n) or 0
        m.avancar(37)
        danos = [args for n, args in m.pool.trilha if n == 'InfligeDegat']
        self.assertEqual((len(danos), len(consultas), m.campo_4dfb44), (149, 149, 15))
        self.assertEqual(sum(a[0] == 0x8080 for a in danos), 1)
        self.assertTrue(all(a[1:] == (4, 7, 30, 0) for a in danos))
        self.assertEqual(m.pool.registro(37)[2], 0)

    def test_tipo33_filho_destino_antigo_dano_destino_novo(self):
        m = modelo(bytes(5600))
        m.pool.definir(37, 33, 0xa0a, 0xa0a, 1, 7, 3, 0, 0, 0)
        m.pool.registro(37)[0x18] = 20
        valores = iter((0, 0, 2, 1))
        pedidos = []
        m.aleatorio = lambda n: pedidos.append(n) or next(valores)
        m.pool.trilha.clear()
        m.avancar(37)
        self.assertEqual(pedidos, [0x29, 0x2a, 0x2b, 0x2c])
        self.assertEqual(m.pool.trilha, [('ProjectileSet', (0, 7, 0x90b, 0xa0a, 1, 7, 3, 0, 0, 0)),
                                        ('InfligeDegat', (0x90b, 1, 7, 3, 0))])
        self.assertEqual(u16(m.pool.registro(37), 0x16), 0x90b)

    def test_temporarios_ordem_desativacao_e_igualdade(self):
        for tipo, atividade in ((6, 0), (25, 1)):
            m = modelo(bytes(5600))
            m.pool.definir(37, tipo, 1, 2, 1, 7, 3, 0, 0, 0)
            m.aleatorio = lambda _: 5
            m.pool.registro(37)[0x18] = 33
            m.avancar(37)
            self.assertEqual(m.pool.registro(37)[2], 1)
            m.pool.registro(37)[0x18] = 32
            m.avancar(37)
            self.assertEqual(m.atividades, [('CreerExplosion', atividade)])
            self.assertEqual((m.explosoes[2], m.pool.registro(37)[2]), (61, 0))

    def test_tipo28_tempo_word_e_atacante_byte(self):
        m = modelo(bytes(5600), tempo=65535)
        p = m.pool.registro(37)
        p[0], p[2], p[0x18] = 28, 1, 255
        por16(p, 0x16, 0x1234); por16(p, 0x20, 0xabcd)
        m.avancar(37)
        self.assertEqual(m.pool.trilha, [('SortilegeGetTempsFin', (0,))])
        self.assertEqual(p[2], 1)
        m.tempo_magia = lambda _: 255
        m.avancar(37)
        self.assertEqual(m.pool.trilha[-1], ('EteintTerrain', (0x1234, 3, 205)))
        self.assertEqual(p[2], 0)

    def test_calcul_30_passagens_portao_e_inativos(self):
        for portao, passos in ((0, 30), (1, 29), (255, 29)):
            m = modelo(bytes(5600))
            m.pool.definir(37, 2, 0, 0x101, 1, 7, 3, 16, 16, 0)
            p = m.pool.registro(37)
            p[1], p[0x19] = portao, 0
            m.pool.registro(99)[1] = 255
            m.calcular(1)
            self.assertEqual((p[0x18], p[3], u16(p, 0x34)), (1, passos, 32 - passos))
            self.assertEqual(m.pool.registro(99)[1], 0)

    def test_falta_rng_preserva_desativacao_anterior(self):
        m = modelo(bytes(5600))
        m.pool.definir(37, 6, 0, 0, 1, 7, 3, 0, 0, 0)
        m.pool.registro(37)[0x18] = 32
        with self.assertRaises(NotImplementedError):
            m.avancar(37)
        self.assertEqual(m.pool.registro(37)[2], 0)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Opcional: RISING_EMULAR=1')
class DiferencialMaquina(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_maquina_projeteis import BancadaMaquinaProjeteis
        cls.b = BancadaMaquinaProjeteis()

    def preparar(self, m, seed=1, incremento=1, tempo=32, raio=3):
        self.b.pool(m.pool.memoria)
        self.b.contexto_maquina(seed, incremento, tempo, raio, m.campo_4dfb44)
        m.pool.trilha.clear()

    def conferir(self, m, indice=37, calcular=False, incremento=1):
        m.pool.trilha.clear(); m.atividades.clear(); m.avancos.clear()
        if calcular:
            self.b.calcular()
        else:
            self.b.avancar_completo(indice)
        resultados = iter(self.b.resultados_random)
        def consultar(marcador):
            valor = next(resultados)
            m.pool.trilha.append(('Random', (marcador, valor)))
            return valor
        m.aleatorio = consultar
        if calcular:
            m.calcular(incremento)
        else:
            m.avancar(indice)
        self.assertEqual(list(resultados), [])
        self.assertEqual(self.b.trilha, m.pool.trilha)
        self.assertEqual(self.b.indices_avanco, m.avancos)
        self.assertEqual(self.b.atividades_efeitos, m.atividades)
        self.assertEqual(self.b.campo_tipo30(), m.campo_4dfb44)
        self.assertEqual(self.b.ler_explosoes(), (m.explosoes, m.quadros))
        self.assertEqual(self.b.ler_pool(), m.pool.memoria)

    def test_despacho_todos_bytes_tipo_e_quadros(self):
        rng = random.Random(0x46eaf8)
        for tipo in range(256):
            for quadro in (0, 7, 8, 15, 16, 19, 20, 31, 32, 255):
                m = modelo(rng.randbytes(5600))
                for i in range(100):
                    m.pool.registro(i)[2] = 1
                p = m.pool.registro(37)
                p[0], p[2], p[0x18], p[0x19], p[0x1f], p[0x23] = tipo, quadro & 1, quadro, 0, 1, 0
                por16(p, 0x20, 7); por16(p, 0x34, 1)
                self.preparar(m, seed=tipo + 1)
                with self.subTest(tipo=tipo, quadro=quadro):
                    self.conferir(m)

    def test_tipo30_circulo_cantos_recorte_e_pool_cheio(self):
        for alvo in (0, 7, 0x707, 0x808, 0x8080, 0xff, 0xff00, 0xffff, 0xf8f8):
            for livres in (0, 99):
                m = modelo(bytearray([173] * 5600))
                for i in range(100):
                    m.pool.registro(i)[2] = int(i >= livres)
                m.pool.definir(99, 30, alvo, alvo, 1, 7, 31, 16, 16, 255)
                m.pool.registro(99)[0x18] = 12
                self.preparar(m, seed=alvo + 1)
                with self.subTest(alvo=alvo, livres=livres):
                    self.conferir(m, indice=99)
                pedidos = [a for n, a in m.pool.trilha if n == 'InfligeDegat']
                self.assertEqual(len(pedidos), sum(1 for y in range(256) for x in range(256)
                    if (x - (alvo & 255)) ** 2 + (y - (alvo >> 8)) ** 2 <= 49))

    def test_tipo33_sorteio_destino_e_saturacao(self):
        for alvo in (0, 0xff, 0xff00, 0xffff, 0x101, 0x8080):
            for seed in (0, 1, 2, 3, 0xffffffff):
                for livre in (False, True):
                    m = modelo(bytearray([173] * 5600))
                    m.pool.registro(0)[2] = 0 if livre else 1
                    m.pool.definir(37, 33, alvo, alvo, 1, 7, 3, 0, 0, 255)
                    m.pool.registro(37)[0x18] = 20
                    self.preparar(m, seed=seed)
                    self.conferir(m)

    def test_tipo28_tempo_16bits_e_extincao_sem_celulas(self):
        for tempo in (0, 1, 255, 256, 65535):
            for quadro in (0, 1, 8, 16, 20, 32, 255):
                for atacante in (7, 0xabcd):
                    m = modelo(bytes(5600), tempo=tempo, raio=7)
                    p = m.pool.registro(37)
                    p[0], p[2], p[0x18] = 28, 1, quadro
                    por16(p, 0x20, atacante); por16(p, 0x16, 0xffff)
                    self.preparar(m, tempo=tempo, raio=7)
                    self.conferir(m)

    def test_calcul_pool_inativo_e_criacoes_antes_depois_do_pai(self):
        rng = random.Random(0x46fc0f)
        m = modelo(rng.randbytes(5600))
        for i in range(100):
            m.pool.registro(i)[2] = 0
        self.preparar(m, incremento=255)
        self.conferir(m, calcular=True, incremento=255)
        for indice in (0, 50, 99):
            for portao in (0, 1, 255):
                m = modelo(bytes(5600))
                m.pool.definir(indice, 1, 0x101, 0x103, 1, 7, 3, 16, 16, 0)
                m.pool.registro(indice)[1] = portao
                self.preparar(m)
                for _ in range(3):
                    self.conferir(m, calcular=True)

    def test_calcul_misto_com_area_sorteio_luz_e_expiracao(self):
        m = modelo(bytes(5600), tempo=32)
        for indice, tipo, quadro in ((0, 30, 11), (3, 33, 19), (7, 28, 31),
                                    (15, 25, 31), (31, 6, 31), (60, 26, 7), (99, 14, 15)):
            p = m.pool.registro(indice)
            p[0], p[2], p[0x18], p[0x1f] = tipo, 1, quadro, 1
            por16(p, 0x16, 0x101); por16(p, 0x20, 7)
        self.preparar(m, seed=1234)
        self.conferir(m, calcular=True)


if __name__ == '__main__':
    unittest.main()
