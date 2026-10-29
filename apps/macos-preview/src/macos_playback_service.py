"""Isolated JSON-lines inspection service; separate from the synthetic engine."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import argparse
import json
from macos_m22_playback import MacOSM22Playback, PHASES
from macos_graphics_inspection import GraphicsInspectionRenderer


class PlaybackInspectionService:
    def __init__(self, root, graphics_sources=None):
        # Refuse unsupported render versions before opening/publishing playback.
        self.renderer = GraphicsInspectionRenderer(root, graphics_sources)
        self.playback = MacOSM22Playback.open(root)
        self.render_playback = self.playback.fork()

    def _render_to(self, index):
        if index < self.renderer.index:
            self.renderer.reset(); self.render_playback.reset()
        for i in range(self.renderer.index + 1, index + 1):
            image = self.render_playback.step_to_phase(i)
            memory = self.render_playback.drawing_input() if image.phase_name.startswith('between_frames') else None
            self.renderer.consume(image, memory)
        return self.renderer.present()

    def handle(self, request):
        operation = request.get('operation', 'open')
        p = self.playback
        previous = p._state, p._previous, p._index, p._current
        try:
            if operation in ('open', 'reset'):
                p.reset(); self.renderer.reset(); self.render_playback.reset()
            elif operation == 'phase': p.step_to_phase(request['phase'])
            elif operation == 'frame': p.step_to_frame(request['frame'])
            elif operation == 'read':
                return dict(read_hex=p.read(int(request['address'], 0), int(request['size'])).hex())
            else: raise ValueError('Unknown playback inspection operation')
            render = self._render_to(p.current.phase_index)
        except Exception:
            p._state, p._previous, p._index, p._current = previous
            raise
        result = p.inspect()
        result['phases'] = list(PHASES)
        result['verified_phases'] = len(p.integrity)
        result['verified_checkpoints'] = sum(bool(i.get('checkpoint_full_state_equal')) for i in p.integrity)
        result['render'] = render
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', required=True, type=Path)
    parser.add_argument('--graphics-sources', type=Path)
    args = parser.parse_args()
    service = None
    for line in sys.stdin:
        request = {}
        try:
            request = json.loads(line)
            if not isinstance(request, dict): raise ValueError('Inspection request must be an object')
            if service is None:
                service = PlaybackInspectionService(args.source_root, args.graphics_sources)
            response = dict(id=request.get('id'), ok=True, playback=service.handle(request))
        except Exception as exc:
            response = dict(id=request.get('id') if isinstance(request, dict) else None, ok=False, error=str(exc), error_type=type(exc).__name__)
        print(json.dumps(response, separators=(',', ':')), flush=True)


if __name__ == '__main__': main()
