"""Original-only isolated captures of the Missions frame callees at exact frame inputs.

Reruns the committed first-frame path (accepted M1 startup and MissionLoad,
load_tail, between_frames, frame1) with ``oraculo_quadro_missao.Isolamento``
pausing at EvenementEnCours 0x4581b6 and TestFinDeMission 0x458606.  Each call
is executed natively in isolation on the exact saved state (AL, registers,
changed bytes, bytes read before written with entry values) and the state is
restored; the phases then continue.  The run must still reproduce every
committed phase state and the entry trace, which proves the restorations are
exact.  No Python translation is imported.

    python3 -B pesquisas-paralelas/missoes/capturar_isolados_quadro1.py \
        --saida pesquisas-paralelas/missoes/evidencias/captura-isolada-missoes-quadro1.json
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time

import ambiente_missoes
import capturar_quadro_missao_original as cq
from emulador import HASH_ORIGINAL
from oraculo_quadro_missao import BancadaQuadroMissaoOriginal, Isolamento

ROOT = ambiente_missoes.ROOT
OWNED = ambiente_missoes.OWNED
CAPTURA = OWNED/'evidencias/captura-quadro1-monde01-original.json'
ROTINAS = ('EvenementEnCours', 'TestFinDeMission')


def executar(perturbacoes=None, observador=None, injecoes=None, rotinas=ROTINAS):
    cap = json.loads(CAPTURA.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaQuadroMissaoOriginal(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    iso = Isolamento(b, rotinas, perturbacoes, observador, injecoes)
    iso.instalar()
    resumos = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(120)),
                         ('frame1', lambda: b.executar_quadro(600))):
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    saida = ROOT/a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'pesquisas-paralelas/missoes'],
                          capture_output=True, text=True).stdout
    t0 = time.monotonic()
    b, iso, cap, reproducao = executar()
    relatorio = dict(
        schema='rising-lands/monde01-frame1-isolated-missions-calls/1', original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, source_dirty_paths=sujo.splitlines(),
        source_sha256={n: hashlib.sha256((OWNED/n).read_bytes()).hexdigest()
                       for n in ('oraculo_quadro_missao.py', 'capturar_isolados_quadro1.py')},
        frame_capture=dict(path=str(CAPTURA.relative_to(ROOT)), sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        routines=list(ROTINAS), path_reproduction=reproducao, calls=iso.registros,
        method='Native call from the exact saved entry state to its stack return; local Unicorn read/write '
               'hooks (translation cache flushed) over DGROUP+.bss, CRT thread page, active allocations and '
               'the native stack; stack bytes at or above the exit ESP that the call read (caller arguments) are '
               'listed, the return slot and the callee frame below it are excluded; state restored after each case',
        seconds=round(time.monotonic()-t0, 3))
    resultado = 0 if reproducao['passed'] and all(c['reached_return'] for r in iso.registros for c in r['cases']) else 2
    if resultado:
        saida = ROOT/'.local'/('m2-isolated-failed-'+time.strftime('%Y%m%dT%H%M%S')+'.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), sha256=hashlib.sha256(saida.read_bytes()).hexdigest(),
                          reproduction=reproducao,
                          calls=[dict(routine=r['routine'], phase=r['phase'], al=r['cases'][0]['al'],
                                      changed=len(r['cases'][0]['changed_bytes']),
                                      reads=len(r['cases'][0]['read_before_write'])) for r in iso.registros],
                          seconds=relatorio['seconds']), indent=1))
    return resultado


if __name__ == '__main__':
    sys.exit(main())
