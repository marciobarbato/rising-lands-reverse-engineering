"""Consume Graphics API 1.0 in an isolated inspection process. No drawing code."""
import base64
import importlib.util
from pathlib import Path
import sys
from macos_state_consumer import StateValidationError, _sha

EXPECTED_GRAPHICS_VERSION = (1, 0)


class GraphicsVersionError(StateValidationError):
    pass


def load_graphics(root):
    folder = Path(root) / 'pesquisas-paralelas/graficos-animacao'
    # The worker owns its flat module namespace; never import this in the
    # synthetic engine, where Economy's construcoes module is already loaded.
    for name, module in list(sys.modules.items()):
        if name in ('graficos', 'construcoes', 'quadro_jogo'):
            path = getattr(module, '__file__', None)
            if path is None or Path(path).resolve().parent != folder.resolve():
                raise StateValidationError('Graphics requires an isolated provider namespace: ' + name)
    if str(folder) not in sys.path: sys.path.insert(0, str(folder))
    spec = importlib.util.spec_from_file_location('_macos_graphics_render', folder / 'render_quadro.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    require_version(module.VERSAO_RENDER_QUADRO)
    return module


def require_version(version):
    if version != EXPECTED_GRAPHICS_VERSION:
        raise GraphicsVersionError('Graphics API version mismatch: expected (1, 0), got ' + repr(version))


class GraphicsInspectionRenderer:
    def __init__(self, root, graphics_sources=None, surface_source=None):
        self.api = load_graphics(root)
        self.graphics_sources = graphics_sources
        self.surface_source = surface_source
        self.catalog = None
        self.encode_png = sys.modules['graficos'].png

    def render(self, playback):
        require_version(self.api.VERSAO_RENDER_QUADRO)
        image = playback.current
        try:
            previous = playback.previous_surface(self.surface_source(playback) if self.surface_source else None)
        except StateValidationError as exc:
            return dict(status='stop', stage='consumer-input', api_called=False,
                        code='missing_previous_surface' if str(exc).startswith('Missing previous surface') else 'invalid_previous_surface', detail=str(exc), version=[1, 0])
        called = False
        try:
            if self.catalog is None:
                self.catalog = self.api.Catalogo(fontes=self.graphics_sources)
            # Omit habitado deliberately: no fabricated Economy callback. The
            # published Graphics API reports its named stop when it needs one.
            called = True
            result = self.api.renderizar_quadro(image, superficie_anterior=previous, catalogo=self.catalog)
            require_version(result.versao)
            if (result.largura, result.altura) != (800, 600) or len(result.rgba) != 1920000 or len(result.pixels) != 480000:
                raise StateValidationError('Graphics API returned an invalid image extent')
            # PNG encoding is provided by Graphics too; the shell only displays it.
            png = self.encode_png(result.largura, result.altura, result.rgba)
            return dict(status='partial' if result.parada else 'full', stage='graphics', api_called=True,
                        version=list(result.versao), stop=result.parada, width=result.largura,
                        height=result.altura, pixels_sha256=_sha(result.pixels), rgba_sha256=_sha(result.rgba),
                        image='data:image/png;base64,' + base64.b64encode(png).decode(),
                        calls=len(result.chamadas), effects=list(result.efeitos))
        except GraphicsVersionError:
            raise
        except (OSError, ValueError, KeyError) as exc:
            return dict(status='stop', stage='graphics-input', api_called=called,
                        code='graphics_input_unavailable', detail=str(exc), version=[1, 0])
