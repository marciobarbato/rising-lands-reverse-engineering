"""N consecutive MONDE01 frames composed in Python on one map (M2.2): load_tail, then between_frames(k) and
frame(k) for k = 1..N.

This generalizes the M2.1 chain (a)->(b)->(c) of ``composicao_encadeada_ia`` in mode 'prova'. It uses
the same providers, no crossing, and ONE map built from the display scenario's MissionLoad final state. The
phase names follow Missions' ``oraculo_quadro_missao.nomes_fases``: frame 1 keeps ``between_frames``/``frame1``,
and frame k >= 2 is ``between_frames{k}``/``frame{k}``.

Registers are carried from phase to phase:
- load_tail starts from the reference's declared MissionLoad-return registers.
- between_frames(1) starts from the reference's between_frames entry registers, as in M2.1. Python does not
  model CalculGame's return inside the load-state frame.
- between_frames(k), k >= 2, starts from frame(k-1)'s entry registers with ESP + 4. CalculGame pushes
  EBX/ECX/EDX/ESI/EDI/EBP at 0x42c868 and pops them in its shared epilogue. Its leftover EAX is never read
  there, because AffGame's leftover EAX replaces it before the first boundary (``affgame_hud_ia``).
- frame(k) starts from between_frames(k)'s exit registers.

ProgIteration's saved (EDX, ECX, EBX) words are declared for frame 1 (0, 0, 0, from the bench loop frame).
For frame k >= 2 they are the values that the previous between-frames phase pushed (``empilhadas``).

Frame inputs are the scenario's named inputs: no key, no message (PeekMessageA 0), and the GetCursorPos
answer. Display ticks, DirectDraw calls and palette work are display context and are not produced.
"""
import json
import struct
import sys

from ambiente_ia_runtime import ROOT
from bancos_quadro_ia import ArenaQuadro
from composicao_encadeada_ia import (ContextoEncadeado, Registro, Travessias, fase_cauda_carga,
                                     fase_entre_quadros_exibicao, fase_quadro)
from composicao_quadro1_ia import mundo
from inventario_ia_runtime import OriginalImage

MISSOES = ROOT / 'pesquisas-paralelas/missoes'
if str(MISSOES) not in sys.path:
    sys.path.insert(0, str(MISSOES))
from oraculo_quadro_missao import nomes_fases  # noqa: E402

REGISTRADORES = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP')
PRESERVADOS_CALCUL_GAME = ('EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
MSG_LACO = (0x3000000, 0, 0, 0)          # bench _WinMain@16 loop frame MSG words (M2.1 declared input)


def fases_quadros(n):
    """Phase names of load_tail plus N frames, in order."""
    saida = ['load_tail']
    for k in range(1, n + 1):
        saida += nomes_fases(k)
    return saida


class ComposicaoQuadros:
    """One map carried through load_tail and N frames; ``executar`` yields one record per phase."""

    def __init__(self, estado_s0, captura_quadro, entrada, captura_m1, hashes_ponto=None, pontos=None,
                 planejamento=False):
        self.cap = captura_quadro
        fases = {p['phase']: p for p in captura_quadro['phases']}
        superficie = next(s for s in fases['load_tail']['display_state']['surfaces'] if s['role'] == 'offscreen')
        self.mapa, self.prov = mundo(estado_s0)
        self.arena = ArenaQuadro(self.mapa, entrada['arena'], captura_m1['allocations'])
        self.ctx = ContextoEncadeado(OriginalImage(), 'exibicao', modo='prova', arena=self.arena,
                                     superficie=int(superficie['pixels'], 16), planejamento=planejamento)
        self.travessias = Travessias(pontos or {}, {}, hashes_ponto or (lambda m: {}))
        self.regs_carga = {k: int(v, 16) for k, v in fases['load_tail']['entry']['registers'].items()}
        self.regs_entre1 = {k: int(v, 16) for k, v in fases['between_frames']['entry']['registers'].items()}
        self.cursor = tuple(captura_quadro['named_inputs']['frame']['cursor'])
        self.declarados = dict(offscreen_surface_pixels=superficie['pixels'], msg_words=[hex(x) for x in MSG_LACO],
                               saved_frame_words_frame1=[0, 0, 0], cursor=list(self.cursor),
                               between_frames1_entry_registers=fases['between_frames']['entry']['registers'])

    def executar(self, n):
        """Yield ``dict(phase, registro, entry, exit)`` per phase. A stop propagates to the caller."""
        registro = Registro('load_tail')
        fase_cauda_carga(self.mapa, self.prov, self.ctx, registro, self.travessias, dict(self.regs_carga))
        yield dict(phase='load_tail', registro=registro, entry=dict(self.regs_carga), exit=None)
        palavras, entrada_quadro_anterior = (0, 0, 0), None
        for k in range(1, n + 1):
            entre, quadro = nomes_fases(k)
            if k == 1:
                regs = dict(self.regs_entre1)
            else:
                regs = {r: entrada_quadro_anterior[r] for r in PRESERVADOS_CALCUL_GAME}
                regs.update(ESP=(entrada_quadro_anterior['ESP'] + 4) & 0xffffffff, EAX=None)
            entradas = dict(salvo_edx=palavras[0], salvo_ecx=palavras[1], salvo_ebx=palavras[2], msg=MSG_LACO,
                            peek_message=0, cursor=self.cursor, empilhadas=None)
            registro = Registro(entre)
            saida = fase_entre_quadros_exibicao(self.mapa, self.prov, self.ctx, registro, self.travessias, regs,
                                                entradas, fase=entre)
            if saida['EAX'] is None or entradas['empilhadas'] is None:
                raise RuntimeError(f'{entre}: AffGame EAX or the pushed frame words were not produced')
            palavras = entradas['empilhadas']
            yield dict(phase=entre, registro=registro, entry=regs, exit=dict(saida))
            registro = Registro(quadro)
            entrada_quadro_anterior = dict(saida)
            fase_quadro(self.mapa, self.prov, self.ctx, registro, self.travessias, dict(saida), fase=quadro)
            yield dict(phase=quadro, registro=registro, entry=dict(saida), exit=None)


def carregar_cenario_exibicao():
    """The display -v2 reference inputs: S0 blocks, per-phase states, the frame capture, the entry and M1."""
    import cenarios_oraculo
    from comparar_quadro1_encadeado_ia import estados_cenario
    estados, cap = estados_cenario('exibicao')
    entrada = json.loads(cenarios_oraculo.caminho('exibicao', 'entrada').read_bytes())
    m1 = json.loads(cenarios_oraculo.caminho('exibicao', 'captura_m1').read_bytes())
    return estados, cap, entrada, m1


def indicadores(mapa):
    """Frame-end indicators in the form of Core's 0..128 survey (``levantar_quadros_exibicao``)."""
    u32 = lambda a: struct.unpack('<I', mapa.ler(a, 4))[0]  # noqa: E731
    u16 = lambda a: struct.unpack('<H', mapa.ler(a, 2))[0]  # noqa: E731
    return dict(counter=u32(0x508f7c), game_frame=u32(0x496d40), world_rng=hex(u32(0x497164)),
                ai_rng=hex(u32(0x498db4)), crt_seed=hex(u32(u32(0x522244) + 0xc)), cursor=mapa.ler(0x4e1d18, 1)[0],
                view_origin=[u16(0x508720), u16(0x508722)])
