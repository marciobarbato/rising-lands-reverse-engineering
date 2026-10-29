"""M2 byte inventory: the CalculGame frame pipeline and what MONDE01 reaches in it.

Run from any directory: ``python3 -B pesquisas-paralelas/ia-runtime/inventario_quadro_m2.py``.
Writes ``evidencias/inventario-quadro-m2.json``. Reads only the intact executable
bytes, the original SBL names and the frozen accepted M1 post-load state
(``captura-carga-missao-original-v2.json``, final blocks, read-only). Nothing is
executed. The M1 post-load state is MissionLoad's return to ``0x42d22d``; the load
entry tail (RestoreAll, SetClipping, counter reset, MenuInit, InitGameZone) still runs
before the frame body, so values that tail writes are reported as such, not as
frame-1 inputs.
"""
import base64
import hashlib
import json
import struct
import zlib

from ambiente_ia_runtime import EVIDENCE, ORIGINAL_SHA256, ROOT
from inventario_ia_runtime import CONDITIONAL, OriginalImage

M1_CAPTURE = ROOT / 'pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json'
M1_CAPTURE_SHA256 = 'eb7d2303e13e62d4f5692c9cb6ef302b573d138df6a8b51183a6d9b0bd703afc'
M1_FINAL_STATE_SHA256 = '58a5020e79f812e741991410bde0ebc847c927ce141176975a82c0a51a7a1114'
OUTPUT = EVIDENCE / 'inventario-quadro-m2.json'

FRAME_BODY = (0x42d2de, 0x42d4f5)   # CalculGame frame body up to its last reached instruction
UNIT_POOL_POINTER, UNIT_COUNT, UNIT_STRIDE = 0x4e19a0, 800, 276
STRUCTURE_POOL, STRUCTURE_COUNT, STRUCTURE_STRIDE = 0x49a0c8, 1000, 276
PLAYER_POINTER, PLAYER_STRIDE = 0x5080a8, 20
AI_CONTEXT, AI_CONTEXT_STRIDE = 0x51a98c, 16
UNIT_STATE_TABLE, STRUCTURE_TYPE_TABLE = 0x4543c8, 0x426880

# Callee owner, per the agreed table in docs/AI_RUNTIME.md and the M2 brief
# (Core: clocks, fields, animation; Economy: research, materials, market;
# Combat: projectiles; Missions: events and the end condition).
OWNERS = {
    'PlayerAttaqueReset': 'economy', 'EvenementEnCours': 'missions', 'MCICD_Play': 'audio (second wave)',
    'InputGame': 'ai-runtime (input: second wave)', 'InputSend': 'ai-runtime (network: second wave)',
    'InputReceive': 'ai-runtime (network: second wave)', 'MissionGetNum': 'missions',
    'CalculNextReflect': 'ai-runtime', 'PlayerGetType': 'economy',
    'ProcessInputGame': 'ai-runtime', 'MessageBoxCalcul': 'ai-runtime',
    'GameNextFrame': 'ai-runtime', 'CalculIconeAction': 'ai-runtime (interface: second wave)',
    'ProjectileCalcul': 'combat', 'CalculEnginNextEtape': 'ai-runtime', 'CalculBatimentNextEtape': 'ai-runtime',
    'RechercheCalcul': 'economy', 'PlayerInitAllianceCompteur': 'economy', 'SetUpdateChamp': 'core',
    'UpdateChamp': 'core', 'CalculMatiere': 'economy', 'CalculCompteurMarche': 'economy',
    'CalculCompteurProposition': 'economy', 'NextAnimTerrain': 'core', 'NextAnimVegetFullMap': 'core',
    'NextAnimVeget': 'core', 'PlayerAttaqueCalculSympa': 'economy', 'TestFinDeMission': 'missions',
    'MessageBoxSet': 'ai-runtime (interface: second wave)', 'PlaySnd_StopAllSound': 'audio (second wave)',
}
# Gates and branch conditions of the frame body: (address, meaning). Each address
# must decode to a compare/test or a conditional jump in the intact bytes.
GATES = (
    (0x42d2ea, 'gate 2: EvenementEnCours AL != 0 exits at 0x42d4ea (skips the 0x5099b0 clear)'),
    (0x42d2f7, 'byte 0x4e2f28 != 0 skips MCICD_Play'),
    (0x42d380, 'PlayerGetType(cl) AL: 1 -> human input, 2 -> CalculNextReflect, other -> nothing'),
    (0x42d337, 'type 1: cl == local 0x508041 -> InputGame+InputSend, else InputReceive'),
    (0x42d368, 'type 2: cl == local 0x508041 -> InputGame after CalculNextReflect'),
    (0x42d391, 'player loop cl = 0..4 single player'),
    (0x42d3a0, 'network flag 0x4e0730 set: player 4 skipped'),
    (0x42d3be, 'ProcessInputGame for bl = 0..3'),
    (0x42d3c9, 'gate 3: state 0x4e2f78 == 0x12 continues'),
    (0x42d3ce, 'gate 3: state 0x10 continues only with the network flag; else exit 0x42d4e2'),
    (0x42d44d, 'network flag: NextAnimVegetFullMap, else NextAnimVeget'),
    (0x42d478, 'network flag: exit before TestFinDeMission'),
    (0x42d48d, 'TestFinDeMission AL (stored at 0x4e05a0) == 0 exits'),
    (0x42d49c, 'MissionGetNum == 6 and u32 0x4e061c == 0 -> MessageBoxSet(10, 500)'),
    (0x42d4c6, 'u32 0x4e061c += 1; below 100 exits, at 100 stop sound and MenuInit(local, 0x13)'),
)
# EnginNextEtape prelude predicates (static, Stage 1 contract, docs/AI_RUNTIME.md).
SCAN_TYPES = frozenset((0, 1, 2, 3, 8, 11, 12, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 14))
SCAN_STATES_EXCLUDED = frozenset((14, 1, 19))
FATIGUE_TYPES = frozenset(tuple(range(11)) + (25,))


def load_m1_post_load_state():
    raw = M1_CAPTURE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != M1_CAPTURE_SHA256:
        raise ValueError('The frozen accepted M1 capture changed; it must stay read-only')
    capture = json.loads(raw)
    final = capture['oracle']['final_state']
    if final['summary']['sha256'] != M1_FINAL_STATE_SHA256 or capture['oracle']['real_return'] != '0x42d22d':
        raise ValueError('Unexpected M1 post-load state identity')
    blocks = []
    for name, block in final['blocks'].items():
        data = zlib.decompress(base64.b64decode(block['zlib_base64']))
        if len(data) != block['bytes'] or hashlib.sha256(data).hexdigest() != block['sha256']:
            raise ValueError(f'M1 block {name} does not match its recorded size/SHA-256')
        blocks.append((int(block['base'], 16), data))
    return blocks


class PostLoadView:
    def __init__(self, blocks):
        self.blocks = blocks

    def read(self, address, size):
        for base, data in self.blocks:
            if base <= address and address + size <= base + len(data):
                return data[address - base:address - base + size]
        raise KeyError(f'0x{address:08x}+{size} is not inside one M1 block')

    def u8(self, address):
        return self.read(address, 1)[0]

    def u16(self, address):
        return struct.unpack('<H', self.read(address, 2))[0]

    def u32(self, address):
        return struct.unpack('<I', self.read(address, 4))[0]


def frame_pipeline(image):
    calls = []
    for insn in image.decode(*FRAME_BODY):
        if insn.mnemonic == 'call' and insn.op_str.startswith('0x'):
            target = int(insn.op_str, 16)
            name = image.name(target)
            calls.append(dict(site=f'0x{insn.address:08x}', target=f'0x{target:08x}', routine=name,
                              owner=OWNERS[name]))
        elif insn.mnemonic == 'call':
            slot = image.import_slot(insn)
            calls.append(dict(site=f'0x{insn.address:08x}', routine=image.imports[slot], owner='Win32 import'))
    gates = []
    for address, meaning in GATES:
        insn = image.instruction(address)
        if insn.mnemonic not in CONDITIONAL:
            raise ValueError(f'Gate 0x{address:x} is not a conditional jump: {insn.mnemonic}')
        gates.append(dict(site=f'0x{address:08x}', instruction=f'{insn.mnemonic} {insn.op_str}', meaning=meaning))
    return calls, gates


def player_get_type_constant(image):
    """PlayerGetType 0x46d817 returns AL = 2 for any player index >= 4 (0x46d81c/0x46d834)."""
    cmp_, jge, mov = image.instruction(0x46d81c), image.instruction(0x46d81f), image.instruction(0x46d834)
    if (cmp_.op_str, jge.mnemonic, jge.op_str, mov.op_str) != ('edx, 4', 'jge', '0x46d834', 'al, 2'):
        raise ValueError('PlayerGetType bytes differ from the inventoried constant path')
    return 2


def units(view, image):
    pool = view.u32(UNIT_POOL_POINTER)
    table = image.table(UNIT_STATE_TABLE, 25)
    local = view.u8(0x508041)
    result = []
    for index in range(UNIT_COUNT):
        record = view.read(pool + index * UNIT_STRIDE, UNIT_STRIDE)
        owner, kind, state = record[0], record[1], record[2]
        if not state:
            continue
        # Frame 1 runs with u32 0x508f7c = 0 (load entry 0x42d1da step 5 zeroes it).
        scan = ((0 + index) & 0x1f) == 0 and state not in SCAN_STATES_EXCLUDED and owner != 200 and \
            kind in SCAN_TYPES and (kind not in (14, 16) or record[0xda] != 0)
        result.append(dict(
            index=index, owner=owner, type=kind, state=state, branch=f'0x{table[state]:08x}',
            counted=state not in (0, 4), ia_test_utilite=state not in (0, 4),
            counter_4e1a3x='0x4e1a3a (local)' if owner == local else '0x4e1a38', target_scan_frame1=scan,
            fatigue_branch=kind in FATIGUE_TYPES, group=f'0x{struct.unpack_from("<I", record, 0x10c)[0]:08x}',
            spell_bit_byte_dc=record[0xdc], reload_u16_102=struct.unpack_from('<H', record, 0x102)[0]))
    return pool, result


def structures(view, image):
    table = image.table(STRUCTURE_TYPE_TABLE, 21)
    result = []
    for index in range(STRUCTURE_COUNT):
        record = view.read(STRUCTURE_POOL + index * STRUCTURE_STRIDE, STRUCTURE_STRIDE)
        owner, state, kind = record[4], record[5], record[8]
        if not state:
            continue
        branch = 'DemonteBatiment 0x41effd' if state == 3 else (
            f'0x{table[kind - 1]:08x}' if 1 <= kind <= 21 else 'exit 0x4281c0')
        result.append(dict(index=index, owner=owner, state=state, type=kind, branch=branch,
                           counted=owner < 4 and kind not in (9, 12, 17),
                           decouvre_illumine_players=[p for p in range(4) if p != owner],
                           illumination_flags_110=list(record[0x110:0x114])))
    return result


def players(view, image):
    records = view.u32(PLAYER_POINTER)
    constant = player_get_type_constant(image)
    result = []
    for player in range(5):
        kind = view.u8(records + player * PLAYER_STRIDE + 1) if player < 4 else constant
        context = view.read(AI_CONTEXT + player * AI_CONTEXT_STRIDE, AI_CONTEXT_STRIDE)
        entry = dict(player=player, type=kind, type_source=(f'[0x{PLAYER_POINTER:x}]+{player * PLAYER_STRIDE + 1}'
                                                            if player < 4 else 'PlayerGetType constant 0x46d834'))
        if kind == 2:
            entry['calls'] = 'CalculNextReflect(player, MissionGetNum) -> iaCalculPlayer'
            if player == 4:
                entry['ia_calcul_player_path'] = 'AvanceMonstre(4) then iaSolver(0x5148f0)'
            else:
                inactive = context[4]
                entry['context'] = f'0x{AI_CONTEXT + player * AI_CONTEXT_STRIDE:08x}'
                entry['context_bytes'] = context.hex()
                entry['inactive_byte_51a990'] = inactive
                entry['ia_calcul_player_path'] = ('inactive: return 0, no call' if inactive else
                                                  'counters, then iagUnit/Ville/Ress/WarNoyau and iaSolver')
        elif kind == 1:
            entry['calls'] = 'InputGame+InputSend (local)' if player == view.u8(0x508041) else 'InputReceive'
        else:
            entry['calls'] = 'none'
        result.append(entry)
    return result


def build():
    image = OriginalImage()
    view = PostLoadView(load_m1_post_load_state())
    calls, gates = frame_pipeline(image)
    pool, unit_list = units(view, image)
    structure_list = structures(view, image)
    states = {}
    for unit in unit_list:
        states.setdefault(str(unit['state']), dict(branch=unit['branch'], units=[]))['units'].append(unit['index'])
    types = {}
    for structure in structure_list:
        types.setdefault(str(structure['type']), dict(branch=structure['branch'], structures=[]))[
            'structures'].append(structure['index'])
    monster = dict(count_u16_50a9ce=view.u16(0x50a9bc + 18), human_only_u8_50a9bc=view.u8(0x50a9bc),
                   group_counts_50b124=[view.u8(0x50af84 + 416 + g) for g in range(16)])
    return dict(
        schema='rising-lands/ai-runtime-m2-frame-inventory/1',
        original_sha256=ORIGINAL_SHA256,
        input=dict(label='M1 post-load input', capture=str(M1_CAPTURE.relative_to(ROOT)),
                   capture_sha256=M1_CAPTURE_SHA256, final_state_sha256=M1_FINAL_STATE_SHA256,
                   point='MissionLoad real return 0x42d22d (before the load-entry tail 0x42d22d..0x42d2de)'),
        frame_body=dict(interval=[f'0x{FRAME_BODY[0]:08x}', f'0x{FRAME_BODY[1]:08x}'], calls=calls, gates=gates),
        gate_inputs_post_load=dict(
            state_4e2f78=view.u8(0x4e2f78), state_note='MenuInit(local, 0x12, 1) at 0x42d2cb stores 0x12 before the body',
            evenement_en_cours_4e1b0e=view.u8(0x4e1b0e), cd_music_off_4e2f28=view.u8(0x4e2f28),
            network_4e0730=view.u8(0x4e0730), local_player_508041=view.u8(0x508041),
            mission_496fe4=view.u8(0x496fe4), end_counter_4e061c=view.u32(0x4e061c),
            frame_counters_508f7c_80_84=[view.u32(0x508f7c), view.u32(0x508f80), view.u32(0x508f84)],
            frame_counters_note='zeroed again by the load entry (0x42d1da step 5) before the body',
            game_next_frame_496d40=view.u32(0x496d40), structure_period_495c02=view.u16(0x495c02),
            unit_counters_4e1a38_4e1a3a=[view.u16(0x4e1a38), view.u16(0x4e1a3a)],
            structure_counters_4dfaa8=[view.u32(0x4dfaa8 + 4 * p) for p in range(4)],
            unit_counters_4e1928=[view.u16(0x4e1928 + 2 * p) for p in range(5)]),
        players=players(view, image),
        monster_tables=monster,
        units=dict(pool=f'0x{pool:08x}', live=len(unit_list), by_state=states, records=unit_list),
        structures=dict(pool=f'0x{STRUCTURE_POOL:08x}', live=len(structure_list), by_type=types,
                        records=structure_list),
    )


def export():
    OUTPUT.write_text(json.dumps(build(), indent=1, ensure_ascii=False) + '\n')
    return OUTPUT


if __name__ == '__main__':
    print(export())
