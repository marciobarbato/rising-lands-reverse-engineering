"""M2.1 round 3: the chained Python composition of MONDE01 (a)->(b)->(c) against the original.

    python3 -B pesquisas-paralelas/ia-runtime/comparar_quadro1_encadeado_ia.py \
        --saida pesquisas-paralelas/ia-runtime/validacao/m2-quadro1-encadeado-ia.json

1. A native replay of Missions' committed first-frame path (which must
   reproduce every committed phase state, the entry trace and the boundaries)
   pauses, without executing anything extra, at:
   - every checkpoint routine entry, where it records the state hashes;
   - the entries and call-return sites of the declared stops, where it records
     the full return state, the return EAX and the bindings/boundaries in between.
2. The Python composition (``composicao_encadeada_ia``) runs the three phases on
   ONE map built from the accepted M1 post-load state.
3. At the end of each phase it is compared with Missions' capture: all 881 block
   hashes, both RNGs, the ordered bindings and boundary events, and the
   registers where modeled. The first stop or divergence is reported with its
   owner and original address.
"""
import argparse
import hashlib
import json
import struct
import subprocess
import sys
import time

from ambiente_ia_runtime import ROOT
from bancada_quadro1_ia import executar_caminho_pausas
from composicao_encadeada_ia import (PONTOS, TRAVESSIAS, ContextoEncadeado, Divergencia, Registro, fase_cauda_carga,
                                     fase_quadro)
from composicao_quadro1_ia import estados_originais, fase_entre_quadros, mundo
from inventario_ia_runtime import OriginalImage
from reinicio_ia import DependenciaIA

RETORNOS = {'RestoreAll': (0x42d284,), 'SetClipping': (0x42d2ab,), 'InitGameZone': (0x468489, 0x42d2de),
            'NextAnimTerrain': (0x42d446,), 'NextAnimVeget': (0x42d46c,)}
VINCULO = ('name', 'arguments', 'caller_return', 'results', 'memory_writes')
FRONTEIRA = ('phase', 'routine', 'caller_return', 'caller', 'top_callee', 'registers', 'declared_eax',
             'stack_cleanup', 'guards', 'stack_words')


def hashes_blocos(blocos):
    return {n: hashlib.sha256(d).hexdigest() for n, (_, d) in blocos.items() if n != 'native_stack'}


def hashes_mapa(mapa):
    return hashes_blocos(mapa.serializar())


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
                faltam = [k for k, w in enumerate(pv) if w is None]
                saida['not_modeled'].append(dict(index=i, routine=o.get('routine'), words=faltam))
                pv = [o[campo][k] if w is None else w for k, w in enumerate(pv)]
            if pv != ov:
                saida['equal'] = False
                saida.setdefault('first_difference', dict(index=i, field=campo, python=pv, original=ov))
    return saida


def coletar_original():
    enderecos = {}
    simbolos = OriginalImage()
    nomes = {n: a for a, ns in simbolos.names.items() for n in ns}
    for nome in PONTOS + tuple(TRAVESSIAS):
        enderecos[nomes[nome]] = f'{nome}:entry'
    for nome, sitios in RETORNOS.items():
        for s in sitios:
            enderecos[s] = f'{nome}:return'
    pontos, retornos, abertas, contagem = {}, {}, [], {}

    def observador(rotulo, fase, regs, b):
        nome, onde = rotulo.split(':')
        if onde == 'entry':
            n = contagem.get((fase, nome), 0)
            contagem[(fase, nome)] = n + 1
            pontos[(fase, nome, n)] = hashes_blocos(b.imagem())
            if nome in TRAVESSIAS:
                abertas.append((fase, nome, n, (len(b.vinculos_declarados.eventos), len(b.eventos_fronteira))))
            return
        if not abertas or abertas[-1][1] != nome:
            return                      # 0x42d2de is also frame 1's state-0x12 entry: not a return
        fase0, _, n, inicio = abertas.pop()
        vinculos, fronteiras = eventos(b, inicio)
        retornos[(fase0, nome, n)] = dict(blocks=b.imagem(), eax=regs['EAX'], bindings=vinculos, boundaries=fronteiras)

    b, cap, reproducao = executar_caminho_pausas(enderecos, observador)
    return pontos, retornos, reproducao, abertas


def comparar_fase(nome, mapa, registro, fase_cap, extra=None):
    estado = hashes_mapa(mapa)
    esperado = {n: h['sha256'] for n, h in fase_cap['state_after']['block_hashes'].items()}
    rng = {hex(a): hex(mapa.u32(a)) for a in (0x497164, 0x498db4)}
    r = dict(state_equal=estado == esperado,
             differing_blocks=sorted(n for n in esperado if estado.get(n) != esperado[n]),
             rng_equal=rng == fase_cap['exit']['rng'], rng=rng,
             bindings=comparar_eventos(registro.vinculos, fase_cap['bindings'], VINCULO),
             boundaries=comparar_eventos(registro.fronteiras, fase_cap['boundaries'], FRONTEIRA))
    r.update(extra or {})
    r['equal'] = r['state_equal'] and r['rng_equal'] and r['bindings']['equal'] and r['boundaries']['equal'] and \
        all((extra or {}).get('registers_equal', {}).values())
    return r


def primeira_diferenca_bytes(mapa, estados, fase):
    """For a differing phase: the first differing byte addresses per block (diagnostic)."""
    saida = {}
    python = mapa.serializar()
    for n, (base, d) in estados[fase].items():
        p = python.get(n)
        if p is None or p[1] == d:
            continue
        dif = [i for i in range(len(d)) if p[1][i] != d[i]]
        saida[n] = [[hex(base + i), d[i], p[1][i]] for i in dif[:12]] + ([f'... {len(dif)} bytes'] if len(dif) > 12 else [])
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--dados-originais', help='local pickle cache of the collected original data (.local only)')
    a = ap.parse_args()
    saida = ROOT / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing validation {saida}')
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'pesquisas-paralelas/ia-runtime'],
                          capture_output=True, text=True).stdout
    t0 = time.monotonic()
    import pickle
    cache = ROOT / a.dados_originais if a.dados_originais else None
    if cache is not None and cache.exists():
        pontos, retornos, reproducao, abertas = pickle.loads(cache.read_bytes())
        reproducao = dict(reproducao, note='loaded from a local cache of an earlier native collection')
    else:
        pontos, retornos, reproducao, abertas = coletar_original()
        if cache is not None:
            cache.write_bytes(pickle.dumps((pontos, retornos, reproducao, abertas)))
    estados, cap = estados_originais()
    fases = {p['phase']: p for p in cap['phases']}
    ctx = ContextoEncadeado(OriginalImage())
    from composicao_encadeada_ia import Travessias
    travessias = Travessias(pontos, retornos, pontos, hashes_mapa)
    relatorio = dict(schema='rising-lands/ai-runtime-m2-frame1-chained-composition/1', source_revision=revisao,
                     source_dirty_paths=sujo.splitlines(), frame_capture=cap['source_revision'],
                     path_reproduction=reproducao, unclosed_original_crossings=[x[:3] for x in abertas],
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
            elif fase == 'between_frames':
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
                                              for k in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP')},
                             registers_not_modeled=['EFLAGS', 'EIP'],
                             declared_inputs='caller frame, cursor and PeekMessageA answer of the capture')
            else:
                fase_quadro(mapa, prov, ctx, registro, travessias, regs)
            r = comparar_fase(fase, mapa, registro, e, extra)
            r['result'] = 'returned'
            if not r['state_equal']:
                r['first_differing_bytes'] = primeira_diferenca_bytes(mapa, estados, fase)
        except Divergencia as erro:
            r = dict(result='diverged', at=dict(routine=erro.rotina, occurrence=erro.ocorrencia),
                     differing_blocks=erro.blocos, equal=False)
            resultado = 'diverged'
        except DependenciaIA as erro:
            r = dict(result='stopped', stop=dict(routine=erro.rotina, site=hex(erro.sitio)), equal=False)
            resultado = 'stopped'
        except Exception as erro:          # another owner's named dependency or guard: recorded, phase stops
            import traceback
            r = dict(result='stopped', traceback=traceback.format_exc()[-3000:],
                     stop=dict(type=type(erro).__name__, message=str(erro)[:500],
                                                 routine=getattr(erro, 'rotina', None),
                                                 site=hex(getattr(erro, 'endereco', getattr(erro, 'chamada', 0)) or 0)),
                     equal=False)
            resultado = 'stopped'
        r['checkpoints'] = [v for v in travessias.verificados if v['phase'] == fase]
        r['crossings'] = [v for v in travessias.feitas if v['phase'] == fase]
        relatorio['phases'][fase] = r
        print(fase, r['result'], r.get('equal'), r.get('stop') or r.get('at') or '', flush=True)
        if r['result'] != 'returned':
            break
    relatorio['summary'] = dict(result=resultado, phases={f: dict(result=v['result'], equal=v.get('equal'),
                                                                  stop=v.get('stop'), at=v.get('at'),
                                                                  crossings=[(c['routine'], c['owner'])
                                                                             for c in v['crossings']])
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
