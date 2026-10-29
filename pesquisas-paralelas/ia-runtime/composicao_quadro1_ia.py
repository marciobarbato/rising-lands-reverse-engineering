"""Python composition of MONDE01 phases (a) load_tail, (b) between_frames and (c) frame1.

The memory is Missions' one-address-space M1 model, used by import:
``mapa_memoria_m1.MapaMemoriaM1`` plus ``ligacao_provedores_m1.montar_provedores``.
It is built from a captured original state block set. Phase (a) starts from the
accepted M1 post-load state; its bytes equal the Stage14 strict composition
output and the frozen v2 final state. Every provider is an integrated,
committed function called in original order:
- this front's frame skeleton, CalculNextReflect, the dispatcher loops,
  AvanceMonstre, MessageBoxCalcul and ProcessInputGame;
- Core frame foundations and ``tarefas_ia``;
- Economy ``Mercado``;
- Missions ``fim_missao``.

A routine without one raises ``DependenciaIA(name, original CALL)`` after every
earlier effect.

Declared non-executed boundaries of the original capture are recorded and
stepped over exactly as the original bench does: AffGame, PlaySnd_Manage,
MCICD_Manage, MCICD_Play (with its guards), and the display routines inside
RestoreAll and MenuInit. **AffGame is an open item**: graphics is proving its
write set. The Windows answers are the capture's named inputs: PeekMessageA 0,
GetCursorPos (0, 0), SetCursorPos 1, GetAsyncKeyState 0.

Registers are modeled where the composed code defines them: phase (b)
completely (EAX/EBX/ECX/EDX/ESI/EDI/EBP/ESP), and the registers each recorded
binding or boundary carries. Bench stack bytes (the boundary stack words that
lie in caller locals) are not modeled; those fields are listed as such.
"""
import base64
import hashlib
import json
import struct
import sys
import zlib

from ambiente_ia_runtime import ROOT

MISSOES = ROOT / 'pesquisas-paralelas/missoes'
if str(MISSOES) not in sys.path:
    sys.path.insert(0, str(MISSOES))
import ambiente_missoes  # noqa: E402,F401
from mapa_memoria_m1 import MapaMemoriaM1, carregar_blocos  # noqa: E402
from ligacao_provedores_m1 import montar_provedores  # noqa: E402
from fim_missao import evento_em_curso  # noqa: E402
from fundacoes_quadro import avancar_contadores_iteracao, zerar_contadores_carga  # noqa: E402

from laco_despachantes import REGIOES_DESPACHO, calcular_proxima_etapa_estruturas, calcular_proxima_etapa_unidades  # noqa: E402
from quadro_calcul_game import REGIOES_QUADRO, calcular_quadro  # noqa: E402
from reinicio_ia import DependenciaIA  # noqa: E402
from rotinas_quadro_ia import (REGIOES_ROTINAS, TABELA_COMANDOS, PonteTarefas, avancar_monstros,  # noqa: E402
                               calcular_caixa_mensagens, processar_entrada, resolver_ia)
from simbolos_ia import ler_rul  # noqa: E402
from tarefas_ia import MaquinaTarefas  # noqa: E402
from ambiente_ia_runtime import CD  # noqa: E402

CAPTURA_M1 = MISSOES / 'evidencias/captura-carga-missao-original-v2.json'
CAPTURA_QUADRO = MISSOES / 'evidencias/captura-quadro1-monde01-original.json'
FASES = ('load_tail', 'between_frames', 'frame1')
REGIOES_COMPOSICAO = REGIOES_QUADRO + REGIOES_DESPACHO + REGIOES_ROTINAS + (
    (0x49a010, 0x49a012, 'CalculGame cursor constant'), (0x5099a8, 0x5099b3, 'cursor words and input-edge flags'),
    (0x49a058, 0x49a05a, 'window active and quit flags'), (0x496fe4, 0x496fe5, 'mission number'),
    (0x4e1b0e, 0x4e1b0f, 'event in progress'), (0x508724, 0x508728, 'viewport size'),
    (0x5080a8, 0x5080ac, 'player records pointer'), (0x51a98c, 0x51a9dc, 'AI player contexts'))
TABELA_ESTADOS = 0x42c804


def regioes_dinamicas(u32):
    """Regions behind live pointers: the unit pool [0x4e19a0] and the four input records [0x4e2458 + 4p]."""
    pool = u32(0x4e19a0)
    return ((pool, pool + 800 * 276, 'unit pool [0x4e19a0]'),) + tuple(
        (u32(0x4e2458 + 4 * p), u32(0x4e2458 + 4 * p) + 10, f'input record [0x4e2458+{4 * p}]') for p in range(4))


def memoria_composicao(mapa):
    return mapa.memoria_declarada(REGIOES_COMPOSICAO + regioes_dinamicas(mapa.u32))


def estados_originais():
    """Original state block sets: S0 (M1 return 0x42d22d) and after each captured phase."""
    m1 = json.loads(CAPTURA_M1.read_bytes())
    quadro = json.loads(CAPTURA_QUADRO.read_bytes())
    estado = carregar_blocos(m1['oracle']['final_state']['blocks'])
    if quadro['state_s0']['summary']['sha256'] != m1['oracle']['final_state']['summary']['sha256']:
        raise ValueError('Frame capture S0 is not the accepted M1 final state')
    estados = {'s0': dict(estado)}
    for fase in quadro['phases']:
        estado = dict(estado)
        for nome, bloco in fase['state_after']['blocks_changed_since_previous'].items():
            dados = zlib.decompress(base64.b64decode(bloco['zlib_base64']))
            if hashlib.sha256(dados).hexdigest() != bloco['sha256']:
                raise ValueError(f'Phase block {nome} hash mismatch')
            estado[nome] = (int(bloco['base'], 16), dados)
        hashes = {n: hashlib.sha256(d).hexdigest() for n, (_, d) in estado.items()}
        if hashes != {n: h['sha256'] for n, h in fase['state_after']['block_hashes'].items()}:
            raise ValueError(f"Reconstructed state after {fase['phase']} does not match its block hashes")
        estados[fase['phase']] = estado
    return estados, quadro


class ContextoQuadro(PonteTarefas):
    """Core's task machine (RISING.RUL from the read-only CD) plus jump tables read from the intact image."""

    def __init__(self, imagem):
        super().__init__(MaquinaTarefas(ler_rul((CD / 'INSTALHD/RISING.RUL').read_bytes())))
        self.comandos = imagem.table(TABELA_COMANDOS, 40)
        self.estados = imagem.table(TABELA_ESTADOS, 25)


def mundo(blocos):
    mapa = MapaMemoriaM1({n: v for n, v in blocos.items() if n != 'native_stack'})
    provedores = montar_provedores(mapa)
    mapa.fechar()
    return mapa, provedores


class Registro:
    """Bindings and boundary events in the capture's comparable fields, in order."""

    def __init__(self, fase):
        self.fase, self.vinculos, self.fronteiras = fase, [], []

    def vinculo(self, nome, argumentos, retorno, resultado, escritas=()):
        self.vinculos.append(dict(name=nome, arguments=[hex(a & 0xffffffff) for a in argumentos],
                                  caller_return=hex(retorno), results={'EAX': hex(resultado)},
                                  memory_writes=[dict(address=hex(a), sha256=hashlib.sha256(d).hexdigest(),
                                                      size=len(d)) for a, d in escritas]))

    def fronteira(self, rotina, retorno, chamador, registros, guardas=None, palavras=None):
        self.fronteiras.append(dict(phase=self.fase, routine=rotina, caller_return=hex(retorno), caller=chamador,
                                    top_callee=rotina,
                                    registers={k: hex(v) for k, v in registros.items()}, declared_eax=None,
                                    stack_cleanup=0, guards=guardas or {},
                                    stack_words=None if palavras is None else [hex(p) for p in palavras]))


def _provedores_quadro(mapa, prov, memoria, registro, ebx_entrada, ponte):
    """Original-name providers of the frame body over the mapped live memory."""
    def mcicd_play(sitio, faixa, edx):
        indice = mapa.u8(0x4e1d18)
        registro.fronteira('MCICD_Play', sitio + 5, 'CalculGame+0xac5',
                           dict(EAX=faixa, EDX=edx, EBX=(ebx_entrada & ~0xff) | indice, ECX=2),
                           {'0x4e2f28': mapa.u8(0x4e2f28), '0x4e2f29': mapa.u8(0x4e2f29)})
        return faixa

    p = {
        'EvenementEnCours': lambda sitio: evento_em_curso(mapa.vista(0x4e1b0e, 1)),
        'MCICD_Play': mcicd_play,
        'PlayerGetType': lambda sitio, jogador: prov.mercado.tipo_jogador(jogador),
        'MissionGetNum': lambda sitio: mapa.u8(0x496fe4),
        'ProcessInputGame': lambda sitio, jogador: processar_entrada(memoria, jogador, ponte.comandos),
        'MessageBoxCalcul': lambda sitio: calcular_caixa_mensagens(memoria),
        'AvanceMonstre': lambda sitio, jogador: avancar_monstros(memoria, p),
        'iaSolver': lambda sitio, contexto: resolver_ia(memoria, ponte, contexto),
        'CalculEnginNextEtape': lambda sitio: calcular_proxima_etapa_unidades(memoria, p),
        'CalculBatimentNextEtape': lambda sitio: calcular_proxima_etapa_estruturas(memoria, p),
    }
    return p


def fase_cauda_carga(mapa, prov, ponte, registro):
    """(a) 0x42d22d (jmp 0x42d27f) .. load-state CalculGame RET; the frame body is frame 0."""
    memoria = memoria_composicao(mapa)
    faltante = {}

    def chamar(rotina, sitio, **argumentos):
        provedor = faltante.get(rotina)
        if provedor is None:
            raise DependenciaIA(rotina, sitio)
        return provedor(sitio=sitio, **argumentos)

    chamar('RestoreAll', 0x42d27f)
    chamar('SetClipping', 0x42d2a6, eax=0, edx=0, ebx=(mapa.u16(0x508724) << 5) - 1,
           ecx=(mapa.u16(0x508726) << 5) - 1)
    zerar_contadores_carga(mapa.vista(0x508f7c, 12))
    chamar('MenuInit', 0x42d2d0, jogador=mapa.u8(0x508041), estado=0x12, ecx=1)
    chamar('InitGameZone', 0x42d2d9, eax=1, edx=0)
    return calcular_quadro(memoria, _provedores_quadro(mapa, prov, memoria, registro, 0, ponte))


def fase_entre_quadros(mapa, entradas, registro, registros):
    """(b) ProgIteration 0x475063 .. _WinMain@16 loop .. ProgIteration .. CalculGame entry 0x42c868.

    ``registros``: the declared register file at 0x475063 (ESP = the POINT local of
    ProgIteration's frame). Returns the register file at the CalculGame entry.
    """
    r = dict(registros)
    pilha = {}                      # modeled stack words written by this phase
    point = r['ESP']
    # 0x475063 call AffGame (declared boundary, not executed): stack words are the POINT
    # local and ProgIteration's saved EDX/ECX.
    salvos = dict(EDX=entradas['salvo_edx'], ECX=entradas['salvo_ecx'], EBX=entradas['salvo_ebx'])
    registro.fronteira('AffGame', 0x475068, 'ProgIteration+0x5a', {k: r[k] for k in ('EAX', 'EDX', 'EBX', 'ECX')},
                       palavras=(entradas['point'][0], entradas['point'][1], salvos['EDX'], salvos['ECX']))
    if mapa.u8(0x5099af):
        r['EDX'] &= ~0xff00
        mapa.vista(0x5099af, 1)[0] = 0
        mapa.vista(0x5099ae, 1)[0] = 0
    if mapa.u8(0x5099b2):
        r['ECX'] &= ~0xff
        mapa.vista(0x5099b1, 1)[0] = 0
        mapa.vista(0x5099b2, 1)[0] = 0
    r['ESP'] = point + 8
    r['EDX'], r['ECX'], r['EBX'] = salvos['EDX'], salvos['ECX'], salvos['EBX']
    r['ESP'] += 12 + 4                                  # pops and RET to 0x460212
    msg = r['ESP']
    for rotina, retorno, chamador in (('PlaySnd_Manage', 0x460220, '_WinMain@16+0xb0'),
                                      ('MCICD_Manage', 0x460225, '_WinMain@16+0xb5')):
        guardas = {'0x4e2f28': mapa.u8(0x4e2f28), '0x4e2f29': mapa.u8(0x4e2f29)} if rotina == 'MCICD_Manage' else {}
        registro.fronteira(rotina, retorno, chamador, {k: r[k] for k in ('EAX', 'EDX', 'EBX', 'ECX')}, guardas,
                           palavras=entradas['msg'])
    if r['EBX'] & 0xff != mapa.u8(0x49a059):
        raise DependenciaIA('_WinMain@16 quit path', 0x460227)
    # PeekMessageA(&msg, 0, 0, 0, 0): four pushes of EBX (0), then lea eax,[esp+0x10]; push eax.
    r['EAX'] = msg
    registro.vinculo('USER32.PeekMessageA', (msg, r['EBX'], r['EBX'], r['EBX'], r['EBX']), 0x4601d8,
                     entradas['peek_message'])
    r['EAX'] = entradas['peek_message']
    if r['EAX']:
        raise DependenciaIA('_WinMain@16 GetMessageA/DispatchMessageA path', 0x4601dc)
    if r['EBX'] & 0xff == mapa.u8(0x49a058):
        raise DependenciaIA('_WinMain@16 WaitMessage path', 0x460214)
    # 0x46020d call ProgIteration; 0x47500e push ebx/ecx/edx; sub esp, 8
    r['ESP'] = msg - 4 - 12 - 8
    avancar_contadores_iteracao(mapa.vista(0x508f7c, 12))
    r['EBX'] = 3
    r['EAX'], r['EDX'] = mapa.u32(0x508f7c) // 3, mapa.u32(0x508f7c) % 3
    r['EDX'] = r['ESP']
    x, y = entradas['cursor']
    registro.vinculo('USER32.GetCursorPos', (r['ESP'],), 0x47504b, 1,
                     escritas=((r['ESP'], struct.pack('<ii', x, y)),))
    r['EAX'] = x & 0xffffffff
    mapa.vista(0x5099a8, 2)[:] = struct.pack('<H', x & 0xffff)
    r['EAX'] = y & 0xffffffff
    mapa.vista(0x5099aa, 2)[:] = struct.pack('<H', y & 0xffff)
    r['ESP'] -= 4                                       # call CalculGame
    pilha[r['ESP']] = 0x475063
    return r, pilha


def fase_quadro(mapa, prov, ponte, entradas, registro, registros):
    """(c) CalculGame 0x42c868 (entered from ProgIteration) .. its return to 0x475063."""
    memoria = memoria_composicao(mapa)
    estado = mapa.u8(0x4e2f78)
    mapa.vista(0x49a010, 2)[:] = struct.pack('<H', 0x1dd8)
    registro.vinculo('USER32.SetCursorPos', (mapa.u16(0x5099a8), mapa.u16(0x5099aa)), 0x42c8a5,
                     entradas['set_cursor_pos'])
    if estado != 0x12:
        raise DependenciaIA(f'CalculGame state 0x{estado:x}', ponte.estados[estado] if estado <= 0x18 else 0x42d4e2)
    return calcular_quadro(memoria, _provedores_quadro(mapa, prov, memoria, registro, registros['EBX'], ponte))
