"""M2.2 per-frame comparison: the N-frame Python composition against an N-frame native capture (Mac mini).

    python3 -B pesquisas-paralelas/ia-runtime/comparar_quadros_ia.py \
        --captura <N-frame display capture JSON> --politica <politica_comparacao_quadros.py --quadros N report> \
        --saida pesquisas-paralelas/ia-runtime/validacao/m2-2-quadros-ia.json

Reference contract: the capture uses the schema of Missions' frame capture (``captura-quadro1-monde01-exibicao-v2``)
with phases ``load_tail, between_frames, frame1, between_frames2, frame2, ...`` (``nomes_fases``). Its
``state_s0`` must be the -v2 MissionLoad final state. The file may be xz-compressed (``.xz``); ``--sha256``
pins the hash of the raw JSON. Each phase must carry:
- its state, in one of two forms:
  - -v2 form: ``state_after.blocks_changed_since_previous`` (full changed blocks) and ``block_hashes``;
  - M2.2 delta form (Mac mini): ``state_delta`` against the previous phase's state, with
    ``released`` (block names), ``allocated`` (``{name: {base, zlib_base64}}``) and ``ranges``
    (``[{address, zlib_base64 | hex}]``, each inside one block), applied in that order.
    ``state_after.summary`` (Missions' ``resumo_imagem``: blocks, bytes, SHA-256 over the name-sorted blocks
    as ``<II base, size>`` + bytes) checks the replay. At checkpoint frames, ``state_after.full_state``
    (``{name: {base, zlib_base64}}``) must equal the replayed state exactly;
- ``entry``/``exit`` registers and RNGs;
- ``bindings`` and ``boundaries``.
The top-level ``allocations`` list is the record set after the last phase. Any replay or checkpoint mismatch
stops the comparison as a capture-integrity failure before Python is compared.

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

``--parte`` compares one self-contained part of a long run (M2.3, Missions' ``pacotes_quadros_missao``).
A part opens with a full state and carries complete deltas, and each phase adds ``compared_summary`` and
``masked_sha256``. Python starts from the opening state, every phase hash and full state is checked by replay,
and each part runs independently of the others.

``--a-partir-de K`` starts Python from the reference state after frame K (for example a full state at frame
8,999 for M2.3b), with the capture's allocation records and the between_frames(K+1) entry registers as
declared inputs. The full chain from load_tail stays the default.

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


class IntegridadeCaptura(RuntimeError):
    """The capture's own replay (deltas, summaries, checkpoint full states) is inconsistent."""


def resumo_estado(blocos):
    """Missions' ``oraculo_carga_missao.resumo_imagem`` over a block dict (name -> (base, bytes))."""
    h = hashlib.sha256()
    for nome in sorted(blocos):
        base, dados = blocos[nome]
        h.update(struct.pack('<II', base, len(dados)))
        h.update(dados)
    return dict(blocks=len(blocos), bytes=sum(len(d) for _, d in blocos.values()), sha256=h.hexdigest())


def resumos_mascarados(mascara, blocos):
    """(compared_summary, masked_sha256) with the definitions of Missions' ``pacotes_quadros_missao``.

    compared_summary is ``resumo_imagem`` with every masked byte set to 0. masked_sha256 is SHA-256 over, for
    each block sorted by name and each mask range intersecting it in address order,
    ``<II start, length>`` + those bytes. ``native_stack`` is never a block.
    """
    comparado, mascarado = {}, hashlib.sha256()
    for nome in sorted(blocos):
        if nome == 'native_stack':
            continue
        base, dados = blocos[nome]
        faixas = list(mascara._sobrepostas(base, base + len(dados)))
        if faixas:
            buf = bytearray(dados)
            for a, z in faixas:
                mascarado.update(struct.pack('<II', a, z - a))
                mascarado.update(dados[a - base:z - base])
                buf[a - base:z - base] = bytes(z - a)
            dados = bytes(buf)
        comparado[nome] = (base, dados)
    return resumo_estado(comparado), mascarado.hexdigest()


def _dados(campo):
    if 'zlib_base64' in campo:
        return zlib.decompress(base64.b64decode(campo['zlib_base64']))
    return bytes.fromhex(campo['hex'])


def aplicar_delta(estado, delta, fase):
    """``state_delta`` onto a copy of ``estado``: released, then allocated, then the byte ranges."""
    novo = dict(estado)
    for nome in delta.get('released', ()):
        if nome not in novo:
            raise IntegridadeCaptura(f'{fase}: released block {nome} is not live')
        del novo[nome]
    for nome, bloco in delta.get('allocated', {}).items():
        if nome in novo:
            raise IntegridadeCaptura(f'{fase}: allocated block {nome} already live')
        novo[nome] = (int(bloco['base'], 16), _dados(bloco))
    por_base = sorted((b, n) for n, (b, _) in novo.items())
    bases = [b for b, _ in por_base]
    editados = {}
    for faixa in delta.get('ranges', ()):
        endereco, dados = int(faixa['address'], 16), _dados(faixa)
        i = bisect.bisect_right(bases, endereco) - 1
        nome = por_base[i][1] if i >= 0 else None
        if nome is None or endereco + len(dados) > novo[nome][0] + len(novo[nome][1]):
            raise IntegridadeCaptura(f'{fase}: range 0x{endereco:x}+{len(dados)} is not inside one live block')
        if nome not in editados:
            editados[nome] = bytearray(novo[nome][1])
        o = endereco - novo[nome][0]
        editados[nome][o:o + len(dados)] = dados
    for nome, dados in editados.items():
        novo[nome] = (novo[nome][0], bytes(dados))
    return novo


def fases_referencia(cap, s0, mascara=None):
    """Yield (phase capture, full block state after it, integrity record), replaying from ``s0``.

    With ``mascara``, a phase's ``compared_summary`` and ``masked_sha256`` (M2.3 parts) are checked too."""
    estado = dict(s0)
    for fase in cap['phases']:
        apos = fase['state_after']
        if 'blocks_changed_since_previous' in apos:
            estado = dict(estado)
            for nome, bloco in apos['blocks_changed_since_previous'].items():
                estado[nome] = (int(bloco['base'], 16), _dados(bloco))
            estado = {n: v for n, v in estado.items() if n in apos['block_hashes']}
            forma = 'v2_blocks'
        else:
            estado = aplicar_delta(estado, fase['state_delta'], fase['phase'])
            forma = 'delta'
        integridade = dict(form=forma)
        if 'summary' in apos:
            resumo = resumo_estado({n: v for n, v in estado.items() if n != 'native_stack'})
            integridade['summary_equal'] = resumo == apos['summary']
            if not integridade['summary_equal']:
                raise IntegridadeCaptura(f"{fase['phase']}: replayed state {resumo} != summary {apos['summary']}")
        if 'compared_summary' in apos or 'masked_sha256' in apos:
            if mascara is None:
                raise IntegridadeCaptura(f"{fase['phase']}: compared_summary present but no mask given")
            comparado, mascarado = resumos_mascarados(mascara, estado)
            integridade['compared_summary_equal'] = comparado == apos.get('compared_summary', comparado)
            integridade['masked_sha256_equal'] = mascarado == apos.get('masked_sha256', mascarado)
            if not (integridade['compared_summary_equal'] and integridade['masked_sha256_equal']):
                raise IntegridadeCaptura(f"{fase['phase']}: replayed compared_summary/masked_sha256 differ")
        if 'full_state' in apos:
            completo = {n: (int(b['base'], 16), _dados(b)) for n, b in apos['full_state'].items()}
            atual = {n: v for n, v in estado.items() if n in completo or n != 'native_stack'}
            integridade['checkpoint_full_state_equal'] = completo == atual
            if not integridade['checkpoint_full_state_equal']:
                diferentes = sorted(n for n in set(completo) | set(atual) if completo.get(n) != atual.get(n))
                raise IntegridadeCaptura(f"{fase['phase']}: checkpoint full state differs from the replay in "
                                         f"{diferentes[:8]}")
        elif forma == 'delta' and 'summary' not in apos:
            raise IntegridadeCaptura(f"{fase['phase']}: delta phase without a summary hash")
        yield fase, estado, integridade


def carregar_captura(caminho, sha256_bruto=None):
    """The capture JSON, xz-decompressed when the name ends in .xz; the raw JSON hash checked when pinned."""
    import lzma
    bruto = caminho.read_bytes()
    if caminho.suffix == '.xz':
        bruto = lzma.decompress(bruto)
    h = hashlib.sha256(bruto).hexdigest()
    if sha256_bruto is not None and h != sha256_bruto:
        raise IntegridadeCaptura(f'raw capture SHA-256 {h} != pinned {sha256_bruto}')
    return json.loads(bruto), h


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


def alocacoes_no_ponto(cap, fase_ponto, seguintes):
    """Allocation records live after ``fase_ponto``.

    They come from ``checkpoint_allocations[phase]`` or, when the capture begins after the checkpoint,
    ``allocations_at_start``. Otherwise the final ``allocations`` list is used, and only when no later phase
    allocates or releases a block and every later phase keeps the same record count.
    """
    if fase_ponto in cap.get('checkpoint_allocations', {}):
        return cap['checkpoint_allocations'][fase_ponto], 'checkpoint_allocations'
    if 'allocations_at_start' in cap and cap['phases'][0]['phase'] == seguintes[0]['phase']:
        return cap['allocations_at_start'], 'allocations_at_start'
    contagens = {f['exit']['allocations'] for f in seguintes} | {len(cap['allocations'])}
    mudancas = [f['phase'] for f in seguintes if f.get('state_delta', {}).get('allocated')
                or f.get('state_delta', {}).get('released')]
    if len(contagens) != 1 or mudancas:
        raise SystemExit(f'No allocation records at {fase_ponto}: later phases change them ({mudancas[:3]}, '
                         f'counts {sorted(contagens)[:4]})')
    return cap['allocations'], 'final allocations (unchanged after the checkpoint)'


INDICADORES = (('world_rng', 0x497164, 4), ('ai_rng', 0x498db4, 4), ('cursor_4e1d18', 0x4e1d18, 1),
               ('hud_4e05a2', BANDEIRA_HUD, 1), ('counter', 0x508f7c, 4), ('view_x', 0x508720, 2),
               ('view_y', 0x508722, 2))


def ler_estado(estado, endereco, largura):
    for base, dados in estado.values():
        if base <= endereco and endereco + largura <= base + len(dados):
            return int.from_bytes(dados[endereco - base:endereco - base + largura], 'little')
    return None


def comparar_sequencia(comp, nomes, quadros, referencia, mascara, contexto, continuar=False):
    """Run ``comp`` for ``quadros`` frames and compare each phase with the next reference phase.

    Returns (per-phase records, HUD table, result).
    """
    fases, hud, resultado = {}, [], 'equal'
    passos = comp.executar(quadros)
    primeira = True
    for nome in nomes:
        try:
            fase_cap, estado_ref, integridade = next(referencia)
        except IntegridadeCaptura as erro:
            fases[nome] = dict(result='capture_integrity_failure', message=str(erro), equal=False)
            print(nome, 'capture integrity failure:', erro, flush=True)
            resultado = 'capture_integrity_failure_' + nome
            break
        r = dict(reference_integrity=integridade)
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
            if 'compared_summary' in fase_cap['state_after']:
                comparado, _ = resumos_mascarados(mascara, python)
                r['compared_summary'] = dict(python=comparado['sha256'],
                                             reference=fase_cap['state_after']['compared_summary']['sha256'],
                                             equal=comparado == fase_cap['state_after']['compared_summary'])
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
                if not primeira:
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
            r['indicators'] = {nome_: dict(python=int.from_bytes(comp.mapa.ler(a, k), 'little'),
                                           reference=ler_estado(estado_ref, a, k)) for nome_, a, k in INDICADORES}
            for v in r['indicators'].values():
                v['equal'] = v['python'] == v['reference']
            r['equal'] = (r['state']['equal'] and r.get('compared_summary', {}).get('equal', True) and
                          r['rng']['equal'] and r['bindings']['equal'] and
                          r['boundaries']['equal'] and r['allocation_count']['equal'] and
                          all(v['equal'] for v in r.get('registers', {}).values()) and
                          all(v['equal'] for v in r.get('carried_entry_registers', {}).values()))
        else:
            r['equal'] = False
        fases[nome] = r
        primeira = False
        print(nome, r['result'], r['equal'], r.get('stop', ''), flush=True)
        if not r['equal']:
            if resultado == 'equal':
                resultado = 'first_difference_' + nome
            if not continuar or r['result'] != 'returned':
                break
    return fases, hud, resultado


def quadro_da_fase(fase):
    if fase == 'load_tail':
        return 0
    if fase.startswith('between_frames'):
        return int(fase[len('between_frames'):] or 1)
    return int(fase[len('frame'):])


def alocacoes_da_parte(parte, cap_v2, alocacoes_caminho=None):
    """Allocation records live at a part's opening.

    They come from ``opening_state.allocations`` or from a declared file (a list, or a part or capture with
    ``allocations``). Otherwise the -v2 frame capture's final records are used, and only when every phase of the
    part keeps that count and no block is allocated or released in the part.
    """
    if 'allocations' in parte['opening_state']:
        return parte['opening_state']['allocations'], 'opening_state.allocations'
    if alocacoes_caminho is not None:
        dados, _ = carregar_captura(alocacoes_caminho)
        return (dados if isinstance(dados, list) else dados['allocations']), str(alocacoes_caminho.relative_to(ROOT))
    registros = cap_v2['allocations']
    contagens = {f['exit']['allocations'] for f in parte['phases']}
    mudancas = [f['phase'] for f in parte['phases'] if f['state_delta'].get('allocated') or
                f['state_delta'].get('released')]
    if contagens != {len(registros)} or mudancas:
        raise SystemExit(f'Part {parte.get("part")}: no allocation records at its opening (counts {sorted(contagens)}, '
                         f'block changes in {mudancas[:3]})')
    return registros, '-v2 final records (the part keeps the count and allocates/releases nothing)'


def comparar_parte(caminho, politica, sha256_bruto=None, alocacoes_caminho=None, continuar=False):
    """Compare one self-contained part of a long run (Missions' ``pacotes_quadros_missao`` format).

    The part's opening full state is checked against its summary, compared_summary and masked_sha256. Python
    starts from it (with load_tail from the -v2 MissionLoad state in part 0), every phase is replayed and checked,
    and Python is compared phase by phase. Parts are independent and can run in parallel.
    """
    from composicao_quadros_ia import carregar_cenario_exibicao
    parte, sha_bruto = carregar_captura(caminho, sha256_bruto)
    pol, faixas, raizes = carregar_politica(politica)
    if parte['policy']['sha256'] != sha(politica):
        raise SystemExit('The part was packaged with another policy file')
    mascara = MascaraEnderecos(faixas)
    estados, cap_v2, entrada, m1 = carregar_cenario_exibicao()
    aberto = parte['opening_state']
    s0 = {n: (int(b['base'], 16), _dados(b)) for n, b in aberto['full_state'].items()}
    comparado, mascarado = resumos_mascarados(mascara, s0)
    abertura = dict(summary_equal=resumo_estado(s0) == aberto['summary'],
                    compared_summary_equal=comparado == aberto['compared_summary'],
                    masked_sha256_equal=mascarado == aberto['masked_sha256'])
    if not all(abertura.values()):
        raise SystemExit(f'Part opening state does not match its own hashes: {abertura}')
    nomes = [f['phase'] for f in parte['phases']]
    named = parte.get('named_inputs') or cap_v2['named_inputs']
    captura_quadro = dict(named_inputs=named, phases=parte['phases'])
    if nomes[0] == 'load_tail':
        if s0 != {n: v for n, v in estados['s0'].items() if n != 'native_stack'}:
            raise SystemExit('Part 0 does not open with the -v2 MissionLoad final state')
        inicio, quadros = 0, (len(nomes) - 1) // 2
        comp = ComposicaoQuadros(estados['s0'], captura_quadro, entrada, m1)
        alocacoes, origem = m1['allocations'], '-v2 MissionLoad records'
    else:
        inicio, quadros = quadro_da_fase(nomes[0]) - 1, len(nomes) // 2
        alocacoes, origem = alocacoes_da_parte(parte, cap_v2, alocacoes_caminho)
        comp = ComposicaoQuadros(s0, captura_quadro, entrada, m1, inicio=inicio, alocacoes=alocacoes,
                                 regs_inicio=parte['phases'][0]['entry']['registers'])
    if nomes != fases_quadros(quadros, inicio):
        raise SystemExit(f'Part phases {nomes[:3]}... are not whole frames after frame {inicio}')
    contexto = ContextoExibicao(OriginalImage(), raizes)
    referencia = fases_referencia(dict(phases=parte['phases']), s0, mascara)
    fases, hud, resultado = comparar_sequencia(comp, nomes, quadros, referencia, mascara, contexto, continuar)
    registros = None
    if resultado == 'equal' and 'allocations' in parte:
        registros = comparar_alocacoes(comp.arena.registros, parte['allocations'])
        if not registros['equal']:
            resultado = 'allocation_records_differ'
    return dict(
        part=dict(path=str(caminho.relative_to(ROOT)), sha256=sha(caminho), raw_json_sha256=sha_bruto,
                  raw_json_sha256_pinned=sha256_bruto, number=parte.get('part'), frames=parte.get('frames'),
                  first_phase=nomes[0], last_phase=nomes[-1], previous_part_raw_sha256=parte.get(
                      'previous_part_raw_sha256'), opening_state=dict(abertura, start_frame=inicio,
                                                                       allocation_records=dict(count=len(alocacoes),
                                                                                               source=origem)),
                  named_inputs='part' if 'named_inputs' in parte else '-v2 frame capture (same declared answers)',
                  full_states=[f for f, v in fases.items() if v.get('reference_integrity', {}).get(
                      'checkpoint_full_state_equal')]),
        policy=dict(path=str(politica.relative_to(ROOT)), sha256=sha(politica), masked_bytes=mascara.bytes),
        crossings=dict(count=0, writing_compared_bytes=0), hud_flag=hud, phases=fases, allocation_records=registros,
        summary=dict(result=resultado, phases_compared=len(fases),
                     phases_equal=sum(1 for v in fases.values() if v['equal'])))


def comparar(captura, politica, n=None, sha256_bruto=None, inicio=0, continuar=False):
    """Run the composition along the capture's phases and compare each one. Returns the report body.

    ``inicio = k > 0`` starts Python from the reference state after frame(k) instead of composing frames 1..k.
    The capture either holds those phases (they are replayed and integrity-checked first) or begins at
    between_frames(k+1), with ``state_s0`` the state after frame(k).
    """
    from composicao_quadros_ia import carregar_cenario_exibicao
    cap, sha_bruto = carregar_captura(captura, sha256_bruto)
    pol, faixas, raizes = carregar_politica(politica)
    mascara = MascaraEnderecos(faixas)
    estados, cap_v2, entrada, m1 = carregar_cenario_exibicao()
    nomes = [f['phase'] for f in cap['phases']]
    comeca_no_ponto = bool(inicio) and nomes[0] == fases_quadros(1, inicio)[0]
    if comeca_no_ponto:
        s0 = {n_: (int(b['base'], 16), _dados(b)) for n_, b in cap['state_s0']['full_state'].items()}
        if resumo_estado(s0) != cap['state_s0']['summary']:
            raise SystemExit('The capture state_s0 full state does not match its summary')
        anteriores = 0
    else:
        if cap['state_s0']['summary']['sha256'] != cap_v2['state_s0']['summary']['sha256']:
            raise SystemExit('The capture S0 is not the -v2 MissionLoad final state')
        s0 = estados['s0']
        anteriores = len(fases_quadros(inicio)) if inicio else 0
    quadros = n if n is not None else (len(nomes) - anteriores - (0 if inicio else 1)) // 2
    esperado = (fases_quadros(inicio) if inicio and not comeca_no_ponto else []) + fases_quadros(quadros, inicio)
    if nomes[:len(esperado)] != esperado:
        raise SystemExit(f'Capture phases {nomes[:5]}... do not follow {esperado[:5]}...')
    imagem = OriginalImage()
    contexto = ContextoExibicao(imagem, raizes)
    referencia = fases_referencia(cap, s0, mascara)
    ponto = None
    if inicio:
        estado_ponto = s0
        for _ in range(anteriores):
            fase_cap, estado_ponto, _integridade = next(referencia)
        seguintes = cap['phases'][anteriores:anteriores + 2 * quadros]
        alocacoes, origem_alocacoes = alocacoes_no_ponto(cap, nomes[anteriores - 1] if anteriores else None,
                                                         seguintes)
        regs_inicio = seguintes[0]['entry']['registers']
        comp = ComposicaoQuadros(estado_ponto, cap, entrada, m1, inicio=inicio, alocacoes=alocacoes,
                                 regs_inicio=regs_inicio)
        ponto = dict(frame=inicio, layout='capture begins after the checkpoint' if comeca_no_ponto else
                     'replayed from state_s0 through the capture', replayed_phases=anteriores,
                     state_summary=resumo_estado({k: v for k, v in estado_ponto.items() if k != 'native_stack'}),
                     allocation_records=dict(count=len(alocacoes), source=origem_alocacoes),
                     entry_registers=regs_inicio)
    else:
        comp = ComposicaoQuadros(estados['s0'], cap, entrada, m1)
    fases, hud, resultado = comparar_sequencia(comp, fases_quadros(quadros, inicio), quadros, referencia, mascara,
                                               contexto, continuar)
    alocacoes = comparar_alocacoes(comp.arena.registros, cap['allocations']) if resultado == 'equal' else None
    if alocacoes and not alocacoes['equal']:
        resultado = 'allocation_records_differ'
    return dict(
        capture=dict(path=str(captura.relative_to(ROOT)), sha256=sha(captura), raw_json_sha256=sha_bruto,
                     raw_json_sha256_pinned=sha256_bruto, frames=quadros, checkpoint_start=ponto,
                     state_forms=sorted({v['reference_integrity']['form'] for v in fases.values()
                                         if 'reference_integrity' in v}),
                     checkpoint_full_states=[f for f, v in fases.items() if 'checkpoint_full_state_equal' in
                                             v.get('reference_integrity', {})]),
        policy=dict(path=str(politica.relative_to(ROOT)), sha256=sha(politica), masked_bytes=mascara.bytes,
                    format='cumulative' if 'cumulative' in pol else 'm2.1'),
        crossings=dict(count=0, writing_compared_bytes=0),
        display_roots_python=comp.ctx.raizes_nao_executadas[-12:], hud_flag=hud, phases=fases,
        allocation_records=alocacoes, summary=dict(result=resultado, phases_compared=len(fases),
                                                   phases_equal=sum(1 for v in fases.values() if v['equal'])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--captura', help='a whole N-frame capture')
    ap.add_argument('--parte', help='one self-contained part of a long run (M2.3)')
    ap.add_argument('--alocacoes', help='declared allocation records at the part opening (list, part or capture)')
    ap.add_argument('--politica', required=True)
    ap.add_argument('--quadros', type=int)
    ap.add_argument('--sha256', help='pinned SHA-256 of the raw (decompressed) capture JSON')
    ap.add_argument('--continuar', action='store_true',
                    help='diagnostic only (output under .local/): keep comparing after the first difference')
    ap.add_argument('--a-partir-de', type=int, default=0, metavar='K',
                    help='start Python from the reference state after frame K (checkpoint start)')
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    saida = ROOT / a.saida
    if a.continuar and not saida.resolve().is_relative_to((ROOT / '.local').resolve()):
        raise SystemExit('A --continuar diagnostic writes under .local/ only')
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    t0 = time.monotonic()
    rel = dict(schema='rising-lands/ai-runtime-m2.2-frames-comparison/1',
               source_revision=subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True,
                                              text=True).stdout.strip(),
               source_dirty_paths=subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--',
                                                  'pesquisas-paralelas/ia-runtime'], capture_output=True,
                                                 text=True).stdout.splitlines())
    if bool(a.captura) == bool(a.parte):
        raise SystemExit('Give exactly one of --captura and --parte')
    if a.parte:
        rel.update(comparar_parte(ROOT / a.parte, ROOT / a.politica, a.sha256,
                                  ROOT / a.alocacoes if a.alocacoes else None, a.continuar))
    else:
        rel.update(comparar(ROOT / a.captura, ROOT / a.politica, a.quadros, a.sha256, a.a_partir_de, a.continuar))
    rel['diagnostic_continued_after_difference'] = a.continuar
    rel['seconds'] = round(time.monotonic() - t0, 1)
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(rel, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), summary=rel['summary'], seconds=rel['seconds']), indent=1))
    return 0 if rel['summary']['result'] == 'equal' else 2


if __name__ == '__main__':
    sys.exit(main())
