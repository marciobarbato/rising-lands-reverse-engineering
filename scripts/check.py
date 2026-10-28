#!/usr/bin/env python3
"""Run research suites without rewriting their versioned validation reports."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SUITES = {'core': 'testes', 'combat': 'pesquisas-paralelas/combate',
          'economy': 'pesquisas-paralelas/economia/testes',
          'graphics': 'pesquisas-paralelas/graficos-animacao',
          'missions': 'pesquisas-paralelas/missoes/testes',
          'ai-runtime': 'pesquisas-paralelas/ia-runtime/testes',
          'audio': 'pesquisas-paralelas/audio/testes'}


def documentation_links(root):
    errors = []
    paths = [root / 'README.md', root / 'AGENTS.md']
    paths += list((root / 'docs').rglob('*.md'))
    paths += list((root / 'apps/macos-preview').glob('*.md'))
    paths += list((root / 'pesquisas-paralelas').glob('*/*.md'))
    paths += list((root / 'integracao').glob('*.md'))
    for path in paths:
        if not path.exists():
            continue
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', path.read_text()):
            target = unquote(target.split('#', 1)[0])
            if not target or re.match(r'[a-z]+:', target):
                continue
            if not (path.parent / target).exists():
                errors.append(str(path.relative_to(root)) + ': ' + target)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--domain', choices=SUITES)
    args = parser.parse_args()
    errors = documentation_links(ROOT)
    if errors:
        print('Broken documentation links:\n' + '\n'.join(errors), file=sys.stderr)
        return 1
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    existing = env.get('PYTHONPATH', '')
    inputs = [str(ROOT.parent / 'source/python'), str(ROOT / '.local/python')]
    env['PYTHONPATH'] = os.pathsep.join(inputs + ([existing] if existing else []))
    failures = []
    suites = {**SUITES, 'workflow': 'scripts/tests'}
    for domain in ([args.domain] if args.domain else suites):
        if domain == 'graphics' and not (ROOT / SUITES[domain] / 'fontes/cd').is_dir():
            print('MISSING INPUT: graphics requires its hash-checked fontes/cd copies.', flush=True)
            failures.append(domain)
            continue
        print('Running', domain, flush=True)
        result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', suites[domain], '-p', 'test_*.py', '-v'], cwd=ROOT, env=env)
        if result.returncode:
            failures.append(domain)
    if failures:
        print('Failed suites: ' + ', '.join(failures), file=sys.stderr)
        return 1
    print('Documentation links and requested research suites passed.', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
