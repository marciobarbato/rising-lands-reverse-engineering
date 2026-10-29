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
        self.playback = MacOSM22Playback.open(root)
        self.renderer = GraphicsInspectionRenderer(root, graphics_sources)

    def handle(self, request):
        operation = request.get('operation', 'open')
        if operation in ('open', 'reset'): self.playback.reset()
        elif operation == 'phase': self.playback.step_to_phase(request['phase'])
        elif operation == 'frame': self.playback.step_to_frame(request['frame'])
        elif operation == 'read':
            return dict(read_hex=self.playback.read(int(request['address'], 0), int(request['size'])).hex())
        else: raise ValueError('Unknown playback inspection operation')
        result = self.playback.inspect()
        result['phases'] = list(PHASES)
        result['verified_phases'] = len(self.playback.integrity)
        result['verified_checkpoints'] = sum(bool(i.get('checkpoint_full_state_equal')) for i in self.playback.integrity)
        result['render'] = (dict(status='stop', stage='consumer-input', api_called=False,
                                  code='select_phase', detail='Select a phase to inspect its render')
                            if self.playback.current.phase_index < 0 else self.renderer.render(self.playback))
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
            response = dict(id=request.get('id') if isinstance(request, dict) else None, ok=False, error=str(exc))
        print(json.dumps(response, separators=(',', ':')), flush=True)


if __name__ == '__main__': main()
