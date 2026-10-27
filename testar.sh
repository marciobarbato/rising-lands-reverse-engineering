#!/bin/sh
set -eu
cd "$(dirname "$0")"
"${RISING_PYTHON:-python3}" -m unittest discover -s testes -p 'test_*.py' -v
