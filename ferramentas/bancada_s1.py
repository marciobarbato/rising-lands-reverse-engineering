"""The S1 victory trajectory as a bench: Missions' scripted-input oracle resumed from S1 snapshots, observed in situ.

S1 (feat/re-missions ``82ec5ea``) wins MONDE01 on the original from the frame-128 checkpoint F0. Missions' pass-2
records run of the same input (``passo2_sondas.py registros``, Mac mini ``.local/m3/passo2/S1``) left a snapshot
every 250 frames. This module opens one of them with ``entrada_roteirizada.abrir`` (the S1 input installed, as
``passo2_sondas._abrir`` does), runs frames exactly as ``entrada_roteirizada.correr`` does, and checks every frame
against the replay-checked S1 record (``quadros.jsonl`` from the git object: counter, RNGs, DGROUP and whole-state
SHA-256), so a capture taken here is a capture of S1 itself.

Observation is in situ and passive: a code hook at each chosen routine's entry snapshots registers, the pushed
words and the whole mapped state (``imagem()`` plus the native stack page); a code hook at each static return site
of the routine (every ``call rel32`` to it, + 5) closes the case when ESP is back at entry ESP + 4 + the RET
immediate. The case gets the exit registers, every changed byte outside the stack and the declared boundary calls
made in between. Nothing is isolated or skipped: the trajectory stays S1's (the per-frame check proves it).

Snapshots are local copies (ignored ``.local/m3/``): ``quadro128/`` (the F0 checkpoint) and ``passo2/S1/``
(``instantaneo-NNNNN.pickle``). Importing this module executes nothing.
"""
import bisect
import hashlib
import io
import json
import lzma
from pathlib import Path
import struct
import subprocess
import sys

RAIZ = Path(__file__).resolve().parents[1]
MISSOES = RAIZ / 'pesquisas-paralelas/missoes'
M3 = MISSOES / 'm3'
for _p in (MISSOES, M3):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

S1_REV = '82ec5eaa98d4f212b650c2c8ce2b293a30fb50ef'
S1_QUADROS = 'pesquisas-paralelas/missoes/m3/sondas/S1/quadros.jsonl.xz'
S1_ENTRADA = M3 / 'entradas/S1.json'
INICIO = RAIZ / '.local/m3/quadro128'
INSTANTANEOS = RAIZ / '.local/m3/passo2/S1'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
CAMPOS_AMOSTRA = ('counter', 'world_rng', 'ai_rng', 'crt_seed', 'dgroup_sha256', 'state_sha256')
CODIGO = (0x401000, 0x493c00)
EXE = RAIZ.parent.parent / 'source/cd/INSTALHD/RISING.EXE'
PILHA_NATIVA, TAMANHO_PILHA = 0x2000000, 0x10000


def registros_s1():
    """{frame: record} of the replay-checked S1 capture (read from the git object)."""
    bruto = subprocess.run(['git', '-C', str(RAIZ), 'show', f'{S1_REV}:{S1_QUADROS}'], check=True,
                           capture_output=True).stdout
    saida = {}
    for linha in io.BytesIO(lzma.decompress(bruto)):
        d = json.loads(linha)
        saida[d['frame']] = {k: d[k] for k in CAMPOS_AMOSTRA + ('entries',)}
    return saida


def sitios_retorno(nomes):
    """{routine: sorted return addresses of its static ``call rel32`` sites} from RISING.EXE's code section."""
    import oraculo_carga_missao as ocm
    sym = ocm.simbolos()
    alvos = {sym[n]: n for n in nomes}
    raw = EXE.read_bytes()
    codigo = raw[0x400:0x400 + CODIGO[1] - CODIGO[0]]
    saida = {n: set() for n in nomes}
    for i in range(len(codigo) - 5):
        if codigo[i] == 0xe8:
            alvo = (CODIGO[0] + i + 5 + struct.unpack_from('<i', codigo, i + 1)[0]) & 0xffffffff
            if alvo in alvos:
                saida[alvos[alvo]].add(CODIGO[0] + i + 5)
    return {n: sorted(v) for n, v in saida.items()}


class Observacao:
    """Passive in-situ cases of ``rotinas`` ({name: RET immediate}); ``escolher(name, regs, bench)`` filters
    entries, ``ao_fechar(case, entry_blocks)`` receives each closed case (its entry state for a translation)."""

    def __init__(self, b, rotinas, escolher=None, ao_fechar=None, retornos_extra=None):
        import unicorn
        from unicorn import x86_const as x86
        self.b, self.rotinas = b, dict(rotinas)
        self.escolher, self.ao_fechar = escolher, ao_fechar
        self.abertos = []               # stack of open cases (nested observed calls allowed)
        self.ativo = True               # off while leaf variants run from a saved entry state
        self.quadro = None
        self.erros = []
        sitios = sitios_retorno(self.rotinas)
        for n, extra in (retornos_extra or {}).items():
            sitios[n] = sorted(set(sitios[n]) | set(extra))
        self.retornos = {}
        for n, rs in sitios.items():
            for r in rs:
                self.retornos.setdefault(r, set()).add(n)
        self._x86 = x86

        def entrada(cpu, endereco, tamanho, nome):
            self._entrada(nome)

        def retorno(cpu, endereco, tamanho, _):
            self._retorno(endereco)

        self._ganchos = []
        for n in self.rotinas:
            a = b.sym[n]
            self._ganchos.append(b.cpu.hook_add(unicorn.UC_HOOK_CODE, entrada, user_data=n, begin=a, end=a))
        for r in self.retornos:
            self._ganchos.append(b.cpu.hook_add(unicorn.UC_HOOK_CODE, retorno, begin=r, end=r))
        b.cpu.ctl_flush_tb()

    def imagem(self):
        return imagem(self.b)

    def _regs(self):
        cpu, x86 = self.b.cpu, self._x86
        return {k: cpu.reg_read(getattr(x86, 'UC_X86_REG_' + k)) for k in REGISTROS + ('ESP',)}

    def _entrada(self, nome):
        if not self.ativo:
            return
        b = self.b
        regs = self._regs()
        esp = regs['ESP']
        retorno = struct.unpack('<I', bytes(b.cpu.mem_read(esp, 4)))[0]
        if self.escolher is not None and not self.escolher(nome, regs, retorno, self):
            return
        if retorno not in self.retornos or nome not in self.retornos[retorno]:
            self.erros.append(dict(routine=nome, frame=self.quadro, caller_return=hex(retorno),
                                   error='return address outside the static call sites'))
            return
        n = self.rotinas[nome] // 4
        pilha = list(struct.unpack(f'<{n}I', bytes(b.cpu.mem_read(esp + 4, 4 * n)))) if n else []
        self.abertos.append(dict(routine=nome, regs=regs, retorno=retorno, pilha=pilha, blocos=self.imagem(),
                                 fronteiras=len(b.eventos_fronteira), fase=b.fase))

    def _retorno(self, endereco):
        if not self.ativo or not self.abertos:
            return
        caso = self.abertos[-1]
        esp = self.b.cpu.reg_read(self._x86.UC_X86_REG_ESP)
        if caso['retorno'] != endereco or esp != (caso['regs']['ESP'] + 4 + self.rotinas[caso['routine']]) & 0xffffffff:
            return
        self.abertos.pop()
        b = self.b
        saida = self._regs()
        depois = self.imagem()
        antes = caso['blocos']
        mudancas = []
        for nome, (base, dados) in antes.items():
            if nome == 'native_stack':
                continue
            novo = depois.get(nome)
            if novo is None or novo[0] != base or len(novo[1]) != len(dados):
                raise RuntimeError(f'{caso["routine"]}: block {nome} changed shape inside the call')
            if novo[1] != dados:
                mudancas += [[hex(base + i), dados[i], novo[1][i]] for i in range(len(dados)) if dados[i] != novo[1][i]]
        if set(depois) - set(antes):
            raise RuntimeError(f'{caso["routine"]}: blocks allocated inside the call')
        fronteiras = [dict(routine=e['routine'], caller=e['caller'], registers=e['registers'],
                           stack_words=e['stack_words'], declared_eax=e.get('declared_eax'))
                      for e in b.eventos_fronteira[caso['fronteiras']:]]
        r = caso['regs']
        registro = dict(routine=caso['routine'], kind='in_situ', frame=self.quadro, phase=caso['fase'],
                        caller_return=hex(caso['retorno']), caller=b.nome(caso['retorno']),
                        entry_registers={k: hex(r[k]) for k in REGISTROS}, esp=hex(r['ESP']),
                        stack_args=[hex(w) for w in caso['pilha']],
                        exit_registers={k: hex(saida[k]) for k in REGISTROS + ('ESP',)},
                        changed_bytes=sorted(mudancas, key=lambda x: int(x[0], 16)), boundaries=fronteiras)
        if self.ao_fechar is not None:
            self.ao_fechar(registro, antes)

    def remover(self):
        for g in self._ganchos:
            self.b.cpu.hook_del(g)
        self.b.cpu.ctl_flush_tb()
        self._ganchos = []


class BancadaS1:
    """The S1 bench from snapshot frame ``de`` (``.local/m3/passo2/S1/instantaneo-NNNNN.pickle``)."""

    def __init__(self, de, registros=None):
        import emulador  # noqa: F401  (puts .local/python, with unicorn, on sys.path)
        import entrada_roteirizada as er
        import delta_estado_missao as delta
        self.er = er
        self.registros = registros if registros is not None else registros_s1()
        quadros, self.ate = er.carregar_entrada(json.loads(S1_ENTRADA.read_bytes()))
        caminho = INSTANTANEOS / f'instantaneo-{de:05d}.pickle'
        self.instantaneo = dict(path=str(caminho.relative_to(RAIZ)),
                                sha256=hashlib.sha256(caminho.read_bytes()).hexdigest())
        self.b, _, k = er.abrir(INICIO, caminho)
        if k != de:
            raise RuntimeError(f'snapshot frame {k}, expected {de}')
        self.b.roteiro.quadros = quadros
        self.k = de
        self.eventos = delta.compactar_eventos(self.b)
        del self.b.eventos_fronteira[:]
        self.conferidos = 0
        self.conferir()

    def amostra(self):
        a = self.er.amostra(self.b)
        return {c: a[c] for c in CAMPOS_AMOSTRA}

    def conferir(self):
        """The current state equals the S1 record of frame ``k`` (counter, RNGs, DGROUP and whole state)."""
        esperado = {c: self.registros[self.k][c] for c in CAMPOS_AMOSTRA}
        atual = self.amostra()
        if atual != esperado:
            raise RuntimeError(f'frame {self.k}: state differs from the S1 record: '
                               f'{ {c: (atual[c], esperado[c]) for c in CAMPOS_AMOSTRA if atual[c] != esperado[c]} }')
        self.conferidos += 1

    def avancar(self, observacao=None, segundos=(300, 600)):
        """Run frame k + 1 (between_frames then frame) as ``entrada_roteirizada.correr`` does, then check it."""
        b, k = self.b, self.k + 1
        if observacao is not None:
            observacao.quadro = k
        b.roteiro.iniciar_quadro(k)
        b.executar_entre_quadros(segundos[0], k)
        b.executar_quadro(segundos[1], k)
        if observacao is not None and observacao.abertos:
            raise RuntimeError(f'frame {k}: observed calls still open at the frame end')
        b.roteiro.eventos.clear()
        del b.eventos_fronteira[:]
        self.eventos.descartar_ate(len(self.eventos))
        self.k = k
        self.conferir()

    def reproducao(self):
        return dict(snapshot=self.instantaneo, frames_checked=self.conferidos, last_frame=self.k,
                    code_unchanged=self.b.sha256_codigo() == self.b.sha256_codigo_exe)


def folha(b, rotina, regs, pilha=(), escritas=(), rotulo='', quadro=None):
    """The original ``rotina`` as a leaf call from the bench's current state (emulation stopped between frames),
    with ``escritas`` applied first and the pushed words ``pilha`` (``validar_fadiga_vegetacao.Execucao.folha``'s
    method). Returns (case, entry blocks); the caller restores the state afterwards."""
    from emulador import RETORNO
    from oraculo_carga_missao import BancadaCargaMissaoOriginal
    from unicorn import x86_const as x86
    for endereco, dados in escritas:
        b.cpu.mem_write(endereco, bytes(dados))
    contexto = b.cpu.context_save()
    esp = b.cpu.reg_read(x86.UC_X86_REG_ESP) - 0x100
    b.cpu.mem_write(esp, struct.pack('<I', RETORNO))
    for i, w in enumerate(pilha):
        b.cpu.mem_write(esp + 4 + 4 * i, struct.pack('<I', w & 0xffffffff))
    antes = imagem(b)
    for k in REGISTROS:
        b.cpu.reg_write(getattr(x86, 'UC_X86_REG_' + k), regs[k] & 0xffffffff)
    b.cpu.reg_write(x86.UC_X86_REG_ESP, esp)
    fase, eventos, fronteiras = b.fase, len(b.vinculos_declarados.eventos), len(b.eventos_fronteira)
    b._retomando = set()
    try:
        saida = BancadaCargaMissaoOriginal._correr(b, 'leaf', b.sym[rotina], {}, (RETORNO,), retomar=True)
    finally:
        b.fase = fase
    if saida['EIP'] != RETORNO or saida['ESP'] != esp + 4 + 4 * len(pilha):
        raise RuntimeError(f'{rotulo}: {rotina} did not return (EIP {saida["EIP"]:#x}, ESP {saida["ESP"]:#x})')
    if len(b.vinculos_declarados.eventos) != eventos:
        raise RuntimeError(f'{rotulo}: binding inside the leaf call')
    limites = [dict(routine=e['routine'], caller=e['caller'], registers=e['registers'],
                    stack_words=e['stack_words'], declared_eax=e.get('declared_eax'))
               for e in b.eventos_fronteira[fronteiras:]]
    del b.eventos_fronteira[fronteiras:]
    b.cpu.context_restore(contexto)
    depois = imagem(b)
    if set(depois) != set(antes):
        raise RuntimeError(f'{rotulo}: blocks changed')
    mudancas = []
    for nome, (base, dados) in antes.items():
        if nome != 'native_stack' and depois[nome][1] != dados:
            novo = depois[nome][1]
            mudancas += [[hex(base + i), dados[i], novo[i]] for i in range(len(dados)) if dados[i] != novo[i]]
    caso = dict(routine=rotina, label=rotulo, kind='variant', frame=quadro,
                entry_registers={k: hex(regs[k] & 0xffffffff) for k in REGISTROS}, esp=hex(esp),
                stack_args=[hex(w & 0xffffffff) for w in pilha],
                writes=[[hex(a), bytes(d).hex()] for a, d in escritas],
                exit_registers={k: hex(saida[k]) for k in REGISTROS + ('ESP',)},
                changed_bytes=sorted(mudancas, key=lambda x: int(x[0], 16)), boundaries=limites)
    return caso, antes


def imagem(b):
    blocos = b.imagem()
    blocos['native_stack'] = (PILHA_NATIVA, bytes(b.cpu.mem_read(PILHA_NATIVA, TAMANHO_PILHA)))
    return blocos


def restaurar(b, blocos):
    for base, dados in blocos.values():
        b.cpu.mem_write(base, dados)
