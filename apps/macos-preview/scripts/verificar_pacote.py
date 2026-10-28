"""Confere o payload final e suas assinaturas, sem modificar o .app."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def runtime_inside_app(runtime, app):
    return bool(runtime) and all(Path(value).resolve().is_relative_to(app.resolve()) for value in runtime.values())

def main():
    build=json.loads((ROOT/'dist/build-manifest.json').read_text());app=ROOT/'dist/RisingLands-Preview.app';errors=[]
    expected={f['path'] for f in build['files']};actual={str(p.relative_to(app)) for p in app.rglob('*') if p.is_file()}
    if actual!=expected:errors.append('Arquivos extras ou ausentes no pacote')
    for item in build['files']:
        p=app/item['path']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:errors.append(item['path'])
    verification=subprocess.run(['codesign','--verify','--deep','--strict',str(app)],capture_output=True,text=True)
    if verification.returncode:errors.append(verification.stderr)
    python=app/'Contents/Resources/Python/bin/python3'
    check=subprocess.run([str(python),'-I','-B','-c','import sys,os,json;print(json.dumps({"prefix":sys.prefix,"executable":sys.executable,"stdlib":os.__file__}))'],capture_output=True,text=True)
    runtime=json.loads(check.stdout) if check.returncode==0 else {}
    if not runtime_inside_app(runtime, app):errors.append('Runtime não está inteiramente dentro do .app')
    snapshot=json.loads((ROOT/'snapshot.json').read_text())
    if snapshot['commit']!=build['commit']:errors.append('Build e snapshot de commits distintos')
    report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':not errors,'commit':build['commit'],'bundleFiles':len(expected),'runtime':runtime,'errors':errors}
    (ROOT/'build/logs/pacote.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if not errors else 1
if __name__=='__main__':sys.exit(main())
