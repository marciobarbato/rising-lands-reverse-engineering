"""Native bench for the structure-entry, lodging and Bag routines (M3/M4 groundwork, Economy's work cycle).

It extends ``bancada_selecao_ordens`` (Missions' accepted MONDE01 display path, paused at frame 1's first
``ProcessInputGame`` entry) with three things that bench does not need:
- **native preparation**: before a case, declared steps run ORIGINAL routines natively from the restored pause
  (stores kept, not recorded), or write named bytes. That is how the completed 0xc8 CAVE and the released
  colonist are built: ``CreerBatiment``, the progress word, ``BatimentConstruction`` and ``BatimentRetireColon``,
  the same original calls Economy's ``capturar_ciclo_trabalho`` makes at frame 2. A step may declare the EAX it
  must return (``expect_eax``); any other value stops the run;
- **body entries**: a measured step may enter mid-routine (``entry`` address, e.g. unit state 13's body
  0x4558e4 inside EnginNextEtape) with declared registers and stop at declared addresses (``stops``) instead of
  the bench return slot. Such a step pushes no return slot;
- **windows**: a case is a list of measured ``steps``, each optionally repeated; the state carries from step to
  step (as consecutive frames of one unit carry it), and every repetition is recorded and compared on its own.

Per measured step it records what ``bancada_selecao_ordens`` records (entry/exit registers, every non-stack
store, the changed bytes of every state block, the nested routine entries, the boundary events, optionally the
bytes read before written). ``observador(caso, passo, antes, resultado)`` runs after each measured step with the
state blocks at that step's entry. Importing this module executes nothing.
"""
import copy
import struct
import sys
import time

from bancada_selecao_ordens import Folhas, _mudancas


def executar(cenario, casos, observador=None, quadro_s=1800, leituras=False, progresso=False):
    """Run the declared ``casos`` at frame 1's first ProcessInputGame entry of ``cenario``.

    ``casos``: a list or a callable(bench) of dicts ``case``, optional ``preparation`` (list of
    ``{'kind': 'call', 'routine', 'registers', 'expect_eax'?}`` or ``{'kind': 'write', 'address', 'bytes'}``)
    and ``steps`` (list of ``{'routine', 'entry'?, 'stops'?, 'registers', 'writes'?, 'stack'?, 'repeat'?,
    'until'?}``). ``until`` is ``(address, width, value)``: the repetitions stop after the one that leaves
    that value (``repeat`` is then the maximum). Returns (bench, cases, results, reproduction, pause, seconds);
    each result is one measured repetition, named ``case`` (single step, single repetition) or
    ``case/step.repetition``."""
    import percurso_quadro1 as pq
    from oraculo_carga_missao import BancadaCargaMissaoOriginal, DADOS_THREAD_CRT, DGROUP
    from oraculo_quadro_missao import Isolamento
    from emulador import PILHA, RETORNO
    from unicorn import x86_const as x86
    b, cap = pq._bancada(cenario)
    resultados, estado = [], dict(feito=False, pausa=None)
    t0 = time.monotonic()

    def ler(endereco, largura):
        return int.from_bytes(bytes(b.cpu.mem_read(endereco, largura)), 'little')

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
            gravador = Folhas(b, regioes, (PILHA, PILHA + 0x10000), leituras)
            retorno_pausa = struct.unpack('<I', b.cpu.mem_read(regs['ESP'], 4))[0]
            estado['pausa'] = dict(routine=self.entradas[regs['EIP']], caller_return=hex(retorno_pausa),
                                   caller=b.nome(retorno_pausa), registers={k: hex(v) for k, v in regs.items()},
                                   state_sha256=b.resumo_imagem(blocos))
            estado['casos'] = casos(b) if callable(casos) else list(casos)

            def preparar_chamada(passo, esp):
                b.cpu.mem_write(esp, struct.pack('<I', RETORNO))
                for nome, valor in passo['registers'].items():
                    b.cpu.reg_write(getattr(x86, 'UC_X86_REG_' + nome), valor & 0xffffffff)
                b.cpu.reg_write(x86.UC_X86_REG_ESP, esp)
                b._retomando = set()
                inicio = len(b.eventos_fronteira)
                saida = BancadaCargaMissaoOriginal._correr(b, 'preparation', b.sym[passo['routine']], {}, (RETORNO,),
                                                           retomar=True)
                eventos = b.eventos_fronteira[inicio:]
                del b.eventos_fronteira[inicio:]
                if saida['EIP'] != RETORNO or saida['ESP'] != esp + 4:
                    raise RuntimeError(f'Preparation {passo["routine"]} did not return: {saida}')
                if 'expect_eax' in passo and saida['EAX'] & 0xffff != passo['expect_eax']:
                    raise RuntimeError(f'Preparation {passo["routine"]} returned EAX {saida["EAX"]:#x}, '
                                       f'declared {passo["expect_eax"]:#x}')
                return dict(routine=passo['routine'], registers={k: hex(v) for k, v in passo['registers'].items()},
                            eax=hex(saida['EAX']), boundaries=[e['routine'] for e in eventos])

            def medir(caso, passo, nome, esp):
                for endereco, dados in passo.get('writes', ()):
                    b.cpu.mem_write(endereco, bytes(dados))
                corpo = 'entry' in passo
                paradas = tuple(passo.get('stops', ())) if corpo else (RETORNO,)
                if corpo:
                    b.cpu.mem_write(esp, struct.pack('<I', RETORNO))      # sentinel only; the body never returns to it
                else:
                    palavras = [RETORNO] + list(passo.get('stack', ()))
                    b.cpu.mem_write(esp, struct.pack(f'<{len(palavras)}I', *palavras))
                for nome_r, valor in passo['registers'].items():
                    b.cpu.reg_write(getattr(x86, 'UC_X86_REG_' + nome_r), valor & 0xffffffff)
                b.cpu.reg_write(x86.UC_X86_REG_ESP, esp)
                entrada = passo['entry'] if corpo else b.sym[passo['routine']]
                antes = self._salvar()[1]
                regs_entrada = gravador._regs(b.cpu)
                regs_entrada['EIP'] = entrada
                # The oracle stops only at addresses that carry its stop hook: add one per declared stop.
                import unicorn
                ganchos = [b.cpu.hook_add(unicorn.UC_HOOK_CODE, b._parar_se_pedido, begin=p, end=p)
                           for p in (paradas if corpo else ())]
                ganchos += gravador.armar(esp + (4 if corpo else 0))
                inicio = len(b.eventos_fronteira)
                try:
                    b._retomando = set()
                    saida = BancadaCargaMissaoOriginal._correr(b, 'leaf', entrada, {}, paradas, retomar=True)
                finally:
                    for g in ganchos:
                        b.cpu.hook_del(g)
                    b.cpu.ctl_flush_tb()
                eventos = b.eventos_fronteira[inicio:]
                del b.eventos_fronteira[inicio:]
                depois = self._salvar()[1]
                if gravador.abertas:
                    raise RuntimeError(f'Unclosed nested calls in {nome}')
                if corpo:
                    chegou = saida['EIP'] in paradas and saida['ESP'] == esp
                else:
                    chegou = saida['EIP'] == RETORNO and saida['ESP'] == esp + 4 + passo.get('ret_imm', 0)
                resultado = dict(
                    case=nome, routine=passo['routine'], entry=hex(entrada),
                    stops=[hex(p) for p in paradas] if corpo else None,
                    declared_registers={k: hex(v) for k, v in passo['registers'].items()},
                    writes=[[hex(x), bytes(d).hex()] for x, d in passo.get('writes', ())],
                    stack_words=[hex(v) for v in passo.get('stack', ())],
                    entry_registers={k: hex(v) for k, v in regs_entrada.items()},
                    exit_registers={k: hex(v) for k, v in saida.items()},
                    reached_return=chegou,
                    stores=gravador.escritas, changed_bytes=_mudancas(antes, depois), calls=gravador.chamadas,
                    boundaries=[dict(routine=e['routine'], caller=e['caller'], registers=e['registers'],
                                     stack_words=e['stack_words'], declared_eax=e['declared_eax'],
                                     stack_cleanup=e['stack_cleanup']) for e in eventos])
                if leituras:
                    resultado['read_before_write'] = gravador.leituras_em_runs()
                resultados.append(resultado)
                if observador is not None:
                    observador(caso, passo, antes, resultado)
                return resultado

            try:
                for caso in estado['casos']:
                    self._restaurar(contexto, blocos)
                    esp = regs['ESP'] - 0x100
                    feitos = []
                    for passo in caso.get('preparation', ()):
                        if passo['kind'] == 'write':
                            b.cpu.mem_write(passo['address'], bytes(passo['bytes']))
                            feitos.append(dict(write=hex(passo['address']), bytes=bytes(passo['bytes']).hex()))
                        else:
                            feitos.append(preparar_chamada(passo, esp))
                    caso['_preparation_record'] = feitos
                    passos = caso['steps']
                    unico = len(passos) == 1 and passos[0].get('repeat', 1) == 1
                    for i, passo in enumerate(passos):
                        for k in range(passo.get('repeat', 1)):
                            nome = caso['case'] if unico else f"{caso['case']}/{i}.{k}"
                            if progresso:
                                print(nome, file=sys.stderr, flush=True)
                            r = medir(caso, passo, nome, esp)
                            r['preparation'] = feitos if (i, k) == (0, 0) else None
                            if 'until' in passo:
                                endereco, largura, valor = passo['until']
                                if ler(endereco, largura) == valor:
                                    break
                            if not r['reached_return']:
                                break
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
