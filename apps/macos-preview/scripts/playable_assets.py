"""Derive body atlases with the committed opacity/palette and verified mappings."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil


def prepare_units(source, cd, output):
    module_path = source / 'pesquisas-paralelas/graficos-animacao/graficos.py'
    spec = importlib.util.spec_from_file_location('playable_graphics', module_path)
    graphics = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[spec.name] = graphics
    spec.loader.exec_module(graphics)
    inputs = output.parent / 'graphics-inputs'
    inputs.mkdir(exist_ok=True)
    shutil.copy2(module_path.parent / 'fontes/manifesto.json', inputs / 'manifesto.json')
    if not (inputs / 'cd').exists():
        (inputs / 'cd').symlink_to(os.path.relpath(Path(cd).resolve(), inputs.resolve()), target_is_directory=True)
    catalog = graphics.Catalogo(inputs)
    palette = catalog.paleta()
    metadata = {}
    frames = {}
    for kind in (0, 7, 9):
        for direction in range(1, 17):
            for phase in range(8):
                for bag in (0, 1):
                    query = graphics.consultar(kind, 'andando', direction, phase, bolsa_u16=bag)
                    frame_id = query['id_motor']
                    frames[frame_id] = catalog.quadro(frame_id)
                    metadata[f'{kind}/{direction}/{phase}/{bag}'] = frame_id
    cols, size = 16, 96
    width, height = cols * size, ((len(frames) + cols - 1) // cols) * size
    rgba = bytearray(width * height * 4)
    atlas = {}
    for i, (frame_id, frame) in enumerate(sorted(frames.items())):
        if frame.largura > size or frame.altura > size:
            raise ValueError('Body exceeds atlas cell')
        x, y = (i % cols) * size, (i // cols) * size
        pixels = graphics.rgba(frame, palette)
        for row in range(frame.altura):
            offset = ((y + row) * width + x) * 4
            rgba[offset:offset + frame.largura * 4] = pixels[row * frame.largura * 4:(row + 1) * frame.largura * 4]
        atlas[str(frame_id)] = {'x': x, 'y': y, 'w': frame.largura, 'h': frame.altura}
    (output / 'unidades.png').write_bytes(graphics.png(width, height, rgba))
    (output / 'unidades.json').write_text(json.dumps({'queries': metadata, 'frames': atlas,
        'anchors': {str(t): graphics.TIPOS[t]['ancora'] for t in (0, 7, 9)},
        'contract': 'Verified player-0 base bodies in states 2/7. Other states/owners use explicit markers.'}) + '\n')
    # Replace only new generated terrain output, preserving explicit opaque zero.
    terrain = catalog.banco('BLOCS.CMP')
    width, height = 1024, ((len(terrain) + 31) // 32) * 32
    pixels = bytearray(width * height * 4)
    for i, frame in enumerate(terrain):
        body = graphics.rgba(frame, palette)
        x, y = i % 32 * 32, i // 32 * 32
        for row in range(frame.altura):
            offset = ((y + row) * width + x) * 4
            pixels[offset:offset + frame.largura * 4] = body[row * frame.largura * 4:(row + 1) * frame.largura * 4]
    (output / 'terreno.png').write_bytes(graphics.png(width, height, pixels))
    provenance = json.loads((output / 'fontes.json').read_text())
    provenance['graphicsProvider'] = str(module_path.relative_to(source))
    provenance['outputs'] = [{'path': p.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}
                             for p in sorted(output.iterdir()) if p.is_file() and p.name != 'fontes.json']
    (output / 'fontes.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
