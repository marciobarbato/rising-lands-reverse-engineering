"""Regressões Python dos objetos, contra capturas preservadas do x86 original."""
import hashlib
import json
import unittest
from graficos import Catalogo, RAIZ, localizar
from objetos import *


class ObjetosTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=Catalogo();cls.r=json.loads((RAIZ/'validacao/x86-objetos.json').read_text())
        cls.tab=bytes(cls.r['tabela_sombra'])

    def test_512_flags_contra_original(self):
        self.assertEqual(len(self.r['flags']),512)
        for campo,v,out in self.r['flags']:
            vis=visibilidade(v if campo=='descoberta' else 0,v if campo=='iluminacao' else 0)
            self.assertEqual(vis['descoberto' if campo=='descoberta' else 'iluminado'],bool(out))
        self.assertFalse(visibilidade(1,0)['descoberto'])
        self.assertTrue(visibilidade(32,32)['descoberto'])
        self.assertTrue(visibilidade(32,32)['iluminado'])

    def test_1344_capturas_dos_dois_passes(self):
        self.assertEqual(self.r['resultado'],'PASSOU');self.assertEqual(len(self.r['capturas']),1344)
        for r in self.r['capturas']:
            pl=consultar_objeto(r['codigo'],auxiliar_u8=r['auxiliar'],descoberta_u8=r['descoberta'],iluminacao_u8=r['iluminacao'])
            ev=[dict(id_motor=q['id_motor'],x=64+q['x'],y=108+q['y'],operacao=q['operacao']) for q in pl[r['passe']]]
            self.assertEqual(ev,r['camadas'])

    def test_grupo_preserva_corpo_sombra_intercalados(self):
        p=consultar_objeto(5,auxiliar_u8=3,descoberta_u8=0,iluminacao_u8=0)
        self.assertEqual([x['operacao'] for x in p['sprites']],['copiar','sombra']*3)
        self.assertEqual(p['terreno'],[])
        escuro=consultar_objeto(5,auxiliar_u8=3,descoberta_u8=0,iluminacao_u8=16)
        for a,b in zip(p['sprites'],escuro['sprites']):
            self.assertEqual(b['id_motor']-a['id_motor'],92 if a['operacao']=='copiar' else 0)
        for co in [12,22,28,52]:
            p=consultar_objeto(co,auxiliar_u8=255,descoberta_u8=0,iluminacao_u8=0)
            self.assertEqual(len(p['terreno']),1);self.assertEqual(p['sprites'],[])

    def test_193_superficies_e_recortes(self):
        self.assertEqual(len(self.r['pixels']),193);fundo=bytes((i*17+23)%256 for i in range(160*160))
        for r in self.r['pixels']:
            pl=consultar_objeto(r['codigo'],auxiliar_u8=r['auxiliar'],descoberta_u8=r['descoberta'],iluminacao_u8=r['iluminacao'])
            out=compor_passe(self.c,fundo,160,160,pl,r['passe'],r['x'],r['y'],tabela_sombra=self.tab,recorte=r['recorte'])
            self.assertEqual(hashlib.sha256(out).hexdigest(),r['sha256'])

    def test_consumo_aleatorio_4096_estados(self):
        self.assertEqual(len(self.r['animacao']),4096)
        for codigo,fase,clock,cursor,fim,idx in self.r['animacao']:
            r=avancar_arvore(fase_u8=fase,relogio_u32=clock,indice_aleatorio_u8=cursor,tabela_aleatoria=bytes(range(256)))
            self.assertEqual((r['fase'],r['indice']),(fim,idx));self.assertEqual(r['consumiu'],clock%4==0)
        r=avancar_arvore(fase_u8=3,relogio_u32=0,indice_aleatorio_u8=255,tabela_aleatoria=bytes([1])*256)
        self.assertEqual(r,dict(fase=3,indice=0,consumiu=True))

    def test_fase_bruta_overflow_e_objetos_estaticos(self):
        self.assertEqual(len(self.r['animacao_bruta']),256)
        for fase,fim,idx in self.r['animacao_bruta']:
            r=avancar_arvore(fase_u8=fase,relogio_u32=0xfffffffc,indice_aleatorio_u8=255,tabela_aleatoria=bytes(256))
            self.assertEqual((r['fase'],r['indice']),(fim,idx))
        self.assertEqual(self.r['objetos_estaticos'],[v for v in CODIGOS if v>11])

    def test_ordem_da_varredura_e_cursor_compartilhado(self):
        self.assertEqual(len(self.r['varreduras']),2)
        for r in self.r['varreduras']:
            cursor=r['cursor_inicial'];fases=[]
            for co,fa in zip(r['codigos'],r['fases_iniciais']):
                if co<=11:
                    p=avancar_arvore(fase_u8=fa,relogio_u32=r['relogio'],indice_aleatorio_u8=cursor,tabela_aleatoria=bytes(range(256)))
                    fa=p['fase'];cursor=p['indice']
                fases.append(fa)
            self.assertEqual(fases,r['fases_finais']);self.assertEqual(cursor,r['cursor_final'])
            self.assertTrue(r['fora_da_janela_inalterado'])

    def test_ETA_e_leitura_parcial_original(self):
        eta=self.c._ler('cd/WORLD/MONDE01.ETA');r=ler_objetos_eta(eta)
        self.assertEqual(r,self.r['eta']);self.assertEqual(len(r['registros']),486)
        self.assertEqual(sum(v['mapeado'] for v in r['registros']),470)
        self.assertEqual(sum(v['codigo']<=11 for v in r['registros']),38)
        for read in self.r['leituras_ETA']:
            raw=eta[read['offset']:read['offset']+read['bytes']]
            self.assertEqual(hashlib.sha256(raw).hexdigest(),read['sha256'])
        self.assertEqual([v['offset'] for v in self.r['leituras_ETA']],[4,0x10004,0x30004,0x40004])
        self.assertEqual({v['codigo'] for v in r['registros'] if not v['mapeado']},{66,67})
        with self.assertRaises(ValueError):ler_objetos_eta(eta[:0x50003])

    def test_fora_do_contrato_falha(self):
        kw=dict(auxiliar_u8=0,descoberta_u8=0,iluminacao_u8=0)
        for co in (0,23,27,53,66,255,True):
            with self.assertRaises(NotImplementedError):consultar_objeto(co,**kw)
        for k,v in [('auxiliar_u8',4),('auxiliar_u8',-1),('descoberta_u8',256),('iluminacao_u8',False)]:
            with self.assertRaises(ValueError):consultar_objeto(1,**(kw|{k:v}))
        with self.assertRaises(TypeError):consultar_objeto(1,auxiliar_u8=0)
        with self.assertRaises(ValueError):avancar_arvore(fase_u8=0,relogio_u32=0,indice_aleatorio_u8=0,tabela_aleatoria=bytes(255))

    def test_tabelas_atlas_e_html(self):
        rows=json.loads((RAIZ/'artefatos/associacoes-objetos.json').read_text())
        self.assertEqual(len(rows),344);self.assertEqual(len({r['id_motor'] for r in rows}),156)
        for r in rows:
            for k,v in localizar(r['id_motor']).items():self.assertEqual(r[k],v)
            q=self.c.quadro(r['id_motor'])
            self.assertEqual(hashlib.sha256(q.pixels).hexdigest(),r['sha256_pixels'])
            self.assertEqual(hashlib.sha256(q.opacidade).hexdigest(),r['sha256_opacidade'])
        html=(RAIZ/'artefatos/demo-objetos.html').read_text();self.assertNotIn('/*DADOS_OBJETOS*/',html)
        self.assertNotIn('<script src=',html)
        data=json.loads(html.split('const data=')[1].split(';\nconst $')[0])
        self.assertEqual(len(data['planos']),160);self.assertEqual(len(data['referencias']),102)
        self.assertEqual(len(data['quadros']),156)
        for p in data['planos']:
            self.assertEqual(p,consultar_objeto(p['codigo'],auxiliar_u8=p['auxiliar_u8'],descoberta_u8=p['descoberta_u8'],iluminacao_u8=p['iluminacao_u8']))


if __name__=='__main__':unittest.main()
