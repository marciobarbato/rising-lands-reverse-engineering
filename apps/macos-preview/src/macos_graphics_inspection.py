"""Consume Graphics API 1.7 in an isolated inspection process. No drawing code."""
import base64
import importlib.util
from pathlib import Path
import sys
from macos_state_consumer import StateValidationError, _sha

EXPECTED_GRAPHICS_VERSION = (1, 7)


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
        raise GraphicsVersionError('Graphics API version mismatch: expected (1, 7), got ' + repr(version))


GRAPHICS_EVIDENCE = 'pesquisas-paralelas/graficos-animacao/evidencias/'
RENDER_PINS = {
    'superficie-inicial-m22-v2.json': '4581aafab6685f5f118317c2b5debcb158ca85f7212e477bc0a6fe155e0c0ff7',
    'cache-terreno-inicial-m22-v2.json': 'da8f2bf58bf5b6832a0b21c00356c76e7a8a027c3cfa56001757a8dec0da2962',
    'verificacao-cadeia-m22-v2-api17-128.json': '4448aeb44920d89b271e9af276477ee545fe797164b5b654e26c18a545d1a16c',
    'superficies-fase-m22-v2.json': 'ded5d695083877eb046334d9e931c2f4a91d70681966e2295a4be0fbc140160a',
}


class GraphicsInspectionRenderer:
    """Sequential cache/surface consumer; no independent mid-sequence start.

    Returned 'full' includes the HUD/cursor in Graphics' published domain.
    'undrawn' carries the previous complete or explicitly partial surface.
    """
    def __init__(self, root, graphics_sources=None):
        import json
        self.root = Path(root)
        self.api = load_graphics(root)
        self.folder = self.root / GRAPHICS_EVIDENCE
        for name, expected in RENDER_PINS.items():
            if _sha((self.folder/name).read_bytes()) != expected:
                raise StateValidationError('Unpinned Graphics artifact: ' + name)
        self.catalog = self.api.Catalogo(fontes=graphics_sources)
        self.encode_png = sys.modules['graficos'].png
        self.references = {r['frame']: r for r in json.loads((self.folder/'verificacao-cadeia-m22-v2-api17-128.json').read_bytes())['rows']}
        self.phase_hashes = {r['phase']: r['offscreen'] for r in json.loads((self.folder/'superficies-fase-m22-v2.json').read_bytes())['phases']}
        self.initial_pixels = self.api.carregar_superficie_inicial(self.folder/'superficie-inicial-m22-v2.json')
        self.initial_cache = self.api.carregar_cache_inicial(self.folder/'cache-terreno-inicial-m22-v2.json', catalogo=self.catalog)
        if _sha(self.initial_pixels) != self.phase_hashes['load_tail']:
            raise StateValidationError('Initial surface does not match accepted load-tail hash')
        self.palette=self.catalog.paleta()
        self.reset()

    def reset(self):
        require_version(self.api.VERSAO_RENDER_QUADRO)
        self.pixels, self.cache = self.initial_pixels, self.initial_cache
        self.index = -1
        self.last = None
        self.records = []

    def consume(self, image, memory=None):
        from macos_habitation_view import habitation_query
        require_version(self.api.VERSAO_RENDER_QUADRO)
        if image.phase_index != self.index + 1:
            raise StateValidationError('Render sequence must advance from the initial artifacts in phase order')
        name = image.phase_name
        drawing = name.startswith('between_frames')
        result = None
        regions = []
        next_pixels, next_cache = self.pixels, self.cache
        if drawing:
            if memory is None: raise StateValidationError('Drawing phase requires captured AffGame-entry memory')
            for start, end, label in self.api.regioes_necessarias(memory, hud=True):
                data = memory.ler_mundo(start, end - start)
                if len(data) != end - start:
                    raise StateValidationError('Incomplete Graphics region: ' + label)
                regions.append(dict(name=label, base=hex(start), bytes=end - start))
            result = self.api.renderizar_quadro(memory, superficie_anterior=self.pixels,
                         cache=self.cache, catalogo=self.catalog, paleta=getattr(self,'palette',None), habitado=habitation_query(self.root, memory), hud=True)
            require_version(result.versao)
            if ((result.largura, result.altura) != (800, 600) or len(result.pixels) != 480000
                    or len(result.rgba) != 1920000 or result.cache is None):
                raise StateValidationError('Invalid Graphics 1.7 result shape/cache')
            next_pixels, next_cache = result.pixels, result.cache
        stop = result.parada if result else None
        status = ('partial' if stop else 'full') if drawing else 'undrawn'
        if result is not None and result.chamadas == (('CalculFrame',),): status = 'undrawn'
        frame = (1 if name == 'between_frames' else int(name[len('between_frames'):])) if drawing else None
        record = dict(status=status, phase=name, api_called=drawing, version=[1, 7], hud=True, stop=stop,
                      required_regions=regions,
                      pixels_sha256=_sha(next_pixels), cache_keys_sha256=_sha(next_cache.registros),
                      cache_payloads_sha256=_sha(next_cache.blocos_crus), cache_cursor=next_cache.proximo,
                      limitations=['Graphics HUD domain only; unsupported states return named stops', 'no independent mid-sequence cache', 'static palette; palette cycling not applied'],
                      native_phase_end_sha256=self.phase_hashes.get(name),
                      equals_native_phase_end=(_sha(next_pixels) == self.phase_hashes[name] if name in self.phase_hashes else None))
        if drawing:
            record['memory_phase'] = memory.phase_name
            record['memory_summary_sha256'] = memory.summary_sha256
        if frame in self.references:
            reference = self.references[frame]
            record.update(checkpoint_reference_frame=frame,
                          graphics_chain_sha256=reference['chained']['sha256'],
                          graphics_chain_equal=_sha(next_pixels) == reference['chained']['sha256'],
                          native_full_surface_sha256=reference['native_full_surface_sha256'],
                          equals_native_full_surface=_sha(next_pixels) == reference['native_full_surface_sha256'],
                          reference_first_differing_row=reference['chained']['first_row'])
            if not record['graphics_chain_equal']:
                raise StateValidationError('Graphics checkpoint chain mismatch at frame ' + str(frame))
        effective_stop = stop if result else (self.last.parada if self.last else None)
        if effective_stop is None and record['equals_native_phase_end'] is False:
            raise StateValidationError('Native phase-end surface mismatch at phase ' + name)
        # Publish only after version, region, shape and full-surface checks pass.
        self.pixels, self.cache, self.index = next_pixels, next_cache, image.phase_index
        self.last = result if result is not None else self.last
        self.records.append(record)
        return record

    def present(self, raw=False):
        if self.index < 0:
            return dict(status='undrawn', api_called=False, version=[1, 7], hud=True,
                        detail='Initial surface is available only after the load tail; select a phase')
        record = dict(self.records[-1])
        if raw:
            record['frame']=dict(format='indexed8-rgb24/1',width=800,height=600,stride=800,
                                 pixels=base64.b64encode(self.pixels).decode('ascii'),
                                 palette=base64.b64encode(self.palette).decode('ascii'),
                                 pixels_sha256=record['pixels_sha256'],generation=self.index)
            if record['status']=='undrawn' and self.last and self.last.parada:
                record['inherited_stop']=self.last.parada
            return record
        # Use only Graphics' palette expansion and PNG encoder. No game drawing.
        if self.last is None:
            graphics = sys.modules['graficos']
            rgba = graphics.rgba(graphics.Quadro(800, 600, self.pixels, b'\xff'*480000, 0, b''), self.catalog.paleta())
        else:
            rgba = self.last.rgba
        png = self.encode_png(800, 600, rgba)
        record['image'] = 'data:image/png;base64,' + base64.b64encode(png).decode()
        record['detail'] = 'HUD and cursor enabled within the Graphics domain. Cache starts only at frame 1 entry.'
        if record['status'] == 'undrawn' and self.last and self.last.parada:
            record['inherited_stop'] = self.last.parada
        return record
