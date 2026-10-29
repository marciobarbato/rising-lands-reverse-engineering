"""Isolated native captures that extend the domain of the RestoreAll / AffGame logic-effect providers.

Original only.  The display scenario runs to the real entry of RestoreAll (load tail) and AffGame (between frames);
at each entry the saved state is perturbed and the intact routine runs natively to its return, then the exact saved
state is restored (Missions' ``Isolamento`` mechanism, with the declared DirectDraw backend allowed inside the call).
Cases: the captured inputs, every valid 25x17 view origin on a grid, the Santuario record in each structure state,
``[0x4dfb44]=1`` and three consecutive AffGame calls (later frames at one logic state).  Per case: changed bytes in
DGROUP, the CRT thread page and every heap block, the declared-binding count and whether the routine returned.

    python3 -B pesquisas-paralelas/graficos-animacao/capturar_dominio_exibicao_isolado.py \
        --saida pesquisas-paralelas/graficos-animacao/evidencias/dominio-exibicao-isolado.json
"""
import argparse, json, struct, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'missoes'))
import ambiente_missoes
import cenarios_oraculo as cen
import oraculo_quadro_missao as oq
from emulador import x86
from mapa_memoria_m1 import carregar_json

SO_VISIVEL = '--so-visivel' in sys.argv
POOL, PASSO = 0x49a0c8, 276
LARGURA, ALTURA = 0x497168, 0x49716a


def u16(v):
    return struct.pack('<H', v)


class IsolamentoExibicao(oq.Isolamento):
    """Isolamento that lets declared bindings run and records instead of stopping."""
    def executar(self, regs):
        b, entrada = self.b, regs['EIP']
        nome, fase = self.entradas[entrada], b.fase
        retorno = struct.unpack('<I', b.cpu.mem_read(regs['ESP'], 4))[0]
        contexto, blocos = self._salvar()
        m = b.cpu.mem_read
        largura, altura = (int.from_bytes(m(a, 2), 'little') for a in (LARGURA, ALTURA))
        dd = b.directdraw
        trava0 = {k: v.bloqueada for k, v in dd.superficies.items()}
        eventos0 = len(dd.eventos)
        sup0 = bytes(m(dd.base_superficies, dd.tamanho_superficies))
        pool = bytes(m(POOL, 1000*PASSO))
        santuario = next(i for i in range(1000) if pool[i*PASSO+5] == 5) if nome in ('AffGame', 'RestoreAll') else 0
        casos = [dict(case='captured_inputs', writes=[], repeat=1)]
        for y in range(0, altura-16, max(1, (altura-17)//6)) if not SO_VISIVEL else ():
            for x in range(0, largura-24, max(1, (largura-25)//6)):
                casos.append(dict(case=f'origin_{x}_{y}', writes=[(0x508720, u16(x)), (0x508722, u16(y))], repeat=1))
        for estado in (1, 2, 3, 4, 6, 7) if not SO_VISIVEL else ():
            casos.append(dict(case=f'structure_{santuario}_state_{estado}',
                              writes=[(POOL+santuario*PASSO+5, bytes([estado]))], repeat=1))
        sx, sy = (int(a) for a in divmod(2828, 64)[::-1])    # Santuario origin cell 2828 = (12, 44)
        for ox, oy in (((4, 30), (0, 28), (12, 40), (4, 44)) if not SO_VISIVEL else tuple((x, y) for y in (0, 6, 12, 18, 24, 30, 36, 42, 47) for x in (0, 8, 16, 24, 32, 39))):
            for estado in ((3, 5, 1, 2, 4, 6, 7) if not SO_VISIVEL else (5,)):
                casos.append(dict(case=f'visible_{ox}_{oy}_structure_{santuario}_state_{estado}',
                                  writes=[(0x508720, u16(ox)), (0x508722, u16(oy)),
                                          (POOL+santuario*PASSO+5, bytes([estado]))], repeat=1))
        casos.append(dict(case='dfb44_1', writes=[(0x4dfb44, b'\x01')], repeat=1))
        if nome == 'AffGame':
            casos.append(dict(case='three_consecutive_calls', writes=[], repeat=3))
        resultados = []
        cob = {}

        def cobrir(cpu, endereco, tamanho, _):
            if endereco == 0x40816b:   # AffBatiments: mov al, [ebp+5] (structure state)
                est = cpu.mem_read(cpu.reg_read(x86.UC_X86_REG_EBP)+5, 1)[0]
                cob.setdefault('state_read', {}).setdefault(str(est), 0)
                cob['state_read'][str(est)] += 1
            else:
                cob[hex(endereco)] = cob.get(hex(endereco), 0)+1
        for a in (0x40816b, 0x408195, 0x4081ac):   # state read; state==3 branch; first cursor read site
            b.cpu.hook_add(oq.unicorn.UC_HOOK_CODE, cobrir, None, begin=a, end=a)
        self.ativo = False   # b.fase stays the real phase: declared boundaries (LoadPie...) keep their recorded skips
        pulos0, front0 = len(b.eventos_pulados), len(b.eventos_fronteira)
        try:
            for caso in casos:
                self._restaurar(contexto, blocos)
                self._restaurar_exibicao(dd, trava0, eventos0, sup0)
                for endereco, dados in caso['writes']:
                    b.cpu.mem_write(endereco, bytes(dados))
                del b.eventos_pulados[pulos0:], b.eventos_fronteira[front0:]
                antes = self._salvar()[1]
                eventos = len(b.vinculos_declarados.eventos)
                chamadas = []
                cob.clear()
                for k in range(caso['repeat']):
                    ant = self._salvar()[1]
                    b.cpu.mem_write(regs['ESP'], struct.pack('<I', retorno))
                    for n, v in regs.items():
                        if n in ('EIP', 'ESP', 'EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP'):
                            b.cpu.reg_write(getattr(x86, 'UC_X86_REG_'+n), v)
                    ganchos = [b.cpu.hook_add(oq.unicorn.UC_HOOK_CODE, b._parar_se_pedido, begin=retorno, end=retorno)]
                    b.cpu.ctl_flush_tb()
                    try:
                        b._retomando = {entrada}
                        parou = None
                        saida = oq.BancadaCargaMissaoOriginal._correr(b, 'isolated', entrada, {}, (retorno,), retomar=True)
                    except Exception as e:   # a stop of the bench is a named result, not a crash
                        parou, saida = f'{type(e).__name__}: {e}'[:300], dict(EIP=0, ESP=0, EAX=0)
                    finally:
                        for g in ganchos:
                            b.cpu.hook_del(g)
                        b.cpu.ctl_flush_tb()
                    depois = self._salvar()[1]
                    chamadas.append(dict(returned=saida['EIP'] == retorno, stopped=parou, changed=self._diff(ant, depois)))
                    if parou:
                        break
                resultados.append(dict(case=caso['case'], writes=[[hex(a), bytes(d).hex()] for a, d in caso['writes']],
                                       bindings=len(b.vinculos_declarados.eventos)-eventos, coverage=dict(cob), calls=chamadas))
        finally:
            self._restaurar(contexto, blocos)
            self._restaurar_exibicao(dd, trava0, eventos0, sup0)
            del b.eventos_pulados[pulos0:], b.eventos_fronteira[front0:]
            self.ativo = True
        self.registros.append(dict(routine=nome, structure_record=[santuario, pool[santuario*PASSO:santuario*PASSO+32].hex()], phase=fase, entry=hex(entrada), caller=b.nome(retorno),
                                   map=[largura, altura], cases=resultados))

    def _restaurar_exibicao(self, dd, trava, eventos, sup):
        for k, v in trava.items():
            dd.superficies[k].bloqueada = v
        del dd.eventos[eventos:]
        self.b.cpu.mem_write(dd.base_superficies, sup)

    @staticmethod
    def _diff(antes, depois):
        saida = {}
        for nome, (base, dados) in depois.items():
            if nome == 'native_stack':
                continue
            velho = antes[nome][1]
            if dados != velho:
                mud = [(hex(base+i), velho[i], dados[i]) for i in range(len(dados)) if dados[i] != velho[i]]
                saida[nome] = mud if nome in ('dgroup', 'crt_thread_data') else dict(changed=len(mud), first=mud[0][0])
        return saida


def principal(saida):
    cap = carregar_json(cen.caminho('exibicao', 'captura_quadro'))
    ni = cap['named_inputs']['m1']
    b, _, _ = cen.bancada('exibicao', ni['allocation_fill'], ni['clock_ms'][0])
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    iso = IsolamentoExibicao(b, ('RestoreAll', 'AffGame'))
    iso.instalar()
    b.executar_cauda_carga(1800)
    b.executar_entre_quadros(1800)
    resumo = []
    for r in iso.registros:
        for c in r['cases']:
            resumo.append((r['routine'], c['case'], [(x['returned'], bool(x['stopped'])) for x in c['calls']]))
    json.dump(dict(schema='rising-lands/display-isolated-domain/1', source_scenario='exibicao', records=iso.registros),
              open(saida, 'w'))
    print(len(iso.registros), 'records;', sum(len(r['cases']) for r in iso.registros), 'cases')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--so-visivel', action='store_true')
    principal(ap.parse_args().saida)
