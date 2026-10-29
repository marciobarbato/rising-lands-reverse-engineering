"""Native capture of the logic-state effects of RestoreAll and AffGame in the display scenario.

Original only.  Pass 1 reruns Missions' ``exibicao`` scenario and records every value-changing write made inside
the dynamic extent of RestoreAll (0x474b08) or AffGame (0x417698) in phases load_tail / between_frames / frame1
(declared surface pixels excluded).  Pass 2 hooks reads of exactly those bytes and keeps the ones first accessed by
code outside both extents (a logic read) before any other write.  The phase states must reproduce Missions' capture.

    python3 -B pesquisas-paralelas/graficos-animacao/capturar_efeitos_logicos_exibicao.py \
        --saida pesquisas-paralelas/graficos-animacao/evidencias/efeitos-logicos-exibicao.json
"""
import argparse, hashlib, json, struct, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'missoes'))
import ambiente_missoes
import cenarios_oraculo as cen
from emulador import unicorn, x86
from mapa_memoria_m1 import carregar_json
import importlib.util

_spec = importlib.util.spec_from_file_location('extrair_evidencias_graficos', Path(__file__).resolve().parent/'extrair_evidencias.py')
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
imagem_pe = _mod.imagem_pe

RAIZES = {0x474b08: 'RestoreAll', 0x417698: 'AffGame'}
SUPERFICIES = (0x3800000, 0x3a00000)


def retornos():
    """Return addresses of every direct CALL to a root (raw E8 scan; extra sites are harmless)."""
    base, img = imagem_pe()
    saida = {}
    for i in range(0x401000-base, 0x493c00-base-4):
        if img[i] == 0xe8:
            alvo = (base+i+5+struct.unpack_from('<i', img, i+1)[0]) & 0xffffffff
            if alvo in RAIZES:
                saida[base+i+5] = RAIZES[alvo]
    return saida


class Observador:
    def __init__(self, b):
        self.b, self.pilha, self.ret, self.guardas = b, [], retornos(), []
        for a in RAIZES:
            b.cpu.hook_add(unicorn.UC_HOOK_CODE, self.entrada, None, begin=a, end=a)
        for a in self.ret:
            b.cpu.hook_add(unicorn.UC_HOOK_CODE, self.saida, None, begin=a, end=a)

    def esp(self):
        return self.b.cpu.reg_read(x86.UC_X86_REG_ESP)

    def entrada(self, cpu, endereco, tamanho, _):
        self.pilha.append((RAIZES[endereco], self.esp()+4, self.b.fase))
        m = self.b.cpu.mem_read
        u = lambda a, n: int.from_bytes(m(a, n), 'little')
        pool = bytes(m(0x49a0c8, 1000*276))
        self.guardas.append(dict(
            phase=self.b.fase, root=RAIZES[endereco], dfb44=u(0x4dfb44, 1), cursor_4e1d18=u(0x4e1d18, 1),
            view_origin=[u(0x508720, 2), u(0x508722, 2)], viewport=[u(0x508724, 2), u(0x508726, 2)],
            screen=[u(0x49a018, 2), u(0x49a01a, 2)], mode_4e2f78=u(0x4e2f78, 4),
            structure_states={str(k): sum(1 for i in range(1000) if pool[i*276+5] == k) for k in range(8)}))

    def saida(self, cpu, endereco, tamanho, _):
        if self.pilha and self.esp() == self.pilha[-1][1]:
            self.pilha.pop()

    @property
    def dentro(self):
        return self.pilha[-1][0] if self.pilha else None


def rodar(passo, alvos=None):
    cap = carregar_json(cen.caminho('exibicao', 'captura_quadro'))
    ni = cap['named_inputs']['m1']
    b, _, _ = cen.bancada('exibicao', ni['allocation_fill'], ni['clock_ms'][0])
    obs = Observador(b)
    escritas, leituras, ordem = [], [], {}

    def escrever(cpu, acesso, endereco, tamanho, valor, _):
        antigo = int.from_bytes(cpu.mem_read(endereco, tamanho), 'little')
        novo = valor & ((1 << 8*tamanho)-1)
        if passo == 1:
            if obs.dentro and antigo != novo:
                eip = cpu.reg_read(x86.UC_X86_REG_EIP)
                escritas.append((b.fase, obs.dentro, b.nome(eip), endereco, tamanho, antigo, novo))
        else:
            for k in range(tamanho):
                a = endereco+k
                if a in alvos:
                    ordem.setdefault(a, 'W' if obs.dentro is None else 'D')   # first access kind
                    escritas.append((b.fase, obs.dentro, b.nome(cpu.reg_read(x86.UC_X86_REG_EIP)), a))

    def ler(cpu, acesso, endereco, tamanho, valor, _):
        if obs.dentro:
            return
        eip = cpu.reg_read(x86.UC_X86_REG_EIP)
        for k in range(tamanho):
            a = endereco+k
            if a in alvos:
                leituras.append((b.fase, b.nome(eip), a))

    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    # hooks only for the three frame phases
    if passo == 1:
        for ini, fim in ((0, SUPERFICIES[0]-1), (SUPERFICIES[1], 0xfffffff0)):
            b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, escrever, None, begin=ini, end=fim)
    else:
        for ini, fim in faixas(alvos):
            b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, escrever, None, begin=ini-3, end=fim-1)
            b.cpu.hook_add(unicorn.UC_HOOK_MEM_READ, ler, None, begin=ini-3, end=fim-1)
    b.cpu.ctl_flush_tb()
    resumos = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(300)),
                         ('frame1', lambda: b.executar_quadro(600))):
        correr()
        resumos[nome] = b.resumo_imagem(b.imagem())
    reproduz = {p['phase']: resumos[p['phase']] == p['state_after']['summary'] for p in cap['phases']}
    return escritas, leituras, ordem, reproduz, obs.guardas


def faixas(enderecos):
    saida = []
    for a in sorted(enderecos):
        if saida and a == saida[-1][1]:
            saida[-1][1] += 1
        else:
            saida.append([a, a+1])
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    args = ap.parse_args()
    esc1, _, _, rep1, guardas = rodar(1)
    # per byte: final-writer bookkeeping
    por_byte = {}
    for fase, raiz, rotina, a, n, antigo, novo in esc1:
        for k in range(n):
            por_byte.setdefault(a+k, []).append(dict(phase=fase, root=raiz, writer=rotina,
                                                     old=(antigo >> 8*k) & 0xff, new=(novo >> 8*k) & 0xff))
    alvos = set(por_byte)
    print('pass1 written bytes', len(alvos), 'phases reproduced', rep1, flush=True)
    esc2, leit, ordem, rep2, _ = rodar(2, alvos)
    def classe(a):
        if SUPERFICIES[0] <= a < SUPERFICIES[1] or a >> 20 == 0x600:
            return 'declared_surface'
        if a >> 20 == 0x20:
            return 'bench_stack'
        if 0x494000 <= a < 0x523000:
            return 'dgroup'
        return 'heap/%x' % (a >> 20)
    lidos = {}
    for f, r, a in leit:
        lidos.setdefault(int(a, 16) if isinstance(a, str) else a, set()).add((f, r.split('+')[0]))
    resumo, detalhe = {}, {}
    for a, v in por_byte.items():
        c = classe(a)
        resumo[c] = resumo.get(c, 0) + 1
        if c in ('dgroup',) or (c.startswith('heap') and a in lidos):
            detalhe[hex(a)] = dict(writes=v[:6], write_count=len(v),
                                   logic_readers=sorted(map(list, lidos.get(a, []))))
    heap = {}
    for a, v in por_byte.items():
        c = classe(a)
        if c.startswith('heap'):
            k = (c, v[0]['root'], v[0]['writer'].split('+')[0])
            heap[k] = heap.get(k, 0)+1
    json.dump(dict(schema='rising-lands/display-logic-effects/1', reproduced=[rep1, rep2],
                   value_changing_bytes_by_class=resumo,
                   logic_read_bytes_by_class={c: len({a for a in alvos if classe(a) == c and a in lidos})
                                              for c in resumo},
                   dgroup_and_logic_read_bytes=detalhe,
                   heap_buffers=[dict(region=k[0], root=k[1], writer=k[2], bytes=n) for k, n in sorted(heap.items())],
                   guards_at_root_entry=guardas),
              open(args.saida, 'w'), indent=1)
    print('pass2 reads', len(leit))


if __name__ == '__main__':
    sys.exit(main())
