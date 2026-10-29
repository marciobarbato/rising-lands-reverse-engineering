"""Per-phase surface SHA-256 values recorded by Missions' M2.2 capture (-v2 display scenario).

Reads the committed xz capture (hash-verified against its manifest) and writes a small table: for every phase, the
SHA-256 of the declared primary and offscreen surfaces at the end of the phase.  Surfaces are excluded from the compared
game state; these hashes are the only per-phase pixel witness the capture holds.

    python3 -B pesquisas-paralelas/graficos-animacao/extrair_hashes_superficie_m22.py --saida evidencias/superficies-fase-m22-v2.json
"""
import argparse, hashlib, json, lzma
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
XZ = RAIZ/'pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz'
MANIFESTO = XZ.with_suffix('').with_suffix('.manifest.json')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--saida', required=True); a = ap.parse_args()
    manifesto = json.loads(MANIFESTO.read_text())
    bruto = XZ.read_bytes()
    if hashlib.sha256(bruto).hexdigest() != manifesto['compressed']['sha256']: raise SystemExit('xz hash differs from its manifest')
    d = json.loads(lzma.decompress(bruto))
    fases = []
    for p in d['phases']:
        s = {x['role']: x['sha256'] for x in p['display_state']['surfaces']}
        fases.append(dict(phase=p['phase'], offscreen=s['offscreen'], primaria=s['primaria'], counter=p['observed'].get('counter_508f7c') if isinstance(p.get('observed'), dict) else None))
    saida = dict(schema='rising-lands/m22-surface-hashes/1', source_xz=str(XZ.relative_to(RAIZ)), source_xz_sha256=manifesto['compressed']['sha256'],
                 source_raw_json_sha256=manifesto['raw_json']['sha256'], scenario='exibicao (-v2 display reference)', phases=fases)
    Path(a.saida).write_text(json.dumps(saida, indent=0))
    print(len(fases), 'phases', fases[0], fases[1])


if __name__ == '__main__':
    main()
