"""M2.1 comparison: the Python composition of MONDE01 phases (a)/(b)/(c) against the original capture.

    python3 -B pesquisas-paralelas/ia-runtime/comparar_quadro1_ia.py \
        --saida pesquisas-paralelas/ia-runtime/validacao/m2-quadro1-composicao-ia.json

Each phase is composed in Python (``composicao_quadro1_ia``) from the original
state at its entry: S0 for (a), then the captured state after the previous phase.
The run either reaches the phase end, in which case it is compared with the
captured phase state (all 881 blocks), the RNGs, the modeled registers, the
ordered bindings and the boundary events, or it stops at a named dependency.
At a stop, the Python state and the binding/boundary prefix are compared with
the original at the same point. That point comes from a snapshot pause taken
during a native replay of Missions' committed path, which must reproduce every
committed phase state.

The same native replay runs this front's reached routines in isolation at every
frame-0/1 entry (``capturar_isolados_ia_quadro1``). The Python translation then
runs on a copy of the exact entry state and must produce the same changed bytes
and returns.
"""
import argparse
import hashlib
import json
import struct
import subprocess
import sys
import time

from ambiente_ia_runtime import ROOT
from bancada_quadro1_ia import executar_caminho
from composicao_quadro1_ia import (REGIOES_COMPOSICAO, ContextoQuadro, regioes_dinamicas, Registro, estados_originais, fase_cauda_carga,
                                   fase_entre_quadros, fase_quadro, mundo)
from capturar_isolados_ia_quadro1 import EXECUTADAS, INSTANTANEOS
from fundacoes_quadro import avancar_quadro_jogo
from inventario_ia_runtime import OriginalImage
from laco_despachantes import PASSO, UNIDADES, calcular_proxima_etapa_unidades
from memoria_ia_runtime import MemoriaDeclarada
from mercado import Mercado
from quadro_calcul_game import Quadro
from reinicio_ia import DependenciaIA
from rotinas_quadro_ia import avancar_monstros, calcular_caixa_mensagens, processar_entrada, resolver_ia

VINCULO = ('name', 'arguments', 'caller_return', 'results', 'memory_writes')
FRONTEIRA = ('phase', 'routine', 'caller_return', 'caller', 'top_callee', 'registers', 'declared_eax',
             'stack_cleanup', 'guards', 'stack_words')
REGISTRADORES = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP')


def hashes(blocos):
    return {n: hashlib.sha256(d).hexdigest() for n, (_, d) in blocos.items() if n != 'native_stack'}


def diferencas(python, original):
    nomes = sorted(set(python) | set(original))
    return [n for n in nomes if python.get(n) != original.get(n)]


def comparar_eventos(python, original, campos, limite=None):
    original = original if limite is None else original[:limite]
    saida = dict(python=len(python), original=len(original), equal=True, fields_not_modeled=[])
    if len(python) != len(original):
        saida['equal'] = False
    for i, (p, o) in enumerate(zip(python, original)):
        for campo in campos:
            if p.get(campo) is None and campo == 'stack_words':
                saida['fields_not_modeled'].append(dict(index=i, field=campo, original=o.get(campo)))
                continue
            if p.get(campo) != o.get(campo):
                saida['equal'] = False
                saida.setdefault('first_difference', dict(index=i, field=campo, python=p.get(campo), original=o.get(campo)))
    return saida


def eventos_bancada(b, fase_entrada):
    vinculos = [dict(e, arguments=[hex(a & 0xffffffff) for a in e['arguments']],
                     results={k: hex(v) for k, v in e.get('results', {}).items()})
                for e in b.vinculos_declarados.eventos[fase_entrada['bindings']:]]
    return vinculos, b.eventos_fronteira[fase_entrada['boundaries']:]


def memoria_copia(antes):
    segmentos = [(base, bytearray(d)) for n, (base, d) in antes.items() if n != 'native_stack']
    def ler(a, n):
        return next(bytes(d[a - b:a - b + n]) for b, d in segmentos if b <= a and a + n <= b + len(d))
    u32 = lambda a: struct.unpack('<I', ler(a, 4))[0]  # noqa: E731
    pool = u32(0x4e19a0)
    regioes = REGIOES_COMPOSICAO + regioes_dinamicas(u32)
    jogadores = ler(struct.unpack('<I', ler(0x5080a8, 4))[0], 80)
    return MemoriaDeclarada(segmentos, regioes), segmentos, Mercado(jogadores=jogadores), pool


def alterados(antes, segmentos):
    saida = []
    velhos = {base: d for n, (base, d) in antes.items() if n != 'native_stack'}
    for base, d in segmentos:
        v = velhos[base]
        saida += [[hex(base + i), v[i], d[i]] for i in range(len(d)) if d[i] != v[i]]
    return sorted(saida, key=lambda x: int(x[0], 16))


class Diferencial:
    """Run the Python translation at each isolated native call and compare."""

    def __init__(self, contexto):
        self.contexto, self.casos = contexto, []

    def __call__(self, nome, fase, caso, antes, resultado):
        regs = {k: int(v, 16) for k, v in resultado['entry_registers'].items()}
        m, segmentos, mercado, pool = memoria_copia(antes)
        provedores = {'PlayerGetType': lambda sitio, jogador: mercado.tipo_jogador(jogador),
                      'MissionGetNum': lambda sitio: m.u8(0x496fe4)}
        provedores['AvanceMonstre'] = lambda sitio, jogador: avancar_monstros(m, provedores)
        provedores['iaSolver'] = lambda sitio, contexto: resolver_ia(m, self.contexto, contexto)
        registro = dict(routine=nome, phase=fase, entry_registers=resultado['entry_registers'])
        eax = None
        try:
            if nome == 'CalculNextReflect':
                eax = Quadro(m, provedores).calcul_next_reflect(regs['EAX'], regs['EDX'])
                esperado_eax = int(resultado['exit_registers']['EAX'], 16) & 0xff
            elif nome == 'ProcessInputGame':
                eax = processar_entrada(m, regs['EAX'], self.contexto.comandos)
                esperado_eax = int(resultado['exit_registers']['EAX'], 16)
            elif nome == 'MessageBoxCalcul':
                calcular_caixa_mensagens(m)
            elif nome == 'GameNextFrame':
                dg = next(d for b, d in segmentos if b == 0x494000)
                avancar_quadro_jogo(memoryview(dg)[0x496d40 - 0x494000:0x496d44 - 0x494000])
            elif nome == 'CalculEnginNextEtape':
                despachos = []
                provedores['EnginNextEtape'] = lambda sitio, unidade: despachos.append(unidade)  # declared stub
                calcular_proxima_etapa_unidades(m, provedores)
                registro['dispatched'] = despachos
            else:
                raise DependenciaIA(f'{nome}: per-structure providers (ResetTableauHangar, BatimentNextEtape, '
                                    'discover/illuminate) are owned by Economy/Core', 0x4281d0)
            registro['result'] = 'returned'
        except DependenciaIA as erro:
            registro['result'] = 'stopped'
            registro['stop'] = dict(routine=erro.rotina, site=hex(erro.sitio))
        except Exception as erro:       # recorded as a failed case; the summary then fails
            registro['result'] = 'error'
            registro['error'] = f'{type(erro).__name__}: {erro}'
        python = alterados(antes, segmentos)
        original = [[a, v0, v1] for a, v0, v1 in resultado['changed_bytes']]
        if nome == 'CalculEnginNextEtape':
            # Only the bytes the loop itself owns; EnginNextEtape bodies are not reconstructed.
            proprios = lambda a: (0x4e1928 <= a < 0x4e1932 or 0x4e1a38 <= a < 0x4e1a3c + 4 * 0x34 or
                                  (pool <= a < pool + UNIDADES * PASSO and (a - pool) % PASSO in (0x10a, 0x10b)))
            original = [x for x in original if proprios(int(x[0], 16))]
            python = [x for x in python if proprios(int(x[0], 16))]
            registro['scope'] = 'loop-owned bytes (counters, unit +0x10a/+0x10b); EnginNextEtape declared stub'
        registro['changes_equal'] = python == original
        registro['changes'] = dict(python=len(python), original=len(original))
        if eax is not None:
            registro['eax_equal'] = eax == esperado_eax
        if not registro['changes_equal']:
            registro['first_differences'] = dict(python=python[:8], original=original[:8])
        self.casos.append(registro)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    saida = ROOT / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing validation {saida}')
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'pesquisas-paralelas/ia-runtime'],
                          capture_output=True, text=True).stdout
    t0 = time.monotonic()
    estados, cap = estados_originais()
    contexto = ContextoQuadro(OriginalImage())
    fases = {p['phase']: p for p in cap['phases']}
    relatorio = dict(schema='rising-lands/ai-runtime-m2-frame1-composition/1', source_revision=revisao,
                     source_dirty_paths=sujo.splitlines(), frame_capture=cap['source_revision'], phases={})
    python = {}

    # (a) load_tail from S0.
    mapa, prov = mundo(estados['s0'])
    reg = Registro('load_tail')
    try:
        fase_cauda_carga(mapa, prov, contexto, reg)
        python['load_tail'] = dict(result='returned')
    except DependenciaIA as erro:
        python['load_tail'] = dict(result='stopped', stop=dict(routine=erro.rotina, site=hex(erro.sitio)))
    python['load_tail'].update(state=hashes(mapa.serializar()), registro=reg)

    # (b) between_frames from the captured state after (a).
    e = fases['between_frames']
    mapa, prov = mundo(estados['load_tail'])
    reg = Registro('between_frames')
    regs = {k: int(v, 16) for k, v in e['entry']['registers'].items()}
    regs['ESP'] = int(e['declared_caller_frame']['esp'], 16)
    for k, v in e['declared_caller_frame']['registers'].items():
        regs[k] = int(v, 16)
    palavras = {w['address']: int(w['value'], 16) for w in e['declared_caller_frame']['words']}
    esp = regs['ESP']
    entradas = dict(salvo_edx=palavras[hex(esp + 8)], salvo_ecx=palavras[hex(esp + 0xc)],
                    salvo_ebx=palavras[hex(esp + 0x10)], point=(0, 0), msg=(0, 0, 0, 0),
                    peek_message=0, cursor=tuple(cap['named_inputs']['frame']['cursor']))
    saida_regs, _ = fase_entre_quadros(mapa, entradas, reg, regs)
    estado = hashes(mapa.serializar())
    esperado = {n: h['sha256'] for n, h in e['state_after']['block_hashes'].items()}
    rng = {hex(a): hex(mapa.u32(a)) for a in (0x497164, 0x498db4)}
    relatorio['phases']['between_frames'] = dict(
        start='captured state after load_tail; declared caller frame of the capture',
        result='returned', state_equal=estado == esperado, differing_blocks=diferencas(estado, esperado),
        rng_equal=rng == e['exit']['rng'], rng=rng,
        registers_equal={k: hex(saida_regs[k]) == e['exit']['registers'][k] for k in REGISTRADORES},
        registers_not_modeled=['EFLAGS', 'EIP (the composition ends at the CalculGame entry 0x42c868)'],
        bindings=comparar_eventos(reg.vinculos, e['bindings'], VINCULO),
        boundaries=comparar_eventos(reg.fronteiras, e['boundaries'], FRONTEIRA),
        inputs=dict(point_and_msg_stack_bytes='0: BancadaX86.executar zero-fills PILHA before the load-state call, '
                                              'and nothing above that frame is written', **{
                        k: v for k, v in entradas.items() if k not in ('point', 'msg')}))

    # (c) frame1 from the captured state after (b).
    e = fases['frame1']
    mapa, prov = mundo(estados['between_frames'])
    reg = Registro('frame1')
    regs = {k: int(v, 16) for k, v in e['entry']['registers'].items()}
    try:
        fase_quadro(mapa, prov, contexto, dict(set_cursor_pos=1), reg, regs)
        python['frame1'] = dict(result='returned')
    except DependenciaIA as erro:
        python['frame1'] = dict(result='stopped', stop=dict(routine=erro.rotina, site=hex(erro.sitio)))
    python['frame1'].update(state=hashes(mapa.serializar()), registro=reg)

    # Native replay: snapshot comparisons at the stops and isolated differentials.
    alvo_pausa = {('RestoreAll', 'load_tail'): 'load_tail', ('InputGame', 'frame1'): 'frame1'}
    pausas = {}

    def instantaneo(nome, fase, blocos, regs_pausa, retorno, bancada):
        chave = alvo_pausa.get((nome, fase))
        if chave is None or python[chave]['result'] != 'stopped' or python[chave]['stop']['routine'] != nome:
            return
        vinculos, fronteiras = eventos_bancada(bancada, fases[chave]['entry'])
        r = python[chave]['registro']
        pausas[chave] = dict(at=nome, caller_return=hex(retorno), state_equal=python[chave]['state'] == hashes(blocos),
                             differing_blocks=diferencas(python[chave]['state'], hashes(blocos)),
                             bindings_prefix=comparar_eventos(r.vinculos, vinculos, VINCULO),
                             boundaries_prefix=comparar_eventos(r.fronteiras, fronteiras, FRONTEIRA))

    diferencial = Diferencial(contexto)
    b, pausa, _, reproducao = executar_caminho(EXECUTADAS, INSTANTANEOS, diferencial, instantaneo)
    for chave in ('load_tail', 'frame1'):
        p = python[chave]
        relatorio['phases'][chave] = dict(start='S0 (accepted M1 post-load state)' if chave == 'load_tail'
                                          else 'captured state after between_frames',
                                          result=p['result'], stop=p.get('stop'), at_stop=pausas.get(chave))
    relatorio['path_reproduction'] = reproducao
    relatorio['isolated_differential'] = diferencial.casos
    relatorio['summary'] = dict(
        load_tail=relatorio['phases']['load_tail']['stop'],
        between_frames_equal=all((relatorio['phases']['between_frames']['state_equal'],
                                  relatorio['phases']['between_frames']['rng_equal'],
                                  all(relatorio['phases']['between_frames']['registers_equal'].values()),
                                  relatorio['phases']['between_frames']['bindings']['equal'],
                                  relatorio['phases']['between_frames']['boundaries']['equal'])),
        frame1=relatorio['phases']['frame1']['stop'],
        stops_equal_original_prefix={k: bool(v and v['state_equal'] and v['bindings_prefix']['equal']
                                             and v['boundaries_prefix']['equal']) for k, v in pausas.items()},
        isolated=dict(cases=len(diferencial.casos),
                      equal=sum(1 for c in diferencial.casos if c['changes_equal'] and c.get('eax_equal', True)
                                and c['result'] == 'returned'),
                      stopped=[(c['routine'], c['phase'], c['stop']) for c in diferencial.casos if c['result'] == 'stopped']))
    relatorio['seconds'] = round(time.monotonic() - t0, 3)
    ok = reproducao['passed'] and relatorio['summary']['between_frames_equal'] and all(
        relatorio['summary']['stops_equal_original_prefix'].values())
    if not ok:
        saida = ROOT / '.local' / ('m2-frame1-composition-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), summary=relatorio['summary'], seconds=relatorio['seconds']), indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
