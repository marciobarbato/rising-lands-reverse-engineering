"""Atlas, tabela de associações e demonstração offline do Santuário."""
import base64
import csv
import hashlib
import json
from graficos import Catalogo, RAIZ, Quadro, localizar, compor_indices
from construcoes import consultar_santuario, compor_fachada, tabelas_jogador, ler_estruturas_eta
from gerar_artefatos import Raster
from extrair_evidencias import exigir_area_editavel

W,H=300,260
ORIGEM=(52,76)
GATILHO_TELA=(212,140)


def fundo():
    return bytes(82 if (x//16+y//16)%2 else 115 for y in range(H) for x in range(W))


def terreno(c,entrada):
    for y in range(5):
        for x in range(6):
            entrada=compor_indices(entrada,W,H,c.quadro(732+y*6+x),52+x*32,76+y*32)
    return entrada


def comprimir_referencia(d):
    out=bytearray();i=0
    while i<len(d):
        j=i+1
        while j<len(d) and d[j]==d[i] and j-i<255:j+=1
        out.extend((j-i,d[i]));i=j
    return base64.b64encode(out).decode()


def gerar():
    exigir_area_editavel();c=Catalogo();pal=c.paleta();tabs=tabelas_jogador();p=RAIZ/'artefatos'
    ident=json.loads((RAIZ/'evidencias/identidade-construcoes.json').read_text())
    eta=ler_estruturas_eta(c._ler('cd/WORLD/MONDE01.ETA'))[0]
    plano=consultar_santuario(habitado=True,jogador=0,relogios=(0,0,0),celula_mapa=(17,13))
    faixas=[(7032,1),(7049,8),(7033,8),(7041,8),(7059,8),(7067,8),(7057,2)]
    linhas=[];atlas=Raster(1580,1600)
    atlas.texto(20,20,'SANTUARIO TIPO 2 | BUILDING.CMP | SETE CAMADAS',3)
    atlas.texto(20,56,'L/G: INDICES BASE 0 | ID: MOTOR BASE 1 | MODO 5 / HABITADO / AUXILIAR +06 ZERO',2)
    for ordem,(base,n) in enumerate(faixas):
        camada=plano['camadas'][ordem];seq=list(range(base,base+n));y=94+ordem*214
        atlas.texto(20,y,f'{ordem}: '+camada['papel'].upper().replace('_',' '),2)
        for fase,id_motor in enumerate(seq):
            q=c.quadro(id_motor);x=20+fase*194;esc=1 if ordem==0 else 2
            atlas.sprite(x,y+26,q,pal,esc)
            atlas.texto(x,y+184,f'ID {id_motor} L{id_motor-7029} G{id_motor-1}',1)
            atlas.texto(x,y+198,f'FASE {fase} / X{esc}',1)
            linhas.append(dict(**localizar(id_motor),tipo=2,chave_ini='SANCTUAIRE',estado='modo 5 / habitado / +06=0',
                direcao=None,camada=camada['papel'],ordem=ordem,fase=fase,sequencia=seq,
                relogio=camada['relogio'],fase_soma_celula=ordem in (1,2,3,6),
                periodo_chamadas=[None,3,1,2,1,1,1][ordem],
                ancoragem=dict(x=-camada['x'],y=-camada['y'],referencia='origem da célula gatilho (5,2)'),
                operacao=camada['operacao'],jogadores=[0,1,2,3,4],largura=q.largura,altura=q.altura,
                sha256_pixels=hashlib.sha256(q.pixels).hexdigest(),sha256_opacidade=hashlib.sha256(q.opacidade).hexdigest(),
                confianca='confirmada_codigo_e_comparacao_x86',evidencia=['0x407dd3','0x408577','0x4087bf..0x408923']))
    atlas.salvar(p/'atlas-santuario.png')
    piso=Raster(1120,820)
    piso.texto(20,20,'SANTUARIO | BLOCS.CMP | TERRENO 6X5',3)
    piso.texto(20,58,'GATILHO: ID 749 EM 5,2 | MASCARA: OCUPACAO, NAO TRANSPARENCIA',2)
    for y in range(5):
        for x in range(6):
            i=y*6+x;mid=732+i;q=c.quadro(mid);px=20+x*182;py=100+y*140
            piso.sprite(px,py,q,pal,3)
            piso.texto(px,py+103,f'ID {mid} L/G {mid-1}',1)
            piso.texto(px,py+118,f'CEL {x},{y} OC {ident["mascara_santuario"][i]}'.replace(',','/'),1)
            linhas.append(dict(**localizar(mid),tipo=2,chave_ini='SANCTUAIRE',estado='terreno colocado por PlaceBatiment',
                direcao=None,camada='terreno',ordem=None,fase=0,sequencia=[mid],relogio=None,fase_soma_celula=False,
                periodo_chamadas=None,ancoragem=dict(x=0,y=0,referencia=f'célula relativa ({x},{y}) da origem da construção'),
                operacao='copiar',jogadores=None,largura=q.largura,altura=q.altura,
                sha256_pixels=hashlib.sha256(q.pixels).hexdigest(),sha256_opacidade=hashlib.sha256(q.opacidade).hexdigest(),
                confianca='indices_confirmados_PlaceBatiment_e_ETA',evidencia=['0x41c4e7','0x41ba49','0x476251']))
    piso.salvar(p/'terreno-santuario.png')
    (p/'associacoes-santuario.json').write_text(json.dumps(linhas,ensure_ascii=False,indent=2)+'\n')
    with (p/'associacoes-santuario.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=list(linhas[0]),lineterminator='\n');wr.writeheader()
        for m in linhas:wr.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in m.items()})
    ids=sorted({r['id_motor'] for r in linhas});quadros={}
    for mid in ids:
        q=c.quadro(mid);quadros[mid]=dict(w=q.largura,h=q.altura,rle=base64.b64encode(q.comprimido).decode())
    referencias=[];painel=Raster(1560,680)
    painel.texto(20,20,'SANTUARIO | TABELAS DE JOGADOR 0 A 4 | ITERACAO 7',3)
    painel.texto(20,56,'TERRENO ORIGINAL + FACHADA VALIDADA | ENTORNO QUADRICULADO SINTETICO',2)
    for jogador in range(5):
        for t in (0,7,47):
            rel=(t,t//2,t//3);pl=consultar_santuario(habitado=True,jogador=jogador,relogios=rel,celula_mapa=(17,13))
            out=compor_fachada(c,terreno(c,fundo()),W,H,pl,*GATILHO_TELA,tabelas=tabs)
            referencias.append(dict(jogador=jogador,iteracao=t,indices_rle=comprimir_referencia(out),sha256=hashlib.sha256(out).hexdigest()))
            if t==7:
                x=20+(jogador%3)*510;y=94+(jogador//3)*286
                # Os sprites são mostrados em 1x para manter a folha compacta.
                painel.sprite(x,y,Quadro(W,H,out,bytes([255])*len(out),0,b''),pal,1)
                painel.texto(x+312,y+44,f'JOGADOR {jogador}',2)
                for i in range(8):painel.rect(x+312+i*20,y+82,18,20,tuple(pal[tabs[jogador][160+i]*3:tabs[jogador][160+i]*3+3])+(255,))
    painel.salvar(p/'santuario-composicao.png')
    data=dict(quadros=quadros,paleta=list(pal),tabelas=[list(t) for t in tabs],referencias=referencias,
        planos=[consultar_santuario(habitado=True,jogador=0,relogios=(t,t//2,t//3),celula_mapa=(17,13)) for t in range(48)],
        largura=W,altura=H,origem=ORIGEM,gatilho=GATILHO_TELA)
    (p/'demo-santuario.html').write_text((RAIZ/'construcoes.template.html').read_text().replace('/*DADOS_SANTUARIO*/',json.dumps(data,ensure_ascii=False)))
    (p/'exemplo-eta-santuario.json').write_text(json.dumps(dict(fonte='MONDE01.ETA',
        registro={k:v for k,v in eta.items() if k!='bytes'},celula_gatilho=[17,13],
        condicoes='Habitação conferida por BatimentEstHabiter com unidades recompostas; não emula LoadMission inteiro.',
        plano_relogios_zero=plano),ensure_ascii=False,indent=2)+'\n')
    print('Gerados 73 registros, 73 quadros CMP e 15 referências Python; atlas, terreno e demonstração.')


if __name__=='__main__':gerar()
