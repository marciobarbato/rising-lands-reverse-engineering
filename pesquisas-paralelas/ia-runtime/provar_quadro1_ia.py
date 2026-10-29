"""M2.1 formal first-frame equality proof (AI/runtime): chained Python composition vs the display -v2 reference.

    python3 -B pesquisas-paralelas/ia-runtime/provar_quadro1_ia.py \
        --saida pesquisas-paralelas/ia-runtime/validacao/m2-1-prova-quadro1.json

Reference: Missions' display scenario on Graphics' backend (the ``-v2``
artifacts). Comparison policy: ``m2-politica-comparacao-quadro1.json``. Every
state byte outside its ``exclusion_mask`` is compared; surfaces lie outside the
state.

1. **Native.** One fresh replay of the reference must reproduce every committed
   phase state, the entry trace and the boundaries. It pauses at the entries
   and call-return sites of the checkpoint routines and of every display root of
   the policy, and records:
   - the masked state hashes at each checkpoint;
   - the display-root nesting intervals, to know which bindings and boundaries
     the original issued in display context;
   - the write set of every top-level display root call.
2. **Python.** The composition (``composicao_encadeada_ia``, mode ``prova``) runs
   (a)->(b)->(c) on ONE map built from the -v2 MissionLoad final state, with ZERO
   crossings:
   - RestoreAll and AffGame use Graphics' ``efeitos_logicos_exibicao``;
   - MenuInit's display roots (DDLockSurface, FilledBox, DDUnlockSurface,
     DDFlipPage) are not executed, and their write sets are proved below;
   - DeleteBank/MemFree run on Missions' arena;
   - NextAnim* are Core's 25x17 providers.
3. **Comparison at each phase end:** every compared byte, both RNGs, the bindings
   and boundaries outside display context, the modeled registers, and the
   allocation records (the 146 freed bank records included).

The first difference stops the proof and is reported.
"""
import argparse
import hashlib
import json
import struct
import subprocess
import sys
import time

from ambiente_ia_runtime import ROOT
from bancada_quadro1_ia import MISSOES, executar_caminho_pausas
from bancos_quadro_ia import ArenaQuadro
from comparar_quadro1_encadeado_ia import (FRONTEIRA, VINCULO, blocos_mapa, comparar_eventos, estados_cenario, eventos)
from composicao_encadeada_ia import (PONTOS, ContextoEncadeado, Divergencia, Registro, Travessias, fase_cauda_carga,
                                     fase_entre_quadros_exibicao, fase_quadro)
from composicao_quadro1_ia import mundo
from inventario_ia_runtime import OriginalImage
from reinicio_ia import DependenciaIA

POLITICA = MISSOES / 'validacao/m2-politica-comparacao-quadro1.json'
FASES = ('load_tail', 'between_frames', 'frame1')
# Graphics' evidence (efeitos-logicos-exibicao.json): the nested-lock bookkeeping 0x4e17a4..ab is written and
# read only by DDLockSurface/DDUnlockSurface. It is excluded at CHECKPOINTS inside a lock only; phase ends
# use the policy mask alone.
TRANSITORIO_EXIBICAO = ((0x4e17a4, 0x4e17ac),)
METADADOS_ALOCACAO = ('caller_return', 'stack', 'freed_caller_return')


def sha(caminho):
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


class Mascara:
    def __init__(self, politica, extra=()):
        self.por_bloco = {}
        for r in politica['exclusion_mask']:
            self.por_bloco.setdefault(r['block'], []).append((int(r['start'], 16), int(r['end'], 16)))
        for inicio, fim in extra:
            self.por_bloco.setdefault('dgroup', []).append((inicio, fim))

    def aplicar(self, nome, base, dados):
        faixas = self.por_bloco.get(nome)
        if not faixas:
            return dados
        b = bytearray(dados)
        for inicio, fim in faixas:
            b[max(0, inicio - base):max(0, fim - base)] = bytes(max(0, fim - base) - max(0, inicio - base))
        return bytes(b)

    def hashes(self, blocos):
        return {n: hashlib.sha256(self.aplicar(n, b, d)).hexdigest() for n, (b, d) in blocos.items()
                if n != 'native_stack'}

    def mascarado(self, nome, endereco):
        return any(i <= endereco < f for i, f in self.por_bloco.get(nome, ()))


def coletar_original(politica, mascara_ponto):
    simbolos = OriginalImage()
    nomes = {n: a for a, ns in simbolos.names.items() for n in ns}
    raizes = set(politica['display_roots'])
    rotinas = set(PONTOS) | raizes | {'DeleteBank'}
    enderecos = {nomes[n]: f'{n}:entry' for n in rotinas if n in nomes}
    pontos, contagem, abertas, intervalos, escritas = {}, {}, [], {f: [] for f in FASES}, []
    profundidade = [0]

    def fechar(regs, b):
        """Close every open display root whose RET lands here: its return address, with ESP = entry + 4 plus
        the routine's own RET immediate (FilledBox and Box end with ``ret 8``)."""
        while abertas and abertas[-1][1] == regs['EIP'] and 4 <= regs['ESP'] - abertas[-1][2] <= 4 + 0x40:
            nome, retorno, _, fase0, n, antes = abertas.pop()
            profundidade[0] -= 1
            if profundidade[0] != 0:
                continue
            intervalos[fase0][-1][2:] = [len(b.vinculos_declarados.eventos), len(b.eventos_fronteira)]
            depois = b.imagem()
            mudancas = []
            for bloco, (base, dados) in depois.items():
                velho = antes.get(bloco)
                if velho is None:
                    mudancas.append(dict(block=bloco, event='allocated'))
                    continue
                if velho[1] != dados:
                    mudancas += [dict(block=bloco, address=hex(base + i), before=velho[1][i], after=dados[i])
                                 for i in range(len(dados)) if dados[i] != velho[1][i]]
            mudancas += [dict(block=bloco, event='released') for bloco in antes if bloco not in depois]
            escritas.append(dict(phase=fase0, routine=nome, caller_return=hex(retorno), occurrence=n,
                                 changes=mudancas))

    def observador(rotulo, fase, regs, b):
        fechar(regs, b)
        nome, onde = rotulo.split(':')
        if onde != 'entry':
            return
        retorno = struct.unpack('<I', bytes(b.cpu.mem_read(regs['ESP'], 4)))[0]
        k = (fase, nome, retorno)
        n = contagem.get(k, 0)
        contagem[k] = n + 1
        imagem = b.imagem()
        pontos[k + (n,)] = mascara_ponto.hashes(imagem)
        if nome in raizes:
            topo = profundidade[0] == 0
            if topo:
                intervalos[fase].append([len(b.vinculos_declarados.eventos), len(b.eventos_fronteira), None, None])
            profundidade[0] += 1
            abertas.append((nome, retorno, regs['ESP'], fase, n, imagem if topo else None))
            b.pausa_enderecos.pausar_em(retorno, f'{nome}:return')

    b, cap, reproducao = executar_caminho_pausas(enderecos, observador, cenario='exibicao')
    inicio = {p['phase']: (p['entry']['bindings'], p['entry']['boundaries']) for p in cap['phases']}
    contexto = {}
    nao_fechados = []
    for fase in FASES:
        v0, f0 = inicio[fase]
        nao_fechados += [dict(phase=fase, interval=x) for x in intervalos[fase] if x[2] is None]
        fechados = [x for x in intervalos[fase] if x[2] is not None]
        contexto[fase] = dict(bindings=sorted({i - v0 for a, _, z, _ in fechados for i in range(a, z)}),
                              boundaries=sorted({i - f0 for _, a, _, z in fechados for i in range(a, z)}))
    return pontos, contexto, escritas, reproducao, dict(open_roots=[(a[0], hex(a[1]), a[3]) for a in abertas],
                                                        unclosed_intervals=nao_fechados)


def provar_escritas(escritas, mascara, estados):
    """Each non-executed top-level display root call: every changed byte masked, outside the state, or the
    self-restoring lock bookkeeping (restored before its phase ends)."""
    saida, comparados_total = [], 0
    for e in escritas:
        mascarados, comparados, outros = 0, [], []
        for c in e['changes']:
            if 'event' in c:
                outros.append(c)
            elif mascara.mascarado(c['block'], int(c['address'], 16)):
                mascarados += 1
            else:
                comparados.append(c)
        saida.append(dict(phase=e['phase'], routine=e['routine'], caller_return=e['caller_return'],
                          masked_bytes=mascarados, compared_bytes=comparados, block_events=outros))
        comparados_total += len(comparados)
    # Compared bytes written by display roots must hold, at the end of their phase, the value they had
    # before the phase's first display-root write (lock/unlock pairs restore their bookkeeping).
    restauracao = []
    por_fase = {}
    for e in saida:
        for c in e['compared_bytes']:
            por_fase.setdefault(e['phase'], {}).setdefault((c['block'], c['address']), []).append(c)
    for fase, bytes_ in por_fase.items():
        for (bloco, endereco), mudancas in sorted(bytes_.items()):
            base, dados = estados[fase][bloco]
            final = dados[int(endereco, 16) - base]
            restauracao.append(dict(phase=fase, block=bloco, address=endereco, first_before=mudancas[0]['before'],
                                    phase_end=final, restored=final == mudancas[0]['before'],
                                    writers=len(mudancas)))
    return saida, restauracao, comparados_total


def comparar_estado(mascara, python, referencia):
    p, r = mascara.hashes(python), mascara.hashes(referencia)
    diferentes = sorted(n for n in set(p) | set(r) if p.get(n) != r.get(n))
    primeiros = {}
    for n in diferentes[:5]:
        if n not in python or n not in referencia:
            primeiros[n] = 'missing in Python' if n not in python else 'extra in Python'
            continue
        base, a = python[n]
        _, o = referencia[n]
        a, o = mascara.aplicar(n, base, a), mascara.aplicar(n, base, o)
        primeiros[n] = [[hex(base + i), o[i], a[i]] for i in range(len(o)) if a[i] != o[i]][:12]
    compared = sum(len(d) - sum(min(f, base + len(d)) - max(i, base) for i, f in mascara.por_bloco.get(n, ())
                                if i < base + len(d) and f > base)
                   for n, (base, d) in referencia.items())
    return dict(equal=not diferentes, blocks=len(r), compared_bytes=compared, differing_blocks=diferentes[:40],
                first_differences=primeiros)


def comparar_alocacoes(python, referencia):
    limpo = lambda r: {k: v for k, v in r.items() if k not in METADADOS_ALOCACAO}  # noqa: E731
    a, b = [limpo(r) for r in python], [limpo(r) for r in referencia]
    dif = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    return dict(equal=a == b, python=len(a), reference=len(b), first_differences=[
        dict(index=i, python=a[i], reference=b[i]) for i in dif[:5]],
        freed_by_memfree_total=sum(1 for x in referencia if x.get('freed_caller_return') == '0x467ef0'),
        excluded_metadata=list(METADADOS_ALOCACAO))


def verificar_rodada4(mascara):
    """Round-4 crossings' written bytes (validacao/m2-quadro1-exibicao-ia.json) against the policy mask."""
    r4 = json.loads((ROOT / 'pesquisas-paralelas/ia-runtime/validacao/m2-quadro1-exibicao-ia.json').read_text())
    saida = []
    for fase, v in r4['phases'].items():
        for c in v['crossings']:
            classificacao = 'logic' if c['owner'] == 'core' else 'display'
            nao_mascarados, blocos = [], {}
            for bloco, mud in c['changed_bytes'].items():
                if isinstance(mud, list):
                    nao_mascarados += [a for a, _, _ in mud if not mascara.mascarado(bloco, int(a, 16))]
                else:
                    blocos[bloco] = 'masked' if mascara.mascarado(bloco, int(mud['first'], 16)) and \
                        mascara.mascarado(bloco, int(mud['last'], 16)) else 'compared'
            compared_blocks = sorted(b for b, k in blocos.items() if k == 'compared')
            sem_escrita = not c['changed_bytes'] and not c['released']
            politica = ('no write' if sem_escrita else
                        'logic (compared)' if nao_mascarados or compared_blocks else 'display-only (masked)')
            if c['released']:
                politica += f"; {c['released']} freed allocation records compared (coordinator decision)"
            acordo = sem_escrita or (classificacao == 'display') == politica.startswith('display-only') and not c['released']
            saida.append(dict(phase=fase, routine=c['routine'], round4=classificacao, policy=politica,
                              agree=acordo, unmasked_bytes=nao_mascarados, compared_blocks=compared_blocks))
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--dados-originais', help='local pickle cache of the native collection (.local only)')
    a = ap.parse_args()
    saida = ROOT / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    import pickle
    import cenarios_oraculo
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'pesquisas-paralelas/ia-runtime'],
                          capture_output=True, text=True).stdout
    t0 = time.monotonic()
    politica = json.loads(POLITICA.read_bytes())
    referencias = {k: dict(path=str(cenarios_oraculo.caminho('exibicao', k).relative_to(ROOT)),
                           sha256=sha(cenarios_oraculo.caminho('exibicao', k)))
                   for k in ('entrada', 'captura_m1', 'captura_quadro', 'rastro_quadro')}
    for k in ('entrada', 'captura_m1', 'captura_quadro'):
        if politica['reference'][k]['sha256'] != referencias[k]['sha256']:
            raise SystemExit(f'Policy reference {k} differs from the committed -v2 artifact')
    mascara = Mascara(politica)
    mascara_ponto = Mascara(politica, TRANSITORIO_EXIBICAO)
    cache = ROOT / a.dados_originais if a.dados_originais else None
    if cache is not None and cache.exists():
        pontos, contexto, escritas, reproducao, abertas = pickle.loads(cache.read_bytes())
        reproducao = dict(reproducao, note='loaded from a local cache of an earlier native collection')
    else:
        pontos, contexto, escritas, reproducao, abertas = coletar_original(politica, mascara_ponto)
        if cache is not None:
            cache.write_bytes(pickle.dumps((pontos, contexto, escritas, reproducao, abertas)))
    estados, cap = estados_cenario('exibicao')
    fases = {p['phase']: p for p in cap['phases']}
    entrada = json.loads(cenarios_oraculo.caminho('exibicao', 'entrada').read_bytes())
    m1 = json.loads(cenarios_oraculo.caminho('exibicao', 'captura_m1').read_bytes())
    superficie = next(s for s in fases['load_tail']['display_state']['surfaces'] if s['role'] == 'offscreen')
    mapa, prov = mundo(estados['s0'])
    arena = ArenaQuadro(mapa, entrada['arena'], m1['allocations'])
    ctx = ContextoEncadeado(OriginalImage(), 'exibicao', modo='prova', arena=arena,
                            superficie=int(superficie['pixels'], 16))
    travessias = Travessias(pontos, {}, lambda m: mascara_ponto.hashes(blocos_mapa(m)))
    prova_escritas, restauracao, escritas_comparadas = provar_escritas(escritas, mascara, estados)
    relatorio = dict(
        schema='rising-lands/ai-runtime-m2.1-first-frame-proof/1', source_revision=revisao,
        source_dirty_paths=sujo.splitlines(), references=referencias,
        policy=dict(path=str(POLITICA.relative_to(ROOT)), sha256=sha(POLITICA), masked_bytes=politica['totals'],
                    exclusion_ranges=len(politica['exclusion_mask'])),
        path_reproduction=reproducao, display_root_tracking=abertas, native_checkpoints=len(pontos),
        declared_inputs=dict(offscreen_surface_pixels=superficie['pixels'],
                             offscreen_provenance='reference display_state (Graphics backend layout): the EAX '
                                                  'DDLockSurface returns to MenuInit, stored at 0x508f70',
                             frame_inputs=cap['named_inputs']['frame']),
        crossings=dict(count=0, writing_compared_bytes=0,
                       note='the composition crosses nothing; travessias carries no crossing data in mode prova'),
        display_roots_not_executed=dict(calls=prova_escritas, compared_bytes_written=escritas_comparadas,
                                        restoration=restauracao,
                                        all_restored=all(r['restored'] for r in restauracao)),
        round4_classification_check=verificar_rodada4(mascara),
        phases={})
    resultado = 'equal'
    for fase in FASES:
        registro = Registro(fase)
        e = fases[fase]
        regs = {k: int(v, 16) for k, v in e['entry']['registers'].items()}
        r = {}
        try:
            if fase == 'load_tail':
                fase_cauda_carga(mapa, prov, ctx, registro, travessias, regs)
            elif fase == 'between_frames':
                entradas = dict(salvo_edx=0, salvo_ecx=0, salvo_ebx=0, msg=(0x3000000, 0, 0, 0), peek_message=0,
                                cursor=tuple(cap['named_inputs']['frame']['cursor']))
                saida_regs = fase_entre_quadros_exibicao(mapa, prov, ctx, registro, travessias, regs, entradas)
                r['registers'] = {k: dict(python=hex(saida_regs[k]), reference=e['exit']['registers'][k],
                                          equal=hex(saida_regs[k]) == e['exit']['registers'][k])
                                  for k in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP')}
            else:
                fase_quadro(mapa, prov, ctx, registro, travessias, regs)
            r['result'] = 'returned'
        except Divergencia as erro:
            r.update(result='diverged', at=dict(routine=erro.rotina, key=[str(x) for x in erro.chave]),
                     differing_blocks=erro.blocos[:40])
        except DependenciaIA as erro:
            r.update(result='stopped', stop=dict(routine=erro.rotina, site=hex(erro.sitio)))
        except Exception as erro:
            import traceback
            r.update(result='stopped', stop=dict(type=type(erro).__name__, message=str(erro)[:500]),
                     traceback=traceback.format_exc()[-3000:])
        if r['result'] == 'returned':
            python = blocos_mapa(mapa)
            r['state'] = comparar_estado(mascara, python, estados[fase])
            rng = {'0x497164': hex(struct.unpack('<I', mapa.ler(0x497164, 4))[0]),
                   '0x498db4': hex(struct.unpack('<I', mapa.ler(0x498db4, 4))[0])}
            r['rng'] = dict(python=rng, reference=e['exit']['rng'], equal=rng == e['exit']['rng'])
            exibicao_v = set(contexto[fase]['bindings'])
            exibicao_f = set(contexto[fase]['boundaries'])
            ref_v = [x for i, x in enumerate(e['bindings']) if i not in exibicao_v]
            ref_f = [x for i, x in enumerate(e['boundaries']) if i not in exibicao_f]
            r['bindings'] = comparar_eventos(registro.vinculos, ref_v, VINCULO)
            r['bindings']['display_context_not_modeled'] = len(exibicao_v)
            r['boundaries'] = comparar_eventos(registro.fronteiras, ref_f, FRONTEIRA)
            r['boundaries']['display_context_not_modeled'] = [e['boundaries'][i]['routine'] + ' @ ' +
                                                               e['boundaries'][i]['caller'] for i in sorted(exibicao_f)]
            r['allocation_records'] = comparar_alocacoes(arena.registros, cap['allocations'])
            r['allocation_records']['freed_by_python_composition'] = sum(
                1 for x, y in zip(arena.registros, m1['allocations']) if y['active'] and not x['active'])
            r['equal'] = (r['state']['equal'] and r['rng']['equal'] and r['bindings']['equal'] and
                          r['boundaries']['equal'] and r['allocation_records']['equal'] and
                          all(v['equal'] for v in r.get('registers', {}).values()))
        else:
            r['equal'] = False
        r['checkpoints'] = dict(total=sum(1 for v in travessias.verificados if v['phase'] == fase),
                                equal=sum(1 for v in travessias.verificados if v['phase'] == fase and v['equal']))
        r['display_roots_python'] = [x for x in ctx.raizes_nao_executadas if x['phase'] == fase]
        relatorio['phases'][fase] = r
        print(fase, r['result'], r['equal'], r.get('stop') or r.get('at') or '', flush=True)
        if not r['equal']:
            resultado = 'first_difference_' + fase
            break
    relatorio['unmodeled'] = [
        'stack words of MCICD_Play in the CalculGame frame bodies (uninitialized caller locals)',
        'EFLAGS and EIP',
        'bindings and boundaries issued inside policy display roots (DirectDraw COM calls, display ticks, palette, '
        'LoadPie inside RestoreAll): Graphics\' provider produces none; counted per phase',
        'masked display-only state (policy exclusion_mask) and the surfaces (outside the state)',
        'ProgIteration frame words of phase (b): saved EDX/ECX/EBX = 0 and the MSG buffer [0x3000000, 0, 0, 0] '
        '(declared from the boundary registers and the bench loop frame)']
    relatorio['summary'] = dict(result=resultado, phases={f: v.get('equal') for f, v in relatorio['phases'].items()},
                                crossings_writing_compared_bytes=0,
                                display_root_compared_writes_restored=relatorio['display_roots_not_executed'][
                                    'all_restored'])
    relatorio['seconds'] = round(time.monotonic() - t0, 3)
    ok = (reproducao['passed'] and cache is None and resultado == 'equal' and not abertas['open_roots']
          and not abertas['unclosed_intervals'])
    if not ok:
        saida = ROOT / '.local' / ('m2-1-proof-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), summary=relatorio['summary'], seconds=relatorio['seconds']), indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
