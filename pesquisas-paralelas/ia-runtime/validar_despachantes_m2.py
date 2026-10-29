"""Compare the Python dispatcher loops and frame AI step with the original at the M1 post-load input.

    python3 -B pesquisas-paralelas/ia-runtime/validar_despachantes_m2.py \
        --saida pesquisas-paralelas/ia-runtime/validacao/m2-despachantes-native.json

The intact startup and MissionLoad are replayed exactly as in
``capturar_quadro_m2`` and must reach the frozen accepted M1 final state. For each
case the bench memory is restored to that state, and then the Python
reconstruction runs over the bench's own memory through ``MemoriaBancada``,
which applies the declared-region policy. Every provider the Python code calls
(EnginNextEtape, BatimentNextEtape, PlayerGetType, AvanceMonstre, iaSolver, …)
executes the original routine natively on the same memory. The final image is
compared byte for byte with the committed native capture of the same routine
(``evidencias/captura-quadro-m2-pos-carga.json``), and the provider call order is
compared with the routine's direct callees in that capture's entry trace.
A failure is preserved under ``.local/`` and exits nonzero.
"""
import argparse
import hashlib
import json
import struct
import subprocess
import sys
import time

from ambiente_ia_runtime import OWNED, ROOT
import capturar_quadro_m2 as captura
from capturar_quadro_m2 import (BancadaCargaMissaoOriginal, OraculoInterrompido, ParadaVinculoDeclarado,
                                RETORNO_MISSION_LOAD, changed, entradas, restore)
from inventario_quadro_m2 import M1_FINAL_STATE_SHA256
from laco_despachantes import (PASSO, REGIOES_DESPACHO, UNIDADES, calcular_proxima_etapa_estruturas,
                               calcular_proxima_etapa_unidades, testar_utilidade)
from memoria_ia_runtime import AcessoNaoDeclarado, MemoriaDeclarada
from quadro_calcul_game import Quadro
from reinicio_ia import DependenciaIA

CAPTURE = OWNED / 'evidencias/captura-quadro-m2-pos-carga.json'
# Provider name -> register for each keyword argument the Python code passes.
REGISTRADORES = {'unidade': 'EAX', 'estrutura': 'EAX', 'jogador': 'EAX', 'contexto': 'EAX', 'missao': 'EDX'}
# Reproduced inline in Python (iabTestEngin 0x4897a4 is a ret reached by IATestUtilite's tail jump).
INLINE = ('iabTestEngin',)
SEGUNDO = {'CaseEstDecouverte': ('caso', 'jogador'), 'BatimentEstDecouvert': ('estrutura', 'jogador'),
           'BatimentDecouvre': ('estrutura', 'jogador'), 'BatimentContourEstIllumine': ('estrutura', 'jogador'),
           'BatimentIllumine': ('estrutura', 'jogador', 'ebx')}


class MemoriaBancada(MemoriaDeclarada):
    """MemoriaDeclarada over the bench CPU memory: same region policy, no copy."""

    def __init__(self, cpu, regioes):
        super().__init__([], regioes)
        self.cpu = cpu

    def _acesso(self, largura, endereco, valor):
        endereco &= 0xffffffff
        if not any(a <= endereco and endereco + largura <= b for a, b, _ in self.regioes):
            raise AcessoNaoDeclarado(endereco, largura, 'Access outside the declared regions')
        formato = {1: '<B', 2: '<H', 4: '<I'}[largura]
        if valor is None:
            return struct.unpack(formato, bytes(self.cpu.mem_read(endereco, largura)))[0]
        valor &= (1 << (8 * largura)) - 1
        self.cpu.mem_write(endereco, struct.pack(formato, valor))
        return valor


class ProvedoresNativos(dict):
    """Each provider runs the original routine natively and records its call."""

    def __init__(self, bench, nomes):
        super().__init__()
        self.bench, self.chamadas = bench, []
        for nome in nomes:
            self[nome] = self._provedor(nome)

    def _provedor(self, nome):
        def chamar(sitio, **argumentos):
            if nome in SEGUNDO:
                registros = dict(zip(('EAX', 'EDX', 'EBX'), (argumentos[k] for k in SEGUNDO[nome])))
            else:
                registros = {REGISTRADORES[k]: v for k, v in argumentos.items()}
            self.chamadas.append(f'{nome}@0x{sitio:x}')
            return self.bench.chamar(f'python-provider-{nome}', nome, registros)['EAX']
        return chamar


def direct_callees(trace, routines):
    """Callees whose return address lies in one of ``routines`` (the routine's own call sites)."""
    result = []
    for line in trace:
        callee, caller = line.split(' ')[0].split('@')
        if caller.split('+')[0] in routines and callee not in routines and callee not in INLINE:
            result.append(callee)
    return result


def casos():
    unidade = ('EnginNextEtape', 'PlayerGetType')
    estrutura = ('ResetTableauHangar', 'DemonteBatiment', 'BatimentNextEtape', 'BatimentGetCase',
                 'CaseEstDecouverte', 'BatimentEstDecouvert', 'BatimentDecouvre', 'BatimentContourEstIllumine',
                 'BatimentIllumine', 'PlayerGetType')
    resultado = [('calcul_engin_next_etape', unidade, calcular_proxima_etapa_unidades,
                  ('CalculEnginNextEtape', 'IATestUtilite', 'iagMessTestSendMessageEngin')),
                 ('calcul_batiment_next_etape', estrutura, calcular_proxima_etapa_estruturas,
                  ('CalculBatimentNextEtape', 'IATestUtilite', 'iagMessTestSendMessageEngin'))]
    for u in captura.LIVE_UNITS:
        resultado.append((f'ia_test_utilite_unit{u}', ('PlayerGetType',),
                          lambda m, p, u=u: testar_utilidade(m, p, 1, u), ('IATestUtilite', 'iagMessTestSendMessageEngin')))
    for s in captura.LIVE_STRUCTURES:
        resultado.append((f'ia_test_utilite_structure{s}', ('PlayerGetType',),
                          lambda m, p, s=s: testar_utilidade(m, p, 3, s), ('IATestUtilite',)))
    ia = ('AvanceMonstre', 'iaSolver', 'iagUnitDeleteAllGroups', 'iagUnitNoyau', 'iagVilleNoyau', 'iagRessNoyau',
          'iagWarNoyau')
    for jogador in (1, 2, 3, 4):
        resultado.append((f'calcul_next_reflect_p{jogador}', ia,
                          lambda m, p, j=jogador: Quadro(m, p).calcul_next_reflect(j, captura.MISSION),
                          ('CalculNextReflect', 'iaCalculPlayer')))
    return resultado


def regioes(bench):
    pool = struct.unpack('<I', bytes(bench.cpu.mem_read(0x4e19a0, 4)))[0]
    return REGIOES_DESPACHO + ((pool, pool + UNIDADES * PASSO, 'unit pool'),
                               (0x4dfaa8, 0x4dfab8, 'structure counters'), (0x4e1928, 0x4e1930, 'unit counters'),
                               (0x51a98c, 0x51a9dc, 'AI player contexts'))


def run(saida):
    capture = json.loads(CAPTURE.read_text())
    by_label = {c['label']: c for c in capture['captures']}
    revision = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'pesquisas-paralelas/ia-runtime'],
                           capture_output=True, text=True).stdout
    report = dict(schema='rising-lands/ai-runtime-m2-dispatcher-validation/1', label=captura.LABEL,
                  source_revision=revision, source_dirty_paths=dirty.splitlines(),
                  capture=str(CAPTURE.relative_to(ROOT)), capture_sha256=hashlib.sha256(CAPTURE.read_bytes()).hexdigest(),
                  method='Python loop over bench memory; providers execute the original natively; image and call '
                         'order compared with the whole-routine native capture', cases=[])
    t0 = time.monotonic()
    bench = BancadaCargaMissaoOriginal(entradas(captura.FILL, captura.CLOCK), segundos=120.0)
    status = 0
    try:
        bench.iniciar_relogio()
        bench.executar_inicio()
        regs = bench.executar_mission_load(60.0)
        post = bench.imagem()
        if regs['EIP'] != RETORNO_MISSION_LOAD or bench.resumo_imagem(post)['sha256'] != M1_FINAL_STATE_SHA256:
            raise RuntimeError('Replayed post-load state differs from the frozen accepted M1 final state')
        bench.fase = 'm2-validation'
        for label, nomes, executar, rotinas in casos():
            restore(bench, post)
            bench.limite_segundos = captura.CAPTURE_SECONDS
            bench.iniciar_relogio()
            memoria = MemoriaBancada(bench.cpu, regioes(bench))
            provedores = ProvedoresNativos(bench, nomes)
            caso = dict(label=label)
            try:
                executar(memoria, provedores)
                caso['result'] = 'returned'
            except (DependenciaIA, AcessoNaoDeclarado, OraculoInterrompido, ParadaVinculoDeclarado,
                    RuntimeError, ZeroDivisionError) as error:
                caso['result'] = 'stopped'
                caso['stop'] = f'{type(error).__name__}: {error}'[:1000]
            after = bench.imagem()
            original = by_label[label]
            esperado = direct_callees(original['trace'], rotinas)
            obtido = [c.split('@')[0] for c in provedores.chamadas]
            caso.update(provider_calls=len(obtido), call_order_equal=obtido == esperado,
                        state_equal=bench.resumo_imagem(after)['sha256'] == original['state_after_sha256'],
                        changes_equal=changed(post, after) == original['changes'])
            if not caso['call_order_equal']:
                caso['calls'] = dict(python=obtido, original=esperado)
            if not caso['changes_equal']:
                caso['changes'] = dict(python=changed(post, after), original=original['changes'])
            ok = caso['result'] == 'returned' and caso['call_order_equal'] and caso['state_equal']
            caso['equal'] = ok
            status |= 0 if ok else 1
            report['cases'].append(caso)
            print(f"{label}: {'EQUAL' if ok else 'DIFFERENT'} calls={len(obtido)} {caso['result']}", flush=True)
    except (OraculoInterrompido, ParadaVinculoDeclarado, RuntimeError) as error:
        report['stop'] = f'{type(error).__name__}: {error}'[:2000]
        status = 2
    report['total_seconds'] = round(time.monotonic() - t0, 3)
    report['summary'] = dict(cases=len(report['cases']), equal=sum(c['equal'] for c in report['cases']))
    if status:
        saida = ROOT / '.local' / ('m2-dispatcher-validation-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as handle:
        json.dump(report, handle, indent=1, sort_keys=True)
        handle.write('\n')
    print(json.dumps(dict(output=str(saida), summary=report['summary'], stop=report.get('stop'),
                          total_seconds=report['total_seconds'])))
    return status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--saida', required=True)
    args = parser.parse_args()
    saida = ROOT / args.saida if not args.saida.startswith('/') else __import__('pathlib').Path(args.saida)
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing validation {saida}')
    return run(saida)


if __name__ == '__main__':
    sys.exit(main())
