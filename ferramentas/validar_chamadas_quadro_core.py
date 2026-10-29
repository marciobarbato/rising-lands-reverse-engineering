"""Fresh native differential of the Core frame-0/frame-1 callees at the exact frame inputs.

Reruns the committed first-frame path (``percurso_quadro1``) with
``oraculo_quadro_missao.Isolamento`` at every Core callee entry of both captures
(``capturar_chamadas_core_quadro1`` and ``capturar_zonas_animacao_quadro1``). For each
call the captured inputs and, for the first calls of each routine per phase,
declared perturbations (registers and/or explicit byte writes at the exact
entry state) run natively; an observer then runs the Python translation over
copies of the exact entry blocks (DGROUP+.bss, CRT page, every live allocation,
native stack) and compares every changed byte and the general registers. The
rerun must still reproduce the committed phase states, boundaries and trace.

    python3 -B ferramentas/validar_chamadas_quadro_core.py [--saida relatorios/chamadas-quadro1-emulada.json]
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
import capturar_chamadas_core_quadro1 as cc   # noqa: E402  (adds the Missions folder to sys.path)
from chamadas_quadro_core import ROTINAS, ARGUMENTO_PILHA, DependenciaRamoCore   # noqa: E402
import capturar_zonas_animacao_quadro1 as cz   # noqa: E402
from memoria_quadro_core import MemoriaQuadro   # noqa: E402

REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
TABELA_BONUS, TAMANHO_BONUS = 0x4dfba0, 4 * 26 * 18
ESTRUTURA0 = 0x49a0c8
LIMITE_POR_FASE = 4


def perturbacoes(unidades, descoberta0):
    """Declared native cases per routine; ``unidades`` is the unit pool base u32 [0x4e19a0] and
    ``descoberta0`` owner 0's discovery grid pointer u32 [0x507d78]."""
    r = lambda nome, **regs: dict(case=nome, writes=[], registers=regs)
    w = lambda nome, escritas, **regs: dict(case=nome, writes=escritas, registers=regs)
    u0 = unidades                     # unit 0 record
    estruturas = []
    for tipo in (0, 9, 17, 21, 24, 25):
        for origem in (0x0000, 0x00fe, 0xfe00, 0xffff, 0x8080):
            for jogador in (0, 4):
                estruturas.append(w(f'type{tipo}_origin{origem:04x}_owner{jogador}',
                                    [(ESTRUTURA0 + 8, [tipo]), (ESTRUTURA0 + 2, list(origem.to_bytes(2, 'little')))],
                                    EAX=0, EDX=jogador))
    # Owners 0..7 index 64 KiB grids in both pointer tables (discovery, light, light-count); higher
    # owners alias the attribute/animation pointers and then smaller blocks or the zero slot 15.
    # A footprint cell (row 1, column 1 of a type-0 structure at 0x8080) made "discovered" for owner 0.
    estruturas.append(w('type0_origin8080_owner0_cell8181_bit10_clear',
                        [(ESTRUTURA0 + 8, [0]), (ESTRUTURA0 + 2, [0x80, 0x80]), (descoberta0 + 0x8181, [0])],
                        EAX=0, EDX=0))
    grade = [r('owner0', EDX=0), r('owner4_alias', EDX=4), r('owner7', EDX=0x307), r('owner6', EDX=0x106),
             r('cell_ffff', EAX=0xffff), r('high_bits_owner0', EAX=0x12340f07, EDX=0x5500)]
    return {
        'GetBit': [r('a5_0', EAX=0xffffffa5, EDX=0), r('a5_7', EAX=0xa5, EDX=7), r('a5_8', EAX=0x1a5, EDX=0x108),
                   r('80_31', EAX=0x80, EDX=0x1f), r('80_39', EAX=0x80, EDX=0x27)],
        'SetBit': [r('clear', EBX=0), r('noop', EBX=2), r('set_shift9', EBX=0x101, EDX=9),
                   r('clear_shift35', EBX=0x100, EDX=0x23)],
        'CaseEstDecouverte': grade, 'CaseEstIlluminee': grade,
        'BatimentCollision': [r('type16', EAX=0x16), r('type20_alias15', EAX=0x14), r('high_type21', EAX=0x115),
                              r('high_index', EDX=0xffff0003), r('type9_far', EAX=9, EDX=0x7f)],
        'SetCollision': [r('mask2', EDX=2), r('mask80', EDX=0x80), r('high_cell', EAX=0xabcd0000)],
        'Chemin_ModifieZone': [r('insert_cell0', EAX=0), r('insert_cell8080', EAX=0x8080),
                               r('high_unit', EAX=0x8080, EDX=0x10000),
                               w('insert_class2', [(u0 + 1, [12])], EAX=0x8181, EDX=0)],
        'SetEnginCollision': [w(f'unit0_type{t}', [(u0 + 1, [t])], EAX=0) for t in (3, 11, 16, 17, 25, 0x1a, 0xff)]
                             + [w('unit0_free_cell', [(u0 + 1, [0])], EAX=0, EDX=0x8282)],
        'CalculFatigue': [w(f'unit0_type{t}', [(u0 + 1, [t]), (u0 + 0x72, [1])], EAX=0) for t in (11, 14, 17)]
                         + [w('unit0_inactive', [(u0 + 0x72, [0])], EAX=0),
                            w('counter_bb6', [(u0 + 0x72, [1]), (u0 + 0x74, [0xb6, 0x0b])], EAX=0),
                            w('counter_wrap', [(u0 + 0x72, [1]), (u0 + 0x74, [0xff, 0xff])], EAX=0),
                            w('owner2_f8', [(u0, [2]), (u0 + 0x72, [1]), (u0 + 0xf8, [0x20])], EAX=0)],
        'BatimentGetCase': estruturas, 'BatimentEstDecouvert': estruturas, 'BatimentContourEstIllumine': estruturas,
        'Random': [w('seed_zero', [(0x497164, [0, 0, 0, 0])]), w('seed_max', [(0x497164, [0xff] * 4)])],
        'GameNextFrame': [w('wrap', [(0x496d40, [0xff] * 4)])],
        'SetClipping': [r('high_bits', EAX=0x12345678, EBX=0x9abcdef0, ECX=1, EDX=0xffff)],
        'InitGameZone': [
            w('screen640_480', [(0x49a018, [0x80, 0x02]), (0x49a01a, [0xe0, 0x01])]),
            w('minimap_off', [(0x497285, [0])]),
            w('contact_type1_screen640', [(0x4e2e7c + 0xff, [1]), (0x49a018, [0x80, 0x02]), (0x508726, [15, 0])]),
            w('contact_type2_panel_negative', [(0x4e2e7c + 0xff, [2]), (0x508f90, [0xfe]), (0x508726, [15, 0])]),
            w('contact_type3_market', [(0x4e2e7c + 0xff, [3]), (0x4e2906, [5, 0]), (0x496f80, [7, 0]),
                                       (0x496f7c, [20, 0]), (0x496f7e, [30, 0])]),
            w('contact_self_type2', [(0x4e2928, [1]), (0x4e2e7c, [2]), (0x508f90, [3])]),
            w('message_box_panel_negative', [(0x507d56, [5, 0]), (0x508f90, [0xf0]), (0x508726, [12, 0])]),
            w('alliances', [(0x5080b0 + 4, [1, 0, 0, 0]), (0x5080b0 + 12, [0, 1, 0, 0]), (0x508724, [20, 0]),
                            (0x508726, [15, 0]), (0x508f90, [3])]),
            w('local_player2_alliances', [(0x508041, [2]), (0x5080b0 + 32, [1, 0, 0, 0]), (0x508724, [9, 0])])],
        'MouseSetZone': [r('index256_aliases_test_and_max', EAX=0x100), r('high_bits', EAX=0x10005, EDX=0xffff1234,
                                                                            EBX=0xabcd0001, ECX=0x8000ffff)],
        'MouseTestZone': [r('high_bits', EAX=0x12345678, EDX=0x9abcdef0)],
        'ChercheContacteur': [r('owner1', EAX=1), r('owner3_high', EAX=0x103),
                              w('contacted_self', [(0x4e2928, [1])], EAX=0)],
        'MessageBoxExiste': [w('box_differs_high_eax', [(0x507d56, [0x34, 0x12])], EAX=0xabcd1234)],
        'PlayerEstContacterPourAlliance': [w('owner1_target3', [(0x5080b0 + 16 + 12, [9, 0, 0, 0])],
                                             EAX=0x101, EDX=0x203)],
        'MiniMapGetPos': [w('values', [(0x507d68, [1, 2]), (0x507d6a, [3, 4])])],
        'MiniMapGetTaille': [w('values', [(0x496fe0, [5, 6]), (0x496fe2, [7, 8])])],
        'NextAnimTerrain': [r('high_bits', EAX=0xffff0002, EDX=0x01000005)],
        'NextAnimVeget': [r('high_bits', EAX=0xffff0002, EDX=0x01000005)],
    }


def perturbacoes_exibicao(bancada, base):
    """Display-scenario cases, built from the live bench after MissionLoad (grid pointers, CRT seed).

    ``base``: the v1 cases for the routines both scenarios share (static addresses only).
    Viewport cells 0x806..0x80d (row 8, columns 6..13) lie inside the 25x17 viewport at the
    frame-0 origin (4, 6) and the frame-1 origin (3, 5); 0x604/0x503 are those origins.
    """
    import struct
    u32 = lambda a: struct.unpack('<I', bancada.cpu.mem_read(a, 4))[0]
    tiles, objetos, animacao = u32(0x507d70), u32(0x507d74), u32(0x507dac)
    semente = u32(0x522244) + 0xc
    r = lambda nome, **regs: dict(case=nome, writes=[], registers=regs)
    w = lambda nome, escritas, **regs: dict(case=nome, writes=escritas, registers=regs)
    celulas = range(0x806, 0x80e)
    agua = [(tiles + 2 * c, list(struct.pack('<H', t)))
            for c, t in zip(celulas, (0x5d, 0x94, 0x95, 0x9c, 0x251, 0x252, 0x255, 0x256))]
    agua += [(animacao + 0x80a, [1]), (animacao + 0x80b, [0]), (0x4e1d18, [155])]   # perm[155] % 64 == 0
    queda = [(tiles + 2 * 0x604, [0x8b, 0]), (objetos + 0x604, [0]), (tiles + 2 * 0x503, [0x6d, 0]),
             (objetos + 0x503, [0]), (semente, list(struct.pack('<I', 0x72d)))]      # next rand % 0x400 == 0
    vegetacao = ([(objetos + c, [o]) for c, o in zip(celulas, (1, 0x17, 0x1b, 0x37, 0x38, 0x3a, 0x3e, 0xb))]
                 + [(animacao + c, [a]) for c, a in zip(celulas, (0, 0xe, 0xf, 0xf, 0x3f, 0x3f, 0x1f, 3))]
                 + [(0x4e1d18, [7])])                                                 # perm[7], perm[8] % 4 == 0
    casos = {n: base[n] for n in ('SetClipping', 'InitGameZone', 'MouseSetZone', 'MouseTestZone', 'ChercheContacteur',
                                  'MessageBoxExiste', 'PlayerEstContacterPourAlliance', 'MiniMapGetPos',
                                  'MiniMapGetTaille', 'GameNextFrame', 'Random')}
    casos.update({
        'NextAnimTerrain': [w('tiles_even_counter', agua + [(0x508f7c, [2])]),
                            w('tiles_odd_counter', agua + [(0x508f7c, [3])]),
                            w('object_drop_0x8b_and_0x6d', queda),
                            w('zero_width_high_edi', [(0x508724, [0, 0])], EDI=0xabcd1234),
                            w('zero_rows', [(0x508726, [0, 0])], EDX=0x01000005)],
        'NextAnimVeget': [w('objects_counter0', vegetacao + [(0x508f7c, [0])]),
                          w('objects_counter2', vegetacao + [(0x508f7c, [2])]),
                          w('objects_counter1', vegetacao + [(0x508f7c, [1])]),
                          r('high_ecx', ECX=0xabcd0005),
                          w('zero_width_high_ecx', [(0x508724, [0, 0])], ECX=0x12340005)],
        'LongRand': [w('seed_zero', [(semente, [0, 0, 0, 0])]), w('seed_max', [(semente, [0xff] * 4)])],
        'rand': [w('seed_drop', [(semente, list(struct.pack('<I', 0x72d)))]),
                 w('zero_seed_pointer', [(0x522244, [0xf4, 0xff, 0xff, 0xff])])],
    })
    return casos


class PerturbacoesLimitadas:
    """Hand the declared cases only to the first ``limite`` calls of a routine in each phase."""
    def __init__(self, bancada, casos, limite):
        self.b, self.casos, self.limite, self.vistos = bancada, casos, limite, {}

    def get(self, nome, padrao=()):
        chave = (nome, self.b.fase)
        self.vistos[chave] = self.vistos.get(chave, 0) + 1
        return self.casos.get(nome, padrao) if self.vistos[chave] <= self.limite else padrao


def executar_python(nome, antes, entrada, classe_bonus):
    """Run the translation over copies of the exact entry blocks; returns (changed bytes, registers)."""
    buffers = {n: (base, bytearray(dados)) for n, (base, dados) in antes.items()}
    m = MemoriaQuadro(buffers.values())
    sub = m.u32(entrada['ESP'] + 4) if nome in ARGUMENTO_PILHA else None
    tabela = classe_bonus.da_memoria(m)          # Economy's live bonus table and runtime types (no copy)
    bonus = lambda jogador, tipo, seletor: tabela.consultar(jogador, tipo, seletor)
    saida = ROTINAS[nome][1](m, entrada, sub, bonus)
    mudancas = []
    for n, (base, dados) in buffers.items():
        if n == 'native_stack':
            continue
        velho = antes[n][1]
        if dados != velho:
            mudancas += [[hex(base + i), velho[i], dados[i]] for i in range(len(dados)) if dados[i] != velho[i]]
    return sorted(mudancas, key=lambda x: int(x[0], 16)), dict(entrada, **saida)


def diferencial(limite=LIMITE_POR_FASE, cenario='v1'):
    from integracao.providers import load_economy_bonus
    classe_bonus = load_economy_bonus().BonusUnidades
    registro = dict(comparisons=0, by_routine={}, mismatches=[], dependencies=[], al_by_routine={})
    caixa = {}

    def observador(nome, fase, caso, antes, resultado):
        entrada = {k: int(v, 16) for k, v in resultado['entry_registers'].items()}
        entrada.update(caso['registers'])
        chave = f"{nome}:{caso['case']}"
        try:
            mudancas, regs = executar_python(nome, antes, entrada, classe_bonus)
        except DependenciaRamoCore as e:
            registro['dependencies'].append(dict(routine=nome, phase=fase, case=caso['case'], address=hex(e.endereco)))
            return
        except Exception as e:          # reported as a failing comparison, never ignored
            registro['mismatches'].append(dict(routine=nome, phase=fase, case=caso['case'],
                                               python_error=f'{type(e).__name__}: {e}'))
            return
        nativo = {k: int(v, 16) for k, v in resultado['exit_registers'].items()}
        nativas = sorted(resultado['changed_bytes'], key=lambda x: int(x[0], 16))
        if mudancas != nativas or any(regs[k] != nativo[k] for k in REGISTROS) or not resultado['reached_return']:
            registro['mismatches'].append(dict(
                routine=nome, phase=fase, case=caso['case'], python_changed=mudancas[:20], native_changed=nativas[:20],
                python_registers={k: hex(regs[k]) for k in REGISTROS},
                native_registers={k: hex(nativo[k]) for k in REGISTROS}))
        registro['comparisons'] += 1
        registro['by_routine'][nome] = registro['by_routine'].get(nome, 0) + 1
        al = registro['al_by_routine'].setdefault(nome, {})
        al[str(nativo['EAX'] & 0xff)] = al.get(str(nativo['EAX'] & 0xff), 0) + 1
        if mudancas:
            caixa[nome] = caixa.get(nome, 0) + 1

    captura = json.loads((RAIZ / 'evidencias/fundacoes-quadro/captura-chamadas-quadro1.json').read_bytes())
    primeira = next(c for c in captura['calls'] if c['routine'] == 'SetEnginCollision')
    lidos = {int(a, 16): v for a, v, _ in primeira['read_before_write']}
    unidades = int.from_bytes(bytes(lidos[0x4e19a0 + i] for i in range(4)), 'little')
    from estado_m1_quadro import carregar_m1   # the grid pointers are set by MissionLoad and never move
    descoberta0 = int.from_bytes(carregar_m1()[0][0x507d78 - 0x494000:0x507d7c - 0x494000], 'little')
    import percurso_quadro1 as pq
    casos = perturbacoes(unidades, descoberta0)
    if cenario == 'v1':
        rotinas, limites = cc.ROTINAS + tuple(n for n in cz.ROTINAS if n not in cc.ROTINAS), None
        construir = lambda b: PerturbacoesLimitadas(b, casos, limite)
    else:
        import capturar_exibicao_quadro1 as ce
        rotinas, limites = ce.ROTINAS, ce.LIMITES
        construir = lambda b: PerturbacoesLimitadas(b, perturbacoes_exibicao(b, casos), limite)
    b, iso, cap, reproducao, _ = pq.executar(rotinas, construir, observador, cenario=cenario, limites=limites)
    registro.update(scenario=cenario, path_reproduction=reproducao, calls=len(iso.registros), cases_with_stores=caixa,
                    unit_pool_base=hex(unidades), owner0_discovery_grid=hex(descoberta0),
                    perturbation_limit_per_phase=limite)
    return registro


def main():
    from emulador import HASH_ORIGINAL
    ap = argparse.ArgumentParser()
    ap.add_argument('--cenario', default='v1', choices=('v1', 'exibicao'))
    ap.add_argument('--saida')
    a = ap.parse_args()
    a.saida = a.saida or ('relatorios/chamadas-quadro1-emulada.json' if a.cenario == 'v1'
                          else 'relatorios/chamadas-exibicao-quadro1-emulada.json')
    t0 = time.monotonic()
    r = diferencial(cenario=a.cenario)
    r.update(original_sha256=HASH_ORIGINAL, seconds=round(time.monotonic() - t0, 3),
             source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in (
                 'ferramentas/chamadas_quadro_core.py', 'ferramentas/memoria_quadro_core.py',
                 'ferramentas/validar_chamadas_quadro_core.py')})
    ok = r['path_reproduction']['passed'] and not r['mismatches'] and not r['dependencies']
    saida = RAIZ / a.saida if ok else RAIZ / '.local/frame' / ('chamadas-quadro1-falha-' + time.strftime('%Y%m%dT%H%M%S')
                                                              + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(json.dumps(r, indent=1, sort_keys=True) + '\n')
    print(json.dumps({k: r[k] for k in ('comparisons', 'by_routine', 'path_reproduction', 'calls', 'seconds')}
                     | dict(mismatches=len(r['mismatches']), dependencies=len(r['dependencies']), output=str(saida)),
                     indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
