"""M2.2 per-frame comparison: the N-frame Python composition against an N-frame native capture (Mac mini).

    python3 -B pesquisas-paralelas/ia-runtime/comparar_quadros_ia.py \
        --captura <N-frame display capture JSON> --politica <politica_comparacao_quadros.py --quadros N report> \
        --saida pesquisas-paralelas/ia-runtime/validacao/m2-2-quadros-ia.json

Reference contract: the capture uses the schema of Missions' frame capture (``captura-quadro1-monde01-exibicao-v2``)
with phases ``load_tail, between_frames, frame1, between_frames2, frame2, ...`` (``nomes_fases``). Its
``state_s0`` must be the -v2 MissionLoad final state. Each phase must carry:
- ``state_after`` (``blocks_changed_since_previous`` and ``block_hashes``);
- ``entry``/``exit`` registers and RNGs;
- ``bindings`` and ``boundaries``.
The top-level ``allocations`` list is the record set after the last phase.

Policy: only the CUMULATIVE ``exclusion_mask`` of the N-frame report excludes bytes. The M2.1 report's
per-block mask format is accepted too.

Per phase this compares:
- every state byte outside the mask;
- both RNGs;
- the bindings and boundaries outside display context (``contexto_exibicao_ia``; an issuer that both display
  roots and logic call is matched in order against Python's events, and an unmatched one is a difference);
- for between_frames(k): the 8 exit registers, and for k >= 2 the entry registers that Python carried from
  frame(k-1) (EBX..EBP and ESP);
- the allocation-record count, and after the last phase the full records (bench call-site metadata excluded, as
  in M1/M2.1).
It also tables the HUD flag 0x4e05a2 after every between-frames phase. AffGame's store to it is derived from the
code (``affgame_hud_ia``) and checked against the capture here.

The first phase that differs stops the comparison. The report gives its first differing bytes. Locating the
writer needs a native rerun with watch hooks on those bytes, which is the Mac mini's to do.
"""
import argparse
import base64
import bisect
import hashlib
import json
import struct
import subprocess
import sys
import time
import zlib

from ambiente_ia_runtime import ROOT
from comparar_quadro1_encadeado_ia import FRONTEIRA, VINCULO, blocos_mapa, comparar_eventos
from composicao_quadros_ia import ComposicaoQuadros, PRESERVADOS_CALCUL_GAME, REGISTRADORES, fases_quadros
from contexto_exibicao_ia import ContextoAmbiguo, ContextoExibicao
from inventario_ia_runtime import OriginalImage
from reinicio_ia import DependenciaIA

METADADOS_ALOCACAO = ('caller_return', 'stack', 'freed_caller_return')
BANDEIRA_HUD = 0x4e05a2


def sha(caminho):
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


class MascaraEnderecos:
    """Exclusion ranges by address: N-frame ``[[start, end], ...]`` or M2.1 ``[{block, start, end}, ...]``."""
    def __init__(self, faixas):
        pares = sorted((int(f['start'], 16), int(f['end'], 16)) if isinstance(f, dict) else
                       (int(f[0], 16), int(f[1], 16)) for f in faixas)
        self.inicios, self.fins = [a for a, _ in pares], [z for _, z in pares]
        self.bytes = sum(z - a for a, z in pares)

    def _sobrepostas(self, base, fim):
        i = max(0, bisect.bisect_right(self.inicios, base) - 1)
        while i < len(self.inicios) and self.inicios[i] < fim:
            if self.fins[i] > base:
                yield max(self.inicios[i], base), min(self.fins[i], fim)
            i += 1

    def aplicar(self, base, dados):
        faixas = list(self._sobrepostas(base, base + len(dados)))
        if not faixas:
            return dados, 0
        b = bytearray(dados)
        for a, z in faixas:
            b[a - base:z - base] = bytes(z - a)
        return bytes(b), sum(z - a for a, z in faixas)

    def mascarado(self, endereco):
        return any(True for _ in self._sobrepostas(endereco, endereco + 1))


def carregar_politica(caminho):
    pol = json.loads(caminho.read_bytes())
    if 'cumulative' in pol:
        return pol, pol['cumulative']['exclusion_mask'], pol['display_roots']
    return pol, pol['exclusion_mask'], pol['display_roots']


def fases_referencia(cap, s0):
    """Yield (phase capture, full block state after it), rebuilding each state from the previous one."""
    estado = dict(s0)
    for fase in cap['phases']:
        for nome, bloco in fase['state_after']['blocks_changed_since_previous'].items():
            estado[nome] = (int(bloco['base'], 16), zlib.decompress(base64.b64decode(bloco['zlib_base64'])))
        estado = {n: v for n, v in estado.items() if n in fase['state_after']['block_hashes']}
        yield fase, estado


def comparar_estado(mascara, python, referencia):
    diferentes, comparados, primeiras = [], 0, {}
    for nome in sorted(set(python) | set(referencia)):
        if nome == 'native_stack':
            continue
        if nome not in python or nome not in referencia:
            diferentes.append(nome)
            primeiras.setdefault(nome, 'missing in Python' if nome not in python else 'extra in Python')
            continue
        base, o = referencia[nome]
        pb, p = python[nome]
        o, excluidos = mascara.aplicar(base, o)
        p, _ = mascara.aplicar(pb, p)
        comparados += len(o) - excluidos
        if pb != base or p != o:
            diferentes.append(nome)
            if len(primeiras) < 5:
                primeiras[nome] = [[hex(base + i), o[i], p[i]] for i in range(min(len(o), len(p)))
                                   if o[i] != p[i]][:12]
    return dict(equal=not diferentes, blocks=len(referencia), compared_bytes=comparados,
                differing_blocks=diferentes[:40], first_differences=primeiras)


def eventos_logicos(referencia, python, classe, campos):
    """Reference events outside display context, aligned with Python's events in order."""
    saida, exibicao, ambiguos_resolvidos, ambiguos_sem_par = [], [], [], []
    j = 0
    for i, e in enumerate(referencia):
        try:
            c = classe(e)
        except ContextoAmbiguo as erro:
            if j < len(python) and comparar_eventos([python[j]], [e], campos)['equal']:
                saida.append(e)
                ambiguos_resolvidos.append(dict(index=i, issuer=erro.rotina))
                j += 1
            else:
                ambiguos_sem_par.append(dict(index=i, issuer=erro.rotina, event=e.get('name') or e.get('routine')))
            continue
        if c == 'display':
            exibicao.append(i)
            continue
        saida.append(e)
        j += 1
    return saida, exibicao, ambiguos_resolvidos, ambiguos_sem_par


def comparar_eventos_fase(python, referencia, classe, campos, rotulo):
    filtrados, exibicao, resolvidos, sem_par = eventos_logicos(referencia, python, classe, campos)
    r = comparar_eventos(python, filtrados, campos)
    r.update(display_context_not_modeled=len(exibicao), shared_issuers_matched=resolvidos,
             shared_issuers_unmatched=sem_par)
    if rotulo == 'boundaries':
        r['display_context_not_modeled'] = [referencia[i]['routine'] + ' @ ' + referencia[i]['caller']
                                            for i in exibicao]
    if sem_par:
        r['equal'] = False
    return r


def comparar_alocacoes(python, referencia):
    limpo = lambda r: {k: v for k, v in r.items() if k not in METADADOS_ALOCACAO}  # noqa: E731
    a, b = [limpo(r) for r in python], [limpo(r) for r in referencia]
    dif = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    return dict(equal=a == b, python=len(a), reference=len(b),
                first_differences=[dict(index=i, python=a[i], reference=b[i]) for i in dif[:5]],
                excluded_metadata=list(METADADOS_ALOCACAO))


def comparar(captura, politica, n=None):
    """Run the composition along the capture's phases and compare each one. Returns the report body."""
    import cenarios_oraculo
    from composicao_quadros_ia import carregar_cenario_exibicao
    cap = json.loads(captura.read_bytes())
    pol, faixas, raizes = carregar_politica(politica)
    mascara = MascaraEnderecos(faixas)
    estados, cap_v2, entrada, m1 = carregar_cenario_exibicao()
    if cap['state_s0']['summary']['sha256'] != cap_v2['state_s0']['summary']['sha256']:
        raise SystemExit('The capture S0 is not the -v2 MissionLoad final state')
    nomes = [f['phase'] for f in cap['phases']]
    quadros = n if n is not None else (len(nomes) - 1) // 2
    if nomes[:2 * quadros + 1] != fases_quadros(quadros):
        raise SystemExit(f'Capture phases {nomes[:5]}... do not follow load_tail + {quadros} frames')
    imagem = OriginalImage()
    contexto = ContextoExibicao(imagem, raizes)
    comp = ComposicaoQuadros(estados['s0'], cap, entrada, m1)
    fases, hud, resultado, anterior_quadro = {}, [], 'equal', None
    referencia = fases_referencia(cap, estados['s0'])
    passos = comp.executar(quadros)
    for nome in fases_quadros(quadros):
        fase_cap, estado_ref = next(referencia)
        r = {}
        try:
            passo = next(passos)
            r['result'] = 'returned'
        except DependenciaIA as erro:
            r.update(result='stopped', stop=dict(routine=erro.rotina, site=hex(erro.sitio)))
        except Exception as erro:  # reported; the comparison stops at this phase
            r.update(result='stopped', stop=dict(type=type(erro).__name__, message=str(erro)[:500]))
        if r['result'] == 'returned':
            if passo['phase'] != nome:
                raise RuntimeError(f'Phase order: Python {passo["phase"]} vs capture {nome}')
            python = blocos_mapa(comp.mapa)
            r['state'] = comparar_estado(mascara, python, estado_ref)
            rng = {a: hex(struct.unpack('<I', comp.mapa.ler(int(a, 16), 4))[0]) for a in ('0x497164', '0x498db4')}
            r['rng'] = dict(python=rng, reference=fase_cap['exit']['rng'], equal=rng == fase_cap['exit']['rng'])
            reg = passo['registro']
            r['bindings'] = comparar_eventos_fase(reg.vinculos, fase_cap['bindings'], contexto.vinculo, VINCULO,
                                                  'bindings')
            r['boundaries'] = comparar_eventos_fase(reg.fronteiras, fase_cap['boundaries'], contexto.fronteira,
                                                    FRONTEIRA, 'boundaries')
            r['allocation_count'] = dict(python=len(comp.arena.registros), reference=fase_cap['exit']['allocations'],
                                         equal=len(comp.arena.registros) == fase_cap['exit']['allocations'])
            if nome.startswith('between_frames'):
                saida = passo['exit']
                r['registers'] = {k: dict(python=hex(saida[k]), reference=fase_cap['exit']['registers'][k],
                                          equal=hex(saida[k]) == fase_cap['exit']['registers'][k])
                                  for k in REGISTRADORES}
                if nome != 'between_frames':
                    r['carried_entry_registers'] = {
                        k: dict(python=hex(passo['entry'][k]), reference=fase_cap['entry']['registers'][k],
                                equal=hex(passo['entry'][k]) == fase_cap['entry']['registers'][k])
                        for k in PRESERVADOS_CALCUL_GAME + ('ESP',)}
                aff = [x for x in comp.ctx.raizes_nao_executadas if x['phase'] == nome and x['routine'] == 'AffGame']
                base, dados = estado_ref[next(b for b, (a, d) in estado_ref.items()
                                              if a <= BANDEIRA_HUD < a + len(d))]
                hud.append(dict(phase=nome, affgame_counter=dict(aff[-1]['reads']).get('counter'),
                                drew=aff[-1]['drew'], python=comp.mapa.ler(BANDEIRA_HUD, 1)[0],
                                reference=dados[BANDEIRA_HUD - base], masked=mascara.mascarado(BANDEIRA_HUD)))
                hud[-1]['equal'] = hud[-1]['python'] == hud[-1]['reference']
            r['equal'] = (r['state']['equal'] and r['rng']['equal'] and r['bindings']['equal'] and
                          r['boundaries']['equal'] and r['allocation_count']['equal'] and
                          all(v['equal'] for v in r.get('registers', {}).values()) and
                          all(v['equal'] for v in r.get('carried_entry_registers', {}).values()))
        else:
            r['equal'] = False
        fases[nome] = r
        print(nome, r['result'], r['equal'], r.get('stop', ''), flush=True)
        if not r['equal']:
            resultado = 'first_difference_' + nome
            break
    alocacoes = comparar_alocacoes(comp.arena.registros, cap['allocations']) if resultado == 'equal' else None
    if alocacoes and not alocacoes['equal']:
        resultado = 'allocation_records_differ'
    return dict(
        capture=dict(path=str(captura.relative_to(ROOT)), sha256=sha(captura), frames=quadros),
        policy=dict(path=str(politica.relative_to(ROOT)), sha256=sha(politica), masked_bytes=mascara.bytes,
                    format='cumulative' if 'cumulative' in pol else 'm2.1'),
        crossings=dict(count=0, writing_compared_bytes=0),
        display_roots_python=comp.ctx.raizes_nao_executadas[-12:], hud_flag=hud, phases=fases,
        allocation_records=alocacoes, summary=dict(result=resultado, phases_compared=len(fases),
                                                   phases_equal=sum(1 for v in fases.values() if v['equal'])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--captura', required=True)
    ap.add_argument('--politica', required=True)
    ap.add_argument('--quadros', type=int)
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    saida = ROOT / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    t0 = time.monotonic()
    rel = dict(schema='rising-lands/ai-runtime-m2.2-frames-comparison/1',
               source_revision=subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True,
                                              text=True).stdout.strip(),
               source_dirty_paths=subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--',
                                                  'pesquisas-paralelas/ia-runtime'], capture_output=True,
                                                 text=True).stdout.splitlines())
    rel.update(comparar(ROOT / a.captura, ROOT / a.politica, a.quadros))
    rel['seconds'] = round(time.monotonic() - t0, 1)
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(rel, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), summary=rel['summary'], seconds=rel['seconds']), indent=1))
    return 0 if rel['summary']['result'] == 'equal' else 2


if __name__ == '__main__':
    sys.exit(main())
