"""Declared case matrix for the economy order setters and construction gates (M3 groundwork).

Every case starts from the exact paused frame-1 state of ``bancada_ordens_economia`` (Core's
selection-orders pause: MONDE01 display reference, first ProcessInputGame entry). Facts of that
state used below (probed natively at the pause, then checked by the capture):
- the unit pool is at 0x474a8000; units 0..15 belong to player 0: 0..2 soldiers (type 0),
  3..10 colonists (type 9, state 14), 11 type 1, 12 the builder (type 7, cell (17,16)),
  13/14 type 5 at (14,16)/(12,16), 15 type 8; units from 16 on are free (state 0);
- every selection list is empty; the local player is 0; the search owner 0x496304 is 0xffff;
- player 0 holds food 30 and stone 30 (records 1 and 2: +2 total 30, +0 RMI 30); players 1..3 hold 0;
- the per-player stock indicator words at 0x4dfb2c + 6p are (0, 100) for players 0..3, so
  CreerBatiment's indicator recalculation is skipped unless a case declares the first word;
- structure 0 is the sanctuary (type 2, 6x5, origin (12,11)); records 1.. are free;
- the cave (type 3) is 5x5 and costs food 10, stone 6, parts 0, Bag capacity 2;
- mine 0 (43,8) and the field (26,32) are undiscovered for player 0 (grid byte 31); the unit
  cells are discovered (0).

A case adds only declared byte writes and argument registers (Core's helpers: a selection list
write also sets each unit's +0xbd). Importing this module executes nothing.
"""
from pathlib import Path
import struct
import sys

_F = Path(__file__).resolve().parents[2] / 'ferramentas'
if str(_F) not in sys.path:
    sys.path.insert(0, str(_F))

from casos_selecao_ordens import (BUSCA_UNIDADE, DESCOBERTA_0, ESTRUTURAS, UNIDADES, caso, campo, celula,  # noqa: E402
                                  estrutura, lista, u8, u16, u32)

RECURSOS = 0x4e2ea8              # u16 RMI +0, total +2; player * 32 + resource * 8 (0 parts, 1 food, 2 stone)
INDICADOR = 0x4dfb2c             # per player (stride 6): u16 divisor, u16 divisor, u8 level
ZONA = 0x508728 + 0x600 + 0x1e0  # tail of player 3's (empty) selection list: output words of GetRessourceStock
MINA = celula(43, 8)
CAMPO = celula(26, 32)
CAVERNA = celula(21, 12)         # proposed CAVE click (M3_ALVOS); type-3 offset 0x202 gives the build cell
OBRA = CAVERNA + 0x202           # cell CalculConstruireBatiment hands to BatimentConstructible/CreerBatiment


def recurso(jogador, rid, total=None, rmi=None):
    base = RECURSOS + 32 * jogador + 8 * rid
    return ([(base + 2, u16(total))] if total is not None else []) + ([(base, u16(rmi))] if rmi is not None else [])


def indicador(jogador, a, b):
    return [(INDICADOR + 6 * jogador, u16(a) + u16(b))]


def ordem_construir(unidade, tipo, alvo, posicao, b2=None, extra=None):
    """Unit state after SetEnginConstruitBatiment (state 11, +0xbe type, +0x7e/+0xb2 target), at ``posicao``."""
    w = [campo(unidade, 2, u8(0xb)), campo(unidade, 0xbe, u8(tipo)), campo(unidade, 0x7e, u16(alvo)),
         campo(unidade, 0xb2, u16(alvo if b2 is None else b2)), campo(unidade, 8, u16(posicao))]
    return w + [campo(unidade, o, d) for o, d in (extra or {}).items()]


def casos(grade_descoberta_0):
    """The declared matrix; ``grade_descoberta_0`` is player 0's discovery grid address at the pause."""
    descoberta = lambda c, v: (grade_descoberta_0 + c, u8(v))
    c = []
    # ------------------------------------------------------------ EnginTravailSelectionne: AL player, DL kind
    t = 'EnginTravailSelectionne'
    c += [caso('work_stone_builder', t, lista(0, [12]), EAX=0, EDX=2),
          caso('work_stone_builder_and_u13', t, lista(0, [12, 13]), EAX=0, EDX=2),
          caso('work_stone_u13', t, lista(0, [13]), EAX=0, EDX=2),
          caso('work_stone_empty', t, EAX=0, EDX=2),
          caso('work_stone_free_then_builder', t, lista(0, [16, 12]), EAX=0, EDX=2),
          caso('work_stone_free_only', t, lista(0, [16]), EAX=0, EDX=2),
          caso('work_stone_colonist', t, lista(0, [3]), EAX=0, EDX=2),
          caso('work_stone_p1_list_p0_builder', t, lista(1, [12]), EAX=1, EDX=2),
          caso('work_food_u13', t, lista(0, [13]), EAX=0, EDX=1),
          caso('work_food_u13_u14', t, lista(0, [13, 14]), EAX=0, EDX=1),
          caso('work_food_u13_builder', t, lista(0, [13, 12]), EAX=0, EDX=1),
          caso('work_food_type13', t, lista(0, [14]) + [campo(14, 1, u8(13))], EAX=0, EDX=1),
          caso('work_food_type1', t, lista(0, [11]), EAX=0, EDX=1),
          caso('work_parts_type6', t, lista(0, [15]) + [campo(15, 1, u8(6))], EAX=0, EDX=0),
          caso('work_parts_builder', t, lista(0, [12]), EAX=0, EDX=0),
          caso('work_kind3_builder', t, lista(0, [12]), EAX=0, EDX=3),
          caso('work_kind_ff_free_last', t, lista(0, [12, 16]), EAX=0, EDX=0xff),
          caso('work_upper_bits', t, lista(0, [12]), EAX=0x12345600, EDX=0xabcdff02),
          caso('work_upper_bits_empty', t, EAX=0x12345600, EDX=0xabcdff02)]
    # ------------------------------------------------------------ SetMineEnginSelect: AL player, DX cell
    t = 'SetMineEnginSelect'
    c += [caso('mine_builder', t, lista(0, [12]), EAX=0, EDX=MINA),
          caso('mine_builder_target_discovered', t, lista(0, [12]) + [descoberta(MINA, 0)], EAX=0, EDX=MINA),
          caso('mine_three_mixed', t, lista(0, [12, 13, 14]), EAX=0, EDX=MINA),
          caso('mine_p1_owner_mismatch', t, lista(1, [12]), EAX=1, EDX=MINA),
          caso('mine_p1_own_unit_not_local', t, lista(1, [12]) + [campo(12, 0, u8(1))], EAX=1, EDX=MINA),
          caso('mine_free_then_builder', t, lista(0, [16, 12]), EAX=0, EDX=MINA),
          caso('mine_search_owner', t, lista(0, [12]) + [(BUSCA_UNIDADE, u16(12))], EAX=0, EDX=MINA),
          caso('mine_unit_cell_undiscovered', t, lista(0, [12]) + [descoberta(celula(17, 16), 1)], EAX=0, EDX=MINA),
          caso('mine_handle_busy', t, lista(0, [12]) + [campo(12, 0x104, u32(0))], EAX=0, EDX=MINA),
          caso('mine_empty', t, EAX=0, EDX=MINA),
          caso('mine_cell_ffff', t, lista(0, [12]), EAX=0, EDX=0xffff),
          caso('mine_upper_bits', t, lista(0, [12]), EAX=0x7f7f7f00, EDX=0xdead0000 | MINA),
          caso('mine_second_mine', t, lista(0, [12]), EAX=0, EDX=celula(6, 59))]
    t = 'SetMineEngin'
    c += [caso('engin_mine_u12', t, EAX=12, EDX=MINA),
          caso('engin_mine_u13', t, EAX=13, EDX=MINA),
          caso('engin_mine_search_owner', t, [(BUSCA_UNIDADE, u16(12))], EAX=12, EDX=MINA),
          caso('engin_mine_upper_bits', t, EAX=0x5555000c, EDX=0x1234ff2b)]
    # ------------------------------------------------------------ SetDepotEnginSelect: AL player, DL, BX, CL
    t = 'SetDepotEnginSelect'
    c += [caso('depot_builder', t, lista(0, [12]), EAX=0, EDX=1, EBX=0x0b0c, ECX=2),
          caso('depot_two', t, lista(0, [12, 13]), EAX=0, EDX=0, EBX=0, ECX=0),
          caso('depot_p1_list_p0_units', t, lista(1, [12, 13]), EAX=1, EDX=1, EBX=0x0b0c, ECX=2),
          caso('depot_free_then_builder', t, lista(0, [16, 12]), EAX=0, EDX=1, EBX=0x0b0c, ECX=2),
          caso('depot_free_only', t, lista(0, [16]), EAX=0, EDX=1, EBX=0x0b0c, ECX=2),
          caso('depot_empty', t, EAX=0, EDX=1, EBX=0x0b0c, ECX=2),
          caso('depot_upper_bits', t, lista(0, [12]), EAX=0x11111100, EDX=0x9900ff01, EBX=0xffff1234,
               ECX=0x123456fe)]
    t = 'SetDepotEngin'
    c += [caso('engin_depot_u12', t, EAX=12, EDX=1, EBX=0x0b0c, ECX=2),
          caso('engin_depot_u300', t, EAX=300, EDX=0x7f, EBX=0xffff, ECX=0xff),
          caso('engin_depot_upper_bits', t, EAX=0xabcd000d, EDX=0x12345680, EBX=0x5678abcd, ECX=0x9abcdef0)]
    # ------------------------------------------------------------ SetRamasseEnginSelect: AL player, DX cell
    saco = celula(20, 18)
    t = 'SetRamasseEnginSelect'
    c += [caso('pickup_u13', t, lista(0, [13]), EAX=0, EDX=saco),
          caso('pickup_two', t, lista(0, [13, 14]), EAX=0, EDX=saco),
          caso('pickup_builder', t, lista(0, [12]), EAX=0, EDX=saco),
          caso('pickup_p1_owner_mismatch', t, lista(1, [13]), EAX=1, EDX=saco),
          caso('pickup_p1_own_unit_not_local', t, lista(1, [13]) + [campo(13, 0, u8(1))], EAX=1, EDX=saco),
          caso('pickup_free_then_u13', t, lista(0, [16, 13]), EAX=0, EDX=saco),
          caso('pickup_search_owner', t, lista(0, [13]) + [(BUSCA_UNIDADE, u16(13))], EAX=0, EDX=saco),
          caso('pickup_unit_cell_undiscovered', t, lista(0, [13]) + [descoberta(celula(14, 16), 1)], EAX=0,
               EDX=saco),
          caso('pickup_empty', t, EAX=0, EDX=saco),
          caso('pickup_upper_bits', t, lista(0, [13]), EAX=0x0f0f0f00, EDX=0x77770000 | saco)]
    t = 'SetRamasseEngin'
    c += [caso('engin_pickup_u14', t, EAX=14, EDX=saco),
          caso('engin_pickup_search_owner', t, [(BUSCA_UNIDADE, u16(14))], EAX=14, EDX=saco),
          caso('engin_pickup_upper_bits', t, EAX=0x1111000e, EDX=0x2222ffff)]
    # ------------------------------------------------------------ resource queries and debit
    t = 'TestRessource'                     # AX food, DX stone, BX parts, player as the RET-4 stack word
    c += [caso('test_cave_p0', t, stack=[0], ret_imm=4, EAX=10, EDX=6, EBX=0),
          caso('test_cave_food9', t, recurso(0, 1, total=9), stack=[0], ret_imm=4, EAX=10, EDX=6, EBX=0),
          caso('test_cave_stone5', t, recurso(0, 2, total=5), stack=[0], ret_imm=4, EAX=10, EDX=6, EBX=0),
          caso('test_cave_exact', t, recurso(0, 1, total=10) + recurso(0, 2, total=6), stack=[0], ret_imm=4,
               EAX=10, EDX=6, EBX=0),
          caso('test_parts_one', t, stack=[0], ret_imm=4, EAX=10, EDX=6, EBX=1),
          caso('test_cave_p1', t, stack=[1], ret_imm=4, EAX=10, EDX=6, EBX=0),
          caso('test_player_upper_bits', t, stack=[0xffffff00], ret_imm=4, EAX=0xffff000a, EDX=0xffff0006,
               EBX=0xffff0000)]
    t = 'GetRessourceStock'                 # EAX/EDX/EBX/ECX output words, player as the RET-4 stack word
    ptrs = dict(EAX=ZONA, EDX=ZONA + 2, EBX=ZONA + 4, ECX=ZONA + 6)
    c += [caso('stock_p0', t, stack=[0], ret_imm=4, **ptrs),
          caso('stock_p0_rmi', t, recurso(0, 1, rmi=8) + recurso(0, 2, rmi=3) + recurso(0, 0, total=5, rmi=1),
               stack=[0], ret_imm=4, **ptrs),
          caso('stock_rmi_above_total', t, recurso(0, 1, rmi=40) + recurso(0, 2, rmi=0xffff), stack=[0], ret_imm=4,
               **ptrs),
          caso('stock_p3', t, recurso(3, 1, total=7) + recurso(3, 2, total=9), stack=[3], ret_imm=4, **ptrs),
          caso('stock_same_pointer', t, recurso(0, 1, total=12), stack=[0], ret_imm=4,
               EAX=ZONA, EDX=ZONA, EBX=ZONA, ECX=ZONA + 8),
          caso('stock_pointer_upper_bits', t, stack=[0], ret_imm=4, EAX=ZONA, EDX=ZONA + 2, EBX=ZONA + 4,
               ECX=ZONA + 6, ESI=0x13572468, EDI=0x24681357)]
    t = 'EnleveMatiere'                     # AL resource, BX player, DX quantity
    c += [caso('debit_food10_p0', t, EAX=1, EBX=0, EDX=10),
          caso('debit_stone6_p0', t, EAX=2, EBX=0, EDX=6),
          caso('debit_all', t, EAX=1, EBX=0, EDX=30),
          caso('debit_above_total', t, EAX=2, EBX=0, EDX=31),
          caso('debit_rmi', t, recurso(0, 1, rmi=8), EAX=1, EBX=0, EDX=6),
          caso('debit_rmi_below', t, recurso(0, 1, rmi=4), EAX=1, EBX=0, EDX=6),
          caso('debit_zero', t, EAX=1, EBX=0, EDX=0),
          caso('debit_p3_record3', t, recurso(3, 3, total=50, rmi=20), EAX=3, EBX=3, EDX=21),
          caso('debit_upper_bits', t, recurso(0, 2, rmi=9), EAX=0xabcdef02, EBX=0x77770000, EDX=0x55550006,
               EDI=0x89ab0000),
          caso('debit_above_total_rmi', t, recurso(0, 2, rmi=9), EAX=2, EBX=0, EDX=0x40, EDI=0x89ab0000)]
    # ------------------------------------------------------------ CreerBatiment: AX cell, DL type, BL player
    t = 'CreerBatiment'
    pleno = [estrutura(i, 5, u8(1)) for i in range(1000)]
    c += [caso('create_cave_p0', t, EAX=OBRA, EDX=3, EBX=0),
          caso('create_cave_food9', t, recurso(0, 1, total=9), EAX=OBRA, EDX=3, EBX=0),
          caso('create_cave_stone5', t, recurso(0, 2, total=5), EAX=OBRA, EDX=3, EBX=0),
          caso('create_cave_exact', t, recurso(0, 1, total=10) + recurso(0, 2, total=6), EAX=OBRA, EDX=3, EBX=0),
          caso('create_cave_rmi', t, recurso(0, 1, rmi=8) + recurso(0, 2, rmi=3), EAX=OBRA, EDX=3, EBX=0),
          caso('create_cave_indicator', t, indicador(0, 5, 10), EAX=OBRA, EDX=3, EBX=0),
          caso('create_cave_indicator_wrap', t, indicador(0, 1, 1), EAX=OBRA, EDX=3, EBX=0),
          caso('create_pool_full', t, pleno, EAX=OBRA, EDX=3, EBX=0),
          caso('create_second_free', t, [estrutura(1, 5, u8(2))], EAX=OBRA, EDX=3, EBX=0),
          caso('create_cave_p1_no_stock', t, EAX=OBRA, EDX=3, EBX=1),
          caso('create_cave_p1_stocked', t, recurso(1, 1, total=30) + recurso(1, 2, total=30), EAX=OBRA, EDX=3,
               EBX=1),
          caso('create_sanctuary_type2_refused', t, EAX=OBRA, EDX=2, EBX=0),
          caso('create_type17_p0', t, EAX=OBRA, EDX=17, EBX=0),
          caso('create_gate_type9_p0', t, EAX=OBRA, EDX=9, EBX=0),
          caso('create_type12_no_gates', t, EAX=OBRA, EDX=12, EBX=0),
          caso('create_type12_gate_same_cell', t, [estrutura(1, 5, u8(2)), estrutura(1, 8, u8(9)),
                                                    estrutura(1, 4, u8(0)), estrutura(1, 2, u16(OBRA))],
               EAX=OBRA, EDX=12, EBX=0),
          caso('create_type12_gate_elsewhere', t, [estrutura(1, 5, u8(2)), estrutura(1, 8, u8(9)),
                                                    estrutura(1, 4, u8(0)), estrutura(1, 2, u16(OBRA + 3))],
               EAX=OBRA, EDX=12, EBX=0),
          caso('create_upper_bits', t, EAX=0x7fff0000 | OBRA, EDX=0x12345603, EBX=0xabcdef00)]
    # ------------------------------------------------------------ CalculConstruireBatiment: AX unit (one builder tick)
    t = 'CalculConstruireBatiment'
    chegou = lambda tipo=3, b2=None, extra=None: ordem_construir(12, tipo, CAVERNA, CAVERNA, b2, extra)
    santuario = celula(14, 13)
    c += [caso('build_tick_idle_builder', t, EAX=12),
          caso('build_tick_not_builder', t, EAX=13),
          caso('build_tick_progress_byte2', t, [campo(12, 0x89, u8(2))], EAX=12),
          caso('build_tick_state14', t, [campo(12, 2, u8(14))], EAX=12),
          caso('build_tick_walking', t, ordem_construir(12, 3, CAVERNA, celula(17, 16)), EAX=12),
          caso('build_tick_arrived_cave', t, chegou(), EAX=12),
          caso('build_tick_arrived_cave_indicator', t, chegou() + indicador(0, 5, 10), EAX=12),
          caso('build_tick_arrived_cave_food9', t, chegou() + recurso(0, 1, total=9), EAX=12),
          caso('build_tick_arrived_cave_food9_search_owner', t,
               chegou() + recurso(0, 1, total=9) + [(BUSCA_UNIDADE, u16(12))], EAX=12),
          caso('build_tick_arrived_on_sanctuary', t, ordem_construir(12, 3, santuario, santuario), EAX=12),
          caso('build_tick_arrived_pushed', t, chegou(extra={0x86: u8(1)}), EAX=12),
          caso('build_tick_arrived_pushed_87', t, chegou(extra={0x87: u8(0x80)}), EAX=12),
          caso('build_tick_target_moved', t, chegou(b2=CAVERNA + 1), EAX=12),
          caso('build_tick_target_moved_search_owner', t, chegou(b2=CAVERNA + 1) + [(BUSCA_UNIDADE, u16(12))],
               EAX=12),
          caso('build_tick_no_order', t, chegou(tipo=0xff), EAX=12),
          caso('build_tick_type17', t, chegou(tipo=17), EAX=12),
          caso('build_tick_owner1', t, chegou() + [campo(12, 0, u8(1))] + recurso(1, 1, total=30) +
               recurso(1, 2, total=30), EAX=12),
          caso('build_tick_upper_bits', t, chegou(), EAX=0xabcd000c),
          # Outside the translated domain: the translation raises at these branches (no store before them).
          caso('build_tick_gate_type9', t, ordem_construir(12, 9, CAVERNA, celula(17, 16)), EAX=12),
          caso('build_tick_state15', t, [campo(12, 2, u8(15)), campo(12, 0xc0, u16(0))], EAX=12),
          caso('build_tick_progress_byte1', t, chegou(extra={0x89: u8(1), 0xc0: u16(0)}), EAX=12)]
    nomes = [x['case'] for x in c]
    if len(nomes) != len(set(nomes)):
        raise ValueError('Duplicate case names')
    return c


def verificar_pausa(ler):
    """Check the documented pause facts with ``ler(addr, n) -> bytes``; raises on any difference."""
    u16_ = lambda a: struct.unpack('<H', ler(a, 2))[0]
    u32_ = lambda a: struct.unpack('<I', ler(a, 4))[0]
    fatos = {
        'unit pool': (u32_(0x4e19a0), UNIDADES),
        'player 0 food/stone totals': ((u16_(RECURSOS + 10), u16_(RECURSOS + 18)), (30, 30)),
        'player 0 indicator words': ((u16_(INDICADOR), u16_(INDICADOR + 2)), (0, 100)),
        'cave size and cost': (tuple(u16_(0x495d8c + 52 * 3 + o) for o in (0, 2, 0xc, 0xe, 0x10)), (5, 5, 10, 6, 0)),
        'search owner': (u16_(BUSCA_UNIDADE), 0xffff),
        'builder type/state/cell': ((ler(UNIDADES + 12 * 276 + 1, 2), u16_(UNIDADES + 12 * 276 + 8)),
                                    (bytes([7, 7]), celula(17, 16))),
        'free structure record 1': (ler(ESTRUTURAS + 276 + 5, 1), b'\x00'),
        'scratch output words': (ler(ZONA, 16), bytes(16)),
    }
    erradas = {k: v for k, v in fatos.items() if v[0] != v[1]}
    if erradas:
        raise RuntimeError(f'Pause state differs from the documented facts: {erradas}')
    return u32_(DESCOBERTA_0)
