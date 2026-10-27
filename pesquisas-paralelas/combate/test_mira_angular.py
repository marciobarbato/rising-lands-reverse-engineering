"""Mira contra o EXE original, incluindo FSQRT/FPATAN e truncamento Watcom."""
import os
import random
import struct
import unittest

from alvos_alcance import a_portee, manter_ciclo_apos_espera
from mira_angular import (angulo_calcul, celula_alvo_mira, mira_requerida,
                         engin_vise_cible, TIPOS_TORRE)
from test_alvos_alcance import unidade, tabela


def armar(tipo=0, modo=5, origem=0x8080, alvo=0x808a, indice=0):
    u = unidade(tipo=tipo, atual=origem, passo=0x4040)
    u[0xb7], u[0xb0] = modo, 100
    struct.pack_into('<H', u, 0xb8, 799 if modo == 1 else 0 if modo == 3 else alvo)
    us = tabela()
    us[indice] = u
    if modo == 1:
        us[799] = unidade(dono=1, atual=0x1010, passo=alvo)
    return us


VETORES = ((-100, 0), (-100, -100), (0, -100), (100, -100), (100, 0),
           (100, 100), (0, 100), (-100, 100), (0, 0), (100, 41),
           (100, 42), (100, 9), (100, 10))


class ContratosMira(unittest.TestCase):
    def test_eixos_coincidencia_e_limites_angulares(self):
        destinos = ((0, 10), (0, 0), (10, 0), (20, 0), (20, 10), (20, 20), (10, 20), (0, 20))
        for i, destino in enumerate(destinos):
            self.assertEqual(angulo_calcul(10, 10, *destino, 8), i + 1)
            self.assertEqual(angulo_calcul(10, 10, *destino, 32), i * 4 + 1)
        self.assertEqual(angulo_calcul(10, 10, 10, 10, 8), 5)
        self.assertEqual(angulo_calcul(10, 10, 10, 10, 32), 17)
        self.assertEqual(angulo_calcul(0, 0, 100, 41, 8), 5)
        self.assertEqual(angulo_calcul(0, 0, 100, 42, 8), 6)
        self.assertEqual(angulo_calcul(0, 0, 100, 9, 32), 17)
        self.assertEqual(angulo_calcul(0, 0, 100, 10, 32), 18)
        with self.assertRaises(ValueError):
            angulo_calcul(0, 0, 256, 1, 8)
        with self.assertRaises(ValueError):
            angulo_calcul(0, 0, 1, 1, 16)

    def test_corpo_torre_rotacao_tipo3_e_celulas_distintas(self):
        for tipo, campo, esperada in ((0, 0x91, 9), (3, 0x91, 5), (12, 0x94, 17), (15, 0x94, 17)):
            us = armar(tipo, 1)
            info = mira_requerida(us, 0)
            self.assertEqual((info['campo_orientacao'], info['orientacao_requerida']), (campo, esperada))
            us[0][campo] = esperada
            self.assertTrue(engin_vise_cible(us, 0))
            self.assertEqual(info['celula_alvo'], 0x808a)

    def test_ordem_das_consultas_de_construcao(self):
        for tipo in (0, 12, 15):
            for alcance in (0, 1, 2):
                for adj in (0x8081, 0xffff):
                    us = armar(tipo, 3)
                    us[0][0xb0] = alcance
                    chamadas = []
                    def centro(ref):
                        chamadas.append(('centro', ref))
                        return 0x8181
                    def adjacente(ref, origem):
                        chamadas.append(('adjacente', ref, origem))
                        return adj
                    alvo = celula_alvo_mira(us, 0, celula_construcao=centro, celula_construcao_adjacente=adjacente)
                    esperado = []
                    if alcance <= 1:
                        esperado.append(('adjacente', 0, 0x4040))
                    if alcance > 1 or adj == 0xffff:
                        esperado.append(('centro', 0))
                    if tipo in TIPOS_TORRE:
                        esperado.append(('centro', 0))
                    self.assertEqual(chamadas, esperado)
                    self.assertEqual(alvo, 0x8181 if tipo in TIPOS_TORRE or alcance > 1 or adj == 0xffff else adj)

    def test_dominios_e_callbacks_necessarios(self):
        us = armar(0, 3)
        with self.assertRaises(NotImplementedError):
            engin_vise_cible(us, 0)
        us[0][0xb0] = 0
        with self.assertRaises(NotImplementedError):
            engin_vise_cible(us, 0, celula_construcao=lambda _: 0)
        us = armar(0, 1)
        struct.pack_into('<H', us[0], 0xb8, 0xffff)
        with self.assertRaises(IndexError):
            engin_vise_cible(us, 0)
        us = armar(12, 0)
        with self.assertRaises(ValueError):
            engin_vise_cible(us, 0)
        self.assertEqual(celula_alvo_mira(armar(0, 0), 0), 0xffff)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Opcional: RISING_EMULAR=1')
class DiferencialMira(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_combate import BancadaCombate
        cls.b = BancadaCombate()

    def test_angulo_todas_65536_inclinacoes_u8_duas_resolucoes(self):
        for setores in (8, 32):
            for dx in range(256):
                for dy in range(256):
                    self.assertEqual(self.b.angulo(0, 0, dx, dy, setores),
                                     angulo_calcul(0, 0, dx, dy, setores), (setores, dx, dy))

    def test_quadrantes_bordas_e_translacoes_aleatorias(self):
        casos = []
        for dx in (0, 1, 9, 10, 41, 42, 127, 254, 255):
            for dy in (0, 1, 9, 10, 41, 42, 127, 254, 255):
                for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                    x, y = (0 if sx == 1 else 255), (0 if sy == 1 else 255)
                    casos.append((x, y, x + sx * dx, y + sy * dy))
        rng = random.Random(0x4796cb)
        casos += [tuple(rng.randrange(256) for _ in range(4)) for _ in range(2048)]
        for setores in (8, 32):
            for xy in casos:
                self.assertEqual(self.b.angulo(*xy, setores), angulo_calcul(*xy, setores), (setores, xy))

    def test_mira_completa_todos_tipos_modos1_5_e_orientacoes(self):
        for tipo in range(26):
            for dx, dy in VETORES:
                alvo = (128 + dx) + 256 * (128 + dy)
                for modo in (1, 5):
                    us = armar(tipo, modo, alvo=alvo, indice=7)
                    info = mira_requerida(us, 7)
                    campo, requerida = info['campo_orientacao'], info['orientacao_requerida']
                    # Modo 5 cobre cada orientação, inclusive valores inválidos.
                    orientacoes = (*range(34 if tipo in TIPOS_TORRE else 18), 255) if modo == 5 else (0, requerida, (requerida + 1) & 255, 255)
                    for atual in orientacoes:
                        us[7][campo] = atual
                        # O outro campo não deve afetar a consulta.
                        us[7][0x91 if campo == 0x94 else 0x94] = (atual + 7) & 255
                        self.b.escrever_unidade(us[7], 7)
                        if modo == 1:
                            self.b.escrever_unidade(us[799], 799)
                        self.assertEqual(self.b.mira(7), engin_vise_cible(us, 7), (tipo, alvo, modo, atual))
                        self.assertEqual(self.b.ler_unidade(7), bytes(us[7]))

    def test_mira_construcao_adjacencia_fallback_e_segunda_resolucao_torre(self):
        for tamanho in (1, 3):
            origem = 0x8080
            centro = origem + (tamanho // 2) * 257
            celulas = {origem + dx + 256 * dy for dy in range(tamanho) for dx in range(tamanho)}
            def adjacente(_, pos):
                x, y = pos & 255, pos >> 8
                return next((x + dx + 256 * (y + dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                             if x + dx + 256 * (y + dy) in celulas), 0xffff)
            for tipo in (0, 3, 12, 15, 25):
                for alcance in (0, 1, 2):
                    for passo in (0x7f7f, 0x8080, 0x8181, 0x8282, 0x8383, 0x9090):
                        us = armar(tipo, 3, origem=0x7060)
                        u = us[0]
                        u[0xb0] = alcance
                        struct.pack_into('<H', u, 0x7c, passo)
                        self.b.mundo(us)
                        predio = bytearray(276)
                        struct.pack_into('<H', predio, 2, origem)
                        self.b.cpu.mem_write(0x49a0c8, bytes(predio))
                        self.b.cpu.mem_write(0x495d8c, struct.pack('<HH', tamanho, tamanho))
                        self.b.cpu.mem_write(0x495c04, bytes([1]) * (tamanho * tamanho))
                        callbacks = dict(celula_construcao=lambda _: centro, celula_construcao_adjacente=adjacente)
                        info = mira_requerida(us, 0, **callbacks)
                        for atual in (info['orientacao_requerida'], (info['orientacao_requerida'] + 1) & 255):
                            u[info['campo_orientacao']] = atual
                            self.b.escrever_unidade(u)
                            self.assertEqual(self.b.mira(0), engin_vise_cible(us, 0, **callbacks),
                                             (tamanho, tipo, alcance, passo, atual))
                            self.assertEqual(self.b.ler_unidade(), bytes(u))

    def test_manutencao_executa_alcance_e_mira_sem_substituicoes(self):
        from bancada_combate import MIRA, UNIDADES
        for tipo in range(26):
            for dx, dy in VETORES:
                alvo = (128 + dx) + 256 * (128 + dy)
                for desalinhada in (False, True):
                    us = armar(tipo, 1, alvo=alvo)
                    u = us[0]
                    info = mira_requerida(us, 0)
                    u[info['campo_orientacao']] = info['orientacao_requerida'] + int(desalinhada)
                    u[0x8a] = 1
                    self.b.mundo(us)
                    self.b.modificadores(0, tipo)
                    em_alcance = a_portee(us, 0, 1, 799)
                    manteve = manter_ciclo_apos_espera(tipo, em_alcance, engin_vise_cible(us, 0))
                    r = self.b.executar(0x452b10, [(0x452b10, 0x452b7c)] + MIRA,
                        dict(ESI=UNIDADES, EDI=0), parada={0x452c89, 0x451e51})
                    esperado = bytearray(u)
                    if not manteve:
                        esperado[0x8a] = 0
                    self.assertEqual(self.b.ler_unidade(), bytes(esperado), (tipo, alvo, desalinhada))
                    self.assertEqual(r['EIP'] == 0x451e51, tipo in (14, 16))

    def test_registradores_memoria_e_controle_x87_preservados(self):
        from bancada_combate import MIRA, UNIDADES, x86, PILHA
        rng = random.Random(0x451464)
        for tipo in range(26):
            us = armar(tipo, 1, alvo=rng.randrange(65536), indice=7)
            us[7][0x91], us[7][0x94] = rng.randrange(256), rng.randrange(256)
            self.b.mundo(us)
            antes = bytes(self.b.cpu.mem_read(UNIDADES, 800 * 276))
            regs = {n: rng.randrange(0x100000000) for n in ('EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')}
            r = self.b.executar(0x451464, MIRA, dict(EAX=7, **regs))
            self.assertEqual({n: r[n] for n in regs}, regs)
            self.assertEqual(r['ESP'], PILHA + 0x8004)
            self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_FPCW), 0x037f)
            self.assertEqual(bytes(self.b.cpu.mem_read(UNIDADES, 800 * 276)), antes)
            self.assertEqual(bool(r['EAX'] & 255), engin_vise_cible(us, 7))

    def test_modos_outros_corpo_sentinela_e_torre_depende_edi(self):
        for modo in (0, 2, 4, 255):
            for tipo in (0, 3):
                us = armar(tipo, modo)
                info = mira_requerida(us, 0)
                us[0][0x91] = info['orientacao_requerida']
                self.b.mundo(us)
                self.assertTrue(self.b.mira(0))
                self.assertTrue(engin_vise_cible(us, 0))
            for tipo in (12, 15):
                us = armar(tipo, modo)
                us[0][0x94] = angulo_calcul(128, 128, 0, 0, 32)
                self.b.mundo(us)
                self.assertTrue(self.b.mira(0, edi_entrada=0))
                self.assertFalse(self.b.mira(0, edi_entrada=0xffff))
                with self.assertRaises(ValueError):
                    engin_vise_cible(us, 0)


if __name__ == '__main__':
    unittest.main()
