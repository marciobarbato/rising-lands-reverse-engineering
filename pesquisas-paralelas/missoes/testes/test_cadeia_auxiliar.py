"""Complete L7 auxiliary chain against original-only captures and native whole images."""
import hashlib
import json
import os
from pathlib import Path
import random
import re
import struct
import sys
import unittest

OWNED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNED))
from capturar_cadeia_auxiliar import (CD,DATA_BASE,INI_NAME,casos_sinteticos,fluxo,imagem_base,
    imagem_herdada,inicio_cadeia,mapas,resumo_imagem)
from carregador_cadeia_auxiliar import (BuffersCadeiaAuxiliar,DependenciaEntradaMonstros,
    ForaDoDominioAuxiliar,carregar_cadeia_auxiliar)
from perfil_privado_missao import DependenciaPerfil,PerfilPrivado
from candidatos_rota import aleatorio_caminhos
from formatos import ErroFormato,Leitor

BASE=bytes(imagem_base())
TIPOS=BASE[0x498400-DATA_BASE:0x498408-DATA_BASE]
SHIPPED=(CD/'INSTALHD/MONSTRE.INI').read_bytes()
ORDER=[0x47534a,0x47c24d,0x47bcc7,0x47c04a,0x458b05,0x47c30f,0x47c404,0x47ac30,0x45844c]


class LeitorRastreado(Leitor):
    def __init__(self,*args):
        super().__init__(*args);self.reads=[]

    def ler(self,size):
        start=self.posicao;data=super().ler(size)
        self.reads.append((start,size))
        return data


def fatias(image):
    view=memoryview(image)
    def region(address,size):
        return view[address-DATA_BASE:address-DATA_BASE+size]
    return BuffersCadeiaAuxiliar(region(0x509954,80),region(0x50d5b4,1004),region(0x50b18c,5254),
        region(0x50c614,4000),region(0x4e1d20,114),region(0x511ffc,804),region(0x50a9bc,1220),
        region(0x50af84,432),region(0x497164,4))


def python(data,offset,image,profile):
    """Run Python in place over image; return (result or exception, reader)."""
    reader=LeitorRastreado(data,offset)
    try:
        return carregar_cadeia_auxiliar(reader,fatias(image),tipos_grupo8=TIPOS,perfil=profile),reader
    except (ValueError,NotImplementedError,LookupError,ErroFormato) as error:
        return error,reader


def caso(name):
    return next((n,d,f,s) for n,d,f,s in casos_sinteticos() if n==name)


def perfil_tokens(groups):
    return PerfilPrivado({INI_NAME:b'[GENERAL]\r\n'+b''.join(b'GROUPE%02d=%s\r\n'%(i,v) for i,v in groups.items())})


class CapturasCadeiaAuxiliar(unittest.TestCase):
    def test_caller_order_matches_exported_original_bytes(self):
        for name in ('cadeia-0046c57d.asm','cadeia-0046c946.asm'):
            text=(OWNED/'evidencias'/name).read_text()
            self.assertEqual([int(t,16) for t in re.findall(r'call 0x([0-9a-f]+)',text)],ORDER[:-1])
        manifest=json.loads((OWNED/'evidencias/cadeia-auxiliar-manifesto.json').read_text())
        self.assertEqual(manifest['data'][1]['hex'],TIPOS.hex())

    def test_original_only_captures_all_maps_both_callers_and_synthetic(self):
        report=json.loads((OWNED/'evidencias/captura-cadeia-auxiliar-original.json').read_text())
        index={p.stem:i for i,p in enumerate(mapas())}
        synthetic={n:(i,d,f,s) for i,(n,d,f,s) in enumerate(casos_sinteticos())}
        self.assertEqual((len(report['cases']),len(report['synthetic'])),(76,20))
        for case in report['cases']+report['synthetic']:
            if case['name'] in synthetic:
                i,data,files,seed=synthetic[case['name']];offset=0;i+=100
            else:
                i=index[case['name']];data=(CD/'WORLD'/(case['name']+'.ETA')).read_bytes()
                offset,files,seed=case['offset'],{INI_NAME:SHIPPED},0x1000+i
            image=imagem_herdada(BASE,i,seed)
            self.assertEqual(hashlib.sha256(bytes(image)).hexdigest(),case['input_image_sha256'])
            profile=PerfilPrivado(files)
            result,reader=python(data,offset,image,profile)
            self.assertEqual(result.rotina_seguinte,0x45844c)
            self.assertEqual(resumo_imagem(image,reader.posicao,reader.reads,profile.chamadas,
                                           int(case['output']['stop'],16)),case['output'],case['name'])
            if 'monde01_span_hex' in case:
                self.assertEqual(image[0x50a9bc-DATA_BASE:0x50d9a0-DATA_BASE].hex(),case['monde01_span_hex'])

    def test_shape_guards_precede_every_effect(self):
        image=imagem_herdada(BASE,1,7);before=bytes(image)
        buffers=fatias(image);bad=BuffersCadeiaAuxiliar(*[getattr(buffers,f) for f in buffers.__dataclass_fields__][:-1],bytearray(3))
        reader=Leitor(fluxo())
        with self.assertRaises(ValueError):
            carregar_cadeia_auxiliar(reader,bad,tipos_grupo8=TIPOS,perfil=None)
        with self.assertRaises(ValueError):
            carregar_cadeia_auxiliar(reader,buffers,tipos_grupo8=TIPOS[:7],perfil=None)
        self.assertEqual((bytes(image),reader.posicao),(before,0))

    def test_missing_profile_binding_retains_tables_records_and_random(self):
        data=(CD/'WORLD/MONDE01.ETA').read_bytes();offset=inicio_cadeia(data)
        image=imagem_herdada(BASE,0,0x1000);seed=0x1000
        error,reader=python(data,offset,image,None)
        self.assertIsInstance(error,DependenciaEntradaMonstros);self.assertEqual(error.endereco,0x47a665)
        for _ in range(100):
            seed=aleatorio_caminhos(seed)
        monsters=fatias(image).monstros
        self.assertEqual((struct.unpack_from('<I',image,0x497164-DATA_BASE)[0],monsters[0]),(seed,0))
        self.assertTrue(all(monsters[20+12*i:22+12*i]==b'\xff\xff' for i in range(100)))
        complete=imagem_herdada(BASE,0,0x1000);python(data,offset,complete,PerfilPrivado({INI_NAME:SHIPPED}))
        for address,size in ((0x509954,80),(0x50b18c,5254),(0x50c614,4000),(0x4e1d20,114),(0x511ffc,804),(0x50d5b4,1004)):
            self.assertEqual(image[address-DATA_BASE:address-DATA_BASE+size],complete[address-DATA_BASE:address-DATA_BASE+size])
        undeclared,_=python(data,offset,imagem_herdada(BASE,0,1),PerfilPrivado({}))
        self.assertIsInstance(undeclared,DependenciaPerfil)

    def test_unsupported_domains_name_their_original_sites(self):
        cases=[(fluxo(ghosts=[(1,2)]*751),None,0x47bce1),(fluxo(influence=(401,10,[bytes(10)]*401)),None,0x47c0b1),
               (fluxo(monsters=(101,6,[bytes(6)]*101)),None,0x47ac9b),(fluxo(monsters=(100,13,[bytes(13)]*100)),None,0x47ac9b),
               (fluxo(),perfil_tokens({3:b'1,8'}),0x47a7c9),(fluxo(),perfil_tokens({2:b'0,07'}),0x48c41c),
               (fluxo(),perfil_tokens({2:b'0x5'}),0x48c41c)]
        for data,profile,address in cases:
            error,_=python(data,0,imagem_herdada(BASE,2,9),profile or PerfilPrivado({INI_NAME:SHIPPED}))
            self.assertIsInstance(error,ForaDoDominioAuxiliar);self.assertEqual(error.endereco,address)

    def test_strict_reader_failure_keeps_completed_reads(self):
        data=caso('ghost1_influence_size6')[1]
        for cut in (0,7,15,len(data)-1):
            image=imagem_herdada(BASE,3,4);error,reader=python(data[:cut],0,image,PerfilPrivado({INI_NAME:SHIPPED}))
            self.assertIsInstance(error,ErroFormato)
            self.assertEqual(reader.posicao,sum(s for _,s in reader.reads))


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional intact-x86: RISING_EMULAR=1')
class DiferencialCadeiaAuxiliar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_cadeia_auxiliar import BancadaCadeiaAuxiliar
        cls.native=BancadaCadeiaAuxiliar()
        cls.boundary_stops=cls.failure_stops=0

    def compare(self,data,offset,image,files,caller,stop=None,expected=None):
        native=self.native;native_profile=PerfilPrivado(files) if files is not None else None
        try:
            eip=native.carregar(data,offset,image,native_profile,caller,stop)
        except (ValueError,LookupError):
            eip=None;type(self).failure_stops+=1
        if stop and eip==stop[0]:
            type(self).boundary_stops+=1
        after=native.imagem();mine=bytearray(image)
        profile=PerfilPrivado(files) if files is not None else None
        result,reader=python(data,offset,mine,profile)
        if expected:
            self.assertIsInstance(result,expected)
        else:
            self.assertNotIsInstance(result,Exception)
        if bytes(mine)!=after:
            first=next(i for i in range(len(after)) if mine[i]!=after[i])
            self.fail(f'image differs first at 0x{DATA_BASE+first:x}')
        self.assertEqual((reader.posicao,reader.reads),(native.cursor,native.reads))
        if profile is not None:
            self.assertEqual(profile.chamadas,native_profile.chamadas)

    def test_all_maps_both_callers_fresh_inherited_patterns(self):
        for index,path in enumerate(mapas()):
            data=path.read_bytes();offset=inicio_cadeia(data)
            for caller,seed in (('MissionLoad',0x80000000+index),('MissionLoadName',index*0x9e3779b9)):
                self.compare(data,offset,imagem_herdada(BASE,500+index,seed),{INI_NAME:SHIPPED},caller)

    def test_supported_count_size_and_profile_domains(self):
        rng=random.Random(19);ini={INI_NAME:SHIPPED};n=0
        def run(data,files=ini,seed=None,caller=None):
            nonlocal n;n+=1
            self.compare(data,0,imagem_herdada(BASE,700+n,rng.getrandbits(32) if seed is None else seed),files,
                         caller or ('MissionLoad','MissionLoadName')[n%2])
        for count in (0,1,2,374,749,750):
            run(fluxo(ghosts=[(rng.getrandbits(16),rng.getrandbits(32)) for _ in range(count)]))
        for size in range(13):
            for count in (0,1,2,399,400):
                if count==0 or (count-1)*10+size<=4000:
                    run(fluxo(influence=(count,size,[rng.randbytes(size) for _ in range(count)])))
        for count in (0,1,2,50,99,100):
            for size in (0,1,2,5,6,7,11,12,13,24):
                if count==0 or (count-1)*12+size<=1200:
                    run(fluxo(monsters=(count,size,[rng.randbytes(size) for _ in range(count)])))
        for _ in range(12):
            records=[struct.pack('<HHH',0xffff if rng.random()<0.4 else rng.getrandbits(16),
                                 rng.choice((0,1<<rng.randrange(16),rng.getrandbits(16))),rng.getrandbits(16)) for _ in range(100)]
            run(fluxo(monsters=(100,6,records)))
        for seed in (0,1,0x7fffffff,0x80000000,0xffffffff,127773,2836):
            run(fluxo(),seed=seed)
        for name in ('absent_profile_empty_tables','profile_tokens_and_seed0'):
            _,data,files,seed=caso(name)
            for caller in ('MissionLoad','MissionLoadName'):
                run(data,files,seed,caller)

    def test_dependency_domain_and_truncation_stops_match_native_state(self):
        shipped={INI_NAME:SHIPPED};always=lambda bench,regs:True
        def token(prefix):
            return lambda bench,regs:bytes(bench.cpu.mem_read(regs['EBP'],len(prefix)))==prefix
        tokens=lambda groups:{INI_NAME:b'[GENERAL]\r\n'+b''.join(b'GROUPE%02d=%s\r\n'%(i,v) for i,v in groups.items())}
        cases=[(fluxo(),None,(0x47a665,always),DependenciaEntradaMonstros),
               (fluxo(ghosts=[(1,2)]*751),shipped,(0x47bce1,lambda b,r:r['EAX']==751),ForaDoDominioAuxiliar),
               (fluxo(influence=(401,10,[bytes(10)]*401)),shipped,(0x47c0b1,lambda b,r:r['EAX']==0x50c614+4000),ForaDoDominioAuxiliar),
               (fluxo(influence=(1,4001,[bytes(4001)])),shipped,(0x47c0b1,lambda b,r:r['EAX']==0x50c614),ForaDoDominioAuxiliar),
               (fluxo(monsters=(101,6,[bytes(6)]*101)),shipped,(0x47ac9b,lambda b,r:r['EAX']==0x50a9d0+1200),ForaDoDominioAuxiliar),
               (fluxo(monsters=(100,13,[bytes(13)]*100)),shipped,(0x47ac9b,lambda b,r:r['EAX']==0x50a9d0+99*12),ForaDoDominioAuxiliar),
               (fluxo(),tokens({1:b'0,1',3:b'1,8'}),(0x47a7c9,lambda b,r:r['ESI']==8),ForaDoDominioAuxiliar),
               (fluxo(),tokens({1:b'4',2:b'0,07'}),(0x47a7b3,token(b'07')),ForaDoDominioAuxiliar),
               (fluxo(),tokens({2:b'0x5'}),(0x47a7b3,token(b'0x')),ForaDoDominioAuxiliar)]
        for index,(data,files,stop,expected) in enumerate(cases):
            for caller in ('MissionLoad','MissionLoadName'):
                self.compare(data,0,imagem_herdada(BASE,900+index,index),files,caller,stop,expected)
        self.compare(fluxo(),0,imagem_herdada(BASE,950,5),{},'MissionLoad',expected=DependenciaPerfil)
        data=(CD/'WORLD/MONDE04.ETA').read_bytes();offset=inicio_cadeia(data)
        self.native.carregar(data,offset,imagem_herdada(BASE,951,6),PerfilPrivado(shipped),'MissionLoad')
        reads=list(self.native.reads)
        for k in sorted({0,1,2,3,len(reads)//7,len(reads)//3,len(reads)//2,len(reads)-1700,len(reads)-1210,
                         len(reads)-1201,len(reads)-1199,len(reads)-4,len(reads)-1}):
            start,size=reads[k]
            for cut in sorted({start,start+size-1}):
                self.compare(data[:cut],offset,imagem_herdada(BASE,960+k,k),shipped,'MissionLoadName',expected=ErroFormato)


if __name__=='__main__':
    unittest.main()
