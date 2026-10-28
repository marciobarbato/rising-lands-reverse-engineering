"""Whole-pool original capture regressions and opt-in intact-x86 comparisons."""
import hashlib
import json
import os
from pathlib import Path
import random
import struct
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
from caminhos import CD
from carregador_unidades import continuar_carga_unidades, DependenciaCargaUnidades
from entradas import bloco_unidades, tipos_originais
from formatos import Leitor, ErroFormato
from bonus_unidades import BonusUnidades


class LeitorRastreado(Leitor):
    def __init__(self, *args):
        super().__init__(*args)
        self.reads = []

    def ler(self, count):
        self.reads.append((self.posicao, count))
        return super().ler(count)


def fixture(records):
    return struct.pack('<HH', len(records), 784) + b''.join(
        struct.pack('<H', i) + bytes(data) for i, data in records)


def disk(kind=0, owner=0, state=7, pattern=0xa5):
    record = bytearray([pattern]) * 784
    record[:3] = bytes((owner, kind, state))
    return record


class CapturasCarga(unittest.TestCase):
    def test_independent_original_captures(self):
        # Regressions use the saved native pool hashes, never translated expectations.
        from capturar_original import sparse_fixture
        report = json.loads((OWNED/'evidencias/captura-original.json').read_text())
        types = tipos_originais()
        bonuses = BonusUnidades(bytes((i*19+71) & 255 for i in range(1872)))
        for case in report['cases']:
            data = (CD/'WORLD/MONDE01.ETA').read_bytes() if case['name'] == 'MONDE01' else sparse_fixture()
            self.assertEqual(hashlib.sha256(data).hexdigest(), case['input_sha256'])
            pool, flags = bytearray([0xa5])*220800, bytearray(b'\x11\x22\x33\x44')
            reader = LeitorRastreado(data, case['offset'])
            result = continuar_carga_unidades(reader, pool, flags, types,
                        modificador12=lambda owner, kind: bonuses.consultar(owner, kind, 12))
            self.assertEqual(hashlib.sha256(pool).hexdigest(), case['output_pool_sha256'])
            self.assertEqual(flags.hex(), case['flags_hex'])
            self.assertEqual(result.fim, case['cursor'])
            self.assertEqual(reader.reads, [tuple(event[1:]) for event in case['io']])
            for item in case['changed']:
                self.assertEqual(pool[item['index']*276:(item['index']+1)*276].hex(), item['output_hex'])

    def test_sparse_inactive_record_preserves_four_uncopied_bytes(self):
        pool, flags = bytearray([0x63])*220800, bytearray(4)
        data = fixture([(799, disk(state=0))])
        result = continuar_carga_unidades(Leitor(data), pool, flags, bytes(1300))
        self.assertEqual(result.indices, (799,))
        self.assertEqual(pool[799*276+272:800*276], b'cccc')
        self.assertEqual(pool[0xbd], 0)
        self.assertEqual(pool[799*276+0xbd], 0xa5)

    def test_missing_modifier_retains_prior_native_effects(self):
        pool, flags = bytearray([0x63])*220800, bytearray(4)
        reader = Leitor(fixture([(7, disk(4))]))
        with self.assertRaises(DependenciaCargaUnidades) as error:
            continuar_carga_unidades(reader, pool, flags, bytes(1300))
        self.assertEqual(error.exception.endereco, 0x428cc0)
        self.assertEqual((reader.posicao, flags), (790, b'2222'))
        self.assertEqual(pool[7*276+0x7a], 0xa5)
        self.assertEqual(pool[7*276+0xda], 1)
        self.assertEqual(pool[0xbd], 0)

    def test_strict_reader_failure_preserves_first_copy(self):
        # Protected Python failure; no native short-read equivalence is claimed.
        data = fixture([(7, disk())])[:6+140]
        pool, flags = bytearray([0x63])*220800, bytearray(4)
        with self.assertRaises(ErroFormato):
            continuar_carga_unidades(Leitor(data), pool, flags, bytes(1300))
        self.assertEqual(pool[7*276:7*276+140], data[6:146])
        self.assertEqual(pool[7*276+140:8*276], b'c'*136)
        self.assertEqual(pool[0xbd], 0x63)

    def test_invalid_buffers_fail_before_effects(self):
        pool, flags = bytearray(220799), bytearray(b'abcd')
        reader = Leitor(b'\0\0\x10\x03')
        with self.assertRaises(ValueError):
            continuar_carga_unidades(reader, pool, flags, bytes(1300))
        self.assertEqual((reader.posicao, flags), (0, b'abcd'))

    def test_unsupported_header_or_index_preserves_reached_effects(self):
        for data, cursor in ((struct.pack('<HH', 1, 783), 4),
                             (fixture([(800, disk())]), 6)):
            pool, flags = bytearray([0x63])*220800, bytearray(4)
            reader = Leitor(data)
            with self.assertRaises(ValueError):
                continuar_carga_unidades(reader, pool, flags, bytes(1300))
            self.assertEqual((reader.posicao, flags), (cursor, b'2222'))
            self.assertEqual(pool, b'c'*220800)

    def test_empty_block_and_neutral_modifier_bypass(self):
        pool, flags = bytearray([0x63])*220800, bytearray(4)
        result = continuar_carga_unidades(Leitor(fixture([])), pool, flags, bytes(1300))
        self.assertEqual(result.indices, ())
        for owner in (4, 200):
            continuar_carga_unidades(Leitor(fixture([(799, disk(4, owner))])), pool, flags, bytes(1300))
            self.assertEqual(pool[799*276+0xda], 10)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional intact-x86: RISING_EMULAR=1')
class DiferencialCarga(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_unidades import BancadaCargaUnidades
        cls.native = BancadaCargaUnidades()
        cls.types = tipos_originais()
        cls.bonuses = bytes((i*19+71) & 255 for i in range(1872))
        cls.provider = BonusUnidades(cls.bonuses)

    def compare(self, data, offset=0, *, missing=False, seed=1):
        rng = random.Random(seed)
        pool, flags = bytearray(rng.randbytes(220800)), bytearray(rng.randbytes(4))
        self.native.carregar(data, offset, pool, flags, self.types, self.bonuses, parar_bonus=missing)
        reader = LeitorRastreado(data, offset)
        if missing:
            with self.assertRaises(DependenciaCargaUnidades):
                continuar_carga_unidades(reader, pool, flags, self.types)
        else:
            continuar_carga_unidades(reader, pool, flags, self.types,
                modificador12=lambda owner, kind: self.provider.consultar(owner, kind, 12))
        self.assertEqual((bytes(pool), bytes(flags)), self.native.estado())
        self.assertEqual(reader.posicao, self.native.cursor)
        self.assertEqual(reader.reads, [(event[1], event[2]) for event in self.native.io])

    def test_all_types_states_owners_and_edge_indices(self):
        for kind in range(26):
            for state in (0, 4, 7, 14):
                for owner in (0, 3, 4, 200):
                    index = (0, 7, 799)[(kind+state+owner) % 3]
                    self.compare(fixture([(index, disk(kind, owner, state, (kind*31+state)&255))]),
                                 seed=(kind*10000+state*256+owner))

    def test_corpus_unit_blocks(self):
        for path in sorted((CD/'WORLD').glob('*.ETA')):
            data = path.read_bytes()
            with self.subTest(map=path.name):
                self.compare(data, bloco_unidades(data)['offset'])

    def test_sparse_repeated_and_empty(self):
        from capturar_original import sparse_fixture
        for data in (sparse_fixture(), fixture([]), fixture([(799,disk(0)), (0,disk(4)), (799,disk(16))])):
            self.compare(data)

    def test_modifier_checkpoint_partial_effects(self):
        for index in (0, 7, 799):
            for owner in (0, 3):
                for preceding in ([], [(799, disk(25, 200, 14))]):
                    self.compare(fixture(preceding+[(index, disk(4, owner))]), missing=True)
