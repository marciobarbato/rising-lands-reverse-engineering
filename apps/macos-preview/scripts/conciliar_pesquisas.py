"""Congela entregas concluídas; nunca importa código das pastas dos outros chats."""
from pathlib import Path
import datetime,hashlib,json,shutil,sys
ROOT=Path(__file__).resolve().parents[1]
SOURCES={
 'economia':{'chat':'01a17d97-28ed-71b1-b599-7af204c36add','title':'Investigar economia de Rising Lands','completedTurn':'01a17daf-5b76-71d2-b533-9d65b9ca98e4'},
 'combate':{'chat':'01a17d98-8087-75b3-ba8b-81cb5ffa64aa','title':'Investigar seleção de alvos','completedTurn':'entrega final EnginViseCible / AngleCalcul'}
}
def capture(name):
    source=ROOT.parents[1]/'pesquisas-paralelas'/name
    def read():
        return {str(p.relative_to(source)):p.read_bytes() for p in sorted(source.rglob('*')) if p.is_file() and not p.is_symlink() and not any(v.startswith('.') or v=='__pycache__' for v in p.relative_to(source).parts) and p.suffix!='.pyc'}
    data=read()
    for required in ('README.md','INTEGRACAO.md','validacao-emulada.json','validacao-local.json'):
        if required not in data:raise ValueError('Entrega incompleta: '+name+'/'+required)
    evidence=json.loads(data['validacao-emulada.json'])
    if not evidence.get('sucesso') or evidence.get('falhas') or evidence.get('erros') or evidence.get('ignorados'):raise ValueError('Pesquisa sem validação completa: '+name)
    if data!=read():raise RuntimeError('Pesquisa mudou durante a leitura; captura recusada: '+name)
    files=[{'path':p,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)} for p,b in data.items()]
    digest=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    target=ROOT/'research'/name/digest
    for p,b in data.items():
        out=target/p;out.parent.mkdir(parents=True,exist_ok=True)
        if out.exists() and out.read_bytes()!=b:raise ValueError('Snapshot de pesquisa alterado: '+str(out))
        if not out.exists():out.write_bytes(b)
    manifest={**SOURCES[name],'name':name,'path':str(target.relative_to(ROOT)),'sha256':digest,'capturedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completionEvidence':'Chat idle com turno concluído e resposta final, conferido pelo read_thread.','historicalValidation':evidence,'files':files}
    (target/'snapshot-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    return manifest
if __name__=='__main__':
    manifests={n:capture(n) for n in SOURCES}
    (ROOT/'research.json').write_text(json.dumps({'policy':'Entregas concluídas capturadas integralmente em duas leituras iguais. Atualizações normais preservam estes snapshots; nova conciliação exige conferir conclusão dos chats.','research':manifests},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({n:{'sha256':m['sha256'],'files':len(m['files']),'historicalTests':m['historicalValidation']['testes']} for n,m in manifests.items()},indent=2))
