#!/usr/bin/env python3
"""Executa o Ghidra portátil com dados de trabalho confinados ao repositório."""
import argparse
import os
from pathlib import Path
import subprocess

RAIZ = Path(__file__).resolve().parents[1]
GHIDRA = RAIZ / '.local/ghidra_12.2_PUBLIC'
JDK = RAIZ / '.local/jdk-25.0.5+8/Contents/Home'


def ambiente():
    env = os.environ.copy()
    env['JAVA_HOME'] = str(JDK)
    env['PATH'] = str(JDK / 'bin') + os.pathsep + env.get('PATH', '')
    propriedades = {
        'user.home': RAIZ / '.local/home',
        'java.io.tmpdir': RAIZ / '.local/tmp',
        'application.settingsdir': RAIZ / '.local/config',
        'application.cachedir': RAIZ / '.local/cache',
        'application.tempdir': RAIZ / '.local/tmp',
        'java.util.prefs.userRoot': RAIZ / '.local/config/java-prefs',
    }
    for caminho in propriedades.values():
        caminho.mkdir(parents=True, exist_ok=True)
    # O launcher do Java reconhece aspas em JAVA_TOOL_OPTIONS. Necessárias
    # porque o diretório Rising Lands contém espaço. Não usamos um shell.
    env['JAVA_TOOL_OPTIONS'] = ' '.join(f'-D{k}="{v}"' for k, v in propriedades.items())
    env['TMPDIR'] = str(RAIZ / '.local/tmp')
    env['XDG_CONFIG_HOME'] = str(RAIZ / '.local/config')
    env['XDG_CACHE_HOME'] = str(RAIZ / '.local/cache')
    env['GRADLE_USER_HOME'] = str(RAIZ / '.local/cache/gradle')
    return env


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('modo', choices=['gui', 'headless', 'java'])
    parser.add_argument('argumentos', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    programas = {'gui': GHIDRA / 'ghidraRun',
                 'headless': GHIDRA / 'support/analyzeHeadless',
                 'java': JDK / 'bin/java'}
    programa = programas[args.modo]
    if not programa.exists():
        raise SystemExit('Instalação ausente. Execute python3 ghidra/instalar.py.')
    raise SystemExit(subprocess.call([str(programa), *args.argumentos], env=ambiente(), cwd=RAIZ))


if __name__ == '__main__':
    main()
