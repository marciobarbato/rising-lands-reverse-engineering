"""Cenários de estruturas e bloqueadores, compartilhados com o diferencial x86."""
import struct
import sys
import unittest
import json
import subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ferramentas'))
from desbloqueio_unidades import afastar_bloqueadores, procurar_celula_livre
from estruturas_caminhos import CoresEstruturas
from test_emulacao_navegacao import preparar


def inserir_bloqueador(m, tipo=0, dono=0, celula=0x506, indice=1, estado=7, modo=0):
    u = bytearray(276)
    u[0], u[1], u[2], u[0x72], u[0xab] = dono, tipo, estado, 1, modo
    for off in (8, 0x7c, 0x7e):
        struct.pack_into('<H', u, off, celula)
    for off in (0xb8, 0xc0):
        struct.pack_into('<H', u, off, 0xffff)
    m.escrever_unidade(indice, u)
    m.ocupar(indice, celula, True)


def inserir_estrutura(m, celulas, indice=0, dono=0, tipo=9, cor=255):
    """Fixture de RAM: não substitui BatimentCollision/BatimentOccupeCase."""
    p = indice * 276
    m.estruturas[p + 4], m.estruturas[p + 8] = dono, tipo
    for sub, c in enumerate(celulas):
        struct.pack_into('<H', m.estruturas, p + 0xcc + sub * 2, m.regioes[c])
        m.regioes[c] = 0x8000 | indice << 5 | sub
        m.cores_estruturas.grade[c] = cor
        m.atributos[c] |= 1


class EstruturasDesbloqueio(unittest.TestCase):
    def test_insercao_preserva_regiao_e_recusa_sobrepor_ocupante(self):
        m = preparar(); m.refazer_regioes()
        antiga = m.regioes[0x506]
        self.assertTrue(m.modificar_regiao_estrutura(999,31,0x506,True))
        self.assertFalse(m.modificar_regiao_estrutura(998,0,0x506,True))
        self.assertFalse(m.modificar_regiao_estrutura(998,0,0x506,False))
        self.assertTrue(m.modificar_regiao_estrutura(999,31,0x506,False))
        self.assertEqual(m.regioes[0x506],antiga)
        self.assertEqual(m.cores_estruturas.grade[0x506],0)

    def test_demonstracoes_reproduzem_relatorio_com_imports_x86_bloqueados(self):
        raiz = Path(__file__).resolve().parents[1]
        codigo = '''
import json,sys
sys.path.insert(0,'ferramentas')
for nome in ('emulador','unicorn','solucionador_original','solucionador_misto'):
    sys.modules[nome] = None
from demonstrar_estruturas import executar_integracao
print(json.dumps([executar_integracao(n) for n in ('muros','aliados_bloqueadores')]))
'''
        r = subprocess.run([sys.executable,'-c',codigo],cwd=raiz,text=True,capture_output=True,check=True)
        esperado = json.loads((raiz/'relatorios/estruturas-desbloqueio-python.json').read_text())
        self.assertEqual(json.loads(r.stdout),esperado['cenarios'])

    def test_remapeamento_com_estrutura_recusa_antes_de_alterar_dados(self):
        m = preparar(); inserir_estrutura(m,[0x506])
        regioes = m.regioes[:]
        with self.assertRaises(NotImplementedError): m.refazer_regioes()
        self.assertEqual(m.regioes,regioes)

    def test_geometria_distingue_retangulo_e_colisao(self):
        from pegadas_estruturas import celulas_estrutura, estrutura_ocupa_celula
        m = preparar()
        struct.pack_into('<H',m.estruturas,2,0x505)
        m.estruturas[8] = 0
        self.assertEqual(celulas_estrutura(m,0), tuple(0x505+y*256+x for y in (3,2,1,0) for x in range(3)))
        self.assertTrue(estrutura_ocupa_celula(m,0,0x505))
        self.assertFalse(estrutura_ocupa_celula(m,0,0x507))

    def test_muros_unem_e_separam_componentes(self):
        c = CoresEstruturas(16,16)
        c.adicionar_muro(0x505); c.adicionar_muro(0x507)
        self.assertNotEqual(c.grade[0x505],c.grade[0x507])
        c.adicionar_muro(0x506)
        self.assertEqual(c.grade[0x505],c.grade[0x507])
        c.retirar_muro(0x506)
        self.assertEqual(c.grade[0x506],0)
        self.assertNotEqual(c.grade[0x505],c.grade[0x507])

    def test_pilha_de_cores_esgotamento_reuso_e_liberacao_repetida(self):
        cores = CoresEstruturas(16, 16)
        self.assertEqual([cores.alocar() for _ in range(256)], list(range(255, 0, -1)) + [0])
        cores.liberar(42); cores.liberar(42); cores.liberar(0)
        self.assertEqual((cores.alocar(), cores.alocar()), (42, 0))

    def test_cor_preenche_quatro_vizinhos_e_nao_atravessa_diagonal(self):
        cores = CoresEstruturas(16, 16)
        for c in (0x505, 0x506, 0x607): cores.grade[c] = 4
        cores.preencher(0x505, 7)
        self.assertEqual([cores.grade[c] for c in (0x505, 0x506, 0x607)], [7, 7, 4])
        with self.assertRaises(ValueError): cores.preencher(0x505, 7)

    def test_ordem_sai_da_frente_e_limpa_referencias(self):
        m = preparar(); inserir_bloqueador(m)
        self.assertEqual(afastar_bloqueadores(m, 0), dict(desbloqueou=True))
        self.assertEqual(m.palavra(1, 0x7e), 0x405)
        self.assertEqual(m.unidades[276 + 2], 2)
        self.assertEqual((m.unidades[0x88], m.unidades[0x8b]), (1, 0))

    def test_retorno_verdadeiro_mesmo_sem_celula_livre(self):
        m = preparar(); inserir_bloqueador(m)
        m.atributos[:] = bytes([1]) * 65536
        self.assertEqual(procurar_celula_livre(m, 0x506, 1), 0xffff)
        self.assertTrue(afastar_bloqueadores(m, 0)['desbloqueou'])
        self.assertEqual(m.palavra(1, 0x7e), 0x506)

    def test_alianca_nao_substitui_dono_identico(self):
        m = preparar(); inserir_bloqueador(m, dono=1)
        m.mascaras_alianca[0] = m.mascaras_alianca[1] = 31
        self.assertFalse(afastar_bloqueadores(m, 0)['desbloqueou'])

    def test_candidatos_mesma_cor_registram_primeira_estrutura_inimiga(self):
        from candidatos_rota import iniciar_candidatos
        from otimizacao_caminhos import ContextoLinha
        m = preparar(); m.refazer_regioes()
        inserir_estrutura(m, [0x504], indice=7, dono=0, cor=12)
        inserir_estrutura(m, [0x404], indice=8, dono=1, cor=12)
        r = iniciar_candidatos(ContextoLinha.da_unidade(m, 0), 0x505, 0x50a)
        self.assertEqual(r.regioes, (0x800c,))
        self.assertEqual(struct.unpack_from('<H', r.registro_ocupantes, 2)[0], 8)
        self.assertEqual((r.registro_ocupantes[5], r.registro_ocupantes[7]), (1, 1))

    def test_busca_estrutura_preserva_unidades(self):
        from solucionador_python import SolucionadorCaminhosPython
        m = preparar(); m.refazer_regioes()
        inserir_estrutura(m, [0x506, 0x606], indice=999, dono=1, cor=3)
        antes = bytes(m.unidades)
        r = SolucionadorCaminhosPython().iniciar(m, 0)
        self.assertTrue(r['contexto']['sucesso'])
        self.assertGreater(struct.unpack_from('<H', r['buffer_rota'])[0], 0)
        self.assertEqual(bytes(m.unidades), antes)
