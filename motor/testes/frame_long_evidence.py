"""Pinned 0..9200 package reader; no engine or original-x86 execution."""
import copy
import hashlib
import json
import lzma
from pathlib import Path

from frame_differential import (ROOT, M1_ENTRY, M1_CAPTURE, FIRST_CAPTURE, PINS as FROZEN_PINS,
                                sha, normalize_events, named_snapshot, mismatch_bytes,
                                reject_mutated_events, update_allocations, check_mutation_detection,
                                static_inputs, FrameInput, FrameRegisters, Frames)
from frame_evidence import (MascaraEnderecos, carregar_captura, fases_referencia, resumo_estado,
                            resumos_mascarados, comparar_estado, comparar_eventos_fase,
                            comparar_alocacoes, ler_estado, VINCULO, FRONTEIRA, _dados)
from mapa_memoria_m1 import carregar_json, expandir_captura, carregar_blocos
from contexto_exibicao_ia import ContextoExibicao
from inventario_ia_runtime import OriginalImage

DIRECTORY = ROOT / 'pesquisas-paralelas/missoes/evidencias/m2-3'
MANIFEST = DIRECTORY / 'captura-quadros9200-monde01-exibicao-v2.manifest.json'
POLICY = ROOT / 'pesquisas-paralelas/missoes/validacao/m2-3-politica-comparacao-9200-quadros.json'
PINS = {MANIFEST: 'e88dc3fcaca11d03a774dad8bd9c768345f13c884cc2d8df493107ec9d180b09',
        POLICY: '384f985bea05137197ea22b3439f96db2f1e6b9a6d8b1a6c986f4955697fc21e'}
PINS.update({p: FROZEN_PINS[p] for p in (M1_ENTRY, M1_CAPTURE, FIRST_CAPTURE)})
# A new harness pins the reviewed reference revision independently. The frozen
# stage2a/2b harness is never edited to accommodate later source changes.
REFERENCE_PINS = {
    ROOT / 'pesquisas-paralelas/ia-runtime/comparar_quadro1_encadeado_ia.py': 'd1a268d35261c1f75afec9938c9c09b3bbc2bb371d9c81e17e3a8ff9374f82a6',
    ROOT / 'pesquisas-paralelas/ia-runtime/comparar_quadros_ia.py': 'fd803036a33d6bab2859ae16adcd90023a4001feeb840bd7153aa0705c10ab60',
    ROOT / 'pesquisas-paralelas/ia-runtime/composicao_quadros_ia.py': 'afdc8a396b254f5e65167b215c9a785d18cba530169c683ad5c35d63ed786e43',
    ROOT / 'pesquisas-paralelas/ia-runtime/composicao_encadeada_ia.py': '4d4f45ce5fc2c2599884d876f7c189554c61b71852115a83d4c96a6f4efc873b',
    ROOT / 'pesquisas-paralelas/ia-runtime/quadro_calcul_game.py': '1634bed75de495041871540bf33176e3aad607e1cf2c843f96453df623c540d7',
    ROOT / 'pesquisas-paralelas/ia-runtime/contexto_exibicao_ia.py': 'e8ba0fbbba0d0b8dd39511b3cca3df0a3a6737411992f488400e3e3b24b70d87',
    ROOT / 'pesquisas-paralelas/missoes/mapa_memoria_m1.py': '7507e065c20ff0c05d6d86972d0a11919cc59e484a6b4f306c122c309a2d74c9',
    ROOT / 'pesquisas-paralelas/ia-runtime/partes_quadros_ia.py': 'fc86436f1af38ab1b71701471a598a19324e7f8d094f62549567e4377a7fdd06',
}
ALLOCATOR_NAMES = {'KERNEL32.GlobalAlloc', 'KERNEL32.GlobalLock', 'KERNEL32.GlobalHandle',
                   'KERNEL32.GlobalUnlock', 'KERNEL32.GlobalFree', 'KERNEL32.VirtualAlloc',
                   'KERNEL32.VirtualFree'}
HASH_FIELDS = ('summary', 'compared_summary', 'masked_sha256')


def pins():
    for path, expected in {**PINS, **REFERENCE_PINS}.items():
        if sha(path) != expected:
            raise ValueError('ReferenceIdentityMismatch: ' + str(path.relative_to(ROOT)))


def phase_names(first, last):
    names = ['load_tail'] if first == 0 else []
    for frame in range(max(1, first), last + 1):
        names += ['between_frames' if frame == 1 else f'between_frames{frame}', f'frame{frame}']
    return names


def phase_frame(name):
    if name == 'load_tail':
        return 0
    suffix = name[len('between_frames'):] if name.startswith('between_frames') else name[len('frame'):]
    return int(suffix) if suffix else 1


def load_manifest():
    pins()
    data = carregar_json(MANIFEST)
    if data['policy'] != dict(path=str(POLICY.relative_to(ROOT)), sha256=PINS[POLICY]):
        raise ValueError('Manifest policy identity differs')
    parts = data['parts']
    if [p['part'] for p in parts] != list(range(10)) or sum(p['phases'] for p in parts) != 18401:
        raise ValueError('Manifest does not cover the exact ten-part 18,401-phase domain')
    if parts[0]['frames'][0] != 0 or parts[-1]['frames'][1] != 9200:
        raise ValueError('Manifest frame bounds differ')
    for i, part in enumerate(parts):
        names = phase_names(*part['frames'])
        if (len(names), names[0], names[-1]) != (part['phases'], part['first_phase'], part['last_phase']):
            raise ValueError('Manifest phase bounds differ')
        if i and part['frames'][0] != parts[i - 1]['frames'][1] + 1:
            raise ValueError('Manifest frame intervals are not contiguous')
    return data


def load_part(manifest, number):
    entry = manifest['parts'][number]
    path = ROOT / entry['artifact']
    compressed = path.read_bytes()
    if len(compressed) != entry['compressed_bytes'] or hashlib.sha256(compressed).hexdigest() != entry['compressed_sha256']:
        raise ValueError(f'Part {number}: compressed identity differs')
    raw = lzma.decompress(compressed)
    if len(raw) != entry['raw_bytes'] or hashlib.sha256(raw).hexdigest() != entry['raw_sha256']:
        raise ValueError(f'Part {number}: raw identity differs')
    part = json.loads(raw)
    expected_previous = None if number == 0 else manifest['parts'][number - 1]['raw_sha256']
    if (part['part'] != number or part['frames'] != entry['frames'] or part['policy'] != manifest['policy']
            or part.get('previous_part_raw_sha256') != expected_previous
            or [p['phase'] for p in part['phases']] != phase_names(*entry['frames'])):
        raise ValueError(f'Part {number}: identity, hash chain or phase order differs')
    if part['original_sha256'] != '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb':
        raise ValueError('Intact original identity differs')
    return part


def opening(part, mask):
    opened = part['opening_state']
    state = {n: (int(b['base'], 16), _dados(b)) for n, b in opened['full_state'].items()}
    compared, masked = resumos_mascarados(mask, state)
    if resumo_estado(state) != opened['summary'] or compared != opened['compared_summary'] or masked != opened['masked_sha256']:
        raise ValueError(f"Part {part['part']}: full opening state does not match its three hashes")
    return state


def allocator_invariants(part):
    """Prove the adopted post-load records stay unchanged on later openings."""
    counts = {p[k]['allocations'] for p in part['phases'] for k in ('entry', 'exit')}
    if counts != {25482}:
        raise ValueError('Unexpected allocation-record count')
    changes = []
    for p in part['phases']:
        delta = p['state_delta']
        calls = [e['name'] for e in p['bindings'] if e['name'] in ALLOCATOR_NAMES]
        changed = bool(delta.get('allocated') or delta.get('released') or calls)
        if changed:
            changes.append(dict(phase=p['phase'], allocated=len(delta.get('allocated', {})),
                                released=len(delta.get('released', [])), allocator_bindings=len(calls)))
            if p['phase'] != 'load_tail' or delta.get('allocated') or len(delta.get('released', [])) != 146 or len(calls) != 584:
                raise ValueError('Allocator history exceeds the adopted-record checkpoint contract')
    return dict(record_count=25482, transitions=changes, unchanged_after_load_tail=True)


def mission_inputs():
    entry = carregar_json(M1_ENTRY)
    m1 = expandir_captura(carregar_json(M1_CAPTURE), entry)
    short = carregar_json(FIRST_CAPTURE)
    s0 = carregar_blocos(m1['oracle']['final_state']['blocks'])
    after = copy.deepcopy(short['allocations'])
    return s0, m1['allocations'], after, short


def verify_packages():
    manifest = load_manifest()
    policy = carregar_json(POLICY)
    mask = MascaraEnderecos(policy['cumulative']['exclusion_mask'])
    if mask.bytes != 153060 or policy['frames'] != 9200 or policy['phases'] != 18401:
        raise ValueError('Long policy domain differs')
    first_s0, _, after_records, _ = mission_inputs()
    previous, records = None, []
    for n in range(10):
        part = load_part(manifest, n)
        state = opening(part, mask)
        if n == 0 and state != first_s0:
            raise ValueError('Part 0 is not accepted display MissionLoad S0')
        if previous is not None and any(part['opening_state'][k] != previous[k] for k in HASH_FIELDS):
            raise ValueError(f'Part {n}: opening hashes differ from previous final hashes')
        record = dict(part=n, raw_sha256=manifest['parts'][n]['raw_sha256'], frames=part['frames'],
                      phases=len(part['phases']), first_phase=part['first_phase'], last_phase=part['last_phase'],
                      opening={k: part['opening_state'][k] for k in HASH_FIELDS},
                      ending={k: part['phases'][-1]['state_after'][k] for k in HASH_FIELDS},
                      allocator=allocator_invariants(part))
        if n == 9:
            record['allocation_records'] = comparar_alocacoes(after_records, part['allocations'])
            if not record['allocation_records']['equal']:
                raise ValueError('Final original allocation records differ from adopted post-load records')
        records.append(record)
        previous = record['ending']
        print(f'package {n:02d}: hashes/opening/chain/allocator checked', flush=True)
    return dict(schema='rising-lands/rust-engine-long-package-plan/1', manifest=dict(path=str(MANIFEST.relative_to(ROOT)),
                sha256=PINS[MANIFEST]), policy=manifest['policy'], parts=records,
                summary=dict(result='verified', parts=10, phases=18401, full_phase_replay='performed separately by each comparison'))
