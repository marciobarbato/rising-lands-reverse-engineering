"""Bounded original-x86 check of the input-chain's live CalculTroupe route.

Uses Economy's committed native read-before-write fixtures (not a new mission
capture). Each original call executes up to return or the first unbound owner
callee EnginSetType, without stubs/crossings. Compare every touched non-stack
byte and the provided AX/DX/CL at that stop. Missing BL is reported explicitly. This proves the prefix only, never
recruit completion. Run through heavy_lease.py; --saida is required.
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
from reinicio_ia import DependenciaIA

CAPTURA = 'pesquisas-paralelas/economia/evidencias/caverna-recrutamento/captura-caverna-recrutamento-exibicao.json.xz'
CONVERSAO, CHAMADA = 0x457b87, 0x420f69


class Memoria:
    """Only the native fixture's declared bytes and writes are readable."""
    def __init__(self, dados):
        self.dados, self.escritos = dict(dados), set()

    def _acesso(self, n, a, v):
        if v is None:
            return int.from_bytes(bytes(self.dados[a + i] for i in range(n)), 'little')
        for i, b in enumerate((v & ((1 << (8 * n)) - 1)).to_bytes(n, 'little')):
            self.dados[a + i] = b
            self.escritos.add(a + i)
        return v

    def u8(self, a, v=None):
        return self._acesso(1, a, v)

    def u16(self, a, v=None):
        return self._acesso(2, a, v)

    def u32(self, a, v=None):
        return self._acesso(4, a, v)

    def ler(self, a, n):
        return bytes(self.dados[a + i] for i in range(n))


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
    fim = b.executar(0x4259e6, [(0x401000, 0x494000)], regs,
                     parada={CONVERSAO, RETORNO}, limite_instrucoes=100000)
    if fim['EIP'] not in (CONVERSAO, RETORNO):
        raise RuntimeError('Original did not reach its bounded stop')
    m = Memoria(dados)
    d = DonosM3(m, som=None)
    pedidos = []
    externo = d.externo

    def observar(nome, chamada, entrada):
        if nome == 'EnginSetType':
            pedidos.append(dict(routine=nome, call=hex(chamada), registers=entrada))
        return externo(nome, chamada, entrada)
    d.caverna.externo = observar
    parada, saida = None, None
    try:
        saida = d.calcular_tropa_entrada(regs['EAX'])
    except DependenciaIA as erro:
        parada = dict(routine=erro.rotina, call=hex(erro.sitio))
    espera_parada = fim['EIP'] == CONVERSAO
    enderecos = set(dados) | escritos | m.escritos
    diferentes = [hex(a) for a in sorted(enderecos)
                  if a not in m.dados or m.dados[a] != uc.mem_read(a, 1)[0]]
    argumentos = dict(EAX=fim['EAX'] & 0xffff, EDX=fim['EDX'] & 0xffff,
                      ECX=fim['ECX'] & 0xff, EBX=fim['EBX'] & 0xff) if espera_parada else {}
    faltantes = sorted(set(argumentos) - set(pedidos[0]['registers'])) if pedidos else []
    argumentos_iguais = not espera_parada or (len(pedidos) == 1 and all(
        argumentos[k] == v for k, v in pedidos[0]['registers'].items()))
    lojas_ref = [[int(s[1], 16), int(s[2], 16), s[3], int(s[4], 16)] for s in caso['stores']]
    prefixo_igual = lojas == (lojas_ref[:len(lojas)] if espera_parada else lojas_ref)
    if espera_parada:
        chamada_ref = next(c for c in caso['calls'] if c[1] == 'EnginSetType')
        prefixo_igual = prefixo_igual and all(
            argumentos[k] == (int(chamada_ref[2][k], 16) & (0xff if k in ('EBX', 'ECX') else 0xffff))
            for k in argumentos)
    retorno_igual = espera_parada or (saida is not None and saida['EAX'] == fim['EAX'])
    ok = (parada == dict(routine='EnginSetType', call=hex(CHAMADA)) if espera_parada else parada is None)
    return dict(frame=caso['frame'], structure=regs['EAX'] & 0xffff,
                native_stop=hex(fim['EIP']), python_stop=parada, owner_requests=pedidos,
                bytes_checked=len(enderecos), byte_differences=diferentes[:20],
                native_written_bytes=len(escritos), python_written_bytes=len(m.escritos),
                provided_arguments_equal=argumentos_iguais, native_conversion_arguments=argumentos,
                missing_conversion_arguments=faltantes, consumed_return_equal=retorno_igual,
                native_prefix_matches_capture=prefixo_igual,
                equal=ok and not diferentes and argumentos_iguais and retorno_igual and prefixo_igual)


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
    r = dict(schema='rising-lands/ai-runtime-recruit-production-prefix/1',
             original_sha256=ORIGINAL_SHA256, fixture=CAPTURA,
             fixture_sha256=hashlib.sha256(bruto).hexdigest(),
             scope='Native CalculTroupe through return or before EnginSetType; no stubs, no completion claim',
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
