"""Original-only captures behind the AI/runtime contract (call order, gates, stores).

Run with ``python3 -B pesquisas-paralelas/ia-runtime/capturar_contrato_ia.py``; it needs
Unicorn (core's bench) and writes ``evidencias/capturas-originais.json``. Every
scenario declares its synthetic fixture: memory written before entry, the value
each stubbed callee returns, and any declared callee side effect. Callees that
are stubs are not executed; their effects are not part of any capture.
"""
import json
import re

from ambiente_ia_runtime import EVIDENCE, ORIGINAL_SHA256, ROOT
from captura_chamadas_ia import CallCapture, regions, returns, returns_by_register, summarize_writes
from emulador import UNIDADES
from inventario_ia_runtime import OriginalImage

CALL_COLUMNS = ('name', 'callee', 'call_site', 'eax', 'edx', 'ebx', 'ecx', 'declared_return', 'stack_arguments')
STORE_COLUMNS = ('address', 'width', 'stores', 'first', 'last', 'first_pc', 'routine')
UNIT = 276
STRUCTURES = 0x49a0c8
GROUPS = 0x51a9e0
PLAYERS = 0x1100000  # declared allocation for the player table pointed to by 0x5080a8
LOCAL_PLAYER = 0x508041
STATE = 0x4e2f78
NETWORK = 0x4e0730
FRAME = 0x508f7c
# Declared player types for the call-order fixtures (PlayerGetType byte +1 of 20-byte records;
# players >= 4 return 2 in the original without reading the table).
PLAYER_TYPES = {0: 1, 1: 2, 2: 0, 3: 1, 4: 2}
GAME_IMPORTS = {0x5232c8: 8, 0x523290: 4, 0x5232d0: 4, 0x5232bc: 4}  # SetCursorPos, GetAsyncKeyState, ShowCursor, PostQuitMessage


def monde01_units():
    """Owner/type/state bytes of MONDE01's 16 serialized units from core's committed report."""
    rows = json.loads((ROOT / 'relatorios/missao01-unidades.json').read_text(encoding='utf-8'))
    return [(u['indice'], u['proprietario_id'], u['tipo'], u['byte_estado']) for u in rows]


class Scenarios:
    def __init__(self):
        self.image = OriginalImage()
        self.results = []

    def capture(self):
        return CallCapture(self.image)

    def own(self, start, end=None):
        """The routine interval plus the shared Watcom tails reached from it."""
        end = end or self.image.symbol_end(start)
        walked = self.image.walk(start, [(start, end)])
        return [(start, end)] + self.image.shared_chunks(walked), walked

    def stub_all(self, walked, declared, default=0):
        stubs = {target: returns(default) for target in walked['calls']}
        stubs.update(declared)
        return stubs

    def player_table(self, capture, types=PLAYER_TYPES):
        capture.cpu.mem_map(PLAYERS, 0x1000)
        for player in range(4):
            capture.u8(PLAYERS + player * 20 + 1, types[player])
        capture.u32(0x5080a8, PLAYERS)

    def record(self, name, routine, capture, fixture, result, stores=True, **extra):
        entry = dict(scenario=name, routine=routine, fixture=fixture, bench_segments=capture.bench.execucoes,
                     calls=[[e[k] if k in e else None for k in CALL_COLUMNS] for e in capture.events],
                     final_eax=f'0x{result["EAX"]:08x}', **extra)
        if stores:
            cells = summarize_writes(capture.store_trace(), self.image)
            entry['stores'] = [[c[k] for k in STORE_COLUMNS] for c in cells]
            entry['store_regions'] = regions(cells)
        self.results.append(entry)
        return entry

    # ---------------------------------------------------------------- frame
    def prog_iteration(self):
        native, walked = self.own(0x47500e, 0x47509d)
        c = self.capture()
        cursor = c.bind_import(0x523294, 4)

        def get_cursor_pos(cap, call):
            cap.u32(call['stack'][0], 320)
            cap.u32(call['stack'][0] + 4, 240)
            return 1
        for address, value in ((FRAME, 5), (0x508f80, 7), (0x508f84, 11)):
            c.u32(address, value)
        for address in (0x5099ae, 0x5099af, 0x5099b1, 0x5099b2):
            c.u8(address, 1)
        stubs = self.stub_all(walked, {cursor: get_cursor_pos})
        result = c.run(0x47500e, native, stubs)
        self.record('prog_iteration', 'ProgIteration 0x47500e', c, dict(
            memory={'0x508f7c': 5, '0x508f80': 7, '0x508f84': 11, '0x5099ae/af/b1/b2': 1},
            bindings={'USER32.dll!GetCursorPos': 'writes POINT (320, 240), returns 1'},
            callees='CalculGame and AffGame are stops returning EAX=0'), result)

    def calcul_game(self, name, state, network=0, events=0, end=0, counter=0, mission=1, music=0,
                    effects=None, note=''):
        native, walked = self.own(0x42c868)
        c = self.capture()
        self.player_table(c)
        thunks = {c.bind_import(slot, size): returns(0) for slot, size in GAME_IMPORTS.items()}
        c.u8(STATE, state)
        c.u8(NETWORK, network)
        c.u8(0x4e2f28, music)
        c.u8(LOCAL_PLAYER, 0)
        c.u32(0x4e061c, counter)
        c.u8(0x5099b0, 1)
        declared = {0x46d817: returns_by_register('eax', PLAYER_TYPES), 0x4581b6: returns(events),
                    0x458606: returns(end), 0x46c11a: returns(mission)}
        for target, effect in (effects or {}).items():
            declared[target] = effect
        stubs = self.stub_all(walked, declared)
        stubs.update(thunks)
        result = c.run(0x42c868, native, stubs)
        self.record(name, 'CalculGame 0x42c868', c, dict(
            memory={'0x4e2f78 state': state, '0x4e0730 network': network, '0x4e2f28 music flag': music,
                    '0x508041 local player': 0, '0x4e061c end counter': counter, '0x5099b0': 1},
            declared_returns={'PlayerGetType': PLAYER_TYPES, 'EvenementEnCours': events, 'TestFinDeMission': end,
                              'MissionGetNum': mission, 'other direct callees': 0, 'imports': 0},
            note=note), result,
            state_after=c.u8(STATE), end_counter_after=c.u32(0x4e061c), flag_5099b0_after=c.u8(0x5099b0))

    def menu_init_state(self):
        """Declared MenuInit effect: the new state in DL is stored at 0x4e2f78 (original store 0x468c6d)."""
        def effect(cap, call):
            if (call['eax'] & 0xff) == cap.u8(LOCAL_PLAYER):
                cap.u8(STATE, call['edx'])
            return 0
        return effect

    def process_input_leaves_game(self):
        def effect(cap, call):
            if call['eax'] & 0xff == 3:
                cap.u8(STATE, 0x10)
            return 0
        return effect

    def game_next_frame(self):
        native, walked = self.own(0x45d015)
        c = self.capture()
        c.u32(0x496d40, 0xffffffff)
        result = c.run(0x45d015, native, {})
        self.record('game_next_frame_wraps', 'GameNextFrame 0x45d015', c,
                    dict(memory={'0x496d40': '0xffffffff'}), result)

    # ------------------------------------------------------- unit dispatcher
    def unit_loop(self):
        native, walked = self.own(0x456db5)
        c = self.capture()
        c.u8(LOCAL_PLAYER, 0)
        units = monde01_units() + [(16, 4, 3, 1), (17, 200, 2, 2), (18, 1, 17, 4), (19, 2, 5, 1), (20, 1, 0, 0)]
        for index, owner, kind, state in units:
            base = UNIDADES + index * UNIT
            c.u8(base, owner)
            c.u8(base + 1, kind)
            c.u8(base + 2, state)
        stubs = self.stub_all(walked, {})
        result = c.run(0x456db5, native, stubs, limit=1000000)
        self.record('unit_loop_monde01', 'CalculEnginNextEtape 0x456db5', c, dict(
            units='MONDE01 disk owner/type/state bytes for units 0..15 (core relatorios/missao01-unidades.json); '
                  'synthetic units 16..20 (owner,type,state) = (4,3,1), (200,2,2), (1,17,4), (2,5,1), (1,0,0); '
                  'all other unit bytes zero',
            memory={'0x508041 local player': 0},
            declared_returns={'IATestUtilite': 0, 'EnginNextEtape': 0}), result)

    def unit_states(self):
        ene, walked = self.own(0x45442c)
        cases = [('monde01_type0_state7', 0, 0, 7, None), ('monde01_type9_state14', 0, 9, 14, None),
                 ('monde01_type1_state7', 0, 1, 7, None), ('monde01_type7_state7', 0, 7, 7, None),
                 ('monde01_type5_state7', 0, 5, 7, None), ('monde01_type8_state7', 0, 8, 7, None),
                 ('type0_state7_target_found_human', 0, 0, 7, 5), ('type0_state7_target_found_ai', 1, 0, 7, 5),
                 ('state0_direct_entry', 0, 0, 0, None)]
        for name, owner, kind, state, target in cases:
            c = self.capture()
            index = 3
            base = UNIDADES + index * UNIT
            c.u8(base, owner)
            c.u8(base + 1, kind)
            c.u8(base + 2, state)
            c.u32(base + 0x104, 0xffffffff)
            c.u32(FRAME, 32 - index)  # (frame + unit) & 0x1f == 0: the 32-frame scan runs
            declared = {0x46d817: returns_by_register('eax', {0: 1, 1: 2}),
                        0x453f74: returns(0xffff if target is None else target)}
            stubs = self.stub_all(walked, declared)
            result = c.run(0x45442c, ene, stubs, registers={'eax': index}, limit=1000000)
            self.record('unit_state_' + name, 'EnginNextEtape 0x45442c', c, dict(
                unit=dict(index=index, owner=owner, type=kind, state=state, sound_handle_0x104='0xffffffff',
                          other_bytes='zero'),
                memory={'0x508f7c frame counter': 32 - index},
                declared_returns={'PlayerGetType': {0: 1, 1: 2}, 'EnginTrouveCible': '0xffff' if target is None else target,
                                  'other direct callees': 0}), result)

    # -------------------------------------------------- structure dispatcher
    def structure_loop(self):
        native, walked = self.own(0x4281c7)
        c = self.capture()
        rows = [(0, 0, 1, 2), (1, 1, 1, 9), (2, 0, 3, 3), (3, 4, 1, 1), (4, 2, 1, 12)]
        for index, owner, state, kind in rows:
            base = STRUCTURES + index * UNIT
            c.u8(base + 4, owner)
            c.u8(base + 5, state)
            c.u8(base + 8, kind)
        c.u32(FRAME, 0)
        declared = {0x41aee2: returns(2828), 0x4766d6: returns(0), 0x419c4f: returns(1), 0x4199f9: returns(0)}
        stubs = self.stub_all(walked, declared)
        result = c.run(0x4281c7, native, stubs, limit=1000000)
        self.record('structure_loop', 'CalculBatimentNextEtape 0x4281c7', c, dict(
            structures='(index, owner +4, state +5, type +8) = ' + repr(rows) + '; structure 0 mirrors MONDE01 type 2 at cell 2828',
            memory={'0x508f7c frame counter': 0},
            declared_returns={'BatimentGetCase': 2828, 'CaseEstDecouverte': 0, 'BatimentEstDecouvert': 1,
                              'BatimentContourEstIllumine': 0, 'other direct callees': 0}), result)

    def structure_types(self):
        native, walked = self.own(0x4268d4)
        for kind, contains in ((2, 0), (2, 1), (12, 0)):
            c = self.capture()
            c.u8(STRUCTURES + 8, kind)
            c.u8(STRUCTURES + 5, 1)
            declared = {0x4471b8: returns(contains), 0x44724a: returns(contains)}
            stubs = self.stub_all(walked, declared)
            result = c.run(0x4268d4, native, stubs, registers={'eax': 0}, limit=1000000)
            self.record(f'structure_type{kind}_bag{contains}', 'BatimentNextEtape 0x4268d4', c, dict(
                structure=dict(index=0, type=kind, state=1, other_bytes='zero'),
                declared_returns={'BagContient': contains, 'BagContientTroupe': contains, 'other direct callees': 0}),
                result)

    # ------------------------------------------------------------ AI player
    def ai_player(self):
        native, walked = self.own(0x47f927, 0x47fa2f)
        cases = [('player0_all_kernels', 0, dict(structures=1, units=3), {}),
                 ('player1_inactive', 1, dict(inactive=1), {}),
                 ('player2_tenth_empty_cycle', 2, dict(cycles=9), {}),
                 ('player3_city_kernel_stops', 3, dict(cycles=3), {0x48453c: 0x1a1a0005}),
                 ('player0_solver_result', 0, dict(units=1), {0x47d314: 0x1a1a000e}),
                 ('player4_monster', 4, {}, {0x47d314: 7})]
        for name, player, state, values in cases:
            c = self.capture()
            context = 0x51a990 + player * 16
            if player < 4:
                c.u8(context, state.get('inactive', 0))
                c.u8(context + 5, state.get('cycles', 0))
                c.u32(0x4dfaa8 + player * 4, state.get('structures', 0))
                c.u16(0x4e1928 + player * 2, state.get('units', 0))
            stubs = self.stub_all(walked, {k: returns(v) for k, v in values.items()})
            result = c.run(0x47f927, native, stubs, registers={'eax': player, 'edx': 1})
            self.record('ia_calcul_player_' + name, 'iaCalculPlayer 0x47f927', c, dict(
                registers=dict(eax=player, edx='mission 1'), state=state,
                declared_returns={**{self.image.name(k): f'0x{v:08x}' for k, v in values.items()},
                                  'other callbacks': 0}), result,
                inactive_after=c.u8(context) if player < 4 else None,
                cycles_after=c.u8(context + 5) if player < 4 else None)

    # ----------------------------------------------------------- AI tables
    def closure(self, entry, stubs, end=None):
        """Native intervals reachable from ``entry`` without entering a stubbed routine."""
        native, pending, done, imports, indirect = [], [(entry, end)], set(), set(), set()
        while pending:
            start, stop = pending.pop()
            if start in done:
                continue
            done.add(start)
            interval, walked = self.own(start, stop)
            native.extend(interval)
            imports.update(walked['imports'])
            indirect.update(walked['indirect_calls'])
            for target in list(walked['calls']) + list(walked['tail_calls']):
                if target not in stubs and target not in done:
                    pending.append((target, None))
        return native, sorted(done), sorted(imports), sorted(indirect)

    def bind_reached_imports(self, capture, imports, value):
        """Bind each reached import (all take no stack arguments here) to a declared constant."""
        stubs = {}
        for slot in sorted(self.image.imports):
            if self.image.imports[slot] in imports:
                if self.image.imports[slot] != 'WINMM.dll!timeGetTime':
                    raise RuntimeError('Undeclared import binding: ' + self.image.imports[slot])
                stubs[capture.bind_import(slot, 0)] = returns(value)
        return stubs

    def ia_reset(self):
        world = {0x46d817: 'PlayerGetType', 0x4717c2: 'RechercheGetNiveau', 0x470b37: 'RechercheSetBranche',
                 0x46c11a: 'MissionGetNum', 0x443dad: 'EnginEstVivant', 0x41a735: 'BatimentExiste',
                 0x41a08c: 'BatimentGetPlayer', 0x41a4f4: 'BatimentGetType', 0x440e11: 'EnginGetEtat',
                 0x467670: 'GetRessource', 0x442025: 'EnginGetType', 0x4422dd: 'TypeEnginEstMonstre',
                 0x443108: 'EnginSetPlayer'}
        native, routines, imports, indirect = self.closure(0x47f36e, world)
        if indirect or imports != ['WINMM.dll!timeGetTime']:
            raise RuntimeError(f'IaReset closure reaches undeclared imports/indirect calls: {imports} {indirect}')
        c = self.capture()
        types = {0: 1, 1: 2, 2: 0, 3: 0, 4: 2}
        self.player_table(c, types)
        stubs = {a: returns(0) for a in world}
        stubs.update(self.bind_reached_imports(c, imports, 0x12345678))
        stubs[0x46d817] = returns_by_register('eax', types)
        stubs[0x46c11a] = returns(1)

        def get_ressource(cap, call):
            for register in ('eax', 'edx', 'ebx', 'ecx'):  # four u16 outputs through pointers
                cap.u16(call[register], 0)
            return 0
        stubs[0x467670] = get_ressource
        result = c.run(0x47f36e, native, stubs, limit=1000000)
        self.record('ia_reset_empty_world', 'IaReset 0x47f36e', c, dict(
            players=f'PlayerGetType and the 0x5080a8 table (declared allocation 0x{PLAYERS:x}) give types {types}',
            world='no live unit (EnginEstVivant=0), no structure (BatimentExiste=0), GetRessource stores 0 to its four '
                  'u16 output pointers (EAX/EDX/EBX/ECX) and returns 0, MissionGetNum=1, '
                  'Recherche*=0; all other memory as mapped from the intact image',
            imports_bound={name: 'returns 0x12345678 (statically reachable through iaRandom(0); not reached)' for name in imports},
            native_routines=[self.image.name(a) or f'sub_{a:08x}' for a in routines],
            stubbed_world_queries=sorted(world.values())), result)

    def ia_alloc(self):
        io = {0x48d5fd: 'debugSymLoad', 0x48d699: 'debugSymUnload', 0x47e437: 'iaProbLoadBinaryRules'}
        native, routines, imports, indirect = self.closure(0x47fb15, io)
        # The Watcom C runtime reached through sprintf dispatches through its own pointer
        # tables; that library code runs natively from the image as one declared interval.
        native.append((0x48c341, self.image.symbol_end(0x4937a5)))  # utoa .. end of code
        c = self.capture()
        stubs = {a: returns(0) for a in io}
        stubs.update(self.bind_reached_imports(c, imports, 0x12345678))
        result = c.run(0x47fb15, native, stubs, limit=1000000)
        self.record('ia_alloc_program_start', 'IaAlloc 0x47fb15', c, dict(
            io_stops=sorted(io.values()), imports_bound={name: 'returns 0x12345678' for name in imports},
            runtime_library='0x0048c341 (utoa)..0x00494000 executed natively (Watcom C runtime)',
            native_routines=[self.image.name(a) or f'sub_{a:08x}' for a in routines],
            indirect_calls=[f'0x{a:08x}' for a in indirect]), result)

    # ------------------------------------------------------------ messages
    def unit_messages(self):
        native, walked = self.own(0x4829c8)
        handlers = {h for p in self.image.table(0x498e94, 12) if 0x498000 <= p < 0x499000
                    for h in self.image.table(p, 5) if h}
        for message in list(range(0x41, 0x4d)) + [0x40, 0x4d]:
            for owner_type in (2, 1):
                if owner_type == 1 and message != 0x41:
                    continue
                c = self.capture()
                unit = 5
                base = UNIDADES + unit * UNIT
                c.u8(base, 1)
                c.u32(base + 0x10c, 3)
                group = GROUPS + 3 * 32
                c.u8(group + 0x1b, 1)
                c.u32(group + 0x0c, 7)
                declared = {0x46d817: returns(owner_type)}
                stubs = self.stub_all(walked, declared)
                stubs.update({h: returns(0) for h in handlers})
                result = c.run(0x4829c8, native, stubs, registers={'eax': unit, 'edx': message, 'ebx': 0x22})
                self.record(f'unit_message_0x{message:02x}_owner_type{owner_type}', 'iagUnitSendMessage 0x4829c8', c, dict(
                    registers=dict(eax=unit, dl=f'0x{message:02x}', ebx='0x22 payload'),
                    unit=dict(index=unit, owner=1, group_0x10c=3), group=dict(index=3, behavior_0x1b=1, task_0x0c=7),
                    declared_returns={'PlayerGetType': owner_type, 'other callees and iab* handlers': 0}), result)

    def city_messages(self):
        native, walked = self.own(0x484808)
        for message in (0, 1, 2, 3, 4, 5):
            c = self.capture()
            declared = {0x41a08c: returns(1), 0x46d817: returns(2), 0x41a4f4: returns(3), 0x44113e: returns(2828),
                        0x487594: returns(0xffffffff)}
            stubs = self.stub_all(walked, declared)
            result = c.run(0x484808, native, stubs, registers={'eax': 0, 'edx': message, 'ebx': 9})
            self.record(f'city_message_{message}', 'iagVilleSendMessage 0x484808', c, dict(
                registers=dict(eax='structure 0', dl=message, ebx='9 (payload: unit/structure index)'),
                declared_returns={'BatimentGetPlayer': 1, 'PlayerGetType': 2, 'BatimentGetType': 3,
                                  'EnginGetCase': 2828, 'iagWarSearchBattleFromPos': '0xffffffff',
                                  'other callees': 0}), result)

    def run_all(self):
        self.prog_iteration()
        self.game_next_frame()
        self.calcul_game('frame_single_player', 0x12)
        self.calcul_game('frame_music_flag_set_skips_cd_play', 0x12, music=1)
        self.calcul_game('gate2_event_in_progress', 0x12, events=1)
        self.calcul_game('gate3_state_left_during_input', 0x12, effects={0x45edc0: self.process_input_leaves_game()},
                         note='declared synthetic effect: ProcessInputGame(3) stores 0x10 at 0x4e2f78')
        self.calcul_game('end_condition_counting', 0x12, end=1, counter=5)
        self.calcul_game('end_condition_mission6_first_frame', 0x12, end=1, counter=0, mission=6)
        self.calcul_game('end_condition_reached', 0x12, end=1, counter=99,
                         effects={0x4682bb: self.menu_init_state()},
                         note='declared MenuInit effect: stores DL at 0x4e2f78 when AL is the local player')
        self.calcul_game('gate1_single_player_state_0x10', 0x10)
        self.calcul_game('gate1_network_state_0x10', 0x10, network=1)
        self.calcul_game('network_frame_state_0x12', 0x12, network=1)
        self.calcul_game('load_state0_then_first_frame', 0x00, effects={0x4682bb: self.menu_init_state()},
                         note='declared MenuInit effect: stores DL at 0x4e2f78 when AL is the local player')
        self.calcul_game('load_state0_network_by_name', 0x00, network=1, effects={0x4682bb: self.menu_init_state()},
                         note='declared MenuInit effect: stores DL at 0x4e2f78 when AL is the local player')
        self.unit_loop()
        self.unit_states()
        self.structure_loop()
        self.structure_types()
        self.ai_player()
        self.ia_reset()
        self.ia_alloc()
        self.unit_messages()
        self.city_messages()
        return self.results


def dump(document):
    """Indented JSON whose innermost arrays/objects (one call, one store cell) stay on one line."""
    text = json.dumps(document, indent=1, ensure_ascii=False)
    leaf = re.compile(r'([\[{])\n\s*([^\[\]{}]*?)\n\s*([\]}])')
    return leaf.sub(lambda m: m.group(1) + ' '.join(x.strip() for x in m.group(2).split('\n')) + m.group(3), text) + '\n'


def build():
    results = Scenarios().run_all()
    return dict(original_sha256=ORIGINAL_SHA256, bench='ferramentas/emulador.py BancadaX86 (core)',
                    scope='Original-only captures with declared synthetic fixtures; stubbed callees are not executed.',
                    call_columns=CALL_COLUMNS, store_columns=STORE_COLUMNS, scenarios=results)


def main():
    document = build()
    results = document['scenarios']
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / 'capturas-originais.json').write_text(dump(document), encoding='utf-8')
    print('Scenarios:', len(results), 'calls:', sum(len(r['calls']) for r in results),
          'bench segments:', sum(r['bench_segments'] for r in results))


if __name__ == '__main__':
    main()
