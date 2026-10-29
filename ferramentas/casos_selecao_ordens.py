"""Declared case matrix for the selection and order-setter leaf calls (M3 groundwork).

Every case starts from the exact paused frame-1 state of ``bancada_selecao_ordens`` (MONDE01
display reference, first ProcessInputGame entry). In that state (``relatorios/selecao-ordens-*``):
- every selection list (u16 count at 0x508728 + 0x200*player, entries from +2) is empty;
- the structure selection words 0x495be0 are 0xffff;
- the local player 0x508041 is 0, the cycle counter is 1 and the view is (3, 5, 25, 17);
- units 0..15 belong to player 0. Units 0..2 are soldiers (type 0), 3..10 colonists (type 9, state 14,
  inside the sanctuary), 11 type 1, 12 type 7 (the builder), 13/14 type 5 and 15 type 8. Units 0..2
  and 11..15 are in state 7 and visible; unit records from 16 on are free (state 0);
- structure 0 is the sanctuary (type 2, owner 0, +5 = 5) whose Bag holds units 3..10.

A case only adds declared byte writes (``writes``) and argument registers. Writes that build a
selection list set both the list and each unit's +0xbd flag, the invariant the game maintains.
Importing this module executes nothing.
"""
import struct

PASSO = 276
UNIDADES = 0x474a8000            # [0x4e19a0] at the pause (checked by the capture)
SELECOES = 0x508728
ESTRUTURAS = 0x49a0c8
BUSCA_UNIDADE = 0x496304
JANELA = 0x508720                # u16 view x, y, width, height
DESCOBERTA_0 = 0x507d78          # u32 pointer to player 0's discovery grid (resolved at run time)


def u8(v):
    return bytes([v & 0xff])


def u16(v):
    return struct.pack('<H', v & 0xffff)


def u32(v):
    return struct.pack('<I', v & 0xffffffff)


def campo(unidade, offset, dados):
    return (UNIDADES + unidade * PASSO + offset, dados)


def lista(jogador, unidades, marcar=True, contagem=None):
    """Selection list of ``jogador`` = ``unidades`` (count = len unless ``contagem``), +0xbd = 1 on each."""
    escritas = [(SELECOES + 0x200 * jogador, u16(len(unidades) if contagem is None else contagem) +
                 b''.join(u16(x) for x in unidades))]
    if marcar:
        escritas += [campo(x, 0xbd, u8(1)) for x in unidades]
    return escritas


def estrutura(indice, offset, dados):
    return (ESTRUTURAS + indice * PASSO + offset, dados)


def celula(x, y):
    return (y << 8) | x


def caso(nome, rotina, writes=(), stack=(), ret_imm=0, **regs):
    return dict(case=nome, routine=rotina, registers=regs, writes=list(writes), stack=list(stack), ret_imm=ret_imm)


def casos(grade_descoberta_0):
    """The declared matrix; ``grade_descoberta_0`` is player 0's discovery grid address at the pause."""
    c = []
    # ---------------------------------------------------------------- unit selection
    c += [caso('add_u12_p0', 'EnginAddSelection', EAX=12, EDX=0),
          caso('add_u13_p0', 'EnginAddSelection', EAX=13, EDX=0),
          caso('add_u3_colonist_state14', 'EnginAddSelection', EAX=3, EDX=0),
          caso('add_u16_free', 'EnginAddSelection', EAX=16, EDX=0),
          caso('add_u12_p1_owner_mismatch', 'EnginAddSelection', EAX=12, EDX=1),
          caso('add_u12_already_selected', 'EnginAddSelection', lista(0, [12]), EAX=12, EDX=0),
          caso('add_u12_list_full', 'EnginAddSelection', lista(0, [], contagem=0xff), EAX=12, EDX=0),
          caso('add_u12_invisible', 'EnginAddSelection', [campo(12, 0x72, u8(0))], EAX=12, EDX=0),
          caso('add_u0_after_two', 'EnginAddSelection', lista(0, [12, 13]), EAX=0, EDX=0),
          caso('add_type16_state13_ab32', 'EnginAddSelection',
               [campo(11, 1, u8(0x10)), campo(11, 2, u8(0xd)), campo(11, 0xab, u8(0x32))], EAX=11, EDX=0),
          caso('add_type16_state13_ab0', 'EnginAddSelection',
               [campo(11, 1, u8(0x10)), campo(11, 2, u8(0xd)), campo(11, 0xab, u8(0))], EAX=11, EDX=0),
          caso('add_upper_bits', 'EnginAddSelection', EAX=0x7fff000c, EDX=0x12345600)]
    c += [caso('selectable_u12', 'EnginSelectionnable', EAX=12),
          caso('selectable_u3', 'EnginSelectionnable', EAX=3),
          caso('selectable_u12_invisible', 'EnginSelectionnable', [campo(12, 0x72, u8(0))], EAX=12),
          caso('selectable_type16_state13_ab0', 'EnginSelectionnable',
               [campo(11, 1, u8(0x10)), campo(11, 2, u8(0xd)), campo(11, 0xab, u8(0))], EAX=11)]
    c += [caso('append_u12_p0', 'SelectionAddEngin', EAX=12, EDX=0),
          caso('append_u3_p0_unchecked', 'SelectionAddEngin', EAX=3, EDX=0),
          caso('append_u13_p2', 'SelectionAddEngin', EAX=13, EDX=2),
          caso('append_list_full', 'SelectionAddEngin', lista(0, [], contagem=0xff), EAX=12, EDX=0),
          caso('append_after_three', 'SelectionAddEngin', lista(0, [11, 12, 13]), EAX=14, EDX=0)]
    tres = lista(0, [11, 12, 13])
    c += [caso('remove_middle', 'RetireSelectionEngin', tres, EAX=12, EDX=0),
          caso('remove_first', 'RetireSelectionEngin', tres, EAX=11, EDX=0),
          caso('remove_last', 'RetireSelectionEngin', tres, EAX=13, EDX=0),
          caso('remove_absent', 'RetireSelectionEngin', tres, EAX=14, EDX=0),
          caso('remove_empty_list', 'RetireSelectionEngin', [campo(12, 0xbd, u8(1))], EAX=12, EDX=0),
          caso('remove_duplicate', 'RetireSelectionEngin', lista(0, [12, 12, 13]), EAX=12, EDX=0),
          caso('remove_other_player_list', 'RetireSelectionEngin', lista(3, [12, 13]), EAX=13, EDX=3)]
    c += [caso('deselect_selected', 'DeselectionEngin', lista(0, [12, 13]), EAX=12),
          caso('deselect_unselected', 'DeselectionEngin', lista(0, [12, 13]), EAX=14),
          caso('deselect_flag_only', 'DeselectionEngin', [campo(14, 0xbd, u8(1))], EAX=14)]
    c += [caso('group_deselect_p0', 'DeSelectionGroupe', lista(0, [11, 12, 13, 15]), EAX=0),
          caso('group_deselect_empty', 'DeSelectionGroupe', EAX=0),
          caso('group_deselect_p1', 'DeSelectionGroupe', lista(0, [12]), EAX=1),
          caso('group_deselect_colonist', 'DeSelectionGroupe', lista(0, [3, 12]), EAX=0)]
    c += [caso('deselection_all', 'Deselection', lista(0, [12, 13]) + [(0x495be0, u16(0))], EAX=0)]
    # EnginInZone: AX unit, DX x1, BX y1, CX x2, pushed y2 (RET 4)
    c += [caso('zone_u12_inside', 'EnginInZone', stack=[16], ret_imm=4, EAX=12, EDX=17, EBX=16, ECX=17),
          caso('zone_u12_left', 'EnginInZone', stack=[16], ret_imm=4, EAX=12, EDX=18, EBX=16, ECX=20),
          caso('zone_u12_below', 'EnginInZone', stack=[15], ret_imm=4, EAX=12, EDX=0, EBX=0, ECX=255),
          caso('zone_four_cell_type12', 'EnginInZone', [campo(12, 1, u8(12))], stack=[15], ret_imm=4,
               EAX=12, EDX=16, EBX=15, ECX=16),
          caso('zone_four_cell_origin', 'EnginInZone', [campo(12, 1, u8(12)), campo(12, 8, u16(0))], stack=[0],
               ret_imm=4, EAX=12, EDX=0, EBX=0, ECX=255)]
    # SelectionEngin: AL player, DX corner A, BX corner B
    estado = lambda u, s: campo(u, 2, u8(s))
    c += [caso('box_u12', 'SelectionEngin', EAX=0, EDX=celula(17, 16), EBX=celula(17, 16)),
          caso('box_all_field_units', 'SelectionEngin', EAX=0, EDX=celula(5, 10), EBX=celula(20, 25)),
          caso('box_reversed', 'SelectionEngin', EAX=0, EDX=celula(20, 25), EBX=celula(5, 10)),
          caso('box_x_reversed', 'SelectionEngin', EAX=0, EDX=celula(18, 15), EBX=celula(12, 17)),
          caso('box_empty_area', 'SelectionEngin', EAX=0, EDX=celula(100, 100), EBX=celula(110, 110)),
          caso('box_empty_replaces', 'SelectionEngin', lista(0, [12, 13]), EAX=0, EDX=celula(100, 100),
               EBX=celula(110, 110)),
          caso('box_p1', 'SelectionEngin', EAX=1, EDX=celula(5, 10), EBX=celula(20, 25)),
          caso('box_builder_state11', 'SelectionEngin', [estado(12, 0xb)], EAX=0, EDX=celula(17, 16),
               EBX=celula(17, 16)),
          caso('box_builder_state15', 'SelectionEngin', [estado(12, 0xf)], EAX=0, EDX=celula(17, 16),
               EBX=celula(17, 16)),
          caso('box_sanctuary_colonists', 'SelectionEngin', EAX=0, EDX=celula(12, 11), EBX=celula(15, 13)),
          caso('box_u12_handle_busy', 'SelectionEngin', [campo(12, 0x104, u32(0))], EAX=0, EDX=celula(17, 16),
               EBX=celula(17, 16)),
          caso('box_u12_undiscovered', 'SelectionEngin', [(grade_descoberta_0 + celula(17, 16), u8(1))], EAX=0,
               EDX=celula(17, 16), EBX=celula(17, 16)),
          caso('box_first_type10', 'SelectionEngin', [campo(13, 1, u8(10))], EAX=0, EDX=celula(12, 16),
               EBX=celula(17, 16)),
          caso('box_first_looping_type12', 'SelectionEngin', [campo(13, 1, u8(12))], EAX=0, EDX=celula(12, 15),
               EBX=celula(17, 16)),
          caso('box_list_full', 'SelectionEngin', lista(0, [], contagem=0xff), EAX=0, EDX=celula(5, 10),
               EBX=celula(20, 25)),
          caso('box_selected_reselected', 'SelectionEngin', lista(0, [12, 13]), EAX=0, EDX=celula(12, 16),
               EBX=celula(17, 16))]
    # ---------------------------------------------------------------- structure selection
    sem_tropas = estrutura(0, 0x4e, bytes(16))
    c += [caso('struct_sanctuary', 'BatimentSelection', EAX=0),
          caso('struct_sanctuary_inactive', 'BatimentSelection', [estrutura(0, 5, u8(0))], EAX=0),
          caso('struct_free_slot', 'BatimentSelection', EAX=1),
          caso('struct_type12_owner2', 'BatimentSelection', [estrutura(1, 8, u8(12)), estrutura(1, 4, u8(2))],
               EAX=1),
          caso('struct_sanctuary_empty_bag', 'BatimentSelection', [sem_tropas], EAX=0),
          caso('struct_type5_colonists', 'BatimentSelection', [estrutura(0, 8, u8(5))], EAX=0),
          caso('struct_type5_empty_bag', 'BatimentSelection', [estrutura(0, 8, u8(5)), sem_tropas], EAX=0),
          caso('struct_type21_troops', 'BatimentSelection', [estrutura(0, 8, u8(0x15))], EAX=0),
          caso('struct_type21_empty_bag', 'BatimentSelection', [estrutura(0, 8, u8(0x15)), sem_tropas], EAX=0),
          caso('struct_owner1', 'BatimentSelection', [estrutura(0, 4, u8(1))], EAX=0),
          caso('struct_sound_busy', 'BatimentSelection', [estrutura(0, 0x100, u32(0))], EAX=0),
          caso('struct_deselect_p0', 'BatimentDeselectionner', [(0x495be0, u16(0))], EAX=0),
          caso('struct_deselect_p3', 'BatimentDeselectionner', EAX=3)]
    # ---------------------------------------------------------------- order setters
    destino = celula(20, 16)
    todos = [11, 12, 13, 14, 15, 0, 1, 2]
    c += [caso('move_u12', 'SetDeplaceEnginSelect', lista(0, [12]), EAX=0, EDX=destino),
          caso('move_field_units', 'SetDeplaceEnginSelect', lista(0, todos), EAX=0, EDX=destino),
          caso('move_colonist', 'SetDeplaceEnginSelect', lista(0, [3]), EAX=0, EDX=destino),
          caso('move_free_unit', 'SetDeplaceEnginSelect', lista(0, [16, 12]), EAX=0, EDX=destino),
          caso('move_p1_owner_mismatch', 'SetDeplaceEnginSelect', lista(1, [12]), EAX=1, EDX=destino),
          caso('move_empty', 'SetDeplaceEnginSelect', EAX=0, EDX=destino),
          caso('move_vehicle_first', 'SetDeplaceEnginSelect', lista(0, [12, 13]) + [campo(12, 1, u8(11))], EAX=0,
               EDX=destino),
          caso('move_aerial_first', 'SetDeplaceEnginSelect', lista(0, [12, 13]) + [campo(12, 1, u8(16))], EAX=0,
               EDX=destino),
          caso('move_search_owner', 'SetDeplaceEnginSelect', lista(0, [12]) + [(BUSCA_UNIDADE, u16(12))], EAX=0,
               EDX=destino)]
    c += [caso('attack_unit_mode1', 'SetAttaqueEnginSelect', lista(0, [0]), EAX=0, EDX=1, EBX=12),
          caso('attack_structure_mode3', 'SetAttaqueEnginSelect', lista(0, [0, 1, 2]), EAX=0, EDX=3, EBX=0),
          caso('attack_builder_refused', 'SetAttaqueEnginSelect', lista(0, [12]), EAX=0, EDX=1, EBX=0),
          caso('attack_cell_mode5', 'SetAttaqueEnginSelect', lista(0, [0, 11]), EAX=0, EDX=5, EBX=destino),
          caso('attack_bad_mode', 'SetAttaqueEnginSelect', lista(0, [0]), EAX=0, EDX=2, EBX=12),
          caso('attack_empty', 'SetAttaqueEnginSelect', EAX=0, EDX=1, EBX=12),
          caso('attack_p1_owner_mismatch', 'SetAttaqueEnginSelect', lista(1, [0]), EAX=1, EDX=1, EBX=12)]
    obra = celula(15, 9)
    c += [caso(f'build_type{t}', 'SetConstruitBatimentSelect', lista(0, [12]), EAX=0, EDX=t, EBX=obra)
          for t in (3, 0, 1, 2, 4, 9, 12, 13, 17, 21)]
    c += [caso('build_mixed_selection', 'SetConstruitBatimentSelect', lista(0, [11, 13, 12, 14]), EAX=0, EDX=3,
               EBX=obra),
          caso('build_no_builder', 'SetConstruitBatimentSelect', lista(0, [13]), EAX=0, EDX=3, EBX=obra),
          caso('build_p1_owner_mismatch', 'SetConstruitBatimentSelect', lista(1, [12]), EAX=1, EDX=3, EBX=obra),
          caso('build_two_builders', 'SetConstruitBatimentSelect', lista(0, [12, 13]) + [campo(13, 1, u8(7))],
               EAX=0, EDX=3, EBX=obra),
          caso('build_gate_queue_append', 'SetConstruitBatimentSelect',
               lista(0, [12]) + [campo(12, 2, u8(0xb)), campo(12, 0xbe, u8(9)), campo(12, 0xd8, u16(2))],
               EAX=0, EDX=9, EBX=obra),
          caso('build_gate_queue_full', 'SetConstruitBatimentSelect',
               lista(0, [12]) + [campo(12, 2, u8(0xb)), campo(12, 0xbe, u8(9)), campo(12, 0xd8, u16(10))],
               EAX=0, EDX=9, EBX=obra),
          caso('build_search_owner', 'SetConstruitBatimentSelect', lista(0, [12]) + [(BUSCA_UNIDADE, u16(12))],
               EAX=0, EDX=3, EBX=obra),
          caso('build_origin_cell', 'SetConstruitBatimentSelect', lista(0, [12]), EAX=0, EDX=3, EBX=0)]
    c += [caso('engin_build_unit13', 'SetEnginConstruitBatiment', EAX=13, EDX=3, EBX=obra),
          caso('engin_build_gate_unit12', 'SetEnginConstruitBatiment', EAX=12, EDX=9, EBX=obra),
          caso('engin_build_type12', 'SetEnginConstruitBatiment', EAX=12, EDX=12, EBX=obra)]
    recolha = celula(21, 18)
    c += [caso('harvest_u13', 'SetRecolteEnginSelect', lista(0, [13]), EAX=0, EDX=recolha),
          caso('harvest_three', 'SetRecolteEnginSelect', lista(0, [13, 14, 12]), EAX=0, EDX=recolha),
          caso('harvest_p1_owner_mismatch', 'SetRecolteEnginSelect', lista(1, [13]), EAX=1, EDX=recolha),
          caso('harvest_search_owner', 'SetRecolteEnginSelect', lista(0, [13]) + [(BUSCA_UNIDADE, u16(13))],
               EAX=0, EDX=recolha),
          caso('harvest_free_unit', 'SetRecolteEnginSelect', lista(0, [16, 14]), EAX=0, EDX=recolha),
          caso('engin_harvest_u14', 'SetRecolteEngin', EAX=14, EDX=recolha)]
    c += [caso('transport_u13', 'SetTransporteEnginSelect', lista(0, [13]), EAX=0, EDX=0),
          caso('transport_two', 'SetTransporteEnginSelect', lista(0, [13, 14]), EAX=0, EDX=0x1234),
          caso('transport_p1_list_p0_units', 'SetTransporteEnginSelect', lista(1, [13]), EAX=1, EDX=0),
          caso('transport_free_unit', 'SetTransporteEnginSelect', lista(0, [16, 13]), EAX=0, EDX=0),
          caso('transport_search_owner', 'SetTransporteEnginSelect', lista(0, [13]) + [(BUSCA_UNIDADE, u16(13))],
               EAX=0, EDX=0),
          caso('engin_transport_u14', 'SetTransporteEngin', EAX=14, EDX=0x0203)]
    # Shared Core setters on this state (translated in M2.3; reconfirmed here)
    c += [caso('engin_move_u12', 'SetDeplaceEngin', EAX=12, EDX=destino),
          caso('engin_reset_u13', 'ResetOrdre', EAX=13)]
    # Unit voice request (Core) reached by every setter: AX unit, DX mode, BL flag
    c += [caso('ask_u12_mode8', 'EnginAsk', EAX=12, EDX=8, EBX=0),
          caso('ask_u12_mode16_full_volume', 'EnginAsk', EAX=12, EDX=0x10, EBX=3),
          caso('ask_u12_selected', 'EnginAsk', lista(0, [12]), EAX=12, EDX=0xb, EBX=0),
          caso('ask_u0_view_volume180', 'EnginAsk', [(JANELA, u16(8))], EAX=0, EDX=0x17, EBX=0),
          caso('ask_u0_view_volume100', 'EnginAsk', [(JANELA, u16(15))], EAX=0, EDX=0x17, EBX=0),
          caso('ask_u0_view_volume0', 'EnginAsk', [(JANELA, u16(40))], EAX=0, EDX=0x17, EBX=0),
          caso('ask_u0_view_volume0_mode16', 'EnginAsk', [(JANELA, u16(40))], EAX=0, EDX=0x10, EBX=0),
          caso('ask_u12_handle_busy', 'EnginAsk', [campo(12, 0x104, u32(7))], EAX=12, EDX=8, EBX=1),
          caso('ask_u12_undiscovered', 'EnginAsk', [(grade_descoberta_0 + celula(17, 16), u8(1))], EAX=12, EDX=8,
               EBX=0)]
    nomes = [x['case'] for x in c]
    if len(nomes) != len(set(nomes)):
        raise ValueError('Duplicate case names')
    return c
