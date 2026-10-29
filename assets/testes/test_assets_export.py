import importlib.util
import io
import json
from pathlib import Path
import tempfile
import subprocess
import unittest
import wave

OWNED=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('asset_bundle_export_tests',OWNED/'extract_assets.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
TEMP_ROOT=OWNED.parent/'.local/assets-tests'
TEMP_ROOT.mkdir(parents=True,exist_ok=True)


class AssetExportTests(unittest.TestCase):
    def test_canonical_json_is_order_independent_and_utf8(self):
        self.assertEqual(a.canonical({'b':2,'a':'ação'}),a.canonical({'a':'ação','b':2}))
        self.assertIn('ação',a.canonical({'a':'ação'}).decode('utf-8'))

    def test_source_identity_and_range_fail_before_decoding(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            p=Path(directory)/'x';p.write_bytes(b'abc')
            inputs=a.Inputs(directory,dict(files=[dict(path='x',bytes=3,sha256=a.sha(b'abc'))]))
            inputs.verify();self.assertEqual(inputs.read('x'),b'abc')
            self.assertEqual(inputs.source('x',1,2)['offset'],1)
            with self.assertRaisesRegex(ValueError,'SourceRangeOutsideFile'):inputs.source('x',2,2)
            p.write_bytes(b'xbc')
            with self.assertRaisesRegex(ValueError,'SourceIdentityMismatch'):inputs.read('x')

    def test_wav_preserves_written_pcm_without_fixture_tail(self):
        pcm=b'\x01\x02\xff\x7f'
        result=a.pcm_wave(pcm,1,16,22050)
        with wave.open(io.BytesIO(result),'rb') as w:
            self.assertEqual(w.getnchannels(),1);self.assertEqual(w.getframerate(),22050)
            self.assertEqual(w.readframes(w.getnframes()),pcm)
        self.assertEqual(result,a.pcm_wave(pcm,1,16,22050))
        with self.assertRaisesRegex(ValueError,'IncompletePcmFrame'):a.pcm_wave(b'x',1,16,22050)

    def test_incomplete_native_pcm_frame_is_preserved_without_padding(self):
        raw=b'\x01\x02\xff'
        encoded,tail=a.lossless_pcm_parts(raw,1,16,22050)
        with wave.open(io.BytesIO(encoded),'rb') as wav:
            self.assertEqual(wav.readframes(wav.getnframes()),b'\x01\x02')
        self.assertEqual(tail,b'\xff')
        self.assertNotIn(b'\xff\x00',encoded[-3:])

    def test_writer_refuses_existing_data_and_detects_tampering(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            output=Path(directory)/'pack'
            w=a.Writer(output,False);r=w.emit('x',b'abc',{}, {},'test',{})
            manifest=dict(outputs=[r]);w.finish(manifest)
            with self.assertRaisesRegex(ValueError,'RefusingExisting'):a.Writer(output,False)
            check=a.Writer(output,True);check.emit('x',b'abc',{}, {},'test',{});check.finish(manifest)
            (output/'x').write_bytes(b'xbc')
            with self.assertRaisesRegex(ValueError,'OutputByteMismatch'):
                a.Writer(output,True).emit('x',b'abc',{}, {},'test',{})

    def test_index_zero_opacity_is_preserved_by_reference_decoder(self):
        # One opaque literal zero, then one transparent skip.
        g=a.load_module('pesquisas-paralelas/graficos-animacao/graficos.py','assets_test_graphics_reader')
        import struct
        frame=g.ler_cmp(struct.pack('<HHHI',1,2,1,3)+bytes([255,0,1]))[0]
        self.assertEqual(frame.pixels,b'\0\0');self.assertEqual(frame.opacidade,b'\xff\0')

    def test_no_oversized_or_escaping_output(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            w=a.Writer(Path(directory)/'pack',False)
            with self.assertRaisesRegex(ValueError,'EscapingOutputPath'):w.emit('../bad',b'x',{}, {},'test',{})
            with self.assertRaisesRegex(ValueError,'OutputRequiresSplitting'):
                w.emit('large',bytes(a.MAX_PART_BYTES+1),{}, {},'test',{})

    def test_text_transport_round_trips_all_byte_values(self):
        raw=bytes(range(256));encoded=raw.decode('latin-1').encode('utf-8')
        self.assertEqual(encoded.decode('utf-8').encode('latin-1'),raw)


class PublishedDataPinTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=TEMP_ROOT)
        self.parent=Path(self.temp.name)
        self.repo=self.parent/'data-repository'
        self.repo.mkdir()
        self.git('init','--initial-branch=main')
        self.git('config','user.name','Asset pin fixture')
        self.git('config','user.email','assets-fixture@example.invalid')
        self.git('remote','add','origin',a.ASSETS_REPOSITORY)
        (self.repo/'README.md').write_text('Fixture only\n')
        self.inventory=a.canonical({'files':[]})
        (self.repo/'source-inventory.json').write_bytes(self.inventory)
        manifest={'content_root':'data','source_inventory':'source-inventory.json',
                  'source_inventory_sha256':a.sha(self.inventory)}
        (self.repo/'manifest.json').write_bytes(a.canonical(manifest))
        self.git('add','.')
        self.git('commit','-q','-m','Fixture release')
        self.git('tag','-a','v1-fixture','-m','Fixture immutable release')
        self.origin=dict(schema='rising-lands/assets-origin/1',repository=a.ASSETS_REPOSITORY,
                         release_tag='v1-fixture',release_commit=self.git('rev-parse','HEAD'),
                         tag_object=self.git('rev-parse','refs/tags/v1-fixture'),
                         manifest_sha256=a.sha((self.repo/'manifest.json').read_bytes()),
                         source_inventory_sha256=a.sha(self.inventory))
        self.origin_path=self.parent/'ORIGIN.json'
        self.origin_path.write_bytes(a.canonical(self.origin))

    def tearDown(self):self.temp.cleanup()

    def git(self,*arguments):
        return subprocess.check_output(['git','-c','commit.gpgsign=false','-c','core.hooksPath=/dev/null',
                                       '-C',str(self.repo),*arguments],stderr=subprocess.STDOUT,text=True).strip()

    def test_exact_repository_commit_annotated_tag_and_manifest_pass(self):
        self.assertEqual(a.load_origin(self.origin_path),self.origin)
        self.assertEqual(a.verify_data_checkout(self.repo,self.origin),self.origin)

    def test_missing_or_malformed_origin_never_falls_back(self):
        with self.assertRaisesRegex(ValueError,'AssetsOriginMissing'):a.load_origin(self.parent/'absent.json')
        self.origin_path.write_text('{}')
        with self.assertRaisesRegex(ValueError,'InvalidAssetsOriginPin'):a.load_origin(self.origin_path)

    def test_wrong_commit_and_tag_pins_are_refused(self):
        with self.assertRaisesRegex(ValueError,'AssetsCommitMismatch'):
            a.verify_data_checkout(self.repo,dict(self.origin,release_commit='0'*40))
        with self.assertRaisesRegex(ValueError,'AssetsReleaseTagMismatch'):
            a.verify_data_checkout(self.repo,dict(self.origin,tag_object='0'*40))
        with self.assertRaisesRegex(ValueError,'AssetsReleaseTagMissing'):
            a.verify_data_checkout(self.repo,dict(self.origin,release_tag='v1-absent'))

    def test_different_checkout_commit_is_refused(self):
        (self.repo/'README.md').write_text('Changed release\n')
        self.git('add','README.md');self.git('commit','-q','-m','Different checkout')
        with self.assertRaisesRegex(ValueError,'AssetsCommitMismatch'):a.verify_data_checkout(self.repo,self.origin)

    def test_modified_manifest_is_refused_before_regeneration(self):
        (self.repo/'manifest.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'AssetsManifestPinMismatch'):a.verify_data_checkout(self.repo,self.origin)

    def test_modified_inventory_and_dirty_checkout_are_refused(self):
        (self.repo/'source-inventory.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'AssetsSourceInventoryPinMismatch'):a.verify_data_checkout(self.repo,self.origin)
        (self.repo/'source-inventory.json').write_bytes(self.inventory)
        (self.repo/'README.md').write_text('Dirty checkout\n')
        with self.assertRaisesRegex(ValueError,'AssetsCheckoutModified'):a.verify_data_checkout(self.repo,self.origin)

    def test_wrong_repository_and_missing_checkout_are_refused(self):
        self.git('remote','set-url','origin','https://github.com/example/wrong.git')
        with self.assertRaisesRegex(ValueError,'AssetsRepositoryMismatch'):a.verify_data_checkout(self.repo,self.origin)
        with self.assertRaisesRegex(ValueError,'AssetsCheckoutMissing'):a.verify_data_checkout(self.parent/'absent',self.origin)

    def test_missing_or_unpinned_source_inventory_is_refused(self):
        with self.assertRaisesRegex(ValueError,'SourceInventoryMissing'):
            a.Inputs(self.repo,inventory_path=self.parent/'absent.json')
        with self.assertRaisesRegex(ValueError,'SourceInventoryIdentityMismatch'):
            a.Inputs(self.repo,inventory_path=self.repo/'source-inventory.json')


if __name__=='__main__':unittest.main()

