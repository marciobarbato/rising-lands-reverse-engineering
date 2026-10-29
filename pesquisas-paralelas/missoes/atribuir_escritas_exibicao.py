"""Native writer attribution for every byte that differs between the v1 and display captures.

Original only.  The differing bytes come from ``comparar_quadros_exibicao``
over the committed captures (v1 addresses for v1, partner-allocation addresses
for the display scenario).  Each scenario is rerun from the program start
through frame 1 with Unicorn write hooks on exactly those bytes (translation
cache flushed); every write is recorded with its phase, writer routine and
value.  The runs must reproduce each committed phase state.

    python3 -B pesquisas-paralelas/missoes/atribuir_escritas_exibicao.py \
        --relatorio pesquisas-paralelas/missoes/validacao/m2r3-v1-vs-exibicao-writers.json
"""
import argparse
import hashlib
import json
import subprocess
import sys

import ambiente_missoes
import cenarios_oraculo as cen
import comparar_quadros_exibicao as cmp
from emulador import unicorn, x86
from mapa_memoria_m1 import carregar_json

FASES = ('load_tail', 'between_frames', 'frame1')


def enderecos_diferentes():
    """{'v1': set, 'exibicao': set} of absolute byte addresses differing in any state."""
    i1, aloc1_q, aloc1, _ = cmp.imagens('v1')
    i2, aloc2_q, aloc2, _ = cmp.imagens('exibicao')
    pares = cmp.emparelhar(aloc1, aloc2)
    reloc = cmp.Relocacao(aloc1, pares)
    nome2 = {int(r['pointer'], 16): f"alloc{r['index']:05d}" for r in aloc2}
    v1, ex = set(), set()
    for estado in cmp.ESTADOS:
        a, b = i1[estado], i2[estado]
        for nome, (base, dados) in a.items():
            nome_b = nome2[int(pares[int(nome[5:])]['pointer'], 16)] if nome.startswith('alloc') else nome
            base_b, dados_b = b[nome_b]
            restantes, _ = cmp.diferencas(dados, dados_b, base, reloc)
            v1.update(base+i for i in restantes)
            ex.update(base_b+i for i in restantes)
    return dict(v1=v1, exibicao=ex)


def faixas(enderecos):
    saida = []
    for a in sorted(enderecos):
        if saida and a == saida[-1][1]:
            saida[-1][1] += 1
        else:
            saida.append([a, a+1])
    return saida


def rodar(cenario, enderecos):
    cap = carregar_json(cen.caminho(cenario, 'captura_quadro'))
    ni = cap['named_inputs']['m1']
    b, _, _ = cen.bancada(cenario, ni['allocation_fill'], ni['clock_ms'][0])
    escritas = {}

    def escrever(cpu, acesso, endereco, tamanho, valor, _):
        eip = cpu.reg_read(x86.UC_X86_REG_EIP)
        for k in range(tamanho):
            a = endereco+k
            if a in enderecos:
                escritas.setdefault(a, []).append((b.fase, b.nome(eip), (valor >> (8*k)) & 0xff))
    for inicio, fim in faixas(enderecos):
        b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, escrever, None, begin=inicio, end=fim-1)
    b.cpu.ctl_flush_tb()
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    resumos = {}
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(300)),
                         ('frame1', lambda: b.executar_quadro(600))):
        correr()
        resumos[nome] = b.resumo_imagem(b.imagem())
    reproduz = {p['phase']: resumos[p['phase']] == p['state_after']['summary'] for p in cap['phases']}
    return escritas, reproduz


def resumir(escritas, enderecos):
    """Per byte: writes per phase as (writer, value) runs, collapsed."""
    saida = {}
    for a in sorted(enderecos):
        lista = escritas.get(a, [])
        por_fase = {}
        for fase, rotina, valor in lista:
            fases = por_fase.setdefault(fase, [])
            if fases and fases[-1][0] == rotina:
                fases[-1][1] += 1
                fases[-1][2] = valor
            else:
                fases.append([rotina, 1, valor])
        saida[hex(a)] = {f: [dict(writer=r, writes=n, last_value=hex(v)) for r, n, v in w] for f, w in por_fase.items()}
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--relatorio', required=True)
    args = ap.parse_args()
    saida = ambiente_missoes.ROOT/args.relatorio
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    alvos = enderecos_diferentes()
    resultados = {}
    for cenario in ('v1', 'exibicao'):
        escritas, reproduz = rodar(cenario, alvos[cenario])
        resultados[cenario] = dict(bytes=len(alvos[cenario]), phase_states_reproduced=reproduz,
                                   writers=resumir(escritas, alvos[cenario]))
    revisao = subprocess.run(['git', '-C', str(ambiente_missoes.ROOT), 'rev-parse', 'HEAD'],
                             capture_output=True, text=True).stdout.strip()
    rel = dict(schema='rising-lands/monde01-v1-vs-display-writers/1', source_revision=revisao,
               translation_executed=False,
               captures={c: dict(path=str(cen.caminho(c, 'captura_quadro').relative_to(ambiente_missoes.ROOT)),
                                 sha256=hashlib.sha256(cen.caminho(c, 'captura_quadro').read_bytes()).hexdigest())
                         for c in ('v1', 'exibicao')},
               scenarios=resultados,
               passed=all(all(r['phase_states_reproduced'].values()) for r in resultados.values()))
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(rel, f, indent=1)
        f.write('\n')
    print(json.dumps(dict(passed=rel['passed'], bytes={c: r['bytes'] for c, r in resultados.items()},
                          reproduced={c: r['phase_states_reproduced'] for c, r in resultados.items()}), indent=1))
    return 0 if rel['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
