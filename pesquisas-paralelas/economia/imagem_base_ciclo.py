"""Native dump of the whole mapped state at frame 2's CalculGame entry of the work-cycle bench (before any declared
action), the base image of ``compor_ciclo_trabalho``: Core's live world binds every grid and pointer table when it
is built, so a CPU-free composition needs the bytes no single recorded call reads.

    python3 "…/heavy_lease.py" economy -- python3 -B pesquisas-paralelas/economia/imagem_base_ciclo.py \\
        --saida .local/caverna/imagem-base-ciclo-quadro2.bin.xz
"""
import argparse
import hashlib
import lzma
from pathlib import Path
import pickle
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    from bancada_ciclo_trabalho import Ciclo
    imagem = {}

    def ordens(c, k):
        if k == 2 and not imagem:
            imagem.update({n: (base, bytes(d)) for n, (base, d) in c.b.imagem().items()})
        return iter(())

    c = Ciclo((), lambda *x: False, ordens)
    c.executar(2)
    bruto = pickle.dumps(dict(frame=2, reproduction=c.reproducao, blocks=imagem), protocol=4)
    Path(RAIZ / a.saida).parent.mkdir(parents=True, exist_ok=True)
    Path(RAIZ / a.saida).write_bytes(lzma.compress(bruto, preset=6))
    print(dict(blocks=len(imagem), bytes=sum(len(d) for _, d in imagem.values()), reproduction=c.reproducao,
               sha256=hashlib.sha256(bruto).hexdigest()))


if __name__ == '__main__':
    main()
