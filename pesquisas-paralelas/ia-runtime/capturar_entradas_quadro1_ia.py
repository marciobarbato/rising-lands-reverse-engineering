"""Original-only captures of the M2.1 round-3 AI/runtime routines at the exact MONDE01 frame-0/1 inputs.

    python3 -B pesquisas-paralelas/ia-runtime/capturar_entradas_quadro1_ia.py \
        --saida pesquisas-paralelas/ia-runtime/evidencias/captura-entradas-quadro1-ia.json

This replays Missions' committed first-frame path and pauses, without executing
anything extra, at the entry and at the call-return site of every call of
MenuInit (load tail), InputGame, InputSend, CalculIconeAction and EnginNextEtape
(frame 0 and frame 1). For each call it records:
- the entry and exit registers;
- every byte changed between entry and return, with the before/after values;
- the declared bindings and boundary events in between, with their fields;
- every basic block executed while the call is open, nested callees included (the reached path).

The run must reproduce every committed phase state, the entry trace and the
boundaries. No Python translation is imported.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time

from ambiente_ia_runtime import OWNED, ROOT
from bancada_quadro1_ia import CAPTURA_QUADRO, MISSOES, executar_caminho_pausas
from emulador import HASH_ORIGINAL

# routine -> (entry, call-return sites)
ROTINAS = {
    'MenuInit': (0x4682bb, (0x42d2d5,)),
    'InputGame': (0x429278, (0x42d340,)),
    'InputSend': (0x45ec9f, (0x42d347,)),
    'CalculIconeAction': (0x45e944, (0x42d3f0,)),
    'EnginNextEtape': (0x45442c, (0x456eb2,)),
}
INTERVALOS = {'MenuInit': (0x4682bb, 0x469320), 'InputGame': (0x429278, 0x42c31b), 'InputSend': (0x45ec9f, 0x45ecd4),
              'CalculIconeAction': (0x45e944, 0x45ea7c), 'EnginNextEtape': (0x45442c, 0x456c34)}
LABEL = 'exact MONDE01 frame-0/1 input (Missions first-frame path)'


def eventos(b, inicio):
    vinculos = [dict(name=e['name'], arguments=[hex(a & 0xffffffff) for a in e['arguments']],
                     caller_return=e['caller_return'], results={k: hex(v) for k, v in e.get('results', {}).items()},
                     memory_writes=e['memory_writes'])
                for e in b.vinculos_declarados.eventos[inicio[0]:]]
    return vinculos, b.eventos_fronteira[inicio[1]:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    saida = ROOT / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'pesquisas-paralelas/ia-runtime',
                           'pesquisas-paralelas/missoes'], capture_output=True, text=True).stdout
    enderecos, retornos = {}, {}
    for nome, (entrada, sitios) in ROTINAS.items():
        enderecos[entrada] = f'{nome}:entry'
        for s in sitios:
            enderecos[s] = f'{nome}:return'
    abertas, chamadas, executados = {}, [], {}

    def observador(rotulo, fase, regs, b):
        nome, onde = rotulo.split(':')
        if onde == 'entry':
            abertas[nome] = dict(phase=fase, image=b.imagem(), registers=regs,
                                 counts=(len(b.vinculos_declarados.eventos), len(b.eventos_fronteira)),
                                 caller_return=hex(int.from_bytes(bytes(b.cpu.mem_read(regs['ESP'], 4)), 'little')))
            executados[nome] = set()
            return
        if nome not in abertas:
            # 0x456eb2 is also the loop target for skipped (state 0) units: not a return.
            return
        aberta = abertas.pop(nome)
        depois = b.imagem()
        mudados = []
        for n, (base, dados) in depois.items():
            velho = aberta['image'].get(n, (base, None))[1]
            if velho is None:
                mudados.append(dict(block=n, event='allocated'))
            elif velho != dados:
                mudados += [[hex(base + i), velho[i], dados[i]] for i in range(len(dados)) if dados[i] != velho[i]]
        vinculos, fronteiras = eventos(b, aberta['counts'])
        chamadas.append(dict(routine=nome, phase=aberta['phase'], caller_return=aberta['caller_return'],
                             entry_registers={k: hex(v) for k, v in aberta['registers'].items()},
                             exit_registers={k: hex(v) for k, v in regs.items()},
                             entry_state_sha256=b.resumo_imagem(aberta['image'])['sha256'],
                             changed_bytes=mudados, bindings=vinculos, boundaries=fronteiras,
                             executed_blocks=sorted(hex(x) for x in executados.pop(nome))))

    def blocos(fase, endereco):
        # Every block executed while a call is open (its own interval and its nested callees).
        for nome in executados:
            executados[nome].add(endereco)

    t0 = time.monotonic()
    b, cap, reproducao = executar_caminho_pausas(enderecos, observador, blocos)
    relatorio = dict(
        schema='rising-lands/ai-runtime-frame1-entry-return-captures/1', label=LABEL, original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, source_dirty_paths=sujo.splitlines(),
        source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (
            OWNED / 'bancada_quadro1_ia.py', OWNED / 'capturar_entradas_quadro1_ia.py',
            MISSOES / 'oraculo_quadro_missao.py')},
        frame_capture=dict(path=str(CAPTURA_QUADRO.relative_to(ROOT)),
                           sha256=hashlib.sha256(CAPTURA_QUADRO.read_bytes()).hexdigest()),
        routines={n: dict(entry=hex(e), returns=[hex(s) for s in r], interval=[hex(x) for x in INTERVALOS[n]])
                  for n, (e, r) in ROTINAS.items()},
        path_reproduction=reproducao, unclosed=sorted(abertas), calls=chamadas,
        method='Pause at entry and at the call-return site on the uninterrupted original path; full-image diff, '
               'declared binding/boundary log slices, every basic block executed while the call is open',
        seconds=round(time.monotonic() - t0, 3))
    resultado = 0 if reproducao['passed'] and not abertas else 2
    if resultado:
        saida = ROOT / '.local' / ('ai-frame1-entries-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), sha256=hashlib.sha256(saida.read_bytes()).hexdigest(),
                          reproduction=reproducao, unclosed=sorted(abertas),
                          calls=[(c['routine'], c['phase'], len(c['changed_bytes']), len(c['bindings']),
                                  len(c['boundaries']), len(c['executed_blocks'])) for c in chamadas
                                 if c['routine'] != 'EnginNextEtape'],
                          engin=len([c for c in chamadas if c['routine'] == 'EnginNextEtape']),
                          seconds=relatorio['seconds'])))
    return resultado


if __name__ == '__main__':
    sys.exit(main())
