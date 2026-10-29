"""Comparison policy over N consecutive frames of the display reference (M2.2 preparation).

Original only.  Generalizes ``politica_comparacao_quadro1`` (whose committed
frame-1 report stays the M2.1 policy) to load_tail plus N frames, each frame k
segmented into between_frames(k) and frame(k):

1. Pass 1 runs the display scenario natively and snapshots every state block
   after each phase; a byte is *changed* in a phase when it differs from the
   state before that phase.
2. Pass 2 reruns from the program start with Unicorn read/write hooks on
   exactly the changed bytes (ranges widened by 3 bytes, filtered per byte,
   translation cache flushed), on the declared surface region, and with the
   display-root context tracker of ``politica_comparacao_quadro1`` (a root ends
   exactly when its RET lands on the return address with ESP = entry+4).
   Pass 2 must reproduce every phase state of pass 1.
3. A byte is display-only only when every writer and every reader is
   ``display`` or ``backend``.  The rule is applied per frame window (load_tail
   joins window 1) and cumulatively over all phases; only the cumulative mask
   may be used to exclude bytes from a comparison of the whole run.

Writes a report (default under .local/: captures beyond frame 1 are not
evidence until the coordinator asks for them).

    python3 -B pesquisas-paralelas/missoes/politica_comparacao_quadros.py --quadros 3 \
        --relatorio .local/m2-politica-3-quadros.json
"""
import argparse
import json
import struct
import subprocess
import sys
import time

import ambiente_missoes
import cenarios_oraculo as cen
from emulador import unicorn, x86
from mapa_memoria_m1 import carregar_json
from oraculo_exibicao_missao import BASE_SUPERFICIES, TAMANHO_SUPERFICIES
from politica_comparacao_quadro1 import RAIZES_EXIBICAO, faixas


def bancada():
    cap = carregar_json(cen.caminho('exibicao', 'captura_m1'))
    ni = cap['named_inputs']
    b, _, _ = cen.bancada('exibicao', ni['allocation_fill'], ni['clock_ms'][0])
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    return b


def janela(fase):
    """Frame window of a phase: load_tail and frame 1 form window 1."""
    if fase == 'load_tail':
        return 1
    sufixo = fase[len('between_frames'):] if fase.startswith('between_frames') else fase[len('frame'):]
    return int(sufixo) if sufixo else 1


def passo1(n):
    b = bancada()
    anterior, alterados, resumos, fases, liberados = b.imagem(), {}, {}, [], {}
    for fase, _ in b.executar_quadros(n):
        atual = b.imagem()
        mudou = {}
        for nome, (base, dados) in atual.items():
            velho = anterior.get(nome)
            if velho is None:
                mudou[nome] = (base, list(range(len(dados))))
            elif velho[1] != dados:
                v = velho[1]
                mudou[nome] = (base, [i for i in range(len(dados)) if dados[i] != v[i]])
        alterados[fase], resumos[fase] = mudou, b.resumo_imagem(atual)
        liberados[fase] = sorted(set(anterior)-set(atual))
        fases.append(fase)
        anterior = atual
    return fases, alterados, resumos, liberados


def passo2(n, alvos):
    b = bancada()
    raizes = {b.sym[r] for r in RAIZES_EXIBICAO if r in b.sym}
    pilha, acessos, superficie = [], {}, {}

    def contexto(cpu):
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        while pilha and esp > pilha[-1][0]:
            pilha.pop()
        return 'display' if pilha else 'logic'

    def bloco(cpu, endereco, tamanho, _):
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        while pilha and (esp > pilha[-1][0] or (endereco == pilha[-1][1] and esp == pilha[-1][0]+4)):
            pilha.pop()
        if endereco in raizes:
            retorno = struct.unpack('<I', cpu.mem_read(esp, 4))[0]
            if not pilha or pilha[-1] != (esp, retorno):
                pilha.append((esp, retorno))

    def acesso(tipo):
        def gancho(cpu, _a, endereco, tamanho, valor, _):
            chave = None
            for k in range(tamanho):
                a = endereco+k
                if a in alvos:
                    chave = chave or (tipo, contexto(cpu), b.fase, b.nome(cpu.reg_read(x86.UC_X86_REG_EIP)))
                    d = acessos.setdefault(a, {})
                    d[chave] = d.get(chave, 0)+1
        return gancho

    def gancho_superficie(tipo):
        def gancho(cpu, _a, endereco, tamanho, valor, _):
            ctx = contexto(cpu)
            chave = (tipo, ctx, b.fase, b.nome(cpu.reg_read(x86.UC_X86_REG_EIP)) if ctx == 'logic' else '*')
            superficie[chave] = superficie.get(chave, 0)+1
        return gancho

    b.cpu.hook_add(unicorn.UC_HOOK_BLOCK, bloco, None, begin=0x401000, end=0x493bff)
    for inicio, fim in faixas(alvos):
        b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, acesso('write'), None, begin=inicio-3, end=fim-1)
        b.cpu.hook_add(unicorn.UC_HOOK_MEM_READ, acesso('read'), None, begin=inicio-3, end=fim-1)
    for tipo, gancho in (('write', unicorn.UC_HOOK_MEM_WRITE), ('read', unicorn.UC_HOOK_MEM_READ)):
        b.cpu.hook_add(gancho, gancho_superficie(tipo), None, begin=BASE_SUPERFICIES,
                       end=BASE_SUPERFICIES+TAMANHO_SUPERFICIES-1)
    b.cpu.ctl_flush_tb()
    resumos, visto = {}, len(b.vinculos_declarados.eventos)
    for fase, _ in b.executar_quadros(n):
        for ev in b.vinculos_declarados.eventos[visto:]:
            ctx = 'backend' if ev['kind'] == 'backend' or ev['name'].startswith('DDRAW.') else 'logic'
            for w in ev['memory_writes']:
                a0 = int(w['address'], 16)
                for k in range(w['size']):
                    if a0+k in alvos:
                        d = acessos.setdefault(a0+k, {})
                        chave = ('write', ctx, fase, 'binding '+ev['name'])
                        d[chave] = d.get(chave, 0)+1
                if BASE_SUPERFICIES <= a0 < BASE_SUPERFICIES+TAMANHO_SUPERFICIES and ctx == 'logic':
                    chave = ('write', ctx, fase, 'binding '+ev['name'])
                    superficie[chave] = superficie.get(chave, 0)+1
        visto = len(b.vinculos_declarados.eventos)
        resumos[fase] = b.resumo_imagem(b.imagem())
    return acessos, superficie, resumos


def classificar(acs, filtro=lambda fase: True):
    sel = {k: v for k, v in acs.items() if filtro(k[2])}
    escritores = sorted({(c, r) for (t, c, f, r) in sel if t == 'write'})
    ctxs = {c for (_, c, _, _) in sel}
    if not sel:
        return None
    if not escritores:
        return 'read_only_in_window'
    return 'display_only' if ctxs <= {'display', 'backend'} else 'game_logic'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quadros', type=int, required=True)
    ap.add_argument('--relatorio', required=True)
    args = ap.parse_args()
    saida = ambiente_missoes.ROOT/args.relatorio
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    t0 = time.monotonic()
    fases, alterados, resumos1, liberados = passo1(args.quadros)
    alvos, origem = set(), {}
    for fase, blocos in alterados.items():
        for nome, (base, offs) in blocos.items():
            for o in offs:
                alvos.add(base+o)
                origem.setdefault(base+o, [nome, base, set()])[2].add(fase)
    acessos, superficie, resumos2 = passo2(args.quadros, alvos)
    janelas = sorted({janela(f) for f in fases})
    cumulativo, por_janela, sem_escritor = {}, {w: {} for w in janelas}, []
    for a in sorted(alvos):
        acs = acessos.get(a, {})
        classe = classificar(acs)
        if classe in (None, 'read_only_in_window'):
            sem_escritor.append(hex(a))
        cumulativo[a] = classe
        for w in janelas:
            c = classificar(acs, lambda f, w=w: janela(f) == w)
            if c is not None:
                por_janela[w][a] = c

    def mascara(classes):
        return [[hex(x), hex(z)] for x, z in faixas([a for a, c in classes.items() if c == 'display_only'])]
    revisao = subprocess.run(['git', '-C', str(ambiente_missoes.ROOT), 'rev-parse', 'HEAD'],
                             capture_output=True, text=True).stdout.strip()
    contagem = lambda classes: {c: sum(1 for v in classes.values() if v == c)
                                for c in ('display_only', 'game_logic', 'read_only_in_window')}
    detalhe = {}
    for a in sorted(alvos):
        if cumulativo[a] == 'game_logic':
            acs = acessos.get(a, {})
            nome, base, fs = origem[a]
            detalhe[hex(a)] = dict(block=nome, phases=sorted(fs, key=fases.index),
                                   writers=sorted({f'{c}:{r}' for (t, c, f, r) in acs if t == 'write'}),
                                   readers=sorted({f'{c}:{r}' for (t, c, f, r) in acs if t == 'read'}))
    sup_logica = {f'{t}:{c}:{f}:{r}': n for (t, c, f, r), n in superficie.items() if c == 'logic'}
    rel = dict(schema='rising-lands/monde01-n-frame-comparison-policy/1', source_revision=revisao,
               translation_executed=False, evidence=False, frames=args.quadros, phases=fases,
               display_roots=list(RAIZES_EXIBICAO),
               phase_states_reproduced={f: resumos1[f] == resumos2.get(f) for f in fases},
               phase_state_summaries=resumos1, changed_bytes=len(alvos),
               changed_bytes_by_phase={f: sum(len(o) for _, o in alterados[f].values()) for f in fases},
               freed_blocks={f: v for f, v in liberados.items() if v},
               cumulative=dict(totals=contagem(cumulativo), exclusion_mask=mascara(cumulativo)),
               windows={str(w): dict(totals=contagem(c), exclusion_mask=mascara(c)) for w, c in por_janela.items()},
               bytes_without_observed_writer=sem_escritor, game_logic_bytes=detalhe,
               surfaces=dict(accesses_by_context={c: sum(n for k, n in superficie.items() if k[1] == c)
                                                  for c in ('display', 'backend', 'logic')},
                             logic_context_accesses=sup_logica, excluded_with_proof=not sup_logica),
               seconds=round(time.monotonic()-t0, 1))
    rel['passed'] = all(rel['phase_states_reproduced'].values()) and not sem_escritor and not sup_logica
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(rel, f, indent=1)
        f.write('\n')
    print(json.dumps({k: rel[k] for k in ('passed', 'frames', 'changed_bytes', 'changed_bytes_by_phase',
                                           'phase_states_reproduced', 'seconds')}
                     | dict(cumulative=rel['cumulative']['totals'],
                            windows={w: v['totals'] for w, v in rel['windows'].items()},
                            without_writer=sem_escritor[:10], surface_logic=sup_logica), indent=1))
    return 0 if rel['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
