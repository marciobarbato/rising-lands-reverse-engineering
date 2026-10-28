"""Bancada própria v5: MissionLoad parcial, dois passes e NextAnimVeget."""
import hashlib
import json
import struct
import time
from bancada_x86 import SUPERFICIE, unicorn
from validar_composicao import BancadaComposicao
from extrair_evidencias import RAIZ, COMMIT, HASH_EXE, exigir_area_editavel
from graficos import Catalogo, ORDEM
from objetos import consultar_objeto, compor_passe, visibilidade, avancar_arvore, ler_objetos_eta, CODIGOS


def sha(d):return hashlib.sha256(d).hexdigest()


class BancadaObjetos(BancadaComposicao):
    def __init__(self):
        self.registrar=False;self.eventos=[]
        super().__init__();self.ptrs={}
        for n,g,t in [('atributos',0x507da8,0x10000),('terreno',0x507d70,0x20000),
                      ('objetos',0x507d74,0x10000),('auxiliares',0x507dac,0x10000),
                      ('descoberta',0x507d78,0x10000),('iluminacao',0x507d88,0x10000)]:
            p=self.alocar(t);self.ptrs[n]=p;self.escrever(g,struct.pack('<I',p));self.escrever(p,bytes(t))
        self.escrever(0x508041,b'\0')

    def _hook(self,cpu,a,n,data):
        if self.registrar and a in (0x45b247,0x45b796):
            i16=lambda v:(v+32768)%65536-32768
            self.eventos.append(dict(id_motor=self.reg('EBX')&65535,x=i16(self.reg('EAX')),
                y=i16(self.reg('EDX')),operacao='copiar' if a==0x45b247 else 'sombra'))
        super()._hook(cpu,a,n,data)

    def carregar_eta(self,eta):
        pos=4;reads=[]
        def ler(b):
            nonlocal pos
            n=b.reg('EDX');dest=b.reg('EAX');d=eta[pos:pos+n];assert len(d)==n
            b.escrever(dest,d);reads.append(dict(offset=pos,bytes=n,destino=hex(dest),sha256=sha(d)))
            pos+=n;b.retornar_stub()
        self.executar(0x46c3a2,[(0x46c3a2,0x46c3de)],paradas=[0x46c3de],stubs={0x458461:ler})
        assert pos==0x50004
        for k,o,n in [('atributos',4,65536),('terreno',0x10004,131072),('objetos',0x30004,65536),('auxiliares',0x40004,65536)]:
            assert self.ler(self.ptrs[k],n)==eta[o:o+n]
        return reads

    def desenhar(self,codigo,aux,d,l,passe,*,celula=0x0d11,x=64,y=108,pixels=False,recorte=(0,0,159,159),tabela=None):
        for n,v in [('objetos',codigo),('auxiliares',aux),('descoberta',d),('iluminacao',l)]:self.escrever(self.ptrs[n]+celula,bytes([v]))
        intervalos=[(0x410085,0x41068e),(0x415acf,0x416864),(0x410b38,0x410b40),
                    (0x4766f0,0x47670a),(0x47693a,0x476951),(0x4766d6,0x4766f0)]
        stubs={a:lambda b:b.retornar_stub() for a in (0x45b247,0x45b796)}
        if pixels:
            fundo=bytes((i*17+23)%256 for i in range(160*160))
            self.preparar_superficie(160,160,fundo,recorte,tabela)
            intervalos += [(0x45b247,0x45b4fd)]+self.intervalos_sombra();stubs={}
        self.eventos=[];self.registrar=True
        self.executar(0x410085 if passe=='terreno' else 0x415acf,intervalos,
            {'EAX':x,'EDX':y,'EBX':celula},stubs=stubs,limite=1000000)
        self.registrar=False
        return self.eventos,self.ler(SUPERFICIE,160*160) if pixels else None

    def animar(self,codigo,fase,relogio,cursor,tabela,*,celula=0x0d11):
        self.escrever(self.ptrs['objetos']+celula,bytes([codigo]));self.escrever(self.ptrs['auxiliares']+celula,bytes([fase]))
        self.escrever(0x508f7c,struct.pack('<I',relogio));self.escrever(0x4e1d18,bytes([cursor]))
        self.escrever(0x4e1c18,bytes(tabela));self.escrever(0x508724,struct.pack('<HH',1,1))
        self.executar(0x4772ec,[(0x4772ec,0x4774fa),(0x475bf8,0x475bfe)],{'EAX':celula%256,'EDX':celula//256})
        assert self.ler(self.ptrs['objetos']+celula,1)==bytes([codigo])
        return dict(fase=self.ler(self.ptrs['auxiliares']+celula,1)[0],indice=self.ler(0x4e1d18,1)[0],consumiu=self.ler(0x4e1d18,1)[0]!=cursor)


def eventos(plano,passe,x=64,y=108):
    return [dict(id_motor=q['id_motor'],x=x+q['x'],y=y+q['y'],operacao=q['operacao']) for q in plano[passe]]


def validar():
    exigir_area_editavel();inicio=time.monotonic();b=BancadaObjetos();c=Catalogo()
    r=dict(commit_snapshot=COMMIT,commit_predecessor='46e826c7c112a2ddda4376d8587500cc7e742f68',
        exe_sha256=HASH_EXE,unicorn=unicorn.__version__,
        limites=dict(instrucoes_maximo=1000000,microssegundos=2000000),
        substituicoes=dict(leitura_ETA=['FileRead em memória; parada em 0x46c3de antes de pós-processamento'],
            capturas=['PasteBobCmp e PasteOmbreCmp capturados'],pixels=[],visibilidade=[],animacao=[],
            bancos=['IO e alocação em memória']),condicoes=['Objetos 1..22 e 28..52, árvores em fase 0..3; efeitos de outros objetos fora do contrato',
            'Tabela de sombra original v3, percentual 60/ciclos vazios como entradas declaradas',
            'Dois passes completos até retorno; nenhuma ordem global da cena presumida'])
    eta=c._ler('cd/WORLD/MONDE01.ETA');r['leituras_ETA']=b.carregar_eta(eta);r['eta']=ler_objetos_eta(eta)
    r['flags']=[]
    for v in range(256):
        for campo in ['descoberta','iluminacao']:
            b.escrever(b.ptrs[campo]+0x0d11,bytes([v]))
            a,z=(0x4766f0,0x47670a) if campo=='descoberta' else (0x47693a,0x476951)
            out=b.executar(a,[(a,z),(0x4766e8,0x4766f0)],{'EAX':0x0d11,'EDX':0})['EAX']&255
            expected=visibilidade(v if campo=='descoberta' else 0,v if campo=='iluminacao' else 0)
            assert out==expected['descoberto' if campo=='descoberta' else 'iluminado']
            r['flags'].append([campo,v,out])
    r['capturas']=[]
    for codigo in CODIGOS:
        for aux in (range(4) if codigo<=11 else (0,1,3,128,255)):
            for d,l in ((0,0),(0,16),(16,0)):
                plano=consultar_objeto(codigo,auxiliar_u8=aux,descoberta_u8=d,iluminacao_u8=l)
                for passe in ('terreno','sprites'):
                    ev,_=b.desenhar(codigo,aux,d,l,passe)
                    assert ev==eventos(plano,passe),(codigo,aux,d,l,passe,ev,eventos(plano,passe))
                    r['capturas'].append(dict(codigo=codigo,auxiliar=aux,descoberta=d,iluminacao=l,passe=passe,camadas=ev))
    print('Associações:',len(r['capturas']),'e 512 testes de flags conferidos',flush=True)
    r['animacao']=[];tab=bytes(range(256))
    for clock in range(4):
        for cursor in range(256):
            for fase in range(4):
                codigo=1+cursor%11
                out=b.animar(codigo,fase,clock,cursor,tab)
                expected=avancar_arvore(fase_u8=fase,relogio_u32=clock,indice_aleatorio_u8=cursor,tabela_aleatoria=tab)
                assert out==expected
                r['animacao'].append([codigo,fase,clock,cursor,out['fase'],out['indice']])
    # Fase bruta e overflow u8 no ramo que efetivamente incrementa.
    r['animacao_bruta']=[]
    for fase in range(256):
        out=b.animar(1,fase,0xfffffffc,255,bytes(256))
        assert out==avancar_arvore(fase_u8=fase,relogio_u32=0xfffffffc,indice_aleatorio_u8=255,tabela_aleatoria=bytes(256))
        r['animacao_bruta'].append([fase,out['fase'],out['indice']])
    r['objetos_estaticos']=[]
    for codigo in [v for v in CODIGOS if v>11]:
        out=b.animar(codigo,3,0,255,bytes(256));assert (out['fase'],out['indice'])==(3,255)
        r['objetos_estaticos'].append(codigo)
    r['varreduras']=[]
    for clock in (4,5):
        celulas=[(30+y)*256+20+x for y in range(2) for x in range(3)]
        codigos=[1,12,4,22,6,11];fases=[0,99,3,255,2,1];cursor=252
        for cell,co,fa in zip(celulas,codigos,fases):
            b.escrever(b.ptrs['objetos']+cell,bytes([co]));b.escrever(b.ptrs['auxiliares']+cell,bytes([fa]))
        antes_obj=b.ler(b.ptrs['objetos'],65536);antes_aux=b.ler(b.ptrs['auxiliares'],65536)
        b.escrever(0x508f7c,struct.pack('<I',clock));b.escrever(0x4e1d18,bytes([cursor]))
        b.escrever(0x4e1c18,bytes(range(256)));b.escrever(0x508724,struct.pack('<HH',3,2))
        b.executar(0x4772ec,[(0x4772ec,0x4774fa),(0x475bf8,0x475bfe)],{'EAX':20,'EDX':30})
        esperado=bytearray(antes_aux)
        for cell,co,fa in zip(celulas,codigos,fases):
            if co<=11:
                passo=avancar_arvore(fase_u8=fa,relogio_u32=clock,indice_aleatorio_u8=cursor,tabela_aleatoria=bytes(range(256)))
                esperado[cell]=passo['fase'];cursor=passo['indice']
        assert b.ler(b.ptrs['objetos'],65536)==antes_obj
        assert b.ler(b.ptrs['auxiliares'],65536)==bytes(esperado)
        assert b.ler(0x4e1d18,1)==bytes([cursor])
        r['varreduras'].append(dict(origem=[20,30],dimensoes=[3,2],relogio=clock,cursor_inicial=252,cursor_final=cursor,
            codigos=codigos,fases_iniciais=fases,fases_finais=[esperado[i] for i in celulas],fora_da_janela_inalterado=True))
    print('Avanço: 4096 estados e 256 fases brutas conferidos',flush=True)
    b.carregar_banco_original({n:c._ler('cd/INSTALHD/GRAPHICS/'+n) for n in ORDEM})
    tab=bytes(json.loads((RAIZ/'validacao/x86-composicao.json').read_text())['tabelas_sombra'][1]['indices'])
    r['tabela_sombra']=list(tab);r['pixels']=[];fundo=bytes((i*17+23)%256 for i in range(160*160))
    cases=[]
    for codigo in CODIGOS:
        for aux in (range(4) if codigo<=11 else (0,)):
            for l in (0,16):cases.append((codigo,aux,0,l,64,108,(0,0,159,159)))
    for codigo in (1,4,5,9,10,12,17,22,29,40,52):
        for x,y,rec in [(0,0,(0,0,159,159)),(150,150,(0,0,159,159)),(64,108,(70,80,83,101))]:
            cases.append((codigo,3,0,0,x,y,rec))
    for codigo,aux,d,l,x,y,rec in cases:
        passe='sprites' if codigo<=11 else 'terreno'
        plano=consultar_objeto(codigo,auxiliar_u8=aux,descoberta_u8=d,iluminacao_u8=l)
        ev,out=b.desenhar(codigo,aux,d,l,passe,x=x,y=y,pixels=True,recorte=rec,tabela=tab)
        assert ev==eventos(plano,passe,x,y)
        assert out==compor_passe(c,fundo,160,160,plano,passe,x,y,tabela_sombra=tab,recorte=rec),(codigo,aux,l,x,y)
        r['pixels'].append(dict(codigo=codigo,auxiliar=aux,descoberta=d,iluminacao=l,passe=passe,x=x,y=y,recorte=rec,sha256=sha(out)))
    r.update(resultado='PASSOU',execucoes_delimitadas=b.execucoes,instrucoes=b.instrucoes,duracao_segundos=round(time.monotonic()-inicio,3))
    (RAIZ/'validacao/x86-objetos.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print('PASSOU',len(r['pixels']),'superfícies;',b.execucoes,'execuções',flush=True)


if __name__=='__main__':validar()
