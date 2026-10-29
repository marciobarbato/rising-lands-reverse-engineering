"""Lossless run encoding of an isolated-call capture (``read_before_write``/``changed_bytes``).

``read_before_write`` [[addr, value|None, reader], ...] becomes runs
[[start, hex values | None, count, reader]] of consecutive addresses with the same
reader (a run of unknown values - freed pages - keeps None and its count);
``changed_bytes`` [[addr, old, new], ...] becomes runs [[start, old hex, new hex]].
Everything else is copied. ``expandir`` restores the exact original lists, and the
compact file records the SHA-256 of the raw capture it encodes.

    python3 -B ferramentas/compactar_captura_isolada.py RAW.json --saida COMPACT.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def _runs_leitura(lista):
    runs = []
    for a, v, leitor in lista:
        a = int(a, 16)
        if runs:
            inicio, valores, n, l = runs[-1]
            if l == leitor and inicio + n == a and (valores is None) == (v is None):
                runs[-1][2] += 1
                if v is not None:
                    runs[-1][1] += f'{v:02x}'
                continue
        runs.append([a, None if v is None else f'{v:02x}', 1, leitor])
    return [[hex(a), v, n, l] for a, v, n, l in runs]


def _runs_mudanca(lista):
    runs = []
    for a, velho, novo in lista:
        a = int(a, 16)
        if runs and runs[-1][0] + len(runs[-1][1]) // 2 == a:
            runs[-1][1] += f'{velho:02x}'
            runs[-1][2] += f'{novo:02x}'
        else:
            runs.append([a, f'{velho:02x}', f'{novo:02x}'])
    return [[hex(a), v, n] for a, v, n in runs]


def compactar(chamada):
    c = dict(chamada)
    c['read_before_write'] = _runs_leitura(chamada['read_before_write'])
    c['changed_bytes'] = _runs_mudanca(chamada['changed_bytes'])
    return c


def expandir(chamada):
    """Inverse of ``compactar`` for one call record."""
    c = dict(chamada)
    leituras = []
    for a, valores, n, leitor in chamada['read_before_write']:
        a = int(a, 16)
        for i in range(n):
            leituras.append([hex(a + i), None if valores is None else int(valores[2 * i:2 * i + 2], 16), leitor])
    mudancas = []
    for a, velhos, novos in chamada['changed_bytes']:
        a = int(a, 16)
        for i in range(len(velhos) // 2):
            mudancas.append([hex(a + i), int(velhos[2 * i:2 * i + 2], 16), int(novos[2 * i:2 * i + 2], 16)])
    c['read_before_write'], c['changed_bytes'] = leituras, mudancas
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('bruta')
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    bruta = Path(a.bruta).read_bytes()
    dados = json.loads(bruta)
    compacta = dict(dados, calls=[compactar(c) for c in dados['calls']],
                    encoding=dict(scheme='rising-lands/isolated-call-runs/1', raw_sha256=hashlib.sha256(bruta).hexdigest(),
                                  raw_bytes=len(bruta), decoder='ferramentas/compactar_captura_isolada.py:expandir'))
    if [expandir(c) for c in compacta['calls']] != dados['calls']:
        raise SystemExit('Run encoding is not lossless')
    saida = Path(a.saida)
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    saida.write_text(json.dumps(compacta, indent=None, sort_keys=True, separators=(',', ':')) + '\n')
    print(saida, saida.stat().st_size, 'bytes from', len(bruta))


if __name__ == '__main__':
    sys.exit(main())
