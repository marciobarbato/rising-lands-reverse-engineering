"""Validate TerrainReset, MiniMapReset and BatimentModifyMap against the original."""
import argparse
import json
import os
from pathlib import Path
import platform
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ/'testes'))
MODULOS = ('test_reset_terreno', 'test_emulacao_reset_terreno')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular', action='store_true')
    p.add_argument('--relatorio', type=Path, help='Write a separate report without replacing historical results')
    args = p.parse_args()
    os.environ['RISING_EMULAR'] = '1' if args.emular else '0'
    from validar import Resultado
    suite = unittest.defaultTestLoader.loadTestsFromNames(MODULOS)
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(python=platform.python_version(), x86_enabled=args.emular, tests=r.testsRun,
                  failures=len(r.failures), errors=len(r.errors),
                  skips=[dict(test=t.id(), reason=s) for t, s in r.skipped],
                  bounded_x86_executions=r.execucoes_x86, success=r.wasSuccessful(),
                  scope='TerrainReset 0x46b315, MiniMapReset 0x469f00 and BatimentModifyMap 0x419e97 (both DL '
                        'variants, SetMiniMap modes 6/7) over synthetic inherited layers; no MissionLoad caller.')
    if args.emular:
        from emulador import HASH_ORIGINAL, unicorn
        from test_emulacao_reset_terreno import DiferencialResetTerreno
        b = DiferencialResetTerreno.bancada
        report.update(original_sha256=HASH_ORIGINAL, unicorn=unicorn.__version__,
                      original_entries=dict(b.entradas_originais), reached_stops=dict(b.paradas_atingidas),
                      bounded_segments=b.execucoes, preserved_minimap_resumptions=b.retomadas_minimapa,
                      preserved_loop_head_resumptions=b.retomadas_laco,
                      maximum_native_instructions_per_segment=getattr(b, 'maximo_instrucoes', None),
                      failed_native_segment=getattr(b, 'ultima_falha', None),
                      expected_native_exceptions=0, expected_execution_limits=0,
                      native_instruction_cap=1000000, native_segment_timeout_us=1000000,
                      native_subcalls='Unpatched Random/memset/fill/SetMiniMap and leaf queries; same instruction/'
                                      'CPU/stack at each SetMiniMap-entry, pixel-loop or TerrainReset-loop resume')
    nome = 'reset-terreno-emulada.json' if args.emular else 'reset-terreno-local.json'
    destino = args.relatorio or Path('relatorios')/nome
    if not destino.is_absolute():
        destino = RAIZ/destino
    destino.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'skips'}, indent=2))
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
