"""Abre o .app via LaunchServices e testa a interface real, sem automação externa."""
from pathlib import Path
import json,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]

def main():
    log=ROOT/'build/logs/abertura.json';shot=ROOT/'build/logs/abertura.png'
    for p in (log,shot):
        if p.exists():p.unlink()
    app=ROOT/'dist/RisingLands-Preview.app'
    command=['open','-W','-n',str(app),'--args','--smoke-test',str(log),'--screenshot',str(shot)]
    print('Abrindo janela nativa e exercitando a interface…',flush=True)
    p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60)
    (ROOT/'build/logs/launchservices.log').write_text(p.stdout+p.stderr)
    if p.returncode or not log.exists():
        print('Teste de abertura falhou:',p.returncode,p.stdout,p.stderr);return 1
    report=json.loads(log.read_text())
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report.get('passed') or not report.get('nativeWindowVisible') or not shot.exists():return 1
    return 0
if __name__=='__main__':sys.exit(main())
