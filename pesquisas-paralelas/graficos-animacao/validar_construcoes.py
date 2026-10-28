"""V4: trecho gráfico do Santuário, leitura ETA e associação de terreno originais."""
import hashlib
import json
import struct
import time
from graficos import Catalogo, ORDEM
from construcoes import *
from bancada_x86 import Bancada, UNIDADE, SUPERFICIE, unicorn
from extrair_evidencias import RAIZ, COMMIT, HASH_EXE, imagem_pe, exigir_area_editavel


def sha(d):return hashlib.sha256(d).hexdigest()


class BancadaConstrucoes(Bancada):
    def __init__(self):
        self.eventos=[];self.registrar=False
        super().__init__()

    def _hook(self,cpu,a,n,data):
        if self.registrar and a in (0x45b247,0x45c455):
            def i16(v):return (v+32768)%65536-32768
            self.eventos.append(dict(id_motor=self.reg('EBX')&65535,x=i16(self.reg('EAX')),
                y=i16(self.reg('EDX')),operacao='jogador' if a==0x45c455 else 'copiar',
                jogador=self.ler(self.reg('ESP')+4,1)[0] if a==0x45c455 else None))
        super()._hook(cpu,a,n,data)

    def preparar_mundo(self,c):
        eta=c._ler('cd/WORLD/MONDE01.ETA');self.eta=eta
        self.ptrs={}
        for nome,globalptr,tam in [('terreno',0x507d70,0x20000),('objetos',0x507d74,0x10000),
                ('colisao',0x507da8,0x10000),('ocupacao',0x4e0f38,0x20000),('descoberta',0x507d78,0x10000)]:
            p=self.alocar(tam);self.ptrs[nome]=p;self.escrever(globalptr,struct.pack('<I',p))
            self.escrever(p,bytes(tam))
        self.escrever(self.ptrs['terreno'],eta[0x10004:0x30004])
        self.escrever(self.ptrs['objetos'],eta[0x30004:0x40004])
        self.escrever(0x508041,b'\0')
        self.escrever(0x49a0c8,bytes(276))
        self.escrever(UNIDADE,bytes(0x40000))
        n,t=struct.unpack_from('<HH',eta,0x50030);assert (n,t)==(1,204)
        bloco=eta[0x50030:0x50034+n*(t+2)];pos=0;leituras=[]
        def ler(b):
            nonlocal pos
            n=b.reg('EDX');d=bloco[pos:pos+n];assert len(d)==n
            b.escrever(b.reg('EAX'),d);leituras.append(dict(n=n,destino=hex(b.reg('EAX'))))
            pos+=n;b.retornar_stub()
        self.executar(0x46c517,[(0x46c517,0x46c578)],paradas=[0x46c578],stubs={0x458461:ler})
        assert pos==len(bloco)
        self.registro=ler_estruturas_eta(eta)[0]
        assert self.ler(0x49a0c8,204)==self.registro['bytes']
        # Unidades são somente dependências da consulta de habitação. Os últimos
        # quatro bytes não vêm da recomposição; permanecem zero, e não são lidos.
        p=0x50034+206;n,t=struct.unpack_from('<HH',eta,p);p+=4;assert t==784
        for _ in range(n):
            idx=struct.unpack_from('<H',eta,p)[0];raw=eta[p+2:p+2+t]
            self.escrever(UNIDADE+idx*276,raw[:140]+raw[652:]);p+=t+2
        r=self.executar(0x41a5b8,[(0x41a5b8,0x41a61c),(0x44724a,0x4472d3)],{'EAX':0})
        assert r['EAX']&255==1
        # PlaceBatiment → BatimentModifyTerrain → Chemin_ModifieZone originais.
        # MurAjoute atualiza cache de conectividade; não é consultado por AffBatiments.
        self.executar(0x41c4ac,[(0x41c4ac,0x41c652),(0x41ba49,0x41bb8a),
            (0x476251,0x476263),(0x47622e,0x47623e),(0x43e138,0x43e2a3),
            (0x41db1e,0x41db24),(0x41fd56,0x41fd5e)],{'EAX':0},
            stubs={0x43e616:lambda b:b.retornar_stub()})
        return leituras

    def paletas_jogador(self):
        pts=[]
        for i in range(5):
            p=self.alocar(256);pts.append(p);self.escrever(0x4e24c8+i*4,struct.pack('<I',p))
        self.executar(0x45ff61,[(0x45ff61,0x46003b),(0x45fdd9,0x45fddf)],{'EAX':0,'EDX':4})
        return tuple(self.ler(p,256) for p in pts)

    def desenhar(self,*,relogios=(0,0,0),jogador=0,x=224,y=160,celula=0x0d11,
                  quadro_terreno=None,descoberta=0,ocupacao=None,com_pixels=False,recorte=(0,0,319,319)):
        for ptr,v in zip((0x508f7c,0x508f80,0x508f84),relogios):self.escrever(ptr,struct.pack('<I',v))
        self.escrever(0x49a0c8+4,bytes([jogador]))
        # Cenário de visibilidade declarado, dono igual ao jogador da câmera.
        self.escrever(0x508041,bytes([jogador]))
        self.escrever(0x507d78+jogador*4,struct.pack('<I',self.ptrs['descoberta']))
        self.escrever(self.ptrs['descoberta']+celula,bytes([descoberta]))
        old_t=self.ler(self.ptrs['terreno']+celula*2,2);old_o=self.ler(self.ptrs['ocupacao']+celula*2,2)
        if quadro_terreno is not None:self.escrever(self.ptrs['terreno']+celula*2,struct.pack('<H',quadro_terreno))
        if ocupacao is not None:self.escrever(self.ptrs['ocupacao']+celula*2,struct.pack('<H',ocupacao))
        self.escrever(0x508724,struct.pack('<HH',10,10))
        l,t,r,bt=recorte;self.escrever(0x49a01c,struct.pack('<4H',t,bt,l,r))
        self.escrever(0x508f70,struct.pack('<I',SUPERFICIE));self.escrever(0x4e17a0,struct.pack('<I',320))
        fundo=bytes((i*17+23)%256 for i in range(320*320));self.escrever(SUPERFICIE,fundo)
        self.eventos=[];self.registrar=True
        def player(b):b.retornar_stub();b.reg('ESP',b.reg('ESP')+4)
        intervalos=[(0x407dd3,0x40f49c),(0x41a6ec,0x41a70b),(0x41a08c,0x41a0ab),
            (0x4766d6,0x4766f0),(0x40f4b7,0x40f4e8),(0x41a8e5,0x41a940),
            (0x41a5b8,0x41a61c),(0x44724a,0x4472d3)]
        stubs={0x45b247:lambda b:b.retornar_stub(),0x45c455:player}
        if com_pixels:
            stubs={};intervalos += [(0x45b247,0x45b4fd),(0x45c455,0x45c72a),
                                   (0x45f850,0x45f871),(0x45cd8b,0x45cd91)]
        self.executar(0x407dd3,intervalos,{'EAX':x,'EDX':y,'EBX':celula},
                      paradas=[0x40f342],stubs=stubs,limite=1000000)
        self.registrar=False;self.escrever(self.ptrs['terreno']+celula*2,old_t)
        self.escrever(self.ptrs['ocupacao']+celula*2,old_o)
        return self.eventos,self.ler(SUPERFICIE,320*320)


def validar():
    exigir_area_editavel();inicio=time.monotonic();b=BancadaConstrucoes();c=Catalogo()
    report=dict(commit_snapshot=COMMIT,commit_predecessor='b67215a3870d17a51b063cb9d82ea391c1852f56',
        exe_sha256=HASH_EXE,unicorn=unicorn.__version__,
        limites=dict(instrucoes_por_execucao_maximo=1000000,microssegundos_por_execucao=2000000),
        substituicoes=dict(leitura_ETA=['FileRead em memória'],
            colocacao=['MurAjoute 0x43e616: cache de conectividade não consultado pelo renderizador'],
            captura=['PasteBobCmp/PastePlayerCmp capturados; pilha do argumento de jogador respeitada'],
            pixels=[],paletas=[],relogios=[],habitacao=[]))
    report['leituras_ETA']=b.preparar_mundo(c)
    report['registro_ETA']={k:v for k,v in b.registro.items() if k!='bytes'}
    report['registro_ETA']['habitado_original']=True
    base,im=imagem_pe();mask=im[0x495c30-base:0x495c30-base+30]
    report['colocacao']=[]
    ordinal=0
    for y in range(5):
        for x in range(6):
            cell=(11+y)*256+12+x;ter=struct.unpack('<H',b.ler(b.ptrs['terreno']+cell*2,2))[0]
            occ=struct.unpack('<H',b.ler(b.ptrs['ocupacao']+cell*2,2))[0]
            assert ter==732+y*6+x
            assert occ==(0x8000+ordinal if mask[y*6+x] else 0)
            if mask[y*6+x]:ordinal+=1
            report['colocacao'].append(dict(x=x,y=y,celula=cell,id_terreno=ter,ocupacao=occ))
    assert b.ler(b.ptrs['terreno'],0x20000)==b.eta[0x10004:0x30004]
    tabs=b.paletas_jogador();assert tabs==tabelas_jogador()
    report['tabelas_jogador']=[list(t) for t in tabs]
    report['capturas']=[]
    for a in range(8):
        for bb in range(8):
            for cc in range(8):
                rel=(a,bb,cc);ev,_=b.desenhar(relogios=rel)
                plano=consultar_santuario(habitado=True,jogador=0,relogios=rel,celula_mapa=(17,13))
                esp=[dict(id_motor=q['id_motor'],x=224+q['x'],y=160+q['y'],
                          operacao=q['operacao'],jogador=q['jogador']) for q in plano['camadas']]
                assert ev==esp,(rel,ev,esp)
                report['capturas'].append(dict(relogios=rel,camadas=ev))
    report['variacoes_celula_jogador']=[]
    for cell in [y*256+x for y in (13,201) for x in range(16,24)]:
        for jogador in range(5):
            for rel in [(0,0,0),(0xffffffff,0x12345678,0xfffffff7)]:
                ev,_=b.desenhar(relogios=rel,jogador=jogador,celula=cell,quadro_terreno=749,ocupacao=0x800f)
                plano=consultar_santuario(habitado=True,jogador=jogador,relogios=rel,celula_mapa=(cell%256,cell//256))
                esp=[dict(id_motor=q['id_motor'],x=224+q['x'],y=160+q['y'],
                          operacao=q['operacao'],jogador=q['jogador']) for q in plano['camadas']]
                assert ev==esp,(cell,jogador,rel,ev,esp)
                report['variacoes_celula_jogador'].append(dict(celula=cell,jogador=jogador,relogios=rel,camadas=ev))
    print('512 combinações de relógios e 5 tabelas de jogador conferidas',flush=True)
    report['gates']=[]
    for nome,kw in [('terreno_incorreto',dict(quadro_terreno=0x2ec)),
                    ('sem_ocupacao',dict(ocupacao=0)),('nao_descoberta',dict(descoberta=16))]:
        ev,_=b.desenhar(**kw);assert not ev
        report['gates'].append(dict(caso=nome,argumentos=kw,camadas=ev))
    # Restaurar descoberta após o caso negativo.
    b.escrever(b.ptrs['descoberta']+0x0d11,b'\0')
    report['relogios']=[]
    for rel in [(a,0xffffffff-a,0xffffff00+a) for a in range(256)]+[(0xffffffff,0xffffffff,0xffffffff),(0xfffffffe,7,9)]:
        for p,v in zip((0x508f7c,0x508f80,0x508f84),rel):b.escrever(p,struct.pack('<I',v))
        b.executar(0x47500e,[(0x47500e,0x475041)],paradas=[0x475041])
        out=tuple(struct.unpack('<I',b.ler(p,4))[0] for p in (0x508f7c,0x508f80,0x508f84))
        assert out==avancar_relogios(rel);report['relogios'].append(dict(entrada=rel,saida=out))
    b.carregar_banco_original({n:c._ler('cd/INSTALHD/GRAPHICS/'+n) for n in ORDEM})
    report['pixels']=[];fundo=bytes((i*17+23)%256 for i in range(320*320))
    for jogador in range(5):
        for t in range(48):
            rel=(t,t//2,t//3);ev,out=b.desenhar(relogios=rel,jogador=jogador,com_pixels=True)
            plano=consultar_santuario(habitado=True,jogador=jogador,relogios=rel,celula_mapa=(17,13))
            assert out==compor_fachada(c,fundo,320,320,plano,224,160,tabelas=tabs),(jogador,t)
            report['pixels'].append(dict(jogador=jogador,relogios=rel,x=224,y=160,recorte=[0,0,319,319],sha256=sha(out)))
        print('Pixels conferidos para jogador',jogador,flush=True)
    for x,y,rec in [(20,30,(0,0,319,319)),(310,310,(0,0,319,319)),
                    (224,160,(80,100,165,205)),(224,160,(100,100,100,100))]:
        rel=(7,5,3);ev,out=b.desenhar(relogios=rel,x=x,y=y,recorte=rec,com_pixels=True)
        plano=consultar_santuario(habitado=True,jogador=0,relogios=rel,celula_mapa=(17,13))
        assert out==compor_fachada(c,fundo,320,320,plano,x,y,tabelas=tabs,recorte=rec)
        report['pixels'].append(dict(jogador=0,relogios=rel,x=x,y=y,recorte=rec,sha256=sha(out)))
    report.update(resultado='PASSOU',execucoes_delimitadas=b.execucoes,instrucoes_observadas=b.instrucoes,
        duracao_segundos=round(time.monotonic()-inicio,3),limites_de_conclusao=[
        'Somente fachada habitada, modo 5, +0x06=0; parada antes de 0x40f342 (fogo/seleção/barras fora do contrato).',
        'Leitura parcial de estruturas do ETA e unidades recompostas como entrada de BagContientTroupe; não emula carregamento inteiro.',
        'PlaceBatiment original com apenas MurAjoute substituído; ocupação e terreno escritos pelas funções originais.',
        'Relógios globais por chamada de ProgIteration; nenhuma frequência original em segundos afirmada.',
        'Tipos restantes, habitação falsa, modos 0..4 e ancoragem global da cena permanecem fora do adaptador.'])
    (RAIZ/'validacao/x86-construcoes.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASSOU:',len(report['pixels']),'superfícies;',b.execucoes,'execuções',flush=True)


if __name__=='__main__':validar()
