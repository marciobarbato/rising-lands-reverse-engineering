"""Os dois buffers de contorno, custos e regiões confrontados com o original."""
import os
import random
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ferramentas'))
from candidatos_rota import iniciar_candidatos
from caminhos import CLASSES_OCUPACAO
from contornos_caminhos import construir_contornos
from demonstrar_desvios import preparar_cenario
from otimizacao_caminhos import ContextoLinha
from preparacao_destino import preparar_destino


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialContornos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_contornos import BancadaContornos
        cls.bancada = BancadaContornos()

    @staticmethod
    def _tipo(m, tipo):
        m.ocupar(0, m.palavra(0,8), False)
        m.unidades[1] = tipo
        m.unidades[0xab] = 50 if tipo in (16,17) else 0
        m.ocupar(0, m.palavra(0,8), True)

    def _comparar(self, m, inicio=0x402, destino=0x40a):
        p = preparar_destino(m, 0, inicio, destino)
        self.assertFalse(p.concluida)
        esperado, buffers, residuos, registros = self.bancada.contornar_original(m, 0, inicio, destino)
        contexto = ContextoLinha.da_unidade(m, 0)
        dados = iniciar_candidatos(contexto, inicio, p.destino)
        atual = construir_contornos(contexto, dados, buffers, residuos, registros)
        for campo, valor in esperado.items():
            self.assertEqual(getattr(atual, campo), valor, (campo, inicio, destino, m.unidades[1], atual.passos))
        return atual

    def test_classe_1_parede_e_obstaculo_simples(self):
        for tipo in (i for i, classe in enumerate(CLASSES_OCUPACAO) if classe == 1):
            for nome in ('parede_com_passagem', 'obstaculo'):
                m, _, _, _ = preparar_cenario(nome)
                self._tipo(m,tipo)
                self._comparar(m)

    def test_obstaculos_naturais_deterministicos(self):
        rng = random.Random(0x430b7e)
        for i in range(104):
            m, _, _, _ = preparar_cenario('obstaculo')
            self._tipo(m, i % 26)
            for _ in range(30):
                c = rng.randrange(3, 14) + 256 * rng.randrange(1, 15)
                if c not in (0x402, 0x40a): m.atributos[c], m.objetos[c] = 1, 1
            m.refazer_regioes()
            self._comparar(m)

    def test_outros_ocupantes_e_flags_de_passagem(self):
        import struct
        for mover in (0,3,11,16,24,25):
            for tipo in (0,3):
                for dono in (0,1):
                    for celula in (0x403,0x503,0x303,0x401):
                        m, _, _, _ = preparar_cenario('obstaculo')
                        self._tipo(m,mover)
                        u = bytearray(276)
                        u[0],u[1],u[2],u[0x72],u[0x90] = dono,tipo,7,1,9
                        for off in (8,0x7c,0x7e): struct.pack_into('<H',u,off,celula)
                        m.escrever_unidade(1,u); m.ocupar(1,celula,True)
                        self._comparar(m)

    def test_pegadas_de_quatro_celulas_parede_e_obstaculo(self):
        for tipo in (i for i, classe in enumerate(CLASSES_OCUPACAO) if classe != 1):
            for nome in ('parede_com_passagem', 'obstaculo'):
                m, _, _, _ = preparar_cenario(nome)
                self._tipo(m,tipo)
                self._comparar(m)

    def test_solucionador_independente_todos_tipos_tres_mapas(self):
        import struct
        from solucionador_python import SolucionadorCaminhosPython
        ids = [self.bancada.grades['rotas'] + i * 512 for i in range(800)]
        solver = SolucionadorCaminhosPython(ids)
        for tipo in range(26):
            for nome in ('parede_com_passagem','sem_passagem','destino_bloqueado'):
                m, _, _, _ = preparar_cenario(nome)
                self._tipo(m,tipo)
                m.palavra(0,0x7e,0x40a)
                self.bancada.cpu.mem_write(0x4e0f44,struct.pack('<HH',solver.inicio_calculado,solver.destino_calculado))
                for a,b in zip((0x4e116a,0x4e136a),solver.buffers):self.bancada.cpu.mem_write(a,b)
                self.bancada.cpu.mem_write(0x4e0f6a,solver.regioes)
                self.bancada.cpu.mem_write(0x4e0f54,b''.join(solver.registros))
                esperado=self.bancada.preparar_busca(m,0)
                atual=solver.iniciar(m,0)
                self.assertEqual(atual,esperado,(tipo,nome))

    def test_sem_vizinhos_e_dois_contornos_sem_saida(self):
        m, _, _, _ = preparar_cenario('obstaculo')
        for dx,dy in ((-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1)):
            c=0x402+dx+dy*256
            m.atributos[c],m.regioes[c]=1,2
        self.assertEqual(self._comparar(m).status_falha,8)
        m, _, _, _ = preparar_cenario('sem_passagem')
        m.ocupar(0,0x402,False)
        m.palavra(0,8,0x405)
        m.palavra(0,0x7c,0x405)
        m.ocupar(0,0x405,True)
        # Rótulos iguais forçam a construção; o teste de região normal já
        # recusaria esta parede fechada antes de percorrê-la.
        m.regioes[0x40a]=m.palavra(0,0xfa)
        self.assertEqual(self._comparar(m,inicio=0x405).status_falha,6)
