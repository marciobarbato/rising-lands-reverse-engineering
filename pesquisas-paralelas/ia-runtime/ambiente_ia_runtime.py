"""Resolve committed providers and read-only local inputs for AI/runtime research."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OWNED = Path(__file__).resolve().parent
EVIDENCE = OWNED / 'evidencias'
CD = ROOT.parent / 'source/cd'
EXE = CD / 'INSTALHD/RISING.EXE'
SBL = CD / 'INSTALHD/RISING.SBL'
# The intact executable is the only execution oracle; the normalized PE is analysis-only.
ORIGINAL_SHA256 = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
ANALYSIS_SHA256 = '26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0'
for path in (ROOT, ROOT / 'ferramentas', ROOT / '.local/python', ROOT.parent / 'source/python'):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
if str(OWNED) not in sys.path:
    sys.path.insert(0, str(OWNED))
