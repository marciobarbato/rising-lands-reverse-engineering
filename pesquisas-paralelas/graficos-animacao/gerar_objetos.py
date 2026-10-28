"""Associações, atlas e página offline para objetos 1..22 e 28..52."""
import base64
import csv
import hashlib
import json
from graficos import Catalogo, RAIZ, Quadro, localizar
from objetos import CODIGOS, ARVORES, BAIXOS, consultar_objeto, compor_passe, ler_objetos_eta
from composicao import tabela_sombra
from gerar_artefatos import Raster
from extrair_evidencias import exigir_area_editavel


def referencia_rle(d):
    out=bytearray();i=0
    while i<len(d):
        j=i+1
        while j<len(d) and d[j]==d[i] and j-i<255:j+=1
        out.extend((j-i,d[i]));i=j
    return base64.b64encode(out).decode()


def fundo(w=160,h=160):
    return bytes(82 if (x//16+y//16)%2 else 115 for y in range(h) for x in range(w))


def gerar():
    exigir_area_editavel();c=Catalogo();pal=c.paleta();p=RAIZ/'artefatos'
    tab=tabela_sombra(pal,percentual=60,ciclos=());linhas=[];quadros={};planos=[];sombras=set()
    for codigo in CODIGOS:
        for fase in (range(4) if codigo<=11 else (0,)):
            for luz in (0,16):
                pl=consultar_objeto(codigo,auxiliar_u8=fase,descoberta_u8=0,iluminacao_u8=luz);planos.append(pl)
                for passe in ('terreno','sprites'):
                    for ca in pl[passe]:
                        mid=ca['id_motor'];q=c.quadro(mid)
                        quadros[mid]=dict(w=q.largura,h=q.altura,rle=base64.b64encode(q.comprimido).decode())
                        if ca['operacao']=='sombra':sombras.add(mid)
                        linhas.append(dict(**localizar(mid),tipo_objeto=codigo,classe_visual=pl['classe_visual'],
                            classe_confianca='inferencia_visual_sem_semantica_economica',
                            estado='descoberto_iluminado' if luz==0 else 'descoberto_sem_iluminacao',direcao=None,
                            passe=passe,ordem=ca['ordem'],operacao=ca['operacao'],fase=ca['fase'],sequencia=ca['sequencia'],
                            auxiliar_ignorado=codigo>11,ancoragem=dict(x=-ca['x'],y=-ca['y'],referencia='origem da célula de 32×32'),
                            periodo='condicional ao relógio e byte aleatório; não há período fixo' if codigo<=11 else 'estático',
                            largura=q.largura,altura=q.altura,sha256_pixels=hashlib.sha256(q.pixels).hexdigest(),
                            sha256_opacidade=hashlib.sha256(q.opacidade).hexdigest(),confianca=ca['confianca'],evidencia=ca['evidencia']))
    (p/'associacoes-objetos.json').write_text(json.dumps(linhas,ensure_ascii=False,indent=2)+'\n')
    with (p/'associacoes-objetos.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=list(linhas[0]),lineterminator='\n');wr.writeheader()
        for row in linhas:wr.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()})
    ids=sorted(quadros);atlas=Raster(1680,80+((len(ids)+11)//12)*154)
    atlas.texto(20,18,'OBJETOS | OTHERS.CMP | L/G BASE 0 | ID MOTOR BASE 1',3)
    atlas.texto(20,54,'S: MASCARA DE SOMBRA EM BRANCO / CORES LITERAIS IGNORADAS NO BLIT',2)
    branco=bytes(765)+bytes([255])*3
    for i,mid in enumerate(ids):
        x=16+(i%12)*140;y=80+(i//12)*154;q=c.quadro(mid);esc=1 if q.altura>50 or q.largura>60 else 2
        if mid in sombras:atlas.sprite(x,y,Quadro(q.largura,q.altura,bytes([255])*len(q.pixels),q.opacidade,0,b''),branco,esc)
        else:atlas.sprite(x,y,q,pal,esc)
        atlas.texto(x,y+112,f'ID {mid}'+(' S' if mid in sombras else ''),1)
        atlas.texto(x,y+125,f'L{mid-7640} G{mid-1}',1);atlas.texto(x,y+138,f'{q.largura}X{q.altura} / X{esc}',1)
    atlas.salvar(p/'atlas-objetos.png')
    # Dois estados de iluminação lado a lado, preservando a ordem de cada passe.
    contato=Raster(1460,90+((len(CODIGOS)+3)//4)*206)
    contato.texto(20,18,'OBJETOS 1-22 E 28-52 | CLARO / SEM ILUMINACAO',3)
    contato.texto(20,54,'FASE 0 | FUNDO SINTETICO | SOMBRA 60 POR CENTO / CICLOS VAZIOS: ENTRADAS DO ENSAIO',1)
    refs=[]
    for i,codigo in enumerate(CODIGOS):
        for j,luz in enumerate((0,16)):
            pl=consultar_objeto(codigo,auxiliar_u8=0,descoberta_u8=0,iluminacao_u8=luz);passe='sprites' if codigo<=11 else 'terreno'
            out=compor_passe(c,fundo(),160,160,pl,passe,64,108,tabela_sombra=tab)
            x=20+(i%4)*360+j*164;y=90+(i//4)*206
            contato.sprite(x,y,Quadro(160,160,out,bytes([255])*len(out),0,b''),pal,1)
            contato.texto(x,y+169,f'OBJ {codigo} '+('CLARO' if j==0 else 'ESCURO'),1)
            if j==0:contato.texto(x,y+184,'SPRITES' if codigo<=11 else 'TERRENO',1)
        # Uma referência completa por código e estado; mais fases de grupos complexos.
        for fase,luz in ([(0,0),(0,16)]+([(3,0),(3,16)] if codigo in (4,5,9,10) else [])):
            pl=consultar_objeto(codigo,auxiliar_u8=fase,descoberta_u8=0,iluminacao_u8=luz);passe='sprites' if codigo<=11 else 'terreno'
            out=compor_passe(c,fundo(),160,160,pl,passe,64,108,tabela_sombra=tab)
            refs.append(dict(codigo=codigo,auxiliar=fase,iluminacao=luz,passe=passe,
                indices_rle=referencia_rle(out),sha256=hashlib.sha256(out).hexdigest()))
    contato.salvar(p/'objetos-contato.png')
    eta=ler_objetos_eta(c._ler('cd/WORLD/MONDE01.ETA'))
    eta['ressalva']='Camadas do disco; descoberta/iluminação não são obtidas destes bytes. Associação condicionada ao passe e flags fornecidos pelo consumidor. Objetos fora do catálogo permanecem sem CMP atribuído.'
    (p/'exemplos-eta-objetos.json').write_text(json.dumps(eta,ensure_ascii=False,indent=2)+'\n')
    data=dict(codigos=CODIGOS,quadros=quadros,paleta=list(pal),tabela=list(tab),arvores=ARVORES,
        baixos={str(k):v for k,v in BAIXOS.items()},planos=planos,referencias=refs,
        exemplos=[next((r for r in eta['registros'] if r['codigo']==co),None) for co in CODIGOS])
    (p/'demo-objetos.html').write_text((RAIZ/'objetos.template.html').read_text().replace('/*DADOS_OBJETOS*/',json.dumps(data,ensure_ascii=False)))
    print(len(linhas),'associações;',len(ids),'CMPs;',len(planos),'planos;',len(refs),'referências;',sum(r['mapeado'] for r in eta['registros']),'registros ETA mapeados')


if __name__=='__main__':gerar()
