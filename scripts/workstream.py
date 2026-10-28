#!/usr/bin/env python3
"""Prepare isolated research worktrees and serialize verified merges to origin/main."""
import argparse
import fcntl
import os
from pathlib import Path
import subprocess
import sys
import uuid

DOMAINS = ('core', 'combat', 'economy', 'graphics')
DOMAIN_PATH = {'combat': 'combate', 'economy': 'economia', 'graphics': 'graficos-animacao'}


def git(repo, *args, capture=True):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip() if capture else subprocess.check_call(['git', '-C', str(repo), *args])


def canonical(repo):
    common = Path(git(repo, 'rev-parse', '--git-common-dir'))
    if not common.is_absolute():
        common = repo / common
    return common.resolve().parent


def link_missing(link, target):
    if target.exists() and not link.exists() and not link.is_symlink():
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(target.resolve(), target_is_directory=target.is_dir())


def prepare(repo, checkout):
    """Link only ignored inputs; never replace a tracked file or mutate a source input."""
    repo, checkout = canonical(repo), checkout.resolve()
    link_missing(checkout.parent / 'source', repo.parent / 'source')
    link_missing(checkout / '.local/python', repo / '.local/python')
    graphics = Path('pesquisas-paralelas/graficos-animacao')
    for name in ('fontes', 'snapshot', 'dependencias'):
        source = repo / graphics / name
        if source.is_dir():
            for item in source.iterdir():
                if item.name != 'manifesto.json' and item.name != '__pycache__':
                    link_missing(checkout / graphics / name / item.name, item)
    link_missing(checkout / graphics / 'entregas', repo / graphics / 'entregas')


def start(repo, domain):
    repo = canonical(repo)
    git(repo, 'fetch', 'origin', capture=False)
    branch = 'feat/re-' + domain
    target = repo.parent / 'worktrees' / ('re-' + domain)
    if target.exists():
        if git(target, 'branch', '--show-current') != branch:
            raise RuntimeError('Existing directory belongs to a different branch: ' + str(target))
        prepare(repo, target)
        print('Resuming existing worktree:', target)
        return target
    if subprocess.run(['git', '-C', str(repo), 'show-ref', '--verify', '--quiet', 'refs/heads/' + branch]).returncode == 0:
        git(repo, 'worktree', 'add', str(target), branch, capture=False)
    else:
        git(repo, 'worktree', 'add', '-b', branch, str(target), 'origin/main', capture=False)
    prepare(repo, target)
    print('Worktree:', target, '\nBranch:', branch)
    return target


def changed_paths(repo, base, head):
    # Include both names of renames: deleting a foreign path violates ownership too.
    return git(repo, 'diff', '--name-only', '--no-renames', base + '...' + head).splitlines()


def owned(domain, path):
    if domain == 'core':
        return path.startswith(('ferramentas/', 'testes/', 'evidencias/', 'relatorios/', 'docs/core/')) or path == 'docs/CORE.md'
    return path.startswith('pesquisas-paralelas/' + DOMAIN_PATH[domain] + '/') or path == 'docs/' + domain.upper() + '.md'


def check_ownership(repo, domain, branch):
    foreign = [p for p in changed_paths(repo, 'origin/main', branch) if not owned(domain, p)]
    if foreign:
        raise RuntimeError('Changes outside ' + domain + ' ownership:\n' + '\n'.join(foreign))


def integrate(repo, domain):
    """Hold the common lock through fetch, candidate tests, and non-force push."""
    checkout = repo.resolve()
    repo = canonical(checkout)
    branch = 'feat/re-' + domain
    if git(checkout, 'branch', '--show-current') != branch:
        raise RuntimeError('Run integrate from the completed ' + branch + ' worktree.')
    if git(checkout, 'status', '--porcelain'):
        raise RuntimeError('Commit or preserve local changes before integration.')
    common = repo / '.git'
    with (common / 'rising-integration.lock').open('a') as lock:
        print('Waiting for the repository integration lock...', flush=True)
        fcntl.flock(lock, fcntl.LOCK_EX)
        git(repo, 'fetch', 'origin', capture=False)
        check_ownership(repo, domain, branch)
        git(checkout, 'merge', '--no-edit', 'origin/main', capture=False)
        git(checkout, 'push', '-u', 'origin', branch, capture=False)
        target = repo.parent / 'worktrees' / ('integration-' + domain + '-' + uuid.uuid4().hex[:8])
        git(repo, 'worktree', 'add', '--detach', str(target), 'origin/main', capture=False)
        prepare(repo, target)
        successful = False
        try:
            git(target, 'merge', '--no-ff', '--no-edit', branch, capture=False)
            for attempt in range(3):
                subprocess.check_call([sys.executable, '-B', str(target / 'scripts/check.py')], cwd=target)
                # A remote writer outside this machine may race our local lock.
                # A normal non-force push rejects that race; merge and retest before retrying.
                result = subprocess.run(['git', '-C', str(target), 'push', 'origin', 'HEAD:main'])
                if result.returncode == 0:
                    successful = True
                    print('Merged and pushed origin/main:', git(target, 'rev-parse', 'HEAD'))
                    return
                previous = git(target, 'rev-parse', 'origin/main')
                git(target, 'fetch', 'origin', capture=False)
                if git(target, 'rev-parse', 'origin/main') == previous:
                    raise RuntimeError('Push failed without a remote-main advance; inspect authentication or branch policy.')
                git(target, 'merge', '--no-edit', 'origin/main', capture=False)
            raise RuntimeError('Remote main kept advancing; candidate preserved for inspection.')
        finally:
            if successful:
                git(repo, 'worktree', 'remove', str(target), capture=False)
            else:
                print('Integration candidate preserved:', target, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('start', 'prepare', 'integrate'))
    parser.add_argument('domain', nargs='?', choices=DOMAINS)
    args = parser.parse_args()
    repo = Path(git(Path.cwd(), 'rev-parse', '--show-toplevel'))
    if args.action == 'prepare':
        prepare(repo, repo)
    elif args.domain is None:
        parser.error('start and integrate require a domain')
    elif args.action == 'start':
        start(repo, args.domain)
    else:
        integrate(repo, args.domain)


if __name__ == '__main__':
    main()
