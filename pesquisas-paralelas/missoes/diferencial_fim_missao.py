"""Native differential of fim_missao against the intact routines at the MONDE01 frame entries.

Reruns the committed first-frame path with ``Isolamento`` pausing at
EvenementEnCours 0x4581b6 and TestFinDeMission 0x458606 in load_tail and
frame1.  At each pause the intact routine runs on the captured inputs and on
every declared perturbation below; after each native case the Python
translation runs on copies of that case's exact entry bytes.  Compared: AL and
the complete set of changed bytes.  A Python stop at a provider the caller did
not supply is reported per case as a named dependency, never as a pass.

    python3 -B pesquisas-paralelas/missoes/diferencial_fim_missao.py \
        --relatorio pesquisas-paralelas/missoes/validacao/m2-fim-missao-differential-x86.json
"""
import argparse
import hashlib
import json
import struct
import subprocess
import sys
import time

import ambiente_missoes
import capturar_isolados_quadro1 as ci
from economia import Economia
from fim_missao import (CONDICOES, CONTAGEM_INICIAL, DependenciaFimMissao, ESTADO, EVENEMENT, EXERCITOS,
                        EXERCITOS_IA, consultas_publicadas, evento_em_curso, testar_fim_missao)
from oraculo_carga_missao import DGROUP

ESTRUTURAS, RECURSOS, MISSAO, INFLUENCIA = 0x49a0c8, 0x4e2ea8, 0x496fe4, 0x50c614


def u16(v):
    return struct.pack('<H', v)


def total(jogador, recurso):
    """Address of the u16 total of resource 0 (parts) / 1 (food) / 2 (stone) for a player."""
    return RECURSOS + 32*jogador + 8*recurso + 2


def caso(nome, escritas=(), registradores=None):
    return dict(case=nome, writes=[(a, list(d)) for a, d in escritas], registers=registradores or {})


COMIDA50, PEDRA50 = (total(0, 1), u16(50)), (total(0, 2), u16(50))
PERTURBACOES = {
    'TestFinDeMission': [
        caso('food_50', [COMIDA50]),
        caso('food_49', [(total(0, 1), u16(49))]),
        caso('food_and_stone_50', [COMIDA50, PEDRA50]),
        caso('marks_all_set', [(ESTADO+4, b'\x01'*10)]),
        caso('latch_set', [(ESTADO, b'\x01')]),
        caso('first_record_none', [(CONDICOES, b'\xff')]),
        caso('initial_word_zero', [(CONTAGEM_INICIAL, b'\0\0')]),
        caso('victory_without_cave_record', [(CONDICOES, b'\x06'), COMIDA50, PEDRA50]),
        caso('victory_mission8_without_type4_match', [(CONDICOES, b'\x06'), COMIDA50, PEDRA50, (MISSAO, b'\x08')]),
        caso('record3_type2_zero', [(CONDICOES+30, b'\x02\x00\x00\x00')]),
        caso('record3_type0_above', [(CONDICOES+30, b'\x00\x00\x1f\x00')]),
        caso('record3_type7_ignored', [(CONDICOES+30, b'\x07\x00\x00\x00')]),
        caso('record3_type3', [(CONDICOES+30, b'\x03\x00\x00\x00')]),
        caso('record3_type5', [(CONDICOES+30, b'\x05')]),
        caso('mission6', [(MISSAO, b'\x06')]),
        caso('structure0_type3', [(ESTRUTURAS+8, b'\x03')]),
        caso('structure0_owner1', [(ESTRUTURAS+4, b'\x01')]),
        caso('player1', registradores=dict(EAX=1)),
        caso('player1_food_stone_50', [(total(1, 1), u16(50)), (total(1, 2), u16(50))], dict(EAX=1)),
        caso('player0_high_eax_bits', registradores=dict(EAX=0x12345600)),
    ],
    'EvenementEnCours': [caso('event_active', [(EVENEMENT, b'\x01')]), caso('event_0x80', [(EVENEMENT, b'\x80')])],
}


class Comparador:
    def __init__(self):
        self.linhas = []

    def __call__(self, rotina, fase, c, antes, nativo):
        base, d = antes['dgroup']
        if base != DGROUP[0]:
            raise ValueError('Unexpected DGROUP block')
        fatia = lambda a, n: bytearray(d[a-base:a-base+n])
        linha = dict(routine=rotina, phase=fase, case=c['case'], native_al=nativo['al'],
                     native_changed=nativo['changed_bytes'], reached_return=nativo['reached_return'])
        try:
            if rotina == 'EvenementEnCours':
                al, mudados = evento_em_curso(fatia(EVENEMENT, 1)), []
            else:
                estado = fatia(ESTADO, 14)
                anterior = bytes(estado)
                consultas = consultas_publicadas(memoryview(bytes(d[ESTRUTURAS-base:ESTRUTURAS-base+276000])),
                                                 Economia(memoria=fatia(RECURSOS, 128)), fatia(MISSAO, 1),
                                                 fatia(INFLUENCIA, 4000))
                al = testar_fim_missao(c['registers'].get('EAX', int(nativo['entry_registers']['EAX'], 16)),
                                       fatia(CONDICOES, 100), estado,
                                       fatia(CONTAGEM_INICIAL, 2), fatia(EXERCITOS, 8), fatia(EXERCITOS_IA, 16),
                                       consultas)
                mudados = [[hex(ESTADO+i), anterior[i], estado[i]] for i in range(14) if estado[i] != anterior[i]]
            linha.update(python_al=al & 0xff, python_changed=mudados,
                         equal=(al & 0xff) == nativo['al'] and mudados == nativo['changed_bytes'],
                         status='compared')
        except DependenciaFimMissao as erro:
            linha.update(status='python_dependency_stop', dependency=erro.rotina, call=hex(erro.chamada),
                         message=str(erro), equal=None)
        self.linhas.append(linha)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--relatorio', required=True)
    a = ap.parse_args()
    saida = ambiente_missoes.ROOT/a.relatorio
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    t0 = time.monotonic()
    comparador = Comparador()
    perturbacoes = {r: [dict(x, writes=[(a, d) for a, d in x['writes']]) for x in v] for r, v in PERTURBACOES.items()}
    b, iso, cap, reproducao = ci.executar(perturbacoes, comparador)
    linhas = comparador.linhas
    comparados = [x for x in linhas if x['status'] == 'compared']
    paradas = [x for x in linhas if x['status'] != 'compared']
    revisao = subprocess.run(['git', '-C', str(ambiente_missoes.ROOT), 'rev-parse', 'HEAD'],
                             capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ambiente_missoes.ROOT), 'status', '--porcelain', '--',
                           'pesquisas-paralelas/missoes'], capture_output=True, text=True).stdout
    relatorio = dict(
        schema='rising-lands/monde01-fim-missao-native-differential/1', source_revision=revisao,
        source_dirty_paths=sujo.splitlines(),
        source_sha256={n: hashlib.sha256((ambiente_missoes.OWNED/n).read_bytes()).hexdigest()
                       for n in ('fim_missao.py', 'diferencial_fim_missao.py', 'oraculo_quadro_missao.py')},
        path_reproduction=reproducao, cases=len(linhas), compared=len(comparados),
        equal=sum(1 for x in comparados if x['equal']), differing=[x for x in comparados if not x['equal']],
        dependency_stops=[dict(routine=x['routine'], phase=x['phase'], case=x['case'], dependency=x['dependency'],
                               call=x['call'], native_al=x['native_al']) for x in paradas],
        all_native_returned=all(x['reached_return'] for x in linhas), rows=linhas,
        seconds=round(time.monotonic()-t0, 3))
    relatorio['passed'] = (reproducao['passed'] and relatorio['all_native_returned'] and not relatorio['differing']
                           and relatorio['compared'] > 0)
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps({k: v for k, v in relatorio.items() if k != 'rows'}, indent=1)[:8000])
    return 0 if relatorio['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
