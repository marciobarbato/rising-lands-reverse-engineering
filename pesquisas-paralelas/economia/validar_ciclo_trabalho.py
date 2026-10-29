"""Native differential of ``ciclo_trabalho`` against the original work, deposit and lodging calls.

Reruns the committed capture natively (``capturar_ciclo_trabalho.executar``: same declared actions, same
recorded calls). At every recorded call of a translated routine the translation runs over a copy of the
exact entry state (every mapped block), and is compared with what the original did:
- exit registers EAX..EBP and ESP;
- every byte of every mapped block afterwards (the original's: entry state + its changed bytes);
- in order, each call into another front, by name and by the argument bits the callee reads.
A callee owned elsewhere is the original's own call replayed: its name and arguments are checked, then its
stores are applied in order and its exit registers returned (validation scaffolding, not a translation).
The rerun must also equal the committed capture call for call.

    python3 "…/heavy_lease.py" economy -- python3 -B pesquisas-paralelas/economia/validar_ciclo_trabalho.py \
        --captura pesquisas-paralelas/economia/evidencias/ciclo-trabalho/captura-ciclo-trabalho-exibicao.json.xz \
        --saida pesquisas-paralelas/economia/validacao-ciclo-trabalho-emulada.json
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import ciclo_trabalho as ct  # noqa: E402

TRADUZIDAS = ('CalculWorkEngin', 'BatimentLogeEngin', 'BatimentAjouteMatiere', 'TerrainRecolte', 'MineRecolte',
              'MineSetWork', 'MineEndWork')
REG7 = ct.REG7


def carregar(caminho):
    bruto = Path(caminho).read_bytes()
    if str(caminho).endswith('.xz'):
        bruto = lzma.decompress(bruto)
    return json.loads(bruto), hashlib.sha256(bruto).hexdigest()


class Replay:
    """``externo`` serving another front's callee from the original's own nested call."""

    def __init__(self, resultado, proprias):
        self.chamadas = resultado['calls']
        self.lojas = resultado['stores']
        self.fronteiras = list(resultado.get('boundaries', ()))
        self.proprias = set(proprias)
        self.sequencia = self._fronteira()
        self.i = 0
        self.erros = []

    def _fronteira(self):
        """Indices of calls whose ancestors are all translated routines (or the top) and which are not."""
        saida, pilha = [], []
        for i, c in enumerate(self.chamadas):
            p = c[0]
            del pilha[p:]
            if all(self.chamadas[a][1] in self.proprias for a in pilha) and c[1] not in self.proprias:
                saida.append(i)
            pilha.append(i)
        return saida

    def _subarvore(self, i):
        p = self.chamadas[i][0]
        fim = i + 1
        while fim < len(self.chamadas) and self.chamadas[fim][0] > p:
            fim += 1
        return set(range(i, fim))

    def __call__(self, m):
        def externo(nome, chamada, regs):
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
                if k.startswith('_'):
                    continue
                largura = ct.ARGUMENTOS[nome][k]
                if (int(c[2][k], 16) & largura) != v:
                    self.erros.append(f'{nome} at {chamada:#x}: {k} {v:#x} != original {int(c[2][k], 16) & largura:#x}')
            arvore = self._subarvore(j)
            for loja in self.lojas:
                if loja[5] in arvore:
                    endereco, tamanho, valor = int(loja[2], 16), loja[3], int(loja[4], 16)
                    for b in range(tamanho):
                        m.u8(endereco + b, (valor >> (8 * b)) & 0xff)
            return {k: int(c[5][k], 16) for k in REG7}
        return externo

    def _som(self, nome, chamada, regs):
        f = self.fronteiras.pop(0)
        if f['routine'] != nome:
            self.erros.append(f'boundary {f["routine"]} != {nome}')
        r = {k: int(v, 16) for k, v in f['registers'].items()}
        for k in ('EAX', 'EDX', 'EBX', 'ECX'):
            if k in regs and (r[k] & ct.ARGUMENTOS[nome][k]) != regs[k]:
                self.erros.append(f'{nome} at {chamada:#x}: {k} {regs[k]:#x} != original {r[k]:#x}')
        return dict(r, ESI=0, EDI=0, EBP=0)


def comparar(nome, regs, antes, resultado):
    """(ok, detail) of the translation of one recorded call over a copy of its entry state."""
    from memoria_quadro_core import MemoriaQuadro
    buffers = {n: (base, bytearray(d)) for n, (base, d) in antes.items() if n != 'native_stack'}
    m = MemoriaQuadro([(base, buf) for base, buf in buffers.values()])
    replay = Replay(resultado, set(ct.ROTINAS) | set(ct.INTERNAS))
    ciclo = ct.CicloTrabalho(m, externo=replay(m))
    entrada = {k: regs[k] & 0xffffffff for k in REG7 + ('ESP',)}
    detalhe = dict(routine=nome, frame=resultado['frame'], unit_or_cell=hex(regs['EAX'] & 0xffff))
    try:
        saida = getattr(ciclo, '_' + nome)(entrada)
    except ct.ForaDoDominioTrabalho as e:
        detalhe.update(outcome='outside_domain', address=hex(e.endereco), reason=str(e))
        return False, detalhe
    except (ct.DependenciaCicloTrabalho, KeyError, ValueError) as e:
        detalhe.update(outcome='error', error=repr(e), replay_errors=replay.erros)
        return False, detalhe
    esperado = {k: int(resultado['exit_registers'][k], 16) for k in REG7 + ('ESP',)}
    mascara = {k: 0xffffffff & ~saida.get('_incertos', {}).get(k, 0) for k in esperado}
    regs_dif = {k: [hex(saida[k]), hex(esperado[k])] for k in esperado if (saida[k] ^ esperado[k]) & mascara[k]}
    nativo = {n: bytearray(d) for n, (_, d) in antes.items() if n != 'native_stack'}
    bases = {n: base for n, (base, _) in antes.items()}
    indice = sorted((base, n) for n, base in bases.items() if n != 'native_stack')
    import bisect
    chaves = [b for b, _ in indice]
    for endereco, _velho, novo in resultado['changed_bytes']:
        a = int(endereco, 16)
        k = bisect.bisect_right(chaves, a) - 1
        n = indice[k][1]
        nativo[n][a - bases[n]] = novo
    bytes_dif = []
    for n, buf in buffers.items():
        b = buf[1]
        if b != nativo[n]:
            bytes_dif += [hex(buf[0] + i) for i in range(len(b)) if b[i] != nativo[n][i]][:20]
    sobras = len(replay.sequencia) - replay.i
    ok = not regs_dif and not bytes_dif and not replay.erros and sobras == 0
    detalhe.update(outcome='match' if ok else 'mismatch', changed_bytes=len(resultado['changed_bytes']),
                   foreign_calls=replay.i)
    if not ok:
        detalhe.update(registers=regs_dif, bytes=bytes_dif, replay_errors=replay.erros, unconsumed_calls=sobras,
                       exit_registers=resultado['exit_registers'])
    return ok, detalhe


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--captura', required=True)
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    captura, sha = carregar(RAIZ / a.captura)
    import capturar_ciclo_trabalho as cct
    relatorio = dict(schema='rising-lands/economy-work-cycle-validation/1', capture=a.captura, capture_raw_sha256=sha,
                     translation=hashlib.sha256((PASTA / 'ciclo_trabalho.py').read_bytes()).hexdigest(),
                     results=[], counts={})
    gravadas = []

    def observador(nome, regs, antes, resultado):
        gravadas.append(resultado)
        if nome not in TRADUZIDAS:
            return
        ok, detalhe = comparar(nome, regs, antes, resultado)
        relatorio['results'].append(detalhe)
        c = relatorio['counts'].setdefault(nome, dict(match=0, mismatch=0, outside_domain=0, error=0))
        c[detalhe['outcome']] += 1

    c, estado, segundos = cct.executar(captura['last_counter'], observador=observador)
    # The native rerun must equal the committed capture, call for call.
    chaves = ('routine', 'frame', 'entry_registers', 'exit_registers', 'changed_bytes', 'calls', 'stores')
    iguais = len(gravadas) == len(captura['calls']) and all(
        json.loads(json.dumps({k: g[k] for k in chaves})) == {k: o[k] for k in chaves}
        for g, o in zip(gravadas, captura['calls']))
    relatorio.update(seconds=segundos, reproduction=c.reproducao, rerun_equals_capture=iguais,
                     recorded_calls=len(gravadas),
                     compared=len(relatorio['results']),
                     mismatches=sum(1 for r in relatorio['results'] if r['outcome'] != 'match'))
    Path(RAIZ / a.saida).write_text(json.dumps(relatorio, indent=1, sort_keys=True) + '\n')
    print(json.dumps({k: relatorio[k] for k in ('counts', 'compared', 'mismatches', 'rerun_equals_capture',
                                                'recorded_calls', 'seconds')}, indent=1), flush=True)
    from encerramento_captura import encerrar_captura
    encerrar_captura(0 if relatorio['mismatches'] == 0 and iguais else 1, RAIZ / a.saida)


if __name__ == '__main__':
    main()
