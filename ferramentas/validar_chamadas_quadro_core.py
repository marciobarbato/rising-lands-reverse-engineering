"""Fresh native differential of the Core frame-0/frame-1 callees at the exact frame inputs.

Reruns the committed first-frame path with ``oraculo_quadro_missao.Isolamento``
at every Core callee entry (as ``capturar_chamadas_core_quadro1``). For each
call the captured inputs and, for the first calls of each routine per phase,
declared perturbations (registers and/or explicit byte writes at the exact
entry state) run natively; an observer then runs the Python translation over
copies of the exact entry blocks (DGROUP+.bss, CRT page, every live allocation,
native stack) and compares every changed byte and the general registers. The
rerun must still reproduce the committed phase states, boundaries and trace.

    python3 -B ferramentas/validar_chamadas_quadro_core.py [--saida relatorios/chamadas-quadro1-emulada.json]
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
import capturar_chamadas_core_quadro1 as cc   # noqa: E402  (adds the Missions folder to sys.path)
from chamadas_quadro_core import ROTINAS, DependenciaRamoCore   # noqa: E402
from memoria_quadro_core import MemoriaQuadro   # noqa: E402

REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
TABELA_BONUS, TAMANHO_BONUS = 0x4dfba0, 4 * 26 * 18
ESTRUTURA0 = 0x49a0c8
LIMITE_POR_FASE = 4


def perturbacoes(unidades, descoberta0):
    """Declared native cases per routine; ``unidades`` is the unit pool base u32 [0x4e19a0] and
    ``descoberta0`` owner 0's discovery grid pointer u32 [0x507d78]."""
    r = lambda nome, **regs: dict(case=nome, writes=[], registers=regs)
    w = lambda nome, escritas, **regs: dict(case=nome, writes=escritas, registers=regs)
    u0 = unidades                     # unit 0 record
    estruturas = []
    for tipo in (0, 9, 17, 21, 24, 25):
        for origem in (0x0000, 0x00fe, 0xfe00, 0xffff, 0x8080):
            for jogador in (0, 4):
                estruturas.append(w(f'type{tipo}_origin{origem:04x}_owner{jogador}',
                                    [(ESTRUTURA0 + 8, [tipo]), (ESTRUTURA0 + 2, list(origem.to_bytes(2, 'little')))],
                                    EAX=0, EDX=jogador))
    # Owners 0..7 index 64 KiB grids in both pointer tables (discovery, light, light-count); higher
    # owners alias the attribute/animation pointers and then smaller blocks or the zero slot 15.
    # A footprint cell (row 1, column 1 of a type-0 structure at 0x8080) made "discovered" for owner 0.
    estruturas.append(w('type0_origin8080_owner0_cell8181_bit10_clear',
                        [(ESTRUTURA0 + 8, [0]), (ESTRUTURA0 + 2, [0x80, 0x80]), (descoberta0 + 0x8181, [0])],
                        EAX=0, EDX=0))
    grade = [r('owner0', EDX=0), r('owner4_alias', EDX=4), r('owner7', EDX=0x307), r('owner6', EDX=0x106),
             r('cell_ffff', EAX=0xffff), r('high_bits_owner0', EAX=0x12340f07, EDX=0x5500)]
    return {
        'GetBit': [r('a5_0', EAX=0xffffffa5, EDX=0), r('a5_7', EAX=0xa5, EDX=7), r('a5_8', EAX=0x1a5, EDX=0x108),
                   r('80_31', EAX=0x80, EDX=0x1f), r('80_39', EAX=0x80, EDX=0x27)],
        'SetBit': [r('clear', EBX=0), r('noop', EBX=2), r('set_shift9', EBX=0x101, EDX=9),
                   r('clear_shift35', EBX=0x100, EDX=0x23)],
        'CaseEstDecouverte': grade, 'CaseEstIlluminee': grade,
        'BatimentCollision': [r('type16', EAX=0x16), r('type20_alias15', EAX=0x14), r('high_type21', EAX=0x115),
                              r('high_index', EDX=0xffff0003), r('type9_far', EAX=9, EDX=0x7f)],
        'SetCollision': [r('mask2', EDX=2), r('mask80', EDX=0x80), r('high_cell', EAX=0xabcd0000)],
        'Chemin_ModifieZone': [r('insert_cell0', EAX=0), r('insert_cell8080', EAX=0x8080),
                               r('high_unit', EAX=0x8080, EDX=0x10000),
                               w('insert_class2', [(u0 + 1, [12])], EAX=0x8181, EDX=0)],
        'SetEnginCollision': [w(f'unit0_type{t}', [(u0 + 1, [t])], EAX=0) for t in (3, 11, 16, 17, 25, 0x1a, 0xff)]
                             + [w('unit0_free_cell', [(u0 + 1, [0])], EAX=0, EDX=0x8282)],
        'CalculFatigue': [w(f'unit0_type{t}', [(u0 + 1, [t]), (u0 + 0x72, [1])], EAX=0) for t in (11, 14, 17)]
                         + [w('unit0_inactive', [(u0 + 0x72, [0])], EAX=0),
                            w('counter_bb6', [(u0 + 0x72, [1]), (u0 + 0x74, [0xb6, 0x0b])], EAX=0),
                            w('counter_wrap', [(u0 + 0x72, [1]), (u0 + 0x74, [0xff, 0xff])], EAX=0),
                            w('owner2_f8', [(u0, [2]), (u0 + 0x72, [1]), (u0 + 0xf8, [0x20])], EAX=0)],
        'BatimentGetCase': estruturas, 'BatimentEstDecouvert': estruturas, 'BatimentContourEstIllumine': estruturas,
        'Random': [w('seed_zero', [(0x497164, [0, 0, 0, 0])]), w('seed_max', [(0x497164, [0xff] * 4)])],
        'GameNextFrame': [w('wrap', [(0x496d40, [0xff] * 4)])],
    }


class PerturbacoesLimitadas:
    """Hand the declared cases only to the first ``limite`` calls of a routine in each phase."""
    def __init__(self, bancada, casos, limite):
        self.b, self.casos, self.limite, self.vistos = bancada, casos, limite, {}

    def get(self, nome, padrao=()):
        chave = (nome, self.b.fase)
        self.vistos[chave] = self.vistos.get(chave, 0) + 1
        return self.casos.get(nome, padrao) if self.vistos[chave] <= self.limite else padrao


def executar_python(nome, antes, entrada, classe_bonus):
    """Run the translation over copies of the exact entry blocks; returns (changed bytes, registers)."""
    buffers = {n: (base, bytearray(dados)) for n, (base, dados) in antes.items()}
    m = MemoriaQuadro(buffers.values())
    sub = m.u8(entrada['ESP'] + 4) if nome == 'Chemin_ModifieZone' else None
    bonus = lambda jogador, tipo, seletor: classe_bonus(m.ler(TABELA_BONUS, TAMANHO_BONUS)).consultar(jogador, tipo,
                                                                                                    seletor)
    saida = ROTINAS[nome][1](m, entrada, sub, bonus)
    mudancas = []
    for n, (base, dados) in buffers.items():
        if n == 'native_stack':
            continue
        velho = antes[n][1]
        if dados != velho:
            mudancas += [[hex(base + i), velho[i], dados[i]] for i in range(len(dados)) if dados[i] != velho[i]]
    return sorted(mudancas, key=lambda x: int(x[0], 16)), dict(entrada, **saida)


def diferencial(limite=LIMITE_POR_FASE):
    from integracao.providers import ECONOMY, _load_providers
    classe_bonus = _load_providers((('economia', ECONOMY / 'economia.py'),
                                    ('bonus_unidades', ECONOMY / 'bonus_unidades.py'))).BonusUnidades
    registro = dict(comparisons=0, by_routine={}, mismatches=[], dependencies=[], al_by_routine={})
    caixa = {}

    def observador(nome, fase, caso, antes, resultado):
        entrada = {k: int(v, 16) for k, v in resultado['entry_registers'].items()}
        entrada.update(caso['registers'])
        chave = f"{nome}:{caso['case']}"
        try:
            mudancas, regs = executar_python(nome, antes, entrada, classe_bonus)
        except DependenciaRamoCore as e:
            registro['dependencies'].append(dict(routine=nome, phase=fase, case=caso['case'], address=hex(e.endereco)))
            return
        except Exception as e:          # reported as a failing comparison, never ignored
            registro['mismatches'].append(dict(routine=nome, phase=fase, case=caso['case'],
                                               python_error=f'{type(e).__name__}: {e}'))
            return
        nativo = {k: int(v, 16) for k, v in resultado['exit_registers'].items()}
        nativas = sorted(resultado['changed_bytes'], key=lambda x: int(x[0], 16))
        if mudancas != nativas or any(regs[k] != nativo[k] for k in REGISTROS) or not resultado['reached_return']:
            registro['mismatches'].append(dict(
                routine=nome, phase=fase, case=caso['case'], python_changed=mudancas[:20], native_changed=nativas[:20],
                python_registers={k: hex(regs[k]) for k in REGISTROS},
                native_registers={k: hex(nativo[k]) for k in REGISTROS}))
        registro['comparisons'] += 1
        registro['by_routine'][nome] = registro['by_routine'].get(nome, 0) + 1
        al = registro['al_by_routine'].setdefault(nome, {})
        al[str(nativo['EAX'] & 0xff)] = al.get(str(nativo['EAX'] & 0xff), 0) + 1
        if mudancas:
            caixa[nome] = caixa.get(nome, 0) + 1

    captura = json.loads((RAIZ / 'evidencias/fundacoes-quadro/captura-chamadas-quadro1.json').read_bytes())
    primeira = next(c for c in captura['calls'] if c['routine'] == 'SetEnginCollision')
    lidos = {int(a, 16): v for a, v, _ in primeira['read_before_write']}
    unidades = int.from_bytes(bytes(lidos[0x4e19a0 + i] for i in range(4)), 'little')
    from estado_m1_quadro import carregar_m1   # the grid pointers are set by MissionLoad and never move
    descoberta0 = int.from_bytes(carregar_m1()[0][0x507d78 - 0x494000:0x507d7c - 0x494000], 'little')
    b, iso, cap, reproducao = _executar(perturbacoes(unidades, descoberta0), observador, limite)
    registro.update(path_reproduction=reproducao, calls=len(iso.registros), cases_with_stores=caixa,
                    unit_pool_base=hex(unidades), owner0_discovery_grid=hex(descoberta0),
                    perturbation_limit_per_phase=limite)
    return registro


def _executar(casos, observador, limite):
    import capturar_isolados_quadro1 as ci
    import capturar_quadro_missao_original as cq
    from oraculo_quadro_missao import BancadaQuadroMissaoOriginal, Isolamento
    cap = json.loads(ci.CAPTURA.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaQuadroMissaoOriginal(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    iso = Isolamento(b, cc.ROTINAS, PerturbacoesLimitadas(b, casos, limite), observador)
    iso.instalar()
    resumos = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(3600)),
                         ('between_frames', lambda: b.executar_entre_quadros(120)),
                         ('frame1', lambda: b.executar_quadro(3600))):
        correr()
        resumos[nome] = b.resumo_imagem(b.imagem())
    fases = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao = dict(phase_states_equal={f: resumos[f] == fases[f] for f in fases},
                      entry_trace_equal=json.loads(json.dumps(b.rastro_json())) == cap['entry_trace'],
                      boundaries_equal=b.eventos_fronteira == [e for p in cap['phases'] for e in p['boundaries']],
                      code_unchanged=b.sha256_codigo() == cap['code_integrity']['after'])
    reproducao['passed'] = all(reproducao['phase_states_equal'].values()) and all(
        reproducao[k] for k in ('entry_trace_equal', 'boundaries_equal', 'code_unchanged'))
    return b, iso, cap, reproducao


def main():
    from emulador import HASH_ORIGINAL
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', default='relatorios/chamadas-quadro1-emulada.json')
    a = ap.parse_args()
    t0 = time.monotonic()
    r = diferencial()
    r.update(original_sha256=HASH_ORIGINAL, seconds=round(time.monotonic() - t0, 3),
             source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in (
                 'ferramentas/chamadas_quadro_core.py', 'ferramentas/memoria_quadro_core.py',
                 'ferramentas/validar_chamadas_quadro_core.py')})
    ok = r['path_reproduction']['passed'] and not r['mismatches'] and not r['dependencies']
    saida = RAIZ / a.saida if ok else RAIZ / '.local/frame' / ('chamadas-quadro1-falha-' + time.strftime('%Y%m%dT%H%M%S')
                                                              + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(json.dumps(r, indent=1, sort_keys=True) + '\n')
    print(json.dumps({k: r[k] for k in ('comparisons', 'by_routine', 'path_reproduction', 'calls', 'seconds')}
                     | dict(mismatches=len(r['mismatches']), dependencies=len(r['dependencies']), output=str(saida)),
                     indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
