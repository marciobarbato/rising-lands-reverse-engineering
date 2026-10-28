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
        self.assertTrue(workflow.owned('missions', 'pesquisas-paralelas/missoes/validar.py'))
        self.assertTrue(workflow.owned('missions', 'docs/MISSIONS.md'))
        self.assertTrue(workflow.owned('ai-runtime', 'pesquisas-paralelas/ia-runtime/testes/test_namespace.py'))
        self.assertTrue(workflow.owned('ai-runtime', 'docs/AI_RUNTIME.md'))
        self.assertFalse(workflow.owned('ai-runtime', 'ferramentas/ia.py'))
        self.assertTrue(workflow.owned('audio', 'pesquisas-paralelas/audio/testes/test_namespace_audio.py'))
        self.assertTrue(workflow.owned('audio', 'docs/AUDIO.md'))
        self.assertFalse(workflow.owned('audio', 'apps/macos-preview/src/engine.py'))
        self.assertFalse(workflow.owned('macos', 'pesquisas-paralelas/audio/README.md'))
        self.assertTrue(workflow.owned('macos', 'compilar-jogável'))
        self.assertTrue(workflow.owned('macos', 'apps/macos-preview/src/engine.py'))
        self.assertFalse(workflow.owned('macos', 'ferramentas/unidades.py'))
        for domain in workflow.RESEARCH:
            self.assertFalse(workflow.owned(domain, 'scripts/check.py'))
            self.assertFalse(workflow.owned(domain, 'docs/STATUS.md'))
            self.assertFalse(workflow.owned(domain, 'integracao/providers.py'))
        self.assertTrue(workflow.owned('maintenance', 'scripts/check.py'))
        self.assertTrue(workflow.owned('maintenance', 'docs/STATUS.md'))
        self.assertTrue(workflow.owned('maintenance', 'AGENTS.md'))
        self.assertFalse(workflow.owned('maintenance', 'docs/MISSIONS.md'))
        self.assertFalse(workflow.owned('maintenance', 'pesquisas-paralelas/ia-runtime/README.md'))
        self.assertFalse(workflow.owned('maintenance', 'pesquisas-paralelas/ia-runtime/README.md', 'D'))
        # Seeding a new front adds files under its paths without touching existing research files.
        self.assertTrue(workflow.owned('maintenance', 'pesquisas-paralelas/ia-runtime/README.md', 'A'))
        self.assertFalse(workflow.owned('core', 'pesquisas-paralelas/ia-runtime/README.md', 'A'))

    def test_every_front_has_distinct_branch_and_worktree(self):
        branches = [front.branch for front in workflow.FRONTS.values()]
        worktrees = [front.worktree for front in workflow.FRONTS.values()]
        self.assertEqual(len(branches), len(set(branches)))
        self.assertEqual(len(worktrees), len(set(worktrees)))
        self.assertEqual(workflow.FRONTS['missions'].branch, 'feat/re-missions')
        self.assertEqual(workflow.FRONTS['macos'].worktree, 'macos-playable')
        self.assertEqual(workflow.FRONTS['ai-runtime'].branch, 'feat/re-ai-runtime')
        self.assertEqual(workflow.FRONTS['audio'].worktree, 're-audio')

    def test_start_tracks_existing_remote_branch(self):
        with tempfile.TemporaryDirectory(prefix='rising-workflow-') as directory:
            base = Path(directory)
            remote, repo = base / 'remote.git', base / 'repository'
            environment = dict(os.environ, GIT_AUTHOR_NAME='Workflow Test', GIT_AUTHOR_EMAIL='workflow@example.invalid',
                               GIT_COMMITTER_NAME='Workflow Test', GIT_COMMITTER_EMAIL='workflow@example.invalid')
            def run(*args, cwd=None):
                return subprocess.check_output(['git', *map(str, args)], cwd=cwd, env=environment, stderr=subprocess.STDOUT, text=True).strip()
            run('init', '--bare', remote)
            run('init', '-b', 'main', repo)
            (repo / 'README.md').write_text('fixture\n')
            run('add', '.', cwd=repo);run('commit', '-m', 'Initial fixture', cwd=repo)
            run('remote', 'add', 'origin', remote, cwd=repo);run('push', '-u', 'origin', 'main', cwd=repo)
            # A branch that exists only on the remote must be resumed, not recreated from main.
            run('branch', 'feat/re-missions', cwd=repo)
            (repo / 'note.txt').write_text('remote feature\n')
            run('checkout', '-q', 'feat/re-missions', cwd=repo);run('add', 'note.txt', cwd=repo)
            run('commit', '-m', 'Remote feature', cwd=repo);run('push', 'origin', 'feat/re-missions', cwd=repo)
            run('checkout', '-q', 'main', cwd=repo);run('branch', '-D', 'feat/re-missions', cwd=repo)
            missions = workflow.start(repo, 'missions')
            self.assertEqual(run('branch', '--show-current', cwd=missions), 'feat/re-missions')
            self.assertEqual((missions / 'note.txt').read_text(), 'remote feature\n')
            self.assertEqual(run('rev-parse', '--abbrev-ref', '@{upstream}', cwd=missions), 'origin/feat/re-missions')

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
