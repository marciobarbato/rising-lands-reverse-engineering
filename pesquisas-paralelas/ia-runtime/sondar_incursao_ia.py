"""M2.3 readiness probe (Python only; output under .local/, NOT evidence): the composition through the raid frames.

    python3 -B pesquisas-paralelas/ia-runtime/sondar_incursao_ia.py 40

It starts from the -v2 reference state after frame 1 with u32 0x508f7c set to 8999, so the next frame runs at
counter 9000, the forcing Combat's and this front's raid captures use. The checkpoint start is
``ComposicaoQuadros(inicio=1)`` with the reference allocation records and the between_frames entry registers.
Graphics' drawing-domain stops are bypassed (``planejamento``). The probe runs N frames, keeps the raid unit's
(16) record whenever it changes, and reports the first stop with its traceback. It finds the next missing
provider or contract before the Mac mini's M2.3 parts arrive; it proves nothing about equality.
"""
import json, struct, sys, time, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ambiente_ia_runtime
from composicao_quadros_ia import ComposicaoQuadros, carregar_cenario_exibicao
n = int(sys.argv[1])
estados, cap, entrada, m1 = carregar_cenario_exibicao()
estado = dict(estados['frame1'])
nome, (base, dados) = next((k, v) for k, v in estado.items() if v[0] <= 0x508f7c < v[0] + len(v[1]))
d = bytearray(dados); struct.pack_into('<I', d, 0x508f7c - base, 8999); estado[nome] = (base, bytes(d))
regs = next(p for p in cap['phases'] if p['phase'] == 'between_frames')['entry']['registers']
comp = ComposicaoQuadros(estado, cap, entrada, m1, inicio=1, alocacoes=cap['allocations'], regs_inicio=regs,
                         planejamento=True)
t0, ultimo, parada, unidade = time.time(), None, None, []
try:
    for r in comp.executar(n):
        ultimo = r['phase']
        if r['phase'].startswith('frame'):
            c = struct.unpack('<I', comp.mapa.ler(0x508f7c, 4))[0]
            base_u = struct.unpack('<I', comp.mapa.ler(0x4e19a0, 4))[0] + 16 * 276
            u = comp.mapa.ler(base_u, 276)
            if not unidade or unidade[-1][1] != u.hex():
                unidade.append((c, u.hex()))
except Exception as e:
    parada = dict(phase_after=ultimo, type=type(e).__name__, message=str(e)[:300], tb=traceback.format_exc()[-1800:])
out = dict(frames_requested=n, last_phase=ultimo, stop=parada, seconds=round(time.time() - t0, 1),
           graphics_planning_stops=len(comp.ctx.paradas_planejamento), unit16_changes=len(unidade),
           unit16=[(c, h[:16], h[0x7c*2:0x7e*2], h[16:18]) for c, h in unidade[:5] + unidade[-3:]])
from ambiente_ia_runtime import ROOT
(ROOT / '.local').mkdir(exist_ok=True)
json.dump(dict(out, unit16_full=unidade), open(ROOT / f'.local/m2-3-sonda-{n}.json', 'w'))
print(json.dumps(out, indent=1))
