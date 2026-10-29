"""Declared case matrix for the structure-entry, lodging and Bag routines (M3/M4 groundwork).

Every case starts from the exact paused frame-1 state of ``bancada_entrada_estruturas`` (MONDE01 display
reference, first ProcessInputGame entry; the pause of SELECTION_ORDERS and CONSTRUCTION). Facts of that state
used below (probed natively, checked by the capture in ``verificar_pausa``):
- units 0..15 belong to player 0; 3..10 are colonists (type 9, state 14, cell (14,12)) inside the sanctuary;
  11 type 1, 12 type 7 (builder, (17,16)), 13 type 5 ((14,16)), 14 type 5 ((12,16)), 15 type 8; every unit has
  life +0x9a = 100 = the type maximum; unit records from 16 are free;
- structure 0 is the sanctuary (type 2, 6x5, origin (12,11), owner 0, +5 = 5): Bag count 8, capacity 16,
  +0x66 = 8, tag-1 entries 3..10; structure records from 1 are free; the local player is 0.

**Prepared state ``CAVERNA``** (original routines called natively from the pause, as Economy's work-cycle
capture does at frame 2): ``CreerBatiment(cell (23,14), type 3, player 0)`` returns structure 1; its progress
word := target - 2; ``BatimentConstruction(1)`` completes it (owner stays 0xc8, origin (19,10), Bag capacity 2);
``BatimentRetireColon(0)`` releases colonist 3 to (15,14) (state 2, destination (14,14)). A case only adds its
declared writes and argument registers after that. Importing this module executes nothing.
"""
import struct

from casos_selecao_ordens import ESTRUTURAS, UNIDADES, campo, celula, estrutura, lista, u8, u16

PASSO = 276
BOLSA_SANTUARIO = ESTRUTURAS + 0xc
CAVE, COLONO = 1, 3
ORIGEM_CAVE = celula(19, 10)
BUSCA_UNIDADE = 0x496304
CORPO_13, CONTINUACAO = 0x4558e4, 0x454ccd         # EnginNextEtape state-13 body and its common continuation


def bolsa_unidade(u):
    return UNIDADES + PASSO * u + 0xa


def bolsa_estrutura(s):
    return ESTRUTURAS + PASSO * s + 0xc


def conteudo(bolsa, entradas, capacidade=None, volume=None, contagem=None):
    """Bag at ``bolsa``: count, capacity, +0x66 volume and the (tag, value) entries (rest of the 30 slots zero)."""
    n = len(entradas) if contagem is None else contagem
    cap = max(n, 1) if capacidade is None else capacidade
    tags = bytes(t for t, _ in entradas) + bytes(30 - len(entradas))
    valores = b''.join(u16(v) for _, v in entradas) + bytes(2 * (30 - len(entradas)))
    return [(bolsa, u16(n) + u16(cap)), (bolsa + 6, valores), (bolsa + 0x42, tags),
            (bolsa + 0x66, u16(n if volume is None else volume))]


def chamada(rotina, **regs):
    return dict(kind='call', routine=rotina, registers=regs)


def escrita(endereco, dados):
    return dict(kind='write', address=endereco, bytes=bytes(dados))


def preparar_caverna(alvo_progresso):
    """The prepared CAVE + released colonist (``alvo_progresso`` = the cave's type word +4, read at the pause)."""
    return [dict(chamada('CreerBatiment', EAX=celula(23, 14), EDX=3, EBX=0), expect_eax=CAVE),
            escrita(ESTRUTURAS + PASSO * CAVE + 0xa, u16(alvo_progresso - 2)),
            dict(chamada('BatimentConstruction', EAX=CAVE), expect_eax=5),
            dict(chamada('BatimentRetireColon', EAX=0), expect_eax=COLONO)]


def caso(nome, rotina, writes=(), preparo=(), stack=(), **regs):
    return dict(case=nome, preparation=list(preparo),
                steps=[dict(routine=rotina, registers=regs, writes=list(writes), stack=list(stack))])


def corpo13(nome, unidade, writes=(), preparo=(), repeat=1, until=None, antes=()):
    """Unit state 13's body inside EnginNextEtape: ESI = record, DI = unit; stops at the continuation 0x454ccd.
    ``antes``: measured leaf steps run first (e.g. the order setter)."""
    passo = dict(routine='EnginNextEtape:state13', entry=CORPO_13, stops=(CONTINUACAO,), writes=list(writes),
                 registers=dict(ESI=UNIDADES + PASSO * unidade, EDI=unidade), repeat=repeat)
    if until is not None:
        passo['until'] = until
    return dict(case=nome, preparation=list(preparo), steps=list(antes) + [passo])


def casos(alvo_progresso, grade):
    """The declared matrix; ``grade`` maps 'regioes'/'atributos' to the grid pointers at the pause."""
    cav = preparar_caverna(alvo_progresso)
    reg = lambda c, v: (grade['regioes'] + 2 * c, u16(v))
    c = []
    # ------------------------------------------------------------ Bag primitives
    mista = [(2, 1), (2, 2), (2, 1), (3, 7), (6, 9), (4, 1), (5, 1), (7, 3), (1, 13), (1, 3), (1, 12)]
    b13 = bolsa_unidade(13)
    t = 'BagContient'                                # EAX Bag, DL tag, BX target
    c += [caso('contient_sanctuary_colonists', t, EAX=BOLSA_SANTUARIO, EDX=1, EBX=9),
          caso('contient_sanctuary_type5', t, EAX=BOLSA_SANTUARIO, EDX=1, EBX=5),
          caso('contient_sanctuary_tag2', t, EAX=BOLSA_SANTUARIO, EDX=2, EBX=1),
          caso('contient_cave_empty', t, preparo=cav, EAX=bolsa_estrutura(CAVE), EDX=1, EBX=9),
          caso('contient_unit13_empty_cap1', t, EAX=b13, EDX=2, EBX=1)]
    for tag, alvo in ((1, 9), (1, 5), (1, 7), (2, 1), (2, 2), (2, 5), (3, 7), (3, 8), (4, 1), (5, 1), (6, 9),
                      (6, 1), (7, 3), (7, 9), (0, 0), (8, 1), (0xff, 1)):
        c.append(caso(f'contient_mixed_tag{tag}_{alvo}', t, conteudo(b13, mista, capacidade=12), EAX=b13, EDX=tag,
                      EBX=alvo))
    c += [caso('contient_upper_bits', t, conteudo(b13, mista, capacidade=12), EAX=b13, EDX=0xabcdef02,
               EBX=0x12340001, ECX=0x55555555, ESI=0x66666666, EDI=0x77777777, EBP=0x88888888),
          caso('contient_capacity_below_count', t, conteudo(b13, mista, capacidade=3), EAX=b13, EDX=2, EBX=1),
          caso('contient_stale_beyond_count', t, conteudo(b13, mista, capacidade=12, contagem=2), EAX=b13, EDX=2,
               EBX=1),
          caso('contient_capacity_zero', t, conteudo(b13, mista, capacidade=0), EAX=b13, EDX=2, EBX=1),
          caso('contient_food_cargo', t, conteudo(b13, [(2, 1)]), EAX=b13, EDX=2, EBX=1),
          caso('contient_stone_cargo', t, conteudo(b13, [(2, 2)]), EAX=b13, EDX=2, EBX=2)]
    t = 'BagContientTroupe'                          # EAX Bag
    c += [caso('troupe_sanctuary_colonists', t, EAX=BOLSA_SANTUARIO),
          caso('troupe_sanctuary_plus_worker', t, conteudo(BOLSA_SANTUARIO, [(1, 3), (1, 4), (1, 13)], 16),
               EAX=BOLSA_SANTUARIO),
          caso('troupe_soldier_first', t, conteudo(BOLSA_SANTUARIO, [(1, 0), (1, 4)], 16), EAX=BOLSA_SANTUARIO),
          caso('troupe_type8_unit', t, conteudo(BOLSA_SANTUARIO, [(1, 15)], 16), EAX=BOLSA_SANTUARIO),
          caso('troupe_tag2_only', t, conteudo(b13, [(2, 0), (2, 13)], 4), EAX=b13),
          caso('troupe_empty', t, preparo=cav, EAX=bolsa_estrutura(CAVE)),
          caso('troupe_quad_types', t, conteudo(b13, [(1, 16), (1, 17)], 4) +
               [campo(16, 1, u8(3)), campo(17, 1, u8(0x19))], EAX=b13),
          caso('troupe_vehicle_types', t, conteudo(b13, [(1, 16), (1, 17), (1, 18)], 4) +
               [campo(16, 1, u8(0xe)), campo(17, 1, u8(0x12)), campo(18, 1, u8(0x17))], EAX=b13),
          caso('troupe_type_ranges', t, conteudo(b13, [(1, 16), (1, 17), (1, 18), (1, 19)], 4) +
               [campo(16, 1, u8(0x11)), campo(17, 1, u8(0xb)), campo(18, 1, u8(2)), campo(19, 1, u8(0x18))], EAX=b13),
          caso('troupe_upper_bits', t, EAX=BOLSA_SANTUARIO, EBX=0x11111111, ECX=0x22222222, EDX=0x33333333)]
    t = 'BagRetire'                                  # EAX Bag, DL tag, BX type (tag 1) or value
    c += [caso('retire_sanctuary_colonist', t, EAX=BOLSA_SANTUARIO, EDX=1, EBX=9),
          caso('retire_sanctuary_type5_absent', t, EAX=BOLSA_SANTUARIO, EDX=1, EBX=5),
          caso('retire_mixed_type5', t, conteudo(b13, mista, capacidade=12), EAX=b13, EDX=1, EBX=5),
          caso('retire_mixed_food', t, conteudo(b13, mista, capacidade=12), EAX=b13, EDX=2, EBX=1),
          caso('retire_mixed_stone', t, conteudo(b13, mista, capacidade=12), EAX=b13, EDX=2, EBX=2),
          caso('retire_mixed_tag7', t, conteudo(b13, mista, capacidade=12), EAX=b13, EDX=7, EBX=3),
          caso('retire_mixed_last', t, conteudo(b13, mista, capacidade=12), EAX=b13, EDX=1, EBX=7),
          caso('retire_mixed_absent', t, conteudo(b13, mista, capacidade=12), EAX=b13, EDX=2, EBX=9),
          caso('retire_food_cargo', t, conteudo(b13, [(2, 1)]), EAX=b13, EDX=2, EBX=1),
          caso('retire_volume_mismatch', t, conteudo(b13, [(2, 1), (2, 1)], 2, volume=7), EAX=b13, EDX=2, EBX=1),
          caso('retire_empty', t, EAX=b13, EDX=2, EBX=1),
          caso('retire_upper_bits', t, conteudo(b13, mista, capacidade=12), EAX=b13, EDX=0x77777702, EBX=0x99990002,
               ECX=0x12345678, ESI=0x9abcdef0, EDI=0x0f0f0f0f, EBP=0xf0f0f0f0)]
    t = 'BagPrend'                                   # EAX Bag, DL tag, BX value
    c += [caso('prend_cave_colonist', t, preparo=cav, EAX=bolsa_estrutura(CAVE), EDX=1, EBX=COLONO),
          caso('prend_sanctuary_worker', t, EAX=BOLSA_SANTUARIO, EDX=1, EBX=13),
          caso('prend_unit_food', t, EAX=b13, EDX=2, EBX=1),
          caso('prend_after_mixed', t, conteudo(b13, mista, capacidade=12), EAX=b13, EDX=3, EBX=0x1234),
          caso('prend_upper_bits', t, EAX=b13, EDX=0xabcdef02, EBX=0x56780002, ECX=0x11223344, ESI=0x55667788)]
    t = 'EnginGetBag'                                # AX unit
    c += [caso('getbag_13', t, EAX=13), caso('getbag_3', t, EAX=3), caso('getbag_799', t, EAX=799),
          caso('getbag_upper_bits', t, EAX=0xffff000d, EDX=0x12345678)]
    t = 'BagAccepte'                                 # EAX Bag, DL tag, BX amount
    for tag in (0, 1, 2, 3, 4, 5, 9):
        c.append(caso(f'accepte_tag{tag}', t, conteudo(b13, [(2, 1)], 2), EAX=b13, EDX=tag, EBX=3))
    c += [caso('accepte_full', t, conteudo(b13, [(2, 1)], 1), EAX=b13, EDX=2, EBX=1),
          caso('accepte_tag3_room', t, conteudo(b13, [(2, 1)], 9), EAX=b13, EDX=3, EBX=0x10005)]
    # ------------------------------------------------------------ PlaceLibre: AX structure, DX unit
    t = 'PlaceLibre'
    def estrutura_tipo(tipo, entradas, cap=16):
        return [estrutura(2, 8, u8(tipo)), estrutura(2, 5, u8(5)), estrutura(2, 4, u8(0))] + \
            conteudo(bolsa_estrutura(2), entradas, cap)
    c += [caso('placelibre_cave_colonist', t, preparo=cav, EAX=CAVE, EDX=COLONO),
          caso('placelibre_cave_full', t, conteudo(bolsa_estrutura(CAVE), [(1, 4), (1, 5)], 2), preparo=cav,
               EAX=CAVE, EDX=COLONO),
          caso('placelibre_sanctuary_worker', t, EAX=0, EDX=13),
          caso('placelibre_sanctuary_full', t, [(BOLSA_SANTUARIO + 0x66, u16(16))], EAX=0, EDX=13),
          caso('placelibre_type8_room', t, estrutura_tipo(8, [(1, 4)] * 3), EAX=2, EDX=13),
          caso('placelibre_type8_limit', t, estrutura_tipo(8, [(1, 4)] * 9), EAX=2, EDX=13),
          caso('placelibre_type8_over', t, estrutura_tipo(8, [(1, 4)] * 10), EAX=2, EDX=13)]
    ferido = [campo(13, 0x9a, u16(60))]
    for nome, extra, unidade in (('healthy_worker', [], 13), ('wounded_worker', ferido, 13),
                                 ('healthy_colonist', [], 4), ('wounded_colonist', [campo(4, 0x9a, u16(1))], 4)):
        for tipo in (0x13, 0xe):
            c.append(caso(f'placelibre_type{tipo:x}_{nome}', t, estrutura_tipo(tipo, [(1, 3), (1, 5)]) + extra,
                          EAX=2, EDX=unidade))
    c += [caso('placelibre_type13_colonists_full_life', t,
               estrutura_tipo(0x13, [(1, 3), (1, 5), (1, 6), (1, 7), (2, 9)]) + [campo(4, 0x9a, u16(50))], EAX=2,
               EDX=4),
          caso('placelibre_typee_colonists', t, estrutura_tipo(0xe, [(1, 3), (1, 5), (1, 6), (1, 7), (1, 8)]) +
               [campo(4, 0x9a, u16(50))], EAX=2, EDX=4),
          caso('placelibre_type13_room_full', t, estrutura_tipo(0x13, [(1, 3), (1, 5)], 2) + ferido, EAX=2, EDX=13),
          caso('placelibre_upper_bits', t, preparo=cav, EAX=0x12340001, EDX=0x56780003, EBX=0x9abcdef0,
               ECX=0x0badf00d, ESI=0x11111111, EDI=0x22222222, EBP=0x33333333)]
    # ------------------------------------------------------------ geometry: BatimentAdjacent, GetCaseCentrale, ...
    t = 'BatimentAdjacent'                           # AX structure, DX cell
    for x, y in ((18, 10), (18, 11), (18, 12), (19, 9), (22, 9), (22, 10), (23, 10), (23, 11), (23, 12), (18, 9),
                 (20, 12), (17, 12), (19, 13), (21, 13), (22, 12), (19, 10), (24, 11)):
        c.append(caso(f'adjacent_cave_{x}_{y}', t, preparo=cav, EAX=CAVE, EDX=celula(x, y)))
    c += [caso('adjacent_sanctuary_15_14', t, EAX=0, EDX=celula(15, 14)),
          caso('adjacent_sanctuary_14_16', t, EAX=0, EDX=celula(14, 16)),
          caso('adjacent_sanctuary_11_10', t, EAX=0, EDX=celula(11, 10)),
          caso('adjacent_sanctuary_far', t, EAX=0, EDX=celula(30, 30)),
          caso('adjacent_corner_0_0', t, [estrutura(2, 8, u8(3)), estrutura(2, 2, u16(0))], EAX=2, EDX=0),
          caso('adjacent_row255', t, [estrutura(2, 8, u8(3)), estrutura(2, 2, u16(celula(5, 252)))], EAX=2,
               EDX=celula(5, 255)),
          caso('adjacent_column255', t, [estrutura(2, 8, u8(3)), estrutura(2, 2, u16(celula(252, 5)))], EAX=2,
               EDX=celula(255, 6)),
          caso('adjacent_upper_bits', t, preparo=cav, EAX=0xabcd0001, EDX=0x12340000 | celula(18, 10),
               EBX=0x55555555, ECX=0x66666666, ESI=0x77777777, EDI=0x88888888, EBP=0x99999999)]
    t = 'GetCaseCentrale'                            # AX structure
    c += [caso('centrale_sanctuary', t, EAX=0), caso('centrale_cave', t, preparo=cav, EAX=CAVE)]
    for tipo in (0, 1, 4, 8, 9, 12, 14, 19, 21):
        c.append(caso(f'centrale_type{tipo}', t, [estrutura(2, 8, u8(tipo)), estrutura(2, 2, u16(celula(30, 20)))],
                      EAX=2))
    c.append(caso('centrale_upper_bits', t, EAX=0xffff0000, EBX=0x1234, ECX=0x5678, EDX=0x9abc, EDI=0xdef0))
    t = 'BatimentGetCase'
    c += [caso('getcase_sanctuary', t, EAX=0), caso('getcase_cave', t, preparo=cav, EAX=CAVE)]
    t = 'BatimentGetCaseEntrer'                      # AX structure, DX unit
    for tipo in (2, 3, 8, 0xe, 0x12):
        for u, tu in ((13, None), (16, 3), (16, 0xb), (16, 0x11), (16, 0x12)):
            extra = [] if tu is None else [campo(16, 1, u8(tu))]
            c.append(caso(f'caseentrer_type{tipo:x}_unit{tu if tu is not None else 13}', t,
                          [estrutura(2, 8, u8(tipo)), estrutura(2, 2, u16(celula(30, 20)))] + extra, EAX=2, EDX=u))
    t = 'BatimentGetVolume'
    c += [caso('batvolume_sanctuary', t, EAX=0), caso('batvolume_cave', t, preparo=cav, EAX=CAVE),
          caso('batvolume_far', t, [estrutura(2, 2, u16(celula(60, 60)))], EAX=2)]
    t = 'EnginGetVolume'
    c += [caso('volume_unit13', t, EAX=13), caso('volume_unit13_selected', t, [campo(13, 0xbd, u8(1))], EAX=13),
          caso('volume_colonist_released', t, preparo=cav, EAX=COLONO)]
    for t, n in (('EnginGetType', 13), ('EnginGetPlayer', 13), ('TerrainEstDecouvert', None)):
        if n is not None:
            c.append(caso(f'{t}_13_upper', t, EAX=0x5555000d, EDX=0x12345678))
    c += [caso('decouvert_cave_site', 'TerrainEstDecouvert', EAX=ORIGEM_CAVE, EDX=0),
          caso('decouvert_far', 'TerrainEstDecouvert', EAX=celula(40, 40), EDX=0x1234ff00)]
    # ------------------------------------------------------------ unit primitives
    t = 'RetireEngin'                                # AX unit
    c += [caso('retire_unit13', t, EAX=13), caso('retire_unit13_upper', t, EAX=0xabcd000d, EBX=0x1111, ECX=0x2222,
                                                  EDX=0x3333, ESI=0x4444, EDI=0x5555, EBP=0x6666),
          caso('retire_unit13_moving', t, [campo(13, 0x7c, u16(celula(15, 16)))] + [reg(celula(15, 16), 0x4000 | 13 << 3)],
               EAX=13),
          caso('retire_unit13_selected', t, lista(0, [13]), EAX=13),
          caso('retire_colonist_released', t, preparo=cav, EAX=COLONO),
          caso('retire_owner4', t, [campo(13, 0, u8(4))], EAX=13),
          caso('retire_owner_c8', t, [campo(13, 0, u8(0xc8))], EAX=13),
          caso('retire_hidden_unit', t, [campo(13, 0x72, u8(0))], EAX=13),
          caso('retire_builder', t, EAX=12)]
    t = 'AnimWorkEngin'                              # AX unit
    for tipo, fase, a9, a7, a4, a5 in ((5, 1, 0, 3, 0, 4), (5, 1, 2, 3, 3, 4), (5, 0, 2, 3, 3, 4), (5, 2, 2, 3, 3, 4),
                                       (5, 4, 2, 3, 3, 4), (7, 12, 1, 2, 4, 5), (7, 12, 0, 2, 4, 5), (7, 3, 1, 2, 4, 5),
                                       (13, 1, 1, 2, 3, 4), (13, 4, 1, 2, 1, 4), (13, 4, 0, 2, 1, 4), (13, 2, 1, 2, 1, 4),
                                       (13, 5, 1, 2, 1, 4), (6, 1, 1, 2, 1, 4), (4, 1, 1, 2, 1, 4), (8, 1, 1, 2, 1, 4),
                                       (7, 12, 1, 2, 4, 0x81)):
        c.append(caso(f'animwork_type{tipo}_phase{fase}_{a9}_{a7}_{a4}_{a5}', t,
                      [campo(13, 1, u8(tipo)), campo(13, 0x89, u8(fase)), campo(13, 0xa9, u8(a9)),
                       campo(13, 0xa7, u8(a7)), campo(13, 0xa4, u8(a4)), campo(13, 0xa5, u8(a5))], EAX=13))
    c.append(caso('animwork_upper_bits', t, [campo(13, 0x89, u8(1)), campo(13, 0xa9, u8(2)), campo(13, 0xa7, u8(3))],
                  EAX=0x7777000d, EBX=0x1, ECX=0x2, EDX=0x3))
    t = 'SetEnginCollision'                          # AX unit, DX cell
    c += [caso('collision_unit13_free_cell', t, EAX=13, EDX=celula(15, 16)),
          caso('collision_colonist_cave_cell', t, preparo=cav, EAX=COLONO, EDX=celula(18, 10))]
    t = 'SetDeplaceEngin'                            # AX unit, DX cell
    c += [caso('deplace_colonist_cave', t, preparo=cav, EAX=COLONO, EDX=celula(21, 12)),
          caso('deplace_unit13_search_owner', t, [(BUSCA_UNIDADE, u16(13))], EAX=13, EDX=celula(20, 20))]
    t = 'EnginPeutPasser'                            # AX unit, DX cell, BL mask, CL
    c += [caso('peutpasser_free', t, EAX=13, EDX=celula(15, 16), EBX=1, ECX=0),
          caso('peutpasser_unit', t, EAX=13, EDX=celula(17, 16), EBX=1, ECX=0),
          caso('peutpasser_sanctuary', t, EAX=13, EDX=celula(14, 14), EBX=1, ECX=0),
          caso('peutpasser_own_cell', t, EAX=13, EDX=celula(14, 16), EBX=2, ECX=0)]
    t = 'DecouvreTerrain'                            # AX cell, DX radius, BL player
    c += [caso('decouvre_cave_r7', t, EAX=celula(21, 12), EDX=7, EBX=0),
          caso('decouvre_far_r3', t, EAX=celula(40, 40), EDX=3, EBX=0)]
    t = 'IllumineTerrain'
    c += [caso('illumine_cave_r5', t, EAX=celula(21, 12), EDX=5, EBX=0),
          caso('illumine_far_r3', t, EAX=celula(40, 40), EDX=3, EBX=0)]
    t = 'BatimentModifyMap'                          # AX structure, DL mode
    c += [caso('modifymap_cave_on', t, preparo=cav, EAX=CAVE, EDX=1),
          caso('modifymap_cave_off', t, preparo=cav, EAX=CAVE, EDX=0)]
    # ------------------------------------------------------------ order setters and the selection query
    t = 'SetEnginRentreBatiment'                     # AX unit, DX structure, BL unit type
    c += [caso('rentre_colonist_cave', t, preparo=cav, EAX=COLONO, EDX=CAVE, EBX=9),
          caso('rentre_worker_sanctuary', t, EAX=13, EDX=0, EBX=5),
          caso('rentre_worker_sanctuary_search_owner', t, [(BUSCA_UNIDADE, u16(13))], EAX=13, EDX=0, EBX=5),
          caso('rentre_dead_unit', t, [campo(13, 2, u8(0))], EAX=13, EDX=0, EBX=5),
          caso('rentre_dying_unit', t, [campo(13, 2, u8(4))], EAX=13, EDX=0, EBX=5),
          caso('rentre_upper_bits', t, EAX=0xabcd000d, EDX=0x12340000, EBX=0x55555505, ECX=0x66666666,
               ESI=0x77777777, EDI=0x88888888, EBP=0x99999999)]
    for tipo, u, tu, modo in ((8, 13, None, None), (8, 3, None, None), (8, 16, 3, None), (0xe, 16, 0xb, 5),
                              (0xe, 16, 0x11, 5), (0xe, 16, 0x12, 5), (0xe, 16, 0xb, 4), (0x12, 16, 0x10, None),
                              (0x12, 13, None, None), (0x10, 13, None, None)):
        extra = [] if tu is None else [campo(16, 0, u8(0)), campo(16, 1, u8(tu)), campo(16, 2, u8(7)),
                                       campo(16, 8, u16(celula(20, 20)))]
        if modo is not None:
            extra.append(estrutura(2, 5, u8(modo)))
        c.append(caso(f'rentre_type{tipo:x}_unit{u}_{tu}_{modo}', t, [estrutura(2, 8, u8(tipo)),
                                                                     estrutura(2, 2, u16(celula(30, 20)))] + extra,
                      EAX=u, EDX=2, EBX=tu or 5))
    t = 'SetEnginSelectRentreBatiment'              # AL player, DX structure
    c += [caso('select_rentre_colonist_cave', t, lista(0, [COLONO]), preparo=cav, EAX=0, EDX=CAVE),
          caso('select_rentre_worker_sanctuary', t, lista(0, [13]), EAX=0, EDX=0),
          caso('select_rentre_two_workers', t, lista(0, [13, 14]), EAX=0, EDX=0),
          caso('select_rentre_dead_first', t, lista(0, [16, 13]), EAX=0, EDX=0),
          caso('select_rentre_empty', t, EAX=0, EDX=0),
          caso('select_rentre_player1', t, lista(1, [13]), EAX=1, EDX=0)]
    for tipo in (1, 2, 8, 0xa, 0xc, 0xd, 0x10, 0x11):
        for u in (13, 4, 16):
            extra = [campo(16, 0, u8(0)), campo(16, 1, u8(0xa)), campo(16, 2, u8(7))] if u == 16 else []
            c.append(caso(f'select_rentre_type{tipo:x}_unit{u}', t,
                          lista(0, [u]) + extra + [estrutura(2, 8, u8(tipo)), estrutura(2, 5, u8(5)),
                                                   estrutura(2, 4, u8(0)), estrutura(2, 2, u16(celula(30, 20)))],
                          EAX=0, EDX=2))
    t = 'EnginSelectPeutEntrer'                      # AL player, DL mode, BX structure or unit
    sel = lambda us: lista(0, us)
    c += [caso('peutentrer_worker_sanctuary', t, sel([13]), EAX=0, EDX=3, EBX=0),
          caso('peutentrer_worker_cave_c8', t, sel([13]), preparo=cav, EAX=0, EDX=3, EBX=CAVE),
          caso('peutentrer_colonist_cave_c8', t, sel([COLONO]), preparo=cav, EAX=0, EDX=3, EBX=CAVE),
          caso('peutentrer_worker_cave_owned', t, sel([13]) + [estrutura(CAVE, 4, u8(0))], preparo=cav, EAX=0, EDX=3,
               EBX=CAVE),
          caso('peutentrer_colonist_sanctuary', t, sel([COLONO]), preparo=cav, EAX=0, EDX=3, EBX=0),
          caso('peutentrer_empty_selection', t, EAX=0, EDX=3, EBX=0),
          caso('peutentrer_mirror_unit', t, sel([13]) + [campo(13, 0xdc, u8(4))], EAX=0, EDX=3, EBX=0),
          caso('peutentrer_dead_mirror_ignored', t, sel([16, 13]) + [campo(16, 0xdc, u8(4))], EAX=0, EDX=3, EBX=0),
          caso('peutentrer_worker_and_colonist_cave', t, sel([13, COLONO]), preparo=cav, EAX=0, EDX=3, EBX=CAVE),
          caso('peutentrer_foreign_structure', t, sel([13]) + [estrutura(0, 4, u8(1))], EAX=0, EDX=3, EBX=0),
          caso('peutentrer_mode0', t, sel([13]), EAX=0, EDX=0, EBX=0),
          caso('peutentrer_mode2', t, sel([13]), EAX=0, EDX=2, EBX=0),
          caso('peutentrer_mode4', t, sel([13]), EAX=0, EDX=4, EBX=0),
          caso('peutentrer_upper_bits', t, sel([13]), EAX=0x12345600, EDX=0xabcdef03, EBX=0x77770000,
               ECX=0x11111111, ESI=0x22222222, EDI=0x33333333, EBP=0x44444444)]
    soldados = [campo(16, 0, u8(0)), campo(16, 2, u8(7)), campo(17, 0, u8(0)), campo(17, 2, u8(7))]
    for tipo in (2, 8, 9, 0xe, 0x10, 0x12, 0x13, 0x15, 3, 5):
        for nome, us, tipos in (('worker', [13], ()), ('colonist', [4], ()), ('soldier', [0], ()),
                                ('wounded', [13], ()), ('vehicle', [16], (0xb,)), ('type16', [16], (0x10,)),
                                ('type10', [16], (0xa,)), ('quad', [16], (3,)), ('fullbomb', [16], (0xb,))):
            extra = sel(us) + soldados + [estrutura(2, 8, u8(tipo)), estrutura(2, 5, u8(5)), estrutura(2, 4, u8(0))]
            extra += [campo(16, 1, u8(x)) for x in tipos]
            if nome == 'wounded':
                extra.append(campo(13, 0x9a, u16(40)))
            if nome == 'fullbomb':
                extra.append(campo(16, 0xda, u8(5)))
            c.append(caso(f'peutentrer_type{tipo:x}_{nome}', t, extra, EAX=0, EDX=3, EBX=2))
    for nome, alvo_t, us, tipos in (('vehicle_troops', 0xb, [13, 0], ()), ('vehicle_type16', 0x10, [13], ()),
                                    ('vehicle_soldier', 0x11, [0], ()), ('vehicle_type11_type8', 0x11, [15], ()),
                                    ('vehicle_type11_mixed', 0x11, [15, 13], ()), ('not_vehicle', 5, [13], ()),
                                    ('vehicle_colonist', 0xc, [4], ())):
        extra = sel(us) + [campo(16, 0, u8(0)), campo(16, 1, u8(alvo_t)), campo(16, 2, u8(7))]
        c.append(caso(f'peutentrer_mode1_{nome}', t, extra, EAX=0, EDX=1, EBX=16))
    # ------------------------------------------------------------ CalculEntreBatiment: AX unit (main branch)
    t = 'CalculEntreBatiment'
    rumo = lambda u, s, b2=0xffff: [campo(u, 2, u8(13)), campo(u, 0xc0, u16(s)), campo(u, 0xb2, u16(b2))]
    c += [caso('entre_colonist_far', t, rumo(COLONO, CAVE) + [campo(COLONO, 0x7e, u16(celula(21, 12)))], preparo=cav,
               EAX=COLONO),
          caso('entre_colonist_at_destination', t, rumo(COLONO, CAVE) + [campo(COLONO, 0x7e, u16(celula(15, 14)))],
               preparo=cav, EAX=COLONO),
          caso('entre_colonist_at_destination_search_owner', t, rumo(COLONO, CAVE) +
               [campo(COLONO, 0x7e, u16(celula(15, 14))), (BUSCA_UNIDADE, u16(COLONO))], preparo=cav, EAX=COLONO),
          caso('entre_no_structure', t, [campo(13, 0xc0, u16(0xffff))], EAX=13),
          caso('entre_pushed_86', t, rumo(COLONO, CAVE) + [campo(COLONO, 0x86, u8(1)),
                                                          campo(COLONO, 8, u16(celula(18, 10)))], preparo=cav,
               EAX=COLONO),
          caso('entre_pushed_87', t, rumo(COLONO, CAVE) + [campo(COLONO, 0x87, u8(0x80)),
                                                          campo(COLONO, 8, u16(celula(18, 10)))], preparo=cav,
               EAX=COLONO),
          caso('entre_type8_own', t, [estrutura(2, 8, u8(8)), estrutura(2, 4, u8(0)), estrutura(2, 5, u8(5)),
                                      estrutura(2, 2, u16(celula(30, 20)))] + rumo(13, 2), EAX=13),
          caso('entre_type8_own_search_owner', t, [estrutura(2, 8, u8(8)), estrutura(2, 4, u8(0)),
                                                   estrutura(2, 2, u16(celula(30, 20))), (BUSCA_UNIDADE, u16(13))] +
               rumo(13, 2), EAX=13),
          caso('entre_type8_dead_unit', t, [estrutura(2, 8, u8(8)), estrutura(2, 4, u8(0)),
                                            estrutura(2, 2, u16(celula(30, 20)))] + rumo(13, 2) +
               [campo(13, 2, u8(0))], EAX=13),
          caso('entre_type8_foreign', t, [estrutura(2, 8, u8(8)), estrutura(2, 4, u8(1)),
                                          estrutura(2, 2, u16(celula(30, 20)))] + rumo(13, 2) +
               [campo(13, 0x7e, u16(celula(29, 20)))], EAX=13),
          caso('entre_unit_type_out_of_branch', t, rumo(13, 0) + [campo(13, 1, u8(0x10))], EAX=13)]
    # ------------------------------------------------------------ state 13 body and short windows
    c += [corpo13('state13_colonist_cave_far', COLONO, rumo(COLONO, CAVE) +
                  [campo(COLONO, 0x7e, u16(celula(21, 12)))], cav),
          corpo13('state13_no_structure_no_vehicle', 13, [campo(13, 2, u8(13)), campo(13, 0xc0, u16(0xffff)),
                                                          campo(13, 0xb8, u16(0xffff))]),
          corpo13('state13_worker_cave_c8', 13, rumo(13, CAVE) + [campo(13, 0x7e, u16(celula(21, 12)))], cav),
          corpo13('state13_destroyed_structure', 13, rumo(13, 0) + [estrutura(0, 5, u8(3)),
                                                                     campo(13, 0x7e, u16(celula(14, 14)))]),
          corpo13('state13_foreign_owner', 13, rumo(13, 0) + [estrutura(0, 4, u8(1)),
                                                               campo(13, 0x7e, u16(celula(14, 14)))]),
          corpo13('state13_type10_c8', 13, rumo(13, CAVE) + [campo(13, 1, u8(0xa))], cav),
          corpo13('state13_type10_own_type16', 13, rumo(13, 0) + [campo(13, 1, u8(0xa)), estrutura(0, 8, u8(0x10))]),
          corpo13('state13_type10_foreign', 13, rumo(13, 0) + [campo(13, 1, u8(0xa)), estrutura(0, 4, u8(1)),
                                                                campo(13, 0x7e, u16(celula(14, 14)))]),
          corpo13('state13_type10_own_sanctuary_far', 13, rumo(13, 0) + [campo(13, 1, u8(0xa)),
                                                                          campo(13, 0x7e, u16(celula(14, 14)))])]
    # the colonist's whole walk into the 0xc8 cave: order, then one state-13 body per frame until it lodges
    ordem = dict(routine='SetEnginRentreBatiment', registers=dict(EAX=COLONO, EDX=CAVE, EBX=9))
    c.append(corpo13('window_colonist_into_cave', COLONO, preparo=cav, antes=[ordem], repeat=240,
                     until=(UNIDADES + PASSO * COLONO + 2, 1, 14)))
    # an idle worker entering the own sanctuary (Economy's frame-512 order; empty Bag here)
    ordem13 = dict(routine='SetEnginRentreBatiment', registers=dict(EAX=13, EDX=0, EBX=5))
    c.append(corpo13('window_worker_into_sanctuary', 13, antes=[ordem13], repeat=200,
                     until=(UNIDADES + PASSO * 13 + 2, 1, 14)))
    # ------------------------------------------------------------ releasing a colonist (tag 0x21)
    t = 'BatimentRetireColon'                        # AX structure
    c += [caso('retirecolon_sanctuary', t, EAX=0),
          caso('retirecolon_sanctuary_after_first', t, preparo=cav, EAX=0),
          caso('retirecolon_owned_cave_one_colonist', t, conteudo(bolsa_estrutura(CAVE), [(1, 4)], 2) +
               [estrutura(CAVE, 4, u8(0)), estrutura(0, 0x66 + 0xc, u16(7))] +
               conteudo(BOLSA_SANTUARIO, [(1, i) for i in range(5, 11)], 16), preparo=cav, EAX=CAVE)]
    # (the empty 0xc8 cave is not a case: the original faults there, EteintTerrain indexes the light grid of 0xc8)
    nomes = [x['case'] for x in c]
    if len(nomes) != len(set(nomes)):
        raise ValueError('Duplicate case names')
    return c


def verificar_pausa(ler):
    """Check the documented pause facts with ``ler(addr, n) -> bytes``; returns (cave progress target, grids)."""
    u16_ = lambda a: struct.unpack('<H', ler(a, 2))[0]
    u32_ = lambda a: struct.unpack('<I', ler(a, 4))[0]
    u = lambda i, o, n=1: ler(UNIDADES + PASSO * i + o, n)
    fatos = {
        'unit pool': (u32_(0x4e19a0), UNIDADES),
        'local player': (ler(0x508041, 1), b'\x00'),
        'unit types 0..15': (bytes(u(i, 1)[0] for i in range(16)),
                             bytes([0, 0, 0] + [9] * 8 + [1, 7, 5, 5, 8])),
        'colonists 3..10 inside (state 14)': (bytes(u(i, 2)[0] for i in range(3, 11)), bytes([14] * 8)),
        'units 13/14/12 cells': ((u16_(UNIDADES + PASSO * 13 + 8), u16_(UNIDADES + PASSO * 14 + 8),
                                  u16_(UNIDADES + PASSO * 12 + 8)), (celula(14, 16), celula(12, 16), celula(17, 16))),
        'unit 16 free': (u(16, 2), b'\x00'),
        'sanctuary record': ((ler(ESTRUTURAS + 4, 2), u16_(ESTRUTURAS + 2), ler(ESTRUTURAS + 8, 1)),
                             (b'\x00\x05', celula(12, 11), b'\x02')),
        'sanctuary Bag count/capacity/volume': ((u16_(BOLSA_SANTUARIO), u16_(BOLSA_SANTUARIO + 2),
                                                 u16_(BOLSA_SANTUARIO + 0x66)), (8, 16, 8)),
        'sanctuary Bag entries': (ler(BOLSA_SANTUARIO + 0x42, 8) + ler(BOLSA_SANTUARIO + 6, 16),
                                  bytes([1] * 8) + b''.join(u16(i) for i in range(3, 11))),
        'free structure records 1 and 2': ((ler(ESTRUTURAS + PASSO + 5, 1), ler(ESTRUTURAS + 2 * PASSO + 5, 1)),
                                           (b'\x00', b'\x00')),
        'selection lists empty': ((u16_(0x508728), u16_(0x508928)), (0, 0)),
    }
    erradas = {k: v for k, v in fatos.items() if v[0] != v[1]}
    if erradas:
        raise RuntimeError(f'Pause state differs from the documented facts: {erradas}')
    grade = dict(regioes=u32_(0x4e0f38), atributos=u32_(0x507da8))
    return u16_(0x495d8c + 52 * 3 + 4), grade
