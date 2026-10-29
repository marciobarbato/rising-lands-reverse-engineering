"""Native capture of the AffDeplaceEngin tail (tired icon, experience icon) at the M1 AffGame entry state.

Original only.  Hooks on the tail 0x413568..0x4136DC of the body routine inside the real AffGame run to the HUD
checkpoint: per unit, the entry condition (word +4 == word +0x76, life word +0x74 < 100), the life/5 parity gate,
TypeEnginSeFatigue's answer, the draw call (PasteBobCmp 0x45B247 / PastePlayerCmp 0x45C455) with its arguments, and the
experience-icon branch.  Also the surface at the checkpoint (the fixture of ``capturar_quadro_original_pixels``).

    python3 -B pesquisas-paralelas/graficos-animacao/capturar_cauda_engin.py --saida evidencias/captura-cauda-engin-m1.json
"""
import argparse, json, struct, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import capturar_quadro_original_pixels as cq
from emulador import x86
import oraculo_quadro_missao as oq

ENTRADAS = {0x413568: 'tail_entry', 0x4135f1: 'fatigue_call', 0x4135f6: 'fatigue_result', 0x41362e: 'bob_draw_owner200',
            0x413650: 'player_draw', 0x41369b: 'xp_level_result', 0x4136a7: 'xp_gain_call', 0x4136d7: 'xp_draw', 0x413655: 'xp_gate'}


class Observador:
    def __init__(self, b):
        self.b, self.eventos, self.ganchos = b, [], []
        for a in ENTRADAS:
            self.ganchos.append(b.cpu.hook_add(oq.unicorn.UC_HOOK_CODE, self.ver, None, begin=a, end=a))

    def ver(self, cpu, endereco, tamanho, _):
        r = lambda n: cpu.reg_read(getattr(x86, 'UC_X86_REG_'+n))
        esi = r('ESI')
        unidade = bytes(cpu.mem_read(esi, 0x100)) if esi else b''
        ev = dict(at=ENTRADAS[endereco], unit_ptr=hex(esi), regs={n: r(n) & 0xffffffff for n in ('EAX', 'EBX', 'ECX', 'EDX', 'EDI')})
        if unidade:
            ev['unit'] = dict(owner=unidade[0], type=unidade[1], state=unidade[2], w4=struct.unpack_from('<H', unidade, 4)[0],
                              life74=struct.unpack_from('<H', unidade, 0x74)[0], w76=struct.unpack_from('<H', unidade, 0x76)[0],
                              ba=unidade[0xba])
        self.eventos.append(ev)

    def resultado(self):
        return self.eventos


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--saida', required=True); a = ap.parse_args()
    rs = cq.capturar(1, observador=Observador)
    r = rs[0]
    out = dict(schema='rising-lands/engin-tail-capture/1', stop=r['parou_em'], phase=r['fase'], events=r['observado'],
               surface_at_checkpoint_sha256=cq.sha(r['pixels_depois']))
    Path(a.saida).write_text(json.dumps(out, indent=1))
    print(len(out['events']), 'events', out['surface_at_checkpoint_sha256'][:12])
