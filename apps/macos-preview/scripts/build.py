"""Empacota um .app ARM64 sem pip, rede, Rosetta ou mudanças de segurança."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,plistlib,shutil,struct,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
RUNTIME=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/python'


def env():
    result=dict(os.environ)
    result.update({'TMPDIR':str(ROOT/'build/tmp')+'/', 'CLANG_MODULE_CACHE_PATH':str(ROOT/'build/module-cache'),'SWIFT_MODULECACHE_PATH':str(ROOT/'build/module-cache'),'PYTHONPYCACHEPREFIX':str(ROOT/'build/pycache'),'PYTHONDONTWRITEBYTECODE':'1'})
    return result

def run(args,log=None):
    print('>', ' '.join(str(a) for a in args),flush=True)
    p=subprocess.run([str(a) for a in args],cwd=ROOT,env=env(),capture_output=True,text=True)
    if log:(ROOT/'build/logs'/log).write_text(p.stdout+p.stderr)
    if p.returncode:
        print(p.stdout+p.stderr);raise SystemExit(p.returncode)
    return p.stdout

def prepare_runtime():
    target=ROOT/'dependencies/python'
    if not (target/'bin/python3').exists():
        source=Path(os.environ.get('RISING_PYTHON_RUNTIME',str(RUNTIME))).resolve()
        if not (source/'bin/python3').exists():raise SystemExit('Runtime ausente. Defina RISING_PYTHON_RUNTIME para uma distribuição relocável ARM64 do CPython 3.12.')
        stdlib=source/'lib/python3.12'
        if not stdlib.is_dir():raise SystemExit('Runtime precisa de lib/python3.12')
        (target/'bin').mkdir(parents=True,exist_ok=True);(target/'lib').mkdir(exist_ok=True)
        shutil.copy2((source/'bin/python3').resolve(),target/'bin/python3')
        shutil.copytree(stdlib,target/'lib/python3.12',ignore=shutil.ignore_patterns('site-packages','__pycache__','*.pyc','test','tests','ensurepip','idlelib','tkinter','turtledemo','config-*','_tkinter*'),dirs_exist_ok=True)
        # O executável fornecido é estático; somente extensões da stdlib são usadas.
        (target/'ORIGEM.txt').write_text('CPython 3.12 ARM64 copiado do runtime local do Codex; biblioteca padrão; sem site-packages.\nFonte: '+str(source)+'\nLicença: lib/python3.12/LICENSE.txt\n')
    for unneeded in (target/'lib/python3.12/lib-dynload').glob('_tkinter*'):unneeded.unlink()
    run([target/'bin/python3','-I','-B','-c','import sys,platform,json,struct,hashlib,math,zlib,copy; assert platform.machine()=="arm64"; print(sys.version); print(sys.prefix)'],'runtime.log')
    files=[{'path':str(p.relative_to(target)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(target.rglob('*')) if p.is_file()]
    (ROOT/'dependencies/runtime-manifest.json').write_text(json.dumps({'files':files,'python':'3.12','architecture':'arm64'},indent=2)+'\n')
    return target


def copy_preview_sources(source, destination):
    """Mirror Python modules and UI assets; native Swift is compiled separately.

    Both builders use this inventory so new consumer modules ship alongside
    engine.py and satisfy the byte-identical source verification.
    """
    for path in sorted(source.rglob('*')):
        relative = path.relative_to(source)
        if '__pycache__' in relative.parts or path.suffix == '.pyc':
            continue
        if path.is_file() and (path.suffix in ('.py', '.html', '.css', '.js')
                               or relative.parts[0] == 'ui'):
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def build():
    for p in ('build/tmp','build/logs','build/module-cache','build/pycache','dist'): (ROOT/p).mkdir(parents=True,exist_ok=True)
    runtime=prepare_runtime();manifest=json.loads((ROOT/'snapshot.json').read_text())
    app=ROOT/'build/RisingLands-Preview.app'
    if app.exists():shutil.rmtree(app)
    contents=app/'Contents';macos=contents/'MacOS';resources=contents/'Resources';preview=resources/'preview'
    macos.mkdir(parents=True);preview.mkdir(parents=True)
    shutil.copytree(runtime,resources/'Python')
    copy_preview_sources(ROOT/'src', preview)
    shutil.copytree(ROOT/'assets',preview/'assets')
    shutil.copy2(ROOT/'research.json',preview/'research.json')
    for m in json.loads((ROOT/'research.json').read_text())['research'].values():
        shutil.copytree(ROOT/m['path'],preview/m['path'])
    shutil.copy2(ROOT/'snapshot.json',preview/'snapshot.json')
    shutil.copy2(ROOT/'dependencies/runtime-manifest.json',preview/'runtime-manifest.json')
    snap=ROOT/manifest['snapshot'];shutil.copytree(snap,preview/manifest['snapshot'],ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    plist={'CFBundleExecutable':'RisingLands-Preview','CFBundleIdentifier':'local.risinglands.preview','CFBundleName':'Rising Lands Preview','CFBundleDisplayName':'Rising Lands Preview','CFBundlePackageType':'APPL','CFBundleShortVersionString':'0.1.0','CFBundleVersion':'1','RisingLandsSourceCommit':manifest['commit'],'LSMinimumSystemVersion':'13.0','LSArchitecturePriority':['arm64'],'NSHighResolutionCapable':True,'NSPrincipalClass':'NSApplication','CFBundleIconFile':'AppIcon'}
    (contents/'Info.plist').write_bytes(plistlib.dumps(plist))
    run(['xcrun','swiftc','-swift-version','5','-O','-target','arm64-apple-macosx13.0','-module-cache-path',ROOT/'build/module-cache','-framework','AppKit','-framework','WebKit',ROOT/'src/native/main.swift','-o',macos/'RisingLands-Preview'],'swift-build.log')
    icons=ROOT/'build/icons';icons.mkdir(exist_ok=True);iconset=ROOT/'build/AppIcon.iconset';iconset.mkdir(exist_ok=True)
    run(['xcrun','swiftc','-swift-version','5','-module-cache-path',ROOT/'build/module-cache',ROOT/'scripts/icon.swift','-o',ROOT/'build/icon-generator'],'icon-build.log')
    run([ROOT/'build/icon-generator',icons])
    for size in (16,32,128,256,512):
        shutil.copy2(icons/f's{size}.png',iconset/f'icon_{size}x{size}.png')
        shutil.copy2(icons/f's{size*2}.png',iconset/f'icon_{size}x{size}@2x.png')
    chunks=[]
    for kind,size in [('ic07',128),('ic08',256),('ic09',512),('ic10',1024)]:
        data=(icons/f's{size}.png').read_bytes();chunks.append(kind.encode()+struct.pack('>I',len(data)+8)+data)
    payload=b''.join(chunks);(resources/'AppIcon.icns').write_bytes(b'icns'+struct.pack('>I',len(payload)+8)+payload)
    run(['sips','-g','pixelWidth','-g','pixelHeight',resources/'AppIcon.icns'],'icon-check.log')
    for p in sorted((resources/'Python').rglob('*.so')):run(['codesign','--force','--sign','-','--timestamp=none',p])
    run(['codesign','--force','--sign','-','--timestamp=none',resources/'Python/bin/python3'],'sign-python.log')
    run(['codesign','--force','--sign','-','--options','runtime','--timestamp=none',app],'sign-app.log')
    run(['codesign','--verify','--deep','--strict','--verbose=2',app],'codesign-verify.log')
    run(['file',macos/'RisingLands-Preview',resources/'Python/bin/python3'],'architecture.log')
    # Verifica o payload empacotado, antes de publicar o diretório final.
    payload=[]
    for p in sorted(app.rglob('*')):
        if p.is_file():payload.append({'path':str(p.relative_to(app)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    final=ROOT/'dist/RisingLands-Preview.app'
    if final.exists():shutil.rmtree(final)
    shutil.move(str(app),str(final))
    report={'builtAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':manifest['commit'],'architecture':'arm64','bundle':str(final),'signing':'ad-hoc local; executable principal com hardened runtime; sem notarização','files':payload}
    (ROOT/'dist/build-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Aplicativo pronto:',final,flush=True)
if __name__=='__main__':build()
