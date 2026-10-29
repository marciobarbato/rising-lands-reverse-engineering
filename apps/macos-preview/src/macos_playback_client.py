"""Serial bridge to the isolated inspection worker; no game input protocol."""
import json
import os
from pathlib import Path
import subprocess
import sys


class MacOSPlaybackClient:
    def __init__(self, source_root, payload, commit, graphics_sources=None):
        self.source_root, self.payload = source_root, Path(payload)
        self.process = None
        self.commit = commit
        self.graphics_sources = graphics_sources

    def request(self, request):
        if self.process is None:
            command = [sys.executable, '-I', '-B', '-u',
                       str(self.payload / 'macos_playback_service.py'), '--source-root', str(self.source_root)]
            for flag, path in [('--graphics-sources', Path(self.graphics_sources) if self.graphics_sources else self.payload / 'graphics-inputs')]:
                if path.is_dir(): command += [flag, str(path)]
            self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                            text=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        if self.process.poll() is not None: raise RuntimeError('Playback inspection worker exited')
        self.process.stdin.write(json.dumps(request) + '\n'); self.process.stdin.flush()
        line = self.process.stdout.readline()
        if not line: raise RuntimeError('Playback inspection worker returned no response')
        response = json.loads(line)
        if response.get('ok'):
            if not isinstance(response.get('playback'), dict): raise RuntimeError('Invalid playback worker response')
            response['playback']['commit'] = self.commit
        return response

    def close(self):
        if self.process is not None:
            self.process.stdin.close()
            try: self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.terminate(); self.process.wait(timeout=5)
            self.process.stdout.close()
            self.process = None
