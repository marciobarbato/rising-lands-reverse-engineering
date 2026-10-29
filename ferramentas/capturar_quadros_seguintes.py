"""Original-only isolated captures over the display-reference frames 0..128 (M2 round 5).

Runs the committed Missions display reference (``cenarios_oraculo`` 'exibicao'),
reproduces frames 0/1 against its v2 capture, then keeps the real loop running
with the same declared inputs until the frame whose cycle counter u32 0x508f7c
is 128 (see ``levantar_quadros_exibicao``). Missions' ``Isolamento`` pauses at:

* NextAnimTerrain / NextAnimVeget in every frame (records kept for the sampled
  frames and for every frame in which they change more than the CRT seed and
  the permutation cursor);
* InitGameZone (frame 0), with declared mode perturbations EAX = 2, 3, 4 (the
  menu modes; MissionGetNum >= 7 and < 7 for mode 2) and 0, 5 (invalid modes);
* NextAnimVegetFullMap as a *foreign entry* - network games only, never called
  in single player - run natively from NextAnimVeget's exact paused state in
  frames 1, 2, 64 and 128 (the state at the network-only call site 0x42d44f is
  the same: both follow NextAnimTerrain), with its own counter-parity cases;
* in the sampled frames, the Core queries the display path (AffGame) calls
  between frames - TerrainEstDecouvert, TerrainEstIllumine, ExisteEngin,
  EnginGetType, EnginGetPlayer, EnginEstArmure, EnginEstMiroir,
  EnginEstTerreur, TypeEnginSeFatigue - and GameNextFrame, Random, LongRand, rand.

Each kept case records registers, changed bytes, bytes read before written and
the executed native blocks. No Python translation is imported.

    python3 -B ferramentas/capturar_quadros_seguintes.py \
        --saida evidencias/fundacoes-quadro/captura-quadros-seguintes.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
AMOSTRAS = (1, 2, 3, 4, 17, 45, 64, 127, 128)
FULLMAP = (1, 2, 64, 128)
CONSULTAS = ('TerrainEstDecouvert', 'TerrainEstIllumine', 'ExisteEngin', 'EnginGetType', 'EnginGetPlayer',
             'EnginEstArmure', 'EnginEstMiroir', 'EnginEstTerreur', 'TypeEnginSeFatigue')
AMOSTRADAS = CONSULTAS + ('GameNextFrame', 'Random', 'LongRand', 'rand')
SEMPRE = ('NextAnimTerrain', 'NextAnimVeget', 'InitGameZone', 'MouseSetZone', 'MouseTestZone', 'MissionGetNum',
          'MenuGetNbItem')
ROTINAS = SEMPRE + AMOSTRADAS
LIMITE_AMOSTRA = {**{n: 2 for n in CONSULTAS}, 'GameNextFrame': 1, 'Random': 1, 'LongRand': 2, 'rand': 2,
                  'MouseSetZone': 2}


def perturbacoes(bancada):
    r = lambda nome, **regs: dict(case=nome, writes=[], registers=regs)
    w = lambda nome, escritas, **regs: dict(case=nome, writes=escritas, registers=regs)
    return {
        'InitGameZone': [r('mode2_mission1', EAX=2), w('mode2_mission7', [(0x496fe4, [7])], EAX=2),
                         r('mode3_menu_items', EAX=3), w('mode3_five_items', [(0x4e2f40, [5, 0])], EAX=3),
                         w('mode3_no_items', [(0x4e2f40, [0, 0])], EAX=3, EBX=0x12345678, ECX=0x9abcdef0),
                         r('mode4', EAX=4), r('mode0_invalid', EAX=0), r('mode5_invalid', EAX=0xabcd0005)],
        'NextAnimVegetFullMap': [w('counter0', [(0x508f7c, [0])]), w('counter2', [(0x508f7c, [2])]),
                                 w('counter1', [(0x508f7c, [1])])],
    }


def interessante(caso):
    """A NextAnim* case that changes more than the CRT seed (thread page) and the cursor."""
    return any(not (0x3400000 <= int(a, 16) < 0x3401000) and int(a, 16) != 0x4e1d18 for a, _, _ in caso['changed_bytes'])


def main():
    import percurso_quadro1 as pq
    import cenarios_oraculo
    from emulador import HASH_ORIGINAL
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--ate', type=int, default=128)
    a = ap.parse_args()
    saida = RAIZ / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    t0 = time.monotonic()
    b, cap = pq._bancada('exibicao')
    blocos = []
    cobertura = pq.Cobertura(b, sob_demanda=True)      # hooked only around isolated calls
    # Each case's native blocks and the frame index current while it ran.
    observador = lambda nome, fase, caso, antes, resultado: blocos.append((cobertura.drenar(), iso.quadro))
    limites = dict(LIMITE_AMOSTRA)
    iso = pq._isolamento_limitado(b, ROTINAS, perturbacoes(b), observador, limites,
                                  {'NextAnimVeget': ('NextAnimVegetFullMap', lambda i: i.quadro in FULLMAP)}, cobertura)
    iso.instalar()
    referencia = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao = {}

    def amostrar(k):
        for n in AMOSTRADAS:
            limites[n] = LIMITE_AMOSTRA[n] if k in AMOSTRAS else 0

    iso.quadro = 0
    amostrar(0)
    b.executar_cauda_carga(600)
    reproducao['load_tail'] = b.resumo_imagem(b.imagem()) == referencia['load_tail']
    iso.quadro = 1
    amostrar(1)
    b.executar_entre_quadros(300)
    reproducao['between_frames'] = b.resumo_imagem(b.imagem()) == referencia['between_frames']
    b.executar_quadro(600)
    reproducao['frame1'] = b.resumo_imagem(b.imagem()) == referencia['frame1']
    reproducao['entry_trace_equal'] = json.loads(json.dumps(b.rastro_json())) == cap['entry_trace']
    contador = lambda: int.from_bytes(bytes(b.cpu.mem_read(0x508f7c, 4)), 'little')
    k = 1
    while contador() < a.ate:
        k += 1
        iso.quadro = k
        amostrar(k)
        b.executar_entre_quadros(300)
        b.executar_quadro(600)
    # Flatten: one record per case, with its frame and native blocks; NextAnim* records are kept only
    # for the sampled frames, frame 0 and every frame in which they change more than seed/cursor.
    guardadas, i = [], 0
    for registro in iso.registros:
        for caso in registro['cases']:
            blocos_caso, quadro = blocos[i]
            i += 1
            c = dict(routine=registro['routine'], entry=registro['entry'], phase=registro['phase'], frame=quadro,
                     caller=registro['caller'], caller_return=registro['caller_return'], **caso,
                     native_blocks=[hex(x) for x in blocos_caso])
            if (c['routine'] in ('NextAnimTerrain', 'NextAnimVeget') and quadro not in AMOSTRAS + (0,)
                    and not interessante(c)):
                continue
            guardadas.append(c)
    contagem = {}
    for c in guardadas:
        contagem[c['routine']] = contagem.get(c['routine'], 0) + 1
    relatorio = dict(
        schema='rising-lands/monde01-display-frames-isolated-core-calls/1', original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, scenario='exibicao',
        reference=dict(path=str(cenarios_oraculo.caminho('exibicao', 'captura_quadro').relative_to(RAIZ)),
                       sha256=hashlib.sha256(cenarios_oraculo.caminho('exibicao', 'captura_quadro').read_bytes())
                       .hexdigest()),
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest()
                       for p in ('ferramentas/capturar_quadros_seguintes.py', 'ferramentas/percurso_quadro1.py',
                                 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py')},
        inputs='display-reference named inputs; later frames keep the declared no-input answers',
        reproduction_frames_0_1=reproducao, frames_run=k, stop_counter=a.ate, sampled_frames=list(AMOSTRAS),
        fullmap_foreign_entry_frames=list(FULLMAP),
        foreign_entry='NextAnimVegetFullMap is called only at 0x42d44f when [0x4e0730] (network) is set; its '
                      'records run the intact routine from NextAnimVeget\'s exact paused state (same state, '
                      'both follow NextAnimTerrain); caller fields name that pause',
        isolated_entries={f'{n}:{f}:{q}': v for (n, f, q), v in sorted(iso.vistos.items(), key=str)},
        kept_counts=contagem, code_unchanged=b.sha256_codigo() == cap['code_integrity']['after'],
        calls=guardadas, seconds=round(time.monotonic() - t0, 3))
    ok = all(reproducao.values()) and relatorio['code_unchanged'] and all(c['reached_return'] for c in guardadas)
    if not ok:
        saida = RAIZ / '.local/frame' / ('quadros-seguintes-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), sha256=hashlib.sha256(saida.read_bytes()).hexdigest(),
                          reproduction=reproducao, frames=k, kept=contagem, seconds=relatorio['seconds']), indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
