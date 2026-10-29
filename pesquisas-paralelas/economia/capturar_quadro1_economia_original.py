"""Original-only isolated captures of the economy calls at the exact MONDE01 frame-0/1 inputs.

Reruns Missions' committed first-frame path of a named oracle scenario
(``--cenario v1``: accepted M1 startup and MissionLoad; ``--cenario exibicao``:
the real window loop with the display path executed, the M2 reference; then
load_tail = frame 0, between_frames, frame1) with Missions'
``oraculo_quadro_missao.Isolamento`` pausing at every entry of the economy
routines and the two economy branch fragments that path reaches. Each call
runs natively in isolation on the exact saved state and records registers,
changed bytes and the bytes read before written, with their entry values.
The state is then restored and the phase resumes. The run must reproduce
every committed phase state, the entry trace, the boundaries and the code
hash, which proves the restorations were exact. Fragments (the EnginNextEtape
state-7 body and the BatimentNextEtape type-1/2/13/16 branch) have no return
address and run to their declared exits. No Python translation is imported.

    python3 -B pesquisas-paralelas/economia/capturar_quadro1_economia_original.py \
        --saida pesquisas-paralelas/economia/evidencias/captura-quadro1-economia-original-v2.json
    python3 -B pesquisas-paralelas/economia/capturar_quadro1_economia_original.py --cenario exibicao \
        --saida pesquisas-paralelas/economia/evidencias/captura-quadro1-economia-exibicao.json
    python3 -B pesquisas-paralelas/economia/capturar_quadro1_economia_original.py --cenario exibicao \
        --conjunto consultas --saida pesquisas-paralelas/economia/evidencias/captura-consultas-economia-exibicao-v2.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import time

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
sys.path.insert(0, str(RAIZ / 'pesquisas-paralelas/missoes'))
import ambiente_missoes  # noqa: E402,F401
import capturar_quadro_missao_original as cq  # noqa: E402
import cenarios_oraculo  # noqa: E402
import oraculo_quadro_missao as oq  # noqa: E402
from emulador import HASH_ORIGINAL  # noqa: E402

ROTINAS = ('RechercheCalcul', 'PlayerInitAllianceCompteur', 'SetUpdateChamp', 'UpdateChamp', 'CalculMatiere',
           'CalculCompteurMarche', 'CalculCompteurProposition', 'PlayerAttaqueCalculSympa', 'MAJSympathie',
           'BonusGetValEngin', 'ResetTableauHangar', 'BagContientTroupe', 'CalculTroupe', 'BatimentGetCase')
FRAGMENTOS = {0x456966: ('EnginNextEtape:state7', 0x454ccd),
              0x426918: ('BatimentNextEtape:type1_2_13_16', 0x4281c0)}
# ``--conjunto consultas``: the economy queries the frames reach outside the routines above (nested calls
# included, e.g. IntToBCD/BCDToInt inside CalculMatiere), plus BagVide, which AffGame reaches next to
# BagContientTroupe. Kept apart so the ``quadro`` set stays comparable call by call across scenarios.
CONSULTAS = ('PlayerGetType', 'PlayerEstAllie', 'TestRessource', 'BatimentGetType', 'BatimentEstHabiter',
             'IntToBCD', 'BCDToInt', 'BagVide')
CONJUNTOS = {'quadro': (ROTINAS, FRAGMENTOS, False), 'consultas': (CONSULTAS, {}, True)}


class IsolamentoEconomia(oq.Isolamento):
    """Missions' isolation plus fragment entries that run to a declared exit instead of a stack return."""
    def __init__(self, bancada, rotinas, fragmentos, pilha_chamador=False):
        super().__init__(bancada, rotinas)
        self.fragmentos = fragmentos
        # Also record writes into the caller's frame (at or above the exit ESP; the entry ESP for
        # fragments), e.g. IntToBCD's caller buffer. Off for the ``quadro`` set, whose frozen captures
        # predate it; on for ``consultas`` (v2).
        self.pilha_chamador = pilha_chamador
        self.entradas.update({a: nome for a, (nome, _) in fragmentos.items()})

    def executar(self, regs):
        b, entrada = self.b, regs['EIP']
        nome, fase = self.entradas[entrada], b.fase
        fragmento = entrada in self.fragmentos
        retorno = self.fragmentos[entrada][1] if fragmento else struct.unpack('<I', b.cpu.mem_read(regs['ESP'], 4))[0]
        contexto, blocos = self._salvar()
        self.ativo = False
        b.fase = 'isolated'
        try:
            self._restaurar(contexto, blocos)
            antes = self._salvar()[1]
            eventos, fronteiras = len(b.vinculos_declarados.eventos), len(b.eventos_fronteira)
            lidos, escritos, ganchos = self._rastrear(blocos)
            ganchos.append(b.cpu.hook_add(oq.unicorn.UC_HOOK_CODE, b._parar_se_pedido, begin=retorno, end=retorno))
            b.cpu.ctl_flush_tb()
            try:
                b._retomando = {entrada}
                saida = oq.BancadaCargaMissaoOriginal._correr(b, 'isolated', entrada, {}, (retorno,), retomar=True)
            finally:
                for g in ganchos:
                    b.cpu.hook_del(g)
                b.cpu.ctl_flush_tb()
            if len(b.vinculos_declarados.eventos) != eventos or len(b.eventos_fronteira) != fronteiras:
                b._interromper('binding_or_boundary_in_isolated_call', routine=nome, case='captured_inputs')
            depois = self._salvar()[1]
            mudados = {}
            for n, (base, dados) in depois.items():
                if n == 'native_stack':
                    continue
                velho = antes[n][1]
                if dados != velho:
                    mudados.update({base+i: (velho[i], dados[i]) for i in range(len(dados)) if dados[i] != velho[i]})
            # Fragments keep the caller's frame: its locals at or above the exit ESP are inputs too.
            limite = saida['ESP'] if not fragmento else regs['ESP']
            leituras = sorted(a for a in lidos if not (oq.PILHA <= a < limite))
            self.registros.append(dict(
                routine=nome, entry=hex(entrada), phase=fase, kind='fragment' if fragmento else 'routine',
                exit=hex(retorno), caller=b.nome(retorno),
                entry_registers={k: hex(v) for k, v in regs.items()},
                exit_registers={k: hex(v) for k, v in saida.items()},
                reached_exit=saida['EIP'] == retorno,
                changed_bytes=[[hex(a), v[0], v[1]] for a, v in sorted(mudados.items())],
                # Bytes written to the value they already held: their entry value, needed when not read first.
                written_unchanged=[[hex(a), self._valor(depois, a)] for a in sorted(escritos)
                                   if a not in mudados and not oq.PILHA <= a < oq.PILHA + 0x10000],
                read_before_write=[[hex(a), self._valor(antes, a), b.nome(lidos[a])] for a in leituras]))
            # Callee-popped arguments (RET n) lie below the exit ESP, so the read set above excludes them:
            # record their entry bytes. Absent for routines that pop nothing (every ``quadro`` routine).
            if self.pilha_chamador:
                pilha_antes, pilha_depois = antes['native_stack'][1], depois['native_stack'][1]
                topo = oq.PILHA + len(pilha_antes)
                self.registros[-1]['caller_stack_changes'] = [
                    [hex(a), pilha_antes[a - oq.PILHA], pilha_depois[a - oq.PILHA]] for a in range(limite, topo)
                    if pilha_antes[a - oq.PILHA] != pilha_depois[a - oq.PILHA]]
                self.registros[-1]['caller_stack_written_unchanged'] = [
                    [hex(a), pilha_depois[a - oq.PILHA]] for a in sorted(escritos)
                    if limite <= a < topo and pilha_antes[a - oq.PILHA] == pilha_depois[a - oq.PILHA]]
            if not fragmento and saida['ESP'] > regs['ESP'] + 4:
                self.registros[-1]['stack_arguments'] = bytes(
                    self._valor(antes, a) for a in range(regs['ESP'] + 4, saida['ESP'])).hex()
        finally:
            self._restaurar(contexto, blocos)
            b.fase = fase
            self.ativo = True


# Oracle sources each scenario actually runs (v1 does not touch the display backend).
FONTES = {'v1': ('pesquisas-paralelas/missoes/oraculo_quadro_missao.py',),
          'exibicao': ('pesquisas-paralelas/missoes/oraculo_quadro_missao.py',
                       'pesquisas-paralelas/missoes/oraculo_exibicao_missao.py',
                       'pesquisas-paralelas/missoes/cenarios_oraculo.py',
                       'pesquisas-paralelas/graficos-animacao/fronteiras_exibicao.py')}


def fontes(cenario):
    return (Path(__file__),) + tuple(RAIZ / f for f in FONTES[cenario])


def captura_quadro(cenario):
    return cenarios_oraculo.caminho(cenario, 'captura_quadro')


def executar(cenario='v1', conjunto='quadro'):
    cap = json.loads(captura_quadro(cenario).read_bytes())
    if cap.get('scenario', 'v1') != cenario:
        raise RuntimeError(f'Frame capture scenario {cap.get("scenario")!r} is not {cenario!r}')
    ni = cap['named_inputs']['m1']
    if cenario == 'v1':
        b = oq.BancadaQuadroMissaoOriginal(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    else:
        b, _, nomeadas = cenarios_oraculo.bancada(cenario, ni['allocation_fill'], ni['clock_ms'][0], segundos=300)
        if json.loads(json.dumps(nomeadas)) != cap['named_inputs']:
            raise RuntimeError('Scenario named inputs differ from the committed frame capture')
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    iso = IsolamentoEconomia(b, *CONJUNTOS[conjunto])
    iso.instalar()
    resumos = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(120)),
                         ('frame1', lambda: b.executar_quadro(600))):
        correr()
        resumos[nome] = b.resumo_imagem(b.imagem())
    fases = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao = dict(phase_states_equal={f: resumos[f] == fases[f] for f in fases},
                      entry_trace_equal=json.loads(json.dumps(b.rastro_json())) == cap['entry_trace'],
                      boundaries_equal=b.eventos_fronteira == [e for p in cap['phases'] for e in p['boundaries']],
                      code_unchanged=b.sha256_codigo() == cap['code_integrity']['after'])
    reproducao['passed'] = (all(reproducao['phase_states_equal'].values()) and reproducao['entry_trace_equal']
                            and reproducao['boundaries_equal'] and reproducao['code_unchanged'])
    return b, iso, cap, reproducao


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--saida', required=True)
    # exibicao_interino (Stage17, retired interim backend) is historical and not rerunnable.
    ap.add_argument('--cenario', default='v1', choices=tuple(FONTES))
    ap.add_argument('--conjunto', default='quadro', choices=tuple(CONJUNTOS))
    a = ap.parse_args()
    saida = RAIZ / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    t0 = time.monotonic()
    b, iso, cap, reproducao = executar(a.cenario, a.conjunto)
    contagem = {}
    for r in iso.registros:
        contagem.setdefault(f"{r['phase']}:{r['routine']}", 0)
        contagem[f"{r['phase']}:{r['routine']}"] += 1
    relatorio = dict(
        schema='rising-lands/monde01-frame1-isolated-economy-calls/2', original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, scenario=a.cenario, named_inputs=cap['named_inputs'],
        source_sha256={str(p.relative_to(RAIZ)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in fontes(a.cenario)},
        frame_capture=dict(path=str(captura_quadro(a.cenario).relative_to(RAIZ)),
                           sha256=hashlib.sha256(captura_quadro(a.cenario).read_bytes()).hexdigest()),
        phases_label='load_tail = frame 0 (counter 0), frame1 = frame 1 (counter 1)',
        routine_set=a.conjunto, routines=list(CONJUNTOS[a.conjunto][0]),
        fragments={hex(a): dict(name=n, exit=hex(x)) for a, (n, x) in CONJUNTOS[a.conjunto][1].items()},
        path_reproduction=reproducao, call_counts=contagem, calls=iso.registros,
        method='Missions Isolamento: native call from the exact saved entry state to its stack return (routines) '
               'or declared exit (fragments), local read/write hooks with the translation cache flushed, state '
               'restored after each call; the resumed phases must reproduce the committed frame capture',
        seconds=round(time.monotonic()-t0, 3))
    falhou = not reproducao['passed'] or not all(r['reached_exit'] for r in iso.registros)
    if falhou:
        saida = RAIZ / '.local' / (f'economia-quadro1-{a.cenario}-{a.conjunto}-isolado-falhou-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), reproduction=reproducao, counts=contagem, seconds=relatorio['seconds']),
                     indent=1))
    return 2 if falhou else 0


if __name__ == '__main__':
    sys.exit(main())
