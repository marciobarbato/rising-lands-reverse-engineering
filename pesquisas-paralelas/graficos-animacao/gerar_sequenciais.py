"""Tabelas, atlas e inspetor offline dos objetos 54/66/67/68."""
import base64
import csv
import hashlib
import json
from graficos import Catalogo, Quadro, localizar, RAIZ
from composicao import tabela_sombra
from objetos import compor_passe
from sequenciais import CODIGOS_SEQUENCIAIS, consultar_sequencial, ler_objetos_eta_v6
from gerar_artefatos import Raster
from gerar_objetos import fundo, referencia_rle
from extrair_evidencias import exigir_area_editavel


def gerar():
    exigir_area_editavel()
    c=Catalogo();pal=c.paleta();tab=tabela_sombra(pal,percentual=60,ciclos=())
    p=RAIZ/'artefatos';linhas=[];quadros={};planos=[];refs=[]
    for co in CODIGOS_SEQUENCIAIS:
        for aux in ((0,) if co==54 else range(32)):
            for d,l in ((0,0),(0,16),(16,0)):
                pl=consultar_sequencial(co,auxiliar_u8=aux,descoberta_u8=d,iluminacao_u8=l)
                planos.append(pl)
                if d:continue
                for ca in pl['terreno']:
                    mid=ca['id_motor'];q=c.quadro(mid)
                    quadros[mid]=dict(w=q.largura,h=q.altura,rle=base64.b64encode(q.comprimido).decode())
                    if co!=54 and aux%2:continue
                    linhas.append(dict(**localizar(mid),tipo_objeto=co,
                        classe_visual=pl['classe_visual'],classe_confianca='inferencia_visual',
                        estado='descoberto_iluminado' if l==0 else 'descoberto_sem_iluminacao',
                        direcao=None,passe='terreno',ordem=ca['ordem'],operacao=ca['operacao'],
                        fase=pl['fase'],auxiliares=[aux,aux+1] if co!=54 else 'u8 ignorado',
                        sequencia=ca['sequencia'],
                        ancoragem=dict(x=-ca['x'],y=-ca['y'],referencia='origem da célula de 32×32'),
                        periodo='sem avanço em NextAnimVeget; alterações do auxiliar são externas',
                        largura=q.largura,altura=q.altura,sha256_pixels=hashlib.sha256(q.pixels).hexdigest(),
                        sha256_opacidade=hashlib.sha256(q.opacidade).hexdigest(),
                        confianca=ca['confianca'],evidencia=ca['evidencia']))
                if co==54 or aux%2==0:
                    out=compor_passe(c,fundo(),160,160,pl,'terreno',64,108,tabela_sombra=tab)
                    refs.append(dict(codigo=co,auxiliar=aux,descoberta=d,iluminacao=l,
                        indices_rle=referencia_rle(out),sha256=hashlib.sha256(out).hexdigest()))
    (p/'associacoes-sequenciais.json').write_text(json.dumps(linhas,ensure_ascii=False,indent=2)+'\n')
    with (p/'associacoes-sequenciais.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=list(linhas[0]),lineterminator='\n');wr.writeheader()
        for row in linhas:wr.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()})
    atlas=Raster(1440,80+6*148)
    atlas.texto(20,18,'OBJETOS 66-68 | 16 QUADROS POR CODIGO | OTHERS.CMP',2)
    atlas.texto(20,49,'L/G BASE 0 | ID MOTOR BASE 1 | AUXILIAR = FASE X 2 OU FASE X 2 + 1',1)
    for i,mid in enumerate(sorted(quadros)):
        x=16+i%8*180;y=80+i//8*148;q=c.quadro(mid)
        atlas.sprite(x+12,y,q,pal,3)
        atlas.texto(x,y+98,f'ID {mid} / F{(mid-10823)%16}',1)
        atlas.texto(x,y+113,f'L{mid-7640} G{mid-1}',1)
        atlas.texto(x,y+128,f'{q.largura}X{q.altura}',1)
    atlas.salvar(p/'atlas-sequenciais.png')
    # Cada linha mostra os 16 estados de uma família, com as duas iluminações.
    contato=Raster(16*86+32,80+6*130)
    contato.texto(16,15,'SEQUENCIAS 66-68 | CLARO E SEM ILUMINACAO',2)
    contato.texto(16,47,'FUNDO SINTETICO | SOMBRA 60 POR CENTO / CICLOS VAZIOS: PARAMETROS DO ENSAIO',1)
    for j,co in enumerate((66,67,68)):
        for luz in (0,16):
            y=80+(j*2+(luz==16))*130
            for fase in range(16):
                pl=consultar_sequencial(co,auxiliar_u8=fase*2,descoberta_u8=0,iluminacao_u8=luz)
                out=compor_passe(c,fundo(80,80),80,80,pl,'terreno',24,24,tabela_sombra=tab)
                x=16+fase*86
                contato.sprite(x,y,Quadro(80,80,out,bytes([255])*6400,0,b''),pal,1)
                contato.texto(x,y+85,f'{co} F{fase}',1)
                contato.texto(x,y+100,'ESCURO' if luz else 'CLARO',1)
    contato.salvar(p/'sequenciais-contato.png')
    eta=ler_objetos_eta_v6(c._ler('cd/WORLD/MONDE01.ETA'))
    eta['ressalva']='Cobertura dos códigos de disco: 486/486; não comprova missão carregada, flags de jogador ou estado futuro do auxiliar.'
    (p/'exemplos-eta-v6.json').write_text(json.dumps(eta,ensure_ascii=False,indent=2)+'\n')
    exemplos=[x for x in eta['registros'] if x['codigo'] in CODIGOS_SEQUENCIAIS]
    data=dict(quadros=quadros,paleta=list(pal),tabela=list(tab),planos=planos,
              referencias=refs,exemplos=exemplos)
    (p/'demo-sequenciais.html').write_text((RAIZ/'sequenciais.template.html').read_text().replace('/*DADOS_SEQUENCIAIS*/',json.dumps(data,ensure_ascii=False)))
    print(len(linhas),'associações;',len(quadros),'quadros;',len(planos),'planos;',len(refs),'buffers; 486/486 ETA')


if __name__=='__main__':gerar()
