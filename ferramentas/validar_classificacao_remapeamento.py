"""Fresh Stage16 validation, separate from preserved capture/predecessor reports."""
import argparse
import json
import os
from pathlib import Path
import platform
import sys
import unittest

RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/'testes'))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--emular',action='store_true')
    p.add_argument('--relatorio',type=Path);args=p.parse_args()
    os.environ['RISING_EMULAR']='1' if args.emular else '0'
    from validar import Resultado
    nomes=('test_vinculos_declarados','test_classificacao_remapeamento','test_emulacao_classificacao_remapeamento')
    r=unittest.TextTestRunner(verbosity=2,resultclass=Resultado).run(unittest.defaultTestLoader.loadTestsFromNames(nomes))
    out=dict(python=platform.python_version(),x86_enabled=args.emular,tests=r.testsRun,failures=len(r.failures),
             errors=len(r.errors),skips=[dict(test=t.id(),reason=s) for t,s in r.skipped],
             bounded_x86_executions=r.execucoes_x86,success=r.wasSuccessful(),
             scope='Declared boundaries, remap allocation/classification and readonly initialization queries; no labeling/full remap or full MissionLoad')
    if args.emular:
        from emulador import HASH_ORIGINAL,unicorn
        from test_emulacao_classificacao_remapeamento import DiferencialClassificacaoRemapeamento
        b=DiferencialClassificacaoRemapeamento.bancada
        consultas=getattr(DiferencialClassificacaoRemapeamento,'bancada_consultas',None)
        io=getattr(DiferencialClassificacaoRemapeamento,'bancada_io',None)
        out.update(original_sha256=HASH_ORIGINAL,unicorn=unicorn.__version__,
                   original_remap_calls=dict(b.origens),binding_resumptions=b.retomadas_vinculos,
                   preserved_loop_resumptions=b.retomadas_laco,remap_bounded_segments=b.execucoes,
                   remap_reached_stops=dict(b.paradas_atingidas),
                   maximum_remap_segment_instructions=getattr(b,'maximo_instrucoes',None),
                   failed_native_segment=getattr(b,'ultima_falha',None),
                   intentional_lock_fixture_stops=DiferencialClassificacaoRemapeamento.lock_stops,
                   intentional_binding_budget_failures=DiferencialClassificacaoRemapeamento.binding_limits,
                   readonly_query_entries=getattr(consultas,'execucoes',0),
                   io_wrapper_entries=getattr(DiferencialClassificacaoRemapeamento,'origens_io',[]),
                   io_bounded_segments=getattr(io,'execucoes',0),
                   expected_native_instruction_or_wall_limits=0,expected_native_faults=0,
                   full_flow_status='NOT RUN: no final Chemin_Remap return or MissionLoad composition')
    destino=args.relatorio or Path('relatorios')/('classificacao-remapeamento-emulada.json' if args.emular else 'classificacao-remapeamento-local.json')
    if not destino.is_absolute():destino=RAIZ/destino
    destino.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
    return 0 if r.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
