"""Original-only capture of RechercheGetNbInvention 0x470554 over the M1 post-load state.

Missions' TestFinDeMission names this query; MONDE01 frames 0/1 do not reach
it. Input: the frozen M1 post-load state (not a frame input), plus declared
overrides of the four invention counts 0x50871c. Every AL value 0..255 runs,
with zero and with nonzero upper EAX bits. No translation is imported.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

import capturar_quadro_m2_original as base

ENTRADA = 0x470554


def capturar(destino):
    destino = Path(destino)
    if destino.exists():
        raise FileExistsError('Preserve existing capture; choose a new output')
    c = base.Captura()
    cenarios = []
    for nome, overrides in (('m1', []), ('m1_override_counts', [(0x50871c, bytes([1, 2, 7, 0xff]))])):
        c.recarregar()
        for a, dados in overrides:
            c.escrever(a, dados)
        inicial = c.sha_estado()
        chamadas = [c.chamar(f'AL={al:#x}:upper={alto:#x}', ENTRADA, dict(EAX=alto | al))
                    for al in range(256) for alto in (0, 0xabcd1200)]
        cenarios.append(dict(name=nome, overrides=[dict(address=hex(a), bytes=d.hex()) for a, d in overrides],
                             initial_state_sha256=inicial, calls=chamadas, final_state_sha256=c.sha_estado()))
    entradas = [k for s in cenarios for k in s['calls']]
    saida = dict(
        schema='rising-lands/economy-research-count-original-capture/1', sha256_exe=base.HASH_EXE,
        input=dict(path=str(base.ENTRADA_M1.relative_to(base.RAIZ)), state_sha256=base.SHA_ESTADO_M1,
                   label='M1 post-load state; NOT a frame input'),
        source_commit=subprocess.check_output(['git', '-C', str(base.RAIZ), 'rev-parse', 'HEAD'], text=True).strip(),
        source_files=[dict(path=str(p.relative_to(base.RAIZ)), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                      for p in (Path(__file__), Path(base.__file__))],
        captured_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), translation_executed=False,
        original_entries=len(entradas), returns=sum(k['outcome'] == 'return' for k in entradas), captures=cenarios)
    destino.write_text(json.dumps(saida, separators=(',', ':')) + '\n')
    print(f"Captured original-only: {saida['original_entries']} entries, {saida['returns']} returns.")


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True)
    capturar(p.parse_args().output)
