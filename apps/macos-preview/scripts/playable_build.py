"""Package the committed playable consumer without changing preview outputs."""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    for name in ('data', 'workspace', 'source', 'manifest'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--skip-ui-smoke', action='store_true')
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    revision, mode = manifest['commit'], manifest['mode']
    base = args.data / 'build' / mode / revision
    app_source = args.source / 'apps/macos-preview'
    for name in ('tmp', 'logs', 'module-cache', 'pycache', 'dependencies'):
        (base / 'build' / name).mkdir(parents=True, exist_ok=True)
    # Reuse the existing preview's portable-runtime packaging and compiler IO.
    legacy = load(app_source / 'scripts/build.py', 'preview_builder')
    legacy.ROOT = base
    os.environ.setdefault('RISING_PYTHON_RUNTIME', str(args.workspace / 'local-data/macos-preview/dependencies/python'))
    runtime = legacy.prepare_runtime()
    source_link = base / 'source'
    if not source_link.exists():
        source_link.symlink_to(os.path.relpath(Path(args.source).resolve(), source_link.parent.resolve()), target_is_directory=True)
    shutil.copy2(args.manifest, base / 'snapshot.json')
    assets = load(app_source / 'scripts/preparar_assets.py', 'asset_builder')
    assets.ROOT = base
    original_argv = sys.argv
    try:
        sys.argv = [str(app_source / 'scripts/preparar_assets.py'), str(args.workspace / 'source/cd')]
        assets.main()
    finally:
        sys.argv = original_argv
    from playable_assets import prepare_units, prepare_render_inputs
    prepare_units(args.source, args.workspace / 'source/cd', base / 'assets')
    environment = {**os.environ, 'RISING_APP_ROOT': str(base), 'PYTHONDONTWRITEBYTECODE': '1'}
    check = subprocess.run([str(runtime / 'bin/python3'), '-B', '-m', 'unittest', 'discover',
                            '-s', str(app_source / 'testes'), '-v'], env=environment,
                           cwd=app_source, capture_output=True, text=True)
    (base / 'build/logs/consumer-tests.log').write_text(check.stdout + check.stderr)
    if check.returncode:
        raise SystemExit(check.stdout + check.stderr)
    app = base / 'RisingLands-ptbr.app'
    if app.exists():
        shutil.rmtree(app)
    contents = app / 'Contents'
    resources = contents / 'Resources'
    payload = resources / 'preview'
    (contents / 'MacOS').mkdir(parents=True)
    payload.mkdir(parents=True)
    shutil.copytree(runtime, resources / 'Python')
    shutil.copytree(args.source, payload / 'source', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    legacy.copy_preview_sources(app_source / 'src', payload)
    shutil.copytree(base / 'assets', payload / 'assets')
    prepare_render_inputs(args.source, args.workspace / 'source/cd', payload / 'graphics-inputs')
    shutil.copy2(args.manifest, payload / 'snapshot.json')
    shutil.copy2(base / 'dependencies/runtime-manifest.json', payload / 'runtime-manifest.json')
    plist = {'CFBundleExecutable': 'RisingLands-ptbr', 'CFBundleIdentifier': 'local.risinglands.ptbr',
             'CFBundleName': 'RisingLands-ptbr', 'CFBundleDisplayName': 'RisingLands-ptbr',
             'CFBundlePackageType': 'APPL', 'CFBundleShortVersionString': '0.2.0', 'CFBundleVersion': '2',
             'RisingLandsSourceCommit': revision, 'RisingLandsBuildMode': mode,
             'LSMinimumSystemVersion': '13.0', 'LSArchitecturePriority': ['arm64'],
             'NSHighResolutionCapable': True, 'NSPrincipalClass': 'NSApplication'}
    (contents / 'Info.plist').write_bytes(plistlib.dumps(plist))
    legacy.run(['xcrun', 'swiftc', '-swift-version', '5', '-O', '-target', 'arm64-apple-macosx13.0',
                '-module-cache-path', base / 'build/module-cache', '-framework', 'AppKit', '-framework', 'WebKit',
                app_source / 'src/native/main.swift', '-o', contents / 'MacOS/RisingLands-ptbr'], 'swift-build.log')
    for path in sorted((resources / 'Python').rglob('*.so')):
        legacy.run(['codesign', '--force', '--sign', '-', '--timestamp=none', path])
    legacy.run(['codesign', '--force', '--sign', '-', '--timestamp=none', resources / 'Python/bin/python3'], 'sign-python.log')
    legacy.run(['codesign', '--force', '--sign', '-', '--options', 'runtime', '--timestamp=none', app], 'sign-app.log')
    legacy.run(['codesign', '--verify', '--deep', '--strict', '--verbose=2', app], 'codesign-verify.log')
    legacy.run(['file', contents / 'MacOS/RisingLands-ptbr', resources / 'Python/bin/python3'], 'architecture.log')
    # Verify binding and relocatability using the bundled interpreter and sources.
    from playable_verify import verify
    verify(app)
    dist = args.data / 'dist'
    if mode == 'development':
        dist /= 'development'
    dist.mkdir(parents=True, exist_ok=True)
    final = dist / app.name
    # Preserve prior builds, including a failed previous smoke candidate.
    if final.exists():
        archive = args.data / 'previous' / (mode + '-' + datetime.datetime.now().strftime('%Y%m%dT%H%M%S%f'))
        archive.parent.mkdir(parents=True, exist_ok=True)
        final.rename(archive)
    app.rename(final)
    verify(final)
    if not args.skip_ui_smoke:
        smoke, screenshot = base / 'build/logs/native-smoke.json', base / 'build/logs/native-smoke.png'
        smoke.unlink(missing_ok=True)
        proc = subprocess.run(['open', '-W', '-n', str(final), '--args', '--smoke-test', str(smoke),
                               '--screenshot', str(screenshot)], capture_output=True, text=True, timeout=60,
                              env={k: v for k, v in os.environ.items() if k not in ('RISING_APP_ROOT', 'PYTHONPATH', 'PYTHONHOME')})
        (base / 'build/logs/native-process.log').write_text('LaunchServices exit: ' + str(proc.returncode) + '\n' + proc.stdout + proc.stderr)
        result = json.loads(smoke.read_text()) if smoke.exists() else {'passed': False, 'error': 'Smoke output missing'}
        if proc.returncode or not result.get('passed') or not result.get('nativeWindowVisible') or result.get('commit') != revision:
            raise SystemExit('Falha na validação da janela: ' + json.dumps(result, ensure_ascii=False))
    if not args.skip_ui_smoke:
        inspection = base / 'build/logs/native-inspection-smoke.json'
        inspection.unlink(missing_ok=True)
        proc = subprocess.run(['open', '-W', '-n', str(final), '--args', '--inspection',
                               '--smoke-test', str(inspection)], capture_output=True, text=True, timeout=60,
                              env={k: v for k, v in os.environ.items() if k not in ('RISING_APP_ROOT', 'PYTHONPATH', 'PYTHONHOME')})
        (base / 'build/logs/native-inspection-process.log').write_text(proc.stdout + proc.stderr)
        result = json.loads(inspection.read_text()) if inspection.exists() else {'passed': False}
        if proc.returncode or not result.get('passed') or result.get('commit') != revision:
            raise SystemExit('Native inspection smoke failed: ' + json.dumps(result))
    report = {'commit': revision, 'mode': mode, 'features': manifest['features'], 'bundle': str(final),
              'uiSmoke': not args.skip_ui_smoke, 'logs': str(base / 'build/logs'),
              'builtAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'files': [{'path': str(p.relative_to(final)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                        for p in sorted(final.rglob('*')) if p.is_file()]}
    (dist / 'build-manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(str(final.resolve()), flush=True)


if __name__ == '__main__':
    main()
