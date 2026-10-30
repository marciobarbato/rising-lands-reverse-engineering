"""CPU-free replay of the committed restore captures against ``restauracao`` (and ``alimentacao`` composed with it).

Every recorded EnginRestaureEtat, BatimentEnleveMatiere, SetDechargeCaveEnginSelect and (``corpo`` capture)
state-19 body is replayed over a sparse memory holding exactly the bytes the original read before writing in that call
(``read_before_write``); a translation that reads any other byte fails. Other fronts' callees are the original's own
nested calls and the frame boundaries their recorded registers (``validar_restauracao.Replay``/``ReplayCorpo``). The
result must match the exit registers and the final value of every byte the original changed, and every byte the
translation wrote must end equal to the original's last store there (or its entry value).

    python3 -B pesquisas-paralelas/economia/replay_restauracao.py [rotinas|corpo] [--sem-core]
"""
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import alimentacao as al  # noqa: E402
from replay_ciclo_trabalho import LeituraNaoGravada, MemoriaEsparsa  # noqa: E402
from validar_ciclo_trabalho import carregar  # noqa: E402
from validar_restauracao import CAPTURAS, ERROS, TRADUZIDAS, comparar_saida, executar_traducao  # noqa: E402


def replay_chamada(r, executar=executar_traducao):
    """(outcome, detail) of one recorded call."""
    m = MemoriaEsparsa(r['read_before_write'])
    d = dict(routine=r['routine'], frame=r['frame'], action=r.get('action'), eax=r['entry_registers']['EAX'])
    try:
        saida, rp = executar(r['routine'], m, r)
    except al.ForaDoDominioFome as e:
        return 'outside_domain', dict(d, address=hex(e.endereco))
    except ERROS + (LeituraNaoGravada,) as e:
        return 'error', dict(d, error=repr(e))
    regs_dif, _ = comparar_saida(saida, r)
    final = {int(a, 16): novo for a, _v, novo in r['changed_bytes']}
    bytes_dif = [hex(a) for a, v in final.items() if m.escritos.get(a, m.bytes.get(a)) != v]
    lojas = {}
    for loja in r['stores']:
        endereco, tamanho, valor = int(loja[2], 16), loja[3], int(loja[4], 16)
        for b in range(tamanho):
            lojas[endereco + b] = (valor >> (8 * b)) & 0xff
    bytes_dif += [hex(a) for a, v in m.escritos.items()
                  if a not in final and v != lojas.get(a, m.bytes.get(a, -1))]
    sobras = len(rp.sequencia) - rp.i
    fronteiras = len(getattr(rp, 'fronteiras', ()))
    if regs_dif or bytes_dif or rp.erros or sobras or fronteiras:
        return 'mismatch', dict(d, registers=regs_dif, bytes=bytes_dif[:20], replay=rp.erros, unconsumed=sobras,
                                unconsumed_boundaries=fronteiras)
    return 'match', d


def replay(captura, executar=executar_traducao):
    contagem, falhas = {}, []
    for r in captura['calls']:
        if r['routine'] not in TRADUZIDAS:
            continue
        resultado, d = replay_chamada(r, executar)
        c = contagem.setdefault(r['routine'], dict(match=0, mismatch=0, outside_domain=0, error=0))
        c[resultado] += 1
        if resultado != 'match':
            falhas.append(dict(d, outcome=resultado))
    return contagem, falhas


def com_core(nome, m, resultado):
    """``executar_traducao`` with Core's ``provedor_fadiga`` serving the bodies' ChercheVegetLibre."""
    from validar_alimentacao import provedores_fadiga
    return executar_traducao(nome, m, resultado, provedores_fadiga())


if __name__ == '__main__':
    modo = next((a for a in sys.argv[1:] if not a.startswith('-')), 'rotinas')
    contagem, falhas = replay(carregar(CAPTURAS[modo])[0], executar_traducao if '--sem-core' in sys.argv else com_core)
    print(json.dumps(contagem, indent=1))
    for f in falhas[:40]:
        print(json.dumps(f))
