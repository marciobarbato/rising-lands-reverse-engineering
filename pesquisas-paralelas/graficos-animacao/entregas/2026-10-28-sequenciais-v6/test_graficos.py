"""Integridade, regressões diferenciais e limites do adaptador independente."""
import csv
import hashlib
import importlib
import json
import struct
import sys
import unittest
from graficos import *
from extrair_evidencias import COMMIT, HASH_EXE, imagem_pe


class GraficosTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogo=Catalogo()
        cls.x86=json.loads((RAIZ/'validacao/x86.json').read_text())
        cls.associacoes=json.loads((RAIZ/'artefatos/associacoes.json').read_text())

    def test_snapshot_commit_e_integridade(self):
        m=json.loads((RAIZ/'snapshot/manifesto.json').read_text())
        self.assertEqual(m['commit'],COMMIT)
        for item in m['arquivos']:
            p=RAIZ/'snapshot'/COMMIT/item['caminho']
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),item['sha256'],str(p))

    def test_fontes_integrais(self):
        for item in self.catalogo.manifesto:
            self.assertEqual(hashlib.sha256((RAIZ/item['copia']).read_bytes()).hexdigest(),item['sha256'])

    def test_banco_e_ponteiros_no_exe(self):
        b,m=imagem_pe();ptrs=struct.unpack_from('<6I',m,0x495bc8-b)
        nomes=[m[p-b:].split(b'\0')[0].decode().split('\\')[-1].upper() for p in ptrs]
        self.assertEqual(nomes,list(ORDEM))
        self.assertEqual(struct.unpack_from('<I',m,0x412328-b)[0],0x412cfe)
        self.assertEqual(struct.unpack_from('<I',m,0x410f64-b)[0],0x410fe6)
        self.assertEqual(struct.unpack_from('<I',m,0x44812c-b)[0],0x4481c7)

    def test_identidade_soldado_no_exe_e_ini(self):
        import configparser
        b,m=imagem_pe();nome=m[0x4965ba-b:0x4965d8-b].split(b'\0')[0].decode()
        self.assertEqual(nome,'SOLDAT')
        ini=configparser.ConfigParser(interpolation=None)
        ini.read_string(self.catalogo._ler('cd/INSTALHD/RISING.INI').decode('cp1252').replace('\x1a',''))
        self.assertEqual(ini[nome]['NAME'],'SOLDADO')

    def test_bytes_das_evidencias_extraidas(self):
        base,imagem=imagem_pe()
        manifesto=json.loads((RAIZ/'evidencias/manifesto.json').read_text())
        self.assertEqual(manifesto['exe_sha256'],HASH_EXE)
        for item in manifesto['trechos']:
            a,z=int(item['inicio'],16),int(item['fim'],16)
            self.assertEqual(hashlib.sha256(imagem[a-base:z-base]).hexdigest(),item['sha256_bytes'])
            for linha in (RAIZ/'evidencias'/item['arquivo']).read_text().splitlines():
                if linha.startswith(';'):continue
                campos=linha.split();p=int(campos[0],16);bytes_asm=bytes.fromhex(campos[1])
                self.assertEqual(imagem[p-base:p-base+len(bytes_asm)],bytes_asm)

    def test_limites_indices_globais(self):
        total=0
        for nome,n in zip(ORDEM,QUANTIDADES):
            self.assertEqual(localizar(total+1)['indice_local'],0)
            self.assertEqual(localizar(total+n)['indice_local'],n-1)
            self.assertEqual(localizar(total+n)['arquivo_cmp'],nome)
            total+=n
        for invalido in (0,-1,total+1):
            with self.assertRaises(ValueError):localizar(invalido)

    def test_todos_cmp_contra_leitor_commitado(self):
        # Referência somente do snapshot privado identificado, nunca do checkout vivo.
        pasta=RAIZ/'snapshot'/COMMIT/'ferramentas';sys.path.insert(0,str(pasta))
        ref=importlib.import_module('formatos')
        self.assertEqual(Path(ref.__file__).resolve(),pasta/'formatos.py')
        total=0
        for nome in list(ORDEM)+['MENU.CMP','INVENTE.CMP']:
            dados=self.catalogo._ler('cd/INSTALHD/GRAPHICS/'+nome)
            novo=ler_cmp(dados);antigo=ref.ler_cmp(dados)
            self.assertEqual(len(novo),len(antigo))
            for a,b in zip(novo,antigo):
                self.assertEqual((a.largura,a.altura,a.pixels),(b.largura,b.altura,b.pixels))
                self.assertEqual(len(a.opacidade),a.largura*a.altura)
            total+=len(novo)
        self.assertEqual(total,12268)

    def test_alpha_literal_zero_e_salto(self):
        dados=struct.pack('<HHHI',1,4,1,5)+bytes([1,254,0,255,1])
        q=ler_cmp(dados)[0]
        self.assertEqual(q.pixels,bytes([0,0,255,0]))
        self.assertEqual(q.opacidade,bytes([0,255,255,0]))
        self.assertEqual(compor_indices(bytes([99])*4,4,1,q,0,0),bytes([99,0,255,99]))

    def test_cmp_rejeita_truncamento_e_comando_invalido(self):
        for payload in [b'',b'\x01',struct.pack('<HHHI',1,1,1,1)+b'\x80',
                        struct.pack('<HHHI',1,2,1,1)+b'\x03',
                        struct.pack('<HHHI',1,2,1,1)+b'\xfe',
                        struct.pack('<HHHI',1,0,1,0)]:
            with self.assertRaises(ErroFormato):ler_cmp(payload)

    def test_associacoes_contra_capturas_originais(self):
        self.assertEqual(self.x86['resultado'],'PASSOU')
        self.assertEqual(self.x86['exe_sha256'],HASH_EXE)
        self.assertEqual(len(self.x86['capturas_desenho']),144)
        for captura in self.x86['capturas_desenho']:
            m=consultar(captura['tipo'],captura['estado'],captura['direcao'],captura['fase'])
            self.assertEqual(m['id_motor'],captura['id_motor'])
            self.assertEqual(m['ancoragem']['x'],128-captura['x'])
            self.assertEqual(m['ancoragem']['y'],128-captura['y'])

    def test_associacoes_serializadas_completas(self):
        self.assertEqual(len(self.associacoes),144)
        with (RAIZ/'artefatos/associacoes.csv').open() as f:csv_rows=list(csv.DictReader(f))
        self.assertEqual(len(csv_rows),144)
        for m in self.associacoes:
            q=self.catalogo.quadro(m['id_motor'])
            self.assertEqual(hashlib.sha256(q.pixels).hexdigest(),m['sha256_pixels'])
            self.assertEqual(hashlib.sha256(q.opacidade).hexdigest(),m['sha256_opacidade'])
        self.assertEqual(len(set(m['id_motor'] for m in self.associacoes)),64)

    def test_fase_parada_nao_e_primeiro_quadro(self):
        self.assertEqual([consultar(0,'parado',d)['id_motor'] for d in range(1,17,2)],
                         [2084,2092,2100,2108,2116,2124,2132,2140])
        self.assertEqual(self.x86['parada']['fase_resultante'],2)

    def test_sequencia_e_overflow_contador(self):
        fase=2;contador=0;seq=[]
        for _ in range(16):
            fase,contador=avancar_animacao(fase,contador);seq.append(fase)
        self.assertEqual(seq,[2,3,3,4,4,5,5,6,6,7,7,0,0,1,1,2])
        self.assertEqual(avancar_animacao(7,255,0),(0,0))
        self.assertEqual(avancar_animacao(7,2,2),(7,3))
        self.assertEqual(avancar_animacao(7,1,2),(0,0))

    def test_rejeita_mapeamento_nao_validado(self):
        with self.assertRaises(NotImplementedError):consultar(tipo=1)
        for kw in [dict(estado='ataque'),dict(direcao=0),dict(direcao=17),dict(fase=8)]:
            with self.assertRaises(ValueError):consultar(**kw)

    def test_direcoes_mapa_contra_x86(self):
        for r in self.x86['direcoes']:
            self.assertEqual(tuple(consultar(direcao=r['direcao'])['vetor_mapa']),(r['dx'],r['dy']))
        for d in range(1,17,2):
            self.assertEqual(consultar(direcao=d)['id_motor'],consultar(direcao=d+1)['id_motor'])
            self.assertIsNone(consultar(direcao=d+1)['vetor_mapa'])

    def test_posicao_na_celula(self):
        self.assertEqual(posicao_desenho(7,15,3,11), (88,106))
        for r in self.x86['ancoragem']:
            self.assertEqual(posicao_desenho(4,4,deslocamento_x=r['dx'],deslocamento_y=r['dy']),
                             (r['resultado']['x'],r['resultado']['y']))

    def test_composicoes_contra_hashes_x86(self):
        w=h=128;fundo=bytes((i*17+23)%256 for i in range(w*h))
        for caso in self.x86['composicao']['comparacoes']:
            pixels=compor_indices(fundo,w,h,self.catalogo.quadro(caso['id_motor']),caso['x'],caso['y'],caso['recorte'])
            self.assertEqual(hashlib.sha256(pixels).hexdigest(),caso['sha256_superficie'])

    def test_exemplos_eta_com_registro_original(self):
        doc=json.loads((RAIZ/'artefatos/exemplos-eta.json').read_text());eta=self.catalogo._ler('cd/WORLD/MONDE01.ETA')
        self.assertEqual(len(doc['soldados']),3)
        for r in doc['soldados']:
            raw=eta[r['offset_registro']:r['offset_registro']+784]
            self.assertEqual(hashlib.sha256(raw).hexdigest(),r['sha256_registro'])
            self.assertEqual((raw[1],raw[2]),(0,7))
            self.assertEqual(r['id_motor_por_formula'],2084)

    def test_demo_e_atlas_autonomos(self):
        texto=(RAIZ/'artefatos/demo.html').read_text()
        self.assertNotIn('/*DADOS_SPRITES*/',texto)
        self.assertEqual(texto.count('data:image/png;base64,'),64)
        self.assertNotIn('<script src=',texto)
        for nome in ('atlas-soldado.png','parada-soldado.png'):
            self.assertTrue((RAIZ/'artefatos'/nome).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))

    def test_saida_png_rgba(self):
        dados=self.catalogo.imagem_png(direcao=1)
        self.assertEqual(struct.unpack_from('>II',dados,16),(68,61))
        self.assertEqual(dados[25],6)  # PNG RGBA, não palette com zero transparente.


if __name__=='__main__':unittest.main()
