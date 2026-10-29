"""Segment-parallel execution of the display reference (M2.3a tooling; proved on M2.2 before any use).

Pass A runs the frames sequentially and saves an exact resumable snapshot after
every K-th frame: every mapped Unicorn region (bytes and protection), the
Unicorn CPU context (``context_save``: registers, flags, segments, FPU/SSE),
and the bench's Python state (declared-input cursors, Windows/clock answers
consumed, binding and boundary logs, arena records, DirectDraw backend state,
trace and counters).  Pass B starts a fresh bench (constructor only), restores
a snapshot *in place* (objects the bindings already hold keep their identity),
reinstalls the frame hooks and continues from frame k+1 on its own lease slot.

Each run writes one JSON line per phase, built by the capture's own
``registrar_fase`` minus the wall-clock ``seconds``.  ``comparar`` joins the
segments and requires them to equal the sequential capture byte for byte.
Not evidence: everything stays under ``.local/``.

    python3 -B pesquisas-paralelas/missoes/segmentos_quadros_missao.py passo-a --quadros 128 --cada 32 \
        --dir .local/segmentos/m2-2
    python3 -B pesquisas-paralelas/missoes/segmentos_quadros_missao.py segmento --dir .local/segmentos/m2-2 \
        --de 32 --ate 64
    python3 -B pesquisas-paralelas/missoes/segmentos_quadros_missao.py comparar --dir .local/segmentos/m2-2 \
        --captura pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz
"""
import argparse
import hashlib
import json
from pathlib import Path
import pickle
import sys
import time
import zlib

import ambiente_missoes
import cenarios_oraculo as cen
from mapa_memoria_m1 import carregar_json
from emulador import x86
from oraculo_carga_missao import RETORNO_MISSION_LOAD
from oraculo_quadro_missao import RETORNO_CALCUL_GAME, nomes_fases

ROOT = ambiente_missoes.ROOT
# Bench attributes holding Unicorn objects: only their plain attributes are saved and restored.
COM_CPU = {'arena': ('cpu',), 'directdraw': ('_cpu',), 'vinculos_declarados': ('cpu', 'vinculos')}
FORMATO = 'rising-lands/missions-segment-snapshot/1'


def bancada_nova():
    cap = carregar_json(cen.caminho('exibicao', 'captura_m1'))
    ni = cap['named_inputs']
    b, _, _ = cen.bancada('exibicao', ni['allocation_fill'], ni['clock_ms'][0])
    return b


def _python(b):
    estado = {}
    for nome, valor in vars(b).items():
        if nome == 'cpu':
            continue
        if nome in COM_CPU:
            estado[nome] = {k: v for k, v in vars(valor).items() if k not in COM_CPU[nome]}
        else:
            estado[nome] = valor
    return estado


def salvar(b, caminho, quadro):
    """Exact resumable snapshot after frame ``quadro`` (EIP at the frame's RET into ProgIteration)."""
    esperado = RETORNO_MISSION_LOAD if quadro == 0 else RETORNO_CALCUL_GAME
    if b.cpu.reg_read(x86.UC_X86_REG_EIP) != esperado:
        raise RuntimeError('Snapshots are taken at the MissionLoad return (frame 0) or at a frame end (0x475063)')
    regioes = [(a, z, p, zlib.compress(bytes(b.cpu.mem_read(a, z-a+1)), 1)) for a, z, p in b.cpu.mem_regions()]
    dados = dict(format=FORMATO, frame=quadro, regions=regioes, context=pickle.dumps(b.cpu.context_save()),
                 python=pickle.dumps(_python(b), protocol=4),
                 bindings=sorted(b.vinculos_declarados.vinculos))
    texto = pickle.dumps(dados, protocol=4)
    with open(caminho, 'xb') as f:
        f.write(texto)
    return hashlib.sha256(texto).hexdigest()


def _no_lugar(atual, novo):
    """Replace ``atual``'s contents with ``novo``'s, keeping ``atual``'s identity when it is a container/object."""
    if isinstance(atual, list) and isinstance(novo, list):
        atual[:] = novo
    elif isinstance(atual, dict) and isinstance(novo, dict):
        atual.clear()
        atual.update(novo)
    elif isinstance(atual, set) and isinstance(novo, set):
        atual.clear()
        atual.update(novo)
    elif hasattr(atual, '__dict__') and type(atual) is type(novo) and not isinstance(atual, type):
        for k, v in vars(novo).items():
            if k in vars(atual):
                vars(atual)[k] = _no_lugar(vars(atual)[k], v)
            else:
                vars(atual)[k] = v
        return atual
    else:
        return novo
    return atual


def restaurar(b, caminho):
    """Restore a snapshot into a freshly constructed bench; returns the snapshot's frame."""
    from emulador import unicorn
    dados = pickle.loads(Path(caminho).read_bytes())
    if dados['format'] != FORMATO:
        raise RuntimeError('Unknown snapshot format')
    if dados['bindings'] != sorted(b.vinculos_declarados.vinculos):
        raise RuntimeError('The fresh bench declares other bindings than the snapshot')
    mapeadas = {(a, z) for a, z, _ in b.cpu.mem_regions()}
    for a, z, p, comprimido in dados['regions']:
        if (a, z) not in mapeadas:
            b.cpu.mem_map(a, z-a+1, p)
        b.cpu.mem_protect(a, z-a+1, unicorn.UC_PROT_ALL)
        b.cpu.mem_write(a, zlib.decompress(comprimido))
        b.cpu.mem_protect(a, z-a+1, p)
    if sorted((a, z, p) for a, z, p, _ in dados['regions']) != sorted(b.cpu.mem_regions()):
        raise RuntimeError('Region layout differs from the snapshot after restore')
    b.cpu.context_restore(pickle.loads(dados['context']))
    if dados['frame']:
        b._ganchar_quadros()    # frame 0: executar_cauda_carga installs them
    for nome, valor in pickle.loads(dados['python']).items():
        if nome in COM_CPU:
            alvo = getattr(b, nome)
            for k, v in valor.items():
                vars(alvo)[k] = _no_lugar(vars(alvo).get(k), v)
        else:
            vars(b)[nome] = _no_lugar(vars(b).get(nome), valor)
    b.cpu.ctl_flush_tb()
    return dados['frame']


def _linha(registro):
    registro = dict(registro)
    registro.pop('seconds', None)
    return json.dumps(registro, sort_keys=True)


def _correr(b, fases, saida, checkpoints, de, ate, cada=None, pasta=None, leve=False):
    """Run ``fases`` (an iterator of (phase, regs)), writing one record line per phase.

    The binding-event log is compacted: events are dropped once their phase is written.  ``leve``
    (pass A of a long run) writes only each phase's exit counters and builds no state images."""
    import capturar_quadros_exibicao_missao as cq
    import delta_estado_missao as delta
    eventos = delta.compactar_eventos(b)
    anterior, antes = (None if leve else b.imagem()), b._estado_fase()
    ddcalls = len(b.chamadas_exibicao())
    instantaneos = {}
    with open(saida, 'x') as f:
        for nome, regs in fases:
            depois = b._estado_fase()
            if not leve:
                imagem = b.imagem()
                registro = cq.registrar_fase(b, nome, regs, antes, depois, anterior, imagem, ddcalls, checkpoints, 0)
                f.write(_linha(registro)+'\n')
                anterior = imagem
            else:
                f.write(json.dumps(dict(phase=nome, exit=depois), sort_keys=True)+'\n')
            eventos.descartar_ate(depois['bindings'])
            ddcalls, antes = len(b.chamadas_exibicao()), depois
            if cada and nome.startswith('frame') and int(nome[5:]) % cada == 0 and int(nome[5:]) < ate:
                k = int(nome[5:])
                instantaneos[k] = salvar(b, pasta/f'instantaneo-{k:05d}.pickle', k)
        f.flush()
        __import__('os').fsync(f.fileno())
    return instantaneos


def passo_a(a):
    import capturar_quadros_exibicao_missao as cq
    pasta = ROOT/a.dir
    pasta.mkdir(parents=True, exist_ok=False)
    checkpoints = tuple(k for k in cq.CHECKPOINTS if k <= a.quadros)
    t0 = time.monotonic()
    b = bancada_nova()
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    import delta_estado_missao as delta
    delta.compactar_eventos(b).descartar_ate(len(b.vinculos_declarados.eventos))
    zero = salvar(b, pasta/'instantaneo-00000.pickle', 0)
    saida = pasta/f'fases-00000-{a.quadros:05d}.jsonl'
    inst = _correr(b, b.executar_quadros(a.quadros, a.segundos_quadro), saida, checkpoints, 0, a.quadros,
                   a.cada, pasta, leve=a.leve)
    inst = {0: zero, **inst}
    manifesto = dict(frames=a.quadros, every=a.cada, light=a.leve, checkpoints=list(checkpoints), snapshots=inst,
                     records=saida.name, seconds=round(time.monotonic()-t0, 1))
    caminho = pasta/'passo-a.json'
    caminho.write_text(json.dumps(manifesto, indent=1)+'\n')
    print(json.dumps(manifesto, indent=1))
    return [saida, caminho] + [pasta/f'instantaneo-{k:05d}.pickle' for k in inst]


def _fases_segmento(b, de, ate, segundos):
    if de == 0:
        yield from b.executar_quadros(ate, segundos)
        return
    for q in range(de+1, ate+1):
        entre, quadro = nomes_fases(q)
        yield entre, b.executar_entre_quadros(segundos, q)
        yield quadro, b.executar_quadro(segundos, q)


def segmento(a):
    pasta = ROOT/a.dir
    manifesto = json.loads((pasta/'passo-a.json').read_text())
    t0 = time.monotonic()
    b = bancada_nova()
    k = restaurar(b, pasta/f'instantaneo-{a.de:05d}.pickle')
    if k != a.de:
        raise RuntimeError('Snapshot frame mismatch')
    saida = pasta/f'fases-{a.de:05d}-{a.ate:05d}.jsonl'
    _correr(b, _fases_segmento(b, a.de, a.ate, a.segundos_quadro), saida, tuple(manifesto['checkpoints']),
            a.de, a.ate)
    print(json.dumps(dict(segment=[a.de, a.ate], records=saida.name, seconds=round(time.monotonic()-t0, 1))))
    return [saida]


def comparar(a):
    import delta_estado_missao as delta
    pasta = ROOT/a.dir
    referencia = None
    if a.captura:
        captura, _ = delta.carregar(ROOT/a.captura)
        referencia = {f['phase']: _linha(f) for f in captura['phases']}
    manifesto = json.loads((pasta/'passo-a.json').read_text())
    leve = manifesto.get('light', False)
    if leve and referencia is None:
        raise SystemExit('A light pass A has no records: compare its segments with a capture')
    sequencial = {json.loads(l)['phase']: l.rstrip('\n') for l in (pasta/manifesto['records']).open()}
    resultado = dict(pass_a=dict(phases=len(sequencial), light=leve, equal_capture=None if referencia is None or leve
                                 else sum(1 for n, l in sequencial.items() if referencia.get(n) == l)))
    segmentos = sorted(p for p in pasta.glob('fases-*.jsonl') if p.name != manifesto['records'])
    por_segmento, diferentes = [], []
    for p in segmentos:
        linhas = [l.rstrip('\n') for l in p.open()]
        iguais = 0
        for l in linhas:
            nome = json.loads(l)['phase']
            if (leve or sequencial.get(nome) == l) and (referencia is None or referencia.get(nome) == l):
                iguais += 1
            else:
                diferentes.append(nome)
        por_segmento.append(dict(file=p.name, phases=len(linhas), equal=iguais))
    resultado.update(segments=por_segmento, differing_phases=diferentes[:20],
                     capture_phases=None if referencia is None else len(referencia),
                     result='equal' if not diferentes and por_segmento and
                     resultado['pass_a']['equal_capture'] in (None, len(sequencial)) else 'different')
    caminho = pasta/'comparacao.json'
    caminho.write_text(json.dumps(resultado, indent=1)+'\n')
    print(json.dumps(resultado, indent=1))
    return resultado


# ---------------------------------------------------------------- policy pass 2 by segment
def passo1_da_captura(captura, s0):
    """Pass-1 inputs of politica_comparacao_quadros from the capture: phases, exact changed bytes, summaries, frees."""
    import delta_estado_missao as delta
    estado, fases, alterados, resumos, liberados = dict(s0), [], {}, {}, {}
    for f in captura['phases']:
        novo = delta.aplicar(estado, f['state_delta'], f['phase'])
        mudou = {}
        for nome, (base, dados) in novo.items():
            velho = estado.get(nome)
            if velho is None or velho[0] != base or len(velho[1]) != len(dados):
                mudou[nome] = (base, list(range(len(dados))))
            elif velho[1] != dados:
                v = velho[1]
                mudou[nome] = (base, [o for a_, z in delta.faixas_diferentes(v, dados) for o in range(a_, z)
                                      if v[o] != dados[o]])
        fases.append(f['phase'])
        alterados[f['phase']], resumos[f['phase']] = mudou, delta.resumo(novo)
        liberados[f['phase']] = sorted(set(estado)-set(novo))
        estado = novo
    return fases, alterados, resumos, liberados


def preparar_politica(a):
    import delta_estado_missao as delta
    import politica_comparacao_quadros as pol
    pasta = ROOT/a.dir
    captura, sha = delta.carregar(ROOT/a.captura)
    fases, alterados, resumos, liberados = passo1_da_captura(captura, delta.s0_exibicao())
    alvos, origem = pol.alvos_de(alterados)
    with open(pasta/'politica-passo1.pickle', 'xb') as f:
        pickle.dump(dict(capture_raw_sha256=sha, frames=captura['frames'], fases=fases, alterados=alterados,
                         resumos=resumos, liberados=liberados, alvos=alvos, origem=origem), f, protocol=4)
    print(json.dumps(dict(phases=len(fases), changed_bytes=len(alvos))))


def politica_segmento(a):
    import politica_comparacao_quadros as pol
    pasta = ROOT/a.dir
    passo1 = pickle.loads((pasta/'politica-passo1.pickle').read_bytes())
    t0 = time.monotonic()
    b = bancada_nova()
    restaurar(b, pasta/f'instantaneo-{a.de:05d}.pickle')
    acessos, superficie, coletar = pol.ganchos(b, passo1['alvos'])
    resumos = {}
    for fase, _ in _fases_segmento(b, a.de, a.ate, a.segundos_quadro):
        coletar(fase)
        resumos[fase] = b.resumo_imagem(b.imagem())
    saida = pasta/f'politica-{a.de:05d}-{a.ate:05d}.pickle'
    with open(saida, 'xb') as f:
        pickle.dump(dict(acessos=acessos, superficie=superficie, resumos=resumos), f, protocol=4)
    print(json.dumps(dict(segment=[a.de, a.ate], output=saida.name, seconds=round(time.monotonic()-t0, 1))))
    return [saida]


def comparar_politica(a):
    import politica_comparacao_quadros as pol
    pasta = ROOT/a.dir
    p1 = pickle.loads((pasta/'politica-passo1.pickle').read_bytes())
    acessos, superficie, resumos2, partes = {}, {}, {}, []
    for p in sorted(pasta.glob('politica-0*.pickle')):
        parte = pickle.loads(p.read_bytes())
        partes.append(p.name)
        for endereco, chaves in parte['acessos'].items():
            d = acessos.setdefault(endereco, {})
            for k, n in chaves.items():
                d[k] = d.get(k, 0)+n
        for k, n in parte['superficie'].items():
            superficie[k] = superficie.get(k, 0)+n
        resumos2.update(parte['resumos'])
    rel = pol.relatorio(p1['frames'], p1['fases'], p1['alterados'], p1['resumos'], p1['liberados'], p1['alvos'],
                        p1['origem'], acessos, superficie, resumos2)
    sequencial = json.loads((ROOT/a.relatorio).read_text())
    ignorar = ('schema', 'source_revision', 'translation_executed', 'evidence', 'seconds')
    corpo = {k: v for k, v in sequencial.items() if k not in ignorar}
    segmentado = json.loads(json.dumps(rel))
    diferentes = sorted(k for k in set(corpo) | set(segmentado) if corpo.get(k) != segmentado.get(k))
    resultado = dict(parts=partes, compared_fields=sorted(corpo), differing_fields=diferentes,
                     body_json_equal=json.dumps(corpo) == json.dumps({k: segmentado[k] for k in corpo}),
                     result='equal' if not diferentes else 'different')
    (pasta/'comparacao-politica.json').write_text(json.dumps(resultado, indent=1)+'\n')
    print(json.dumps(resultado, indent=1))
    return resultado


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='modo', required=True)
    pa = sub.add_parser('passo-a')
    pa.add_argument('--quadros', type=int, required=True)
    pa.add_argument('--cada', type=int, required=True)
    pa.add_argument('--dir', required=True)
    pa.add_argument('--leve', action='store_true', help='no phase records or images: snapshots only')
    pa.add_argument('--segundos-quadro', type=float, default=600.0)
    ps = sub.add_parser('segmento')
    ps.add_argument('--dir', required=True)
    ps.add_argument('--de', type=int, required=True)
    ps.add_argument('--ate', type=int, required=True)
    ps.add_argument('--segundos-quadro', type=float, default=600.0)
    pc = sub.add_parser('comparar')
    pc.add_argument('--dir', required=True)
    pc.add_argument('--captura', help='sequential capture (.json.xz); omitted: segments vs pass A only')
    pp = sub.add_parser('preparar-politica')
    pp.add_argument('--dir', required=True)
    pp.add_argument('--captura', required=True)
    pg = sub.add_parser('politica')
    pg.add_argument('--dir', required=True)
    pg.add_argument('--de', type=int, required=True)
    pg.add_argument('--ate', type=int, required=True)
    pg.add_argument('--segundos-quadro', type=float, default=600.0)
    pk = sub.add_parser('comparar-politica')
    pk.add_argument('--dir', required=True)
    pk.add_argument('--relatorio', required=True, help='the sequential politica_comparacao_quadros report')
    a = ap.parse_args()
    if a.modo == 'preparar-politica':
        return preparar_politica(a)
    if a.modo == 'comparar-politica':
        return 0 if comparar_politica(a)['result'] == 'equal' else 1
    if a.modo == 'politica':
        from encerramento_captura import encerrar_captura
        encerrar_captura(0, *politica_segmento(a))
    if a.modo == 'comparar':
        return 0 if comparar(a)['result'] == 'equal' else 1
    caminhos = passo_a(a) if a.modo == 'passo-a' else segmento(a)
    from encerramento_captura import encerrar_captura
    encerrar_captura(0, *caminhos)


if __name__ == '__main__':
    sys.exit(main())
