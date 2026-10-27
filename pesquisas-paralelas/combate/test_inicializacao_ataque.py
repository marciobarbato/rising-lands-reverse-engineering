"""Inicialização com bytes preexistentes, rastros de escrita e chamadas reais."""
import os
import random
import struct
import unittest

from animacao_disparo import BuscaAtaque, guardar, calcular_ataque
from inicializacao_ataque import (CaracteristicasTipo, caracterizar_tipo, definir_tipo,
    pedido_leitura_registro, preparar_apos_carga_missao, preparar_apos_carga_game,
    PROJETIL_POR_TIPO, QUADRO_POR_TIPO)

# Entrada externa explícita nos testes, conferida por EnginTypeGetCapacite x86
# dentro de EnginSetType. Não é uma implementação nova da economia.
CAPACIDADES = {5: 1, 6: 1, 7: 1, 11: 1, 12: 2, 13: 5, 14: 1, 15: 3, 16: 1, 17: 6}


class ContratosInicializacao(unittest.TestCase):
    def test_preserva_campos_ausentes_e_subestado(self):
        u = bytearray([173] * 276)
        u[0], u[1] = 0, 14
        caracterizar_tipo(u, 0x1234, None)
        self.assertEqual((u[0x79], u[0x7a], u[0x8a], u[0x8b]), (173,) * 4)
        self.assertEqual(struct.unpack_from('<H', u, 0x102)[0], 0x34)
        self.assertEqual((u[0xda], u[0xdb]), (1, 8))

    def test_ordem_de_tipo_reseta_espera_preserva_fase(self):
        u = bytearray([173] * 276)
        u[0], u[2], u[0x8a] = 0, 1, 3
        busca = BuscaAtaque(7, 1, 1, 123)
        definir_tipo(u, 7, 0x1234, 9, 14, CaracteristicasTipo(0x105, 0x124, 0x178),
            lambda t: CAPACIDADES.get(t, 0), lambda *args: 0, busca)
        self.assertEqual((u[0x79], u[0x7a], u[0x8a], u[0x8b]), (173, 173, 3, 0))
        self.assertEqual((u[0xbb], u[0xb0]), (5, 36))
        self.assertEqual(busca, BuscaAtaque())

    def test_mago_modificador_e_wrap(self):
        u = bytearray(276)
        u[1] = 4
        caracterizar_tipo(u, 65535, lambda dono, tipo: 250)
        self.assertEqual((u[0xda], u[0x7a]), (4, 5))
        for dono in (4, 200):
            u[0] = dono
            caracterizar_tipo(u, 1, None)
            self.assertEqual(u[0xda], 10)

    def test_pedido_salvo_inclui_campos_sem_normalizar(self):
        self.assertEqual(pedido_leitura_registro(799), (799 * 276, 276))
        self.assertEqual(pedido_leitura_registro(0x10001), (276, 276))

    def test_carga_missao_sobrescreve_mago_e_recarga_game_preserva(self):
        u = bytearray([173] * 276)
        u[0], u[1], u[0x8a] = 0, 4, 2
        preparar_apos_carga_missao(u, CaracteristicasTipo(5, 36, 0x1234), lambda d, t: 99)
        self.assertEqual((u[0xda], u[0x8a], u[0x8b]), (10, 2, 173))
        self.assertEqual(struct.unpack_from('<H', u, 0x102)[0], 0x1234)
        u[0x79], u[0x7a], u[0x8a], u[0x8b] = 99, 88, 3, 77
        preparar_apos_carga_game(u)
        self.assertEqual((u[0x79], u[0x7a], u[0x8a], u[0x8b]), (99, 88, 3, 77))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Opcional: RISING_EMULAR=1')
class DiferencialInicializacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_inicializacao import BancadaInicializacao
        cls.b = BancadaInicializacao()
        # Tipos inválidos 26..255 leem além da tabela de 26 elementos. Seus
        # parâmetros sintéticos sobrepõem outros dados; restaurar entre testes.
        cls.dados_originais = bytes(cls.b.cpu.mem_read(0x4965ae, 256 * 50))

    def setUp(self):
        self.b.cpu.mem_write(0x4965ae, self.dados_originais)

    def test_caracteristicas_todos_tipos_preservacao_e_escritas(self):
        rng = random.Random(0x457350)
        for tipo in range(256):
            for padrao in (0, 255, None):
                u = bytearray([padrao] * 276) if padrao is not None else bytearray(rng.randbytes(276))
                u[0], u[1] = 0, tipo
                c = CaracteristicasTipo(0x1234, 0x2345, rng.randrange(65536))
                self.b.parametros_tipo(tipo, c, mod12=250)
                self.b.escrever_unidade(u, 7)
                antes = bytes(u)
                self.b.caracterizar(0xabcd0007)  # AX, não o EAX inteiro
                caracterizar_tipo(u, c.recarga, lambda dono, t: 250)
                with self.subTest(tipo=tipo, padrao=padrao):
                    self.assertEqual(self.b.ler_unidade(7), u)
                    self.assertEqual(u[0x8a:0x8c], antes[0x8a:0x8c])
                    self.assertTrue(all(campo in (0x79, 0x7a) for _, _, campo, _ in self.b.escritas_campos))
                    escritos = {campo: valor for _, _, campo, valor in self.b.escritas_campos}
                    self.assertEqual(escritos, {**({0x79: PROJETIL_POR_TIPO[tipo]} if tipo in PROJETIL_POR_TIPO else {}),
                        **({0x7a: QUADRO_POR_TIPO[tipo]} if tipo in QUADRO_POR_TIPO else {})})

    def test_mago_todos_modificadores_e_donos(self):
        for dono in (0, 1, 2, 3, 4, 200):
            for mod in range(256):
                u = bytearray([101] * 276)
                u[0], u[1] = dono, 4
                self.b.parametros_tipo(4, CaracteristicasTipo(0, 0, 0x8100), dono, mod12=mod)
                self.b.escrever_unidade(u)
                self.b.caracterizar(0)
                caracterizar_tipo(u, 0x8100, lambda d, t: mod)
                self.assertEqual(self.b.ler_unidade(), u)

    def test_definir_tipo_registro_inteiro_busca_e_callbacks(self):
        rng = random.Random(0x457b87)
        for tipo in (*range(26), 26, 255):
            for indice in (0, 7, 799):
                for estado in (0, 1, 4, 24):
                    for dono in (0, 4, 200):
                        u = bytearray(rng.randbytes(276))
                        u[0], u[2] = dono, estado
                        c = CaracteristicasTipo(rng.randrange(65536), rng.randrange(65536), rng.randrange(65536))
                        celula, direcao = rng.randrange(65536), rng.randrange(256)
                        mod1, mod12 = rng.randrange(256), rng.randrange(256)
                        busca = BuscaAtaque(rng.choice((indice, 65535)), 1, 1, 0x12345678)
                        self.b.preparar_busca(busca)
                        self.b.parametros_tipo(tipo, c, dono, mod1, mod12)
                        self.b.escrever_unidade(u, indice)
                        fase, proj, quadro = u[0x8a], u[0x79], u[0x7a]
                        self.b.definir(indice, celula, direcao, tipo)
                        chamadas = []
                        def capacidade(t):
                            chamadas.append(('capacidade', t))
                            return CAPACIDADES.get(t, 0)
                        def modificador(d, t, n):
                            chamadas.append(('modificador', d, t, n))
                            return mod1 if n == 1 else mod12
                        definir_tipo(u, indice, celula, direcao, tipo, c, capacidade, modificador, busca)
                        with self.subTest(tipo=tipo, indice=indice, estado=estado, dono=dono):
                            self.assertEqual(self.b.ler_unidade(indice), u)
                            self.assertEqual(self.b.ler_busca(), busca)
                            self.assertEqual((u[0x8a], u[0x8b]), (fase, 0))
                            self.assertEqual(u[0x79], PROJETIL_POR_TIPO.get(tipo, proj))
                            self.assertEqual(u[0x7a], QUADRO_POR_TIPO.get(tipo, quadro))
                            self.assertEqual(chamadas, ([('modificador', dono, tipo, 12)] if tipo == 4 and dono not in (4, 200) else [])
                                + [('capacidade', tipo)] + ([('modificador', dono, tipo, 1)] if dono not in (4, 200) else []))

    def test_caracterizar_sequencias_de_trocas_preservam_valores(self):
        rng = random.Random(0x797a)
        for origem in range(26):
            for destino in range(26):
                u = bytearray(rng.randbytes(276))
                u[0], u[1] = 0, origem
                self.b.escrever_unidade(u)
                for tipo in (origem, destino):
                    u[1] = tipo
                    self.b.cpu.mem_write(0x1000001, bytes([tipo]))
                    self.b.parametros_tipo(tipo, CaracteristicasTipo(5, 36, 0x178), mod12=255)
                    self.b.caracterizar(0)
                    caracterizar_tipo(u, 0x178, lambda d, t: 255)
                    self.assertEqual(self.b.ler_unidade(), u)

    def test_ordem_de_ataque_original_preserva_espera(self):
        from bancada_animacao import ANIMACAO
        from test_animacao_disparo import contexto
        for tipo in range(26):
            for espera in (0, 1, 20, 50, 255):
                ctx = contexto(tipo, subestado=3)
                u = ctx.unidades[0]
                u[2], u[0x8b] = 7, espera
                guardar(u, 0xc0, 65535)
                self.b.mundo(ctx.unidades)
                self.b.preparar_busca(ctx.busca)
                self.b.escritas_campos = []
                self.b.executar(0x445a36, ANIMACAO + [(0x445a36, 0x445af1)],
                    dict(EAX=0, EDX=5, EBX=0x2024))
                r = self.b.ler_unidade()
                self.assertEqual((r[0x79], r[0x7a], r[0x8b]), (u[0x79], u[0x7a], espera))
                self.assertEqual(r[0x8a], 3 if tipo in (5, 6, 7, 9, 10, 13) else 0)
                self.assertTrue(all(campo == 0x8a and valor == 0 for _, _, campo, valor in self.b.escritas_campos))

    def test_pedido_de_load_por_id_sem_filtro_de_subestado(self):
        from bancada_combate import UNIDADES
        for indice in (0, 1, 7, 799, 800, 65535):
            r = self.b.pedido_leitura(indice)
            offset, tamanho = pedido_leitura_registro(indice)
            self.assertEqual((r['EAX'], r['EDX']), (UNIDADES + offset, tamanho))
            self.assertEqual(r['EIP'], 0x458461)

    def test_inicializacao_seguida_de_disparo_original(self):
        from test_animacao_disparo import contexto
        from bancada_combate import RETORNO
        for tipo in range(26):
            ctx = contexto(tipo, subestado=1)
            u = ctx.unidades[0]
            # Quadro herdado 2 distingue ramos que não escrevem +7a.
            u[0x7a], u[0xa4], u[0xa9] = 2, 0, 0
            c = CaracteristicasTipo(10, 100, 100)
            self.b.mundo(ctx.unidades)
            self.b.preparar_busca(ctx.busca)
            self.b.parametros_tipo(tipo, c)
            self.b.caracterizar(0)
            caracterizar_tipo(u, 100, lambda d, t: 0)
            # Tick começa imediatamente antes do quadro de disparo configurado.
            from animacao_disparo import TIPOS_ANIMAM
            if tipo in TIPOS_ANIMAM:
                u[0xa9] = (u[0xa8] - 1) & 255
                u[0xa4] = (u[0x7a] - 1) % u[0xa6]
            else:
                u[0xa4], u[0xa9] = u[0x7a], 0
            guardar(u, 0x7c, struct.unpack_from('<H', u, 8)[0])
            self.b.escrever_unidade(u)
            r = self.b.passo_ataque(0)
            calcular_ataque(ctx, 0)
            self.assertEqual(r['EIP'], RETORNO)
            self.assertEqual(self.b.ler_unidade(), u)
            self.assertEqual(self.b.chamadas, ctx.chamadas)

    def test_pos_carga_missao_fases_2_3_preservadas(self):
        rng = random.Random(0x46acbf)
        for tipo in range(26):
            for estado in (0, 1, 4, 14, 24):
                for fase in (0, 1, 2, 3, 255):
                    u = bytearray(rng.randbytes(276))
                    u[0], u[1], u[2], u[0x8a] = rng.choice((0, 3, 4, 200)), tipo, estado, fase
                    c = CaracteristicasTipo(0x1234, 0x2345, 0x3456)
                    self.b.parametros_tipo(tipo, c, u[0], mod12=231)
                    self.b.escrever_unidade(u, 7)
                    espera = u[0x8b]
                    self.b.pos_carga_missao(7)
                    preparar_apos_carga_missao(u, c, lambda d, t: 231)
                    with self.subTest(tipo=tipo, estado=estado, fase=fase):
                        self.assertEqual(self.b.ler_unidade(7), u)
                        self.assertEqual((u[0x8a], u[0x8b]), (fase, espera))
                        self.assertTrue(all(campo in (0x79, 0x7a) for _, _, campo, _ in self.b.escritas_campos))

    def test_pos_carga_game_preserva_campos_e_nao_recaracteriza(self):
        rng = random.Random(0x46b01e)
        for tipo in range(26):
            for fase in range(256):
                u = bytearray(rng.randbytes(276))
                u[1], u[0x8a] = tipo, fase
                self.b.escrever_unidade(u, 799)
                self.b.pos_carga_game(799)
                preparar_apos_carga_game(u)
                self.assertEqual(self.b.ler_unidade(799), u)
                self.assertEqual(self.b.escritas_campos, [])

    def test_pedido_leitura_game_tamanho_do_cabecalho(self):
        from bancada_combate import UNIDADES
        for indice in (0, 7, 799, 65535):
            for tamanho in (0, 140, 272, 276, 65535):
                r = self.b.pedido_leitura_game(indice, tamanho)
                offset, n = pedido_leitura_registro(indice, tamanho)
                self.assertEqual((r['EAX'], r['EDX'], r['EIP']), (UNIDADES + offset, n, 0x458461))
