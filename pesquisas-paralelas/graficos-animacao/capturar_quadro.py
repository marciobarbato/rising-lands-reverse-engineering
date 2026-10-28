"""Original-only inventory and native captures of AffGame in-game frames.

No reconstruction module is imported. Writes evidencias/quadro-jogo.json
(exact bytes, call order, static write scan, configuration evidence) and
evidencias/captura-quadro-original.json (native frames, traces and every
write observed by a whole writable-memory diff).
"""
import bisect
import hashlib
import json
import struct
import time
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, simbolos, exigir_area_editavel
from graficos import Catalogo
from bancada_x86 import unicorn
from bancada_quadro import BancadaQuadro, LIMITE_QUADRO, CHECKPOINT_HUD, RENDERIZADORES, CODIGO
from cenas_quadro import (GLOBAIS, cena_monde01, cenas_sinteticas, mundo_monde01, fundo, resumo_mundo, sha, fixar_monde01, monde01_fixado,
    GATILHOS_FACHADA, CODIGOS_AFFVEGET)
from capturar_ciclo_cache import json_compacto, HASH_NORMALIZADO

REGIOES = [
    ('AffGame', 0x417698, 0x417f38), ('AffGame_shared_epilogue', 0x4171f1, 0x4171f8),
    ('CalculFrame', 0x43f710, 0x43f7af), ('DDLockSurface', 0x43f3b4, 0x43f445), ('DDLockSurface_epilogue', 0x43f316, 0x43f31c),
    ('DDUnlockSurface', 0x43f445, 0x43f4a3), ('EvenementEnCours', 0x4581b6, 0x4581bc),
    ('SaveCurrentClipping_RestaureClipping', 0x40f4b7, 0x40f519), ('CaseEstDecouverte_TerrainEstDecouvert', 0x4766d6, 0x47670a),
    ('AffBatiments_prefix', 0x407dd3, 0x407fb3), ('AffBatiments_terrain_switch_and_tail', 0x40f23b, 0x40f49c),
    ('AffVehiculeAtelier_guard', 0x402864, 0x40288b), ('AffVeget_code_table_and_prefix', 0x415a58, 0x415b3a),
    ('AffEngin_state_dispatch', 0x41591f, 0x415a57), ('AffSprite', 0x416864, 0x416e41), ('AffTerrain', 0x41068e, 0x41087e),
    ('DDInit_mode_window_pitch', 0x43f50b, 0x43f592), ('WndProc_draw_divisor_keys', 0x418321, 0x418351),
    ('ResetMode_clip', 0x40f645, 0x40f758), ('ProgIteration_AffGame_call', 0x47505e, 0x475068),
    ('draw_divisor_initial', 0x497284, 0x497285), ('affveget_tree_table_bytes', 0x415a58, 0x415a6f),
]
ROTINAS_ESCRITA = (0x417698, 0x43f710, 0x43f3b4, 0x41068e, 0x416864, 0x407dd3, 0x415acf, 0x41591f, 0x412390,
    0x46ff70, 0x40f4b7, 0x40f4e8, 0x4766d6, 0x402864, 0x410085, 0x45c72a, 0x45b247, 0x45b796, 0x40fd95)


def varredura_escritas(base, imagem):
    """Static absolute-address writes per routine (pointer writes need the diff)."""
    import sys
    sys.path.insert(0, str(RAIZ/'dependencias'))
    import capstone
    from capstone import x86 as X
    nomes = simbolos(); ordenados = sorted(nomes)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32); cs.detail = True
    escreve = {'mov', 'inc', 'dec', 'add', 'sub', 'and', 'or', 'xor', 'not', 'neg', 'shl', 'shr', 'sar', 'adc', 'sbb'}
    saida = {}
    for inicio in ROTINAS_ESCRITA:
        fim = ordenados[bisect.bisect_right(ordenados, inicio)]; achados = {}
        for i in cs.disasm(imagem[inicio-base:fim-base], inicio):
            if i.operands and i.mnemonic in escreve:
                op = i.operands[0]
                if op.type == X.X86_OP_MEM and op.mem.base == 0 and op.mem.index == 0 and 0x494000 <= op.mem.disp < 0x522400:
                    achados.setdefault(hex(op.mem.disp), []).append(hex(i.address))
        saida[nomes[inicio]] = dict(intervalo=[hex(inicio), hex(fim)], escritas=achados)
    return saida


def inventario():
    base, imagem = imagem_pe(); regioes = []
    for nome, inicio, fim in REGIOES:
        bruto = imagem[inicio-base:fim-base]
        regioes.append(dict(name=nome, start=hex(inicio), end=hex(fim), bytes_hex=bruto.hex(), sha256=sha(bruto)))
    return dict(exe_sha256=HASH_EXE, analysis_pe_sha256_not_executed=HASH_NORMALIZADO, regions=regioes,
        static_absolute_writes=varredura_escritas(base, imagem), facade_trigger_words=[hex(v) for v in GATILHOS_FACHADA],
        affveget_codes_with_handlers=list(CODIGOS_AFFVEGET), globals_inventory=[[n, hex(a), w] for n, a, w in GLOBAIS],
        predecessor_sources={n: sha((RAIZ/n).read_bytes()) for n in ('passe_terreno.py', 'passe_sprites.py', 'ciclo_cache_terreno.py',
            'cache_terreno.py', 'composicao.py', 'objetos.py', 'sequenciais.py', 'projeteis_graficos.py')})


def tabelas():
    sombra = bytes.fromhex(json.loads((RAIZ/'validacao/x86-cache-terreno.json').read_text())['tables_hex'][0])
    ecl = next(t for t in json.loads((RAIZ/'validacao/x86-eclairage.json').read_text())['tables']
        if t['name'] == 'PLATGAME' and t['percentage'] == 60)
    return sombra, bytes.fromhex(ecl['table_hex'])


def executar_cena(b, cena, sombra, eclairage, parar_evento=None):
    b.carregar_cena(cena, tabela_sombra=sombra, tabela_eclairage=eclairage, fundo=fundo(), globais_nomes=GLOBAIS)
    antes = b.fotografia(); r = b.quadro(ticks=list(cena['ticks']), parar_evento=parar_evento); depois = b.fotografia()
    return r, antes, depois


def linha_rastro(rastro):
    contagem = {}
    for evento in rastro: contagem[evento[0]] = contagem.get(evento[0], 0)+1
    return dict(eventos=len(rastro), por_funcao=dict(sorted(contagem.items())),
        sha256=sha(json.dumps(rastro, separators=(',', ':')).encode('ascii')))


def capturar():
    exigir_area_editavel(); inicio = time.monotonic(); catalogo = Catalogo()
    inv = inventario(); (RAIZ/'evidencias/quadro-jogo.json').write_text(json_compacto(inv)+'\n')
    print('Original-byte inventory:', len(inv['regions']), 'regions', flush=True)
    sombra, eclairage = tabelas()
    b = BancadaQuadro(catalogo); _, alocacao = b.cache_alloc(); jogadores = b.calcular_tabelas_jogador()
    registros = {t: b.inicializar_tipo(t) for t in (0, 2, 5, 6, 7, 9)}
    import subprocess
    revisao = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=RAIZ, capture_output=True, text=True, check=True).stdout.strip()
    manifesto = fixar_monde01(mundo_monde01(), revisao=revisao); base = monde01_fixado()
    cenas = [cena_monde01(base)]+cenas_sinteticas(base, registros)
    quadros = []
    for cena in cenas:
        if cena['antes'] == 'InitCache': b.init_cache()
        r, antes, depois = executar_cena(b, cena, sombra, eclairage)
        diff = b.diferencas(antes, depois, ignorar=('superficie', 'arena'))
        estado = b.estado()
        quadros.append(dict(nome=cena['nome'], antes=cena['antes'], sinteticos=cena['sinteticos'], entradas=resumo_mundo(cena['mundo']),
            globais={n: cena['globais'][n].hex() for n, a, w in GLOBAIS}, ticks=cena['ticks'],
            parada=hex(r['eip']), esp=hex(r['esp']), instrucoes=r['instrucoes'], vinculos=r['vinculos'], rastro=linha_rastro(r['rastro']),
            superficie_sha256=sha(depois['superficie']), superficie_mudou=antes['superficie'] != depois['superficie'],
            escritas=diff, cache=dict(chaves_sha256=sha(estado['chaves']), blocos_sha256=sha(estado['blocos']), cursor=estado['cursor_u16'])))
        print('Original AffGame frame', cena['nome'], hex(r['eip']), r['instrucoes'], 'instructions', flush=True)
    captura = dict(exe_sha256=HASH_EXE, analysis_pe_sha256_not_executed=HASH_NORMALIZADO, unicorn_version=unicorn.__version__,
        limits=LIMITE_QUADRO, code_interval=[hex(v) for v in CODIGO], checkpoint=hex(CHECKPOINT_HUD),
        renderers_traced={hex(a): n for a, n in RENDERIZADORES.items()},
        bindings=dict(iat_resolution=b.resolucao_iat, directdraw='IDirectDrawSurface IsLost/Lock/Restore/Unlock via COM object 0x4E1790',
            fixture_files=b.arquivos_declarados, LoadSTRATBank=b.registro.resumo(*b.banco['marca_vinculos'])),
        tables=dict(shadow_sha256=sha(sombra), eclairage_sha256=sha(eclairage), shadow_source='validacao/x86-cache-terreno.json tables_hex[0]',
            eclairage_source='validacao/x86-eclairage.json PLATGAME 60%'),
        palette_alloc=dict(pointers={hex(0x4e24b0+4*i): hex(b.u32(0x4e24b0+4*i)) for i in range(11)}),
        player_tables_sha256=[sha(t) for t in jogadores], cache_alloc=alocacao, unit_initializer_records={str(t): r.hex() for t, r in registros.items()},
        monde01_checkpoint=dict(manifesto, pinned_file='evidencias/monde01-checkpoint-quadro.zlib'),
        frames=quadros, totals=dict(native_entries=b.execucoes, instructions_observed=b.instrucoes, bound_calls=b.registro.marca()),
        seconds=round(time.monotonic()-inicio, 3))
    (RAIZ/'evidencias/captura-quadro-original.json').write_text(json_compacto(captura)+'\n')
    print('Original-only frames captured:', captura['totals'], flush=True)


if __name__ == '__main__': capturar()
