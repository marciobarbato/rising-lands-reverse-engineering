"""Verificação somente leitura da entrega congelada, inclusive lista exata de arquivos."""
from pathlib import Path
import argparse
import hashlib
import json


def verificar(pasta):
    raiz=Path(pasta).resolve();manifesto=json.loads((raiz/'MANIFESTO.json').read_text())
    esperado=set();sums=[]
    for item in manifesto['arquivos']:
        caminho=(raiz/item['caminho']).resolve()
        caminho.relative_to(raiz)
        dados=caminho.read_bytes();sha=hashlib.sha256(dados).hexdigest()
        if sha!=item['sha256'] or len(dados)!=item['bytes']:
            raise ValueError(f'Integridade divergente: {item["caminho"]}')
        esperado.add(item['caminho']);sums.append(f'{sha}  {item["caminho"]}\n')
    atual={p.relative_to(raiz).as_posix() for p in raiz.rglob('*') if p.is_file()}
    if atual!=esperado|{'MANIFESTO.json','SHA256SUMS'}:
        raise ValueError('Arquivos ausentes/extras na entrega')
    sha=hashlib.sha256((raiz/'MANIFESTO.json').read_bytes()).hexdigest()
    sums.append(f'{sha}  MANIFESTO.json\n')
    if ''.join(sums)!=(raiz/'SHA256SUMS').read_text():raise ValueError('SHA256SUMS divergente')
    return dict(resultado='PASSOU',identificador=manifesto['identificador'],arquivos=len(esperado),sha256_manifesto=sha)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('pasta',nargs='?',default=str(Path(__file__).resolve().parent))
    print(json.dumps(verificar(p.parse_args().pasta),indent=2))
