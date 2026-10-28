"""Conclusão da biblioteca, flags independentes e reconstrução das duas listas."""
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(PASTA))
from aprendizagem import Aprendizagem
from construcoes import EconomiaConstrucoes
from producao import Producao, CONTROLE_X87_INICIAL
from proprietarios import PropriedadeConstrucoes, PASSO_ORDENS_JOGADOR, PASSO_PENDENCIAS_JOGADOR
from recrutamento import Recrutamento


def w(m, o, v):
    struct.pack_into('<H', m, o, v & 65535)


def d(m, o, v):
    struct.pack_into('<I', m, o, v & 0xffffffff)


def ler_progresso(a, indice=0):
    return struct.unpack_from('<I', a.producao.recrutamento.mundo.estruturas, indice * 276 + 0x8c)[0]


def preparar(jogador=0, indice=0, tipo=0, tempo=10, progresso=1, quantidade=3, divisor=3):
    r = Recrutamento(EconomiaConstrucoes(estruturas=bytes(1000 * 276)))
    p = Producao(r)
    a = Aprendizagem(p)
    s = r.mundo.estruturas
    o = indice * 276
    s[o + 4], s[o + 5], s[o + 8] = jogador, 4, 6
    s[o + 0x74], s[o + 0x7b] = 1, tipo
    d(s, o + 0x8c, progresso)
    w(s, o + 0xe, 30)
    s[o + 0x4e:o + 0x4e + quantidade] = b'\1' * quantidade
    r.unidades[1] = 9
    for t in range(5):
        w(r.tipos_sortilegios, t * 46, tempo)
    p.tipos_construcoes[6 * 52 + 18] = divisor
    return a


def lista(m, o):
    tamanho = struct.unpack_from('<H', m, o)[0]
    return [(m[o + 0x42 + i], struct.unpack_from('<H', m, o + 6 + 2 * i)[0]) for i in range(tamanho)]


class ExemplosAprendizagem(unittest.TestCase):
    def test_flags_independentes_e_acessores_de_byte(self):
        a = preparar()
        a.inventados[7] = 0x80
        a.propriedade.sortilegios[7] = 255
        self.assertEqual(a.inventado(1, 2), 128)
        self.assertEqual(a.disponivel(1, 2), 255)
        a.liberar(0x101, 0x10002)
        self.assertEqual(a.disponivel(1, 2), 1)
        self.assertEqual(a.inventado(1, 2), 128)
        a.marcar_inventado(1, 2)
        self.assertEqual(a.inventado(1, 2), 1)
        self.assertEqual(a.propriedade.ordens, bytes(10816))
        self.assertEqual(a.propriedade.pendencias, bytes(9152))

    def test_listas_usam_predicados_diferentes_e_preservam_bytes_opacos(self):
        a = preparar(jogador=2)
        a.propriedade.ordens[:] = b'\xa5' * 10816
        a.propriedade.pendencias[:] = b'\x5a' * 9152
        a.inventados[10:15] = bytes((1, 255, 0, 128, 1))
        a.propriedade.sortilegios[10:15] = bytes((0, 2, 255, 0, 0))
        a.atualizar_ordens(2)
        a.atualizar_pesquisas_biblioteca(2)
        for m, o, itens, opaco in ((a.propriedade.ordens, 2 * PASSO_ORDENS_JOGADOR + 416, [1, 2], 0xa5),
                                  (a.propriedade.pendencias, 2 * PASSO_PENDENCIAS_JOGADOR + 624, [0, 3, 4], 0x5a)):
            self.assertEqual(lista(m, o), [(4, i) for i in itens])
            self.assertEqual(struct.unpack_from('<HH', m, o), (len(itens), 5))
            self.assertEqual(struct.unpack_from('<H', m, o + 0x66)[0], len(itens))
            self.assertEqual(m[o + 0x60:o + 0x66], bytes([opaco]) * 6)
            self.assertEqual(m[o - 1], opaco)
            self.assertEqual(m[o + 104], opaco)

    def test_resets_nao_refazem_listas_e_init_ordens_nao_zera_flags(self):
        a = preparar()
        a.inventados[:] = b'\x80' * 20
        a.propriedade.sortilegios[:] = b'\xff' * 20
        a.inicializar_ordens()
        ordens = bytes(a.propriedade.ordens)
        self.assertEqual(a.propriedade.sortilegios, b'\xff' * 20)
        a.zerar_disponiveis(1)
        self.assertEqual(a.inventados, b'\x80' * 20)
        self.assertEqual(a.propriedade.sortilegios, b'\xff' * 5 + bytes(5) + b'\xff' * 10)
        self.assertEqual(a.propriedade.ordens, ordens)
        a.zerar_tecnologia()
        self.assertEqual(a.inventados, bytes(20))
        self.assertEqual(a.propriedade.sortilegios, bytes(20))
        self.assertEqual(a.propriedade.ordens, ordens)

    def test_flag_zero_retorna_antes_da_consulta_de_tempo(self):
        a = preparar()
        s = a.producao.recrutamento.mundo.estruturas
        s[0x74], s[0x7b] = 0, 255
        antes = bytes(s)
        self.assertIsNone(a.calcular_biblioteca(0))
        self.assertEqual(s, antes)
        s[0x74] = 1
        d(s, 0x8c, 0)
        with self.assertRaises(ValueError):
            a.calcular_biblioteca(0)  # Flag ativa consulta tempo mesmo com progresso zero.

    def test_arredondamento_decide_se_conclui_na_mesma_chamada(self):
        a = preparar(progresso=871, quantidade=29, divisor=100)
        a.calcular_biblioteca(0)
        self.assertEqual(ler_progresso(a), 999)
        self.assertEqual(a.disponivel(0, 0), 0)
        a.calcular_biblioteca(0)
        self.assertEqual(ler_progresso(a), 0)
        self.assertEqual(a.disponivel(0, 0), 1)

    def test_conclusao_sem_inventado_e_reset_seletivo(self):
        a = preparar(jogador=3, tipo=4, progresso=1000)
        s = a.producao.recrutamento.mundo.estruturas
        s[0x75:0x8c] = b'\xa5' * (0x8c - 0x75)
        s[0x7b] = 4
        a.calcular_biblioteca(0)
        self.assertEqual(a.disponivel(3, 4), 1)
        self.assertEqual(a.inventados, bytes(20))
        self.assertEqual((s[5], s[0x74], s[0x7b], ler_progresso(a)), (5, 0, 255, 0))
        for campo in (0x78, 0x86):
            self.assertEqual(s[campo:campo + 2], b'\xff\xff')
        for campo in (0x7c, 0x7e, 0x80, 0x82):
            self.assertEqual(s[campo:campo + 2], b'\0\0')
        for campo in (0x75, 0x76, 0x77, 0x7a, 0x84, 0x85, 0x88, 0x89, 0x8a, 0x8b):
            self.assertEqual(s[campo], 0xa5)
        antes = bytes(s), bytes(a.propriedade.ordens), bytes(a.propriedade.pendencias)
        a.calcular_biblioteca(0)
        self.assertEqual((bytes(s), bytes(a.propriedade.ordens), bytes(a.propriedade.pendencias)), antes)

    def test_estado3_preservado_outros_viram5_sem_cobranca(self):
        for estado in (0, 3, 4, 5, 255):
            a = preparar(tempo=0)
            r = a.producao.recrutamento
            r.mundo.estruturas[5] = estado
            r.mundo.economia.memoria[:] = b'\xa5' * 128
            a.calcular_biblioteca(0)
            self.assertEqual(r.mundo.estruturas[5], 3 if estado == 3 else 5)
            self.assertEqual(r.mundo.economia.memoria, b'\xa5' * 128)

    def test_perda_da_ultima_biblioteca_preserva_inventados(self):
        a = preparar(progresso=1000)
        a.inventados[:] = b'\1' * 20
        a.propriedade.bibliotecas[0] = 1
        a.calcular_biblioteca(0)
        a.propriedade.inicializar_neutro(0, 0)
        self.assertEqual(a.propriedade.sortilegios[:5], bytes(5))
        self.assertEqual(a.inventados, b'\1' * 20)
        self.assertEqual(lista(a.propriedade.ordens, 416), [])

    def test_guardas_de_dominio_e_ramos_fora_do_escopo(self):
        a = preparar()
        with self.assertRaises(ValueError):
            Aprendizagem(inventados=bytes(19))
        with self.assertRaises(ValueError):
            Aprendizagem(a.producao, PropriedadeConstrucoes())
        for j, t in ((4, 0), (0, 5), (0, 0x100)):
            with self.assertRaises(ValueError):
                a.disponivel(j, t)
        antes = bytes(a.propriedade.pendencias)
        a.atualizar_pesquisas_biblioteca(4)  # Guarda existente no x86.
        self.assertEqual(a.propriedade.pendencias, antes)
        a.producao.recrutamento.mundo.estruturas[8] = 1
        with self.assertRaises(NotImplementedError):
            a.calcular_biblioteca(0)
        with self.assertRaises(ValueError):
            a.calcular_biblioteca(65535)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: usar --emular')
class DiferencialAprendizagem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_aprendizagem import BancadaAprendizagem
        cls.b = BancadaAprendizagem()

    def setUp(self):
        self.rng = random.Random(0x4259e6)
        self.b.sujeira_pilha = None

    def carregar(self, a):
        self.b.carregar_aprendizagem(a)
        self.guardas = self.b.guardas_aprendizagem(), self.b.guardas(), self.b.outras_guardas()

    def conferir(self, a):
        p = a.producao
        r = p.recrutamento
        m = r.mundo
        esperado = dict(economia=bytes(m.economia.memoria), capacidades=bytes(m.capacidades.memoria),
                        estruturas=bytes(m.estruturas), tipos=bytes(m.terreno.tipos),
                        quantidades=bytes(m.terreno.quantidades), semente=m.terreno.semente,
                        periodo_nova=r.periodo_nova, tipos_construcoes=bytes(p.tipos_construcoes),
                        ajuste_hospital=p.ajuste_hospital & 255, inventados=bytes(a.inventados),
                        jogador_deposito=a.propriedade.jogador_deposito)
        for objeto, campos in ((r, ('selecoes', 'tipos_unidades', 'tipos_sortilegios', 'unidades')),
                               (a.propriedade, ('bibliotecas', 'baloes', 'numeros_unidades', 'pendencias', 'ordens', 'sortilegios'))):
            esperado.update({k: bytes(getattr(objeto, k)) for k in campos})
        atual = self.b.estado()
        atual.update(self.b.estado_recrutamento())
        atual.update(self.b.estado_producao())
        atual.update(self.b.estado_aprendizagem())
        for campo, valor in atual.items():
            if valor != esperado[campo] and isinstance(valor, bytes):
                i = next(i for i, (x, y) in enumerate(zip(valor, esperado[campo])) if x != y)
                self.fail(f'{campo}[{i:#x}]: x86={valor[i]:#x}, Python={esperado[campo][i]:#x}')
            self.assertEqual(valor, esperado[campo], campo)
        self.assertEqual((self.b.guardas_aprendizagem(), self.b.guardas(), self.b.outras_guardas()), self.guardas)

    def helper(self, a, entrada, metodo, *args, edx=None, consulta=False, carregar=True):
        if carregar:
            self.carregar(a)
        esperado = getattr(a, metodo)(*args)
        regs = self.b.chamar_aprendizagem(entrada, args[0] if args else 0,
                                         edx if edx is not None else (args[1] if len(args) > 1 else 0))
        if consulta:
            self.assertEqual(regs['EAX'] & 255, esperado)
        self.conferir(a)

    def calcular(self, a, indice=0, carregar=True):
        from emulador import RETORNO, x86
        if carregar:
            self.carregar(a)
        s = a.producao.recrutamento.mundo.estruturas
        o = (indice & 65535) * 276
        flag, progress = s[o + 0x74], ler_progresso(a, indice & 65535)
        a.calcular_biblioteca(indice)
        regs = {k: self.rng.getrandbits(32) for k in ('EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')}
        atual = self.b.chamar_aprendizagem(0x4259e6, indice, regs['EDX'], regs)
        self.assertEqual(atual['EIP'], RETORNO)
        for k, v in regs.items():
            self.assertEqual(atual[k], v, k)
        self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_FPCW), CONTROLE_X87_INICIAL)
        self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_FPTAG), 0xffff)
        chamadas = self.b.acessos_aprendizagem
        tempos = sum(c['entrada'] == 0x47476a for c in chamadas)
        self.assertEqual(tempos, 0 if flag == 0 else 1 if progress == 0 else 3)
        efeitos = [c['entrada'] for c in chamadas if c['entrada'] in (0x474974, 0x474a38, 0x41c76c)]
        concluiu = flag != 0 and s[o + 0x74] == 0
        self.assertEqual(efeitos, [0x474974, 0x474a38, 0x41c76c] if concluiu else [])
        self.assertFalse(any(c['entrada'] in (0x4678f2, 0x46792c) for c in self.b.chamadas))
        self.conferir(a)

    def test_320_acessores_flags_preservam_tabelas_e_listas(self):
        for j in range(4):
            for tipo in range(5):
                for valor in (0, 1, 128, 255):
                    for entrada, metodo, consulta in ((0x474958, 'disponivel', True), (0x474991, 'inventado', True),
                                                      (0x474974, 'liberar', False), (0x4749ad, 'marcar_inventado', False)):
                        a = preparar()
                        a.inventados[:] = self.rng.randbytes(20)
                        a.propriedade.sortilegios[:] = self.rng.randbytes(20)
                        a.propriedade.ordens[:] = self.rng.randbytes(10816)
                        a.propriedade.pendencias[:] = self.rng.randbytes(9152)
                        a.inventados[j * 5 + tipo] = valor
                        a.propriedade.sortilegios[j * 5 + tipo] = valor
                        self.helper(a, entrada, metodo, j | 0xabcd0000, tipo | 0x13570000, consulta=consulta)

    def test_2048_listas_todas_combinacoes_de_flags(self):
        for disponiveis in range(32):
            for inventados in range(32):
                a = preparar()
                j = (disponiveis + inventados) % 4
                a.propriedade.ordens[:] = self.rng.randbytes(10816)
                a.propriedade.pendencias[:] = self.rng.randbytes(9152)
                a.inventados[:] = self.rng.randbytes(20)
                a.propriedade.sortilegios[:] = self.rng.randbytes(20)
                for t in range(5):
                    a.inventados[j * 5 + t] = 128 if inventados & (1 << t) else 0
                    a.propriedade.sortilegios[j * 5 + t] = 255 if disponiveis & (1 << t) else 0
                self.helper(a, 0x474a38, 'atualizar_ordens', j)
                self.helper(a, 0x41c76c, 'atualizar_pesquisas_biblioteca', j, edx=0xff000006)

    def test_256_guardas_originais_da_tecnologia_de_biblioteca(self):
        for j in range(256):
            a = preparar()
            a.inventados[:] = b'\1' * 20
            a.propriedade.pendencias[:] = b'\xa5' * 9152
            self.helper(a, 0x41c76c, 'atualizar_pesquisas_biblioteca', j | 0xff000000, edx=6)

    def test_256_resets_e_reconstrucao_global_em_sequencia(self):
        for n in range(64):
            a = preparar()
            a.inventados[:] = self.rng.randbytes(20)
            a.propriedade.sortilegios[:] = self.rng.randbytes(20)
            a.propriedade.ordens[:] = self.rng.randbytes(10816)
            self.carregar(a)
            self.helper(a, 0x474a95, 'inicializar_ordens', carregar=False)
            self.helper(a, 0x4749ca, 'zerar_disponiveis', n % 4, carregar=False)
            self.helper(a, 0x4749f2, 'zerar_tecnologia', carregar=False)
            self.helper(a, 0x474a95, 'inicializar_ordens', carregar=False)

    def test_512_bibliotecas_com_estados_limites_e_campos_opacos(self):
        for n in range(512):
            j, indice, tipo = n % 4, self.rng.choice((0, 1, 999)), n % 5
            tempo = self.rng.choice((0, 1, 10, 65535))
            progress = self.rng.choice((0, 1, max(0, tempo * 100 - 1), tempo * 100, 0xffffffff))
            a = preparar(j, indice, tipo, tempo, progress, self.rng.randrange(31), self.rng.randrange(256))
            r = a.producao.recrutamento
            s = r.mundo.estruturas
            o = indice * 276
            s[o + 0x75:o + 0x8c] = self.rng.randbytes(0x8c - 0x75)
            s[o + 0x7b] = tipo
            s[o + 5] = self.rng.randrange(256)
            s[o + 0x74] = self.rng.choice((0, 1, 255))
            a.inventados[:] = self.rng.randbytes(20)
            a.propriedade.sortilegios[:] = self.rng.randbytes(20)
            a.propriedade.ordens[:] = self.rng.randbytes(10816)
            a.propriedade.pendencias[:] = self.rng.randbytes(9152)
            r.mundo.economia.memoria[:] = self.rng.randbytes(128)
            r.mundo.capacidades.memoria[:] = self.rng.randbytes(24)
            self.b.sujeira_pilha = n & 255
            self.calcular(a, indice | 0xfefe0000)

    def test_sequencias_de_aprendizagem_e_chamadas_apos_conclusao(self):
        for j in range(4):
            for tipo in range(5):
                a = preparar(jogador=j, tipo=tipo, tempo=2, quantidade=0)
                a.inventados[:] = b'\1' * 20
                self.carregar(a)
                for _ in range(4):
                    self.calcular(a, carregar=False)
                self.assertEqual(a.disponivel(j, tipo), 1)
                self.assertEqual(ler_progresso(a), 0)
        # Arredondamento decide se o ramo de conclusão é executado.
        a = preparar(progresso=871, quantidade=29, divisor=100)
        self.calcular(a)
        self.assertEqual(ler_progresso(a), 999)
        self.calcular(a, carregar=False)
        self.assertEqual(ler_progresso(a), 0)

    def test_256_estados_da_construcao_e_inatividade_com_tipo_invalido(self):
        for estado in range(256):
            a = preparar(progresso=1000)
            a.producao.recrutamento.mundo.estruturas[5] = estado
            self.calcular(a)
        for indice in (0, 999):
            a = preparar(indice=indice)
            s = a.producao.recrutamento.mundo.estruturas
            s[indice * 276 + 0x74], s[indice * 276 + 0x7b] = 0, 255
            self.calcular(a, indice)


if __name__ == '__main__':
    unittest.main()
