"""CPU-free replay of the committed work-cycle capture against ``ciclo_trabalho``.

Every recorded call of a translated routine is replayed over a sparse memory holding exactly the bytes the
original read before writing in that call (``read_before_write``); a translation that reads any other byte
fails. Other fronts' callees are the original's own nested calls (``validar_ciclo_trabalho.Replay``). The
result must match the exit registers and the final value of every byte the original changed, and every byte
the translation wrote must end equal to the original's.

    python3 -B pesquisas-paralelas/economia/replay_ciclo_trabalho.py
"""
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import ciclo_trabalho as ct  # noqa: E402
from validar_ciclo_trabalho import Replay, TRADUZIDAS, carregar  # noqa: E402

CAPTURA = PASTA / 'evidencias/ciclo-trabalho/captura-ciclo-trabalho-exibicao.json.xz'


class LeituraNaoGravada(LookupError):
    pass


class MemoriaEsparsa:
    def __init__(self, runs):
        self.bytes = {}
        for inicio, dados in runs:
            a = int(inicio, 16)
            for i, b in enumerate(bytes.fromhex(dados)):
                self.bytes[a + i] = b
        self.escritos = {}

    def _ler(self, a):
        a &= 0xffffffff
        if a in self.escritos:
            return self.escritos[a]
        if a not in self.bytes:
            raise LeituraNaoGravada(f'0x{a:08x} was not read by the original before its writes')
        return self.bytes[a]

    def _acesso(self, n, a, valor):
        if valor is None:
            return sum(self._ler(a + i) << (8 * i) for i in range(n))
        valor &= (1 << 8 * n) - 1
        for i in range(n):
            self.escritos[(a + i) & 0xffffffff] = (valor >> (8 * i)) & 0xff
        return valor

    def u8(self, a, v=None):
        return self._acesso(1, a, v)

    def u16(self, a, v=None):
        return self._acesso(2, a, v)

    def u32(self, a, v=None):
        return self._acesso(4, a, v)


def replay_chamada(r):
    """(outcome, detail) of one recorded call."""
    m = MemoriaEsparsa(r['read_before_write'])
    rp = Replay(r, set(ct.ROTINAS) | set(ct.INTERNAS))
    ciclo = ct.CicloTrabalho(m, externo=rp(m))
    regs = {k: int(v, 16) for k, v in r['entry_registers'].items()}
    d = dict(routine=r['routine'], frame=r['frame'], arg=hex(regs['EAX'] & 0xffff))
    try:
        saida = getattr(ciclo, '_' + r['routine'])(regs)
    except ct.ForaDoDominioTrabalho as e:
        return 'outside_domain', dict(d, address=hex(e.endereco))
    except (ct.DependenciaCicloTrabalho, LeituraNaoGravada, KeyError) as e:
        return 'error', dict(d, error=repr(e), replay=rp.erros)
    esperado = {k: int(r['exit_registers'][k], 16) for k in ct.REG7 + ('ESP',)}
    incertos = saida.get('_incertos', {})
    regs_dif = {k: [hex(saida[k]), hex(v)] for k, v in esperado.items() if (saida[k] ^ v) & ~incertos.get(k, 0)}
    final = {int(a, 16): novo for a, _v, novo in r['changed_bytes']}
    bytes_dif = [hex(a) for a, v in final.items() if m.escritos.get(a, m.bytes.get(a)) != v]
    bytes_dif += [hex(a) for a, v in m.escritos.items() if a not in final and v != m.bytes.get(a, v)]
    sobras = len(rp.sequencia) - rp.i
    if regs_dif or bytes_dif or rp.erros or sobras:
        return 'mismatch', dict(d, registers=regs_dif, bytes=bytes_dif[:20], replay=rp.erros, unconsumed=sobras)
    return 'match', d


def replay(captura=None):
    captura = captura or carregar(CAPTURA)[0]
    contagem, falhas = {}, []
    for r in captura['calls']:
        if r['routine'] not in TRADUZIDAS:
            continue
        resultado, d = replay_chamada(r)
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
