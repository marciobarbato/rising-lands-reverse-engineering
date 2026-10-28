"""Original-only Engin_RetrieveExperimente 0x441623 captures before translation.

Each case writes distinct current/saved queues and a distinct neighbourhood,
enters the intact routine with sentinel registers/flags and records registers,
flags, ordered memory writes, the complete 2 MiB image difference and the
stack words. Two provenance chains first run the original saved-buffer
producers (Engin_ResetExperience, Engin_StoreExperimente). No mission data is
loaded and no Python translation is executed here.
"""
import hashlib
import json
from pathlib import Path
import random
import struct

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / 'evidencias/recuperacao-experiencia/captura-original.json'
SENTINELAS = dict(EAX=0x1111aaaa, EBX=0x2222bbbb, ECX=0x3333cccc, EDX=0x4444dddd,
                  ESI=0x5555eeee, EDI=0x6666ffff, EBP=0x77770000)
# CF|PF|AF|ZF|SF|DF|OF plus reserved bit 1; TF/IF are never set.
FLAGS_CHEIAS, FLAGS_VAZIAS = 0xcd7, 0x2


def _aleatorios(semente, n):
    r = random.Random(semente)
    return bytes(r.randrange(256) for _ in range(n))


def _vizinhanca(semente):
    from bancada_recuperacao_experiencia import VIZINHANCA
    return _aleatorios(0x5eed0000 ^ semente, VIZINHANCA[1]-VIZINHANCA[0])


def casos():
    """(name, kind, current, saved, neighbourhood seed, registers, eflags)."""
    crescente = bytes(range(40))
    saida = []
    saida.append(('distinct_words_ascending', 'retrieve', crescente, bytes(0x80+i for i in range(40)), 1,
                  SENTINELAS, FLAGS_CHEIAS))
    saida.append(('distinct_words_descending', 'retrieve', bytes(0xff-i for i in range(40)),
                  bytes(0x40+(39-i) for i in range(40)), 2, SENTINELAS, FLAGS_VAZIAS))
    saida.append(('saved_all_ff_current_zero', 'retrieve', bytes(40), b'\xff'*40, 3, SENTINELAS, FLAGS_CHEIAS))
    saida.append(('saved_zero_current_all_ff', 'retrieve', b'\xff'*40, bytes(40), 4, SENTINELAS, FLAGS_VAZIAS))
    saida.append(('reset_shape_saved_ff00', 'retrieve', _aleatorios(5, 40), b'\xff\x00'*20, 5,
                  SENTINELAS, FLAGS_CHEIAS))
    saida.append(('saved_equals_current', 'retrieve', _aleatorios(6, 40), _aleatorios(6, 40), 6,
                  SENTINELAS, FLAGS_VAZIAS))
    # Per-owner discrimination: only one owner's saved words differ from current.
    for dono in range(4):
        atual = bytearray(_aleatorios(10+dono, 40))
        guardada = bytearray(atual)
        for k in range(10):
            guardada[dono*10+k] ^= 0x5a+k
        saida.append((f'only_owner_{dono}_differs', 'retrieve', bytes(atual), bytes(guardada), 10+dono,
                      SENTINELAS, FLAGS_CHEIAS if dono % 2 else FLAGS_VAZIAS))
    # Word-boundary values: 0x0000, 0x00ff, 0xff00, 0xffff, 0x8000, 0x7fff and 0x0001.
    palavras = (0x0000, 0x00ff, 0xff00, 0xffff, 0x8000, 0x7fff, 0x0001)
    guardada = struct.pack('<20H', *(palavras[i % 7] for i in range(20)))
    saida.append(('boundary_word_values', 'retrieve', _aleatorios(20, 40), guardada, 20, SENTINELAS, FLAGS_CHEIAS))
    # Register-consumption probes: identical memory with extreme register inputs.
    for i, (eax, resto) in enumerate(((0, 0), (0xffffffff, 0xffffffff), (0x28, 0x80000000))):
        regs = {n: (eax if n == 'EAX' else resto ^ (k*0x01010101)) for k, n in enumerate(SENTINELAS)}
        saida.append((f'register_probe_{i}', 'retrieve', _aleatorios(30, 40), _aleatorios(31, 40), 30+i, regs,
                      (FLAGS_VAZIAS, FLAGS_CHEIAS, 0x8d3)[i]))
    for s in range(4):
        saida.append((f'random_{s}', 'retrieve', _aleatorios(100+s, 40), _aleatorios(200+s, 40), 40+s,
                      SENTINELAS, FLAGS_CHEIAS if s % 2 else FLAGS_VAZIAS))
    # Provenance chains: the saved bytes are produced by original producers.
    saida.append(('chain_fresh_campaign_reset', 'reset_then_retrieve', _aleatorios(50, 40), _aleatorios(51, 40),
                  50, SENTINELAS, FLAGS_CHEIAS))
    saida.append(('chain_mission_end_store', 'store_then_retrieve', _aleatorios(60, 40), _aleatorios(61, 40),
                  60, SENTINELAS, FLAGS_VAZIAS))
    return saida


def pool_store(semente=0x570e):
    """Synthetic unit pool for the Store producer: active owners stay 0..3."""
    r = random.Random(semente)
    pool = bytearray(r.randrange(256) for _ in range(220800))
    for i in range(800):
        p = i*276
        estado = r.choice((0, 0, 4, 1, 2, 3, 5, 7, 255))
        pool[p+2] = estado
        if estado not in (0, 4):
            pool[p] = r.randrange(4)
    # Ties and boundary AF values: equal minima, AF 0 and 255.
    for i, (dono, tipo, af) in enumerate(((0, 4, 255), (0, 5, 255), (1, 6, 1), (1, 7, 0), (2, 8, 128))):
        p = (790+i)*276
        pool[p], pool[p+1], pool[p+2], pool[p+0xaf] = dono, tipo, 1, af
    return bytes(pool)


def _texto(seg):
    regs = {k: hex(v) for k, v in seg['registers'].items()}
    return dict(registers=regs, instructions=seg['instructions'],
                image_changes=[[hex(a), b, d] for a, b, d in seg['image_changes']],
                writes=[[hex(a), t, hex(v)] for a, t, v in seg['writes']],
                stack_writes=[[hex(a), t, hex(v)] for a, t, v in seg['stack_writes']])


def _resumo_produtor(seg):
    return dict(registers={k: hex(v) for k, v in seg['registers'].items()}, instructions=seg['instructions'],
                writes=len(seg['writes']), image_changes=len(seg['image_changes']),
                image_changes_sha256=hashlib.sha256(json.dumps(
                    [[a, b, d] for a, b, d in seg['image_changes']]).encode()).hexdigest())


def main():
    from bancada_recuperacao_experiencia import (BancadaRecuperacaoExperiencia, ATUAL, GUARDADA, FIM,
                                                VIZINHANCA)
    from emulador import HASH_ORIGINAL
    b = BancadaRecuperacaoExperiencia()
    registros = []
    for nome, tipo, atual, guardada, semente, regs, flags in casos():
        b.carregar(atual, guardada, _vizinhanca(semente))
        entrada = dict(regs, EFLAGS=flags)
        produtor = None
        if tipo == 'reset_then_retrieve':
            produtor = dict(entry='0x441470', name='Engin_ResetExperience',
                            **_resumo_produtor(b.resetar(dict(SENTINELAS, EFLAGS=FLAGS_VAZIAS))))
        elif tipo == 'store_then_retrieve':
            pool = pool_store()
            b.carregar_unidades(pool)
            produtor = dict(entry='0x4414f8', name='Engin_StoreExperimente',
                            unit_pool_sha256=hashlib.sha256(pool).hexdigest(),
                            **_resumo_produtor(b.armazenar(dict(SENTINELAS, EFLAGS=FLAGS_VAZIAS))))
        antes = dict(current=b.ler(ATUAL, GUARDADA).hex(), saved=b.ler(GUARDADA, FIM).hex(),
                     neighbourhood=b.ler(*VIZINHANCA).hex())
        seg = b.recuperar(entrada)
        depois = dict(current=b.ler(ATUAL, GUARDADA).hex(), saved=b.ler(GUARDADA, FIM).hex(),
                      neighbourhood=b.ler(*VIZINHANCA).hex())
        registros.append(dict(name=nome, kind=tipo, neighbourhood_seed=semente,
                              registers_in={k: hex(v) for k, v in entrada.items()},
                              producer=produtor, before=antes, after=depois, retrieve=_texto(seg)))
    SAIDA.write_text(json.dumps(dict(
        original_sha256=HASH_ORIGINAL, translation_executed=False,
        routine=dict(name='Engin_RetrieveExperimente', entry='0x441623', intervals=[['0x441623', '0x441659'],
                                                                                 ['0x440d59', '0x440d5e']]),
        neighbourhood=[hex(VIZINHANCA[0]), hex(VIZINHANCA[1])], image=['0x400000', '0x600000'],
        stack_return_slot=hex(0x2008000), original_entries=b.entradas_originais, bounded_segments=b.execucoes,
        maximum_native_instructions_per_segment=b.maximo_instrucoes, cases=registros,
        scope='Original-only intact routine over synthetic discriminating queues plus two original-producer '
              'chains (fresh-campaign reset, mission-end store over a synthetic pool). No MONDE01 memory '
              'snapshot of these buffers exists; no Python translation, binding or patch was used.'),
        indent=1) + '\n')
    print(SAIDA, 'cases', len(registros), 'segments', b.execucoes, 'max instructions', b.maximo_instrucoes)


if __name__ == '__main__':
    main()
