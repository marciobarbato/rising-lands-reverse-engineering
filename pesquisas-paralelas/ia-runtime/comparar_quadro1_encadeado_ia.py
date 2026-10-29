"""M2.1: the chained Python composition of MONDE01 (a)->(b)->(c) against the original, per scenario.

    python3 -B pesquisas-paralelas/ia-runtime/comparar_quadro1_encadeado_ia.py --cenario exibicao \
        --saida pesquisas-paralelas/ia-runtime/validacao/m2-quadro1-exibicao-ia.json

1. A native replay of Missions' committed first-frame path for the scenario
   (which must reproduce every committed phase state, the entry trace and the
   boundaries) pauses, without executing anything extra:
   - at every checkpoint routine entry, keyed by phase, routine, call-return
     site and occurrence, where it records all block hashes;
   - at every crossing routine entry and its call-return site, where it records
     the changed, allocated and released blocks, the return EAX and the
     bindings/boundaries in between.
2. The Python composition (``composicao_encadeada_ia``) runs the three phases on
   ONE map built from the scenario's MissionLoad final state.
3. At the end of each phase it is compared with Missions' capture: all block
   hashes, both RNGs, the ordered bindings and boundary events, and the
   registers where modeled. The first stop or divergence is reported with its
   owner and original address. Every crossing lists the bytes it changed, so
   that logic state can be told from display state.
"""
import argparse
import hashlib
import json
import pickle
import struct
import subprocess
import sys
import time

from ambiente_ia_runtime import ROOT
from bancada_quadro1_ia import MISSOES, executar_caminho_pausas
from composicao_encadeada_ia import (DONOS, GRAFICOS_EXIBICAO, NUCLEO, PONTOS, ContextoEncadeado, Divergencia,
                                     Registro, Travessias, fase_cauda_carga, fase_entre_quadros_exibicao, fase_quadro)
from composicao_quadro1_ia import fase_entre_quadros, mundo
from inventario_ia_runtime import OriginalImage
from reinicio_ia import DependenciaIA

VINCULO = ('name', 'arguments', 'caller_return', 'results', 'memory_writes')
FRONTEIRA = ('phase', 'routine', 'caller_return', 'caller', 'top_callee', 'registers', 'declared_eax',
             'stack_cleanup', 'guards', 'stack_words')
DGROUP = 0x494000


def hashes_blocos(blocos):
    return {n: hashlib.sha256(d).hexdigest() for n, (_, d) in blocos.items() if n != 'native_stack'}


def blocos_mapa(mapa):
    """The map's blocks rebuilt in one pass over its sorted segments (``serializar`` is quadratic on 25k blocks)."""
    mapa.empurrar()
    partes = {}
    for s in mapa.segmentos:
        partes.setdefault(s.bloco, []).append(s)
    saida = {}
    for nome, (inicio, fim) in mapa.blocos.items():
        segs = sorted(partes.get(nome, ()), key=lambda s: s.base)
        dados = b''.join(s.bytes() for s in segs)
        if not segs or segs[0].base != inicio or len(dados) != fim - inicio:
            raise ValueError(f'Block {nome} is not covered by its segments')
        saida[nome] = (inicio, dados)
    return saida


def hashes_mapa(mapa):
    return hashes_blocos(blocos_mapa(mapa))


def eventos(b, inicio):
    vinculos = [dict(name=e['name'], arguments=[hex(a & 0xffffffff) for a in e['arguments']],
                     caller_return=e['caller_return'], results={k: hex(v) for k, v in e.get('results', {}).items()},
                     memory_writes=e['memory_writes']) for e in b.vinculos_declarados.eventos[inicio[0]:]]
    return vinculos, [dict(e) for e in b.eventos_fronteira[inicio[1]:]]


def comparar_eventos(python, original, campos):
    saida = dict(python=len(python), original=len(original), equal=len(python) == len(original), not_modeled=[])
    for i, (p, o) in enumerate(zip(python, original)):
        for campo in campos:
            pv, ov = p.get(campo), o.get(campo)
            if campo == 'stack_words' and (pv is None or None in pv):
                pv = pv or [None] * 4
                saida['not_modeled'].append(dict(index=i, routine=o.get('routine'),
                                                 words=[k for k, w in enumerate(pv) if w is None]))
                pv = [o[campo][k] if w is None else w for k, w in enumerate(pv)]
            if pv != ov:
                saida['equal'] = False
                saida.setdefault('first_difference', dict(index=i, field=campo, python=pv, original=ov))
    return saida


def bytes_alterados(antes, depois):
    """DGROUP byte changes listed (logic/display classification), other blocks summarized."""
    saida = {}
    for nome, (base, dados) in depois.items():
        velho = antes.get(nome)
        if velho is None or velho[1] == dados:
            continue
        dif = [i for i in range(len(dados)) if dados[i] != velho[1][i]]
        if nome == 'dgroup':
            saida[nome] = [[hex(base + i), velho[1][i], dados[i]] for i in dif]
        else:
            saida[nome] = dict(base=hex(base), bytes=len(dif), first=hex(base + dif[0]), last=hex(base + dif[-1]))
    return saida


def coletar_original(cenario):
    simbolos = OriginalImage()
    nomes = {n: a for a, ns in simbolos.names.items() for n in ns}
    cruzadas = set(GRAFICOS_EXIBICAO if cenario == 'exibicao' else ('RestoreAll',)) | set(NUCLEO)
    enderecos = {nomes[n]: f'{n}:entry' for n in set(PONTOS) | cruzadas}
    pontos, retornos, abertas, contagem = {}, {}, [], {}

    def observador(rotulo, fase, regs, b):
        nome, onde = rotulo.split(':')
        if onde == 'entry':
            retorno = struct.unpack('<I', bytes(b.cpu.mem_read(regs['ESP'], 4)))[0]
            k = (fase, nome, retorno)
            n = contagem.get(k, 0)
            contagem[k] = n + 1
            imagem = b.imagem()
            if nome in PONTOS or nome in cruzadas:
                pontos[k + (n,)] = hashes_blocos(imagem)
            if nome in cruzadas:
                abertas.append((k + (n,), retorno, imagem, (len(b.vinculos_declarados.eventos), len(b.eventos_fronteira))))
                b.pausa_enderecos.pausar_em(retorno, f'{nome}:return')
            return
        if not abertas or abertas[-1][0][1] != nome or abertas[-1][1] != regs['EIP']:
            return                      # a pause address that is not this open call's return
        chave, _, antes, inicio = abertas.pop()
        depois = b.imagem()
        vinculos, fronteiras = eventos(b, inicio)
        retornos[chave] = dict(
            eax=regs['EAX'], bindings=vinculos, boundaries=fronteiras,
            changed={n: v for n, v in depois.items() if n in antes and antes[n][1] != v[1]},
            allocated={n: v for n, v in depois.items() if n not in antes},
            released=[n for n in antes if n not in depois], changed_bytes=bytes_alterados(antes, depois))

    b, cap, reproducao = executar_caminho_pausas(enderecos, observador, cenario=cenario)
    return pontos, retornos, reproducao, [a[0] for a in abertas]


def estados_cenario(cenario):
    """Scenario MissionLoad final blocks (S0) and the per-phase original states."""
    import base64
    import zlib
    import cenarios_oraculo
    from mapa_memoria_m1 import carregar_blocos, carregar_json, expandir_captura
    m1 = expandir_captura(carregar_json(cenarios_oraculo.caminho(cenario, 'captura_m1')),
                          carregar_json(cenarios_oraculo.caminho(cenario, 'entrada'))
                          if cenario != 'v1' else None)
    quadro = carregar_json(cenarios_oraculo.caminho(cenario, 'captura_quadro'))
    estado = carregar_blocos(m1['oracle']['final_state']['blocks'])
    if quadro['state_s0']['summary']['sha256'] != m1['oracle']['final_state']['summary']['sha256']:
        raise ValueError('Frame capture S0 is not the scenario MissionLoad final state')
    estados = {'s0': dict(estado)}
    for fase in quadro['phases']:
        estado = dict(estado)
        for nome, bloco in fase['state_after']['blocks_changed_since_previous'].items():
            dados = zlib.decompress(base64.b64decode(bloco['zlib_base64']))
            estado[nome] = (int(bloco['base'], 16), dados)
        estado = {n: v for n, v in estado.items() if n in fase['state_after']['block_hashes']}
        estados[fase['phase']] = estado
    return estados, quadro


def comparar_fase(mapa, registro, fase_cap, extra=None):
    estado = hashes_mapa(mapa)
    esperado = {n: h['sha256'] for n, h in fase_cap['state_after']['block_hashes'].items()}
    rng = {'0x497164': hex(struct.unpack('<I', mapa.ler(0x497164, 4))[0]),
           '0x498db4': hex(struct.unpack('<I', mapa.ler(0x498db4, 4))[0])}
    r = dict(state_equal=estado == esperado,
             differing_blocks=sorted(n for n in set(esperado) | set(estado) if estado.get(n) != esperado.get(n)),
             rng_equal=rng == fase_cap['exit']['rng'], rng=rng,
             bindings=comparar_eventos(registro.vinculos, fase_cap['bindings'], VINCULO),
             boundaries=comparar_eventos(registro.fronteiras, fase_cap['boundaries'], FRONTEIRA))
    r.update(extra or {})
    r['equal'] = r['state_equal'] and r['rng_equal'] and r['bindings']['equal'] and r['boundaries']['equal'] and \
        all((extra or {}).get('registers_equal', {}).values())
    return r


def primeira_diferenca_bytes(mapa, estados, fase, limite=12):
    saida = {}
    python = blocos_mapa(mapa)
    for n, (base, d) in estados[fase].items():
        p = python.get(n)
        if p is None:
            saida[n] = 'missing in Python'
            continue
        if p[1] == d:
            continue
        dif = [i for i in range(len(d)) if p[1][i] != d[i]]
        saida[n] = [[hex(base + i), d[i], p[1][i]] for i in dif[:limite]] + ([f'... {len(dif)} bytes'] if len(dif) > limite else [])
    for n in python:
        if n not in estados[fase]:
            saida[n] = 'extra in Python'
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--cenario', default='exibicao', choices=('v1', 'exibicao'))
    ap.add_argument('--dados-originais', help='local pickle cache of the collected original data (.local only)')
    a = ap.parse_args()
    saida = ROOT / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing validation {saida}')
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'pesquisas-paralelas/ia-runtime'],
                          capture_output=True, text=True).stdout
    t0 = time.monotonic()
    cache = ROOT / a.dados_originais if a.dados_originais else None
    if cache is not None and cache.exists():
        pontos, retornos, reproducao, abertas = pickle.loads(cache.read_bytes())
        reproducao = dict(reproducao, note='loaded from a local cache of an earlier native collection')
    else:
        pontos, retornos, reproducao, abertas = coletar_original(a.cenario)
        if cache is not None:
            cache.write_bytes(pickle.dumps((pontos, retornos, reproducao, abertas)))
    estados, cap = estados_cenario(a.cenario)
    fases = {p['phase']: p for p in cap['phases']}
    ctx = ContextoEncadeado(OriginalImage(), a.cenario)
    travessias = Travessias(pontos, retornos, hashes_mapa)
    relatorio = dict(schema='rising-lands/ai-runtime-m2-frame1-chained-composition/2', scenario=a.cenario,
                     source_revision=revisao, source_dirty_paths=sujo.splitlines(),
                     frame_capture=dict(path=str(MISSOES.relative_to(ROOT)), source_revision=cap['source_revision']),
                     path_reproduction=reproducao, unclosed_original_crossings=abertas,
                     original_checkpoints=len(pontos), original_crossings=len(retornos), phases={})
    mapa, prov = mundo(estados['s0'])
    resultado = 'complete'
    for fase in ('load_tail', 'between_frames', 'frame1'):
        registro = Registro(fase)
        e = fases[fase]
        regs = {k: int(v, 16) for k, v in e['entry']['registers'].items()}
        extra = {}
        try:
            if fase == 'load_tail':
                fase_cauda_carga(mapa, prov, ctx, registro, travessias, regs)
            elif fase == 'between_frames' and a.cenario == 'v1':
                quadro = e['declared_caller_frame']
                regs['ESP'] = int(quadro['esp'], 16)
                regs.update({k: int(v, 16) for k, v in quadro['registers'].items()})
                palavras = {w['address']: int(w['value'], 16) for w in quadro['words']}
                esp = regs['ESP']
                entradas = dict(salvo_edx=palavras[hex(esp + 8)], salvo_ecx=palavras[hex(esp + 0xc)],
                                salvo_ebx=palavras[hex(esp + 0x10)], point=(0, 0), msg=(0, 0, 0, 0), peek_message=0,
                                cursor=tuple(cap['named_inputs']['frame']['cursor']))
                saida_regs, _ = fase_entre_quadros(mapa, entradas, registro, regs)
                extra = dict(registers_equal={k: hex(saida_regs[k]) == e['exit']['registers'][k]
                                              for k in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP')})
            elif fase == 'between_frames':
                # The real ProgIteration frame: saved EDX/ECX/EBX are the values the startup loop pushed
                # (all 0, as the boundary registers after the pops show); the MSG buffer holds the bench
                # loop frame's return sentinel 0x3000000 written by BancadaX86.executar, then zeros.
                entradas = dict(salvo_edx=0, salvo_ecx=0, salvo_ebx=0, msg=(0x3000000, 0, 0, 0), peek_message=0,
                                cursor=tuple(cap['named_inputs']['frame']['cursor']))
                saida_regs = fase_entre_quadros_exibicao(mapa, prov, ctx, registro, travessias, regs, entradas)
                extra = dict(registers_equal={k: hex(saida_regs[k]) == e['exit']['registers'][k]
                                              for k in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP')},
                             declared_inputs=dict(entradas, msg=[hex(w) for w in entradas['msg']]))
            else:
                fase_quadro(mapa, prov, ctx, registro, travessias, regs)
            r = comparar_fase(mapa, registro, e, extra)
            r['result'] = 'returned'
            if not r['state_equal']:
                r['first_differing_bytes'] = primeira_diferenca_bytes(mapa, estados, fase)
        except Divergencia as erro:
            r = dict(result='diverged', at=dict(routine=erro.rotina, key=[str(x) for x in erro.chave]),
                     differing_blocks=erro.blocos[:40], equal=False)
            resultado = 'diverged'
        except DependenciaIA as erro:
            r = dict(result='stopped', stop=dict(routine=erro.rotina, site=hex(erro.sitio)), equal=False)
            resultado = 'stopped'
        except Exception as erro:          # another owner's named dependency or guard: recorded, phase stops
            import traceback
            r = dict(result='stopped', traceback=traceback.format_exc()[-3000:], equal=False,
                     stop=dict(type=type(erro).__name__, message=str(erro)[:500], routine=getattr(erro, 'rotina', None),
                               site=hex(getattr(erro, 'endereco', getattr(erro, 'chamada', 0)) or 0)))
            resultado = 'stopped'
        r['checkpoints'] = [v for v in travessias.verificados if v['phase'] == fase]
        r['crossings'] = [v for v in travessias.feitas if v['phase'] == fase]
        r['core_provider_stops'] = [v for v in travessias.paradas_nucleo if v['phase'] == fase]
        relatorio['phases'][fase] = r
        print(fase, r['result'], r.get('equal'), r.get('stop') or r.get('at') or '', flush=True)
        if r['result'] != 'returned':
            break
    relatorio['summary'] = dict(result=resultado, phases={
        f: dict(result=v['result'], equal=v.get('equal'), stop=v.get('stop'), at=v.get('at'),
                crossings=[(c['routine'], c['owner'], c['reason']) for c in v['crossings']],
                core_provider_stops=[(c['routine'], c['core_address']) for c in v['core_provider_stops']])
        for f, v in relatorio['phases'].items()})
    relatorio['seconds'] = round(time.monotonic() - t0, 3)
    ok = reproducao['passed'] and cache is None
    if not ok:
        saida = ROOT / '.local' / ('m2-chained-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), summary=relatorio['summary'], seconds=relatorio['seconds']), indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
