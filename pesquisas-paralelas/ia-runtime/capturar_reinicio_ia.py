"""Original-only whole-image captures for IaReset, IaAlloc and IAResetAttaque.

``python3 -B pesquisas-paralelas/ia-runtime/capturar_reinicio_ia.py`` (Unicorn) writes
``evidencias/captura-reinicio-original.json``. Each case stores the inherited image
as a compressed delta against the intact sections (so later readers need no fixture
generator), the native final hashes and EAX, and the compressed world observations
that let the Python translation be replayed without Unicorn.
"""
import base64
import json
import random
import zlib

from ambiente_ia_runtime import EVIDENCE, ORIGINAL_SHA256
from oraculo_reinicio_ia import (DADOS_BASE, JOGADORES_BASE, JOGADORES_TAMANHO, UNIDADES_BASE, UNIDADES_TAMANHO,
                                 Imagem, MundoRepetido, fixture_monde01, fixture_sintetica, imagem_base, poluir)

ARQUIVO = EVIDENCE / 'captura-reinicio-original.json'
SEGMENTOS = ('dados', 'unidades', 'jogadores')
REGIOES_SEGMENTOS = ((UNIDADES_BASE, UNIDADES_BASE + UNIDADES_TAMANHO, 'unit pool 800x276'),
                     (JOGADORES_BASE, JOGADORES_BASE + JOGADORES_TAMANHO, 'player table 4x20'))


def _comprimir(objeto):
    return base64.b64encode(zlib.compress(json.dumps(objeto, separators=(',', ':')).encode(), 9)).decode()


def _expandir(texto):
    return json.loads(zlib.decompress(base64.b64decode(texto)))


def delta(imagem, base):
    """Runs where ``imagem`` differs from ``base``: [segment, offset, hex]."""
    runs = []
    for nome in SEGMENTOS:
        a, b = getattr(imagem, nome), getattr(base, nome)
        i = 0
        while i < len(a):
            if a[i] == b[i]:
                i += 1
                continue
            j = i
            while j < len(a) and (a[j] != b[j] or (j + 1 < len(a) and a[j + 1] != b[j + 1])):
                j += 1
            runs.append([nome, i, bytes(a[i:j]).hex()])
            i = j
    return runs


def aplicar_delta(base, runs):
    imagem = base.copia()
    for nome, offset, dados in runs:
        bruto = bytes.fromhex(dados)
        getattr(imagem, nome)[offset:offset + len(bruto)] = bruto
    return imagem


def _ligacoes_alocacao(relogio, regras, descarga):
    """Declared IaAlloc bindings: (address -> name, EAX, argument reader, tail-jump site)."""
    return {0x48d5fd: ('debugSymLoad', 0, lambda r, s: (r['EAX'],), None),
            0x47e437: ('iaProbLoadBinaryRules', regras, lambda r, s: (r['EAX'], r['EDX']), None),
            0x48d699: ('debugSymUnload', descarga, lambda r, s: (), 0x47fb67)}, relogio


def casos():
    """(name, routine entry, fixture builder, IaAlloc bindings or None, description)."""
    def alocacao_sujo():
        imagem = imagem_base()
        poluir(imagem, random.Random(0x1a10), ((0x498c10, 0x498d5c), (0x51bcdc, 0x51bcfc), (0x521350, 0x521368),
                                               (0x498db4, 0x498db8)))
        return imagem

    def ataques_sujo():
        imagem = imagem_base()
        poluir(imagem, random.Random(0x1a11), ((0x50d5b4, 0x50d9a0),))
        return imagem

    def grupos_sujos(todos_usados):
        imagem = imagem_base()
        rng = random.Random(0x1a12 + todos_usados)
        poluir(imagem, rng, ((0x51a9e0, 0x51b844),))
        for grupo in range(100):  # 'used' byte +0x18: all set, or about 70 % set
            imagem.u8(0x51a9e0 + grupo * 32 + 0x18, 1 if todos_usados or rng.random() < 0.7 else 0)
        imagem.u32(0x51b660, 37 if todos_usados else rng.randrange(100))
        return imagem

    def grupo_com_cadeia():
        imagem = imagem_base()
        cadeia = (11, 300, 42, 799)
        for posicao, unidade in enumerate(cadeia):  # +0x108 links: 11 -> 300 -> 42 -> 799 -> end
            seguinte = cadeia[posicao + 1] if posicao + 1 < len(cadeia) else 0xffff
            imagem.unidades[unidade * 276 + 0x108:unidade * 276 + 0x10a] = seguinte.to_bytes(2, 'little')
        imagem.u16(0x51a9e0 + 5 * 32 + 0x10, cadeia[0])
        imagem.u16(0x51a9e0 + 5 * 32 + 0x12, len(cadeia))
        return imagem
    return (
        ('ia_reset_monde01', 0x47f36e, lambda: fixture_monde01(), None,
         'MONDE01 structures/units/monster tables from missions\' committed loaders; players (1,0,0,0); mission 1'),
        ('ia_reset_monde01_ai_players', 0x47f36e, lambda: fixture_monde01((1, 2, 2, 2)), None,
         'MONDE01 world with players 1..3 declared AI (type 2): contexts, research, cities, resources, war'),
        ('ia_reset_synthetic_world', 0x47f36e, lambda: fixture_sintetica(1), None,
         'Synthetic valid world: 220 units, 60 structures, players (1,2,2,2), mission 3'),
        ('ia_reset_synthetic_monsters', 0x47f36e, lambda: fixture_sintetica(2, monstros=40), None,
         'Synthetic world with 40 monster units (types 20..24) converted to player 4 and grouped'),
        ('ia_reset_dirty_tables_monster_cap', 0x47f36e, lambda: fixture_sintetica(3, sujo=True, monstros=70), None,
         'Inherited dirty AI tables (task pool, contexts with zeroed thresholds, groups, pools, cities, resources, '
         'war, monster outputs); 70 monsters reach the 50-monster cap'),
        ('ia_reset_dirty_contexts_mission9', 0x47f36e,
         lambda: fixture_sintetica(4, sujo=True, contextos_zerados=False, monstros=20, missao=9), None,
         'Dirty AI tables including nonzero research thresholds (creation skipped, dirty byte +9 reachable); '
         'mission 9'),
        ('ia_reset_mission23_single_monster_group', 0x47f36e, lambda: fixture_sintetica(5, monstros=10, missao=0x17),
         None, 'Mission 0x17: InitMissionMonstre registers the reserve group and returns early'),
        ('ia_reset_researched_branches', 0x47f36e, lambda: fixture_sintetica(6, missao=2, pesquisa=0x40), None,
         'Every research level above the thresholds: all four bytes 0xff, branch selection skipped'),
        ('ia_reset_no_ai_players', 0x47f36e, lambda: fixture_sintetica(7, tipos=(1, 1, 0, 0), monstros=15), None,
         'No AI player among 0..3: only player 4 pools and the monster setup'),
        ('ia_reset_monster_group_cap16', 0x47f36e,
         lambda: fixture_sintetica(8, monstros=45, tipos_monstro=(20,), grupos_monstros={2: (5, {22: 1}), 7: (3, {20: 2})}),
         None, 'Monster specs: an unsatisfiable spec leaves an empty group (deleted), then groups of two type-20 '
               'monsters fill the 16-group list (iaGroupNew skips the used group after the hint)'),
        ('ia_reset_monster_reserve_emptied', 0x47f36e,
         lambda: fixture_sintetica(9, monstros=6, tipos_monstro=(20,), grupos_monstros={4: (2, {20: 3})}),
         None, 'Six type-20 monsters fill two groups exactly; the third group and then the empty reserve are '
               'deleted (iaGroupDelete walks the list)'),
        ('ia_alloc_clean', 0x47fb15, imagem_base, _ligacoes_alocacao(0x12345678, 0, 0),
         'Program start over the intact sections; clock 0x12345678; rule loader and SBL bindings return 0'),
        ('ia_alloc_dirty_clock_wrap', 0x47fb15, alocacao_sujo, _ligacoes_alocacao(0xfffffff0, 0, 0x55),
         'Dirty constant tables and RNG; clock above 0x7fffffff; debugSymUnload returns 0x55'),
        ('ia_alloc_rule_load_failure', 0x47fb15, alocacao_sujo, _ligacoes_alocacao(7, 0x1a1a0003, 0),
         'iaProbLoadBinaryRules returns 0x1a1a0003: IaAlloc stops before the table initializers'),
        ('ia_reset_attaque_dirty', 0x47c162, ataques_sujo, None,
         'IAResetAttaque (uncalled in the image) over a dirty 100x10 attack table'),
        ('helper_ia_group_new_dirty', 0x483bd8, lambda: grupos_sujos(False), {'eax': 2, 'edx': 7},
         'iaGroupNew(2, 7) directly over dirty groups with ~70% used and a random hint (skips used groups)'),
        ('helper_ia_group_new_full', 0x483bd8, lambda: grupos_sujos(True), {'eax': 4, 'edx': 0x10},
         'iaGroupNew(4, 0x10) with every group used from hint 37: returns 0xffffffff'),
        ('helper_unit_remove_missing', 0x4832b1, grupo_com_cadeia, {'eax': 5, 'edx': 77},
         'iagUnitRemoveFromGroup(5, 77): unit absent from the chain, returns 0x1a1a0012'),
        ('helper_unit_remove_middle', 0x4832b1, grupo_com_cadeia, {'eax': 5, 'edx': 42},
         'iagUnitRemoveFromGroup(5, 42): unlinks a middle unit'),
    )


HELPERS = {0x483bd8: ('ia_group_new', ('eax', 'edx')), 0x4832b1: ('unit_remove_from_group', ('eax', 'edx'))}
# Declared checkpoints: native state at the entry of the k-th world call (negative = from the end),
# which is where an absent provider must stop the translation with every earlier store retained.
PONTOS_PARADA = {'ia_reset_synthetic_monsters': (0, 5, 300, 3500, -3),
                 'ia_reset_monde01_ai_players': (1, 100, 5000, -1)}


def executar_nativo(image, entrada, imagem, extra, parar_antes=None):
    """``extra``: IaAlloc bindings, or the entry registers of a directly exercised helper."""
    from oraculo_reinicio_ia import ExecucaoNativa
    execucao = ExecucaoNativa(image, imagem.copia())
    tabela, registradores = None, None
    if entrada in HELPERS:
        registradores = extra
    elif extra:
        tabela, relogio = extra
        execucao.ligar_importacao(0x5234a4, relogio)  # WINMM.dll!timeGetTime IAT slot
    return execucao.executar(entrada, ligacoes=tabela, registradores=registradores, parar_antes=parar_antes)


def executar_python(entrada, imagem, observacoes, registradores=None, ate=None):
    """Run the translation over a copy of ``imagem`` with the replayed world; return (eax, image, replay)."""
    from memoria_ia_runtime import MemoriaDeclarada
    from reinicio_ia import (REGIOES_ALOCACAO, REGIOES_ATAQUES, REGIOES_REINICIO, _Rotinas, iniciar_ia_programa,
                             reiniciar_ia, resetar_ataques_ia)
    copia = imagem.copia()
    if entrada in HELPERS:
        memoria = MemoriaDeclarada(copia.segmentos(), REGIOES_REINICIO + REGIOES_SEGMENTOS)
        mundo = MundoRepetido(observacoes, memoria)
        metodo, nomes = HELPERS[entrada]
        eax = getattr(_Rotinas(memoria, mundo), metodo)(*(registradores[n] for n in nomes))
    elif entrada == 0x47f36e:
        memoria = MemoriaDeclarada(copia.segmentos(), REGIOES_REINICIO + REGIOES_SEGMENTOS)
        mundo = MundoRepetido(observacoes, memoria, ate=ate)
        eax = reiniciar_ia(memoria, mundo)
    elif entrada == 0x47fb15:
        memoria = MemoriaDeclarada(copia.segmentos(), REGIOES_ALOCACAO)
        mundo = MundoRepetido(observacoes, memoria)
        eax = iniciar_ia_programa(memoria, mundo)
    else:
        memoria = MemoriaDeclarada(copia.segmentos(), REGIOES_ATAQUES)
        mundo = MundoRepetido(observacoes, memoria)
        resetar_ataques_ia(memoria)
        eax = None
    return eax, copia, mundo


def capturar():
    from inventario_ia_runtime import OriginalImage
    image, base = OriginalImage(), imagem_base()
    resultado = []
    for nome, entrada, construir, extra, descricao in casos():
        inicial = construir()
        nativo = executar_nativo(image, entrada, inicial, extra)
        final = nativo['imagem']
        alterados = {s: sum(1 for x, y in zip(getattr(inicial, s), getattr(final, s)) if x != y) for s in SEGMENTOS}
        contagem = {}
        for obs in nativo['observacoes']:
            contagem[obs['nome']] = contagem.get(obs['nome'], 0) + 1
        pontos = []
        for k in PONTOS_PARADA.get(nome, ()):
            k = k % len(nativo['observacoes'])
            parcial = executar_nativo(image, entrada, inicial, extra, parar_antes=k)
            seguinte = nativo['observacoes'][k]
            pontos.append(dict(chamada=k, rotina=seguinte['nome'], sitio=f'0x{seguinte["sitio"]:08x}',
                               imagem=parcial['imagem'].hashes()))
        resultado.append(dict(
            caso=nome, rotina=f'0x{entrada:08x}', descricao=descricao, pontos_parada=pontos,
            registradores=extra if entrada in HELPERS else None,
            eax=f'0x{nativo["eax"]:08x}' if entrada != 0x47c162 else None,
            segmentos_bancada=nativo['segmentos'], chamadas_mundo=dict(sorted(contagem.items())),
            inicial=inicial.hashes(), final=final.hashes(), bytes_alterados=alterados,
            alteracoes_final=_comprimir(delta(final, inicial)),
            imagem_inicial=_comprimir(delta(inicial, base)), observacoes=_comprimir(nativo['observacoes'])))
    return dict(original_sha256=ORIGINAL_SHA256, bancada='ferramentas/emulador.py BancadaX86 (core)',
                escopo=('Whole-routine native runs: every routine reached executes from the intact image; world '
                        'routines are observed (arguments, EAX, stores), only IaAlloc file I/O and the clock are '
                        'declared bindings. Images: DGROUP+.bss 0x494000..0x523000, unit pool 800x276, players 4x20.'),
                compressao='zlib+base64 JSON', casos=resultado)


def main():
    documento = capturar()
    ARQUIVO.write_text(json.dumps(documento, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print('Cases:', len(documento['casos']),
          'world calls:', sum(sum(c['chamadas_mundo'].values()) for c in documento['casos']),
          'bench segments:', sum(c['segmentos_bancada'] for c in documento['casos']))


if __name__ == '__main__':
    main()
