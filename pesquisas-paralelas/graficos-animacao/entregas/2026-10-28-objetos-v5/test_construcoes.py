"""Regressões stdlib contra capturas originais preservadas; não executa x86."""
import hashlib
import json
import unittest
from graficos import Catalogo, RAIZ, Quadro, localizar
from construcoes import *


class ConstrucoesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=Catalogo();cls.r=json.loads((RAIZ/'validacao/x86-construcoes.json').read_text())
        cls.ident=json.loads((RAIZ/'evidencias/identidade-construcoes.json').read_text())

    def test_identidade_e_registro_eta(self):
        i=self.ident['registros'][2]
        self.assertEqual(i['chave_ini'],'SANCTUAIRE');self.assertEqual(i['dimensoes_celulas'],[6,5])
        self.assertEqual(hashlib.sha256(bytes.fromhex(i['bytes_hex'])).hexdigest(),i['sha256'])
        ini=self.c._ler('cd/INSTALHD/RISING.INI').decode('cp1252').split('[SANCTUAIRE]')[1].split('[')[0]
        self.assertIn('NAME=SANTUÁRIO',ini)
        r=ler_estruturas_eta(self.c._ler('cd/WORLD/MONDE01.ETA'))
        self.assertEqual(len(r),1);r=r[0]
        self.assertEqual((r['tipo'],r['modo'],r['jogador'],r['origem_celula'],r['auxiliar_06']),(2,5,0,(12,11),0))
        self.assertEqual(r['sha256'],self.r['registro_ETA']['sha256'])
        self.assertEqual(r['offset_registro'],0x50036)
        self.assertEqual([v['n'] for v in self.r['leituras_ETA']],[2,2,2,204])
        self.assertTrue(self.r['registro_ETA']['habitado_original'])

    def test_terreno_e_mascara_contra_colocacao_original(self):
        self.assertEqual(len(self.r['colocacao']),30);ordinal=0
        for i,r in enumerate(self.r['colocacao']):
            self.assertEqual(r['id_terreno'],732+i)
            occ=self.ident['mascara_santuario'][i]
            self.assertEqual(r['ocupacao'],0x8000+ordinal if occ else 0)
            ordinal+=bool(occ)
        self.assertEqual(ordinal,17)
        gatilho=self.r['colocacao'][17]
        self.assertEqual((gatilho['id_terreno'],gatilho['celula'],gatilho['ocupacao']),(749,0x0d11,0x800f))

    def test_512_associacoes_contra_original(self):
        self.assertEqual(self.r['resultado'],'PASSOU');self.assertEqual(len(self.r['capturas']),512)
        for r in self.r['capturas']:
            p=consultar_santuario(habitado=True,jogador=0,relogios=r['relogios'],celula_mapa=(17,13))
            self.assertEqual(self.eventos(p),r['camadas'])

    @staticmethod
    def eventos(p):
        return [dict(id_motor=q['id_motor'],x=224+q['x'],y=160+q['y'],operacao=q['operacao'],jogador=q['jogador']) for q in p['camadas']]

    def test_fase_por_celula_nao_por_jogador(self):
        self.assertEqual(len(self.r['variacoes_celula_jogador']),160)
        for r in self.r['variacoes_celula_jogador']:
            p=consultar_santuario(habitado=True,jogador=r['jogador'],relogios=r['relogios'],celula_mapa=(r['celula']%256,r['celula']//256))
            self.assertEqual(self.eventos(p),r['camadas'])
        p=consultar_santuario(habitado=True,jogador=4,relogios=(0,0,0),celula_mapa=(17,13))
        self.assertEqual([c['id_motor'] for c in p['camadas']],[7032,7050,7034,7042,7059,7067,7058])

    def test_relogios_e_overflow_original(self):
        self.assertEqual(len(self.r['relogios']),258)
        for r in self.r['relogios']:self.assertEqual(avancar_relogios(r['entrada']),tuple(r['saida']))
        self.assertEqual(avancar_relogios((0xffffffff,0xffffffff,0xffffffff)),(0,0,0))
        for v in [(-1,0,0),(0,False,0),(0,0,0x100000000),(0,0)]:
            with self.assertRaises(ValueError):avancar_relogios(v)

    def test_tabelas_de_jogador_contra_original(self):
        tabs=tabelas_jogador(self.ident['faixas_jogador'])
        self.assertEqual(tabs,tabelas_jogador());self.assertEqual(tabs,tuple(bytes(t) for t in self.r['tabelas_jogador']))
        for t in tabs:
            self.assertEqual(t[:160],bytes(range(160)));self.assertEqual(t[168:],bytes(range(168,256)))
        self.assertEqual(tabs[0],bytes(range(256)))

    def test_244_superficies_contra_original(self):
        self.assertEqual(len(self.r['pixels']),244);fundo=bytes((i*17+23)%256 for i in range(320*320))
        for r in self.r['pixels']:
            plano=consultar_santuario(habitado=True,jogador=r['jogador'],relogios=r['relogios'],celula_mapa=(17,13))
            out=compor_fachada(self.c,fundo,320,320,plano,r['x'],r['y'],tabelas=tabelas_jogador(),recorte=r['recorte'])
            self.assertEqual(hashlib.sha256(out).hexdigest(),r['sha256'])

    def test_precondicoes_originais_e_escopo_explicito(self):
        self.assertEqual(len(self.r['gates']),3)
        for r in self.r['gates']:self.assertEqual(r['camadas'],[])
        kw=dict(habitado=True,jogador=0,relogios=(0,0,0),celula_mapa=(17,13))
        for k,v in [('tipo',3),('modo',4),('habitado',False),('auxiliar_06',1)]:
            with self.assertRaises(NotImplementedError):consultar_santuario(**(kw|{k:v}))
        for k,v in [('jogador',5),('jogador',True),('celula_mapa',(256,0)),('celula_mapa',(-1,0)),('relogios',(0,0,-1))]:
            with self.assertRaises(ValueError):consultar_santuario(**(kw|{k:v}))
        with self.assertRaises(TypeError):consultar_santuario(habitado=True,jogador=0,relogios=(0,0,0))

    def test_recoloracao_preserva_mascara_e_zero_literal(self):
        class Sintetico:
            def quadro(self,_):return Quadro(4,1,bytes([160,160,0,167]),bytes([0,255,255,255]),0,b'')
        plano=dict(camadas=[dict(id_motor=1,operacao='jogador',jogador=1,x=0,y=0)])
        out=compor_fachada(Sintetico(),bytes([20])*4,4,1,plano,0,0,tabelas=tabelas_jogador())
        self.assertEqual(out,bytes([20,144,0,254]))

    def test_73_associacoes_arquivos_e_mascaras(self):
        rs=json.loads((RAIZ/'artefatos/associacoes-santuario.json').read_text());self.assertEqual(len(rs),73)
        for r in rs:
            for k,v in localizar(r['id_motor']).items():self.assertEqual(r[k],v)
            q=self.c.quadro(r['id_motor'])
            self.assertEqual(hashlib.sha256(q.pixels).hexdigest(),r['sha256_pixels'])
            self.assertEqual(hashlib.sha256(q.opacidade).hexdigest(),r['sha256_opacidade'])
        self.assertEqual(sum(r['arquivo_cmp']=='BUILDING.CMP' for r in rs),43)
        html=(RAIZ/'artefatos/demo-santuario.html').read_text()
        self.assertNotIn('/*DADOS_SANTUARIO*/',html);self.assertNotIn('<script src=',html)
        self.assertEqual(html.count('"rle":'),73)
        data=json.loads(html.split('const data=')[1].split(';\nconst $')[0])
        self.assertEqual(len(data['referencias']),15);self.assertEqual(len(data['planos']),48)
        for t,p in enumerate(data['planos']):
            self.assertEqual(p,consultar_santuario(habitado=True,jogador=0,relogios=(t,t//2,t//3),celula_mapa=(17,13)))


if __name__=='__main__':unittest.main()
