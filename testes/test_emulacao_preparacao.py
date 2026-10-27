"""Preparação e início dos candidatos comparados com o EXE original."""
import os
import random
import struct
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ferramentas'))
from candidatos_rota import iniciar_candidatos, selecionar_candidato
from otimizacao_caminhos import ContextoLinha
from preparacao_destino import preparar_destino
from test_emulacao_navegacao import preparar


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialPreparacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_preparacao import BancadaPreparacao
        cls.bancada = BancadaPreparacao()

    def setUp(self):
        self.bancadas_auxiliares = []

    def _preparacao(self, m, inicio, destino, mascara=None, flags=(0, 0)):
        from bancada_preparacao import gravar_preparacao
        # Extremos anteriores e cauda não zerada permitem detectar escritas indevidas.
        m.rotas[0][:] = bytes(range(256)) * 2
        self.bancada.carregar_navegacao(m)
        self.bancada.cpu.mem_write(0x4e0f44, struct.pack('<HH', 0x2323, 0x3434))
        antes = self.bancada.memoria_preparacao()
        r = self.bancada.preparar_original(m, 0, inicio, destino, mascara, flags)
        esperado = self.bancada.memoria_preparacao()
        self.bancada.carregar_navegacao(m)
        self.bancada.cpu.mem_write(0x4e0f34, antes[0])
        self.bancada.cpu.mem_write(0x496302, antes[1])
        p = preparar_destino(m, 0, inicio, destino, mascara, *flags)
        gravar_preparacao(self.bancada, p, self.bancada.grades['rotas'])
        self.assertEqual(self.bancada.memoria_preparacao(), esperado, (m.unidades[1], inicio, destino, mascara))
        self.assertEqual(p.retorno, bool(r['EAX'] & 255))
        return p

    def test_preparacao_26_tipos_destinos_bloqueados_e_bordas(self):
        for tipo in range(26):
            for destino, bloco in ((0x50a,False), (0x50a,True), (0x505,False), (0x505,True),
                                    (0,True), (0xf0f,True), (0x1010,False)):
                m = preparar(tipo)
                if bloco:
                    for c in m._pegada(tipo, destino): m.atributos[c] |= 3
                self._preparacao(m, 0x505, destino)

    def test_regioes_preservadas_e_flags(self):
        for regiao in (0, 1, 33):
            m = preparar()
            m.regioes[0x50a] = regiao
            self._preparacao(m, 0x505, 0x50a, flags=(7, 255))
        for regiao in (0, 33):
            m = preparar()
            m.regioes[0x50a] = 0x8000 | (2 << 5) | 3
            struct.pack_into('<H', m.estruturas, 2 * 276 + 0xcc + 6, regiao)
            self._preparacao(m, 0x505, 0x50a)
        m = preparar(largura=256, altura=256)
        p = self._preparacao(m, 0x505, 0xffff)
        self.assertEqual(p.status, 6)

    def test_aneis_mapas_retangulares_e_mascaras(self):
        rng = random.Random(0x43b30b)
        for i in range(100):
            largura, altura = rng.choice(((8,16), (16,8), (16,16), (32,16)))
            m = preparar(i % 26, largura=largura, altura=altura)
            destino = rng.randrange(largura) + 256 * rng.randrange(altura)
            for _ in range(50): m.atributos[rng.randrange(largura) + 256 * rng.randrange(altura)] = 3
            m.atributos[destino] = 3
            self._preparacao(m, 0x505, destino, mascara=1 + i % 2)

    def _inicio(self, m):
        from bancada_preparacao import gravar_inicio_candidatos
        inicio, destino = m.palavra(0, 8), m.palavra(0, 0x7e)
        # Início do cálculo exige preparação não concluída.
        self.bancada.preparar_original(m, 0, inicio, destino)
        self.bancada.cpu.mem_write(0x496302, b'\0')
        self.bancada.cpu.mem_write(0x4e0f37, b'\0')
        self.bancada.cpu.mem_write(0x4e0f44, struct.pack('<HH', inicio, destino))
        # A tradução começa no mesmo estado anterior; não reutiliza os valores
        # já produzidos pelo original para ocultar uma escrita ausente.
        self.bancada.cpu.mem_write(0x4e0f50, bytes([0xa5]) * 538)
        self.bancada.cpu.mem_write(0x4e116a, b'\xa5\xa5')
        self.bancada.cpu.mem_write(0x4e136a, b'\xa5\xa5')
        antes = bytes(self.bancada.cpu.mem_read(0x4e0f50, 538))
        r = self.bancada.inicio_original()
        self.assertEqual(r['EIP'], 0x430b7e)
        esperado = self.bancada.memoria_inicio(r['ESP'])
        dados = iniciar_candidatos(ContextoLinha.da_unidade(m, 0), inicio, destino)
        self.bancada.cpu.mem_write(0x4e0f50, antes)
        self.bancada.cpu.mem_write(0x4e1772, b'\xa5\xa5')
        self.bancada.cpu.mem_write(0x4e0f40, b'\xa5')
        self.bancada.cpu.mem_write(0x4e116a, b'\xa5\xa5')
        self.bancada.cpu.mem_write(0x4e136a, b'\xa5\xa5')
        for off, tamanho in ((0xec,4),(0x108,4),(0xd4,2),(0x4c,2),(0x3c4,1),(0x2e0,1)):
            self.bancada.cpu.mem_write(r['ESP'] + off, bytes([0xa5]) * tamanho)
        gravar_inicio_candidatos(self.bancada, dados, r['ESP'])
        self.assertEqual(self.bancada.memoria_inicio(r['ESP']), esperado, (m.unidades[1], inicio, destino))

    def test_inicio_candidatos_tipos_direcoes_obstaculos_naturais(self):
        for tipo in range(26):
            for destino in (0x502,0x202,0x205,0x208,0x508,0x808,0x805,0x802):
                m = preparar(tipo, destino=destino)
                for y in range(2,9):
                    m.atributos[0x06 + y * 256] = 3
                    m.regioes[0x06 + y * 256] = 7
                self._inicio(m)

    def test_inicio_ocupantes_aliancas_e_pegadas(self):
        for tipo in (0,3,11,16):
            for outro_tipo in (0,3,7,12):
                for dono in (0,1):
                    m = preparar(tipo)
                    u = bytearray(276)
                    u[0],u[1],u[2],u[0x72],u[0x90] = dono,outro_tipo,7,1,9
                    for off in (8,0x7c,0x7e): struct.pack_into('<H',u,off,0x506)
                    m.escrever_unidade(1,u); m.ocupar(1,0x506,True)
                    m.mascaras_alianca[0] = 2
                    self._inicio(m)

    def test_selecao_custos_desempates_flags_e_contadores_inconsistentes(self):
        rng = random.Random(0x43b073)
        for i in range(400):
            buffers = [bytearray(range(256)) * 2 for _ in range(2)]
            for b in buffers: struct.pack_into('<H', b, 0, rng.choice((0, 1, 17, 254, 255)))
            if i % 2 == 0:
                for b in buffers: struct.pack_into('<H', b, 0, 255)
            custos = (rng.choice((0, 1, 50, 255, 65535)), rng.choice((0, 1, 50, 255, 65535)))
            registros = [bytes(rng.randrange(256) if j in (4,5,6,7,8,9) else 0 for j in range(10)) for _ in range(2)]
            flags = (rng.choice((0, 1)), rng.choice((0, 1)))
            semente = rng.choice((0, 1, 2, 127773, 0x7fffffff, 0xffffffff))
            esperado = self.bancada.escolher_original(buffers, custos, registros, semente, status=2, flags=flags)
            r = selecionar_candidato(buffers, custos, registros, semente, status=2, flags=flags)
            self.assertEqual(dict(escolhido=r.escolhido, buffers=r.buffers, status=r.status, semente=r.semente), esperado, i)

    def test_busca_parcial_python_26_tipos_nos_tres_mapas(self):
        from demonstrar_desvios import preparar_cenario
        from solucionador_misto import BancadaMista
        misto = BancadaMista()
        self.bancadas_auxiliares.append(misto)
        for tipo in range(26):
            for nome in ('parede_com_passagem', 'sem_passagem', 'destino_bloqueado'):
                m, _, _, _ = preparar_cenario(nome)
                m.ocupar(0, m.palavra(0, 8), False)
                m.unidades[1], m.unidades[2] = tipo, 2
                m.unidades[0xab] = 50 if tipo in (16,17) else 0
                m.palavra(0, 0x7e, 0x40a)
                m.ocupar(0, m.palavra(0, 8), True)
                esperado = self.bancada.preparar_busca(m, 0)
                atual = misto.preparar_busca(m, 0)
                self.assertEqual(atual, esperado, (tipo, nome))
        m = preparar()
        m.regioes[:] = [1] * 65536
        m.palavra(0, 0xfa, 1)
        for dx,dy in ((-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1)):
            c = 0x505 + dx + dy * 256
            m.atributos[c],m.regioes[c] = 1,2
        esperado = self.bancada.preparar_busca(m, 0)
        atual = misto.preparar_busca(m, 0)
        self.assertEqual(atual, esperado)
        self.assertEqual(atual['status'], 8)
