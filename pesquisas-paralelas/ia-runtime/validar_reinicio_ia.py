"""Run the owning AI/runtime suite with an explicit, separate recovery report."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

from ambiente_ia_runtime import EVIDENCE, ORIGINAL_SHA256, OWNED, ROOT


def validar(emular, destino):
    if emular:
        os.environ['RISING_EMULAR'] = '1'
    else:
        os.environ.pop('RISING_EMULAR', None)
    suite = unittest.defaultTestLoader.discover(str(OWNED / 'testes'), pattern='test_*.py')
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    classe = sys.modules['test_reinicio_ia'].FreshNativeWholeImages
    arquivos = ('reinicio_ia.py', 'memoria_ia_runtime.py', 'oraculo_reinicio_ia.py', 'capturar_reinicio_ia.py',
                'auditar_reinicio_ia.py', 'testes/test_reinicio_ia.py', 'validar_reinicio_ia.py')
    fontes = {str((OWNED / nome).relative_to(ROOT)): hashlib.sha256((OWNED / nome).read_bytes()).hexdigest()
              for nome in arquivos}
    dependencias = ('ferramentas/cadencia.py', 'ferramentas/emulador.py', 'ferramentas/simbolos_ia.py',
                    'pesquisas-paralelas/missoes/carregador_unidades.py',
                    'pesquisas-paralelas/missoes/carregador_estruturas.py',
                    'pesquisas-paralelas/missoes/carregador_cadeia_auxiliar.py')
    fontes.update({nome: hashlib.sha256((ROOT / nome).read_bytes()).hexdigest() for nome in dependencias})
    relatorio = dict(round='CXR-20261028-01', utc=datetime.now(timezone.utc).isoformat(),
        git_head_before_report=subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
        original_sha256=ORIGINAL_SHA256, native=emular, successful=resultado.wasSuccessful(),
        tests=resultado.testsRun, skips=[dict(test=t.id(), reason=razao) for t, razao in resultado.skipped],
        failures=[dict(test=t.id(), detail=d) for t, d in resultado.failures],
        errors=[dict(test=t.id(), detail=d) for t, d in resultado.errors],
        source_sha256=fontes,
        original_capture_sha256=hashlib.sha256((EVIDENCE / 'captura-reinicio-original.json').read_bytes()).hexdigest(),
        static_audit_sha256=hashlib.sha256((EVIDENCE / 'reinicio-byte-audit.json').read_bytes()).hexdigest(),
        fresh_capture=getattr(classe, 'captura_fresca', None),
        fresh_differential=getattr(classe, 'comparacoes_frescas', None),
        intentional_native_cycle=getattr(classe, 'ciclo_nativo', None),
        scope='Initialization providers and fixture comparisons only; no production provider adapter, full MissionLoad or frame runtime')
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(relatorio, indent=1) + '\n', encoding='utf-8')
    return 0 if resultado.wasSuccessful() else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true')
    parser.add_argument('--relatorio', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(validar(args.emular, args.relatorio))
