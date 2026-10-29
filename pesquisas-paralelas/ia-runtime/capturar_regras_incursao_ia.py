"""Original-only capture of the iaSolver rule calls of MONDE01's first raid (M2.3), from the forced counter 9000.

Input (as Combat's raid course a1f589a): Missions' v1 bench, used read-only, reruns the committed path (startup,
MissionLoad, load_tail, between_frames). At frame 1's CalculGame entry, u32 0x508f7c is written to 9000; whole
frames then run natively, with the real ProgIteration tail and window loop between them, so frame k runs with
counter 8999 + k. The no-input answers and boundaries are Missions' v1 declarations. No translation is imported.

A rule call is a call that returns to iaSolver's indirect call sites 0x47d4ec or 0x47d73c. At the selected
counters, each rule call records:
- the rule name, the argument block EAX points to (seven argument words, the player at +0x1c, the task index at
  +0x20) and the exit EAX;
- the read-before-write footprint of the whole call (DGROUP, CRT thread page, arena; the stack excluded);
- every byte it writes, same-value writes included (value before the first write, value at the return), and
  the net changed bytes;
- each top-level call it makes to another owner's routine (anything but rule, ia* and iag* routines): entry
  registers and stack words, exit registers, every byte written and the net changed bytes.

    python3 -B pesquisas-paralelas/ia-runtime/capturar_regras_incursao_ia.py --quadros 3 --registrar 9000 \
        --saida pesquisas-paralelas/ia-runtime/evidencias/captura-regras-incursao-9000-ia.json

The run through counter 11101 (--quadros 2103 --registrar 9000,9500,9700,11100,11101) is long native work for
the Mac mini.
"""
import argparse
import hashlib
import json
import re
import struct
import sys
import time

from ambiente_ia_runtime import ROOT

MISSOES = ROOT / 'pesquisas-paralelas/missoes'
if str(MISSOES) not in sys.path:
    sys.path.insert(0, str(MISSOES))
import ambiente_missoes  # noqa: E402,F401
import capturar_quadro_missao_original as cq  # noqa: E402
import oraculo_quadro_missao as oq  # noqa: E402
from oraculo_quadro_missao import (BancadaQuadroMissaoOriginal, CALCUL_GAME, RETORNO_CALCUL_GAME,  # noqa: E402
                                   SAIDA_LACO, nomes_fases)
import unicorn  # noqa: E402
from unicorn import x86_const as x86  # noqa: E402

HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
CAPTURA = MISSOES / 'evidencias/captura-quadro1-monde01-original.json'
CONTADOR, CONTADOR_FORCADO = 0x508f7c, 9000
RETORNOS_REGRA = (0x47d4ec, 0x47d73c)
PROPRIAS = re.compile(r'^(B_|I_|V_|iag|ia[A-Z])')
PILHA = (0x2000000, 0x2010000)


class BancadaRegras(BancadaQuadroMissaoOriginal):
    def executar_entre_quadros_k(self, segundos, k):
        """between_frames(k >= 2): the real ProgIteration tail and window loop to the next CalculGame entry
        (the same steps as Combat's ``sondar_vida_incursao.BancadaVida``)."""
        if self.cpu.reg_read(x86.UC_X86_REG_EIP) != RETORNO_CALCUL_GAME:
            raise RuntimeError('between_frames starts at ProgIteration 0x475063')
        entre, _ = nomes_fases(k)
        self._fase(entre)
        self.limite_segundos = segundos
        self.iniciar_relogio()
        self._retomando = {RETORNO_CALCUL_GAME}
        self._passar_uma_vez.add(RETORNO_CALCUL_GAME)
        regs = self._correr(entre, RETORNO_CALCUL_GAME, {}, (CALCUL_GAME, SAIDA_LACO), retomar=True)
        if regs['EIP'] != CALCUL_GAME:
            self._interromper('window_loop_exit', eip=hex(regs['EIP']))
        return regs


def executar(quadros, registrar):
    cap = json.loads(CAPTURA.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaRegras(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    simbolos = {b.sym[n]: n for n in b.sym}
    regioes = ((oq.DGROUP[0], oq.DGROUP[1]), (oq.DADOS_THREAD_CRT, oq.DADOS_THREAD_CRT + 0x1000),
               (b.arena.base, b.arena.proximo))
    estado = dict(ativo=False, regra=None, pilha=[], chamadas=[], ganchos=[], contador=None)
    registros = []

    def regs(cpu):
        return {r: cpu.reg_read(getattr(x86, 'UC_X86_REG_' + r)) for r in ('EAX', 'EDX', 'EBX', 'ECX', 'ESP')}

    def ler_mem(cpu, _a, endereco, tamanho, _v, _):
        r = estado['regra']
        for k in range(tamanho):
            a = endereco + k
            if a not in r['escritos'] and a not in r['lidos']:
                r['lidos'][a] = cpu.mem_read(a, 1)[0]

    def escrever_mem(cpu, _a, endereco, tamanho, _v, _):
        r = estado['regra']
        aberta = estado['pilha'][-1] if estado['pilha'] else None
        for k in range(tamanho):
            a = endereco + k
            if a not in r['antes']:
                r['antes'][a] = cpu.mem_read(a, 1)[0]
            r['escritos'].add(a)
            if aberta is not None:
                aberta['antes'].setdefault(a, cpu.mem_read(a, 1)[0])

    def fechar_regra(cpu, r_):
        r = estado['regra']
        for g in estado['ganchos']:
            cpu.hook_del(g)
        estado['ganchos'] = []
        r['registro'].update(
            exit={k: hex(v) for k, v in r_.items()},
            read_before_write=[[hex(a), v] for a, v in sorted(r['lidos'].items())],
            changed_bytes=[[hex(a), v, cpu.mem_read(a, 1)[0]] for a, v in sorted(r['antes'].items())
                           if v != cpu.mem_read(a, 1)[0] and not PILHA[0] <= a < PILHA[1]],
            written_bytes=[[hex(a), v, cpu.mem_read(a, 1)[0]] for a, v in sorted(r['antes'].items())
                           if not PILHA[0] <= a < PILHA[1]])
        registros.append(r['registro'])
        estado['regra'] = None
        estado['pilha'] = []

    def bloco(cpu, endereco, _tamanho, _):
        if not estado['ativo']:
            return
        r_ = regs(cpu)
        r = estado['regra']
        if r is not None:
            pilha = estado['pilha']
            while pilha and pilha[-1]['ret'] == endereco and r_['ESP'] > pilha[-1]['esp']:
                aberta = pilha.pop()
                aberta['registro'].update(exit={k: hex(v) for k, v in r_.items()}, changed_bytes=[
                    [hex(a), v, cpu.mem_read(a, 1)[0]] for a, v in sorted(aberta['antes'].items())
                    if v != cpu.mem_read(a, 1)[0] and not PILHA[0] <= a < PILHA[1]], written_bytes=[
                    [hex(a), v, cpu.mem_read(a, 1)[0]] for a, v in sorted(aberta['antes'].items())
                    if not PILHA[0] <= a < PILHA[1]])
            if endereco == r['ret'] and r_['ESP'] > r['esp']:
                fechar_regra(cpu, r_)
                return
            nome = simbolos.get(endereco)
            if nome is None or pilha or PROPRIAS.match(nome):
                return
            palavras = struct.unpack('<7I', bytes(cpu.mem_read(r_['ESP'], 28)))
            registro = dict(routine=nome, caller=b.nome(palavras[0]), caller_return=hex(palavras[0]),
                            entry={k: hex(v) for k, v in r_.items()}, stack_words=[hex(p) for p in palavras[1:]])
            r['registro']['outside_calls'].append(registro)
            pilha.append(dict(ret=palavras[0], esp=r_['ESP'], registro=registro, antes={}))
            return
        nome = simbolos.get(endereco)
        if nome is None:
            return
        retorno = struct.unpack('<I', bytes(cpu.mem_read(r_['ESP'], 4)))[0]
        if retorno not in RETORNOS_REGRA:
            return
        bloco_args = struct.unpack('<9I', bytes(cpu.mem_read(r_['EAX'], 36)))
        registro = dict(counter=estado['contador'], rule=nome, address=hex(endereco), caller_return=hex(retorno),
                        arguments=[hex(v) for v in bloco_args[:7]], player=bloco_args[7], task=bloco_args[8],
                        entry={k: hex(v) for k, v in r_.items()}, outside_calls=[])
        estado['regra'] = dict(registro=registro, ret=retorno, esp=r_['ESP'], lidos={}, escritos=set(), antes={})
        for inicio, fim in regioes:
            estado['ganchos'].append(cpu.hook_add(unicorn.UC_HOOK_MEM_READ, ler_mem, None, begin=inicio, end=fim - 1))
            estado['ganchos'].append(cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, escrever_mem, None, begin=inicio,
                                                  end=fim - 1))

    b.cpu.hook_add(unicorn.UC_HOOK_BLOCK, bloco, begin=0x401000, end=0x493bff)
    b.cpu.ctl_flush_tb()
    b.executar_cauda_carga(600)
    b.executar_entre_quadros(120)
    b.cpu.mem_write(CONTADOR, struct.pack('<I', CONTADOR_FORCADO))
    for k in range(1, quadros + 1):
        if k > 1:
            b.executar_entre_quadros_k(120, k)
        contador = struct.unpack('<I', bytes(b.cpu.mem_read(CONTADOR, 4)))[0]
        estado.update(ativo=contador in registrar, contador=contador)
        b.executar_quadro(300, k)
        if estado['regra'] is not None:
            raise RuntimeError(f'Rule call {estado["regra"]["registro"]["rule"]} still open at the frame end')
        estado['ativo'] = False
        print(k, contador, sum(1 for r in registros if r['counter'] == contador), flush=True)
    return registros


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quadros', type=int, required=True, help='frames from the forced counter 9000')
    ap.add_argument('--registrar', required=True, help='comma-separated counters whose rule calls are recorded')
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    saida = ROOT / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    registrar = {int(x) for x in a.registrar.split(',')}
    t0 = time.monotonic()
    registros = executar(a.quadros, registrar)
    relatorio = dict(
        schema='rising-lands/ai-runtime-raid-rule-calls/1', original_sha256=HASH, translation_executed=False,
        label=f'forced input: v1 path, counter written to 9000 at frame 1\'s CalculGame entry, {a.quadros} frames',
        frame_capture=dict(path=str(CAPTURA.relative_to(ROOT)), sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in (
            'pesquisas-paralelas/ia-runtime/capturar_regras_incursao_ia.py',
            'pesquisas-paralelas/missoes/oraculo_quadro_missao.py')},
        frames=a.quadros, recorded_counters=sorted(registrar), rule_calls=registros,
        rules=sorted({r['rule'] for r in registros}), seconds=round(time.monotonic() - t0, 3))
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida.relative_to(ROOT)), rules=relatorio['rules'], calls=len(registros),
                          seconds=relatorio['seconds']), indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
