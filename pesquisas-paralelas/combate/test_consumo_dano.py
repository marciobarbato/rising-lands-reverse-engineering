"""Whole-buffer comparisons against the original occupied-unit damage consumer."""
import os
import random
import struct
import unittest

from consumo_dano import ConsumidorDanoUnidade, LimiteMorte
from projeteis import PoolProjeteis, por16, u16
from avanco_projeteis import avancar_linear


def fixture(tipo_alvo=2, tipo_fonte=0, vida=100, matriz=20):
    us = [bytearray(276) for _ in range(800)]
    for i, tipo in ((0, tipo_fonte), (1, tipo_alvo)):
        u = us[i]
        u[0], u[1], u[2], u[0x72], u[0xab] = i, tipo, 6, 1, 1
        por16(u, 8, 0x1010 if i == 0 else 0x8080)
        por16(u, 0x7c, u16(u, 8))
        por16(u, 0x9a, vida)
        struct.pack_into('<I', u, 0x104, 0xffffffff)
    return us, [bytes([matriz] * 26) for _ in range(26)]


def local(us, rows, query=None, effect=None):
    calls = []
    def consultar(n, a):
        calls.append((n, a))
        return query(n, a) if query else 0
    def emitir(n, a):
        calls.append((n, a))
        if effect:
            effect(n, a)
    return ConsumidorDanoUnidade(us, rows, consultar, emitir), calls


class ContratosConsumoDano(unittest.TestCase):
    def test_mode_width_and_nonlethal_consumer(self):
        us, rows = fixture()
        c, calls = local(us, rows)
        c.infligir(0xabcd0001, 0x101, 0xbeef0000, 255)
        self.assertEqual(u16(us[1], 0x9a), 80)
        self.assertEqual(calls, [('Modificateur', (0, 5, 0)),
            ('ChercheTypeEnginProximite', (2, 0, 0x1010, 10)),
            ('iagUnitSendMessage', (1, 0x48, 0)), ('Modificateur', (0, 6, 0)),
            ('TerrainEstDecouvert', (0x8080, 0))])

    def test_callback_rereads_and_protected_zero_heals(self):
        us, rows = fixture(matriz=0)
        def change(n, a):
            us[0][0], us[0][1], us[1][0xdc] = 2, 25, 8
        c, calls = local(us, rows, effect=change)
        c.infligir(1, 1, 0)
        self.assertEqual(calls[3], ('Modificateur', (2, 6, 25)))
        self.assertEqual(u16(us[1], 0x9a), 101)

    def test_death_preserves_life_and_prior_effects(self):
        us, rows = fixture(vida=20)
        c, calls = local(us, rows)
        with self.assertRaises(LimiteMorte) as caught:
            c.infligir(1, 1, 0)
        self.assertEqual((caught.exception.endereco, caught.exception.dano), (0x4506a1, 20))
        self.assertEqual(u16(us[1], 0x9a), 20)
        self.assertEqual(len(calls), 5)

    def test_audio_dependency_occurs_after_f9_write_before_life(self):
        us, rows = fixture()
        us[1][0xf9] = 127
        def query(n, a):
            return 1 if n == 'TerrainEstDecouvert' else 128 if n == 'EnginGetVolume' else 0
        c, calls = local(us, rows, query)
        c.efeito = lambda n, a: (_ for _ in ()).throw(NotImplementedError(n)) if n == 'PlaySnd_PostSound' else None
        with self.assertRaisesRegex(NotImplementedError, 'PlaySnd_PostSound'):
            c.infligir(1, 1, 0)
        self.assertEqual((us[1][0xf9], u16(us[1], 0x9a)), (0, 100))

    def test_unsupported_and_missing_callbacks_fail_without_fabricated_damage(self):
        us, rows = fixture()
        c = ConsumidorDanoUnidade(us, rows)
        before = b''.join(us)
        with self.assertRaisesRegex(NotImplementedError, 'mode 1'):
            c.infligir(1, 2, 0)
        with self.assertRaisesRegex(NotImplementedError, 'Modificateur'):
            c.infligir(1, 1, 0)
        with self.assertRaises(ValueError):
            c.infligir(800, 1, 0)
        self.assertEqual(b''.join(us), before)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialConsumoDano(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_consumo_dano import BancadaConsumoDano
        cls.b = BancadaConsumoDano()
        cls.expected_death_stops = 0
        cls.expected_audio_stops = 0
        cls.pipeline_checkpoints = 0

    def replay(self, us, rows, events, bonus=0, audio_stop=False):
        events = iter(events)
        def check(n, a):
            e = next(events)
            self.assertEqual((n, a), (e[0], e[1]))
            return e
        def query(n, a):
            return check(n, a)[2]
        def effect(n, a):
            check(n, a)
            if n == 'PlaySnd_PostSound' and audio_stop:
                raise NotImplementedError('Native audio dependency stop')
        c = ConsumidorDanoUnidade(us, rows, query, effect, bonus_4965ac=bonus)
        return c, events

    def compare(self, us, rows, mod5=0, mod6=0, bonus=0, grade=None, visible=False,
                victim=1, attacker=0):
        self.b.preparar_consumo(us, rows, mod5, mod6, bonus, grade, visible)
        r = self.b.infligir_unidade(victim, attacker, direcao=255)
        c, remaining = self.replay(us, rows, self.b.eventos_consumo, bonus, r['EIP'] == 0x48aa79)
        if r['EIP'] == 0x4506a1:
            type(self).expected_death_stops += 1
            with self.assertRaises(LimiteMorte):
                c.infligir(victim, 1, attacker, 255)
        elif r['EIP'] == 0x48aa79:
            type(self).expected_audio_stops += 1
            with self.assertRaisesRegex(NotImplementedError, 'audio'):
                c.infligir(victim, 1, attacker, 255)
        else:
            c.infligir(victim, 1, attacker, 255)
        self.assertEqual(list(remaining), [])
        self.assertEqual(self.b.ler_unidades(), b''.join(us))

    def test_original_consumer_boundaries_and_all_valid_types(self):
        rng = random.Random(0x4502f0)
        for i in range(26 * 26):
            us, rows = fixture(i % 26, (i // 26) % 26)
            rows = [rng.randbytes(26) for _ in range(26)]
            us[0][0xf7], us[1][0xf6] = rng.randrange(256), rng.randrange(256)
            us[1][0xdc] = (0, 8, 255)[i % 3]
            us[1][0xf9] = rng.randrange(256)
            por16(us[1], 0x9a, (0, 1, 2, 20, 127, 128, 65535)[i % 7])
            # Same-owner occupancy toggles the actual proximity query result;
            # its misleading Type name is not treated as a type filter here.
            grade = {0x1010: 0x4000} if i % 2 else {}
            with self.subTest(case=i):
                self.compare(us, rows, rng.randrange(256), rng.randrange(256),
                             rng.randrange(256), grade)

    def test_original_zero_protection_and_life_edges(self):
        for life in (0, 1, 127, 128, 65535):
            for raw in (0, 1, 127, 128, 255):
                for protection in (0, 8):
                    us, rows = fixture(vida=life, matriz=raw)
                    us[1][0xdc] = protection
                    self.compare(us, rows)

    def test_original_visible_existing_handle_and_audio_stops(self):
        for kind in (0, 2, 12, 25):
            for handle in (0, 1, 0x80000000, 0xfffffffe, 0xffffffff):
                us, rows = fixture(tipo_alvo=kind)
                us[1][0xf9] = 223
                struct.pack_into('<I', us[1], 0x104, handle)
                self.compare(us, rows, visible=True)

    def test_original_id_edges_and_aliased_source(self):
        for victim in (0, 1, 798, 799):
            for attacker in (0, 799):
                us, rows = fixture()
                target, source = bytes(us[1]), bytes(us[0])
                us[attacker][:] = source
                us[victim][:] = target
                self.compare(us, rows, victim=victim, attacker=attacker)

    def test_original_reads_after_synthetic_message_callback_mutation(self):
        # Deliberate synthetic callback mutation at a native call boundary;
        # this does not claim the non-AI original message body makes it.
        us, rows = fixture()
        self.b.preparar_consumo(us, rows)
        def change(records):
            records[0][0], records[0][1], records[0][0xf7] = 2, 25, 200
            records[1][0xf6], records[1][0xdc] = 3, 8
            por16(records[1], 8, 0x9090)
        def native_change():
            records = [bytearray(self.b.ler_unidade(i)) for i in range(2)]
            change(records)
            for i, record in enumerate(records):
                self.b.escrever_unidade(record, i)
        self.b.on_message = native_change
        self.b.infligir_unidade(1, 0)
        events = iter(self.b.eventos_consumo)
        def query(n, a):
            event = next(events)
            self.assertEqual((n, a), (event[0], event[1]))
            return event[2]
        def effect(n, a):
            event = next(events)
            self.assertEqual((n, a), (event[0], event[1]))
            change(us)
        ConsumidorDanoUnidade(us, rows, query, effect).infligir(1, 1, 0)
        self.assertEqual(u16(us[1], 0x9a), 84)
        self.assertEqual(list(events), [])
        self.assertEqual(self.b.ler_unidades(), b''.join(us))

    def test_original_projectile_to_occupied_consumer_checkpoint(self):
        # This scenario ends at the consumer return, before the world wrapper's
        # post-damage effects and parent retirement. Its fixture resolver is the
        # observed native consumer arguments, not an invented world lookup.
        for direction in (0, 7, 17, 255):
            us, rows = fixture()
            us[1][0xab] = 0  # flag 0 requests ContientCellule filter 1
            pool = PoolProjeteis(bytearray(5600))
            pool.definir(37, 9, 0x8080, 0x8080, 1, 0, direction, 16, 16, 0)
            pool.registro(37)[0x19] = 0
            self.b.preparar_consumo(us, rows)
            self.b.pool(pool.memoria)
            self.b.capturar_impacto()
            self.assertEqual(self.b.entradas_consumo, [(1, 1, 0, direction)])
            self.assertEqual(self.b.retomar_consumidor()['EIP'], 0x450da5)
            c, remaining = self.replay(us, rows, self.b.eventos_consumo)
            class ConsumerCheckpoint(Exception):
                pass
            def world_callback(n, args):
                self.assertEqual((n, args), ('InfligeDegat', (0x8080, 1, 0, direction, 0)))
                c.infligir(1, args[1], args[2], args[3])
                raise ConsumerCheckpoint()
            pool.efeito_externo = world_callback
            with self.assertRaises(ConsumerCheckpoint):
                avancar_linear(pool, 37)
            self.assertEqual(list(remaining), [])
            self.assertEqual(u16(us[1], 0x9a), 80)
            self.assertEqual(self.b.ler_unidades(), b''.join(us))
            self.assertEqual(self.b.ler_pool(), pool.memoria)
            type(self).pipeline_checkpoints += 1
