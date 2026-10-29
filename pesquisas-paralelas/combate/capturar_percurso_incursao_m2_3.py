"""Original-only course of MONDE01's raid units over forced counters 9000..9000+N-1 (M2.3).

Same forced input as `capturar_vida_incursao_m2_3.py`: Missions' committed
v1 path with u32 0x508f7c = 9000 written at frame 1's CalculGame entry, then
whole native frames with the real ProgIteration tail and window loop between
them.  Nothing is isolated; a block hook counts routine entries.  Per frame
the output keeps the routines entered for the first time since startup, the
entry counts of the combat routines, the registers and caller of every entry
of the order/attack routines (KEY), boundary lists that differ from the usual
four, and the raid units' cell, order target and first bytes when they change.
No Python translation is imported.

    python3 -B pesquisas-paralelas/combate/capturar_percurso_incursao_m2_3.py [--quadros 3001]
"""
import argparse
import hashlib
import json
import struct
import sys
import time
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parents[1]
sys.path.insert(0, str(REPO / 'pesquisas-paralelas/missoes'))
import ambiente_missoes  # noqa: E402,F401  (Missions bootstrap: ferramentas, inputs)
import capturar_quadro_missao_original as cq  # noqa: E402
import unicorn  # noqa: E402
from unicorn import x86_const as x86  # noqa: E402

from capturar_isolados_combate_quadro1 import CAPTURA, CONTADOR, HASH, UNIDADES  # noqa: E402
from sondar_vida_incursao import BancadaVida  # noqa: E402

DESTINO = AQUI / 'evidencias/percurso-incursao-m2-3-original.json'
CONTADOR_FORCADO, UNIDADE = 9000, 0x114
UNIDADES_INCURSAO = (16, 17)
COMBATE = ('SetAttaqueEngin', 'CalculAttaqueEngin', 'InfligeDegat', 'ProjectileInit', 'ProjectileSet',
           'ProjectileCalcul', 'ProjectileAvance', 'EnginTrouveCible', 'EnginTrouveCibleScan', 'PlayerEstAllie',
           'PlayerAttaqueReset', 'PlayerAttaqueCalculSympa', 'MAJSympathie', 'iagUnitSendMessage',
           'CreerExplosion', 'EnginInfligeDegat', 'ProjectileInfligeDegat', 'BatimentInfligeDegat',
           'SetDyingEngin', 'DetruireEngin', 'DetruireBatiment')
CHAVE = ('ConstruitGroupeMonstre', 'ProjectileInit', 'Chemin_Accessible', 'StockeAction', 'SetDeplaceEngin',
         'CheminCalcul', 'EnginTrouveCibleScan', 'SetAttaqueEngin', 'CalculAttaqueEngin', 'InfligeDegat',
         'iagUnitSendMessage', 'iagWarDeleteBattle', 'CreerEngin')
FRONTEIRAS_USUAIS = ['AffGame', 'PlaySnd_Manage', 'MCICD_Manage', 'MCICD_Play']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quadros', type=int, default=3001)
    args = ap.parse_args()
    if DESTINO.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {DESTINO}')
    t0 = time.monotonic()
    cap = json.loads(CAPTURA.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaVida(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    simbolos = {b.sym[n]: n for n in b.sym}
    ausentes = sorted(set(COMBATE + CHAVE) - set(b.sym))
    if ausentes:
        raise SystemExit(f'Unknown routine names: {ausentes}')
    contagem, linhas = Counter(), []

    def bloco(cpu, endereco, _tamanho, _):
        nome = simbolos.get(endereco)
        if nome is None:
            return
        contagem[nome] += 1
        if nome in CHAVE:
            esp = cpu.reg_read(x86.UC_X86_REG_ESP)
            retorno = struct.unpack('<I', bytes(cpu.mem_read(esp, 4)))[0]
            regs = [cpu.reg_read(getattr(x86, 'UC_X86_REG_' + r)) for r in ('EAX', 'EDX', 'EBX', 'ECX')]
            linhas.append(' '.join([nome + '@' + b.nome(retorno)] + [f'{v:x}' for v in regs]))

    b.cpu.hook_add(unicorn.UC_HOOK_BLOCK, bloco, begin=0x401000, end=0x493bff)
    b.cpu.ctl_flush_tb()

    def unidades():
        base = struct.unpack('<I', bytes(b.cpu.mem_read(UNIDADES, 4)))[0]
        saida = {}
        for i in UNIDADES_INCURSAO:
            u = bytes(b.cpu.mem_read(base + UNIDADE * i, UNIDADE))
            saida[i] = dict(head=u[:4].hex(), cell=hex(struct.unpack_from('<H', u, 8)[0]),
                            order_target=hex(struct.unpack_from('<H', u, 0x7e)[0]), b7=u[0xb7],
                            b8=hex(struct.unpack_from('<H', u, 0xb8)[0]))
        return saida

    b.executar_cauda_carga(600)
    b.executar_entre_quadros(120)
    vistos = set(contagem)
    contagem.clear()
    linhas.clear()
    if struct.unpack('<I', bytes(b.cpu.mem_read(CONTADOR, 4)))[0] != 1:
        raise RuntimeError('Frame 1 must enter CalculGame with counter 1 before the forced write')
    b.cpu.mem_write(CONTADOR, struct.pack('<I', CONTADOR_FORCADO))
    quadros, totais, anterior, eventos, parada = [], Counter(), unidades(), len(b.eventos_fronteira), None
    try:
        for k in range(1, args.quadros + 1):
            if k > 1:
                b.executar_entre_quadros_k(120, k)
            contador = struct.unpack('<I', bytes(b.cpu.mem_read(CONTADOR, 4)))[0]
            b.executar_quadro(300, k)
            totais.update({n: c for n, c in contagem.items() if n in COMBATE})
            registro = dict(frame=k, counter=contador)
            novos = sorted(set(contagem) - vistos)
            vistos |= set(contagem)
            if novos:
                registro['new_routines'] = novos
            combate = {n: contagem[n] for n in COMBATE if contagem[n]}
            if combate:
                registro['combat_counts'] = combate
            if linhas:
                registro['key_entries'] = list(linhas)
            fronteiras = [e['routine'] for e in b.eventos_fronteira[eventos:]]
            if fronteiras != FRONTEIRAS_USUAIS:
                registro['boundaries'] = fronteiras
            atuais = unidades()
            mudancas = {str(i): v for i, v in atuais.items() if v != anterior[i]}
            if mudancas:
                registro['raid_units'] = mudancas
            quadros.append(registro)
            anterior, eventos = atuais, len(b.eventos_fronteira)
            contagem.clear()
            linhas.clear()
    except Exception as e:  # recorded with the frames reached, then re-raised
        parada = repr(e)
        raise
    finally:
        relatorio = dict(
            schema='rising-lands/monde01-raid-course-forced/1', original_sha256=HASH,
            label=f'forced input: v1 path, u32 0x508f7c = {CONTADOR_FORCADO} at frame 1\'s CalculGame entry, '
                  f'{args.quadros} whole native frames, no isolation', translation_executed=False,
            frame_capture=dict(path=str(CAPTURA.relative_to(REPO)),
                               sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
            source_sha256={s: hashlib.sha256((REPO / p).read_bytes()).hexdigest() for s, p in (
                ('capturar_percurso_incursao_m2_3.py', 'pesquisas-paralelas/combate/capturar_percurso_incursao_m2_3.py'),
                ('sondar_vida_incursao.py', 'pesquisas-paralelas/combate/sondar_vida_incursao.py'),
                ('oraculo_quadro_missao.py', 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py'))},
            stop=parada, frames_requested=args.quadros, combat_totals=dict(sorted(totais.items())),
            never_entered=[n for n in COMBATE if not totais[n]], usual_boundaries=FRONTEIRAS_USUAIS,
            key_entry_format='routine@caller EAX EDX EBX ECX (hex)', code_sha256_after=b.sha256_codigo(),
            frames=quadros, seconds=round(time.monotonic() - t0, 1))
        ok = parada is None and len(quadros) == args.quadros
        saida = DESTINO if ok else REPO / '.local' / ('combat-raid-course-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
        saida.parent.mkdir(parents=True, exist_ok=True)
        with open(saida, 'x') as f:
            json.dump(relatorio, f, indent=1, sort_keys=True)
            f.write('\n')
        print(json.dumps(dict(output=str(saida.relative_to(REPO)), totals=relatorio['combat_totals'],
                              never=relatorio['never_entered'], seconds=relatorio['seconds'])), flush=True)


if __name__ == '__main__':
    main()
