"""Read-only check: committed missions MONDE01 unit scan through core discovery.

Consumes the missions front's committed scan, fixtures and original capture
without modifying them. With --emular, also reruns their unpatched native
MissionPlaceTerrain prefix for MONDE01 and compares it with the same output.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[1]
MISSOES = RAIZ / 'pesquisas-paralelas/missoes'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular', action='store_true')
    args = p.parse_args()
    for caminho in (MISSOES, MISSOES/'testes'):
        sys.path.insert(0, str(caminho))
    import ambiente_missoes  # noqa: F401  missions-owned bootstrap
    from capturar_terreno_unidades import preparar_caso, resumo_original
    from terreno_unidades import preparar_unidades_no_terreno, provedores_terreno_core
    from test_terreno_unidades import MundoRastreado, carregar_python, rastrear, resumo_python
    from insercao_unidades import SOMA_VISAO_MAXIMA_INSERCAO
    captura = json.loads((MISSOES/'evidencias/captura-terreno-unidades-original-v2.json').read_text())
    esperado = next(c for c in captura['cases'] if c['name'] == 'MONDE01')
    args_caso = preparar_caso('MONDE01', MundoRastreado)
    mundo = args_caso[0]
    bonus = carregar_python(args_caso)
    p15 = 15*276
    soma15 = mundo.unidades[p15+0xbb]+mundo.unidades[p15+0xf5]
    trace = []
    resultado = preparar_unidades_no_terreno(rastrear(provedores_terreno_core(mundo, bonus_unidades=bonus), trace))
    saida = resumo_python(mundo, trace)
    relatorio = dict(missions_capture='pesquisas-paralelas/missoes/evidencias/captura-terreno-unidades-original-v2.json',
                     missions_capture_sha256=hashlib.sha256(
                         (MISSOES/'evidencias/captura-terreno-unidades-original-v2.json').read_bytes()).hexdigest(),
                     original_checkpoint=esperado['checkpoint'], published_vision_sum=SOMA_VISAO_MAXIMA_INSERCAO,
                     unit15_type=mundo.unidades[p15+1], unit15_vision_sum=soma15,
                     placed_units=list(resultado.colocadas), python_checkpoint=hex(resultado.endereco_dependencia),
                     python_matches_original_capture=saida == esperado['output'],
                     differing_fields=[k for k in saida if saida[k] != esperado['output'].get(k)])
    if args.emular:
        from bancada_terreno_unidades import BancadaTerrenoUnidades
        nativo = BancadaTerrenoUnidades()
        args_nativo = preparar_caso('MONDE01', MundoRastreado)
        nativo.carregar_caso(*args_nativo)
        regs = nativo.prefixo()
        fresco = resumo_original(nativo)
        relatorio.update(fresh_native_checkpoint=hex(regs['EIP']), fresh_native_segments=nativo.execucoes,
                         fresh_native_minimap_resumptions=nativo.retomadas_minimapa,
                         fresh_native_matches_capture=fresco == esperado['output'],
                         fresh_native_matches_python=fresco == saida,
                         fresh_native_buffer_differences=nativo.conferir_saida(mundo))
    nome = 'descoberta-terreno-monde01-emulada.json' if args.emular else 'descoberta-terreno-monde01.json'
    (RAIZ/'relatorios'/nome).write_text(json.dumps(relatorio, indent=2)+'\n')
    print(json.dumps(relatorio, indent=2))
    ok = relatorio['python_matches_original_capture'] and relatorio['python_checkpoint'] == '0x46c16d'
    if args.emular:
        ok = ok and relatorio['fresh_native_matches_capture'] and not relatorio['fresh_native_buffer_differences']
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
