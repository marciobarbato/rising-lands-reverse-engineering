"""Gera tabelas, atlas PNG e HTML autônomo com biblioteca padrão Python."""
import base64
import csv
import hashlib
import json
import struct
from graficos import *
from extrair_evidencias import exigir_area_editavel

# Fonte bitmap pequena apenas para rótulos técnicos do atlas; sprites intocados.
FONT = {
'0':'01110/10001/10011/10101/11001/10001/01110','1':'00100/01100/00100/00100/00100/00100/01110',
'2':'01110/10001/00001/00010/00100/01000/11111','3':'11110/00001/00001/01110/00001/00001/11110',
'4':'00010/00110/01010/10010/11111/00010/00010','5':'11111/10000/10000/11110/00001/00001/11110',
'6':'01110/10000/10000/11110/10001/10001/01110','7':'11111/00001/00010/00100/01000/01000/01000',
'8':'01110/10001/10001/01110/10001/10001/01110','9':'01110/10001/10001/01111/00001/00001/01110',
'A':'01110/10001/10001/11111/10001/10001/10001','B':'11110/10001/10001/11110/10001/10001/11110',
'C':'01111/10000/10000/10000/10000/10000/01111','D':'11110/10001/10001/10001/10001/10001/11110',
'E':'11111/10000/10000/11110/10000/10000/11111','F':'11111/10000/10000/11110/10000/10000/10000',
'G':'01111/10000/10000/10111/10001/10001/01111','H':'10001/10001/10001/11111/10001/10001/10001',
'I':'01110/00100/00100/00100/00100/00100/01110','J':'00001/00001/00001/00001/10001/10001/01110',
'L':'10000/10000/10000/10000/10000/10000/11111','M':'10001/11011/10101/10101/10001/10001/10001',
'N':'10001/11001/11001/10101/10011/10011/10001','O':'01110/10001/10001/10001/10001/10001/01110',
'P':'11110/10001/10001/11110/10000/10000/10000','Q':'01110/10001/10001/10001/10101/10010/01101',
'R':'11110/10001/10001/11110/10100/10010/10001','S':'01111/10000/10000/01110/00001/00001/11110',
'T':'11111/00100/00100/00100/00100/00100/00100','U':'10001/10001/10001/10001/10001/10001/01110',
'V':'10001/10001/10001/10001/10001/01010/00100','X':'10001/10001/01010/00100/01010/10001/10001',
'W':'10001/10001/10001/10101/10101/10101/01010','Y':'10001/10001/01010/00100/00100/00100/00100',
'Z':'11111/00001/00010/00100/01000/10000/11111',
'-':'00000/00000/00000/11111/00000/00000/00000','/':'00001/00001/00010/00100/01000/10000/10000',
'.':'00000/00000/00000/00000/00000/00110/00110',':':'00000/00110/00110/00000/00110/00110/00000',
'=':'00000/00000/11111/00000/11111/00000/00000','|':'00100/00100/00100/00100/00100/00100/00100',
'+':'00000/00100/00100/11111/00100/00100/00000',' ':'00000/00000/00000/00000/00000/00000/00000'}


class Raster:
    def __init__(self,w,h):
        self.w=w;self.h=h;self.p=bytearray(bytes((19,28,39,255))*w*h)
    def rect(self,x,y,w,h,color):
        for yy in range(max(0,y),min(self.h,y+h)):
            for xx in range(max(0,x),min(self.w,x+w)):
                self.p[(yy*self.w+xx)*4:(yy*self.w+xx+1)*4]=bytes(color)
    def texto(self,x,y,texto,escala=2,cor=(207,220,228,255)):
        for c in texto:
            for yy,linha in enumerate(FONT.get(c,FONT[' ']).split('/')):
                for xx,p in enumerate(linha):
                    if p=='1':self.rect(x+xx*escala,y+yy*escala,escala,escala,cor)
            x+=6*escala
    def sprite(self,x,y,q,pal,escala=2):
        for yy in range(q.altura):
            for xx in range(q.largura):
                i=yy*q.largura+xx
                if q.opacidade[i]:
                    v=q.pixels[i]*3;self.rect(x+xx*escala,y+yy*escala,escala,escala,tuple(pal[v:v+3])+(255,))
    def salvar(self,p):p.write_bytes(png(self.w,self.h,bytes(self.p)))


def gerar():
    exigir_area_editavel()
    c=Catalogo();pal=c.paleta();pasta=RAIZ/'artefatos';pasta.mkdir(exist_ok=True)
    linhas=[]
    for estado in ('parado','andando'):
        for direcao in range(1,17):
            for fase in ([2] if estado=='parado' else range(8)):
                m=consultar(0,estado,direcao,fase);q=c.quadro(m['id_motor'])
                m.update(largura=q.largura,altura=q.altura,offset_cmp=q.offset_cabecalho,
                         sha256_pixels=hashlib.sha256(q.pixels).hexdigest(),
                         sha256_opacidade=hashlib.sha256(q.opacidade).hexdigest())
                linhas.append(m)
    (pasta/'associacoes.json').write_text(json.dumps(linhas,ensure_ascii=False,indent=2)+'\n')
    with (pasta/'associacoes.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(linhas[0]),lineterminator="\n");writer.writeheader()
        for m in linhas:
            writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict,tuple)) else v for k,v in m.items()})
    base=0;bancos=[]
    for nome,n in zip(ORDEM,QUANTIDADES):
        bancos.append(dict(arquivo=nome,quantidade=n,indice_global_inicial=base,indice_global_final=base+n-1,
                           id_motor_inicial=base+1,id_motor_final=base+n))
        base+=n
    (pasta/'bancos.json').write_text(json.dumps(bancos,indent=2)+'\n')
    atlas=Raster(1560,1590)
    atlas.texto(22,20,'SOLDADO TIPO 0 | TROOPS.CMP | MOVIMENTO',3)
    atlas.texto(22,54,'L = INDICE LOCAL 0-BASE | G = INDICE GLOBAL 0-BASE | ID MOTOR = G+1',2)
    for f in range(8):atlas.texto(110+f*180,88,f'FASE {f}',2,cor=(245,196,113,255))
    imagens=[]
    for d in range(8):
        y=118+d*180;atlas.texto(14,y+44,DIRECOES[d],3);atlas.texto(14,y+76,f'{d*2+1}/{d*2+2}',1)
        for f in range(8):
            m=consultar(0,'andando',d*2+1,f);q=c.quadro(m['id_motor']);x=100+f*180
            atlas.rect(x,y,174,174,(31,44,53,255) if f!=2 else (46,60,62,255))
            atlas.sprite(x+(174-q.largura*2)//2,y+4,q,pal)
            atlas.texto(x+7,y+146,f'L{m["indice_local"]} G{m["indice_global"]}',1)
            atlas.texto(x+7,y+160,f'ID {m["id_motor"]}',1)
            dados=png(q.largura,q.altura,rgba(q,pal))
            imagens.append(dict(**m,w=q.largura,h=q.altura,uri='data:image/png;base64,'+base64.b64encode(dados).decode()))
    atlas.texto(22,1565,'PARADA ESTABELECIDA = FASE 2 | OITO DIRECOES VISUAIS PARA 16 ORIENTACOES',2)
    atlas.salvar(pasta/'atlas-soldado.png')
    parada=Raster(1480,236);parada.texto(20,16,'SOLDADO PARADO | FASE 2 | ID DO MOTOR 1-BASE',2)
    for d in range(8):
        m=consultar(0,'parado',d*2+1);q=c.quadro(m['id_motor']);x=20+d*180
        parada.sprite(x+6,46,q,pal)
        parada.texto(x+6,186,f'{DIRECOES[d]} {d*2+1}/{d*2+2}',2)
        parada.texto(x+6,210,f'L{m["indice_local"]} ID{m["id_motor"]}',1)
    parada.salvar(pasta/'parada-soldado.png')
    html=(RAIZ/'demo.template.html').read_text().replace('/*DADOS_SPRITES*/',json.dumps(imagens,ensure_ascii=False))
    (pasta/'demo.html').write_text(html)
    eta=c._ler('cd/WORLD/MONDE01.ETA')
    if eta[:4]!=b'V0.3':raise ValueError('ETA inesperado')
    pos=0x50030;n,s=struct.unpack_from('<HH',eta,pos);pos+=4+n*(s+2)
    n,s=struct.unpack_from('<HH',eta,pos);pos+=4
    if s!=784:raise ValueError('Tamanho de registro inesperado')
    exemplos=[]
    for _ in range(n):
        indice=struct.unpack_from('<H',eta,pos)[0];raw=eta[pos+2:pos+2+s];ram=raw[:140]+raw[652:]
        if ram[1]==0:
            celula=struct.unpack_from('<H',ram,8)[0]
            exemplos.append(dict(indice=indice,offset_registro=pos+2,tipo=ram[1],estado_no_disco=ram[2],
                                 direcao_no_disco=ram[0x91],fase_no_disco=ram[0xa4],
                                 celula_x=celula&255,celula_y=celula>>8,
                                 id_motor_por_formula=consultar(0,'andando',ram[0x91],ram[0xa4])['id_motor'],
                                 sha256_registro=hashlib.sha256(raw).hexdigest()))
        pos+=s+2
    (pasta/'exemplos-eta.json').write_text(json.dumps(dict(fonte='MONDE01.ETA',
        ressalva='Campos serializados; não emula pós-processamento do carregador nem o mundo.',soldados=exemplos),indent=2)+'\n')
    print('Gerados:',len(linhas),'associações;',len(imagens),'sprites;',len(exemplos),'exemplos ETA')


if __name__=='__main__':gerar()
