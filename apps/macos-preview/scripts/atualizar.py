"""Snapshot commitado → assets → testes → .app → abertura real."""
from pathlib import Path
import argparse,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build import prepare_runtime,env

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--commit',default='HEAD',help='Commit/ref local para fixar; padrão HEAD')
    parser.add_argument('--cd',default=str(ROOT.parents[2]/'source/cd'),help='CD extraído, somente leitura')
    args=parser.parse_args()
    for d in ('build/tmp','build/logs','build/pycache'): (ROOT/d).mkdir(parents=True,exist_ok=True)
    prepare_runtime();python=ROOT/'dependencies/python/bin/python3'
    commands=[['scripts/snapshot.py','--commit',args.commit],['scripts/preparar_assets.py',args.cd],['scripts/testar.py'],['scripts/build.py'],['scripts/abrir_teste.py'],['scripts/verificar_pacote.py']]
    for cmd in commands:
        result=subprocess.run([str(python),'-B',*cmd],cwd=ROOT,env=env())
        if result.returncode:return result.returncode
    print('\nAtualização concluída. Abra dist/RisingLands-Preview.app. Instruções em LEIA-ME.md.')
    return 0
if __name__=='__main__':sys.exit(main())
