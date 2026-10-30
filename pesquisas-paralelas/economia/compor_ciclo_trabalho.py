"""CPU-free replay of the committed work-cycle capture through the wired providers (composition check).

``ciclo_trabalho.CicloTrabalho`` runs every recorded call of a translated routine, as in
``replay_ciclo_trabalho``, but its named dependencies are served by the real translations where they exist:
- Core: ``entrada_estruturas.provedor_entrada`` (Bag primitives, PlaceLibre, BatimentAdjacent, GetCaseCentrale,
  RetireEngin, AnimWorkEngin, DeplaceEngin through ``construcao_core``, the world effects, ...), with Economy's
  live ``BonusUnidades`` for DeplaceEngin's CalculFatigue;
- Economy: ``caverna_recrutamento.provedor_caverna`` (BatimentHabitable, InitBatimentPlayer; its own Core callees
  through ``visao_grupos.provedor_saida`` for CalculPosition/RechercheDecalageSortie, else ``provedor_entrada``)
  and the live ``BonusUnidades`` (BonusGetValEngin);
- every other callee (terrain search, Random, SetMiniMap, PlaySnd_PostSound, MineGetCapacite, TerrainDeposeSac)
  stays the original's own nested call replayed, and is counted as such.
A provided callee is checked against the original's nested call: its name and argument bits, then its exit
registers (bits it marks uncertain excluded; a difference is listed as a diagnostic, because Economy passes only
the argument bits it models). The provider's registers are what the caller receives. The call as a whole must match the exit registers and the final
value of every byte the original changed, and every byte written must end equal to the original's.

Memory: the bytes the original read before writing in that call; every other byte holds the poison 0xa5. Core's
live world (``mundo_vivo``) binds all its grid and pointer tables when it is built, reading far more than any one
call of the original does, so reads of unrecorded bytes are allowed and counted (``unrecorded_bytes_read``): a
provider whose result depends on a byte the original did not read shows up as a mismatch, not as an error.
``--estrito`` makes such a read fail instead. ``--base`` takes those bytes from the whole mapped state at frame 2's
CalculGame entry (``imagem_base_ciclo.py``, native, before any declared action) instead of the poison; the
recorded bytes of each call always override it.

    python3 -B pesquisas-paralelas/economia/compor_ciclo_trabalho.py [--saida <report.json>]
"""
import argparse
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import ciclo_trabalho as ct  # noqa: E402
from validar_ciclo_trabalho import TRADUZIDAS, carregar  # noqa: E402

CAPTURA = PASTA / 'evidencias/ciclo-trabalho/captura-ciclo-trabalho-exibicao.json.xz'
VENENO = 0xa5
M32 = 0xffffffff


class LeituraNaoGravada(LookupError):
    pass


class MemoriaComposta:
    """Recorded bytes in 16 MiB chunks; strict scalar reads, lenient ``vista`` (see the module docstring)."""
    PEDACO = 1 << 24

    def __init__(self, runs, estrito=False, base=None):
        self.estrito, self.nao_gravadas = estrito, set()
        self.dados, self.conhecidos, self.original = {}, {}, {}
        for c, d in (base or {}).items():
            self.dados[c], self.conhecidos[c] = bytearray(d), bytearray(self.PEDACO)
        for inicio, hexa in runs:
            a = int(inicio, 16)
            for i, b in enumerate(bytes.fromhex(hexa)):
                d, k = self._pedaco(a + i)
                d[(a + i) % self.PEDACO], k[(a + i) % self.PEDACO] = b, 1
                self.original[a + i] = b
        self.inicial = {c: bytes(d) for c, d in self.dados.items()}

    def _pedaco(self, a):
        c = a // self.PEDACO
        if c not in self.dados:
            self.dados[c] = bytearray([VENENO]) * self.PEDACO
            self.conhecidos[c] = bytearray(self.PEDACO)
            if hasattr(self, 'inicial'):
                self.inicial[c] = bytes(self.dados[c])
        return self.dados[c], self.conhecidos[c]

    def _acesso(self, n, a, v):
        a &= M32
        d, k = self._pedaco(a)
        o = a % self.PEDACO
        if v is None:
            for i in range(n):
                if not k[o + i] and d[o + i] == self.inicial[a // self.PEDACO][o + i]:
                    if self.estrito:
                        raise LeituraNaoGravada(f'0x{a + i:08x} was not read by the original before its writes')
                    self.nao_gravadas.add(a + i)
            return int.from_bytes(d[o:o + n], 'little')
        v &= (1 << 8 * n) - 1
        d[o:o + n] = v.to_bytes(n, 'little')
        k[o:o + n] = b'\x01' * n
        return v

    def u8(self, a, v=None):
        return self._acesso(1, a, v)

    def u16(self, a, v=None):
        return self._acesso(2, a, v)

    def u32(self, a, v=None):
        return self._acesso(4, a, v)

    def vista(self, a, n):
        d, _ = self._pedaco(a)
        o = a % self.PEDACO
        if o + n > self.PEDACO:
            raise LeituraNaoGravada(f'0x{a:x}+{n} crosses a chunk')
        return memoryview(d)[o:o + n]

    def ler(self, a, n):
        return bytes(self.vista(a, n))

    def valor(self, a):
        d, _ = self._pedaco(a)
        return d[a % self.PEDACO]

    def final(self):
        """{address: value} of every byte that differs from its entry content."""
        saida = {}
        for c, d in self.dados.items():
            ini = self.inicial[c]
            if d == ini:
                continue
            for b in range(0, self.PEDACO, 4096):
                if d[b:b + 4096] != ini[b:b + 4096]:
                    for o in range(b, b + 4096):
                        if d[o] != ini[o]:
                            saida[c * self.PEDACO + o] = d[o]
        return saida


class ReplayComposto:
    """The original's foreign-call sequence of one recorded call; ``provedores`` serves the names it holds by
    real translations (checked against the original's exit registers), the rest are the original replayed."""

    def __init__(self, resultado, proprias, provedores):
        self.chamadas, self.lojas = resultado['calls'], resultado['stores']
        self.fronteiras = list(resultado.get('boundaries', ()))
        self.proprias, self.provedores = set(proprias), provedores
        self.sequencia = self._fronteira()
        self.i = 0
        self.erros, self.servidas, self.replayed, self.diferencas_saida = [], {}, {}, []
        self.ultimos_incertos = {}

    def _fronteira(self):
        saida, pilha = [], []
        for i, c in enumerate(self.chamadas):
            del pilha[c[0]:]
            if all(self.chamadas[a][1] in self.proprias for a in pilha) and c[1] not in self.proprias:
                saida.append(i)
            pilha.append(i)
        return saida

    def _subarvore(self, i):
        p, fim = self.chamadas[i][0], i + 1
        while fim < len(self.chamadas) and self.chamadas[fim][0] > p:
            fim += 1
        return set(range(i, fim))

    def externo(self, m):
        def f(nome, chamada, regs):
            if self.i >= len(self.sequencia):
                if nome == 'PlaySnd_PostSound' and self.fronteiras:
                    return self._som(nome, chamada, regs)
                self.erros.append(f'extra call {nome} at {chamada:#x}')
                raise ct.DependenciaCicloTrabalho(nome, chamada, 'not in the original call sequence')
            j = self.sequencia[self.i]
            c = self.chamadas[j]
            if c[1] != nome and nome == 'PlaySnd_PostSound' and self.fronteiras:
                return self._som(nome, chamada, regs)
            self.i += 1
            if c[1] != nome:
                self.erros.append(f'call {self.i}: translation {nome} at {chamada:#x}, original {c[1]} from {c[3]}')
                raise ct.DependenciaCicloTrabalho(nome, chamada, 'differs from the original call sequence')
            for k, v in regs.items():
                if not k.startswith('_') and (int(c[2][k], 16) & ct.ARGUMENTOS[nome][k]) != v:
                    self.erros.append(f'{nome} at {chamada:#x}: {k} {v:#x} != original '
                                      f'{int(c[2][k], 16) & ct.ARGUMENTOS[nome][k]:#x}')
            original = {k: int(c[5][k], 16) for k in ct.REG7}
            if nome in self.provedores:
                self.servidas[nome] = self.servidas.get(nome, 0) + 1
                saida = self.provedores[nome](nome, chamada, regs)
                incertos = saida.get('_incertos') or {}
                for k in ct.REG7:
                    if k in saida and (saida[k] ^ original[k]) & M32 & ~incertos.get(k, 0):
                        # Diagnostic only: Economy passes the argument bits it models, so a callee that keeps an
                        # unpassed upper half differs there; the call's own outcome is the criterion.
                        self.diferencas_saida.append(f'{nome} at {chamada:#x}: exit {k} {saida[k]:#x} '
                                                     f'(original {original[k]:#x})')
                self.ultimos_incertos = dict(incertos)
                return {k: saida[k] & M32 for k in ct.REG7 if k in saida}
            self.replayed[nome] = self.replayed.get(nome, 0) + 1
            arvore = self._subarvore(j)
            for loja in self.lojas:
                if loja[5] in arvore:
                    endereco, tamanho, valor = int(loja[2], 16), loja[3], int(loja[4], 16)
                    for b in range(tamanho):
                        m.u8(endereco + b, (valor >> (8 * b)) & 0xff)
            return original
        return f

    def _som(self, nome, chamada, regs):
        fr = self.fronteiras.pop(0)
        self.replayed[nome] = self.replayed.get(nome, 0) + 1
        r = {k: int(v, 16) for k, v in fr['registers'].items()}
        return dict(r, ESI=0, EDI=0, EBP=0)


def provedores(m):
    """The real providers over memory ``m``, by callee name, each ``f(nome, chamada, regs) -> regs``."""
    from bonus_unidades import BonusUnidades
    from caverna_recrutamento import CavernaRecrutamento, provedor_caverna
    from entrada_estruturas import EntradaEstruturas, ROTINAS_ECONOMIA, provedor_entrada
    from visao_grupos import VisaoGrupos, provedor_saida
    bonus = BonusUnidades.da_memoria(m)

    def sem_provedor(nome, chamada, regs):
        raise ct.DependenciaCicloTrabalho(nome, chamada, 'no provider (composition)')

    entrada = EntradaEstruturas(m, externo=sem_provedor, som=None,
                                bonus=lambda jogador, tipo, seletor: bonus.consultar(jogador, tipo, seletor))
    core = provedor_entrada(entrada)
    # The cave/recruitment routines reach Core's exit position (CalculPosition, RechercheDecalageSortie) through
    # ``visao_grupos.provedor_saida`` and every other Core callee through ``provedor_entrada``.
    caverna = provedor_caverna(CavernaRecrutamento(m, externo=provedor_saida(VisaoGrupos(m),
                                                                             outros=provedor_entrada(entrada))))

    def bonus_get_val(nome, chamada, regs):
        return dict(EAX=bonus.consultar(regs['EAX'] & 0xff, regs['EBX'] & 0xff, regs['EDX'] & 0xff))

    saida = {n: core for n in ROTINAS_ECONOMIA}
    saida.update(BatimentHabitable=caverna, InitBatimentPlayer=caverna, BonusGetValEngin=bonus_get_val)
    return saida


_BASE = {}


def base_pedacos(caminho):
    """16 MiB chunks (poison-filled) of the base image written by ``imagem_base_ciclo.py``."""
    if caminho not in _BASE:
        import lzma
        import pickle
        dados = pickle.loads(lzma.decompress(Path(caminho).read_bytes()))
        pedacos = {}
        P = MemoriaComposta.PEDACO
        for base, d in dados['blocks'].values():
            a = 0
            while a < len(d):
                c, o = (base + a) // P, (base + a) % P
                n = min(len(d) - a, P - o)
                if c not in pedacos:
                    pedacos[c] = bytearray([VENENO]) * P
                pedacos[c][o:o + n] = d[a:a + n]
                a += n
        _BASE[caminho] = {c: bytes(v) for c, v in pedacos.items()}
    return _BASE[caminho]


def compor_chamada(r, estrito=False, base=None):
    m = MemoriaComposta(r['read_before_write'], estrito, base_pedacos(base) if base else None)
    rp = ReplayComposto(r, set(ct.ROTINAS) | set(ct.INTERNAS), provedores(m))
    ciclo = ct.CicloTrabalho(m, externo=rp.externo(m))
    regs = {k: int(v, 16) for k, v in r['entry_registers'].items()}
    d = dict(routine=r['routine'], frame=r['frame'], arg=hex(regs['EAX'] & 0xffff))
    try:
        saida = getattr(ciclo, '_' + r['routine'])(regs)
    except ct.ForaDoDominioTrabalho as e:
        return 'outside_domain', dict(d, address=hex(e.endereco)), rp
    except Exception as e:  # noqa: BLE001  (every other failure is reported, never hidden)
        return 'error', dict(d, error=repr(e), replay=rp.erros[:5]), rp
    esperado = {k: int(r['exit_registers'][k], 16) for k in ct.REG7 + ('ESP',)}
    incertos = saida.get('_incertos', {})
    regs_dif = {k: [hex(saida[k]), hex(v)] for k, v in esperado.items() if (saida[k] ^ v) & ~incertos.get(k, 0)}
    final = {int(a, 16): novo for a, _v, novo in r['changed_bytes']}
    atual = m.final()
    bytes_dif = [hex(a) for a, v in final.items() if m.valor(a) != v]
    # A byte written but not changed by the original must hold the original's last stored value there.
    lojas = {}
    for loja in r['stores']:
        endereco, tamanho, valor = int(loja[2], 16), loja[3], int(loja[4], 16)
        for b in range(tamanho):
            lojas[endereco + b] = (valor >> (8 * b)) & 0xff
    bytes_dif += [hex(a) for a, v in atual.items() if a not in final and lojas.get(a, m.original.get(a, -1)) != v]
    sobras = len(rp.sequencia) - rp.i
    # ``ciclo_trabalho`` returns a callee's EAX as its own (DeplaceEngin's in a walk); Core marks the bits of that
    # EAX it does not reconstruct. A difference confined to them is reported apart, not as a match.
    if (regs_dif and set(regs_dif) == {'EAX'} and not bytes_dif and not rp.erros and not sobras
            and not ((saida['EAX'] ^ esperado['EAX']) & ~rp.ultimos_incertos.get('EAX', 0))):
        return 'uncertain_register', dict(d, registers=regs_dif, uncertain_eax=hex(rp.ultimos_incertos['EAX'])), rp
    if regs_dif or bytes_dif or rp.erros or sobras:
        return 'mismatch', dict(d, registers=regs_dif, bytes=sorted(bytes_dif)[:20], n_bytes=len(bytes_dif),
                                replay=rp.erros[:10], unconsumed=sobras, callee_exit_differences=rp.diferencas_saida[:10],
                                unrecorded_bytes_read=len(m.nao_gravadas)), rp
    return 'match', dict(d, callee_exit_differences=len(rp.diferencas_saida), unrecorded_bytes_read=len(m.nao_gravadas)), rp


def compor(captura=None, estrito=False, base=None):
    captura = captura or carregar(CAPTURA)[0]
    contagem, falhas, servidas, replayed = {}, [], {}, {}
    for r in captura['calls']:
        if r['routine'] not in TRADUZIDAS:
            continue
        resultado, d, rp = compor_chamada(r, estrito, base)
        c = contagem.setdefault(r['routine'], dict(match=0, uncertain_register=0, mismatch=0, outside_domain=0, error=0))
        c[resultado] += 1
        for k, v in rp.servidas.items():
            servidas[k] = servidas.get(k, 0) + v
        for k, v in rp.replayed.items():
            replayed[k] = replayed.get(k, 0) + v
        if resultado != 'match':
            falhas.append(dict(d, outcome=resultado))
    return dict(counts=contagem, served_by_translation=servidas, replayed_original=replayed, failures=falhas)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida')
    ap.add_argument('--estrito', action='store_true')
    ap.add_argument('--base', help='base image from imagem_base_ciclo.py (bytes no recorded call read)')
    a = ap.parse_args()
    rel = compor(estrito=a.estrito, base=a.base and str(RAIZ / a.base))
    texto = json.dumps(rel, indent=1, sort_keys=True)
    if a.saida:
        Path(RAIZ / a.saida).write_text(texto + '\n')
    print(json.dumps({k: rel[k] for k in ('counts', 'served_by_translation', 'replayed_original')}, indent=1))
    for f in rel['failures'][:20]:
        print(json.dumps(f))
