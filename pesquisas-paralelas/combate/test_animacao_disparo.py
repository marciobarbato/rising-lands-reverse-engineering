"""Comparações dos subestados, registros inteiros e argumentos de disparo."""
import os
import random
import struct
import unittest

from alvos_alcance import palavra
from animacao_disparo import (anim_attaque_engin, anim_attaque_termine_engin, girar,
    saida_projetil, ContextoAtaque, BuscaAtaque, calcular_ataque, guardar, TIPOS_ANIMAM)
from mira_angular import mira_requerida
from test_alvos_alcance import unidade, tabela


def contexto(tipo=0, subestado=1, modo=5):
    u = unidade(tipo=tipo, atual=0x2020, passo=0x2021, estado=1)
    u[0xb7], u[0xb0], u[0x8a], u[0x78], u[0x79] = modo, 100, subestado, 1, 1
    u[0x90], u[0x91], u[0x94], u[0x93] = 9, 9, 17, 1
    u[0xa5], u[0xa6], u[0xa7], u[0xa8], u[0x7a] = 4, 4, 2, 2, 2
    u[0xa4], u[0xa9], u[0x8b], u[0xda] = 1, 1, 2, 1
    u[0xf4] = 255
    guardar(u, 0x102, 100)
    guardar(u, 0xb8, 7 if modo == 1 else 0x2024)
    guardar(u, 0xc0, 65535)
    us = tabela(u)
    # Alvo não colocado/ativo: o despacho CalculAttaqueEngin é testado
    # diretamente; células de dano não têm ocupantes elegíveis neste cenário.
    us[7] = unidade(tipo=0, dono=1, atual=0x5050, passo=0x2024, estado=0)
    us[7][0x72] = 0
    return ContextoAtaque(us, recargas={tipo: 100}, descoberto=lambda _: False,
                         busca=BuscaAtaque(0, 1, 1, 0x12345678), efeito_externo=lambda *args: None)


class ContratosAnimacao(unittest.TestCase):
    def test_incremento_overflow_igualdade_e_divisor(self):
        ctx = contexto()
        u = ctx.unidades[0]
        u[0xa9], u[0xa8], u[0xa4], u[0xa6] = 255, 0, 255, 3
        anim_attaque_engin(u)
        self.assertEqual((u[0xa9], u[0xa4]), (0, 1))
        u[0xa9], u[0xa8] = 9, 3
        anim_attaque_engin(u)
        self.assertEqual(u[0xa9], 10)
        u[0xa9], u[0xa8], u[0xa6] = 0, 1, 0
        with self.assertRaises(ZeroDivisionError):
            anim_attaque_engin(u)

    def test_quadros_estaticos_e_attaque_termine(self):
        for tipo in (5, 6, 7, 9, 10, 12, 13, 16, 17):
            u = contexto(tipo).unidades[0]
            antes = bytes(u)
            anim_attaque_engin(u)
            self.assertEqual(bytes(u), antes)
        u = contexto(2).unidades[0]
        self.assertTrue(anim_attaque_termine_engin(u))
        u[1] = 0
        self.assertFalse(anim_attaque_termine_engin(u))

    def test_disparo_especial_duplo_e_flag_do_alvo(self):
        ctx = contexto(11, modo=1)
        calcular_ataque(ctx, 0)
        self.assertEqual([c[1][0] for c in ctx.chamadas], [1, 26])
        ctx = contexto(25)
        calcular_ataque(ctx, 0)
        self.assertEqual([c[1][0] for c in ctx.chamadas], [33])
        ctx = contexto(8, modo=1)
        ctx.unidades[7][1] = 16
        calcular_ataque(ctx, 0)
        self.assertEqual(ctx.chamadas[0][1][-1], 1)

    def test_subestado2_underflow_e_subestado3_sem_reiniciar_fase(self):
        ctx = contexto(subestado=2)
        ctx.unidades[0][0x8b] = 0
        calcular_ataque(ctx, 0)
        self.assertEqual(ctx.unidades[0][0x8b], 255)
        self.assertEqual(ctx.unidades[0][0x8a], 2)
        ctx = contexto(subestado=3)
        calcular_ataque(ctx, 0)
        self.assertEqual(ctx.unidades[0][2], 7)
        self.assertEqual(ctx.unidades[0][0x8a], 3)
        self.assertEqual(palavra(ctx.unidades[0], 0xb8), 65535)
        self.assertEqual(ctx.busca, BuscaAtaque())

    def test_som_e_efeito_externo_obrigatorio(self):
        ctx = contexto()
        ctx.descoberto = lambda _: True
        struct.pack_into('<I', ctx.unidades[0], 0x104, 0xffffffff)
        ctx.efeito_externo = lambda nome, args: 42 if nome == 'EnginGetVolume' else None
        calcular_ataque(ctx, 0)
        self.assertEqual(ctx.chamadas[:2], [('EnginGetVolume', (0,)), ('PlaySnd_PostSound', (80, 0x2300, 0, 42, 0))])
        ctx = contexto()
        ctx.efeito_externo = None
        with self.assertRaises(NotImplementedError):
            calcular_ataque(ctx, 0)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Opcional: RISING_EMULAR=1')
class DiferencialAnimacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_animacao import BancadaAnimacao
        cls.b = BancadaAnimacao()

    def carregar(self, ctx):
        self.b.mundo(ctx.unidades)
        self.b.preparar_busca(ctx.busca)
        u = ctx.unidades[0]
        self.b.modificadores(u[0], u[1], ctx.modificadores.get((u[0], u[1], 3), 0),
                            ctx.modificadores.get((u[0], u[1], 4), 0))
        self.b.cpu.mem_write(0x4965de + u[1] * 50, struct.pack('<H', ctx.recargas[u[1]]))

    def conferir(self, ctx, carregar=True):
        from bancada_combate import RETORNO
        if carregar:
            self.carregar(ctx)
        ctx.chamadas.clear()
        r = self.b.passo_ataque(0)
        calcular_ataque(ctx, 0)
        self.assertEqual(self.b.ler_unidade(), bytes(ctx.unidades[0]))
        self.assertEqual(self.b.ler_busca(), ctx.busca)
        self.assertEqual(self.b.chamadas, ctx.chamadas)
        return r['EIP'] == RETORNO

    def test_animacao_26_tipos_subestados_overflow_e_quadro255(self):
        from bancada_animacao import ANIMACAO
        rng = random.Random(0x4479c4)
        for tipo in range(26):
            for subestado in range(6):
                for _ in range(12):
                    u = contexto(tipo, subestado).unidades[0]
                    u[0xa4], u[0xa9] = rng.choice((0, 1, 254, 255)), rng.choice((0, 1, 254, 255))
                    u[0xa5], u[0xa6], u[0xa7], u[0xa8] = 3, 5, rng.choice((0, 1, 2, 255)), rng.choice((0, 1, 2, 255))
                    self.b.escrever_unidade(u)
                    self.b.executar(0x4479c4, ANIMACAO)
                    anim_attaque_engin(u)
                    self.assertEqual(self.b.ler_unidade(), bytes(u), (tipo, subestado))
                    r = self.b.executar(0x447977, ANIMACAO)
                    self.assertEqual(bool(r['EAX'] & 255), anim_attaque_termine_engin(u))

    def test_giro_corpo_e_torre(self):
        from bancada_animacao import ANIMACAO
        rng = random.Random(0x4484a7)
        for torre in (False, True):
            for _ in range(600):
                tipo = rng.choice((0, 3, 12, 15))
                u = contexto(tipo).unidades[0]
                u[0x90], u[0x91], u[0xda], u[0x94] = rng.randrange(1, 17), rng.randrange(1, 17), rng.randrange(1, 33), rng.randrange(1, 33)
                u[0x92], u[0x96], u[0x93] = rng.randrange(256), rng.randrange(256), rng.choice((0, 1, 2, 255))
                self.b.escrever_unidade(u)
                self.b.executar(0x4484a7 if torre else 0x448599, ANIMACAO)
                girar(u, torre)
                self.assertEqual(self.b.ler_unidade(), bytes(u))

    def test_saidas_e_deslocamentos_do_corpo_tipos_orientacoes(self):
        from bancada_animacao import ANIMACAO
        for tipo in range(26):
            for d in range(1, 33 if tipo in (12, 15) else 17):
                saida = 0x1178000
                self.b.cpu.mem_write(saida, bytes(4))
                self.b.executar(0x4511a5, ANIMACAO, dict(EAX=tipo, EDX=d, EBX=saida, ECX=saida + 2))
                self.b.executar(0x410fcc, ANIMACAO, dict(EAX=tipo, EDX=saida, EBX=saida + 2))
                obtido = struct.unpack('<hh', self.b.cpu.mem_read(saida, 4))
                self.assertEqual(obtido, saida_projetil(tipo, d), (tipo, d))

    def test_subestado0_preparacao_giro_recarga_e_navegacao_delegada(self):
        for tipo in range(26):
            for caso in range(9):
                ctx = contexto(tipo, 0)
                u = ctx.unidades[0]
                info = mira_requerida(ctx.unidades, 0)
                u[info['campo_orientacao']] = info['orientacao_requerida']
                if caso == 1:
                    u[info['campo_orientacao']] = 1
                elif caso == 2:
                    guardar(u, 0x102, 0)
                elif caso == 3:
                    ctx.modificadores[(0, tipo, 3)] = 101
                elif caso == 4:
                    u[0x86] = 1
                elif caso == 5:
                    u[0xb0] = 0
                elif caso == 6:
                    ctx.terreno[0x2022] = 0x1dd
                elif caso == 7:
                    u[0xda] = 0
                elif caso == 8:
                    u[0xb7] = 1
                    guardar(u, 0xb8, 7)
                    ctx.unidades[7][1] = 16
                    guardar(ctx.unidades[7], 0x7c, 0x2022)
                    ctx.terreno[0x2021] = 0x1dd
                self.carregar(ctx)
                for c, v in ctx.terreno.items():
                    self.b.cpu.mem_write(0x1140000 + c * 2, struct.pack('<H', v))
                self.conferir(ctx, carregar=False)

    def test_subestado1_disparo_e_retorno_de_quadros_todos_tipos(self):
        for tipo in range(26):
            for modo in (1, 5):
                for caso in range(6):
                    ctx = contexto(tipo, 1, modo)
                    u = ctx.unidades[0]
                    if caso == 1:
                        u[0xa9] = 0
                    elif caso == 2:
                        u[0xa9] = 255
                    elif caso == 3:
                        u[0xa4], u[0xa9], u[0x7a] = 3, 1, 0
                    elif caso == 4:
                        u[0xa4], u[0xa9], u[0x7a], u[0x8b] = 0, 0, 0, 0
                    elif caso == 5:
                        ctx.unidades[7][1] = 16
                    self.assertTrue(self.conferir(ctx), (tipo, modo, caso))

    def test_subestado1_melee_sem_duplicar_dano(self):
        for tipo in range(26):
            ctx = contexto(tipo)
            u = ctx.unidades[0]
            u[0x78] = 0
            guardar(u, 0x7c, palavra(u, 8))
            # Todos disparam, inclusive os que não animam nesta função.
            u[0xa4], u[0xa9], u[0x7a], u[0xa8] = (1 if tipo in TIPOS_ANIMAM else 2), 0, 2, 1
            self.assertTrue(self.conferir(ctx), tipo)

    def test_subestados_construcoes_com_consultas_originais(self):
        for tamanho in (1, 3):
            origem = 0x3030
            centro = origem + (tamanho // 2) * 257
            celulas = {origem + dx + 256 * dy for dy in range(tamanho) for dx in range(tamanho)}
            def adjacente(_, pos):
                x, y = pos & 255, pos >> 8
                return next((x + dx + 256 * (y + dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                             if x + dx + 256 * (y + dy) in celulas), 0xffff)
            def contato(_, pos):
                return adjacente(0, pos) != 0xffff
            for tipo in (0, 3, 12, 15):
                for sub in (0, 1, 2):
                    for alcance in (0, 1, 9):
                        ctx = contexto(tipo, sub)
                        u = ctx.unidades[0]
                        u[0xb7], u[0xb0], u[0x8b] = 3, alcance, 1
                        guardar(u, 8, 0x2f2f)
                        guardar(u, 0x7c, 0x2f30)
                        guardar(u, 0xb8, 0)
                        u[0xa4], u[0xa9], u[0xa8] = (1 if tipo in TIPOS_ANIMAM else 2), 0, 1
                        ctx.celula_construcao = lambda _: centro
                        ctx.celula_construcao_adjacente = adjacente
                        ctx.adjacente_construcao = contato
                        self.carregar(ctx)
                        predio = bytearray(276)
                        guardar(predio, 2, origem)
                        self.b.cpu.mem_write(0x49a0c8, bytes(predio))
                        self.b.cpu.mem_write(0x495d8c, struct.pack('<HH', tamanho, tamanho))
                        self.b.cpu.mem_write(0x495c04, bytes([1]) * (tamanho * tamanho))
                        self.conferir(ctx, carregar=False)

    def test_emissao_com_slot_livre_executa_projectile_set_original(self):
        from bancada_animacao import PROJETEIS
        ctx = contexto()
        self.carregar(ctx)
        pool = bytes(self.b.cpu.mem_read(PROJETEIS, 100 * 56))
        self.b.cpu.mem_write(PROJETEIS, bytes(56))
        try:
            self.assertTrue(self.conferir(ctx, carregar=False))
            p = bytes(self.b.cpu.mem_read(PROJETEIS, 56))
            self.assertEqual((p[0], p[2]), (1, 1))
            self.assertEqual(struct.unpack_from('<HH', p, 0x14), (0x2020, 0x2024))
        finally:
            self.b.cpu.mem_write(PROJETEIS, pool)

    def test_disparo_indice7(self):
        from animacao_disparo import BuscaAtaque
        ctx = contexto()
        ctx.unidades[7] = ctx.unidades[0]
        ctx.unidades[0] = bytes(276)
        ctx.busca = BuscaAtaque(7, 1, 1, 0x12345678)
        self.b.mundo(ctx.unidades)
        self.b.preparar_busca(ctx.busca)
        self.b.passo_ataque(7)
        calcular_ataque(ctx, 7)
        self.assertEqual(self.b.ler_unidade(7), bytes(ctx.unidades[7]))
        self.assertEqual(self.b.chamadas, ctx.chamadas)

    def test_subestado2_contador_animacao16_e_limpeza(self):
        for tipo in range(26):
            if tipo == 17:
                continue  # Conferido como fronteira explícita no teste seguinte.
            for espera in (0, 1, 2, 255):
                for da in (0, 1):
                    ctx = contexto(tipo, 2)
                    u = ctx.unidades[0]
                    info = mira_requerida(ctx.unidades, 0)
                    u[info['campo_orientacao']] = info['orientacao_requerida']
                    u[0x8b], u[0xda] = espera, da
                    self.conferir(ctx)

    def test_fronteiras_balao_e_som_nao_sao_mocks(self):
        from bancada_animacao import VISIBILIDADE
        class Pendente(Exception):
            pass
        def parar(*args):
            raise Pendente
        for som in (False, True):
            ctx = contexto(0 if som else 17, 1 if som else 2)
            ctx.efeito_externo = parar
            if som:
                ctx.descoberto = lambda _: True
            self.carregar(ctx)
            if som:
                self.b.cpu.mem_write(VISIBILIDADE + 0x2020, b'\0')
            r = self.b.passo_ataque(0)
            with self.assertRaises(Pendente):
                calcular_ataque(ctx, 0)
            self.assertEqual(r['EIP'], 0x440c5d if som else 0x447b2f)
            self.assertEqual(self.b.chamadas, ctx.chamadas)
            self.assertEqual(self.b.ler_unidade(), bytes(ctx.unidades[0]))
            self.b.cpu.mem_write(VISIBILIDADE + 0x2020, b'\1')

    def test_subestado3_e_invalido_todos_tipos_sem_rng(self):
        for tipo in range(26):
            for sub in (3, 4, 255):
                for estado in (0, 4, 1, 24):
                    ctx = contexto(tipo, sub)
                    ctx.unidades[0][2] = estado
                    self.assertTrue(self.conferir(ctx))
                    self.assertEqual(ctx.chamadas, [])

    def test_magia_invalida_seguida_reset_original(self):
        def reset_local(ctx, nome, args):
            # Contrato já reconstruído de ResetOrdre, só usado como adaptador
            # de teste; a nova tradução o delega e não promete validá-lo aqui.
            if nome != 'ResetOrdre':
                return
            u = ctx.unidades[0]
            if not u[0x86] and not u[0x87] and u[1] != 16:
                u[0xa4] = u[0xa9] = 0
            guardar(u, 0x7e, palavra(u, 0x7c))
            ctx.busca.liberar(0)
            u[0x88] = u[0x82] = 0
            guardar(u, 0xb2, 65535)
            u[2] = 2
        for tipo in (0, 3, 12, 15, 16, 25):
            ctx = contexto(tipo)
            u = ctx.unidades[0]
            u[2], u[0xa4], u[0xa9], u[0x7a], u[0xa8] = 24, (1 if tipo in TIPOS_ANIMAM else 2), 0, 2, 1
            ctx.efeito_externo = lambda nome, args: reset_local(ctx, nome, args)
            self.assertTrue(self.conferir(ctx))
            self.assertEqual([c[0] for c in ctx.chamadas], ['SortilegeEffet', 'ResetOrdre'])

    def test_ciclo_continuo_60_atualizacoes(self):
        ctx = contexto(0, 0)
        u = ctx.unidades[0]
        ctx.recargas[0] = 2
        self.carregar(ctx)
        total_disparos = 0
        for n in range(60):
            # Incremento externo de recarga, separado do despacho de ataque.
            if palavra(u, 0x102) < 2:
                guardar(u, 0x102, palavra(u, 0x102) + 1)
                self.b.cpu.mem_write(0x1000000 + 0x102, struct.pack('<H', palavra(u, 0x102)))
            self.assertTrue(self.conferir(ctx, carregar=False), n)
            total_disparos += sum(nome == 'ProjectileInit' for nome, args in ctx.chamadas)
        self.assertGreater(total_disparos, 2)


if __name__ == '__main__':
    unittest.main()
