"""Combat bootstrap for committed live-memory providers; no execution on import."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
for folder in ('ferramentas', 'pesquisas-paralelas/missoes', 'pesquisas-paralelas/ia-runtime',
               'pesquisas-paralelas/economia', 'pesquisas-paralelas/audio'):
    path = str(ROOT / folder)
    if path not in sys.path:
        sys.path.append(path)
import ambiente_missoes  # noqa: F401,E402
