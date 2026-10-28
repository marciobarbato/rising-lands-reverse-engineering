"""Contratos observáveis de aplicação e limpeza de edifícios no terreno."""
import hashlib
import json
import struct
import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from navegacao_unidades import MundoNavegacao
from pegadas_estruturas import TAMANHOS_E_MASCARAS


def mundo_estrutura(tipo=0, indice=7, origem=0x505, largura=32, altura=24):
    m = MundoNavegacao(largura, altura)
    m.regioes[:] = [1] * 65536
    m.tiles[:] = [77] * 65536
    m.objetos[:] = bytes([19]) * 65536
    m.atributos[:] = bytes([0x82]) * 65536
    p = indice * 276
    m.estruturas[p:p+276] = bytes((i*13+7)&255 for i in range(276))
    struct.pack_into('<H', m.estruturas, p+2, origem)
    m.estruturas[p+8] = tipo
    return m


class TerrenoEstruturas(unittest.TestCase):
    def test_demonstracoes_sem_imports_de_emulacao_reproduzem_relatorio(self):
        codigo='''
import json,sys
sys.path.insert(0,'ferramentas')
for nome in ('unicorn','emulador','solucionador_original','solucionador_misto'):
    sys.modules[nome]=None
from demonstrar_terreno_estruturas import executar_terreno_cenario
print(json.dumps([executar_terreno_cenario(n) for n in ('edificio','edificio_retirado','parede')]))
'''
        p=subprocess.run([sys.executable,'-B','-c',codigo],cwd=RAIZ,text=True,capture_output=True,check=True)
        esperado=json.loads((RAIZ/'relatorios/terreno-estruturas-python.json').read_text())
        self.assertEqual(json.loads(p.stdout),esperado['cenarios'])

    def test_aplicacao_usa_slots_compactos_e_limpa_objetos_do_retangulo(self):
        m = mundo_estrutura()
        antes = bytes(m.estruturas)
        m.aplicar_terreno_estrutura(7,0x505,600)
        for sub, c in enumerate((0x505,0x506,0x605,0x606)):
            self.assertEqual(m.regioes[c],0x8000 | 7 << 5 | sub)
            self.assertEqual(m.atributos[c],0x83)
            self.assertEqual(struct.unpack_from('<H',m.estruturas,7*276+0xcc+sub*2)[0],1)
        for linha in range(4):
            for coluna in range(3):
                c=0x505+linha*256+coluna
                self.assertEqual(m.tiles[c],600+linha*3+coluna)
                self.assertEqual(m.objetos[c],0)
        self.assertEqual(m.atributos[0x507],0x82)
        self.assertEqual(m.regioes[0x507],1)
        self.assertEqual(m.estruturas[:7*276+0xcc],antes[:7*276+0xcc])

    def test_colisao_e_regiao_sao_liberadas_por_operacoes_diferentes(self):
        m=mundo_estrutura(); m.aplicar_terreno_estrutura(7,0x505,600)
        m.resetar_terreno_estrutura(7,1)
        self.assertEqual(m.atributos[0x505],0x82)
        self.assertTrue(m.regioes[0x505]&0x8000)
        self.assertEqual(m.tiles[0x505],600)
        m.remover_regioes_estrutura(7)
        self.assertEqual(m.regioes[0x505],1)
        self.assertEqual(m.cores_estruturas.grade[0x505],0)
        self.assertEqual(m.objetos[0x505],0)

    def test_reposicao_do_piso_conserva_contador_horizontal_entre_linhas(self):
        m=mundo_estrutura(); m.aplicar_terreno_estrutura(7,0x505,600)
        regioes=m.regioes[:]; atributos=bytes(m.atributos)
        m.resetar_terreno_estrutura(7,0)
        self.assertEqual(m.tiles[0x505],0x15d+5+5*8)
        self.assertEqual(m.tiles[0x605],0x15d+0+6*8)
        self.assertEqual(m.regioes,regioes)
        self.assertEqual(bytes(m.atributos),atributos)

    def test_sobreposicao_recusada_ainda_consume_o_slot(self):
        m=mundo_estrutura()
        m.regioes[0x505]=0x4000
        m.aplicar_terreno_estrutura(7,0x505,600)
        self.assertEqual(m.regioes[0x505],0x4000)
        self.assertEqual(m.regioes[0x506],0x8000 | 7 << 5 | 1)
        self.assertEqual(m.atributos[0x505],0x83)
        m.remover_regioes_estrutura(7)
        self.assertEqual(m.regioes[0x505],0x4000)
        self.assertEqual(m.regioes[0x506],1)

    def test_origem_recebida_nao_altera_a_origem_no_registro(self):
        m=mundo_estrutura(origem=0x808)
        m.aplicar_terreno_estrutura(7,0x505,65534)
        self.assertEqual(struct.unpack_from('<H',m.estruturas,7*276+2)[0],0x808)
        self.assertEqual((m.tiles[0x505],m.tiles[0x506],m.tiles[0x507]),(65534,65535,0))

    def test_tipo20_exige_mascara_em_ram_antes_de_qualquer_efeito(self):
        m=mundo_estrutura(tipo=20)
        antes=(bytes(m.estruturas),m.tiles[:],bytes(m.atributos),m.regioes[:],bytes(m.objetos))
        with self.assertRaises(NotImplementedError):m.aplicar_terreno_estrutura(7,0x505,600)
        with self.assertRaises(ValueError):m.aplicar_terreno_estrutura(7,0x505,600,bytes(19))
        self.assertEqual(antes,(bytes(m.estruturas),m.tiles[:],bytes(m.atributos),m.regioes[:],bytes(m.objetos)))
        m.aplicar_terreno_estrutura(7,0x505,600,bytes(20))
        self.assertFalse(any(v&0x8000 for v in m.regioes))
        self.assertEqual(m.tiles[0x505],600)
        self.assertEqual(m.objetos[0x505],0)

    def test_wrap_de_celula_conservado_sem_recorte_pela_largura_do_mapa(self):
        m=mundo_estrutura(origem=0xfffe)
        m.aplicar_terreno_estrutura(7,0xfffe,600)
        self.assertEqual((m.tiles[0xfffe],m.tiles[0xffff],m.tiles[0]),(600,601,602))

    def test_mascaras_estaticas_conferem_com_a_tabela_usada_pelo_aplicador(self):
        manifesto=json.loads((RAIZ/'evidencias/terreno-estruturas/manifesto.json').read_text())
        for t in manifesto['tabelas']:
            w,h,mascara=TAMANHOS_E_MASCARAS[t['tipo']]
            self.assertEqual((w,h),(t['largura'],t['altura']))
            if t['tipo']==20:
                self.assertIsNone(t['mascara'])
                self.assertEqual(t['ponteiro_mascara'],'0x004dfb9c')
            else:self.assertEqual(list(map(int,mascara)),t['mascara'])

    def test_bytes_das_evidencias_conferem_com_o_executavel(self):
        exe=RAIZ.parent/'source/cd/INSTALHD/RISING.EXE'
        if not exe.exists():self.skipTest('CD original ausente')
        dados=exe.read_bytes()
        manifesto=json.loads((RAIZ/'evidencias/terreno-estruturas/manifesto.json').read_text())
        self.assertEqual(hashlib.sha256(dados).hexdigest(),manifesto['sha256_original'])
        for t in manifesto['trechos']:
            inicio=int(t['inicio'],16);offset=inicio-0x401000+0x400
            self.assertEqual(hashlib.sha256(dados[offset:offset+t['tamanho']]).hexdigest(),t['sha256'])
