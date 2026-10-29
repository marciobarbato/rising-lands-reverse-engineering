"""Package a long segmented display-reference run (M2.3) into self-checking xz parts with a manifest.

Input: the segment records of ``segmentos_quadros_missao`` (complete delta form,
one JSON line per phase, wall-clock seconds removed) and the long-run policy
report.  Output, one file per part (frames 0-1000, 1001-2000, ..., 8001-8990,
8991-9200):

* ``opening_state``: the full state before the part's first phase
  (``full_state``, ``summary``, ``compared_summary``, ``masked_sha256``);
* ``phases``: the records, each ``state_after`` extended with
  ``compared_summary`` and ``masked_sha256`` (definitions below), and with
  ``full_state`` after frames 8999, 9000 and 9176;
* the run-level records (named inputs, decisions) in part 0 and the final
  allocations, entry trace and answers in the last part.

Definitions (``mask`` = the policy's cumulative ``exclusion_mask``, a sorted
list of address ranges [start, end); ``native_stack`` is never a block):

* ``compared_summary``: ``resumo_imagem`` of the state with every masked byte
  set to 0 (blocks sorted by name; each block as ``<II base, size>`` + bytes);
* ``masked_sha256``: SHA-256 over, for each block sorted by name and each mask
  range intersecting it in address order, ``<II start, length>`` + the bytes.

The written parts are re-read and checked: raw-JSON hash, opening state,
every phase summary, compared summary and masked hash after replaying the
deltas, every full state, and the chain (each opening state equals the
previous part's replayed end state; part 0 opens with the -v2 MissionLoad
state).  The first 128 frames must equal the committed M2.2 capture.

    python3 -B pesquisas-paralelas/missoes/pacotes_quadros_missao.py --dir .local/segmentos/m2-3 \
        --politica pesquisas-paralelas/missoes/validacao/m2-3-politica-comparacao-9200-quadros.json \
        --saida pesquisas-paralelas/missoes/evidencias/m2-3/captura-quadros9200-monde01-exibicao-v2
"""
import argparse
import bisect
import hashlib
import json
import lzma
from pathlib import Path
import struct
import sys

import ambiente_missoes
import delta_estado_missao as delta
from emulador import HASH_ORIGINAL

ROOT = ambiente_missoes.ROOT
LIMITES = (1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 8990, 9200)
ESTADOS_JANELA = (8999, 9000, 9176)
CAPTURA_M22 = 'pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz'
FILTRO = [dict(id=lzma.FILTER_LZMA2, preset=9 | lzma.PRESET_EXTREME)]


class Mascara:
    def __init__(self, faixas):
        self.faixas = sorted((int(a, 16), int(z, 16)) for a, z in faixas)
        self.inicios = [a for a, _ in self.faixas]
        self._cache = {}

    def no_bloco(self, base, tamanho):
        """Mask ranges intersecting [base, base+tamanho), clipped, in address order."""
        chave = (base, tamanho)
        if chave not in self._cache:
            fim, saida = base+tamanho, []
            i = max(bisect.bisect_right(self.inicios, base)-1, 0)
            while i < len(self.faixas) and self.faixas[i][0] < fim:
                a, z = self.faixas[i]
                if z > base:
                    saida.append((max(a, base), min(z, fim)))
                i += 1
            self._cache[chave] = saida
        return self._cache[chave]

    def resumos(self, estado):
        """(compared_summary, masked_sha256) of a block state."""
        comparado, mascarado = {}, hashlib.sha256()
        for nome in sorted(estado):
            if nome == 'native_stack':
                continue
            base, dados = estado[nome]
            faixas = self.no_bloco(base, len(dados))
            if faixas:
                buf = bytearray(dados)
                for a, z in faixas:
                    mascarado.update(struct.pack('<II', a, z-a))
                    mascarado.update(dados[a-base:z-base])
                    buf[a-base:z-base] = bytes(z-a)
                dados = bytes(buf)
            comparado[nome] = (base, dados)
        return delta.resumo(comparado), mascarado.hexdigest()


def quadro(fase):
    if fase == 'load_tail':
        return 0
    return int(fase[len('between_frames'):] or 1) if fase.startswith('between_frames') else int(fase[len('frame'):])


def registros(pasta):
    import segmentos_quadros_missao as seg
    for arquivo in seg.arquivos_registros(pasta):
        for linha in arquivo.open():
            yield json.loads(linha)


def entradas_nomeadas(ticks):
    import capturar_quadros_exibicao_missao as cq
    import cenarios_oraculo as cen
    import segmentos_quadros_missao as seg
    from mapa_memoria_m1 import carregar_json
    ni = carregar_json(cen.caminho('exibicao', 'captura_m1'))['named_inputs']
    e = cen.entradas_exibicao(ni['allocation_fill'], ni['clock_ms'][0], ticks=seg.ticks_exibicao(ticks))
    named = cq.sem_caminho_host(dict(m1=e.quadro.base.manifesto(), frame=e.quadro.manifesto(), display=e.manifesto()))
    named['display']['display_ticks'] = dict(
        rule='0x123456 + 40*k, k = 1..N, one answer per non-iaRandom timeGetTime/GetTickCount call', N=ticks,
        sha256_of_json_list=hashlib.sha256(json.dumps(list(e.ticks)).encode()).hexdigest(),
        first_4096_equal_reference=True)
    named['cd_audio'] = cq.AUDIO_CD
    return named, cq.DECISOES


def escrever(caminho, objeto):
    texto = (json.dumps(objeto, sort_keys=True, indent=1)+'\n').encode()
    bruto = ROOT/'.local'/'m2-3'/'partes'/(caminho.name[:-len('.xz')])
    bruto.parent.mkdir(parents=True, exist_ok=True)
    with open(bruto, 'xb') as f:
        f.write(texto)
    comprimido = lzma.compress(texto, format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, filters=FILTRO)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, 'xb') as f:
        f.write(comprimido)
    return dict(artifact=str(caminho.relative_to(ROOT)), compressed_sha256=hashlib.sha256(comprimido).hexdigest(),
                compressed_bytes=len(comprimido), raw_sha256=hashlib.sha256(texto).hexdigest(), raw_bytes=len(texto),
                raw_local_copy=str(bruto.relative_to(ROOT)))


def estado_aberto(estado, mascara):
    comparado, mascarado = mascara.resumos(estado)
    return dict(summary=delta.resumo(estado), compared_summary=comparado, masked_sha256=mascarado,
                full_state=delta.estado_completo(estado))


def empacotar(a):
    global LIMITES, ESTADOS_JANELA
    LIMITES = tuple(int(x) for x in a.limites.split(','))
    ESTADOS_JANELA = tuple(int(x) for x in a.estados.split(','))
    pasta = ROOT/a.dir
    politica_caminho = ROOT/a.politica
    politica = json.loads(politica_caminho.read_text())
    mascara = Mascara(politica['cumulative']['exclusion_mask'])
    manifesto_a = json.loads((pasta/'passo-a.json').read_text())
    final = json.loads(next(pasta.glob(f'final-*-{LIMITES[-1]:05d}.json')).read_text())
    named, decisoes = entradas_nomeadas(manifesto_a.get('ticks') or 4096)
    base = Path(a.saida)
    estado = delta.s0_exibicao()
    partes, atual, anterior_sha, inicio = [], None, None, 0
    for f in registros(pasta):
        nome = f['phase']
        if atual is None:
            atual = dict(schema='rising-lands/monde01-long-run-capture-part/1', part=len(partes),
                         frames=[inicio, LIMITES[len(partes)]], first_phase=nome, previous_part_raw_sha256=anterior_sha,
                         opening_state=estado_aberto(estado, mascara), phases=[],
                         policy=dict(path=str(politica_caminho.relative_to(ROOT)),
                                     sha256=hashlib.sha256(politica_caminho.read_bytes()).hexdigest()),
                         original_sha256=HASH_ORIGINAL,
                         scenario='exibicao', translation_executed=False, state_form='complete delta',
                         definitions=DEFINICOES)
            if not partes:
                atual.update(named_inputs=named, decisions=decisoes, state_s0_equals='-v2 MissionLoad final state')
        estado = delta.aplicar(estado, f['state_delta'], nome)
        comparado, mascarado = mascara.resumos(estado)
        f['state_after'].update(compared_summary=comparado, masked_sha256=mascarado)
        if nome.startswith('frame') and quadro(nome) in ESTADOS_JANELA:
            f['state_after']['full_state'] = delta.estado_completo(estado)
        atual['phases'].append(f)
        if nome.startswith('frame') and quadro(nome) == LIMITES[len(partes)]:
            atual['last_phase'] = nome
            if len(partes) == len(LIMITES)-1:
                atual.update({k: final[k] for k in ('allocations', 'entry_trace', 'declared_windows_answers',
                                                    'import_resolutions', 'code_integrity')})
            caminho = ROOT/f'{base}.parte{len(partes):02d}.json.xz'
            registro = escrever(caminho, atual)
            registro.update(part=len(partes), frames=atual['frames'], first_phase=atual['first_phase'],
                            last_phase=nome, phases=len(atual['phases']))
            partes.append(registro)
            print(json.dumps(registro), flush=True)
            anterior_sha, inicio, atual = registro['raw_sha256'], quadro(nome)+1, None
    if atual is not None or len(partes) != len(LIMITES):
        raise RuntimeError('The records do not end exactly at the last part boundary')
    return partes, politica_caminho


def verificar(partes):
    """Re-read every written part and check it (see the module docstring)."""
    s0 = delta.s0_exibicao()
    politica = None
    estado, resultado = None, []
    import capturar_quadros_exibicao_missao  # noqa: F401  (named-input helpers share its imports)
    m22, _ = delta.carregar(ROOT/CAPTURA_M22)
    ref = {}
    for f in m22['phases']:
        f = dict(f)
        f.pop('seconds', None)
        f['state_after'] = {k: v for k, v in f['state_after'].items() if k != 'full_state'}
        ref[f['phase']] = json.dumps(f, sort_keys=True)
    iguais_m22 = 0
    for p in partes:
        bruto = lzma.decompress((ROOT/p['artifact']).read_bytes())
        if hashlib.sha256(bruto).hexdigest() != p['raw_sha256']:
            raise RuntimeError(f"part {p['part']}: raw hash mismatch")
        parte = json.loads(bruto)
        if politica is None:
            politica = json.loads((ROOT/parte['policy']['path']).read_text())
            mascara = Mascara(politica['cumulative']['exclusion_mask'])
        aberto = {n: (int(b['base'], 16), delta._decodificar(b)) for n, b in parte['opening_state']['full_state'].items()}
        esperado = {n: v for n, v in (s0 if estado is None else estado).items() if n != 'native_stack'}
        if aberto != esperado:
            raise RuntimeError(f"part {p['part']}: opening state is not the previous part's end state")
        comparado, mascarado = mascara.resumos(aberto)
        if (delta.resumo(aberto), comparado, mascarado) != (parte['opening_state']['summary'],
                                                           parte['opening_state']['compared_summary'],
                                                           parte['opening_state']['masked_sha256']):
            raise RuntimeError(f"part {p['part']}: opening-state hashes differ")
        estado, cheios = aberto, 0
        for f in parte['phases']:
            estado = delta.aplicar(estado, f['state_delta'], f['phase'])
            apos = f['state_after']
            comparado, mascarado = mascara.resumos(estado)
            if (delta.resumo(estado), comparado, mascarado) != (apos['summary'], apos['compared_summary'],
                                                               apos['masked_sha256']):
                raise RuntimeError(f"{f['phase']}: replayed hashes differ")
            if 'full_state' in apos:
                cheio = {n: (int(b['base'], 16), delta._decodificar(b)) for n, b in apos['full_state'].items()}
                if cheio != {n: v for n, v in estado.items() if n != 'native_stack'}:
                    raise RuntimeError(f"{f['phase']}: full state differs from the replay")
                cheios += 1
            if f['phase'] in ref:
                g = dict(f, state_after={k: v for k, v in apos.items()
                                         if k not in ('compared_summary', 'masked_sha256', 'full_state')})
                if json.dumps(g, sort_keys=True) != ref[f['phase']]:
                    raise RuntimeError(f"{f['phase']}: differs from the committed M2.2 capture")
                iguais_m22 += 1
        resultado.append(dict(part=p['part'], phases=len(parte['phases']), full_states_checked=cheios+1))
    return dict(result='equal', parts=resultado, m2_2_phases_equal=iguais_m22,
                chain='every opening state equals the previous part replayed end state; part 0 opens with s0')


DEFINICOES = dict(
    mask='policy cumulative.exclusion_mask: sorted address ranges [start, end)',
    compared_summary='resumo_imagem of the state (native_stack excluded) with every masked byte set to 0: blocks '
                     'sorted by name, each hashed as struct.pack("<II", base, size) + bytes',
    masked_sha256='SHA-256 over, for each block sorted by name and each mask range intersecting it in address '
                  'order, struct.pack("<II", start, length) + the bytes of that intersection',
    summary='resumo_imagem of the full state (native_stack excluded)',
    state_delta='complete delta (display bytes included): released, then allocated, then ranges (delta_estado_missao)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', required=True)
    ap.add_argument('--politica', required=True)
    ap.add_argument('--saida', required=True, help='repo-relative path prefix of the parts')
    ap.add_argument('--limites', default=','.join(map(str, LIMITES)), help='last frame of each part')
    ap.add_argument('--estados', default=','.join(map(str, ESTADOS_JANELA)), help='frames with a full state after them')
    a = ap.parse_args()
    manifesto_caminho = ROOT/f'{a.saida}.manifest.json'
    if manifesto_caminho.exists():
        raise SystemExit(f'Refusing to overwrite {manifesto_caminho}')
    partes, politica_caminho = empacotar(a)
    verificacao = verificar(partes)
    manifesto = dict(
        schema='rising-lands/compressed-evidence-manifest/2', capture='MONDE01 -v2 display reference, frames 0-9200',
        encoding=dict(format='xz', check='crc64', filter='lzma2', preset='9e'), parts=partes,
        policy=dict(path=str(politica_caminho.relative_to(ROOT)),
                    sha256=hashlib.sha256(politica_caminho.read_bytes()).hexdigest()),
        part_last_frames=list(LIMITES),
        window=dict(frames=[LIMITES[-2], LIMITES[-1]], full_states_after_frames=list(ESTADOS_JANELA),
                    note='every part carries complete deltas; frames 8991-9200 are the last part'),
        definitions=DEFINICOES, replay_check=verificacao,
        command='python3 -B pesquisas-paralelas/missoes/pacotes_quadros_missao.py --dir ' + a.dir +
                ' --politica ' + a.politica + ' --saida ' + a.saida)
    with open(manifesto_caminho, 'x') as f:
        json.dump(manifesto, f, indent=1)
        f.write('\n')
    print(json.dumps(dict(manifest=str(manifesto_caminho), replay=verificacao['result'],
                          total_compressed=sum(p['compressed_bytes'] for p in partes)), indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
