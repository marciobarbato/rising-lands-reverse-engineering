"""Regressões Python contra resultados originais já registrados; sem Unicorn."""
import configparser
import csv
import hashlib
import json
import struct
import unittest
from graficos import RAIZ, TIPOS, Catalogo, consultar, posicao_desenho, compor_indices
from extrair_evidencias import HASH_EXE, imagem_pe


class TrabalhadoresTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=Catalogo()
        cls.x=json.loads((RAIZ/'validacao/x86-trabalhadores.json').read_text())
        cls.rows=json.loads((RAIZ/'artefatos/associacoes-unidades.json').read_text())

    def test_identidade_dos_tipos_e_hashes(self):
        base,im=imagem_pe();doc=json.loads((RAIZ/'evidencias/identidade-tipos.json').read_text())
        self.assertEqual(doc['exe_sha256'],HASH_EXE)
        ini=configparser.ConfigParser(interpolation=None)
        ini.read_string(self.c._ler('cd/INSTALHD/RISING.INI').decode('cp1252').replace('\x1a',''))
        for tipo,s in TIPOS.items():
            r=doc['registros'][tipo];a=0x4965ae+50*tipo;raw=im[a-base:a-base+50]
            self.assertEqual(r['bytes_hex'],raw.hex())
            self.assertEqual(r['sha256'],hashlib.sha256(raw).hexdigest())
            self.assertEqual(raw[12:42].split(b'\0')[0].decode(),s['chave_ini'])
            self.assertEqual(ini[s['chave_ini']]['NAME'],s['nome'])
            for table,field in [(0x412328,'ramo'),(0x4572e8,'init'),(0x44812c,'stop')]:
                self.assertEqual(struct.unpack_from('<I',im,table-base+4*tipo)[0],s[field])

    def test_capturas_originais_todas_direcoes_fases_variantes(self):
        self.assertEqual(self.x['resultado'],'PASSOU');self.assertEqual(self.x['exe_sha256'],HASH_EXE)
        self.assertEqual(len(self.x['capturas_desenho']),1008)
        keys=set()
        for r in self.x['capturas_desenho']:
            m=consultar(r['tipo'],r['estado'],r['direcao'],r['fase'],bolsa_u16=r['bolsa_u16'])
            self.assertEqual(m['id_motor'],r['id_motor'])
            self.assertEqual((128-m['ancoragem']['x'],128-m['ancoragem']['y']),(r['x'],r['y']))
            self.assertEqual(r['sombras'],[dict(id_motor=10784,x=130,y=154)])
            keys.add((r['tipo'],r['estado'],r['direcao'],r['fase'],r['bolsa_u16']))
        self.assertEqual(len(keys),1008)

    def test_parada_por_tipo_contador_preservado(self):
        self.assertEqual(len(self.x['paradas']),32)
        for r in self.x['paradas']:
            m=consultar(r['tipo'],'parado',1,bolsa_u16=0)
            self.assertEqual(m['fase'],r['fase_saida']);self.assertEqual(r['contador_preservado'],77)
        self.assertEqual({t:consultar(t,bolsa_u16=0)['fase'] for t in (5,6,7,9)}, {5:5,6:2,7:3,9:5})

    def test_predicado_bolsa_16_bits_e_campos_posteriores(self):
        for r in self.x['campos_bolsa']:
            self.assertEqual(consultar(r['tipo'],'parado',15,bolsa_u16=r['bolsa_u16'])['id_motor'],r['id_motor'])
        for tipo in (5,6,7):
            self.assertNotEqual(consultar(tipo,bolsa_u16=0)['id_motor'],consultar(tipo,bolsa_u16=256)['id_motor'])
            self.assertEqual(consultar(tipo,bolsa_u16=1)['id_motor'],consultar(tipo,bolsa_u16=65535)['id_motor'])

    def test_bolsa_ausente_e_invalida_falham(self):
        for tipo in (5,6,7):
            with self.assertRaises(ValueError):consultar(tipo)
            for valor in (-1,65536,True,False,'0',1.5):
                with self.assertRaises(ValueError):consultar(tipo,bolsa_u16=valor)
        for tipo in (0,9):
            self.assertEqual(consultar(tipo)['id_motor'],consultar(tipo,bolsa_u16=65535)['id_motor'])

    def test_sem_novos_tipos_ou_estados_presumidos(self):
        for tipo in set(range(26))-set(TIPOS):
            with self.assertRaises(NotImplementedError):consultar(tipo,bolsa_u16=0)
        for estado in (14,'trabalhando','ataque'):
            with self.assertRaises(ValueError):consultar(5,estado=estado,bolsa_u16=0)

    def test_parametros_e_contadores_comparados(self):
        for r in self.x['parametros']:
            self.assertEqual((r['quantidade'],r['periodo'],r['oscilacao_0x99']),(8,2,0))
        self.assertEqual({r['tipo']:r['casos'] for r in self.x['contadores']},{5:4096,6:4096,7:4096,9:4096})

    def test_ancoras_e_deslocamentos_assinados(self):
        self.assertEqual(len(self.x['ancoragem']),28)
        for r in self.x['ancoragem']:
            self.assertEqual(posicao_desenho(4,4,tipo=r['tipo'],deslocamento_x=r['dx'],deslocamento_y=r['dy']),
                             (r['x'],r['y']))
        with self.assertRaises(NotImplementedError):posicao_desenho(0,0,tipo=1)

    def test_512_quadros_e_tabela_integral(self):
        self.assertEqual(len(self.rows),1152)
        with (RAIZ/'artefatos/associacoes-unidades.csv').open() as f:
            csvrows=list(csv.DictReader(f))
        self.assertEqual(len(csvrows),len(self.rows))
        self.assertEqual(len({r['id_motor'] for r in self.rows}),512)
        for r,cr in zip(self.rows,csvrows):
            m=consultar(r['tipo'],r['estado'],r['direcao'],r['fase'],bolsa_u16=r['bolsa_u16'])
            for field in ('id_motor','indice_local','indice_global','arquivo_cmp','ancoragem'):
                self.assertEqual(r[field],m[field])
            self.assertEqual(int(cr['id_motor']),r['id_motor'])
            q=self.c.quadro(r['id_motor'])
            self.assertEqual(r['sha256_pixels'],hashlib.sha256(q.pixels).hexdigest())
            self.assertEqual(r['sha256_opacidade'],hashlib.sha256(q.opacidade).hexdigest())

    def test_composicoes_python_contra_hash_x86(self):
        w=h=128;fundo=bytes((i*17+23)%256 for i in range(w*h))
        self.assertEqual(len(self.x['composicoes']),448)
        for r in self.x['composicoes']:
            pixels=compor_indices(fundo,w,h,self.c.quadro(r['id_motor']),r['x'],r['y'],r['recorte'])
            self.assertEqual(hashlib.sha256(pixels).hexdigest(),r['sha256_superficie'])

    def test_eta_sem_afirmar_estado_14(self):
        doc=json.loads((RAIZ/'artefatos/exemplos-eta-unidades.json').read_text())
        eta=self.c._ler('cd/WORLD/MONDE01.ETA');vinculos=0;excluidos=0
        for r in doc['registros']:
            raw=eta[r['offset_registro']:r['offset_registro']+784];ram=raw[:140]+raw[652:]
            self.assertEqual(hashlib.sha256(raw).hexdigest(),r['sha256_registro'])
            self.assertEqual(struct.unpack_from('<H',ram,10)[0],r['bolsa_u16_no_disco'])
            if ram[2]==14:
                self.assertIsNone(r['associacao']);excluidos+=1
            else:
                self.assertIn(ram[2],(2,7));self.assertEqual(r['associacao']['fase'],ram[0xa4]);vinculos+=1
        self.assertEqual((vinculos,excluidos),(6,8))

    def test_demo_e_atlas(self):
        html=(RAIZ/'artefatos/demo-unidades.html').read_text()
        self.assertEqual(html.count('data:image/png;base64,'),512)
        self.assertNotIn('/*DADOS_UNIDADES*/',html);self.assertNotIn('<script src=',html)
        for tipo,s in TIPOS.items():
            for v in range(len(s['bases'])):
                data=(RAIZ/'artefatos'/f'atlas-tipo-{tipo}-{v}.png').read_bytes()
                self.assertEqual(struct.unpack_from('>II',data,16),(1560,1590))


if __name__=='__main__':unittest.main()
