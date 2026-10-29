"""Native leaf-call bench for the economy order setters and construction gates (M3 groundwork).

It reuses Core's committed selection-orders bench (``ferramentas/bancada_selecao_ordens.py``,
docs/core/SELECTION_ORDERS.md): Missions' accepted MONDE01 display path (startup, MissionLoad,
load_tail, between_frames) is rerun and frame 1 is paused at its first ``ProcessInputGame``
entry. At the pause each declared case runs one routine natively from the exact restored state
(CPU context, DGROUP+.bss, CRT thread page, active allocations, native stack) plus its declared
byte writes and argument registers. ``PlaySnd_*`` is the frame bench's boundary (not executed,
EAX unchanged, logged). After the cases the paused state is restored and frame 1 resumes; the
run must reproduce the committed load_tail, between_frames and frame1 summaries.

One addition over Core's bench, recording only: every store carries the index of the innermost nested call open when it happened, and every
  nested call records all its exit registers. The validator uses this to hand another front's
  routine (for example PlaceBatiment) exactly what the original did inside it.

Importing this module executes nothing.
"""
import copy
from pathlib import Path
import struct
import sys
import time

RAIZ = Path(__file__).resolve().parents[2]
for _p in (RAIZ / 'ferramentas', Path(__file__).resolve().parent):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

REGS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP')


def _gravador(b, regioes, pilha, leituras):
    """Core's ``Folhas`` recorder with per-store call attribution and full nested exit registers."""
    from bancada_selecao_ordens import Folhas

    class FolhasEconomia(Folhas):
        def _bloco(self, cpu, endereco, tamanho, _):
            from unicorn import x86_const as x86
            esp = cpu.reg_read(x86.UC_X86_REG_ESP)
            while self.abertas and endereco == self.abertas[-1]['retorno'] and esp > self.abertas[-1]['esp']:
                f = self.abertas.pop()
                r = self._regs(cpu)
                self.chamadas[f['indice']][4] = hex(r['EAX'])
                self.chamadas[f['indice']].append({k: hex(r[k]) for k in REGS[:7]})
            chave = (endereco, esp)
            repetido, self.ultimo = chave == self.ultimo, chave
            if endereco not in self.simbolos or repetido or esp >= self.esp_inicial:
                return
            r = self._regs(cpu)
            retorno = struct.unpack('<I', bytes(cpu.mem_read(esp, 4)))[0]
            self.abertas.append(dict(retorno=retorno, esp=esp, indice=len(self.chamadas)))
            self.chamadas.append([len(self.abertas) - 1, self.b.nomes[endereco],
                                  {k: hex(r[k]) for k in ('EAX', 'EDX', 'EBX', 'ECX')}, self.b.nome(retorno), None])

        def _escrever(self, cpu, acesso, endereco, tamanho, valor, _):
            if self.pilha[0] <= endereco < self.pilha[1]:
                return
            super()._escrever(cpu, acesso, endereco, tamanho, valor, _)
            self.escritas[-1].append(self.abertas[-1]['indice'] if self.abertas else -1)

    return FolhasEconomia(b, regioes, pilha, leituras)


def executar(cenario, casos, observador=None, quadro_s=1800, leituras=False):
    """Run the declared ``casos`` at frame 1's first ProcessInputGame entry of ``cenario``.

    Returns (bench, cases, results, reproduction, pause, seconds). ``casos`` is a list or a
    callable(bench) evaluated at the pause; each case is a dict with ``case``, ``routine``,
    ``registers``, optional ``writes`` [(address, bytes)], ``stack`` (pushed words above the
    return slot) and ``ret_imm``."""
    import percurso_quadro1 as pq
    from oraculo_carga_missao import BancadaCargaMissaoOriginal, DADOS_THREAD_CRT, DGROUP
    from oraculo_quadro_missao import Isolamento
    from emulador import PILHA, RETORNO
    from bancada_selecao_ordens import _mudancas
    from unicorn import x86_const as x86
    b, cap = pq._bancada(cenario)
    resultados, estado = [], dict(feito=False, pausa=None)
    t0 = time.monotonic()

    class Pausa(Isolamento):
        def executar(self, regs):
            if estado['feito'] or b.fase != 'frame1':
                return
            estado['feito'] = True
            self.ativo = False
            contexto, blocos = self._salvar()
            rastro, topo, ultimo = copy.deepcopy(b.rastro), getattr(b, '_topo', None), getattr(b, '_ultimo_bloco', None)
            fronteiras = len(b.eventos_fronteira)
            a = b.arena
            regioes = ((DGROUP[0], DGROUP[1]), (DADOS_THREAD_CRT, DADOS_THREAD_CRT + 0x1000), (a.base, a.proximo),
                       (PILHA, PILHA + 0x10000))
            gravador = _gravador(b, regioes, (PILHA, PILHA + 0x10000), leituras)
            retorno_pausa = struct.unpack('<I', b.cpu.mem_read(regs['ESP'], 4))[0]
            estado['pausa'] = dict(routine=self.entradas[regs['EIP']], caller_return=hex(retorno_pausa),
                                   caller=b.nome(retorno_pausa), registers={k: hex(v) for k, v in regs.items()},
                                   state_sha256=b.resumo_imagem(blocos))
            estado['casos'] = casos(b) if callable(casos) else list(casos)
            try:
                for caso in estado['casos']:
                    self._restaurar(contexto, blocos)
                    for endereco, dados in caso.get('writes', ()):
                        b.cpu.mem_write(endereco, bytes(dados))
                    esp = regs['ESP'] - 0x100
                    palavras = [RETORNO] + list(caso.get('stack', ()))
                    b.cpu.mem_write(esp, struct.pack(f'<{len(palavras)}I', *palavras))
                    for nome, valor in caso['registers'].items():
                        b.cpu.reg_write(getattr(x86, 'UC_X86_REG_' + nome), valor & 0xffffffff)
                    b.cpu.reg_write(x86.UC_X86_REG_ESP, esp)
                    entrada = b.sym[caso['routine']]
                    antes = self._salvar()[1]
                    regs_entrada = gravador._regs(b.cpu)
                    regs_entrada['EIP'] = entrada
                    ganchos = gravador.armar(esp)
                    inicio = len(b.eventos_fronteira)
                    try:
                        b._retomando = set()
                        saida = BancadaCargaMissaoOriginal._correr(b, 'leaf', entrada, {}, (RETORNO,), retomar=True)
                    finally:
                        for g in ganchos:
                            b.cpu.hook_del(g)
                        b.cpu.ctl_flush_tb()
                    eventos = b.eventos_fronteira[inicio:]
                    del b.eventos_fronteira[inicio:]
                    depois = self._salvar()[1]
                    if gravador.abertas:
                        raise RuntimeError(f'Unclosed nested calls in case {caso["case"]}')
                    resultado = dict(
                        case=caso['case'], routine=caso['routine'], entry=hex(entrada),
                        declared_registers={k: hex(v) for k, v in caso['registers'].items()},
                        writes=[[hex(x), bytes(d).hex()] for x, d in caso.get('writes', ())],
                        stack_words=[hex(v) for v in caso.get('stack', ())],
                        entry_registers={k: hex(v) for k, v in regs_entrada.items()},
                        exit_registers={k: hex(v) for k, v in saida.items()},
                        reached_return=saida['EIP'] == RETORNO and saida['ESP'] == esp + 4 + caso.get('ret_imm', 0),
                        stores=gravador.escritas, changed_bytes=_mudancas(antes, depois), calls=gravador.chamadas,
                        boundaries=[dict(routine=e['routine'], caller=e['caller'], registers=e['registers'],
                                         stack_words=e['stack_words'], declared_eax=e['declared_eax'],
                                         stack_cleanup=e['stack_cleanup']) for e in eventos])
                    if leituras:
                        resultado['read_before_write'] = gravador.leituras_em_runs()
                    resultados.append(resultado)
                    if observador is not None:
                        observador(caso, antes, resultado)
            finally:
                self._restaurar(contexto, blocos)
                del b.eventos_fronteira[fronteiras:]
                b.rastro, b._topo, b._ultimo_bloco = rastro, topo, ultimo
                b.fase = 'frame1'
                b.windows.fase = 'frame1'
                self.ativo = True

    iso = Pausa(b, ('ProcessInputGame',))
    iso.instalar()
    referencia = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(300)),
                         ('frame1', lambda: b.executar_quadro(quadro_s))):
        correr()
        reproducao[nome] = b.resumo_imagem(b.imagem()) == referencia[nome]
    reproducao['code_unchanged'] = b.sha256_codigo() == cap['code_integrity']['after']
    reproducao['paused'] = estado['feito']
    return b, estado.get('casos', []), resultados, reproducao, estado['pausa'], round(time.monotonic() - t0, 3)
