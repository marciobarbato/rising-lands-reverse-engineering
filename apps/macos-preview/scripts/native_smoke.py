"""Bounded native launch; preserve retries and outer-guard failure evidence."""
import datetime
import json
from pathlib import Path
import shutil
import subprocess

# App budgets: window45 (inside init90), checks45, final capture10.
# LaunchServices gets20 additional seconds; this is an outer process guard.
OUTER_TIMEOUT_SECONDS = 165


def preserve_evidence(report, screenshot):
    report, screenshot = Path(report), Path(screenshot)
    files = [report, screenshot, screenshot.with_suffix('.before.png'), screenshot.with_suffix('.after.png'), report.with_name(report.stem+'-process.log')]
    existing = [p for p in files if p.exists()]
    if not existing: return None
    archive = report.parent / 'previous-smoke' / (report.stem + '-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    archive.mkdir(parents=True)
    for path in existing: shutil.move(str(path), str(archive / path.name))
    return archive


def run_native_smoke(app, report, screenshot, environment, inspection=False, ready_delay_ms=0):
    report, screenshot = Path(report), Path(screenshot)
    archive = preserve_evidence(report, screenshot)
    command = ['open', '-W', '-n', str(app), '--args']
    if inspection: command.append('--inspection')
    command += ['--smoke-test', str(report), '--screenshot', str(screenshot)]
    if ready_delay_ms: command += ['--smoke-ready-delay-ms', str(ready_delay_ms)]
    try:
        process = subprocess.run(command, capture_output=True, text=True,
                                 timeout=OUTER_TIMEOUT_SECONDS, env=environment)
        log = 'LaunchServices exit: ' + str(process.returncode) + '\n' + process.stdout + process.stderr
        exit_code = process.returncode
    except subprocess.TimeoutExpired as exc:
        exit_code = -1
        log = 'LaunchServices outer guard expired after ' + str(OUTER_TIMEOUT_SECONDS) + ' seconds\n' + str(exc)
        # Never replace a more specific app-written failure with an outer error.
        if not report.exists():
            report.write_text(json.dumps(dict(passed=False, error='launch_services_outer_timeout',
                                              readiness=dict(phase='outer_guard'),
                                              outerTimeoutSeconds=OUTER_TIMEOUT_SECONDS), indent=2)+'\n')
    if not report.exists():
        report.write_text(json.dumps(dict(passed=False, error='Smoke output missing',
                                          readiness=dict(phase='launch')), indent=2)+'\n')
    result = json.loads(report.read_text())
    if result.get('passed'):
        missing = [str(p) for p in (screenshot, screenshot.with_suffix('.before.png'), screenshot.with_suffix('.after.png')) if not p.is_file()]
        if missing:
            result.update(passed=False, appResultPassed=True, error='native_smoke_capture_missing', missingCaptures=missing)
            report.write_text(json.dumps(result, indent=2)+'\n')
    return exit_code, result, log, str(archive) if archive else None
