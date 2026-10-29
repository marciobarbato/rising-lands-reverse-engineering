"""Load the two different construction providers without replacing a module.

Bootstrap in a fresh consumer process before legacy flat construction imports.
Existing compatible providers are reused by identity; foreign bindings fail.
No search path, provider source, game data or existing module is rewritten.
"""
import importlib.util
from pathlib import Path
import sys
from threading import RLock

ROOT = Path(__file__).resolve().parents[1]
ECONOMY = ROOT / 'pesquisas-paralelas/economia'
GRAPHICS = ROOT / 'pesquisas-paralelas/graficos-animacao'
_LOCK = RLock()
_GRAPHICS_STRUCTURES = '_risinglands_graphics_construcoes'


def _check(name, path):
    if name not in sys.modules:
        return
    module = sys.modules[name]
    source = getattr(module, '__file__', None)
    if source is None or Path(source).resolve() != path.resolve():
        raise ImportError(
            'Provider {!r} is already bound to {!r}; expected {}. '
            'Start a fresh consumer and use the explicit provider loaders.'
            .format(name, source, path))


def _load_providers(entries):
    # Bootstrap is serialized among these loaders. Call before unrelated
    # legacy imports or worker threads start; no global import hooks are used.
    with _LOCK:
        for name, path in entries:
            _check(name, path)
        for name, path in entries:
            if name in sys.modules:
                continue
            spec = importlib.util.spec_from_file_location(name, path)
            if spec is None or spec.loader is None:
                raise ImportError('Cannot load committed provider: ' + str(path))
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module  # A new normal binding, never a swap.
            try:
                spec.loader.exec_module(module)
            except BaseException:
                if sys.modules.get(name) is module:
                    del sys.modules[name]  # Normal failed-import cleanup only.
                raise
        return sys.modules[entries[-1][0]]


def load_graphics_structures():
    """Return the unchanged graphic structures module under a unique name.

    Its actual Catalogo/Quadro dependency remains the shared graphics provider.
    The ambiguous flat name 'construcoes' is never claimed by this loader.
    """
    return _load_providers((
        ('graficos', GRAPHICS / 'graficos.py'),
        (_GRAPHICS_STRUCTURES, GRAPHICS / 'construcoes.py'),
    ))


def load_economy_bonus():
    """Return Economy's actual bonus_unidades module (BonusGetValEngin owner).

    Public replacement for consumers that previously called the private
    loader with the same two entries; identities are checked the same way.
    """
    return _load_providers((
        ('economia', ECONOMY / 'economia.py'),
        ('bonus_unidades', ECONOMY / 'bonus_unidades.py'),
    ))


def load_economy_resources():
    """Return actual extracao with its same-checkout economic dependencies.

    The existing economy modules retain their flat names/class identities.
    All required bindings are checked before importing any missing dependency.
    """
    return _load_providers((
        ('economia', ECONOMY / 'economia.py'),
        ('construcoes', ECONOMY / 'construcoes.py'),
        ('extracao', ECONOMY / 'extracao.py'),
    ))
