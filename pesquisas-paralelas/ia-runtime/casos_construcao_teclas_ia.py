"""Declared case matrix for M3.1 round 2: EnginNextEtape state 11 (builder), CalculConstruireBatiment's
construction-progress branch and its structure leaves, the state-13 dispatch, ProcessInputGame tags
0xb/0xc/0x10/0x21, WndProc's key messages 0x100/0x101 and InputGame's group-number and GoLastAttaque keys.

Every case starts from the same paused frame-1 state as ``casos_entrada_ordens_ia`` (Core's
``bancada_selecao_ordens``, MONDE01 display reference, first ProcessInputGame entry); the facts of that state
are listed there. A case adds only declared byte writes, argument registers, pushed words and ordered
GetAsyncKeyState answers. Importing this module executes nothing.

Declared builds:
- ``ordem_caverna``: unit 12's order state after the committed native case ``process_tag4_build_cave`` of
  ``evidencias/captura-entrada-ordens-ia.json`` (SetConstruitBatimentSelect -> SetEnginConstruitBatiment for a
  cave at 3093 = (21, 12), the site of probe P3): state 11, +0x7e = +0xb2 = 3093, +0xa4 = 0, +0xbe = 3, with the
  selection list {12}. The bytes are those native changed bytes (new values).
- ``estrutura1``: structure record 1 (free at the pause) declared as a cave under construction where P3's
  CreerBatiment put it: +5 = 2, owner +4 = 0xc8, origin +2 = 2579 = (19, 10), type +8 = 3, progress +0xa,
  damage +6, sound handle +0x100.
- ``construindo``: unit 12 working on structure 1 (+0x89 = 1, +0xc0 = 1) with declared facing, countdown
  +0x8b, animation bytes +0xa4/+0xa5/+0xa7/+0xa9 and sound handle +0x104.
The structure-type limits (type word +4 at 0x495d90 + 52 * type) are read from the paused state by the capture
(``limites``), so progress cases sit exactly below, at and above completion.
"""
import struct

from casos_entrada_ordens_ia import (PACOTE, UNIDADES, caso, celula, entrada, lista, pacote, teclas, u8, u16,
                                     u32)

PASSO = 276
ESTRUTURAS = 0x49a0c8
TIPOS_ESTRUTURA = 0x495d8c           # stride 52; u16 +4 = construction limit
GRUPO = 0x49a05a                     # WndProc's digit key (InputGame's group-number path)
ESTADO_JOGO = 0x4e2f78
ULTIMO_ATAQUE, CELULA_ATAQUE = 0x4e19c0, 0x496acc
BUSCA_UNIDADE = 0x496304
SITIO_P3, ORIGEM_P3 = celula(21, 12), celula(19, 10)

# The committed native result of process_tag4_build_cave (unit 12 = 0x474a8cf0): [offset, new byte].
ORDEM_TAG4 = ((0x02, 11), (0x7e, 21), (0x7f, 12), (0xa4, 0), (0xb2, 21), (0xb3, 12), (0xbe, 3))


def unidade(u, offset, dados):
    return (UNIDADES + u * PASSO + offset, dados)


def estrutura(s, offset, dados):
    return (ESTRUTURAS + s * PASSO + offset, dados)


def ordem_caverna():
    return lista(0, [12]) + [unidade(12, o, u8(v)) for o, v in ORDEM_TAG4] + [unidade(12, 0x104, u32(0xffffffff))]


def estrutura1(progresso, *, dano=0, dono=0xc8, tipo=3, estado=2, som=0xffffffff):
    return [estrutura(1, 5, u8(estado)), estrutura(1, 4, u8(dono)), estrutura(1, 2, u16(ORIGEM_P3)),
            estrutura(1, 8, u8(tipo)), estrutura(1, 0xa, u16(progresso)), estrutura(1, 6, u16(dano)),
            estrutura(1, 0x100, u32(som))]


def construindo(*, f90=3, f91=3, contagem=5, a4=0, a9=0, a5=4, a7=3, som=0xffffffff, local=True):
    """Unit 12 building structure 1 at the P3 site (cell, reserved and target 3093)."""
    w = ordem_caverna() + [unidade(12, 8, u16(SITIO_P3)), unidade(12, 0x7c, u16(SITIO_P3)),
                           unidade(12, 0x7e, u16(SITIO_P3)), unidade(12, 0x86, u8(0) + u8(0)),
                           unidade(12, 0x89, u8(1)), unidade(12, 0xc0, u16(1)), unidade(12, 0x90, u8(f90) + u8(f91)),
                           unidade(12, 0x8b, u8(contagem)), unidade(12, 0xa4, u8(a4) + u8(a5) + u8(4) + u8(a7) +
                                                                  u8(3) + u8(a9)),
                           unidade(12, 0x104, u32(som))]
    if not local:
        w.append(unidade(12, 0, u8(1)))
    return w


def teclas_grupo(ctrl=False, shift=False):
    """GetAsyncKeyState answers of a pass with [0x49a05a] set: Escape, then Ctrl (0x4293e9) and, with Ctrl up,
    Shift (0x429403), then the ordinary key block from Shift (0x429556) on."""
    saida = [(0x1b, 0), (0x11, -0x8000 if ctrl else 0)]
    if not ctrl:
        saida.append((0x10, -0x8000 if shift else 0))
    return saida + [k for k in teclas() if k[0] != 0x1b]


def teclas_enter():
    """Enter held: 0x58 is not polled (0x429776 jumps to GoLastAttaque)."""
    return [(vk, -0x8000 if vk == 0x0d else v) for vk, v in teclas() if vk != 0x58]


def casos(limites):
    """The declared matrix; ``limites`` = {type: u16 construction limit} read at the pause for types 3, 9, 0x11."""
    m3 = limites[3]
    c = []
    # ---------------------------------------------------------------- structure leaves
    c += [caso('en_destruction_built', 'BatimentEnDestruction', EAX=0),
          caso('en_destruction_state3', 'BatimentEnDestruction', estrutura1(10, estado=3), EAX=0xabcd0001),
          caso('en_destruction_state2', 'BatimentEnDestruction', estrutura1(10), EAX=1),
          caso('construit_partial', 'BatimentConstruit', estrutura1(10), EAX=1),
          caso('construit_full', 'BatimentConstruit', estrutura1(m3), EAX=0x55550001),
          caso('construit_over', 'BatimentConstruit', estrutura1(m3 + 1), EAX=1),
          caso('degat_effectif', 'BatimentGetDegatEffectif', estrutura1(10, dano=0x1234), EAX=1),
          caso('construction_step_c8', 'BatimentConstruction', estrutura1(10), EAX=1),
          caso('construction_step_local_sound', 'BatimentConstruction', estrutura1(10, dono=0), EAX=1),
          caso('construction_step_local_busy', 'BatimentConstruction', estrutura1(10, dono=0, som=5), EAX=1),
          caso('construction_complete', 'BatimentConstruction', estrutura1(m3 - 2), EAX=1),
          caso('construction_complete_over', 'BatimentConstruction', estrutura1(m3 - 1), EAX=1),
          caso('construction_complete_type17', 'BatimentConstruction', estrutura1(limites[0x11] - 2, tipo=0x11),
               EAX=1),
          caso('construction_complete_type9', 'BatimentConstruction', estrutura1(limites[9] - 2, tipo=9), EAX=1),
          caso('repare_two', 'BatimentRepare', estrutura1(m3, dano=5), EAX=1),
          caso('repare_one', 'BatimentRepare', estrutura1(m3, dano=1), EAX=1),
          caso('repare_local_sound', 'BatimentRepare', estrutura1(m3, dano=9, dono=0), EAX=1)]
    # ---------------------------------------------------------------- AnimConstruireBatiment (AX unit)
    c += [caso('anim_builder_step', 'AnimConstruireBatiment', construindo(a9=0), EAX=12),
          caso('anim_builder_wrap', 'AnimConstruireBatiment', construindo(a4=3, a9=2), EAX=12),
          caso('anim_builder_idle', 'AnimConstruireBatiment', construindo() + [unidade(12, 0x89, u8(0))], EAX=12),
          caso('anim_builder_phase2', 'AnimConstruireBatiment', construindo() + [unidade(12, 0x89, u8(2))], EAX=12),
          caso('anim_type6_wrap', 'AnimConstruireBatiment', construindo(a4=1, a9=2) + [unidade(12, 1, u8(6))],
               EAX=12),
          caso('anim_type14_wrap', 'AnimConstruireBatiment', construindo(a4=2, a9=2) + [unidade(12, 1, u8(0xe))],
               EAX=12),
          caso('anim_type5', 'AnimConstruireBatiment', construindo() + [unidade(12, 1, u8(5))], EAX=12),
          caso('anim_type9', 'AnimConstruireBatiment', construindo() + [unidade(12, 1, u8(9))], EAX=12)]
    # ---------------------------------------------------------------- CalculConstruireBatiment (AX = 12)
    ccb = lambda nome, escritas: caso(nome, 'CalculConstruireBatiment', escritas, EAX=12)   # noqa: E731
    c += [ccb('ccb_walk_first', ordem_caverna()),
          ccb('ccb_at_target_create', ordem_caverna() + [unidade(12, 8, u16(SITIO_P3)), unidade(12, 0x7c, u16(SITIO_P3)),
                                                          unidade(12, 0x86, u8(0) + u8(0))]),
          ccb('ccb_progress_rotate', construindo(f91=1) + estrutura1(10)),
          ccb('ccb_progress_tick', construindo(contagem=5) + estrutura1(10)),
          ccb('ccb_progress_countdown_a4_1', construindo(contagem=1, a4=1) + estrutura1(10)),
          ccb('ccb_progress_countdown_zero', construindo(contagem=0, a4=1) + estrutura1(10)),
          ccb('ccb_progress_build_step', construindo(contagem=1, a4=2) + estrutura1(10)),
          ccb('ccb_progress_build_step_busy', construindo(contagem=1, a4=2, som=7) + estrutura1(10)),
          ccb('ccb_progress_build_step_other_owner', construindo(contagem=1, a4=2, local=False) + estrutura1(10)),
          ccb('ccb_progress_complete_step', construindo(contagem=1, a4=2) + estrutura1(m3 - 2)),
          ccb('ccb_progress_repair_step', construindo(contagem=1, a4=2) + estrutura1(m3, dano=4)),
          ccb('ccb_progress_built_finish', construindo() + estrutura1(m3)),
          ccb('ccb_progress_built_finish_busy', construindo(som=3) + estrutura1(m3)),
          ccb('ccb_progress_built_finish_search_owner', construindo() + estrutura1(m3) +
              [(BUSCA_UNIDADE, u16(12)), (0x4e0f36, u8(1) + u8(1)), (0x4e0f3c, u32(0x1234))]),
          ccb('ccb_progress_built_wall_queue', construindo() + estrutura1(m3) +
              [unidade(12, 0xbe, u8(9)), unidade(12, 0xd8, u16(3)),
               unidade(12, 0xc4, u16(celula(30, 20)) + u16(celula(31, 20)) + u16(celula(32, 20)))]),
          ccb('ccb_progress_built_wall_queue_search_owner', construindo() + estrutura1(m3) +
              [unidade(12, 0xbe, u8(9)), unidade(12, 0xd8, u16(1)), unidade(12, 0xc4, u16(celula(30, 20))),
               (BUSCA_UNIDADE, u16(12)), (0x4e0f36, u8(1) + u8(1)), (0x4e0f3c, u32(0x1234))]),
          ccb('ccb_progress_built_dead_builder', construindo() + estrutura1(m3) + [unidade(12, 2, u8(4))])]
    # ---------------------------------------------------------------- EnginNextEtape (AX = 12): the state-11 glue
    ene = lambda nome, escritas: caso(nome, 'EnginNextEtape', escritas, EAX=12)   # noqa: E731
    c += [ene('etape11_walk', ordem_caverna()),
          ene('etape11_destroyed', construindo() + estrutura1(10, estado=3)),
          ene('etape11_progress_tick', construindo(contagem=5) + estrutura1(10)),
          ene('etape11_progress_build_step', construindo(contagem=1, a4=2) + estrutura1(10)),
          ene('etape11_no_progress_flag_destroyed', ordem_caverna() + [unidade(12, 0xc0, u16(1))] +
              estrutura1(10, estado=3)),
          ene('etape13_dispatch', ordem_caverna() + [unidade(12, 2, u8(13)), unidade(12, 0xc0, u16(0))])]
    # ---------------------------------------------------------------- BatimentNextEtape type 3 (AX = 1)
    c += [caso('structure_type3_cave', 'BatimentNextEtape', estrutura1(10), EAX=1)]
    # ---------------------------------------------------------------- ProcessInputGame tags (AL = 0)
    pig = lambda nome, escritas: caso(nome, 'ProcessInputGame', escritas, EAX=0)   # noqa: E731
    c += [pig('process_tag11_store_group', lista(0, [12]) + pacote(0xb, 2)),
          pig('process_tag12_restore_group', lista(0, [12]) + pacote(0xc, 1)),
          pig('process_tag16_enter_structure', lista(0, [12]) + pacote(0x10, 3, 0)),
          pig('process_tag16_enter_unit', lista(0, [12]) + pacote(0x10, 1, 13)),
          pig('process_tag16_other', lista(0, [12]) + pacote(0x10, 2, 0)),
          pig('process_tag33_release_colonist', pacote(0x21, 0))]
    # ---------------------------------------------------------------- WndProc key messages (RET 0x10)
    wnd = lambda nome, msg, wp, escritas=(): caso(nome, 'WndProc', list(escritas), stack=[0x1234, msg, wp, 0x20001],
                                                  ret_imm=0x10)   # noqa: E731
    c += [wnd(f'wndproc_keydown_{n}', 0x100, wp) for n, wp in (
        ('digit1', 0x31), ('digit9', 0x39), ('digit0', 0x30), ('letter_a', 0x41), ('letter_x', 0x58),
        ('arrow_left', 0x25), ('space', 0x20), ('f1', 0x70), ('f2', 0x71), ('f3', 0x72), ('f4', 0x73),
        ('f5', 0x74), ('add', 0x6b), ('subtract', 0x6d), ('control', 0x11))]
    c += [wnd('wndproc_keydown_digit1_not_playing', 0x100, 0x31, [(ESTADO_JOGO, u8(0x11))]),
          wnd('wndproc_keydown_f1_not_playing', 0x100, 0x70, [(ESTADO_JOGO, u8(0x11))])]
    c += [wnd(f'wndproc_keyup_{n}', 0x101, wp, e) for n, wp, e in (
        ('f5', 0x74, ()), ('f5_wrap', 0x74, [(0x49a05b, u8(3))]), ('f5_network', 0x74, [(0x4e0730, u8(1))]),
        ('tab', 0x09, ()), ('digit1', 0x31, ()), ('letter_x', 0x58, ()), ('f4', 0x73, ()))]
    # ---------------------------------------------------------------- InputGame passes (AL = player 0)
    ig = lambda nome, escritas, **k: caso(nome, 'InputGame', escritas, EAX=0, **k)   # noqa: E731
    meio = entrada(400, 300, vista=(3, 5))
    c += [ig('input_group1_restore', meio + [(GRUPO, u8(1))], keys=teclas_grupo()),
          ig('input_group3_store_ctrl', meio + [(GRUPO, u8(3))], keys=teclas_grupo(ctrl=True)),
          ig('input_group2_shift_centre', meio + [(GRUPO, u8(2))] + lista(0, [12]), keys=teclas_grupo(shift=True)),
          ig('input_golast_x_recent', meio + [(ULTIMO_ATAQUE, u32(0)), (CELULA_ATAQUE, u16(celula(40, 30)))],
             keys=teclas(0x58)),
          ig('input_golast_enter_recent', meio + [(ULTIMO_ATAQUE, u32(0)), (CELULA_ATAQUE, u16(celula(40, 30)))],
             keys=teclas_enter()),
          ig('input_golast_x_none', meio + [(ULTIMO_ATAQUE, u32(0)), (CELULA_ATAQUE, u16(0xffff))],
             keys=teclas(0x58)),
          ig('input_golast_x_old', meio + [(ULTIMO_ATAQUE, u32(2)), (CELULA_ATAQUE, u16(celula(40, 30)))],
             keys=teclas(0x58)),
          ig('input_golast_x_clamp_low', meio + [(ULTIMO_ATAQUE, u32(0)), (CELULA_ATAQUE, u16(celula(2, 1)))],
             keys=teclas(0x58)),
          ig('input_golast_x_clamp_high', meio + [(ULTIMO_ATAQUE, u32(0)), (CELULA_ATAQUE, u16(celula(63, 63)))],
             keys=teclas(0x58))]
    c += [caso('golast_direct', 'GoLastAttaque', [(ULTIMO_ATAQUE, u32(0)), (CELULA_ATAQUE, u16(celula(40, 30)))],
               EAX=0x508720, EDX=0x508722),
          caso('reseau_actif', 'ReseauActif', [(0x4e0730, u8(1))], EAX=0x12345600)]
    return c


def limites_da_memoria(ler):
    """{type: construction limit} for types 3, 9 and 0x11 from ``ler(address, n) -> bytes`` at the pause."""
    return {t: struct.unpack('<H', ler(TIPOS_ESTRUTURA + 52 * t + 4, 2))[0] for t in (3, 9, 0x11)}


assert PACOTE and UNIDADES   # the pause facts this matrix shares with casos_entrada_ordens_ia
