"""Original-only capture of MONDE01's first raid call tree for AI/runtime (M2.3), with the forced counter 9000.

Same forced input as Combat's ``capturar_incursao_m2_3`` (commit 1e9f28e). Missions' committed frame path (v1
scenario) is rerun with their read-only ``Isolamento`` bench. Frame 1's AvanceMonstre gets an extra case with
u32 0x508f7c = 9000, and every other byte is the exact frame-1 input. No translation is imported.

Inside that forced case, this records every top-level call that leaves this front's routines (AvanceMonstre,
ConstruitGroupeMonstre, StockeAction, iaGroupNew, iagUnitAddToGroup, iagUnitGetFirstUnitInGroup) into another
owner's routine. For each call it records:
- the caller return;
- EAX/EDX/EBX/ECX and six stack words at entry;
- EAX/EDX/EBX/ECX at the return (matched on the return address and ESP);
- the net bytes written inside the call's extent (address, value before, value after).

It also records every byte the own routines write themselves, outside any outside call: the value before the
first write and the value when AvanceMonstre returns (``own_writes``, stack included).

With these, a translation of this front's routines can be checked call by call at the exact native inputs, and
each outside call is checked against its own native effect. The whole-call read-before-write footprint and the
changed bytes come from Isolamento itself.

    python3 -B pesquisas-paralelas/ia-runtime/capturar_incursao_ia.py
"""
import hashlib
import json
import struct
import sys
import time

from ambiente_ia_runtime import ROOT

MISSOES = ROOT / 'pesquisas-paralelas/missoes'
if str(MISSOES) not in sys.path:
    sys.path.insert(0, str(MISSOES))
import ambiente_missoes  # noqa: E402,F401
import capturar_quadro_missao_original as cq  # noqa: E402
from oraculo_quadro_missao import BancadaQuadroMissaoOriginal, Isolamento  # noqa: E402
import unicorn  # noqa: E402
from unicorn import x86_const as x86  # noqa: E402

HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
CAPTURA = MISSOES / 'evidencias/captura-quadro1-monde01-original.json'
DESTINO = ROOT / 'pesquisas-paralelas/ia-runtime/evidencias/captura-incursao-ia.json'
CONTADOR, CONTADOR_FORCADO = 0x508f7c, 9000
PROPRIAS = ('AvanceMonstre', 'ConstruitGroupeMonstre', 'StockeAction', 'iaGroupNew', 'iagUnitAddToGroup',
            'iagUnitGetFirstUnitInGroup')
CASO = 'forced-counter-9000'


def executar():
    cap = json.loads(CAPTURA.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaQuadroMissaoOriginal(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    simbolos = {b.sym[n]: n for n in b.sym}
    proprias = {b.sym[n] for n in PROPRIAS}
    estado = dict(ativo=False, pilha=[], chamadas=[], escritas=[], proprias={}, proprias_fim=None)

    def regs(cpu):
        return {r: cpu.reg_read(getattr(x86, 'UC_X86_REG_' + r)) for r in ('EAX', 'EDX', 'EBX', 'ECX', 'ESP')}

    def bloco(cpu, endereco, _tamanho, _):
        if b.fase != 'isolated':
            return
        if endereco == b.sym['AvanceMonstre'] and not estado['pilha'] and \
                struct.unpack('<I', bytes(cpu.mem_read(CONTADOR, 4)))[0] == CONTADOR_FORCADO:
            estado['ativo'] = True          # only the forced case runs with the counter at 9000
            estado['gancho'] = cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, escrita)
        if not estado['ativo']:
            return
        r = regs(cpu)
        pilha = estado['pilha']
        # Close the open outside call whose RET landed here (ESP above its entry ESP).
        while pilha and pilha[-1]['ret'] == endereco and r['ESP'] > pilha[-1]['esp']:
            aberta = pilha.pop()
            if aberta['proprio']:
                if not pilha:   # AvanceMonstre returned: the after-values of the own-routine writes
                    estado['proprias_fim'] = [[hex(a), v, cpu.mem_read(a, 1)[0]]
                                              for a, v in sorted(estado['proprias'].items())]
                continue
            enderecos = sorted({a for a in estado['escritas'][aberta['inicio']:]})
            depois = {a: cpu.mem_read(a, 1)[0] for a in enderecos}
            mudou = [[hex(a), aberta['antes'].get(a), depois[a]] for a in enderecos
                     if aberta['antes'].get(a) != depois[a]]
            aberta['registro'].update(exit={k: hex(v) for k, v in r.items()}, stack_pop=r['ESP'] - aberta['esp'] - 4,
                                      changed_bytes=mudou)
        if endereco not in simbolos:
            return
        nome = simbolos[endereco]
        esp = r['ESP']
        palavras = struct.unpack('<7I', bytes(cpu.mem_read(esp, 28)))
        dentro_de_proprio = not pilha or pilha[-1]['proprio']
        if endereco in proprias:
            if dentro_de_proprio:
                pilha.append(dict(ret=palavras[0], esp=esp, proprio=True))
            return
        if not dentro_de_proprio:
            return
        registro = dict(routine=nome, caller=b.nome(palavras[0]), caller_return=hex(palavras[0]),
                        entry={k: hex(v) for k, v in r.items()}, stack_words=[hex(p) for p in palavras[1:]])
        estado['chamadas'].append(registro)
        pilha.append(dict(ret=palavras[0], esp=esp, proprio=False, registro=registro, inicio=len(estado['escritas']),
                          antes=_Antes(cpu)))

    def escrita(cpu, _acesso, endereco, tamanho, _valor, _):
        if b.fase != 'isolated' or not estado['ativo'] or not estado['pilha']:
            return
        aberta = estado['pilha'][-1]
        for k in range(tamanho):
            if aberta['proprio']:
                if endereco + k not in estado['proprias']:
                    estado['proprias'][endereco + k] = cpu.mem_read(endereco + k, 1)[0]
            else:
                aberta['antes'].lembrar(endereco + k)
                estado['escritas'].append(endereco + k)

    b.cpu.hook_add(unicorn.UC_HOOK_BLOCK, bloco, begin=0x401000, end=0x493bff)
    b.cpu.ctl_flush_tb()
    perturbacoes = {'(no routine)': []}   # non-empty on purpose: Isolamento keeps `perturbacoes or {}`
    casos = []

    def observador(rotina, fase, caso, antes, resultado):
        if estado['ativo']:
            casos.append(dict(phase=fase, case=caso['case'], outside_calls=list(estado['chamadas']),
                              own_writes=estado['proprias_fim'], open_at_end=len(estado['pilha'])))
        if estado.get('gancho') is not None:
            b.cpu.hook_del(estado['gancho'])
        estado.update(ativo=False, pilha=[], chamadas=[], escritas=[], gancho=None, proprias={}, proprias_fim=None)
        if rotina == 'AvanceMonstre' and fase == 'load_tail':
            perturbacoes['AvanceMonstre'] = [dict(case=CASO, writes=[(CONTADOR, struct.pack('<I', CONTADOR_FORCADO))],
                                                  registers={})]

    iso = Isolamento(b, ('AvanceMonstre',), perturbacoes, observador)
    iso.instalar()
    resumos = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(120)),
                         ('frame1', lambda: b.executar_quadro(600))):
        correr()
        resumos[nome] = b.resumo_imagem(b.imagem())
    fases = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao = dict(phase_states_equal={f: resumos[f] == fases[f] for f in fases},
                      boundaries_equal=b.eventos_fronteira == [e for p in cap['phases'] for e in p['boundaries']],
                      code_unchanged=b.sha256_codigo() == cap['code_integrity']['after'])
    reproducao['passed'] = all(reproducao['phase_states_equal'].values()) and all(
        v for k, v in reproducao.items() if k != 'phase_states_equal')
    return iso, cap, reproducao, casos


class _Antes:
    """First-write values of the bytes an outside call writes (read lazily before the write lands)."""
    def __init__(self, cpu):
        self.cpu, self.valores = cpu, {}

    def lembrar(self, endereco):
        if endereco not in self.valores:
            self.valores[endereco] = self.cpu.mem_read(endereco, 1)[0]

    def get(self, endereco):
        return self.valores.get(endereco)


def main():
    if DESTINO.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {DESTINO}')
    t0 = time.monotonic()
    iso, cap, reproducao, casos = executar()
    forcado = [c for r in iso.registros for c in r['cases'] if c['case'] == CASO]
    relatorio = dict(
        schema='rising-lands/ai-runtime-first-raid-call-tree/1', original_sha256=HASH, translation_executed=False,
        label='forced input: frame-1 exact state (v1 scenario) with u32 0x508f7c = 9000, as Combat 1e9f28e',
        frame_capture=dict(path=str(CAPTURA.relative_to(ROOT)), sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in (
            'pesquisas-paralelas/ia-runtime/capturar_incursao_ia.py', 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py')},
        own_routines=list(PROPRIAS), path_reproduction=reproducao, avance_monstre_cases=iso.registros,
        forced_outside_calls=casos,
        method=('Isolamento case of AvanceMonstre at frame 1 with the counter forced to 9000; a block hook keeps a '
                'stack of own-routine and outside calls (closed when execution reaches the return address with ESP '
                'above the entry ESP); a write hook records the bytes each top-level outside call writes.'),
        seconds=round(time.monotonic() - t0, 3))
    ok = (reproducao['passed'] and len(forcado) == 1 and forcado[0]['reached_return'] and len(casos) == 1
          and casos[0]['open_at_end'] == 0 and casos[0]['own_writes'] is not None and all('exit' in c for c in casos[0]['outside_calls']))
    saida = DESTINO if ok else ROOT / '.local' / ('ai-raid-capture-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida.relative_to(ROOT)), reproduction=reproducao,
                          outside_calls=[(c['routine'], c['caller'], len(c.get('changed_bytes', ())))
                                         for k in casos for c in k['outside_calls']],
                          seconds=relatorio['seconds']), indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
