"""M3.1 chain check over a Mac mini scripted-input probe (P1, P2, P3, ...): Python only, frame by frame.

Starts the Python chain (``composicao_entrada_ia.ComposicaoEntrada``) from the accepted M2.2 frame-128 state
(``state_after.full_state`` of phase ``frame128`` in Missions' ``captura-quadros128-monde01-exibicao-v2.json.xz``,
its summary checked), replays the probe's committed input file and compares, per frame, with the probe's
original-only records (read from a pinned git ref, never merged):
- ``comandos.jsonl``: every SetPlayerOrdre packet (frame, player, tag, words 2..8) and every ProcessInputGame
  dispatch (frame, tag, packet bytes, jump target);
- ``entradas.jsonl``: every consumed input answer (peek/get/translate/dispatch, cursor, key) with frame, phase,
  poll site and value;
- ``quadros.jsonl`` (state after frame k): counter, game frame, the world/AI RNGs, the CRT seed, the permutation
  cursor 0x4e1d18, the view origin, the selection list head (8 bytes), the objective block (marks, AL, victory
  counter, forced word, player-0 resources, every live structure, the UI bytes) and the whole 276-byte records
  of units 11..15 (SHA-256 prefix, cell, state and order fields); DGROUP's SHA-256 is reported, not required
  (DGROUP holds display-only bytes of the published mask).

The run stops at the first difference or at the first ``DependenciaIA`` and reports it. This is an indicator-
level check: the per-phase whole-state comparison under the published mask needs the probes' pass-2 delta
captures (``docs/M3_PLAN.md`` §2), which do not exist yet.

    python3 -B pesquisas-paralelas/ia-runtime/provar_entrada_ia.py --sonda P1 --ref origin/feat/re-missions \\
        [--quadros N] [--nucleo-ref DIR] --saida pesquisas-paralelas/ia-runtime/validacao/m3-1-p1.json
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

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))
from ambiente_ia_runtime import ROOT  # noqa: E402

M22 = ROOT / 'pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz'
SONDAS = 'pesquisas-paralelas/missoes/m3'
UNIDADES = (11, 12, 13, 14, 15)
FONTES = tuple(f'pesquisas-paralelas/ia-runtime/{n}' for n in (
    'provar_entrada_ia.py', 'composicao_entrada_ia.py', 'entrada_ordens_ia.py', 'provedores_entrada_ia.py',
    'composicao_quadros_ia.py', 'composicao_encadeada_ia.py', 'affgame_hud_ia.py', 'proxima_etapa_quadro.py'))


def git_show(ref, caminho):
    return subprocess.run(['git', '-C', str(ROOT), 'show', f'{ref}:{caminho}'], capture_output=True, check=True).stdout


def jsonl(dados):
    return [json.loads(x) for x in lzma.decompress(dados).decode().splitlines() if x.strip()]


def estado_quadro128():
    from comparar_quadros_ia import _dados, resumo_estado
    cap = json.loads(lzma.decompress(M22.read_bytes()))
    fase = cap['phases'][-1]
    if fase['phase'] != 'frame128':
        raise SystemExit('The M2.2 capture does not end at frame128')
    estado = {n: (int(b['base'], 16), _dados(b)) for n, b in fase['state_after']['full_state'].items()}
    if resumo_estado({n: v for n, v in estado.items() if n != 'native_stack'}) != fase['state_after']['summary']:
        raise SystemExit('frame128 full state does not match its summary')
    e = fase['entry']['registers']
    regs = {k: e[k] for k in ('EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')}
    regs.update(ESP=hex(int(e['ESP'], 16) + 4), EAX='0x0')
    return cap, estado, regs


def indicadores(mm):
    """The probe's per-frame record fields that the Python state determines (``entrada_roteirizada.amostra``)."""
    u32, u16, u8 = mm.u32, mm.u16, mm.u8
    ler = lambda a, n: bytes(u8(a + i) for i in range(n))  # noqa: E731
    r = dict(counter=u32(0x508f7c), game_frame=u32(0x496d40), world_rng=hex(u32(0x497164)), ai_rng=hex(u32(0x498db4)),
             crt_seed=hex(u32(u32(0x522244) + 0xc)), cursor=u8(0x4e1d18), view_origin=[u16(0x508720), u16(0x508722)],
             selection=ler(0x508728, 8).hex())
    obj = dict(marks=ler(0x4e1d84, 14).hex(), al=ler(0x4e05a0, 1).hex(), victory_counter=ler(0x4e061c, 4).hex(),
               forced=ler(0x4e1a3a, 2).hex(), player0_resources=ler(0x4e2ea8, 32).hex())
    obj['structures'] = [[i, u8(0x49a0c8 + 276 * i + 4), u8(0x49a0c8 + 276 * i + 8), u16(0x49a0c8 + 276 * i + 2),
                          u8(0x49a0c8 + 276 * i + 5)] for i in range(1000) if u8(0x49a0c8 + 276 * i + 5)]
    jog = ler(0x4e2ea8, 32)
    obj['food'], obj['stone'], obj['parts'] = (struct.unpack_from('<h', jog, o)[0] for o in (0xa, 0x12, 2))
    obj['ui'] = {hex(a): u8(a) for a in (0x496207, 0x4e05ae, 0x496208)}
    base = u32(0x4e19a0)
    obj['units'] = {}
    for i in UNIDADES:
        u = ler(base + 276 * i, 276)
        obj['units'][str(i)] = dict(cell=struct.unpack_from('<H', u, 0x7c)[0], state=u[2],
                                    target_b2=struct.unpack_from('<H', u, 0xb2)[0], b7=u[0xb7], b8=u[0xb8], be=u[0xbe],
                                    f110=u[0x110:0x114].hex(), sha256=hashlib.sha256(u).hexdigest()[:16])
    r['objective'] = obj
    return r


def comparar_quadro(k, py, ref):
    campos = ('counter', 'game_frame', 'world_rng', 'ai_rng', 'crt_seed', 'cursor', 'view_origin', 'selection')
    dif = {c: [py[c], ref[c]] for c in campos if py[c] != ref[c]}
    for c, v in py['objective'].items():
        if v != ref['objective'].get(c):
            dif['objective.' + c] = [v, ref['objective'].get(c)]
    return dif


def eventos_referencia(entradas, k):
    return normalizar_eventos([e for e in entradas if e['frame'] == k and e['kind'] in (
        'peek_message', 'get_message', 'translate_message', 'dispatch_message', 'cursor', 'key')])


def normalizar_eventos(eventos):
    saida = []
    for e in eventos:
        e = {c: v for c, v in e.items() if c != 'phase'}
        if e['kind'] == 'dispatch_message':
            e.pop('hwnd', None)                     # the MSG hwnd word is the declared [0x4e27e8]
        saida.append(e)
    return saida


def main():
    from composicao_entrada_ia import ComposicaoEntrada, RoteiroEntrada
    from composicao_quadros_ia import carregar_cenario_exibicao
    from composicao_encadeada_ia import MemoriaMapaRapida
    from reinicio_ia import DependenciaIA
    ap = argparse.ArgumentParser()
    ap.add_argument('--sonda', required=True)
    ap.add_argument('--ref', required=True, help='git ref holding the probe (read with git show, never merged)')
    ap.add_argument('--quadros', type=int, help='frames after 128 (default: the probe\'s frames)')
    ap.add_argument('--nucleo-ref', help='directory with Core\'s construcao_core.py (read-only extraction)')
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    if a.nucleo_ref:
        sys.path.append(str(ROOT / a.nucleo_ref))
    sha_ref = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', a.ref], capture_output=True, text=True,
                             check=True).stdout.strip()
    bruto_entrada = git_show(sha_ref, f'{SONDAS}/entradas/{a.sonda}.json')
    dados = json.loads(bruto_entrada)
    base = f'{SONDAS}/sondas/{a.sonda}'
    arquivos = {n: git_show(sha_ref, f'{base}/{n}') for n in ('quadros.jsonl.xz', 'entradas.jsonl.xz',
                                                              'comandos.jsonl.xz', 'replay.json')}
    if not json.loads(arquivos['replay.json'])['equal']:
        raise SystemExit('The probe was not replay-equal on the Mac mini')
    quadros_ref = {q['frame']: q for q in jsonl(arquivos['quadros.jsonl.xz'])}
    entradas_ref = jsonl(arquivos['entradas.jsonl.xz'])
    comandos_ref = jsonl(arquivos['comandos.jsonl.xz'])
    t0 = time.monotonic()
    cap, estado, regs = estado_quadro128()
    _, _, entrada, m1 = carregar_cenario_exibicao()
    roteiro = RoteiroEntrada(dados)
    comp = ComposicaoEntrada(estado, cap, entrada, m1, roteiro, inicio=128, alocacoes=cap['allocations'],
                             regs_inicio=regs)
    n = a.quadros or (max(quadros_ref) - 128)
    quadros, parada, primeira_diferenca = [], None, None
    ordens_py = []
    k = 128
    try:
        for r in comp.executar(n):
            k = int(''.join(ch for ch in r['phase'] if ch.isdigit()))
            for o in r['ordens']:
                ordens_py.append(dict(o, frame=k))
            if r['phase'].startswith('frame'):
                eventos = normalizar_eventos(roteiro.eventos)
                roteiro.eventos.clear()
                ref_ev = eventos_referencia(entradas_ref, k)
                py = indicadores(MemoriaMapaRapida(comp.mapa))
                dif = comparar_quadro(k, py, quadros_ref[k])
                if eventos != ref_ev:
                    dif['inputs'] = dict(python=eventos[:12], probe=ref_ev[:12])
                ordens_k = [o for o in ordens_py if o['frame'] == k]
                ref_k = [c for c in comandos_ref if c['frame'] == k]
                ord_py = [(o.get('event', 'SetPlayerOrdre'), o['tag'], o.get('word2'), o.get('word4'), o.get('word6'),
                           o.get('word8'), o.get('jump_target')) for o in ordens_k]
                ord_ref = [(c['event'], c['tag'], c.get('word2'), c.get('word4'), c.get('word6'), c.get('word8'),
                            c.get('jump_target')) for c in ref_k]
                if ord_py != ord_ref:
                    dif['orders'] = dict(python=ord_py, probe=ord_ref)
                quadros.append(dict(frame=k, equal=not dif, orders=len(ord_ref),
                                    dgroup_sha256_python=None))
                if dif:
                    primeira_diferenca = dict(frame=k, differences=dif)
                    break
    except DependenciaIA as erro:
        parada = dict(frame=k, dependency=str(erro))
    relatorio = dict(
        schema='rising-lands/m3-1-input-chain-check/1', probe=a.sonda, probe_ref=dict(ref=a.ref, sha=sha_ref),
        probe_files_sha256={n: hashlib.sha256(d).hexdigest() for n, d in arquivos.items()},
        input_sha256=hashlib.sha256(bruto_entrada).hexdigest(),
        start=dict(frame=128, source=str(M22.relative_to(ROOT)), summary=cap['phases'][-1]['state_after']['summary']),
        frames_requested=n, frames_equal=sum(q['equal'] for q in quadros), last_frame=k,
        orders_python=ordens_py, first_difference=primeira_diferenca, stop=parada,
        core_construction_reference=a.nucleo_ref and dict(path=a.nucleo_ref, construcao_core_sha256=hashlib.sha256(
            (ROOT / a.nucleo_ref / 'construcao_core.py').read_bytes()).hexdigest()),
        source_revision=subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True,
                                       text=True).stdout.strip(),
        source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in FONTES},
        seconds=round(time.monotonic() - t0, 3),
        compared=('per frame: inputs consumed, SetPlayerOrdre/ProcessInputGame, counter, game frame, RNGs, CRT seed, '
                  '0x4e1d18, view, selection head, objective block, units 11..15 whole-record SHA-256 prefix'))
    saida = ROOT / a.saida
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(json.dumps(relatorio, indent=1, sort_keys=True) + '\n')
    print(json.dumps(dict(frames_equal=relatorio['frames_equal'], last_frame=k, stop=parada,
                          first_difference=primeira_diferenca and {'frame': primeira_diferenca['frame'],
                                                                   'fields': list(primeira_diferenca['differences'])},
                          seconds=relatorio['seconds']), indent=1, default=str))


if __name__ == '__main__':
    main()
