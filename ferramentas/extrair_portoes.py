"""Exporta os predicados, comandos e ramo físico dos portões no EXE original."""
import hashlib
import json
import struct
import sys
from pathlib import Path

RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ.parent/'source/python'))
HASH='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
INTERVALOS=(('HerseEnAnimation',0x4191fd,0x419233),
            ('HerseEstBaisser',0x41934f,0x419379),
            ('HerseEstLever',0x419379,0x4193ac),
            ('HerseEstFace',0x4193ac,0x4193d4),
            ('BaisseTouteHerse',0x4193d4,0x4195ca),
            ('RemonteTouteHerse',0x4195ca,0x419917),
            ('ChercheEtatHerse',0x419917,0x4199a3),
            ('epilogo_BaisseTouteHerse',0x41c87f,0x41c887),
            ('BatimentNextEtape_prologo',0x4268d4,0x426918),
            ('BatimentNextEtape_tipo12',0x427bb7,0x427d5d),
            ('BatimentNextEtape_epilogo',0x4281c0,0x4281c7))


def extrair():
    import capstone
    raw=(RAIZ.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=HASH:raise ValueError('Executável diferente do original identificado')
    pe=struct.unpack_from('<I',raw,60)[0]
    n,op=(struct.unpack_from('<H',raw,pe+off)[0] for off in (6,20))
    secoes=[struct.unpack_from('<III',raw,pe+24+op+i*40+12) for i in range(n)]
    def ler(a,t):
        r=a-0x400000
        for base,tamanho,offset in secoes:
            if offset and base<=r and r+t<=base+tamanho:return raw[offset+r-base:offset+r-base+t]
        raise ValueError('Endereço sem bytes no PE')
    pasta=RAIZ/'evidencias/portoes';pasta.mkdir(exist_ok=True,parents=True)
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
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
    alvo=struct.unpack('<I',ler(0x426880+11*4,4))[0]
    m=dict(sha256_original=HASH,capstone=capstone.__version__,trechos=trechos,
           despacho_tipo12=dict(entrada_tabela='0x004268ac',destino=f'0x{alvo:08x}'),
           limite='Efeitos de simulação; entrada de mouse desativada na bancada e nenhum sprite escolhido.')
    (pasta/'manifesto.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return m


if __name__=='__main__':print('Trechos extraídos:',len(extrair()['trechos']))
