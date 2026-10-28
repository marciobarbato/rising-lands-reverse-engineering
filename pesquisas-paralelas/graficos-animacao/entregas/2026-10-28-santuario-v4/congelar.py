"""Publica uma nova revisão; nunca substitui uma pasta de entrega existente."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
from extrair_evidencias import RAIZ, COMMIT, HASH_EXE, exigir_area_editavel


def congelar(identificador):
    exigir_area_editavel()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,100}',identificador):
        raise ValueError('Identificador inválido')
    for nome in ('python','x86','visual','x86-trabalhadores','visual-trabalhadores',
                 'x86-composicao','visual-composicao','x86-construcoes','visual-construcoes'):
        report=json.loads((RAIZ/'validacao'/f'{nome}.json').read_text())
        if report['resultado']!='PASSOU':raise RuntimeError(f'Validação {nome} não passou')
    destino=RAIZ/'entregas'/identificador
    destino.mkdir(parents=True,exist_ok=False)
    arquivos=['README.md','INTEGRACAO.md','VALIDACAO.md','graficos.py','extrair_evidencias.py',
              'bancada_x86.py','validar_x86.py','validar_python.py','test_graficos.py',
              'gerar_artefatos.py','demo.template.html','congelar.py','verificar_manifesto.py',
              'validar_trabalhadores.py','gerar_trabalhadores.py','unidades.template.html',
              'test_trabalhadores.py','CONTINUIDADE_V2.md','REPRODUCAO_PUBLICACAO.md',
              'composicao.py','validar_composicao.py','gerar_composicao.py',
              'composicao.template.html','test_composicao.py','CONTINUIDADE_V3.md',
              'construcoes.py','validar_construcoes.py','gerar_construcoes.py',
              'construcoes.template.html','test_construcoes.py','CONTINUIDADE_V4.md']
    for nome in arquivos:shutil.copyfile(RAIZ/nome,destino/nome)
    for pasta in ('fontes','snapshot','dependencias','evidencias','artefatos','validacao'):
        shutil.copytree(RAIZ/pasta,destino/pasta,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    items=[]
    for p in sorted(destino.rglob('*')):
        if p.is_file():items.append(dict(caminho=p.relative_to(destino).as_posix(),bytes=p.stat().st_size,
                                         sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    manifesto=dict(identificador=identificador,commit_base=COMMIT,exe_sha256=HASH_EXE,
                   commit_entrega_anterior='b67215a3870d17a51b063cb9d82ea391c1852f56',
                   regra='Imutável após publicação; alterações exigem nova revisão.',
                   arquivos=items,quantidade_arquivos=len(items))
    if identificador == '2026-10-28-composicao-v3r2':
        anterior=RAIZ/'entregas/2026-10-28-composicao-v3/MANIFESTO.json'
        manifesto['revisao_substituida'] = dict(identificador='2026-10-28-composicao-v3',
            sha256_manifesto=hashlib.sha256(anterior.read_bytes()).hexdigest())
    mp=destino/'MANIFESTO.json';mp.write_text(json.dumps(manifesto,ensure_ascii=False,indent=2)+'\n')
    hash_manifesto=hashlib.sha256(mp.read_bytes()).hexdigest()
    sums=''.join(f'{i["sha256"]}  {i["caminho"]}\n' for i in items)
    sums+=f'{hash_manifesto}  MANIFESTO.json\n'
    (destino/'SHA256SUMS').write_text(sums)
    print(json.dumps(dict(entrega=str(destino),arquivos=len(items),sha256_manifesto=hash_manifesto),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('identificador')
    congelar(p.parse_args().identificador)
