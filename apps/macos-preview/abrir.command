#!/bin/zsh
set -euo pipefail
PASTA_VISUALIZADOR="${0:A:h}"
exec open "$PASTA_VISUALIZADOR/dist/RisingLands-Preview.app"
