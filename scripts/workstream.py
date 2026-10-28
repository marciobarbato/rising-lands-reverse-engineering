#!/usr/bin/env python3
"""Prepare isolated research worktrees and serialize verified merges to origin/main.

Seven research fronts plus a coordinator maintenance front share one canonical
repository. Every front has its own branch, worktree, write ownership and
integration validation. The integration helper holds one advisory lock in the
common Git directory across fetch, ownership review, feature merge/push, the
detached merge candidate, common and domain checks and the non-force main push.
"""
import argparse
from dataclasses import dataclass
import fcntl
import os
from pathlib import Path
import subprocess
import sys
import uuid


@dataclass(frozen=True)
class Front:
    branch: str
    worktree: str
    prefixes: tuple
    exact: tuple = ()
    # Extra validation commands run inside the merge candidate after the
    # common checks. Each entry is an argv list; '{python}' is replaced.
    validation: tuple = ()


MISSION_NATIVE = ('env', 'RISING_EMULAR=1', '{python}', '-B', '-m', 'unittest', 'discover',
                  '-s', 'pesquisas-paralelas/missoes/testes', '-p', 'test_*.py', '-v')
AI_RUNTIME_NATIVE = ('env', 'RISING_EMULAR=1', '{python}', '-B', '-m', 'unittest', 'discover',
                     '-s', 'pesquisas-paralelas/ia-runtime/testes', '-p', 'test_*.py', '-v')
APP_BUILD = ('{python}', '-B', 'compilar-jogável', '--development-ref', 'HEAD')

FRONTS = {
    'core': Front('feat/re-core', 're-core',
                  ('ferramentas/', 'testes/', 'evidencias/', 'relatorios/', 'docs/core/'),
                  ('docs/CORE.md',)),
    'combat': Front('feat/re-combat', 're-combat', ('pesquisas-paralelas/combate/',), ('docs/COMBAT.md',)),
    'economy': Front('feat/re-economy', 're-economy', ('pesquisas-paralelas/economia/',), ('docs/ECONOMY.md',)),
    'graphics': Front('feat/re-graphics', 're-graphics', ('pesquisas-paralelas/graficos-animacao/',),
                      ('docs/GRAPHICS.md',)),
    'missions': Front('feat/re-missions', 're-missions', ('pesquisas-paralelas/missoes/',), ('docs/MISSIONS.md',),
                      (MISSION_NATIVE,)),
    'ai-runtime': Front('feat/re-ai-runtime', 're-ai-runtime', ('pesquisas-paralelas/ia-runtime/',),
                        ('docs/AI_RUNTIME.md',), (AI_RUNTIME_NATIVE,)),
    'macos': Front('feat/macos-playable', 'macos-playable', ('apps/macos-preview/',),
                   ('compilar-jogável', 'docs/MACOS_PLAYABLE.md'), (APP_BUILD,)),
    # The coordinator front owns every shared path that no research front owns.
    'maintenance': Front('coordinator/maintenance', 'maintenance', (), ()),
}
RESEARCH = tuple(name for name in FRONTS if name != 'maintenance')
DOMAINS = tuple(FRONTS)


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
    front = FRONTS[domain]
    git(repo, 'fetch', 'origin', capture=False)
    target = repo.parent / 'worktrees' / front.worktree
    if target.exists():
        if git(target, 'branch', '--show-current') != front.branch:
            raise RuntimeError('Existing directory belongs to a different branch: ' + str(target))
        prepare(repo, target)
        print('Resuming existing worktree:', target)
        return target
    if subprocess.run(['git', '-C', str(repo), 'show-ref', '--verify', '--quiet', 'refs/heads/' + front.branch]).returncode == 0:
        git(repo, 'worktree', 'add', str(target), front.branch, capture=False)
    elif subprocess.run(['git', '-C', str(repo), 'show-ref', '--verify', '--quiet', 'refs/remotes/origin/' + front.branch]).returncode == 0:
        git(repo, 'worktree', 'add', '--track', '-b', front.branch, str(target), 'origin/' + front.branch, capture=False)
    else:
        git(repo, 'worktree', 'add', '-b', front.branch, str(target), 'origin/main', capture=False)
    prepare(repo, target)
    print('Worktree:', target, '\nBranch:', front.branch)
    return target


def changed_paths(repo, base, head):
    # Include both names of renames: deleting a foreign path violates ownership too.
    return git(repo, 'diff', '--name-only', '--no-renames', base + '...' + head).splitlines()


def changed_statuses(repo, base, head):
    lines = git(repo, 'diff', '--name-status', '--no-renames', base + '...' + head).splitlines()
    return [(line.split('\t')[0][:1], line.split('\t', 1)[1]) for line in lines if line]


def research_owned(path):
    return any(path.startswith(FRONTS[name].prefixes) or path in FRONTS[name].exact for name in RESEARCH)


def owned(domain, path, status='M'):
    """Ownership of one changed path. The coordinator may seed a new front by
    adding files under its paths, but never modifies or deletes research files."""
    front = FRONTS[domain]
    if domain == 'maintenance':
        return not research_owned(path) or status == 'A'
    return path.startswith(front.prefixes) or path in front.exact


def check_ownership(repo, domain, branch):
    foreign = [p for s, p in changed_statuses(repo, 'origin/main', branch) if not owned(domain, p, s)]
    if foreign:
        raise RuntimeError('Changes outside ' + domain + ' ownership:\n' + '\n'.join(foreign))


def run_validation(domain, target):
    subprocess.check_call([sys.executable, '-B', str(target / 'scripts/check.py')], cwd=target)
    for command in FRONTS[domain].validation:
        argv = [sys.executable if part == '{python}' else part for part in command]
        print('Front validation:', ' '.join(argv), flush=True)
        subprocess.check_call(argv, cwd=target)
    if git(target, 'status', '--porcelain'):
        raise RuntimeError('Validation modified tracked candidate state; inspect the candidate.')


def integrate(repo, domain):
    """Hold the common lock through fetch, candidate tests, and non-force push."""
    checkout = repo.resolve()
    repo = canonical(checkout)
    front = FRONTS[domain]
    if git(checkout, 'branch', '--show-current') != front.branch:
        raise RuntimeError('Run integrate from the completed ' + front.branch + ' worktree.')
    if git(checkout, 'status', '--porcelain'):
        raise RuntimeError('Commit or preserve local changes before integration.')
    common = repo / '.git'
    with (common / 'rising-integration.lock').open('a') as lock:
        print('Waiting for the repository integration lock...', flush=True)
        fcntl.flock(lock, fcntl.LOCK_EX)
        git(repo, 'fetch', 'origin', capture=False)
        check_ownership(repo, domain, front.branch)
        git(checkout, 'merge', '--no-edit', 'origin/main', capture=False)
        check_ownership(repo, domain, front.branch)
        git(checkout, 'push', '-u', 'origin', front.branch, capture=False)
        target = repo.parent / 'worktrees' / ('integration-' + domain + '-' + uuid.uuid4().hex[:8])
        git(repo, 'worktree', 'add', '--detach', str(target), 'origin/main', capture=False)
        prepare(repo, target)
        successful = False
        try:
            git(target, 'merge', '--no-ff', '--no-edit', front.branch, capture=False)
            for attempt in range(3):
                run_validation(domain, target)
                # A remote writer outside this machine may race our local lock.
                # A normal non-force push rejects that race; merge and retest before retrying.
                result = subprocess.run(['git', '-C', str(target), 'push', 'origin', 'HEAD:main'])
                if result.returncode == 0:
                    successful = True
                    merged = git(target, 'rev-parse', 'HEAD')
                    git(repo, 'fetch', 'origin', 'main', capture=False)
                    for sha in (git(checkout, 'rev-parse', 'HEAD'), merged):
                        git(repo, 'merge-base', '--is-ancestor', sha, 'origin/main', capture=False)
                    print('Merged and pushed origin/main:', merged)
                    print('Feature and merge commits verified reachable from fetched origin/main.')
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
    parser.add_argument('action', choices=('start', 'prepare', 'integrate', 'fronts'))
    parser.add_argument('domain', nargs='?', choices=DOMAINS)
    args = parser.parse_args()
    if args.action == 'fronts':
        for name, front in FRONTS.items():
            owned_paths = ', '.join(front.prefixes + front.exact) or 'every path not owned by a research front'
            print(f'{name}: {front.branch} worktrees/{front.worktree} -> {owned_paths}')
        return
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
