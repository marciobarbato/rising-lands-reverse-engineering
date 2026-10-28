"""Original-only inventory and native captures of the GetNumBob cache lifecycle.

Runs before any translation: no reconstruction module is imported. Writes the
exact-byte inventory (evidencias/ciclo-cache.json) and the native observation
record (evidencias/captura-ciclo-cache-original.json).
"""
import bisect
import hashlib
import json
import struct
import time
from pathlib import Path
from extrair_evidencias import RAIZ, HASH_EXE, imagem_pe, simbolos, exigir_area_editavel
from graficos import Catalogo
from bancada_x86 import unicorn
from bancada_ciclo_cache import (BancadaCicloCache, INTERVALOS, IMPORTACOES, CRT, LIMITE_BANCO,
    PONTEIRO_CHAVES, CURSOR, CONTADOR_MEMORIA)
from cache_terreno import FIRST_CACHED_ID

HASH_NORMALIZADO = '26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0'
REGIOES = [
    ('CacheAlloc_CacheFree_InitCache', 0x40fa18, 0x40fa72),
    ('uncalled_SetCacheBloc_SearchCacheBloc', 0x40fa72, 0x40fb27),
    ('uncalled_ConstruitCache', 0x40fbc7, 0x40fd95),
    ('GetNumBob', 0x40fd95, 0x410085),
    ('MemInit_MemAlloc_MemFree_into_MemClose_ret', 0x467e34, 0x467ef4),
    ('SetBank', 0x418590, 0x418599),
    ('LoadSTRATBank', 0x41877a, 0x4189c2),
    ('FileOpen_FileExists_FileClose_FileRead', 0x458420, 0x458476),
    ('ProgInit_MemInit_call', 0x474bf8, 0x474bfd),
    ('ProgInit_bank_then_CacheAlloc', 0x474e9b, 0x474ecd),
    ('ProgExit_CacheFree_then_DeleteBank', 0x474faa, 0x474fc8),
    ('CalculGame_start_InitCache_before_MissionLoad', 0x42d1da, 0x42d239),
    ('MenuNewSelect_InitCache_before_GameLoad', 0x42c693, 0x42c710),
    ('capacity_word', 0x495bc4, 0x495bc6),
    ('bank_name_pointer_table', 0x495bc8, 0x495be0),
    ('bank_mode_and_name_strings', 0x4941d6, 0x494260),
    ('kernel32_global_iat_slots', 0x5231c0, 0x5231dc),
]
ALVOS_CHAMADA = (0x40fa18, 0x40fa2e, 0x40fa38, 0x40fa72, 0x40fae0, 0x40fbc7, 0x40fd95, 0x45c8a2, 0x45c779, 0x45c7ff,
    0x467ea6, 0x467ecb, 0x467e34)
REFERENCIAS = (PONTEIRO_CHAVES, CURSOR, 0x495bc4, CONTADOR_MEMORIA)


def sha(data): return hashlib.sha256(data).hexdigest()


def json_compacto(valor, nivel=0):
    """Dicts indented; each list row of scalars/lists on one readable line."""
    recuo = ' '*(nivel+1)
    if isinstance(valor, dict):
        if not valor: return '{}'
        return '{\n'+',\n'.join(recuo+json.dumps(k)+': '+json_compacto(v, nivel+1) for k, v in valor.items())+'\n'+' '*nivel+'}'
    if isinstance(valor, list) and valor and any(isinstance(x, (dict, list)) for x in valor):
        return '[\n'+',\n'.join(recuo+(json_compacto(x, nivel+1) if isinstance(x, dict) else json.dumps(x, separators=(',', ':')))
            for x in valor)+'\n'+' '*nivel+']'
    return json.dumps(valor, separators=(',', ':'))


def varredura_estatica(base, imagem):
    """Direct rel32 CALL/JMP targets and 4-byte absolute references only."""
    nomes = simbolos(); ordenados = sorted(nomes)
    def funcao(endereco):
        i = bisect.bisect_right(ordenados, endereco)-1
        return f'{nomes[ordenados[i]]}+0x{endereco-ordenados[i]:x}'
    chamadas = {hex(a): [] for a in ALVOS_CHAMADA}
    for offset in range(len(imagem)-5):
        if imagem[offset] in (0xe8, 0xe9):
            alvo = base+offset+5+struct.unpack_from('<i', imagem, offset+1)[0]
            if alvo in ALVOS_CHAMADA:
                chamadas[hex(alvo)].append(['call' if imagem[offset] == 0xe8 else 'jmp', hex(base+offset), funcao(base+offset)])
    referencias = {}
    for alvo in REFERENCIAS:
        padrao = struct.pack('<I', alvo); lista = []; i = imagem.find(padrao)
        while i != -1:
            lista.append([hex(base+i), funcao(base+i)]); i = imagem.find(padrao, i+1)
        referencias[hex(alvo)] = lista
    return dict(nomes={hex(a): nomes.get(a) for a in ALVOS_CHAMADA}, chamadas_rel32=chamadas, referencias_absolutas=referencias,
        limite='A computed address (base register plus index) or a pointer stored elsewhere is not excluded by this scan.')


def secoes():
    dados = (RAIZ/'fontes/cd/INSTALHD/RISING.EXE').read_bytes(); pe = struct.unpack_from('<I', dados, 0x3c)[0]
    n = struct.unpack_from('<H', dados, pe+6)[0]; opcional = struct.unpack_from('<H', dados, pe+20)[0]; lista = []
    for i in range(n):
        c = pe+24+opcional+i*40; virtual, rva, bruto, ponteiro = struct.unpack_from('<IIII', dados, c+8)
        lista.append(dict(nome=dados[c:c+8].rstrip(b'\0').decode('ascii'), cabecalho_hex=dados[c:c+40].hex(), virtual_size=virtual,
            rva=hex(rva), size_of_raw_data=bruto, pointer_to_raw_data=ponteiro, characteristics=hex(struct.unpack_from('<I', dados, c+36)[0])))
    return lista


def inventario():
    base, imagem = imagem_pe(); regioes = []
    for nome, inicio, fim in REGIOES:
        bruto = imagem[inicio-base:fim-base]
        regioes.append(dict(name=nome, start=hex(inicio), end=hex(fim), bytes_hex=bruto.hex(), sha256=sha(bruto)))
    return dict(exe_sha256=HASH_EXE, analysis_pe_sha256_not_executed=HASH_NORMALIZADO, regions=regioes, sections=secoes(),
        static_scan=varredura_estatica(base, imagem),
        predecessor_sources={n: sha((RAIZ/n).read_bytes()) for n in ('cache_terreno.py', 'passe_terreno.py', 'graficos.py')})


def consultas():
    """Deterministic (source u16, discovery u8, lighting u8) phases."""
    inicio = [(0, 0, 0), (65535, 0, 0), (5, 16, 0), (5, 0x30, 0x0f), (300, 1, 0), (300, 1, 0), (300, 0, 1),
        (300, 0, 16), (300, 0xe1, 0xe0), (300, 1, 0)]
    distintos = []
    for s in range(1, 271):
        fog, light = (s*7) % 16, (s*5) % 16
        if fog == 0 and light == 0: light = 16
        distintos.append((s, fog | (0xe0 if s % 3 == 0 else 0), light | (0xe0 if s % 5 == 0 else 0)))
    reuso = [(300, 1, 0), distintos[-1], distintos[0], (300, 1, 0)]
    mascaras = [(777, fog, light) for fog in range(16) for light in range(16) if fog or light]
    reinicio = [(777, 1, 1), (777, 1, 1), (300, 1, 0), (1081, 2, 3), (1, 4, 5), (1081, 2, 3), (0, 0, 0), (9, 16, 16)]
    return dict(apos_primeiro_init=inicio+distintos+reuso+mascaras, apos_segundo_init=reinicio)


def capturar_lista(b, lista, tabela, deslocamento):
    linhas = []
    for indice, (fonte, descoberta, iluminacao) in enumerate(lista):
        n = deslocamento+indice; celula = (0x1234+977*n) & 0xffff; camera = n % 4
        eax, ramo = b.get_num_bob(fonte, descoberta, iluminacao, celula, camera, tabela)
        e = b.estado()
        linhas.append([[fonte, descoberta, iluminacao, celula, camera], eax, ramo, e['cursor_u16'], sha(e['chaves']), sha(e['blocos'])])
    b.verificar_entradas()
    return linhas


def bloqueio_inicial_nulo(catalogo):
    """InitCache before CacheAlloc writes through the .bss null pointer."""
    b = BancadaCicloCache(catalogo)
    try:
        b.init_cache()
    except unicorn.UcError as erro:
        return dict(expected_fault=str(erro), eip=hex(b.reg('EIP')), key_pointer_u32=b.u32(PONTEIRO_CHAVES), bound_calls=b.registro.marca())
    raise RuntimeError('InitCache with a null key pointer unexpectedly returned')


def capturar():
    exigir_area_editavel(); inicio = time.monotonic(); catalogo = Catalogo()
    inv = inventario(); (RAIZ/'evidencias/ciclo-cache.json').write_text(json_compacto(inv)+'\n')
    print('Original-byte inventory:', len(inv['regions']), 'regions', flush=True)
    tabela = bytes.fromhex(json.loads((RAIZ/'validacao/x86-cache-terreno.json').read_text())['tables_hex'][0])
    b = BancadaCicloCache(catalogo); carga = dict(b.estado_carga)
    banco = b.carregar_banco(); marca_banco = banco['marca_vinculos']
    blocos_banco = b.blocos_cache(); descritores = [b.descritor(FIRST_CACHED_ID+s) for s in range(256)]
    arquivo = {FIRST_CACHED_ID+s: catalogo.quadro(FIRST_CACHED_ID+s).comprimido for s in range(256)}
    nao_cache = b''.join(b.ler(b.descritor(i)['dados'], b.descritor(i)['tamanho']) for i in range(1, FIRST_CACHED_ID))
    tabela_desc = b''.join(b.ler(b.descritor(i)['descritor'], 12) for i in range(1, banco['quantidade']+1))
    captura = dict(exe_sha256=HASH_EXE, analysis_pe_sha256_not_executed=HASH_NORMALIZADO, unicorn_version=unicorn.__version__,
        shadow_table_hex=tabela.hex(), process_load_state=carga,
        bindings=dict(iat_resolution=b.resolucao_iat, crt=[dict(endereco=hex(a), rotina=n, convencao='Watcom register') for a, n in CRT],
            fixture_files=b.arquivos_declarados, path_prefix_0x509494=b.prefixo, arena=dict(start=hex(b.arena.inicio), bytes=b.arena.fim-b.arena.inicio,
            alignment=b.arena.alinhamento, uninitialized_fill_u8=0xa5)),
        explicit_inputs=['visibility map pointers 0x507D78/0x507D88 (harness heap)', 'shadow table pointer 0x4E24B4 (harness heap)',
            'camera byte 0x508041', 'path prefix 0x509494'],
        limits=dict(bank=LIMITE_BANCO, routine_instructions=100000, getnumbob_instructions=300000, timeout_us=2000000),
        intervals={k: [[hex(a), hex(z)] for a, z in v] for k, v in INTERVALOS.items()})
    captura['LoadSTRATBank'] = dict(return_eax=hex(banco['banco']), table=hex(banco['tabela']), count=banco['quantidade'],
        instructions=banco['instrucoes'], bound_calls=b.registro.resumo(*marca_banco),
        first_bound_calls=b.registro.desde(marca_banco[0], marca_banco[0]+12),
        counter_after_u32=b.u32(CONTADOR_MEMORIA), arena_next_after=hex(b.arena.proximo),
        cached_descriptors=[[hex(d['descritor']), d['largura'], d['altura'], d['tamanho'], hex(d['dados'])] for d in descritores],
        cached_payload_sha256=sha(blocos_banco), cached_payload_equals_blocs_cmp=blocos_banco == b''.join(arquivo[i] for i in sorted(arquivo)),
        cached_distinct_payloads={sha(v): [i for i in arquivo if arquivo[i] == v] for v in set(arquivo.values())},
        non_cached_payload_sha256=sha(nao_cache), descriptor_table_sha256=sha(tabela_desc))
    e = b.estado(); r, log = b.cache_alloc(); depois = b.estado()
    captura['CacheAlloc'] = dict(before=dict(pointer=e['ponteiro_chaves_u32'], cursor=e['cursor_u16'], counter=e['contador_memoria_u32']),
        bound_calls=log, registers={k: hex(v) for k, v in r.items() if k != 'instrucoes'}, instructions=r['instrucoes'],
        pointer_u32=depois['ponteiro_chaves_u32'], counter_u32=depois['contador_memoria_u32'], cursor_u16=depois['cursor_u16'],
        keys_hex=depois['chaves'].hex(), payload_sha256=sha(depois['blocos']))
    eventos = []
    def init(nome):
        antes = b.estado(); r = b.init_cache(); e = b.estado()
        eventos.append(dict(event=nome, registers={k: hex(v) for k, v in r.items() if k != 'instrucoes'}, instructions=r['instrucoes'],
            keys_before_sha256=sha(antes['chaves']), keys_hex=e['chaves'].hex(), cursor_before=antes['cursor_u16'], cursor_u16=e['cursor_u16'],
            payload_before_sha256=sha(antes['blocos']), payload_sha256=sha(e['blocos']), pointer_u32=e['ponteiro_chaves_u32'],
            counter_u32=e['contador_memoria_u32']))
        print('Original', nome, 'returned', flush=True)
    fases = consultas()
    init('InitCache_1')
    linhas = capturar_lista(b, fases['apos_primeiro_init'], tabela, 0)
    eventos.append(dict(event='GetNumBob_phase_1', queries=linhas)); print('Original GetNumBob phase 1:', len(linhas), flush=True)
    init('InitCache_2')
    linhas2 = capturar_lista(b, fases['apos_segundo_init'], tabela, len(linhas))
    eventos.append(dict(event='GetNumBob_phase_2', queries=linhas2)); print('Original GetNumBob phase 2:', len(linhas2), flush=True)
    final = b.estado(); r, log = b.cache_free(); livre = b.estado()
    eventos.append(dict(event='CacheFree', bound_calls=log, registers={k: hex(v) for k, v in r.items() if k != 'instrucoes'},
        instructions=r['instrucoes'], pointer_u32=livre['ponteiro_chaves_u32'], cursor_u16=livre['cursor_u16'],
        counter_u32=livre['contador_memoria_u32'], payload_sha256=sha(livre['blocos']), keys_before_free_hex=final['chaves'].hex()))
    nao_cache_final = b''.join(b.ler(b.descritor(i)['dados'], b.descritor(i)['tamanho']) for i in range(1, FIRST_CACHED_ID))
    tabela_final = b''.join(b.ler(b.descritor(i)['descritor'], 12) for i in range(1, banco['quantidade']+1))
    captura.update(lifecycle=eventos, final_non_cached_payload_sha256=sha(nao_cache_final), final_descriptor_table_sha256=sha(tabela_final),
        null_pointer_initcache=bloqueio_inicial_nulo(catalogo),
        totals=dict(native_entries=b.execucoes+1, instructions_observed=b.instrucoes, bound_calls=b.registro.marca(),
            getnumbob_calls=len(linhas)+len(linhas2)), seconds=round(time.monotonic()-inicio, 3))
    (RAIZ/'evidencias/captura-ciclo-cache-original.json').write_text(json_compacto(captura)+'\n')
    print('Original-only lifecycle captured:', captura['totals'], flush=True)


if __name__ == '__main__': capturar()
