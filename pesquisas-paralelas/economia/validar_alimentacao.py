"""Native differential of ``alimentacao`` against the original state-19 (hunger) body.

Reruns the committed capture natively (``capturar_alimentacao.executar``: same declared actions, same recorded
calls). At every recorded ``EnginNextEtape:19`` call the translation runs over a copy of the exact entry state
(every mapped block) and is compared with what the original did:
- exit registers EAX..EBP and ESP (bits a provider marks uncertain excluded);
- every byte of every mapped block afterwards (the original's: entry state + its changed bytes);
- in order, each call into another front, by name and by the argument bits the callee reads, and each frame
  boundary (PlaySnd_PostSound) by its argument registers.
A callee owned elsewhere is the original's own call replayed: its stores are applied in order and its exit
registers returned; a frame boundary returns its declared EAX with every other register unchanged (the bench's
rule). This is validation scaffolding, not a translation. The rerun must also equal the committed capture call for
call.

    python3 "…/heavy_lease.py" economy -- python3 -B pesquisas-paralelas/economia/validar_alimentacao.py \\
        --captura pesquisas-paralelas/economia/evidencias/alimentacao/captura-alimentacao-exibicao.json.xz \\
        --saida pesquisas-paralelas/economia/validacao-alimentacao-emulada.json
"""
import argparse
import bisect
import hashlib
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import alimentacao as al  # noqa: E402
from validar_caverna_recrutamento import Replay as ReplayBase  # noqa: E402
from validar_ciclo_trabalho import carregar  # noqa: E402

TRADUZIDAS = ('EnginNextEtape:19',)
REG7 = al.REG7
CAPTURA = PASTA / 'evidencias/alimentacao/captura-alimentacao-exibicao.json.xz'
FRONTEIRAS = ('PlaySnd_PostSound',)


class Replay(ReplayBase):
    """The cave replay plus frame boundaries, served from the recorded ``boundaries`` in order."""

    def __init__(self, resultado, proprias, provedores=None):
        super().__init__(resultado, proprias, argumentos=al.ARGUMENTOS, erro=al.DependenciaFome, provedores=provedores)
        self.fronteiras = list(resultado.get('boundaries', ()))

    def __call__(self, m):
        base = super().__call__(m)

        def externo(nome, chamada, regs):
            if nome in FRONTEIRAS:
                return self._fronteira_som(nome, chamada, regs)
            return base(nome, chamada, regs)
        return externo

    def _fronteira_som(self, nome, chamada, regs):
        # The recorder also lists the boundary among the nested calls: consume it there in order.
        if self.i < len(self.sequencia) and self.chamadas[self.sequencia[self.i]][1] == nome:
            self.i += 1
        else:
            self.erros.append(f'boundary {nome} at {chamada:#x} is not the next recorded call')
        if not self.fronteiras:
            self.erros.append(f'extra boundary {nome} at {chamada:#x}')
            raise al.DependenciaFome(nome, chamada, 'not in the original boundary sequence')
        f = self.fronteiras.pop(0)
        if f['routine'] != nome:
            self.erros.append(f'boundary {f["routine"]} != {nome}')
        r = {k: int(v, 16) for k, v in f['registers'].items()}
        for k in ('EAX', 'EDX', 'EBX', 'ECX'):
            if k in regs and (r[k] ^ regs[k]) & al.ARGUMENTOS[nome][k]:
                self.erros.append(f'{nome} at {chamada:#x}: {k} {regs[k]:#x} != original {r[k]:#x}')
        pilha = [int(x, 16) for x in f.get('stack_words', ())]
        if regs.get('_pilha') and pilha[:len(regs['_pilha'])] != list(regs['_pilha']):
            self.erros.append(f'{nome} at {chamada:#x}: pushed {regs["_pilha"]} != original {pilha[:1]}')
        return {} if f.get('declared_eax') is None else {'EAX': f['declared_eax'] & 0xffffffff}


def provedores_fadiga():
    """Core's ``fadiga_vegetacao.provedor_fadiga`` by callee name, a factory over the call's memory: ChercheVegetLibre
    (the state-19 body's new search, 0x455756)."""
    from fadiga_vegetacao import FadigaVegetacao, provedor_fadiga

    def fabrica(m):
        return provedor_fadiga(FadigaVegetacao(m))
    return {'ChercheVegetLibre': fabrica}


def proprias():
    return set(al.ROTINAS) | set(al.INTERNAS)


def comparar_saida(saida, resultado):
    esperado = {k: int(resultado['exit_registers'][k], 16) for k in REG7 + ('ESP',)}
    incertos = saida.get('_incertos', {})
    return {k: [hex(saida[k]), hex(v)] for k, v in esperado.items()
            if (saida[k] ^ v) & 0xffffffff & ~incertos.get(k, 0)}, incertos


def comparar(nome, regs, antes, resultado, provedores=None):
    """(ok, detail) of the translation of one recorded call over a copy of its entry state (``provedores``: callee
    name -> a Core provider factory serving that callee instead of the original's replayed call)."""
    from memoria_quadro_core import MemoriaQuadro
    buffers = {n: (base, bytearray(d)) for n, (base, d) in antes.items() if n != 'native_stack'}
    m = MemoriaQuadro([(base, buf) for base, buf in buffers.values()])
    replay = Replay(resultado, proprias(), provedores)
    fome = al.Alimentacao(m, externo=replay(m))
    entrada = {k: regs[k] & 0xffffffff for k in REG7 + ('ESP',)}
    detalhe = dict(routine=nome, frame=resultado['frame'], unit=hex(regs['EDI'] & 0xffff))
    try:
        saida = fome.chamar(nome, entrada)
    except al.ForaDoDominioFome as e:
        detalhe.update(outcome='outside_domain', address=hex(e.endereco), reason=str(e))
        return False, detalhe
    except (al.DependenciaFome, KeyError, ValueError) as e:
        detalhe.update(outcome='error', error=repr(e), replay_errors=replay.erros)
        return False, detalhe
    regs_dif, incertos = comparar_saida(saida, resultado)
    nativo = {n: bytearray(d) for n, (_, d) in antes.items() if n != 'native_stack'}
    bases = {n: base for n, (base, _) in antes.items()}
    indice = sorted((base, n) for n, base in bases.items() if n != 'native_stack')
    chaves = [b for b, _ in indice]
    for endereco, _velho, novo in resultado['changed_bytes']:
        a = int(endereco, 16)
        n = indice[bisect.bisect_right(chaves, a) - 1][1]
        nativo[n][a - bases[n]] = novo
    bytes_dif = []
    for n, buf in buffers.items():
        if buf[1] != nativo[n]:
            bytes_dif += [hex(buf[0] + i) for i in range(len(buf[1])) if buf[1][i] != nativo[n][i]][:20]
    sobras = len(replay.sequencia) - replay.i
    ok = not regs_dif and not bytes_dif and not replay.erros and sobras == 0 and not replay.fronteiras
    detalhe.update(outcome='match' if ok else 'mismatch', changed_bytes=len(resultado['changed_bytes']),
                   foreign_calls=replay.i, boundaries=len(resultado.get('boundaries', ())))
    if replay.servidas:
        detalhe['served_by_translation'] = dict(replay.servidas)
    if incertos:
        detalhe['uncertain'] = {k: hex(v) for k, v in incertos.items()}
    if not ok:
        detalhe.update(registers=regs_dif, bytes=bytes_dif, replay_errors=replay.erros, unconsumed_calls=sobras,
                       unconsumed_boundaries=len(replay.fronteiras), exit_registers=resultado['exit_registers'])
    return ok, detalhe


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--captura', required=True)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--sem-core', action='store_true',
                    help="replay the original's ChercheVegetLibre instead of Core's provedor_fadiga")
    a = ap.parse_args()
    captura, sha = carregar(RAIZ / a.captura)
    import capturar_alimentacao as cal
    provedores = None if a.sem_core else provedores_fadiga()
    relatorio = dict(schema='rising-lands/economy-hunger-validation/1', capture=a.captura, capture_raw_sha256=sha,
                     translation=hashlib.sha256((PASTA / 'alimentacao.py').read_bytes()).hexdigest(),
                     core_fatigue_provider=None if provedores is None else
                         'fadiga_vegetacao.provedor_fadiga',
                     results=[], counts={}, served_by_translation={})
    gravadas = []

    def observador(nome, regs, antes, resultado):
        gravadas.append(resultado)
        if nome not in TRADUZIDAS:
            return
        ok, detalhe = comparar(nome, regs, antes, resultado, provedores)
        relatorio['results'].append(detalhe)
        for k, v in detalhe.get('served_by_translation', {}).items():
            relatorio['served_by_translation'][k] = relatorio['served_by_translation'].get(k, 0) + v
        c = relatorio['counts'].setdefault(nome, dict(match=0, mismatch=0, outside_domain=0, error=0))
        c[detalhe['outcome']] += 1

    c, estado, segundos = cal.executar(captura['last_counter'], observador=observador)
    chaves = ('routine', 'frame', 'entry_registers', 'exit_registers', 'changed_bytes', 'calls', 'stores')
    iguais = len(gravadas) == len(captura['calls']) and all(
        json.loads(json.dumps({k: g[k] for k in chaves})) == {k: o[k] for k in chaves}
        for g, o in zip(gravadas, captura['calls']))
    relatorio.update(seconds=segundos, reproduction=c.reproducao, rerun_equals_capture=iguais,
                     recorded_calls=len(gravadas), compared=len(relatorio['results']),
                     mismatches=sum(1 for r in relatorio['results'] if r['outcome'] == 'mismatch'),
                     errors=sum(1 for r in relatorio['results'] if r['outcome'] == 'error'),
                     outside_domain=sum(1 for r in relatorio['results'] if r['outcome'] == 'outside_domain'))
    Path(RAIZ / a.saida).write_text(json.dumps(relatorio, indent=1, sort_keys=True) + '\n')
    print(json.dumps({k: relatorio[k] for k in ('counts', 'compared', 'mismatches', 'errors', 'outside_domain',
                                                'rerun_equals_capture', 'recorded_calls', 'served_by_translation',
                                                'seconds')}, indent=1),
          flush=True)
    from encerramento_captura import encerrar_captura
    encerrar_captura(0 if relatorio['mismatches'] == relatorio['errors'] == 0 and iguais else 1, RAIZ / a.saida)


if __name__ == '__main__':
    main()
