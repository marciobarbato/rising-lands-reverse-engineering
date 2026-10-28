"""M1 comparison: Python whole-MissionLoad composition vs the frozen original capture (CPU-free).

Runs the strict composition (the only run that can be M1 evidence) from the
frozen entry snapshot to its return or its first named provider stop, then
compares the whole state, allocation records, AL and the ordered binding
requests with ``captura-carga-missao-original-v2.json``. A second, explicitly
labelled diagnostic run applies the declared bridges of
``composicao_carga_missao.PONTES`` to show what lies beyond a strict stop; it
is never M1 evidence.

    python3 -B pesquisas-paralelas/missoes/validar_composicao_carga_missao.py \
        --relatorio pesquisas-paralelas/missoes/validacao/stage13-m1-composition.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

import ambiente_missoes
from mapa_memoria_m1 import carregar_blocos, carregar_json
from composicao_carga_missao import ComposicaoCargaMissaoM1, PONTES
from comparacao_carga_missao import comparar_estado, comparar_vinculos

ENTRADA = ambiente_missoes.OWNED / 'evidencias/entrada-carga-missao-original.json'
CAPTURA = ambiente_missoes.OWNED / 'evidencias/captura-carga-missao-original-v2.json'
FONTES = ('mapa_memoria_m1.py', 'arena_composicao_m1.py', 'ligacao_provedores_m1.py', 'composicao_carga_missao.py',
          'comparacao_carga_missao.py', 'validar_composicao_carga_missao.py', 'carregador_cabecalho.py',
          'carregador_unidades.py')

CONTRATO_ECONOMIA = dict(
    owner='economy',
    file='pesquisas-paralelas/economia/proprietarios.py (PropriedadeConstrucoes.__init__ / .ordens) and its '
         'consumers cauda_carga.CaudaCargaEconomia.definir_tecnologia_unidades, '
         'aprendizagem.Aprendizagem.atualizar_ordens and proprietarios.py line ~166',
    function='PropriedadeConstrucoes(ordens=...) / CaudaCargaEconomia.inicializar_tecnologia_unidades '
             '(EnginInitTechnologie 0x441459, MissionLoad CALL 0x46c5af)',
    needed='Accept the four live per-owner Bag pools by identity (the Core world\'s bolsas_tipos_unidades: four '
           'distinct 2,704-byte bytearrays, 26 x 104-byte Bags each) and address owner j as ordens[j] + '
           'type*104, instead of copying into one 10,816-byte buffer with a 2,704-byte owner stride.',
    why='The constructor copies (bytearray(ordens)) into a single contiguous buffer. The original reaches the '
        'Bags through the pointer table [0x4e19b8], whose four entries point at four separate page-aligned '
        'allocations; Core already owns them as four bytearrays (ciclo_unidades.resetar_todas_unidades requires '
        'exactly that). One buffer cannot alias four non-contiguous allocations, so no shared memory map can '
        'include Economy\'s copy without a shadow.',
    evidence='entry snapshot: [0x4e19b8]=0x41780000 -> 0x41781000, 0x41782000, 0x41783000, 0x41784000 '
             '(alloc00845..alloc00848, 2,704 bytes each); strict stop traceback cauda_carga.py:60 '
             'definir_tecnologia_unidades; the diagnostic copy-in/copy-out bridge then reaches AL=1 with the '
             'whole state equal, so this is the only blocking contract on the MONDE01 path.')

RECOMENDADOS = [
    dict(owner='core', file='ferramentas/reset_terreno.py resetar_minimapa; avanco_unidades.MundoFisico mini_*',
         needed='Accept the exact 16,384-byte (128x128) minimap allocations of [0x507d5c]/[0x507d60]/[0x507d64] '
                '(length >= w*h) instead of requiring 65,536-byte layers.',
         status='non-blocking: the map exposes the first 16,384 bytes of Core\'s own layers as the allocations; '
                'the 49,152 provider-private bytes are poisoned 0x5c and verified unchanged at the end'),
    dict(owner='core', file='ferramentas/avanco_unidades.py MundoFisico.tiles/.regioes; '
                            'estruturas_caminhos.CoresEstruturas.pilha',
         needed='Optionally keep these u16 grids as u16 views of their allocations instead of Python lists.',
         status='non-blocking: the lists are canonical, filled in place from the snapshot and packed for '
                'comparison; the header loader writes the tile layer through one staged byte image'),
]


def _git(*argumentos):
    return subprocess.run(['git', *argumentos], cwd=ambiente_missoes.ROOT, capture_output=True,
                          text=True, check=True).stdout.strip()


def _sha_arquivo(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def _estado_sha(composicao):
    h = hashlib.sha256()
    for nome, (base, dados) in sorted(composicao.mapa.serializar().items()):
        h.update(nome.encode() + base.to_bytes(4, 'little') + dados)
    return h.hexdigest()


def executar(entrada, captura, entrada_blocos, pontes=()):
    t = time.monotonic()
    composicao = ComposicaoCargaMissaoM1(entrada, pontes=pontes)
    resultado = composicao.executar()
    segundos = round(time.monotonic() - t, 3)
    estado = comparar_estado(composicao, captura, entrada_blocos, al=resultado.al)
    vinculos = comparar_vinculos(resultado.registro, captura)
    return composicao, resultado, dict(
        bridges=list(pontes), reached_return=resultado.retornou, al=resultado.al, stop=resultado.parada,
        completed_steps=resultado.passos, seconds=segundos, state_sha256=_estado_sha(composicao),
        details=resultado.detalhes, state_comparison=estado, binding_comparison=vinculos,
        whole_state_equal=estado['equal'] and vinculos['equal'])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--relatorio', required=True)
    args = ap.parse_args()
    entrada, captura = carregar_json(ENTRADA), carregar_json(CAPTURA)
    entrada_blocos = carregar_blocos(entrada['blocks'])
    _, _, estrito = executar(entrada, captura, entrada_blocos)
    _, _, repeticao = executar(entrada, captura, entrada_blocos)
    _, _, diagnostico = executar(entrada, captura, entrada_blocos, pontes=tuple(PONTES))
    m1 = bool(estrito['reached_return'] and estrito['whole_state_equal'] and not estrito['bridges'])
    relatorio = dict(
        schema='rising-lands/missionload-m1-composition/1',
        source_revision=_git('rev-parse', 'HEAD'),
        source_dirty_paths=[l[3:] for l in _git('status', '--porcelain').splitlines()],
        source_sha256={f: _sha_arquivo(ambiente_missoes.OWNED / f) for f in FONTES},
        entry_snapshot=dict(path='evidencias/entrada-carga-missao-original.json', sha256=_sha_arquivo(ENTRADA)),
        original_capture=dict(path='evidencias/captura-carga-missao-original-v2.json', sha256=_sha_arquivo(CAPTURA)),
        original_sha256=entrada['original_sha256'],
        cpu_free=True, native_executed=False,
        m1_accepted=m1,
        verdict=('M1: strict composition reached AL=1 and the whole state equals the original' if m1 else
                 'NOT M1: strict composition stopped at a named provider contract; see strict.stop'),
        strict=estrito,
        strict_determinism=dict(repeated_state_sha256=repeticao['state_sha256'],
                                identical=repeticao['state_sha256'] == estrito['state_sha256']
                                and repeticao['stop'] == estrito['stop']),
        diagnostic_bridged=dict(
            not_m1_evidence=True,
            purpose='Show what lies beyond the strict stop; every bridge is a declared copy-in/copy-out',
            bridge_descriptions=PONTES, **diagnostico),
        provider_contract_changes_needed=[CONTRATO_ECONOMIA] if not m1 else [],
        recommended_non_blocking_changes=RECOMENDADOS)
    Path(args.relatorio).write_text(json.dumps(relatorio, indent=1, default=str) + '\n')
    resumo = dict(m1_accepted=m1, strict_stop=estrito['stop'] and {k: estrito['stop'][k] for k in (
        'step', 'routine', 'call_site', 'owner', 'exception')},
        strict_bindings_equal=estrito['binding_comparison']['equal'],
        strict_differing=estrito['state_comparison']['differing_bytes_or_blocks'],
        bridged_reached_return=diagnostico['reached_return'], bridged_al=diagnostico['al'],
        bridged_whole_state_equal=diagnostico['whole_state_equal'],
        deterministic=relatorio['strict_determinism']['identical'])
    print(json.dumps(resumo, indent=1))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
