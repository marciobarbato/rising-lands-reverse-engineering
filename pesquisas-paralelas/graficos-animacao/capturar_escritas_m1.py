"""Native AffGame (original x86, intact RISING.EXE) over the accepted M1 post-load world: DGROUP writes through the HUD checkpoint.

Uses the existing BancadaQuadro unchanged (no new renderer, no DirectDraw invention: its declared IsLost/Lock fixture).
World buffers come from the frozen M1 capture; AffGame globals not in M1 are declared (mode byte 0x12 set by CalculGame
in the load-state frame per Missions' QUADRO1 note, 800x600 geometry from globais_base, M1 origin/viewer).
Run under the heavy lease. Usage: python3 capturar_escritas_m1.py out.json
"""
import json, struct, sys, time
from graficos import RAIZ, Catalogo
from renderizar_m1_estatico import EstadoM1, CAPTURA, montar, sha
from cenas_quadro import globais_base, fundo, GLOBAIS
from capturar_quadro import tabelas, executar_cena, linha_rastro
from bancada_quadro import BancadaQuadro, DADOS
from fechamento_escritas_affgame import fechar, _abs_dgroup

ALVOS = {0x4e2f78: 1, 0x4e1b0e: 1, 0x4e060c: 4, 0x4e0610: 2, 0x507d54: 2, 0x50a9b4: 2, 0x50a9b6: 2, 0x4e1d18: 1}


def cena_m1(m1, mundo, forcar_modo=0x12, **globais):
    camera = m1.u(0x508041, 1)
    origem = m1.estatico(0x508720, 4)
    g = globais_base(camera_u8=camera, origem=origem, modo_jogo_u8=forcar_modo, **globais)
    ptrs = lambda base: [m1.bloco(base+4*i, 65536) for i in range(4)]
    mundo_d = dict(terreno=mundo.terreno, objetos=mundo.objetos, auxiliares=mundo.auxiliares, atributos=m1.bloco(0x507da8, 65536),
        regioes=mundo.regioes, unidades=mundo.unidades, projeteis=mundo.projeteis, descoberta=mundo.descoberta,
        iluminacao=mundo.iluminacao, contagem_luz=ptrs(0x507d98), estruturas=m1.estatico(0x49a0c8, 276000))
    return dict(nome='m1', mundo=mundo_d, globais=g, ticks=[1500], antes='InitCache')


def principal(saida):
    inicio = time.monotonic(); m1 = EstadoM1(CAPTURA); mundo = montar(m1, 0)
    catalogo = Catalogo(); sombra, ecl = tabelas()
    b = BancadaQuadro(catalogo); b.cache_alloc(); b.calcular_tabelas_jogador(); b.init_cache()
    cena = cena_m1(m1, mundo)
    # Seed the AffGame-relevant runtime bytes the bench would otherwise leave at image defaults with M1's own values.
    for a, n in ALVOS.items(): b.escrever(a, m1.estatico(a, n))
    r, antes, depois = executar_cena(b, cena, sombra, ecl)
    diff = b.diferencas(antes, depois, ignorar=('superficie', 'arena', 'heap', 'unidades'))
    corridas = [dict(endereco=hex(DADOS[0]+off), antes=a, depois=d) for off, a, d in diff.get('dados', [])]
    def toca(c, alvo, n): e = int(c['endereco'], 16); return e < alvo+n and e+len(c['antes'])//2 > alvo
    alvos = {hex(a): dict(m1=m1.estatico(a, n).hex(), antes=b_antes, depois=b_depois, escrito=[c for c in corridas if toca(c, a, n)])
        for a, n in ALVOS.items() for b_antes, b_depois in [(antes['dados'][a-DADOS[0]:a-DADOS[0]+n].hex(), depois['dados'][a-DADOS[0]:a-DADOS[0]+n].hex())]}
    # Resolve the runtime blit tables (zero in M1, filled by the bench's video/bank setup) and close their static write sets.
    tabelas_blit = {hex(a): [hex(b.u32(a+4*i)) for i in range(10)] for a in (0x496cdc, 0x496d04)}
    alvos_blit = sorted({int(x, 16) for v in tabelas_blit.values() for x in v if int(x, 16)})
    escritas_blit = {}
    for t in alvos_blit:
        vis, g, todas, desc = fechar(t)
        escritas_blit[hex(t)] = dict(rotinas=len(vis), indiretos=len(desc), stores_dgroup_abs=sorted({hex(ad) for a, (f, i) in todas.items() if i for ad, sz, w in _abs_dgroup(i) if w}))
    out = dict(tabelas_blit=tabelas_blit, fechamento_alvos_blit=escritas_blit, input_sha256=m1.sha256, parada=hex(r['eip']), instrucoes=r['instrucoes'], rastro=linha_rastro(r['rastro']),
        vinculos_n=len(r['vinculos']), alvos=alvos, dgroup_runs=corridas, segundos=round(time.monotonic()-inicio, 1),
        mudou_unidades=antes['unidades'] != depois['unidades'])
    json.dump(out, open(saida, 'w'), indent=1)
    print(json.dumps({k: out[k] for k in ('parada', 'instrucoes', 'rastro', 'segundos')}, indent=1))
    for a, v in alvos.items(): print(a, v['antes'], '->', v['depois'], len(v['escrito']))
    print(len(corridas), 'DGROUP runs changed')


if __name__ == '__main__': principal(sys.argv[1])
