"""Export the intact intervals and static inventories behind the AI/runtime contract.

Run from any directory: ``python3 -B pesquisas-paralelas/ia-runtime/extrair_contrato_ia.py``.
Writes ``evidencias/manifesto.json`` (every interval with its SHA-256),
one ``.asm`` listing per code interval and ``evidencias/inventario.json``.
Only original bytes and original SBL names are read; nothing is executed.
"""
import hashlib
import json

from ambiente_ia_runtime import ANALYSIS_SHA256, EVIDENCE, ORIGINAL_SHA256, ROOT, SBL
from inventario_ia_runtime import OriginalImage, interval_record

BASE_MAIN = '8a499a9'
CORE_INPUTS = ('ferramentas/ia.py', 'ferramentas/tarefas_ia.py', 'ferramentas/simbolos_ia.py',
               'ferramentas/ordens_unidades.py', 'ferramentas/mensagens_chegada.py', 'ferramentas/cadencia.py',
               'ferramentas/emulador.py', 'ferramentas/analisar.py', 'relatorios/regras-ia.json',
               'relatorios/simbolos-originais.tsv')

# (group, routine entry, exclusive end or None for the next SBL symbol). ProgIteration's
# SBL successor is 0x475118, but an unnamed routine starts after its ret at 0x47509d.
ROUTINES = (
    ('frame', 0x47500e, 0x47509d), ('frame', 0x42c868, None), ('frame', 0x45d015, None),
    ('frame', 0x47fbea, None), ('frame', 0x47fbfd, None), ('frame', 0x46d628, None),
    ('unit-dispatch', 0x456db5, None), ('unit-dispatch', 0x45442c, None),
    ('structure-dispatch', 0x4281c7, None), ('structure-dispatch', 0x4268d4, None),
    ('ai-player', 0x47f927, None),
    ('ai-tables', 0x47fb15, None), ('ai-tables', 0x47f328, None), ('ai-tables', 0x47f36e, None),
    ('ai-tables', 0x47cfd0, None), ('ai-tables', 0x47d1a4, None), ('ai-tables', 0x47d220, None),
    ('ai-tables', 0x4826a4, None), ('ai-tables', 0x48270b, None), ('ai-tables', 0x484214, None),
    ('ai-tables', 0x484310, None), ('ai-tables', 0x484bc4, None), ('ai-tables', 0x485002, None),
    ('ai-tables', 0x48614c, None), ('ai-tables', 0x4864c1, None), ('ai-tables', 0x48134c, None),
    ('ai-tables', 0x47af90, None), ('ai-tables', 0x47c162, None), ('ai-tables', 0x47fc54, None),
    ('ai-tables', 0x483bd8, None), ('ai-tables', 0x4846a7, None), ('ai-tables', 0x48569a, None),
    ('ai-tables', 0x486ca7, None),
    ('messages', 0x4829c8, None), ('messages', 0x484808, None),
)
DATA_TABLES = (
    ('CalculGame state table', 0x42c804, 25),
    ('EnginNextEtape type table (types 11..16)', 0x45432c, 6),
    ('EnginNextEtape type table (types 0..25)', 0x454344, 26),
    ('EnginNextEtape type table (types 11..17)', 0x4543ac, 7),
    ('EnginNextEtape state table', 0x4543c8, 25),
    ('BatimentNextEtape type table', 0x426880, 21),
    ('iagUnitSendMessage message table', 0x482998, 12),
    ('iagVilleSendMessage message table', 0x4847f8, 4),
    ('unit behavior table (group byte +0x1b)', 0x498e94, 12),
)
BEHAVIOR_SLOTS = (0x48, 0x4a, 0x49, 0x4c, 0x4b)  # message served by each 4-byte slot of a behavior record
# Callee-name rules used only to label the provider family each operation needs;
# the agreed owner of every family is recorded in docs/AI_RUNTIME.md. Rules are
# tried in order; a rule matches a name prefix or, for ghosts, a substring.
FAMILIES = (
    ('ai-runtime AI state', ('iag', 'iaGroup', 'iab', 'iaf', 'iaConfig'), ()),
    ('core rule VM', ('iaProb', 'iaSolver', 'list'), ()),
    ('core RNG', ('iaRandom', 'Random'), ()),
    ('user interface', ('MessageBox', 'BatimentSelection', 'BatimentDeselectionner'), ()),
    ('C runtime', ('memset', 'sprintf', '__CHP'), ()),
    ('combat', ('SetAttaque', 'EnginTrouveCible', 'Tourelle', 'Projectile'), ()),
    ('structure ghosts', (), ('Ghost',)),
    ('economy resources/production/technology', ('Ressource', 'GetRessource', 'TestRessource', 'Champ', 'Mine',
                                                 'GetIndiceMine', 'Piece', 'Bag', 'Marche', 'Recherche', 'Matiere',
                                                 'Cave', 'Sac', 'GetNbrPatates', 'InventionFuture',
                                                 'TypeBatimentEstRealisable', 'InitRecruteTroupe'), ()),
    ('economy players/diplomacy', ('Player', 'MAJSympathie', 'Sympathie', 'Alliance'), ()),
    ('core units', ('Engin', 'SetDeplace', 'Deplace', 'RetireEngin', 'TypeEngin', 'SetDying', 'GetEngin', 'SetEngin',
                    'SetDepot', 'SetRecolte', 'SetMine', 'SetTransporte', 'SetRamasse', 'SetDechargeCave', 'PlaceEngin',
                    'ChercheType', 'CreerEngin'), ()),
    ('structures', ('Batiment', 'GetCaseIndiceBatiment', 'GetNumIndice', 'ChercheIndiceBatiment', 'ChercheCaseBatiment',
                    'GetTypeBatiment', 'DetectPlaceLibre', 'GetNbTroupes', 'GetIndiceBatiment', 'GetCaseBatPlace'), ()),
    ('core terrain/navigation', ('Terrain', 'Case', 'Chemin', 'Decouvre', 'Illumine', 'MiniMap', 'Veget',
                                 'Distance', 'Direction', 'GetFreeCaseZone'), ()),
    ('missions', ('Mission',), ()),
)


def family(name):
    for label, prefixes, fragments in FAMILIES:
        if name and (name.startswith(prefixes) or any(f in name for f in fragments)):
            return label
    return 'unclassified'


def hexs(values):
    return [f'0x{v:08x}' for v in values]


def named_calls(image, calls):
    return [dict(address=f'0x{target:08x}', name=image.name(target), sites=hexs(sorted(sites)))
            for target, sites in sorted(calls.items())]


def summarize(image, walked):
    return dict(entry=f'0x{walked["entry"]:08x}', instructions=walked['instructions'],
                calls=named_calls(image, walked['calls']),
                imports={name: hexs(sites) for name, sites in sorted(walked['imports'].items())},
                indirect_calls=hexs(walked['indirect_calls']),
                tail_calls={f'0x{a:08x}': n for a, n in sorted(walked['tail_calls'].items())},
                stops_reached=hexs(walked['stops_reached']), returns=hexs(walked['returns']))


def routine_intervals(image):
    """Each routine's own interval plus the shared Watcom tails its paths reach."""
    result = []
    for group, start, end in ROUTINES:
        end = end or image.symbol_end(start)
        name = image.name(start) or f'sub_{start:08x}'
        walked = image.walk(start, [(start, end)])
        tails = image.shared_chunks(walked)
        result.append((group, name, start, end, tails, walked))
    return result


def operations(image):
    rules = json.loads((ROOT / 'relatorios/regras-ia.json').read_text(encoding='utf-8'))
    by_address = {}
    for op in rules['operacoes']:
        if op['endereco'] is None:
            continue
        by_address.setdefault(int(op['endereco'], 16), []).append(op)
    implemented = core_implemented_operations([op['nome_original'] for op in rules['operacoes']])
    records = []
    for address in sorted(by_address):
        end = image.symbol_end(address)
        walked = image.walk(address, [(address, end)])
        callee_names = sorted({image.name(t) or f'sub_{t:08x}' for t in walked['calls']} |
                              {n for n in walked['tail_calls'].values()})
        families = sorted({family(n) for n in callee_names}) or ['no callee (arithmetic or direct table access)']
        accesses = image.absolute_accesses(address, end, walked['visited'])
        names = [op['nome_original'] for op in by_address[address]]
        records.append(dict(
            address=f'0x{address:08x}', end_exclusive=f'0x{end:08x}', names=names,
            occurrences={op['nome_original']: len(op['ocorrencias']) for op in by_address[address]},
            sha256=hashlib.sha256(image.read(address, end)).hexdigest(), instructions=walked['instructions'],
            callees=callee_names, imports=sorted(walked['imports']), indirect_calls=hexs(walked['indirect_calls']),
            shared_tails=[f'0x{a:08x}..0x{b:08x}' for a, b in image.shared_chunks(walked)],
            globals=sorted({f'0x{a["address"]:08x}/{a["width"]}/{a["access"]}' for a in accesses}),
            provider_families=families,
            core_status={n: implemented[n] for n in names}))
    unresolved = [op['nome_original'] for op in rules['operacoes'] if op['endereco'] is None]
    return dict(names=len(rules['operacoes']), addresses=len(records), instructions=rules['quantidade_instrucoes'],
                unresolved_names=unresolved, records=records)


def core_implemented_operations(names):
    """Probe core's committed MaquinaTarefas without a world: which names it already serves."""
    from tarefas_ia import MaquinaTarefas
    from simbolos_ia import ProgramaRegras
    machine = MaquinaTarefas(ProgramaRegras(0, 0, (), tuple([0] * 64)), operacoes={}, missao=1, mundo=None)
    machine.memoria = bytearray(100 * 96)
    status = {}
    for name in names:
        try:
            machine.executar_operacao(name, [1, 1, 1, 1, 1, 1], 0, 0)
            status[name] = 'core: implemented without world state'
        except NotImplementedError as error:
            text = str(error)
            status[name] = ('core: implemented, needs unit world' if 'Estado das unidades' in text
                            else 'pending: world operation not reconstructed')
    return status


def dispatch_inventory(image):
    ene = (0x45442c, 0x456c34)
    states = image.table(0x4543c8, 25)
    unit_states = []
    for state, target in enumerate(states):
        walked = image.walk(target, [ene], stops={0x454ccd})
        unit_states.append(dict(state=state, target=f'0x{target:08x}', **{
            k: v for k, v in summarize(image, walked).items() if k != 'entry'}))
    prelude = image.walk(0x45442c, [ene], stops={0x456c1c, 0x454ccd})
    bne = (0x4268d4, 0x4281c7)
    types = []
    for index, target in enumerate(image.table(0x426880, 21)):
        walked = image.walk(target, [bne], stops={0x4281c0})
        types.append(dict(type=index + 1, target=f'0x{target:08x}', **{
            k: v for k, v in summarize(image, walked).items() if k != 'entry'}))
    game_states = image.table(0x42c804, 25)
    frame_body = image.walk(0x42d3e1, [(0x42c868, 0x42d4f8)], stops={0x42d4e2, 0x42d4ea, 0x42c92c})
    input_loop = image.walk(0x42d2de, [(0x42c868, 0x42d4f8)], stops={0x42d3c0, 0x42d4ea})
    return dict(
        calcul_game=dict(state_byte='0x004e2f78', entry_state_copy='[esp+0x104]', table='0x0042c804',
                         targets={str(i): f'0x{t:08x}' for i, t in enumerate(game_states)},
                         gates=dict(gate_1='0x0042d14c', gate_2='0x0042d2e3', gate_3='0x0042d3c0'),
                         input_loop=summarize(image, input_loop), frame_body=summarize(image, frame_body)),
        engin_next_etape=dict(loop=summarize(image, image.walk(0x456db5, [(0x456db5, 0x456f0a)])),
                              prelude=summarize(image, prelude), state_switch='0x00456c1c',
                              state_table='0x004543c8', exit='0x00454ccd', states=unit_states),
        batiment_next_etape=dict(loop=summarize(image, image.walk(0x4281c7, [(0x4281c7, 0x4283e2)])),
                                 type_table='0x00426880', exit='0x004281c0', types=types),
        ia_calcul_player=summarize(image, image.walk(0x47f927, [(0x47f927, 0x47fa2f)])))


def message_inventory(image, xref_sites):
    result = {}
    for entry, base, table in ((0x4829c8, 0x41, 0x482998), (0x484808, 0x01, 0x4847f8)):
        end = image.symbol_end(entry)
        walked = image.walk(entry, [(entry, end)])
        count = walked['jump_tables'][min(walked['jump_tables'])]['count']
        branches = []
        for i, target in enumerate(image.table(table, count)):
            branch = image.walk(target, [(entry, end)])
            branches.append(dict(message=f'0x{base + i:02x}', target=f'0x{target:08x}',
                                 calls=[c['name'] or c['address'] for c in named_calls(image, branch['calls'])],
                                 indirect_calls=hexs(branch['indirect_calls'])))
        callers = []
        for site in xref_sites.get(entry, ()):
            code = image.immediate_before(site, 'edx')
            callers.append(dict(site=f'0x{site:08x}', routine=image.owner(site)[1],
                                message=f'0x{code:02x}' if code is not None else 'computed'))
        result[image.name(entry)] = dict(entry=f'0x{entry:08x}', end_exclusive=f'0x{end:08x}',
                                         message_table=f'0x{table:08x}', first_message=f'0x{base:02x}',
                                         branches=branches, callers=callers,
                                         globals=sorted({f'0x{a["address"]:08x}/{a["width"]}/{a["access"]}'
                                                         for a in image.absolute_accesses(entry, end, walked['visited'])}))
    behaviors = []
    for index, pointer in enumerate(image.table(0x498e94, 12)):
        record = dict(index=index, record=f'0x{pointer:08x}')
        if 0x498000 <= pointer < 0x499000:
            record['handlers'] = {f'0x{m:02x}': (image.name(h) if h else None)
                                  for m, h in zip(BEHAVIOR_SLOTS, image.table(pointer, 5))}
        else:
            record['handlers'] = 'record outside initialized data; resolved at run time only'
        behaviors.append(record)
    result['behaviors'] = dict(table='0x00498e94', selector='group byte +0x1b (written by V_AffecteComportement 0x4897a5)',
                               slot_messages=[f'0x{m:02x}' for m in BEHAVIOR_SLOTS], records=behaviors)
    return result


def caller_index(image, targets):
    """Direct callers of ``targets`` found by decoding every named routine of the image."""
    targets, found = set(targets), {}
    code_starts = [a for a in image.starts if 0x401000 <= a < 0x494000]
    for start, end in zip(code_starts, code_starts[1:] + [0x494000]):
        address = start
        while address < end:
            try:
                insn = image.instruction(address)
            except ValueError:
                address += 1
                continue
            target = image.direct_target(insn)
            if insn.mnemonic == 'call' and target in targets:
                found.setdefault(target, []).append(insn.address)
            address += insn.size
    return {t: sorted(s) for t, s in found.items()}


def table_inventory(image, routines):
    tables = {}
    for group, name, start, end, tails, walked in routines:
        if group != 'ai-tables':
            continue
        accesses = image.absolute_accesses(start, end, walked['visited'])
        for a, b in tails:
            accesses += image.absolute_accesses(a, b, walked['visited'])
        tables[name] = dict(entry=f'0x{start:08x}', calls=[c['name'] or c['address'] for c in named_calls(image, walked['calls'])],
                            globals=sorted({(a['address'], a['width'], a['access'], a['index'] or '', a['base'] or '')
                                            for a in accesses}))
        tables[name]['globals'] = [dict(address=f'0x{a:08x}', width=w, access=x, base=b or None, index=i or None)
                                   for a, w, x, i, b in tables[name]['globals']]
    return tables


def build():
    """Manifest, inventory and listings computed from the intact image (nothing written)."""
    image = OriginalImage()
    routines = routine_intervals(image)
    intervals, listings = [], {}
    for group, name, start, end, tails, walked in routines:
        filename = f'{start:08x}.asm'
        body = image.listing(start, end, f'{name} ({group})', image.code_end(walked, start, end))
        for a, b in tails:
            body += '\n' + image.listing(a, b, f'shared Watcom tail reached from {name}')
        listings[filename] = body
        record = interval_record(image, name, start, end)
        record.update(group=group, file=filename, code_end=f'0x{image.code_end(walked, start, end):08x}',
                      shared_tails=[interval_record(image, f'{name} shared tail', a, b) for a, b in tails])
        intervals.append(record)
    data = [dict(interval_record(image, name, address, address + 4 * count, kind='data'),
                 entries=count, values=hexs(image.table(address, count))) for name, address, count in DATA_TABLES]
    ops = operations(image)
    for record in ops['records']:
        intervals.append(dict(interval_record(image, '/'.join(record['names']), int(record['address'], 16),
                                              int(record['end_exclusive'], 16)), group='operations', file=None))
    xref = caller_index(image, (0x4829c8, 0x484808, 0x47f36e, 0x47fb15, 0x47f328, 0x47c162, 0x453062,
                                0x451914, 0x44bc74, 0x44f2d4, 0x4259e6, 0x42c868, 0x456db5, 0x4281c7,
                                0x47f927, 0x45d015, 0x45442c, 0x4268d4))
    manifest = dict(original_sha256=ORIGINAL_SHA256, analysis_sha256=ANALYSIS_SHA256,
                    analysis_note='Normalized analysis PE is a different identity; no interval here was read from it.',
                    sbl_sha256=hashlib.sha256(SBL.read_bytes()).hexdigest(), base_main=BASE_MAIN,
                    core_inputs={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in CORE_INPUTS},
                    intervals=intervals, data_tables=data)
    inventory = dict(original_sha256=ORIGINAL_SHA256,
                     scope='Static reachability over intact bytes; call order is claimed only by the native captures.',
                     dispatch=dispatch_inventory(image), messages=message_inventory(image, xref),
                     ai_tables=table_inventory(image, routines), operations=ops,
                     callers={f'0x{t:08x}': dict(name=image.name(t), sites=[dict(site=f'0x{s:08x}', routine=image.owner(s)[1])
                                                                            for s in xref.get(t, [])])
                              for t in sorted((0x47f36e, 0x47fb15, 0x47f328, 0x47c162, 0x453062, 0x451914, 0x44bc74,
                                               0x44f2d4, 0x4259e6, 0x42c868, 0x456db5, 0x4281c7, 0x47f927, 0x45d015,
                                               0x45442c, 0x4268d4))})
    return manifest, inventory, listings


def export():
    manifest, inventory, listings = build()
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    for filename, text in listings.items():
        (EVIDENCE / filename).write_text(text, encoding='utf-8')
    (EVIDENCE / 'manifesto.json').write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    (EVIDENCE / 'inventario.json').write_text(json.dumps(inventory, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    return manifest, inventory


if __name__ == '__main__':
    m, inv = export()
    print('Intervals:', len(m['intervals']), 'data tables:', len(m['data_tables']),
          'operation addresses:', inv['operations']['addresses'], 'names:', inv['operations']['names'])
