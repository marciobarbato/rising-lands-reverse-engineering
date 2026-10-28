"""Copia blobs de um commit por Git somente leitura; nunca lê o working tree."""
from pathlib import Path
import argparse,hashlib,json,subprocess,tempfile,os
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]

def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args],env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
def update(ref='HEAD',activate=True):
    commit=git('rev-parse',ref+'^{commit}').decode().strip()
    snap=ROOT/'snapshots'/commit;snap.mkdir(parents=True,exist_ok=True)
    entries=[]; research={}
    for line in git('ls-tree','-r','-z',commit).split(b'\0'):
        if not line:continue
        meta,name=line.split(b'\t',1);mode,kind,blob=meta.decode().split();name=name.decode()
        if name.startswith(('apps/', 'pesquisas-paralelas/visualizador-mac/')):continue
        if kind!='blob' or mode not in ('100644','100755'):continue
        p=Path(name)
        if p.is_absolute() or '..' in p.parts:raise ValueError('Caminho de snapshot inválido')
        data=git('cat-file','blob',blob);out=snap/name;out.parent.mkdir(parents=True,exist_ok=True)
        if out.exists() and out.read_bytes()!=data:raise ValueError('Snapshot alterado: '+name)
        if not out.exists():out.write_bytes(data)
        entries.append({'path':name,'git_blob':blob,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
        if name.startswith('pesquisas-paralelas/'):
            research.setdefault(p.parts[1],[]).append(name)
    result={'commit':commit,'commitSubject':git('show','-s','--format=%s',commit).decode().strip(),'snapshot':str(snap.relative_to(ROOT)),'policy':'Somente blobs commitados; alterações locais e pesquisas não commitadas excluídas. Adaptadores só habilitam APIs explicitamente suportadas.','researchCommitted':research,'files':entries}
    serialized=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    archive=ROOT/'snapshots/manifests'/f'{commit}.json';archive.parent.mkdir(parents=True,exist_ok=True);archive.write_text(serialized)
    if activate:
        temp=ROOT/'build/tmp/snapshot.json';temp.parent.mkdir(parents=True,exist_ok=True);temp.write_text(serialized);temp.replace(ROOT/'snapshot.json')
    print('Snapshot:',commit,'—',len(entries),'arquivos; pesquisas commitadas:',', '.join(research) or 'nenhuma')
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--commit',default='HEAD');p.add_argument('--archive-only',action='store_true');a=p.parse_args();update(a.commit,activate=not a.archive_only)
