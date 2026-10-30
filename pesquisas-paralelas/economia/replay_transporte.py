"""CPU-free replay of the committed transport capture against ``transporte`` (and the state-19 bodies against
``alimentacao`` composed with ``restauracao``).

Every recorded CalculTransporteEngin, CalculDechargeCaveEngin and state-19 body is replayed over a sparse memory
holding exactly the bytes the original read before writing in that call (``read_before_write``); a translation that
reads any other byte fails. Other fronts' callees are the original's own nested calls (``validar_transporte.Replay``);
Economy's own callees run in-process. The result must match the exit registers and the final value of every byte the
original changed, and every byte the translation wrote must end equal to the original's last store there.

    python3 -B pesquisas-paralelas/economia/replay_transporte.py [--core]
"""
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import replay_restauracao as rr  # noqa: E402
import transporte as tr  # noqa: E402
from validar_ciclo_trabalho import carregar  # noqa: E402
from validar_transporte import CAPTURA, TRADUZIDAS, executar_traducao  # noqa: E402

# A transport callee reached without the original's call (an extra or reordered call) is an error, like the restore
# routines' own dependency errors.
rr.ERROS = rr.ERROS + (tr.DependenciaTransporte,)


def replay(captura, executar=executar_traducao):
    contagem, falhas = {}, []
    for r in captura['calls']:
        if r['routine'] not in TRADUZIDAS:
            continue
        resultado, d = rr.replay_chamada(r, executar)
        c = contagem.setdefault(r['routine'], dict(match=0, mismatch=0, outside_domain=0, error=0))
        c[resultado] += 1
        if resultado != 'match':
            falhas.append(dict(d, outcome=resultado))
    return contagem, falhas


def com_core(nome, m, resultado):
    from validar_alimentacao import provedores_fadiga
    return executar_traducao(nome, m, resultado, provedores_fadiga())


if __name__ == '__main__':
    contagem, falhas = replay(carregar(CAPTURA)[0], com_core if '--core' in sys.argv else executar_traducao)
    print(json.dumps(contagem, indent=1))
    for f in falhas[:40]:
        print(json.dumps(f))
    sys.exit(1 if falhas else 0)
