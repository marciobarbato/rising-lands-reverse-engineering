"""Build the native pass-2 hook library (ferramentas/nativo/ganchos_memoria.c) into .local/nativo/.

Deterministic: the system clang, fixed flags, no timestamps.  The library
embeds an identity, the sha256 of the source bytes and of the exact flag list,
and ``ganchos_nativos`` refuses to load a library whose identity differs from
the current source and flags (stale build).  The binary is local and ignored;
it is never committed.

    python3 -B ferramentas/compilar_ganchos_nativos.py
"""
import hashlib
import os
from pathlib import Path
import subprocess
import sys

RAIZ = Path(__file__).resolve().parents[1]
FONTE = RAIZ / 'ferramentas/nativo/ganchos_memoria.c'
BIBLIOTECA = RAIZ / '.local/nativo/libganchos_memoria.dylib'
COMPILADOR = '/usr/bin/clang'
OPCOES = ('-std=c11', '-O2', '-fPIC', '-dynamiclib', '-Wall', '-Wextra', '-Werror',
          '-Wl,-install_name,@rpath/libganchos_memoria.dylib')


def identidade(fonte=FONTE):
    """sha256 over the source bytes and the flag list: the identity the library must embed."""
    h = hashlib.sha256()
    h.update(Path(fonte).read_bytes())
    h.update(b'\0' + '\0'.join(OPCOES).encode())
    return h.hexdigest()


def comando(saida=BIBLIOTECA, fonte=FONTE):
    """clang command line, run from the repository root with a relative source path (no absolute path embedded)."""
    fonte = Path(fonte).resolve()
    relativa = fonte.relative_to(RAIZ) if RAIZ in fonte.parents else fonte
    return [COMPILADOR, *OPCOES, f'-DGANCHOS_IDENTIDADE="sha256={identidade(fonte)}"', '-o', str(saida),
            str(relativa)]


def compilar(saida=BIBLIOTECA, fonte=FONTE):
    saida = Path(saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    temporario = saida.with_name(saida.name + '.tmp')
    if temporario.exists():
        temporario.unlink()
    subprocess.run(comando(temporario, fonte), check=True, cwd=RAIZ, env=dict(os.environ, ZERO_AR_DATE='1'))
    os.replace(temporario, saida)
    return saida


def main():
    saida = compilar()
    print(f'{saida.relative_to(RAIZ)} sha256={hashlib.sha256(saida.read_bytes()).hexdigest()} '
          f'identity={identidade()}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
