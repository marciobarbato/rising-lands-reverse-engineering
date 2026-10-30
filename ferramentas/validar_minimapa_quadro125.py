"""Frame-125 discovery, light and structure minimap of the lodging that makes the cave the player's (native).

Economy's work-cycle composition (``pesquisas-paralelas/economia/compor_ciclo_trabalho*.py``) reported one mismatch:
frame 125, BatimentLogeEngin(cave 1, colonist 3) -> 196 bytes of the minimap view (0x47933a26.., original 32 -> 162)
differ, attributed to DecouvreTerrain. This script settles it original-first, at that exact state.

Bench: Economy's committed work-cycle capture driver (``capturar_ciclo_trabalho``: Missions' MONDE01 display path,
frames 0/1 reproduced, the same declared actions), imported read-only and rerun natively to frame 125. Only
BatimentLogeEngin is isolated (at frame 125); the isolation restores the state after each recorded call, so the
trajectory is the capture's. During that call code hooks snapshot the whole mapped state (every DGROUP/thread/
allocation block) and the registers at the entries of DecouvreTerrain 0x476851, IllumineTerrain 0x476cb3 and
BatimentModifyMap 0x419e97. From those snapshots the cases (``CASOS``) run the ORIGINAL routine natively as leaf
calls (each from its snapshot, state restored afterwards by the isolation): the three calls exactly as the original
made them, plus declared variants (BatimentModifyMap with DL = 0, the register Economy's composition handed Core;
DL = 1 and 0 before the light; DecouvreTerrain with radius 3, Economy's earlier wiring bug).

``--capturar <file>`` writes the original-only capture (no translation imported). The default mode reruns natively,
checks the native rerun against the committed capture and Economy's committed work-cycle record of that call, and
compares each case with Core's ``entrada_estruturas`` (the provider Economy wires) over a copy of the case's exact
entry state: exit registers EAX..EBP (except declared uncertain bits) and every byte of every block. It also runs the
call shapes of ``provedor_entrada``: with AX and DL the in-situ result, without DL ``ArgumentoNaoPassado``.

    python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_minimapa_quadro125.py --capturar \\
        evidencias/minimapa-quadro125/captura-minimapa-quadro125.json.xz
    python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_minimapa_quadro125.py
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import subprocess
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'ferramentas', RAIZ / 'pesquisas-paralelas/economia'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

CAPTURA = RAIZ / 'evidencias/minimapa-quadro125/captura-minimapa-quadro125.json.xz'
RELATORIO = RAIZ / 'relatorios/minimapa-quadro125-emulada.json'
CAPTURA_ECONOMIA = RAIZ / 'pesquisas-paralelas/economia/evidencias/ciclo-trabalho/captura-ciclo-trabalho-exibicao.json.xz'
QUADRO, ROTINA = 125, 'BatimentLogeEngin'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
M32 = 0xffffffff
SNAPSHOTS = ('DecouvreTerrain', 'IllumineTerrain', 'BatimentModifyMap')
# case -> (routine, snapshot taken at the entry of, register overrides of the snapshot's entry registers)
CASOS = {
    'decouvre_terrain_in_situ': ('DecouvreTerrain', 'DecouvreTerrain', {}),
    'illumine_terrain_in_situ': ('IllumineTerrain', 'IllumineTerrain', {}),
    'modify_map_in_situ': ('BatimentModifyMap', 'BatimentModifyMap', {}),
    'modify_map_dl0_composition_input': ('BatimentModifyMap', 'BatimentModifyMap', {'EDX': 0}),
    'modify_map_dl1_before_light': ('BatimentModifyMap', 'DecouvreTerrain', {'EAX': 1, 'EDX': 1}),
    'modify_map_dl0_before_light': ('BatimentModifyMap', 'DecouvreTerrain', {'EAX': 1, 'EDX': 0}),
    'decouvre_terrain_radius3': ('DecouvreTerrain', 'DecouvreTerrain', {'EDX': 3}),
}
FONTES = ('ferramentas/validar_minimapa_quadro125.py', 'ferramentas/entrada_estruturas.py',
          'ferramentas/visao_movimento.py', 'ferramentas/minimapa_estruturas.py', 'ferramentas/mundo_vivo.py',
          'pesquisas-paralelas/economia/capturar_ciclo_trabalho.py',
          'pesquisas-paralelas/economia/bancada_ciclo_trabalho.py')
MINIMAPAS = (0x507d5c, 0x507d60, 0x507d64)   # pointers: view, unit layer, structure layer (128 x 128 each)


def _sem_pilha(blocos):
    return {n: v for n, v in blocos.items() if n != 'native_stack'}


def executar_nativo():
    """Rerun natively to frame 125's BatimentLogeEngin; returns (record, snapshots, cases, reproduction, seconds).

    ``record``: the isolated call's result (as Economy's bench records it); ``snapshots[name]`` = (entry registers,
    blocks) at the first entry of that routine inside the call; ``cases[case]`` = the native leaf run (entry/exit
    registers, changed bytes, snapshot blocks)."""
    import capturar_ciclo_trabalho as cct
    from bancada_ciclo_trabalho import Ciclo
    import unicorn
    from unicorn import x86_const as x86
    estado = cct.Estado()
    alvo = dict(registro=None, snapshots={}, casos={}, ganchos=[])

    def instantaneo(b, nome):
        def f(cpu, endereco, tamanho, _):
            if nome not in alvo['snapshots']:
                regs = {k: cpu.reg_read(getattr(x86, 'UC_X86_REG_' + k)) for k in REGISTROS + ('ESP',)}
                alvo['snapshots'][nome] = (regs, b.imagem())
        return f

    def escolher(nome, regs, c):
        if nome != ROTINA or c.k != QUADRO or alvo['registro'] is not None:
            return False
        b = c.b
        for n in SNAPSHOTS:
            a = b.sym[n]
            alvo['ganchos'].append(b.cpu.hook_add(unicorn.UC_HOOK_CODE, instantaneo(b, n), begin=a, end=a))
        return True

    def observador(nome, regs, blocos, resultado):
        b = ciclo.b
        for g in alvo['ganchos']:
            b.cpu.hook_del(g)
        b.cpu.ctl_flush_tb()
        alvo['ganchos'] = []
        alvo['registro'] = resultado
        faltam = [n for n in SNAPSHOTS if n not in alvo['snapshots']]
        if faltam:
            raise RuntimeError(f'No entry of {faltam} inside the frame-{QUADRO} {ROTINA}')
        # Leaf runs from each snapshot (the isolation restores the call's entry state afterwards).
        for caso, (rotina, origem, trocas) in CASOS.items():
            regs_in, blocos_in = alvo['snapshots'][origem]
            for base, dados in blocos_in.values():
                b.cpu.mem_write(base, dados)
            if b.imagem().keys() != blocos_in.keys():
                raise RuntimeError(f'{caso}: the block set differs from the snapshot')
            entrada = {k: regs_in[k] for k in REGISTROS}
            entrada.update(trocas)
            n = len(ciclo.acoes)
            r = ciclo._passo(ciclo.k, dict(kind='call', label=caso, routine=rotina, registers=entrada))
            del ciclo.acoes[n:]
            if r['blocks_added'] or r['blocks_removed']:
                raise RuntimeError(f'{caso}: blocks changed {r["blocks_added"]} {r["blocks_removed"]}')
            alvo['casos'][caso] = dict(routine=rotina, snapshot=origem, overrides={k: hex(v) for k, v in trocas.items()},
                                       entry_registers={k: hex(v) for k, v in entrada.items()},
                                       exit_registers=r['exit_registers'], changed_bytes=r['changed_bytes'],
                                       boundaries=r['boundaries'])

    ciclo = Ciclo((ROTINA,), escolher, cct.ordens(estado), observador=observador)
    segundos = ciclo.executar(QUADRO)
    if alvo['registro'] is None:
        raise RuntimeError(f'No {ROTINA} call at frame {QUADRO}')
    return alvo['registro'], alvo['snapshots'], alvo['casos'], ciclo.reproducao, segundos


def _minimapas(blocos):
    """{address range name: (start, end)} of the three 128x128 minimap buffers, from the snapshot's pointers."""
    from memoria_quadro_core import MemoriaQuadro
    m = MemoriaQuadro((base, bytearray(d)) for base, d in _sem_pilha(blocos).values())
    return {nome: (m.u32(p), m.u32(p) + 0x4000) for nome, p in zip(('view', 'units', 'structures'), MINIMAPAS)}


def resumo_caso(caso, regioes):
    mm = {nome: sum(1 for a, _, _ in caso['changed_bytes'] if i <= int(a, 16) < f) for nome, (i, f) in regioes.items()}
    return dict(changed=len(caso['changed_bytes']), minimap_changed=mm)


def comparar_economia(registro):
    """The native rerun of the call against Economy's committed work-cycle record of it."""
    dados = json.loads(lzma.decompress(CAPTURA_ECONOMIA.read_bytes()))
    ref = [c for c in dados['calls'] if c['routine'] == ROTINA and c['frame'] == QUADRO]
    if len(ref) != 1:
        return dict(equal=False, reason=f'{len(ref)} committed records')
    ref = ref[0]
    chaves = ('entry_registers', 'exit_registers', 'changed_bytes')
    return dict(equal=all(ref[k] == registro[k] for k in chaves), compared=list(chaves),
                capture_sha256=hashlib.sha256(CAPTURA_ECONOMIA.read_bytes()).hexdigest())


def comparar_caso(nome, caso, blocos):
    """Core's translation over a copy of the case's entry state against the native leaf run."""
    from entrada_estruturas import EntradaEstruturas
    from validar_visao_grupos import memoria_de, mudancas
    m, copias = memoria_de(blocos)
    entrada = {k: int(caso['entry_registers'][k], 16) for k in REGISTROS}
    registro = dict(case=nome, routine=caso['routine'])
    try:
        saida = EntradaEstruturas(m).chamar(caso['routine'], entrada)
    except Exception as erro:            # a mismatch, never ignored
        return dict(registro, ok=False, python_error=f'{type(erro).__name__}: {erro}')
    incertos = saida.get('_incertos') or {}
    nativos = {k: int(caso['exit_registers'][k], 16) for k in REGISTROS}
    dif = {k: [hex(saida[k]), hex(nativos[k])] for k in REGISTROS if (saida[k] ^ nativos[k]) & ~incertos.get(k, 0) & M32}
    py = mudancas(blocos, copias)
    registro.update(ok=not dif and py == caso['changed_bytes'] and not caso['boundaries'],
                    register_differences=dif, changed_equal=py == caso['changed_bytes'],
                    native_changed=len(caso['changed_bytes']), uncertain_bits={k: hex(v) for k, v in incertos.items() if v})
    if py != caso['changed_bytes']:
        a, b = {x[0]: x for x in py}, {x[0]: x for x in caso['changed_bytes']}
        registro.update(python_only=[a[k] for k in a if a[k] != b.get(k)][:16],
                        native_only=[b[k] for k in b if b[k] != a.get(k)][:16])
    return registro


def comparar_formas_provedor(casos, snapshots):
    """``provedor_entrada`` with Economy's call shapes for BatimentModifyMap at 0x41fa88."""
    from entrada_estruturas import ArgumentoNaoPassado, EntradaEstruturas, provedor_entrada
    from validar_visao_grupos import memoria_de, mudancas
    blocos = _sem_pilha(snapshots['BatimentModifyMap'][1])
    saida = []
    m, copias = memoria_de(blocos)
    r = provedor_entrada(EntradaEstruturas(m))('BatimentModifyMap', 0x41fa88, {'EAX': 1, 'EDX': 1})
    nativo = casos['modify_map_in_situ']
    saida.append(dict(shape="{'EAX': 1, 'EDX': 1}", ok=mudancas(blocos, copias) == nativo['changed_bytes'] and
                      int(nativo['exit_registers']['EAX'], 16) & ~r.get('_incertos', {}).get('EAX', 0) ==
                      r['EAX'] & ~r.get('_incertos', {}).get('EAX', 0)))
    m, copias = memoria_de(blocos)
    try:
        provedor_entrada(EntradaEstruturas(m))('BatimentModifyMap', 0x41fa88, {'EAX': 1})
        saida.append(dict(shape="{'EAX': 1}", ok=False, reason='no ArgumentoNaoPassado'))
    except ArgumentoNaoPassado as erro:
        saida.append(dict(shape="{'EAX': 1}", ok=mudancas(blocos, copias) == [], raised=str(erro)))
    return saida


def diferenca(a, b):
    """Addresses whose final value differs between two leaf runs from the same snapshot."""
    fa, fb = {x[0]: x[2] for x in a['changed_bytes']}, {x[0]: x[2] for x in b['changed_bytes']}
    va, vb = {x[0]: x[1] for x in a['changed_bytes']}, {x[0]: x[1] for x in b['changed_bytes']}
    return sorted((k for k in set(fa) | set(fb) if fa.get(k, va.get(k, vb.get(k))) != fb.get(k, vb.get(k, va.get(k)))),
                  key=lambda k: int(k, 16))


def capturar(saida):
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    registro, snapshots, casos, reproducao, segundos = executar_nativo()
    if 'entrada_estruturas' in sys.modules:
        raise RuntimeError('The capture imported the translation')
    regioes = _minimapas(snapshots['DecouvreTerrain'][1])
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    dados = dict(
        schema='rising-lands/core-minimap-frame125-capture/1', original_sha256=HASH_ORIGINAL, translation_executed=False,
        source_revision=revisao, source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES[5:]},
        frame=QUADRO, routine=ROTINA, path_reproduction=reproducao, seconds=segundos,
        economy_record=comparar_economia(registro), minimap_buffers={k: [hex(i), hex(f)] for k, (i, f) in regioes.items()},
        snapshot_registers={n: {k: hex(v) for k, v in snapshots[n][0].items()} for n in SNAPSHOTS},
        cases=casos, summary={n: resumo_caso(c, regioes) for n, c in casos.items()},
        dl0_vs_in_situ=len(diferenca(casos['modify_map_dl0_composition_input'], casos['modify_map_in_situ'])))
    saida.parent.mkdir(parents=True, exist_ok=True)
    bruto = (json.dumps(dados, sort_keys=True) + '\n').encode()
    saida.write_bytes(lzma.compress(bruto, preset=9))
    print(json.dumps(dict(output=str(saida), reproduction=reproducao, economy_record=dados['economy_record']['equal'],
                          summary=dados['summary'], dl0_vs_in_situ=dados['dl0_vs_in_situ'], seconds=segundos), indent=1))
    encerrar_captura(0, saida)


def validar(saida):
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    captura = json.loads(lzma.decompress(CAPTURA.read_bytes()))
    registro, snapshots, casos, reproducao, segundos = executar_nativo()
    regioes = _minimapas(snapshots['DecouvreTerrain'][1])
    registros = []
    for nome, caso in casos.items():
        r = comparar_caso(nome, caso, _sem_pilha(snapshots[CASOS[nome][1]][1]))
        r['native_equals_capture'] = captura['cases'].get(nome) == caso
        r['ok'] = r['ok'] and r['native_equals_capture']
        registros.append(r)
        print(f"{nome}: {'ok' if r['ok'] else 'MISMATCH'}", file=sys.stderr, flush=True)
    formas = comparar_formas_provedor(casos, snapshots)
    economia = comparar_economia(registro)
    dl0 = diferenca(casos['modify_map_dl0_composition_input'], casos['modify_map_in_situ'])
    relatorio = dict(
        schema='rising-lands/core-minimap-frame125-differential/1', original_sha256=HASH_ORIGINAL,
        capture=dict(path=str(CAPTURA.relative_to(RAIZ)), sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        frame=QUADRO, routine=ROTINA, path_reproduction=reproducao, economy_record=economia,
        comparisons=len(registros), mismatches=[r for r in registros if not r['ok']], cases=registros,
        changed_bytes_compared=sum(r.get('native_changed', 0) for r in registros),
        summary={n: resumo_caso(c, regioes) for n, c in casos.items()}, provider_shapes=formas,
        dl0_vs_in_situ=dict(bytes=len(dl0), first=dl0[:4]), seconds=segundos)
    ok = (all(reproducao.values()) and economia['equal'] and not relatorio['mismatches'] and
          len(registros) == len(CASOS) and all(f['ok'] for f in formas))
    if not ok:
        saida = RAIZ / '.local/minimapa-quadro125' / f'falha-{time.strftime("%Y%m%dT%H%M%S")}.json'
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'w') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), comparisons=len(registros), mismatches=len(relatorio['mismatches']),
                          economy_record=economia['equal'], provider_shapes=[f['ok'] for f in formas],
                          dl0_vs_in_situ=len(dl0), reproduction=reproducao, seconds=segundos), indent=1))
    encerrar_captura(0 if ok else 2, saida)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--capturar', help='write the original-only capture here (relative to the repository)')
    ap.add_argument('--saida', default=str(RELATORIO.relative_to(RAIZ)))
    a = ap.parse_args()
    if a.capturar:
        capturar(RAIZ / a.capturar)
    else:
        validar(RAIZ / a.saida)


if __name__ == '__main__':
    main()
