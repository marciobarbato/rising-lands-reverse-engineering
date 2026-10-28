"""Executa as suítes dentro da pasta isolada e registra contagens reais."""
from pathlib import Path
import datetime,json,os,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]

def main():
    (ROOT/'build/logs').mkdir(parents=True,exist_ok=True)
    manifest=json.loads((ROOT/'snapshot.json').read_text());snap=ROOT/manifest['snapshot']
    # Os testes originais usam RAIZ.parent/source. Este link só permite leituras;
    # a suíte foi inspecionada e não escreve no corpus.
    source=ROOT.parents[2]/'source';link=ROOT/'snapshots/source'
    if source.is_dir() and not link.exists():link.symlink_to(source,target_is_directory=True)
    # Caminhos relativos dos testes de pesquisa apontam para cópias commitadas e CD somente leitura.
    for alias,target in [(ROOT/'research/relatorios',snap/'relatorios'),(ROOT/'research/ferramentas',snap/'ferramentas'),(ROOT/'source',source),((ROOT/'research').resolve().parent/'source',source)]:
        if alias.is_symlink() and alias.resolve()!=target.resolve():alias.unlink()
        if not alias.exists():alias.symlink_to(target,target_is_directory=True)
    environment=dict(os.environ);environment.pop('RISING_EMULAR',None)
    environment.update({'PYTHONDONTWRITEBYTECODE':'1','PYTHONPYCACHEPREFIX':str(ROOT/'build/pycache'),'TMPDIR':str(ROOT/'build/tmp')+'/'})
    suites=[]
    research=json.loads((ROOT/'research.json').read_text())['research']
    targets=[('snapshot',snap/'testes'),('economia',ROOT/research['economia']['path']/'testes'),('combate',ROOT/research['combate']['path']),('preview',ROOT/'testes')]
    for name,path in targets:
        p=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s',str(path),'-v'],cwd=ROOT,env=environment,text=True,capture_output=True)
        output=p.stdout+p.stderr;(ROOT/f'build/logs/testes-{name}.log').write_text(output)
        count=re.search(r'Ran (\d+) tests?',output);skip=re.search(r'skipped=(\d+)',output)
        result={'suite':name,'returncode':p.returncode,'tests':int(count[1]) if count else None,'skipped':int(skip[1]) if skip else 0,'log':f'build/logs/testes-{name}.log'}
        suites.append(result);print(json.dumps(result),flush=True)
        if p.returncode:print(output)
    report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':manifest['commit'],'x86Executed':False,'suites':suites,'passed':all(s['returncode']==0 for s in suites)}
    (ROOT/'build/logs/tests.json').write_text(json.dumps(report,indent=2)+'\n')
    return 0 if report['passed'] else 1
if __name__=='__main__':sys.exit(main())
