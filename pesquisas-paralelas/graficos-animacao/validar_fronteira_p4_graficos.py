"""Classify P4 frame 484 against the actual native AffText/TextGetMessage boundary.

This does not enable glyphs in a capture that deliberately did not execute them.
"""
import argparse
import hashlib
import json
from pathlib import Path

from validar_colheita_graficos import CapturaLimitada
from validar_entrada_m3 import ArgumentosRasterM3, CatalogoRastreado
from validar_sondas_graficos_m3 import AQUI, FronteiraTextoGravada


def validar(auditoria):
    raw = Path(auditoria).read_bytes()
    audit = json.loads(raw)
    assert audit['executable_sha256'] == '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
    assert audit['source_sha256'] == hashlib.sha256((AQUI / 'capturar_texto_p4_484.py').read_bytes()).hexdigest()
    assert [r['frame'] for r in audit['checks']] == list(range(129, 485))
    assert all(r['surface_equal'] and r['state_equal'] for r in audit['checks'])
    assert [r['routine'] for r in audit['calls']] == ['AffText', 'TextGetMessage']
    assert not audit['body_instructions']
    assert all(r['surface_before'] == r['surface_after'] for r in audit['calls'])
    assert audit['calls'][0]['entry_eax'] == audit['calls'][0]['return_eax']
    assert audit['calls'][1]['return_eax'] == '0x0'
    assert all(r['address'] == '0x5099a6' and r['eip'] == '0x417ce2'
               for r in audit['pointer_overlap_reads'])

    cap = CapturaLimitada(AQUI / 'evidencias/sonda-colheita-P4-129-728.json.xz')
    row = next(r for r in cap.d['rows'] if r['frame'] == 484)
    catalog = CatalogoRastreado()
    stopped = cap.render(row, catalog, texto=False)
    assert int(stopped.parada['endereco'], 16) == 0x459454
    boundary = FronteiraTextoGravada(cap, row)
    with ArgumentosRasterM3(catalog) as raster:
        result = cap.render(row, catalog, texto=boundary)
    assert result.parada is None and result.pixels == cap.blob(row['after'])
    assert raster.calls == row['blits'] and boundary.checked == 1 and not boundary.pending
    assert audit['calls'][0]['surface_before'] == row['text_boundaries'][0]['surface_before']
    return dict(
        schema='rising-lands/graphics-p4-text-boundary-verdict/1',
        native_frames=356, native_equal=356, frame=484,
        audit_sha256=hashlib.sha256(raw).hexdigest(),
        default_stop=stopped.parada, explicit_boundary_stop=result.parada,
        explicit_boundary_surfaces_equal=1, raster_calls_equal=len(raster.calls),
        text_boundaries_checked=boundary.checked,
        verdict='Inside the declared non-executed AffText/TextGetMessage boundary; no glyph provider is needed for this probe.',
        glyph_enabled_scope='Use the separately native-validated TextoAffTextBitmap explicitly; this probe is not glyph-enabled evidence.',
    )


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--audit', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    result = validar(a.audit)
    Path(a.output).write_text(json.dumps(result, indent=2) + '\n')
    print(result['verdict'], flush=True)
