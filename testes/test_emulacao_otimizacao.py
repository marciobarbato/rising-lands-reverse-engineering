"""Comparação com as rotinas originais, incluindo resíduos fora da contagem ativa."""
import os
import random
import struct
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ferramentas'))
from otimizacao_caminhos import ContextoLinha, otimizar_rota, testar_linha
from test_emulacao_navegacao import preparar


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialOtimizacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_otimizacao import BancadaOtimizacao
        cls.bancada = BancadaOtimizacao()

    def setUp(self):
        self.bancadas_auxiliares = []

    def _linha(self, contexto, origem, destino):
        self.bancada.carregar_contexto(contexto)
        inicial = bytes(range(256)) * 2
        r = testar_linha(contexto, origem, destino)
        esperado = bytearray(inicial)
        for i, c in enumerate(r.celulas): struct.pack_into('<H', esperado, i * 2, c)
        atual = self.bancada.linha(origem, destino, inicial)
        self.assertEqual(atual, (r.permitido, r.contador if r.contador is not None else 0xa5a5a5a5, bytes(esperado)),
                         (contexto.classe, contexto.mascara, origem, destino))
        self.assertEqual(self.bancada.cpu.mem_read(0x4e1771, 1)[0], contexto.mundo.permitir_aliados_parados)

    def test_linha_26_tipos_direcoes_blocos_e_mesma_celula(self):
        for tipo in range(26):
            for destino in (0x502, 0x202, 0x205, 0x208, 0x508, 0x808, 0x805, 0x802, 0x505):
                for bloqueio in (None, 0x506, 0x505):
                    m = preparar(tipo)
                    m.permitir_aliados_parados = 1
                    if bloqueio is not None: m.atributos[bloqueio] |= 3
                    self._linha(ContextoLinha.da_unidade(m, 0), 0x505, destino)

    def test_objeto_fd_mascaras_bordas_e_limite_255(self):
        for tipo in (0, 3, 11, 16, 17):
            for objeto in (0, 0xfd):
                for mascara in (1, 2, 3):
                    m = preparar(tipo)
                    m.objetos[0x506] = objeto
                    m.atributos[0x506] = 0
                    c = ContextoLinha(m, 0, ContextoLinha.da_unidade(m, 0).classe, mascara, 0)
                    self._linha(c, 0x505, 0x508)
            for a, b in ((0, 0x005), (0x001, 0x101), (0x005, 0x005), (0xf0f, 0x1010)):
                m = preparar(tipo)
                m.atributos[0xffff] = 3
                self._linha(ContextoLinha.da_unidade(m, 0), a, b)
        m = preparar(largura=256, altura=256)
        self._linha(ContextoLinha.da_unidade(m, 0), 0, 0xfffe)

    def test_ocupantes_aliancas_direcoes_e_excecoes(self):
        for tipo in (0, 3, 12, 15, 17):
            for outro_tipo in (0, 3, 7, 16):
                for dono, direcao, movendo in ((0,9,True), (1,9,True), (1,1,True), (1,9,False)):
                    m = preparar(tipo)
                    u = bytearray(276)
                    u[0], u[1], u[2], u[0x72], u[0x90] = dono, outro_tipo, 2, 1, direcao
                    for off, valor in ((8,0x506), (0x7c,0x506), (0x7e,0x508 if movendo else 0x506)):
                        struct.pack_into('<H', u, off, valor)
                    m.escrever_unidade(1,u)
                    m.ocupar(1,0x506,True)
                    m.mascaras_alianca[0] = 2
                    self._linha(ContextoLinha.da_unidade(m, 0), 0x505, 0x508)

    def _otimizar(self, m, celulas):
        c = ContextoLinha.da_unidade(m, 0)
        self.bancada.carregar_contexto(c)
        b = bytearray(range(256)) * 2
        struct.pack_into('<H', b, 0, len(celulas))
        for i, celula in enumerate(celulas, 1): struct.pack_into('<H', b, i * 2, celula)
        self.assertEqual(self.bancada.otimizar(b), otimizar_rota(c, b), celulas)
        self.assertEqual(self.bancada.cpu.mem_read(0x4e1771, 1)[0], m.permitir_aliados_parados)

    def test_otimizacao_lacos_cauda_e_rotas_deterministicas(self):
        for celulas in ([], [0x505], [0x505,0x506], [0x505,0x506,0x607,0x606,0x605],
                        [0x505,0x606,0x707,0x708,0x709,0x609,0x509,0x508]):
            for tipo in (0,3,11,17): self._otimizar(preparar(tipo), celulas)
        sorteio = random.Random(0x42e890)
        for caso in range(100):
            m = preparar(caso % 26)
            celulas, x, y = [0x505], 5, 5
            for _ in range(sorteio.randrange(2, 100)):
                dx, dy = sorteio.choice(((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1)))
                x, y = max(2,min(13,x+dx)), max(2,min(13,y+dy))
                celulas.append(x+256*y)
            for _ in range(10): m.atributos[sorteio.randrange(2,14)+256*sorteio.randrange(2,14)] |= 3
            self._otimizar(m, celulas)

    def test_backend_misto_trajetos_mensagens_e_novo_obstaculo(self):
        from demonstrar_desvios import preparar_cenario
        from solucionador_misto import SolucionadorComOtimizacaoPython
        for nome, dinamico in (('obstaculo', False), ('parede_com_passagem', False),
                               ('sem_passagem', False), ('destino_bloqueado', False),
                               ('parede_com_passagem', True)):
            m, maquina, bloqueios, _ = preparar_cenario(nome, SolucionadorComOtimizacaoPython())
            self.bancadas_auxiliares.append(m.solucionador.bancada)
            self.bancada.carregar(maquina.programa)
            self.bancada.carregar_navegacao(m)
            self.assertEqual(maquina.postar(0, 1, (0, 0x40a)), self.bancada.postar(0, 1, (0, 0x40a)))
            self.assertEqual(maquina.atualizar(0), self.bancada.atualizar(0))
            inserido, eventos = False, []
            for ciclo in range(1, 1201):
                if dinamico and not inserido and m.palavra(0, 8) == 0x605:
                    m.atributos[0x705] |= 1
                    self.bancada.cpu.mem_write(self.bancada.grades['atributos'] + 0x705, bytes([m.atributos[0x705]]))
                    bloqueios.append((5, 7))
                    inserido = True
                self.bancada.pulso_navegacao(0)
                evento = m.atualizar_movimento(0, maquina)
                if evento: eventos.append(evento)
                self.assertEqual(self.bancada.conferir_fisica(m), [], (nome, dinamico, ciclo))
                self.assertEqual(self.bancada.memoria_tarefas(), bytes(maquina.memoria))
                pos = m.palavra(0, 8)
                self.assertNotIn((pos & 255, pos >> 8), bloqueios)
                if m.unidades[2] == 7: break
            else: self.fail('Trajeto misto não terminou')
            self.assertEqual(m.palavra(0, 8) == 0x40a, nome not in ('sem_passagem', 'destino_bloqueado'))
            self.assertEqual(len(eventos), 1)
            self.assertEqual(maquina.atualizar(0), self.bancada.atualizar(0))
            self.assertEqual(self.bancada.memoria_tarefas(), bytes(maquina.memoria))
            self.assertEqual(maquina.ativas, 0)
            otimizacoes = m.solucionador.bancada.otimizacoes_python
            self.assertEqual(len(otimizacoes) > 0, nome == 'parede_com_passagem')
            if dinamico:
                self.assertTrue(inserido)
                self.assertGreaterEqual(len(otimizacoes), 2)
