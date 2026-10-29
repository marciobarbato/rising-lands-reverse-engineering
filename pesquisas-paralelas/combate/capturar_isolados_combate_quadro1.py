"""Original-only isolated captures of the combat frame calls at exact frame-0/1 inputs.

Reruns Missions' committed first-frame path (accepted M1 startup and
MissionLoad, load_tail = frame 0, between_frames, frame1) with Missions'
read-only `oraculo_quadro_missao.Isolamento`, pausing at the combat-relevant
entries. Each call runs natively in isolation on the exact saved state, the
state is restored, and the phase continues; the run must still reproduce every
committed phase state, the entry trace and the boundaries. An observer stores
the exact inputs the Python entries need (pool, unit table, occupancy grid,
alliance masks, attack matrix, counter). No Python translation is imported.

    python3 -B pesquisas-paralelas/combate/capturar_isolados_combate_quadro1.py
"""
import base64
import hashlib
import json
import struct
import sys
import time
import zlib
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parents[1]
sys.path.insert(0, str(REPO / 'pesquisas-paralelas/missoes'))
import ambiente_missoes  # noqa: E402,F401  (Missions bootstrap: ferramentas, inputs)
import capturar_quadro_missao_original as cq  # noqa: E402
from oraculo_quadro_missao import BancadaQuadroMissaoOriginal, Isolamento  # noqa: E402

HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
CAPTURA = REPO / 'pesquisas-paralelas/missoes/evidencias/captura-quadro1-monde01-original.json'
DESTINO = AQUI / 'evidencias/captura-isolada-combate-quadro1.json'
ROTINAS = ('PlayerAttaqueReset', 'ProjectileCalcul', 'EnginTrouveCible', 'PlayerEstAllie',
           'PlayerAttaqueCalculSympa')
CONTADOR, POOL, UNIDADES, GRADE, JOGADORES, MATRIZ = 0x508f7c, 0x5080f0, 0x4e19a0, 0x4e0f38, 0x5080a8, 0x508044
FASES = {'load_tail': 'frame0', 'frame1': 'frame1'}


def ler(blocos, endereco, n):
    for base, dados in blocos.values():
        if base <= endereco and endereco + n <= base + len(dados):
            return bytes(dados[endereco - base:endereco - base + n])
    raise KeyError(f'{endereco:#x}+{n} is not inside one saved block')


def u32(blocos, endereco):
    return struct.unpack('<I', ler(blocos, endereco, 4))[0]


def empacotar(dados):
    return dict(sha256=hashlib.sha256(dados).hexdigest(), bytes=len(dados),
                zlib_base64=base64.b64encode(zlib.compress(dados, 9)).decode())


def entradas_python(rotina, blocos):
    e = dict(counter=u32(blocos, CONTADOR))
    jogadores = u32(blocos, JOGADORES)
    mascaras = bytes(ler(blocos, jogadores + 20 * i + 6, 1)[0] for i in range(5))
    if rotina == 'ProjectileCalcul':
        e['pool'] = empacotar(ler(blocos, u32(blocos, POOL), 5600))
    elif rotina == 'EnginTrouveCible':
        e['units'] = empacotar(ler(blocos, u32(blocos, UNIDADES), 800 * 276))
        e['grid'] = empacotar(ler(blocos, u32(blocos, GRADE), 0x20000))
        e['masks'] = mascaras.hex()
    elif rotina == 'PlayerEstAllie':
        e['masks'] = mascaras.hex()
    elif rotina == 'PlayerAttaqueCalculSympa':
        e['attack_matrix'] = ler(blocos, MATRIZ, 80).hex()
    return e


def executar():
    cap = json.loads(CAPTURA.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaQuadroMissaoOriginal(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    observadas = []

    def observador(rotina, fase, caso, antes, resultado):
        observadas.append(dict(routine=rotina, phase=fase, case=caso['case'],
                               inputs=entradas_python(rotina, antes)))

    iso = Isolamento(b, ROTINAS, None, observador)
    iso.instalar()
    resumos = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(120)),
                         ('frame1', lambda: b.executar_quadro(600))):
        correr()
        resumos[nome] = b.resumo_imagem(b.imagem())
    fases = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao = dict(phase_states_equal={f: resumos[f] == fases[f] for f in fases},
                      entry_trace_equal=json.loads(json.dumps(b.rastro_json())) == cap['entry_trace'],
                      boundaries_equal=b.eventos_fronteira == [e for p in cap['phases'] for e in p['boundaries']],
                      code_unchanged=b.sha256_codigo() == cap['code_integrity']['after'])
    reproducao['passed'] = (all(reproducao['phase_states_equal'].values()) and reproducao['entry_trace_equal']
                            and reproducao['boundaries_equal'] and reproducao['code_unchanged'])
    if len(observadas) != len(iso.registros):
        raise RuntimeError('Observer and isolated call records disagree')
    for registro, obs in zip(iso.registros, observadas):
        if (registro['routine'], registro['phase']) != (obs['routine'], obs['phase']):
            raise RuntimeError('Observer order differs from isolated call order')
        registro['frame'] = FASES.get(registro['phase'], registro['phase'])
        registro['python_inputs'] = obs['inputs']
    return iso, cap, reproducao


def main():
    if DESTINO.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {DESTINO}')
    t0 = time.monotonic()
    iso, cap, reproducao = executar()
    relatorio = dict(
        schema='rising-lands/monde01-frame1-isolated-combat-calls/1', original_sha256=HASH,
        label='exact frame-0/frame-1 inputs (Missions first-frame path)', translation_executed=False,
        frame_capture=dict(path=str(CAPTURA.relative_to(REPO)),
                           sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={n: hashlib.sha256((REPO / p).read_bytes()).hexdigest() for n, p in (
            ('capturar_isolados_combate_quadro1.py', 'pesquisas-paralelas/combate/capturar_isolados_combate_quadro1.py'),
            ('oraculo_quadro_missao.py', 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py'))},
        routines=list(ROTINAS), path_reproduction=reproducao, calls=iso.registros,
        method=('Missions Isolamento: native call from the exact saved entry state to its stack return with '
                'local read/write hooks, state restored afterwards; python_inputs are read from that saved '
                'entry state. Nested entries of listed routines inside an isolated call run natively; the '
                'resumed phase isolates them separately.'),
        seconds=round(time.monotonic() - t0, 3))
    ok = reproducao['passed'] and all(c['reached_return'] for r in iso.registros for c in r['cases'])
    saida = DESTINO if ok else REPO / '.local' / ('combat-isolated-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida.relative_to(REPO)), reproduction=reproducao,
                          calls=[(r['routine'], r['frame'], r['cases'][0]['exit_registers']['EAX'],
                                  len(r['cases'][0]['changed_bytes'])) for r in iso.registros],
                          seconds=relatorio['seconds'])))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
