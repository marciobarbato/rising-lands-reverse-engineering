"""M3 scripted-input oracle: the display reference from the accepted frame-128 checkpoint with frame-scheduled input.

Original only (no translation runs here). It implements the harness of docs/M3_PLAN.md §2:

* **Input file**, schema ``rising-lands/monde01-scripted-input/1`` (``carregar_entrada``). Per frame k it may hold
  the ``GetCursorPos`` answer, the ordered ``PeekMessageA`` messages ``[msg, wParam, lParam]`` and the
  ``GetAsyncKeyState`` table by vkey. Frames not listed keep the no-input answers for messages (none) and keys
  (0). The cursor is a position, not an event: it holds its last declared value (initially (0,0), the accepted
  no-input answer) until a later frame declares another.
* **Frame k** is the pair of phases ``between_frames{k}`` (the AffGame of frame k-1, the real ``_WinMain@16``
  loop and ProgIteration up to the CalculGame entry) and ``frame{k}`` (CalculGame). Frame k's messages are queued
  when ``between_frames{k}`` starts; the original loop (0x4601c0) drains them one per iteration with
  ``PeekMessageA`` (PM_NOREMOVE), ``GetMessageA``, ``TranslateMessage`` and ``DispatchMessageA`` before it runs
  ProgIteration, whose single ``GetCursorPos`` (0x475044) takes frame k's cursor.
* **DispatchMessageA** calls the registered window procedure ``WndProc 0x4181a1`` natively: after the declared
  import returns, the harness turns its frame into the stdcall frame ``WndProc(hwnd, msg, wParam, lParam)`` with
  the same return address (``RegistroComDespacho``), so WndProc's ``RET 0x10`` leaves ESP exactly where
  ``DispatchMessageA``'s ``RET 4`` would. No WndProc flag is written by the harness. Only messages WndProc handles
  without ``DefWindowProcA`` are accepted (0x100, 0x101, 0x200..0x205); every other import stays a trap.
  ``TranslateMessage`` answers 0 and posts nothing: a WM_CHAR the user wants must be in the input file.
* The run starts from the M2.2 frame-128 snapshot of ``checkpoint_quadro128.py``. The scripted bindings are added
  *after* that restore (three new IAT slots, ``GetMessageA``/``TranslateMessage``/``DispatchMessageA``, and the
  existing ``GetCursorPos``/``PeekMessageA``/``GetAsyncKeyState`` bindings answer from the input file). Later
  checkpoints of a scripted run are restored into a bench that already carries those bindings.

Recorded outputs (§2 "Recorded outputs"), all under the run directory:

1. ``quadros.jsonl``: one line per frame (frame, counter 0x508f7c, game frame, routines first entered with
   first-entry phase and caller return address, per-routine entry counts, whole mapped-state SHA-256,
   DGROUP SHA-256, game RNG 0x497164, AI RNG 0x498db4, CRT seed, permutation cursor 0x4e1d18, view origin, the
   display surface hashes at the end of both phases, and the objective trace (item 4)).
2. ``entradas.jsonl``: every declared input answer consumed (frame, phase, poll site, value) and, for each
   dispatched message, the WndProc flag bytes 0x5099a8..0x5099b2 at its return to 0x460203.
3. ``comandos.jsonl``: every ``SetPlayerOrdre 0x45ecd4`` call (player, tag and arguments, caller, the packet
   before it) and every ``ProcessInputGame 0x45edc0`` entry whose packet tag is not 0 (packet, jump target from
   table 0x45ed20).
4. Objective trace inside each frame line: 0x4e1d84..0x4e1d91, 0x4e05a0, 0x4e061c, 0x4e1a3a, the player-0
   resource record 0x4e2ea8..+0x20 and every existing structure (index, owner +4, type +8, origin +2).
5. Snapshots (``segmentos_quadros_missao.salvar``) after the frames the input file lists, after each frame with
   a SetPlayerOrdre call, at the first CreerBatiment entry, the first nonzero 0x4e05a0, the first MenuInit
   entry with mode 0x13 and every ``--instantaneo-cada`` frames.
6. ``fronteiras.jsonl``: the PlaySnd_* and MCICD_* boundary calls in order, with arguments and caller.

``resumo.json`` holds the manifest: input file hash, start snapshot hash, source hashes, frames, status and the
routines first entered. Two runs of one input file must give equal ``quadros.jsonl``, ``entradas.jsonl``,
``comandos.jsonl`` and ``fronteiras.jsonl`` once the wall-clock field ``seconds`` is dropped (``comparar``).

    python3 -B pesquisas-paralelas/missoes/m3/entrada_roteirizada.py correr --entrada <input.json> \
        --inicio .local/m3/quadro128 --saida .local/m3/sondas/P1-a
    python3 -B pesquisas-paralelas/missoes/m3/entrada_roteirizada.py comparar .local/m3/sondas/P1-a \
        .local/m3/sondas/P1-b
"""
import argparse
import dataclasses
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import time
import traceback

MISSOES = Path(__file__).resolve().parents[1]
if str(MISSOES) not in sys.path:
    sys.path.insert(0, str(MISSOES))
import ambiente_missoes  # noqa: E402

ROOT = ambiente_missoes.ROOT
ESQUEMA = 'rising-lands/monde01-scripted-input/1'
QUADRO_INICIAL = 128

# Original addresses (intact RISING.EXE), all operands or entries of the cited code.
WNDPROC = 0x4181a1
RETORNO_DISPATCH = 0x460203          # _WinMain@16, after CALL [DispatchMessageA]
SET_PLAYER_ORDRE, PROCESS_INPUT_GAME = 0x45ecd4, 0x45edc0
PACOTES, TABELA_PROCESS = 0x4e2458, 0x45ed20
CREER_BATIMENT, MENU_INIT = 0x41fea2, 0x4682bb
IAT = dict(GetCursorPos=0x523294, PeekMessageA=0x5232b8, GetAsyncKeyState=0x523290,
           GetMessageA=0x523298, TranslateMessage=0x5232d8, DispatchMessageA=0x523284)
JANELA = 0x4e27e8                    # HWND stored by AppWindowInit (never executed: declared value)
FLAGS = (0x5099a8, 0x5099b3)         # WndProc stores: coordinates, then 0x5099ae..0x5099b2
MENSAGENS = {0x100: 'WM_KEYDOWN', 0x101: 'WM_KEYUP', 0x200: 'WM_MOUSEMOVE', 0x201: 'WM_LBUTTONDOWN',
             0x202: 'WM_LBUTTONUP', 0x203: 'WM_LBUTTONDBLCLK', 0x204: 'WM_RBUTTONDOWN', 0x205: 'WM_RBUTTONUP'}
OBJETIVO = dict(marks=(0x4e1d84, 14), al=(0x4e05a0, 1), victory_counter=(0x4e061c, 4), forced=(0x4e1a3a, 2),
                player0_resources=(0x4e2ea8, 32))
ESTRUTURAS, PASSO_ESTRUTURA, N_ESTRUTURAS = 0x49a0c8, 276, 1000   # +2 origin cell, +4 owner, +5 exists, +8 type
UNIDADES_PTR, PASSO_UNIDADE = 0x4e19a0, 276                        # +2 state, +0x7c cell (EnginGetCase)
UNIDADES_SEGUIDAS = (11, 12, 13, 14, 15)
UI = (0x496207, 0x4e05ae, 0x496208)                                # structure to build, its copy, discovery gate


# ------------------------------------------------------------------------------------------------ input file
def _inteiro(v):
    return int(v, 0) if isinstance(v, str) else int(v)


def carregar_entrada(dados):
    """Validate an input-file dict; returns {frame: (cursor or None, messages, keys)} and the stop frame."""
    if dados.get('schema') != ESQUEMA:
        raise ValueError(f'Input schema must be {ESQUEMA}')
    if dados.get('start', {}).get('frame') != QUADRO_INICIAL:
        raise ValueError('Scripted runs start from the accepted M2.2 frame-128 checkpoint')
    ate = int(dados['stop_frame'])
    quadros = {}
    for q in dados.get('frames', ()):
        k = int(q['frame'])
        if not QUADRO_INICIAL < k <= ate or k in quadros:
            raise ValueError(f'Frame {k} outside {QUADRO_INICIAL + 1}..{ate} or listed twice')
        cursor = q.get('cursor')
        if cursor is not None:
            x, y = (int(c) for c in cursor)
            if not (0 <= x < 800 and 0 <= y < 600):
                raise ValueError(f'Frame {k}: cursor {cursor} outside the 800x600 screen')
            cursor = (x, y)
        mensagens = []
        for m in q.get('messages', ()):
            msg, wp, lp = (_inteiro(v) for v in m)
            if msg not in MENSAGENS:
                raise ValueError(f'Frame {k}: message {msg:#x} is not one WndProc handles without DefWindowProcA')
            if not (0 <= wp < 1 << 32 and 0 <= lp < 1 << 32):
                raise ValueError(f'Frame {k}: wParam/lParam must be u32')
            mensagens.append((msg, wp, lp))
        teclas = {}
        for vk, valor in (q.get('keys') or {}).items():
            vk, valor = _inteiro(vk), _inteiro(valor)
            if not (0 < vk < 256 and -0x8000 <= valor < 0x8000):
                raise ValueError(f'Frame {k}: key {vk:#x} answer {valor} must be an i16 for vkey 1..255')
            teclas[vk] = valor
        quadros[k] = (cursor, tuple(mensagens), teclas)
    for k in dados.get('checkpoint_frames', ()):
        if not QUADRO_INICIAL < int(k) <= ate:
            raise ValueError(f'Checkpoint frame {k} outside the run')
    return quadros, ate


def lparam(x, y):
    return (y & 0xffff) << 16 | (x & 0xffff)


def clique(k, x, y, botao='left'):
    """M3_PLAN §2 click: WM_MOUSEMOVE at k, button DOWN at k+1 and UP at k+3, the cursor held at (x,y) from k."""
    baixo, cima, mk = (0x201, 0x202, 1) if botao == 'left' else (0x204, 0x205, 2)
    lp = lparam(x, y)
    return [dict(frame=k, cursor=[x, y], messages=[[0x200, 0, lp]]),
            dict(frame=k + 1, messages=[[baixo, mk, lp]]),
            dict(frame=k + 3, messages=[[cima, 0, lp]])]


def juntar_quadros(*listas):
    """Merge frame entries of several clicks; two entries of one frame concatenate their messages."""
    por = {}
    for lista in listas:
        for q in lista:
            d = por.setdefault(q['frame'], dict(frame=q['frame']))
            if 'cursor' in q:
                if 'cursor' in d and d['cursor'] != q['cursor']:
                    raise ValueError(f"Frame {q['frame']}: two cursor answers")
                d['cursor'] = q['cursor']
            if q.get('messages'):
                d.setdefault('messages', []).extend(q['messages'])
            if q.get('keys'):
                d.setdefault('keys', {}).update(q['keys'])
    return [por[k] for k in sorted(por)]


# ------------------------------------------------------------------------------------------------ answers
class RoteiroEntrada:
    """Frame-scheduled declared answers. Plain data only: it is pickled inside bench snapshots."""
    def __init__(self, quadros):
        self.quadros = quadros
        self.quadro = QUADRO_INICIAL
        self.cursor = (0, 0)
        self.fila = []
        self.teclas = {}
        self.despachos = 0
        self.eventos = []          # drained by the run every frame

    def iniciar_quadro(self, k):
        if self.fila:
            raise RuntimeError(f'Messages of frame {self.quadro} were not consumed: {self.fila}')
        cursor, mensagens, teclas = self.quadros.get(k, (None, (), {}))
        self.quadro, self.fila, self.teclas = k, list(mensagens), dict(teclas)
        if cursor is not None:
            self.cursor = cursor

    def _msg(self, janela, m):
        msg, wp, lp = m
        # MSG: hwnd, message, wParam, lParam, time (declared 0), pt (the frame's cursor).
        return struct.pack('<IIIIIii', janela, msg, wp, lp, 0, *self.cursor)


class AtendenteEntrada:
    """The binding handlers over a bench's RoteiroEntrada (bound after any restore keeps its identity)."""
    def __init__(self, bancada):
        self.b = bancada

    @property
    def r(self):
        return self.b.roteiro

    def _evento(self, chamada, tipo, **valores):
        self.r.eventos.append(dict(frame=self.r.quadro, phase=self.b.fase, kind=tipo, site=hex(chamada.retorno),
                                   **valores))

    def cursor(self, chamada):
        x, y = self.r.cursor
        chamada.escrever(chamada.argumentos[0], struct.pack('<ii', x, y))
        self._evento(chamada, 'cursor', x=x, y=y)
        return 1

    def tecla(self, chamada):
        vk, = chamada.argumentos
        valor = self.r.teclas.get(vk, 0)
        self._evento(chamada, 'key', vk=vk, value=valor)
        return valor & 0xffff

    def _janela(self):
        return struct.unpack('<I', self.b.cpu.mem_read(JANELA, 4))[0]

    def peek(self, chamada):
        from vinculos_declarados import ParadaVinculoDeclarado
        msg, hwnd, minimo, maximo, remover = chamada.argumentos
        if (hwnd, minimo, maximo, remover) != (0, 0, 0, 0):
            raise ParadaVinculoDeclarado('PeekMessageA outside the declared (0,0,0,PM_NOREMOVE) loop poll')
        if not self.r.fila:
            self._evento(chamada, 'peek_message', message=None)
            return 0
        chamada.escrever(msg, self.r._msg(self._janela(), self.r.fila[0]))
        self._evento(chamada, 'peek_message', message=list(self.r.fila[0]))
        return 1

    def get(self, chamada):
        from vinculos_declarados import ParadaVinculoDeclarado
        msg, hwnd, minimo, maximo = chamada.argumentos
        if (hwnd, minimo, maximo) != (0, 0, 0) or not self.r.fila:
            raise ParadaVinculoDeclarado('GetMessageA without a peeked declared message')
        m = self.r.fila.pop(0)
        chamada.escrever(msg, self.r._msg(self._janela(), m))
        self._evento(chamada, 'get_message', message=list(m))
        return 1

    def traduzir(self, chamada):
        self._evento(chamada, 'translate_message', result=0)
        return 0

    def despachar(self, chamada):
        endereco, = chamada.argumentos
        hwnd, msg, wp, lp = struct.unpack('<4I', self.b.cpu.mem_read(endereco, 16))
        self.b.vinculos_declarados.pendente = (hwnd, msg, wp, lp)
        self.r.despachos += 1
        self._evento(chamada, 'dispatch_message', message=[msg, wp, lp], hwnd=hwnd, wndproc=hex(WNDPROC))
        return 0


def _registro_com_despacho():
    from vinculos_declarados import RegistroVinculosDeclarados

    class RegistroComDespacho(RegistroVinculosDeclarados):
        """After the declared DispatchMessageA returns, enter WndProc natively with the message (stdcall)."""
        def invocar(self, endereco):
            retorno = super().invocar(endereco)
            if endereco != getattr(self, 'despacho', None):
                return retorno
            esp = self.cpu.reg_read(self.registradores['ESP'])
            hwnd, msg, wp, lp = self.pendente
            self.pendente = None
            novo = esp - 20
            self.cpu.mem_write(novo, struct.pack('<5I', retorno, hwnd, msg, wp, lp))
            self.cpu.reg_write(self.registradores['ESP'], novo)
            self.cpu.reg_write(self.registradores['EIP'], WNDPROC)
            return WNDPROC
    return RegistroComDespacho


def instalar_entrada(b):
    """Bind the scripted answers on a display bench (after the frame-128 restore, or before a later restore)."""
    from emulador import unicorn
    if getattr(b, 'roteiro', None) is None:
        b.roteiro = RoteiroEntrada({})
    at = AtendenteEntrada(b)
    por_nome = {d['name']: int(d['target'], 16) for d in b.importacoes_declaradas}
    trocas = {'USER32.GetCursorPos': at.cursor, 'USER32.PeekMessageA': at.peek,
              'USER32.GetAsyncKeyState': at.tecla}
    vinculos = b.vinculos_declarados.vinculos
    for nome, atender in trocas.items():
        a = por_nome[nome]
        vinculos[a] = dataclasses.replace(vinculos[a], atender=atender)
    reg = b.vinculos_declarados
    reg.__class__ = _registro_com_despacho()
    novos = (('USER32.GetMessageA', IAT['GetMessageA'], 4, at.get),
             ('USER32.TranslateMessage', IAT['TranslateMessage'], 1, at.traduzir),
             ('USER32.DispatchMessageA', IAT['DispatchMessageA'], 1, at.despachar))
    for nome, slot, n, atender in novos:
        if nome in por_nome:
            a = por_nome[nome]
            vinculos[a] = dataclasses.replace(vinculos[a], atender=atender)
        else:
            b.declarar_importacao(slot, nome, n, atender)
            a = int(b.importacoes_declaradas[-1]['target'], 16)
        b.cpu.hook_add(unicorn.UC_HOOK_CODE, b._parar_se_pedido, begin=a, end=a)
        if nome == 'USER32.DispatchMessageA':
            reg.despacho = a
    reg.pendente = None
    b.cpu.ctl_flush_tb()
    return at


# ------------------------------------------------------------------------------------------------ bench
def bancada_fresca(ticks):
    """The -v2 display bench (constructor only) with Missions' block trace off, as Core's long runs build it."""
    import cenarios_oraculo as cen
    from mapa_memoria_m1 import carregar_json
    from oraculo_exibicao_missao import BancadaExibicaoOriginal
    import segmentos_quadros_missao as seg
    ni = carregar_json(cen.caminho('exibicao', 'captura_m1'))['named_inputs']
    e = cen.entradas_exibicao(ni['allocation_fill'], ni['clock_ms'][0], ticks=seg.ticks_exibicao(ticks))
    return BancadaExibicaoOriginal(e, segundos=300, rastrear=False)


def abrir(inicio, instantaneo=None):
    """(bench, handlers, start frame). ``inicio``: the frame-128 snapshot directory; ``instantaneo``: a later
    snapshot of a scripted run (restored after the scripted bindings are installed)."""
    import segmentos_quadros_missao as seg
    manifesto = json.loads((Path(inicio) / 'manifesto.json').read_text())
    b = bancada_fresca(manifesto['ticks'])
    if instantaneo is None:
        k = seg.restaurar(b, Path(inicio) / manifesto['snapshot'])
        if k != QUADRO_INICIAL:
            raise RuntimeError('The start snapshot is not frame 128')
        b.roteiro = None
        at = instalar_entrada(b)
    else:
        b.roteiro = None
        at = instalar_entrada(b)
        k = seg.restaurar(b, instantaneo)
    return b, at, k


# ------------------------------------------------------------------------------------------------ recording
class Cobertura:
    """One UC_HOOK_BLOCK counting original symbol entries (Core's ContadorEntradas rule) plus the first entry's
    phase and caller return address ([ESP] when the block starts at the entry; None for a fall-through)."""
    def __init__(self, b, vistos=()):
        from bisect import bisect_left
        from emulador import unicorn, x86
        codigo = (0x401000, 0x493c00)
        self.nomes = {a: n for a, n in b.nomes.items() if codigo[0] <= a < codigo[1]}
        self.quadro, self.primeiras, self.vistos = {}, [], set(vistos)
        entradas, quadro, n = sorted(self.nomes), self.quadro, len(self.nomes)
        primeiras, vistos_, nomes = self.primeiras, self.vistos, self.nomes

        def bloco(cpu, endereco, tamanho, _):
            i = bisect_left(entradas, endereco)
            fim = endereco + tamanho
            while i < n and entradas[i] < fim:
                a = entradas[i]
                quadro[a] = quadro.get(a, 0) + 1
                if a not in vistos_:
                    vistos_.add(a)
                    chamador = None
                    if a == endereco:
                        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
                        chamador = hex(struct.unpack('<I', cpu.mem_read(esp, 4))[0])
                    primeiras.append(dict(routine=nomes[a], address=hex(a), phase=b.fase, caller_return=chamador,
                                          caller=b.nome(int(chamador, 16)) if chamador else None))
                i += 1
        self._bloco = bloco
        b.cpu.hook_add(unicorn.UC_HOOK_BLOCK, bloco, begin=codigo[0], end=codigo[1] - 1)
        b.cpu.ctl_flush_tb()

    def drenar(self):
        contagens = {self.nomes[a]: k for a, k in self.quadro.items()}
        primeiras = list(self.primeiras)
        self.quadro.clear()
        self.primeiras.clear()
        return contagens, primeiras


class Comandos:
    """Code hooks at SetPlayerOrdre / ProcessInputGame entries, at the DispatchMessageA return and at the
    CreerBatiment / MenuInit entries (checkpoint triggers)."""
    def __init__(self, b):
        from emulador import unicorn, x86
        self.b, self.eventos, self.gatilhos, self.flags = b, [], [], []
        u32 = lambda a: struct.unpack('<I', b.cpu.mem_read(a, 4))[0]

        def pacote(jogador):
            p = u32(PACOTES + 4 * jogador)
            return p, bytes(b.cpu.mem_read(p, 10))

        def regs():
            return {n: b.cpu.reg_read(getattr(x86, 'UC_X86_REG_' + n)) for n in ('EAX', 'EBX', 'ECX', 'EDX', 'ESP')}

        def set_ordre(cpu, endereco, tamanho, _):
            r = regs()
            jogador = r['EAX'] & 0xff
            ret, a6, a8 = struct.unpack('<3I', cpu.mem_read(r['ESP'], 12))
            p, antes = pacote(jogador)
            self.eventos.append(dict(event='SetPlayerOrdre', phase=b.fase, player=jogador, tag=r['EDX'] & 0xffff,
                                     word2=r['EBX'] & 0xffff, word4=r['ECX'] & 0xffff, word6=a6 & 0xffff,
                                     word8=a8 & 0xffff, caller_return=hex(ret), caller=b.nome(ret),
                                     packet_address=hex(p), packet_before=antes.hex()))

        def process(cpu, endereco, tamanho, _):
            r = regs()
            jogador = r['EAX'] & 0xff
            p, dados = pacote(jogador)
            tag = struct.unpack_from('<H', dados)[0]
            if tag == 0:
                return
            alvo = u32(TABELA_PROCESS + 4 * tag) if tag <= 0x27 else 0x45f2de
            ret = u32(r['ESP'])
            self.eventos.append(dict(event='ProcessInputGame', phase=b.fase, player=jogador, tag=tag,
                                     packet=dados.hex(), jump_target=hex(alvo), jump_target_routine=b.nome(alvo),
                                     caller_return=hex(ret), caller=b.nome(ret)))

        def despacho(cpu, endereco, tamanho, _):
            self.flags.append(bytes(cpu.mem_read(FLAGS[0], FLAGS[1] - FLAGS[0])).hex())

        def creer(cpu, endereco, tamanho, _):
            self.gatilhos.append(('CreerBatiment', b.fase))

        def menu(cpu, endereco, tamanho, _):
            if b.cpu.reg_read(x86.UC_X86_REG_EDX) & 0xff == 0x13 or b.cpu.reg_read(x86.UC_X86_REG_EAX) & 0xff == 0x13:
                self.gatilhos.append(('MenuInit13', b.fase))

        self._ganchos = (set_ordre, process, despacho, creer, menu)
        for a, f in ((SET_PLAYER_ORDRE, set_ordre), (PROCESS_INPUT_GAME, process), (RETORNO_DISPATCH, despacho),
                     (CREER_BATIMENT, creer), (MENU_INIT, menu)):
            b.cpu.hook_add(unicorn.UC_HOOK_CODE, f, begin=a, end=a)
        b.cpu.ctl_flush_tb()


def objetivo(b):
    ler = lambda a, n: bytes(b.cpu.mem_read(a, n))
    r = {k: ler(a, n).hex() for k, (a, n) in OBJETIVO.items()}
    pool = ler(ESTRUTURAS, PASSO_ESTRUTURA * N_ESTRUTURAS)
    r['structures'] = [[i, pool[i * PASSO_ESTRUTURA + 4], pool[i * PASSO_ESTRUTURA + 8],
                        struct.unpack_from('<H', pool, i * PASSO_ESTRUTURA + 2)[0], pool[i * PASSO_ESTRUTURA + 5]]
                       for i in range(N_ESTRUTURAS) if pool[i * PASSO_ESTRUTURA + 5]]
    jogador = ler(0x4e2ea8, 32)
    r['food'], r['stone'], r['parts'] = (struct.unpack_from('<h', jogador, o)[0] for o in (0xa, 0x12, 2))
    r['ui'] = {hex(a): ler(a, 1)[0] for a in UI}
    base = struct.unpack('<I', ler(UNIDADES_PTR, 4))[0]
    r['units'] = {}
    for i in UNIDADES_SEGUIDAS:
        u = ler(base + i * PASSO_UNIDADE, PASSO_UNIDADE)
        r['units'][str(i)] = dict(cell=struct.unpack_from('<H', u, 0x7c)[0], state=u[2],
                                  target_b2=struct.unpack_from('<H', u, 0xb2)[0], b7=u[0xb7], b8=u[0xb8],
                                  be=u[0xbe], f110=u[0x110:0x114].hex(), sha256=hashlib.sha256(u).hexdigest()[:16])
    return r


def superficies(b):
    return {s['role']: hashlib.sha256(b.directdraw.pixels(s['role'])).hexdigest()
            for s in b.directdraw.manifesto()['surfaces']}


def amostra(b):
    from oraculo_carga_missao import DGROUP
    u32 = lambda a: struct.unpack('<I', b.cpu.mem_read(a, 4))[0]
    u16 = lambda a: struct.unpack('<H', b.cpu.mem_read(a, 2))[0]
    return dict(counter=u32(0x508f7c), game_frame=u32(0x496d40), world_rng=hex(u32(0x497164)),
                ai_rng=hex(u32(0x498db4)), crt_seed=hex(u32(u32(0x522244) + 0xc)),
                cursor=b.cpu.mem_read(0x4e1d18, 1)[0], view_origin=[u16(0x508720), u16(0x508722)],
                selection=bytes(b.cpu.mem_read(0x508728, 8)).hex(),
                dgroup_sha256=hashlib.sha256(bytes(b.cpu.mem_read(DGROUP[0], DGROUP[1] - DGROUP[0]))).hexdigest(),
                state_sha256=b.resumo_imagem(b.imagem())['sha256'])


SAIDAS = ('quadros.jsonl', 'entradas.jsonl', 'comandos.jsonl', 'fronteiras.jsonl')


def _fsync(f):
    f.flush()
    os.fsync(f.fileno())


def correr(a):
    import segmentos_quadros_missao as seg
    from encerramento_captura import encerrar_captura
    from emulador import HASH_ORIGINAL
    from oraculo_quadro_missao import nomes_fases
    entrada_bruta = Path(a.entrada).read_bytes()
    dados = json.loads(entrada_bruta)
    quadros, ate = carregar_entrada(dados)
    if a.ate:
        ate = min(ate, a.ate)
    pasta = ROOT / a.saida
    pasta.mkdir(parents=True, exist_ok=False)
    inicio = ROOT / a.inicio
    t0 = time.monotonic()
    b, at, k0 = abrir(inicio, ROOT / a.retomar if a.retomar else None)
    if a.retomar and {k: v for k, v in b.roteiro.quadros.items() if k <= k0} != {k: v for k, v in quadros.items()
                                                                               if k <= k0}:
        raise RuntimeError('The resumed snapshot was taken under another input prefix')
    b.roteiro.quadros = quadros
    cobertura = Cobertura(b)
    comandos = Comandos(b)
    pedidos = {int(k) for k in dados.get('checkpoint_frames', ())}
    manifesto_inicio = json.loads((inicio / 'manifesto.json').read_text())
    resumo = dict(
        schema='rising-lands/m3-scripted-input-run/1', evidence=False, original_sha256=HASH_ORIGINAL,
        translation_executed=False, input_file=str(Path(a.entrada).resolve().relative_to(ROOT)),
        input_sha256=hashlib.sha256(entrada_bruta).hexdigest(), input_name=dados.get('name'),
        start=dict(frame=k0, snapshot_sha256=manifesto_inicio['snapshot_sha256'],
                   frame128_summary=manifesto_inicio['frame128_summary'],
                   resumed_from=dict(path=a.retomar, sha256=hashlib.sha256((ROOT / a.retomar).read_bytes()).hexdigest())
                   if a.retomar else None),
        source_revision=subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True,
                                       text=True).stdout.strip(),
        source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in (
            'pesquisas-paralelas/missoes/m3/entrada_roteirizada.py',
            'pesquisas-paralelas/missoes/oraculo_exibicao_missao.py',
            'pesquisas-paralelas/missoes/oraculo_quadro_missao.py',
            'pesquisas-paralelas/missoes/segmentos_quadros_missao.py')},
        stop_frame=ate, status='running', snapshots={}, outputs=list(SAIDAS))
    arquivos = {n: open(pasta / n, 'x') for n in SAIDAS}
    rotinas, gatilhos_vistos, estado = {}, set(), None
    ev_fronteira = len(b.eventos_fronteira)
    # The checkpoint's routine set is not known (Missions' trace is off): first entries count from F0.
    codigo, k = 0, k0
    al_visto = False

    def escrever(nome, linha):
        arquivos[nome].write(json.dumps(linha, sort_keys=True) + '\n')

    def instantaneo(k, motivo):
        caminho = pasta / f'instantaneo-{k:05d}.pickle'
        if caminho.exists():
            resumo['snapshots'][str(k)]['reasons'].append(motivo)
            return
        resumo['snapshots'][str(k)] = dict(sha256=seg.salvar(b, caminho, k), reasons=[motivo])

    try:
        t = time.monotonic()
        for k in range(k0 + 1, ate + 1):
            entre, quadro = nomes_fases(k)
            b.roteiro.iniciar_quadro(k)
            b.executar_entre_quadros(300, k)
            sup_entre = superficies(b)
            b.executar_quadro(600, k)
            contagens, primeiras = cobertura.drenar()
            for p in primeiras:
                rotinas[p['routine']] = dict(first_frame=k, **{c: p[c] for c in ('phase', 'caller_return', 'caller')})
            despachos = list(comandos.flags)
            comandos.flags.clear()
            entradas_q = list(b.roteiro.eventos)
            b.roteiro.eventos.clear()
            i = 0
            for e in entradas_q:
                if e['kind'] == 'dispatch_message':
                    e['wndproc_flags_after'] = despachos[i]
                    i += 1
                escrever('entradas.jsonl', e)
            if i != len(despachos):
                raise RuntimeError('DispatchMessageA returns and dispatched messages differ')
            ordens = list(comandos.eventos)
            comandos.eventos.clear()
            for e in ordens:
                escrever('comandos.jsonl', dict(frame=k, **e))
            for e in b.eventos_fronteira[ev_fronteira:]:
                if e['routine'].startswith(('PlaySnd_', 'MCICD_')):
                    escrever('fronteiras.jsonl', dict(frame=k, **{c: e[c] for c in (
                        'phase', 'routine', 'caller_return', 'caller', 'registers', 'stack_words')}))
            ev_fronteira = len(b.eventos_fronteira)
            obj = objetivo(b)
            estado = dict(frame=k, seconds=round(time.monotonic() - t, 3), new_routines=primeiras,
                          entries=dict(sorted(contagens.items())), surfaces_between=sup_entre,
                          surfaces_frame=superficies(b), objective=obj, inputs=len(entradas_q),
                          orders=[e['event'] + ':' + str(e['tag']) for e in ordens], **amostra(b))
            t = time.monotonic()
            escrever('quadros.jsonl', estado)
            motivos = []
            if k in pedidos:
                motivos.append('input_file')
            if any(e['event'] == 'SetPlayerOrdre' for e in ordens):
                motivos.append('order')
            for nome, _ in comandos.gatilhos:
                if nome not in gatilhos_vistos:
                    gatilhos_vistos.add(nome)
                    motivos.append('first_' + nome)
            comandos.gatilhos.clear()
            if obj['al'] != '00' and not al_visto:
                al_visto = True
                motivos.append('first_AL_1')
            if a.instantaneo_cada and k % a.instantaneo_cada == 0:
                motivos.append('periodic')
            for m in motivos:
                instantaneo(k, m)
            if k % 100 == 0 or motivos:
                for f in arquivos.values():
                    _fsync(f)
                resumo.update(frames_run=k - k0, last_frame=k, routines_first_entered=rotinas,
                              seconds=round(time.monotonic() - t0, 1))
                seg_escrever(pasta / 'resumo.json', resumo)
        resumo['status'] = 'completed'
        instantaneo(k, 'end')
    except Exception as erro:
        codigo = 2
        resumo.update(status='stopped', stop=dict(frame=k, error=repr(erro)[:4000], traceback=traceback.format_exc(),
                                                  detail=getattr(erro, 'detalhe', None)))
    for f in arquivos.values():
        _fsync(f)
        f.close()
    resumo.update(frames_run=k - k0, last_frame=estado['frame'] if estado else k0, routines_first_entered=rotinas,
                  seconds=round(time.monotonic() - t0, 1),
                  code_unchanged=b.sha256_codigo() == b.sha256_codigo_exe)
    seg_escrever(pasta / 'resumo.json', resumo)
    print(json.dumps(dict(output=str(pasta), status=resumo['status'], frames=resumo['frames_run'],
                          new_routines=len(rotinas), seconds=resumo['seconds']), indent=1))
    encerrar_captura(codigo, pasta / 'resumo.json', *(pasta / n for n in SAIDAS))


def seg_escrever(caminho, dados):
    tmp = caminho.with_name(caminho.name + '.tmp')
    with open(tmp, 'w') as f:
        json.dump(dados, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
        _fsync(f)
    os.replace(tmp, caminho)


def comparar(a):
    """Replay check: two runs of one input give equal records once wall-clock ``seconds`` is dropped."""
    r = {}
    for nome in SAIDAS:
        linhas = []
        for pasta in (a.a, a.b):
            texto = (ROOT / pasta / nome).read_text().splitlines()
            linhas.append([json.dumps({k: v for k, v in json.loads(x).items() if k != 'seconds'}, sort_keys=True)
                           for x in texto])
        primeira = next((i for i, (x, y) in enumerate(zip(*linhas)) if x != y), None)
        r[nome] = dict(lines=[len(x) for x in linhas], equal=linhas[0] == linhas[1], first_difference=primeira)
    r['equal'] = all(v['equal'] for v in r.values())
    print(json.dumps(r, indent=1))
    return 0 if r['equal'] else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('correr')
    c.add_argument('--entrada', required=True)
    c.add_argument('--inicio', default='.local/m3/quadro128')
    c.add_argument('--saida', required=True)
    c.add_argument('--ate', type=int, help='stop earlier than the input file stop_frame')
    c.add_argument('--instantaneo-cada', type=int, default=1000)
    c.add_argument('--retomar', help='continue from a snapshot of a run of the same input file')
    d = sub.add_parser('comparar')
    d.add_argument('a')
    d.add_argument('b')
    a = ap.parse_args()
    if a.cmd == 'correr':
        return correr(a)
    return comparar(a)


if __name__ == '__main__':
    raise SystemExit(main())
