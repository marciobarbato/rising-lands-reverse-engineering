"""Native differential of Core's world-model movement code at the real raid states (M2.3, counters 9000..).

Reruns ``capturar_movimento_incursao`` (Combat's forced-counter v1 method, Missions' read-only
Isolamento on the Core routines). For a sample of the isolated calls of every mapped routine,
Core's existing world model is bound over the exact saved entry blocks. The binding is Missions'
``ligacao_provedores_m1.montar_provedores`` over a ``MapaMemoriaM1``, the same composition AI/runtime
uses. The matching world method or function runs, the map is serialized, and its changed bytes
(stack excluded) and its primary return value are compared with the original's isolated result.

The mapping is ``ADAPTADORES``. Exceptions are recorded and never ignored:
- a ``NotImplementedError`` (including ``DependenciaRamoCore`` and Missions' ``AtributoNaoMapeadoM1``)
  is a dependency stop;
- any other exception is a mismatch.
Routines with a flat translation (``incursao_core.traducao_core``) are also compared, with
registers EAX..EBP, over copies of the same entry blocks. Routines with neither are listed as gaps.
The world adapters also run on ``mundo_vivo.mundo_vivo`` (the world bound live to a flat memory)
over copies of the entry blocks, and are compared in the same way.

    python3 -B ferramentas/validar_movimento_incursao.py --quadros 12 --por-rotina 4
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
M32 = 0xffffffff
LISTA = 2048   # changed bytes kept per mismatch
JANELA_BUSCA = 9170   # every call is compared from this counter on (path search at 9176..9179)
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')


def _adaptadores():
    from movimento import celula_vizinha, direcao_entre_celulas, distancia_quadratica
    from passagem_unidades import consultar_passagem, ocupa_celula, procurar_ocupante
    u16 = lambda r, k: r[k] & 0xffff
    # name -> f(world, entry registers) -> {register part: value} compared with the native exit
    return {
        'EnginEstVivant': lambda w, r: dict(AL=int(w.viva(u16(r, 'EAX')))),
        'ResetOrdre': lambda w, r: w.redefinir_ordem(u16(r, 'EAX')) or {},
        'SetDeplaceEngin': lambda w, r: w.definir_movimento(u16(r, 'EAX'), u16(r, 'EDX')) or {},
        'RotateEngin': lambda w, r: w.girar(u16(r, 'EAX')) or {},
        'SetEnginCollision': lambda w, r: w.ocupar(u16(r, 'EAX'), u16(r, 'EDX'), True) or {},
        'ResetEnginCollision': lambda w, r: w.ocupar(u16(r, 'EAX'), u16(r, 'EDX'), False) or {},
        'EnginOccupeCase': lambda w, r: dict(AL=int(ocupa_celula(w, u16(r, 'EAX'), u16(r, 'EDX'), r['EBX'] & 0xff))),
        'EnginPeutPasser': lambda w, r: dict(AL=int(consultar_passagem(w, u16(r, 'EAX'), u16(r, 'EDX'),
                                                                       r['EBX'] & 0xff)[0])),
        'ChercheIndiceEngin': lambda w, r: dict(AX=procurar_ocupante(w, u16(r, 'EAX'))),
        'CalculDirection': lambda w, r: dict(AL=direcao_entre_celulas(u16(r, 'EAX'), u16(r, 'EDX'))),
        'CalculDirCase': lambda w, r: dict(AX=celula_vizinha(u16(r, 'EAX'), r['EDX'] & 0xff, w.largura, w.altura)),
        'Distance2d': lambda w, r: dict(EAX=distancia_quadratica(r['EAX'], r['EDX'], r['EBX'], r['ECX'])),
        'EnginNextCase': lambda w, r: w.escolher_direto(u16(r, 'EAX')) and {},
        'EnginNextCaseChemin': lambda w, r: w.escolher_da_rota(u16(r, 'EAX')) and {},
        'AvanceEngin': lambda w, r: w.avancar_passo(u16(r, 'EAX')) and {},
        'CalculNextCase': lambda w, r: w.calcular_proxima_celula(u16(r, 'EAX')) or {},
        'DeplaceEngin': lambda w, r: w.deslocar(u16(r, 'EAX')) or {},
    }


PARTES = dict(AL=(0xff, 0), AX=(0xffff, 0), EAX=(M32, 0))


def main():
    import capturar_movimento_incursao as cm
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    sys.path.insert(0, str(RAIZ / 'pesquisas-paralelas/missoes'))
    import ambiente_missoes  # noqa: F401
    from ligacao_provedores_m1 import montar_provedores
    from mapa_memoria_m1 import MapaMemoriaM1
    from memoria_quadro_core import MemoriaQuadro
    from incursao_core import traducao_core
    from mundo_vivo import mundo_vivo
    from solucionador_vivo import SolucionadorCaminhosVivo
    from integracao.providers import load_economy_bonus
    ap = argparse.ArgumentParser()
    ap.add_argument('--quadros', type=int, default=201)
    ap.add_argument('--por-rotina', type=int, default=6, help='world-model comparisons per routine')
    ap.add_argument('--saida')
    a = ap.parse_args()
    saida = RAIZ / (a.saida or 'relatorios/movimento-incursao-mundo-emulada.json')
    adaptadores = _adaptadores()
    registro = dict(comparisons=0, by_routine={}, flat_comparisons=0, flat_by_routine={}, live_comparisons=0,
                    live_by_routine={}, mismatches=[],
                    dependencies=[], isolated={},
                    gaps=sorted(n for n in cm.ROTINAS if n not in adaptadores and traducao_core(n) is None))
    classe = load_economy_bonus().BonusUnidades

    def bonus_de(m):
        tabela = classe.vivo(bytearray(m.ler(0x4dfba0, 1872)), tipos_unidades=bytearray(m.ler(0x4965ae, 1300)))
        return lambda jogador, tipo, seletor: tabela.consultar(jogador, tipo, seletor)

    def plano(nome, caso, antes, resultado):
        """Flat translation (``incursao_core.traducao_core``) over copies of the entry blocks: EAX..EBP and bytes."""
        entrada = {k: int(v, 16) for k, v in resultado['entry_registers'].items()}
        chave = dict(routine=nome, entry=resultado['entry_registers'], kind='flat')
        copias = {n: (b, bytearray(d)) for n, (b, d) in antes.items()}
        m = MemoriaQuadro(copias.values())
        pilha = [m.u32(entrada['ESP'] + 4 + 4 * k) for k in range(6)]
        try:
            regs = dict(entrada, **traducao_core(nome)(m, entrada, pilha, bonus_de(m)))
        except NotImplementedError as e:
            registro['dependencies'].append(dict(chave, reason=f'{type(e).__name__}: {e}'))
            return
        except Exception as e:      # recorded as a failing comparison, never ignored
            registro['mismatches'].append(dict(chave, python_error=f'{type(e).__name__}: {e}'))
            return
        mudancas = []
        for n, (base, dados) in copias.items():
            if n != 'native_stack' and dados != antes[n][1]:
                velho = antes[n][1]
                mudancas += [[hex(base + i), velho[i], dados[i]] for i in range(len(dados)) if dados[i] != velho[i]]
        mudancas.sort(key=lambda x: int(x[0], 16))
        nativas = sorted(resultado['changed_bytes'], key=lambda x: int(x[0], 16))
        nativo = {k: int(v, 16) for k, v in resultado['exit_registers'].items()}
        registro['flat_comparisons'] += 1
        registro['flat_by_routine'][nome] = registro['flat_by_routine'].get(nome, 0) + 1
        if mudancas != nativas or any(regs[k] & M32 != nativo[k] for k in REGISTROS):
            registro['mismatches'].append(dict(chave, python_registers={k: hex(regs[k] & M32) for k in REGISTROS},
                                               native_registers={k: hex(nativo[k]) for k in REGISTROS},
                                               python_changed=mudancas[:LISTA], native_changed=nativas[:LISTA]))

    def vivo(nome, caso, antes, resultado):
        """The world adapter on ``mundo_vivo`` over copies of the entry blocks (the live binding)."""
        entrada = {k: int(v, 16) for k, v in resultado['entry_registers'].items()}
        chave = dict(routine=nome, entry=resultado['entry_registers'], kind='live')
        copias = {n: (b, bytearray(d)) for n, (b, d) in antes.items()}
        try:
            m = MemoriaQuadro(copias.values())
            solucionador = SolucionadorCaminhosVivo(m)
            partes = adaptadores[nome](mundo_vivo(m, solucionador), entrada) or {}
            if solucionador._resultado is not None:     # the search ran: keep the solver's own state
                registro.setdefault('python_search_state', []).append(dict(
                    entry=resultado['entry_registers'], buffers=[bytes(b).hex() for b in solucionador.buffers],
                    regioes=bytes(solucionador.regioes).hex(), registros=[bytes(r).hex() for r in solucionador.registros],
                    inicio=hex(solucionador.inicio_calculado), destino=hex(solucionador.destino_calculado),
                    preparacoes=solucionador.preparacoes_python, escolhas=solucionador.escolhas_python,
                    contornos=solucionador.contornos_python))
        except NotImplementedError as e:
            registro['dependencies'].append(dict(chave, reason=f'{type(e).__name__}: {e}'))
            return
        except Exception as e:      # recorded as a failing comparison, never ignored
            registro['mismatches'].append(dict(chave, python_error=f'{type(e).__name__}: {e}'))
            return
        mudancas = []
        for n, (base, dados) in copias.items():
            if n != 'native_stack' and dados != antes[n][1]:
                velho = antes[n][1]
                mudancas += [[hex(base + i), velho[i], dados[i]] for i in range(len(dados)) if dados[i] != velho[i]]
        mudancas.sort(key=lambda x: int(x[0], 16))
        nativas = sorted(resultado['changed_bytes'], key=lambda x: int(x[0], 16))
        saida_nativa = int(resultado['exit_registers']['EAX'], 16)
        retorno_ok = all((saida_nativa & PARTES[k][0]) == (v & PARTES[k][0]) for k, v in partes.items())
        registro['live_comparisons'] += 1
        registro['live_by_routine'][nome] = registro['live_by_routine'].get(nome, 0) + 1
        if mudancas != nativas or not retorno_ok:
            registro['mismatches'].append(dict(chave, python_return={k: hex(v) for k, v in partes.items()},
                                               native_eax=hex(saida_nativa), python_changed=mudancas[:LISTA],
                                               native_changed=nativas[:LISTA]))

    def contador(antes):
        base, dados = antes['dgroup']
        return int.from_bytes(dados[0x508f7c - base:0x508f80 - base], 'little')

    def observador(nome, caso, antes, resultado):
        registro['isolated'][nome] = registro['isolated'].get(nome, 0) + 1
        # Every call from counter JANELA_BUSCA on (the first path search is at 9176-9179); a sample before.
        todas = contador(antes) >= JANELA_BUSCA
        if traducao_core(nome) is not None and (todas or registro['flat_by_routine'].get(nome, 0) < a.por_rotina):
            plano(nome, caso, antes, resultado)
        if nome in adaptadores and (todas or registro['live_by_routine'].get(nome, 0) < a.por_rotina):
            vivo(nome, caso, antes, resultado)
        if nome not in adaptadores or (contador(antes) < JANELA_BUSCA and registro['by_routine'].get(nome, 0) + sum(
                1 for d in registro['dependencies'] if d['routine'] == nome) >= a.por_rotina):
            return
        entrada = {k: int(v, 16) for k, v in resultado['entry_registers'].items()}
        chave = dict(routine=nome, entry=resultado['entry_registers'])
        blocos = {n: (b, d) for n, (b, d) in antes.items() if n != 'native_stack'}
        try:
            mapa = MapaMemoriaM1(blocos)
            provedores = montar_provedores(mapa)
            mapa.fechar()
            partes = adaptadores[nome](provedores.mundo, entrada) or {}
            depois = mapa.serializar()
        except NotImplementedError as e:
            registro['dependencies'].append(dict(chave, reason=f'{type(e).__name__}: {e}'))
            return
        except Exception as e:      # recorded as a failing comparison, never ignored
            registro['mismatches'].append(dict(chave, python_error=f'{type(e).__name__}: {e}'))
            return
        mudancas = []
        for n, (base, dados) in depois.items():
            velho = blocos[n][1]
            if dados != velho:
                mudancas += [[hex(base + i), velho[i], dados[i]] for i in range(len(dados)) if dados[i] != velho[i]]
        nativas = sorted(resultado['changed_bytes'], key=lambda x: int(x[0], 16))
        mudancas.sort(key=lambda x: int(x[0], 16))
        saida_nativa = int(resultado['exit_registers']['EAX'], 16)
        retorno_ok = all((saida_nativa & PARTES[k][0]) == (v & PARTES[k][0]) for k, v in partes.items())
        registro['comparisons'] += 1
        registro['by_routine'][nome] = registro['by_routine'].get(nome, 0) + 1
        if mudancas != nativas or not retorno_ok or not resultado['reached_return']:
            registro['mismatches'].append(dict(chave, python_return={k: hex(v) for k, v in partes.items()},
                                               native_eax=hex(saida_nativa), python_changed=mudancas[:LISTA],
                                               native_changed=nativas[:LISTA]))

    t0 = time.monotonic()
    b, cap, iso, quadro_de, resumo = cm.executar(a.quadros, observador)
    registro.update(
        schema='rising-lands/monde01-raid-movement-world-differential/1', original_sha256=HASH_ORIGINAL,
        frames=a.quadros, per_routine_limit=a.por_rotina,
        code_unchanged=b.sha256_codigo() == cap['code_integrity']['after'],
        mapping={n: 'see ferramentas/validar_movimento_incursao.py:_adaptadores' for n in adaptadores},
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in (
            'ferramentas/validar_movimento_incursao.py', 'ferramentas/capturar_movimento_incursao.py',
            'ferramentas/ordens_unidades.py', 'ferramentas/avanco_unidades.py', 'ferramentas/navegacao_unidades.py',
            'ferramentas/passagem_unidades.py', 'ferramentas/movimento.py')},
        seconds=round(time.monotonic() - t0, 3))
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(registro, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps({k: registro[k] for k in ('comparisons', 'by_routine', 'flat_comparisons', 'flat_by_routine',
                                               'live_comparisons', 'live_by_routine',
                                               'gaps', 'seconds')}
                     | dict(mismatches=len(registro['mismatches']), dependencies=len(registro['dependencies']),
                            output=str(saida)), indent=1))
    encerrar_captura(0 if not registro['mismatches'] else 2, saida)


if __name__ == '__main__':
    main()
