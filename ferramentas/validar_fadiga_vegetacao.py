"""EnginSetFatigue, ChercheVegetLibre, ChercheTypeBatimentProximite and EteintTerrain at their real callers (native).

Economy's hunger body (state 19) and SortieTroupe's abandonment name these Core routines; S1 enters EnginSetFatigue
(and its ChercheVegetLibre) at frame 7958. This script settles them original-first on Economy's own scenarios:
- ``fome``: Economy's hunger scenario (``capturar_alimentacao.ordens``: the work cycle plus a declared hunger of
  unit 12 at frame 1100 and unit 14 at 1150), run natively to frame ``ATE['fome']``;
- ``abandono``: Economy's sanctuary abandonment (``capturar_abandono_santuario.ordens``: the recruit takes the
  sanctuary's last colonist at frame 455, SortieTroupe calls EteintTerrain at 0x421116 with radius 10).

Bench: ``bancada_ciclo_trabalho.Ciclo`` (MONDE01 display reference, frames 0/1 reproduced), imported read-only;
only the four routines are isolated (EteintTerrain from AvanceEngin: its first ``MAX_AVANCE`` calls; from every
other caller always). Each isolated call is an in-situ case. At each
EnginSetFatigue the entries of its nested ChercheVegetLibre/ChercheTypeBatimentProximite are snapshotted (whole
state and registers). From the snapshots the declared variants (``variantes_*``) run the ORIGINAL routine natively as
leaf calls, with declared writes and registers (stack words pushed as the callers push them); the isolation restores
the state afterwards, so the trajectory is the scenario's.

``--capturar <file>`` writes the original-only capture (no translation imported). The default mode reruns natively,
checks every native case against the committed capture, and compares each with ``fadiga_vegetacao`` over a copy of
the case's exact entry state (stack included, with the case's ESP): EAX..EBP and ESP, every byte of every block, and
the sound request (PlaySnd_PostSound, a declared frame boundary: arguments and pushed volume; its declared EAX is
what the translation's ``som`` returns). Economy's TestRessource is its committed ``ordens_economia`` translation.

``--fontes-economia DIR`` puts DIR first on ``sys.path`` (copies of Economy files from a branch not yet on main);
the hashes of the Economy modules actually imported are recorded either way.

    python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_fadiga_vegetacao.py --cenario fome \\
        --capturar evidencias/fadiga-vegetacao/captura-fome.json.xz
    python3 "…/heavy_lease.py" core -- python3 -B ferramentas/validar_fadiga_vegetacao.py --cenario fome
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import struct
import subprocess
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'ferramentas', RAIZ / 'pesquisas-paralelas/economia'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
M32 = 0xffffffff
ROTINAS = ('EnginSetFatigue', 'ChercheVegetLibre', 'ChercheTypeBatimentProximite', 'EteintTerrain')
# Isolated by the bench (plain RET). ChercheVegetLibre ends with RET 4, which the bench's isolation does not model:
# its calls outside EnginSetFatigue are snapshotted at entry by a code hook and run as leaf calls from the snapshot at
# the start of the next frame's declared actions (state restored afterwards).
ISOLADAS = ('EnginSetFatigue', 'ChercheTypeBatimentProximite', 'EteintTerrain')
RETORNO_FADIGA_CVL = 0x453bef            # EnginSetFatigue's own ChercheVegetLibre (covered by its nested snapshot)
MAX_CVL_POR_SITIO = 6
PILHA = {'ChercheVegetLibre': 1}
ANINHADAS = ('ChercheVegetLibre', 'ChercheTypeBatimentProximite')
ATE = {'fome': 1200, 'abandono': 470}
MODULO = {'fome': 'capturar_alimentacao', 'abandono': 'capturar_abandono_santuario'}
RETORNO_AVANCE = 0x448923                # AvanceEngin's EteintTerrain call 0x44891e + 5
MAX_AVANCE = 4
PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
ESTRUTURAS = 0x49a0c8
GRADE_OBJETOS, LARGURA, ALTURA = 0x507d74, 0x497168, 0x49716a
JOGADOR_LOCAL, GRADES_DESCOBERTA = 0x508041, 0x507d78
RECURSOS = 0x4e2ea8
BUSCA_UNIDADE, BUSCA_OCUPADA, BUSCA_SUCESSO, BUSCA_ROTA = 0x496304, 0x4e0f36, 0x4e0f37, 0x4e0f3c
FONTES = ('ferramentas/validar_fadiga_vegetacao.py', 'ferramentas/fadiga_vegetacao.py',
          'ferramentas/visao_movimento.py', 'ferramentas/mundo_vivo.py', 'ferramentas/chamadas_quadro_core.py',
          'ferramentas/selecao_ordens.py', 'ferramentas/construcao_core.py')
MODULOS_ECONOMIA = ('bancada_ciclo_trabalho', 'capturar_ciclo_trabalho', 'capturar_alimentacao',
                    'capturar_abandono_santuario', 'capturar_caverna_recrutamento', 'ordens_economia')


def captura_padrao(cenario):
    return RAIZ / f'evidencias/fadiga-vegetacao/captura-{cenario}.json.xz'


def relatorio_padrao(cenario):
    return RAIZ / f'relatorios/fadiga-vegetacao-{cenario}-emulada.json'


def fontes_economia():
    saida = {}
    for nome in MODULOS_ECONOMIA:
        if nome in sys.modules:
            arquivo = Path(sys.modules[nome].__file__).resolve()
            try:
                rotulo = str(arquivo.relative_to(RAIZ))
            except ValueError:
                rotulo = f'pesquisas-paralelas/economia/{arquivo.name} (override {arquivo})'
            saida[nome] = dict(path=rotulo, sha256=hashlib.sha256(arquivo.read_bytes()).hexdigest())
    return saida


# ------------------------------------------------------------------ native runs
class Execucao:
    """One scenario run: in-situ isolated calls, nested snapshots, declared leaf variants."""

    def __init__(self, cenario, traduzir=None):
        self.cenario, self.traduzir = cenario, traduzir
        self.casos, self.avance = [], 0
        self.snapshots, self.ganchos = {}, []
        self.luz_feita = set()
        self.pendentes, self.cvl_sitios, self.em_folha = [], {}, False
        self.ciclo = None

    # -- helpers over the live bench
    def _imagem(self):
        from emulador import PILHA as PILHA_NATIVA
        b = self.ciclo.b
        blocos = b.imagem()
        blocos['native_stack'] = (PILHA_NATIVA, bytes(b.cpu.mem_read(PILHA_NATIVA, 0x10000)))
        return blocos

    def _restaurar(self, blocos):
        b = self.ciclo.b
        for base, dados in blocos.values():
            b.cpu.mem_write(base, dados)

    def folha(self, rotina, regs, pilha=(), escritas=(), rotulo=''):
        """The original ``rotina`` as a leaf from the current state with ``escritas`` applied first; returns
        (case, entry blocks)."""
        from bancada_ciclo_trabalho import _mudancas
        from emulador import RETORNO
        from oraculo_carga_missao import BancadaCargaMissaoOriginal
        from unicorn import x86_const as x86
        b = self.ciclo.b
        for endereco, dados in escritas:
            b.cpu.mem_write(endereco, bytes(dados))
        contexto = b.cpu.context_save()
        esp = b.cpu.reg_read(x86.UC_X86_REG_ESP) - 0x100
        b.cpu.mem_write(esp, struct.pack('<I', RETORNO))
        for i, w in enumerate(pilha):
            b.cpu.mem_write(esp + 4 + 4 * i, struct.pack('<I', w & M32))
        antes = self._imagem()
        for k in REGISTROS:
            b.cpu.reg_write(getattr(x86, 'UC_X86_REG_' + k), regs[k] & M32)
        b.cpu.reg_write(x86.UC_X86_REG_ESP, esp)
        fase, eventos, fronteiras = b.fase, len(b.vinculos_declarados.eventos), len(b.eventos_fronteira)
        b._retomando = set()
        self.em_folha = True
        try:
            saida = BancadaCargaMissaoOriginal._correr(b, 'leaf', b.sym[rotina], {}, (RETORNO,), retomar=True)
        finally:
            b.fase = fase
            self.em_folha = False
        if saida['EIP'] != RETORNO or saida['ESP'] != esp + 4 + 4 * len(pilha):
            raise RuntimeError(f'{rotulo}: {rotina} did not return (EIP {saida["EIP"]:#x}, ESP {saida["ESP"]:#x})')
        if len(b.vinculos_declarados.eventos) != eventos:
            raise RuntimeError(f'{rotulo}: binding inside the leaf call')
        limites = [dict(routine=e['routine'], caller=e['caller'], registers=e['registers'],
                        stack_words=e['stack_words'], declared_eax=e['declared_eax'])
                   for e in b.eventos_fronteira[fronteiras:]]
        del b.eventos_fronteira[fronteiras:]
        b.cpu.context_restore(contexto)
        depois = self._imagem()
        if set(depois) != set(antes):
            raise RuntimeError(f'{rotulo}: blocks changed')
        caso = dict(routine=rotina, label=rotulo, kind='variant', frame=self.ciclo.k,
                    entry_registers={k: hex(regs[k] & M32) for k in REGISTROS}, esp=hex(esp),
                    stack_args=[hex(w & M32) for w in pilha],
                    writes=[[hex(a), bytes(d).hex()] for a, d in escritas],
                    exit_registers={k: hex(saida[k]) for k in REGISTROS + ('ESP',)},
                    changed_bytes=_mudancas(antes, depois, estrito=False), boundaries=limites)
        return caso, antes

    def registrar(self, caso, antes):
        if self.traduzir is not None:
            caso['comparison'] = self.traduzir(caso, antes)
        self.casos.append(caso)

    # -- isolation callbacks
    def escolher(self, nome, regs, c):
        if nome == 'EteintTerrain':
            retorno = c.u32(regs['ESP'])
            if retorno == RETORNO_AVANCE:
                if self.avance >= MAX_AVANCE:
                    return False
                self.avance += 1
            return True
        if nome == 'EnginSetFatigue':
            import unicorn
            from unicorn import x86_const as x86
            b = c.b
            self.snapshots = {}

            def instantaneo(alvo):
                def f(cpu, endereco, tamanho, _):
                    if alvo not in self.snapshots:
                        r = {k: cpu.reg_read(getattr(x86, 'UC_X86_REG_' + k)) for k in REGISTROS + ('ESP',)}
                        self.snapshots[alvo] = (r, self._imagem())
                return f
            for alvo in ANINHADAS:
                a = b.sym[alvo]
                self.ganchos.append(b.cpu.hook_add(unicorn.UC_HOOK_CODE, instantaneo(alvo), begin=a, end=a))
        return True

    def observador(self, nome, regs, blocos, resultado):
        b = self.ciclo.b
        if self.ganchos:
            for g in self.ganchos:
                b.cpu.hook_del(g)
            b.cpu.ctl_flush_tb()
            self.ganchos = []
        # the stack words as they were at entry (the isolation's blocks hold the entry state)
        base_pilha, dados_pilha = blocos['native_stack']
        pilha = [struct.unpack_from('<I', dados_pilha, regs['ESP'] + 4 + 4 * i - base_pilha)[0]
                 for i in range(PILHA.get(nome, 0))]
        caso = dict(routine=nome, label=f'{nome} in situ from {resultado["caller"]}', kind='in_situ',
                    frame=resultado['frame'], caller=resultado['caller'], caller_return=resultado['caller_return'],
                    entry_registers={k: hex(regs[k]) for k in REGISTROS}, esp=hex(regs['ESP']),
                    stack_args=[hex(w) for w in pilha], writes=[],
                    exit_registers={k: resultado['exit_registers'][k] for k in REGISTROS + ('ESP',)},
                    changed_bytes=resultado['changed_bytes'],
                    boundaries=[dict(routine=e['routine'], caller=e['caller'], registers=e['registers'],
                                     stack_words=e['stack_words'], declared_eax=e['declared_eax'])
                                for e in resultado['boundaries']],
                    nested=[c.get('routine') if isinstance(c, dict) else c for c in resultado['calls']][:40])
        self.registrar(caso, blocos)
        if nome == 'EnginSetFatigue':
            self._variantes_fadiga(regs, blocos)
            for alvo, (r, img) in sorted(self.snapshots.items()):
                self._restaurar(img)
                if alvo == 'ChercheVegetLibre':
                    self._variantes_vegetacao(r, img)
                else:
                    self._variantes_proximidade(r, img)
            self._variantes_proximidade_diretas(regs, blocos)
        elif nome == 'EteintTerrain' and resultado['caller_return'] not in self.luz_feita:
            self.luz_feita.add(resultado['caller_return'])       # variants once per caller site
            self._variantes_luz(regs, blocos, resultado)
        self._restaurar(blocos)

    def _rodar(self, rotina, regs, pilha=(), escritas=(), rotulo='', blocos=None):
        if blocos is not None:
            self._restaurar(blocos)
        caso, antes = self.folha(rotina, regs, pilha, escritas, rotulo)
        self.registrar(caso, antes)

    # -- declared variants
    def _unidade(self, regs):
        c = self.ciclo
        u = regs['EAX'] & 0xffff
        return u, c.u32(PONTEIRO_UNIDADES) + PASSO * u

    def _sem_sacos(self, centro, raio=24):
        """Writes clearing the food-sack object bytes 0x43 within ``raio`` of ``centro``."""
        c = self.ciclo
        obj = c.u32(GRADE_OBJETOS)
        larg, alt = c.u16(LARGURA), c.u16(ALTURA)
        x, y = centro & 0xff, centro >> 8
        escritas = []
        for yy in range(max(0, y - raio), min(alt, y + raio + 1)):
            for xx in range(max(0, x - raio), min(larg, x + raio + 1)):
                a = obj + yy * 256 + xx
                if c.u8(a) == 0x43:
                    escritas.append((a, b'\x00'))
        return escritas

    def _variantes_fadiga(self, regs, blocos):
        c = self.ciclo
        u, rec = self._unidade(regs)
        r0 = {k: regs[k] for k in REGISTROS}
        dono, celula = c.u8(rec), c.u16(rec + 8)
        sem = self._sem_sacos(celula)
        comida = RECURSOS + 32 * dono + 8 * 1 + 2
        caves = [ESTRUTURAS + PASSO * s for s in range(1000)
                 if c.u8(ESTRUTURAS + PASSO * s + 5) and c.u8(ESTRUTURAS + PASSO * s + 8) == 3
                 and c.u8(ESTRUTURAS + PASSO * s + 4) == dono]
        sem_cave = [(e + 4, b'\xc8') for e in caves]
        local = c.u8(JOGADOR_LOCAL)
        grade = c.u32(GRADES_DESCOBERTA + 4 * local)
        variantes = [
            ('word +4 = 4', [(rec + 4, struct.pack('<H', 4))]),
            ('state 19 already', [(rec + 2, b'\x13')]),
            ('unit owns the path search', [(BUSCA_UNIDADE, struct.pack('<H', u)), (BUSCA_OCUPADA, b'\x01'),
                                           (BUSCA_SUCESSO, b'\x01'), (BUSCA_ROTA, struct.pack('<I', 0x1234))]),
            ('no sack: own cave', sem),
            ('no sack: own cave, unit owns the path search',
             sem + [(BUSCA_UNIDADE, struct.pack('<H', u)), (BUSCA_OCUPADA, b'\x01')]),
            ('no sack, food 2', sem + [(comida, struct.pack('<H', 2))]),
            ('no sack, no cave, +0x74 = 0', sem + sem_cave + [(rec + 0x74, struct.pack('<H', 0))]),
            ('no sack, no cave, +0x74 = 1 (hungry voice)', sem + sem_cave + [(rec + 0x74, struct.pack('<H', 1)),
                                                                             (rec + 0x104, struct.pack('<I', M32))]),
            ('no sack, no cave, voice handle busy', sem + sem_cave + [(rec + 0x74, struct.pack('<H', 1)),
                                                                      (rec + 0x104, struct.pack('<I', 7))]),
            ('no sack, no cave, cell undiscovered', sem + sem_cave + [(rec + 0x74, struct.pack('<H', 1)),
                                                                      (grade + celula, b'\x10')]),
            ('no sack, no cave, other local player', sem + sem_cave + [(rec + 0x74, struct.pack('<H', 1)),
                                                                       (JOGADOR_LOCAL, bytes([(local + 1) & 3]))]),
            ('upper EAX bits kept', []),
        ]
        for rotulo, escritas in variantes:
            r = dict(r0, EAX=(0x5a5a0000 | u) if rotulo == 'upper EAX bits kept' else r0['EAX'])
            self._rodar('EnginSetFatigue', r, (), escritas, f'EnginSetFatigue: {rotulo}', blocos)

    def _variantes_vegetacao(self, regs, blocos):
        c = self.ciclo
        r0 = {k: regs[k] for k in REGISTROS}
        unidade = c.u32(regs['ESP'] + 4)
        celula = r0['EAX'] & 0xffff
        larg, alt = c.u16(LARGURA), c.u16(ALTURA)
        rec = c.u32(PONTEIRO_UNIDADES) + PASSO * (unidade & 0xffff)
        propria = c.u16(rec + 8)
        obj_propria = c.u8(c.u32(GRADE_OBJETOS) + propria)
        casos = [('in situ', {}, unidade, [])]
        casos += [(f'radius {r}', dict(EDX=r), unidade, []) for r in (0, 1, 2, 3, 5, 8, 10, 30, 40)]
        casos += [(f'bounds {lo:#x}..{hi:#x}', dict(EBX=lo, ECX=hi), unidade, [])
                  for lo, hi in ((0x42, 0x43), (0x44, 0x44), (1, 0xff), (0x1d, 0x34), (0x43, 0x42))]
        for nome_c, cel in (('corner (0,0)', 0), ('corner (w-1,0)', larg - 1), ('corner (0,h-1)', (alt - 1) * 256),
                            ('corner (w-1,h-1)', (alt - 1) * 256 + larg - 1), ('top edge', larg // 2),
                            ('left edge', (alt // 2) * 256), ('right edge', (alt // 2) * 256 + larg - 1),
                            ('bottom edge', (alt - 1) * 256 + larg // 2)):
            casos.append((f'{nome_c}, radius 6, any object', dict(EAX=cel, EDX=6, EBX=1, ECX=0xff), unidade, []))
        casos.append(('own cell in range: EnginOccupeCase passes',
                      dict(EAX=propria, EDX=2, EBX=obj_propria, ECX=obj_propria), unidade, []))
        casos.append(('own cell, +0xab = 1: occupancy excluded',
                      dict(EAX=propria, EDX=2, EBX=obj_propria, ECX=obj_propria), unidade, [(rec + 0xab, b'\x01')]))
        casos.append(('own cell, state 14: occupancy excluded',
                      dict(EAX=propria, EDX=2, EBX=obj_propria, ECX=obj_propria), unidade, [(rec + 2, b'\x0e')]))
        casos.append(('upper register bits', dict(EAX=0x77770000 | celula, EDX=0x00030014, EBX=0x12345643,
                                                  ECX=0xabcd0043), unidade, []))
        for outra in (12, 13, 14):
            if outra != unidade & 0xffff and c.u8(c.u32(PONTEIRO_UNIDADES) + PASSO * outra + 1) in (0, 1, 2, 4, 5, 6,
                                                                                                    7, 8, 9, 10):
                casos.append((f'unit {outra}, radius 20, any object', dict(EBX=1, ECX=0xff), outra, []))
        for rotulo, trocas, u, escritas in casos:
            self._rodar('ChercheVegetLibre', dict(r0, **trocas), (u,), escritas, f'ChercheVegetLibre: {rotulo}',
                        blocos)

    def _variantes_proximidade(self, regs, blocos):
        r0 = {k: regs[k] for k in REGISTROS}
        self._rodar('ChercheTypeBatimentProximite', r0, (), (), 'ChercheTypeBatimentProximite: in situ (nested)',
                    blocos)

    def _variantes_proximidade_diretas(self, regs, blocos):
        c = self.ciclo
        u, rec = self._unidade(regs)
        celula, dono = c.u16(rec + 8), c.u8(rec)
        base = {k: regs[k] for k in REGISTROS}
        for rotulo, trocas in (('cave, radius 40', dict(EDX=0x28, EBX=3, ECX=dono)),
                               ('sanctuary, radius 40', dict(EDX=0x28, EBX=2, ECX=dono)),
                               ('cave, radius 3', dict(EDX=3, EBX=3, ECX=dono)),
                               ('cave, radius 0', dict(EDX=0, EBX=3, ECX=dono)),
                               ('cave of owner 1', dict(EDX=0x28, EBX=3, ECX=1)),
                               ('neutral 0xc8 structures, type 3', dict(EDX=0xff, EBX=3, ECX=0xc8)),
                               ('any type 0, radius 255', dict(EDX=0xff, EBX=0, ECX=dono)),
                               ('upper bits', dict(EDX=0x11110028, EBX=0x22220003, ECX=0x33330000 | dono))):
            r = dict(base, EAX=0x44440000 | celula, **trocas)
            self._rodar('ChercheTypeBatimentProximite', r, (), (), f'ChercheTypeBatimentProximite: {rotulo}', blocos)

    def _variantes_luz(self, regs, blocos, resultado):
        c = self.ciclo
        r0 = {k: regs[k] for k in REGISTROS}
        celula = r0['EAX'] & 0xffff
        larg, alt = c.u16(LARGURA), c.u16(ALTURA)
        origem = 'SortieTroupe' if resultado['caller_return'] == hex(0x42111b) else resultado['caller']
        casos = [(f'radius {r}', dict(EDX=r)) for r in (0, 1, 2, 5, 8, 10, 20, 23)]
        casos += [(f'owner {d}, radius 8', dict(EDX=8, EBX=d)) for d in range(4)]
        casos += [('EDX upper bits, radius 8', dict(EDX=0x00050008)), ('EDX upper bits, radius 10',
                                                                         dict(EDX=0xffff000a))]
        casos += [(f'{n}, radius 10', dict(EAX=cel, EDX=10)) for n, cel in
                  (('corner (0,0)', 0), ('corner (w-1,h-1)', (alt - 1) * 256 + larg - 1), ('left edge', celula & 0xff00),
                   ('top edge', celula & 0xff))]
        if alt < 255:
            casos += [('centre below the map, radius 2 (no row inside)', dict(EAX=255 * 256 + 10, EDX=2)),
                      (f'centre below the map, radius {256 - alt} (rows inside)',
                       dict(EAX=255 * 256 + 10, EDX=256 - alt))]
        for rotulo, trocas in casos:
            self._rodar('EteintTerrain', dict(r0, **trocas), (), (), f'EteintTerrain ({origem} state): {rotulo}',
                        blocos)

    # -- top-level ChercheVegetLibre (RET 4): entry snapshots, run at the next frame start
    def _gancho_cvl(self, cpu, endereco, tamanho, _):
        from unicorn import x86_const as x86
        if self.em_folha:
            return
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        retorno, unidade = struct.unpack('<II', bytes(cpu.mem_read(esp, 8)))
        if retorno == RETORNO_FADIGA_CVL or self.cvl_sitios.get(retorno, 0) >= MAX_CVL_POR_SITIO:
            return
        self.cvl_sitios[retorno] = self.cvl_sitios.get(retorno, 0) + 1
        r = {k: cpu.reg_read(getattr(x86, 'UC_X86_REG_' + k)) for k in REGISTROS + ('ESP',)}
        self.pendentes.append((self.ciclo.k, retorno, unidade, r, self._imagem()))

    def _processar_pendentes(self):
        if not self.pendentes:
            return
        b = self.ciclo.b
        contexto, atual = b.cpu.context_save(), self._imagem()
        try:
            for quadro, retorno, unidade, r, img in self.pendentes:
                self._restaurar(img)
                caso, antes = self.folha('ChercheVegetLibre', r, (unidade,), (),
                                         f'ChercheVegetLibre in situ from {b.nome(retorno)} (frame {quadro})')
                caso.update(kind='in_situ', frame=quadro, caller=b.nome(retorno), caller_return=hex(retorno))
                self.registrar(caso, antes)
        finally:
            self.pendentes = []
            self._restaurar(atual)
            b.cpu.context_restore(contexto)
        if self._imagem() != atual:
            raise RuntimeError('pending ChercheVegetLibre leaves did not restore the state')

    # -- run
    def executar(self):
        import importlib
        import capturar_ciclo_trabalho as cct
        from bancada_ciclo_trabalho import Ciclo
        mod = importlib.import_module(MODULO[self.cenario])
        if self.cenario == 'fome':
            ordens, gravar = mod.ordens(cct.Estado()), False
        else:
            ordens, gravar = mod.ordens(mod.Estado()), True
        def ordens_com_pendentes(c, k):
            if self._gancho is None:              # armed from frame 2, after frames 0/1 reproduce
                import unicorn
                a = c.b.sym['ChercheVegetLibre']
                self._gancho = c.b.cpu.hook_add(unicorn.UC_HOOK_CODE, self._gancho_cvl, begin=a, end=a)
            self._processar_pendentes()
            yield from ordens(c, k)
        self._gancho = None
        self.ciclo = Ciclo(ISOLADAS, self.escolher, ordens_com_pendentes, observador=self.observador,
                           gravar_acoes=gravar)
        def progresso(k, t):
            if k % 100 == 0:
                print(f'frame {k} {t:.0f}s cases {len(self.casos)}', file=sys.stderr, flush=True)
        segundos = self.ciclo.executar(ATE[self.cenario], progresso)
        self._processar_pendentes()
        return segundos


# ------------------------------------------------------------------ translation comparison
def memoria_caso(blocos):
    """(memory with the stack, copies without the stack) over copies of the entry blocks."""
    from memoria_quadro_core import MemoriaQuadro
    copias = {n: (base, bytearray(d)) for n, (base, d) in blocos.items() if n != 'native_stack'}
    segmentos = list(copias.values())
    if 'native_stack' in blocos:
        base, d = blocos['native_stack']
        segmentos.append((base, bytearray(d)))
    return MemoriaQuadro(segmentos), copias


def mudancas(blocos, copias):
    saida = []
    for nome, (base, novo) in copias.items():
        velho = blocos[nome][1]
        if novo != velho:
            saida += [[hex(base + i), velho[i], novo[i]] for i in range(len(velho)) if velho[i] != novo[i]]
    return sorted(saida, key=lambda x: int(x[0], 16))


def traduzir(caso, blocos):
    """``fadiga_vegetacao`` over a copy of the case's entry state against the native result."""
    from fadiga_vegetacao import FadigaVegetacao
    from ordens_economia import OrdensEconomia
    m, copias = memoria_caso(blocos)
    sons = []

    def externo(nome, chamada, regs):
        if nome != 'TestRessource':
            raise KeyError(nome)
        r = {k: regs.get(k, 0) for k in REGISTROS}
        r['ESP'] = 0
        return OrdensEconomia(m).chamar(nome, r, pilha=regs['_pilha'])

    def som(nome, regs, pilha):
        i = len(sons)
        sons.append(dict(routine=nome, registers={k: hex(regs[k]) for k in ('EAX', 'EDX', 'EBX', 'ECX')},
                         pushed=[hex(w) for w in pilha]))
        if i >= len(caso['boundaries']):
            raise RuntimeError('a sound request the original did not make')
        declarado = caso['boundaries'][i]['declared_eax']
        return regs['EAX'] if declarado is None else declarado     # None: the boundary leaves EAX as passed

    f = FadigaVegetacao(m, externo=externo, som=som)
    entrada = {k: int(caso['entry_registers'][k], 16) for k in REGISTROS}
    entrada['ESP'] = int(caso['esp'], 16)
    pilha = [int(w, 16) for w in caso['stack_args']]
    try:
        saida = f.chamar(caso['routine'], entrada, pilha)
    except Exception as erro:                 # a mismatch, never ignored
        return dict(ok=False, python_error=f'{type(erro).__name__}: {erro}')
    incertos = saida.get('_incertos') or {}
    nativos = {k: int(caso['exit_registers'][k], 16) for k in REGISTROS + ('ESP',)}
    dif = {k: [hex(saida[k]), hex(nativos[k])] for k in REGISTROS + ('ESP',)
           if (saida[k] ^ nativos[k]) & ~incertos.get(k, 0) & M32}
    py = mudancas(blocos, copias)
    sons_nativos = [dict(routine=e['routine'], registers=e['registers'],
                         pushed=e['stack_words'][:1]) for e in caso['boundaries']]
    ok = not dif and py == caso['changed_bytes'] and sons == sons_nativos and not incertos
    r = dict(ok=ok, register_differences=dif, changed_equal=py == caso['changed_bytes'],
             native_changed=len(caso['changed_bytes']), sounds_equal=sons == sons_nativos,
             uncertain_bits={k: hex(v) for k, v in incertos.items() if v})
    if py != caso['changed_bytes']:
        a, b = {x[0]: x for x in py}, {x[0]: x for x in caso['changed_bytes']}
        r.update(python_only=[a[k] for k in a if a[k] != b.get(k)][:16],
                 native_only=[b[k] for k in b if b[k] != a.get(k)][:16])
    if sons != sons_nativos:
        r.update(python_sounds=sons, native_sounds=sons_nativos)
    return r


def _sem_comparacao(caso):
    return {k: v for k, v in caso.items() if k != 'comparison'}


def resumo(casos):
    saida = {}
    for c in casos:
        s = saida.setdefault(c['routine'], dict(cases=0, in_situ=0, variants=0, changed_bytes=0))
        s['cases'] += 1
        s['in_situ' if c['kind'] == 'in_situ' else 'variants'] += 1
        s['changed_bytes'] += len(c['changed_bytes'])
    return saida


def capturar(cenario, saida):
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    ex = Execucao(cenario)
    segundos = ex.executar()
    if 'fadiga_vegetacao' in sys.modules:
        raise RuntimeError('The capture imported the translation')
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    dados = dict(schema='rising-lands/core-hunger-search-light-capture/1', original_sha256=HASH_ORIGINAL,
                 translation_executed=False, scenario=cenario, last_counter=ATE[cenario], source_revision=revisao,
                 capture_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 economy_sources=fontes_economia(), path_reproduction=ex.ciclo.reproducao, seconds=segundos,
                 summary=resumo(ex.casos), cases=ex.casos)
    saida.parent.mkdir(parents=True, exist_ok=True)
    bruto = (json.dumps(dados, sort_keys=True) + '\n').encode()
    saida.write_bytes(lzma.compress(bruto, preset=9))
    print(json.dumps(dict(output=str(saida), raw_sha256=hashlib.sha256(bruto).hexdigest(),
                          reproduction=ex.ciclo.reproducao, summary=dados['summary'], seconds=segundos), indent=1))
    encerrar_captura(0, saida)


def validar(cenario, captura, saida):
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ref = json.loads(lzma.decompress(captura.read_bytes()))
    ex = Execucao(cenario, traduzir=traduzir)
    segundos = ex.executar()
    registros, mismatches = [], []
    for i, caso in enumerate(ex.casos):
        cmp = caso['comparison']
        cmp['native_equals_capture'] = i < len(ref['cases']) and ref['cases'][i] == _sem_comparacao(caso)
        cmp['ok'] = cmp['ok'] and cmp['native_equals_capture']
        r = dict(routine=caso['routine'], label=caso['label'], kind=caso['kind'], frame=caso['frame'], **cmp)
        registros.append(r)
        if not r['ok']:
            mismatches.append(r)
    por_rotina = {}
    for r in registros:
        p = por_rotina.setdefault(r['routine'], dict(cases=0, mismatches=0))
        p['cases'] += 1
        p['mismatches'] += int(not r['ok'])
    relatorio = dict(
        schema='rising-lands/core-hunger-search-light-differential/1', original_sha256=HASH_ORIGINAL,
        scenario=cenario, capture=dict(path=str(captura.relative_to(RAIZ)),
                                       sha256=hashlib.sha256(captura.read_bytes()).hexdigest()),
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        economy_sources=fontes_economia(), path_reproduction=ex.ciclo.reproducao,
        comparisons=len(registros), capture_cases=len(ref['cases']), per_routine=por_rotina,
        mismatches=mismatches, changed_bytes_compared=sum(len(c['changed_bytes']) for c in ex.casos),
        cases=registros, seconds=segundos)
    ok = all(ex.ciclo.reproducao.values()) and not mismatches and len(registros) == len(ref['cases'])
    if not ok:
        saida = RAIZ / '.local/fadiga-vegetacao' / f'falha-{cenario}-{time.strftime("%Y%m%dT%H%M%S")}.json'
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'w') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), comparisons=len(registros), mismatches=len(mismatches),
                          per_routine=por_rotina, reproduction=ex.ciclo.reproducao, seconds=segundos), indent=1))
    encerrar_captura(0 if ok else 2, saida)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cenario', choices=sorted(ATE), required=True)
    ap.add_argument('--capturar', help='write the original-only capture here (relative to the repository)')
    ap.add_argument('--captura', help='committed capture to compare with (default evidencias/fadiga-vegetacao/)')
    ap.add_argument('--saida', help='report path (default relatorios/fadiga-vegetacao-<scenario>-emulada.json)')
    ap.add_argument('--fontes-economia', help='directory with Economy files to import first')
    ap.add_argument('--ate', type=int, help='last frame counter (smoke runs only; committed runs use ATE)')
    a = ap.parse_args()
    if a.ate:
        ATE[a.cenario] = a.ate
    if a.fontes_economia:
        sys.path.insert(0, str(Path(a.fontes_economia).resolve()))
    import emulador  # noqa: F401  (puts .local/python, with unicorn, on sys.path)
    if a.capturar:
        capturar(a.cenario, RAIZ / a.capturar)
    else:
        validar(a.cenario, RAIZ / a.captura if a.captura else captura_padrao(a.cenario),
                RAIZ / a.saida if a.saida else relatorio_padrao(a.cenario))


if __name__ == '__main__':
    main()
