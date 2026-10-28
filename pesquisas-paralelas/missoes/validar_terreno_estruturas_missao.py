"""Focused Stage11 validation; opt into original-x86 only with --emular."""
import argparse
import json
import os
from pathlib import Path
import sys
import unittest
from ambiente_missoes import OWNED


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular',action='store_true')
    parser.add_argument('--saida',type=Path,default=OWNED/'validacao/stage11-focused-x86.json')
    args=parser.parse_args()
    os.environ['RISING_EMULAR']='1' if args.emular else '0'
    sys.path.insert(0,str(OWNED/'testes'))
    import test_terreno_estruturas_missao as test
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test))
    if args.emular:
        native=test.DiferencialEstruturasMissao.native
        queries=test.DiferencialEstruturasMissao.queries
        report=dict(tests=result.testsRun,skipped=len(result.skipped),errors=len(result.errors),
            failures=len(result.failures),
            original_sha256='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
            independent_capture_sha256=test.CAPTURE_SHA,
            scan_native_entries=native.entradas,scan_returns=native.retornos,
            scan_expected_dependency_stops=native.dependencias,scan_bounded_segments=native.execucoes,
            scan_minimap_resumes=native.retomadas_minimapa,scan_loop_resumes=native.retomadas_laco,
            max_scan_instructions_per_segment=getattr(native,'maximo_instrucoes',None),
            structure_query_entries=test.DiferencialEstruturasMissao.structure_queries,
            mission_query_entries=test.DiferencialEstruturasMissao.mission_queries,
            query_bounded_segments=queries.execucoes,
            native_faults=0 if not result.errors else 'see errors; unclassified',
            compared_blocks={name:dict(base=hex(start),bytes=end-start)
                             for name,(start,end) in native.blocos.items()},
            scope='Exact structure caller and one joined MissionPlaceTerrain, actual committed physical/habitation providers, whole mapped-state byte equality and ordered traces. Explicit synthetic inherited physical/economic/rule input; no complete MissionLoad or real mission runtime.',
            real_mission_runtime_tested=False)
        args.saida.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__=='__main__':
    raise SystemExit(main())
