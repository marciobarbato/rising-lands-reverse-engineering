"""Probe of the MONDE01 raid unit's life after spawn (M2.3); output under .local/, not evidence.

Missions' read-only v1 bench runs the committed path (startup, MissionLoad,
load_tail, between_frames).  At frame 1's CalculGame entry u32 0x508f7c is
forced to 9000; then whole frames run natively, with the real ProgIteration and
window loop between them, so frame k runs with counter 8999+k.  Per frame the
probe records routine entry counts, the first frame of every routine not seen
before the forced frame, registers of watched routine entries, boundary events
and the raid unit's 276-byte record when it changes.  No Python translation is
imported.

    python3 -B pesquisas-paralelas/combate/sondar_vida_incursao.py --quadros 101
"""
import argparse
import json
import re
import struct
import sys
import time
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parents[1]
sys.path.insert(0, str(REPO / 'pesquisas-paralelas/missoes'))
import ambiente_missoes  # noqa: E402,F401  (Missions bootstrap: ferramentas, inputs)
import capturar_quadro_missao_original as cq  # noqa: E402
from oraculo_quadro_missao import (BancadaQuadroMissaoOriginal, CALCUL_GAME, RETORNO_CALCUL_GAME,  # noqa: E402
                                   SAIDA_LACO, nomes_fases)
import unicorn  # noqa: E402
from unicorn import x86_const as x86  # noqa: E402

from capturar_isolados_combate_quadro1 import CAPTURA  # noqa: E402

CONTADOR, CONTADOR_FORCADO = 0x508f7c, 9000
UNIDADES, UNIDADE, UNIDADE_INCURSAO = 0x4e19a0, 0x114, 16
VIGIADAS = re.compile(r'Projectile|Attaque|Degat|Cible|Deplace|Chemin|Mort|Tir|Explosion|iagUnit|Groupe|'
                      r'Monstre|StockeAction|iaProb|Sortilege|Detruit|Blesse|Engin(Set|Get)?Case')
RUIDOSAS = {'ProjectileAnim', 'Chemin_ModifieZone', 'ProjectileAvance', 'EnginGetCase'}


class BancadaVida(BancadaQuadroMissaoOriginal):
    def executar_entre_quadros_k(self, segundos, k):
        """between_frames(k >= 2): the real ProgIteration tail and window loop to the next CalculGame entry."""
        if self.cpu.reg_read(x86.UC_X86_REG_EIP) != RETORNO_CALCUL_GAME:
            raise RuntimeError('between_frames starts at ProgIteration 0x475063')
        entre, _ = nomes_fases(k)
        self._fase(entre)
        self.limite_segundos = segundos
        self.iniciar_relogio()
        self._retomando = {RETORNO_CALCUL_GAME}
        self._passar_uma_vez.add(RETORNO_CALCUL_GAME)
        regs = self._correr(entre, RETORNO_CALCUL_GAME, {}, (CALCUL_GAME, SAIDA_LACO), retomar=True)
        if regs['EIP'] != CALCUL_GAME:
            self._interromper('window_loop_exit', eip=hex(regs['EIP']))
        return regs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quadros', type=int, default=101)
    ap.add_argument('--leve', action='store_true', help='omit ProjectileAnim/Chemin_ModifieZone entry lines')
    args = ap.parse_args()
    t0 = time.monotonic()
    cap = json.loads(CAPTURA.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaVida(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    simbolos = {b.sym[n]: n for n in b.sym}
    estado = dict(contagem=Counter(), linhas=[])

    def bloco(cpu, endereco, _tamanho, _):
        nome = simbolos.get(endereco)
        if nome is None:
            return
        estado['contagem'][nome] += 1
        if VIGIADAS.search(nome) and not (args.leve and nome in RUIDOSAS):
            esp = cpu.reg_read(x86.UC_X86_REG_ESP)
            pilha = struct.unpack('<6I', bytes(cpu.mem_read(esp, 24)))
            regs = [cpu.reg_read(getattr(x86, 'UC_X86_REG_' + r)) for r in ('EAX', 'EDX', 'EBX', 'ECX')]
            estado['linhas'].append(' '.join([nome + '@' + b.nome(pilha[0])] + [f'{v:x}' for v in regs] +
                                             [f'{v:x}' for v in pilha[1:]]))

    b.cpu.hook_add(unicorn.UC_HOOK_BLOCK, bloco, begin=0x401000, end=0x493bff)
    b.cpu.ctl_flush_tb()

    def unidade():
        base = struct.unpack('<I', bytes(b.cpu.mem_read(UNIDADES, 4)))[0]
        return bytes(b.cpu.mem_read(base + UNIDADE * UNIDADE_INCURSAO, UNIDADE))

    def fechar():
        c, l = dict(estado['contagem']), list(estado['linhas'])
        estado['contagem'].clear()
        estado['linhas'].clear()
        return c, l

    b.executar_cauda_carga(600)
    vistos = set(fechar()[0])
    b.executar_entre_quadros(120)
    vistos |= set(fechar()[0])
    b.cpu.mem_write(CONTADOR, struct.pack('<I', CONTADOR_FORCADO))
    quadros, anterior, eventos = [], unidade(), len(b.eventos_fronteira)
    parada = None
    try:
        for k in range(1, args.quadros + 1):
            if k > 1:
                b.executar_entre_quadros_k(120, k)
                c, l = fechar()
            else:
                c, l = {}, []
            contador = struct.unpack('<I', bytes(b.cpu.mem_read(CONTADOR, 4)))[0]
            b.executar_quadro(300, k)
            cq_, lq = fechar()
            for n in cq_:
                c[n] = c.get(n, 0) + cq_[n]
            novos = sorted(set(c) - vistos)
            vistos |= set(c)
            u = unidade()
            quadros.append(dict(frame=k, counter=contador, new_routines=novos, counts=c, watched=l + lq,
                                boundaries=[e['routine'] for e in b.eventos_fronteira[eventos:]],
                                unit=u.hex() if u != anterior else None))
            anterior, eventos = u, len(b.eventos_fronteira)
            print(k, contador, len(novos), novos[:12], flush=True)
    except Exception as e:  # recorded, then re-raised: the probe never hides a stop
        parada = repr(e)
        raise
    finally:
        destino = REPO / '.local' / ('combat-raid-life-probe-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(json.dumps(dict(forced_counter=CONTADOR_FORCADO, stop=parada, frames=quadros,
                                           seconds=round(time.monotonic() - t0, 1)), indent=1))
        print('wrote', destino, flush=True)


if __name__ == '__main__':
    main()
