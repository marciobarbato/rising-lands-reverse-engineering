"""Regressões Python contra capturas x86 v3; não importa Unicorn."""
import hashlib
import json
import unittest
from graficos import RAIZ, Catalogo, ler_paleta, Quadro
from composicao import *


class ComposicaoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=Catalogo()
        cls.r=json.loads((RAIZ/'validacao/x86-composicao.json').read_text())
        cls.tab=bytes(cls.r['tabelas_sombra'][1]['indices'])

    def test_paleta_contra_original_e_preparo_dd(self):
        p=self.c.paleta()
        self.assertEqual(p.hex(),self.r['paleta']['rgb_hex'])
        self.assertTrue(self.r['paleta']['preparo_DirectDraw_igual'])
        self.assertFalse(self.r['paleta']['DirectDraw_executado'])
        self.assertTrue(all(v%4==0 for v in p))
        raw=bytearray(self.c._ler('cd/INSTALHD/PLATGAME.PIE')[:777])
        raw[9:777]=bytes(i%256 for i in range(768))
        out=ler_paleta(raw)
        self.assertEqual(out[:3],bytes(3))
        self.assertEqual(out[3:],bytes((i<<2)&255 for i in range(3,768)))

    def test_despacho_contra_5105_capturas(self):
        self.assertEqual(self.r['resultado'],'PASSOU')
        self.assertEqual(len(self.r['despachos']),5105)
        for tipo,estado,aux,rota in self.r['despachos']:
            self.assertEqual(encaminhamento(tipo,estado,auxiliar_8a=aux)['rota'],rota)

    def test_despacho_nao_inventa_campos_auxiliares(self):
        for e in (1,22,24):
            with self.assertRaises(ValueError):encaminhamento(0,e)
        with self.assertRaises(NotImplementedError):encaminhamento(16,1,auxiliar_8a=0)
        for e in (-1,256,True,'7'):
            with self.assertRaises(ValueError):encaminhamento(0,e)

    def test_tabelas_completas_contra_original(self):
        self.assertEqual(len(self.r['tabelas_sombra']),4)
        for caso in self.r['tabelas_sombra']:
            out=tabela_sombra(self.c.paleta(),percentual=caso['percentual'],ciclos=caso['ciclos'])
            self.assertEqual(list(out),caso['indices'])
            self.assertEqual(out[5:16],bytes([223,222,221]+[167]*8))

    def test_sombras_com_recorte_e_todas_cores(self):
        w=h=128;q=self.c.quadro(SOMBRA_ID)
        self.assertEqual(len(self.r['sombras']),266)
        for caso in self.r['sombras']:
            v=caso['fundo_indice']
            fundo=bytes([v])*(w*h) if v is not None else bytes((i*17+23)%256 for i in range(w*h))
            out=compor_sombra(fundo,w,h,q,caso['x'],caso['y'],self.tab,caso['recorte'])
            self.assertEqual(hashlib.sha256(out).hexdigest(),caso['sha256'])

    def test_sombra_usa_mascara_e_fundo(self):
        q=Quadro(4,1,bytes([255,0,255,0]),bytes([0,255,255,0]),0,b'')
        self.assertTrue(self.r['sombra_sintetica']['literal_zero_opaco'])
        self.assertEqual(compor_sombra(bytes([82])*4,4,1,q,0,0,self.tab),bytes([82,self.tab[82],self.tab[82],82]))

    def test_512_composicoes_ate_retorno_original(self):
        w=h=128;fundo=bytes((i*17+23)%256 for i in range(w*h))
        self.assertEqual(len(self.r['composicoes']),512)
        for caso in self.r['composicoes']:
            out,plano=compor_unidade(self.c,fundo,w,h,tipo=caso['tipo'],estado_u8=2,
                bolsa_u16=caso['bolsa_u16'],direcao=caso['direcao'],fase=caso['fase'],x=64,y=48,tabela=self.tab)
            self.assertEqual(hashlib.sha256(out).hexdigest(),caso['sha256'])
            self.assertEqual(plano['camadas'],caso['camadas'])

    def test_estado14_sem_chamar_catalogo(self):
        class SemAcesso:
            def quadro(self,*args):raise AssertionError('Não deve consultar sprite')
        fundo=bytes([83])*4
        out,plano=compor_unidade(SemAcesso(),fundo,2,2,tipo=9,estado_u8=14,direcao=13,
                                 fase=5,x=0,y=0,tabela=self.tab)
        self.assertEqual(out,fundo);self.assertEqual(plano['camadas'],[])
        self.assertEqual(len(self.r['eta_estado14']),8)
        for r in self.r['eta_estado14']:self.assertEqual(r['resultado'],'retorno_sem_desenho')

    def test_handlers_nao_mapeados_falham_explicitamente(self):
        for estado,aux in [(4,0),(5,0),(11,0),(1,1)]:
            with self.assertRaises(NotImplementedError):
                compor_unidade(self.c,bytes(4),2,2,tipo=0,estado_u8=estado,auxiliar_8a=aux,
                    direcao=1,fase=2,x=0,y=0,tabela=self.tab)

    def test_artefatos_paleta_sombra_e_html(self):
        doc=json.loads((RAIZ/'artefatos/paleta-sombra.json').read_text())
        self.assertEqual(bytes(doc['paleta_rgb']),self.c.paleta())
        self.assertEqual(bytes(doc['tabela']),self.tab)
        html=(RAIZ/'artefatos/demo-composicao.html').read_text()
        self.assertNotIn('/*DADOS_COMPOSICAO*/',html)
        self.assertNotIn('<script src=',html)
        self.assertEqual(html.count('"rle":'),513)
        doc=json.loads((RAIZ/'artefatos/exemplos-eta-unidades.json').read_text())
        for r in doc['registros']:
            if r['estado_no_disco']==14:
                self.assertEqual(r['despacho']['rota'],'sem_desenho')
                self.assertIsNone(r['associacao'])


if __name__=='__main__':unittest.main()
