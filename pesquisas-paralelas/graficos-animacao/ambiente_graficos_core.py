"""Graphics' bootstrap for Core's committed, native-validated UI-zone provider.

No foreign implementation hash is pinned. Keep the existing flat module identity
and reject a provider imported from a different checkout.
"""
import importlib,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def zonas_core():
    core=ROOT/'ferramentas';name='chamadas_quadro_core'
    if name in sys.modules:
        module=sys.modules[name]
        if Path(module.__file__).resolve()!=(core/(name+'.py')).resolve():
            raise ImportError('Core UI provider belongs to another checkout')
        return module
    if str(core) not in sys.path:sys.path.append(str(core))
    return importlib.import_module(name)
