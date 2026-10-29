"""Fresh remap lifecycle validation; never rewrites original-only captures."""
import argparse
import json
import os
from pathlib import Path
import sys
import unittest

RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/'testes'))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular',action='store_true');p.add_argument('--relatorio',type=Path)
    args=p.parse_args();os.environ['RISING_EMULAR']='1' if args.emular else '0'
    from validar import Resultado
    r=unittest.TextTestRunner(verbosity=2,resultclass=Resultado).run(unittest.defaultTestLoader.loadTestsFromNames(
        ('test_conclusao_remapeamento','test_emulacao_conclusao_remapeamento')))
    report=dict(tests=r.testsRun,failures=len(r.failures),errors=len(r.errors),
                skips=[dict(test=t.id(),reason=s) for t,s in r.skipped],success=r.wasSuccessful(),
                bounded_segments=r.execucoes_x86,x86_enabled=args.emular,
                scope='Complete natural Chemin_Remap over explicit inherited fixtures/resources, plus separate low-u16 final-tail test; no MissionLoad')
    if args.emular:
        from test_emulacao_conclusao_remapeamento import DiferencialConclusaoRemapeamento
        b=DiferencialConclusaoRemapeamento.bancada
        report.update(original_entries=dict(b.origens_conclusao),whole_remap_segments=b.execucoes,
                      binding_resumptions=b.retomadas_vinculos,preserved_loop_resumptions=b.retomadas_laco,
                      maximum_segment_instructions=getattr(b,'maximo_instrucoes',None),
                      observations=DiferencialConclusaoRemapeamento.observacoes,
                      tail_entries=getattr(getattr(DiferencialConclusaoRemapeamento,'bancada_cauda',None),'execucoes',0),
                      intentional_null_lock_original_fault='UC_ERR_WRITE_UNMAPPED at0x42efd9; exact capture case only',
                      full_mission_load='NOT RUN')
    destino=args.relatorio or Path('relatorios')/('conclusao-remapeamento-emulada.json' if args.emular else 'conclusao-remapeamento-local.json')
    if not destino.is_absolute():destino=RAIZ/destino
    destino.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
    return 0 if r.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
