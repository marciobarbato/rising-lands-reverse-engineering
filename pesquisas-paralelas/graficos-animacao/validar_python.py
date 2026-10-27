"""Executa somente testes Python, sem importar Unicorn ou executar x86."""
import io
import json
import time
import unittest
from graficos import RAIZ
from extrair_evidencias import exigir_area_editavel

exigir_area_editavel()
inicio=time.monotonic();saida=io.StringIO()
suite=unittest.defaultTestLoader.loadTestsFromName('test_graficos')
resultado=unittest.TextTestRunner(stream=saida,verbosity=2).run(suite)
report=dict(resultado='PASSOU' if resultado.wasSuccessful() else 'FALHOU',testes=resultado.testsRun,
            falhas=len(resultado.failures),erros=len(resultado.errors),ignorados=len(resultado.skipped),
            executou_x86=False,duracao_segundos=round(time.monotonic()-inicio,3),log=saida.getvalue())
(RAIZ/'validacao').mkdir(exist_ok=True)
(RAIZ/'validacao/python.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(saida.getvalue())
raise SystemExit(0 if resultado.wasSuccessful() else 1)
