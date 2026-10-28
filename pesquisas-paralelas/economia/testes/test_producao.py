"""Avanço, Bag modo 1, arredondamento e preservação de estado econômico."""
import json
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(PASTA))
from producao import Producao, incremento_producao, CONTROLE_X87_INICIAL
from construcoes import EconomiaConstrucoes
from recrutamento import Recrutamento


def w(m, o, v):
    struct.pack_into('<H', m, o, v & 65535)


def d(m, o, v):
    struct.pack_into('<I', m, o, v & 0xffffffff)


def progresso(p, indice=0):
    return struct.unpack_from('<I', p.recrutamento.mundo.estruturas, indice * 276 + 0x8c)[0]


def preparar(tipo=1, indice=0, quantidade=3, divisor=8):
    p = Producao(Recrutamento(EconomiaConstrucoes(estruturas=bytes(1000 * 276))))
    r = p.recrutamento
    s = r.mundo.estruturas
    o = indice * 276
    s[o + 8], s[o + 0x74] = tipo, 1
    w(r.selecoes, 0, indice)
    d(s, o + 0x8c, 1)
    w(s, o + 0xe, 30)
    s[o + 0x4e:o + 0x4e + quantidade] = b'\1' * quantidade
    r.unidades[1] = 9  # Todos os slots etiquetados referenciam a mesma unidade.
    for t in range(26):
        w(r.tipos_unidades, t * 50, 65535)
    for t in range(5):
        w(r.tipos_sortilegios, t * 46, 65535)
    p.tipos_construcoes[tipo * 52 + 18] = divisor
    return p


class ExemplosProducao(unittest.TestCase):
    def test_base_sem_trabalhadores_e_retorno_nao_indica_conclusao(self):
        p = preparar(quantidade=0)
        self.assertTrue(p.avancar_unidade(0))
        self.assertEqual(progresso(p), 101)
        self.assertTrue(p.avancar_sortilegio(0))
        self.assertEqual(progresso(p), 201)

    def test_ultrapassagem_sem_finalizacao_e_limite_ja_atingido(self):
        p = preparar(quantidade=2)
        r = p.recrutamento
        w(r.tipos_unidades, 0, 10)
        d(r.mundo.estruturas, 0x8c, 999)
        self.assertTrue(p.avancar_unidade(0))
        self.assertEqual(progresso(p), 1124)
        antes = bytes(r.mundo.estruturas)
        self.assertTrue(p.avancar_unidade(0))
        self.assertEqual(r.mundo.estruturas, antes)
        self.assertEqual(r.mundo.estruturas[0x74], 1)
        self.assertEqual(r.status(0, 0), 112)

    def test_inativo_e_ordem_das_consultas(self):
        for campo, valor in ((0x8c, 0), (0x74, 0)):
            p = preparar()
            s = p.recrutamento.mundo.estruturas
            s[campo] = valor
            s[0x7b] = 255
            self.assertFalse(p.avancar_unidade(0))  # Não consulta tipo inválido.
            with self.assertRaises(ValueError):
                p.avancar_sortilegio(0)  # Consulta antes de verificar atividade.

    def test_tempo_zero_impede_incremento_sem_acessar_bag_ou_tipo_construcao(self):
        p = preparar()
        r = p.recrutamento
        r.mundo.estruturas[8] = 255
        w(r.mundo.estruturas, 0xe, 65535)
        w(r.tipos_unidades, 0, 0)
        self.assertTrue(p.avancar_unidade(0))
        self.assertEqual(progresso(p), 1)

    def test_bag_usa_capacidade_etiqueta_e_tipo_da_unidade(self):
        p = preparar(quantidade=0)
        r = p.recrutamento
        s = r.mundo.estruturas
        w(s, 0xe, 4)
        w(s, 0xc, 0)  # Contagem não controla a varredura.
        s[0x4e:0x54] = bytes((1, 1, 2, 1, 1, 1))
        for slot, unidade in enumerate((799, 799, 65535, 3)):
            w(s, 0x12 + slot * 2, unidade)
        r.unidades[799 * 276 + 1] = 9
        r.unidades[3 * 276 + 1] = 7
        antes = bytes(s), bytes(r.unidades)
        self.assertEqual(p.contar_unidades(0), 2)
        self.assertEqual(p.contar_unidades(0, 7), 1)
        self.assertEqual(p.contar_unidades(0, 0x10009), 2)
        self.assertEqual(p.contar_unidades(0, 0x109), 0)
        self.assertEqual((bytes(s), bytes(r.unidades)), antes)

    def test_garagem_hospital_e_wrap_do_divisor(self):
        p = preparar(tipo=14, quantidade=3, divisor=4)
        p.avancar_unidade(0)
        self.assertEqual(progresso(p), 111)  # 100 + trunc(3 / (4-1) * 10).
        p = preparar(tipo=19, quantidade=3, divisor=7)
        p.avancar_unidade(0)
        self.assertEqual(progresso(p), 251)  # 100 + trunc(3 / (7-5) * 100).
        p = preparar(tipo=14, quantidade=30, divisor=0)
        p.avancar_unidade(0)
        self.assertEqual(progresso(p), 102)  # 0-1 -> 255.

    def test_arredondamento_e_zero_mascarado(self):
        self.assertEqual(incremento_producao(29, 100, 100), 128)
        self.assertNotEqual(incremento_producao(29, 100, 100), 100 + 29 * 100 // 100)
        self.assertEqual(incremento_producao(0, 0, 100), 100)
        self.assertEqual(incremento_producao(30, 0, 10), 100)

    def test_guardas_adicionais_de_dominio(self):
        with self.assertRaises(ValueError):
            Producao(tipos_construcoes=bytes(52))
        for args in ((31, 1, 10), (1, 256, 10), (1, 1, 20), (-1, 1, 10)):
            with self.assertRaises(ValueError):
                incremento_producao(*args)
        p = preparar()
        with self.assertRaises(ValueError):
            p.avancar_unidade(65535)
        s = p.recrutamento.mundo.estruturas
        w(s, 0xe, 31)
        with self.assertRaises(ValueError):
            p.contar_unidades(0)
        w(s, 0xe, 1)
        w(s, 0x12, 800)
        with self.assertRaises(ValueError):
            p.contar_unidades(0)
        s[0x4e] = 0  # Referência inválida não é lida sem etiqueta 1.
        self.assertEqual(p.contar_unidades(0), 0)
        s[8] = 255
        with self.assertRaises(ValueError):
            p.avancar_unidade(0)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: usar --emular')
class DiferencialProducao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_producao import BancadaProducao
        cls.b = BancadaProducao()

    def setUp(self):
        self.rng = random.Random(0x423b9b)
        self.b.sujeira_pilha = None

    def carregar(self, p):
        self.b.carregar_producao(p)
        self.guardas = self.b.guardas_producao()

    def conferir(self, p):
        r = p.recrutamento
        m = r.mundo
        esperado = dict(economia=bytes(m.economia.memoria), capacidades=bytes(m.capacidades.memoria),
                        estruturas=bytes(m.estruturas), tipos=bytes(m.terreno.tipos),
                        quantidades=bytes(m.terreno.quantidades), semente=m.terreno.semente,
                        periodo_nova=r.periodo_nova, tipos_construcoes=bytes(p.tipos_construcoes),
                        ajuste_hospital=p.ajuste_hospital & 255)
        esperado.update({k: bytes(getattr(r, k)) for k in ('selecoes', 'tipos_unidades', 'tipos_sortilegios', 'unidades')})
        atual = self.b.estado()
        atual.update(self.b.estado_recrutamento())
        atual.update(self.b.estado_producao())
        for campo, valor in atual.items():
            if valor != esperado[campo] and isinstance(valor, bytes):
                i = next(i for i, (a, b) in enumerate(zip(valor, esperado[campo])) if a != b)
                self.fail(f'{campo}[{i:#x}]: x86={valor[i]:#x}, Python={esperado[campo][i]:#x}')
            self.assertEqual(valor, esperado[campo], campo)
        self.assertEqual(self.b.guardas_producao(), self.guardas)
        self.assertEqual(self.b.guardas(), (b'\xa6' * 16, b'\x6a' * 16))
        self.assertEqual(self.b.outras_guardas(), (b'\xc7' * 8, b'\x7c' * 8, b'\xe9' * 8, b'\x9e' * 8, 0x12345678))

    def avancar(self, p, indice=0, sortilegio=False, carregar=True):
        from emulador import RETORNO, x86
        if carregar:
            self.carregar(p)
        esperado = (p.avancar_sortilegio if sortilegio else p.avancar_unidade)(indice)
        regs = {k: self.rng.getrandbits(32) for k in ('EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')}
        atual = self.b.avancar(indice, sortilegio, regs)
        self.assertEqual(atual['EIP'], RETORNO)
        self.assertEqual(atual['EAX'] & 255, esperado)
        for k, valor in regs.items():
            self.assertEqual(atual[k], valor, k)
        self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_FPCW), CONTROLE_X87_INICIAL)
        self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_FPTAG), 0xffff)
        self.conferir(p)

    def test_flags_limites_tempos_e_ordem_das_consultas(self):
        for sortilegio in (False, True):
            for tempo in (0, 1, 65535):
                for flag in (0, 1, 255):
                    for valor in sorted({0, 1, max(0, tempo * 100 - 1), tempo * 100, 0xffffffff}):
                        for indice in (0, 999):
                            p = preparar(indice=indice)
                            r = p.recrutamento
                            o = indice * 276
                            r.mundo.estruturas[o + 0x74] = flag
                            d(r.mundo.estruturas, o + 0x8c, valor)
                            w(r.tipos_unidades, 0, tempo)
                            w(r.tipos_sortilegios, 0, tempo)
                            self.b.sujeira_pilha = 0xa5
                            self.avancar(p, indice | 0xfade0000, sortilegio)
                            ativo = valor != 0 and flag != 0
                            esperado = int(sortilegio) + int(ativo)
                            alvo = 0x47476a if sortilegio else 0x4410b7
                            self.assertEqual(self.b.acessos_producao.count(alvo), esperado)
                            self.assertEqual(self.b.acessos_producao.count(0x4471b8), int(ativo and valor < tempo * 100))

    def test_bag_modo1_capacidades_etiquetas_referencias_e_duplicatas(self):
        for capacidade in range(31):
            p = preparar(quantidade=0, indice=999)
            r = p.recrutamento
            s = r.mundo.estruturas
            o = 999 * 276
            w(s, o + 0xe, capacidade)
            w(s, o + 0xc, self.rng.randrange(65536))
            for slot in range(30):
                etiqueta = self.rng.randrange(8)
                s[o + 0x4e + slot] = etiqueta
                unidade = self.rng.choice((0, 1, 799)) if etiqueta == 1 else 65535
                w(s, o + 0x12 + slot * 2, unidade)
            r.unidades[1], r.unidades[277], r.unidades[799 * 276 + 1] = 9, 7, 255
            for tipo in (0, 7, 9, 255, 256, 0x10009):
                with self.subTest(capacidade=capacidade, tipo=tipo):
                    self.carregar(p)
                    self.assertEqual(self.b.contar(999, tipo), p.contar_unidades(999, tipo))
                    self.conferir(p)

    def test_15872_combinacoes_float_no_corpo_original_completo(self):
        # Todas as contagens protegidas × todos os divisores u8 × ambos coeficientes.
        for tipo in (1, 14):
            for quantidade in range(31):
                p = preparar(tipo=tipo, quantidade=quantidade)
                for divisor in range(256):
                    with self.subTest(tipo=tipo, quantidade=quantidade, divisor=divisor):
                        p.tipos_construcoes[tipo * 52 + 18] = (divisor + (tipo == 14)) & 255
                        d(p.recrutamento.mundo.estruturas, 0x8c, 1)
                        self.avancar(p)
                        if divisor == 0:
                            self.assertEqual(self.b.conversao_inteira, 0x80000000)

    def test_2048_ajustes_u8_de_garagem_e_hospital_nas_duas_rotinas(self):
        for sortilegio in (False, True):
            for tipo, ajuste in ((14, 5), (19, 0), (19, 5), (19, 255)):
                p = preparar(tipo=tipo, quantidade=17)
                p.ajuste_hospital = ajuste
                for bruto in range(256):
                    p.tipos_construcoes[tipo * 52 + 18] = bruto
                    d(p.recrutamento.mundo.estruturas, 0x8c, 1)
                    self.avancar(p, sortilegio=sortilegio)

    def test_512_estados_variados_preservam_memoria_e_saldos(self):
        for n in range(512):
            sortilegio = bool(n % 2)
            indice = self.rng.choice((0, 1, 999))
            tipo = n % 22
            p = preparar(tipo=tipo, indice=indice)
            r = p.recrutamento
            s = r.mundo.estruturas
            o = indice * 276
            s[o:o + 276] = self.rng.randbytes(276)
            s[o + 8], s[o + 0x74] = tipo, self.rng.randrange(1, 256)
            s[o + 0x7b] = self.rng.randrange(5 if sortilegio else 26)
            d(s, o + 0x8c, self.rng.randrange(1, 6553500))
            w(s, o + 0xe, self.rng.randrange(31))
            for slot in range(30):
                s[o + 0x4e + slot] = self.rng.randrange(4)
                unidade = self.rng.randrange(800)
                w(s, o + 0x12 + slot * 2, unidade)
                r.unidades[unidade * 276 + 1] = self.rng.choice((0, 7, 9, 25))
            r.mundo.economia.memoria[:] = self.rng.randbytes(128)
            r.mundo.capacidades.memoria[:] = self.rng.randbytes(24)
            p.tipos_construcoes[:] = self.rng.randbytes(1144)
            p.ajuste_hospital = self.rng.randrange(256)
            self.b.sujeira_pilha = n & 255
            self.avancar(p, indice | 0xabcd0000, sortilegio)

    def test_sequencias_tipos_reais_e_consultas_de_status(self):
        parametros = json.loads((PASTA / 'evidencias/parametros-producao.json').read_text())
        tipos = bytes.fromhex(''.join(t['registro_hex'] for t in parametros['tipos']))
        unidades = json.loads((PASTA.parents[1] / 'relatorios/unidades.json').read_text())['unidades']
        for sortilegio, total in ((False, 26), (True, 5)):
            for solicitado in range(total):
                p = preparar(tipo=6 if sortilegio else 1, quantidade=3)
                p.tipos_construcoes[:] = tipos
                r = p.recrutamento
                for u in unidades:
                    r.tipos_unidades[u['id'] * 50:(u['id'] + 1) * 50] = bytes.fromhex(u['registro_memoria_hex'])
                if sortilegio:
                    w(r.tipos_sortilegios, solicitado * 46, 20 + solicitado)
                    r.mundo.estruturas[0x7b] = solicitado
                else:
                    # Liga com o início Python já validado; geometria continua callback explícito.
                    r.mundo.estruturas[0x74] = 0
                    for recurso in (0, 1, 2):
                        r.mundo.economia.atribuir(0, recurso, 9999)
                    self.assertTrue(r.iniciar(solicitado, 0, escolher_saida=lambda i: 0x1234))
                self.carregar(p)
                for _ in range(24):
                    self.avancar(p, sortilegio=sortilegio, carregar=False)
                    atual = self.b.chamar(0x423f9d, 0, solicitado)['EAX']
                    self.assertEqual(atual, r.calcular_status(0, solicitado))
                    self.conferir(p)

    def test_controle_inicial_e_diferenca_de_precisao(self):
        from emulador import x86
        self.assertEqual(struct.unpack('<H', self.b.cpu.mem_read(0x4993dc, 2))[0], CONTROLE_X87_INICIAL)
        for a, valor in ((0x4943e7, 10.), (0x4943ef, 100.), (0x494402, 10.), (0x49440a, 100.)):
            self.assertEqual(struct.unpack('<d', self.b.cpu.mem_read(a, 8))[0], valor)
        for sortilegio in (False, True):
            for controle, esperado in ((0x127f, 129), (0x037f, 130)):
                p = preparar(quantidade=29, divisor=100)
                self.carregar(p)
                self.b.avancar(0, sortilegio, controle=controle)
                self.assertEqual(struct.unpack_from('<I', self.b.estado()['estruturas'], 0x8c)[0], esperado)
                self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_FPCW), controle)


if __name__ == '__main__':
    unittest.main()
