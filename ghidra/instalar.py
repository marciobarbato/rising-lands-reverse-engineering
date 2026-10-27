"""Reproduz a instalação portátil macOS/ARM64 a partir do manifesto fixado.

Exige curl, unzip, tar, make e clang++ (Xcode Command Line Tools). Não altera
o sistema, o perfil do shell ou o executável original do jogo.
"""
from pathlib import Path
import hashlib
import json
import platform
import shutil
import subprocess

from executar import ambiente, GHIDRA, JDK, RAIZ


def main():
    if platform.system() != 'Darwin' or platform.machine() != 'arm64':
        raise SystemExit('Esta receita está fixada para macOS Apple Silicon.')
    manifesto = json.loads((RAIZ / 'ghidra/instalacao.json').read_text())
    downloads = RAIZ / '.local/downloads'
    downloads.mkdir(parents=True, exist_ok=True)
    for componente, nome in [('ghidra', 'ghidra.zip'), ('jdk', 'jdk.tar.gz')]:
        pacote = manifesto[componente]
        destino = downloads / nome
        if not destino.exists():
            parcial = destino.with_suffix(destino.suffix + '.part')
            subprocess.run(['curl', '-fL', '--retry', '3', pacote['url'], '-o', str(parcial)], check=True)
            parcial.replace(destino)
        if hashlib.sha256(destino.read_bytes()).hexdigest() != pacote['sha256']:
            raise SystemExit('Checksum incorreto: ' + nome)
    if not GHIDRA.exists():
        subprocess.run(['unzip', '-q', str(downloads / 'ghidra.zip'), '-d', str(RAIZ / '.local')], check=True)
    if not JDK.exists():
        subprocess.run(['tar', '-xzf', str(downloads / 'jdk.tar.gz'), '-C', str(RAIZ / '.local')], check=True)
    binario = GHIDRA / 'Ghidra/Features/Decompiler/os/mac_arm_64/decompile'
    if not binario.exists():
        fonte = GHIDRA / 'Ghidra/Features/Decompiler/src/decompile/cpp'
        logs = RAIZ / 'ghidra/logs'
        logs.mkdir(exist_ok=True)
        with (logs / 'compilacao.log').open('w') as log:
            subprocess.run(['make', '-j6', 'ghidra_opt', 'CXX=clang++ -std=c++11',
                            'ARCH_TYPE=-arch arm64', 'ADDITIONAL_FLAGS=-mmacosx-version-min=11.0 -w',
                            'OSDIR=mac_arm_64'], cwd=fonte, env=ambiente(),
                           stdout=log, stderr=subprocess.STDOUT, check=True)
        binario.parent.mkdir(exist_ok=True)
        shutil.copy2(fonte / 'ghidra_opt', binario)
    subprocess.run([str(JDK / 'bin/java'), '-version'], env=ambiente(), check=True)
    print('Ghidra e descompilador ARM64 disponíveis em', GHIDRA)


if __name__ == '__main__':
    main()
