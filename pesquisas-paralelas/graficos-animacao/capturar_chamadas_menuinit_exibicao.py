"""Native per-call capture of the display calls MenuInit makes in phase (a) of the display scenario.

Original only.  Same scenario and hooks as ``capturar_efeitos_logicos_exibicao`` with the roots DDLockSurface,
DDUnlockSurface, FilledBox, DeleteBank and DDFlipPage.  Per call (outermost root): phase, caller, entry registers and
stack arguments, return EAX, value-changing writes outside the bench stack and the declared surface, and the declared
bindings executed inside it.  DGROUP bytes are classified against Missions' comparison policy.

    python3 -B pesquisas-paralelas/graficos-animacao/capturar_chamadas_menuinit_exibicao.py \
        --saida pesquisas-paralelas/graficos-animacao/evidencias/chamadas-menuinit-exibicao.json
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import capturar_efeitos_logicos_exibicao as base
import cenarios_oraculo as cen
from emulador import unicorn, x86
from mapa_memoria_m1 import carregar_json

RAIZ = Path(__file__).resolve().parents[2]
NOMES = ('DDLockSurface', 'DDUnlockSurface', 'FilledBox', 'DeleteBank', 'DDFlipPage')
POLITICA = RAIZ/'pesquisas-paralelas/missoes/validacao/m2-politica-comparacao-quadro1.json'


def simbolos():
    saida = {}
    for linha in open(RAIZ/'relatorios/simbolos-originais.tsv'):
        p = linha.split()
        if len(p) >= 2 and p[1] in NOMES:
            saida[int(p[0], 16)] = p[1]
    return saida


class Chamadas(base.Observador):
    def __init__(self, b):
        super().__init__(b)
        self.chamadas = []

    def entrada(self, cpu, endereco, tamanho, _):
        super().entrada(cpu, endereco, tamanho, _)
        if len(self.pilha) == 1:
            if self.atual is not None:
                self.atual['sem_retorno'] = True
            esp = self.esp()
            ret = int.from_bytes(cpu.mem_read(esp, 4), 'little')
            regs = {n: cpu.reg_read(r) for n, r in (('EAX', x86.UC_X86_REG_EAX), ('EDX', x86.UC_X86_REG_EDX),
                                                    ('EBX', x86.UC_X86_REG_EBX), ('ECX', x86.UC_X86_REG_ECX))}
            args = [int.from_bytes(cpu.mem_read(esp+4+4*i, 4), 'little') for i in range(4)]
            self.atual = dict(phase=self.b.fase, root=self.pilha[0][0], caller=self.b.nome(ret-5), regs_in=regs,
                              stack_args=args, bindings=[], writes=[], eventos0=len(self.b.vinculos_declarados.eventos))
            if self.atual['root'] == 'DeleteBank':
                self.atual['bank_walk'] = self.percurso_banco(regs['EAX'])
            self.chamadas.append(self.atual)

    def percurso_banco(self, banco):
        """Free order DeleteBank 0x418a12 follows from the bank layout: u16 count, table at +4, entry +8 sub-block."""
        m = self.b.cpu.mem_read
        u32 = lambda a: int.from_bytes(m(a, 4), 'little')
        n, tabela = int.from_bytes(m(banco, 2), 'little'), u32(banco+4)
        ordem = []
        for i in range(n):
            e = u32(tabela+4*i)
            if e and u32(e+8):
                ordem.append(u32(e+8))
            if e:
                ordem.append(e)
        return dict(bank=banco, count=n, table=tabela, free_order=ordem+[tabela, banco])

    def saida(self, cpu, endereco, tamanho, _):
        fim = bool(self.pilha) and self.esp() >= self.pilha[-1][1]
        topo = len(self.pilha) == 1
        super().saida(cpu, endereco, tamanho, _)
        if fim and topo:
            ev = self.b.vinculos_declarados.eventos[self.atual.pop('eventos0'):]
            self.atual['bindings'] = [e['name'] for e in ev]
            if self.atual['root'] == 'DeleteBank':
                self.atual['freed_pointers'] = [e['arguments'][0] for e in ev if e['name'] == 'KERNEL32.GlobalHandle'][::2]
            self.atual['eax_out'] = cpu.reg_read(x86.UC_X86_REG_EAX)
            self.atual = None


def capturar():
    cap = carregar_json(cen.caminho('exibicao', 'captura_quadro'))
    ni = cap['named_inputs']['m1']
    b, _, _ = cen.bancada('exibicao', ni['allocation_fill'], ni['clock_ms'][0])
    base.RAIZES.clear()
    base.RAIZES.update(simbolos())
    obs = Chamadas(b)
    obs.atual = None

    def escrever(cpu, acesso, endereco, tamanho, valor, _):
        if not obs.pilha or obs.atual is None:
            return
        antigo = int.from_bytes(cpu.mem_read(endereco, tamanho), 'little')
        novo = valor & ((1 << 8*tamanho)-1)
        if antigo != novo:
            obs.atual['writes'].append((endereco, tamanho, antigo, novo, b.nome(cpu.reg_read(x86.UC_X86_REG_EIP))))
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    for ini, fim in ((0, base.SUPERFICIES[0]-1), (base.SUPERFICIES[1], 0xfffffff0)):
        b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, escrever, None, begin=ini, end=fim)
    b.cpu.ctl_flush_tb()
    resumos = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(300)),
                         ('frame1', lambda: b.executar_quadro(600))):
        correr()
        resumos[nome] = b.resumo_imagem(b.imagem())
    reproduz = {p['phase']: resumos[p['phase']] == p['state_after']['summary'] for p in cap['phases']}
    return obs.chamadas, reproduz


def classe_dgroup(politica):
    cls = {}
    for r in politica['blocks']['dgroup']:
        for a in range(int(r['start'], 16), int(r['end'], 16)):
            cls[a] = r['cls']
    return cls


def principal(saida):
    politica = json.load(open(POLITICA))
    cls = classe_dgroup(politica)
    chamadas, reproduz = capturar()
    out = []
    for c in chamadas:
        por_byte = {}
        pilha = heap = superficie = 0
        outros = []
        for a, n, antigo, novo, w in c['writes']:
            for k in range(n):
                x = a+k
                if a >> 20 == 0x20:
                    pilha += 1
                elif 0x494000 <= x < 0x523000:
                    por_byte.setdefault(hex(x), []).append((w, (antigo >> 8*k) & 0xff, (novo >> 8*k) & 0xff))
                elif a >> 20 == 0x600:
                    superficie += 1
                else:
                    heap += 1
                    outros.append((hex(x), (antigo >> 8*k) & 0xff, (novo >> 8*k) & 0xff, w))
        dg = {a: dict(final_writes=v[-1][1:], count=len(v), writers=sorted({w for w, _, _ in v}),
                      policy=cls.get(int(a, 16), 'not in phase diff (net unchanged)')) for a, v in por_byte.items()}
        out.append(dict(phase=c['phase'], root=c['root'], caller=c['caller'], regs_in={k: hex(v) for k, v in c['regs_in'].items()},
                        stack_args=[hex(v) for v in c['stack_args']], eax_out=hex(c.get('eax_out', -1) & 0xffffffff),
                        bindings=c['bindings'], bank_walk=c.get('bank_walk'), freed_pointers=c.get('freed_pointers'),
                        stack_bytes_changed=pilha, other_memory_bytes_changed=heap, surface_bytes_changed=superficie,
                        other_memory_writes=outros[:64],
                        dgroup_writes=dg))
    json.dump(dict(schema='rising-lands/menuinit-display-calls/1', phases_reproduced=reproduz, calls=out),
              open(saida, 'w'), indent=1)
    print('calls', len(out), reproduz)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    principal(ap.parse_args().saida)
