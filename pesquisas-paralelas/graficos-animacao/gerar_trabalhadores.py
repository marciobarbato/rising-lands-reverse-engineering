"""Artefatos de unidades validadas, com variantes de bolsa explícitas."""
import base64
import csv
import hashlib
import json
import struct
import unicodedata
from graficos import RAIZ, TIPOS, DIRECOES, Catalogo, consultar, png, rgba
from gerar_artefatos import Raster
from extrair_evidencias import exigir_area_editavel, COMMIT, HASH_EXE


def ascii_texto(s):
    return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().upper()


def gerar():
    exigir_area_editavel()
    c=Catalogo();pal=c.paleta();pasta=RAIZ/'artefatos'
    linhas=[];conjuntos=[];tipos=[]
    contato=Raster(1560,1580)
    contato.texto(20,18,'UNIDADES | PARADA ESTABELECIDA | VARIANTES DE BOLSA',3)
    contato.texto(20,54,'L = INDICE LOCAL TROOPS 0-BASE | ID MOTOR 1-BASE | SOMBRA OMITIDA',2)
    linha=0
    for tipo,spec in TIPOS.items():
        tipos.append(dict(tipo=tipo,nome=spec['nome'],parada=spec['parada'],
                          usa_bolsa=len(spec['bases'])==2,ancora=spec['ancora']))
        for variante,base in enumerate(spec['bases']):
            bolsa=variante if len(spec['bases'])==2 else None
            chave=f'{tipo}-{variante}'
            nome_atlas=f'atlas-tipo-{chave}.png'
            r=Raster(1560,1590)
            titulo=ascii_texto(f'{spec["nome"]} TIPO {tipo}')
            condicao='BOLSA '+('NAO VAZIA' if variante else 'VAZIA') if bolsa is not None else 'BASE'
            r.texto(22,20,f'{titulo} | {condicao}',3)
            r.texto(22,54,'TROOPS.CMP | L LOCAL 0-BASE | G GLOBAL 0-BASE | ID MOTOR 1-BASE',2)
            for f in range(8):r.texto(110+f*180,88,f'FASE {f}',2,cor=(245,196,113,255))
            sprites=[]
            for d in range(8):
                y=118+d*180;r.texto(14,y+44,DIRECOES[d],3);r.texto(14,y+76,f'{d*2+1}/{d*2+2}',1)
                for f in range(8):
                    m=consultar(tipo,'andando',d*2+1,f,bolsa_u16=bolsa)
                    q=c.quadro(m['id_motor']);x=100+f*180
                    r.rect(x,y,174,174,(46,60,62,255) if f==spec['parada'] else (31,44,53,255))
                    r.sprite(x+(174-q.largura*2)//2,y+4,q,pal)
                    r.texto(x+7,y+146,f'L{m["indice_local"]} G{m["indice_global"]}',1)
                    r.texto(x+7,y+160,f'ID {m["id_motor"]}',1)
                    sprites.append(dict(id_motor=m['id_motor'],indice_local=m['indice_local'],
                        indice_global=m['indice_global'],w=q.largura,h=q.altura,
                        uri='data:image/png;base64,'+base64.b64encode(png(q.largura,q.altura,rgba(q,pal))).decode()))
            r.texto(22,1565,f'PARADA = FASE {spec["parada"]} | ANCORA {spec["ancora"][0]}/{spec["ancora"][1]} | MOVIMENTO: 2 CHAMADAS POR FASE',2)
            r.salvar(pasta/nome_atlas)
            conjuntos.append(dict(chave=chave,tipo=tipo,variante=variante,base=base,atlas=nome_atlas,sprites=sprites))
            y=90+linha*184
            contato.texto(18,y,titulo+' | '+condicao+f' | FASE {spec["parada"]}',2)
            for d in range(8):
                m=consultar(tipo,'parado',d*2+1,bolsa_u16=bolsa);q=c.quadro(m['id_motor']);x=90+d*180
                contato.sprite(x+(170-q.largura*2)//2,y+24,q,pal)
                contato.texto(x,y+166,f'{DIRECOES[d]} L{m["indice_local"]} ID{m["id_motor"]}',1)
            linha+=1
            for estado in ('parado','andando'):
                for direcao in range(1,17):
                    for fase in ([spec['parada']] if estado=='parado' else range(8)):
                        m=consultar(tipo,estado,direcao,fase,bolsa_u16=bolsa);q=c.quadro(m['id_motor'])
                        m.setdefault('variante','base');m.setdefault('bolsa_u16',None)
                        m.setdefault('condicao_variante','independente de +0x0a')
                        m.update(largura=q.largura,altura=q.altura,offset_cmp=q.offset_cabecalho,
                            sha256_pixels=hashlib.sha256(q.pixels).hexdigest(),
                            sha256_opacidade=hashlib.sha256(q.opacidade).hexdigest())
                        linhas.append(m)
    contato.salvar(pasta/'paradas-unidades.png')
    (pasta/'associacoes-unidades.json').write_text(json.dumps(linhas,ensure_ascii=False,indent=2)+'\n')
    with (pasta/'associacoes-unidades.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(linhas[0]),lineterminator='\n');writer.writeheader()
        for m in linhas:
            writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict,tuple)) else v for k,v in m.items()})
    data=dict(tipos=tipos,conjuntos=conjuntos)
    html=(RAIZ/'unidades.template.html').read_text().replace('/*DADOS_UNIDADES*/',json.dumps(data,ensure_ascii=False))
    (pasta/'demo-unidades.html').write_text(html)
    eta=c._ler('cd/WORLD/MONDE01.ETA');pos=0x50030;n,s=struct.unpack_from('<HH',eta,pos);pos+=4+n*(s+2)
    n,s=struct.unpack_from('<HH',eta,pos);pos+=4
    if s!=784:raise ValueError('Registro ETA inesperado')
    registros=[]
    for _ in range(n):
        indice=struct.unpack_from('<H',eta,pos)[0];raw=eta[pos+2:pos+2+s];ram=raw[:140]+raw[652:]
        if ram[1] in TIPOS:
            tipo=ram[1];celula=struct.unpack_from('<H',ram,8)[0];bolsa=struct.unpack_from('<H',ram,0xa)[0]
            r=dict(indice=indice,offset_registro=pos+2,sha256_registro=hashlib.sha256(raw).hexdigest(),
                tipo=tipo,nome=TIPOS[tipo]['nome'],estado_no_disco=ram[2],direcao_no_disco=ram[0x91],
                fase_no_disco=ram[0xa4],bolsa_u16_no_disco=bolsa,bytes_bolsa_hex=ram[0xa:0x12].hex(),
                celula_x=celula&255,celula_y=celula>>8,associacao=None)
            if ram[2] in (2,7):
                r['associacao']=consultar(tipo,'andando',ram[0x91],ram[0xa4],bolsa_u16=bolsa)
                r['ressalva']='Consulta à fase bruta pelo ramo validado; não simula pós-processamento ETA.'
            else:
                r['ressalva']='Estado serializado fora de 2/7: nenhuma associação de desenho afirmada.'
            registros.append(r)
        pos+=s+2
    (pasta/'exemplos-eta-unidades.json').write_text(json.dumps(dict(fonte='MONDE01.ETA',
        commit_snapshot=COMMIT,exe_sha256=HASH_EXE,registros=registros,
        ressalva='Recomposição raw[:140]+raw[652:]; campos no disco, sem simulação do carregador.'),ensure_ascii=False,indent=2)+'\n')
    print('Gerados:',len(linhas),'associações;',len(conjuntos)*64,'sprites;',len(conjuntos),'atlas;',len(registros),'registros ETA')


if __name__=='__main__':gerar()
