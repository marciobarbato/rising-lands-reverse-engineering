"""Declared case matrix for the M3.1 input-path leaf calls (InputGame -> SetPlayerOrdre -> ProcessInputGame).

Every case starts from the exact paused frame-1 state of Core's ``bancada_selecao_ordens`` (MONDE01 display
reference, first ProcessInputGame entry). Facts of that state used here (dumped natively at the pause):
- the local player 0x508041 is 0, the cycle counter is 1, the view is (3, 5, 25, 17) on a 64x64 map and the
  screen is 800x600; the mouse-zone table 0x5099b4 holds zones 1..8 (2-px edges), 10 (minimap (0,0)-(128,128)),
  11 (HUD (0,544)-(800,600)) and the 1x1 dummies 26..31;
- every selection list is empty, every structure selection word 0x495be0 is 0xffff, the action mode bytes
  0x496207/08/09 are 0xff, the help page 0x4e05ae is 0, the drag flag 0x4e19b0 is 0 and every WndProc
  input flag 0x5099ae..b2 is 0;
- unit 12 (type 7, builder) is on cell 4113 = (17, 16) and its order Bag holds four code-3 (structure)
  entries of types 1..4; units 13/14 (type 5) are on 4110/4108; unit 0 (type 0) on 3847;
- player 0's discovery grid is ``[0x507d78]`` and its illumination grid ``[0x507d88]`` (bit 0x10 set =
  not discovered / not lit); the packet record of player 0 is ``[0x4e2458]``.

A case adds only declared byte writes, argument registers, pushed words and, for GetAsyncKeyState, the
ordered declared answers ``keys`` [(vkey, i16 result), ...] (no entry = every frame-phase call answers 0, the
bench's no-input answer). The InputGame cases declare the M3 view (0, 0) of frame 128 (M3_ALVOS) and every
input flag explicitly. Writes that build a selection list set both the list and each unit's +0xbd flag, the
invariant the game maintains. Importing this module executes nothing.
"""
import struct

PASSO = 276
UNIDADES = 0x474a8000            # [0x4e19a0] at the pause (checked by the capture)
PACOTE = 0x4797f000              # [0x4e2458] at the pause: player 0's 10-byte input packet (checked)
SELECOES = 0x508728
ESTRUTURAS = 0x49a0c8
JANELA = 0x508720
CURSOR = 0x5099a8
FLAGS = 0x5099ae                 # ae (left down), af (left up), b0 (double click), b1 (right down), b2 (right up)
PAGINA, MODO_ACAO, ARRASTO = 0x4e05ae, 0x496207, 0x4e19b0
DESCOBERTA_0, ILUMINACAO_0, OBJETOS = 0x507d78, 0x507d88, 0x507d74


def u8(v):
    return bytes([v & 0xff])


def u16(v):
    return struct.pack('<H', v & 0xffff)


def u32(v):
    return struct.pack('<I', v & 0xffffffff)


def campo(unidade, offset, dados):
    return (UNIDADES + unidade * PASSO + offset, dados)


def lista(jogador, unidades):
    """Selection list of ``jogador`` = ``unidades``, +0xbd = 1 on each."""
    return ([(SELECOES + 0x200 * jogador, u16(len(unidades)) + b''.join(u16(x) for x in unidades))] +
            [campo(x, 0xbd, u8(1)) for x in unidades])


def celula(x, y):
    return (y << 8) | x


def caso(nome, rotina, writes=(), stack=(), ret_imm=0, keys=(), **regs):
    return dict(case=nome, routine=rotina, registers=regs, writes=list(writes), stack=list(stack), ret_imm=ret_imm,
                keys=[list(k) for k in keys])


def entrada(x, y, ae=0, af=0, b0=0, b1=0, b2=0, vista=(0, 0), pagina=0, modo=0xff, arrasto=None):
    """The declared input state of one InputGame pass: cursor, the five WndProc flags, view, help page, action
    mode and (optionally) the drag state (flag, anchor cell words 0x4e19b2/b4, box words 0x49a024..2a)."""
    w = [(CURSOR, u16(x) + u16(y)), (FLAGS, bytes([ae, af, b0, b1, b2])), (JANELA, u16(vista[0]) + u16(vista[1])),
         (PAGINA, u16(pagina)), (MODO_ACAO, u8(modo))]
    if arrasto is not None:
        c, (bx, by) = arrasto
        w += [(ARRASTO, u8(1)), (0x4e19b2, u16(c) + u16(c)), (0x49a024, u16(bx) + u16(by) + u16(bx + 1) + u16(by + 1))]
    return w


def pacote(etiqueta, *palavras):
    p = [etiqueta] + list(palavras) + [0] * (4 - len(palavras))
    return [(PACOTE, b''.join(u16(v) for v in p))]


ORDEM_TECLAS = (0x1b, 0x10, 0x11, 0x2e, 0x12, 0x20, 0x26, 0x28, 0x27, 0x25, 0x0d, 0x58)


def teclas(*pressionadas):
    """The ordered GetAsyncKeyState answers of one InputGame pass with ``pressionadas`` held (-0x8000) and every
    other key up. An up-arrow press skips the down-arrow query and a right-arrow press the left one (InputGame
    0x4296f4/0x429735); 0x45 ('E') is queried only with troops selected over a non-structure cell (0x42a762)."""
    saida = []
    for vk in ORDEM_TECLAS:
        if (vk == 0x28 and 0x26 in pressionadas) or (vk == 0x25 and 0x27 in pressionadas):
            continue
        saida.append((vk, -0x8000 if vk in pressionadas else 0))
    if 0x45 in pressionadas:
        saida.append((0x45, -0x8000))
    return saida


def casos(grades):
    """The declared matrix; ``grades`` = {'descoberta': player 0's discovery grid, 'iluminacao': its
    illumination grid, 'objetos': the object grid} at the pause."""
    d0, il0, ob = grades['descoberta'], grades['iluminacao'], grades['objetos']
    descobrir = lambda c: [(d0 + c, u8(0)), (il0 + c, u8(0))]            # noqa: E731
    encobrir = lambda c: [(d0 + c, u8(0x1f)), (il0 + c, u8(0x1f))]       # noqa: E731
    u12, u13, sitio, livre = celula(17, 16), celula(14, 16), celula(21, 12), celula(19, 14)
    campo_comida, mina = celula(26, 32), celula(43, 8)
    so12, so13 = lista(0, [12]), lista(0, [13])
    c = []
    # ---------------------------------------------------------------- small leaves
    c += [caso(f'mousezone_{n}', 'MouseZone', [(CURSOR, u16(x) + u16(y))])
          for n, (x, y) in (('map', (560, 528)), ('hud', (180, 573)), ('minimap', (46, 49)), ('edge_origin', (0, 0)),
                            ('edge_right', (799, 300)), ('minimap_corner', (128, 128)), ('outside', (900, 700)))]
    c += [caso(f'mouse_moved_{n}', 'MouseEstDeplacer', [(CURSOR, u16(x) + u16(y)), (0x49a042, u16(ax) + u16(ay))])
          for n, (x, y, ax, ay) in (('still', (400, 300, 400, 300)), ('x_far', (420, 300, 400, 300)),
                                    ('x_left_far', (380, 300, 400, 300)), ('y_far', (400, 289, 400, 300)),
                                    ('within', (409, 309, 400, 300)))]
    c += [caso('key_pressed_down', 'KeyPressed', keys=[(0x26, -0x8000)], EAX=0x26),
          caso('key_pressed_up', 'KeyPressed', keys=[(0x26, 0)], EAX=0x26),
          caso('key_pressed_transition_only', 'KeyPressed', keys=[(0x41, 1)], EAX=0x41),
          caso('key_unpressed_released', 'KeyUnPressed', [(0x4e0630 + 0x26, u8(1))], keys=[(0x26, 0)], EAX=0x26),
          caso('key_unpressed_held', 'KeyUnPressed', [(0x4e0630 + 0x26, u8(1))], keys=[(0x26, -0x8000)], EAX=0x26),
          caso('key_unpressed_not_latched', 'KeyUnPressed', EAX=0x26),
          caso('key_test_release', 'KeyTestRelease', keys=[(0x1b, -0x8000), (0x1b, -0x7fff), (0x1b, 0)], EAX=0x1b)]
    c += [caso(f'icon_zone_{n}', 'IconeGetZone', EAX=x, EDX=y)
          for n, (x, y) in (('slot0', (60, 573)), ('slot2_cave', (180, 573)), ('slot3', (240, 573)),
                            ('gap', (150, 573)), ('scroll8', (20, 573)), ('scroll9', (280, 573)),
                            ('above', (180, 540)), ('slot4_none', (300, 573)))]
    c += [caso('icon_zone_width640', 'IconeGetZone', [(0x49a018, u16(640))], EAX=180, EDX=430)]
    c += [caso('bag_code_u12_slot2', 'BagGetCode', EAX=0x4781c2d8, EDX=2),
          caso('bag_type_u12_slot2', 'BagGetType', EAX=0x4781c2d8, EDX=2),
          caso('bag_order_u12', 'EnginGetBagOrdre', EAX=12),
          caso('bag_order_u13', 'EnginGetBagOrdre', EAX=13)]
    c += [caso('grab_all_input', 'GrabAllInput'),
          caso('init_input_player', 'InitInputPlayer')]
    c += [caso('minimap_case', 'MiniMapGetCase', EAX=53, EDX=64),
          caso('minimap_center', 'MiniMapGetCenterSelect', EAX=46, EDX=49, EBX=0x508720, ECX=0x508722),
          caso('minimap_center_clamped', 'MiniMapGetCenterSelect', EAX=127, EDX=127, EBX=0x508720, ECX=0x508722)]
    c += [caso(f'wndproc_{n}', 'WndProc', stack=[0x1234, m, w, lp], ret_imm=0x10)
          for n, (m, w, lp) in (('mousemove', (0x200, 0, (528 << 16) | 560)), ('ldown', (0x201, 1, (528 << 16) | 560)),
                                ('lup', (0x202, 0, (528 << 16) | 560)), ('ldbl_map', (0x203, 1, (300 << 16) | 400)),
                                ('ldbl_hud', (0x203, 1, (570 << 16) | 400)), ('rdown', (0x204, 2, 0)),
                                ('rup', (0x205, 0, 0)))]
    # ---------------------------------------------------------------- packet producer and dispatcher
    c += [caso('set_order_tag1', 'SetPlayerOrdre', stack=[0, 0], ret_imm=8, EAX=0, EDX=1, EBX=u12, ECX=u12),
          caso('set_order_tag4', 'SetPlayerOrdre', stack=[0, 0], ret_imm=8, EAX=0, EDX=4, EBX=3, ECX=sitio),
          caso('set_order_upper_bits', 'SetPlayerOrdre', stack=[0x12345678, 0x9abcdef0], ret_imm=8,
               EAX=0xffffff00, EDX=0x55550005, EBX=0x7777abcd, ECX=0x8888ef01)]
    pig = lambda nome, escritas: caso(nome, 'ProcessInputGame', escritas, EAX=0)   # noqa: E731
    c += [pig('process_tag0_clear', pacote(0, 1, 2, 3, 4)),
          pig('process_tag40_clear', pacote(0x28, 1, 2, 3, 4)),
          pig('process_tag1_select', pacote(1, u12, u12)),
          pig('process_tag1_replaces', so13 + pacote(1, u12, u12)),
          pig('process_tag2_structure', pacote(2, 0)),
          pig('process_tag3_deselect', so12 + pacote(3)),
          pig('process_tag4_build_cave', so12 + pacote(4, 3, sitio)),
          pig('process_tag5_move', so12 + pacote(5, livre)),
          pig('process_tag6_mine', so12 + pacote(6, mina)),
          pig('process_tag7_harvest', so13 + pacote(7, campo_comida)),
          pig('process_tag8_transport', so13 + pacote(8)),
          pig('process_tag14_attack_unit', lista(0, [0]) + pacote(14, 1, 12)),
          pig('process_tag14_structure_selected', [(0x495be0, u16(0))] + pacote(14, 1, 12)),
          pig('process_tag17_recruit', [(0x495be0, u16(0))] + pacote(17, 0)),
          pig('process_tag18_pickup', so13 + pacote(18, celula(20, 16))),
          pig('process_tag19_unload', so13 + pacote(19, 0)),
          pig('process_tag36_add', so13 + pacote(36, 12)),
          caso('process_player1_clear', 'ProcessInputGame', [(0x47980000, u16(0x28) + u16(1) + u16(2) + u16(3) +
                                                              u16(4))], EAX=1)]
    # ---------------------------------------------------------------- the action-icon pass of CalculGame
    c += [caso('icon_action_none', 'CalculIconeAction'),
          caso('icon_action_builder', 'CalculIconeAction', so12),
          caso('icon_action_harvester', 'CalculIconeAction', so13),
          caso('icon_action_two_units', 'CalculIconeAction', lista(0, [12, 13])),
          caso('icon_action_structure', 'CalculIconeAction', [(0x495be0, u16(0))])]
    # ---------------------------------------------------------------- InputGame passes (AL = player 0)
    ig = lambda nome, escritas, **k: caso(nome, 'InputGame', escritas, EAX=0, **k)   # noqa: E731
    p12 = (560, 528)
    c += [
        # P1: hover, press (drag start), hold, release (selection, tag 1), then hover with the unit selected
        ig('p1_hover_unit12', entrada(*p12)),
        ig('p1_press_unit12', entrada(*p12, ae=1)),
        ig('p1_hold_unit12', entrada(*p12, ae=1, arrasto=(u12, p12))),
        ig('p1_release_unit12', entrada(*p12, ae=1, af=1, arrasto=(u12, p12))),
        ig('p1_hover_unit12_selected', so12 + entrada(*p12)),
        ig('p1_press_unit12_selected', so12 + entrada(*p12, ae=1)),
        ig('p1_hover_terrain_selected', so12 + entrada(624, 464)),
        ig('p1_hover_terrain', entrada(624, 464)),
        ig('p1_press_empty_terrain', entrada(624, 464, ae=1)),
        ig('p1_release_empty_box', entrada(624, 464, ae=1, af=1, arrasto=(livre, (624, 464)))),
        ig('p1_hover_unit13', entrada(464, 528)),
        ig('p1_hover_sanctuary', entrada(464, 400)),
        ig('p1_dblclick_selected_unit', so12 + entrada(*p12, b0=1)),
        # P3: the CAVE icon, then the site
        ig('p3_hover_icon_cave', so12 + entrada(180, 573)),
        ig('p3_press_icon_cave', so12 + entrada(180, 573, ae=1)),
        ig('p3_release_icon_cave', so12 + entrada(180, 573, ae=1, af=1)),
        ig('p3_release_icon_cave_poor', so12 + entrada(180, 573, ae=1, af=1) +
           [(0x4e2ea8 + 8 + 2, u16(0))]),
        ig('p3_release_icon_slot0', so12 + entrada(60, 573, ae=1, af=1)),
        ig('p3_release_icon_gap', so12 + entrada(150, 573, ae=1, af=1)),
        ig('p3_release_icon_two_units', lista(0, [12, 13]) + entrada(180, 573, ae=1, af=1)),
        ig('p3_hover_hud_nothing', entrada(400, 580)),
        ig('p3_hover_site', so12 + entrada(688, 400, pagina=3, modo=3)),
        ig('p3_press_site', so12 + entrada(688, 400, ae=1, pagina=3, modo=3)),
        ig('p3_release_site', so12 + entrada(688, 400, ae=1, af=1, pagina=3, modo=3)),
        ig('p3_release_site_on_builder', so12 + entrada(*p12, ae=1, af=1, pagina=3, modo=3)),
        ig('p3_release_site_unit13', so13 + entrada(688, 400, ae=1, af=1, pagina=3, modo=3)),
        # P2: move orders (playfield, undiscovered cell, minimap)
        ig('p2_release_terrain_move', so12 + entrada(624, 464, ae=1, af=1)),
        ig('p2_press_terrain_move', so12 + entrada(624, 464, ae=1)),
        ig('p2_release_undiscovered', so12 + entrada(624, 464, ae=1, af=1) + encobrir(livre)),
        ig('p2_hover_undiscovered', so12 + entrada(624, 464) + encobrir(livre)),
        ig('p2_hover_undiscovered_nothing', entrada(624, 464) + encobrir(livre)),
        ig('p2_release_undiscovered_no_mode', so12 + entrada(624, 464, ae=1, af=1) + encobrir(livre) +
           [(0x496208, u8(0))]),
        ig('p2_minimap_recentre', entrada(46, 49, ae=1)),
        ig('p2_minimap_move', so12 + entrada(53, 64, ae=1)),
        ig('p2_minimap_hover', so12 + entrada(53, 64)),
        ig('p2_minimap_right', entrada(46, 49, b1=1)),
        ig('p2_minimap_right_held', entrada(60, 40, b1=1) + [(0x4e05a8, u8(1)), (0x507d6c, u16(3) + u16(4))]),
        # right button: deselect outside the HUD, kept on the HUD
        ig('rb_deselect_map', so12 + entrada(300, 300, b1=1)),
        ig('rb_hud_keeps', so12 + entrada(400, 580, b1=1)),
        ig('rb_deselect_page3', so12 + entrada(688, 400, b1=1, pagina=3, modo=3)),
        # P4/P5: harvest and mine presses on revealed targets (view moved, target cell declared discovered)
        ig('p4_release_field_u13', so13 + entrada(528, 528, ae=1, af=1, vista=(10, 16)) + descobrir(campo_comida)),
        ig('p4_hover_field_u13', so13 + entrada(528, 528, vista=(10, 16)) + descobrir(campo_comida)),
        ig('p4_release_field_builder', so12 + entrada(528, 528, ae=1, af=1, vista=(10, 16)) +
           descobrir(campo_comida)),
        ig('p5_release_mine_u12', so12 + entrada(400, 272, ae=1, af=1, vista=(31, 0)) + descobrir(mina)),
        ig('p5_hover_mine_u12', so12 + entrada(400, 272, vista=(31, 0)) + descobrir(mina)),
        ig('p5_release_mine_u13', so13 + entrada(400, 272, ae=1, af=1, vista=(31, 0)) + descobrir(mina)),
        # edges and keys
        ig('edge_scroll_origin', entrada(0, 0, vista=(3, 5))),
        ig('edge_scroll_right', entrada(799, 300, vista=(3, 5))),
        ig('edge_scroll_right_pressed', entrada(799, 300, ae=1, vista=(3, 5))),
        # K1-style keys: every GetAsyncKeyState call of the pass is declared, in order
        ig('key_arrow_up', entrada(400, 300, vista=(3, 5)), keys=teclas(0x26)),
        ig('key_arrow_down_left', entrada(400, 300, vista=(3, 5)), keys=teclas(0x28, 0x25)),
        ig('key_arrow_right', entrada(400, 300, vista=(3, 5)), keys=teclas(0x27)),
        ig('key_space', entrada(400, 300, vista=(3, 5)), keys=teclas(0x20)),
        ig('key_e_with_troops', so12 + entrada(624, 464), keys=teclas(0x45)),
    ]
    nomes = [x['case'] for x in c]
    if len(nomes) != len(set(nomes)):
        raise ValueError('Duplicate case names')
    return c
