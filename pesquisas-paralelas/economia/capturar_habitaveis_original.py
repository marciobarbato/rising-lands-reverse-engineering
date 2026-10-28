"""Original-only Stage 15 captures, recorded before any Python translation.

Each case runs the intact executable on core's harness and stores whole-buffer
hashes, the ordered parent-call trace and core effect trace. Requires Unicorn.
"""
import hashlib
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
sys.dont_write_bytecode = True
for caminho in (RAIZ/'ferramentas', PASTA):
    sys.path.insert(0, str(caminho))
import casos_habitaveis as casos
from bancada_habitaveis import BancadaHabitaveis
from emulador import HASH_ORIGINAL


def _casos():
    yield 'caller', casos.caso_monde01('MONDE01 zero tables')
    yield 'caller', casos.caso_monde01('MONDE01 seeded tables/grids', padrao='aleatorio', semear_grades=True)
    yield 'habitable', casos.caso_monde01('MONDE01 all-one tables', padrao='um')
    for tipo, dono, origem in ((0, 1, 0x8080), (2, 0, 0x0000), (3, 2, 0xf0f0), (4, 3, 0x40fa), (5, 0, 0xfa05),
                               (6, 1, 0x2020), (9, 2, 0x3030), (12, 0, 0x5050), (15, 0, 0x6060),
                               (17, 3, 0x7070), (20, 1, 0x9090), (21, 2, 0xa0a0)):
        yield 'habitable', casos.caso_sintetico(f'type {tipo} owner {dono}', tipo, dono, origem,
                                               padrao='um' if tipo in (15, 20) else 'aleatorio',
                                               armazens=(3, 40) if tipo == 3 else None, semente=tipo)
    yield 'habitable_owner4_stop', casos.caso_sintetico('type 2 owner 4', 2, 4, 0x8080)
    for tipo, unidades, tipos_unidades in ((2, (10, 11), (3, 9)), (2, (12,), (25,)), (21, (13,), (9,)),
                                           (21, (14,), (17,)), (1, (15, 16), (9, 4)), (16, (), ())):
        yield 'predicate', casos.caso_sintetico(f'predicate type {tipo} {tipos_unidades}', tipo, 0, 0x4040,
                                               unidades=unidades, tipos_unidades=tipos_unidades)


def capturar():
    bancada = BancadaHabitaveis()
    resultados = []
    for modo, caso in _casos():
        bancada.carregar(caso)
        antes = bancada.resumo()
        if modo == 'caller':
            regs = bancada.varrer_estrutura(caso.indice)
        elif modo == 'predicate':
            regs = bancada.esta_habitada(caso.indice)
        elif modo == 'habitable_owner4_stop':
            regs = bancada.tornar_habitavel(caso.indice, paradas=(0x476851,))
        else:
            regs = bancada.tornar_habitavel(caso.indice)
        resultados.append(dict(name=caso.nome, origin=caso.origem, mode=modo, index=caso.indice,
                               eip=hex(regs['EIP']), al=regs['EAX'] & 255,
                               input=antes['sha256'], output=bancada.resumo()))
    return dict(sha256_exe=HASH_ORIGINAL, captured_before_translation=True,
                scope='Original-only BatimentEstHabiter/BatimentHabitable and MissionPlaceTerrain 0x46c195..0x46c1a7; '
                      'whole mapped buffers hashed before and after; no Python reconstruction consulted',
                entries=bancada.entradas, bounded_segments=bancada.execucoes,
                minimap_resumes=bancada.retomadas_minimapa, stops=dict(bancada.paradas_atingidas),
                cases=resultados)


if __name__ == '__main__':
    r = capturar()
    (PASTA/'evidencias/captura-habitaveis-original.json').write_text(json.dumps(r, indent=2)+'\n')
    print('Original entries:', r['entries'], 'segments:', r['bounded_segments'], 'resumes:', r['minimap_resumes'])
