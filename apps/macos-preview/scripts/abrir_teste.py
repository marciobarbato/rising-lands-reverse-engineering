"""Launch the legacy preview with the shared bounded readiness smoke runner."""
from pathlib import Path
import json
import os
import sys
from native_smoke import run_native_smoke

ROOT=Path(__file__).resolve().parents[1]


def main():
    report=ROOT/'build/logs/abertura.json'
    screenshot=ROOT/'build/logs/abertura.png'
    app=ROOT/'dist/RisingLands-Preview.app'
    code,result,log,previous=run_native_smoke(app,report,screenshot,os.environ.copy())
    (ROOT/'build/logs/launchservices.log').write_text(log+'\nPrevious evidence: '+str(previous))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if not code and result.get('passed') and result.get('nativeWindowVisible') else 1


if __name__=='__main__':sys.exit(main())
