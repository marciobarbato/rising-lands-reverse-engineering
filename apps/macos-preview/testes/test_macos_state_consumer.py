"""CPU-only consumer tests against committed M1 evidence; no local app assets."""
import base64
from dataclasses import FrozenInstanceError
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'apps/macos-preview/src'))
import macos_state_consumer as consumer

spec = importlib.util.spec_from_file_location('_test_macos_missions_decoder', ROOT / 'pesquisas-paralelas/missoes/mapa_memoria_m1.py')
provider = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provider)


def record(base=16, data=b'abc'):
    return dict(base=hex(base), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                zlib_base64=base64.b64encode(zlib.compress(data)).decode())


class MacOSStateConsumerTests(unittest.TestCase):
    def test_accepted_evidence_matches_existing_python_decoder(self):
        image = consumer.load_accepted_m1(ROOT)
        capture = json.loads((ROOT / consumer.CAPTURE).read_bytes())
        expected = provider.carregar_blocos(capture['oracle']['final_state']['blocks'])
        self.assertEqual(len(image.blocks), 881)
        self.assertEqual(image.inspect()['bytes'], 2659375)
        for block in image.blocks:
            self.assertEqual((block.base, block.data), expected[block.name])
            self.assertEqual(image.read(block.base, len(block.data)), block.data)
        self.assertEqual(image.identity, (consumer.CONTRACT, consumer.CAPTURE_SHA256))

    def test_canonical_order_independent_of_json_order(self):
        a, b = record(32), record(16)
        decode = lambda x: consumer._decode_blocks(x, provider.carregar_blocos)
        self.assertEqual(decode(dict(a=a, b=b)), decode(dict(b=b, a=a)))
        self.assertEqual([x.name for x in decode(dict(a=a, b=b))], ['b', 'a'])

    def test_malformed_block_metadata(self):
        for key, value in [('base', '-1'), ('base', '0x100000000'), ('bytes', True),
                           ('bytes', 0), ('bytes', -1), ('sha256', 'bad'),
                           ('zlib_base64', None)]:
            with self.subTest(key=key, value=value):
                bad = record(); bad[key] = value
                with self.assertRaises(consumer.StateValidationError):
                    consumer._decode_blocks({'a': bad}, provider.carregar_blocos)

    def test_bad_payload_size_hash_and_compression(self):
        for key, value in [('bytes', 4), ('sha256', '0' * 64), ('zlib_base64', 'garbage')]:
            with self.subTest(key=key):
                bad = record(); bad[key] = value
                with self.assertRaises(consumer.StateValidationError):
                    consumer._decode_blocks({'a': bad}, provider.carregar_blocos)

    def test_overlap_and_address_overflow(self):
        for records in [dict(a=record(16), b=record(17)), dict(a=record(2**32-1))]:
            with self.assertRaises(consumer.StateValidationError):
                consumer._decode_blocks(records, provider.carregar_blocos)

    def test_empty_and_wrong_shape(self):
        for records in [{}, [], {'a': None}]:
            with self.assertRaises(consumer.StateValidationError):
                consumer._decode_blocks(records, provider.carregar_blocos)

    def test_read_bounds_and_immutable_image(self):
        image = consumer.load_accepted_m1(ROOT)
        for address, size in [(-1, 1), (0, 1), (16, 0), (True, 1), (2**32, 1)]:
            with self.assertRaises(consumer.StateValidationError):
                image.read(address, size)
        block = image.blocks[0]
        with self.assertRaises(consumer.StateValidationError):
            image.read(block.base + len(block.data) - 1, 2)
        with self.assertRaises(FrozenInstanceError):
            image.contract = 'other'
        with self.assertRaises(TypeError):
            image.blocks[0].data[0] = 1

    def test_load_idempotent_reset_reload(self):
        slot = consumer.MacOSStateConsumer()
        self.assertIsNone(slot.current)
        first = slot.load_m1(ROOT)
        self.assertIs(first, slot.load_m1(ROOT))
        slot.reset(); self.assertIsNone(slot.current)
        self.assertEqual(first, slot.load_m1(ROOT))
        self.assertIsNot(first, slot.current)

    def test_failed_load_preserves_previous_image(self):
        slot = consumer.MacOSStateConsumer(); first = slot.load_m1(ROOT)
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(consumer.StateValidationError):
                slot.load_m1(directory)
        self.assertIs(slot.current, first)

    def test_missing_malformed_unaccepted_and_tampered_capture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            acceptance = root / consumer.ACCEPTANCE
            acceptance.parent.mkdir(parents=True)
            acceptance.write_text('{')
            with self.assertRaises(consumer.StateValidationError):
                consumer.load_accepted_m1(root)
            acceptance.write_text(json.dumps(dict(decision='PENDING', original_reference={})))
            with self.assertRaises(consumer.StateValidationError):
                consumer.load_accepted_m1(root)
            acceptance.write_bytes((ROOT / consumer.ACCEPTANCE).read_bytes())
            capture = root / consumer.CAPTURE; capture.parent.mkdir(parents=True)
            capture.write_bytes((ROOT / consumer.CAPTURE).read_bytes() + b' ')
            with self.assertRaisesRegex(consumer.StateValidationError, 'SHA-256'):
                consumer.load_accepted_m1(root)

    def test_frames_stop_before_mutation_both_empty_and_loaded(self):
        slot = consumer.MacOSStateConsumer()
        for loaded in (False, True):
            if loaded: slot.load_m1(ROOT)
            previous = slot.current
            with self.assertRaises(consumer.RuntimeContractPending):
                slot.apply_frame({'unknown': 'not interpreted'})
            self.assertIs(slot.current, previous)
