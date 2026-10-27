"""Importa/atualiza a análise local e exporta as evidências, sem executar o jogo."""
import subprocess
import sys
from pathlib import Path
from executar import RAIZ
from preparar_entrada import preparar


def main():
    preparar()
    projetos = RAIZ / 'ghidra/projetos'
    logs = RAIZ / 'ghidra/logs'
    projetos.mkdir(exist_ok=True)
    logs.mkdir(exist_ok=True)
    # A existência do projeto não garante a presença do programa normalizado;
    # -process falha explicitamente nesse caso, sem substituir dados existentes.
    if (projetos / 'RisingLands.gpr').exists():
        entrada = ['-process', 'RISING-analise.exe', '-noanalysis']
    else:
        entrada = ['-import', str(RAIZ / '.local/entrada/RISING-analise.exe'),
                   '-processor', 'x86:LE:32:default', '-cspec', 'windows',
                   '-analysisTimeoutPerFile', '300']
    comando = [sys.executable, str(RAIZ / 'ghidra/executar.py'), 'headless',
               str(projetos), 'RisingLands', *entrada,
               '-scriptPath', str(RAIZ / 'ghidra/scripts'),
               '-postScript', 'AnotarUnidades.java',
               '-postScript', 'ExportarUnidades.java', str(RAIZ / 'evidencias/ghidra'),
               '-max-cpu', '4', '-log', str(logs / 'analise.log'),
               '-scriptlog', str(logs / 'scripts.log')]
    subprocess.run(comando, cwd=RAIZ, check=True)
    # Alguns erros de script do Ghidra podem não alterar o código de saída.
    indice = RAIZ / 'evidencias/ghidra/exportacao.tsv'
    if not indice.exists() or any(not linha.endswith('\tOK') for linha in indice.read_text().splitlines()[1:]):
        raise SystemExit('Exportação incompleta; consultar ghidra/logs.')


if __name__ == '__main__':
    main()
