"""Exercise isolated local Git remotes, ownership, and serialized integration."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'workstream.py'
spec = importlib.util.spec_from_file_location('workstream', MODULE)
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


class WorkflowTests(unittest.TestCase):
    def test_ownership_excludes_foreign_and_shared_paths(self):
        self.assertTrue(workflow.owned('core', 'ferramentas/portoes.py'))
        self.assertFalse(workflow.owned('core', 'pesquisas-paralelas/economia/economia.py'))
        self.assertTrue(workflow.owned('graphics', 'docs/GRAPHICS.md'))
        for domain in workflow.DOMAINS:
            self.assertFalse(workflow.owned(domain, 'scripts/check.py'))
            self.assertFalse(workflow.owned(domain, 'docs/STATUS.md'))

    def test_two_stale_workers_merge_without_modifying_canonical_checkout(self):
        with tempfile.TemporaryDirectory(prefix='rising-workflow-') as directory:
            base = Path(directory)
            remote, repo = base / 'remote.git', base / 'repository'
            environment = dict(os.environ, GIT_AUTHOR_NAME='Workflow Test', GIT_AUTHOR_EMAIL='workflow@example.invalid',
                               GIT_COMMITTER_NAME='Workflow Test', GIT_COMMITTER_EMAIL='workflow@example.invalid')
            def run(*args, cwd=None):
                return subprocess.check_output(['git', *map(str, args)], cwd=cwd, env=environment, stderr=subprocess.STDOUT, text=True).strip()
            run('init', '--bare', remote)
            run('init', '-b', 'main', repo)
            (repo / 'scripts').mkdir()
            (repo / 'scripts/check.py').write_text('raise SystemExit(0)\n')
            (repo / '.gitignore').write_text('.local/\npesquisas-paralelas/graficos-animacao/fontes/cd\n')
            run('add', '.', cwd=repo);run('commit', '-m', 'Initial fixture', cwd=repo)
            run('remote', 'add', 'origin', remote, cwd=repo);run('push', '-u', 'origin', 'main', cwd=repo)
            initial = run('rev-parse', 'HEAD', cwd=repo)
            core = workflow.start(repo, 'core')
            economy = workflow.start(repo, 'economy')
            for target, path, text in [(core, 'ferramentas/new.py', 'core'), (economy, 'pesquisas-paralelas/economia/new.py', 'economy')]:
                p = target / path;p.parent.mkdir(parents=True);p.write_text(text)
                run('add', path, cwd=target);run('commit', '-m', 'Add independent feature', cwd=target)
            # Start both stale workers at once. The shared lock must protect fetch,
            # merge, candidate checks, and push across separate processes.
            workers = [subprocess.Popen([sys.executable, str(MODULE), 'integrate', domain],
                       cwd=target, env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                       for domain, target in [('core', core), ('economy', economy)]]
            for worker in workers:
                output, _ = worker.communicate(timeout=30)
                self.assertEqual(worker.returncode, 0, output)
            run('fetch', 'origin', cwd=repo)
            self.assertEqual(run('show', 'origin/main:ferramentas/new.py', cwd=repo), 'core')
            self.assertEqual(run('show', 'origin/main:pesquisas-paralelas/economia/new.py', cwd=repo), 'economy')
            self.assertEqual(run('rev-parse', 'HEAD', cwd=repo), initial)
            self.assertEqual(run('status', '--porcelain', cwd=repo), '')
            self.assertFalse(any((base/'worktrees').glob('integration-*')))
            # Preparation must never replace a caller-owned existing input.
            (repo / '.local/python').mkdir(parents=True)
            (core / '.local/python').mkdir(parents=True)
            (core / '.local/python/sentinel').write_text('preserve')
            workflow.prepare(repo, core)
            self.assertEqual((core / '.local/python/sentinel').read_text(), 'preserve')
            self.assertFalse((core / '.local/python').is_symlink())
            remote_before = run('rev-parse', 'origin/main', cwd=repo)
            (core / 'README.md').write_text('Outside core ownership')
            run('add', 'README.md', cwd=core);run('commit', '-m', 'Invalid foreign change', cwd=core)
            with self.assertRaisesRegex(RuntimeError, 'outside core ownership'):
                workflow.integrate(core, 'core')
            self.assertEqual(run('rev-parse', 'origin/main', cwd=repo), remote_before)


if __name__ == '__main__':
    unittest.main()
