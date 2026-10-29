"""Original-only long run of the MONDE01 display reference recording Economy's gate inputs (Mac mini).

Core's coverage run (``ferramentas/cobrir_quadros_exibicao.py``, runs/core/coverage-9200)
says which routines frames 129..9,200 enter, not which branches inside them run.
This run builds the same Missions display bench, checks frames 0/1 against the
display reference, then runs the real loop with the declared no-input answers
(display clock 0x123456 + 40k extended, as Core's run) and records:
- every frame: the counter and, for each watched Economy gate input
  (``VIGIADOS``, plus the player records through [0x5080a8] and the list of live
  structures), its bytes whenever they differ from the previous frame;
- at every frame in ``--estados``: the full state at that frame's CalculGame
  entry (after between_frames, before the frame runs), with Missions' summary,
  stored as a delta against the display post-load state
  (``capturar_campos_exibicao_original.blocos_exibicao``): released block
  names, new blocks (hex) and, per surviving block, the differing byte ranges
  (hex). ``estado_da_sondagem`` rebuilds it and checks the summary. Isolated
  captures start from these states.
The output is one xz-compressed JSON; the process ends with
``encerramento_captura.encerrar_captura``. No translation is imported.

    python3 -B pesquisas-paralelas/economia/sondar_temporizadores_exibicao.py --ate 9000 \
        --estados 100,800,900,1000,2000,9000 \
        --saida pesquisas-paralelas/economia/evidencias/sondagem-temporizadores-exibicao-9000.json.xz
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import struct
import subprocess
import sys
import time

RAIZ = Path(__file__).resolve().parents[2]
CONTADOR = 0x508f7c
VIGIADOS = {
    'market_contact': (0x4e2928, 4), 'market_flags': (0x4e292c, 4), 'market_indicators': (0x4e2930, 8),
    'market_words_2938': (0x4e2938, 8), 'market_words_2940': (0x4e2940, 8), 'market_partners': (0x496f8c, 4),
    'market_states': (0x4e2e7c, 4), 'market_state_ff': (0x4e2f7b, 1), 'hangar': (0x4e296c, 80), 'structure_counts': (0x4dfaa8, 16),
    'structure_step_byte': (0x4dfb9b, 1), 'attack_flags': (0x508044, 80), 'alliance_counters': (0x5080b0, 64),
    'ai_contexts': (0x51a990, 64), 'sympathy_events': (0x497288, 16 * 0x16), 'weather': (0x496d2c, 4),
    'player_colors': (0x4e24dc, 256), 'resources': (0x4e2ea8, 128), 'research_players': (0x5080f4, 64),
    'scientists': (0x508174, 8), 'inventions': (0x50871c, 4), 'local_player': (0x508041, 1),
    'field_row_period': (0x4973e8, 4), 'field_flag': (0x509952, 1), 'structure0': (0x49a0c8, 276),
}


def delta(base, imagem):
    """``imagem`` (name -> (base, bytes)) against ``base`` (name -> (base, bytes)) as released/allocated/ranges."""
    saida = dict(released=sorted(n for n in base if n not in imagem), allocated={}, ranges=[])
    for nome, (inicio, dados) in imagem.items():
        anterior = base.get(nome)
        if anterior is None or anterior[0] != inicio or len(anterior[1]) != len(dados):
            if anterior is not None:
                saida['released'].append(nome)
            saida['allocated'][nome] = dict(base=hex(inicio), hex=dados.hex())
            continue
        if anterior[1] == dados:
            continue
        i, n = 0, len(dados)
        while i < n:
            j = min(n, i + 64)
            if anterior[1][i:j] == dados[i:j]:
                i = j
                continue
            while i < j and anterior[1][i] == dados[i]:
                i += 1
            fim = i
            while fim < n and (anterior[1][fim] != dados[fim] or anterior[1][fim:fim + 16] != dados[fim:fim + 16]):
                fim += 1
            saida['ranges'].append(dict(address=hex(inicio + i), hex=dados[i:fim].hex()))
            i = fim
    saida['released'].sort()
    return saida


def estado_da_sondagem(base, registro):
    """Rebuild (name, base, bytes) blocks from ``delta`` over ``base`` [(name, base, bytes)]; check the summary."""
    import bisect
    import hashlib as _h
    blocos = {n: (b, bytearray(d)) for n, b, d in base}
    for nome in registro['delta']['released']:
        del blocos[nome]
    for nome, bloco in registro['delta']['allocated'].items():
        blocos[nome] = (int(bloco['base'], 16), bytearray.fromhex(bloco['hex']))
    ordem = sorted((b, n) for n, (b, _) in blocos.items())
    bases = [b for b, _ in ordem]
    for faixa in registro['delta']['ranges']:
        a, dados = int(faixa['address'], 16), bytes.fromhex(faixa['hex'])
        inicio, nome = ordem[bisect.bisect_right(bases, a) - 1]
        blocos[nome][1][a - inicio:a - inicio + len(dados)] = dados
    h = _h.sha256()
    for nome in sorted(blocos):
        b, d = blocos[nome]
        h.update(struct.pack('<II', b, len(d)) + bytes(d))
    resumo = dict(blocks=len(blocos), bytes=sum(len(d) for _, d in blocos.values()), sha256=h.hexdigest())
    if resumo != registro['summary']:
        raise ValueError(f'probe state does not rebuild to its summary: {resumo} != {registro["summary"]}')
    return [(n, b, bytes(d)) for n, (b, d) in blocos.items()]


def main():
    sys.path.insert(0, str(RAIZ / 'ferramentas'))
    import percurso_quadro1  # noqa: F401  (puts Missions on sys.path)
    import cenarios_oraculo
    from oraculo_exibicao_missao import BancadaExibicaoOriginal
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--ate', type=int, required=True)
    ap.add_argument('--estados', required=True, help='comma-separated counters whose CalculGame entry state is saved')
    ap.add_argument('--ticks', type=int, default=200000)
    a = ap.parse_args()
    saida = RAIZ / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    estados_pedidos = sorted({int(x) for x in a.estados.split(',')})
    t0 = time.monotonic()
    caminho_cap = cenarios_oraculo.caminho('exibicao', 'captura_quadro')
    cap = json.loads(caminho_cap.read_bytes())
    ni = cap['named_inputs']['m1']
    ticks = tuple(0x123456 + 40 * k for k in range(1, a.ticks + 1))
    if ticks[:len(cenarios_oraculo.TICKS_EXIBICAO)] != cenarios_oraculo.TICKS_EXIBICAO:
        raise SystemExit('Display clock rule differs from cenarios_oraculo.TICKS_EXIBICAO')
    b = BancadaExibicaoOriginal(cenarios_oraculo.entradas_exibicao(ni['allocation_fill'], ni['clock_ms'][0],
                                                                   ticks=ticks), segundos=300, rastrear=False)
    import capturar_campos_exibicao_original as campos
    s0, resumo_s0, _ = campos.blocos_exibicao()
    s0 = {n: (inicio, dados) for n, inicio, dados in s0}
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    ler = lambda e, n: bytes(b.cpu.mem_read(e, n))
    u32 = lambda e: struct.unpack('<I', ler(e, 4))[0]

    def vigiados():
        v = {n: ler(e, t).hex() for n, (e, t) in VIGIADOS.items()}
        v['player_records'] = ler(u32(0x5080a8), 100).hex()
        v['live_structures'] = [i for i in range(1000) if ler(0x49a0c8 + 0x114 * i + 5, 1)[0]]
        return v

    referencia = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao, quadros, estados, anterior = {}, [], {}, {}

    def registrar(k):
        nonlocal anterior
        atual = vigiados()
        quadros.append(dict(frame=k, counter=u32(CONTADOR), world_rng=hex(u32(0x497164)),
                            changed={n: v for n, v in atual.items() if anterior.get(n) != v}))
        anterior = atual

    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(300)),
                         ('frame1', lambda: b.executar_quadro(600))):
        correr()
        reproducao[nome] = b.resumo_imagem(b.imagem()) == referencia[nome]
        if nome != 'between_frames':
            registrar(0 if nome == 'load_tail' else 1)
    if not all(reproducao.values()):
        raise SystemExit(f'Frames 0/1 do not reproduce the display reference: {reproducao}')
    k = 1
    while True:
        k += 1
        b.executar_entre_quadros(300)
        contador = u32(CONTADOR)
        if contador in estados_pedidos:
            imagem = b.imagem()
            estados[str(contador)] = dict(frame=k, phase='calculgame_entry', summary=b.resumo_imagem(imagem),
                                          entry_world_rng=hex(u32(0x497164)), delta_base=resumo_s0,
                                          delta=delta(s0, imagem))
        b.executar_quadro(600)
        registrar(k)
        if contador >= a.ate:
            break
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    resultado = dict(
        schema='rising-lands/economy-display-gate-probe/1', original_sha256=HASH_ORIGINAL, translation_executed=False,
        scenario='exibicao', source_revision=revisao,
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest()
                       for p in ('pesquisas-paralelas/economia/sondar_temporizadores_exibicao.py',
                                 'pesquisas-paralelas/missoes/oraculo_exibicao_missao.py',
                                 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py')},
        reference=dict(path=str(caminho_cap.relative_to(RAIZ)), sha256=hashlib.sha256(caminho_cap.read_bytes()).hexdigest()),
        inputs=f'display-reference named inputs; declared no-input answers; display clock 0x123456+40*k, k=1..{a.ticks}',
        watched={n: [hex(e), t] for n, (e, t) in VIGIADOS.items()}, reproduction_frames_0_1=reproducao,
        stop_counter=a.ate, frames_run=k, requested_states=estados_pedidos, states=estados, frames=quadros,
        code_unchanged=b.sha256_codigo() == cap['code_integrity']['after'], seconds=round(time.monotonic() - t0, 3))
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'xb') as f:
        f.write(lzma.compress(json.dumps(resultado, separators=(',', ':')).encode() + b'\n'))
    print(json.dumps(dict(output=str(saida), frames=k, states=sorted(estados), seconds=resultado['seconds'])), flush=True)
    encerrar_captura(0, saida)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except BaseException:
        import traceback
        traceback.print_exc()
        sys.path.insert(0, str(RAIZ / 'ferramentas'))
        from encerramento_captura import encerrar_captura
        encerrar_captura(2)   # a failed run must not spin in Unicorn teardown either
