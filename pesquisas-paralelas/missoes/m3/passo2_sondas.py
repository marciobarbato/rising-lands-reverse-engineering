"""M2.2-form whole-state captures of the M3 probe windows: records, policy, self-checking xz parts.

The M2.3 pipeline (``segmentos_quadros_missao``, ``politica_comparacao_quadros``, ``pacotes_quadros_missao``) run
on the scripted-input oracle (``entrada_roteirizada``) from the accepted frame-128 snapshot. Original only.

1. ``registros``: one sequential run of a probe input from frame 128. It writes:
   - one record per phase, built by the capture's own ``registrar_fase`` (complete deltas);
   - the scripted answers each phase consumed (``entradas-roteiro.jsonl``);
   - the opening state (``abertura.json``);
   - snapshots every ``--cada`` frames, from which pass 2 runs segment-parallel.
2. ``passo1``: the exact changed bytes, replayed from the opening state. Every record summary must be reproduced.
3. ``politica``: pass 2 of one segment. It takes Missions' read/write hooks on the changed bytes and surfaces,
   and per-access display/logic context, with keys aggregated into 1,000-frame windows as in M2.3.
4. ``relatorio``: ``segmentos_quadros_missao.relatorio_longo`` over the segments. Then it builds the probe's mask:
   - start from the published M2.3 cumulative mask;
   - add the display-only ranges this window proves (writer/reader classification);
   - remove any byte this window classifies as game logic, and report each such byte as a conflict.
5. ``empacotar``: self-checking xz parts of at most 1,000 frames. Each holds:
   - an ``opening_state``;
   - every phase's ``compared_summary`` and ``masked_sha256`` under that mask (M2.3 definitions);
   - the scripted answers.
   Afterwards the parts are re-read and the whole chain is checked.

    python3 -B pesquisas-paralelas/missoes/m3/passo2_sondas.py registros --entrada pesquisas-paralelas/missoes/m3/entradas/P1.json --dir .local/m3/passo2/P1
    python3 -B pesquisas-paralelas/missoes/m3/passo2_sondas.py passo1 --dir .local/m3/passo2/P1
    python3 -B pesquisas-paralelas/missoes/m3/passo2_sondas.py politica --dir .local/m3/passo2/P1 --de 128 --ate 378
    python3 -B pesquisas-paralelas/missoes/m3/passo2_sondas.py relatorio --dir .local/m3/passo2/P1 --sonda P1
    python3 -B pesquisas-paralelas/missoes/m3/passo2_sondas.py empacotar --dir .local/m3/passo2/P1 --sonda P1
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import pickle
import sys
import time

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import entrada_roteirizada as er  # noqa: E402

ROOT = er.ROOT
POLITICA_M23 = 'pesquisas-paralelas/missoes/validacao/m2-3-politica-comparacao-9200-quadros.json'
INICIO = '.local/m3/quadro128'
PARTE = 1000
FILTRO = [dict(id=lzma.FILTER_LZMA2, preset=9 | lzma.PRESET_EXTREME)]


def _fases(b, de, ate, segundos=600):
    from oraculo_quadro_missao import nomes_fases
    for k in range(de + 1, ate + 1):
        entre, quadro = nomes_fases(k)
        b.roteiro.iniciar_quadro(k)
        yield entre, b.executar_entre_quadros(segundos, k)
        yield quadro, b.executar_quadro(segundos, k)


def _abrir(pasta, de, entrada):
    quadros, _ = er.carregar_entrada(entrada)
    if de == er.QUADRO_INICIAL:
        b, _, _ = er.abrir(ROOT / INICIO)
    else:
        b, _, k = er.abrir(ROOT / INICIO, pasta / f'instantaneo-{de:05d}.pickle')
        if k != de:
            raise RuntimeError('Snapshot frame mismatch')
    b.roteiro.quadros = quadros
    return b


def registros(a):
    import delta_estado_missao as delta
    import segmentos_quadros_missao as seg
    pasta = ROOT / a.dir
    pasta.mkdir(parents=True, exist_ok=False)
    bruto = Path(a.entrada).read_bytes()
    entrada = json.loads(bruto)
    _, ate = er.carregar_entrada(entrada)
    ate = min(ate, a.ate or ate)
    t0 = time.monotonic()
    b = _abrir(pasta, er.QUADRO_INICIAL, entrada)
    abertura = b.imagem()
    (pasta / 'abertura.json').write_text(json.dumps(dict(frame=er.QUADRO_INICIAL, summary=delta.resumo(abertura),
                                                         full_state=delta.estado_completo(abertura))) + '\n')
    seg.salvar(b, pasta / f'instantaneo-{er.QUADRO_INICIAL:05d}.pickle', er.QUADRO_INICIAL)
    # Full states after the frames pass A snapshots (multiples of --cada) and after the last frame.
    checkpoints = tuple(k for k in range(a.cada, ate, a.cada) if k > er.QUADRO_INICIAL) + (ate,)
    lado = open(pasta / 'entradas-roteiro.jsonl', 'x')

    def com_entradas(fases):
        for nome, regs in fases:
            for e in b.roteiro.eventos:
                lado.write(json.dumps(e, sort_keys=True) + '\n')
            b.roteiro.eventos.clear()
            yield nome, regs
    saida = pasta / f'fases-{er.QUADRO_INICIAL:05d}-{ate:05d}.jsonl'
    inst = seg._correr(b, com_entradas(_fases(b, er.QUADRO_INICIAL, ate)), saida, checkpoints, er.QUADRO_INICIAL,
                       ate, a.cada, pasta)
    lado.close()
    manifesto = dict(probe=entrada.get('name'), input=str(Path(a.entrada).resolve().relative_to(ROOT)),
                     input_sha256=hashlib.sha256(bruto).hexdigest(), frames=[er.QUADRO_INICIAL, ate], every=a.cada,
                     checkpoints=list(checkpoints), snapshots=inst, records='none', segments_records=[saida.name],
                     seconds=round(time.monotonic() - t0, 1),
                     ticks=json.loads((ROOT / INICIO / 'manifesto.json').read_text())['ticks'])
    (pasta / 'passo-a.json').write_text(json.dumps(manifesto, indent=1) + '\n')
    print(json.dumps(manifesto, indent=1))
    return [saida, pasta / 'passo-a.json', pasta / 'entradas-roteiro.jsonl']


def _abertura(pasta):
    import delta_estado_missao as delta
    d = json.loads((pasta / 'abertura.json').read_text())
    estado = {n: (int(x['base'], 16), delta._decodificar(x)) for n, x in d['full_state'].items()}
    if delta.resumo(estado) != d['summary']:
        raise RuntimeError('Opening state does not reproduce its summary')
    return estado


def passo1(a):
    """``segmentos_quadros_missao.passo1_registros`` with the window's opening state as s0."""
    import delta_estado_missao as delta
    import segmentos_quadros_missao as seg
    pasta = ROOT / a.dir
    abertura = _abertura(pasta)
    original = delta.s0_exibicao
    delta.s0_exibicao = lambda: dict(abertura)
    try:
        seg.passo1_registros(a)
    finally:
        delta.s0_exibicao = original


def politica(a):
    import delta_estado_missao as delta
    import politica_comparacao_quadros as pol
    import segmentos_quadros_missao as seg
    from encerramento_captura import encerrar_captura
    pasta = ROOT / a.dir
    manifesto = json.loads((pasta / 'passo-a.json').read_text())
    entrada = json.loads((ROOT / manifesto['input']).read_bytes())
    alvos = set(pickle.loads((pasta / 'politica-passo1-longo.pickle').read_bytes())['enderecos'])
    t0 = time.monotonic()
    b = _abrir(pasta, a.de, entrada)
    eventos = delta.compactar_eventos(b)
    acessos, superficie, coletar = pol.ganchos(b, alvos, seg.janela_longa)
    resumos = {}
    for fase, _ in _fases(b, a.de, a.ate):
        coletar(fase)
        eventos.descartar_ate(len(eventos))
        b.roteiro.eventos.clear()
        resumos[fase] = b.resumo_imagem(b.imagem())
    saida = pasta / f'politica-{a.de:05d}-{a.ate:05d}.pickle'
    with open(saida, 'xb') as f:
        pickle.dump(dict(acessos=acessos, superficie=superficie, resumos=resumos), f, protocol=4)
    print(json.dumps(dict(segment=[a.de, a.ate], output=saida.name, seconds=round(time.monotonic() - t0, 1))))
    encerrar_captura(0, saida)


def _faixas(enderecos):
    import politica_comparacao_quadros as pol
    return [[hex(x), hex(z)] for x, z in pol.faixas(sorted(enderecos))]


def _expandir(faixas):
    return {e for a, z in faixas for e in range(int(a, 16), int(z, 16))}


def relatorio(a):
    import segmentos_quadros_missao as seg
    pasta = ROOT / a.dir
    destino = AQUI / 'sondas' / a.sonda
    destino.mkdir(parents=True, exist_ok=True)
    caminho = destino / 'politica-janela.json'
    a.relatorio = str(caminho.relative_to(ROOT))
    rel = seg.relatorio_longo(a)
    publicado = json.loads((ROOT / POLITICA_M23).read_text())
    m23 = _expandir(publicado['cumulative']['exclusion_mask'])
    exibicao = _expandir(rel['cumulative']['exclusion_mask'])
    logica = {int(x, 16) for x in rel['game_logic_bytes']}
    conflitos = sorted(m23 & logica)
    mascara = (m23 | exibicao) - logica
    masc = dict(schema='rising-lands/m3-probe-window-mask/1', probe=a.sonda,
                published=dict(path=POLITICA_M23, sha256=hashlib.sha256((ROOT / POLITICA_M23).read_bytes()).hexdigest(),
                               bytes=len(m23)),
                window_policy=dict(path=a.relatorio, sha256=hashlib.sha256(caminho.read_bytes()).hexdigest(),
                                   passed=rel['passed']),
                added_display_only=_faixas(exibicao - m23), added_bytes=len(exibicao - m23),
                removed_game_logic_conflicts=[hex(x) for x in conflitos],
                rule='published M2.3 mask, plus display-only bytes proven in this window, minus bytes this window '
                     'classifies as game logic',
                cumulative=dict(exclusion_mask=_faixas(mascara), bytes=len(mascara)))
    (destino / 'mascara-janela.json').write_text(json.dumps(masc, indent=1) + '\n')
    print(json.dumps({k: masc[k] for k in ('added_bytes', 'removed_game_logic_conflicts')} | dict(passed=rel['passed'])))
    return 0 if rel['passed'] else 1


def _escrever(caminho, objeto, local):
    texto = (json.dumps(objeto, sort_keys=True, indent=1) + '\n').encode()
    comprimido = lzma.compress(texto, format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, filters=FILTRO)
    with open(caminho, 'xb') as f:
        f.write(comprimido)
    (local / caminho.name[:-len('.xz')]).write_bytes(texto)
    return dict(artifact=str(caminho.relative_to(ROOT)), compressed_sha256=hashlib.sha256(comprimido).hexdigest(),
                compressed_bytes=len(comprimido), raw_sha256=hashlib.sha256(texto).hexdigest(), raw_bytes=len(texto))


def empacotar(a):
    import delta_estado_missao as delta
    import pacotes_quadros_missao as pq
    from emulador import HASH_ORIGINAL
    pasta = ROOT / a.dir
    destino = AQUI / 'sondas' / a.sonda
    manifesto_caminho = destino / 'captura-janela.manifest.json'
    if manifesto_caminho.exists():
        raise SystemExit(f'Refusing to overwrite {manifesto_caminho}')
    mascara_caminho = destino / 'mascara-janela.json'
    mascara = pq.Mascara(json.loads(mascara_caminho.read_text())['cumulative']['exclusion_mask'])
    passo_a = json.loads((pasta / 'passo-a.json').read_text())
    roteiro = {}
    for linha in open(pasta / 'entradas-roteiro.jsonl'):
        e = json.loads(linha)
        roteiro.setdefault(e['phase'], []).append(e)
    local = pasta / 'partes'
    local.mkdir(exist_ok=True)
    estado = _abertura(pasta)
    ultimo = passo_a['frames'][1]
    limites = list(range(er.QUADRO_INICIAL + PARTE, ultimo, PARTE)) + [ultimo]
    partes, atual, anterior, inicio = [], None, None, er.QUADRO_INICIAL + 1
    for arquivo in passo_a['segments_records']:
        for linha in open(pasta / arquivo):
            f = json.loads(linha)
            nome = f['phase']
            if atual is None:
                atual = dict(schema='rising-lands/m3-probe-window-part/1', probe=a.sonda, part=len(partes),
                             frames=[inicio, limites[len(partes)]], first_phase=nome,
                             previous_part_raw_sha256=anterior, opening_state=pq.estado_aberto(estado, mascara),
                             phases=[], mask=dict(path=str(mascara_caminho.relative_to(ROOT)),
                                                  sha256=hashlib.sha256(mascara_caminho.read_bytes()).hexdigest()),
                             input=dict(path=passo_a['input'], sha256=passo_a['input_sha256']),
                             original_sha256=HASH_ORIGINAL, scenario='exibicao + scripted input (entrada_roteirizada)',
                             translation_executed=False, state_form='complete delta', definitions=pq.DEFINICOES)
            estado = delta.aplicar(estado, f['state_delta'], nome)
            comparado, mascarado = mascara.resumos(estado)
            f['state_after'].update(compared_summary=comparado, masked_sha256=mascarado)
            f['scripted_inputs'] = roteiro.get(nome, [])
            atual['phases'].append(f)
            if nome.startswith('frame') and pq.quadro(nome) == limites[len(partes)]:
                atual['last_phase'] = nome
                registro = _escrever(ROOT / f'{destino.relative_to(ROOT)}/captura-janela.parte{len(partes):02d}.json.xz',
                                     atual, local)
                registro.update(part=len(partes), frames=atual['frames'], phases=len(atual['phases']))
                partes.append(registro)
                print(json.dumps(registro), flush=True)
                anterior, inicio, atual = registro['raw_sha256'], pq.quadro(nome) + 1, None
    if atual is not None or len(partes) != len(limites):
        raise RuntimeError('Records do not end exactly at the last part boundary')
    verificacao = verificar(partes, _abertura(pasta), mascara)
    manifesto = dict(schema='rising-lands/compressed-evidence-manifest/2', probe=a.sonda,
                     capture=f'M3 probe {a.sonda}: frames {er.QUADRO_INICIAL + 1}-{ultimo} from the M2.2 frame-128 '
                             'state, scripted input, complete deltas',
                     encoding=dict(format='xz', check='crc64', filter='lzma2', preset='9e'), parts=partes,
                     mask=dict(path=str(mascara_caminho.relative_to(ROOT)),
                               sha256=hashlib.sha256(mascara_caminho.read_bytes()).hexdigest()),
                     opening=json.loads((pasta / 'abertura.json').read_text())['summary'],
                     definitions=pq.DEFINICOES, replay_check=verificacao)
    manifesto_caminho.write_text(json.dumps(manifesto, indent=1) + '\n')
    print(json.dumps(dict(manifest=str(manifesto_caminho.relative_to(ROOT)), replay=verificacao['result'],
                          total_compressed=sum(p['compressed_bytes'] for p in partes)), indent=1))


def verificar(partes, abertura, mascara):
    import delta_estado_missao as delta
    estado, saida = None, []
    for p in partes:
        bruto = lzma.decompress((ROOT / p['artifact']).read_bytes())
        if hashlib.sha256(bruto).hexdigest() != p['raw_sha256']:
            raise RuntimeError(f"part {p['part']}: raw hash mismatch")
        parte = json.loads(bruto)
        aberto = {n: (int(b['base'], 16), delta._decodificar(b)) for n, b in parte['opening_state']['full_state'].items()}
        if aberto != (abertura if estado is None else {n: v for n, v in estado.items() if n != 'native_stack'}):
            raise RuntimeError(f"part {p['part']}: opening state is not the previous end state")
        estado, cheios = aberto, 0
        for f in parte['phases']:
            estado = delta.aplicar(estado, f['state_delta'], f['phase'])
            apos = f['state_after']
            comparado, mascarado = mascara.resumos(estado)
            if (delta.resumo(estado), comparado, mascarado) != (apos['summary'], apos['compared_summary'],
                                                               apos['masked_sha256']):
                raise RuntimeError(f"{f['phase']}: replayed hashes differ")
            if 'full_state' in apos:
                if {n: (int(b['base'], 16), delta._decodificar(b)) for n, b in apos['full_state'].items()} != \
                        {n: v for n, v in estado.items() if n != 'native_stack'}:
                    raise RuntimeError(f"{f['phase']}: full state differs from the replay")
                cheios += 1
        saida.append(dict(part=p['part'], phases=len(parte['phases']), full_states_checked=cheios + 1))
    return dict(result='equal', parts=saida,
                chain='part 0 opens with the frame-128 state; every later opening state is the previous replayed end')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('registros')
    r.add_argument('--entrada', required=True)
    r.add_argument('--dir', required=True)
    r.add_argument('--cada', type=int, default=250)
    r.add_argument('--ate', type=int)
    for nome in ('passo1',):
        sub.add_parser(nome).add_argument('--dir', required=True)
    p = sub.add_parser('politica')
    p.add_argument('--dir', required=True)
    p.add_argument('--de', type=int, required=True)
    p.add_argument('--ate', type=int, required=True)
    for nome in ('relatorio', 'empacotar'):
        x = sub.add_parser(nome)
        x.add_argument('--dir', required=True)
        x.add_argument('--sonda', required=True)
    a = ap.parse_args()
    if a.cmd == 'registros':
        from encerramento_captura import encerrar_captura
        encerrar_captura(0, *registros(a))
    return dict(passo1=passo1, politica=politica, relatorio=relatorio, empacotar=empacotar)[a.cmd](a)


if __name__ == '__main__':
    raise SystemExit(main())
