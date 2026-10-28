"""Original unit impact wrapper and connected nonlethal projectile completion."""
import os
import struct
import unittest

from impacto_unidades import ImpactoUnidades, LimiteImpactoBatiment
from consumo_dano import ConsumidorDanoUnidade, LimiteMorte
from projeteis import PoolProjeteis, por16, u16
from avanco_projeteis import avancar_linear
import test_consumo_dano as consumer_tests


class DependencyStop(NotImplementedError):
    pass


class ContratosImpactoUnidades(unittest.TestCase):
    def test_empty_lookup_and_flag_width(self):
        calls = []
        def query(n, a):
            calls.append((n, a))
            return 65535
        us, _ = consumer_tests.fixture()
        w = ImpactoUnidades(us, PoolProjeteis(bytearray(5600)), consulta=query)
        w.infligir(0x12348080, 0x101, 0x10000, 0, 0x100)
        self.assertEqual(calls, [('ChercheIndiceBatiment', (0x8080,)),
            ('ChercheIndiceEnginCible', (0x8080, 65535, 0))])
        calls.clear()
        w.infligir(0x8080, 1, 0, 0, 255)
        self.assertEqual(calls, [('ChercheIndiceEnginCible', (0x8080, 65535, 255))])

    def test_building_and_unsupported_mode_boundaries(self):
        us, _ = consumer_tests.fixture()
        w = ImpactoUnidades(us, None, consulta=lambda n, a: 7)
        with self.assertRaises(LimiteImpactoBatiment):
            w.infligir(0, 1, 0, 0, 0)
        with self.assertRaises(NotImplementedError):
            w.infligir(0, 2, 0, 0, 0)

    def test_missing_query_does_not_retire_parent(self):
        us, _ = consumer_tests.fixture()
        pool = PoolProjeteis(bytearray(5600))
        pool.definir(37, 9, 0, 0, 1, 0, 0, 16, 16, 0)
        pool.registro(37)[0x19] = 0
        pool.efeito_externo = ImpactoUnidades(us, pool).receber
        with self.assertRaisesRegex(NotImplementedError, 'ChercheIndiceBatiment'):
            avancar_linear(pool, 37)
        self.assertEqual((pool.registro(37)[2], pool.registro(37)[3]), (1, 1))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialImpactoUnidades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_impacto_unidades import BancadaImpactoUnidades
        cls.b = BancadaImpactoUnidades()
        cls.dependency_stops = {}
        cls.completed_projectiles = 0

    def model(self, us, rows, pool, native, counter=0, previous=0, local=0, morte=None, danos_modo4=None):
        from bancada_impacto_unidades import QUERIES, EFFECTS
        stop = QUERIES.get(native['EIP']) or EFFECTS.get(native['EIP'])
        events = iter(self.b.eventos_wrapper)
        def next_event(n, a):
            e = next(events)
            self.assertEqual((n, a), (e[0], e[1]))
            if n == stop:
                raise DependencyStop(n)
            return e
        def query(n, a):
            return next_event(n, a)[2]
        def effect(n, a):
            next_event(n, a)
        consumer, consumer_remaining = consumer_tests.DiferencialConsumoDano.replay(
            self, us, rows, self.b.eventos_consumo)
        consumer.jogador_local = local
        consumer.morte = morte
        consumer.danos_modo4 = danos_modo4
        def consume(*args):
            next_event('EnginInfligeDegat', args)
            consumer.infligir(*args)
        w = ImpactoUnidades(us, pool, consume, query, effect,
            contador=counter, jogador_local=local, ultimo_alerta=previous, celula_alerta=0x1234)
        return w, events, consumer_remaining

    def compare(self, us, rows, pool=None, counter=0, previous=0, local=0,
                flag=0, direction=0, prepare=None, consumer_stop=False, allied=False,
                player_type=1, complete_diplomacy=False, projectile=False, mode=1, mode4=None):
        from bancada_impacto_unidades import RETORNO
        pool = pool or PoolProjeteis(bytearray(5600))
        self.b.preparar_wrapper(us, rows, counter, previous, local, aliado=allied,
                               tipo_jogador=player_type, modo4=mode4)
        self.b.pool(pool.memoria)
        if prepare:
            prepare()
        cell = u16(us[1], 8)
        native = (self.b.avancar_ate_fim() if projectile else
            self.b.impacto(cell, flag, direction, consumer_stop, complete_diplomacy, mode))
        w, remaining, consumer_remaining = self.model(us, rows, pool, native, counter, previous, local,
                                                       danos_modo4=mode4)
        def run():
            if projectile:
                pool.efeito_externo = w.receber
                avancar_linear(pool, 37)
            else:
                w.infligir(cell, mode, 0, direction, flag)
        if native['EIP'] == 0x4508af:
            with self.assertRaises(LimiteImpactoBatiment):
                run()
            key = hex(native['EIP'])
            type(self).dependency_stops[key] = type(self).dependency_stops.get(key, 0) + 1
        elif native['EIP'] == 0x4506a1:
            with self.assertRaises(LimiteMorte):
                run()
            key = hex(native['EIP'])
            type(self).dependency_stops[key] = type(self).dependency_stops.get(key, 0) + 1
        elif native['EIP'] != RETORNO:
            with self.assertRaises(DependencyStop):
                run()
            key = hex(native['EIP'])
            type(self).dependency_stops[key] = type(self).dependency_stops.get(key, 0) + 1
        else:
            run()
        self.assertEqual(list(remaining), [])
        self.assertEqual(list(consumer_remaining), [])
        self.assertEqual(self.b.ler_unidades(), b''.join(us))
        self.assertEqual(self.b.ler_pool(), pool.memoria)
        self.assertEqual(self.b.ler_alerta(), (w.ultimo_alerta, w.celula_alerta))
        return native

    def test_all_unit_types_flags_hit_pool_and_rng(self):
        for kind in range(26):
            for flag in (0, 255):
                us, rows = consumer_tests.fixture(tipo_alvo=kind)
                us[1][0xab] = int(bool(flag))
                # Evasion from the corner has no neighboring cell: the native
                # CalculDirCase returns ffff, allowing the consumer to proceed.
                por16(us[0], 0x7c, 0x101)
                por16(us[1], 8, 0)
                por16(us[1], 0x7c, 0)
                with self.subTest(kind=kind, flag=flag):
                    self.compare(us, rows, flag=flag, direction=31)

    def test_retaliation_tick_boundaries_and_provider_stops(self):
        for state, now, old in ((6, 249, 0), (6, 250, 0), (6, 251, 0),
                                (7, 0, 0), (6, 0, 1), (6, 0xffffffff, 0)):
            us, rows = consumer_tests.fixture()
            us[1][0xab], us[1][2] = 0, state
            struct.pack_into('<I', us[1], 0x110, old)
            self.compare(us, rows, counter=now)

    def test_refuge_evasion_and_special_attacker_stops(self):
        for kind, source, state, bits in ((2, 0, 5, 0), (2, 0, 18, 0),
                (4, 0, 6, 0), (2, 0, 6, 2), (2, 10, 6, 0),
                (2, 17, 6, 0), (3, 16, 6, 0)):
            us, rows = consumer_tests.fixture(tipo_alvo=kind, tipo_fonte=source)
            us[1][0xab], us[1][2], us[1][0xdc] = 0, state, bits
            self.compare(us, rows)

    def test_ai_and_neutral_prefix_consumer_boundary(self):
        for player_type in (0, 2):
            for state in (6, 7):
                us, rows = consumer_tests.fixture()
                us[1][0xab], us[1][2] = 0, state
                self.compare(us, rows, player_type=player_type, consumer_stop=True)
        us, rows = consumer_tests.fixture()
        us[1][0xab], us[1][0] = 0, 200
        self.compare(us, rows, consumer_stop=True)

    def test_ally_effect_order_and_alert_counter_edges(self):
        us, rows = consumer_tests.fixture(tipo_alvo=3)
        us[1][0xab] = 0
        self.compare(us, rows, allied=True, complete_diplomacy=True, local=4)
        for now, old in ((199, 0), (200, 0), (201, 1), (0, 0xffffffff),
                          (0xffffffff, 0xfffffffe), (0xffffffff, 0)):
            us, rows = consumer_tests.fixture(tipo_alvo=3)
            us[1][0xab] = 0
            struct.pack_into('<I', us[1], 0x110, now)
            self.compare(us, rows, counter=now, previous=old, local=1)

    def test_pool_saturation_still_consumes_hit_rng(self):
        for free in (0, 1, 100):
            us, rows = consumer_tests.fixture(tipo_alvo=16)
            us[1][0xab] = 0
            pool = PoolProjeteis(bytearray(5600))
            for i in range(free, 100):
                pool.registro(i)[2] = 1
            self.compare(us, rows, pool=pool)

    def test_lookup_empty_filters_and_building_priority(self):
        for state, enabled, stratum in ((0, 1, 0), (4, 1, 0), (14, 1, 0),
                                         (6, 0, 0), (6, 1, 1)):
            us, rows = consumer_tests.fixture()
            us[1][2], us[1][0x72], us[1][0xab] = state, enabled, stratum
            self.compare(us, rows)
        us, rows = consumer_tests.fixture()
        from bancada_combate import GRADE
        def building():
            self.b.cpu.mem_write(GRADE + 0x8080 * 2, struct.pack('<H', 0x8000 | (7 << 5)))
        self.compare(us, rows, prepare=building)

    def test_projectile_finishes_occupied_impact_and_parent_retirement(self):
        for kind in (2, 3, 12, 16, 25):
            us, rows = consumer_tests.fixture(tipo_alvo=kind)
            us[1][0xab] = 0
            pool = PoolProjeteis(bytearray(5600))
            pool.definir(37, 9, 0x8080, 0x8080, 1, 0, 17, 16, 16, 0)
            pool.registro(37)[0x19] = 0
            native = self.compare(us, rows, pool=pool, projectile=True)
            self.assertEqual(pool.registro(37)[2], 0)
            self.assertEqual(u16(us[1], 0x9a), 80)
            type(self).completed_projectiles += 1
