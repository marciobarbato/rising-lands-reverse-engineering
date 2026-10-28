"""Regressões independentes contra os resultados x86 preservados da v6."""
import base64
import csv
import hashlib
import json
import unittest
from graficos import Catalogo, RAIZ, localizar
from objetos import compor_passe, consultar_objeto, ler_objetos_eta
from sequenciais import *


class SequenciaisTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=Catalogo()
        cls.r=json.loads((RAIZ/'validacao/x86-sequenciais.json').read_text())
        cls.tab=bytes(cls.r['tabela_sombra'])

    def test_6144_capturas_dominios_explicitamente_separados(self):
        self.assertEqual(self.r['resultado'],'PASSOU')
        self.assertEqual(len(self.r['capturas']),6144)
        for r in self.r['capturas']:
            kw=dict(auxiliar_u8=r['auxiliar'],descoberta_u8=r['descoberta'],iluminacao_u8=r['iluminacao'])
            if not r['dentro_contrato']:
                with self.assertRaises(ValueError):consultar_sequencial(r['codigo'],**kw)
                continue
            plano=consultar_sequencial(r['codigo'],**kw)
            eventos=[dict(id_motor=q['id_motor'],x=64+q['x'],y=108+q['y'],operacao=q['operacao']) for q in plano[r['passe']]]
            self.assertEqual(eventos,r['camadas'])

    def test_pares_de_auxiliares_e_limites_das_tres_sequencias(self):
        for co in (66,67,68):
            for fase in range(16):
                planos=[consultar_sequencial(co,auxiliar_u8=2*fase+k,descoberta_u8=0,iluminacao_u8=0) for k in (0,1)]
                self.assertEqual(planos[0]['terreno'],planos[1]['terreno'])
        self.assertEqual(consultar_sequencial(66,auxiliar_u8=31,descoberta_u8=0,iluminacao_u8=0)['terreno'][0]['id_motor'],10838)
        self.assertEqual(consultar_sequencial(67,auxiliar_u8=0,descoberta_u8=0,iluminacao_u8=0)['terreno'][0]['id_motor'],10839)
        self.assertEqual(consultar_sequencial(68,auxiliar_u8=31,descoberta_u8=0,iluminacao_u8=0)['terreno'][0]['id_motor'],10870)

    def test_142_buffers_originais_com_sombra_e_recorte(self):
        self.assertEqual(len(self.r['pixels']),142)
        fundo=bytes((i*17+23)%256 for i in range(160*160))
        for r in self.r['pixels']:
            p=consultar_sequencial(r['codigo'],auxiliar_u8=r['aux'],descoberta_u8=0,iluminacao_u8=r['l'])
            out=compor_passe(self.c,fundo,160,160,p,'terreno',r['x'],r['y'],tabela_sombra=self.tab,recorte=r['recorte'])
            self.assertEqual(hashlib.sha256(out).hexdigest(),r['sha256'])
        self.assertEqual(sum(x['origem']=='MONDE01' for x in self.r['pixels']),32)

    def test_mesmo_cmp_copy_depois_sombra_quando_sem_iluminacao(self):
        for co in CODIGOS_SEQUENCIAIS:
            claro=consultar_sequencial(co,auxiliar_u8=17,descoberta_u8=0,iluminacao_u8=0)
            escuro=consultar_sequencial(co,auxiliar_u8=17,descoberta_u8=0,iluminacao_u8=16)
            self.assertEqual([q['operacao'] for q in escuro['terreno']],['copiar','sombra'])
            self.assertEqual({q['id_motor'] for q in escuro['terreno']},{claro['terreno'][0]['id_motor']})
            oculto=consultar_sequencial(co,auxiliar_u8=17,descoberta_u8=16,iluminacao_u8=0)
            self.assertEqual(oculto['terreno'],[])

    def test_normalizacao_integral_contra_original(self):
        eta=self.c._ler('cd/WORLD/MONDE01.ETA')
        fixtures=[(eta[0x30004:0x40004],eta[0x40004:0x50004]),
                  (bytes(i//256 for i in range(65536)),bytes(i%256 for i in range(65536)))]
        self.assertEqual(len(self.r['normalizacao']),2)
        for (obj,aux),r in zip(fixtures,self.r['normalizacao']):
            out=normalizar_inicio(obj,aux)
            self.assertEqual(hashlib.sha256(out['objetos']).hexdigest(),r['objetos_saida'])
            self.assertEqual(hashlib.sha256(out['auxiliares']).hexdigest(),r['auxiliares_saida'])
            self.assertEqual(out['alteradas'],r['alteradas']);self.assertTrue(r['outras_camadas_preservadas'])
        self.assertEqual(len(self.r['normalizacao'][0]['alteradas']),0)
        self.assertEqual(len(self.r['normalizacao'][1]['alteradas']),256)
        self.assertEqual(normalizar_inicio(*fixtures[1])['auxiliares'][54*256:55*256],bytes([1])*256)

    def test_4096_nextanim_sem_alteracao_nem_consumo(self):
        self.assertEqual(len(self.r['next_anim']),4096)
        self.assertEqual({r[0] for r in self.r['next_anim']},set(CODIGOS_SEQUENCIAIS))
        for codigo,aux,relogio,fim,cursor in self.r['next_anim']:
            self.assertEqual(aux,fim);self.assertEqual(cursor,255)

    def test_486_registros_cobertos_sem_mudar_contrato_v5(self):
        dados=self.c._ler('cd/WORLD/MONDE01.ETA');r=ler_objetos_eta_v6(dados)
        self.assertEqual(r,self.r['eta']);self.assertEqual(len(r['registros']),486)
        self.assertTrue(all(x['mapeado'] for x in r['registros']))
        self.assertEqual(sum(x['catalogo']=='v6' for x in r['registros']),16)
        self.assertEqual(sum(x['mapeado'] for x in ler_objetos_eta(dados)['registros']),470)
        for x in r['registros']:
            consultar_objeto_v6(x['codigo'],auxiliar_u8=x['auxiliar_u8'],descoberta_u8=0,iluminacao_u8=0)
        antigo=consultar_objeto(5,auxiliar_u8=2,descoberta_u8=0,iluminacao_u8=0)
        self.assertEqual(consultar_objeto_v6(5,auxiliar_u8=2,descoberta_u8=0,iluminacao_u8=0),antigo)

    def test_entrada_sem_contrato_recusada(self):
        kw=dict(auxiliar_u8=0,descoberta_u8=0,iluminacao_u8=0)
        for co in (0,55,65,69,70,255,True):
            with self.assertRaises(NotImplementedError):consultar_sequencial(co,**kw)
        for key,value in [('auxiliar_u8',32),('auxiliar_u8',256),('auxiliar_u8',False),('descoberta_u8',-1),('iluminacao_u8',True)]:
            with self.assertRaises(ValueError):consultar_sequencial(66,**(kw|{key:value}))
        with self.assertRaises(ValueError):normalizar_inicio(bytes(65535),bytes(65536))

    def test_147_associacoes_e_48_quadros(self):
        rows=json.loads((RAIZ/'artefatos/associacoes-sequenciais.json').read_text())
        self.assertEqual(len(rows),147);self.assertEqual(len({r['id_motor'] for r in rows}),48)
        for r in rows:
            for k,v in localizar(r['id_motor']).items():self.assertEqual(r[k],v)
            q=self.c.quadro(r['id_motor'])
            self.assertEqual(hashlib.sha256(q.pixels).hexdigest(),r['sha256_pixels'])
            self.assertEqual(hashlib.sha256(q.opacidade).hexdigest(),r['sha256_opacidade'])
        with (RAIZ/'artefatos/associacoes-sequenciais.csv').open() as f:self.assertEqual(len(list(csv.DictReader(f))),147)

    def test_html_planos_buffers_e_proveniencia(self):
        html=(RAIZ/'artefatos/demo-sequenciais.html').read_text();self.assertNotIn('/*DADOS_SEQUENCIAIS*/',html)
        self.assertNotIn('<script src=',html)
        data=json.loads(html.split('const data=')[1].split(';\nconst $')[0])
        self.assertEqual(len(data['planos']),291);self.assertEqual(len(data['referencias']),98)
        for p in data['planos']:
            self.assertEqual(p,consultar_sequencial(p['codigo'],auxiliar_u8=p['auxiliar_u8'],descoberta_u8=p['descoberta_u8'],iluminacao_u8=p['iluminacao_u8']))
        for ref in data['referencias']:
            raw=base64.b64decode(ref['indices_rle']);out=b''.join(bytes([raw[i+1]])*raw[i] for i in range(0,len(raw),2))
            self.assertEqual(len(out),160*160);self.assertEqual(hashlib.sha256(out).hexdigest(),ref['sha256'])
        prov=json.loads((RAIZ/'evidencias/proveniencia-v6.json').read_text())
        self.assertEqual(prov['commit_predecessor'],'d96034af2a264e77dc49269c6e0fe563cfddabf4')
        for item in prov['fontes_predecessoras']:
            path=RAIZ/item['caminho'].split('graficos-animacao/',1)[1]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),item['sha256'])


if __name__=='__main__':unittest.main()
