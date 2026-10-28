"""Demonstração offline e folha de contato da composição, sem x86."""
import base64
import json
import hashlib
from graficos import RAIZ, Catalogo, TIPOS, localizar, consultar, png, Quadro
from composicao import SOMBRA_ID, tabela_sombra, compor_unidade, encaminhamento
from gerar_artefatos import Raster
from extrair_evidencias import exigir_area_editavel


def gerar():
    exigir_area_editavel();c=Catalogo();pal=c.paleta();p=RAIZ/'artefatos'
    tabela=tabela_sombra(pal,percentual=60,ciclos=())
    quadros={};tipos=[];associacoes=[]
    for tipo,s in TIPOS.items():
        tipos.append(dict(tipo=tipo,nome=s['nome'],bases=s['bases'],ancora=s['ancora'],parada=s['parada']))
        for base in s['bases']:
            for id_motor in range(base,base+64):
                q=c.quadro(id_motor)
                quadros[id_motor]=dict(w=q.largura,h=q.altura,rle=base64.b64encode(q.comprimido).decode())
        associacoes.append(dict(tipo=tipo,camada='sombra',**localizar(SOMBRA_ID),
            estado='ramo AffDeplaceEngin; 2 comparado até o retorno',direcao='independente de 1..16',
            sequencia=[SOMBRA_ID],ancoragem={'x':-2,'y':-26,'referencia':'origem da célula'},
            ordem='antes do corpo',operacao='remapeia o índice do destino; cores literais CMP ignoradas',
            confianca='confirmada_codigo_e_comparacao_x86',evidencia=['0x412390','0x45b796','0x45f7ba']))
    q=c.quadro(SOMBRA_ID)
    quadros[SOMBRA_ID]=dict(w=q.largura,h=q.altura,rle=base64.b64encode(q.comprimido).decode())
    # Fundo de inspeção sintético, deliberadamente identificado como tal.
    fundo=bytes(82 if ((x//16+y//16)%2) else 115 for y in range(96) for x in range(128))
    painel=Raster(1280,1120)
    painel.texto(22,18,'COMPOSICAO INDEXADA | SOMBRA ANTES DO CORPO',3)
    painel.texto(22,54,'PALETA ORIGINAL | FUNDO SINTETICO | PERCENTUAL 60 E CICLOS VAZIOS: ENTRADAS DO ENSAIO',1)
    casos=[];linha=0
    for tipo,s in TIPOS.items():
        for bolsa,base in enumerate(s['bases']):
            d=9;f=s['parada'];id_motor=consultar(tipo,'parado',d,bolsa_u16=bolsa)['id_motor']
            saida,plano=compor_unidade(c,fundo,128,96,tipo=tipo,estado_u8=7,direcao=d,fase=f,
                                     x=60,y=25,tabela=tabela,bolsa_u16=bolsa)
            x=24+(linha%4)*314;y=92+(linha//4)*268
            painel.texto(x,y,f'TIPO {tipo} BOLSA {bolsa} | L',2)
            painel.sprite(x,y+28,Quadro(128,96,saida,bytes([255])*len(saida),0,b''),pal,2)
            painel.texto(x,y+232,f'ID {id_motor} | SOMBRA 10784 | FASE {f}',1)
            casos.append(dict(tipo=tipo,bolsa_u16=bolsa,direcao=d,fase=f,estado_u8=7,
                x=60,y=25,largura=128,altura=96,sha256_indices=hashlib.sha256(saida).hexdigest(),
                indices_base64=base64.b64encode(saida).decode()))
            linha+=1
    painel.texto(24,652,'SOMBRA 10784 | OTHERS LOCAL 3144 | MASCARA EM BRANCO',2)
    painel.sprite(24,686,Quadro(q.largura,q.altura,bytes([255])*len(q.pixels),q.opacidade,0,b''),
                   bytes(765)+bytes([255])*3,4)
    painel.texto(24,768,'256 INDICES DE FUNDO: ORIGINAL ACIMA / REMAPEADO ABAIXO',2)
    for i in range(256):
        x=24+(i%32)*38;y=810+(i//32)*35
        painel.rect(x,y,34,12,tuple(pal[i*3:i*3+3])+(255,))
        z=tabela[i];painel.rect(x,y+13,34,12,tuple(pal[z*3:z*3+3])+(255,))
        painel.texto(x,y+26,str(i),1)
    painel.salvar(p/'composicao-contato.png')
    data=dict(tipos=tipos,quadros=quadros,paleta=list(pal),tabela=list(tabela),sombra=SOMBRA_ID,
              casos_referencia=casos,percentual=60,ciclos=[])
    (p/'demo-composicao.html').write_text((RAIZ/'composicao.template.html').read_text().replace('/*DADOS_COMPOSICAO*/',json.dumps(data,ensure_ascii=False)))
    (p/'associacoes-sombras.json').write_text(json.dumps(associacoes,ensure_ascii=False,indent=2)+'\n')
    (p/'paleta-sombra.json').write_text(json.dumps(dict(paleta_rgb=list(pal),tabela=list(tabela),
        percentual=60,ciclos=[],confianca='algoritmo confirmado; parâmetros do ensaio explícitos',
        evidencia=['0x4798e9','0x43ee31..0x43ee8d','0x45f940','0x4795af']),ensure_ascii=False,indent=2)+'\n')
    (p/'despacho-estados.json').write_text(json.dumps([encaminhamento(t,e,auxiliar_8a=a)
        for t in TIPOS for e in range(256) for a in ([0,1,2,3,4,255] if e in (1,22,24) else [0])],ensure_ascii=False,indent=2)+'\n')
    print('Composição: 513 quadros comprimidos, 8 referências e 5 associações de sombra')


if __name__=='__main__':gerar()
