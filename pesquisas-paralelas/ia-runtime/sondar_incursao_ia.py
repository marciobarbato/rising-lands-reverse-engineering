"""M2.3 readiness probe (Python only; output under .local/, NOT evidence): the composition through the raid frames.

    python3 -B pesquisas-paralelas/ia-runtime/sondar_incursao_ia.py 2200

It starts exactly as the native raid captures force their input (Combat 1e9f28e/a1f589a, this front's
``capturar_*_incursao_ia``): from the -v2 reference state after between_frames (frame 1's CalculGame entry), with
u32 0x508f7c written to 9000, frame 1 runs as the counter-9000 frame. ``fase_quadro`` runs that frame, then
``ComposicaoQuadros(inicio=1)`` continues with between_frames2, frame2 and so on, using the reference allocation
records and entry registers. Graphics' drawing-domain stops are bypassed (``planejamento``).

The output gives the world RNG and raid unit 16's state, facing and cell at every frame end, its full record
whenever it changes, and the first stop with its traceback. The per-counter values compare directly with native
probes and with Combat's course capture. The probe finds the next missing provider or contract; it proves nothing
about equality.

An earlier version started after frame 1 with the counter set to 8999. That consumes one extra frame of draws
before the raid and is not equivalent to the native forcing. Its apparent movement divergence after counter 9716
was this artifact.
"""
import json
from pathlib import Path
import struct
import sys
import time
import traceback

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente_ia_runtime import ROOT  # noqa: E402
from composicao_encadeada_ia import Registro, fase_quadro  # noqa: E402
from composicao_quadros_ia import ComposicaoQuadros, carregar_cenario_exibicao  # noqa: E402

CONTADOR, RNG, UNIDADES, UNIDADE = 0x508f7c, 0x497164, 0x4e19a0, 16


def main():
    n = int(sys.argv[1])
    estados, cap, entrada, m1 = carregar_cenario_exibicao()
    fases = {p['phase']: p for p in cap['phases']}
    estado = dict(estados['between_frames'])
    nome, (base, dados) = next((k, v) for k, v in estado.items() if v[0] <= CONTADOR < v[0] + len(v[1]))
    d = bytearray(dados)
    struct.pack_into('<I', d, CONTADOR - base, 9000)
    estado[nome] = (base, bytes(d))
    comp = ComposicaoQuadros(estado, cap, entrada, m1, inicio=1, alocacoes=cap['allocations'],
                             regs_inicio=fases['between_frames']['entry']['registers'], planejamento=True)
    u32 = lambda a: struct.unpack('<I', comp.mapa.ler(a, 4))[0]  # noqa: E731
    por_contador, registros = {}, []

    def gravar():
        u = comp.mapa.ler(u32(UNIDADES) + UNIDADE * 276, 276)
        c = u32(CONTADOR)
        por_contador[c] = dict(rng=hex(u32(RNG)), state=u[2], facing=[u[0x90], u[0x91], u[0x92]], cell=hex(u[8] | u[9] << 8))
        if not registros or registros[-1][1] != u.hex():
            registros.append((c, u.hex()))
    t0, parada = time.time(), None
    try:
        fase_quadro(comp.mapa, comp.prov, comp.ctx, Registro('frame1'), comp.travessias,
                    {k: int(v, 16) for k, v in fases['frame1']['entry']['registers'].items()}, fase='frame1')
        gravar()
        for r in comp.executar(n - 1):
            if r['phase'].startswith('frame'):
                gravar()
    except Exception as e:  # reported: the probe stops here
        parada = dict(type=type(e).__name__, message=str(e)[:300], tb=traceback.format_exc()[-1800:])
    saida = dict(evidence=False, forcing='-v2 state after between_frames, counter 9000, frame 1 = counter 9000',
                 frames=len(por_contador), last_counter=max(por_contador) if por_contador else None, stop=parada,
                 seconds=round(time.time() - t0, 1), graphics_planning_stops=len(comp.ctx.paradas_planejamento),
                 per_counter=por_contador, unit16_records=registros)
    (ROOT / '.local').mkdir(exist_ok=True)
    caminho = ROOT / f'.local/m2-3-sonda-{n}.json'
    caminho.write_text(json.dumps(saida))
    print(json.dumps({k: saida[k] for k in ('frames', 'last_counter', 'seconds', 'graphics_planning_stops')}
                     | dict(stop=parada and {k: parada[k] for k in ('type', 'message')}, output=str(caminho)), indent=1))


if __name__ == '__main__':
    main()
