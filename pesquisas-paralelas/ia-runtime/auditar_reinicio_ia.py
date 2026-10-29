"""Static intact-byte closure audit for the recovered Stage 2 providers.

This supplements, never rewrites, the Stage 1 manifest and WIP captures.
No native execution or production translation is used to obtain byte hashes.
"""
import hashlib
import json

from ambiente_ia_runtime import EVIDENCE, ORIGINAL_SHA256
from inventario_ia_runtime import OriginalImage, interval_record
from oraculo_reinicio_ia import MUNDO

ARQUIVO_AUDITORIA = EVIDENCE / 'reinicio-byte-audit.json'
RAIZES = (0x47f36e, 0x47fb15, 0x47c162)
TRADUZIDAS = {
    0x47f36e: 'ia_reset', 0x47fb15: 'ia_alloc', 0x47c162: 'resetar_ataques_ia',
    0x47cfd0: 'list_init', 0x47d220: 'ia_prob_reset', 0x48270b: 'iag_unit_reset',
    0x484310: 'iag_ville_reset', 0x48134c: 'iaf_ressource_reset', 0x485002: 'iag_ress_reset',
    0x4864c1: 'iag_war_reset', 0x47af90: 'init_mission_monstre',
    0x483bd8: 'ia_group_new', 0x483ce7: 'ia_group_delete', 0x482939: 'unit_add_to_group',
    0x4832b1: 'unit_remove_from_group', 0x483286: 'unit_remove_from_pool',
    0x483747: 'unit_find_type_into_group', 0x483790: 'unit_find_type_into_pool',
    0x483685: 'unit_find_suitable_into_pool', 0x4837f0: 'unit_get_first_in_group',
    0x4846a7: 'ville_set_mode', 0x48569a: 'ress_set_mode', 0x486ca7: 'war_set_mode',
    0x486025: 'iag_ress_add_to_cave_list',
    0x484b96: 'iag_war_reset: inline city total query',
    0x47d1a4: 'ia_alloc: iaProbInit forwards the declared rule binding',
    0x4826a4: 'ia_alloc: iagUnitInit returns zero without stores',
    0x484214: 'ia_alloc: INICIO_CIDADES', 0x484bc4: 'ia_alloc: INICIO_RECURSOS',
    0x48614c: 'ia_alloc: INICIO_GUERRA',
    0x47fc54: 'ia_alloc: iaConfigGetValue returns its EBX default',
    0x489728: 'ia_random: core cadencia.proximo_aleatorio; seed path in ia_alloc',
}
LIGACOES = {
    0x48d5fd: 'IaAlloc SBL loader declared binding; original body excluded',
    0x47e437: 'IaAlloc rule loader declared binding; original body excluded',
    0x48d699: 'IaAlloc SBL unload declared binding; original body excluded',
    0x493a24: 'WINMM timeGetTime import thunk; declared seed clock',
}
LIMITES = {**{a: 'Native observed world provider; Python delegates by original name' for a in MUNDO},
           **LIGACOES, 0x48cfbb: 'Native sprintf executes; formatted stack-local key unused by iaConfigGetValue'}


def auditar():
    image = OriginalImage()
    anterior = json.loads((EVIDENCE / 'manifesto.json').read_text(encoding='utf-8'))
    antigos = anterior['intervals'] + [t for r in anterior['intervals'] for t in r.get('shared_tails', [])]
    faixas = [(int(r['start'], 16), int(r['end_exclusive'], 16)) for r in antigos]
    pendentes, vistos, registros, limites = list(RAIZES), set(), [], []
    while pendentes:
        entrada = pendentes.pop()
        if entrada in vistos:
            continue
        vistos.add(entrada)
        if entrada in LIMITES:
            limites.append(dict(address=f'0x{entrada:08x}', name=image.name(entrada), boundary=LIMITES[entrada]))
            continue
        if entrada not in TRADUZIDAS:
            raise AssertionError(f'Unclassified original callee: 0x{entrada:08x}')
        walked = image.walk(entrada, [(entrada, image.symbol_end(entrada))])
        if walked['indirect_calls'] or walked['imports']:
            raise AssertionError(f'Unclassified indirect/import call at 0x{entrada:08x}')
        enderecos = set(walked['visited']) - set(walked['tail_calls'])
        chunks = []
        for a in sorted(enderecos):
            fim = a + image.instruction(a).size
            if chunks and chunks[-1][1] == a:
                chunks[-1][1] = fim
            else:
                chunks.append([a, fim])
        faltantes = sum(not any(a <= x < b for a, b in faixas) for inicio, fim in chunks for x in range(inicio, fim))
        alvos = set(walked['calls']) | set(walked['tail_calls'])
        registros.append(dict(entry=f'0x{entrada:08x}', name=image.name(entrada), implementation=TRADUZIDAS[entrada],
                              instructions=len(enderecos), original_bytes=sum(b-a for a,b in chunks),
                              bytes_not_exported_by_stage1=faltantes,
                              intervals=[interval_record(image, image.name(entrada), a, b) for a, b in chunks],
                              callees=[f'0x{a:08x}' for a in sorted(alvos)]))
        pendentes.extend(alvos - vistos)
    documento = json.loads((EVIDENCE / 'captura-reinicio-original.json').read_text(encoding='utf-8'))
    return dict(original_sha256=ORIGINAL_SHA256,
                scope='Static transitive caller closure until the explicit boundaries below; not branch coverage',
                roots=[f'0x{a:08x}' for a in RAIZES],
                routines=sorted(registros, key=lambda r: r['entry']),
                boundaries=sorted(limites, key=lambda r: r['address']),
                original_capture_sha256=hashlib.sha256((EVIDENCE / 'captura-reinicio-original.json').read_bytes()).hexdigest(),
                historical_capture_counts=dict(cases=len(documento['casos']),
                    world_calls=sum(sum(c['chamadas_mundo'].values()) for c in documento['casos']),
                    bench_segments=sum(c['segmentos_bancada'] for c in documento['casos']),
                    checkpoints=sum(len(c['pontos_parada']) for c in documento['casos'])))


if __name__ == '__main__':
    documento = auditar()
    ARQUIVO_AUDITORIA.write_text(json.dumps(documento, indent=1) + '\n', encoding='utf-8')
    print('Static routines:', len(documento['routines']), 'explicit boundaries:', len(documento['boundaries']))
