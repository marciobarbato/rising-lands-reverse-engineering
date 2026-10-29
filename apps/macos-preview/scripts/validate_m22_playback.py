"""Verify all accepted phases and record render attempts without inventing pixels."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import argparse
import json
from collections import Counter
from macos_m22_playback import MacOSM22Playback, PHASES, PINS, SCENARIO
from macos_graphics_inspection import GraphicsInspectionRenderer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--graphics-sources', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    player = MacOSM22Playback.open(args.source_root)
    renderer = GraphicsInspectionRenderer(args.source_root, args.graphics_sources)
    phases = []
    for index, name in enumerate(PHASES):
        image = player.step_to_phase(index)
        render = renderer.render(player)
        render.pop('image', None)
        phases.append(dict(phase=name, summary_verified=True, checkpoint_verified=image.checkpoint,
                           state_sha256=image.summary_sha256, observed=image.observed_words(), render=render))
        if index % 64 == 0: print('Verified phase', index, name, flush=True)
    result = dict(scenario=SCENARIO, inputs=PINS, phases_verified=len(phases),
                  checkpoints_verified=sum(p['checkpoint_verified'] for p in phases),
                  render_counts=dict(Counter(p['render']['status'] for p in phases)),
                  graphics_api_calls=sum(p['render']['api_called'] for p in phases),
                  phases=phases)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('phases','inputs')}))


if __name__ == '__main__': main()
