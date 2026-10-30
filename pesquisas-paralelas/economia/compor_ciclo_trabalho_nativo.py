"""Native-state composition check: ``compor_ciclo_trabalho``'s wiring over the whole entry state of each call.

Reruns the committed work-cycle capture natively (``capturar_ciclo_trabalho.executar``). At every recorded call of
a translated routine, ``ciclo_trabalho`` runs over a copy of the exact entry state (every mapped block) with the
same providers as the CPU-free composition (Core's ``provedor_entrada``, the live ``BonusUnidades``,
``provedor_caverna``; the rest the original's nested call replayed), and is compared with the original: exit
registers and every byte of every mapped block. This settles what the CPU-free run cannot (bytes no recorded call
reads).

    python3 "…/heavy_lease.py" economy -- python3 -B pesquisas-paralelas/economia/compor_ciclo_trabalho_nativo.py \\
        --saida pesquisas-paralelas/economia/composicao-ciclo-trabalho-nativa.json
"""
import argparse
import bisect
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import ciclo_trabalho as ct  # noqa: E402
from compor_ciclo_trabalho import ReplayComposto, provedores  # noqa: E402
from validar_ciclo_trabalho import TRADUZIDAS  # noqa: E402


def comparar(nome, regs, antes, resultado):
    from memoria_quadro_core import MemoriaQuadro
    buffers = {n: (base, bytearray(d)) for n, (base, d) in antes.items() if n != 'native_stack'}
    m = MemoriaQuadro([(base, buf) for base, buf in buffers.values()])
    rp = ReplayComposto(resultado, set(ct.ROTINAS) | set(ct.INTERNAS), provedores(m))
    d = dict(routine=nome, frame=resultado['frame'], arg=hex(regs['EAX'] & 0xffff))
    try:
        saida = getattr(ct.CicloTrabalho(m, externo=rp.externo(m)), '_' + nome)({k: regs[k] for k in ct.REG7 + ('ESP',)})
    except Exception as e:  # noqa: BLE001  (reported, never hidden)
        return dict(d, outcome='error', error=repr(e)), rp
    esperado = {k: int(resultado['exit_registers'][k], 16) for k in ct.REG7 + ('ESP',)}
    incertos = saida.get('_incertos', {})
    regs_dif = {k: [hex(saida[k]), hex(v)] for k, v in esperado.items() if (saida[k] ^ v) & ~incertos.get(k, 0)}
    nativo = {n: bytearray(dd) for n, (_, dd) in antes.items() if n != 'native_stack'}
    bases = {n: base for n, (base, _) in antes.items()}
    indice = sorted((base, n) for n, base in bases.items() if n != 'native_stack')
    chaves = [b for b, _ in indice]
    for endereco, _velho, novo in resultado['changed_bytes']:
        a = int(endereco, 16)
        n = indice[bisect.bisect_right(chaves, a) - 1][1]
        nativo[n][a - bases[n]] = novo
    bytes_dif = []
    for n, (base, b) in buffers.items():
        if b != nativo[n]:
            bytes_dif += [hex(base + i) for i in range(len(b)) if b[i] != nativo[n][i]]
    sobras = len(rp.sequencia) - rp.i
    if (regs_dif and set(regs_dif) == {'EAX'} and not bytes_dif and not rp.erros and not sobras
            and not ((saida['EAX'] ^ esperado['EAX']) & ~rp.ultimos_incertos.get('EAX', 0))):
        return dict(d, outcome='uncertain_register', registers=regs_dif), rp
    ok = not regs_dif and not bytes_dif and not rp.erros and not sobras
    if ok:
        return dict(d, outcome='match'), rp
    return dict(d, outcome='mismatch', registers=regs_dif, bytes=bytes_dif[:20], n_bytes=len(bytes_dif),
                replay=rp.erros[:10], unconsumed=sobras), rp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--ate', type=int, default=1600)
    a = ap.parse_args()
    import capturar_ciclo_trabalho as cct
    rel = dict(schema='rising-lands/economy-work-cycle-composition-native/1', counts={}, failures=[],
               served_by_translation={}, replayed_original={})

    def observador(nome, regs, antes, resultado):
        if nome not in TRADUZIDAS:
            return
        d, rp = comparar(nome, regs, antes, resultado)
        c = rel['counts'].setdefault(nome, dict(match=0, uncertain_register=0, mismatch=0, error=0))
        c[d['outcome']] += 1
        for k, v in rp.servidas.items():
            rel['served_by_translation'][k] = rel['served_by_translation'].get(k, 0) + v
        for k, v in rp.replayed.items():
            rel['replayed_original'][k] = rel['replayed_original'].get(k, 0) + v
        if d['outcome'] != 'match':
            rel['failures'].append(d)

    c, _, segundos = cct.executar(a.ate, observador=observador)
    rel.update(seconds=segundos, reproduction=c.reproducao)
    Path(RAIZ / a.saida).write_text(json.dumps(rel, indent=1, sort_keys=True) + '\n')
    print(json.dumps({k: rel[k] for k in ('counts', 'seconds')}, indent=1))
    for f in rel['failures'][:10]:
        print(json.dumps(f))


if __name__ == '__main__':
    main()
