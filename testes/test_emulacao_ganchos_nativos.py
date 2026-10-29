"""Native pass-2 hooks against Missions' Python closures (opt-in: RISING_EMULAR=1).

Needs the compiled library (python3 -B ferramentas/compilar_ganchos_nativos.py):
with RISING_EMULAR=1 a missing or stale library fails these tests, it never
skips them.

* Root tracker: the C callbacks are driven directly with a scripted ESP/EIP/
  stack (fake engine API) side by side with the closures of
  ``politica_comparacao_quadros.ganchos`` (read-only) on a fake bench reading
  the same state: nested roots, a same-depth follow-on call after a root
  returns, deeper returns, re-entry after an emulation stop, access-time pops,
  multi-byte accesses, overlapping hook ranges and a seeded random walk.
* Engine registration: ``uc_hook_add`` with native callbacks on a real
  Unicorn engine.
* Short window of the real display reference (load_tail, frames 1-2): the
  Python closures and both native modes hook the same run; their aggregates
  must be equal, key order included, after every phase.
"""
import ctypes
import inspect
import os
import random
import struct
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
for caminho in (RAIZ / 'ferramentas', RAIZ / 'pesquisas-paralelas/missoes'):
    if str(caminho) not in sys.path:
        sys.path.insert(0, str(caminho))

EMULAR = os.environ.get('RISING_EMULAR') == '1'
ESP, EIP = 30, 26          # unicorn.x86_const UC_X86_REG_ESP / EIP (checked in setUpClass)
UC_HOOK_BLOCK, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE = 8, 1024, 2048
RAIZES = {'AffGame': 0x401100, 'RestoreAll': 0x401200, 'AffTerrain': 0x401300}
BASE_SUP = TAM_SUP = None


class Estado:
    """Registers and stack words shared by the fake engine and the fake bench."""

    def __init__(self):
        self.esp, self.eip, self.memoria = 0x2008000, 0x402000, {}

    def empilhar_retorno(self, esp, retorno):
        self.esp = esp
        self.memoria[esp] = retorno


class CpuFalsa:
    def __init__(self, estado):
        self.estado, self.ganchos = estado, []

    def reg_read(self, reg):
        return {ESP: self.estado.esp, EIP: self.estado.eip}[reg]

    def mem_read(self, endereco, tamanho):
        return struct.pack('<I', self.estado.memoria.get(endereco, 0))[:tamanho]

    def hook_add(self, tipo, callback, dados=None, begin=1, end=0):
        self.ganchos.append((tipo, callback, begin, end))
        return len(self.ganchos)

    def ctl_flush_tb(self):
        pass


class BancadaFalsa:
    def __init__(self, estado):
        self.cpu, self.fase, self.sym = CpuFalsa(estado), 'load_tail', dict(RAIZES)
        self.vinculos_declarados = type('V', (), {'eventos': []})()

    @staticmethod
    def nome(endereco):
        return f'rotina_{endereco >> 8:x}'


@unittest.skipUnless(EMULAR, 'Optional native: RISING_EMULAR=1')
class RastreadorRaizes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global BASE_SUP, TAM_SUP
        from unicorn import x86_const
        assert (x86_const.UC_X86_REG_ESP, x86_const.UC_X86_REG_EIP) == (ESP, EIP)
        import unicorn
        assert (unicorn.UC_HOOK_BLOCK, unicorn.UC_HOOK_MEM_READ, unicorn.UC_HOOK_MEM_WRITE) == \
            (UC_HOOK_BLOCK, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
        import ganchos_nativos
        from oraculo_exibicao_missao import BASE_SUPERFICIES, TAMANHO_SUPERFICIES
        BASE_SUP, TAM_SUP = BASE_SUPERFICIES, TAMANHO_SUPERFICIES
        cls.gn = ganchos_nativos
        cls.lib = ganchos_nativos.carregar()      # raises when missing or stale

    def montar(self, alvos):
        """Python closures and native callbacks over one scripted state."""
        import politica_comparacao_quadros as pol
        estado = Estado()
        b = BancadaFalsa(estado)
        acessos_py, superficie_py, _ = pol.ganchos(b, alvos)
        ganchos_py = b.cpu.ganchos
        bloco_py = next(cb for t, cb, _, _ in ganchos_py if t == UC_HOOK_BLOCK)
        pilha_py = inspect.getclosurevars(bloco_py).nonlocals['pilha']

        def reg_read(_uc, reg, saida):
            ctypes.c_uint64.from_address(saida).value = {ESP: estado.esp, EIP: estado.eip}[reg]
            return 0

        def mem_read(_uc, endereco, saida, tamanho):
            ctypes.memmove(saida, struct.pack('<I', estado.memoria.get(endereco, 0)), tamanho)
            return 0
        tipos = (ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p),
                 ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_uint64),
                 ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p))
        cbs = (tipos[0](reg_read), tipos[1](mem_read), tipos[2](lambda _uc: 0))
        api = tuple(ctypes.cast(c, ctypes.c_void_p).value for c in cbs)
        r = self.gn.Rastreador(None, RAIZES.values(), api=api)
        r._mantidos = cbs
        r.marcar_alvos(alvos)
        r.fase('load_tail')
        faixas = self.gn.faixas_gancho(alvos)
        for inicio, fim in faixas:
            r.somar_faixa(inicio, fim)
        self.addCleanup(r.fechar)
        lib = self.lib
        lib.ganchos_cb_bloco.argtypes = (ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint32, ctypes.c_void_p)
        for n in ('ganchos_cb_alvo', 'ganchos_cb_alvo_multiplo', 'ganchos_cb_superficie'):
            getattr(lib, n).argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_uint64, ctypes.c_int,
                                        ctypes.c_int64, ctypes.c_void_p)
        cpu = b.cpu

        class Par:
            pass
        par = Par()
        par.estado, par.b, par.r, par.pilha_py = estado, b, r, pilha_py
        par.acessos_py, par.superficie_py = acessos_py, superficie_py
        par.acessos_n, par.superficie_n = {}, {}

        def bloco(endereco):
            for t, cb, inicio, fim in ganchos_py:
                if t == UC_HOOK_BLOCK and inicio <= endereco <= fim:
                    cb(cpu, endereco, 4, None)
            if 0x401000 <= endereco <= 0x493bff:
                lib.ganchos_cb_bloco(None, endereco, 4, r.h)

        def acesso(tipo, endereco, tamanho, modo='agrupado'):
            gancho = UC_HOOK_MEM_READ if tipo == 'read' else UC_HOOK_MEM_WRITE
            dados = r.dados(tipo)
            for t, cb, inicio, fim in ganchos_py:
                if t == gancho and inicio <= endereco <= fim:
                    cb(cpu, 16 if tipo == 'read' else 17, endereco, tamanho, 0, None)
                    if modo == 'por_faixa' and inicio < BASE_SUP:
                        lib.ganchos_cb_alvo(None, 0, endereco, tamanho, 0, dados)
            if modo == 'agrupado' and faixas and faixas[0][0] <= endereco <= faixas[-1][1]:
                lib.ganchos_cb_alvo_multiplo(None, 0, endereco, tamanho, 0, dados)
            if BASE_SUP <= endereco < BASE_SUP+TAM_SUP:
                lib.ganchos_cb_superficie(None, 0, endereco, tamanho, 0, dados)

        def fase(nome):
            b.fase = nome
            r.fase(nome)
        par.bloco, par.acesso, par.fase = bloco, acesso, fase
        return par

    def conferir(self, par, contexto=''):
        self.assertEqual(par.r.pilha(), [tuple(p) for p in par.pilha_py], contexto)
        acessos, superficie = par.acessos_n, par.superficie_n     # accumulated over drains, like coletar
        par.r.drenar(acessos, superficie, par.b.nome)
        self.assertEqual(list(acessos), list(par.acessos_py), contexto)
        for a, d in par.acessos_py.items():
            self.assertEqual(list(acessos[a].items()), list(d.items()), f'{contexto} {a:#x}')
        self.assertEqual(list(superficie.items()), list(par.superficie_py.items()), contexto)
        par.r.verificar()

    def contexto_em(self, par, esp, endereco=0x4e0000):
        """Context the native and Python trackers give one access at ``endereco`` with ESP ``esp``."""
        par.estado.esp = esp
        par.consultas = getattr(par, 'consultas', 0) + 1
        par.estado.eip = 0x480000 + 0x100*par.consultas       # a new routine: the key is the last one inserted
        par.acesso('read', endereco, 1)
        chaves = list(par.acessos_py[endereco])
        return chaves[-1][1]

    def test_raizes_aninhadas_e_retornos(self):
        par = self.montar({0x4e0000})
        e = par.estado
        par.bloco(0x402000)                                  # logic
        self.assertEqual(self.contexto_em(par, 0x2008000), 'logic')
        e.empilhar_retorno(0x2007ff0, 0x402010)
        par.bloco(RAIZES['AffGame'])                         # enter AffGame
        self.assertEqual(self.contexto_em(par, 0x2007fe0), 'display')
        e.empilhar_retorno(0x2007fd0, 0x401150)
        par.bloco(RAIZES['AffTerrain'])                      # nested root
        self.assertEqual(len(par.r.pilha()), 2)
        e.esp = 0x2007fd4
        par.bloco(0x401150)                                  # AffTerrain RET lands: ESP = entry+4
        self.assertEqual(par.r.pilha(), [(0x2007ff0, 0x402010)])
        self.assertEqual(self.contexto_em(par, 0x2007fd4), 'display')
        e.esp = 0x2007ff4
        par.bloco(0x402010)                                  # AffGame returns
        self.assertEqual(par.r.pilha(), [])
        self.assertEqual(self.contexto_em(par, 0x2007ff4), 'logic')
        self.conferir(par)

    def test_chamada_seguinte_na_mesma_profundidade(self):
        """After a root's RET, a call made at the same depth is logic (the past tracker bug)."""
        par = self.montar({0x4e0000})
        e = par.estado
        e.empilhar_retorno(0x2007ff0, 0x402010)
        par.bloco(RAIZES['RestoreAll'])
        e.esp = 0x2007ff4
        par.bloco(0x402010)                                  # back in the caller
        e.empilhar_retorno(0x2007ff0, 0x402018)              # sibling call reuses the same slot
        par.bloco(0x403000)                                  # not a root
        self.assertEqual(par.r.pilha(), [])
        self.assertEqual(self.contexto_em(par, 0x2007fe8), 'logic')
        self.conferir(par)

    def test_reentrada_apos_parada_nao_duplica(self):
        par = self.montar({0x4e0000})
        e = par.estado
        e.empilhar_retorno(0x2007ff0, 0x402010)
        par.bloco(RAIZES['AffGame'])
        par.bloco(RAIZES['AffGame'])                         # same block resumed after emu_stop
        self.assertEqual(par.r.pilha(), [(0x2007ff0, 0x402010)])
        e.esp = 0x2007fe0
        e.memoria[0x2007fe0] = 0x401180
        par.bloco(RAIZES['AffGame'])                         # recursive entry: a new frame
        self.assertEqual(len(par.r.pilha()), 2)
        self.conferir(par)

    def test_acesso_desempilha_so_quando_avalia_contexto(self):
        """A target hook pops only at a watched byte; a surface hook always pops."""
        par = self.montar({0x4e0000})
        e = par.estado
        e.empilhar_retorno(0x2007ff0, 0x402010)
        par.bloco(RAIZES['AffGame'])
        e.esp = 0x2007ff8                                    # above the root entry
        par.acesso('read', 0x4dfff0, 4)                      # no target in hooked span: no pop
        par.acesso('read', 0x4dfffe, 1)                      # inside the widened range, not a target
        self.assertEqual(len(par.r.pilha()), 1)
        self.assertEqual(len(par.pilha_py), 1)
        par.acesso('write', 0x60000010, 4)                   # surface: context evaluated, pop
        self.assertEqual(par.r.pilha(), [])
        self.conferir(par)

    def test_acessos_multibyte_e_faixas_sobrepostas(self):
        alvos = {0x4e0000, 0x4e0001, 0x4e0003, 0x4e0005, 0x4e0009, 0x4e0100}
        for modo in ('agrupado', 'por_faixa'):
            par = self.montar(alvos)
            e = par.estado
            for endereco in range(0x4dfffc, 0x4e000c):
                for tamanho in (1, 2, 4, 8, 10):
                    e.eip = 0x402000 + endereco % 7 * 0x100
                    par.acesso('read', endereco, tamanho, modo)
                    par.acesso('write', endereco, tamanho, modo)
            par.fase('frame1')
            par.acesso('read', 0x4e00fe, 4, modo)
            self.assertEqual(par.r.multiplicidade(0x4e0002), 2)   # [..0x4e0001] and [0x4e0000..0x4e0003]
            self.conferir(par, modo)

    def test_caminhada_aleatoria(self):
        aleatorio = random.Random(20261029)
        alvos = {0x4e0000 + aleatorio.randrange(0x200) for _ in range(120)}
        par = self.montar(alvos)
        e = par.estado
        pilha_real = []                                      # (entry ESP, return) of the scripted calls
        raizes = list(RAIZES.values())
        for passo in range(6000):
            escolha = aleatorio.random()
            if escolha < 0.15 and e.esp > 0x2000100:         # call: a root or a plain routine
                retorno = 0x404000 + aleatorio.randrange(0x1000)
                e.empilhar_retorno(e.esp - 4 - 4*aleatorio.randrange(4), retorno)
                pilha_real.append((e.esp, retorno))
                par.bloco(aleatorio.choice(raizes) if aleatorio.random() < 0.4 else 0x405000)
            elif escolha < 0.3 and pilha_real:              # RET to the caller
                esp, retorno = pilha_real.pop()
                e.esp = esp + 4
                par.bloco(retorno)
            elif escolha < 0.35:
                par.bloco(0x406000 + aleatorio.randrange(0x100))
            elif escolha < 0.4:
                e.esp += aleatorio.choice((-8, -4, 4, 8))
            elif escolha < 0.42:
                par.fase(aleatorio.choice(('load_tail', 'between_frames1', 'frame1', 'frame2')))
            else:
                e.eip = 0x407000 + aleatorio.randrange(0x40) * 0x10
                endereco = (BASE_SUP + aleatorio.randrange(0x100) if aleatorio.random() < 0.1
                            else 0x4dfffc + aleatorio.randrange(0x210))
                par.acesso(aleatorio.choice(('read', 'write')), endereco, aleatorio.choice((1, 2, 4, 8)))
            if passo % 1000 == 999:
                self.conferir(par, f'step {passo}')
        self.conferir(par, 'end')
        contextos = {c[1] for d in par.acessos_py.values() for c in d} | {c[1] for c in par.superficie_py}
        self.assertEqual(contextos, {'display', 'logic'})
        self.assertGreater(par.r.estatisticas()['context_evaluations'], 1000)

    def test_registro_no_motor_unicorn(self):
        """uc_hook_add with native callbacks on a real engine; counts equal a Python hook."""
        import unicorn
        codigo = bytes.fromhex('31c9' '8b8100001000' '898100081000' '83c104' '81f900040000' '75e9')
        uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
        uc.mem_map(0x1000, 0x1000)
        uc.mem_map(0x100000, 0x10000)
        uc.mem_map(0x200000, 0x1000)
        uc.mem_write(0x1000, codigo)
        uc.reg_write(unicorn.x86_const.UC_X86_REG_ESP, 0x200800)
        alvos = {0x100000 + 6*i for i in range(50)} | {0x100801}
        python = {}

        def gancho(_uc, _acesso, endereco, tamanho, _valor, tipo):
            for k in range(tamanho):
                if endereco + k in alvos:
                    python[(tipo, endereco + k)] = python.get((tipo, endereco + k), 0) + 1
        r = self.gn.Rastreador(uc._uch, [0x1000])
        r.marcar_alvos(alvos)
        r.fase('x')
        for inicio, fim in self.gn.faixas_gancho(alvos):
            uc.hook_add(UC_HOOK_MEM_READ, gancho, 'read', inicio, fim)
            uc.hook_add(UC_HOOK_MEM_WRITE, gancho, 'write', inicio, fim)
            r.somar_faixa(inicio, fim)
        faixas = self.gn.faixas_gancho(alvos)
        r.adicionar_gancho(UC_HOOK_MEM_READ, 'ganchos_cb_alvo_multiplo', r.dados('read'), faixas[0][0], faixas[-1][1])
        r.adicionar_gancho(UC_HOOK_MEM_WRITE, 'ganchos_cb_alvo_multiplo', r.dados('write'), faixas[0][0],
                           faixas[-1][1])
        r.adicionar_gancho(UC_HOOK_BLOCK, 'ganchos_cb_bloco', r.h, 0x1000, 0x1fff)
        uc.emu_start(0x1000, 0x1000 + len(codigo))
        acessos, superficie = {}, {}
        r.drenar(acessos, superficie, hex)
        nativo = {}
        for a, d in acessos.items():
            for (tipo, ctx, fase, _), n in d.items():
                self.assertEqual((ctx, fase), ('display', 'x'))   # the code start is a root
                nativo[(tipo, a)] = nativo.get((tipo, a), 0) + n
        self.assertEqual(nativo, python)
        self.assertGreater(r.estatisticas()['blocks'], 0)
        r.fechar()

    def test_biblioteca_desatualizada_falha(self):
        import compilar_ganchos_nativos as comp
        with tempfile.TemporaryDirectory() as pasta:
            fonte = Path(pasta) / 'ganchos_memoria.c'
            fonte.write_bytes(comp.FONTE.read_bytes() + b'\n/* other build */\n')
            saida = comp.compilar(Path(pasta) / 'libganchos_memoria.dylib', fonte)
            with self.assertRaisesRegex(self.gn.BibliotecaNativaIndisponivel, 'stale'):
                self.gn.carregar(saida)


@unittest.skipUnless(EMULAR, 'Optional native: RISING_EMULAR=1')
class JanelaCurtaContraPython(unittest.TestCase):
    """load_tail and frames 1-2 of the display reference: Python closures and both native modes on one run."""

    QUADROS = 2

    def test_agregados_iguais_por_fase(self):
        import json
        import ganchos_nativos
        import politica_comparacao_quadros as pol
        ganchos_nativos.carregar()
        rel = json.loads((RAIZ / 'pesquisas-paralelas/missoes/validacao/'
                          'm2-2-politica-comparacao-128-quadros.json').read_text())
        # Every changed byte of the M2.2 policy (masked ranges plus compared bytes).
        alvos = {int(a, 16) for a in rel['game_logic_bytes']}
        for inicio, fim in rel['cumulative']['exclusion_mask']:
            alvos.update(range(int(inicio, 16), int(fim, 16)))
        self.assertEqual(len(alvos), rel['changed_bytes'])
        b = pol.bancada()
        try:
            py = pol.ganchos(b, alvos)
            agrupado = ganchos_nativos.ganchos_politica(b, alvos, modo='agrupado')
            por_faixa = ganchos_nativos.ganchos_politica(b, alvos, modo='por_faixa')
            fases = 0
            for fase, _ in b.executar_quadros(self.QUADROS):
                for _, _, coletar in (py, agrupado, por_faixa):
                    coletar(fase)
                for nome, (acessos, superficie, _) in (('agrupado', agrupado), ('por_faixa', por_faixa)):
                    self.assertEqual(list(acessos), list(py[0]), f'{nome} {fase}')
                    for a, d in py[0].items():
                        self.assertEqual(list(acessos[a].items()), list(d.items()), f'{nome} {fase} {a:#x}')
                    self.assertEqual(list(superficie.items()), list(py[1].items()), f'{nome} {fase}')
                fases += 1
            self.assertEqual(fases, 1 + 2*self.QUADROS)
            self.assertTrue(any(c[1] == 'display' for d in py[0].values() for c in d))
            self.assertTrue(any(c[1] == 'logic' for d in py[0].values() for c in d))
        finally:
            for _, _, coletar in (agrupado, por_faixa):
                coletar.rastreador.remover_ganchos()


if __name__ == '__main__':
    unittest.main()
