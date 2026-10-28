"""Extrai PlaceBatiment, consultas locais e a tabela que escolhe os tiles."""
import hashlib
import json
import struct
import sys
from pathlib import Path

RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ.parent/'source/python'))
HASH='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
INTERVALOS=(('ValideHerse',0x41ac8b,0x41ad78),
            ('ChercheMurCombinaisons',0x41c18a,0x41c251),
            ('SetMurAllentour',0x41c251,0x41c451),
            ('PlaceBatiment',0x41c4ac,0x41c652))


def extrair():
    import capstone
    d=(RAIZ.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(d).hexdigest()!=HASH:raise ValueError('Executável diferente do original identificado')
    pe=struct.unpack_from('<I',d,60)[0]
    n,op=(struct.unpack_from('<H',d,pe+off)[0] for off in (6,20))
    secoes=[struct.unpack_from('<III',d,pe+24+op+i*40+12) for i in range(n)]
    def ler(a,t):
        r=a-0x400000
        for base,tamanho,offset in secoes:
            if offset and base<=r and r+t<=base+tamanho:return d[offset+r-base:offset+r-base+t]
        raise ValueError('Endereço sem dados na imagem PE')
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    pasta=RAIZ/'evidencias/colocacao-estruturas';pasta.mkdir(parents=True,exist_ok=True)
    trechos=[]
    for nome,a,b in INTERVALOS:
        bruto=ler(a,b-a);ins=list(md.disasm(bruto,a))
        if sum(i.size for i in ins)!=len(bruto):raise ValueError('Trecho não desmontado integralmente')
        arquivo=f'{a:08x}.asm'
        linhas=[f'; {nome}; SHA-256 do EXE original: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins]
        (pasta/arquivo).write_text('\n'.join(linhas)+'\n',encoding='utf-8')
        trechos.append(dict(nome=nome,inicio=f'0x{a:08x}',fim_exclusivo=f'0x{b:08x}',
                            tamanho=len(bruto),sha256=hashlib.sha256(bruto).hexdigest(),arquivo=arquivo))
    bruto=ler(0x41c454,88);tipos=[]
    for tipo,alvo in enumerate(struct.unpack('<22I',bruto)):
        primeiro=None
        if tipo not in (9,12):
            i=next(md.disasm(ler(alvo,5),alvo))
            if i.mnemonic!='mov' or not i.op_str.startswith('edx, '):raise ValueError('Seletor inesperado')
            primeiro=int(i.op_str.split(', ')[1],0)
        tipos.append(dict(tipo=tipo,alvo=f'0x{alvo:08x}',primeiro_tile=primeiro))
    m=dict(sha256_original=HASH,capstone=capstone.__version__,trechos=trechos,
           tabela=dict(endereco='0x0041c454',bytes_hex=bruto.hex(),sha256=hashlib.sha256(bruto).hexdigest(),tipos=tipos),
           objetos_iniciais=dict(muro=ler(0x495bf8,1)[0],portao=ler(0x495bf9,1)[0]),
           limite='Colocação de registro já preparado; não é criação nem ordem completa de construir.')
    (pasta/'manifesto.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return m


if __name__=='__main__':print('Trechos extraídos:',len(extrair()['trechos']))
