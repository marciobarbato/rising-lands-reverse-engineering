"""Shared runner: the committed MONDE01 first-frame path with isolated Core callees.

Reruns one of Missions' committed paths ('v1': display skipped; 'exibicao':
display executed, the M2 reference) - startup, MissionLoad, then load_tail =
frame 0, between_frames, frame1 - on the intact executable with
``oraculo_quadro_missao.Isolamento`` pausing at the given routine entries. An
optional native block-coverage recorder lists the basic blocks each isolated
case executed (hook added, then the translation cache flushed). The run must
reproduce every committed phase state, boundary log, entry trace and the code
section. Importing this module executes nothing.
"""
import json
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[1]
MISSOES = RAIZ / 'pesquisas-paralelas/missoes'
if str(MISSOES) not in sys.path:
    sys.path.insert(0, str(MISSOES))
CODIGO = (0x401000, 0x493bff)


class Cobertura:
    """Basic blocks executed while the bench is in an isolated call; drained per case."""
    def __init__(self, bancada):
        import unicorn
        self.b, self.blocos = bancada, set()
        bancada.cpu.hook_add(unicorn.UC_HOOK_BLOCK, self._bloco, begin=CODIGO[0], end=CODIGO[1])
        bancada.cpu.ctl_flush_tb()

    def _bloco(self, cpu, endereco, tamanho, _):
        if self.b.fase == 'isolated':
            self.blocos.add(endereco)

    def drenar(self):
        blocos, self.blocos = sorted(self.blocos), set()
        return blocos


def _isolamento_limitado(bancada, rotinas, casos, observador, limites):
    """Isolamento that isolates only the first ``limites[name]`` calls of a routine per phase.

    Later calls are not paused: the phase resumes and executes them natively as usual.
    """
    from oraculo_quadro_missao import Isolamento

    class IsolamentoLimitado(Isolamento):
        def executar(self, regs):
            nome = self.entradas[regs['EIP']]
            chave = (nome, self.b.fase)
            self.vistos[chave] = self.vistos.get(chave, 0) + 1
            if nome in limites and self.vistos[chave] > limites[nome]:
                return
            super().executar(regs)

    iso = IsolamentoLimitado(bancada, rotinas, casos, observador)
    iso.vistos = {}
    return iso


def _bancada(cenario):
    """(bench after MissionLoad, committed frame capture) for the 'v1' or 'exibicao' scenario."""
    import capturar_isolados_quadro1 as ci
    import capturar_quadro_missao_original as cq
    if cenario == 'v1':
        from oraculo_quadro_missao import BancadaQuadroMissaoOriginal
        cap = json.loads(ci.CAPTURA.read_bytes())
        ni = cap['named_inputs']['m1']
        b = BancadaQuadroMissaoOriginal(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    elif cenario == 'exibicao':
        import cenarios_oraculo
        cap = json.loads(cenarios_oraculo.caminho('exibicao', 'captura_quadro').read_bytes())
        ni = cap['named_inputs']['m1']
        b, _, _ = cenarios_oraculo.bancada('exibicao', ni['allocation_fill'], ni['clock_ms'][0], segundos=300)
    else:
        raise ValueError(f'Unknown scenario {cenario!r}')
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    return b, cap


def executar(rotinas, perturbacoes=None, observador=None, cobertura=None, limite=3600, cenario='v1',
             limites=None):
    """Returns (bench, isolation, frame capture, reproduction, coverage or None).

    ``cobertura``: a dict to receive the ``Cobertura`` recorder (key 'recorder')
    before the phases run, so an observer can drain it per case.
    ``perturbacoes``: a dict, or a callable(bench) returning one.
    ``cenario``: 'v1' (display skipped) or 'exibicao' (display executed, the M2 reference).
    ``limites``: {routine: n} isolates only the first n calls of that routine in each phase.
    """
    b, cap = _bancada(cenario)
    cob = Cobertura(b) if cobertura is not None else None
    if cob is not None:
        cobertura['recorder'] = cob
    casos = perturbacoes(b) if callable(perturbacoes) else perturbacoes
    iso = _isolamento_limitado(b, rotinas, casos, observador, limites or {})
    iso.instalar()
    resumos = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(limite)),
                         ('between_frames', lambda: b.executar_entre_quadros(120)),
                         ('frame1', lambda: b.executar_quadro(limite))):
        correr()
        resumos[nome] = b.resumo_imagem(b.imagem())
    fases = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao = dict(phase_states_equal={f: resumos[f] == fases[f] for f in fases},
                      entry_trace_equal=json.loads(json.dumps(b.rastro_json())) == cap['entry_trace'],
                      boundaries_equal=b.eventos_fronteira == [e for p in cap['phases'] for e in p['boundaries']],
                      code_unchanged=b.sha256_codigo() == cap['code_integrity']['after'])
    reproducao['passed'] = all(reproducao['phase_states_equal'].values()) and all(
        reproducao[k] for k in ('entry_trace_equal', 'boundaries_equal', 'code_unchanged'))
    return b, iso, cap, reproducao, cob
