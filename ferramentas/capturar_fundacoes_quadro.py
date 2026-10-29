"""Original-only captures of Core frame foundations before translation.

Every case starts from the frozen M1 post-load DGROUP/thread blocks (M1 post-load
input, not yet frame-1 input). Cases named ``m1_*`` use those bytes unchanged;
``derived_*`` cases first apply explicit, listed byte overrides to reach edge
values. Steps within a case run sequentially on the evolving native state. Each
step records registers/flags, ordered non-stack writes, stack writes, the
complete DGROUP/thread byte difference and declared clock answers. No Python
translation is executed here.
"""
import hashlib
import json
from pathlib import Path
import struct

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / 'evidencias/fundacoes-quadro/captura-original.json'
SENTINELAS = dict(EAX=0x1111aaaa, EBX=0x2222bbbb, ECX=0x3333cccc, EDX=0x4444dddd,
                  ESI=0x5555eeee, EDI=0x6666ffff, EBP=0x77770000)
FLAGS_CHEIAS, FLAGS_VAZIAS = 0xcd7, 0x2
SEMENTE_MUNDO, SEMENTE_IA, CONTADOR_QUADRO, CONTADORES = 0x497164, 0x498db4, 0x496d40, 0x508f7c
CURSOR, TABELA, SEMENTE_CRT = 0x4e1d18, 0x4e1c18, 0x3400000 + 0xc


def _u32(v):
    return struct.pack('<I', v & 0xffffffff)


def _passo(rotina, eax=None, relogio=None, flags=FLAGS_CHEIAS):
    regs = dict(SENTINELAS, EFLAGS=flags)
    if eax is not None:
        regs['EAX'] = eax & 0xffffffff
    return dict(routine=rotina, registers=regs, clock=relogio)


def casos():
    """(name, overrides [(address, bytes)], steps)."""
    c = []
    # GameNextFrame
    c.append(('m1_game_next_frame_x3', [], [_passo('GameNextFrame', flags=f) for f in
                                            (FLAGS_CHEIAS, FLAGS_VAZIAS, FLAGS_CHEIAS)]))
    c.append(('derived_game_next_frame_wrap', [(CONTADOR_QUADRO, _u32(0xffffffff))],
              [_passo('GameNextFrame'), _passo('GameNextFrame', flags=FLAGS_VAZIAS)]))
    c.append(('derived_game_next_frame_sign', [(CONTADOR_QUADRO, _u32(0x7fffffff))], [_passo('GameNextFrame')]))
    # World Random family
    c.append(('m1_random_x24', [], [_passo('Random', flags=(FLAGS_CHEIAS, FLAGS_VAZIAS)[i % 2]) for i in range(24)]))
    for s in (0, 1, 2, 127772, 127773, 0x7ffffffe, 0x7fffffff, 0x80000000, 0xfffffffe, 0xffffffff, 0x1f31d*0x41a7):
        c.append((f'derived_random_seed_{s:08x}', [(SEMENTE_MUNDO, _u32(s))], [_passo('Random'), _passo('Random')]))
    c.append(('m1_get_random_seed', [], [_passo('GetRandomSeed'), _passo('Random'), _passo('GetRandomSeed')]))
    for v in (0, 1, 0x7ffffffe, 0x7fffffff, 0xffffffff, 0x12345678):
        c.append((f'm1_randomize_{v:08x}', [], [_passo('Randomize', v), _passo('Random')]))
    for v in (0, 1, 0x7ffffffe, 0x7fffffff, 0x80000000, 0xfffffffe, 0xffffffff, 0x4926732e):
        c.append((f'm1_set_random_seed_{v:08x}', [], [_passo('SetRandomSeed', v), _passo('GetRandomSeed'),
                                                       _passo('Random')]))
    # iaRandom: sequential limits over the M1 AI seed, all three paths.
    limites = (1, 2, 3, 5, 7, 10, 16, 100, 1000, 0x7fff, 0x7fffffff, 1, 6, 0x80000000, 0xffffffff, 5,
               0xfffffff0, 9, 0, 4, 0, 13)
    relogios = iter((0x0001d4c0, 0xfffffffe))
    c.append(('m1_ia_random_sequence', [], [_passo('iaRandom', lim, next(relogios) if lim == 0 else None,
                                                   (FLAGS_CHEIAS, FLAGS_VAZIAS)[i % 2])
                                            for i, lim in enumerate(limites)]))
    for s in (0, 1, 0x7fffffff, 0x80000000, 0xffffffff):
        c.append((f'derived_ia_random_seed_{s:08x}', [(SEMENTE_IA, _u32(s))],
                  [_passo('iaRandom', 5), _passo('iaRandom', 0x7fffffff)]))
    for relogio in (0, 0x7ffffffe, 0x7fffffff, 0x80000000, 0xffffffff):
        c.append((f'm1_ia_random_clock_{relogio:08x}', [], [_passo('iaRandom', 0, relogio), _passo('iaRandom', 97)]))
    for lim in (0x80000001, 0x80000000, 0xffffffff, 0x8000ffff):
        c.append((f'm1_ia_random_negative_{lim:08x}', [], [_passo('iaRandom', lim), _passo('iaRandom', 3)]))
    # CRT rand through LongRand
    c.append(('m1_long_rand_x16', [], [_passo('LongRand', flags=(FLAGS_CHEIAS, FLAGS_VAZIAS)[i % 2]) for i in range(16)]))
    for s in (0, 1, 0x7fffffff, 0xffffffff):
        c.append((f'derived_crt_seed_{s:08x}', [(SEMENTE_CRT, _u32(s))], [_passo('LongRand'), _passo('LongRand')]))
    # ProgIteration counter prefix
    c.append(('m1_counter_prefix_x7', [], [_passo('ProgIteration_counter_prefix') for _ in range(7)]))
    for a, b, t in ((0xffffffff, 7, 9), (0xfffffffe, 0xffffffff, 0xffffffff), (5, 0xffffffff, 0xffffffff),
                    (0x7fffffff, 0, 0), (0x80000001, 1, 2)):
        c.append((f'derived_counter_prefix_{a:08x}', [(CONTADORES, _u32(a)+_u32(b)+_u32(t))],
                  [_passo('ProgIteration_counter_prefix'), _passo('ProgIteration_counter_prefix')]))
    # CalculGame load-case counter reset (inline)
    c.append(('m1_load_counter_reset', [], [_passo('CalculGame_load_counter_reset')]))
    c.append(('derived_load_counter_reset_nonzero', [(CONTADORES, _u32(0x11111111)+_u32(0x22222222)+_u32(0x33333333))],
              [_passo('CalculGame_load_counter_reset')]))
    # Permutation cursor through CalculGame's CD branch (inline)
    c.append(('m1_cd_permutation_draw_x5', [], [_passo('CalculGame_cd_permutation_draw') for _ in range(5)]))
    for cur in (0xfe, 0xff, 0x80):
        c.append((f'derived_cd_permutation_cursor_{cur:02x}', [(CURSOR, bytes([cur]))],
                  [_passo('CalculGame_cd_permutation_draw'), _passo('CalculGame_cd_permutation_draw')]))
    return c


def _texto(seg):
    return dict(registers={k: hex(v) for k, v in seg['registers'].items()}, instructions=seg['instructions'],
                state_changes=[[hex(a), b, d] for a, b, d in seg['state_changes']],
                writes=[[hex(a), t, hex(v)] for a, t, v in seg['writes']],
                stack_writes=[[hex(a), t, hex(v)] for a, t, v in seg['stack_writes']], clock=seg['clock'])


def main():
    from bancada_fundacoes_quadro import BancadaFundacoesQuadro, carregar_m1, ROTINAS, DGROUP, THREAD
    from emulador import HASH_ORIGINAL
    dgroup, thread, proveniencia = carregar_m1()
    b = BancadaFundacoesQuadro()
    registros = []
    for nome, sobrescritas, passos in casos():
        b.carregar_estado(dgroup, thread, sobrescritas)
        inicial = b.estado()
        saida = []
        for p in passos:
            seg = b.chamar(p['routine'], p['registers'], relogio=p['clock'])
            saida.append(dict(routine=p['routine'], registers_in={k: hex(v) for k, v in p['registers'].items()},
                              declared_clock=None if p['clock'] is None else hex(p['clock']), **_texto(seg)))
        final = b.estado()
        registros.append(dict(name=nome, input='M1 post-load input, not yet frame-1 input',
                              derived_overrides=[[hex(a), d.hex()] for a, d in sobrescritas],
                              initial_sha256=hashlib.sha256(inicial[0]+inicial[1]).hexdigest(),
                              final_sha256=hashlib.sha256(final[0]+final[1]).hexdigest(), steps=saida))
    hash_final = b.hash_codigo()
    if hash_final != b.hash_codigo_inicial:
        raise RuntimeError('Original code section changed during capture')
    SAIDA.write_text(json.dumps(dict(
        original_sha256=HASH_ORIGINAL, translation_executed=False, m1_input=proveniencia,
        loaded_blocks=dict(dgroup=[hex(DGROUP[0]), hex(DGROUP[1])], crt_thread_data=[hex(THREAD[0]), hex(THREAD[1])]),
        unmapped='GlobalAlloc blocks are not mapped; no case accessed them (an access would fault)',
        routines={k: dict(entry=hex(e), intervals=[[hex(a), hex(z)] for a, z in iv],
                          stop=hex(s) if s else 'return slot') for k, (e, iv, s) in ROTINAS.items()},
        declared_bindings=b.importacoes_declaradas, code_sha256_before=b.hash_codigo_inicial,
        code_sha256_after=hash_final, original_entries=b.entradas_originais, bounded_segments=b.execucoes,
        maximum_native_instructions_per_segment=b.maximo_instrucoes, cases=registros), indent=1) + '\n')
    print(SAIDA, 'cases', len(registros), 'segments', b.execucoes, 'max instructions', b.maximo_instrucoes)


if __name__ == '__main__':
    main()
