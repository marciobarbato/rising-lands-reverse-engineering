"""Comparações v3 com código x86 original e limites por segmento de execução."""
import hashlib
import json
import struct
import time
from bancada_x86 import Bancada, UNIDADE, SUPERFICIE, RETORNO, unicorn
from extrair_evidencias import RAIZ, COMMIT, HASH_EXE, exigir_area_editavel
from graficos import Catalogo, ORDEM, TIPOS, ler_paleta, ler_cmp
from composicao import encaminhamento, ROTINAS, tabela_sombra, compor_sombra, compor_unidade, SOMBRA_ID


def sha(dados):
    return hashlib.sha256(dados).hexdigest()


class BancadaComposicao(Bancada):
    def retomar(self, paradas, limite=100000):
        if not 1 <= limite <= 1000000:
            raise ValueError('Limite de instruções inválido')
        self.execucoes += 1
        self.paradas = set(paradas)|{RETORNO}
        self.cpu.emu_start(self.reg('EIP'),RETORNO,timeout=2_000_000,count=limite)
        if self.reg('EIP') not in self.paradas:
            raise RuntimeError('Limite excedido ao retomar segmento')

    def carregar_paleta(self, dados):
        pos = 0
        def abrir(b):
            nonlocal pos
            pos = 0; b.retornar_stub(1)
        def ler(b):
            nonlocal pos
            n = b.reg('EDX'); trecho = dados[pos:pos+n]
            assert len(trecho) == n
            b.escrever(b.reg('EAX'),trecho); pos += n; b.retornar_stub()
        def seek(b):
            nonlocal pos
            assert (b.reg('EAX'),b.reg('EDX')) == (4,1)
            pos += 4; b.retornar_stub()
        p = self.alocar(768)
        r = self.executar(0x4798e9,[(0x4798e9,0x4799c4)],{'EAX':0,'EDX':p},
            stubs={0x458420:abrir,0x458461:ler,0x45848b:seek,0x45844c:lambda b:b.retornar_stub()})
        assert r['EAX'] & 255 == 1
        rgb = self.ler(p,768)
        r = self.executar(0x43ee31,[(0x43ee31,0x43ee8d)],{'EAX':p},paradas=[0x43ee8d])
        entries = self.ler(r['ESP'],1024)
        rgb_dd = b''.join(entries[i:i+3] for i in range(0,1024,4))
        assert rgb == rgb_dd  # somente preparo, sem executar COM/DirectDraw
        return rgb

    def calcular_sombra(self, paleta, percentual, ciclos):
        p = self.alocar(768); t = self.alocar(256)
        self.escrever(p,paleta); self.escrever(0x4e24b4,struct.pack('<I',t))
        self.escrever(0x4e24e1,bytes([len(ciclos)]))
        self.escrever(0x4e24e4,b''.join(bytes([a,z,0]) for a,z in ciclos))
        self.executar(0x45f940,[(0x45f940,0x45fafc),(0x4795af,0x479610)],
                      {'EAX':p,'EDX':percentual},paradas=[0x45fa47])
        # Cada cor é um segmento limitado, preservando CPU/pilha entre eles.
        # Todos os 256 incrementos e o epílogo são executados, sem atalhos.
        for _ in range(256):
            self.retomar([0x45fa46])
            self.retomar([0x45fa47])
        self.retomar([])
        return self.ler(t,256)

    def preparar_superficie(self,w,h,fundo,recorte,tabela):
        self.escrever(SUPERFICIE,fundo)
        self.escrever(0x508f70,struct.pack('<I',SUPERFICIE))
        self.escrever(0x4e17a0,struct.pack('<I',w))
        l,t,r,b = recorte
        self.escrever(0x49a01c,struct.pack('<4H',t,b,l,r))
        p = self.alocar(256); self.escrever(p,tabela)
        self.escrever(0x4e24b4,struct.pack('<I',p))

    @staticmethod
    def intervalos_sombra():
        return [(0x45b796,0x45ba23),(0x45b4f6,0x45b4fd),
                (0x45f7ba,0x45f7d8),(0x45f6de,0x45f6e1)]


def validar():
    exigir_area_editavel(); inicio=time.monotonic(); b=BancadaComposicao(); c=Catalogo()
    report=dict(commit_snapshot=COMMIT,commit_anterior='0c76b34a017c185ab24344137a1cb52266b599d2',
        exe_sha256=HASH_EXE,unicorn=unicorn.__version__,
        limites=dict(instrucoes_por_segmento_maximo=1000000,microssegundos_por_segmento=2000000,
                     segmentos_por_tabela_sombra=514),
        substituicoes={'LoadPalette':['IO em memória'], 'DDSetPalette':['parada antes de COM'],
            'AffEngin_despacho':['parada na entrada dos handlers, que não são executados'],
            'CalculOmbrage':[], 'PasteOmbreCmp':[], 'AffEngin_composicao':[],
            'LoadSTRATBank':['IO e alocação em memória']})
    pie=c._ler('cd/INSTALHD/PLATGAME.PIE'); pal=b.carregar_paleta(pie)
    assert pal == ler_paleta(pie)
    sintetico=bytearray(pie[:777]);sintetico[9:777]=bytes(i%256 for i in range(768))
    assert b.carregar_paleta(sintetico)==ler_paleta(sintetico)
    report['paleta']=dict(sha256=sha(pal),rgb_hex=pal.hex(),cores=256,
        componentes_divergentes_da_v2=sum(a!=z for a,z in zip(pal,bytes(4*(v&63)+3 if v&63 else 0 for v in pie[9:777]))),
        casos=['PLATGAME.PIE','sintético com todos os valores u8 e entrada 0 não preta'],
        preparo_DirectDraw_igual=True,DirectDraw_executado=False)
    print('Paleta original e preparo RGB de DirectDraw conferidos',flush=True)
    report['despachos']=[]
    destinos={a:n for n,a in ROTINAS.items() if a};destinos[RETORNO]='sem_desenho'
    for tipo in TIPOS:
        init=bytearray(b.inicializar_tipo(tipo))
        for estado in range(256):
            for aux in (range(256) if estado in (1,22,24) else [0]):
                u=bytearray(init);u[2]=estado;u[0x8a]=aux;b.escrever(UNIDADE,u)
                r=b.executar(0x41591f,[(0x41591f,0x415a57),(0x442025,0x442045)],
                    {'EAX':64,'EDX':64,'EBX':0},paradas=destinos)
                rota=destinos[r['EIP']]
                assert rota==encaminhamento(tipo,estado,auxiliar_8a=aux)['rota']
                assert b.ler(UNIDADE,276)==u
                report['despachos'].append([tipo,estado,aux,rota])
    print('Despachos conferidos:',len(report['despachos']),flush=True)
    report['tabelas_sombra']=[]
    for percentual,ciclos in [(0,()),(60,()),(100,()),(255,((0,15),(32,63),(200,210)))]:
        original=b.calcular_sombra(pal,percentual,ciclos)
        assert original==tabela_sombra(pal,percentual=percentual,ciclos=ciclos)
        report['tabelas_sombra'].append(dict(percentual=percentual,ciclos=ciclos,
                                            sha256=sha(original),indices=list(original)))
        print('Tabela de sombra conferida:',percentual,ciclos,flush=True)
    tabela=bytes(report['tabelas_sombra'][1]['indices'])
    carga=b.carregar_banco_original({n:c._ler('cd/INSTALHD/GRAPHICS/'+n) for n in ORDEM})
    report['sombras']=[];q=c.quadro(SOMBRA_ID);w=h=128
    casos=[(i,40,45,(0,0,127,127)) for i in range(256)]
    casos += [(None,x,y,rec) for x,y,rec in [
        (-q.largura,0,(0,0,127,127)),(-q.largura+1,4,(0,0,127,127)),
        (-3,-4,(0,0,127,127)),(127,127,(0,0,127,127)),(128,128,(0,0,127,127)),
        (32,48,(40,50,55,52)),(40,45,(42,48,42,48)),(0,0,(40,50,55,52)),
        (110,110,(0,0,127,127)),(40,45,(0,0,127,127))]]
    for indice,x,y,rec in casos:
        fundo=bytes([indice])*(w*h) if indice is not None else bytes((i*17+23)%256 for i in range(w*h))
        b.preparar_superficie(w,h,fundo,rec,tabela)
        b.executar(0x45b796,b.intervalos_sombra(),{'EAX':x,'EDX':y,'EBX':SOMBRA_ID,'ECX':1})
        original=b.ler(SUPERFICIE,w*h)
        assert original==compor_sombra(fundo,w,h,q,x,y,tabela,rec)
        report['sombras'].append(dict(fundo_indice=indice,x=x,y=y,recorte=rec,sha256=sha(original)))
    print('Blits de sombra conferidos:',len(report['sombras']),flush=True)
    raw=struct.pack('<HHHI',1,4,1,5)+bytes([1,254,0,255,1])
    sint=ler_cmp(raw)[0];ptr=b.alocar(12);dados=b.alocar(5)
    b.escrever(dados,sint.comprimido);b.escrever(ptr,struct.pack('<HHII',4,1,5,dados))
    b.escrever(carga['tabela'],struct.pack('<I',ptr))  # somente descritor em RAM emulada
    fundo=bytes([82])*(w*h)
    b.preparar_superficie(w,h,fundo,(0,0,127,127),tabela)
    b.executar(0x45b796,b.intervalos_sombra(),{'EAX':2,'EDX':3,'EBX':1,'ECX':1})
    original=b.ler(SUPERFICIE,w*h)
    assert original==compor_sombra(fundo,w,h,sint,2,3,tabela)
    assert original[3*w+2:3*w+6]==bytes([82,tabela[82],tabela[82],82])
    report['sombra_sintetica']=dict(literal_zero_opaco=True,cores_literais_ignoradas=True,
                                   saltos_transparentes=True,sha256=sha(original))
    report['composicoes']=[]
    # AffEngin até o retorno, incluindo sombra, corpo e testes de efeitos inativos.
    intervalos=[(0x41591f,0x415a57),(0x412390,0x41374c),(0x410fcc,0x41209d),
                (0x4470b9,0x4470c5),(0x442025,0x442065),(0x44fffe,0x45007a),
                (0x467d97,0x467da6),(0x45b247,0x45b4fd)]+b.intervalos_sombra()
    fundo=bytes((i*17+23)%256 for i in range(w*h));rec=(0,0,127,127)
    for tipo,spec in TIPOS.items():
        init=bytearray(b.inicializar_tipo(tipo))
        for bolsa in range(len(spec['bases'])):
            for d in range(1,17,2):
                for fase in range(8):
                    u=bytearray(init);u[2]=2;u[0x91]=d;u[0xa4]=fase
                    struct.pack_into('<H',u,0xa,bolsa)
                    # Desativa o indicador auxiliar em 0x413568..0x4135a4.
                    # Nenhuma regra de fadiga é simulada: condição de entrada explícita.
                    struct.pack_into('<H',u,0x74,100);b.escrever(UNIDADE,u)
                    b.preparar_superficie(w,h,fundo,rec,tabela)
                    b.executar(0x41591f,intervalos,{'EAX':64,'EDX':48,'EBX':0},limite=300000)
                    original=b.ler(SUPERFICIE,w*h)
                    esperado,plano=compor_unidade(c,fundo,w,h,tipo=tipo,estado_u8=2,direcao=d,
                        fase=fase,x=64,y=48,tabela=tabela,bolsa_u16=bolsa)
                    assert original==esperado,(tipo,bolsa,d,fase)
                    report['composicoes'].append(dict(tipo=tipo,bolsa_u16=bolsa,direcao=d,fase=fase,
                                                       sha256=sha(original),camadas=plano['camadas']))
    # Os oito registros de Colono no estado 14: bytes recompostos do ETA, sem init de tipo.
    eta=c._ler('cd/WORLD/MONDE01.ETA')
    exemplos=json.loads((RAIZ/'artefatos/exemplos-eta-unidades.json').read_text())
    report['eta_estado14']=[]
    for r in exemplos['registros']:
        if r['tipo']!=9 or r['estado_no_disco']!=14:continue
        p=r['offset_registro'];raw=eta[p:p+784];u=raw[:140]+raw[652:]
        assert len(u)==272  # a instância RAM tem 276; quatro bytes não vêm deste recorte
        b.escrever(UNIDADE,bytes(276));b.escrever(UNIDADE,u)
        antes=b.ler(UNIDADE,276);b.preparar_superficie(w,h,fundo,rec,tabela)
        b.executar(0x41591f,[(0x41591f,0x415a57)],{'EAX':64,'EDX':48,'EBX':0})
        assert b.ler(SUPERFICIE,w*h)==fundo and b.ler(UNIDADE,276)==antes
        report['eta_estado14'].append(dict(indice=r['indice'],offset=p,sha256_registro=sha(raw),
                                           resultado='retorno_sem_desenho',bytes_recompostos=272,
                                           cauda_ram='4 bytes zerados na bancada; não lidos pelo caminho'))
    assert len(report['eta_estado14'])==8
    report.update(resultado='PASSOU',segmentos_delimitados=b.execucoes,instrucoes_observadas=b.instrucoes,
                  duracao_segundos=round(time.monotonic()-inicio,3),
                  limites_de_conclusao=[
        'Percentual/ciclos explícitos. Literal 60 em ProgInit observado, preservação por toda inicialização não provada.',
        'Paleta inicial antes de ciclagem/efeitos; preparo de DirectDraw, sem executar Windows.',
        'Estado 14 retorna sem desenho em AffEngin. Não prova estado após carregador nem invisibilidade no jogo.',
        'Composição até retorno: jogador 0, estado 2, tipos 0/5/6/7/9, +0x74=100, +0xba=0 e efeitos inativos.',
        'Ataque/trabalho/construção/morte: somente despacho, handlers não executados nesta comparação.'])
    (RAIZ/'validacao/x86-composicao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASSOU:',len(report['composicoes']),'composições integrais;',b.execucoes,'segmentos',flush=True)


if __name__=='__main__':validar()
