"""Casos de contrato e comparações diferenciais com o EXE original identificado."""
import os
import random
import struct
import unittest

from alvos_alcance import (SEM_ALVO, distancia2, aliados, engin_est_ennemi,
    tipo_pode_atacar, encontrar_alvo_scan, encontrar_alvo, ocupa_celula,
    adjacente_unidade, celulas_adjacentes, a_portee, a_portee_minimale,
    linha_de_tiro, arma_carregada, preparar_inicio, iniciar_ciclo_apos_mira,
    ordem_apos_reset, ordem_ja_definida, manter_ciclo_apos_espera, alvo_ordem_valido,
    elegivel_busca_automatica, reacao_alvo_automatico)


def unidade(tipo=0, dono=0, atual=0x1010, passo=None, estado=7, visao=8):
    u = bytearray(276)
    u[0], u[1], u[2], u[0x72], u[0xbb], u[0x78] = dono, tipo, estado, 1, visao, 1
    struct.pack_into('<H', u, 8, atual)
    struct.pack_into('<H', u, 0x7c, atual if passo is None else passo)
    return u


def tabela(*registros):
    return [*registros, *[bytes(276) for _ in range(800 - len(registros))]]


class Contratos(unittest.TestCase):
    def test_filtro_e_donos_especiais(self):
        self.assertFalse(tipo_pode_atacar(0, 16))
        self.assertTrue(tipo_pode_atacar(2, 16))
        self.assertFalse(tipo_pode_atacar(2, 17))
        self.assertTrue(engin_est_ennemi(4, 200, [0] * 5))
        self.assertFalse(engin_est_ennemi(0, 200, [0] * 5))
        self.assertTrue(aliados(200, 200, [0] * 5))

    def test_scan_primeiro_grade_mais_proximo_e_empate(self):
        us = tabela(unidade(), unidade(dono=1, atual=0x1016), unidade(dono=1, atual=0x1012))
        g = {0x1016: 0x4008, 0x1012: 0x4010}
        self.assertEqual(encontrar_alvo_scan(us, 0, [0] * 5), 1)
        self.assertEqual(encontrar_alvo(us, 0, g, [0] * 5), 2)
        self.assertEqual(encontrar_alvo(us, 0, {0x1011: 0x4008, 0x100f: 0x4010}, [0] * 5), 2)
        us[0][1] = 2
        self.assertEqual(encontrar_alvo(us, 0, g, [0] * 5), 1)

    def test_grade_nao_repete_estado_e_inverte_alianca(self):
        us = tabela(unidade(), unidade(dono=1, estado=0))
        us[1][0x72] = 0
        self.assertEqual(encontrar_alvo_scan(us, 0, [2, 0, 0, 0, 0]), SEM_ALVO)
        self.assertEqual(encontrar_alvo(us, 0, {0x1011: 0x4008}, [2, 0, 0, 0, 0]), 1)

    def test_limites_de_alcance_e_contato(self):
        us = tabela(unidade(atual=0x1010), unidade(dono=1, atual=0x5050, passo=0x1012))
        us[0][0xb0] = 4
        self.assertTrue(a_portee(us, 0, 1, 1))
        us[0][0xb0] = 3
        self.assertFalse(a_portee(us, 0, 1, 1))
        us[0][0x78], us[0][0xb0] = 0, 0
        struct.pack_into('<H', us[1], 8, 0x1111)
        self.assertTrue(a_portee(us, 0, 1, 1))

    def test_arma_e_inicio_nao_equivalem_a_dano(self):
        u = unidade()
        self.assertTrue(arma_carregada(0, 100, 101))
        self.assertTrue(preparar_inicio(u, True, True))
        u[0x86] = 1
        self.assertFalse(preparar_inicio(u, True, True))
        u[0x86] = 0
        struct.pack_into('<H', u, 0x102, 99)
        self.assertEqual(iniciar_ciclo_apos_mira(u, 100)[1], 'aguardar_recarga')
        self.assertEqual(iniciar_ciclo_apos_mira(u, 100, 1)[1], 'ciclo_iniciado')

    def test_linha_montanha_no_alvo_e_isencoes(self):
        u = unidade(atual=0x1010)
        self.assertFalse(linha_de_tiro(u, 0x1013, {0x1011: 0x1dd}))
        self.assertTrue(linha_de_tiro(u, 0x1013, {0x1013: 0x1dd}))
        u[1] = 8
        self.assertTrue(linha_de_tiro(u, 0x1013, {0x1011: 0x1dd}))

    def test_ordem_e_manutencao(self):
        u = unidade()
        r, aceitou = ordem_apos_reset(u, 0, 1, 3)
        self.assertTrue(aceitou)
        self.assertTrue(ordem_ja_definida(r, 1, 3))
        self.assertFalse(ordem_apos_reset(u, 0, 1, 0)[1])
        self.assertTrue(manter_ciclo_apos_espera(14, False, False))
        self.assertFalse(manter_ciclo_apos_espera(0, True, False))

    def test_validade_ordem_nao_repete_filtro_de_selecao(self):
        us = tabela(unidade(), unidade(tipo=17, dono=0))
        us[0][0xb7] = 1
        struct.pack_into('<H', us[0], 0xb8, 1)
        self.assertTrue(alvo_ordem_valido(us, 0))
        us[1][0] = 200
        self.assertFalse(alvo_ordem_valido(us, 0))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Opcional: RISING_EMULAR=1')
class Diferencial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_combate import BancadaCombate
        cls.b = BancadaCombate()

    def test_filtro_26_por_26_e_inimizade_direcional(self):
        for a in range(26):
            for d in range(26):
                r = self.b.executar(0x453d7d, [(0x453d7d, 0x453da2)], dict(EAX=a, EDX=d))
                self.assertEqual(bool(r['EAX'] & 255), tipo_pode_atacar(a, d), (a, d))
        for mask in (0, 1, 2, 16, 31):
            mascaras = [mask] * 5
            for a in (0, 1, 4, 200, 255):
                for d in (0, 1, 4, 200, 255):
                    self.b.mundo(tabela(unidade(dono=d)), mascaras=mascaras)
                    r = self.b.executar(0x446fbf, [(0x446fbf, 0x447021), (0x46d838, 0x46d877)], dict(EDX=a))
                    self.assertEqual(bool(r['EAX'] & 255), engin_est_ennemi(a, d, mascaras), (mask, a, d))

    def test_selecao_scan_grade_entradas_sinteticas(self):
        rng = random.Random(0x453f74)
        for n in range(160):
            pos = rng.choice((0, 0xffff, 0x10ff, 0xff10, 0x1010, 0x0404))
            u = unidade(tipo=rng.choice((0, 2, 8, 16)), dono=rng.choice((0, 1, 4, 200)),
                        atual=pos, visao=rng.randrange(9))
            us, grade = tabela(u), {}
            for i in range(1, 15):
                x = min(255, max(0, (pos & 255) + rng.randrange(-9, 10)))
                y = min(255, max(0, (pos >> 8) + rng.randrange(-9, 10)))
                c = x + 256 * y
                us[i] = unidade(tipo=rng.choice((0, 10, 16, 17, 25)), dono=rng.choice((0, 1, 4, 200)),
                                atual=c, estado=rng.choice((0, 4, 7, 14)))
                us[i][0x72] = rng.randrange(2)
                if rng.randrange(3):
                    grade[c] = 0x4000 + i * 8 + rng.randrange(8)
            mascaras = [rng.randrange(32) for _ in range(5)]
            self.b.mundo(us, grade, mascaras)
            self.assertEqual(self.b.selecionar(0, True), encontrar_alvo_scan(us, 0, mascaras), n)
            self.assertEqual(self.b.selecionar(0), encontrar_alvo(us, 0, grade, mascaras), n)

    def test_scan_e_grade_diferencas_e_desempate(self):
        for tipo in (0, 2, 8):
            us = tabela(unidade(tipo=tipo), unidade(dono=1, atual=0x1016), unidade(dono=1, atual=0x1012))
            grade = {0x1016: 0x4008, 0x1012: 0x4010}
            for masks in ([0] * 5, [2, 0, 0, 0, 0], [0, 1, 0, 0, 0]):
                self.b.mundo(us, grade, masks)
                self.assertEqual(self.b.selecionar(0), encontrar_alvo(us, 0, grade, masks))
            us[1][2] = us[1][0x72] = 0
            self.b.mundo(us, {0x100f: 0x4008, 0x1011: 0x4010})
            self.assertEqual(self.b.selecionar(0), encontrar_alvo(us, 0, {0x100f: 0x4008, 0x1011: 0x4010}, [0] * 5))
        us = tabela(unidade(tipo=2))
        # Sem candidatos ativos no scan: usa a grade até para os tipos 2 e 8.
        us[1] = unidade(dono=1, estado=0)
        self.b.mundo(us, {0x1011: 0x4008})
        self.assertEqual(self.b.selecionar(0), 1)
        self.assertEqual(encontrar_alvo(us, 0, {0x1011: 0x4008}, [0] * 5), 1)

    def test_ocupacao_e_adjacencia_tipos_bordas_e_camadas(self):
        from bancada_combate import CONTATO
        rng = random.Random(0x4468e4)
        for n in range(400):
            tipo = n % 26
            c = rng.choice((0, 1, 0x100, 0x101, 0xffff, 0xff00, 0x00ff, 0x1010))
            u = unidade(tipo=tipo, atual=c)
            alvo = unidade(tipo=rng.randrange(26), atual=(c + rng.choice((-257, -1, 0, 1, 257, 514))) & 65535,
                           estado=rng.choice((0, 7, 14)))
            alvo[0xab] = rng.randrange(2)
            struct.pack_into('<H', alvo, 0x7c, rng.randrange(65536))
            u[0x86], u[0x87] = (1, 0) if n % 13 == 0 else (0, 0)
            us = tabela(u, alvo)
            self.b.mundo(us)
            celula = rng.choice((c, (c - 1) & 65535, (c + 257) & 65535))
            filtro = n % 3
            r = self.b.executar(0x44246e, CONTATO, dict(EAX=1, EDX=celula, EBX=filtro))
            self.assertEqual(bool(r['EAX'] & 255), ocupa_celula(alvo, celula, filtro), ('ocupacao', n))
            r = self.b.executar(0x446b0c, CONTATO, dict(EAX=0, EDX=celula))
            self.assertEqual(bool(r['EAX'] & 255), celula in celulas_adjacentes(u), ('celula', n))
            r = self.b.executar(0x4468e4, CONTATO, dict(EAX=0, EDX=1))
            self.assertEqual(bool(r['EAX'] & 255), adjacente_unidade(u, alvo), ('unidade', n))

    def test_alcance_modos1_5_e_excecoes(self):
        rng = random.Random(0x446cb5)
        for n in range(600):
            c = rng.choice((0, 0xffff, 0x1010, rng.randrange(65536)))
            alvo_c = (c + rng.choice((0, 1, 2, 257, 514, -257, 260))) & 65535
            u = unidade(tipo=n % 26, atual=c, estado=24 if n % 7 == 0 else 7)
            u[0x78], u[0xb0], u[0xf4] = rng.randrange(2), rng.randrange(256), 1
            u[0x86], u[0x87] = (0, 1) if n % 11 == 0 else (0, 0)
            struct.pack_into('<H', u, 0xb8, alvo_c)
            alvo = unidade(tipo=rng.choice((0, 16, 25)), dono=1, atual=c, passo=alvo_c)
            us = tabela(u, alvo)
            modo = 1 if n % 2 else 5
            referencia = 1 if modo == 1 else alvo_c
            mod, magia = rng.randrange(256), rng.randrange(65536)
            self.b.mundo(us)
            self.b.modificadores(0, u[1], mod4=mod)
            self.b.cpu.mem_write(0x49717e + 46, struct.pack('<H', magia))
            self.assertEqual(self.b.alcance(0, modo, referencia), a_portee(us, 0, modo, referencia, mod,
                alcance_magia=lambda _: magia), (n, modo))
            self.assertEqual(self.b.alcance(0, modo, referencia, True), a_portee_minimale(us, 0, modo, referencia), ('min', n))

    def test_linha_original_montanhas_e_todos_os_tipos(self):
        rng = random.Random(0x4517a2)
        for n in range(260):
            u = unidade(tipo=n % 26, atual=rng.randrange(65536))
            destino = rng.randrange(65536)
            terreno = {rng.randrange(65536): rng.choice((0x1dc, 0x1dd, 0x25f, 0x260)) for _ in range(300)}
            # Bloqueios explicitamente na rota de sinais.
            if n % 3 == 0:
                x, y = u[8], u[9]
                x += ((destino & 255) > x) - ((destino & 255) < x)
                y += ((destino >> 8) > y) - ((destino >> 8) < y)
                terreno[x + y * 256] = 0x1dd
            terreno[destino] = 0x1dd
            self.b.mundo(tabela(u), terreno=terreno)
            self.assertEqual(self.b.linha(0, 5, destino), linha_de_tiro(u, destino, terreno), n)

    def test_alcance_construcao_com_geometria_sintetica(self):
        # Executa getters/adjacência de construção originais. O Python recebe
        # esses resultados por callbacks explícitos; não traduz a construção.
        for tamanho in (1, 3):
            origem = 0x2020
            centro = origem + (tamanho // 2) * 257
            for tipo in (0, 1, 16):
                for c in (0x1f1f, 0x2020, 0x2121, 0x2424, 0x3030):
                    for flag in (0, 1):
                        u = unidade(tipo=tipo, atual=c)
                        u[0x78], u[0xb0] = flag, 4
                        us = tabela(u)
                        self.b.mundo(us)
                        self.b.modificadores(0, tipo, mod4=1)
                        predio = bytearray(276)
                        struct.pack_into('<H', predio, 2, origem)
                        self.b.cpu.mem_write(0x49a0c8, bytes(predio))
                        self.b.cpu.mem_write(0x495d8c, struct.pack('<HH', tamanho, tamanho))
                        self.b.cpu.mem_write(0x495c04, bytes([1]) * (tamanho * tamanho))
                        celulas = {origem + dx + 256 * dy for dy in range(tamanho) for dx in range(tamanho)}
                        def contato(_, pos):
                            return any(abs((a & 255) - (pos & 255)) <= 1 and
                                       abs((a >> 8) - (pos >> 8)) <= 1 for a in celulas)
                        esperado = a_portee(us, 0, 3, 0, 1, celula_construcao=lambda _: centro,
                                            adjacente_construcao=contato)
                        self.assertEqual(self.b.alcance(0, 3, 0), esperado, (tamanho, tipo, c, flag))

    def test_recarga_e_inicio_ciclo(self):
        from bancada_combate import RECARGA, UNIDADES
        rng = random.Random(0x45173f)
        for n in range(400):
            tipo = n % 26
            u = unidade(tipo=tipo)
            atual, base, mod = [rng.randrange(65536) for _ in range(3)]
            u[0xa4], u[0xa9], u[0x94], u[0xda] = 5, 9, 2, (3 if n % 5 == 0 else 2)
            struct.pack_into('<H', u, 0x102, atual)
            self.b.mundo(tabela(u))
            self.b.modificadores(0, tipo, mod3=mod)
            self.b.cpu.mem_write(0x4965de + tipo * 50, struct.pack('<H', base))
            r = self.b.executar(0x45173f, RECARGA)
            self.assertEqual(bool(r['EAX'] & 255), arma_carregada(atual, base, mod))
            # Entrada após corpo alinhado. Paradas ANTES de giro e efeitos extras.
            r = self.b.executar(0x451d4d, [(0x451d49, 0x451e22), (0x428cc0, 0x428e71)],
                dict(ESI=UNIDADES, EDI=0), parada={0x451d88, 0x452c89, 0x451e22})
            esperado, motivo = iniciar_ciclo_apos_mira(u, base, mod)
            self.assertEqual(r['EIP'], {'girar_torre': 0x451d88, 'aguardar_recarga': 0x452c89,
                                       'ciclo_iniciado': 0x451e22}[motivo])
            self.assertEqual(self.b.ler_unidade(), bytes(esperado), n)

    def test_ordem_efeitos_locais_apos_reset(self):
        from bancada_combate import UNIDADES
        for tipo in range(26):
            for modo in (0, 1, 2, 3, 4, 5, 255):
                for ref in (0, 1):
                    u = unidade(tipo=tipo)
                    u[0x8a] = 3
                    self.b.mundo(tabela(u))
                    self.b.executar(0x445a80, [(0x445a80, 0x445af1)],
                        dict(EDX=UNIDADES, ESI=0, ECX=modo, EBX=ref),
                        parada={0x445aab, 0x445aca, 0x445ae6, 0x445aee})
                    esperado, _ = ordem_apos_reset(u, 0, modo, ref)
                    self.assertEqual(self.b.ler_unidade(), bytes(esperado), (tipo, modo, ref))

    def test_truncamento_distancia_grade_trecho(self):
        from bancada_combate import UNIDADES, PILHA
        for a, c, raio in ((0, 0xffff, 255), (0, 0xff01, 255), (0xffff, 0, 255), (0, 0x0101, 1)):
            u = unidade(atual=a, visao=raio)
            self.b.mundo(tabela(u))
            self.b.executar(0x45416f, [(0x45416f, 0x4541b7), (0x479555, 0x4795af)],
                dict(ESI=UNIDADES, EDI=c & 255), parada=0x4541b7,
                pilha={4: struct.pack('<I', c >> 8), 8: struct.pack('<I', a >> 8),
                       0x10: struct.pack('<I', a & 255), 0x24: struct.pack('<I', 65535),
                       0x28: struct.pack('<I', 1)})
            selecionou = bool(self.b.cpu.mem_read(PILHA + 0x8030, 1)[0])
            d = distancia2(a, c) & 65535
            self.assertEqual(selecionou, d <= raio * raio and d < 65535)

    def test_preparacao_inicio_alcance_e_linha_originais(self):
        from bancada_combate import ALCANCE, LINHA
        for n in range(104):
            u = unidade(tipo=n % 26, atual=0x1010)
            u[0xb0], u[0x78] = n % 8, 1
            u[0x86] = 1 if n % 9 == 0 else 0
            u[0xb7] = 1
            struct.pack_into('<H', u, 0xb8, 1)
            alvo = unidade(dono=1, atual=0x1616, passo=0x1012)
            terreno = {0x1011: 0x1dd} if n % 5 == 0 else {}
            us = tabela(u, alvo)
            self.b.mundo(us, terreno=terreno)
            self.b.modificadores(0, u[1])
            r = self.b.executar(0x451914, [(0x451914, 0x4519bd)] + ALCANCE + LINHA,
                parada={0x4519bd, 0x451e90})
            em_alcance = a_portee(us, 0, 1, 1)
            livre = linha_de_tiro(u, 0x1012, terreno)
            self.assertEqual(r['EIP'] == 0x4519bd, preparar_inicio(u, em_alcance, livre), n)
            self.assertEqual(self.b.ler_unidade(), bytes(u))

    def test_validade_alvo_antes_de_calcular_ataque(self):
        from bancada_combate import UNIDADES
        for estado in (0, 1, 4, 7, 14, 24):
            for dono in (0, 1, 4, 200):
                for flag in (0, 1):
                    for tipo in (0, 16, 17):
                        u = unidade()
                        u[0xb7] = 1
                        struct.pack_into('<H', u, 0xb8, 1)
                        alvo = unidade(tipo=tipo, dono=dono, estado=estado)
                        alvo[0x72] = flag
                        us = tabela(u, alvo)
                        self.b.mundo(us)
                        r = self.b.executar(0x456886, [(0x4567ce, 0x45689e)],
                            dict(ESI=UNIDADES, EDI=0), parada={0x45684f, 0x45689e})
                        self.assertEqual(r['EIP'] == 0x45689e, alvo_ordem_valido(us, 0))
        u = unidade()
        u[0xb7] = 1
        struct.pack_into('<H', u, 0xb8, SEM_ALVO)
        us = tabela(u)
        self.b.mundo(us)
        r = self.b.executar(0x456886, [(0x4567ce, 0x45689e)],
            dict(ESI=UNIDADES), parada={0x45684f, 0x45689e})
        self.assertEqual(r['EIP'], 0x45684f)
        self.assertFalse(alvo_ordem_valido(us, 0))

    def test_manutencao_fragmentos_com_consultas_resolvidas(self):
        from bancada_combate import UNIDADES
        # Este teste é de dois trechos de decisão com retornos como ENTRADAS.
        # Não executa nem substitui EnginAPortee ou EnginViseCible neste teste.
        for tipo in range(26):
            for alcance in (False, True):
                for mira in (False, True):
                    u = unidade(tipo=tipo)
                    u[0x8a] = 1
                    self.b.mundo(tabela(u))
                    if tipo in (14, 16):
                        r = self.b.executar(0x452b10, [(0x452b10, 0x452b3e), (0x452b78, 0x452b7c)],
                            dict(ESI=UNIDADES), parada={0x452b3e, 0x451e51})
                        manteve = r['EIP'] == 0x451e51
                    else:
                        r = self.b.executar(0x452b59, [(0x452b59, 0x452b78)],
                            dict(ESI=UNIDADES, EAX=int(alcance)), parada={0x452b5d, 0x452c89})
                        if r['EIP'] == 0x452b5d:
                            self.b.executar(0x452b64, [(0x452b64, 0x452b78)],
                                dict(ESI=UNIDADES, EAX=int(mira)), parada=0x452c89)
                        manteve = self.b.ler_unidade()[0x8a] == 1
                    self.assertEqual(manteve, manter_ciclo_apos_espera(tipo, alcance, mira))

    def test_portoes_de_busca_automatica_e_reacao(self):
        from bancada_combate import UNIDADES
        for tipo in range(26):
            for estado in (0, 1, 7, 14, 19, 24):
                for da in (0, 1):
                    u = unidade(tipo=tipo, estado=estado)
                    u[0xda] = da
                    self.b.mundo(tabela(u))
                    # Não executa PlayerGetType: verifica os trechos antes/depois.
                    r = self.b.executar(0x4546bc, [(0x4546bc, 0x45471b)],
                        dict(EDI=0), parada={0x45471b, 0x4547e0})
                    passou = r['EIP'] == 0x45471b
                    if passou:
                        r = self.b.executar(0x45472a, [(0x45472a, 0x454794), (0x4547c6, 0x4547ca)],
                            dict(ESI=UNIDADES, EDI=0), parada={0x454794, 0x4547e0},
                            pilha={0x60: bytes([tipo])})
                        passou = r['EIP'] == 0x454794
                    self.assertEqual(passou, elegivel_busca_automatica(u), (tipo, estado, da))
        for estado in (1, 7, 14, 19, 24):
            for controle in (0, 1, 2, 4):
                u = unidade(estado=estado)
                self.b.mundo(tabela(u))
                r = self.b.executar(0x4547ad, [(0x4547ad, 0x4547e0)],
                    dict(ESI=UNIDADES), parada={0x4547b8, 0x4547d4, 0x4547e0},
                    pilha={0x50: bytes([controle])})
                acao = {0x4547b8: 'mensagem_0x49', 0x4547d4: 'ordem_modo_1', 0x4547e0: 'nenhuma'}[r['EIP']]
                self.assertEqual(acao, reacao_alvo_automatico(u, controle))


if __name__ == '__main__':
    unittest.main()
