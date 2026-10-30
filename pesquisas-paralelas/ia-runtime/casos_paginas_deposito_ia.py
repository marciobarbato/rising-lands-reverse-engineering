"""Declared case matrix for M3.1 round 3: InputGame's Ctrl deposit mode (0x429601), help pages 9 (deposit
target, table 0x42923c), 0xc (Shift: add to group), 0xb (engineer target), 2 (Alt: forced attack) and 7
(Delete: sell), page 8 over a field or mine (0x42b393/0x42b525), the structure under the cursor with troops
selected (0x42ac32, the tag-16/20/21/14 producer) and their selection/structure leaves.

Every case starts from the same paused frame-1 state as ``casos_entrada_ordens_ia`` (Core's
``bancada_selecao_ordens``, MONDE01 display reference, first ProcessInputGame entry); the facts of that state are
listed there. Further facts used here (read at the pause): structure 0 is player 0's built sanctuary (type 2,
origin 2828, under the cursor at cell (14, 12) = 3084 with view (0, 0)); structure records 1.. are free; units 0, 1,
2 are player 0's type-0 soldiers, 11 is type 1, 15 is type 8 (engineer), 12 is the builder (type 7), 13/14 are
colonists (type 5); every unit has its full hit points. Pointers read at the pause and handed to ``casos``:
player 0's discovery and illumination grids, the object grid, the structure-at-cell grid ``[0x4e0f38]`` (u16 per
cell: bit 15 set, structure index in bits 5..14) and the player table ``[0x5080a8]`` (PlayerEstAllie reads the
byte +20 * owner + 6, bit = player).

Declared structure ``estrutura1`` (record 1, free at the pause) is placed under the cursor at cell (19, 14) by
writing its record and that cell's grid word (bit 15 | 1 << 5); the cell is declared discovered and lit. The type
limits (u16 +4 of 0x495d8c + 52 * type) are read at the pause (``limites``) so "built" is exact.

A case adds only declared byte writes, argument registers and ordered GetAsyncKeyState answers. The InputGame
passes declare the cursor, the five WndProc flags, the view, help page, action-mode byte and, where used, the
deposit words 0x4e05b0 (table index), 0x4e05b2 (first target cell) and byte 0x4e05b4 (cargo kind) and the
engineer mode byte 0x496209. Importing this module executes nothing.
"""
import struct

from casos_entrada_ordens_ia import (PACOTE, UNIDADES, caso, celula, entrada, lista, teclas, u8, u16)

PASSO = 276
ESTRUTURAS = 0x49a0c8
TIPOS_ESTRUTURA = 0x495d8c           # stride 52; u16 +4 = construction limit
DEPOSITO_MODO, DEPOSITO_CELULA, DEPOSITO_CARGA = 0x4e05b0, 0x4e05b2, 0x4e05b4
MODO_9 = 0x496209
SEL_ESTRUTURA = 0x495be0
TIPOS_LIMITE = (2, 3, 4, 7, 0xe, 0x10, 0x11, 0x13, 0x15)
SANTUARIO = celula(14, 12)
SITIO = celula(19, 14)               # structure 1's declared cell (free terrain at the pause)
CURSOR_SANTUARIO, CURSOR_SITIO = (464, 400), (624, 464)
CAMPO, MINA = celula(26, 32), celula(43, 8)


def unidade(u, offset, dados):
    return (UNIDADES + u * PASSO + offset, dados)


def estrutura(s, offset, dados):
    return (ESTRUTURAS + s * PASSO + offset, dados)


def limites_da_memoria(ler):
    """{type: construction limit} for ``TIPOS_LIMITE`` from ``ler(address, n) -> bytes`` at the pause."""
    return {t: struct.unpack('<H', ler(TIPOS_ESTRUTURA + 52 * t + 4, 2))[0] for t in TIPOS_LIMITE}


def casos(grades, limites):
    """The declared matrix. ``grades``: 'descoberta', 'iluminacao', 'objetos', 'estruturas' (the grid pointers) and
    'jogadores' (``[0x5080a8]``); ``limites``: ``limites_da_memoria``."""
    d0, il0, gb, jog = grades['descoberta'], grades['iluminacao'], grades['estruturas'], grades['jogadores']
    descobrir = lambda c: [(d0 + c, u8(0)), (il0 + c, u8(0))]            # noqa: E731

    def estrutura1(tipo=3, dono=0, construida=True, progresso=10, dano=0, f74=0, estado=None):
        """Structure record 1 at ``SITIO`` (grid word, record, cell lit)."""
        prog = limites[tipo] if construida else progresso
        st = estado if estado is not None else (5 if construida else 2)
        return ([estrutura(1, 5, u8(st)), estrutura(1, 4, u8(dono)), estrutura(1, 2, u16(SITIO)),
                 estrutura(1, 8, u8(tipo)), estrutura(1, 0xa, u16(prog)), estrutura(1, 6, u16(dano)),
                 estrutura(1, 0x74, u8(f74)), estrutura(1, 0x100, struct.pack('<I', 0xffffffff)),
                 (gb + 2 * SITIO, u16(0x8000 | (1 << 5)))] + descobrir(SITIO))

    def deposito(modo, celula_=CAMPO, carga=1):
        return [(DEPOSITO_MODO, u16(modo)), (DEPOSITO_CELULA, u16(celula_)), (DEPOSITO_CARGA, u8(carga))]

    so0, so12, so13, so15 = lista(0, [0]), lista(0, [12]), lista(0, [13]), lista(0, [15])
    ctrl, shift, alt, delete = teclas(0x11), teclas(0x10), teclas(0x12), teclas(0x2e)
    sitio = lambda **k: entrada(*CURSOR_SITIO, **k)              # noqa: E731
    santuario = lambda **k: entrada(*CURSOR_SANTUARIO, **k)      # noqa: E731
    campo = lambda **k: entrada(528, 528, vista=(10, 16), **k) + descobrir(CAMPO)   # noqa: E731
    mina = lambda **k: entrada(400, 272, vista=(31, 0), **k) + descobrir(MINA)      # noqa: E731
    tipo14 = lambda t: [unidade(14, 1, u8(t))]                   # noqa: E731
    so14 = lista(0, [14])
    c = []
    # ---------------------------------------------------------------- selection leaves (AL = player 0)
    sel = lambda nome, rotina, escritas=(), **r: caso(nome, rotina, escritas, **dict(dict(EAX=0), **r))  # noqa: E731
    for rotina, curto in (('EnginSelectPeuventTransporter', 'transport'), ('EnginSelectEstTroupe', 'troop'),
                          ('EnginSelectEstEngin', 'engin'), ('EnginSelectContientMiroir', 'mirror'),
                          ('EnginSelectEstBlesse', 'wounded')):
        c += [sel(f'{curto}_none', rotina), sel(f'{curto}_u13', rotina, so13), sel(f'{curto}_u12', rotina, so12),
              sel(f'{curto}_u0', rotina, so0), sel(f'{curto}_u13_u0', rotina, lista(0, [13, 0])),
              sel(f'{curto}_u0_u13', rotina, lista(0, [0, 13])),
              sel(f'{curto}_u14_type11', rotina, so14 + tipo14(0xb)),
              sel(f'{curto}_u14_type11_u13', rotina, lista(0, [14, 13]) + tipo14(0xb)),
              sel(f'{curto}_u13_dead_u0', rotina, lista(0, [13, 0]) + [unidade(13, 2, u8(4))])]
    c += [sel('mirror_u13_mirror', 'EnginSelectContientMiroir', so13 + [unidade(13, 0xdc, u8(4))]),
          sel('mirror_u13_mirror_dead', 'EnginSelectContientMiroir', so13 + [unidade(13, 0xdc, u8(4)),
                                                                          unidade(13, 2, u8(0))]),
          sel('wounded_u13_hp50', 'EnginSelectEstBlesse', so13 + [unidade(13, 0x9a, u16(50))]),
          sel('wounded_u13_u0_hp50', 'EnginSelectEstBlesse', lista(0, [13, 0]) + [unidade(0, 0x9a, u16(0x150))]),
          sel('wounded_u13_hp50_dead', 'EnginSelectEstBlesse', so13 + [unidade(13, 0x9a, u16(50)),
                                                                     unidade(13, 2, u8(4))]),
          sel('transport_u14_type6_u12', 'EnginSelectPeuventTransporter', lista(0, [14, 12]) + tipo14(6)),
          sel('transport_u14_type13', 'EnginSelectPeuventTransporter', so14 + tipo14(0xd)),
          sel('transport_player1_empty', 'EnginSelectPeuventTransporter', EAX=1)]
    # EnginSelectPeutDeposer (AL player, DX structure)
    dep = lambda nome, escritas, s=1: sel(nome, 'EnginSelectPeutDeposer', escritas, EDX=s)   # noqa: E731
    c += [dep('deposit_sanctuary_u13', so13, s=0),
          dep('deposit_cave_u13', so13 + estrutura1()), dep('deposit_cave_u12', so12 + estrutura1()),
          dep('deposit_cave_u0', so0 + estrutura1()), dep('deposit_cave_none', estrutura1()),
          dep('deposit_cave_u13_u0', lista(0, [13, 0]) + estrutura1()),
          dep('deposit_cave_u13_dead_u0', lista(0, [13, 0]) + [unidade(0, 2, u8(0))] + estrutura1()),
          dep('deposit_type4_u13', so13 + estrutura1(tipo=4)), dep('deposit_type4_u12', so12 + estrutura1(tipo=4)),
          dep('deposit_type4_none', estrutura1(tipo=4)),
          dep('deposit_type7_u13', so13 + estrutura1(tipo=7)),
          dep('deposit_cave_type6_type13', lista(0, [14, 13]) + tipo14(6) + estrutura1())]
    # EnginSelectPeutAttaquer (AL player, DL mode, BX target)
    att = lambda nome, escritas, modo, alvo: sel(nome, 'EnginSelectPeutAttaquer', escritas, EDX=modo,  # noqa: E731
                                                 EBX=alvo)
    c += [att('attack_mode5', so13, 5, SITIO), att('attack_mode1_none', [], 1, 13),
          att('attack_mode1_u0_on_u13', so0, 1, 13), att('attack_mode1_u13_on_u0', so13, 1, 0),
          att('attack_mode1_target17', so0 + [unidade(14, 1, u8(0x11))], 1, 14),
          att('attack_mode1_target10', so0 + [unidade(14, 1, u8(0xa))], 1, 14),
          att('attack_mode1_u15_on_type16', so15 + [unidade(14, 1, u8(0x10))], 1, 14),
          att('attack_mode1_u11_on_type16', lista(0, [11]) + [unidade(14, 1, u8(0x10))], 1, 14),
          att('attack_mode1_u0_on_type16', so0 + [unidade(14, 1, u8(0x10))], 1, 14),
          att('attack_mode3_u0', so0, 3, 0), att('attack_mode3_u13', so13, 3, 0),
          att('attack_mode3_u0_dead_u13', lista(0, [13, 0]) + [unidade(13, 2, u8(0))], 3, 0),
          att('attack_mode3_bomber_empty', so14 + tipo14(0x10) + [unidade(14, 0xda, u8(0))], 3, 0),
          att('attack_mode3_bomber_loaded', so14 + tipo14(0x10) + [unidade(14, 0xda, u8(3))], 3, 0),
          att('attack_mode3_bomber14_empty', so14 + tipo14(0xe) + [unidade(14, 0xda, u8(0))], 3, 0),
          att('attack_mode0_u0', so0, 0, 0)]
    c += [sel(f'attack_mode3_type{t:x}', 'EnginSelectPeutAttaquer', so14 + tipo14(t), EDX=3, EBX=0)
          for t in (0x11, 0x12, 0x13, 0xd, 0x19, 0x1a)]
    # structure leaves
    est = lambda nome, rotina, escritas=(), **r: caso(nome, rotina, escritas, **r)   # noqa: E731
    c += [est('depot_sanctuary', 'BatimentEstDepot', EAX=0), est('depot_cave', 'BatimentEstDepot', estrutura1(), EAX=1),
          est('depot_type4', 'BatimentEstDepot', estrutura1(tipo=4), EAX=0xabcd0001),
          est('depot_type7', 'BatimentEstDepot', estrutura1(tipo=7), EAX=1),
          est('neutral_sanctuary', 'BatimentEstNeutre', EAX=0x12340000),
          est('neutral_c8', 'BatimentEstNeutre', estrutura1(dono=0xc8), EAX=1),
          est('enemy_own', 'BatimentEstEnnemi', EAX=0, EDX=0),
          est('enemy_c8', 'BatimentEstEnnemi', estrutura1(dono=0xc8), EAX=1, EDX=0),
          est('enemy_owner1', 'BatimentEstEnnemi', estrutura1(dono=1), EAX=1, EDX=0),
          est('enemy_owner1_allied', 'BatimentEstEnnemi', estrutura1(dono=1) + [(jog + 26, u8(1))], EAX=1, EDX=0),
          est('enemy_owner1_allied_other_bit', 'BatimentEstEnnemi', estrutura1(dono=1) + [(jog + 26, u8(2))],
              EAX=1, EDX=0),
          est('enemy_owner5', 'BatimentEstEnnemi', estrutura1(dono=5), EAX=1, EDX=0),
          est('enemy_player5', 'BatimentEstEnnemi', EAX=0, EDX=5),
          est('sell_sanctuary', 'BatimentPeutSeVendre', EAX=0),
          est('sell_type17', 'BatimentPeutSeVendre', estrutura1(tipo=0x11), EAX=1),
          est('sell_flag74', 'BatimentPeutSeVendre', estrutura1(f74=1), EAX=1),
          est('find_structure_sanctuary', 'ChercheIndiceBatiment', EAX=0xffff0000 | SANTUARIO),
          est('find_structure_terrain', 'ChercheIndiceBatiment', EAX=SITIO),
          est('find_structure_declared', 'ChercheIndiceBatiment', estrutura1(), EAX=SITIO),
          est('allied_same', 'PlayerEstAllie', EAX=0x1203, EDX=3),
          est('allied_1_0', 'PlayerEstAllie', EAX=1, EDX=0),
          est('allied_1_0_set', 'PlayerEstAllie', [(jog + 26, u8(1))], EAX=1, EDX=0),
          est('allied_5_0', 'PlayerEstAllie', EAX=5, EDX=0), est('allied_0_5', 'PlayerEstAllie', EAX=0, EDX=5)]
    # ---------------------------------------------------------------- InputGame passes (AL = player 0)
    ig = lambda nome, escritas, **k: caso(nome, 'InputGame', escritas, EAX=0, **k)   # noqa: E731
    # Ctrl: deposit mode 8 when every selected unit can carry, mode 9 kept or cleared
    c += [ig('ctrl_carrier_terrain', so13 + sitio(), keys=ctrl),
          ig('ctrl_soldier_terrain', so0 + sitio(), keys=ctrl),
          ig('ctrl_nothing_terrain', sitio(), keys=ctrl),
          ig('ctrl_mixed_terrain', lista(0, [13, 0]) + sitio(), keys=ctrl),
          ig('ctrl_page9_kept', so13 + sitio(pagina=9) + deposito(1), keys=ctrl),
          ig('ctrl_page9_soldier_cleared', so0 + sitio(pagina=9) + deposito(1), keys=ctrl),
          ig('ctrl_page9_nothing_cleared', sitio(pagina=9) + deposito(1), keys=ctrl),
          ig('noctrl_page9_cleared', so13 + sitio(pagina=9) + deposito(1)),
          ig('noctrl_page8_cleared', so13 + sitio(pagina=8))]
    # page 8 over a field or a mine (0x42b393 / 0x42b525)
    c += [ig('page8_field_hover_u13', so13 + campo(), keys=ctrl),
          ig('page8_field_press_u13', so13 + campo(ae=1), keys=ctrl),
          ig('page8_field_release_u13', so13 + campo(ae=1, af=1), keys=ctrl),
          ig('page8_field_release_u12', so12 + campo(ae=1, af=1), keys=ctrl),
          ig('page8_mine_hover_u12', so12 + mina(), keys=ctrl),
          ig('page8_mine_release_u12', so12 + mina(ae=1, af=1), keys=ctrl),
          ig('page8_mine_release_u13', so13 + mina(ae=1, af=1), keys=ctrl)]
    # page 9: the deposit target (table 0x42923c by 0x4e05b0)
    c += [ig(f'page9_terrain_release_mode{k}', so13 + sitio(ae=1, af=1, pagina=9) + deposito(k), keys=ctrl)
          for k in range(5)]
    c += [ig('page9_terrain_hover', so13 + sitio(pagina=9) + deposito(1), keys=ctrl),
          ig('page9_terrain_af_only', so13 + sitio(af=1, pagina=9) + deposito(1), keys=ctrl),
          ig('page9_terrain_press', so13 + sitio(ae=1, pagina=9) + deposito(1), keys=ctrl),
          ig('page9_cave_hover', so13 + sitio(pagina=9) + deposito(1) + estrutura1(), keys=ctrl),
          ig('page9_cave_release_mode1', so13 + sitio(ae=1, af=1, pagina=9) + deposito(1) + estrutura1(), keys=ctrl),
          ig('page9_cave_release_mode3', so13 + sitio(ae=1, af=1, pagina=9) + deposito(3, 1, 1) + estrutura1(),
             keys=ctrl),
          ig('page9_cave_release_mode0_u12', so12 + sitio(ae=1, af=1, pagina=9) + deposito(0, MINA, 2) +
             estrutura1(), keys=ctrl),
          ig('page9_sanctuary_release', so13 + santuario(ae=1, af=1, pagina=9) + deposito(1), keys=ctrl),
          ig('page9_enemy_cave_release', so13 + sitio(ae=1, af=1, pagina=9) + deposito(1) + estrutura1(dono=1),
             keys=ctrl),
          ig('page9_type4_release_u13', so13 + sitio(ae=1, af=1, pagina=9) + deposito(1) + estrutura1(tipo=4),
             keys=ctrl),
          ig('page9_type4_release_u12', so12 + sitio(ae=1, af=1, pagina=9) + deposito(0, MINA, 2) +
             estrutura1(tipo=4), keys=ctrl)]
    # page 8 over a structure (0x42ac32 with page 8)
    c += [ig('page8_cave_hover_u13', so13 + sitio() + estrutura1(), keys=ctrl),
          ig('page8_cave_release_u13', so13 + sitio(ae=1, af=1) + estrutura1(), keys=ctrl),
          ig('page8_cave_release_u12', so12 + sitio(ae=1, af=1) + estrutura1(), keys=ctrl),
          ig('page8_cave_release_type6', so14 + tipo14(6) + sitio(ae=1, af=1) + estrutura1(), keys=ctrl),
          ig('page8_sanctuary_hover_u13', so13 + santuario(), keys=ctrl),
          ig('page8_sanctuary_release_u13', so13 + santuario(ae=1, af=1), keys=ctrl),
          ig('page8_enemy_cave_release_u13', so13 + sitio(ae=1, af=1) + estrutura1(dono=1), keys=ctrl)]
    # the structure under the cursor with troops selected (0x42adab..0x42b23b), page 0
    c += [ig('troops_own_cave_hover_u13', so13 + sitio() + estrutura1()),
          ig('troops_own_cave_release_u13', so13 + sitio(ae=1, af=1) + estrutura1()),
          ig('troops_own_cave_unbuilt_release_u13', so13 + sitio(ae=1, af=1) + estrutura1(construida=False)),
          ig('troops_sanctuary_release_u13', so13 + santuario(ae=1, af=1)),
          ig('troops_builder_unbuilt_release', so12 + sitio(ae=1, af=1) + estrutura1(construida=False)),
          ig('troops_builder_damaged_hover', so12 + sitio() + estrutura1(dano=5)),
          ig('troops_builder_damaged_release', so12 + sitio(ae=1, af=1) + estrutura1(dano=5)),
          ig('troops_builder_built_release', so12 + sitio(ae=1, af=1) + estrutura1()),
          ig('troops_wounded_hospital_release', so0 + [unidade(0, 0x9a, u16(50))] + sitio(ae=1, af=1) +
             estrutura1(tipo=0x13)),
          ig('troops_wounded_hospital_unbuilt', so0 + [unidade(0, 0x9a, u16(50))] + sitio(ae=1, af=1) +
             estrutura1(tipo=0x13, construida=False)),
          ig('troops_wounded_hospital_mirror', so0 + [unidade(0, 0x9a, u16(50)), unidade(0, 0xdc, u8(4))] +
             sitio(ae=1, af=1) + estrutura1(tipo=0x13)),
          ig('troops_wounded_engin_garage', so14 + tipo14(0xb) + [unidade(14, 0x9a, u16(50))] +
             sitio(ae=1, af=1) + estrutura1(tipo=0xe)),
          ig('troops_wounded_soldier_cave', so0 + [unidade(0, 0x9a, u16(50))] + sitio(ae=1, af=1) + estrutura1()),
          ig('troops_enemy_cave_soldier_release', so0 + sitio(ae=1, af=1) + estrutura1(dono=1)),
          ig('troops_enemy_cave_soldier_hover', so0 + sitio() + estrutura1(dono=1)),
          ig('troops_enemy_cave_colonist', so13 + sitio(ae=1, af=1) + estrutura1(dono=1)),
          ig('troops_allied_cave_soldier', so0 + sitio(ae=1, af=1) + estrutura1(dono=1) + [(jog + 26, u8(1))]),
          ig('troops_neutral_cave_u13', so13 + sitio(ae=1, af=1) + estrutura1(dono=0xc8)),
          ig('troops_enemy_sanctuary_type10', so14 + tipo14(0xa) + sitio(ae=1, af=1) + estrutura1(tipo=2, dono=1)),
          ig('troops_enemy_type16_type10_hover', so14 + tipo14(0xa) + sitio() + estrutura1(tipo=0x10, dono=1)),
          ig('troops_enemy_sanctuary_soldier', so0 + sitio(ae=1, af=1) + estrutura1(tipo=2, dono=1)),
          ig('troops_enemy_cave_bomber_empty', so14 + tipo14(0x10) + [unidade(14, 0xda, u8(0))] +
             sitio(ae=1, af=1) + estrutura1(dono=1)),
          ig('troops_enemy_cave_bomber_loaded', so14 + tipo14(0x10) + [unidade(14, 0xda, u8(2))] +
             sitio(ae=1, af=1) + estrutura1(dono=1))]
    # a structure selected, another structure under the cursor (BatimentPeutAttaquer, Combat)
    c += [ig('structure_selected_other_structure', [(SEL_ESTRUTURA, u16(0))] + sitio() + estrutura1(dono=1))]
    # page 0xc (Shift held): add a unit to the group
    c += [ig('pagec_hover_unit13', entrada(464, 528), keys=shift),
          ig('pagec_release_unit13', entrada(464, 528, ae=1, af=1), keys=shift),
          ig('pagec_af_only_unit13', entrada(464, 528, af=1), keys=shift),
          ig('pagec_release_terrain', sitio(ae=1, af=1), keys=shift),
          ig('pagec_release_unit13_invisible', entrada(464, 528, ae=1, af=1) + [unidade(13, 0xab, u8(1)),
                                                                                unidade(13, 2, u8(14))],
             keys=shift)]
    # page 0xb: the engineer's structure target (mode byte 0x496209)
    eng = lambda nome, escritas, modo=1, **k: ig(nome, escritas + [(MODO_9, u8(modo))], **k)   # noqa: E731
    c += [eng('pageb_nothing_selected', sitio(pagina=0xb) + estrutura1()),
          eng('pageb_colonist_selected', so13 + sitio(pagina=0xb) + estrutura1()),
          eng('pageb_cave_hover', so15 + sitio(pagina=0xb) + estrutura1()),
          eng('pageb_cave_release_mode1', so15 + sitio(ae=1, af=1, pagina=0xb) + estrutura1()),
          eng('pageb_cave_release_mode3', so15 + sitio(ae=1, af=1, pagina=0xb) + estrutura1(), modo=3),
          eng('pageb_type7_release_mode3', so15 + sitio(ae=1, af=1, pagina=0xb) + estrutura1(tipo=7), modo=3),
          eng('pageb_type7_release_mode1', so15 + sitio(ae=1, af=1, pagina=0xb) + estrutura1(tipo=7)),
          eng('pageb_sanctuary_release', so15 + santuario(ae=1, af=1, pagina=0xb))]
    # (Page 0xb over a cell with no structure is not a case: BatimentGetType(0xffff) 0x429ea2 reads 0x15d9fbc,
    # outside the bench's mapped memory; the smoke run faulted there natively.)
    # page 2 (Alt held): forced attack
    c += [ig('page2_nothing_terrain', sitio(ae=1, af=1), keys=alt),
          ig('page2_soldier_terrain_release', so0 + sitio(ae=1, af=1), keys=alt),
          ig('page2_soldier_terrain_hover', so0 + sitio(), keys=alt),
          ig('page2_soldier_unit13_release', so0 + entrada(464, 528, ae=1, af=1), keys=alt),
          ig('page2_colonist_unit0_hover', so13 + entrada(240, 496, vista=(0, 0)), keys=alt),
          ig('page2_colonist_type10_release', so13 + [unidade(14, 1, u8(0xa))] + entrada(400, 528, ae=1, af=1),
             keys=alt),
          ig('page2_soldier_type17_hover', so0 + [unidade(14, 1, u8(0x11))] + entrada(400, 528), keys=alt),
          ig('page2_soldier_sanctuary_release', so0 + santuario(ae=1, af=1), keys=alt),
          ig('page2_structure_selected', [(SEL_ESTRUTURA, u16(0))] + sitio(ae=1, af=1), keys=alt)]
    # page 7 (Delete held): sell a structure
    c += [ig('page7_terrain', sitio(ae=1, af=1), keys=delete),
          ig('page7_sanctuary_hover', santuario(), keys=delete),
          ig('page7_sanctuary_release', santuario(ae=1, af=1), keys=delete),
          ig('page7_sanctuary_release_selected', [(SEL_ESTRUTURA, u16(0))] + santuario(ae=1, af=1), keys=delete),
          ig('page7_type17_release', sitio(ae=1, af=1) + estrutura1(tipo=0x11), keys=delete),
          ig('page7_flag74_release', sitio(ae=1, af=1) + estrutura1(f74=1), keys=delete),
          ig('page7_enemy_release', sitio(ae=1, af=1) + estrutura1(dono=1), keys=delete)]
    nomes = [x['case'] for x in c]
    if len(nomes) != len(set(nomes)):
        raise ValueError('Duplicate case names')
    return c


assert PACOTE and UNIDADES   # the pause facts this matrix shares with casos_entrada_ordens_ia
