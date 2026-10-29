"""Waiting-slot provider checked against original-only captures and live buffers."""
import base64
import hashlib
import json
from pathlib import Path
import struct
import sys
import unittest
import zlib

OWNED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNED))
from indices_fila_audio import WaitingSlotIndex
from bancos_som import DependenciaSom


def decode(value):return zlib.decompress(base64.b64decode(value))


def compare_cases(capture):
    for case in capture['cases']:
        counter=bytearray(struct.pack('<I',case['input_maximum']))
        table=bytearray(decode(case['input_table_zlib_base64']))
        index=WaitingSlotIndex(counter,table)
        result=getattr(index,case['operation'])()
        if case['operation']!='give_back':
            assert result==int(case['eax'],16),case
        assert index.maximum()==case['output_maximum'],case
        assert bytes(table)==decode(case['output_table_zlib_base64']),case
        assert hashlib.sha256(table).hexdigest()==case['output_table_sha256'],case


class WaitingSlotIndexTests(unittest.TestCase):
    def test_all_133_original_capture_cases(self):
        capture=json.loads((OWNED/'evidencias/captura-indices-fila-audio-original.json').read_text())
        self.assertFalse(capture['translation_executed'])
        self.assertEqual(capture['native_calls'],133)
        compare_cases(capture)

    def test_live_identity_and_external_status_changes(self):
        word=bytearray(struct.pack('<I',19));table=bytearray([255]*880)
        index=WaitingSlotIndex(word,table)
        self.assertIs(index.index_word,word);self.assertIs(index.playing_table,table)
        table[7*44+8]=0;self.assertEqual(index.find_place(),7)
        self.assertEqual(index.reserve(),20);self.assertEqual(struct.unpack('<I',word)[0],20)
        index.give_back();self.assertEqual(index.maximum(),19)

    def test_full_and_lower_bound_keep_inherited_bytes(self):
        word=bytearray(struct.pack('<I',70));table=bytearray([17]*880)
        before=bytes(table);index=WaitingSlotIndex(word,table)
        self.assertEqual(index.reserve(),0xffffffff)
        self.assertEqual(index.maximum(),70);self.assertEqual(bytes(table),before)
        word[:]=struct.pack('<I',19);index.give_back();self.assertEqual(index.maximum(),19)
        self.assertEqual(bytes(table),before)

    def test_unknown_counter_is_a_named_stop_before_any_write(self):
        for maximum in (0,18,71,0xffffffff):
            for operation in ('reserve','give_back'):
                word=bytearray(struct.pack('<I',maximum));table=bytearray(880)
                index=WaitingSlotIndex(word,table)
                with self.assertRaises(DependenciaSom):getattr(index,operation)()
                self.assertEqual(index.maximum(),maximum);self.assertEqual(table,bytearray(880))

    def test_malformed_buffers_rejected_without_initializing_state(self):
        table=bytearray(880)
        for word in (b'\0'*4,bytearray(3),memoryview(bytearray(8))[::2]):
            with self.assertRaises(ValueError):WaitingSlotIndex(word,table)
        for wrong in (bytes(880),bytearray(879),memoryview(bytearray(1760))[::2]):
            with self.assertRaises(ValueError):WaitingSlotIndex(bytearray(4),wrong)
