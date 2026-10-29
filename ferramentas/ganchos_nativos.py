"""Native pass-2 hooks of the comparison policy: loader and tracker wrapper.

The C library (``ferramentas/nativo/ganchos_memoria.c``, built by
``compilar_ganchos_nativos.py`` into ``.local/nativo/``) holds the display-root
context tracker and the access aggregates.  Its callbacks are registered on the
engine with Unicorn 2.1.4's C ``uc_hook_add`` through ctypes (the Python
binding accepts only Python callables), and they reach the engine through
function pointers taken from the binding's own ``libunicorn``.  No Python runs
per access; Python reads the aggregates once per phase (``drenar``).

Loading fails loudly (``BibliotecaNativaIndisponivel``) when the library is
missing, was built from another source or flags (stale), or the Unicorn
binding is not 2.1.4.  There is no fallback to Python hooks.

``ganchos_politica(b, alvos)`` is a drop-in for
``politica_comparacao_quadros.ganchos`` (Missions, read-only): same arguments,
same ``(acessos, superficie, coletar)`` contract, same keys, counts and key
insertion order.
"""
import ctypes
from pathlib import Path

import compilar_ganchos_nativos as compilacao

RAIZ = Path(__file__).resolve().parents[1]
VERSAO_UNICORN = '2.1.4'
TIPOS = ('read', 'write')
CONTEXTOS = ('logic', 'display')
TAB_ACESSOS, TAB_SUPERFICIE = 0, 1
ERROS = {1: 'native allocation failed', 2: 'stack read failed at a display root entry', 3: 'register read failed'}
CODIGO = (0x401000, 0x493bff)          # UC_HOOK_BLOCK range of the Python tracker
_carregadas = {}


class BibliotecaNativaIndisponivel(RuntimeError):
    """The native hook library cannot be used; nothing falls back to Python hooks."""


class ErroGanchoNativo(RuntimeError):
    """A native callback failed inside emulation (it stopped the engine)."""


def _instrucao():
    return f'build it with: python3 -B {Path(compilacao.__file__).relative_to(RAIZ)}'


def carregar(caminho=None):
    """Load and identity-check the library (cached per path)."""
    caminho = Path(caminho or compilacao.BIBLIOTECA)
    if caminho in _carregadas:
        return _carregadas[caminho]
    if not caminho.is_file():
        raise BibliotecaNativaIndisponivel(f'Native hook library {caminho} is missing; {_instrucao()}')
    esperado = f'ganchos_memoria abi=1 sha256={compilacao.identidade()}'
    lib = ctypes.CDLL(str(caminho))
    lib.ganchos_identidade.restype = ctypes.c_char_p
    obtido = lib.ganchos_identidade().decode()
    if obtido != esperado:
        raise BibliotecaNativaIndisponivel(f'Native hook library {caminho} is stale ({obtido}, expected {esperado}); '
                                           f'{_instrucao()}')
    p, u32, u64, i32 = ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint64, ctypes.c_int
    for nome, res, args in (
            ('ganchos_criar', p, (p, p, p, i32, i32)), ('ganchos_destruir', None, (p,)),
            ('ganchos_dados', p, (p, i32)), ('ganchos_definir_raizes', i32, (p, p, u32)),
            ('ganchos_marcar_alvos', i32, (p, p, u32)), ('ganchos_somar_faixa', i32, (p, u64, u64)),
            ('ganchos_multiplicidade', u32, (p, u64)), ('ganchos_definir_fase', None, (p, u32)),
            ('ganchos_tamanho', u32, (p, i32)), ('ganchos_exportar', None, (p, i32, p, p, p, p, p, p, p)),
            ('ganchos_limpar', None, (p, i32)), ('ganchos_erro', i32, (p, p)), ('ganchos_pilha', u32, (p, p, u32)),
            ('ganchos_estatisticas', None, (p, p))):
        f = getattr(lib, nome)
        f.restype, f.argtypes = res, args
    _carregadas[caminho] = lib
    return lib


def _uclib():
    import unicorn
    if unicorn.__version__ != VERSAO_UNICORN:
        raise BibliotecaNativaIndisponivel(f'Native hooks require Unicorn {VERSAO_UNICORN}, found {unicorn.__version__}')
    from unicorn.unicorn_py3 import unicorn as binding
    return binding.uclib


class Rastreador:
    """One native tracker (root stack + aggregates) bound to one engine.

    ``api`` = (reg_read, mem_read, emu_stop) C function pointers; by default
    the binding's libunicorn.  Tests may pass ctypes callbacks and a fake
    engine pointer to drive the callbacks directly.
    """

    def __init__(self, uch, raizes, *, api=None, biblioteca=None):
        from unicorn import x86_const as x86
        self.lib = carregar(biblioteca)
        if api is None:
            uclib = _uclib()
            api = tuple(ctypes.cast(getattr(uclib, n), ctypes.c_void_p).value
                        for n in ('uc_reg_read', 'uc_mem_read', 'uc_emu_stop'))
        self.uch = uch
        self.h = self.lib.ganchos_criar(api[0], api[1], api[2], x86.UC_X86_REG_ESP, x86.UC_X86_REG_EIP)
        if not self.h:
            raise MemoryError('ganchos_criar failed')
        raizes = sorted(raizes)
        self._exigir(self.lib.ganchos_definir_raizes(self.h, (ctypes.c_uint32*len(raizes))(*raizes), len(raizes)))
        self.fases, self._ids_fase = [], {}
        self.ganchos = []

    @staticmethod
    def _exigir(ok):
        if not ok:
            raise MemoryError('native hook library allocation failed')

    # ------------------------------------------------------------ setup
    def marcar_alvos(self, alvos):
        alvos = sorted(alvos)
        if alvos and not 0 <= alvos[0] <= alvos[-1] < 1 << 32:
            raise ValueError('watched addresses must be 32-bit')
        self._exigir(self.lib.ganchos_marcar_alvos(self.h, (ctypes.c_uint32*len(alvos))(*alvos), len(alvos)))

    def somar_faixa(self, inicio, fim):
        """Count one Python hook range [inicio, fim] in the multiplicity table."""
        if not self.lib.ganchos_somar_faixa(self.h, inicio, fim):
            raise ValueError(f'invalid or saturated hook range [{inicio:#x}, {fim:#x}]')

    def multiplicidade(self, endereco):
        return self.lib.ganchos_multiplicidade(self.h, endereco)

    def fase(self, valor):
        """Make ``valor`` the phase recorded by every following access."""
        i = self._ids_fase.get(valor)
        if i is None:
            i = self._ids_fase[valor] = len(self.fases)
            self.fases.append(valor)
        self.lib.ganchos_definir_fase(self.h, i)

    def ponteiro(self, nome):
        return ctypes.cast(getattr(self.lib, nome), ctypes.c_void_p).value

    def dados(self, tipo):
        return self.lib.ganchos_dados(self.h, TIPOS.index(tipo))

    def adicionar_gancho(self, tipo_uc, callback, dados, inicio, fim):
        """uc_hook_add(engine, &h, type, native callback, user data, begin, end) through the C API."""
        uclib = _uclib()
        h = ctypes.c_size_t()
        status = uclib.uc_hook_add(self.uch, ctypes.byref(h), tipo_uc, ctypes.c_void_p(self.ponteiro(callback)),
                                   ctypes.c_void_p(dados), ctypes.c_uint64(inicio), ctypes.c_uint64(fim))
        if status != 0:
            raise RuntimeError(f'uc_hook_add failed with Unicorn error {status}')
        self.ganchos.append(h.value)
        return h.value

    def remover_ganchos(self):
        uclib = _uclib()
        while self.ganchos:
            uclib.uc_hook_del(self.uch, self.ganchos.pop())

    def fechar(self):
        """Delete the engine hooks first, then free the native state."""
        if self.h:
            if self.uch is not None:
                self.remover_ganchos()
            self.lib.ganchos_destruir(self.h)
            self.h = None

    # ------------------------------------------------------------ results
    def verificar(self):
        detalhe = ctypes.c_uint64()
        erro = self.lib.ganchos_erro(self.h, ctypes.byref(detalhe))
        if erro:
            raise ErroGanchoNativo(f'{ERROS.get(erro, erro)} (detail {detalhe.value:#x})')

    def pilha(self):
        saida = (ctypes.c_uint32*512)()
        n = self.lib.ganchos_pilha(self.h, saida, 256)
        if n > 256:
            raise RuntimeError('root stack deeper than 256')
        return [(saida[2*i], saida[2*i+1]) for i in range(n)]

    def estatisticas(self):
        saida = (ctypes.c_uint64*4)()
        self.lib.ganchos_estatisticas(self.h, saida)
        return dict(zip(('blocks', 'target_callbacks', 'surface_callbacks', 'context_evaluations'), saida))

    def exportar(self, tabela, limpar=True):
        """Columns (address, eip, phase id, kind, context, wildcard, count) in first-occurrence order."""
        self.verificar()
        n = self.lib.ganchos_tamanho(self.h, tabela)
        colunas = [(ctypes.c_uint32*n)(), (ctypes.c_uint32*n)(), (ctypes.c_uint32*n)(),
                   (ctypes.c_uint8*n)(), (ctypes.c_uint8*n)(), (ctypes.c_uint8*n)(), (ctypes.c_uint64*n)()]
        if n:
            self.lib.ganchos_exportar(self.h, tabela, *colunas)
        if limpar:
            self.lib.ganchos_limpar(self.h, tabela)
        return [list(c) for c in colunas]

    def drenar(self, acessos, superficie, nome):
        """Merge the native aggregates into the Python policy dictionaries and clear them.

        ``acessos``: address -> {(kind, context, phase, routine): count};
        ``superficie``: (kind, context, phase, routine or '*') -> count;
        ``nome``: EIP -> routine name (the bench's ``nome``).
        """
        nomes = {}
        enderecos, eips, fases, tipos, ctxs, _, ns = self.exportar(TAB_ACESSOS)
        for a, eip, f, t, c, n in zip(enderecos, eips, fases, tipos, ctxs, ns):
            r = nomes.get(eip)
            if r is None:
                r = nomes[eip] = nome(eip)
            chave = (TIPOS[t], CONTEXTOS[c], self.fases[f], r)
            d = acessos.get(a)
            if d is None:
                d = acessos[a] = {}
            d[chave] = d.get(chave, 0)+n
        _, eips, fases, tipos, ctxs, curingas, ns = self.exportar(TAB_SUPERFICIE)
        for eip, f, t, c, w, n in zip(eips, fases, tipos, ctxs, curingas, ns):
            chave = (TIPOS[t], CONTEXTOS[c], self.fases[f], '*' if w else nome(eip))
            superficie[chave] = superficie.get(chave, 0)+n


# ---------------------------------------------------------------- phase mirror
def espelhar_fase(b, rastreador):
    """Mirror every assignment of ``b.fase`` into the native tracker.

    The Python closures read ``b.fase`` at each access; the native callbacks
    read the tracker's phase, so each assignment must reach it at once.  The
    bench's class is swapped (once per bench) for a subclass with a ``fase``
    property whose value stays in the instance dictionary, so snapshots and
    ``vars(b)`` are unchanged.  Several trackers may mirror the same bench.
    """
    classe = type(b)
    if '_rastreadores_fase_nativa' not in vars(classe):
        destinos = []

        def ler(self):
            return self.__dict__['fase']

        def escrever(self, valor):
            self.__dict__['fase'] = valor
            for r in destinos:
                r.fase(valor)
        classe = type(classe.__name__, (classe,), dict(fase=property(ler, escrever), _rastreadores_fase_nativa=destinos,
                                                       __module__=classe.__module__))
        b.__class__ = classe
    classe._rastreadores_fase_nativa.append(rastreador)
    rastreador.fase(b.__dict__.get('fase'))


# ---------------------------------------------------------------- policy pass 2
def faixas_gancho(alvos):
    """The Python policy's hook ranges: one [start-3, end-1] per run of watched addresses."""
    from politica_comparacao_quadro1 import faixas
    return [(inicio-3, fim-1) for inicio, fim in faixas(alvos)]


def ganchos_politica(b, alvos, *, modo='agrupado', biblioteca=None):
    """Native drop-in for ``politica_comparacao_quadros.ganchos(b, alvos)``.

    ``modo='por_faixa'`` registers one native read and one native write hook
    per Python range (the Python layout, hook for hook).  ``modo='agrupado'``
    registers one read and one write hook spanning all ranges and replays the
    Python per-range firings from the multiplicity table.  Both give the
    Python closures' keys, counts and order.
    """
    import unicorn
    from oraculo_exibicao_missao import BASE_SUPERFICIES, TAMANHO_SUPERFICIES
    from politica_comparacao_quadro1 import RAIZES_EXIBICAO
    raizes = {b.sym[r] for r in RAIZES_EXIBICAO if r in b.sym}
    r = Rastreador(b.cpu._uch, raizes, biblioteca=biblioteca)
    r.marcar_alvos(alvos)
    espelhar_fase(b, r)
    acessos, superficie = {}, {}
    faixas = faixas_gancho(alvos)
    r.adicionar_gancho(unicorn.UC_HOOK_BLOCK, 'ganchos_cb_bloco', r.h, *CODIGO)
    if modo == 'por_faixa':
        for inicio, fim in faixas:
            r.adicionar_gancho(unicorn.UC_HOOK_MEM_WRITE, 'ganchos_cb_alvo', r.dados('write'), inicio, fim)
            r.adicionar_gancho(unicorn.UC_HOOK_MEM_READ, 'ganchos_cb_alvo', r.dados('read'), inicio, fim)
    elif modo == 'agrupado':
        for inicio, fim in faixas:
            r.somar_faixa(inicio, fim)
        if faixas:
            inicio, fim = min(f[0] for f in faixas), max(f[1] for f in faixas)
            r.adicionar_gancho(unicorn.UC_HOOK_MEM_WRITE, 'ganchos_cb_alvo_multiplo', r.dados('write'), inicio, fim)
            r.adicionar_gancho(unicorn.UC_HOOK_MEM_READ, 'ganchos_cb_alvo_multiplo', r.dados('read'), inicio, fim)
    else:
        raise ValueError(f'unknown mode {modo!r}')
    for tipo, gancho in (('write', unicorn.UC_HOOK_MEM_WRITE), ('read', unicorn.UC_HOOK_MEM_READ)):
        r.adicionar_gancho(gancho, 'ganchos_cb_superficie', r.dados(tipo), BASE_SUPERFICIES,
                           BASE_SUPERFICIES+TAMANHO_SUPERFICIES-1)
    b.cpu.ctl_flush_tb()
    visto = [len(b.vinculos_declarados.eventos)]

    def coletar(fase):
        # Hook accesses of the phase first, then the binding writes: the Python insertion order.
        r.drenar(acessos, superficie, b.nome)
        for ev in b.vinculos_declarados.eventos[visto[0]:]:
            ctx = 'backend' if ev['kind'] == 'backend' or ev['name'].startswith('DDRAW.') else 'logic'
            for w in ev['memory_writes']:
                a0 = int(w['address'], 16)
                for k in range(w['size']):
                    if a0+k in alvos:
                        d = acessos.setdefault(a0+k, {})
                        chave = ('write', ctx, fase, 'binding '+ev['name'])
                        d[chave] = d.get(chave, 0)+1
                if BASE_SUPERFICIES <= a0 < BASE_SUPERFICIES+TAMANHO_SUPERFICIES:
                    chave = ('write', ctx, fase, 'binding '+ev['name'] if ctx == 'logic' else '*')
                    superficie[chave] = superficie.get(chave, 0)+1
        visto[0] = len(b.vinculos_declarados.eventos)
    coletar.rastreador = r
    return acessos, superficie, coletar
