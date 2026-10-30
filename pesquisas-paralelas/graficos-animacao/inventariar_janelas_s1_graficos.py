"""Read the original S1 records: gameplay input windows, view origins and partial unit metadata.

No foreign implementation hash is pinned. The immutable capture revision is provenance,
not a requirement on the implementation currently supplied by another front.
"""
import argparse
import collections
import json
import lzma
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[1]
S1_REF = '82ec5eaa98d4f212b650c2c8ce2b293a30fb50ef'
S1_ROOT = 'pesquisas-paralelas/missoes/m3/'


def arquivo(ref, path):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{ref}:{path}'])


def registros(ref=S1_REF):
    return {r['frame']: r for r in map(json.loads, lzma.decompress(
        arquivo(ref, S1_ROOT + 'sondas/S1/quadros.jsonl.xz')).splitlines())}


def janelas(entrada, *, gameplay_through=17031):
    """Union of all gameplay input records and 200 following frames, inclusive.

    17032 is the observed S1 MenuInit(0x13) transition. The later confirmation is
    explicitly outside this M3.2 gameplay census and has its separate screen proof.
    """
    out = []
    for item in entrada['frames']:
        lo = item['frame']
        if lo > gameplay_through:
            continue
        hi = min(lo + 200, gameplay_through)
        if out and lo <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], hi)
        else:
            out.append([lo, hi])
    return out


def inventariar(ref=S1_REF):
    from efeitos_logicos_exibicao import ORIGENS_PROVADAS, ORIGENS_RESTOREALL_PROVADAS
    refs = registros(ref)
    entrada = json.loads(arquivo(ref, S1_ROOT + 'entradas/S1.json'))
    intervals = janelas(entrada)
    windows = []
    for i, (lo, hi) in enumerate(intervals, 1):
        rows = [refs[k] for k in range(lo, hi + 1)]
        origins = sorted({tuple(r['view_origin']) for r in rows})
        windows.append(dict(window=i, frames=[lo, hi], expected_surfaces=len(rows),
            identical_between_and_frame_surfaces=sum(r['surfaces_between'] == r['surfaces_frame'] for r in rows),
            view_origins=origins,
            structures=sorted({tuple(s) for r in rows for s in r['objective']['structures']}),
            tracked_unit_states=sorted({(int(n), u['state']) for r in rows for n, u in r['objective']['units'].items()})))
    origins = {tuple(r['view_origin']) for r in refs.values()}
    return dict(schema='rising-lands/graphics-s1-order-window-inventory/1', source_revision=ref,
        source_paths=[S1_ROOT + 'entradas/S1.json', S1_ROOT + 'sondas/S1/quadros.jsonl.xz'],
        original_frames=len(refs), windows=windows, expected_surfaces=sum(w['expected_surfaces'] for w in windows),
        all_s1_view_origins=sorted(origins),
        unproved_affgame_origins=sorted(origins - set(ORIGENS_PROVADAS)),
        unproved_restoreall_origins=sorted(origins - set(ORIGENS_RESTOREALL_PROVADAS)),
        all_s1_structures=sorted({tuple(s) for r in refs.values() for s in r['objective']['structures']}),
        excluded_input_frames=[r['frame'] for r in entrada['frames'] if r['frame'] > 17031],
        unit_metadata_scope='Only tracked units 11..15. Full 800-record census comes from original render-entry captures; this metadata is not complete unit coverage.',
        boundary_contract='Missions display-v2 declared AffText/TextGetMessage non-execution; no implicit glyph callback.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ref', default=S1_REF)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    result = inventariar(a.ref)
    Path(a.output).write_text(json.dumps(result, indent=2) + '\n')
    print([(w['frames'], w['expected_surfaces']) for w in result['windows']], flush=True)
