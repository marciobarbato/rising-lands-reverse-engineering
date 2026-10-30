"""Bounded native CalculTroupe comparison through the recruit owner callbacks.

Six immutable Economy fixtures execute without stubs through return or the
first unsupported ABI: SetSortEngin CALL 0x420f8c lacks DX in Economy's call.
Compare all non-stack state, native store sequence and every required argument
of each reached recruitment callback. The missing DX is a dependency, never 0.
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import sys
import subprocess

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente_ia_runtime import ROOT, ORIGINAL_SHA256
from emulador import BancadaX86, PILHA, RETORNO, mapear_paginas
from provedores_entrada_ia import DonosM3

CAPTURA = 'pesquisas-paralelas/economia/evidencias/caverna-recrutamento/captura-caverna-recrutamento-exibicao.json.xz'
PARADA, CHAMADA = 0x445fbc, 0x420f8c


def comparar(caso):
    import unicorn
    from unicorn import x86_const as X
    dados = {}
    for a, h in caso['read_before_write']:
        dados.update((int(a, 16) + i, b) for i, b in enumerate(bytes.fromhex(h)))
    b = BancadaX86()
    uc = b.cpu
    regioes = list(uc.mem_regions())
    paginas = {a & ~0xfff for a in dados if not any(lo <= a <= hi for lo, hi, _ in regioes)}
    mapear_paginas(uc, paginas)
    for a, h in caso['read_before_write']:
        uc.mem_write(int(a, 16), bytes.fromhex(h))
    escritos, lojas = set(), []

    def escrita(cpu, acesso, a, n, v, extra):
        if not PILHA <= a < PILHA + 0x10000:
            escritos.update(range(a, a + n))
            lojas.append([cpu.reg_read(X.UC_X86_REG_EIP), a, n, v & ((1 << (8 * n)) - 1)])
    uc.hook_add(unicorn.UC_HOOK_MEM_WRITE, escrita)
    uc.reg_write(X.UC_X86_REG_FPCW, 0x127f)  # captured Watcom: precision 53, chop
    regs = {k: int(v, 16) for k, v in caso['entry_registers'].items() if k not in ('ESP', 'EIP')}
    from recrutamento_core import ROTINAS, ARGUMENTOS
    from entrada_estruturas import ArgumentoNaoPassado
    from validar_fadiga_vegetacao import memoria_caso, mudancas
    blocos = {str(i): (lo, bytes(uc.mem_read(lo, hi-lo+1)))
              for i, (lo, hi, _) in enumerate(uc.mem_regions()) if lo != PILHA}
    nativos = []
    def observar_nativo(cpu, a, n, extra):
        nome = next(k for k, v in ROTINAS.items() if v == a)
        nativos.append(dict(routine=nome, registers={k: cpu.reg_read(getattr(X, 'UC_X86_REG_'+k)) & mask
                                                   for k, mask in ARGUMENTOS[nome].items()}))
    for entry in ROTINAS.values():
        uc.hook_add(unicorn.UC_HOOK_CODE, observar_nativo, begin=entry, end=entry)
    fim = b.executar(0x4259e6, [(0x401000, 0x494000)], regs,
                     parada={PARADA, RETORNO}, limite_instrucoes=1000000)
    if fim['EIP'] not in (PARADA, RETORNO):
        raise RuntimeError('Original did not reach its bounded stop')
    # The bench stops before executing the SetSortEngin entry hook.
    if fim['EIP'] == PARADA and (not nativos or nativos[-1]['routine'] != 'SetSortEngin'):
        nativos.append(dict(routine='SetSortEngin', registers={k: fim[k] & mask
                         for k, mask in ARGUMENTOS['SetSortEngin'].items()}))
    m, copias = memoria_caso(blocos)
    d = DonosM3(m, som=None)
    pedidos = []
    externo = d.externo
    def observar(nome, chamada, entrada):
        if nome in ROTINAS:
            pedidos.append(dict(routine=nome, call=hex(chamada), registers=dict(entrada)))
        return externo(nome, chamada, entrada)
    d.caverna.externo = observar
    parada, saida = None, None
    try:
        saida = d.calcular_tropa_entrada(regs['EAX'])
    except ArgumentoNaoPassado as erro:
        parada = dict(routine=erro.rotina, call=hex(erro.chamada), missing=list(erro.registradores))
    espera_parada = fim['EIP'] == PARADA
    depois = {n: (a, bytes(uc.mem_read(a, len(h)))) for n, (a, h) in blocos.items()}
    ref_mudancas = mudancas(blocos, depois)
    py_mudancas = mudancas(blocos, copias)
    argumentos_iguais = len(pedidos) == len(nativos) and all(
        p['routine'] == n['routine'] and all(k not in p['registers'] or
            (p['registers'][k] & mask) == n['registers'][k]
            for k, mask in ARGUMENTOS[n['routine']].items()) for p, n in zip(pedidos, nativos))
    faltantes = sorted(set(nativos[-1]['registers']) - set(pedidos[-1]['registers'])) if pedidos else []
    lojas_ref = [[int(s[1], 16), int(s[2], 16), s[3], int(s[4], 16)] for s in caso['stores']]
    prefixo_igual = lojas == (lojas_ref[:len(lojas)] if espera_parada else lojas_ref)
    retorno_igual = espera_parada or (saida is not None and saida['EAX'] == fim['EAX'])
    ok = (parada == dict(routine='SetSortEngin', call=hex(CHAMADA), missing=['EDX'])
          if espera_parada else parada is None)
    return dict(frame=caso['frame'], structure=regs['EAX'] & 0xffff,
                native_stop=hex(fim['EIP']), python_stop=parada, owner_requests=pedidos,
                native_owner_arguments=nativos, changed_bytes_equal=ref_mudancas == py_mudancas,
                native_changed_bytes=len(ref_mudancas), python_changed_bytes=len(py_mudancas),
                provided_arguments_equal=argumentos_iguais, missing_final_arguments=faltantes,
                consumed_return_equal=retorno_igual, native_prefix_matches_capture=prefixo_igual,
                equal=ok and ref_mudancas == py_mudancas and argumentos_iguais and retorno_igual and prefixo_igual)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    bruto = (ROOT / CAPTURA).read_bytes()
    cap = json.loads(lzma.decompress(bruto))
    casos = [c for c in cap['calls'] if c['routine'] == 'CalculTroupe' and
             c['frame'] in (296, 297, 868, 869, 1362, 1363)]
    if len(casos) != 6 or cap['original_sha256'] != ORIGINAL_SHA256:
        raise ValueError('Expected six declared original fixtures')
    resultados = [comparar(c) for c in casos]
    r = dict(schema='rising-lands/ai-runtime-recruit-production-prefix/2',
             original_sha256=ORIGINAL_SHA256, fixture=CAPTURA,
             fixture_sha256=hashlib.sha256(bruto).hexdigest(),
             scope='Native CalculTroupe through return or before SetSortEngin; missing Economy DX retained as ABI stop',
             cases=resultados, equal=sum(c['equal'] for c in resultados),
             comparisons=len(resultados),
             source_revision=subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
             source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in (
                 'pesquisas-paralelas/ia-runtime/validar_producao_entrada_ia.py',
                 'pesquisas-paralelas/ia-runtime/provedores_entrada_ia.py',
                 'pesquisas-paralelas/ia-runtime/composicao_entrada_ia.py')})
    destino = ROOT / a.saida
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(r, indent=1, sort_keys=True) + '\n')
    print(json.dumps(r, indent=1))
    return 0 if r['equal'] == len(resultados) else 2


if __name__ == '__main__':
    raise SystemExit(main())
