"""MissionLoad/MissionLoadName reset prefixes against original-only captures and native state."""
import hashlib
import json
import os
from pathlib import Path
import random
import struct
import sys
import unittest

OWNED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNED))
from capturar_reinicio_missao import (DATA_BASE,REGIONS,casos_folhas,imagem_reinicio,pools,regiao,resumo)
from capturar_nome import jogadores_sinteticos
from reinicio_missao import (DependenciaReinicio,ForaDoDominioReinicio,MemoriaReinicio,MemoriaReinicioNome,
    ProvedoresReinicio,continuar_reinicio_missao,continuar_reinicio_missao_nome,inicializar_baloes,
    inicializar_caixas_mensagem,resetar_icones,resetar_para_missao,resetar_para_missao_nome)
from integracao.providers import load_economy_resources
from mercado import Mercado

load_economy_resources()
from aprendizagem import Aprendizagem

FIELDS={'contadores':'counters','icones':'icons','icones_alterados':'icons_changed','mensagens':'message_boxes',
        'baloes':'balloons','estruturas':'structures','estruturas_bandeiras':'structure_flags',
        'estruturas_selecoes':'structure_selections','missao':'mission'}


class Unidades:
    def __init__(self,units,bags):
        self.unidades=bytearray(units);self.bolsas_tipos_unidades=[bytearray(b) for b in bags]


class Estado:
    """Python copies of every inherited region, written back for whole-image comparison."""
    def __init__(self,image,seed,players=(0,0,0)):
        units,bags,projectiles=pools(seed)
        self.image=bytearray(image);self.players=jogadores_sinteticos(players)
        self.memoria=MemoriaReinicio(projeteis=bytearray(projectiles),unidades=Unidades(units,bags),
            **{field:bytearray(regiao(image,name)) for field,name in FIELDS.items()})
        self.extra=MemoriaReinicioNome(bytearray(regiao(image,'unit_realizable')),
                                       bytearray(regiao(image,'structure_realizable')),regiao(image,'network')[0])
        self.economia=Aprendizagem(inventados=bytes(regiao(image,'inventions')))
        self.economia.propriedade.sortilegios[:]=regiao(image,'spells')

    def diretorios(self):
        return {0x509494:bytes(regiao(self.image,'directory_net')),0x509594:bytes(regiao(self.image,'directory'))}

    def tecnologia(self):
        self.economia.zerar_tecnologia()

    def final(self):
        image=bytearray(self.image)
        def put(name,data):
            address,size=REGIONS[name];image[address-DATA_BASE:address-DATA_BASE+size]=data
        for field,name in FIELDS.items():
            put(name,getattr(self.memoria,field))
        put('unit_realizable',self.extra.unidades_realizaveis);put('structure_realizable',self.extra.estruturas_realizaveis)
        put('spells',self.economia.propriedade.sortilegios);put('inventions',self.economia.inventados)
        return dict(image=bytes(image),units=bytes(self.memoria.unidades.unidades),
                    bags=tuple(bytes(b) for b in self.memoria.unidades.bolsas_tipos_unidades),
                    projectiles=bytes(self.memoria.projeteis),players=self.players)


def executar(kind,state,case):
    """Run the Python counterpart of one captured native entry; return (extra strings, error)."""
    m=state.memoria
    try:
        if kind=='IconeReset':
            resetar_icones(m.icones,m.icones_alterados);return {},None
        if kind=='MessageBoxInit':
            inicializar_caixas_mensagem(m.mensagens);return {},None
        if kind=='BallonInit':
            inicializar_baloes(m.baloes);return {},None
        if kind=='MissionLoad_prefix':
            provider=Mercado(jogadores=state.players)
            resetar_para_missao(m,state.diretorios()[0x509594]+b'\0',ProvedoresReinicio(),
                                variante_u8=case.get('variant'),simpatia=provider.simpatia)
        if kind=='MissionLoad_tail':
            request=continuar_reinicio_missao(m,case['path'].encode('latin-1'))
            return dict(path=request.caminho,mode=request.modo),None
        if kind=='MissionLoadName_prefix':
            resetar_para_missao_nome(m,state.extra,case['name'].encode('latin-1')+b'\0',state.diretorios(),ProvedoresReinicio())
        if kind=='MissionLoadName_tail':
            continuar_reinicio_missao_nome(m,state.extra,case['name'].encode('latin-1')+b'\0',state.diretorios(),
                                           ProvedoresReinicio(tecnologia=state.tecnologia))
    except DependenciaReinicio as error:
        extra=dict(path=error.caminho,name=error.caminho[len(state.diretorios()[0x509594].split(b'\0')[0]):]) if error.caminho is not None else {}
        if kind=='MissionLoadName_prefix':
            extra=dict(name_argument=case['name'].encode('latin-1'))
        return extra,error
    raise AssertionError(f'{kind} completed without reaching its declared stop')


def imagem_do_caso(case):
    kind,seed=case['kind'],case['seed']
    if kind=='IconeReset':
        flag=case['flag'];image=imagem_reinicio(case['icon_case']*3+flag%7,icons=casos_folhas()[case['icon_case']])
        image[0x4e05a2-DATA_BASE]=flag;return image,(0,0,0)
    if kind in ('MessageBoxInit','BallonInit'):
        return imagem_reinicio(40+seed),(0,0,0)
    if kind=='MissionLoad_prefix':
        number=case['number'];values=(100,-20 & 255,90) if number in (10,12,17) else (0,0,0)
        return imagem_reinicio(200+number,number=number,variant=case['variant'],directory=case['directory'].encode('latin-1')),values
    if kind=='MissionLoad_tail':
        return imagem_reinicio(300+seed),(0,0,0)
    if kind=='MissionLoadName_prefix':
        return imagem_reinicio(400+seed),(0,0,0)
    return imagem_reinicio(500+seed*2+case['network'],network=case['network']),(0,0,0)


EXPECTED_STOP={'MissionLoad_prefix':('TerrainReset',0x46c35f),'MissionLoadName_prefix':('TerrainReset',0x46c60f),
               'MissionLoadName_tail':('RechercheReset',0x46c68c)}


class CapturasReinicio(unittest.TestCase):
    def test_original_only_captures_leaves_prefixes_and_tails(self):
        report=json.loads((OWNED/'evidencias/captura-reinicio-original.json').read_text())
        self.assertEqual(len(report['cases']),170)
        for case in report['cases']:
            image,players=imagem_do_caso(case)
            self.assertEqual(hashlib.sha256(bytes(image)).hexdigest(),case['input_image_sha256'])
            state=Estado(image,case['seed'],players)
            extra,error=executar(case['kind'],state,case)
            if case['kind'] in EXPECTED_STOP:
                self.assertEqual((error.rotina,error.chamada),EXPECTED_STOP[case['kind']])
                self.assertEqual(error.chamada,int(case['stop'],16))
            self.assertEqual(resumo(state.final(),extra),case['output'],(case['kind'],case['seed']))

    def test_guards_precede_effects_and_dependencies_keep_earlier_stores(self):
        state=Estado(imagem_reinicio(1),1);before=state.final()
        bad=MemoriaReinicio(**{**state.memoria.__dict__,'projeteis':bytearray(5599)})
        with self.assertRaises(ValueError):
            resetar_para_missao(bad,b'\0',ProvedoresReinicio())
        with self.assertRaises(ValueError):
            resetar_para_missao(state.memoria,b'x'*256,ProvedoresReinicio())
        self.assertEqual(state.final(),before)
        number9=Estado(imagem_reinicio(2,number=9),2);before9=number9.final()
        from nome_missao import DependenciaNomeMissao
        with self.assertRaises(DependenciaNomeMissao):
            resetar_para_missao(number9.memoria,b'\0',ProvedoresReinicio())
        self.assertEqual(number9.final(),before9)
        called=[]
        providers=ProvedoresReinicio(terreno=lambda:called.append('terrain'))
        with self.assertRaises(DependenciaReinicio) as error:
            resetar_para_missao(state.memoria,b'C:\0',providers)
        self.assertEqual((error.exception.rotina,error.exception.chamada,called),('MiniMapReset',0x46c364,['terrain']))
        self.assertEqual(bytes(state.memoria.contadores),b'\xff'*4)

    def test_mission_load_name_extension_and_network_branches(self):
        for network,expected in ((0,'Engin_ResetExperience'),(1,'RechercheCheat')):
            state=Estado(imagem_reinicio(7,network=network),7)
            providers=ProvedoresReinicio(tecnologia=state.tecnologia,pesquisa=lambda:None,
                                         experiencia=(lambda:None) if network else None)
            with self.assertRaises(DependenciaReinicio) as error:
                continuar_reinicio_missao_nome(state.memoria,state.extra,b'X.NET\0',state.diretorios(),providers)
            self.assertEqual(error.exception.rotina,expected)
        state=Estado(imagem_reinicio(8,directory=b'C:',directory_net=b'N:'),8)
        everything=ProvedoresReinicio(tecnologia=state.tecnologia,pesquisa=lambda:None,experiencia=lambda:None)
        for name,path in ((b'a.NeT',b'N:\\WORLD\\a.NeT'),(b'MONDE01.ETA',b'C:\\WORLD\\MONDE01.ETA')):
            self.assertEqual(continuar_reinicio_missao_nome(state.memoria,state.extra,name+b'\0',state.diretorios(),everything).caminho,path)
        with self.assertRaises(ForaDoDominioReinicio):
            continuar_reinicio_missao_nome(state.memoria,state.extra,b'abc\0',state.diretorios(),everything)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional intact-x86: RISING_EMULAR=1')
class DiferencialReinicio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_reinicio_missao import BancadaReinicioMissao
        cls.native=BancadaReinicioMissao()

    def compare(self,kind,image,seed,case,players=(0,0,0)):
        native=self.native;units,bags,projectiles=pools(seed)
        native.carregar(image,units,bags,projectiles,jogadores_sinteticos(players))
        if kind in ('IconeReset','MessageBoxInit','BallonInit'):
            regs,native_extra=native.folha(kind),{}
        elif kind=='MissionLoad_prefix':
            regs,native_extra=native.prefixo('MissionLoad',number=case['number'])
        elif kind=='MissionLoad_tail':
            regs,native_extra=native.continuacao('MissionLoad',path=case['path'].encode('latin-1'))
        elif kind=='MissionLoadName_prefix':
            regs,native_extra=native.prefixo('MissionLoadName',name=case['name'].encode('latin-1'))
        else:
            regs,native_extra=native.continuacao('MissionLoadName',name=case['name'].encode('latin-1'))
        state=Estado(image,seed,players);extra,error=executar(kind,state,case)
        if kind in EXPECTED_STOP:
            self.assertEqual(error.chamada,regs['EIP'])
        mine,theirs=state.final(),native.estado()
        for key in theirs:
            if mine[key]!=theirs[key]:
                self.fail(f'{kind} {key} differs')
        self.assertEqual({k:bytes(v) for k,v in extra.items()},native_extra)

    def test_leaf_resets_fresh_patterns(self):
        rng=random.Random(3)
        for index,icons in enumerate(casos_folhas()+[rng.randbytes(60) for _ in range(8)]):
            for flag in (0,1,2,255):
                image=imagem_reinicio(600+index,icons=icons);image[0x4e05a2-DATA_BASE]=flag
                self.compare('IconeReset',image,index,{})
        for seed in range(6):
            for kind in ('MessageBoxInit','BallonInit'):
                self.compare(kind,imagem_reinicio(700+seed),seed,{})

    def test_mission_load_prefix_all_numbers_and_variants(self):
        for number in range(256):
            for variant in ((0,1,2,3) if number==9 else (0,)):
                values=((127,90,-128 & 255),(90,90,90),(0,200,100))[number%3] if number in (10,12,17) else (0,0,0)
                directory=(b'',b'C:\\RISING',b'Z:'+b'\\y'*110)[number%3]
                case=dict(number=number,variant=variant)
                self.compare('MissionLoad_prefix',imagem_reinicio(800+number,number=number,variant=variant,directory=directory),
                             number,case,values)

    def test_tails_and_mission_load_name_prefixes(self):
        for seed,path in enumerate((b'\\World\\Monde01.ETA',b'X'*254,b'',b'C:\\a\\World\\Monde09b.ETA')):
            self.compare('MissionLoad_tail',imagem_reinicio(900+seed),seed,dict(path=path.decode('latin-1')))
        for seed,name in enumerate((b'MONDE01.ETA',b'p.NET',b'SAVE.nEt',b'ab',b'Y'*200)):
            self.compare('MissionLoadName_prefix',imagem_reinicio(950+seed),seed,dict(name=name.decode('latin-1')))
            for network in (0,1,7):
                self.compare('MissionLoadName_tail',imagem_reinicio(960+seed*3+network%3,network=network),seed,
                             dict(name=name.decode('latin-1'),network=network))


if __name__=='__main__':
    unittest.main()
