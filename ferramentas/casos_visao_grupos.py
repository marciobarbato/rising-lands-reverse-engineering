"""Declared case matrix for structure vision, group selection, minimap view and exit position (M3.1 round 2).

The Core routines ai-runtime's M3 probe chain (docs/AI_RUNTIME.md "M3.1 round 2") and Economy's recruitment name:
- CalculBatimentNextEtape's per-player vision of a structure: BatimentIllumine 0x419233 (AX structure, DL player,
  BL on/off) and BatimentDecouvre 0x419d54 (AX structure, DL player), with the per-cell routines they reach,
  IllumineCase 0x476968, EteintCase 0x476adc and DecouvreCase 0x47670a (and SetMiniMap modes 1/2/3);
- ProcessInputGame tags 0xb/0xc and InputGame's group-number path: SauveSelectionGroupe 0x4726f7 (AL player,
  DL group), RestaureSelectionGroupe 0x472769 (AL player, DL group), EnginGetCentreGroupe 0x442139 (AL player,
  EDX/EBX pointers to the u16 x/y results, CL group);
- the minimap view: MiniMapRecentre 0x46a01b (no arguments) and MiniMapSetPos 0x46a19e (AX x, DX y);
- the recruitment exit: CalculPosition 0x420698 (AX structure; BL unused) with every register, and
  RechercheDecalageSortie 0x41d1d0 (AX structure).

Every case starts from the exact paused frame-1 state of ``bancada_entrada_estruturas`` (MONDE01 display reference,
first ProcessInputGame entry; the pause of SELECTION_ORDERS, CONSTRUCTION and STRUCTURE_ENTRY). Facts of that state
used below are those of ``casos_entrada_estruturas.verificar_pausa`` plus (checked by ``verificar_pausa`` here):
- units 0..15 are alive, in no group (+0xbc = 0xff) and unselected; the selection lists are empty;
- the view is (3, 5, 25, 17), the map 64x64, the minimap scroll (0x507d68/6a) and lock (0x507d6c/6e) words are 0,
  the minimap display size words 0x496fe0/2 are 128 and the minimap margin byte 0x508f90 is 0;
- players 1..3 have discovered and lit nothing (discovery/border bytes 0x1f, light counts 0); player 0's
  sanctuary footprint is discovered and lit.
A case only adds its declared writes, native preparation (the prepared CAVE of STRUCTURE_ENTRY: ``CreerBatiment``,
progress, ``BatimentConstruction``, ``BatimentRetireColon`` called natively) and argument registers. Structure
record 2 is free at the pause; cases that need another footprint write its type byte (+8) and origin word (+2)
only, which is all these routines read of it. Importing this module executes nothing.
"""
import struct

from casos_entrada_estruturas import CAVE, preparar_caverna
from casos_selecao_ordens import ESTRUTURAS, UNIDADES, campo, celula, estrutura, lista, u8, u16

PASSO = 276
TIPOS = 0x495d8c                 # u16 width, +2 height per structure type, stride 52
VISTA = 0x508720                 # u16 view x, y, width, height
MAPA = 0x497168                  # u16 map width, height
MINI_DISPLAY = 0x496fe0          # u16 minimap display width, height
MINI_POS, MINI_LOCK = 0x507d68, 0x507d6c
MARGEM = 0x508f90                # signed byte; read as the top byte of the dword at 0x508f8d
DESCOBERTA, BORDAS, CONTAGENS = 0x507d78, 0x507d88, 0x507d98
GRUPO, SELECIONADA = 0xbc, 0xbd
LIXO = dict(EBX=0x5a5a5a5a, ECX=0xc3c3c3c3, ESI=0x12345678, EDI=0x9abcdef0, EBP=0x0f0f0f0f)


def caso(nome, rotina, writes=(), preparo=(), **regs):
    return dict(case=nome, preparation=list(preparo),
                steps=[dict(routine=rotina, registers=regs, writes=list(writes), stack=[])])


def janela(nome, passos, preparo=(), writes=()):
    """Consecutive measured steps (state carried); ``passos`` = [(routine, registers)]."""
    return dict(case=nome, preparation=list(preparo),
                steps=[dict(routine=r, registers=regs, writes=list(writes) if i == 0 else [], stack=[])
                       for i, (r, regs) in enumerate(passos)])


def registro2(tipo, origem):
    return [estrutura(2, 8, u8(tipo)), estrutura(2, 2, u16(origem))]


def tamanho(tipo, largura, altura):
    return [(TIPOS + 52 * tipo, u16(largura) + u16(altura))]


def casos(alvo_progresso, grades, tamanhos):
    """The declared matrix; ``grades`` maps 'D'/'B'/'N' to the per-player grid pointers (0..3) and 'atributos' to
    the attribute grid pointer at the pause; ``tamanhos`` = the (width, height) words of structure types 0..21."""
    cav = preparar_caverna(alvo_progresso)
    D, B, N, A = grades['D'], grades['B'], grades['N'], grades['atributos']
    c = []
    # ------------------------------------------------------------ BatimentIllumine: AX structure, DL player, BL flag
    t = 'BatimentIllumine'
    for p in range(4):
        c.append(caso(f'illumine_sanctuary_p{p}_on', t, EAX=0, EDX=p, EBX=1))
        c.append(caso(f'illumine_sanctuary_p{p}_off', t, EAX=0, EDX=p, EBX=0))
    um = [(N[0] + celula(12, 11) + d, u8(1)) for d in (0, 1, 2)] + [(N[0] + celula(13, 12), u8(1))]
    c += [caso('illumine_sanctuary_p0_off_count1', t, um, EAX=0, EDX=0, EBX=0),
          caso('illumine_sanctuary_p1_saturated', t, [(N[1] + celula(14, 12), u8(0xff)), (N[1] + celula(12, 11),
                                                                                         u8(0xfe))],
               EAX=0, EDX=1, EBX=1),
          caso('illumine_sanctuary_p2_flag_0x80', t, EAX=0, EDX=2, EBX=0x80),
          caso('illumine_upper_bits_on', t, EAX=0xabcd0000, EDX=0x12345601, EBX=0x77777701, **{
              k: v for k, v in LIXO.items() if k != 'EBX'}),
          caso('illumine_upper_bits_off', t, EAX=0xffff0000, EDX=0xfedcba00, EBX=0x55555500, ECX=0x1, ESI=0x2,
               EDI=0x3, EBP=0x4)]
    for p in range(4):
        c.append(caso(f'illumine_cave_p{p}_on', t, preparo=cav, EAX=CAVE, EDX=p, EBX=1))
    c += [caso('illumine_cave_p0_off', t, preparo=cav, EAX=CAVE, EDX=0, EBX=0),
          caso('illumine_cave_created_p0_on', t, preparo=cav[:1], EAX=CAVE, EDX=0, EBX=1),
          caso('illumine_cave_created_p1_on', t, preparo=cav[:1], EAX=CAVE, EDX=1, EBX=1)]
    for tipo in range(22):
        c.append(caso(f'illumine_type{tipo}_p1_on', t, registro2(tipo, celula(30, 30)), EAX=2, EDX=1, EBX=1))
    for nome, origem, tipo, p in (('corner_0_0', celula(0, 0), 8, 1), ('map_edge_61_61', celula(61, 61), 3, 2),
                                  ('map_edge_60_0', celula(60, 0), 8, 3), ('column_253', celula(253, 10), 8, 1),
                                  ('row_251', celula(10, 251), 3, 1), ('corner_255_250', celula(255, 250), 3, 2)):
        c.append(caso(f'illumine_{nome}_on', t, registro2(tipo, origem), EAX=2, EDX=p, EBX=1))
    c += [caso('illumine_corner_0_0_p0_off', t, registro2(8, celula(0, 0)), EAX=2, EDX=0, EBX=0),
          caso('illumine_width0', t, registro2(3, celula(30, 30)) + tamanho(3, 0, 5), EAX=2, EDX=1, EBX=1),
          caso('illumine_height0', t, registro2(3, celula(30, 30)) + tamanho(3, 5, 0), EAX=2, EDX=1, EBX=1),
          caso('illumine_rows_out_of_grid', t, registro2(3, celula(30, 254)) + tamanho(3, 2, 6), EAX=2, EDX=1,
               EBX=1)]
    c.append(janela('illumine_window_p1_on_off',
                    [(t, dict(EAX=0, EDX=1, EBX=1)), (t, dict(EAX=0, EDX=1, EBX=1)), (t, dict(EAX=0, EDX=1, EBX=0)),
                     (t, dict(EAX=0, EDX=1, EBX=0))]))
    # ------------------------------------------------------------ BatimentDecouvre: AX structure, DL player
    t = 'BatimentDecouvre'
    for p in range(4):
        c.append(caso(f'decouvre_sanctuary_p{p}', t, EAX=0, EDX=p))
    c += [caso('decouvre_sanctuary_c8', t, EAX=0, EDX=0xc8),
          caso('decouvre_cave_c8', t, preparo=cav, EAX=CAVE, EDX=0xc8),
          caso('decouvre_upper_bits', t, EAX=0x55550000, EDX=0xaaaaaa02, **LIXO),
          caso('decouvre_upper_bits_c8', t, EAX=0x12340001, EDX=0x567800c8, **LIXO)]
    for p in range(4):
        c.append(caso(f'decouvre_cave_p{p}', t, preparo=cav, EAX=CAVE, EDX=p))
    c.append(caso('decouvre_cave_created_p1', t, preparo=cav[:1], EAX=CAVE, EDX=1))
    for tipo in range(22):
        c.append(caso(f'decouvre_type{tipo}_p2', t, registro2(tipo, celula(30, 30)), EAX=2, EDX=2))
    for nome, origem, tipo, p in (('corner_0_0', celula(0, 0), 8, 1), ('map_edge_59_59', celula(59, 59), 8, 2),
                                  ('map_edge_0_60', celula(0, 60), 3, 3), ('column_252', celula(252, 10), 3, 1),
                                  ('row_250', celula(10, 250), 3, 1), ('p0_partly_known', celula(14, 10), 8, 0)):
        c.append(caso(f'decouvre_{nome}', t, registro2(tipo, origem), EAX=2, EDX=p))
    c += [caso('decouvre_width_256', t, registro2(21, celula(0, 30)) + tamanho(21, 0x100, 1), EAX=2, EDX=1),
          caso('decouvre_height_256', t, registro2(21, celula(30, 0)) + tamanho(21, 1, 0x100), EAX=2, EDX=2),
          caso('decouvre_width0_height0', t, registro2(21, celula(30, 30)) + tamanho(21, 0, 0), EAX=2, EDX=1),
          caso('decouvre_minimap_known_cells', t, registro2(3, celula(30, 30)) +
               [(D[1] + celula(31, 31), u8(0)), (D[1] + celula(32, 31), u8(0x10))], EAX=2, EDX=1)]
    c.append(janela('decouvre_window_twice', [(t, dict(EAX=0, EDX=3)), (t, dict(EAX=0, EDX=3))]))
    # ------------------------------------------------------------ the per-cell routines: AX cell, DL player
    for t, pre in (('IllumineCase', 'illuminecase'), ('EteintCase', 'eteintcase'), ('DecouvreCase', 'decouvrecase')):
        for x, y in ((30, 30), (0, 30), (30, 0), (63, 30), (30, 63), (0, 0), (63, 63), (200, 100)):
            for p in (0, 1):
                c.append(caso(f'{pre}_{x}_{y}_p{p}', t, EAX=celula(x, y), EDX=p))
        c.append(caso(f'{pre}_upper_bits', t, EAX=0x7777000 | celula(31, 30), EDX=0x99999902, **LIXO))
    for contagem in (0, 1, 2, 0xfe, 0xff):
        c += [caso(f'illuminecase_count{contagem:x}', 'IllumineCase', [(N[2] + celula(20, 20), u8(contagem))],
                   EAX=celula(20, 20), EDX=2),
              caso(f'eteintcase_count{contagem:x}', 'EteintCase', [(N[2] + celula(20, 20), u8(contagem))],
                   EAX=celula(20, 20), EDX=2)]
    # ------------------------------------------------------------ SauveSelectionGroupe: AL player, DL group
    t = 'SauveSelectionGroupe'
    tres = lista(0, [11, 12, 13])
    c += [caso('sauve_three_selected_g1', t, tres, EAX=0, EDX=1),
          caso('sauve_clears_previous_members', t, lista(0, [11]) + [campo(0, GRUPO, u8(1)), campo(1, GRUPO, u8(1)),
                                                                     campo(2, GRUPO, u8(2))], EAX=0, EDX=1),
          caso('sauve_moves_members_between_groups', t, lista(0, [0, 1]) + [campo(0, GRUPO, u8(3))], EAX=0, EDX=4),
          caso('sauve_other_player', t, tres, EAX=1, EDX=1),
          caso('sauve_nothing_selected', t, EAX=0, EDX=1),
          caso('sauve_group_ff', t, tres, EAX=0, EDX=0xff),
          caso('sauve_group_0', t, tres + [campo(14, GRUPO, u8(0))], EAX=0, EDX=0),
          caso('sauve_dead_selected', t, tres + [campo(13, 2, u8(0))], EAX=0, EDX=1),
          caso('sauve_state4_selected', t, tres + [campo(13, 2, u8(4))], EAX=0, EDX=1),
          caso('sauve_foreign_owner_selected', t, tres + [campo(12, 0, u8(1))], EAX=0, EDX=1),
          caso('sauve_last_unit_alive_owned', t, tres + [campo(799, 0, u8(0)), campo(799, 2, u8(7)),
                                                         campo(799, SELECIONADA, u8(1))], EAX=0, EDX=1),
          caso('sauve_last_unit_alive_foreign', t, tres + [campo(799, 0, u8(2)), campo(799, 2, u8(7))], EAX=0, EDX=1),
          caso('sauve_upper_bits', t, tres, EAX=0xdead0000, EDX=0xbeef1201, **LIXO)]
    # ------------------------------------------------------------ RestaureSelectionGroupe: AL player, DL group
    t = 'RestaureSelectionGroupe'
    g = lambda us, n=1: [campo(u, GRUPO, u8(n)) for u in us]
    c += [caso('restaure_builder_g1', t, g([12]), EAX=0, EDX=1),
          caso('restaure_builder_state_b', t, g([12]) + [campo(12, 2, u8(0xb))], EAX=0, EDX=1),
          caso('restaure_builder_state_f', t, g([12]) + [campo(12, 2, u8(0xf))], EAX=0, EDX=1),
          caso('restaure_builder_state_b_voice_busy', t, g([12]) + [campo(12, 2, u8(0xb)),
                                                                    campo(12, 0x104, struct.pack('<I', 7))],
               EAX=0, EDX=1),
          caso('restaure_three', t, g([11, 12, 13]), EAX=0, EDX=1),
          caso('restaure_soldiers', t, g([0, 1, 2], 2), EAX=0, EDX=2),
          caso('restaure_type10_first', t, g([11, 13]) + [campo(11, 1, u8(10))], EAX=0, EDX=1),
          caso('restaure_loop_type_first', t, g([11, 13]) + [campo(11, 1, u8(0xc))], EAX=0, EDX=1),
          caso('restaure_loop_type_last', t, g([11]) + [campo(11, 1, u8(0x10))], EAX=0, EDX=1),
          caso('restaure_colonists_inside', t, g(range(3, 11), 5), EAX=0, EDX=5),
          caso('restaure_deselects_others', t, lista(0, [0, 1, 14]) + g([12]), EAX=0, EDX=1),
          caso('restaure_reselects_members', t, lista(0, [12, 13]) + g([12, 13]), EAX=0, EDX=1),
          caso('restaure_list_full', t, lista(0, [], contagem=0xff) + g([12, 13]), EAX=0, EDX=1),
          caso('restaure_list_254', t, lista(0, [], contagem=0xfe) + g([12, 13]), EAX=0, EDX=1),
          caso('restaure_empty_group', t, EAX=0, EDX=7),
          caso('restaure_group_ff_all', t, EAX=0, EDX=0xff),
          caso('restaure_other_player', t, g([13, 14]) + [campo(13, 0, u8(1)), campo(14, 0, u8(1))], EAX=1, EDX=1),
          caso('restaure_dead_member', t, g([13, 14]) + [campo(13, 2, u8(0))], EAX=0, EDX=1),
          caso('restaure_unit_undiscovered_cell', t, g([12]) + [campo(12, 8, u16(celula(60, 60)))], EAX=0, EDX=1),
          caso('restaure_last_unit_owned', t, g([12]) + [campo(799, 0, u8(0)), campo(799, 2, u8(7)),
                                                         campo(799, 1, u8(1)), campo(799, 8, u16(celula(5, 5)))],
               EAX=0, EDX=1),
          caso('restaure_upper_bits', t, g([12, 13]), EAX=0x1111ff00, EDX=0x22222201, **LIXO)]
    c.append(janela('group_save_then_restore',
                    [('SauveSelectionGroupe', dict(EAX=0, EDX=3)), ('BatimentDeselectionner', dict(EAX=0)),
                     ('DeSelectionGroupe', dict(EAX=0)), ('RestaureSelectionGroupe', dict(EAX=0, EDX=3))],
                    writes=lista(0, [12, 13, 14])))
    # ------------------------------------------------------------ EnginGetCentreGroupe: AL, EDX/EBX pointers, CL
    t = 'EnginGetCentreGroupe'
    px, py = VISTA, VISTA + 2
    c += [caso('centre_no_member', t, EAX=0, EDX=px, EBX=py, ECX=5),
          caso('centre_group_ff_first_alive', t, EAX=0, EDX=px, EBX=py, ECX=0xff),
          caso('centre_group1_two_members', t, g([13, 14]), EAX=0, EDX=px, EBX=py, ECX=1),
          caso('centre_group1_builder', t, g([12]), EAX=0, EDX=px, EBX=py, ECX=1),
          caso('centre_member_dead_first', t, g([11, 13]) + [campo(11, 2, u8(0))], EAX=0, EDX=px, EBX=py, ECX=1),
          caso('centre_member_state4_first', t, g([11, 13]) + [campo(11, 2, u8(4))], EAX=0, EDX=px, EBX=py, ECX=1),
          caso('centre_member_foreign_first', t, g([11, 13]) + [campo(11, 0, u8(2))], EAX=0, EDX=px, EBX=py, ECX=1),
          caso('centre_other_player', t, g([13]), EAX=1, EDX=px, EBX=py, ECX=1),
          caso('centre_swapped_pointers', t, g([13]), EAX=0, EDX=py, EBX=px, ECX=1),
          caso('centre_no_member_view_wraps', t, [(VISTA, u16(0xfffe))], EAX=0, EDX=px, EBX=py, ECX=5),
          caso('centre_no_member_view_size0', t, [(VISTA + 4, u16(0) + u16(0))], EAX=0, EDX=px, EBX=py, ECX=5),
          caso('centre_no_member_large_view', t, [(VISTA, u16(40) + u16(50) + u16(0x8001) + u16(0x9000))], EAX=0,
               EDX=px, EBX=py, ECX=5),
          caso('centre_upper_bits', t, g([13]), EAX=0xabcdef00, EDX=px, EBX=py, ECX=0x12345601, ESI=0x5, EDI=0x6,
               EBP=0x7),
          caso('centre_upper_bits_none', t, EAX=0xabcdef00, EDX=px, EBX=py, ECX=0x12345609, ESI=0x5, EDI=0x6,
               EBP=0x7)]
    # ------------------------------------------------------------ MiniMapRecentre (no arguments)
    t = 'MiniMapRecentre'
    pos = lambda x, y: [(MINI_POS, u16(x) + u16(y))]
    vista = lambda x, y, w=25, h=17: [(VISTA, u16(x) + u16(y) + u16(w) + u16(h))]
    c += [caso('recentre_pause', t),
          caso('recentre_pause_upper_bits', t, **LIXO),
          caso('recentre_scroll_inside', t, pos(300, 200)),
          caso('recentre_scroll_past_x', t, pos(700, 10), **LIXO),
          caso('recentre_scroll_past_y', t, pos(10, 600), **LIXO),
          caso('recentre_scroll_past_both', t, pos(0xffff, 0x8000), **LIXO),
          caso('recentre_margin_positive', t, pos(100, 200) + [(MARGEM, u8(5))], **LIXO),
          caso('recentre_margin_positive_past', t, pos(700, 650) + [(MARGEM, u8(5))], **LIXO),
          caso('recentre_margin_negative', t, pos(0, 0) + [(MARGEM, u8(0xfb))], **LIXO),
          caso('recentre_margin_negative_past', t, pos(900, 700) + [(MARGEM, u8(0x80))], **LIXO),
          caso('recentre_margin_large', t, pos(10, 10) + [(MARGEM, u8(0x7f))], **LIXO),
          caso('recentre_view_past_x', t, vista(50, 5), **LIXO),
          caso('recentre_view_past_y', t, vista(3, 60), **LIXO),
          caso('recentre_view_past_both', t, vista(60, 61), EBX=0xffff0000, ECX=0x00010000, ESI=0x80000000,
               EDI=0x7fff0000),
          caso('recentre_view_exact_edge', t, vista(39, 47)),
          caso('recentre_view_wider_than_map', t, vista(0, 0, 100, 80), **LIXO),
          caso('recentre_display_small', t, pos(400, 300) + [(MINI_DISPLAY, u16(16) + u16(8))], **LIXO),
          caso('recentre_map_large', t, vista(200, 200) + [(MAPA, u16(256) + u16(256))], **LIXO)]
    t = 'MiniMapSetPos'
    lock = lambda x, y: [(MINI_LOCK, u16(x) + u16(y))]
    c += [caso('setpos_10_20', t, EAX=10, EDX=20, EBX=0),
          caso('setpos_lock_offsets', t, lock(5, 0xfffd), EAX=10, EDX=20, EBX=0),
          caso('setpos_negative_x', t, EAX=0xfff0, EDX=20, EBX=0),
          caso('setpos_negative_y', t, EAX=10, EDX=0xffff8000, EBX=0),
          caso('setpos_negative_after_lock', t, lock(0xfff0, 0xffe0), EAX=10, EDX=20, EBX=0),
          caso('setpos_far', t, EAX=0x7000, EDX=0x6000, EBX=0),
          caso('setpos_upper_bits', t, lock(3, 4), EAX=0xabcd0040, EDX=0x12340030, EBX=0x5555, ECX=0x77770000,
               ESI=0x1, EDI=0x2, EBP=0x3),
          caso('setpos_edx_carry', t, lock(0, 0x8000), EAX=1, EDX=0x00018000, ECX=0xffff0000, EBX=0),
          caso('setpos_margin_and_view', t, vista(55, 2) + [(MARGEM, u8(3))], EAX=600, EDX=5, EBX=0, **{
              k: v for k, v in LIXO.items() if k != 'EBX'})]
    c.append(janela('minimap_press_then_drag', [('MiniMapSetPos', dict(EAX=40, EDX=30, EBX=0)),
                                                ('MiniMapSetPos', dict(EAX=45, EDX=33, EBX=0)),
                                                ('MiniMapRecentre', dict())], writes=lock(2, 1)))
    # ------------------------------------------------------------ CalculPosition: AX structure (every register)
    t = 'CalculPosition'
    for tipo in range(22):
        c.append(caso(f'position_type{tipo}', t, registro2(tipo, celula(30, 30)), EAX=2, EBX=1, **{
            k: v for k, v in LIXO.items() if k != 'EBX'}))
        c.append(caso(f'position_type{tipo}_origin0', t, registro2(tipo, 0), EAX=2, EBX=0, ECX=0, ESI=0, EDI=0))
    c += [caso('position_type8_short', t, registro2(8, celula(30, 30)) + tamanho(8, 6, 2), EAX=2, **LIXO),
          caso('position_type18_narrow', t, registro2(18, celula(30, 30)) + tamanho(18, 0, 2), EAX=2, **LIXO),
          caso('position_type_out_of_table', t, registro2(0x16, celula(30, 30)), EAX=2, **LIXO),
          caso('position_sanctuary', t, EAX=0), caso('position_cave', t, preparo=cav, EAX=CAVE),
          caso('position_upper_index_bits', t, registro2(0, celula(30, 30)), EAX=0xffff0002, **LIXO)]
    # ------------------------------------------------------------ RechercheDecalageSortie: AX structure
    t = 'RechercheDecalageSortie'
    for tipo in range(22):
        if tipo in (9, 12, 17):
            continue
        c.append(caso(f'decalage_type{tipo}', t, registro2(tipo, celula(30, 30)), EAX=2, **LIXO))
    c += [caso('decalage_sanctuary', t, EAX=0), caso('decalage_cave', t, preparo=cav, EAX=CAVE),
          caso('decalage_upper_bits', t, registro2(1, celula(30, 30)), EAX=0x77770002, EBX=0x1, ECX=0x2, EDX=0x3,
               ESI=0xffff0000, EDI=0x80000000, EBP=0x4)]
    # Type 5's exit cell from the original tables (0x420640 -> 0x420819: width - 1, height; 0x420380: 0x202;
    # 0x4207d9: - 0x102), declared here to aim the blocked neighbours (attribute bit 0, TerrainEnCollision mask 1).
    w5, h5 = tamanhos[5]
    saida5 = (celula(30, 30) + (h5 << 8) + w5 - 1 - 0x202 + 0x102) & 0xffff
    vizinhos = [(saida5 + dy * 256 + dx) & 0xffff for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dx, dy) != (0, 0)]
    livres = [(A + v, u8(0)) for v in vizinhos]
    for bloqueados in (0, 1, 3, 7, 8):
        c.append(caso(f'decalage_type5_blocked{bloqueados}', t, registro2(5, celula(30, 30)) + livres +
                      [(A + v, u8(0xff if k % 2 else 1)) for k, v in enumerate(vizinhos[:bloqueados])], EAX=2, **LIXO))
    c.append(caso('decalage_type5_other_bits_only', t, registro2(5, celula(30, 30)) +
                  [(A + v, u8(0xfe)) for v in vizinhos], EAX=2, **LIXO))
    for nome, origem, tipo in (('corner_0_0', 0, 5), ('row_0', celula(30, 0), 1), ('column_0', celula(0, 30), 18),
                               ('column_255', celula(253, 30), 5), ('row_255', celula(30, 253), 1)):
        c.append(caso(f'decalage_{nome}', t, registro2(tipo, origem), EAX=2, **LIXO))
    return c


def verificar_pausa(ler):
    """Check the documented pause facts with ``ler(addr, n) -> bytes``; returns (cave progress target, grids)."""
    import casos_entrada_estruturas as cee
    alvo, grade = cee.verificar_pausa(ler)
    u16_ = lambda a: struct.unpack('<H', ler(a, 2))[0]
    u32_ = lambda a: struct.unpack('<I', ler(a, 4))[0]
    u = lambda i, o: ler(UNIDADES + PASSO * i + o, 1)[0]
    grades = dict(D=[u32_(DESCOBERTA + 4 * p) for p in range(4)], B=[u32_(BORDAS + 4 * p) for p in range(4)],
                  N=[u32_(CONTAGENS + 4 * p) for p in range(4)], atributos=grade['atributos'])
    santuario = u16_(ESTRUTURAS + 2)
    fatos = {
        'units 0..15 alive, no group, unselected': (
            [(u(i, 2) not in (0, 4), u(i, GRUPO), u(i, SELECIONADA)) for i in range(16)], [(True, 0xff, 0)] * 16),
        'view': ([u16_(VISTA + 2 * k) for k in range(4)], [3, 5, 25, 17]),
        'map': ([u16_(MAPA), u16_(MAPA + 2)], [64, 64]),
        'minimap words': ([u16_(MINI_POS + 2 * k) for k in range(4)] + [u16_(MINI_DISPLAY), u16_(MINI_DISPLAY + 2)],
                          [0, 0, 0, 0, 128, 128]),
        'minimap margin': (ler(MARGEM, 1), b'\x00'),
        'players 1..3 know nothing at the sanctuary': (
            [(ler(grades['D'][p] + santuario, 1), ler(grades['B'][p] + santuario, 1),
              ler(grades['N'][p] + santuario, 1)) for p in (1, 2, 3)], [(b'\x1f', b'\x1f', b'\x00')] * 3),
        'player 0 sees the sanctuary': ((ler(grades['D'][0] + santuario, 1), ler(grades['N'][0] + santuario, 1) != b'\x00'),
                                        (b'\x00', True)),
    }
    erradas = {k: v for k, v in fatos.items() if v[0] != v[1]}
    if erradas:
        raise RuntimeError(f'Pause state differs from the documented facts: {erradas}')
    return alvo, grades, [(u16_(TIPOS + 52 * t), u16_(TIPOS + 52 * t + 2)) for t in range(22)]
