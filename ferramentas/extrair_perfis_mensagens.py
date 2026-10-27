"""Extrai do EXE os perfis de mensagens por estado de unidade."""
import json
import struct
from pathlib import Path
from analisar import dependencias, HASH_ESTUDADO, sha


def main():
    raiz=Path(__file__).resolve().parents[1]
    dados=(raiz.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if sha(dados)!=HASH_ESTUDADO:
        raise ValueError('Executável diferente da edição identificada')
    pefile,_=dependencias()
    memoria=pefile.PE(data=dados).get_memory_mapped_image()
    perfis=[]
    for i in range(10):
        endereco=struct.unpack_from('<I',memoria,0x98b38+i*4)[0]
        regras=[]
        if endereco:
            while memoria[endereco-0x400000]!=255:
                b=memoria[endereco-0x400000:endereco-0x400000+12]
                regras.append(dict(tipo=b[0],estado=b[1],subestado=b[2],despacho_unidade=b[3],
                                   bit=b[4],tamanho_resultado=b[5],offset_resultado=struct.unpack_from('<H',b,6)[0],
                                   despacho_estrutura=b[8],tamanho_estrutura=b[9],offset_estrutura=struct.unpack_from('<H',b,10)[0]))
                endereco+=12
        perfis.append(regras)
    relatorio=dict(sha256_original=HASH_ESTUDADO,origem='RISING.EXE, tabela em 0x498b38; registros de 12 bytes; índices 0 e 9 nulos.',perfis=perfis)
    destino=raiz/'relatorios/perfis-mensagens.json'
    destino.write_text(json.dumps(relatorio,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(str(destino))


if __name__=='__main__':main()
