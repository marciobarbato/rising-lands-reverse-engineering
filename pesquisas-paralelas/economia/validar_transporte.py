"""Native differential of ``transporte`` (and of the state-19 body's saved-state checks) against the original.

Reruns the committed transport capture natively (``capturar_transporte.executar``: same declared actions, same recorded
calls). At every recorded CalculTransporteEngin and CalculDechargeCaveEngin call, and at every state-19 body
``EnginNextEtape:19`` (``alimentacao`` composed with ``restauracao``'s EnginRestaureEtat/BatimentEnleveMatiere, as in
``validar_restauracao``), the translation runs over a copy of the exact entry state (every mapped block) and is
compared with what the original did:
- exit registers EAX..EBP and ESP (bits a provider marks uncertain excluded);
- every byte of every mapped block afterwards (the original's: entry state + its changed bytes);
- in order, each call into another front, by name and by the argument bits ``transporte.ARGUMENTOS`` names (every
  register is passed), and each frame boundary by its argument registers.
Economy's own callees (TerrainRetireMatiere, TestRessource, BatimentEnleveMatiere, BatimentAjouteMatiere and
EnginCalculTransporte) are computed in-process by their translations. A callee owned elsewhere is the original's own
call replayed (its stores applied in order, its exit registers returned), except ChercheVegetLibre, served by Core's
``fadiga_vegetacao.provedor_fadiga`` unless ``--sem-core``. The rerun must also equal the committed capture.

    python3 "…/heavy_lease.py" economy -- python3 -B pesquisas-paralelas/economia/validar_transporte.py \\
        --captura pesquisas-paralelas/economia/evidencias/transporte/captura-transporte.json.xz \\
        --saida pesquisas-paralelas/economia/validacao-transporte-emulada.json
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
import transporte as tr  # noqa: E402
import validar_restauracao as vr  # noqa: E402
from validar_caverna_recrutamento import Replay as ReplayBase  # noqa: E402
from validar_ciclo_trabalho import carregar  # noqa: E402

M32 = 0xffffffff
REG7 = tr.REG7
DIRETAS = ('CalculTransporteEngin', 'CalculDechargeCaveEngin')
TRADUZIDAS = DIRETAS + ('EnginNextEtape:19',)
CAPTURA = PASTA / 'evidencias/transporte/captura-transporte.json.xz'
ERROS = vr.ERROS + (tr.DependenciaTransporte,)


def proprias():
    return set(tr.ROTINAS) | set(tr.PROPRIAS_ECONOMIA) | set(tr.INTERNAS)


class Replay(ReplayBase):
    def __init__(self, resultado, provedores=None):
        super().__init__(resultado, proprias(), argumentos=tr.ARGUMENTOS, erro=tr.DependenciaTransporte,
                         provedores=provedores)


def executar_traducao(nome, m, resultado, provedores=None):
    """(translation output, replay) of one recorded call over memory ``m``."""
    if nome == 'EnginNextEtape:19':
        return vr.executar_traducao(nome, m, resultado, provedores)
    regs = {k: int(resultado['entry_registers'][k], 16) for k in REG7 + ('ESP',)}
    rp = Replay(resultado, provedores)
    return tr.Transporte(m, externo=rp(m)).chamar(nome, regs), rp


def comparar(nome, regs, antes, resultado, provedores=None):
    """(outcome, detail) of the translation of one recorded call over a copy of its entry state."""
    from memoria_quadro_core import MemoriaQuadro
    buffers = {n: (base, bytearray(d)) for n, (base, d) in antes.items() if n != 'native_stack'}
    m = MemoriaQuadro([(base, buf) for base, buf in buffers.values()])
    detalhe = dict(routine=nome, frame=resultado['frame'], action=resultado.get('action'), eax=hex(regs['EAX']))
    try:
        saida, rp = executar_traducao(nome, m, resultado, provedores)
    except al.ForaDoDominioFome as e:
        return 'outside_domain', dict(detalhe, address=hex(e.endereco), reason=str(e))
    except ERROS as e:
        return 'error', dict(detalhe, error=repr(e))
    regs_dif, incertos = vr.comparar_saida(saida, resultado)
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
    sobras = len(rp.sequencia) - rp.i
    fronteiras = len(getattr(rp, 'fronteiras', ()))
    ok = not regs_dif and not bytes_dif and not rp.erros and sobras == 0 and not fronteiras
    detalhe.update(changed_bytes=len(resultado['changed_bytes']), foreign_calls=rp.i)
    if rp.servidas:
        detalhe['served_by_translation'] = dict(rp.servidas)
    if incertos:
        detalhe['uncertain'] = {k: hex(v) for k, v in incertos.items()}
    if not ok:
        detalhe.update(registers=regs_dif, bytes=bytes_dif, replay_errors=rp.erros, unconsumed_calls=sobras,
                       unconsumed_boundaries=fronteiras, exit_registers=resultado['exit_registers'])
    return ('match' if ok else 'mismatch'), detalhe


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--captura', required=True)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--sem-core', action='store_true',
                    help="replay the original's ChercheVegetLibre instead of Core's provedor_fadiga")
    a = ap.parse_args()
    from validar_alimentacao import provedores_fadiga
    provedores = None if a.sem_core else provedores_fadiga()
    captura, sha = carregar(RAIZ / a.captura)
    import capturar_transporte as ct
    relatorio = dict(schema='rising-lands/economy-transport-validation/1', capture=a.captura, capture_raw_sha256=sha,
                     translation={p: hashlib.sha256((PASTA / p).read_bytes()).hexdigest()
                                  for p in ('transporte.py', 'alimentacao.py', 'restauracao.py', 'ciclo_trabalho.py',
                                            'ordens_economia.py')},
                     core_fatigue_provider=None if provedores is None else
                         'fadiga_vegetacao.provedor_fadiga',
                     results=[], counts={}, served_by_translation={})
    gravadas = []

    def observador(nome, regs, antes, resultado):
        gravadas.append(resultado)
        if nome not in TRADUZIDAS:
            return
        saida, detalhe = comparar(nome, regs, antes, resultado, provedores)
        detalhe['outcome'] = saida
        for k, v in detalhe.get('served_by_translation', {}).items():
            relatorio['served_by_translation'][k] = relatorio['served_by_translation'].get(k, 0) + v
        relatorio['results'].append(detalhe)
        c = relatorio['counts'].setdefault(nome, dict(match=0, mismatch=0, outside_domain=0, error=0))
        c[saida] += 1

    c, estado, segundos = ct.executar(captura['last_counter'], observador=observador)
    chaves = ('routine', 'frame', 'entry_registers', 'exit_registers', 'changed_bytes', 'calls', 'stores')
    iguais = len(gravadas) == len(captura['calls']) and all(
        json.loads(json.dumps({k: g[k] for k in chaves})) == {k: o[k] for k in chaves}
        for g, o in zip(gravadas, captura['calls']))
    contar = lambda o: sum(1 for r in relatorio['results'] if r['outcome'] == o)  # noqa: E731
    relatorio.update(seconds=segundos, reproduction=c.reproducao, rerun_equals_capture=iguais,
                     recorded_calls=len(gravadas), compared=len(relatorio['results']), mismatches=contar('mismatch'),
                     errors=contar('error'), outside_domain=contar('outside_domain'))
    Path(RAIZ / a.saida).write_text(json.dumps(relatorio, indent=1, sort_keys=True) + '\n')
    print(json.dumps({k: relatorio[k] for k in ('counts', 'compared', 'mismatches', 'errors', 'outside_domain',
                                                'rerun_equals_capture', 'recorded_calls', 'served_by_translation',
                                                'seconds')}, indent=1), flush=True)
    from encerramento_captura import encerrar_captura
    ok = relatorio['mismatches'] == relatorio['errors'] == relatorio['outside_domain'] == 0 and iguais
    encerrar_captura(0 if ok else 1, RAIZ / a.saida)


if __name__ == '__main__':
    main()
