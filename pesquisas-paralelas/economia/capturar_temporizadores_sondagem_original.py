"""Original-only timer calls from the real CalculGame-entry states of the display run (frames 50..9000).

Input: the Mac mini gate probe (``sondar_temporizadores_exibicao.py``, run
gate-probe-9000, ``evidencias/sondagem-temporizadores-exibicao-9000.json.xz``):
14 CalculGame-entry states, each rebuilt over the display post-load state and
checked against its summary. They ARE the frames' entry states; every call
below is isolated (the frame's other routines are not run) and the forced
counters of the full timer set are declared, as in ``capturar_temporizadores_original``.
- every state, at its own counter: CalculBatimentNextEtape's structure step
  BatimentNextEtape(0), PlayerInitAllianceCompteur, CalculCompteurMarche and
  CalculCompteurProposition (AL = local player) and PlayerAttaqueCalculSympa,
  in CalculGame order (GetMeteo has no caller and is not run here);
- states 2000/4000/6000/8000/9000: the full forced-counter timer set;
- states 8999/9000: PlayerGetColor for every AL (``capturar_cor_jogador_original``).
No translation is imported.

    python3 -B pesquisas-paralelas/economia/capturar_temporizadores_sondagem_original.py \
        --output pesquisas-paralelas/economia/evidencias/captura-temporizadores-sondagem-original.json
"""
import argparse
import datetime
import hashlib
import json
import lzma
from pathlib import Path
import subprocess
import sys

import capturar_campos_exibicao_original as campos
import capturar_cor_jogador_original as cor
import capturar_quadro_m2_original as base
import capturar_temporizadores_original as t
import sondar_temporizadores_exibicao as sonda

RAIZ = base.RAIZ
SONDAGEM = Path(__file__).resolve().parent / 'evidencias/sondagem-temporizadores-exibicao-9000.json.xz'
COMPLETOS = ('2000', '4000', '6000', '8000', '9000')
CORES = ('8999', '9000')


def estados(blocos_s0):
    """{counter: (name, base, bytes) blocks} of every probe state, each summary-checked."""
    r = json.loads(lzma.decompress(SONDAGEM.read_bytes()))
    return {k: sonda.estado_da_sondagem(blocos_s0, e) for k, e in sorted(r['states'].items(), key=lambda x: int(x[0]))}


def natural(c, k):
    c.recarregar()
    local = c.ler(t.LOCAL, 1)[0]
    contador = int.from_bytes(c.ler(t.CONTADOR, 4), 'little')
    if contador != int(k):
        raise ValueError(f'probe state {k} has counter {contador}')
    return [(f'sondagem{k}_natural', f'Entry state of frame {k}, its own counter: economy timer calls in CalculGame order',
             [], [t.chamada(f'c{k}:BatimentNextEtape:0', t.BATIMENT, dict(EAX=0)),
                  t.chamada(f'c{k}:PlayerInitAllianceCompteur', t.ALLIANCE),
                  t.chamada(f'c{k}:CalculCompteurMarche', t.MARCHE, dict(EAX=local)),
                  t.chamada(f'c{k}:CalculCompteurProposition', t.PROPOSITION, dict(EAX=local, EDX=0)),
                  t.chamada(f'c{k}:PlayerAttaqueCalculSympa', t.SYMPA)])]


def cenarios(c, k):
    s = natural(c, k)
    if k in COMPLETOS:
        s += t.cenarios(c, f'sondagem{k}')
    if k in CORES:
        s += cor.cenarios(c, f'sondagem{k}')
    return s


def capturar(destino):
    destino = Path(destino)
    if destino.exists():
        raise FileExistsError('Preserve existing capture; choose a new output')
    if hashlib.sha256((RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()).hexdigest() != base.HASH_EXE:
        raise ValueError('Not the intact executable')
    blocos_s0, resumo_s0, entradas = campos.blocos_exibicao()
    resultados = []
    for k, blocos in estados(blocos_s0).items():
        c = t.CapturaTemporizadores(blocos)
        resultados += [base.cenario(c, *x) for x in cenarios(c, k)]
        del c
    chamadas = [x for r in resultados for x in r['calls']]
    arquivos = [Path(__file__), Path(t.__file__), Path(cor.__file__), Path(sonda.__file__), Path(campos.__file__),
                Path(base.__file__), RAIZ / 'ferramentas/emulador.py']
    saida = dict(
        schema='rising-lands/economy-timers-probe-states-original-capture/1', sha256_exe=base.HASH_EXE,
        inputs=dict(probe=dict(path=str(SONDAGEM.relative_to(RAIZ)), sha256=hashlib.sha256(SONDAGEM.read_bytes()).hexdigest()),
                    delta_base=dict(paths=[str(p.relative_to(RAIZ)) for p in entradas], state_summary=resumo_s0),
                    label='CalculGame-entry states of the display run; isolated calls, declared forced counters'),
        source_commit=subprocess.check_output(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], text=True).strip(),
        source_files=[dict(path=str(p.relative_to(RAIZ)), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                      for p in arquivos],
        captured_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        x87_control_word=hex(base.CONTROLE_X87), translation_executed=False, stops={hex(a): n for a, n in t.PARADAS.items()},
        scenarios=len(resultados), original_entries=len(chamadas),
        returns=sum(x['outcome'] == 'return' for x in chamadas),
        dependency_stops=sum(x['outcome'] == 'stop' for x in chamadas), captures=resultados)
    destino.write_text(json.dumps(saida, separators=(',', ':')) + '\n')
    print(f"Captured original-only: {saida['scenarios']} scenarios, {saida['original_entries']} entries, "
          f"{saida['returns']} returns, {saida['dependency_stops']} dependency stops; translation_executed=False.",
          flush=True)
    return destino


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    sys.path.insert(0, str(RAIZ / 'ferramentas'))
    from encerramento_captura import encerrar_captura
    encerrar_captura(0, capturar(a.output))
