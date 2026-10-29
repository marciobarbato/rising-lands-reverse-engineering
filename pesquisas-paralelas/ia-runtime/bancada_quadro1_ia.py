"""AI/runtime pauses on Missions' committed MONDE01 first-frame path (load tail, window loop, frame 1).

Reuses ``oraculo_quadro_missao.BancadaQuadroMissaoOriginal`` and ``Isolamento``
by import. ``PausaIA`` extends ``Isolamento`` with *snapshot-only* routines. At
such an entry it hands the exact saved state (every block, registers) to an
observer and resumes without running anything extra. This is needed for
routines that reach a binding or a boundary (RestoreAll, InputGame), which an
isolated call may not do. Executed routines (CalculNextReflect,
ProcessInputGame, …) are run in isolation by ``Isolamento`` on the exact saved
state, and the state is then restored. ``executar_caminho`` replays the whole
path and checks that every committed phase state, the entry trace and the
boundaries are reproduced, which proves each restoration was exact. Importing
this module executes nothing.
"""
import json
import struct
import sys

from ambiente_ia_runtime import ROOT

MISSOES = ROOT / 'pesquisas-paralelas/missoes'
if str(MISSOES) not in sys.path:
    sys.path.insert(0, str(MISSOES))
import ambiente_missoes  # noqa: E402,F401
import capturar_quadro_missao_original as cq  # noqa: E402
from oraculo_quadro_missao import BancadaQuadroMissaoOriginal, Isolamento  # noqa: E402
from emulador import PILHA  # noqa: E402

CAPTURA_QUADRO = MISSOES / 'evidencias/captura-quadro1-monde01-original.json'


class PausaIA(Isolamento):
    def __init__(self, bancada, executadas, instantaneos=(), observador=None, instantaneo=None):
        super().__init__(bancada, tuple(executadas) + tuple(instantaneos), None, observador)
        self.instantaneos = {bancada.sym[n] for n in instantaneos}
        self.instantaneo = instantaneo        # f(routine, phase, blocks, registers, caller_return, bench)
        self.pausas = []

    def executar(self, regs):
        entrada = regs['EIP']
        if entrada not in self.instantaneos:
            return super().executar(regs)
        b = self.b
        nome = self.entradas[entrada]
        retorno = struct.unpack('<I', b.cpu.mem_read(regs['ESP'], 4))[0]
        blocos = b.imagem()
        blocos['native_stack'] = (PILHA, bytes(b.cpu.mem_read(PILHA, 0x10000)))
        self.pausas.append(dict(routine=nome, phase=b.fase, caller_return=hex(retorno), caller=b.nome(retorno),
                                registers={k: hex(v) for k, v in regs.items()},
                                state=b.resumo_imagem({k: v for k, v in blocos.items() if k != 'native_stack'})))
        if self.instantaneo is not None:
            self.instantaneo(nome, b.fase, blocos, regs, retorno, b)


def executar_caminho(executadas, instantaneos=(), observador=None, instantaneo=None):
    cap = json.loads(CAPTURA_QUADRO.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaQuadroMissaoOriginal(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    pausa = PausaIA(b, executadas, instantaneos, observador, instantaneo)
    pausa.instalar()
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
    return b, pausa, cap, reproducao
