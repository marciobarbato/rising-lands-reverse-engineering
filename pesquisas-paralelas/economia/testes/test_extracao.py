"""Minas, coleta, crescimento e propagação: exemplos e diferencial x86."""
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(PASTA))
from construcoes import EconomiaConstrucoes
from extracao import RecursosTerreno


def estado(**kwargs):
    m = EconomiaConstrucoes()
    r = RecursosTerreno(m.terreno, **kwargs)
    return m, r


def mina(r, indice, celula, capacidade):
    struct.pack_into('<HH', r.minas, indice * 4, celula, capacidade)


def mosaico(r, celula, valor=0x84):
    struct.pack_into('<H', r.mosaicos, (celula & 65535) * 2, valor)


def fixture_eta(arquivo):
    """Cópia de camadas/registros; não executa MissionLoad nem simula unidades."""
    sys.path.insert(0, str(PASTA.parents[1] / 'ferramentas'))
    from formatos import ler_eta
    bruto = arquivo.read_bytes()
    lido = ler_eta(bruto)
    tabela = next(b for b in lido['blocos'] if b['nome'] == 'tabela_47534a')
    n = tabela['quantidade']
    if n > 20:
        raise ValueError('Corpus excede os vinte registros de minas')
    registros = bruto[tabela['offset'] + 2:tabela['fim']]
    m, r = estado(minas=registros + bytes(80 - len(registros)),
                  mosaicos=bruto[0x10004:0x30004], atributos=bruto[4:0x10004])
    m.terreno.tipos[:] = bruto[0x30004:0x40004]
    m.terreno.quantidades[:] = bruto[0x40004:0x50004]
    # Normalização documentada de MissionLoad; ainda não é o carregador inteiro.
    for c, tipo in enumerate(m.terreno.tipos):
        if tipo == 0x36:
            m.terreno.tipos[c] = 0x42
            m.terreno.quantidades[c] = 1
    return m, r, n


class ExemplosExtracao(unittest.TestCase):
    def test_busca_primeira_mina_ignora_capacidade_e_origem_zero(self):
        _, r = estado()
        mina(r, 0, 0, 99)
        mina(r, 1, 0x10ff, 0)
        mina(r, 2, 0x1100, 200)
        self.assertEqual(r.indice_mina(0), 65535)
        for c in (0x10ff, 0x1100, 0x11ff, 0x1200):
            self.assertEqual(r.indice_mina(c | 0xabcd0000), 1)
        mina(r, 1, 65535, 0)
        self.assertEqual(r.indice_mina(0), 65535)  # +1 não é truncado nesta busca.

    def test_retirada_saturada_e_esgotamento_em_igualdade(self):
        _, r = estado()
        mina(r, 19, 0x20ff, 3)
        self.assertEqual(r.retirar_mina(19, 2), 2)
        self.assertEqual(r.capacidade_mina(19), 1)
        self.assertEqual(r.mosaicos, bytes(131072))
        self.assertEqual(r.recolher_mina(0x2200), 1)
        self.assertEqual(r.capacidade_mina(19), 0)
        self.assertEqual(struct.unpack_from('<HH', r.mosaicos, 0x20ff * 2), (0x1db, 0x1dc))
        self.assertEqual(r.recolher_mina(0x20ff), 0)
        self.assertEqual(r.recolher_mina(0x3210), 0)
        self.assertEqual(r.indice_mina(0x20ff), 19)

    def test_destruir_mina_preserva_reserva_e_retirar_zero_esgota_reserva_zero(self):
        _, r = estado()
        mina(r, 0, 100, 50)
        r.destruir_mina(0)
        self.assertEqual(r.capacidade_mina(0), 50)
        mina(r, 1, 200, 0)
        self.assertEqual(r.retirar_mina(1, 0), 0)
        self.assertEqual(struct.unpack_from('<HH', r.mosaicos, 400), (0x1db, 0x1dc))

    def test_contadores_de_trabalho_sao_bytes_independentes_com_wrap(self):
        m, r = estado()
        mina(r, 0, 0xff, 25)
        m.terreno.quantidades[0xff:0x101] = bytes([255, 0])
        r.iniciar_trabalho_mina(0x100)
        self.assertEqual(m.terreno.quantidades[0xff:0x101], bytes([0, 1]))
        r.encerrar_trabalho_mina(0xff)
        self.assertEqual(m.terreno.quantidades[0xff:0x101], bytes([255, 0]))
        r.encerrar_trabalho_mina(0x1ff)
        self.assertEqual(m.terreno.quantidades[0xff:0x101], bytes([254, 255]))
        self.assertEqual(r.capacidade_mina(0), 25)
        self.assertEqual(m.economia.memoria, bytes(128))

    def test_sacola_zero_ambiguo_e_tipo_sem_validacao(self):
        m, r = estado()
        m.terreno.tipos[40], m.terreno.quantidades[40] = 0x42, 1
        self.assertEqual(r.retirar_sacola(40), 0)
        self.assertEqual((m.terreno.tipos[40], m.terreno.quantidades[40]), (0, 0))
        self.assertEqual(r.retirar_sacola(40), 0)
        m.terreno.tipos[40], m.terreno.quantidades[40] = 0, 2
        self.assertEqual(r.retirar_sacola(40), 190)
        self.assertEqual(m.terreno.quantidades[40], 1)
        m.terreno.tipos[40], m.terreno.quantidades[40] = 255, 0
        r.retirar_sacola(40)
        self.assertEqual(m.terreno.tipos[40], 0)

    def test_coleta_e_intervalos_dos_estagios(self):
        m, r = estado()
        for tipo, esperado in ((0x1c, 0x1c), (0x1d, 0), (0x28, 0), (0x32, 0),
                                (0x33, 0x29), (0x34, 0x2a), (0x35, 0x35)):
            m.terreno.tipos[1], m.terreno.quantidades[1] = tipo, 37
            r.recolher_campo(1)
            self.assertEqual(m.terreno.tipos[1], esperado)
            self.assertEqual(m.terreno.quantidades[1], 37)
        for tipo in (0x28, 0x34):
            m.terreno.tipos[1] = tipo
            self.assertTrue(r.e_campo(1))
            self.assertFalse(r.pode_crescer(1))

    def test_nascimento_so_sorteia_em_sucesso_e_usa_bit_zero(self):
        m, r = estado()
        r.atributos[10] = 2  # Outros bits não impedem a criação.
        m.terreno.quantidades[10] = 99
        self.assertTrue(r.nova_planta(10))
        self.assertEqual((m.terreno.semente, m.terreno.tipos[10]), (16807, 0x29))
        self.assertFalse(r.nova_planta(10))
        r.atributos[11] = 1
        self.assertFalse(r.nova_planta(11))
        self.assertEqual(m.terreno.semente, 16807)
        self.assertEqual(m.terreno.quantidades[10], 99)

    def test_propagacao_prioridade_e_borda_linear(self):
        m, r = estado()
        for c in (65535, 1, 65280, 256):
            mosaico(r, c)
        r.propagar_planta(0)
        self.assertEqual(m.terreno.tipos[65535], 0x29)
        r.propagar_planta(0)
        self.assertEqual(m.terreno.tipos[1], 0x29)
        self.assertEqual(sum(t != 0 for t in m.terreno.tipos), 2)

    def test_agendamento_flag_persistente_e_divisao_zero(self):
        _, r = estado(tempo=12, periodo=3, atualizar=9)
        r.agendar_campos()
        self.assertEqual(r.atualizar, 1)
        r.tempo = 13
        r.agendar_campos()
        self.assertEqual(r.atualizar, 1)
        r.periodo = 0
        with self.assertRaises(ZeroDivisionError):
            r.agendar_campos()
        self.assertEqual(r.atualizar, 1)

    def test_inatividade_continuidade_e_fim_da_passagem(self):
        m, r = estado(linha=1)
        r.atualizar_campos()
        self.assertEqual(r.linha, 1)
        r.linha = 2
        r.atualizar_campos()
        self.assertEqual(r.linha, 3)
        r.linha, r.atualizar = 255, 73
        r.atualizar_campos()
        self.assertEqual((r.linha, r.atualizar, m.terreno.semente), (1, 0, 1))

    def test_atualizacao_preserva_colunas_extremas(self):
        m, r = estado(linha=17, atualizar=1)
        m.terreno.tipos[17 * 256:18 * 256] = bytes([0x1d] * 256)
        r.atualizar_campos()
        self.assertEqual(m.terreno.tipos[17 * 256], 0x1d)
        self.assertEqual(m.terreno.tipos[18 * 256 - 1], 0x1d)
        self.assertGreater(m.terreno.tipos.count(0x1e), 0)
        self.assertEqual(r.linha, 18)

    def test_guardas_da_api_para_dados_fora_do_dominio(self):
        with self.assertRaises(ValueError):
            RecursosTerreno(minas=bytes(79))
        _, r = estado()
        for indice in (20, 65535):
            with self.assertRaises(ValueError):
                r.capacidade_mina(indice)
        mina(r, 0, 65535, 1)
        with self.assertRaises(ValueError):
            r.retirar_mina(0, 1)
        self.assertEqual(r.capacidade_mina(0), 1)
        r.linha = 256
        with self.assertRaises(ValueError):
            r.atualizar_campos()


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialExtracao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_extracao import BancadaExtracao
        cls.b = BancadaExtracao()

    def setUp(self):
        self.rng = random.Random(0x4755a7)

    def carregar(self, m, r):
        self.b.carregar_extracao(m, r)
        self.guardas = self.b.guardas_extracao()

    def conferir(self, m, r):
        esperado = dict(economia=bytes(m.economia.memoria), capacidades=bytes(m.capacidades.memoria),
                        estruturas=bytes(m.estruturas), tipos=bytes(m.terreno.tipos),
                        quantidades=bytes(m.terreno.quantidades), semente=m.terreno.semente)
        esperado.update({k: bytes(getattr(r, k)) for k in ('minas', 'mosaicos', 'atributos')})
        esperado.update({k: getattr(r, k) for k in ('linha', 'periodo', 'tempo', 'atualizar')})
        atual = self.b.estado()
        atual.update(self.b.estado_extracao())
        for campo, valor in atual.items():
            if valor != esperado[campo]:
                if isinstance(valor, bytes):
                    c = next(i for i, (a, b) in enumerate(zip(valor, esperado[campo])) if a != b)
                    self.fail(f'{campo}, offset {c:#x}: x86={valor[c]:#x}, Python={esperado[campo][c]:#x}')
                self.assertEqual(valor, esperado[campo], campo)
        self.assertEqual(self.b.guardas_extracao(), self.guardas)
        self.assertEqual(self.b.guardas(), (b'\xa6' * 16, b'\x6a' * 16))
        self.assertEqual(self.b.outras_guardas(), (b'\xc7' * 8, b'\x7c' * 8, b'\xe9' * 8, b'\x9e' * 8, 0x12345678))

    def chamar(self, m, r, entrada, metodo, *args, mascara=None):
        self.carregar(m, r)
        esperado = getattr(r, metodo)(*args)
        regs = {n: self.rng.getrandbits(32) for n in ('EBX', 'ECX', 'ESI', 'EDI', 'EBP')}
        resultado = self.b.chamar(entrada, args[0] if args else 0, args[1] if len(args) > 1 else 0, regs)
        if mascara is not None:
            self.assertEqual(resultado['EAX'] & mascara, esperado, metodo)
        self.conferir(m, r)
        for nome, valor in regs.items():
            self.assertEqual(resultado[nome], valor, nome)

    def test_busca_capacidade_limites_e_duplicatas_128_tabelas(self):
        for n in range(128):
            m, r = estado()
            for i in range(20):
                mina(r, i, self.rng.choice((0, 0xff, 0xfffe, 0xffff, self.rng.randrange(65536))), self.rng.randrange(65536))
            i = n % 20
            origem = struct.unpack_from('<H', r.minas, i * 4)[0]
            for celula in (origem, origem + 1, origem + 256, origem + 257, 0, 65535):
                self.chamar(m, r, 0x47544c, 'indice_mina', celula | 0xa7310000, mascara=65535)
            self.chamar(m, r, 0x475541, 'capacidade_mina', i | 0xfe210000, mascara=65535)

    def test_retirada_coleta_destruicao_128_estados(self):
        for n in range(128):
            m, r = estado()
            i, c = n % 20, self.rng.randrange(65535)
            reserva = self.rng.choice((0, 1, 2, 255, 65535, self.rng.randrange(65536)))
            mina(r, i, c, reserva)
            pedido = self.rng.choice((0, 1, reserva, 65535, self.rng.randrange(65536)))
            self.chamar(m, r, 0x47554f, 'retirar_mina', i | 0xffff0000, pedido | 0xcdae0000, mascara=65535)
            self.chamar(m, r, 0x4755a7, 'recolher_mina', c | 0xa1410000, mascara=65535)
            self.chamar(m, r, 0x475515, 'destruir_mina', i | 0xaaaa0000)

    def test_trabalho_128_estados_incluindo_mina_ausente(self):
        for n in range(128):
            m, r = estado()
            c = self.rng.randrange(1, 65535)
            mina(r, n % 20, c, n)
            m.terreno.quantidades[c:c + 2] = self.rng.randbytes(2)
            destino = c if n % 3 else (c + 2) & 65535
            self.chamar(m, r, 0x4754a7, 'iniciar_trabalho_mina', destino | 0xc0010000)
            self.chamar(m, r, 0x4754de, 'encerrar_trabalho_mina', destino | 0xdeaf0000)

    def test_sacolas_todos_os_tipos_com_quantidades_zero_um_e_255(self):
        for tipo in range(256):
            for quantidade in (0, 1, 255):
                m, r = estado()
                c = (tipo * 257 + quantidade) & 65535
                m.terreno.tipos[c], m.terreno.quantidades[c] = tipo, quantidade
                self.chamar(m, r, 0x476662, 'retirar_sacola', c | 0xface0000, mascara=255)

    def test_campo_consultas_e_coleta_todos_os_256_tipos(self):
        for tipo in range(256):
            m, r = estado()
            m.terreno.tipos[65535], m.terreno.quantidades[65535] = tipo, 91
            self.chamar(m, r, 0x478247, 'e_campo', 0xffffffff, mascara=255)
            self.chamar(m, r, 0x47826c, 'pode_crescer', 0xffffffff, mascara=255)
            self.chamar(m, r, 0x4781e8, 'recolher_campo', 0xffffffff)

    def test_nascimento_256_flags_e_sementes(self):
        for flag in range(256):
            m, r = estado()
            c = self.rng.randrange(65536)
            r.atributos[c] = flag
            m.terreno.tipos[c] = 0 if flag % 3 else 0x42
            m.terreno.quantidades[c] = 255
            m.terreno.semente = self.rng.choice((0, 1, 0x7fffffff, self.rng.randrange(0x80000000)))
            self.chamar(m, r, 0x4782b4, 'nova_planta', c | 0xabcd0000, mascara=255)

    def test_propagacao_256_estados_incluindo_bordas_e_prioridades(self):
        for n in range(256):
            m, r = estado()
            c = (0, 255, 256, 65535, 65280, self.rng.randrange(65536))[n % 6]
            m.terreno.semente = self.rng.randrange(0x80000000)
            for delta in (-1, 1, -256, 256):
                v = (c + delta) & 65535
                mosaico(r, v, self.rng.choice((0, 0x83, 0x84, 0x86, 0x87, 0x9c, 0x9d, 0xdc, 0xdd)))
                r.atributos[v] = self.rng.choice((0, 0, 1, 2, 255))
                m.terreno.tipos[v] = self.rng.choice((0, 0, 0x1d, 0x28, 0x34, 0x42, 0xff))
            self.chamar(m, r, 0x478319, 'propagar_planta', c | 0xabcd0000)

    def test_agendamento_128_ticks_e_oito_excecoes(self):
        from emulador import unicorn, x86
        from bancada_extracao import BancadaExtracao
        for n in range(128):
            periodo = self.rng.choice((1, 2, 65535, self.rng.randrange(1, 65536)))
            tempo = periodo * n if n % 2 else self.rng.getrandbits(32)
            m, r = estado(tempo=tempo, periodo=periodo, atualizar=n)
            self.chamar(m, r, 0x475328, 'agendar_campos')
        for n in range(8):
            # Unicorn conserva estado de exceção; cada DIV inválido usa CPU nova,
            # como nas bancadas anteriores, sem alterar os bytes da referência.
            anterior = self.b
            type(self).b = BancadaExtracao()
            for campo in ('execucoes', 'excecoes_esperadas', 'limites_esperados'):
                setattr(self.b, campo, getattr(anterior, campo))
            m, r = estado(tempo=n, periodo=0, atualizar=n)
            self.carregar(m, r)
            with self.assertRaises(ZeroDivisionError):
                r.agendar_campos()
            with self.assertRaises(unicorn.UcError) as erro:
                self.b.chamar(0x475328)
            self.assertEqual(erro.exception.errno, unicorn.UC_ERR_EXCEPTION)
            self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_EIP), 0x47533a)
            self.b.excecoes_esperadas += 1
            self.conferir(m, r)

    def test_atualizacao_64_linhas_aleatorias_e_bytes_de_pilha(self):
        for n in range(64):
            m, r = estado(linha=(0, 1, 2, 254, 255, self.rng.randrange(256))[n % 6], atualizar=n % 4)
            m.terreno.semente = self.rng.randrange(0x80000000)
            for y in {(r.linha - 1) & 255, r.linha, (r.linha + 1) & 255}:
                for x in range(256):
                    c = y * 256 + x
                    mosaico(r, c, self.rng.choice((0x84, 0x86, 0x9d, 0xdc, 0)))
                    r.atributos[c] = self.rng.choice((0, 0, 0, 1, 2))
                    m.terreno.tipos[c] = self.rng.choice((0, 0, 0x1c, *range(0x1d, 0x35), 0x42, 255))
                    m.terreno.quantidades[c] = self.rng.randrange(256)
            self.b.sujeira_pilha = n * 3
            try:
                self.chamar(m, r, 0x478806, 'atualizar_campos')
            finally:
                self.b.sujeira_pilha = None

    def test_passagem_completa_de_255_linhas_em_memoria_persistente(self):
        m, r = estado(atualizar=1)
        r.mosaicos[:] = struct.pack('<H', 0x84) * 65536
        for c in range(0, 65536, 7):
            m.terreno.tipos[c] = (0x1c, 0x1d, 0x27, 0x28, 0x29, 0x33, 0x34)[(c // 7) % 7]
        self.carregar(m, r)
        for _ in range(255):
            r.atualizar_campos()
            self.b.chamar(0x478806)
            self.conferir(m, r)
        self.assertEqual((r.linha, r.atualizar), (1, 0))

    def test_corpus_dos_38_mapas_minas_e_campos(self):
        arquivos = sorted((PASTA.parents[2] / 'source/cd/WORLD').glob('*.ETA'))
        self.assertEqual(len(arquivos), 38)
        for n, arquivo in enumerate(arquivos):
            m, r, total = fixture_eta(arquivo)
            for i in range(total):
                c = struct.unpack_from('<H', r.minas, i * 4)[0]
                self.chamar(m, r, 0x475541, 'capacidade_mina', i, mascara=65535)
                self.chamar(m, r, 0x47544c, 'indice_mina', c, mascara=65535)
                self.chamar(m, r, 0x4755a7, 'recolher_mina', c, mascara=65535)
            # Linha com mais campos do mapa: fixture real, instante sintético.
            r.linha = max(range(1, 256), key=lambda y: sum(0x1c <= t <= 0x34 for t in m.terreno.tipos[y*256:(y+1)*256]))
            r.atualizar = 1
            m.terreno.semente = n + 1
            self.chamar(m, r, 0x478806, 'atualizar_campos')

    def test_integracao_extracao_sacola_e_credito_sem_transporte_simulado(self):
        m, r = estado()
        mina(r, 0, 0x2020, 2)
        m.estruturas[8] = 3
        m.capacidades.configurar(0, 1, 100)
        self.carregar(m, r)
        q = r.recolher_mina(0x2121)
        self.assertEqual(self.b.chamar(0x4755a7, 0x2121)['EAX'] & 65535, q)
        self.conferir(m, r)
        m.terreno.depositar(0x4040, 2, q)
        self.b.depositar(0x4040, 2, q)
        self.conferir(m, r)
        recurso = r.retirar_sacola(0x4040)
        self.assertEqual(self.b.chamar(0x476662, 0x4040)['EAX'] & 255, recurso)
        self.conferir(m, r)
        m.adicionar(0, recurso, 1, 0)
        self.b.adicionar(0, recurso, 1, 0)
        self.conferir(m, r)
        self.assertEqual(m.economia.consultar(0).pedra, 1)
