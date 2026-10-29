"""Register view of the committed MONDE01 first-frame entry trace (for the frame pipeline).

Reruns the committed path (accepted M1 startup and MissionLoad, load_tail,
between_frames, frame1) with the intact executable only and logs every routine
entry in order as ``callee@caller+off EAX EDX EBX ECX`` (bare lowercase hex,
the AI/runtime capture format; a caller that is the bench trampoline prints
as 0x3000000).  The run must reproduce every committed phase state, and the
per-routine entry counts of the log must equal the committed trace.

    python3 -B pesquisas-paralelas/missoes/publicar_rastro_registradores_quadro1.py \
        --saida pesquisas-paralelas/missoes/evidencias/rastro-registradores-quadro1-monde01.json
"""
import argparse
from collections import Counter
import hashlib
import json
import subprocess
import sys

import ambiente_missoes
import capturar_quadro_missao_original as cq
from emulador import HASH_ORIGINAL
from oraculo_quadro_missao import BancadaQuadroMissaoOriginal

ROOT, OWNED = ambiente_missoes.ROOT, ambiente_missoes.OWNED
CAPTURA = OWNED/'evidencias/captura-quadro1-monde01-original.json'
RASTRO = OWNED/'evidencias/rastro-quadro1-monde01.json'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    saida = ROOT/a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    cap, rastro = json.loads(CAPTURA.read_bytes()), json.loads(RASTRO.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaQuadroMissaoOriginal(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    b.linhas_registradores = {}
    resumos = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(120)),
                         ('frame1', lambda: b.executar_quadro(600))):
        correr()
        resumos[nome] = b.resumo_imagem(b.imagem())
    fases = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    contagens = {}
    for fase, linhas in b.linhas_registradores.items():
        log = Counter(l.split('@')[0] for l in linhas)
        comprometido = {r['routine']: r['entries'] for r in rastro['phases'][fase]['routines_in_first_entry_order']}
        contagens[fase] = dict(log) == comprometido
    fronteiras = sorted({e['routine'] for p in cap['phases'] for e in p['boundaries']})
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'pesquisas-paralelas/missoes'],
                          capture_output=True, text=True).stdout
    doc = dict(schema='rising-lands/monde01-frame1-register-trace/1', original_sha256=HASH_ORIGINAL,
               translation_executed=False, source_revision=revisao, source_dirty_paths=sujo.splitlines(),
               capture=dict(path=str(CAPTURA.relative_to(ROOT)), sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
               trace=dict(path=str(RASTRO.relative_to(ROOT)), sha256=hashlib.sha256(RASTRO.read_bytes()).hexdigest()),
               format='callee@caller+off EAX EDX EBX ECX: registers at the first instruction of the callee '
                      '(a basic block starting at its symbol address), bare lowercase hex; every entry in order',
               not_executed_boundaries=fronteiras,
               boundary_note='boundary routines appear at their entry; their bodies are not executed',
               phase_states_equal={f: resumos[f] == fases[f] for f in fases}, counts_equal_committed_trace=contagens,
               phases={f: dict(entries=len(l), sha256=hashlib.sha256('\n'.join(l).encode()).hexdigest(), lines=l)
                       for f, l in b.linhas_registradores.items()})
    ok = all(doc['phase_states_equal'].values()) and all(contagens.values()) and len(contagens) == 3
    if not ok:
        saida = ROOT/'.local'/'m2-register-trace-failed.json'
    with open(saida, 'x') as f:
        json.dump(doc, f, indent=1)
        f.write('\n')
    print(json.dumps({k: v for k, v in doc.items() if k != 'phases'} | {
        'entries': {f: p['entries'] for f, p in doc['phases'].items()}, 'output': str(saida)}, indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
