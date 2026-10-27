"""Consultas e desvios locais comparados com as rotinas x86 originais."""
import os
import struct
import sys
import unittest
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from navegacao_unidades import MundoNavegacao
from passagem_unidades import consultar_passagem
from movimento import PARAMETROS_TIPOS


def preparar(tipo=7, origem=0x505, destino=0x50a, largura=16, altura=16):
    m = MundoNavegacao(largura, altura)
    u = bytearray(276)
    u[1], u[2], u[0x90], u[0x91] = tipo, 2, 9, 9
    u[0x98], u[0x93], u[0xa5], u[0xa7] = PARAMETROS_TIPOS[tipo]
    u[0xab] = 50 if tipo in (16, 17) else 0
    for off, val in ((8, origem), (0x7c, origem), (0x7e, destino), (0xb8, 0xffff), (0xc0, 0xffff)):
        struct.pack_into('<H', u, off, val)
    struct.pack_into('<I', u, 0x10c, 0xffffffff)
    m.escrever_unidade(0, u)
    m.ocupar(0, origem, True)
    return m


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialNavegacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from solucionador_original import BancadaNavegacao
        cls.bancada = BancadaNavegacao()

    def setUp(self):
        self.bancadas_auxiliares = []

    def test_passagem_tipos_mascaras_pegadas_e_bordas(self):
        for tipo in range(26):
            for celula, atributo in ((0x506, 0), (0x506, 1), (0x606, 3), (0x500, 3), (0x005, 1)):
                for mascara in (1, 2):
                    m = preparar(tipo)
                    for c in m._pegada(tipo, celula): m.atributos[c] |= atributo
                    self.bancada.carregar_navegacao(m)
                    esperado = consultar_passagem(m, 0, celula, mascara)
                    self.assertEqual(self.bancada.consultar(0, celula, mascara), esperado, (tipo, celula, mascara))

    def test_ocupantes_dono_modo_e_flag_72(self):
        for tipo in (0, 3, 12, 15, 16, 17):
            for dono, outro_tipo, modo, habilitado in ((0, 0, 0, 1), (1, 0, 0, 1), (1, 16, 50, 1), (1, 0, 0, 0), (1, 13, 0, 1)):
                m = preparar(tipo)
                u = bytearray(276)
                u[0], u[1], u[2], u[0x72], u[0xab] = dono, outro_tipo, 7, habilitado, modo
                for off in (8, 0x7c): struct.pack_into('<H', u, off, 0x506)
                m.escrever_unidade(1, u)
                m.ocupar(1, 0x506, True)
                self.bancada.carregar_navegacao(m)
                mascara = 1 + int(m.unidades[0xab] != 0)
                self.assertEqual(self.bancada.consultar(0, 0x506, mascara), consultar_passagem(m, 0, 0x506), (tipo, dono, outro_tipo, modo, habilitado))

    def test_desvio_local_todas_direcoes_e_tipos(self):
        from movimento import celula_vizinha
        for tipo in range(26):
            for direcao in range(1, 17, 2):
                destino = celula_vizinha(0x505, direcao, 16, 16)
                # Destino a duas células; permite testar desvio sem cancelamento imediato.
                destino = celula_vizinha(destino, direcao, 16, 16)
                for bloquear in (False, True):
                    m = preparar(tipo, destino=destino)
                    if bloquear:
                        c = celula_vizinha(0x505, direcao, 16, 16)
                        for pos in m._pegada(tipo, c): m.atributos[pos] |= 3
                    self.bancada.carregar_navegacao(m)
                    m.escolher_direto(0)
                    self.bancada.direto(0)
                    self.assertEqual(self.bancada.conferir_fisica(m), [], (tipo, direcao, bloquear))

    def test_cancelamento_destino_adjacente_e_entrada_em_busca(self):
        for destino, bloqueios in ((0x506, [0x506]), (0x50a, [0x506, 0x406]), (0x505, [])):
            m = preparar(destino=destino)
            for c in bloqueios: m.atributos[c] = 1
            m.busca.unidade, m.busca.ocupada, m.busca.sucesso, m.busca.ponteiro_rota = 0, 1, 1, 123
            self.bancada.carregar_navegacao(m)
            m.escolher_direto(0)
            self.bancada.direto(0)
            self.assertEqual(self.bancada.conferir_fisica(m), [], destino)

    def test_obstaculo_natural_tiles_e_objetos(self):
        from regioes_mapa import obstaculo_natural
        m=preparar()
        self.bancada.carregar_navegacao(m)
        for tile in (0,1,701,702,65535):
            for objeto in (0,1,11,12,255):
                for marcador in (0,1,255):
                    m.tiles[0]=tile;m.objetos[0]=objeto
                    if tile<702:m.marcadores_obstaculos_tiles[tile]=marcador
                    self.bancada.cpu.mem_write(self.bancada.grades['tiles'],struct.pack('<H',tile))
                    self.bancada.cpu.mem_write(0x1300000,bytes([objeto]))
                    self.bancada.cpu.mem_write(self.bancada.grades['sombra']+0x200,bytes(m.marcadores_obstaculos_tiles))
                    r=self.bancada.executar(0x4752b8,[(0x4752b8,0x475302)])
                    self.assertEqual(bool(r['EAX']&255),obstaculo_natural(tile,objeto,m.marcadores_obstaculos_tiles))

    def test_preenchimento_quatro_ou_oito_vizinhos_no_trecho_original(self):
        from regioes_mapa import preencher_componente
        for classe in (0,1):
            classes=bytearray([1-classe])*65536
            for c in (0x505,0x606,0x707,0x708):classes[c]=classe
            esperado=[0]*65536
            preencher_componente(classes,esperado,0x505,7)
            atual=self.bancada.componente(classes,0x505,7)
            self.assertEqual(atual,esperado,classe)
            self.assertEqual(atual[0x606],7 if classe==0 else 0)

    def test_estados_pedido_resultado_e_sem_passagem(self):
        from solucionador_original import SolucionadorOriginal
        for fechado in (False,True):
            m=preparar(origem=0x405,destino=0x40a)
            for y in range(256):
                for x in range(256):
                    if x>=16 or y>=16:m.atributos[y*256+x]=1;m.objetos[y*256+x]=1
            for y in range(16 if fechado else 11):m.atributos[y*256+6]=1;m.objetos[y*256+6]=1
            m.refazer_regioes()
            m.unidades[0x88]=3
            m.solucionador=SolucionadorOriginal()
            self.bancadas_auxiliares.append(m.solucionador.bancada)
            self.bancada.carregar_navegacao(m)
            for _ in range(2):
                m.atualizar_estado_caminho(0)
                self.bancada.executar(0x44930c,self.bancada.intervalos,dict(EAX=0),limite_instrucoes=1000000)
                self.assertEqual(self.bancada.conferir_fisica(m),[],fechado)
            self.assertEqual(m.unidades[0x88],0 if fechado else 5)
            if fechado:self.assertEqual(m.palavra(0,0x7e),0x405)

    def test_rota_invalida_pelo_obstaculo_e_fim_da_rota(self):
        from caminhos import serializar_rota
        for buffer,bloqueado in ((serializar_rota([0x506]),True),(serializar_rota([]),False)):
            m=preparar();m.rotas[0][:len(buffer)]=buffer;m.unidades[0x88]=5
            if bloqueado:m.atributos[0x506]=1
            self.bancada.carregar_navegacao(m)
            m.escolher_da_rota(0)
            self.bancada.escolher_proximo(0)
            self.assertEqual(self.bancada.conferir_fisica(m),[])

    def test_trajetos_integrados_com_despacho_original_e_mensagem(self):
        for nome in ('obstaculo','parede_com_passagem','sem_passagem','destino_bloqueado'):
            self._comparar_trajeto(nome)

    def test_obstaculo_novo_invalida_rota_durante_o_trajeto(self):
        self._comparar_trajeto('parede_com_passagem', obstaculo_novo=True)

    def _comparar_trajeto(self, nome, obstaculo_novo=False):
        from demonstrar_desvios import preparar_cenario
        from solucionador_original import SolucionadorOriginal
        m,maquina,bloqueios,_=preparar_cenario(nome,SolucionadorOriginal())
        self.bancadas_auxiliares.append(m.solucionador.bancada)
        self.bancada.carregar(maquina.programa)
        self.bancada.carregar_navegacao(m)
        self.assertEqual(maquina.postar(0,1,(0,0x40a)),self.bancada.postar(0,1,(0,0x40a)))
        self.assertEqual(maquina.atualizar(0),self.bancada.atualizar(0))
        eventos=[]
        inserido=False
        for ciclo in range(1,1201):
            if obstaculo_novo and not inserido and m.palavra(0,8)==0x605:
                # Colisão temporária: altera atributos, preserva o rótulo natural.
                self.assertEqual(m.palavra(0,0x7c),0x605)
                self.assertEqual(m.unidades[0x88],5)
                m.atributos[0x705] |= 1
                self.bancada.cpu.mem_write(self.bancada.grades['atributos']+0x705,bytes([m.atributos[0x705]]))
                bloqueios.append((5,7))
                inserido=True
            self.bancada.pulso_navegacao(0)
            evento=m.atualizar_movimento(0,maquina)
            if evento:eventos.append(evento)
            self.assertEqual(self.bancada.conferir_fisica(m),[],(nome,ciclo,obstaculo_novo))
            self.assertEqual(self.bancada.memoria_tarefas(),bytes(maquina.memoria))
            pos=m.palavra(0,8)
            self.assertNotIn((pos&255,pos>>8),bloqueios)
            if m.unidades[2]==7:break
        else:self.fail('Trajeto não terminou: '+nome)
        self.assertEqual(m.palavra(0,8)==0x40a,nome not in ('sem_passagem','destino_bloqueado'))
        self.assertEqual(len(eventos),1)
        self.assertEqual(maquina.atualizar(0),self.bancada.atualizar(0))
        self.assertEqual(self.bancada.memoria_tarefas(),bytes(maquina.memoria))
        self.assertEqual(maquina.ativas,0)
        if obstaculo_novo:
            self.assertTrue(inserido)
            self.assertGreaterEqual(len(m.historico_navegacao),2)
