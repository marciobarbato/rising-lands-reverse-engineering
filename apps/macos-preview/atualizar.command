#!/bin/zsh
set -euo pipefail
PASTA_VISUALIZADOR="${0:A:h}"
cd "$PASTA_VISUALIZADOR"
export TMPDIR="$PASTA_VISUALIZADOR/build/tmp/"
export PYTHONPYCACHEPREFIX="$PASTA_VISUALIZADOR/build/pycache"
export PYTHONDONTWRITEBYTECODE=1
if [[ -x dependencies/python/bin/python3 ]]; then
  exec dependencies/python/bin/python3 -B scripts/atualizar.py "$@"
fi
exec /usr/bin/python3 -B scripts/atualizar.py "$@"
