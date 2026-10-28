"""Mode-3 building-source AL getters and distinct common unit-source fields."""
import os
import random
import struct
import unittest

from fonte_batiment import ConsultaFonteBatiment
from consumo_dano import ConsumidorDanoUnidade, LimiteMorte
from bonus_combate import ConsultaBonusCombate
from projeteis import u16
import test_consumo_dano as damage_tests
import test_dano_modo8 as special_tests


class ContratosDanoModo3(unittest.TestCase):
    def test_live_source_pool_rows_and_explicit_other_queries(self):
        structures = bytearray(276000)
        structures[4], structures[8] = 3, 10
        q = ConsultaFonteBatiment(memoryview(structures).toreadonly(), bytes([20]*26), bytes([30]*26))
        self.assertEqual(q('BatimentGetType', (0x10000,)), 10)
        self.assertEqual(q('BatimentGetPlayer', (0,)), 3)
        self.assertEqual(q('TypeBatimentGetDegat', (10, 1, 2)), 20)
        structures[8] = 11
        self.assertEqual(q('BatimentGetType', (0,)), 11)
        self.assertEqual(q('TypeBatimentGetDegat', (11, 1, 2)), 30)
        self.assertEqual(q('TypeBatimentGetDegat', (255, 1, 2)), 0)
        with self.assertRaises(NotImplementedError):
            q('TypeBatimentGetDegat', (10, 3, 2))
        with self.assertRaises(ValueError):
            q('BatimentGetType', (1000,))
        with self.assertRaisesRegex(NotImplementedError, 'Modificateur'):
            q('Modificateur', (0, 6, 0))

    def test_prefix_owner_and_unit_source_modifier_remain_distinct(self):
        us, rows = damage_tests.fixture()
        structures = bytearray(276000)
        structures[4], structures[8] = 3, 10
        calls = []
        source = ConsultaFonteBatiment(structures, bytes([20]*26), bytes([30]*26), lambda n, a: 0)
        def query(n, a):
            calls.append((n, a))
            return source(n, a)
        c = ConsumidorDanoUnidade(us, rows, query, lambda n, a: calls.append((n, a)))
        c.infligir(1, 3, 0)
        self.assertEqual(u16(us[1], 0x9a), 80)
        self.assertEqual(calls, [('BatimentGetType', (0,)), ('TypeBatimentGetDegat', (10, 1, 2)),
            ('BatimentGetPlayer', (0,)), ('iagUnitSendMessage', (1, 0x4c, 0)),
            ('Modificateur', (0, 6, 0)), ('TerrainEstDecouvert', (0x8080, 0))])

    def test_mode3_death_does_not_use_mode1_award_handler(self):
        us, rows = damage_tests.fixture(vida=1)
        structures = bytearray(276000)
        structures[8] = 10
        query = ConsultaFonteBatiment(structures, bytes([20]*26), bytes(26), lambda n, a: 0)
        c = ConsumidorDanoUnidade(us, rows, query, lambda n, a: None,
            morte=lambda *args: self.fail('Mode-1 award handler must not run'))
        with self.assertRaises(LimiteMorte) as caught:
            c.infligir(1, 3, 0)
        self.assertEqual((caught.exception.modo, u16(us[1], 0x9a)), (3, 1))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialDanoModo3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_dano_modo3 import BancadaDanoModo3
        cls.b = BancadaDanoModo3()
        cls.complete_returns = cls.death_stops = cls.audio_stops = cls.getter_returns = 0

    def compare(self, us, rows, kind=10, raw=20, mod6=0, visible=False, victim=1, source=0):
        structures = bytearray(276000)
        structures[source*276+4], structures[source*276+8] = 3, kind
        row10, row11 = bytes([raw]*26), bytes([(raw+17) & 255]*26)
        self.b.preparar_consumo(us, rows, mod5=255, mod6=mod6, bonus=255, visivel=visible)
        self.b.carregar_fonte(structures, row10, row11)
        native = self.b.consumir(victim, source)
        events = iter(self.b.eventos_consumo)
        bonus_bytes = bytes(self.b.cpu.mem_read(0x4dfba0, 1872))
        bonus = ConsultaBonusCombate(special_tests.BonusUnidades(bonus_bytes))
        def remaining(name, args):
            if name == 'Modificateur':
                return bonus(name, args)
            if name == 'TerrainEstDecouvert':
                return int(visible)
            raise NotImplementedError(name)
        provider = ConsultaFonteBatiment(structures, row10, row11, remaining)
        def check(name, args):
            event = next(events)
            self.assertEqual((name, args), tuple(event[:2]))
            return event
        def query(name, args):
            event = check(name, args)
            result = event[2] if name == 'EnginGetVolume' else provider(name, args)
            self.assertEqual(result, event[2] & 255 if name in
                ('BatimentGetType', 'BatimentGetPlayer', 'TypeBatimentGetDegat', 'TerrainEstDecouvert') else event[2])
            return result
        def effect(name, args):
            check(name, args)
            if name == 'iagUnitSendMessage':
                self.assertEqual(args, (victim, 0x4c, source))
                self.assertLess(us[victim][0], 4)  # declared original human no-effect guard
                return
            self.assertEqual(name, 'PlaySnd_PostSound')
            raise NotImplementedError('Expected audio stop')
        c = ConsumidorDanoUnidade(us, rows, query, effect,
            morte=lambda *args: self.fail('Mode-3 death must not use mode-1 handler'))
        if native['EIP'] == 0x4506a1:
            with self.assertRaises(LimiteMorte) as caught:
                c.infligir(victim, 3, source, 255)
            self.assertEqual(caught.exception.modo, 3)
            type(self).death_stops += 1
        elif native['EIP'] == 0x48aa79:
            with self.assertRaisesRegex(NotImplementedError, 'audio'):
                c.infligir(victim, 3, source, 255)
            type(self).audio_stops += 1
        else:
            from bancada_combate import RETORNO
            self.assertEqual(native['EIP'], RETORNO)
            c.infligir(victim, 3, source, 255)
            type(self).complete_returns += 1
        self.assertEqual(list(events), [])
        self.assertEqual(self.b.ler_unidades(), b''.join(us))
        self.assertEqual(bytes(self.b.cpu.mem_read(0x49a0c8, 276000)), structures)
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4dfba0, 1872)), bonus_bytes)
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4dfb80, 26)), row10)
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4dfb64, 26)), row11)

    def test_original_getter_calls_and_selector1_rows(self):
        from bancada_dano_modo3 import INTERVALOS
        structures = bytearray(276000)
        row10, row11 = bytes(range(26)), bytes(range(101, 127))
        for index in (0, 7, 799, 999):
            structures[index*276+4], structures[index*276+8] = index & 255, (index+3) & 255
        self.b.carregar_fonte(structures, row10, row11)
        q = ConsultaFonteBatiment(structures, row10, row11)
        for index in (0, 7, 799, 999):
            for name, at in (('BatimentGetType', 0x41a4f4), ('BatimentGetPlayer', 0x41a08c)):
                r = self.b.executar(at, INTERVALOS, dict(EAX=index | 0xabcd0000, EDX=0xface1234))
                self.assertEqual((r['EAX'] & 255, r['EDX']), (q(name, (index,)), 0xface1234))
                type(self).getter_returns += 1
        for kind in (*range(22), 255):
            for victim_type in range(26):
                r = self.b.executar(0x418b8a, INTERVALOS,
                    dict(EAX=kind | 0xabcd0000, EDX=0xface0001, EBX=victim_type | 0xbeef0000))
                self.assertEqual(r['EAX'] & 255, q('TypeBatimentGetDegat', (kind, 1, victim_type)))
                type(self).getter_returns += 1
        self.assertEqual(bytes(self.b.cpu.mem_read(0x49a0c8, 276000)), structures)

    def test_original_all_building_and_victim_types(self):
        rng = random.Random(0x450377)
        for kind in range(22):
            for victim_type in range(26):
                us, rows = damage_tests.fixture(tipo_alvo=victim_type, tipo_fonte=12, vida=1000)
                us[0][0xf7], us[1][0xf6] = rng.randrange(256), rng.randrange(256)
                self.compare(us, rows, kind, rng.randrange(256), rng.randrange(256))

    def test_original_reduction_life_and_protection_edges(self):
        for life in (0, 1, 20, 127, 65535):
            for raw in (0, 1, 127, 128, 255):
                for reduction in (0, 1, 255):
                    for modifier in (0, 1, 255):
                        for protection in (0, 8):
                            us, rows = damage_tests.fixture(vida=life)
                            us[1][0xf6], us[1][0xdc] = reduction, protection
                            self.compare(us, rows, raw=raw, mod6=modifier)

    def test_original_id_overlap_and_audio_handles(self):
        for victim in (0, 1, 798, 799):
            for source in (0, 799):
                us, rows = damage_tests.fixture(vida=1000)
                source_record, target = bytes(us[0]), bytes(us[1])
                us[source][:], us[victim][:] = source_record, target
                self.compare(us, rows, kind=11, victim=victim, source=source)
        for kind in (0, 2, 12, 25):
            for handle in (0, 1, 0x80000000, 0xfffffffe, 0xffffffff):
                us, rows = damage_tests.fixture(tipo_alvo=kind)
                us[1][0xf9] = 223
                struct.pack_into('<I', us[1], 0x104, handle)
                self.compare(us, rows, visible=True)
