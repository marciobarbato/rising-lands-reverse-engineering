"""Original-only isolated captures of Core callees at the exact MONDE01 frame-0/frame-1 inputs.

Reruns the committed Missions first-frame path (accepted M1 startup and
MissionLoad, then load_tail = "frame 0", between_frames, frame1) on the intact
executable and pauses with ``oraculo_quadro_missao.Isolamento`` at every entry
of the Core-owned callees that the Missions entry trace
(``pesquisas-paralelas/missoes/evidencias/rastro-quadro1-monde01.json``)
reaches. Each call runs natively in isolation from its exact saved entry state
to its stack return under local read/write hooks (Unicorn translation cache
flushed after the hooks are added, so cached blocks cannot under-count reads),
records registers, changed bytes and the bytes read before written with their
entry values, then the exact state is restored and the phase continues. The
rerun must still reproduce every committed phase state, boundary log and the
entry trace, which proves each restoration exact. No Python translation is
imported or executed.

    python3 -B ferramentas/capturar_chamadas_core_quadro1.py \
        --saida evidencias/fundacoes-quadro/captura-chamadas-quadro1.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
MISSOES = RAIZ / 'pesquisas-paralelas/missoes'
if str(MISSOES) not in sys.path:
    sys.path.insert(0, str(MISSOES))

# Core-owned callees reached in frame 0 (load_tail) and frame 1, in trace order.
ROTINAS = ('GameNextFrame', 'GetBit', 'CalculFatigue', 'SetEnginCollision', 'SetCollision',
           'Chemin_ModifieZone', 'Random', 'BatimentGetCase', 'BatimentCollision', 'CaseEstDecouverte',
           'BatimentEstDecouvert', 'BatimentContourEstIllumine', 'CaseEstIlluminee', 'SetBit')
SAIDA_FALHA = RAIZ / '.local/frame'


def executar(rotinas=ROTINAS, observador=None):
    """Run the committed path with isolation; returns (bench, isolation, frame capture, reproduction)."""
    import capturar_isolados_quadro1 as ci
    from oraculo_quadro_missao import BancadaQuadroMissaoOriginal, Isolamento
    import capturar_quadro_missao_original as cq
    cap = json.loads(ci.CAPTURA.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaQuadroMissaoOriginal(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    iso = Isolamento(b, rotinas, None, observador)
    iso.instalar()
    resumos = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(1800)),
                         ('between_frames', lambda: b.executar_entre_quadros(120)),
                         ('frame1', lambda: b.executar_quadro(1800))):
        correr()
        resumos[nome] = b.resumo_imagem(b.imagem())
    fases = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao = dict(phase_states_equal={f: resumos[f] == fases[f] for f in fases},
                      entry_trace_equal=json.loads(json.dumps(b.rastro_json())) == cap['entry_trace'],
                      boundaries_equal=b.eventos_fronteira == [e for p in cap['phases'] for e in p['boundaries']],
                      code_after=b.sha256_codigo(), code_unchanged=b.sha256_codigo() == cap['code_integrity']['after'])
    reproducao['passed'] = (all(reproducao['phase_states_equal'].values()) and reproducao['entry_trace_equal']
                            and reproducao['boundaries_equal'] and reproducao['code_unchanged'])
    return b, iso, cap, reproducao


def _compactar(registro):
    """One isolated call: drop the empty perturbation and the EIP/ESP duplicates kept elsewhere."""
    c, = registro['cases']
    return dict(routine=registro['routine'], phase=registro['phase'], caller=registro['caller'],
                caller_return=registro['caller_return'], entry_registers=c['entry_registers'],
                exit_registers=c['exit_registers'], reached_return=c['reached_return'],
                changed_bytes=c['changed_bytes'], read_before_write=c['read_before_write'])


def main():
    from emulador import HASH_ORIGINAL
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    saida = RAIZ / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    t0 = time.monotonic()
    b, iso, cap, reproducao = executar()
    chamadas = [_compactar(r) for r in iso.registros]
    contagem = {}
    for c in chamadas:
        chave = f"{c['phase']}:{c['routine']}"
        contagem[chave] = contagem.get(chave, 0) + 1
    relatorio = dict(
        schema='rising-lands/monde01-frame1-isolated-core-calls/1', original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao,
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest()
                       for p in ('ferramentas/capturar_chamadas_core_quadro1.py',
                                 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py')},
        input='exact MONDE01 frame inputs: load_tail is frame 0 (the load-state CalculGame body), frame1 the '
              'second pass; Missions capture named inputs unchanged',
        frame_capture=dict(path='pesquisas-paralelas/missoes/evidencias/captura-quadro1-monde01-original.json',
                           sha256=hashlib.sha256((MISSOES / 'evidencias/captura-quadro1-monde01-original.json')
                                                 .read_bytes()).hexdigest()),
        routines={n: hex(b.sym[n]) for n in ROTINAS}, path_reproduction=reproducao, call_counts=contagem,
        method='Native call from the exact saved entry state to its stack return; local Unicorn read/write hooks '
               '(translation cache flushed after hook_add) over DGROUP+.bss, CRT thread page, active allocations '
               'and the native stack; stack bytes at or above the exit ESP that the call read are listed (caller '
               'arguments), the callee frame below it is excluded; nested isolated routines run natively inside '
               'their caller\'s isolated call and are isolated again at their own entry when the phase resumes; '
               'state restored after each call',
        calls=chamadas, seconds=round(time.monotonic() - t0, 3))
    ok = reproducao['passed'] and all(c['reached_return'] for c in chamadas)
    if not ok:
        saida = SAIDA_FALHA / ('core-calls-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), sha256=hashlib.sha256(saida.read_bytes()).hexdigest(),
                          reproduction=reproducao, call_counts=contagem, seconds=relatorio['seconds']), indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
