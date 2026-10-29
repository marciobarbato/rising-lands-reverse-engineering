"""Package the committed playable consumer without changing preview outputs."""
import argparse
import datetime
import hashlib
import io
import tarfile
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
    # Explicit development override while ABI1.3 is awaiting coordinator integration.
    engine_source=Path(os.environ.get('RISING_MACOS_ENGINE_SOURCE',str(args.source/'motor'))).resolve()
    engine_revision=revision
    if engine_source!=(args.source/'motor').resolve():
        if mode!='development':raise ValueError('External engine source is development-only')
        approved='363faa9c252ffb00d62c81db0da2ee5d4a3d7615'
        engine_revision=subprocess.check_output(['git','-C',str(engine_source.parent),'rev-parse',approved+'^{commit}'],text=True).strip()
        archive=subprocess.check_output(['git','-C',str(engine_source.parent),'archive','--format=tar',approved,'motor'])
        pinned=base/'build/engine-source'
        with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
            for member in stream:
                path=Path(member.name)
                if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0]!='motor':raise ValueError('Invalid pinned engine archive')
                if member.isdir():continue
                if not member.isfile():raise ValueError('Non-file pinned engine input')
                content=stream.extractfile(member).read();target=pinned/path
                if target.exists() and target.read_bytes()!=content:raise ValueError('Pinned engine source modified')
                target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(content)
        engine_source=pinned/'motor'
    if '#define RL_ABI_VERSION 0x00010003u' not in (engine_source/'include/rising_engine.h').read_text():
        raise RuntimeError('RustRendererABI1.3NotIntegrated: build requires the reviewed renderer contract')
    # Build into our ignored target; never mutate either engine source tree.
    legacy.run(['cargo','build','--release','--locked','--manifest-path',engine_source/'Cargo.toml',
                '--target-dir',base/'build/engine-target'], 'rust-engine-build.log')
    library = base/'build/engine-target/release/librising_engine.dylib'
    legacy.run(['cargo','rustc','--release','--locked','-p','rl-ffi','--lib','--crate-type','staticlib',
                '--manifest-path',engine_source/'Cargo.toml','--target-dir',base/'build/engine-target'], 'rust-static-build.log')
    static_library=base/'build/engine-target/release/librising_engine.a'
    static_driver=base/'build/macos-live-static.o'
    static_codec=base/'build/macos-codec-static.o'
    for source,target,extra in [('macos_live_driver.c',static_driver,['-DMACOS_STATIC_ENGINE','-I',engine_source/'include']),('macos_projection_codec.c',static_codec,[])]:
        legacy.run(['xcrun','clang','-O3','-c','-arch','arm64','-mmacosx-version-min=13.0','-Wno-deprecated-declarations',
                    *extra,app_source/'src/native'/source,'-o',target], 'native-static-'+source+'.log')
    projection_library=base/'build/librising_macos_projection.dylib'
    legacy.run(['xcrun','clang','-O3','-dynamiclib','-arch','arm64','-mmacosx-version-min=13.0',
                '-Wno-deprecated-declarations',app_source/'src/native/macos_projection_codec.c',
                '-o',projection_library], 'macos-projection-build.log')
    native_library=base/'build/librising_macos_live.dylib'
    legacy.run(['xcrun','clang','-O3','-dynamiclib','-arch','arm64','-mmacosx-version-min=13.0',
                '-Wno-deprecated-declarations','-I',engine_source/'include',
                app_source/'src/native/macos_projection_codec.c',app_source/'src/native/macos_live_driver.c',
                '-install_name','@rpath/librising_macos_live.dylib','-o',native_library],'native-driver-build.log')
    from prepare_native_macos import prepare
    prepare(args.source,library,args.workspace/'source/cd/INSTALHD/RISING.EXE',base/'graphics-inputs',base/'native-inputs',projection_library)
    environment = {**os.environ, 'RISING_APP_ROOT': str(base), 'PYTHONDONTWRITEBYTECODE': '1',
                   'RL_MACOS_ENGINE_LIBRARY': str(library),
                   'RL_MACOS_PROJECTION_LIBRARY': str(projection_library),
                   'RL_MACOS_NATIVE_LIBRARY': str(native_library),
                   'RL_MACOS_NATIVE_INPUTS': str(base/'native-inputs'),
                   'RL_ORIGINAL_EXE': str(args.workspace/'source/cd/INSTALHD/RISING.EXE')}
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
    shutil.copytree(base/'native-inputs',payload/'native-inputs')
    shutil.copy2(native_library,payload/'librising_macos_live.dylib')
    legacy.run(['codesign','--force','--sign','-','--timestamp=none',payload/'librising_macos_live.dylib'],'sign-native-driver.log')
    shutil.copy2(library,payload/'librising_engine.dylib')
    shutil.copy2(projection_library,payload/'librising_macos_projection.dylib')
    legacy.run(['codesign','--force','--sign','-','--timestamp=none',payload/'librising_macos_projection.dylib'],'sign-projection.log')
    engine_inputs = payload/'engine-inputs'
    engine_inputs.mkdir()
    original = args.workspace/'source/cd/INSTALHD/RISING.EXE'
    if hashlib.sha256(original.read_bytes()).hexdigest() != '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb':
        raise ValueError('Original engine table input hash mismatch')
    shutil.copy2(original,engine_inputs/'RISING.EXE')
    legacy.run(['codesign','--force','--sign','-','--timestamp=none',payload/'librising_engine.dylib'],'sign-engine.log')
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
                '-framework','Metal','-framework','QuartzCore',
                '-import-objc-header',app_source/'src/native/MacOSLiveDriver.h',
                static_driver,static_codec,static_library,
                app_source/'src/native/NativeLiveWindow.swift',app_source / 'src/native/SmokeReadiness.swift', app_source / 'src/native/main.swift', '-o', contents / 'MacOS/RisingLands-ptbr'], 'swift-build.log')
    for path in sorted((resources / 'Python').rglob('*.so')):
        legacy.run(['codesign', '--force', '--sign', '-', '--timestamp=none', path])
    legacy.run(['codesign', '--force', '--sign', '-', '--timestamp=none', resources / 'Python/bin/python3'], 'sign-python.log')
    legacy.run(['codesign', '--force', '--sign', '-', '--options', 'runtime', '--timestamp=none', app], 'sign-app.log')
    legacy.run(['codesign', '--verify', '--deep', '--strict', '--verbose=2', app], 'codesign-verify.log')
    legacy.run(['file', contents / 'MacOS/RisingLands-ptbr', resources / 'Python/bin/python3',payload/'librising_engine.dylib',payload/'librising_macos_projection.dylib'], 'architecture.log')
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
        from native_smoke import run_native_smoke
        smoke_env = {k: v for k, v in os.environ.items() if k not in ('RISING_APP_ROOT', 'PYTHONPATH', 'PYTHONHOME')}
        for inspection in (False, True):
            stem = 'native-inspection-smoke' if inspection else 'native-smoke'
            smoke = base / 'build/logs' / (stem + '.json')
            screenshot = base / 'build/logs' / (stem + '.png')
            code, result, log, previous = run_native_smoke(final, smoke, screenshot, smoke_env, inspection=inspection)
            (base / 'build/logs' / (stem + '-process.log')).write_text(log + '\nPrevious evidence: ' + str(previous))
            if code or not result.get('passed') or not result.get('nativeWindowVisible') or result.get('commit') != revision:
                raise SystemExit('Native UI smoke failed: ' + json.dumps(result, ensure_ascii=False))
    report = {'commit': revision, 'mode': mode, 'features': manifest['features'], 'bundle': str(final),
              'uiSmoke': not args.skip_ui_smoke, 'logs': str(base / 'build/logs'),
              'inputsRoot': str(args.workspace), 'engineSourceRevision':engine_revision, 'engineSourceRoot':str(engine_source), 'engineStaticArchiveSHA256':hashlib.sha256(static_library.read_bytes()).hexdigest(), 'nativeEngineBinding':'static-abi13', 'pythonRuntimeInput': os.environ.get('RISING_PYTHON_RUNTIME'),
              'inspectionSmoke': not args.skip_ui_smoke,
              'builtAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'files': [{'path': str(p.relative_to(final)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                        for p in sorted(final.rglob('*')) if p.is_file()]}
    (dist / 'build-manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(str(final.resolve()), flush=True)


if __name__ == '__main__':
    main()
