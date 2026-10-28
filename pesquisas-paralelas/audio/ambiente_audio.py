"""Resolve committed providers and read-only original inputs for audio research."""
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OWNED = Path(__file__).resolve().parent
CD = ROOT.parent / 'source/cd'
SOUND = CD / 'INSTALHD/SOUND'
for path in (ROOT / 'ferramentas', ROOT / '.local/python', ROOT.parent / 'source/python'):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

ORIGINAL_SHA256 = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
ANALYSIS_SHA256 = '26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0'

# Size and SHA-256 of the original banks on the read-only CD copy. This front
# records them because relatorios/fontes.json does not list INSTALHD/SOUND.
IDENTIDADES = {
    'A.HED': (372, 'e98c8cbe1c7734b638c008c905b68bdb2023f185327c3b7ec86b88d5e7707072'),
    'A.SND': (525824, 'ec4874144eca50ddab6bc8fbb5f9db86d06d77960bd6a3e7ec313b2c9288f60b'),
    'B.HED': (2872, '48bf0fbc8c7f93963c3ff2d9ad79963fade15ae165a685f6f30e2e440107bd4a'),
    'B.SND': (1675264, '9b617f4bbb47c5de05ea9a29af1dae03f53ab77b57ed8c8b15582c76126079f3'),
    'P.HED': (10312, '05170234f723c1e9e10c0edf494a432f7dc4fbd4a5c2b917f953b50cace4c66e'),
    'P.SND': (10337891, 'c1193ed24382ba755e0e026c65e51dfc27264e0b480722e7c5779b918a94a977'),
}
LETRAS_BANCO = 'ABP'


def ler_original(nome):
    """Read one original bank file, checked against the recorded identity."""
    dados = (SOUND / nome).read_bytes()
    if (len(dados), hashlib.sha256(dados).hexdigest()) != IDENTIDADES.get(nome):
        raise ValueError(f'Original sound file identity mismatch: {nome}')
    return dados
