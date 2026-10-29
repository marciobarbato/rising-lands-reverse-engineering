"""Original-only PlayerEstAllie / TestRessource calls with edge players over the display post-load state.

The class forms (``Mercado.aliado``, ``Economia.suficiente``) reject players
outside 0..3; the original does not. This capture runs the intact routines
for every (AL, DL) in {0..5, 0x7f, 0x80, 0xff}² for PlayerEstAllie 0x46d838
(with nonzero upper EAX/EDX bits too) and every player byte in {0..5, 0xff}
for TestRessource 0x4676e5 (RET 4: the player is the stack argument) with
costs at, below and above each total. Inputs: the display post-load state
(``capturar_campos_exibicao_original.blocos_exibicao``) with declared
alliance bytes and resource totals; NOT a frame input. No translation is
imported.

    python3 -B pesquisas-paralelas/economia/capturar_consultas_bordas_exibicao_original.py \
        --output pesquisas-paralelas/economia/evidencias/captura-consultas-bordas-exibicao-original.json
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import struct
import subprocess

import capturar_campos_exibicao_original as campos
import capturar_quadro_m2_original as base

RAIZ = base.RAIZ
PLAYER_EST_ALLIE, TEST_RESSOURCE = 0x46d838, 0x4676e5
JOGADORES, RECURSOS = 0x5080a8, 0x4e2ea8
INDICES = (0, 1, 2, 3, 4, 5, 0x7f, 0x80, 0xff)


def cenarios(c):
    c.recarregar()
    registros = struct.unpack('<I', c.ler(JOGADORES, 4))[0]
    # Declared alliance bytes +6 for records 0..4 (record 4 lies past the four players: the original reads it).
    aliancas = [(registros + 20 * j + 6, bytes([b])) for j, b in enumerate((0x0a, 0x15, 0x1f, 0x00, 0x13))]
    passos = [('chamar', f'PlayerEstAllie:{a:#x}:{d:#x}:{alto:#x}', PLAYER_EST_ALLIE,
               {'EAX': alto | a, 'EDX': alto | d})
              for alto in (0, 0xabcd1200) for a in INDICES for d in INDICES]
    saida = [('alliance_edges', 'PlayerEstAllie over all edge index pairs with declared alliance bytes',
              aliancas, passos)]
    # Totals +2 of records 1 (food), 2 (stone), 0 (parts) for players 0..4 (player 4 is past the table).
    totais = []
    for j in range(5):
        for registro, total in ((1, 50 + j), (2, 0x8000 + j), (0, 7 * j)):
            totais.append((RECURSOS + 32 * j + 8 * registro + 2, struct.pack('<H', total)))
    passos = []
    for jogador in (0, 1, 2, 3, 4, 5, 0xff):
        for comida, pedra, pecas in ((0, 0, 0), (50, 0x8000, 0), (51, 0, 0), (0, 0x8001, 0), (0, 0, 1),
                                     (50 + 4, 0x8004, 28), (0xffff, 0, 0), (0x10032, 0x18000, 0x10000)):
            passos.append(('chamar', f'TestRessource:{jogador:#x}:{comida:#x}:{pedra:#x}:{pecas:#x}', TEST_RESSOURCE,
                           {'EAX': comida, 'EDX': pedra, 'EBX': pecas}, jogador))
    saida.append(('resource_edges', 'TestRessource over edge players and costs with declared totals', totais, passos))
    return saida


def chamar_com_argumento(c, rotulo, entrada, regs, argumento):
    """Call with a callee-popped dword argument above the return address (TestRessource's player byte)."""
    pilha = {4: struct.pack('<I', argumento)}   # [ESP+4] at entry, above the bench return address
    c.escritas.clear()
    c.b.cpu.reg_write(c.x86.UC_X86_REG_FPCW, base.CONTROLE_X87)
    r = c.b.executar(entrada, c.codigo, dict(regs), parada={c.RETORNO, *base.PARADAS}, pilha=pilha,
                     limite_instrucoes=400000)
    resultado = 'return' if r['EIP'] == c.RETORNO else 'stop'
    return dict(call=rotulo, entry=hex(entrada), regs_in={k: hex(v) for k, v in regs.items()},
                stack_argument=hex(argumento), outcome=resultado, regs_out={k: hex(v) for k, v in r.items()},
                writes=list(c.escritas))


def cenario(c, nome, descricao, overrides, passos):
    c.recarregar()
    for a, dados in overrides:
        c.escrever(a, dados)
    inicial = c.sha_estado()
    chamadas = [chamar_com_argumento(c, *p[1:]) if len(p) == 5 else c.chamar(*p[1:]) for p in passos]
    return dict(name=nome, description=descricao,
                overrides=[dict(address=hex(a), bytes=bytes(d).hex()) for a, d in overrides],
                initial_state_sha256=inicial, calls=chamadas, final_state_sha256=c.sha_estado())


def capturar(destino):
    destino = Path(destino)
    if destino.exists():
        raise FileExistsError('Preserve existing capture; choose a new output')
    blocos, resumo, entradas = campos.blocos_exibicao()
    c = campos.CapturaExibicao(blocos)
    resultados = [cenario(c, *x) for x in cenarios(c)]
    chamadas = [k for r in resultados for k in r['calls']]
    arquivos = [Path(__file__), Path(campos.__file__), Path(base.__file__), RAIZ / 'ferramentas/emulador.py']
    saida = dict(
        schema='rising-lands/economy-display-query-edges-original-capture/1', sha256_exe=base.HASH_EXE,
        input=dict(paths=[str(p.relative_to(RAIZ)) for p in entradas],
                   input_sha256=[hashlib.sha256(p.read_bytes()).hexdigest() for p in entradas], state_summary=resumo,
                   label='display-scenario post-load state (MissionLoad return); NOT a frame input'),
        source_commit=subprocess.check_output(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], text=True).strip(),
        source_files=[dict(path=str(p.relative_to(RAIZ)), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                      for p in arquivos],
        captured_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), translation_executed=False,
        scenarios=len(resultados), original_entries=len(chamadas),
        returns=sum(k['outcome'] == 'return' for k in chamadas), captures=resultados)
    destino.write_text(json.dumps(saida, separators=(',', ':')) + '\n')
    print(f"Captured original-only: {saida['scenarios']} scenarios, {saida['original_entries']} entries, "
          f"{saida['returns']} returns; translation_executed=False.")


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True)
    capturar(p.parse_args().output)
