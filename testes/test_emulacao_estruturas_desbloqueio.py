"""Grades, candidatos, contornos e ordens confrontados com o x86 original."""
import os
import random
import struct
import unittest
from test_estruturas_desbloqueio import inserir_bloqueador, inserir_estrutura, preparar
from desbloqueio_unidades import afastar_bloqueadores, procurar_celula_livre
from estruturas_caminhos import CoresEstruturas


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Emulação opcional: RISING_EMULAR=1')
class DiferencialEstruturasDesbloqueio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_contornos import BancadaContornos
        cls.bancada = BancadaContornos()

    def test_dimensoes_mascaras_listas_e_consulta_22_tipos(self):
        from pegadas_estruturas import tamanho_estrutura, colisao_estrutura, celulas_estrutura, estrutura_ocupa_celula
        from extrair_pegadas_estruturas import extrair
        b = self.bancada
        intervalos = b.intervalos + [(0x41a996,0x41aa54),(0x41ab5c,0x41ac8b),(0x41aff8,0x41b0b2)]
        saida = 0x1800000
        for t in extrair()['tipos']:
            tipo = t['tipo']; largura,altura = tamanho_estrutura(tipo)
            self.assertEqual((largura,altura),(t['largura'],t['altura']))
            b.executar(0x41a996,intervalos,dict(EAX=saida,EDX=saida+2,EBX=tipo))
            self.assertEqual(bytes(b.cpu.mem_read(saida,4)),struct.pack('<HH',largura,altura))
            for sub, mascara in enumerate(t['mascara']):
                r = b.executar(0x41ab5c,intervalos,dict(EAX=tipo,EDX=sub))
                self.assertEqual(bool(r['EAX']&255),colisao_estrutura(tipo,sub))
                self.assertEqual(colisao_estrutura(tipo,sub),bool(mascara))
            for origem in (0x505,0xfffe):
                m = preparar(); m.estruturas[8] = tipo
                struct.pack_into('<H',m.estruturas,2,origem)
                b.carregar_navegacao(m)
                b.executar(0x41a9c3,intervalos,dict(EAX=0,EDX=saida+2,EBX=saida))
                celulas = celulas_estrutura(m,0)
                self.assertEqual(bytes(b.cpu.mem_read(saida,2+len(celulas)*2)),struct.pack('<'+'H'*(1+len(celulas)),len(celulas),*celulas))
                for celula in celulas+(0x404,):
                    r = b.executar(0x41aff8,intervalos,dict(EAX=0,EDX=celula))
                    self.assertEqual(bool(r['EAX']&255),estrutura_ocupa_celula(m,0,celula),(tipo,origem,celula))

    def test_adicao_remocao_muros_componentes_e_allocator(self):
        b = self.bancada; m = preparar(); c = m.cores_estruturas
        rng = random.Random(0x43e616)
        acoes = [('adicionar',0x505),('adicionar',0x507),('adicionar',0x506),('retirar',0x506)]
        acoes += [(rng.choice(('adicionar','retirar')),rng.randrange(16)+256*rng.randrange(16)) for _ in range(180)]
        for acao, celula in acoes:
            if acao == 'adicionar' and c.grade[celula]: continue
            b.carregar_navegacao(m)
            b.executar(0x43e616 if acao == 'adicionar' else 0x43e8b7,b.intervalos,dict(EAX=celula),limite_instrucoes=1000000)
            (c.adicionar_muro if acao == 'adicionar' else c.retirar_muro)(celula)
            self.assertEqual(bytes(b.cpu.mem_read(b.grades['cores_estruturas'],65536)),bytes(c.grade))
            self.assertEqual(bytes(b.cpu.mem_read(0x4e1570,512)),bytes(c.livres+c.liberadas))
            self.assertEqual(bytes(b.cpu.mem_read(0x4e0732,2048)),struct.pack('<1024H',*c.pilha))

    def test_modificar_regiao_estrutura_insercao_remocao_e_sobreposicao(self):
        b = self.bancada; m = preparar(); m.refazer_regioes()
        rng = random.Random(0x43e138)
        acoes = [(True,0,0,0x506),(True,1,0,0x507),(True,999,31,0x508),
                 (True,998,0,0x508),(False,998,0,0x508),(False,999,31,0x508)]
        acoes += [(bool(rng.randrange(2)),rng.randrange(4),rng.randrange(32),rng.randrange(4,10)+256*rng.randrange(4,10)) for _ in range(100)]
        for inserir,indice,sub,celula in acoes:
            b.carregar_navegacao(m)
            ponteiro = 0x49a0c8+indice*276+0xcc+sub*2
            r = b.executar(0x43e138,b.intervalos,dict(EAX=celula,EDX=indice,EBX=3 if inserir else 1,ECX=ponteiro),
                           pilha={4:struct.pack('<I',sub)},limite_instrucoes=1000000)
            self.assertEqual(bool(r['EAX']&255),m.modificar_regiao_estrutura(indice,sub,celula,inserir))
            self.assertEqual(b.conferir_fisica(m),[])
            c = m.cores_estruturas
            self.assertEqual(bytes(b.cpu.mem_read(b.grades['cores_estruturas'],65536)),bytes(c.grade))
            self.assertEqual(bytes(b.cpu.mem_read(0x4e1570,512)),bytes(c.livres+c.liberadas))
            self.assertEqual(bytes(b.cpu.mem_read(0x4e0732,2048)),struct.pack('<1024H',*c.pilha))

    def test_alocacao_liberacao_cores_e_memoria_completa(self):
        m = preparar(); b = self.bancada
        b.carregar_navegacao(m)
        rng = random.Random(0x43e5a0)
        for i in range(700):
            if i < 260 or rng.randrange(2):
                r = b.executar(0x43e5a0, b.intervalos)
                self.assertEqual(r['EAX'] & 255, m.cores_estruturas.alocar())
            else:
                cor = rng.randrange(256)
                b.executar(0x43e5d5, b.intervalos, dict(EAX=cor))
                m.cores_estruturas.liberar(cor)
            self.assertEqual(bytes(b.cpu.mem_read(0x4e1570, 256)), bytes(m.cores_estruturas.livres))
            self.assertEqual(bytes(b.cpu.mem_read(0x4e1670, 256)), bytes(m.cores_estruturas.liberadas))

    def test_preenchimento_grade_pilha_bordas_e_limite(self):
        rng = random.Random(0x43e464); b = self.bancada
        for largura, altura, inicio in ((1,1,0),(16,16,0),(16,16,0xf0f),(256,256,0x505),(256,256,0xffff)):
            m = preparar(largura=largura, altura=altura)
            c = m.cores_estruturas
            if largura == 16:
                c.grade[:] = bytes(rng.randrange(2) for _ in range(65536))
            c.pilha[:] = [rng.randrange(65536) for _ in range(1024)]
            for cor in (0, 7):
                b.carregar_navegacao(m)
                b.executar(0x43e464, b.intervalos, dict(EAX=inicio, EDX=cor), limite_instrucoes=1000000)
                c.preencher(inicio, cor)
                self.assertEqual(bytes(b.cpu.mem_read(b.grades['cores_estruturas'],65536)), bytes(c.grade))
                self.assertEqual(bytes(b.cpu.mem_read(0x4e0732,2048)), struct.pack('<1024H', *c.pilha))

    def test_celula_livre_tipos_modos_bordas_e_bloqueios(self):
        rng = random.Random(0x44330c); b = self.bancada
        for tipo in range(26):
            for centro in (0, 0x100, 0xf0f, 0x505, 0xffff):
                m = preparar(tipo)
                for y in range(16):
                    for x in range(16):
                        m.atributos[x + y * 256] |= rng.randrange(4)
                b.carregar_navegacao(m)
                r = b.executar(0x44330c, b.intervalos, dict(EAX=centro, EDX=0), limite_instrucoes=1000000)
                self.assertEqual(r['EAX'] & 65535, procurar_celula_livre(m, centro, 0), (tipo,centro))
                self.assertEqual(b.conferir_fisica(m), [])

    def _comparar_desbloqueio(self, m):
        b = self.bancada; b.carregar_navegacao(m)
        r = b.afastar(0)
        atual = afastar_bloqueadores(m, 0)
        self.assertEqual(bool(r['EAX'] & 255), atual['desbloqueou'])
        self.assertEqual(b.conferir_fisica(m), [])
        self.assertEqual(bytes(b.cpu.mem_read(0x4e1a34, 4)), struct.pack('<HH',m.ultimo_bloqueador,m.ultima_celula_livre))

    def test_ordens_tipos_donos_aliancas_e_sem_espaco(self):
        for tipo in range(26):
            for dono, bloqueado in ((0,False),(1,False),(0,True)):
                m = preparar(); inserir_bloqueador(m,tipo,dono,modo=50 if tipo in (16,17) else 0)
                m.mascaras_alianca[:] = bytes([31])*5
                if bloqueado: m.atributos[:] = bytes([3])*65536
                self._comparar_desbloqueio(m)

    def test_ordens_varios_ocupantes_reservas_inativos_e_referencias(self):
        for celula in (0x506,0x406,0x606):
            for estado in (0,4,7,14):
                for habilitado, movendo in ((0,False),(1,False),(1,True)):
                    m = preparar(); inserir_bloqueador(m,13,celula=celula,estado=estado)
                    m.unidades[276+0x72] = habilitado
                    if movendo: m.palavra(1,0x7e,0x50a)
                    m.palavra(1,0xc0,5)
                    m.estruturas[5*276+0x74:5*276+0x77] = bytes([1,1,15])
                    m.busca.unidade,m.busca.ocupada,m.busca.sucesso,m.busca.ponteiro_rota = 1,1,1,123
                    m.ultimo_bloqueador,m.ultima_celula_livre = 123,456
                    self._comparar_desbloqueio(m)

    def _comparar_contorno(self, m, inicio=0x505, destino=0x50a):
        from candidatos_rota import iniciar_candidatos
        from contornos_caminhos import construir_contornos
        from preparacao_destino import preparar_destino
        from otimizacao_caminhos import ContextoLinha
        p = preparar_destino(m,0,inicio,destino)
        self.assertFalse(p.concluida)
        esperado, buffers, residuos, registros = self.bancada.contornar_original(m,0,inicio,destino)
        c = ContextoLinha.da_unidade(m,0)
        atual = construir_contornos(c,iniciar_candidatos(c,inicio,p.destino),buffers,residuos,registros)
        for campo, valor in esperado.items(): self.assertEqual(getattr(atual,campo),valor,campo)

    def test_contornos_estruturas_todas_classes_donos_tipos_e_cores(self):
        for tipo in range(26):
            for dono, estrutura_tipo in ((0,9),(1,9),(1,8)):
                m = preparar(tipo); m.refazer_regioes()
                inserir_estrutura(m,[0x506,0x606,0x706],indice=999,dono=dono,tipo=estrutura_tipo,cor=7)
                inserir_estrutura(m,[0x403,0x404],indice=8,dono=1,cor=7)
                inserir_estrutura(m,[0x808,0x809],indice=9,dono=0,cor=8)
                self._comparar_contorno(m)

    def test_busca_completa_com_estruturas_e_obstaculos_naturais(self):
        from solucionador_python import SolucionadorCaminhosPython
        b = self.bancada
        solver = SolucionadorCaminhosPython([b.grades['rotas']+i*512 for i in range(800)])
        rng = random.Random(0x8000)
        for tipo in range(26):
            for i in range(3):
                m = preparar(tipo); m.refazer_regioes()
                for j in range(10):
                    x,y = rng.randrange(6,14),rng.randrange(1,15)
                    inserir_estrutura(m,[x+y*256],indice=j,dono=j%2,tipo=9 if j%3 else 8,cor=j%3+1)
                inserir_estrutura(m,[0x506],indice=999,dono=1,cor=1)
                b.cpu.mem_write(0x4e0f44,struct.pack('<HH',solver.inicio_calculado,solver.destino_calculado))
                for a,buf in zip((0x4e116a,0x4e136a),solver.buffers): b.cpu.mem_write(a,buf)
                b.cpu.mem_write(0x4e0f6a,solver.regioes)
                b.cpu.mem_write(0x4e0f54,b''.join(solver.registros))
                esperado = b.preparar_busca(m,0)
                self.assertEqual(solver.iniciar(m,0),esperado,(tipo,i))

    def test_movimento_integrado_muros_e_ordens_a_dois_bloqueadores(self):
        from demonstrar_estruturas import preparar_integracao
        b = self.bancada
        for nome in ('muros','aliados_bloqueadores'):
            m,maquina,bloqueios,indices = preparar_integracao(nome)
            m.solucionador.identificadores_rotas = tuple(b.grades['rotas']+i*512 for i in range(800))
            b.carregar(maquina.programa); b.carregar_navegacao(m)
            self.assertEqual(maquina.postar(0,1,(0,0x40a)),b.postar(0,1,(0,0x40a)))
            self.assertEqual(maquina.atualizar(0),b.atualizar(0))
            ordens = set()
            for ciclo in range(1200):
                for i in indices:
                    antes = [m.palavra(j,0x7e) for j in indices]
                    b.pulso_navegacao(i)
                    m.atualizar_movimento(i,maquina)
                    for j,destino in zip(indices,antes):
                        if j and m.palavra(j,0x7e) != destino: ordens.add(j)
                    self.assertEqual(b.conferir_fisica(m),[],(nome,ciclo,i))
                    self.assertEqual(b.memoria_tarefas(),bytes(maquina.memoria))
                    self.assertNotIn((m.palavra(i,8)&255,m.palavra(i,8)>>8),bloqueios)
                if all(m.unidades[i*276+2] == 7 for i in indices): break
            else: self.fail('Movimento integrado não terminou: '+nome)
            self.assertEqual(maquina.atualizar(0),b.atualizar(0))
            self.assertEqual(maquina.ativas,0)
            if nome == 'muros': self.assertEqual(m.palavra(0,8),0x40a)
            else:
                self.assertEqual(ordens,{1,2})
                self.assertNotEqual(m.palavra(1,8),0x403)
                self.assertNotEqual(m.palavra(2,8),0x303)
