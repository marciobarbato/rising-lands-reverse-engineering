"""M2.3 long-run parts: manifest check, per-part comparison plan, and aggregation of the part reports.

Python only. The format is Missions' ``pacotes_quadros_missao`` (``compressed-evidence-manifest/2``).

    # 1. pins and the hash chain, without replay; writes the plan of independent part comparisons
    python3 -B pesquisas-paralelas/ia-runtime/partes_quadros_ia.py verificar --manifesto <prefix>.manifest.json \
        --plano .local/m2-3/plano.json
    # 2. each part, independently (in parallel on the Mac mini), as the plan lists:
    python3 -B pesquisas-paralelas/ia-runtime/comparar_quadros_ia.py --parte <part> --sha256 <raw> --politica <policy> \
        --saida <report>
    # 3. one verdict over every part report
    python3 -B pesquisas-paralelas/ia-runtime/partes_quadros_ia.py agregar --plano .local/m2-3/plano.json \
        --saida <proof.json>

``verificar`` checks each part's compressed and raw SHA-256 against the manifest. It then checks the chain from
the hashes alone, with no replay:
- part k's ``previous_part_raw_sha256`` is part k-1's raw hash;
- part k's ``opening_state`` summary, ``compared_summary`` and ``masked_sha256`` equal part k-1's last
  ``state_after`` hashes (each part's own comparison then proves its full opening state against those hashes,
  and its deltas against every phase hash);
- part 0 opens with load_tail;
- the frames are contiguous;
- every part names the manifest's policy.

``agregar`` requires every part report to be equal, its inputs to match the plan, and the parts to cover the run
without gaps.
"""
import argparse
import hashlib
import json
import lzma
import sys

from ambiente_ia_runtime import ROOT

SCRIPT = 'pesquisas-paralelas/ia-runtime/comparar_quadros_ia.py'


def _sha(dados):
    return hashlib.sha256(dados).hexdigest()


def verificar(manifesto_caminho):
    manifesto = json.loads(manifesto_caminho.read_bytes())
    politica = manifesto['policy']
    if _sha((ROOT / politica['path']).read_bytes()) != politica['sha256']:
        raise SystemExit('The manifest policy file differs from its pinned hash')
    partes, anterior = [], None
    for p in sorted(manifesto['parts'], key=lambda x: x['part']):
        comprimido = (ROOT / p['artifact']).read_bytes()
        if _sha(comprimido) != p['compressed_sha256']:
            raise SystemExit(f"part {p['part']}: compressed hash differs from the manifest")
        bruto = lzma.decompress(comprimido)
        if _sha(bruto) != p['raw_sha256']:
            raise SystemExit(f"part {p['part']}: raw hash differs from the manifest")
        parte = json.loads(bruto)
        if parte['policy'] != politica:
            raise SystemExit(f"part {p['part']}: packaged with another policy")
        abertura = parte['opening_state']
        chaves = ('summary', 'compared_summary', 'masked_sha256')
        if anterior is None:
            if parte['phases'][0]['phase'] != 'load_tail' or parte.get('previous_part_raw_sha256') is not None:
                raise SystemExit('part 0 must open with load_tail and no previous part')
        else:
            fim = anterior['phases'][-1]['state_after']
            if parte['previous_part_raw_sha256'] != partes[-1]['raw_sha256']:
                raise SystemExit(f"part {p['part']}: previous_part_raw_sha256 is not part {p['part'] - 1}'s raw hash")
            if any(abertura[k] != fim[k] for k in chaves):
                raise SystemExit(f"part {p['part']}: opening hashes differ from part {p['part'] - 1}'s end state")
            if parte['frames'][0] != anterior['frames'][1] + 1:
                raise SystemExit(f"part {p['part']}: frames are not contiguous")
        partes.append(dict(part=p['part'], artifact=p['artifact'], raw_sha256=p['raw_sha256'],
                           frames=parte['frames'], first_phase=parte['phases'][0]['phase'],
                           last_phase=parte['phases'][-1]['phase'], phases=len(parte['phases']),
                           final_records=all(k in parte for k in ('allocations',))))
        anterior = parte
    return dict(manifest=dict(path=str(manifesto_caminho.relative_to(ROOT)),
                              sha256=_sha(manifesto_caminho.read_bytes())),
                policy=politica, parts=partes, chain='checked from hashes (no replay)')


def plano(verificacao, pasta_relatorios):
    for p in verificacao['parts']:
        p['report'] = f"{pasta_relatorios}/parte{p['part']:02d}.json"
        p['command'] = (f"python3 -B {SCRIPT} --parte {p['artifact']} --sha256 {p['raw_sha256']} "
                        f"--politica {verificacao['policy']['path']} --saida {p['report']}")
    return verificacao


def agregar(plano_):
    linhas, resultado, fases, iguais = [], 'equal', 0, 0
    for p in plano_['parts']:
        rel = json.loads((ROOT / p['report']).read_bytes())
        parte = rel['part']
        problemas = []
        if parte['raw_json_sha256'] != p['raw_sha256'] or parte['raw_json_sha256_pinned'] != p['raw_sha256']:
            problemas.append('report is not for the planned part')
        if rel['policy']['sha256'] != plano_['policy']['sha256']:
            problemas.append('report used another policy')
        if (parte['first_phase'], parte['last_phase']) != (p['first_phase'], p['last_phase']):
            problemas.append('report does not cover the whole part')
        if rel['summary']['result'] != 'equal' or rel['summary']['phases_equal'] != p['phases']:
            problemas.append(f"part result {rel['summary']['result']}")
        if rel.get('source_dirty_paths'):
            problemas.append('report made from a dirty tree')
        if p['final_records'] and not (rel.get('allocation_records') or {}).get('equal'):
            problemas.append('final allocation records not equal')
        fases += rel['summary']['phases_compared']
        iguais += rel['summary']['phases_equal']
        linhas.append(dict(part=p['part'], frames=p['frames'], phases=rel['summary']['phases_compared'],
                           equal=not problemas, problems=problemas, source_revision=rel.get('source_revision'),
                           hud_flag_equal=all(h['equal'] for h in rel.get('hud_flag', []))))
        if problemas and resultado == 'equal':
            resultado = f"part {p['part']}: " + '; '.join(problemas)
    return dict(schema='rising-lands/ai-runtime-m2.3-parts-proof/1', manifest=plano_['manifest'],
                policy=plano_['policy'], parts=linhas, crossings=dict(count=0, writing_compared_bytes=0),
                summary=dict(result=resultado, phases=fases, phases_equal=iguais))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='comando', required=True)
    v = sub.add_parser('verificar')
    v.add_argument('--manifesto', required=True)
    v.add_argument('--plano', required=True)
    v.add_argument('--relatorios', default='.local/m2-3/partes', help='repo-relative folder of the part reports')
    g = sub.add_parser('agregar')
    g.add_argument('--plano', required=True)
    g.add_argument('--saida', required=True)
    a = ap.parse_args()
    if a.comando == 'verificar':
        saida = ROOT / a.plano
        if saida.exists():
            raise SystemExit(f'Refusing to overwrite {saida}')
        resultado = plano(verificar(ROOT / a.manifesto), a.relatorios)
    else:
        saida = ROOT / a.saida
        if saida.exists():
            raise SystemExit(f'Refusing to overwrite {saida}')
        resultado = agregar(json.loads((ROOT / a.plano).read_bytes()))
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(resultado, f, indent=1)
        f.write('\n')
    print(json.dumps(resultado.get('summary') or [p['command'] for p in resultado['parts']], indent=1))
    return 0 if a.comando == 'verificar' or resultado['summary']['result'] == 'equal' else 2


if __name__ == '__main__':
    sys.exit(main())
