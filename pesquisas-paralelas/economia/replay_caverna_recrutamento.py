"""CPU-free replay of the committed cave/recruitment capture against ``caverna_recrutamento``.

Every recorded call of a translated routine is replayed over a sparse memory holding exactly the bytes the
original read before writing in that call (``read_before_write``); a translation that reads any other byte fails.
Other fronts' callees are the original's own nested calls (``validar_caverna_recrutamento.Replay``). The result
must match the exit registers and the final value of every byte the original changed, and every byte the
translation wrote must end equal to the original's last store there (or its entry value).

    python3 -B pesquisas-paralelas/economia/replay_caverna_recrutamento.py
"""
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import caverna_recrutamento as cr  # noqa: E402
from replay_ciclo_trabalho import LeituraNaoGravada, MemoriaEsparsa  # noqa: E402
from validar_caverna_recrutamento import CAPTURA, Replay, TRADUZIDAS, comparar_saida, proprias  # noqa: E402
from validar_ciclo_trabalho import carregar  # noqa: E402


def replay_chamada(r, cls=cr.CavernaRecrutamento):
    """(outcome, detail) of one recorded call."""
    m = MemoriaEsparsa(r['read_before_write'])
    rp = Replay(r, proprias())
    cav = cls(m, externo=rp(m))
    regs = {k: int(v, 16) for k, v in r['entry_registers'].items()}
    d = dict(routine=r['routine'], frame=r['frame'], action=r.get('action'), arg=hex(regs['EAX'] & 0xffff))
    try:
        saida = getattr(cav, '_' + r['routine'])({k: regs[k] for k in cr.REG7 + ('ESP',)})
    except cr.ForaDoDominioCaverna as e:
        return 'outside_domain', dict(d, address=hex(e.endereco))
    except (cr.DependenciaCavernaRecrutamento, LeituraNaoGravada, KeyError, ZeroDivisionError) as e:
        return 'error', dict(d, error=repr(e), replay=rp.erros)
    regs_dif, _ = comparar_saida(saida, r)
    final = {int(a, 16): novo for a, _v, novo in r['changed_bytes']}
    bytes_dif = [hex(a) for a, v in final.items() if m.escritos.get(a, m.bytes.get(a)) != v]
    # A byte written but not changed by the original must end with the original's last stored value there (a
    # byte the original never stored to is a spurious write).
    lojas = {}
    for loja in r['stores']:
        endereco, tamanho, valor = int(loja[2], 16), loja[3], int(loja[4], 16)
        for b in range(tamanho):
            lojas[endereco + b] = (valor >> (8 * b)) & 0xff
    bytes_dif += [hex(a) for a, v in m.escritos.items()
                  if a not in final and v != lojas.get(a, m.bytes.get(a, -1))]
    sobras = len(rp.sequencia) - rp.i
    if regs_dif or bytes_dif or rp.erros or sobras:
        return 'mismatch', dict(d, registers=regs_dif, bytes=bytes_dif[:20], replay=rp.erros, unconsumed=sobras)
    return 'match', d


def replay(captura=None, cls=cr.CavernaRecrutamento):
    captura = captura or carregar(CAPTURA)[0]
    contagem, falhas = {}, []
    for r in captura['calls']:
        if r['routine'] not in TRADUZIDAS:
            continue
        resultado, d = replay_chamada(r, cls)
        c = contagem.setdefault(r['routine'], dict(match=0, mismatch=0, outside_domain=0, error=0))
        c[resultado] += 1
        if resultado != 'match':
            falhas.append(dict(d, outcome=resultado))
    return contagem, falhas


if __name__ == '__main__':
    contagem, falhas = replay()
    print(json.dumps(contagem, indent=1))
    for f in falhas[:30]:
        print(json.dumps(f))
