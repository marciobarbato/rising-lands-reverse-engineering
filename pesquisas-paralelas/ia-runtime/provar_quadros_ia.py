"""M2.2 formal 128-frame equality proof (AI/runtime): the Python N-frame chain against Missions' original capture.

    python3 -B pesquisas-paralelas/ia-runtime/provar_quadros_ia.py \
        --saida pesquisas-paralelas/ia-runtime/validacao/m2-2-prova-128-quadros.json

Python only; the native side is the committed capture.

- **Reference:** ``captura-quadros128-monde01-exibicao-v2.json.xz`` (257 phases in delta form, full states at the
  checkpoint frames). The raw JSON SHA-256 is pinned, and every phase's replay summary and every checkpoint full
  state are checked before Python is compared.
- **Policy:** ``m2-2-politica-comparacao-128-quadros.json``. Only its cumulative ``exclusion_mask`` excludes bytes.
- **Composition:** ``composicao_quadros_ia`` (mode 'prova', zero crossings), ONE map from the -v2 MissionLoad
  final state through load_tail and frames 1..128.
- **Per phase** (``comparar_quadros_ia.comparar``):
  - every state byte outside the mask;
  - both RNGs;
  - the bindings and boundaries outside display context;
  - the allocation-record count;
  - the between-frames exit registers and the carried entry registers.

  After the last phase, the full allocation records are compared.

The first difference stops the proof. Its writer needs a native watch rerun (Mac mini). The output goes under
``.local/`` unless the tree is clean and every phase is equal.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time

from ambiente_ia_runtime import ROOT
from comparar_quadros_ia import comparar

CAPTURA = ROOT / 'pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz'
MANIFESTO = ROOT / 'pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.manifest.json'
POLITICA = ROOT / 'pesquisas-paralelas/missoes/validacao/m2-2-politica-comparacao-128-quadros.json'
SHA_BRUTO = '1ad031b96300e5c632fd5b6b7857ae30792f78e86531e4f17d1bf7124c6dd930'
SHA_XZ = '4c8f5c14a9623131dd019eafcdc49ea63054ee358f9defde58c12cb949f59ff3'


def sha(caminho):
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def bytes_mistos(politica):
    """Compared bytes with a display-context writer: Python must reproduce their value at every phase end."""
    saida = {}
    for endereco, v in politica['game_logic_bytes'].items():
        exibicao = [w for w in v['writers'] if w.split(':')[0] in ('display', 'backend')]
        if exibicao:
            saida[endereco] = dict(block=v['block'], display_writers=exibicao,
                                   logic_writers=[w for w in v['writers'] if w not in exibicao],
                                   readers=v['readers'])
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    saida = ROOT / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    if sha(CAPTURA) != SHA_XZ:
        raise SystemExit('The capture file is not the committed xz artifact')
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain'], capture_output=True, text=True).stdout
    t0 = time.monotonic()
    politica = json.loads(POLITICA.read_bytes())
    corpo = comparar(CAPTURA, POLITICA, None, SHA_BRUTO)
    fases = corpo['phases']
    mistos = bytes_mistos(politica)
    tabela = {}
    for nome, r in fases.items():
        tabela[nome] = dict(
            equal=r['equal'], compared_bytes=r.get('state', {}).get('compared_bytes'),
            rng=r.get('rng', {}).get('equal'), bindings=r.get('bindings', {}).get('equal'),
            boundaries=r.get('boundaries', {}).get('equal'), allocation_count=r.get('allocation_count', {}).get('equal'),
            registers=all(v['equal'] for v in r.get('registers', {}).values()) if 'registers' in r else None,
            carried_registers=all(v['equal'] for v in r.get('carried_entry_registers', {}).values())
            if 'carried_entry_registers' in r else None,
            display_context_bindings_not_modeled=r.get('bindings', {}).get('display_context_not_modeled'),
            display_context_boundaries_not_modeled=r.get('boundaries', {}).get('display_context_not_modeled'),
            shared_issuers_matched=len(r.get('bindings', {}).get('shared_issuers_matched', [])) +
            len(r.get('boundaries', {}).get('shared_issuers_matched', [])),
            reference_integrity=r.get('reference_integrity'))
    resultado = corpo['summary']['result']
    relatorio = dict(
        schema='rising-lands/ai-runtime-m2.2-128-frame-proof/1', source_revision=revisao,
        source_dirty_paths=sujo.splitlines(),
        capture=dict(corpo['capture'], xz_sha256=SHA_XZ, manifest=dict(path=str(MANIFESTO.relative_to(ROOT)),
                                                                       sha256=sha(MANIFESTO))),
        policy=dict(corpo['policy'], source_revision=politica['source_revision'], totals=politica['cumulative']['totals'],
                    exclusion_ranges=len(politica['cumulative']['exclusion_mask']), passed=politica['passed']),
        crossings=dict(count=0, writing_compared_bytes=0,
                       note='the composition crosses nothing; every routine is a Python provider or a display root '
                            'whose state writes are masked or modeled'),
        compared_bytes_with_display_writers=dict(
            bytes=mistos,
            handling={'0x4e05a2': 'AffGame store modeled (affgame_hud_ia); CalculMatiere is Economy\'s provider',
                      'clip words 0x49a01e/1f, 0x49a022/23': 'RestaureClipping (display) writes back the values '
                                                                'SaveClipping saved; SetClipping (logic) is Core\'s '
                                                                'provider. Equality at every phase end is checked '
                                                                'below'}),
        hud_flag=corpo['hud_flag'], phase_table=tabela, phases=fases,
        allocation_records=corpo['allocation_records'],
        unmodeled=[
            'stack words of MCICD_Play in the CalculGame frame bodies (uninitialized caller locals)',
            'EFLAGS and EIP',
            'bindings and boundaries issued inside policy display roots (DirectDraw COM calls, display ticks, '
            'palette, LoadPie inside RestoreAll), counted per phase in phase_table',
            'masked display-only state (cumulative exclusion_mask, 153,060 bytes) and the surfaces (outside the '
            'state; the policy proves no logic access to them)',
            'ProgIteration frame words: saved EDX/ECX/EBX = 0 and the MSG buffer [0x3000000, 0, 0, 0] (declared; '
            'checked through the between-frames exit registers)',
            'allocation-record metadata caller_return, stack and freed_caller_return (bench call-site metadata)',
            'the CalculGame return EAX (overwritten by AffGame before any use)'],
        summary=dict(result=resultado, phases=len(fases), phases_equal=sum(1 for r in fases.values() if r['equal']),
                     crossings_writing_compared_bytes=0,
                     hud_flag_equal=all(h['equal'] for h in corpo['hud_flag'])),
        seconds=round(time.monotonic() - t0, 1))
    ok = resultado == 'equal' and not sujo.strip() and len(fases) == 257
    if not ok:
        saida = ROOT / '.local' / ('m2-2-proof-not-accepted-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), summary=relatorio['summary'], seconds=relatorio['seconds']), indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
