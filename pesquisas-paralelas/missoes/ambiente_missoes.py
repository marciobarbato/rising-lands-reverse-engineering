"""Resolve committed providers and read-only local inputs for mission research."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OWNED = Path(__file__).resolve().parent
CD = ROOT.parent / 'source/cd'
for path in (ROOT / 'ferramentas', ROOT / 'pesquisas-paralelas/combate',
             ROOT / 'pesquisas-paralelas/economia', ROOT / '.local/python',
             ROOT.parent / 'source/python'):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
