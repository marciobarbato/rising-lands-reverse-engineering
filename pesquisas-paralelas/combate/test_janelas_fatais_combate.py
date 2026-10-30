"""Snapshot identity rejection and bounded leased fatal-window orchestration."""
import hashlib
import json
import lzma
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import executar_janelas_fatais_combate as runner
import capturar_janela_fatal_combate as capture


class FatalWindowRunner(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        printing = patch('builtins.print')
        printing.start()
        self.addCleanup(printing.stop)
        self.records = self.root/'quadros.jsonl.xz'
        self.identity = dict(dgroup_sha256='d'*64, state_sha256='a'*64)
        self.write_records([dict(frame=11000, **self.identity)])

    def write_records(self, rows):
        self.records.write_bytes(lzma.compress(''.join(json.dumps(r)+'\n' for r in rows).encode()))

    def test_alternate_serialization_is_accepted_by_both_published_hashes(self):
        first = self.root/'snapshot-a.pickle'
        second = self.root/'snapshot-b.pickle'
        first.write_bytes(b'first serialization')
        second.write_bytes(b'different serialization of equal game memory')
        self.assertNotEqual(hashlib.sha256(first.read_bytes()).hexdigest(),
                            hashlib.sha256(second.read_bytes()).hexdigest())
        identity = capture.identidade_registrada(self.records, 11000)
        for path in (first, second):
            with patch.object(capture.er, 'abrir', return_value=('bench', None, 11000)), \
                 patch.object(capture.er, 'amostra', return_value=self.identity):
                b, actual_path, digest = capture.abrir_snapshot(self.root, [path], 11000, identity=identity)
            self.assertEqual((b, actual_path), ('bench', path))
            self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertEqual(identity['sha256'], hashlib.sha256(self.records.read_bytes()).hexdigest())

    def test_committed_s1_frame11000_identity(self):
        path = runner.ROOT/'pesquisas-paralelas/missoes/m3/sondas/S1/quadros.jsonl.xz'
        identity = capture.identidade_registrada(path, 11000)
        self.assertEqual(identity['dgroup_sha256'],
                         'd6bcbd2e5e75d24677926e8adf8ce0ff1d0c180f627bb721342e5d1cebb16761')
        self.assertEqual(identity['state_sha256'],
                         '3e1c2b531052721d622880f14306759fc3b670dfe1500409d1385e7782fa85ea')

    def test_frame_and_either_state_hash_mismatch_are_rejected(self):
        snapshot = self.root/'snapshot.pickle'
        snapshot.write_bytes(b'trusted project fixture')
        identity = capture.identidade_registrada(self.records, 11000)
        for frame, observed in ((10999, self.identity),
                                (11000, dict(self.identity, dgroup_sha256='b'*64)),
                                (11000, dict(self.identity, state_sha256='b'*64))):
            with self.subTest(frame=frame, observed=observed), \
                 patch.object(capture.er, 'abrir', return_value=('bench', None, frame)), \
                 patch.object(capture.er, 'amostra', return_value=observed):
                with self.assertRaisesRegex(RuntimeError, 'No verified snapshot'):
                    capture.abrir_snapshot(self.root, [snapshot], 11000, identity=identity)

    def test_exact_continuation_digest_rejects_changed_file_before_restore(self):
        snapshot = self.root/'snapshot.pickle'
        snapshot.write_bytes(b'changed')
        with patch.object(capture.er, 'abrir') as restore:
            with self.assertRaisesRegex(RuntimeError, 'No verified snapshot'):
                capture.abrir_snapshot(self.root, [snapshot], 11000, digest='a'*64)
            restore.assert_not_called()

    def test_restore_errors_propagate(self):
        snapshot = self.root/'snapshot.pickle'
        snapshot.write_bytes(b'bad snapshot')
        with patch.object(capture.er, 'abrir', side_effect=RuntimeError('binding layout differs')):
            with self.assertRaisesRegex(RuntimeError, 'binding layout differs'):
                capture.abrir_snapshot(self.root, [snapshot], 11000, identity=self.identity)

    def test_missing_duplicate_and_malformed_record_are_rejected(self):
        for rows in ([], [dict(frame=11000, **self.identity)]*2,
                     [dict(frame=11000, dgroup_sha256='invalid', state_sha256='a'*64)]):
            with self.subTest(rows=rows):
                self.write_records(rows)
                with self.assertRaises(RuntimeError):
                    capture.identidade_registrada(self.records, 11000)

    def prepare_runner(self, scenario):
        folder = self.root/f'pesquisas-paralelas/missoes/m3/sondas/{scenario}'
        folder.mkdir(parents=True)
        self.records = folder/'quadros.jsonl.xz'
        self.write_records([dict(frame=f, **self.identity) for f in (11000, 11250, 12250, 15250)])
        source = self.root/'input.json'
        source.write_text('{}')
        # Deliberately different from the published pickle serializations.
        manifest = self.root/'pass2-resumo.json'
        manifest.write_text(json.dumps(dict(input_file='input.json', input_sha256=hashlib.sha256(b'{}').hexdigest(),
            last_frame=17050 if scenario=='S1' else 15700,
            snapshots={str(f): dict(sha256='f'*64) for f in (11000, 11250, 12250, 15250)})))
        lease = self.root/'heavy_lease.py'
        lease.touch()
        args = [scenario, '--manifest', str(manifest), '--lease', str(lease), '--saida-root', str(self.root/'out')]
        return args

    def execute_fake(self, command, **kwargs):
        stop = int(command[command.index('--ate')+1])
        out = Path(command[command.index('--saida')+1])
        out.mkdir(parents=True)
        (out/'manifest.json').write_text(json.dumps(dict(failures=[], completed_frame=stop, incomplete_leaves=0,
            end_snapshot=dict(path=str(out/'next.pickle'), sha256='c'*64))))

    def test_default_d1_windows_are_split_and_chain_exact_end_snapshots(self):
        args = self.prepare_runner('D1')
        with patch.object(runner, 'ROOT', self.root), patch.object(runner.subprocess, 'run', side_effect=self.execute_fake) as run:
            runner.main(args)
        commands = [c.args[0] for c in run.call_args_list]
        windows = [(int(c[c.index('--snapshot-frame')+1]), int(c[c.index('--ate')+1])) for c in commands]
        self.assertEqual(windows, [(11250,11500), (11500,11750), (15250,15500), (15500,15700)])
        for i,c in enumerate(commands):
            self.assertIn('heavy_lease.py', c[1])
            self.assertLessEqual(windows[i][1]-windows[i][0], 250)
            if i in (0,2):
                self.assertIn('--snapshot-records', c)
                self.assertNotIn('--snapshot-sha256', c)
            else:
                self.assertEqual(c[c.index('--snapshot-sha256')+1], 'c'*64)
                self.assertIn('--snapshot', c)

    def test_s1_and_optional_override(self):
        args = self.prepare_runner('S1')
        with patch.object(runner, 'ROOT', self.root), patch.object(runner.subprocess, 'run', side_effect=self.execute_fake) as run:
            runner.main(args)
        self.assertEqual(run.call_count, 5)
        args = self.prepare_runner('D1') + ['--intervals','12250-13750']
        with patch.object(runner, 'ROOT', self.root), patch.object(runner.subprocess, 'run', side_effect=self.execute_fake) as run:
            runner.main(args)
        self.assertEqual(run.call_count, 6)

    def test_entire_plan_is_checked_before_any_job(self):
        args = self.prepare_runner('D1')
        for extra in (['--intervals','11250-11750','17000-17500'],
                      ['--intervals','11251-11750']):
            with self.subTest(extra=extra), patch.object(runner, 'ROOT', self.root), patch.object(runner.subprocess, 'run') as run:
                with self.assertRaises(RuntimeError):runner.main(args+extra)
                run.assert_not_called()

    def test_incomplete_segment_stops_chain(self):
        args = self.prepare_runner('D1')
        def incomplete(command, **kwargs):
            self.execute_fake(command, **kwargs)
            out = Path(command[command.index('--saida')+1])/'manifest.json'
            report = json.loads(out.read_text())
            report['incomplete_leaves'] = 1
            out.write_text(json.dumps(report))
        with patch.object(runner, 'ROOT', self.root), patch.object(runner.subprocess, 'run', side_effect=incomplete) as run:
            with self.assertRaisesRegex(RuntimeError, 'Native segment did not complete'):
                runner.main(args)
        self.assertEqual(run.call_count, 1)

    def test_invalid_intervals(self):
        for value in ('11750-11250', '-1-250', '1-1', 'bad'):
            with self.subTest(value=value), self.assertRaises(runner.argparse.ArgumentTypeError):
                runner.parse_interval(value)


if __name__ == '__main__':
    unittest.main()
