"""Original-only PlayerGetColor 0x46003b calls at counter 9000 (first entered in frame 9000, raid).

PlayerGetColor takes AL and returns EAX; its five callers are 0x468646, 0x469864,
0x46a567, 0x46a592 and 0x46a64f. This capture runs it for every AL with EAX's
upper bits 0 and 0xabcd12, from the display post-load state and from the M2.2
frame-128 checkpoint (``capturar_temporizadores_original``), with the counter
forced to 9000. Inputs are NOT frame inputs. No translation is imported.

    python3 -B pesquisas-paralelas/economia/capturar_cor_jogador_original.py \
        --quadros128 .local/m2-3/captura-quadros128-monde01-exibicao-v2.json.xz \
        --output pesquisas-paralelas/economia/evidencias/captura-cor-jogador-original.json
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import capturar_campos_exibicao_original as campos
import capturar_quadro_m2_original as base
import capturar_temporizadores_original as temporizadores

RAIZ = base.RAIZ
PLAYER_GET_COLOR = 0x46003b


def cenarios(c, prefixo):
    c.recarregar()
    passos = [('contador', 9000)] + [
        ('chamar', f'PlayerGetColor:{alto | al:#x}', PLAYER_GET_COLOR, dict(EAX=alto | al))
        for alto in (0, 0xabcd1200) for al in range(256)]
    return [(f'{prefixo}_all_players', 'PlayerGetColor for every AL, upper EAX bits 0 and 0xabcd12; counter 9000',
             [], passos)]


def capturar(destino, quadros128):
    destino = Path(destino)
    if destino.exists():
        raise FileExistsError('Preserve existing capture; choose a new output')
    if hashlib.sha256((RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()).hexdigest() != base.HASH_EXE:
        raise ValueError('Not the intact executable')
    blocos_s0, resumo_s0, entradas = campos.blocos_exibicao()
    blocos_128, resumo_128 = temporizadores.blocos_quadro128(quadros128)
    resultados = []
    for prefixo, blocos in (('exibicao_s0', blocos_s0), ('quadro128', blocos_128)):
        c = temporizadores.CapturaTemporizadores(blocos)
        resultados += [base.cenario(c, *x) for x in cenarios(c, prefixo)]
        del c
    chamadas = [k for r in resultados for k in r['calls']]
    arquivos = [Path(__file__), Path(temporizadores.__file__), Path(campos.__file__), Path(base.__file__),
                RAIZ / 'ferramentas/emulador.py']
    saida = dict(
        schema='rising-lands/economy-player-color-original-capture/1', sha256_exe=base.HASH_EXE,
        inputs=dict(exibicao_s0=dict(paths=[str(p.relative_to(RAIZ)) for p in entradas],
                                     sha256=[hashlib.sha256(p.read_bytes()).hexdigest() for p in entradas],
                                     state_summary=resumo_s0),
                    quadro128=dict(git_object=':'.join(temporizadores.ORIGEM_QUADROS128),
                                   raw_json_sha256=temporizadores.SHA_QUADROS128, phase='frame128',
                                   state_summary=resumo_128),
                    label='post-load and frame-128 states, counter 9000; NOT frame inputs'),
        source_commit=subprocess.check_output(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], text=True).strip(),
        source_files=[dict(path=str(p.relative_to(RAIZ)), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                      for p in arquivos],
        captured_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        x87_control_word=hex(base.CONTROLE_X87), translation_executed=False,
        stops={hex(a): n for a, n in temporizadores.PARADAS.items()},
        scenarios=len(resultados), original_entries=len(chamadas),
        returns=sum(k['outcome'] == 'return' for k in chamadas),
        dependency_stops=sum(k['outcome'] == 'stop' for k in chamadas), captures=resultados)
    destino.write_text(json.dumps(saida, separators=(',', ':')) + '\n')
    print(f"Captured original-only: {saida['scenarios']} scenarios, {saida['original_entries']} entries, "
          f"{saida['returns']} returns; translation_executed=False.", flush=True)
    return destino


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--quadros128', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    sys.path.insert(0, str(RAIZ / 'ferramentas'))
    from encerramento_captura import encerrar_captura
    encerrar_captura(0, capturar(a.output, a.quadros128))
