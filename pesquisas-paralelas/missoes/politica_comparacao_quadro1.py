"""Comparison policy for the M2.1 display reference: which changed bytes are display-only, with proof.

Original only.  Input: the committed display-scenario reference (``exibicao``
-v2 captures).  For every byte that changes in phase (a) load_tail, (b)
between_frames or (c) frame1 (state after the phase vs before it), the
scenario is rerun natively with Unicorn read and write hooks on exactly those
bytes (ranges widened by 3 bytes, filtered per byte; translation cache
flushed) plus the declared surface region, and every access is attributed:

* **context** ``display``: the access happens inside a call of a display-path
  root (``RAIZES_EXIBICAO``: AffGame, RestoreAll, the DD* wrappers, AffTerrain,
  FilledBox/Box, ...), tracked with a stack of root entry ESPs;
* **context** ``backend``: a declared DirectDraw handler (host write recorded
  by the binding log);
* **context** ``logic``: anything else, including declared non-display
  bindings (fread, GetCursorPos...).

A byte is **display-only** when every writer and every reader in the three
phases is ``display`` or ``backend``.  Every other changed byte is game-logic
state and must be compared.  Surfaces are outside every state block; their
proof is that no logic-context access reaches the surface region.

    python3 -B pesquisas-paralelas/missoes/politica_comparacao_quadro1.py \
        --relatorio pesquisas-paralelas/missoes/validacao/m2-politica-comparacao-quadro1.json
"""
import argparse
import hashlib
import json
import struct
import subprocess
import sys

import ambiente_missoes
import cenarios_oraculo as cen
import comparar_quadros_exibicao as cmp
from emulador import unicorn, x86
from mapa_memoria_m1 import carregar_json
from oraculo_exibicao_missao import BASE_SUPERFICIES, TAMANHO_SUPERFICIES

FASES = ('load_tail', 'between_frames', 'frame1')
# Display-path entry points: every access made while one of them is on the
# call stack is a display access.  Logic routines that display code happens to
# share (memset, GetBit, CaseEstDecouverte...) are display only inside them.
RAIZES_EXIBICAO = ('AffGame', 'RestoreAll', 'AffInit', 'DDInit', 'DDSetPalette', 'DDLockSurface', 'DDUnlockSurface',
                   'DDLockSurfaceVideo', 'DDUnlockSurfaceVideo', 'DDLockSurfaceTemp', 'DDFlipPage', 'DDRestoreAll',
                   'DDScreenCopy', 'AffTerrain', 'FilledBox', 'Box', 'MenuDisplay', 'LoadPalette')


def bytes_alterados():
    """{phase: {block: (base, [offsets])}} of bytes that differ from the previous state, plus freed blocks."""
    imagens, _, _, _ = cmp.imagens('exibicao')
    anterior = imagens['s0']
    saida, liberados = {}, {}
    for fase in FASES:
        atual = imagens[fase]
        saida[fase] = {}
        for nome, (base, dados) in atual.items():
            if nome not in anterior:
                saida[fase][nome] = (base, list(range(len(dados))))
                continue
            velho = anterior[nome][1]
            if velho != dados:
                saida[fase][nome] = (base, [i for i in range(len(dados)) if dados[i] != velho[i]])
        liberados[fase] = sorted(set(anterior)-set(atual))
        anterior = atual
    return saida, liberados, imagens


def faixas(enderecos):
    saida = []
    for a in sorted(enderecos):
        if saida and a == saida[-1][1]:
            saida[-1][1] += 1
        else:
            saida.append([a, a+1])
    return saida


def rodar(alvos):
    cap = carregar_json(cen.caminho('exibicao', 'captura_quadro'))
    ni = cap['named_inputs']['m1']
    b, _, _ = cen.bancada('exibicao', ni['allocation_fill'], ni['clock_ms'][0])
    raizes = {b.sym[n] for n in RAIZES_EXIBICAO if n in b.sym}
    pilha = []                       # (entry ESP, return address) of active display roots
    acessos = {}                     # address -> {(kind, context, phase, routine): count}
    superficie = {}                  # (kind, context, phase, routine) -> count

    def contexto(cpu):
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        while pilha and esp > pilha[-1][0]:
            pilha.pop()
        return 'display' if pilha else 'logic'

    def bloco(cpu, endereco, tamanho, _):
        # A root ends exactly when its RET lands on the return address with
        # ESP = entry+4; a sibling call at the same depth is then outside it.
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        while pilha and (esp > pilha[-1][0] or (endereco == pilha[-1][1] and esp == pilha[-1][0]+4)):
            pilha.pop()
        if endereco in raizes:
            retorno = struct.unpack('<I', cpu.mem_read(esp, 4))[0]
            if not pilha or pilha[-1] != (esp, retorno):
                pilha.append((esp, retorno))

    def acesso(tipo):
        def gancho(cpu, _acesso, endereco, tamanho, valor, _):
            if b.fase not in FASES:
                return
            ctx = contexto(cpu)
            chave = None
            for k in range(tamanho):
                a = endereco+k
                if a in alvos:
                    chave = chave or (tipo, ctx, b.fase, b.nome(cpu.reg_read(x86.UC_X86_REG_EIP)))
                    d = acessos.setdefault(a, {})
                    d[chave] = d.get(chave, 0)+1
        return gancho

    def gancho_superficie(tipo):
        def gancho(cpu, _acesso, endereco, tamanho, valor, _):
            if b.fase not in FASES:
                return
            ctx = contexto(cpu)
            chave = (tipo, ctx, b.fase, b.nome(cpu.reg_read(x86.UC_X86_REG_EIP)) if ctx == 'logic' else '*')
            superficie[chave] = superficie.get(chave, 0)+1
        return gancho

    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    # At the MissionLoad return the stack is _WinMain@16 > ProgIteration > CalculGame: no display root is active.
    b.cpu.hook_add(unicorn.UC_HOOK_BLOCK, bloco, None, begin=0x401000, end=0x493bff)
    for inicio, fim in faixas(alvos):
        b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, acesso('write'), None, begin=inicio-3, end=fim-1)
        b.cpu.hook_add(unicorn.UC_HOOK_MEM_READ, acesso('read'), None, begin=inicio-3, end=fim-1)
    b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, gancho_superficie('write'), None, begin=BASE_SUPERFICIES,
                   end=BASE_SUPERFICIES+TAMANHO_SUPERFICIES-1)
    b.cpu.hook_add(unicorn.UC_HOOK_MEM_READ, gancho_superficie('read'), None, begin=BASE_SUPERFICIES,
                   end=BASE_SUPERFICIES+TAMANHO_SUPERFICIES-1)
    b.cpu.ctl_flush_tb()
    resumos, visto = {}, len(b.vinculos_declarados.eventos)
    for fase, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(300)),
                         ('frame1', lambda: b.executar_quadro(600))):
        correr()
        for ev in b.vinculos_declarados.eventos[visto:]:
            ctx = 'backend' if ev['kind'] == 'backend' or ev['name'].startswith('DDRAW.') else 'logic'
            for w in ev['memory_writes']:
                a0 = int(w['address'], 16)
                for k in range(w['size']):
                    if a0+k in alvos:
                        d = acessos.setdefault(a0+k, {})
                        chave = ('write', ctx, fase, 'binding '+ev['name'])
                        d[chave] = d.get(chave, 0)+1
                if BASE_SUPERFICIES <= a0 < BASE_SUPERFICIES+TAMANHO_SUPERFICIES:
                    chave = ('write', ctx, fase, 'binding '+ev['name'] if ctx == 'logic' else '*')
                    superficie[chave] = superficie.get(chave, 0)+1
        visto = len(b.vinculos_declarados.eventos)
        resumos[fase] = b.resumo_imagem(b.imagem())
    reproduz = {p['phase']: resumos[p['phase']] == p['state_after']['summary'] for p in cap['phases']}
    return acessos, superficie, reproduz


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--relatorio', required=True)
    args = ap.parse_args()
    saida = ambiente_missoes.ROOT/args.relatorio
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    alterados, liberados, imagens = bytes_alterados()
    alvos, origem = set(), {}
    for fase, blocos in alterados.items():
        for nome, (base, offs) in blocos.items():
            for o in offs:
                alvos.add(base+o)
                origem.setdefault(base+o, (nome, base, set()))[2].add(fase)
    acessos, superficie, reproduz = rodar(alvos)
    por_bloco, sem_escritor = {}, []
    for a in sorted(alvos):
        nome, base, fases = origem[a]
        acs = acessos.get(a, {})
        escritores = sorted({(c, r) for (t, c, f, r) in acs if t == 'write'})
        leitores = sorted({(c, r) for (t, c, f, r) in acs if t == 'read'})
        if not escritores:
            sem_escritor.append(hex(a))
        ctxs = {c for (_, c, _, _) in acs}
        classe = 'display_only' if escritores and ctxs <= {'display', 'backend'} else 'game_logic'
        por_bloco.setdefault(nome, []).append(dict(address=a, offset=a-base, phases=sorted(fases), cls=classe,
                                                   writers=escritores, readers=leitores))
    # Collapse into ranges with identical class/writers/readers.
    resultado, mascara = {}, []
    totais = dict(display_only=0, game_logic=0)
    for nome, linhas in por_bloco.items():
        faixas_bloco = []
        for l in linhas:
            chave = (l['cls'], tuple(l['writers']), tuple(l['readers']), tuple(l['phases']))
            if faixas_bloco and faixas_bloco[-1]['_k'] == chave and faixas_bloco[-1]['_e'] == l['address']:
                faixas_bloco[-1]['_e'] += 1
            else:
                faixas_bloco.append(dict(_k=chave, _s=l['address'], _e=l['address']+1))
            totais[l['cls']] += 1
        saida_bloco = []
        for f in faixas_bloco:
            cls, esc, lei, fs = f['_k']
            item = dict(start=hex(f['_s']), end=hex(f['_e']), bytes=f['_e']-f['_s'], cls=cls, phases=list(fs),
                        writers=[dict(context=c, routine=r) for c, r in esc],
                        readers=[dict(context=c, routine=r) for c, r in lei])
            saida_bloco.append(item)
            if cls == 'display_only':
                mascara.append(dict(block=nome, start=item['start'], end=item['end'], bytes=item['bytes']))
        resultado[nome] = saida_bloco
    sup_logica = {f'{t}:{c}:{f}:{r}': n for (t, c, f, r), n in superficie.items() if c == 'logic'}
    revisao = subprocess.run(['git', '-C', str(ambiente_missoes.ROOT), 'rev-parse', 'HEAD'],
                             capture_output=True, text=True).stdout.strip()
    rel = dict(
        schema='rising-lands/monde01-m2.1-comparison-policy/1', source_revision=revisao, translation_executed=False,
        reference={k: dict(path=str(cen.caminho('exibicao', k).relative_to(ambiente_missoes.ROOT)),
                           sha256=hashlib.sha256(cen.caminho('exibicao', k).read_bytes()).hexdigest())
                   for k in ('entrada', 'captura_m1', 'captura_quadro')},
        display_roots=list(RAIZES_EXIBICAO),
        rule='display_only iff every writer and every reader of the byte in load_tail/between_frames/frame1 runs '
             'inside a display root call or is a declared DirectDraw handler; everything else is game logic',
        phase_states_reproduced=reproduz, changed_bytes=len(alvos), totals=totais,
        bytes_without_observed_writer=sem_escritor, freed_blocks=liberados,
        surfaces=dict(region=[hex(BASE_SUPERFICIES), hex(BASE_SUPERFICIES+TAMANHO_SUPERFICIES)],
                      in_state_blocks=False,
                      accesses_by_context={c: sum(n for (t, cc, f, r), n in superficie.items() if cc == c)
                                           for c in ('display', 'backend', 'logic')},
                      logic_context_accesses=sup_logica,
                      excluded_with_proof=not sup_logica),
        exclusion_mask=mascara, blocks=resultado,
        method=__doc__.split('\n\n')[1].replace('\n', ' '))
    rel['passed'] = all(reproduz.values()) and not sem_escritor and not sup_logica
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(rel, f, indent=1)
        f.write('\n')
    print(json.dumps(dict(passed=rel['passed'], changed=len(alvos), totals=totais, reproduced=reproduz,
                          without_writer=sem_escritor[:20], surface_logic=sup_logica,
                          mask_ranges=len(mascara)), indent=1))
    return 0 if rel['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
