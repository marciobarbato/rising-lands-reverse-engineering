"""Original-only capture of MONDE01's first scripted monster raid (M2.3) with a forced counter.

Static trigger (intact bytes, see HANDOFF): AvanceMonstre 0x47b283 stamps the
EntrerMonstre records with u32 0x508f7c on its first call (frame 0, counter
0). Record 0 (cell 0x3f3f, group mask 1, period 9000) is the first with a
non-zero period to satisfy `counter - stamp >= period`, at counter 9000, and
calls ConstruitGroupeMonstre 0x47a81d.

Forced input: Missions' committed first-frame path is rerun with their
read-only `Isolamento` bench. At frame 1's AvanceMonstre entry an extra case
writes u32 0x508f7c = 9000 (every other byte is the exact frame-1 input). The
same frame's ProjectileCalcul entry then gets an extra case with every byte
the forced AvanceMonstre call changed, plus the forced counter. That composes
the two calls; the intervening calls (iaSolver, MessageBoxCalcul,
GameNextFrame, CalculIconeAction) are not applied. All calls run natively;
every routine entry inside the forced cases is recorded with registers and
stack words. No Python translation is imported.

    python3 -B pesquisas-paralelas/combate/capturar_incursao_m2_3.py
"""
import hashlib
import json
import struct
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parents[1]
sys.path.insert(0, str(REPO / 'pesquisas-paralelas/missoes'))
import ambiente_missoes  # noqa: E402,F401  (Missions bootstrap: ferramentas, inputs)
import capturar_quadro_missao_original as cq  # noqa: E402
from oraculo_quadro_missao import BancadaQuadroMissaoOriginal, Isolamento  # noqa: E402
import unicorn  # noqa: E402
from unicorn import x86_const as x86  # noqa: E402

from capturar_isolados_combate_quadro1 import CAPTURA, HASH, empacotar, ler, u32  # noqa: E402

DESTINO = AQUI / 'evidencias/captura-incursao-m2-3-original.json'
CONTADOR, POOL, UNIDADES = 0x508f7c, 0x5080f0, 0x4e19a0
CONTADOR_FORCADO = 9000
ROTINAS = ('AvanceMonstre', 'ProjectileCalcul')
TABELAS = {'monster_header': (0x50a9cc, 4), 'monster_records': (0x50a9d0, 5 * 12),
           'group_actions': (0x50ae80, 4 + 50 * 16), 'pending_attacks': (0x50b134, 4 + 16 * 4),
           'monster_count': (0x50b178, 4), 'probabilities': (0x50a9bc, 16), 'rng': (0x497164, 4)}


def executar():
    cap = json.loads(CAPTURA.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaQuadroMissaoOriginal(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    simbolos = {b.sym[n]: n for n in b.sym}
    entradas_caso, observadas = [], []

    def bloco(cpu, endereco, _tamanho, _):
        if b.fase != 'isolated' or endereco not in simbolos:
            return
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        pilha = struct.unpack('<7I', bytes(cpu.mem_read(esp, 28)))
        regs = [cpu.reg_read(getattr(x86, 'UC_X86_REG_' + r)) for r in ('EAX', 'EDX', 'EBX', 'ECX')]
        entradas_caso.append([simbolos[endereco], b.nome(pilha[0]), *(f'{v:x}' for v in regs),
                              *(f'{v:x}' for v in pilha[1:])])

    b.cpu.hook_add(unicorn.UC_HOOK_BLOCK, bloco, begin=0x401000, end=0x493bff)
    b.cpu.ctl_flush_tb()
    # Non-empty on purpose: Isolamento keeps `perturbacoes or {}`, and the cases are added later.
    perturbacoes = {'(no routine)': []}

    def observador(rotina, fase, caso, antes, resultado):
        entradas = list(entradas_caso)
        entradas_caso.clear()
        registro = dict(routine=rotina, phase=fase, case=caso['case'], entries=entradas,
                        counter=u32(antes, CONTADOR))
        if caso['case'] != 'captured_inputs':
            registro['tables_before'] = {n: ler(antes, a, k).hex() for n, (a, k) in TABELAS.items()}
            registro['pool_before'] = empacotar(ler(antes, u32(antes, POOL), 5600))
        if rotina == 'AvanceMonstre' and fase == 'load_tail':
            perturbacoes['AvanceMonstre'] = [dict(case='forced-counter-9000',
                                                  writes=[(CONTADOR, struct.pack('<I', CONTADOR_FORCADO))],
                                                  registers={})]
        if rotina == 'AvanceMonstre' and caso['case'] == 'forced-counter-9000':
            escritas = [(int(a, 16), bytes([novo])) for a, _velho, novo in resultado['changed_bytes']]
            perturbacoes['ProjectileCalcul'] = [dict(
                case='after-forced-avance-monstre',
                writes=[(CONTADOR, struct.pack('<I', CONTADOR_FORCADO))] + escritas, registers={})]
        observadas.append(registro)

    iso = Isolamento(b, ROTINAS, perturbacoes, observador)
    iso.instalar()
    resumos = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(120)),
                         ('frame1', lambda: b.executar_quadro(600))):
        correr()
        resumos[nome] = b.resumo_imagem(b.imagem())
    fases = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao = dict(phase_states_equal={f: resumos[f] == fases[f] for f in fases},
                      boundaries_equal=b.eventos_fronteira == [e for p in cap['phases'] for e in p['boundaries']],
                      code_unchanged=b.sha256_codigo() == cap['code_integrity']['after'])
    reproducao['passed'] = all(reproducao['phase_states_equal'].values()) and all(
        v for k, v in reproducao.items() if k != 'phase_states_equal')
    casos = [(r, c) for r in iso.registros for c in r['cases']]
    if len(casos) != len(observadas):
        raise RuntimeError('Observer and isolated case records disagree')
    for (r, c), obs in zip(casos, observadas):
        if (r['routine'], c['case']) != (obs['routine'], obs['case']):
            raise RuntimeError('Observer order differs from isolated case order')
        c.update(entries=obs['entries'], counter=obs['counter'])
        for k in ('tables_before', 'pool_before'):
            if k in obs:
                c[k] = obs[k]
    return iso, cap, reproducao


def main():
    if DESTINO.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {DESTINO}')
    t0 = time.monotonic()
    iso, cap, reproducao = executar()
    relatorio = dict(
        schema='rising-lands/monde01-first-raid-forced-capture/1', original_sha256=HASH,
        label='forced input: frame-1 exact state with u32 0x508f7c = 9000', translation_executed=False,
        frame_capture=dict(path=str(CAPTURA.relative_to(REPO)),
                           sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={n: hashlib.sha256((REPO / p).read_bytes()).hexdigest() for n, p in (
            ('capturar_incursao_m2_3.py', 'pesquisas-paralelas/combate/capturar_incursao_m2_3.py'),
            ('oraculo_quadro_missao.py', 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py'))},
        routines=list(ROTINAS), path_reproduction=reproducao, calls=iso.registros,
        entry_format='routine, caller, EAX, EDX, EBX, ECX (hex), then six stack words after the return address',
        method=('Missions Isolamento with dynamic perturbations: the forced AvanceMonstre case is added only '
                'for frame 1, and the ProjectileCalcul case replays every byte that forced call changed. '
                'Each case starts from the exact saved entry state and the state is restored afterwards, so '
                'the committed phases still reproduce.'),
        seconds=round(time.monotonic() - t0, 3))
    forcados = [c['case'] for r in iso.registros for c in r['cases'] if c['case'] != 'captured_inputs']
    ok = (reproducao['passed'] and all(c['reached_return'] for r in iso.registros for c in r['cases'])
          and forcados == ['forced-counter-9000', 'after-forced-avance-monstre'])
    saida = DESTINO if ok else REPO / '.local' / ('combat-raid-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida.relative_to(REPO)), reproduction=reproducao,
                          cases=[(r['routine'], r['phase'], c['case'], len(c['changed_bytes']), len(c['entries']))
                                 for r in iso.registros for c in r['cases']],
                          seconds=relatorio['seconds'])))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
