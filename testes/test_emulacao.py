"""Comparações diferenciais opcionais com instruções reais, não mock de fórmula.

Ativar com RISING_EMULAR=1. No sandbox macOS o JIT do Unicorn pode gerar SIGILL;
executar a bancada com autorização para memória JIT quando necessário.
"""
import os
import random
import struct
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from movimento import (direcao_entre_celulas, celula_vizinha, distancia_quadratica,
                       atualizar_orientacao, integrar_prefixo_passo, pode_avancar, PARAMETROS_TIPOS)
from unidades import curar_com_limite
from combate import dano_bruto_unidade, reduzir_dano, aplicar_dano_parcial


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialX86(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from emulador import BancadaX86
        cls.bancada = BancadaX86()

    def test_cura_2000_entradas_mais_limites(self):
        aleatorio = random.Random(41997)
        casos = [(80, 20, 100), (80, 21, 100), (65535, 1, 100)]
        casos += [(aleatorio.randrange(65536), aleatorio.randrange(65536),
                   aleatorio.randrange(65536)) for _ in range(2000)]
        for vida, acrescimo, limite in casos:
            u = bytearray(276)
            struct.pack_into('<H', u, 0x9a, vida)
            self.bancada.escrever_unidade(u)
            self.bancada.cpu.mem_write(0x4965b6, struct.pack('<H', limite))
            r = self.bancada.executar(0x457122, [(0x457122, 0x45718a)], dict(EDX=acrescimo))
            resultado = (struct.unpack_from('<H', self.bancada.ler_unidade(), 0x9a)[0], bool(r['EAX'] & 255))
            self.assertEqual(resultado, curar_com_limite(vida, acrescimo, limite))

    def test_direcao_e_distancia_1024_pares(self):
        aleatorio = random.Random(477042)
        for _ in range(1024):
            a, b = aleatorio.randrange(65536), aleatorio.randrange(65536)
            r = self.bancada.executar(0x477042, [(0x477042, 0x4770ee)], dict(EAX=a, EDX=b))
            self.assertEqual(r['EAX'] & 255, direcao_entre_celulas(a, b))
            xy = [aleatorio.randrange(65536) for _ in range(4)]
            r = self.bancada.executar(0x479555, [(0x479555, 0x4795af)],
                                     dict(EAX=xy[0], EDX=xy[1], EBX=xy[2], ECX=xy[3]))
            self.assertEqual(r['EAX'], distancia_quadratica(*xy))

    def test_vizinhos_interior_bordas_e_direcoes_pares(self):
        for largura, altura in [(1, 1), (64, 64), (128, 192), (256, 256)]:
            self.bancada.cpu.mem_write(0x497168, struct.pack('<HH', largura, altura))
            for x in sorted({0, largura // 2, largura - 1}):
                for y in sorted({0, altura // 2, altura - 1}):
                    for d in range(17):
                        celula = x + 256 * y
                        r = self.bancada.executar(0x4770ee, [(0x4770ee, 0x4772ec)], dict(EAX=celula, EDX=d))
                        self.assertEqual(r['EAX'] & 65535, celula_vizinha(celula, d, largura, altura))

    def test_orientacao_todas_as_combinacoes_e_contadores(self):
        for desejada in range(1, 17):
            for atual in range(1, 17):
                for contador, periodo in [(0, 1), (0, 2), (1, 2), (255, 0)]:
                    u = bytearray(276)
                    u[0x90:0x94] = bytes([desejada, atual, contador, periodo])
                    self.bancada.escrever_unidade(u)
                    self.bancada.executar(0x448599, [(0x448599, 0x448699)])
                    v = self.bancada.ler_unidade()
                    self.assertEqual((v[0x91], v[0x92]), atualizar_orientacao(desejada, atual, contador, periodo))
                # Início de trecho no qual ESI aponta para a unidade, sem executar chamadas.
                from emulador import UNIDADES
                u[0x90], u[0x91] = desejada, atual
                self.bancada.escrever_unidade(u)
                r = self.bancada.executar(0x4490fd, [(0x4490fd, 0x44915d)],
                                         dict(ESI=UNIDADES), parada=0x44915d)
                self.assertEqual(bool(r['EAX'] & 255), pode_avancar(desejada, atual))

    def test_integracao_prefixo_1024_casos_com_overflow(self):
        aleatorio = random.Random(448704)
        for _ in range(1024):
            dx, dy, progresso, incremento, desconto = [aleatorio.randrange(256) for _ in range(5)]
            d = aleatorio.randrange(17)
            u = bytearray(276)
            u[0x86], u[0x87], u[0x90], u[0x97], u[0x98] = dx, dy, d, progresso, incremento
            self.bancada.escrever_unidade(u)
            self.bancada.executar(0x448704, [(0x448704, 0x44889f)], dict(EDX=desconto), parada=0x44889f)
            v = self.bancada.ler_unidade()
            esperado = integrar_prefixo_passo(dx, dy, progresso, d, incremento, desconto)
            self.assertEqual((v[0x86], v[0x87], v[0x97]),
                             (esperado['deslocamento_x_u8'], esperado['deslocamento_y_u8'], esperado['progresso']))

    def test_inicializadores_dos_26_tipos(self):
        for tipo, esperado in enumerate(PARAMETROS_TIPOS):
            u = bytearray(276)
            u[1] = tipo
            self.bancada.escrever_unidade(u)
            # O druida consulta modificador 12. A tabela de modificadores permanece
            # zerada nesta bancada; os quatro campos examinados não dependem dele.
            self.bancada.executar(0x457350, [(0x457350, 0x457b87), (0x428cc0, 0x428e71)])
            v = self.bancada.ler_unidade()
            self.assertEqual(tuple(v[i] for i in (0x98, 0x93, 0xa5, 0xa7)), esperado)

    def test_adicoes_de_dano_512_casos(self):
        from emulador import UNIDADES, PILHA
        aleatorio = random.Random(4503)
        for _ in range(512):
            base, bonus, mod5, proximidade = [aleatorio.randrange(256) for _ in range(4)]
            atacante = bytearray(276)
            atacante[0], atacante[1], atacante[0xf7] = 2, 7, bonus
            self.bancada.escrever_unidade(atacante, 1)
            self.bancada.cpu.mem_write(0x4dfba0 + 2 * 468 + 7 * 18 + 8, struct.pack('<H', mod5))
            self.bancada.executar(0x4503de, [(0x4503de, 0x450410), (0x428cc0, 0x428e71)],
                                  dict(EAX=base, EBP=UNIDADES + 276, EBX=7), parada=0x450410)
            intermediario = bytes(self.bancada.cpu.mem_read(PILHA + 0x8020, 1))
            self.bancada.cpu.mem_write(0x4965ac, bytes([proximidade]))
            self.bancada.executar(0x450430, [(0x450430, 0x45043f)],
                                  parada=0x45043f, pilha={0x20: intermediario})
            resultado = self.bancada.cpu.mem_read(PILHA + 0x8020, 1)[0]
            self.assertEqual(resultado, dano_bruto_unidade(base, bonus, mod5, proximidade))

    def test_reducao_dano_512_casos(self):
        from emulador import UNIDADES, PILHA
        aleatorio = random.Random(4505)
        for _ in range(512):
            bruto, reducao, modificador = [aleatorio.randrange(256) for _ in range(3)]
            alvo, atacante = bytearray(276), bytearray(276)
            alvo[0xf6] = reducao
            atacante[0], atacante[1] = 2, 7
            self.bancada.escrever_unidade(alvo)
            self.bancada.escrever_unidade(atacante, 1)
            self.bancada.cpu.mem_write(0x4dfba0 + 2 * 468 + 7 * 18 + 10, bytes([modificador]))
            self.bancada.executar(0x45059c, [(0x45059c, 0x4505d8), (0x428cc0, 0x428e71)],
                                  dict(ESI=UNIDADES, EBP=UNIDADES + 276), parada=0x4505d8,
                                  pilha={0x20: bytes([bruto])})
            resultado = self.bancada.cpu.mem_read(PILHA + 0x8020, 1)[0]
            self.assertEqual(resultado, reduzir_dano(bruto, reducao, modificador))

    def test_aplicacao_dano_512_casos_e_zero_protegido(self):
        from emulador import UNIDADES
        aleatorio = random.Random(4506)
        casos = [(100, 0, True), (100, 20, False), (20, 20, False)]
        casos += [(aleatorio.randrange(65536), aleatorio.randrange(256), bool(aleatorio.randrange(2)))
                  for _ in range(512)]
        for vida, dano, protegido in casos:
            u = bytearray(276)
            struct.pack_into('<H', u, 0x9a, vida)
            u[0xdc] = 8 if protegido else 0
            self.bancada.escrever_unidade(u)
            r = self.bancada.executar(0x450644, [(0x450644, 0x4506a1), (0x467d97, 0x467da6)],
                                     dict(ESI=UNIDADES, EDI=0), parada={0x45069c, 0x4506a1},
                                     pilha={0x20: bytes([dano])})
            esperado = aplicar_dano_parcial(vida, dano, protegido)
            self.assertEqual(r['EIP'] == 0x4506a1, esperado['entra_no_ramo_morte'])
            if not esperado['entra_no_ramo_morte']:
                self.assertEqual(struct.unpack_from('<H', self.bancada.ler_unidade(), 0x9a)[0], esperado['vida'])

    def test_consulta_de_proximidade_nao_filtra_capitao(self):
        grade = 0x1100000
        self.bancada.cpu.mem_map(grade, 0x20000)
        self.bancada.cpu.mem_write(0x4e0f38, struct.pack('<I', grade))
        for tipo in (0, 2, 9, 24):
            for mesmo_dono in (False, True):
                for celula, dentro in ((0x0a0a, True), (0x0a0b, True), (0x0b0b, False)):
                    u = bytearray(276)
                    u[0], u[1], u[2] = (0 if mesmo_dono else 1), tipo, 7
                    self.bancada.escrever_unidade(u)
                    self.bancada.cpu.mem_write(grade, b'\xff' * 0x20000)
                    self.bancada.cpu.mem_write(grade + celula * 2, struct.pack('<H', 0x4000))
                    r = self.bancada.executar(0x4500e4,
                        [(0x4500e4, 0x450286), (0x479555, 0x4795af),
                         (0x442bbe, 0x442bc5), (0x44271b, 0x442722)],
                        dict(EAX=2, EDX=0, EBX=0x0a0a, ECX=1))
                    self.assertEqual(bool(r['EAX'] & 255), mesmo_dono and dentro)


if __name__ == '__main__':
    unittest.main()
