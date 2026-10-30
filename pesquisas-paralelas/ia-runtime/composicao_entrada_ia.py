"""The MONDE01 frame chain behind a declared-input API: a scripted-input file replayed through the Python chain.

The input file is Missions' schema ``rising-lands/monde01-scripted-input/1`` (``pesquisas-paralelas/missoes/m3/
entrada_roteirizada.py``): per frame k the ``GetCursorPos`` answer (held until a later frame declares another;
(0, 0) before the first), the ordered ``PeekMessageA`` messages [msg, wParam, lParam] and the ``GetAsyncKeyState``
table by vkey (0 for a key not listed). Frame k is ``between_frames{k}`` + ``frame{k}``; frame k's messages are
queued when ``between_frames{k}`` starts.

Declared-input API (``RoteiroEntrada``, ``ComposicaoEntrada``):
- ``RoteiroEntrada(dados)`` validates the file (the same rules as the harness) and serves, per frame, the
  answers the original's poll sites receive: ``peek()`` (the head message or None), ``get()`` (pops it),
  ``tecla(vk)`` and ``cursor()``; every consumed answer is logged in ``eventos`` with frame, phase, site and value,
  in the harness's ``entradas.jsonl`` fields.
- ``ComposicaoEntrada(estado, captura_quadro, entrada, captura_m1, roteiro, inicio=128, alocacoes, regs_inicio)``
  extends the pinned M2.2/M2.3 ``ComposicaoQuadros`` (imported, not modified) with:
  * ``between_frames{k}``: the real ``_WinMain@16`` loop 0x4601c0. Each queued message takes one iteration:
    PeekMessageA (PM_NOREMOVE) = 1, GetMessageA (0x4601e4) = 1, TranslateMessage (0x4601f2) = 0 and
    DispatchMessageA (0x4601fc), which runs ``WndProc 0x4181a1`` (``entrada_ordens_ia.Entrada.wnd_proc``; its
    exit registers EAX = 0, ECX = lParam, EDX = wParam are the loop's), then the PlaySnd_Manage/MCICD_Manage
    boundaries at 0x46021b/0x460220 with the MSG words now on the loop's stack. The empty queue ends the loop as
    before: PeekMessageA = 0 and ProgIteration with frame k's GetCursorPos answer;
  * ``frame{k}``: CalculGame with this front's InputGame, ProcessInputGame and CalculIconeAction
    (``entrada_ordens_ia``) and their committed owners (``provedores_entrada_ia``) in place of the no-input
    translations, and EnginNextEtape's states 11 and 13 dispatched by ``construcao_entrada_ia`` (state 11 with
    Economy's CalculConstruireBatiment and the construction-progress branch); every other provider is the M2.3
    chain's.
  ``executar(n)`` yields ``dict(phase, registro, entry, exit, ordens, eventos)`` per phase: ``ordens`` are the
  SetPlayerOrdre packets (frame, player, tag, words) and the ProcessInputGame dispatches of the phase.

A provider stop propagates as ``DependenciaIA`` (never a default or an empty callback).
"""
import struct

from composicao_encadeada_ia import (JanelasDeclaradas, MemoriaMapaRapida, Registro, provedores)
from composicao_quadros_ia import ComposicaoQuadros, PRESERVADOS_CALCUL_GAME, MSG_LACO
from construcao_entrada_ia import proxima_etapa_entrada
from entrada_ordens_ia import Entrada, LIMPAR, PACOTES, Provedores
from provedores_entrada_ia import construcao_viva, provedores_vivos
from quadro_calcul_game import calcular_quadro
from reinicio_ia import DependenciaIA

ESQUEMA = 'rising-lands/monde01-scripted-input/1'
MENSAGENS = (0x100, 0x101, 0x200, 0x201, 0x202, 0x203, 0x204, 0x205)
JANELA = 0x4e27e8                     # HWND word of the MSG (declared by the harness; read from memory)


def _inteiro(v):
    return int(v, 0) if isinstance(v, str) else int(v)


class RoteiroEntrada:
    """Frame-scheduled declared answers of one scripted-input file."""

    def __init__(self, dados, inicio=128):
        if dados.get('schema') != ESQUEMA:
            raise ValueError(f'Input schema must be {ESQUEMA}')
        if dados.get('start', {}).get('frame') != inicio:
            raise ValueError(f'The input file does not start after frame {inicio}')
        self.ate = int(dados['stop_frame'])
        self.quadros = {}
        for q in dados.get('frames', ()):
            k = int(q['frame'])
            if not inicio < k <= self.ate or k in self.quadros:
                raise ValueError(f'Frame {k} outside {inicio + 1}..{self.ate} or listed twice')
            cursor = tuple(int(c) for c in q['cursor']) if q.get('cursor') is not None else None
            if cursor is not None and not (0 <= cursor[0] < 800 and 0 <= cursor[1] < 600):
                raise ValueError(f'Frame {k}: cursor {cursor} outside the screen')
            mensagens = [tuple(_inteiro(v) for v in m) for m in q.get('messages', ())]
            if any(m[0] not in MENSAGENS for m in mensagens):
                raise ValueError(f'Frame {k}: a message WndProc does not handle without DefWindowProcA')
            teclas = {_inteiro(vk): _inteiro(v) for vk, v in (q.get('keys') or {}).items()}
            self.quadros[k] = (cursor, mensagens, teclas)
        self.quadro, self.fase, self.xy, self.fila, self.teclas, self.eventos = inicio, None, (0, 0), [], {}, []

    def iniciar_quadro(self, k):
        if self.fila:
            raise RuntimeError(f'Messages of frame {self.quadro} were not consumed: {self.fila}')
        cursor, mensagens, teclas = self.quadros.get(k, (None, (), {}))
        self.quadro, self.fila, self.teclas = k, list(mensagens), dict(teclas)
        if cursor is not None:
            self.xy = cursor

    def _evento(self, tipo, sitio, **valores):
        self.eventos.append(dict(frame=self.quadro, phase=self.fase, kind=tipo, site=hex(sitio), **valores))

    def peek(self):
        self._evento('peek_message', 0x4601d8, message=list(self.fila[0]) if self.fila else None)
        return self.fila[0] if self.fila else None

    def get(self):
        m = self.fila.pop(0)
        self._evento('get_message', 0x4601eb, message=list(m))
        return m

    def cursor(self):
        self._evento('cursor', 0x47504b, x=self.xy[0], y=self.xy[1])
        return self.xy

    def tecla(self, vk, sitio=None):
        valor = self.teclas.get(vk, 0)
        self._evento('key', sitio or 0, vk=vk, value=valor)
        return valor & 0xffff


class JanelasRoteiro(JanelasDeclaradas):
    """The Windows answers of the frame phases from the scripted input (ShowCursor stays the declared 0)."""

    def __init__(self, roteiro):
        self.r = roteiro

    def tecla(self, vk):
        return self.r.tecla(vk, self.sitio)

    def cursor(self):
        return self.r.xy

    sitio = None


def affgame_com_marcador(mm, ctx, affgame):
    """AffGame (the chain's provider: Graphics' drawing domain plus ``affgame_hud_ia``) with the order-marker block
    0x417b8f..0x417c3c, which ``affgame_hud_ia`` leaves as a named stop. When u16 [0x496204] (the marker cell an
    order press stores) is not 0xffff and the HUD body runs: u16 [0x4e05ac] += 1 on an even counter byte
    (0x417be2), PastePlayerCmp draws the marker (display output, Graphics' M3.2 domain, not produced here), and at
    0x1e0a the marker ends: [0x4e05ac] = 0x1e03, [0x496204] = 0xffff (0x417c24). The provider runs with the word
    shown as 0xffff (its only use in ``affgame_hud``) and the stores follow it; no other byte is read."""
    marcador = mm.u16(0x496204)
    if marcador == 0xffff:
        return affgame(sitio=0x475063)
    mm.u16(0x496204, 0xffff)
    try:
        eax = affgame(sitio=0x475063)
    finally:
        mm.u16(0x496204, marcador)
    if ctx.raizes_nao_executadas[-1]['drew']:
        if not mm.u8(0x508f7c) & 1:
            mm.u16(0x4e05ac, mm.u16(0x4e05ac) + 1)
        if mm.u16(0x4e05ac) == 0x1e0a:
            mm.u16(0x4e05ac, 0x1e03)
            mm.u16(0x496204, 0xffff)
    return eax


class ComposicaoEntrada(ComposicaoQuadros):
    """``ComposicaoQuadros`` with the declared input of a ``RoteiroEntrada`` (see the module docstring)."""

    def __init__(self, estado, captura_quadro, entrada, captura_m1, roteiro, **kw):
        super().__init__(estado, captura_quadro, entrada, captura_m1, **kw)
        self.roteiro = roteiro
        self.palavras_msg = MSG_LACO
        self.textos = []              # TextGetMessage boundary events (frame, call site, message number)
        from inventario_ia_runtime import OriginalImage
        self.imagem = OriginalImage()

    # ---------------------------------------------------------------- between_frames{k}
    def _entre(self, regs, entradas, registro, fase):
        """``fase_entre_quadros_exibicao`` with the message loop (see the module docstring)."""
        from fundacoes_quadro import avancar_contadores_iteracao
        mm = MemoriaMapaRapida(self.mapa)
        r = dict(regs)
        p, _ = provedores(self.mapa, self.prov, mm, self.ctx, registro, JanelasDeclaradas(), self.travessias, fase,
                          regs)
        r['EAX'] = affgame_com_marcador(mm, self.ctx, p['AffGame'])
        if mm.u8(0x5099af):
            mm.u8(0x5099af, 0)
            mm.u8(0x5099ae, 0)
        if mm.u8(0x5099b2):
            mm.u8(0x5099b1, 0)
            mm.u8(0x5099b2, 0)
        point = r['ESP']
        r['EDX'], r['ECX'], r['EBX'] = entradas['salvo_edx'], entradas['salvo_ecx'], entradas['salvo_ebx']
        r['ESP'] = point + 8 + 12 + 4
        msg = r['ESP']
        entrada_wnd = Entrada(mm, Provedores({'InitGameZone': lambda eax, edx: p['InitGameZone'](
            sitio=0x4182bb, eax=eax, edx=edx)}))
        while True:
            for rotina, retorno, chamador in (('PlaySnd_Manage', 0x460220, '_WinMain@16+0xb0'),
                                              ('MCICD_Manage', 0x460225, '_WinMain@16+0xb5')):
                guardas = {'0x4e2f28': mm.u8(0x4e2f28), '0x4e2f29': mm.u8(0x4e2f29)} if rotina == 'MCICD_Manage' else {}
                registro.fronteira(rotina, retorno, chamador, {k: r[k] for k in ('EAX', 'EDX', 'EBX', 'ECX')}, guardas,
                                   palavras=self.palavras_msg)
            if r['EBX'] & 0xff != mm.u8(0x49a059):
                raise DependenciaIA('_WinMain@16 quit path', 0x460227)
            mensagem = self.roteiro.peek()
            janela = mm.u32(JANELA)
            # PeekMessageA (PM_NOREMOVE) fills the MSG with the head message as GetMessageA then does.
            corpo = None if mensagem is None else struct.pack('<IIIIIii', janela, *mensagem, 0, *self.roteiro.xy)
            registro.vinculo('USER32.PeekMessageA', (msg, r['EBX'], r['EBX'], r['EBX'], r['EBX']), 0x4601d8,
                             int(mensagem is not None), escritas=((msg, corpo),) if corpo else ())
            if mensagem is None:
                r['EAX'] = 0
                break
            m, wp, lp = self.roteiro.get()
            registro.vinculo('USER32.GetMessageA', (msg, 0, 0, 0), 0x4601eb, 1, escritas=((msg, corpo),))
            registro.vinculo('USER32.TranslateMessage', (msg,), 0x4601f9, 0)
            self.roteiro._evento('translate_message', 0x4601f9, result=0)
            registro.vinculo('USER32.DispatchMessageA', (msg,), 0x460203, 0)
            saida = entrada_wnd.wnd_proc(dict(r, EAX=msg), [janela, m, wp, lp])
            self.roteiro._evento('dispatch_message', 0x460203, message=[m, wp, lp], hwnd=janela, wndproc='0x4181a1',
                                 wndproc_flags_after=bytes(mm.u8(0x5099a8 + i) for i in range(11)).hex())
            r.update(EAX=0, ECX=saida['ECX'], EDX=saida['EDX'])
            self.palavras_msg = (janela, m, wp, lp)
        if r['EBX'] & 0xff == mm.u8(0x49a058):
            raise DependenciaIA('_WinMain@16 WaitMessage path', 0x460214)
        entradas['empilhadas'] = (r['EDX'], r['ECX'], r['EBX'])
        r['ESP'] = msg - 4 - 12 - 8
        avancar_contadores_iteracao(mm.vista(0x508f7c, 12))
        r['EBX'] = 3
        r['EDX'] = r['ESP']
        x, y = self.roteiro.cursor()
        registro.vinculo('USER32.GetCursorPos', (r['ESP'],), 0x47504b, 1, escritas=((r['ESP'], struct.pack('<ii', x, y)),))
        mm.u16(0x5099a8, x)
        mm.u16(0x5099aa, y)
        r['EAX'] = y & 0xffffffff
        r['ESP'] -= 4
        return r

    # ---------------------------------------------------------------- frame{k}
    def _quadro(self, regs, registro, fase, ordens):
        mm = MemoriaMapaRapida(self.mapa)
        janelas = JanelasRoteiro(self.roteiro)
        p, _ = provedores(self.mapa, self.prov, mm, self.ctx, registro, janelas, self.travessias, fase, regs)

        def som(nome, regs_som, pilha):
            """The sound-library boundary (PlaySnd_PostSound/StopSound), recorded as the original records it: call
            site and caller from the provider's declared call address, the pushed words (the stale caller words
            after them are not modeled), and the callee's ``ret`` cleanup of the pushed words."""
            chamada = _sitio_chamada()
            retorno, chamador = 0, None
            if chamada is not None:
                retorno = chamada + 5
                inicio, dono = self.imagem.owner(retorno)
                chamador = f'{dono}+0x{retorno - inicio:x}'
            palavras = list(pilha) + [None] * (4 - len(pilha))
            registro.fronteira(nome, retorno, chamador, regs_som, palavras=palavras, limpeza=4 * len(pilha))
            return regs_som['EAX']
        vivos = provedores_vivos(mm, janelas=_TeclasSitio(self.roteiro, registro), som=som)
        def texto(n, local):
            """TextGetMessage as Missions' declared display-scenario boundary: EAX 0, no cleanup, logged."""
            registro.fronteira('TextGetMessage', local + 5, f'InputGame+0x{local + 5 - 0x429278:x}', dict(EAX=n),
                               declarado=0)
            self.textos.append(dict(frame=self.roteiro.quadro, site=hex(local), message=n))
            return 0
        vivos.funcoes['TextGetMessage'] = texto
        e = Entrada(mm, vivos)
        e.comandos = self.ctx.comandos
        e.ordens = ordens

        def process(sitio, jogador):
            pac = mm.u32(PACOTES + 4 * (jogador & 0xff))
            etiqueta = mm.u16(pac)
            if etiqueta:
                ordens.append(dict(event='ProcessInputGame', player=jogador & 0xff, tag=etiqueta,
                                   packet=bytes(mm.u8(pac + i) for i in range(10)).hex(),
                                   jump_target=hex(LIMPAR if etiqueta > 0x27 else e.comandos[etiqueta])))
            return e.process_input_game(dict(EAX=jogador & 0xff, EBX=0, ECX=0, EDX=0, ESI=0, EDI=0, EBP=0))['EAX']
        construcao = construcao_viva(mm, som=som, provedores_nucleo=p, bonus=lambda j, t, s: p['BonusGetValEngin'](
            sitio=0x452d48, jogador=j, tipo=t, seletor=s, ecx=0))
        etapa_pinada = p['EnginNextEtape']
        p['EnginNextEtape'] = lambda sitio, unidade: proxima_etapa_entrada(
            mm, p, unidade, self.ctx.tabelas, construcao, etapa=lambda: etapa_pinada(sitio=sitio, unidade=unidade))
        p['InputGame'] = lambda sitio, jogador: e.input_game(jogador)
        p['ProcessInputGame'] = process
        p['CalculIconeAction'] = lambda sitio: e.calcul_icone_action(dict(EAX=0, EBX=0, ECX=0, EDX=0, ESI=0, EDI=0,
                                                                         EBP=0))['EAX']
        estado = mm.u8(0x4e2f78)
        mm.u16(0x49a010, 0x1dd8)
        registro.vinculo('USER32.SetCursorPos', (mm.u16(0x5099a8), mm.u16(0x5099aa)), 0x42c8a5, 1)
        if estado != 0x12:
            raise DependenciaIA(f'CalculGame state 0x{estado:x}', self.ctx.estados[estado] if estado <= 0x18 else 0x42d4e2)
        return calcular_quadro(mm, p)

    def executar(self, n):
        from oraculo_quadro_missao import nomes_fases
        palavras, entrada_anterior = (0, 0, 0), None
        for k in range(self.inicio + 1, self.inicio + n + 1):
            entre, quadro = nomes_fases(k)
            if entrada_anterior is None:
                regs = dict(self.regs_entre)
            else:
                regs = {r: entrada_anterior[r] for r in PRESERVADOS_CALCUL_GAME}
                regs.update(ESP=(entrada_anterior['ESP'] + 4) & 0xffffffff, EAX=None)
            self.roteiro.iniciar_quadro(k)
            self.roteiro.fase = entre
            inicio_eventos = len(self.roteiro.eventos)
            entradas = dict(salvo_edx=palavras[0], salvo_ecx=palavras[1], salvo_ebx=palavras[2], empilhadas=None)
            registro = Registro(entre)
            saida = self._entre(regs, entradas, registro, entre)
            palavras = entradas['empilhadas']
            yield dict(phase=entre, registro=registro, entry=regs, exit=dict(saida), ordens=[],
                       eventos=self.roteiro.eventos[inicio_eventos:])
            self.roteiro.fase = quadro
            inicio_eventos = len(self.roteiro.eventos)
            registro, ordens = Registro(quadro), []
            self.ordens_fase = ordens                  # readable after a stop inside the phase
            entrada_anterior = dict(saida)
            self._quadro(dict(saida), registro, quadro, ordens)
            yield dict(phase=quadro, registro=registro, entry=dict(saida), exit=None, ordens=ordens,
                       eventos=self.roteiro.eventos[inicio_eventos:])


def _sitio_chamada(profundidade=12):
    """The original CALL address a provider declared for a boundary it raises: Core's ``SelecaoOrdens._fronteira(
    nome, endereco, ...)`` passes the boundary to ``som`` without the site, so it is read from that frame's
    ``endereco`` argument (Core's own declared address, never inferred). None when no such frame is found."""
    import sys
    f = sys._getframe(2)
    for _ in range(profundidade):
        if f is None:
            return None
        if f.f_code.co_name == '_fronteira' and isinstance(f.f_locals.get('endereco'), int):
            return f.f_locals['endereco']
        f = f.f_back
    return None


class _TeclasSitio:
    """``janelas`` for ``provedores_vivos``: keys and cursor from the script. Each key poll is logged as an input
    event and as the ``USER32.GetAsyncKeyState`` binding (argument vk, the poll's return address, EAX = the
    declared answer & 0xffff), as the original's import binding records it."""
    def __init__(self, roteiro, registro=None):
        self.r, self.registro = roteiro, registro

    def tecla(self, vk, local):
        valor = self.r.tecla(vk, local)
        if self.registro is not None:
            self.registro.vinculo('USER32.GetAsyncKeyState', (vk,), local, valor)
        return valor

    def cursor(self):
        return self.r.xy
