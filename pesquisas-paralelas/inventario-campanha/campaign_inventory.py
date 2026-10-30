#!/usr/bin/env python3
"""Read-only original-data inventory; writes derived JSON only beside this script.

No engine execution, reconstructed world initialization, or gameplay simulation.
Run with -B. --check regenerates in memory and compares the published products.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re
import struct
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'pesquisas-paralelas/missoes'))
import ambiente_missoes  # bootstrap the committed flat namespace
from analisar import HASH_ESTUDADO, dependencias
from formatos import ler_eta, Leitor
from regras import extrair_regras, ler_ini
from nome_missao import nome_arquivo_missao
from carregador_condicoes import carregar_condicoes_fim, carregar_objetivos

UNKNOWN = {'status': 'unknown', 'reason': 'Not serialized by the documented ETA load path; requires campaign entry state and original execution.'}
CONDITIONS = {0: 'food_threshold', 1: 'stone_threshold', 2: 'parts_threshold',
              3: 'invention_count', 4: 'owned_structure_in_zone',
              5: 'no_non_allied_opponent_forces', 255: 'inert_except_first_record_blocks_victory'}
DEPENDENCIES = [
    'ferramentas/formatos.py', 'ferramentas/unidades.py', 'ferramentas/regras.py',
    'pesquisas-paralelas/missoes/ambiente_missoes.py',
    'pesquisas-paralelas/missoes/nome_missao.py',
    'pesquisas-paralelas/missoes/carregador_condicoes.py',
    'pesquisas-paralelas/missoes/fim_missao.py',
    'pesquisas-paralelas/missoes/carregador_cadeia_auxiliar.py',
    'pesquisas-paralelas/ia-runtime/incursao_ia.py',
    'pesquisas-paralelas/ia-runtime/reinicio_ia.py',
    'pesquisas-paralelas/economia/cauda_carga.py',
    'pesquisas-paralelas/economia/extracao.py',
    'pesquisas-paralelas/missoes/evidencias/inventario.json',
    'relatorios/simbolos-originais.json',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()


def hist(values):
    return {str(k): v for k, v in sorted(Counter(values).items())}


def words(raw):
    return list(struct.unpack('<' + 'H' * (len(raw) // 2), raw))


def source(cd, path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(cd)), 'size': len(data), 'sha256': sha(data)}


def records(data, block):
    p = block['offset'] + (2 if block['nome'] in ('tabela_47534a', 'tabela_47bcc7') else 4)
    rows = []
    for ordinal in range(block['quantidade']):
        index = ordinal
        if block['indexado']:
            index = struct.unpack_from('<H', data, p)[0]
            p += 2
        end = p + block['tamanho_registro']
        rows.append((index, p, data[p:end]))
        p = end
    assert p == block['fim']
    return rows


def selection_paths():
    """Enumerate filename-reader inputs, not guessed progression branches."""
    selected = {}
    for n in range(1, 26):
        inputs = [(None, None)]
        if n == 9:
            inputs = [(i, None) for i in range(4)]
        elif n in (10, 12, 17):
            inputs = [(None, i) for i in (1, 2, 3)]
        for variant, least in inputs:
            name = nome_arquivo_missao(n, bytearray(64), variante_u8=variant,
                                      simpatia=lambda owner, other: -1 if owner == least else 0)
            stem = name.decode('ascii').split('\\')[-1].split('.')[0].upper()
            selected[stem] = {'stage': n, 'variant_index': variant,
                              'least_sympathy_owner_example': least}
    return selected


def catalogs(cd):
    pefile, _ = dependencias()
    exe = (cd / 'INSTALHD/RISING.EXE').read_bytes()
    assert sha(exe) == HASH_ESTUDADO, 'Wrong original executable identity'
    pe = pefile.PE(data=exe)
    image, base = pe.get_memory_mapped_image(), pe.OPTIONAL_HEADER.ImageBase
    ini_bytes = (cd / 'INSTALHD/RISING.INI').read_bytes()
    ini = ler_ini(ini_bytes)
    units = extrair_regras(image, base, ini_bytes)['unidades']
    structures = []
    for t in range(22):
        start = 0x495d8c - base + t * 52
        raw = image[start:start + 52]
        symbol = raw[19:].split(b'\0')[0].decode('cp1252')
        structures.append({'id': t, 'symbol_original': symbol,
                           'name_pt_br': ini.get(symbol, 'NAME', fallback=None),
                           'table_va': hex(0x495d8c + t * 52), 'record_sha256': sha(raw)})
    research = []
    for section in ini.sections():
        match = re.fullmatch(r'(AGRICULTURE|MILITAIRE|GENIECIVIL|RELIGIEUX)(\d+)', section)
        if match:
            fields = {k.upper(): int(v) for k, v in ini.items(section)}
            research.append({'section': section, 'branch_original': match[1], 'ordinal': int(match[2]),
                             'declared_fields': fields})
    spells = [{'section_original': s, 'name_pt_br': ini.get(s, 'NAME'),
               'mission_unlock_state': 'unknown'}
              for s in ini.sections() if ini.has_option(s, 'APPRENTISSAGE')]
    monster_types = list(image[0x498400-base:0x498408-base])
    monster_ini = ler_ini((cd / 'INSTALHD/MONSTRE.INI').read_bytes())
    groups = []
    for g in range(16):
        key = f'GROUPE{g:02d}'
        raw = monster_ini.get('GENERAL', key, fallback=None)
        indices = [int(x) for x in raw.split(',')] if raw else []
        assert all(0 <= i < 8 for i in indices)
        groups.append({'id': g, 'declared_csv': raw, 'types': hist(monster_types[i] for i in indices)})
    # Hash exact original ranges relied on for the extra static annotations.
    ranges = [('structure_type_names', 0x495d8c, 0x495d8c+22*52),
              ('monster_profile_type_lookup', 0x498400, 0x498408),
              ('MissionNext', 0x46c08c, 0x46c11a),
              ('InitPlayer', 0x46dcb4, 0x46ddfc),
              ('BatimentGetPlayer', 0x41a08c, 0x41a0ab)]
    return {'unit_types': [{'id': u['id'], 'symbol_original': u['secao_original'], 'name_pt_br': u['nome']}
                           for u in units], 'structure_types': structures,
            'research_declarations': research,
            'spell_declarations': spells,
            'research_note': 'MISSION and APPARITION are original INI declarations, not a decoded per-owner unlocked state. Missing APPARITION stays absent; no default invented.',
            'monster_group_type_lookup': monster_types, 'monster_groups': groups,
            'monster_profile_note': 'Shipped file has no HumanOnly/Proba* keys. Profile API defaults and working-directory binding are runtime dependencies.',
            'original_ranges': [{'name': n, 'start_va': hex(a), 'end_exclusive_va': hex(b),
                                 'sha256': sha(image[a-base:b-base])} for n, a, b in ranges]}


def inventory_map(cd, path, catalog, selected):
    data = path.read_bytes()
    parsed = ler_eta(data)  # authoritative sizes, layers, disk units and suffix
    blocks = {b['nome']: b for b in parsed['blocos']}
    stem, campaign = path.stem, path.suffix.upper() == '.ETA'
    stage = int(stem[5:7]) if campaign else None
    features = set()
    def feature(f):
        features.add(f)
    units = parsed['unidades']
    for u in units:
        # Only the documented owner overrides; keep raw disk fields alongside.
        u['owner_after_documented_load_override'] = (
            0 if u['tipo'] == 16 else 4 if 20 <= u['tipo'] <= 24 else u['proprietario_id']
        ) if u['byte_estado'] else u['proprietario_id']
        if u['byte_estado']:
            feature(f'unit.initial.type.{u["tipo"]}')
            feature(f'unit.initial.state.{u["byte_estado"]}')
    structures = []
    for index, offset, raw in records(data, blocks['estruturas']):
        row = {'index': index, 'offset': offset, 'cell': words(raw[2:4])[0],
               'owner_raw': raw[4], 'state_raw': raw[5], 'type': raw[8], 'sha256_record': sha(raw)}
        structures.append(row)
        if row['state_raw']:
            feature(f'structure.initial.type.{row["type"]}')
    unit_counts = Counter((u['proprietario_id'], u['owner_after_documented_load_override'], u['tipo'],
                           u['byte_estado']) for u in units)
    structure_counts = Counter((s['owner_raw'], s['type'], s['state_raw']) for s in structures)
    owners = sorted({u['owner_after_documented_load_override'] for u in units if u['byte_estado']} |
                    {s['owner_raw'] for s in structures if s['state_raw']})
    players = []
    for owner in sorted(set(range(4)) | set(owners)):
        role = ('human (new-campaign convention; inherited type not in ETA)' if owner == 0 else
                'AI (new-campaign convention; inherited type not in ETA)' if owner in (1, 2, 3) else
                'monster/raid owner' if owner == 4 else 'owner-200 sentinel; gameplay kind unknown' if owner == 200 else 'unknown')
        players.append({'owner': owner, 'kind_annotation': role if campaign else ('session-configured; unknown' if owner < 4 else role),
                        'control_type_serialized': None, 'has_active_serialized_entities': owner in owners})
    if campaign and any(x in owners for x in (1, 2, 3)):
        feature('owner.opponent_clan_entities')
    if 4 in owners:
        feature('owner.monster_entities')
    if 200 in owners:
        feature('owner.sentinel_200_entities')
    conditions = []
    # Reuse actual loader; poison proves that no unprovided parameter is invented.
    condition_memory = bytearray(b'\xa5' * 114)
    loaded = carregar_condicoes_fim(Leitor(data, blocks['tabela_458b05']['offset']), condition_memory)
    assert loaded.fim == blocks['tabela_458b05']['fim']
    for i, (_, offset, raw) in enumerate(records(data, blocks['tabela_458b05'])):
        kind, params = raw[0], words(raw[2:])
        row = {'ordinal': i, 'offset': offset, 'raw_hex': raw.hex(), 'kind_raw': kind,
               'pad_raw': raw[1], 'parameters_u16': params,
               'decoded_kind': CONDITIONS.get(kind, 'ignored_by_current_evaluator')}
        conditions.append(row)
        if kind != 255 or i == 0:
            feature(f'condition.kind.{kind}')
        if kind == 4:
            feature(f'condition.required_structure.{params[0]}')
            row['zone_words'] = params[1:]
            row['wildcard_rule'] = '255 is wildcard; 65535 is not'
    objective_memory = bytearray(b'\xa5' * 804)
    loaded_obj = carregar_objetivos(Leitor(data, blocks['listas_por_jogador']['offset']), objective_memory)
    assert loaded_obj.fim == blocks['listas_por_jogador']['fim']
    objectives = []
    objective_flags = []
    obj_block = blocks['listas_por_jogador']
    for i in range(400):
        offset = obj_block['offset'] + i * 3
        word, flag = struct.unpack_from('<HB', data, offset)
        objective_flags.append(flag)
        if word != 65535:
            objectives.append({'player': i // 100, 'ordinal': i % 100, 'word_raw': word, 'discarded_flag_raw': flag})
    aux = {}
    for name in ('tabela_47534a', 'tabela_47c24d', 'tabela_47bcc7', 'tabela_47c04a', 'tabela_47ac30'):
        entries = []
        for ordinal, offset, raw in records(data, blocks[name]):
            row = {'ordinal': ordinal, 'offset': offset, 'words_raw': words(raw)}
            if name == 'tabela_47534a':
                row.update(cell=words(raw)[0], capacity_raw=words(raw)[1])
                if row['cell']:
                    feature('resource.mine_table_nonzero_origin')
            elif name == 'tabela_47c24d':
                row['bytes_raw'] = list(raw)
                row['field_meanings'] = 'unknown; serialized IALoadAttaqueIni record, no attack activation inferred'
            elif name == 'tabela_47c04a':
                row.update(rectangle_xyxy_u16=words(raw)[:4], tail_u16_unknown=words(raw)[4])
            elif name == 'tabela_47ac30':
                cell, mask, period = words(raw)
                row.update(cell=cell, group_mask=mask, period_disk=period,
                           period_after_loader_low16=(period*30) & 65535,
                           is_used_disk_slot=cell != 65535)
                if cell != 65535:
                    feature('raid.used_monster_entry')
                    if period:
                        feature('raid.periodic_entry')
                    for g in range(16):
                        if mask >> g & 1:
                            feature(f'raid.profile_group.{g}')
            entries.append(row)
        aux[name] = {'count': len(entries), 'records': entries}
    if blocks['tabela_47c24d']['quantidade']:
        feature('script.initial_attack_records')
    if blocks['tabela_47bcc7']['quantidade']:
        feature('script.ghost_records')
    if blocks['tabela_47c04a']['quantidade']:
        feature('influence.rectangles')
    if stage == 6:
        feature('special.mission06_illumination_result_override')
    if stage in (8, 13):
        feature('special.mission08_13_structure_owner_tally')
    if stage == 23:
        feature('special.mission23_monster_reserve_and_advance_branch')
    # Keep render/data IDs separate from behavior selectors used in the ranking.
    layers = {name: hist(parsed[name]) for name in ('terreno', 'objetos', 'atributos', 'variantes')}
    # Resource object codes from the committed economy reader; source bytes
    # stay distinct from MissionLoad's 54 -> 66, quantity 1 normalization.
    resource_objects = {}
    for name, predicate in [('food_fields', lambda t: 0x1d <= t <= 0x34),
                            ('parts_sacks', lambda t: t in (54, 66)),
                            ('food_sacks', lambda t: t == 67),
                            ('stone_sacks', lambda t: t == 68)]:
        count = sum(predicate(t) for t in parsed['objetos'])
        resource_objects[name] = {'cells_in_playable_rectangle': count,
                                  'quantity_total': sum((1 if t == 54 else q) for t, q in zip(parsed['objetos'], parsed['variantes']) if predicate(t)) if name != 'food_fields' else None}
        if count:
            feature('resource.' + name)
    eligible = []
    auto = []
    if campaign:
        for row in catalog['research_declarations']:
            fields = row['declared_fields']
            if fields.get('MISSION') is not None and fields['MISSION'] <= stage:
                eligible.append(row['section'])
            if fields.get('APPARITION') is not None and fields['APPARITION'] <= stage:
                auto.append(row['section'])
        # Gate-qualified declarations, deliberately not called unlocks.
        for section in eligible:
            feature(f'research.declared_mission_gate.{section}')
        for section in auto:
            feature(f'research.declared_apparition_gate.{section}')
    briefing = cd / f'WORLD/MONDE{stage:02d}.TXT' if campaign else None
    return {'id': stem, 'source': source(cd, path), 'campaign': campaign,
            'stage_numeric': stage, 'campaign_selection': selected.get(stem) if campaign else None,
            'campaign_selection_status': ('selected_by_MakeMissionName' if stem in selected else
                                          'base_asset_not_selected_by_current_MakeMissionName' if campaign else 'non_campaign_network_map'),
            'briefing_source': source(cd, briefing) if briefing and briefing.exists() else None,
            'size': {'width': parsed['largura'], 'height': parsed['altura'], 'cell_stride': 256},
            'players': players, 'alliance_state': UNKNOWN, 'weather_state': UNKNOWN,
            'illumination_state': UNKNOWN,
            'resources_by_id_by_owner_0_to_3': parsed['recursos_por_tipo'],
            'resource_ids': {'0': 'parts', '1': 'food', '2': 'stone'},
            'resource_object_summary': resource_objects,
            'camera_origins_by_owner': parsed['origens_visualizacao'],
            'units': units,
            'unit_counts': [{'owner_disk': o, 'owner_after_documented_load_override': a,
                             'type': t, 'state_raw': s, 'count': c}
                            for (o, a, t, s), c in sorted(unit_counts.items())],
            'structures': structures,
            'structure_counts': [{'owner_disk': o, 'type': t, 'state_raw': s, 'count': c}
                                 for (o, t, s), c in sorted(structure_counts.items())],
            'technology': {'actual_unlocked_per_owner': UNKNOWN,
                           'declared_mission_gate_satisfied': eligible,
                           'declared_apparition_gate_satisfied': auto,
                           'note': 'Lists reference catalog declarations; eligibility is not invention, unlock, research progress or order availability.'},
            'end_conditions': conditions,
            'end_evaluator_specials': [f for f in sorted(features) if f.startswith('special.') and 'monster' not in f],
            'defeat': {'serialized_defeat_kind': None, 'known_shared_evaluator': '0x458606: live word 0x4e1a3a == 0 forces completion with victory latch 0; not a disk defeat record'},
            'auxiliary_tables': aux,
            'objective_list': {'record_count': 400, 'non_ffff_word_records': objectives,
                               'discarded_flag_histograms_by_player': [hist(objective_flags[p*100:p*100+100]) for p in range(4)],
                               'words_after_existing_loader_histogram': hist(words(objective_memory[:800])),
                               'note': 'Flags discarded by loader. These lists do not replace end conditions.'},
            'discarded_divers_hex': data[blocks['bytes_descartados']['offset']:blocks['bytes_descartados']['fim']].hex(),
            'layer_histograms_playable_rectangle': layers,
            'full_layer_sha256': {n: sha(data[a:b]) for n, a, b in
                                   [('attributes', 4, 0x10004), ('terrain', 0x10004, 0x30004),
                                    ('objects', 0x30004, 0x40004), ('auxiliary', 0x40004, 0x50004)]},
            'blocks': parsed['blocos'], 'unknown_suffix': parsed['sufixo'],
            'features': sorted(features)}


def covers(missions, include_unselected=False, include_declarations=True):
    rows = {m['id']: {f for f in m['features'] if include_declarations or not f.startswith('research.')}
            for m in missions if m['campaign'] and
            (include_unselected or m['campaign_selection'] is not None)}
    baseline = rows['MONDE01']
    universe = set().union(*rows.values())
    candidates = sorted(set(rows) - {'MONDE01'})
    target = universe - baseline
    order, covered = [], set(baseline)
    while universe - covered:
        name = min((x for x in candidates if x not in order),
                   key=lambda x: (-len(rows[x] - covered), x))
        added = rows[name] - covered
        assert added
        order.append(name)
        covered |= rows[name]
    best = {}
    for k in (1, 2, 3):
        winners, score = [], -1
        for combo in combinations(candidates, k):
            union = set().union(*(rows[n] for n in combo)) - baseline
            if len(union) > score:
                score, winners = len(union), [combo]
            elif len(union) == score:
                winners.append(combo)
        # Among equally large covers prefer exercising the separately loaded
        # attack table, then deterministic lexical order. Scores stay equal.
        chosen = min(winners, key=lambda c: (-int(any('script.initial_attack_records' in rows[n] for n in c)), c))
        covered_new = set().union(*(rows[n] for n in chosen)) - baseline
        best[str(k)] = {'missions': list(chosen), 'new_features_covered': score,
                         'new_features_total': len(target), 'covers_all': covered_new == target,
                         'missing_features': sorted(target - covered_new),
                         'tied_optimal_sets': [list(x) for x in winners]}
    # Exact minimum, independently of greedy: bit masks + branch on rarest
    # uncovered feature. Every possible covering solution is represented.
    bits = {f: 1 << i for i, f in enumerate(sorted(target))}
    masks = {n: sum(bits[f] for f in rows[n] & target) for n in candidates}
    all_mask = (1 << len(bits)) - 1
    incumbent = order[:]
    seen = {}
    def search(covered_mask, chosen):
        nonlocal incumbent
        if covered_mask == all_mask:
            if len(chosen) < len(incumbent):
                incumbent = chosen[:]
            return
        if len(chosen) >= len(incumbent):
            return
        if seen.get(covered_mask, len(incumbent)+1) <= len(chosen):
            return
        seen[covered_mask] = len(chosen)
        remaining = all_mask ^ covered_mask
        gains = {n: bin(mask & remaining).count('1') for n, mask in masks.items()}
        maximum = max(gains.values())
        if len(chosen) + (bin(remaining).count('1')+maximum-1)//maximum >= len(incumbent):
            return
        alternatives = min(([n for n, mask in masks.items() if mask & bit]
                            for bit in bits.values() if bit & remaining), key=len)
        for name in sorted(alternatives, key=lambda n: (-gains[n], n)):
            search(covered_mask | masks[name], chosen + [name])
    search(0, [])
    rare = [{'feature': f, 'missions': [n for n in sorted(rows) if f in rows[n]]}
            for f in sorted(universe) if sum(f in row for row in rows.values()) in (1, 2)]
    forced_by = {r['feature']: r['missions'][0] for r in rare
                 if len(r['missions']) == 1 and r['feature'] in target}
    forced = sorted(set(forced_by.values()))
    residual = target - set().union(*(rows[n] for n in forced))
    largest_residual_single = max(len(residual & row) for row in rows.values())
    certificate_lower_bound = len(forced) + (2 if largest_residual_single < len(residual) else int(bool(residual)))
    assert certificate_lower_bound == len(incumbent), 'Minimum needs a stronger independent certificate'
    return {'baseline': 'MONDE01', 'campaign_feature_total': len(universe),
            'baseline_feature_count': len(baseline), 'new_feature_total': len(target),
            'candidate_scope': ('all 38 ETA files' if include_unselected else '34 ETA files selectable by documented MakeMissionName') + '; NET excluded',
            'includes_declarative_research_gates': include_declarations,
            'tie_break': 'single/greedy: lexical ID; exact equal-score sets: prefer presence of initial attack records, then lexical ID; equal weights per feature',
            'greedy_order': order,
            'greedy_steps': [{'mission': n, 'added_features': sorted(rows[n] - baseline - set().union(*(rows[p] for p in order[:i])))}
                             for i, n in enumerate(order)],
            'exact_best_up_to_three': best,
            'exact_minimum_additional_cover': {'missions': sorted(incumbent), 'count': len(incumbent),
                                              'search_states': len(seen), 'covers_all': set().union(*(rows[n] for n in incumbent), baseline) == universe},
            'minimum_certificate': {'singleton_features_force': forced_by, 'forced_missions': forced,
                                    'features_left_after_forced': sorted(residual),
                                    'largest_single_mission_residual_coverage': largest_residual_single,
                                    'lower_bound': certificate_lower_bound,
                                    'explanation': 'Five forced missions leave 13 features; no one remaining mission supplies all 13. The exhibited seven-map set covers the universe.'},
            'rare_campaign_features': rare}


def products(cd):
    catalog = catalogs(cd)
    selected = selection_paths()
    paths = sorted((p for p in cd.rglob('*') if p.suffix.upper() in ('.ETA', '.NET')),
                   key=lambda p: (p.suffix.upper() != '.ETA', p.name))
    missions = [inventory_map(cd, p, catalog, selected) for p in paths]
    previous = json.loads((ROOT / 'pesquisas-paralelas/missoes/evidencias/inventario.json').read_text())
    old = {r['path']: r for r in previous['assets']}
    for m in missions:
        ref = old[m['source']['path']]
        assert all(ref[k] == m['source'][k] for k in ('size', 'sha256'))
        if m['campaign']:
            assert ref['blocks'] == m['blocks']
            briefing = m['briefing_source']
            assert old[briefing['path']]['sha256'] == briefing['sha256']
    assert sum(m['campaign'] for m in missions) == 38
    assert sum(len(m['units']) for m in missions if m['campaign']) == 2604
    sources = [source(cd, cd / p) for p in ('INSTALHD/RISING.EXE', 'INSTALHD/RISING.INI',
               'INSTALHD/MONSTRE.INI', 'INSTALHD/EVENTS.INI', 'INSTALHD/RISING.SBL')]
    events = ler_ini((cd / 'INSTALHD/EVENTS.INI').read_bytes())
    inventory = {'schema': 'rising-lands/static-campaign-inventory/1',
                 'original_sources': sources,
                 'reader_provenance': [{'path': p, 'sha256': sha((ROOT / p).read_bytes())} for p in DEPENDENCIES],
                 'catalog': catalog,
                 'global_event_ids': dict(events.items('EVENEMENT')),
                 'events_note': 'Global EVENT IDs are not mission IDs; no per-map event schedule inferred from EVENTS.INI or briefing prose.',
                 'counts': {'campaign_eta': 38, 'numbered_stages': 25, 'network_maps': 5,
                            'campaign_serialized_unit_records': 2604}, 'maps': missions}
    analysis = covers(missions)
    analysis['all_eta_including_unselected'] = covers(missions, include_unselected=True)
    analysis['without_declarative_research_gates'] = covers(missions, include_declarations=False)
    campaign_features = set().union(*(set(m['features']) for m in missions if m['campaign']))
    network_features = set().union(*(set(m['features']) for m in missions if not m['campaign']))
    analysis['network_only_features'] = sorted(network_features - campaign_features)
    initial_unit_types = {u['tipo'] for m in missions if m['campaign'] for u in m['units'] if u['byte_estado']}
    initial_structure_types = {s['type'] for m in missions if m['campaign'] for s in m['structures'] if s['state_raw']}
    analysis['absent_from_all_campaign_initial_entities'] = {
        'unit_types': [u for u in catalog['unit_types'] if u['id'] not in initial_unit_types],
        'structure_types': [s for s in catalog['structure_types'] if s['id'] not in initial_structure_types],
        'note': 'Absence from initial entities is not absence from gameplay: recruitment, research, production and scripts can introduce content.'}
    feature_ids = sorted(set().union(*(set(m['features']) for m in missions)))
    matrix = {'schema': 'rising-lands/static-content-matrix/1',
              'feature_ids': feature_ids,
              'definition': 'Binary serialized/declared/static-code selector presence, not dynamic reach. Unit/structure features require nonzero disk state; thresholds, counts, raw tile IDs and unknown state do not inflate ranking. Research declarations are separately labelled.',
              'rows': [{'mission': m['id'], 'campaign': m['campaign'],
                        'present': [int(f in m['features']) for f in feature_ids]} for m in missions]}
    overview = []
    for m in missions:
        aux = m['auxiliary_tables']
        used = [r for r in aux['tabela_47ac30']['records'] if r['is_used_disk_slot']]
        overview.append({'mission': m['id'], 'campaign': m['campaign'], 'stage': m['stage_numeric'],
                         'selection_status': m['campaign_selection_status'], 'size': m['size'],
                         'serialized_unit_count': len(m['units']), 'unit_counts_by_owner_type_state': m['unit_counts'],
                         'serialized_structure_count': len(m['structures']), 'structure_counts_by_owner_type_state': m['structure_counts'],
                         'initial_resources': m['resources_by_id_by_owner_0_to_3'],
                         'end_conditions': [{'kind': r['kind_raw'], 'decoded': r['decoded_kind'], 'parameters': r['parameters_u16']}
                                            for r in m['end_conditions'] if r['kind_raw'] != 255],
                         'mines_nonzero_origin': sum(bool(r['cell']) for r in aux['tabela_47534a']['records']),
                         'attack_record_count': aux['tabela_47c24d']['count'],
                         'used_monster_entry_count': len(used),
                         'monster_periods_after_load_low16': sorted({r['period_after_loader_low16'] for r in used}),
                         'feature_count': len(m['features']),
                         'feature_count_without_research_declarations': sum(not f.startswith('research.') for f in m['features'])})
    return {'inventory.json': inventory, 'matrix.json': matrix, 'coverage.json': analysis, 'overview.json': overview}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cd-root', required=True, type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = products(args.cd_root.resolve())
    for name, value in result.items():
        raw = canonical(value)
        path = HERE / name
        if args.check:
            assert path.read_bytes() == raw, f'Out of date: {name}'
        else:
            path.write_bytes(raw)
    best = {k: {f: row[f] for f in ('missions', 'new_features_covered', 'new_features_total')}
            for k, row in result['coverage.json']['exact_best_up_to_three'].items()}
    print(json.dumps({'mode': 'check' if args.check else 'generate', 'counts': result['inventory.json']['counts'],
                      'best': best,
                      'exact_minimum': result['coverage.json']['exact_minimum_additional_cover']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
