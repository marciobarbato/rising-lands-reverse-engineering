"""Fresh native comparison of the complete cache lifecycle against Python.

Each step compares whole buffers: key pointer, 1024 key bytes, cursor, all
256 bank payloads, MemAlloc counter and the exact declared-binding calls.
The fresh native run must also reproduce the committed original-only capture.
"""
import hashlib
import json
import time
from extrair_evidencias import RAIZ, HASH_EXE, exigir_area_editavel
from graficos import Catalogo
from bancada_x86 import unicorn
from bancada_ciclo_cache import BancadaCicloCache, LIMITE_BANCO, PONTEIRO_CHAVES
from vinculos_graficos import RegistroVinculos
from cache_terreno import resolver_bloco_terreno
from ciclo_cache_terreno import CicloCacheTerreno, MemoriaMotor, DependenciaCicloCache
from capturar_ciclo_cache import consultas, json_compacto, HASH_NORMALIZADO


def sha(data): return hashlib.sha256(data).hexdigest()


def comparar(b, ciclo, memoria, rotulo):
    nativo = b.estado()
    assert nativo['ponteiro_chaves_u32'] == ciclo.ponteiro_chaves_u32, rotulo
    assert nativo['cursor_u16'] == ciclo.proximo_u16, rotulo
    assert nativo['blocos'] == ciclo.blocos_crus, rotulo
    assert nativo['contador_memoria_u32'] == memoria.contador_u32, rotulo
    if ciclo.registros is not None: assert nativo['chaves'] == ciclo.registros, rotulo
    return nativo


def fase(b, ciclo, memoria, lista, tabela, deslocamento, capturadas, catalogo):
    linhas = []
    for indice, (fonte, descoberta, iluminacao) in enumerate(lista):
        n = deslocamento+indice; celula = (0x1234+977*n) & 0xffff; camera = n % 4
        eax, ramo = b.get_num_bob(fonte, descoberta, iluminacao, celula, camera, tabela)
        plano = resolver_bloco_terreno(catalogo, ciclo.cache, id_terreno_u16=fonte, descoberta_u8=descoberta,
            iluminacao_u8=iluminacao, tabela_sombra=tabela)
        assert (eax, ramo) == (plano['id_motor'], plano['motivo']), (n, eax, ramo, plano)
        nativo = comparar(b, ciclo, memoria, ('GetNumBob', n))
        linha = [[fonte, descoberta, iluminacao, celula, camera], eax, ramo, nativo['cursor_u16'], sha(nativo['chaves']), sha(nativo['blocos'])]
        assert linha == capturadas[indice], ('fresh native differs from original-only capture', n)
        linhas.append(linha)
    b.verificar_entradas()
    return linhas


def validar():
    exigir_area_editavel(); inicio = time.monotonic(); catalogo = Catalogo()
    captura = json.loads((RAIZ/'evidencias/captura-ciclo-cache-original.json').read_text())
    tabela = bytes.fromhex(captura['shadow_table_hex'])
    b = BancadaCicloCache(catalogo); ciclo = CicloCacheTerreno.apos_carregar_banco(catalogo)
    assert b.estado_carga == captura['process_load_state'] and b.estado_carga['ponteiro_chaves_u32'] == ciclo.ponteiro_chaves_u32
    assert b.estado_carga['cursor_u16'] == ciclo.proximo_u16 == 0
    banco = b.carregar_banco(); resumo_banco = b.registro.resumo(*banco['marca_vinculos'])
    assert resumo_banco == captura['LoadSTRATBank']['bound_calls'] and banco['instrucoes'] == captura['LoadSTRATBank']['instructions']
    # Python model side starts from the same declared fixture position.
    registro_py = RegistroVinculos(); arena_py = b.arena.derivar(registro=registro_py)
    memoria = MemoriaMotor(contador_u32=b.u32(0x4e2f3c), vinculos=arena_py)
    comparar(b, ciclo, memoria, 'after LoadSTRATBank/SetBank')
    passos = []
    r, log = b.cache_alloc(); marca = registro_py.marca(); ponteiro = ciclo.alocar(memoria)
    assert ponteiro == r['EAX'] and registro_py.desde(marca) == log == captura['CacheAlloc']['bound_calls']
    nativo = comparar(b, ciclo, memoria, 'CacheAlloc'); assert ciclo.registros is None and nativo['chaves'] == bytes([0xa5])*1024
    passos.append(dict(step='CacheAlloc', bound_calls=log, pointer_u32=ponteiro, counter_u32=memoria.contador_u32,
        native_keys='fixture fill 0xA5 (undefined GMEM_FIXED content); model keys undefined'))
    capturas = {e['event']: e for e in captura['lifecycle']}
    def init(nome):
        r = b.init_cache(); eax = ciclo.iniciar(); assert r['EAX'] == eax == 256
        nativo = comparar(b, ciclo, memoria, nome); assert nativo['chaves'] == bytes(1024) == bytes.fromhex(capturas[nome]['keys_hex'])
        assert (nativo['cursor_u16'], sha(nativo['blocos'])) == (capturas[nome]['cursor_u16'], capturas[nome]['payload_sha256'])
        passos.append(dict(step=nome, eax=eax, cursor_u16=ciclo.proximo_u16, payload_sha256=sha(nativo['blocos']), instructions=r['instrucoes']))
    lista = consultas()
    init('InitCache_1')
    linhas = fase(b, ciclo, memoria, lista['apos_primeiro_init'], tabela, 0, capturas['GetNumBob_phase_1']['queries'], catalogo)
    print('Native/Python GetNumBob phase 1:', len(linhas), flush=True)
    init('InitCache_2')
    linhas2 = fase(b, ciclo, memoria, lista['apos_segundo_init'], tabela, len(linhas), capturas['GetNumBob_phase_2']['queries'], catalogo)
    print('Native/Python GetNumBob phase 2:', len(linhas2), flush=True)
    r, log = b.cache_free(); marca = registro_py.marca(); eax = ciclo.liberar(memoria)
    assert r['EAX'] == eax == 0 and registro_py.desde(marca) == log == capturas['CacheFree']['bound_calls']
    nativo = comparar(b, ciclo, memoria, 'CacheFree'); assert ciclo.registros is None and nativo['ponteiro_chaves_u32'] == ponteiro
    passos.append(dict(step='CacheFree', bound_calls=log, eax=eax, stale_pointer_u32=ponteiro, counter_u32=memoria.contador_u32))
    for chamada in (ciclo.iniciar, lambda: ciclo.cache):
        try: chamada(); raise AssertionError('freed table accepted')
        except DependenciaCicloCache: pass
    nulo = BancadaCicloCache(catalogo); falha = None
    try: nulo.init_cache()
    except unicorn.UcError as erro: falha = dict(native=str(erro), eip=hex(nulo.reg('EIP')))
    assert falha == dict(native=captura['null_pointer_initcache']['expected_fault'], eip='0x40fa49')
    try: CicloCacheTerreno.apos_carregar_banco(catalogo).iniciar(); raise AssertionError('null table accepted')
    except DependenciaCicloCache as erro: falha['model'] = hex(erro.endereco)
    assert falha['model'] == '0x40fa49'
    report = dict(exe_sha256=HASH_EXE, analysis_pe_sha256_not_executed=HASH_NORMALIZADO, unicorn_version=unicorn.__version__,
        result='PASS', limits=dict(bank=LIMITE_BANCO, routine_instructions=100000, getnumbob_instructions=300000, timeout_us=2000000),
        bindings=dict(iat_resolution=b.resolucao_iat, fixture_files=b.arquivos_declarados, path_prefix_0x509494=b.prefixo,
            LoadSTRATBank=resumo_banco, model_side='Python MemoriaMotor consumes a derived ArenaGlobalFixa at the same position'),
        synthetic_payload_binding=None, explicit_inputs=captura['explicit_inputs'], steps=passos,
        getnumbob=dict(phase_1=len(linhas), phase_2=len(linhas2), branches={k: sum(1 for x in linhas+linhas2 if x[2] == k)
            for k in ('undiscovered', 'direct', 'hit', 'miss')}),
        expected_faults=[dict(case='InitCache before CacheAlloc', **falha)],
        totals=dict(native_entries=b.execucoes+nulo.execucoes, instructions_observed=b.instrucoes+nulo.instrucoes,
            bound_calls=b.registro.marca(), whole_state_comparisons=5+len(linhas)+len(linhas2)),
        expected_limits=0, skips=0, seconds=round(time.monotonic()-inicio, 3))
    (RAIZ/'validacao/x86-ciclo-cache.json').write_text(json_compacto(report)+'\n')
    print('PASS:', report['totals'], flush=True)


if __name__ == '__main__': validar()
