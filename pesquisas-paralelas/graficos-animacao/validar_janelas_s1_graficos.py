"""S1 full-surface render proof and full-pool census from original AffGame-entry captures.

Each capture starts from its native surface/cache, then carries Python outputs through
every consecutive row. Disjoint capture prefixes are never called one continuous chain.
Only the two previously proved DD pointer slots are excluded from display-effect comparison.
"""
import argparse
import collections
import hashlib
import json
import struct
import time
from pathlib import Path

from efeitos_logicos_exibicao import DependenciaExibicao, desenhar_jogo
from inventariar_janelas_s1_graficos import AQUI, inventariar, registros, S1_REF
from render_quadro import renderizar_quadro
from validar_colheita_graficos import CapturaLimitada
from validar_entrada_m3 import ArgumentosRasterM3, CatalogoRastreado, MemoriaEntradaM3
from validar_sondas_graficos_m3 import FronteiraTextoGravada

sha = lambda b: hashlib.sha256(b).hexdigest()


def habitado(memory, index):
    record = memory.ler_mundo(0x49a0c8 + 276 * index, 276)
    capacity = struct.unpack_from('<H', record, 0xe)[0]
    types = []
    for slot in range(capacity):
        if record[0x4e + slot] == 1:
            unit = struct.unpack_from('<H', record, 0x12 + 2 * slot)[0]
            types.append(memory.u8(memory.u32(0x4e19a0) + 276 * unit + 1))
    if record[8] in (2, 21):
        return any(t not in (3, 11, 12, 13, 14, 15, 16, 17, 25) for t in types)
    return 9 in types


def comparar(path, refs, initial=None, capture=None):
    started = time.monotonic()
    cap = CapturaLimitada(path) if capture is None else capture
    assert cap.d['probe'] == 'S1' and cap.d['executable_sha256'] == '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
    assert all(r['surface_equal'] and r['state_equal'] for r in cap.d['checks'])
    catalog = CatalogoRastreado()
    rows, units, structures, origins = [], collections.Counter(), collections.Counter(), set()
    state, cache, background = initial if initial is not None else (None, None, None)
    # Census is independent of whether the renderer has reached this native row yet.
    for row in cap.d['rows']:
        m = cap.memory(row)
        pool = m.ler_mundo(m.u32(0x4e19a0), 220800)
        for i in range(800):
            r = pool[i * 276:(i + 1) * 276]
            if r[2]:
                units[(r[1], r[2], r[0])] += 1
        pool = m.ler_mundo(0x49a0c8, 276000)
        for i in range(1000):
            r = pool[i * 276:(i + 1) * 276]
            if r[5]:
                structures[(r[8], r[5], r[4], struct.unpack_from('<H', r, 0xc)[0])] += 1
        origins.add((m.u16(0x508720), m.u16(0x508722)))
    for row in cap.d['rows']:
        frame = row['frame']
        assert row['after'] == refs[frame]['surfaces_between']['offscreen']
        assert refs[frame]['surfaces_between'] == refs[frame]['surfaces_frame']
        m = cap.memory(row)
        if state is None:
            state, cache = cap.blob(row['before']), cap.cache_entry(row)
        assert sha(state) == row['before'] and cache == cap.cache_entry(row), ('Chained native entry differs', frame)
        if background is not None and 'saved_background' in row['entry']:
            assert sha(background[1]) == row['entry']['saved_background'][1]
            m = MemoriaEntradaM3([background] + m.blocks)
        logic_stop = None;logic_effects=()
        try:
            logic_effects=desenhar_jogo(m, habitado=lambda i: habitado(m, i)).escritas
        except DependenciaExibicao as error:
            logic_stop = dict(address=hex(error.sitio), reason=error.motivo)
        adapter = FronteiraTextoGravada(cap, row)
        with ArgumentosRasterM3(catalog) as raster:
            result = renderizar_quadro(m, superficie_anterior=state, cache=cache, catalogo=catalog,
                habitado=lambda i: habitado(m, i), hud=True, texto=adapter,
                relogio=lambda: struct.unpack_from('<I', cap.blob(row['exit_dgroup']), 0x4e17b4 - 0x494000)[0])
        expected = cap.blob(row['after'])
        pixels = sum(a != b for a, b in zip(result.pixels, expected))
        arguments = sum(a != b for a, b in zip(raster.calls, row['blits'])) + abs(len(raster.calls) - len(row['blits']))
        native_dg = cap.blob(row['exit_dgroup'])
        input_writes=[(a,n,v) for a,n,v in logic_effects if 0x5099b4<=a<a+n<=0x50a9ba]
        logic_writes_bad=[hex(a) for a,n,v in input_writes if native_dg[a-0x494000:a-0x494000+n]!=v.to_bytes(n,'little')]
        projected = bytearray(cap.memory(row).ler_mundo(0x494000, len(native_dg)))
        for name, address, old, new in result.efeitos:
            data = bytes.fromhex(new)
            if 0x494000 <= address < address + len(data) <= 0x523000:
                projected[address - 0x494000:address - 0x494000 + len(data)] = data
            elif name == 'saved_background_pixels':
                background = (address, data)
        struct.pack_into('<H', projected, 0x49a04e - 0x494000, result.cache.proximo)
        ignored = {a + i for a in (0x508f70, 0x4e17a4) for i in range(4)}
        effects = [] if result.parada else [hex(0x494000 + i) for i, (a, b) in enumerate(zip(projected, native_dg))
                                                if a != b and 0x494000 + i not in ignored]
        equal = not (result.parada or logic_stop or pixels or arguments or effects or adapter.pending or logic_writes_bad)
        item = dict(frame=frame, equal=equal, stop=result.parada, logic_stop=logic_stop,
            pixel_mismatches=pixels, argument_mismatches=arguments, effect_mismatches=effects,
            text_boundaries=adapter.checked, drawing_calls=len(raster.calls),
            logic_input_writes=input_writes,logic_write_mismatches=logic_writes_bad,
            sha256=sha(result.pixels), native_sha256=row['after'])
        if arguments:
            item['argument_details'] = [dict(index=i, python=a, native=b) for i, (a, b) in enumerate(zip(raster.calls, row['blits'])) if a != b][:5]
        rows.append(item)
        state, cache = result.pixels, result.cache
        if not equal:
            print('S1 first difference', item, flush=True)
            break
        if frame % 100 == 0:
            print('S1', frame, 'full surface/arguments/effects equal', flush=True)
    return dict(capture=Path(path).name, capture_sha256=cap.sha, native_frames=cap.d['frames'],
        native_status=cap.d['status'], compared=len(rows), equal=sum(r['equal'] for r in rows),
        first_difference=next((r for r in rows if not r['equal']), None), rows=rows,
        full_pool_unit_states=[dict(kind=k, state=s, owner=o, native_record_observations=n) for (k, s, o), n in sorted(units.items())],
        full_pool_structure_modes=[dict(kind=k, mode=s, owner=o, bag_count=c, native_record_observations=n) for (k, s, o, c), n in sorted(structures.items())],
        origins=sorted(origins), elapsed_seconds=round(time.monotonic() - started, 3),
        continued_from_previous_capture=initial is not None,
        _exit=(state, cache, background))


def validar(paths, ref=S1_REF):
    refs = registros(ref)
    inventory = inventariar(ref)
    captures = []
    previous_end = previous_exit = None
    for path in paths:
        # Transport partitions keep one continuous Python surface/cache chain.
        head = CapturaLimitada(path)
        first = head.d['frames'][0]
        capture = comparar(path, refs, previous_exit if previous_end == first - 1 else None, head)
        del head
        previous_exit = capture.pop('_exit')
        previous_end = capture['native_frames'][1] if capture['first_difference'] is None else None
        captures.append(capture)
    by_frame = {}
    for capture in captures:
        for row in capture['rows']:
            if row['frame'] in by_frame:
                assert row['native_sha256'] == by_frame[row['frame']]['native_sha256']
            if row['frame'] not in by_frame or row['equal']:
                by_frame[row['frame']] = row
    windows = []
    for window in inventory['windows']:
        lo, hi = window['frames']
        available = [by_frame[k] for k in range(lo, hi + 1) if k in by_frame]
        windows.append(dict(window=window['window'], frames=[lo, hi], expected=hi - lo + 1,
            compared=len(available), equal=sum(r['equal'] for r in available),
            missing_ranges=_ranges([k for k in range(lo, hi + 1) if k not in by_frame]),
            first_difference=next((r for r in available if not r['equal']), None)))
    sources = ('render_quadro.py', 'quadro_jogo.py', 'hud_quadro.py', 'sobreposicoes_entrada_m3.py',
        'cave_scriptada_m3.py', 'camadas_exibicao_m3.py', 'camadas_m3_api18.json', 'hud_scriptado_m3.py',
        'colheita_exibicao_m3.py', 'efeitos_logicos_exibicao.py', 'cronometro_s1_graficos.py', 'validar_janelas_s1_graficos.py')
    return dict(schema='rising-lands/graphics-s1-window-render-comparison/1', source_revision=ref,
        sources_sha256={n: sha((AQUI / n).read_bytes()) for n in sources},
        boundary_contract=inventory['boundary_contract'], expected_surfaces=inventory['expected_surfaces'],
        equal_surfaces=sum(w['equal'] for w in windows), windows=windows, captures=captures,
        scope='Native entry states seed each capture independently. Python surface/cache/background are chained within each capture. No whole-state simulation or glyph-enabled retail-screen claim.')


def _ranges(values):
    out = []
    for k in values:
        if out and k == out[-1][1] + 1:
            out[-1][1] = k
        else:
            out.append([k, k])
    return out


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--capture', action='append', required=True)
    p.add_argument('--ref', default=S1_REF)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    result = validar(a.capture, a.ref)
    Path(a.output).write_text(json.dumps(result, indent=1) + '\n')
    print([(w['window'], w['equal'], w['expected'], w['first_difference']) for w in result['windows']], flush=True)
    if any(c['first_difference'] for c in result['captures']):
        raise SystemExit(1)
