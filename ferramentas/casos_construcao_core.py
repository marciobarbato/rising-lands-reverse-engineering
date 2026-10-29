"""Declared case matrix for the Core construction routines Economy's build path calls (M3 groundwork).

Every case starts from the exact paused frame-1 state of ``bancada_selecao_ordens`` (MONDE01 display
reference, first ProcessInputGame entry; the same pause as SELECTION_ORDERS and Economy's
ordens_economia). Facts of that state used below (probed natively at the pause, checked by the capture):
- the map is 64x64 (u16 0x497168/0x49716a); the grids are 256 cells wide: tiles u16 [0x507d70],
  objects [0x507d74], attributes [0x507da8], regions u16 [0x4e0f38], structure colours [0x4e156c],
  player 0's discovery [0x507d78];
- wall object 0xfe (0x495bf8), gate object 0xfd (0x495bf9); no wall or gate is on the map;
- the colour free list 0x4e1570 holds 0xfe free colours; the sanctuary's 17 collision cells hold colour 0xfe;
- free cells hold region 1; units hold their tag 0x4000 | unit << 3; the sanctuary (structure 0, type 2,
  6x5, origin (12,11), owner 0) holds its tags 0x8000 | slot;
- units 0..15 belong to player 0 (units 3..10 in state 14 inside the sanctuary); the builder 12 (type 7)
  is at (17,16), unit 13 (type 5) at (14,16); records from 16 and structures from 1 are free;
- the CAVE (type 3) is 5x5; its collision mask (pointer [0x495d94 + 52*3]) has ones only at
  (0..2, 0) and (0..3, 1); the type-20 mask pointer is RAM 0x4dfb9c (all zero at the pause);
- player 0 has discovered every cell with x <= 26 in rows 6..21 (grid byte 0); (27,10) is not (grid
  byte 2), and from x = 28 on rows 10..14 are not; every cell of the cave site (19..23, 10..14) is grass (tiles 0x15d..0x1a4).

The concrete M3 target: the CAVE clicked at (21,12) is built at reference cell (23,14) (offset 0x202),
record origin (19,10). A case only adds declared byte writes and argument registers. Importing this
module executes nothing.
"""
import struct

from casos_selecao_ordens import ESTRUTURAS, UNIDADES, caso, campo, celula, estrutura, u8, u16, u32

PASSO = 276
GRADES = dict(tiles=0x507d70, objetos=0x507d74, atributos=0x507da8, regioes=0x4e0f38, cores=0x4e156c,
              descoberta0=0x507d78)
MURO, PORTAO = 0xfe, 0xfd
CORES_LIVRES, CORES_LIBERADAS = 0x4e1570, 0x4e1670
BUSCA_OCUPADA, BUSCA_CONCLUIDA, BUSCA_SUCESSO, STATUS_BUSCA = 0x4e0f36, 0x496302, 0x4e0f37, 0x4e0f4c
MASCARA_TIPO20 = 0x4dfb9c
CLIQUE = celula(21, 12)          # the proposed CAVE click (M3_ALVOS)
OBRA = CLIQUE + 0x202            # reference cell CalculConstruireBatiment hands to BatimentConstructible
ORIGEM = celula(19, 10)          # the CAVE record origin CreerBatiment stores
CONSTRUTOR = 12


def registro_criado(indice, tipo, origem, dono=0xc8):
    """Structure record as CreerBatiment leaves it before PlaceBatiment: +5 = 2, owner, origin, type, +0xa = 1, +6 = 0."""
    return [estrutura(indice, 5, u8(2)), estrutura(indice, 4, u8(dono)), estrutura(indice, 2, u16(origem)),
            estrutura(indice, 8, u8(tipo)), estrutura(indice, 0xa, u8(1)), estrutura(indice, 6, u8(0))]


def casos(p):
    """The declared matrix; ``p`` maps the ``GRADES`` names to the grid addresses at the pause."""
    grade = lambda nome, c, dados: (p[nome] + (c & 0xffff) * (2 if nome in ('tiles', 'regioes') else 1), dados)
    obj = lambda c, v: grade('objetos', c, u8(v))
    atr = lambda c, v: grade('atributos', c, u8(v))
    reg = lambda c, v: grade('regioes', c, u16(v))
    cor = lambda c, v: grade('cores', c, u8(v))
    desc = lambda c, v: grade('descoberta0', c, u8(v))
    sobre = lambda unidade, c: [campo(unidade, 8, u16(c)), campo(unidade, 0x7c, u16(c)), atr(c, 1)]
    c = []
    # ------------------------------------------------------------ PlaceBatiment: AX structure index
    t = 'PlaceBatiment'
    c += [caso('place_cave_target_19_10', t, registro_criado(1, 3, ORIGEM), EAX=1),
          caso('place_cave_index_upper_bits', t, registro_criado(1, 3, ORIGEM), EAX=0xabcd0001, EDX=0x5a5a5a5a,
               EBX=0x13572468, ECX=0x24681357)]
    for tipo in (0, 1, 2, 4, 5, 6, 7, 8, 10, 11, 13, 14, 15, 16, 17, 18, 19, 21):
        c.append(caso(f'place_type{tipo}_19_10', t, registro_criado(1, tipo, ORIGEM), EAX=1))
    c += [caso('place_type20_runtime_mask_zero', t, registro_criado(1, 20, ORIGEM), EAX=1),
          caso('place_type20_runtime_mask_declared', t, registro_criado(1, 20, ORIGEM) +
               [(MASCARA_TIPO20, bytes([0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1]))], EAX=1),
          caso('place_cave_record999', t, registro_criado(999, 3, ORIGEM), EAX=999),
          caso('place_cave_over_sanctuary', t, registro_criado(1, 3, celula(10, 10)), EAX=1),
          caso('place_cave_over_builder', t, registro_criado(1, 3, celula(16, 15)), EAX=1),
          caso('place_cave_map_edge_61_61', t, registro_criado(1, 3, celula(61, 61)), EAX=1),
          caso('place_cave_row_wrap_19_254', t, registro_criado(1, 3, celula(19, 254)), EAX=1),
          caso('place_cave_column_254', t, registro_criado(1, 3, celula(254, 20)), EAX=1),
          caso('place_cave_colours_exhausted', t, registro_criado(1, 3, ORIGEM) + [(CORES_LIVRES, u8(0))], EAX=1),
          caso('place_cave_one_colour_left', t, registro_criado(1, 3, ORIGEM) + [(CORES_LIVRES, u8(1))], EAX=1),
          caso('place_cave_next_to_sanctuary', t, registro_criado(1, 3, celula(18, 12)), EAX=1),
          caso('place_cave_owner_player1', t, registro_criado(1, 3, ORIGEM, dono=1), EAX=1),
          # walls (type 9) and gates (type 12): objects, +0x7c, collision bit 0, one region tag
          caso('place_wall_isolated', t, registro_criado(1, 9, CLIQUE), EAX=1),
          caso('place_wall_four_neighbours', t, registro_criado(1, 9, CLIQUE) +
               [obj(CLIQUE - 1, MURO), obj(CLIQUE + 1, PORTAO), obj(CLIQUE - 0x100, MURO), obj(CLIQUE + 0x100, MURO)],
               EAX=1),
          caso('place_wall_west_south', t, registro_criado(1, 9, CLIQUE) +
               [obj(CLIQUE - 1, MURO), obj(CLIQUE + 0x100, PORTAO)], EAX=1),
          caso('place_wall_on_gate_object', t, registro_criado(1, 9, CLIQUE) + [obj(CLIQUE, PORTAO),
                                                                                obj(CLIQUE - 1, MURO)], EAX=1),
          caso('place_wall_on_unit_region', t, registro_criado(1, 9, celula(17, 16)), EAX=1),
          caso('place_wall_next_to_colour', t, registro_criado(1, 9, celula(18, 12)), EAX=1),
          caso('place_gate_no_neighbours', t, registro_criado(1, 12, CLIQUE), EAX=1),
          caso('place_gate_horizontal', t, registro_criado(1, 12, CLIQUE) +
               [obj(CLIQUE - 1, MURO), obj(CLIQUE + 1, MURO)], EAX=1),
          caso('place_gate_vertical', t, registro_criado(1, 12, CLIQUE) +
               [obj(CLIQUE - 0x100, MURO), obj(CLIQUE + 0x100, PORTAO)], EAX=1),
          caso('place_gate_both_axes', t, registro_criado(1, 12, CLIQUE) +
               [obj(CLIQUE + d, MURO) for d in (-1, 1, -0x100, 0x100)], EAX=1),
          caso('place_gate_column0', t, registro_criado(1, 12, celula(0, 12)) +
               [obj(celula(1, 12), MURO), obj(celula(0, 11), MURO), obj(celula(0, 13), MURO)], EAX=1),
          caso('place_gate_west_only', t, registro_criado(1, 12, CLIQUE) + [obj(CLIQUE - 1, MURO)], EAX=1),
          caso('place_gate_on_unit_region', t, registro_criado(1, 12, celula(17, 16)) +
               [obj(celula(16, 16), MURO), obj(celula(18, 16), MURO)], EAX=1)]
    # ------------------------------------------------------------ ResetCheminTerrainModify: AX structure index
    t = 'ResetCheminTerrainModify'
    marcas_caverna = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (3, 1)]
    caverna_colocada = registro_criado(1, 3, ORIGEM) + [
        w for s, (x, y) in enumerate(marcas_caverna)
        for w in (reg(ORIGEM + y * 256 + x, 0x8000 | 1 << 5 | s), estrutura(1, 0xcc + 2 * s, u16(1)),
                  cor(ORIGEM + y * 256 + x, 0xfd))] + [(CORES_LIBERADAS + 0xfd, u8(0))]
    c += [caso('reset_sanctuary', t, EAX=0),
          caso('reset_sanctuary_upper_bits', t, EAX=0x77770000, EBX=0x11111111, ECX=0x22222222, EDX=0x33333333,
               ESI=0x44444444, EDI=0x55550000, EBP=0x66666666),
          caso('reset_tag_mismatch', t, registro_criado(1, 2, celula(12, 11)), EAX=1),
          caso('reset_placed_cave', t, caverna_colocada, EAX=1),
          caso('reset_placed_cave_partial_tags', t, caverna_colocada + [reg(ORIGEM + 1, 1)], EAX=1),
          caso('reset_placed_cave_full_free_list', t, caverna_colocada + [(CORES_LIVRES, u8(0xff))], EAX=1),
          caso('reset_placed_wall', t, registro_criado(1, 9, CLIQUE) +
               [reg(CLIQUE, 0x8020), estrutura(1, 0xcc, u16(1)), cor(CLIQUE, 0xfd), (CORES_LIBERADAS + 0xfd, u8(0))],
               EAX=1),
          caso('reset_placed_wall_no_colour', t, registro_criado(1, 9, CLIQUE) +
               [reg(CLIQUE, 0x8020), estrutura(1, 0xcc, u16(1))], EAX=1),
          caso('reset_type20_alias15', t, registro_criado(1, 20, ORIGEM), EAX=1)]
    # ------------------------------------------------------------ BatimentCollision: AL type, DX mask index
    t = 'BatimentCollision'
    c += [caso('collision_cave_0', t, EAX=3, EDX=0), caso('collision_cave_3', t, EAX=3, EDX=3),
          caso('collision_cave_8', t, EAX=3, EDX=8), caso('collision_wall_0', t, EAX=9, EDX=0),
          caso('collision_type20_alias', t, EAX=20, EDX=5), caso('collision_type22', t, EAX=22, EDX=1),
          caso('collision_upper_bits', t, EAX=0x12345603, EDX=0xabcd0006, EBX=0x5555aaaa)]
    # ------------------------------------------------------------ BatimentConstructible: AL type, DX reference cell, BX unit
    t = 'BatimentConstructible'
    dentro = celula(20, 11)
    c += [caso('constructible_cave_target', t, EAX=3, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_cave_builder_inside', t, sobre(CONSTRUTOR, dentro), EAX=3, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_cave_builder_last_cell', t, sobre(CONSTRUTOR, OBRA), EAX=3, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_cave_builder_next_cell', t,
               [campo(CONSTRUTOR, 0x7c, u16(dentro)), atr(dentro, 1)], EAX=3, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_cave_other_unit_inside', t, sobre(13, dentro), EAX=3, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_cave_builder_ab_mask1', t, sobre(CONSTRUTOR, dentro) + [campo(CONSTRUTOR, 0xab, u8(1))],
               EAX=3, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_cave_builder_state14', t, sobre(CONSTRUTOR, dentro) + [campo(CONSTRUTOR, 2, u8(14))],
               EAX=3, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_cave_quad_builder', t, [campo(CONSTRUTOR, 1, u8(3)), campo(CONSTRUTOR, 8, u16(dentro + 0x101)),
                                                     campo(CONSTRUTOR, 0x7c, u16(dentro + 0x101)), atr(dentro, 1)],
               EAX=3, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_cave_quad_7c', t, [campo(CONSTRUTOR, 1, u8(3)), campo(CONSTRUTOR, 0x7c, u16(dentro + 0x100)),
                                                atr(dentro, 1)], EAX=3, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_cave_type26_unit', t, [campo(CONSTRUTOR, 1, u8(26)), atr(dentro, 1)],
               EAX=3, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_cave_on_sanctuary', t, EAX=3, EDX=celula(16, 15), EBX=CONSTRUTOR),
          caso('constructible_cave_on_builder_from_13', t, EAX=3, EDX=celula(19, 18), EBX=13),
          caso('constructible_cave_attr_bit1_only', t, [atr(dentro, 2)], EAX=3, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_type1', t, EAX=1, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_type2', t, EAX=2, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_type4', t, EAX=4, EDX=OBRA, EBX=CONSTRUTOR),
          caso('constructible_type9_free', t, EAX=9, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('constructible_type9_on_unit13', t, EAX=9, EDX=celula(14, 16), EBX=CONSTRUTOR),
          caso('constructible_top_edge_wrap', t, EAX=3, EDX=celula(4, 2), EBX=CONSTRUTOR),
          caso('constructible_upper_bits', t, EAX=0xfedcba03, EDX=0x12340000 | OBRA, EBX=0x5678000c,
               ECX=0x9abcdef0, ESI=0x0badf00d, EDI=0xdeadbeef, EBP=0x01234567),
          caso('constructible_gate_on_own_wall', t, registro_criado(1, 9, CLIQUE, dono=0) +
               [obj(CLIQUE, MURO), reg(CLIQUE, 0x8020)], EAX=12, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('constructible_gate_on_foreign_wall', t, registro_criado(1, 9, CLIQUE, dono=1) +
               [obj(CLIQUE, MURO), reg(CLIQUE, 0x8020)], EAX=12, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('constructible_gate_wall_no_tag', t, [obj(CLIQUE, MURO)], EAX=12, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('constructible_gate_free_cell', t, EAX=12, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('constructible_gate_unit_tag', t, [obj(celula(17, 16), MURO)], EAX=12, EDX=celula(17, 16),
               EBX=CONSTRUTOR)]
    # ------------------------------------------------------------ BatimentPosable: AL type, DX centre cell, BX unit
    t = 'BatimentPosable'
    c += [caso('posable_cave_target', t, EAX=3, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('posable_type1', t, EAX=1, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('posable_type2', t, EAX=2, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('posable_type4', t, EAX=4, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('posable_cave_east_discovered_edge', t, EAX=3, EDX=celula(24, 12), EBX=CONSTRUTOR),
          caso('posable_cave_undiscovered_corner', t, EAX=3, EDX=celula(25, 12), EBX=CONSTRUTOR),
          caso('posable_cave_on_sanctuary', t, EAX=3, EDX=celula(14, 13), EBX=CONSTRUTOR),
          caso('posable_cave_builder_inside', t, sobre(CONSTRUTOR, dentro), EAX=3, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('posable_cave_other_unit_inside', t, sobre(13, dentro), EAX=3, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('posable_cave_one_cell_hidden', t, [desc(dentro, 1)], EAX=3, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('posable_cave_one_cell_not_grass', t, [grade('tiles', dentro, u16(0x15c))], EAX=3, EDX=CLIQUE,
               EBX=CONSTRUTOR),
          caso('posable_cave_tile_upper_grass', t, [grade('tiles', dentro, u16(0x1a4)), grade('tiles', dentro + 1,
                                                                                            u16(0x1a5))],
               EAX=3, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('posable_cave_player1_unit', t, [campo(CONSTRUTOR, 0, u8(1))], EAX=3, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('posable_cave_left_edge', t, EAX=3, EDX=celula(1, 12), EBX=CONSTRUTOR),
          caso('posable_cave_top_edge', t, EAX=3, EDX=celula(21, 1), EBX=CONSTRUTOR),
          caso('posable_cave_column_254', t, EAX=3, EDX=celula(254, 12), EBX=CONSTRUTOR),
          caso('posable_cave_column_255', t, EAX=3, EDX=celula(255, 12), EBX=CONSTRUTOR),
          caso('posable_cave_row_254', t, EAX=3, EDX=celula(21, 254), EBX=CONSTRUTOR),
          caso('posable_cave_row_255', t, EAX=3, EDX=celula(21, 255), EBX=CONSTRUTOR),
          caso('posable_type9', t, EAX=9, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('posable_type9_on_unit', t, EAX=9, EDX=celula(14, 16), EBX=CONSTRUTOR),
          caso('posable_gate_on_wall_horizontal', t, [obj(CLIQUE, MURO), obj(CLIQUE - 1, MURO), obj(CLIQUE + 1, MURO)],
               EAX=12, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('posable_gate_on_wall_alone', t, [obj(CLIQUE, MURO)], EAX=12, EDX=CLIQUE, EBX=CONSTRUTOR),
          caso('posable_gate_free_cell', t, [obj(CLIQUE - 1, MURO), obj(CLIQUE + 1, MURO)], EAX=12, EDX=CLIQUE,
               EBX=CONSTRUTOR),
          caso('posable_upper_bits', t, EAX=0x99999903, EDX=0x77770000 | CLIQUE, EBX=0x3333000c, ECX=0x12121212,
               ESI=0x34343434, EDI=0x56565656, EBP=0x78787878)]
    # ------------------------------------------------------------ helpers reached by the routines above
    t = 'EnginOccupeCase'                    # AX unit, DX cell, BL mask
    c += [caso('occupe_own_cell', t, EAX=12, EDX=celula(17, 16), EBX=1),
          caso('occupe_other_cell', t, EAX=12, EDX=CLIQUE, EBX=1),
          caso('occupe_7c_cell', t, [campo(12, 0x7c, u16(CLIQUE))], EAX=12, EDX=CLIQUE, EBX=1),
          caso('occupe_ab_mask1', t, [campo(12, 0xab, u8(1))], EAX=12, EDX=celula(17, 16), EBX=1),
          caso('occupe_ab0_mask2', t, EAX=12, EDX=celula(17, 16), EBX=2),
          caso('occupe_ab_mask2', t, [campo(12, 0xab, u8(1))], EAX=12, EDX=celula(17, 16), EBX=2),
          caso('occupe_state14', t, EAX=3, EDX=celula(14, 12), EBX=1),
          caso('occupe_quad_minus_101', t, [campo(12, 1, u8(3))], EAX=12, EDX=celula(16, 15), EBX=1),
          caso('occupe_quad_7c_minus_1', t, [campo(12, 1, u8(16)), campo(12, 0x7c, u16(CLIQUE))], EAX=12,
               EDX=CLIQUE - 1, EBX=1),
          caso('occupe_quad_miss', t, [campo(12, 1, u8(25))], EAX=12, EDX=CLIQUE, EBX=1),
          caso('occupe_type26', t, [campo(12, 1, u8(26))], EAX=12, EDX=CLIQUE, EBX=0x1234ff01),
          caso('occupe_upper_bits', t, EAX=0xffff000c, EDX=0xeeee0000 | celula(17, 16), EBX=0xdddd0001)]
    t = 'TerrainEstHerbe'                    # AX cell
    c += [caso('grass_cave_cell', t, EAX=CLIQUE), caso('grass_sanctuary_tile', t, EAX=celula(13, 12)),
          caso('grass_low_bound', t, [grade('tiles', CLIQUE, u16(0x15d))], EAX=CLIQUE),
          caso('grass_upper_range', t, [grade('tiles', CLIQUE, u16(0x1a0))], EAX=0x5555_0000 | CLIQUE, EDX=7),
          caso('grass_above', t, [grade('tiles', CLIQUE, u16(0x1a5))], EAX=CLIQUE),
          caso('grass_below', t, [grade('tiles', CLIQUE, u16(0x15c))], EAX=CLIQUE)]
    t = 'ValideHerse'                        # AX cell
    c += [caso('gate_query_none', t, EAX=CLIQUE),
          caso('gate_query_horizontal', t, [obj(CLIQUE - 1, PORTAO), obj(CLIQUE + 1, MURO)], EAX=CLIQUE),
          caso('gate_query_vertical', t, [obj(CLIQUE - 0x100, MURO), obj(CLIQUE + 0x100, MURO)], EAX=0x12340000 | CLIQUE)]
    t = 'ChercheMurCombinaisons'             # AX cell
    c += [caso('wall_combo_none', t, EAX=CLIQUE),
          caso('wall_combo_all', t, [obj(CLIQUE + d, MURO) for d in (-1, 1, -0x100, 0x100)], EAX=CLIQUE),
          caso('wall_combo_on_gate', t, [obj(CLIQUE, PORTAO), obj(CLIQUE - 1, MURO)], EAX=CLIQUE)]
    # ------------------------------------------------------------ DeplaceEngin: AX unit (the builder's walk)
    t = 'DeplaceEngin'
    ordem = [campo(CONSTRUTOR, 2, u8(0xb)), campo(CONSTRUTOR, 0xbe, u8(3)), campo(CONSTRUTOR, 0x7e, u16(CLIQUE)),
             campo(CONSTRUTOR, 0xb2, u16(CLIQUE)), campo(CONSTRUTOR, 0xc0, u16(0xffff))]
    c += [caso('move_build_order_state0', t, ordem, EAX=CONSTRUTOR),
          caso('move_build_order_state0_upper_bits', t, ordem, EAX=0x1234000c, EBX=0x11223344, ECX=0x55667788,
               EDX=0x99aabbcc, ESI=0xddeeff00, EDI=0x01020304, EBP=0x05060708),
          caso('move_build_order_at_target', t, ordem + [campo(CONSTRUTOR, 8, u16(CLIQUE)),
                                                         campo(CONSTRUTOR, 0x7c, u16(CLIQUE))], EAX=CONSTRUTOR),
          caso('move_build_order_blocked_by_unit13', t, ordem + [campo(13, 8, u16(celula(18, 15))),
                                                                 campo(13, 0x7c, u16(celula(18, 15))),
                                                                 reg(celula(18, 15), 0x4000 | 13 << 3),
                                                                 atr(celula(18, 15), 1)], EAX=CONSTRUTOR),
          caso('move_state1', t, ordem + [campo(CONSTRUTOR, 0x88, u8(1))], EAX=CONSTRUTOR),
          caso('move_state2', t, ordem + [campo(CONSTRUTOR, 0x88, u8(2))], EAX=CONSTRUTOR),
          caso('move_state7', t, ordem + [campo(CONSTRUTOR, 0x88, u8(7))], EAX=CONSTRUTOR),
          caso('move_state6_count', t, ordem + [campo(CONSTRUTOR, 0x88, u8(6)), campo(CONSTRUTOR, 0x8b, u8(4))],
               EAX=CONSTRUTOR),
          caso('move_state6_wait_over', t, ordem + [campo(CONSTRUTOR, 0x88, u8(6)), campo(CONSTRUTOR, 0x8b, u8(0x13))],
               EAX=CONSTRUTOR),
          caso('move_state3_search_busy', t, ordem + [campo(CONSTRUTOR, 0x88, u8(3)), (BUSCA_OCUPADA, u8(1))],
               EAX=CONSTRUTOR),
          caso('move_state3_pushed', t, ordem + [campo(CONSTRUTOR, 0x88, u8(3)), campo(CONSTRUTOR, 0x86, u8(1))],
               EAX=CONSTRUTOR),
          caso('move_state3_search', t, ordem + [campo(CONSTRUTOR, 0x88, u8(3))], EAX=CONSTRUTOR),
          caso('move_state4_blocked_status8', t, ordem + [campo(CONSTRUTOR, 0x88, u8(4)), (BUSCA_CONCLUIDA, u8(1)),
                                                          (BUSCA_SUCESSO, u8(0)), (STATUS_BUSCA, u8(8))],
               EAX=CONSTRUTOR),
          caso('move_state0_other_unit13', t, [campo(13, 0x7e, u16(celula(16, 13)))], EAX=13)]
    nomes = [x['case'] for x in c]
    if len(nomes) != len(set(nomes)):
        raise ValueError('Duplicate case names')
    return c


def verificar_pausa(ler):
    """Check the documented pause facts with ``ler(addr, n) -> bytes``; returns the grid pointers. Raises on
    any difference."""
    u16_ = lambda a: struct.unpack('<H', ler(a, 2))[0]
    u32_ = lambda a: struct.unpack('<I', ler(a, 4))[0]
    p = {nome: u32_(slot) for nome, slot in GRADES.items()}
    linha = lambda nome, c, n, passo=1: ler(p[nome] + c * passo, n * passo)
    fatos = {
        'unit pool': (u32_(0x4e19a0), UNIDADES),
        'map size': ((u16_(0x497168), u16_(0x49716a)), (64, 64)),
        'wall/gate objects': (ler(0x495bf8, 2), bytes([MURO, PORTAO])),
        'free colours': (ler(CORES_LIVRES, 1), b'\xfe'),
        'cave size': (tuple(u16_(0x495d8c + 52 * 3 + o) for o in (0, 2)), (5, 5)),
        'type-20 mask pointer': (u32_(0x495d94 + 52 * 20), MASCARA_TIPO20),
        'builder type/state/cell': ((ler(UNIDADES + CONSTRUTOR * PASSO + 1, 2), u16_(UNIDADES + CONSTRUTOR * PASSO + 8)),
                                    (bytes([7, 7]), celula(17, 16))),
        'unit 13 cell': (u16_(UNIDADES + 13 * PASSO + 8), celula(14, 16)),
        'sanctuary record': ((ler(ESTRUTURAS + 4, 2), u16_(ESTRUTURAS + 2), ler(ESTRUTURAS + 8, 1)),
                             (b'\x00\x05', celula(12, 11), b'\x02')),
        'free structure records 1 and 999': ((ler(ESTRUTURAS + PASSO + 5, 1), ler(ESTRUTURAS + 999 * PASSO + 5, 1)),
                                             (b'\x00', b'\x00')),
        'cave site regions free': (linha('regioes', ORIGEM, 5, 2) + linha('regioes', ORIGEM + 0x100, 5, 2),
                                   struct.pack('<10H', *[1] * 10)),
        'cave site attributes/objects clear': (b''.join(linha('atributos', ORIGEM + 0x100 * y, 5) +
                                                        linha('objetos', ORIGEM + 0x100 * y, 5) for y in range(5)),
                                               bytes(50)),
        'cave site discovered by player 0': (b''.join(linha('descoberta0', ORIGEM + 0x100 * y, 5) for y in range(5)),
                                             bytes(25)),
        'builder region tag': (u16_(p['regioes'] + 2 * celula(17, 16)), 0x4000 | CONSTRUTOR << 3),
    }
    erradas = {k: v for k, v in fatos.items() if v[0] != v[1]}
    if erradas:
        raise RuntimeError(f'Pause state differs from the documented facts: {erradas}')
    return p
