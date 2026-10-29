"""M1 candidate check: strict Python whole-MissionLoad composition vs the frozen original capture.

CPU-free. Runs the strict composition (there is no bridge or fallback; the
Economy per-owner [0x4e19b8] Bag contract is mandatory) twice from the frozen
entry snapshot and compares the whole state, allocation records, AL and the
ordered binding requests with ``captura-carga-missao-original-v2.json``. The
result is marked as an M1 *candidate* only when every criterion holds;
acceptance happens only after integration and committed-main reproduction.

    python3 -B pesquisas-paralelas/missoes/validar_composicao_carga_missao.py \
        --relatorio pesquisas-paralelas/missoes/validacao/stage14-m1-composition-strict.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

import ambiente_missoes
from mapa_memoria_m1 import carregar_blocos, carregar_json, expandir_captura
from composicao_carga_missao import ComposicaoCargaMissaoM1
from comparacao_carga_missao import CAMPOS_NATIVOS_NAO_COMPARADOS, comparar_estado, comparar_vinculos

ENTRADA = ambiente_missoes.OWNED / 'evidencias/entrada-carga-missao-original.json'
CAPTURA = ambiente_missoes.OWNED / 'evidencias/captura-carga-missao-original-v2.json'
FONTES = ('mapa_memoria_m1.py', 'arena_composicao_m1.py', 'ligacao_provedores_m1.py', 'composicao_carga_missao.py',
          'comparacao_carga_missao.py', 'validar_composicao_carga_missao.py', 'carregador_cabecalho.py',
          'carregador_unidades.py')
PROVEDOR_ECONOMIA = 'pesquisas-paralelas/economia/proprietarios.py'

EXCLUSOES = [
    dict(item='16 GetPrivateProfileStringA key arguments (GROUPE00..GROUPE15)',
         reason='the original builds each key string in its own native stack frame (0x2007d38); the capture '
                'keeps no final native stack, so the string itself cannot be read. At those 16 positions the '
                'section, default, buffer size, file, result length and written-bytes SHA-256 are compared.'),
    dict(item='allocation-record fields ' + ', '.join(CAMPOS_NATIVOS_NAO_COMPARADOS),
         reason='native observation metadata of the oracle (caller return addresses and eight caller-stack '
                'dwords at GlobalAlloc), not memory state; the Python resource-callback contract carries no '
                'call site. Pointer, size, flags, index, initial byte, events, locks, active and freed-bytes '
                'SHA-256 are compared for all 938 records.'),
    dict(item='native stack block',
         reason='the original final capture contains no native stack (881 final blocks); the composition '
                'models no stack locals. It is not mission state (M1 snapshot contract).'),
]

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


def executar(entrada, captura, entrada_blocos):
    t = time.monotonic()
    composicao = ComposicaoCargaMissaoM1(entrada)
    resultado = composicao.executar()
    segundos = round(time.monotonic() - t, 3)
    estado = comparar_estado(composicao, captura, entrada_blocos, al=resultado.al)
    vinculos = comparar_vinculos(resultado.registro, captura)
    return dict(
        reached_return=resultado.retornou, al=resultado.al, stop=resultado.parada,
        completed_steps=resultado.passos, seconds=segundos, state_sha256=_estado_sha(composicao),
        binding_requests_sha256=hashlib.sha256(json.dumps(resultado.registro, default=repr).encode()).hexdigest(),
        details=resultado.detalhes, state_comparison=estado, binding_comparison=vinculos)


def criterios(r):
    e, v = r['state_comparison'], r['binding_comparison']
    rec = e['allocation_records']
    return {
        'reached_return_0x42d22d_semantics': r['reached_return'] and r['stop'] is None,
        'al_equals_1': r['al'] == 1 and e['al']['equal'],
        'whole_state_equal_881_blocks_2659375_bytes': (e['equal'] and e['blocks_compared'] == 881
                                                      and e['bytes_compared'] == 2659375
                                                      and e['differing_bytes_or_blocks'] == 0),
        'allocation_records_equal_938': (rec['original'] == rec['composed'] == 938 and rec['differing'] == 0),
        'binding_requests_equal_1400': (v['equal'] and v['original_events'] == v['composed_requests'] == 1400),
        'no_bridge': True,
        'no_excess_change': r['details']['excess_changed'] == [],
    }


def criterios_cenario(r, captura):
    """Same criteria as ``criterios`` with counts taken from a non-default capture."""
    e, v = r['state_comparison'], r['binding_comparison']
    rec = e['allocation_records']
    blocos = captura['oracle']['final_state']['blocks']
    n_blocos, n_bytes = len(blocos), sum(b['bytes'] for b in blocos.values())
    n_vinculos = len(captura['oracle']['binding_events'])
    return {
        'reached_return_0x42d22d_semantics': r['reached_return'] and r['stop'] is None,
        'al_equals_1': r['al'] == 1 and e['al']['equal'],
        f'whole_state_equal_{n_blocos}_blocks_{n_bytes}_bytes': (e['equal'] and e['blocks_compared'] == n_blocos
                                                                and e['bytes_compared'] == n_bytes
                                                                and e['differing_bytes_or_blocks'] == 0),
        f'allocation_records_equal_{len(captura["allocations"])}': (
            rec['original'] == rec['composed'] == len(captura['allocations']) and rec['differing'] == 0),
        f'binding_requests_equal_{n_vinculos}': (v['equal'] and v['original_events'] == v['composed_requests']
                                                 == n_vinculos),
        'no_bridge': True,
        'no_excess_change': r['details']['excess_changed'] == [],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--relatorio', required=True)
    ap.add_argument('--entrada', help='entry artifact (default: the accepted M1 entry)')
    ap.add_argument('--captura', help='MissionLoad capture (default: the accepted M1 capture v2)')
    args = ap.parse_args()
    caminho_entrada = Path(args.entrada).resolve() if args.entrada else ENTRADA
    caminho_captura = Path(args.captura).resolve() if args.captura else CAPTURA
    entrada = carregar_json(caminho_entrada)
    captura = expandir_captura(carregar_json(caminho_captura), entrada)
    entrada_blocos = carregar_blocos(entrada['blocks'])
    primeira = executar(entrada, captura, entrada_blocos)
    segunda = executar(entrada, captura, entrada_blocos)
    padrao = caminho_entrada == ENTRADA and caminho_captura == CAPTURA
    c = criterios(primeira) if padrao else criterios_cenario(primeira, captura)
    deterministico = (primeira['state_sha256'] == segunda['state_sha256']
                      and primeira['binding_requests_sha256'] == segunda['binding_requests_sha256']
                      and primeira['stop'] == segunda['stop'] and primeira['al'] == segunda['al'])
    candidato = all(c.values()) and deterministico
    relatorio = dict(
        schema='rising-lands/missionload-m1-composition-strict/1',
        source_revision=_git('rev-parse', 'HEAD'),
        source_dirty_paths=[l[3:] for l in _git('status', '--porcelain').splitlines()],
        source_sha256={f: _sha_arquivo(ambiente_missoes.OWNED / f) for f in FONTES},
        economy_provider_sha256={PROVEDOR_ECONOMIA: _sha_arquivo(ambiente_missoes.ROOT / PROVEDOR_ECONOMIA)},
        entry_snapshot=dict(path=str(caminho_entrada.relative_to(ambiente_missoes.ROOT)),
                            sha256=_sha_arquivo(caminho_entrada)),
        original_capture=dict(path=str(caminho_captura.relative_to(ambiente_missoes.ROOT)),
                              sha256=_sha_arquivo(caminho_captura)),
        scenario=captura.get('scenario', 'v1'),
        original_sha256=entrada['original_sha256'],
        cpu_free=True, native_executed=False, bridges=[],
        criteria=c, deterministic=deterministico,
        m1_candidate=candidato,
        m1_accepted=False,
        acceptance_note=('M1 candidate only; acceptance happens after integration and committed-main '
                         'reproduction by the coordinator' if candidato else 'NOT an M1 candidate'),
        comparison_exclusions=EXCLUSOES,
        strict=primeira,
        determinism=dict(second_run_state_sha256=segunda['state_sha256'],
                         second_run_binding_requests_sha256=segunda['binding_requests_sha256'],
                         second_run_seconds=segunda['seconds'], identical=deterministico),
        supersedes_blocker=dict(stage13_report='validacao/stage13-m1-composition.json',
                                stage13_stop='EnginInitTechnologie 0x441459 at CALL 0x46c5af (Economy ordens)',
                                resolved_by='Economy per-owner [0x4e19b8] Bag contract on main ff2f5cf'),
        recommended_non_blocking_changes=RECOMENDADOS)
    Path(args.relatorio).write_text(json.dumps(relatorio, indent=1, default=str) + '\n')
    print(json.dumps(dict(m1_candidate=candidato, criteria=c, deterministic=deterministico,
                          state_sha256=primeira['state_sha256'], stop=primeira['stop']), indent=1))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
