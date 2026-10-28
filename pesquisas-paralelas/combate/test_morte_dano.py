"""Original lethal mutation order and explicit physical lifecycle boundary."""
import os
import unittest

from consumo_dano import ConsumidorDanoUnidade, LimiteMorte
from morte_dano import MorteDanoUnidade
from projeteis import PoolProjeteis, por16, u16
from avanco_projeteis import avancar_linear
import test_consumo_dano as damage_tests
import test_impacto_unidades as impact_tests


class LethalDependency(NotImplementedError):
    pass


class ContratosMorteDano(unittest.TestCase):
    def test_default_death_boundary_is_preserved(self):
        us, rows = damage_tests.fixture(vida=1)
        c, _ = damage_tests.local(us, rows)
        with self.assertRaises(LimiteMorte):
            c.infligir(1, 1, 0)
        self.assertEqual(u16(us[1], 0x9a), 1)

    def test_missing_level_provider_preserves_life_after_experience_clear(self):
        us, _ = damage_tests.fixture(vida=1)
        us[0][0xaf] = 255
        with self.assertRaisesRegex(NotImplementedError, 'EnginSetLevelExperience'):
            MorteDanoUnidade(us, None)(1, 0, 20, 0, 0)
        self.assertEqual((us[0][0xaf], u16(us[1], 0x9a)), (224, 1))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialMorteDano(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_morte_dano import BancadaMorteDano
        cls.b = BancadaMorteDano()
        cls.level_stops, cls.dying_stops, cls.sympathy_fragment_stops = 0, 0, 0
        cls.projectile_dying_stops = 0

    def compare_prefix(self, us, rows, pool=None, mutate_message=False):
        pool = pool or PoolProjeteis(bytearray(5600))
        self.b.preparar_consumo(us, rows)
        self.b.pool(pool.memoria)
        if mutate_message:
            def change_native():
                record = bytearray(self.b.ler_unidade(1))
                por16(record, 0x7c, 0x9090)
                self.b.escrever_unidade(record, 1)
            self.b.on_message = change_native
        native = self.b.infligir_letal()
        consumer, remaining = damage_tests.DiferencialConsumoDano.replay(
            self, us, rows, self.b.eventos_consumo)
        previous_effect = consumer.efeito
        def message(n, a):
            previous_effect(n, a)
            if mutate_message:
                por16(us[1], 0x7c, 0x9090)
        consumer.efeito = message
        def lethal_effect(n, a):
            self.assertEqual((n, a), self.b.eventos_morte[0])
            raise LethalDependency(n)
        consumer.morte = MorteDanoUnidade(us, pool, lethal_effect)
        with self.assertRaises(LethalDependency):
            consumer.infligir(1, 1, 0, 255)
        self.assertEqual(list(remaining), [])
        self.assertEqual(self.b.ler_unidades(), b''.join(us))
        self.assertEqual(self.b.ler_pool(), pool.memoria)
        if native['EIP'] == 0x44fb20:
            type(self).level_stops += 1
        else:
            self.assertEqual(native['EIP'], 0x444938)
            self.assertEqual(u16(us[1], 0x9a), 0)
            type(self).dying_stops += 1

    def test_original_source_types_and_all_experience_bytes(self):
        for kind in range(26):
            us, rows = damage_tests.fixture(tipo_fonte=kind, vida=1)
            us[0][0xaf] = 255
            self.compare_prefix(us, rows)
        for value in range(256):
            us, rows = damage_tests.fixture(vida=1)
            us[0][0xaf] = value
            self.compare_prefix(us, rows)

    def test_original_dying_boundary_child_pool_and_saved_entry_cell(self):
        for kind in (0, 1, 2, 12, 25):
            for full in (False, True):
                us, rows = damage_tests.fixture(tipo_alvo=kind, tipo_fonte=12, vida=1)
                pool = PoolProjeteis(bytearray(5600))
                if full:
                    for i in range(100):
                        pool.registro(i)[2] = 1
                self.compare_prefix(us, rows, pool, mutate_message=True)

    def test_original_post_dying_sympathy_fragment(self):
        # Separate synthetic post-provider states validate the suffix only;
        # no lifecycle implementation or whole lethal return is claimed.
        for kind in range(26):
            for owner in (0, 1, 4, 200):
                us, rows = damage_tests.fixture(tipo_alvo=kind)
                us[1][0] = owner
                self.b.mundo(us)
                self.b.simpatia_apos_dying(1, 3)
                observed = []
                h = MorteDanoUnidade(us, None, lambda n, a: observed.append((n, a)))
                h._apos_dying(1, 3)
                self.assertEqual(observed, self.b.eventos_morte)
                self.assertEqual(self.b.ler_unidades(), b''.join(us))
                type(self).sympathy_fragment_stops += 1

    def test_original_projectile_reaches_physical_dying_request(self):
        us, rows = damage_tests.fixture(tipo_fonte=12, vida=1)
        us[1][0xab] = 0
        pool = PoolProjeteis(bytearray(5600))
        pool.definir(37, 9, 0x8080, 0x8080, 1, 0, 17, 16, 16, 0)
        pool.registro(37)[0x19] = 0
        self.b.preparar_wrapper(us, rows)
        self.b.pool(pool.memoria)
        native = self.b.impacto_letal()
        self.assertEqual(native['EIP'], 0x444938)
        def lethal_effect(n, a):
            self.assertEqual((n, a), ('SetDyingEngin', (1,)))
            raise LethalDependency(n)
        handler = MorteDanoUnidade(us, pool, lethal_effect)
        w, remaining, consumer_remaining = impact_tests.DiferencialImpactoUnidades.model(
            self, us, rows, pool, native, morte=handler)
        pool.efeito_externo = w.receber
        with self.assertRaises(LethalDependency):
            avancar_linear(pool, 37)
        self.assertEqual(list(remaining), [])
        self.assertEqual(list(consumer_remaining), [])
        self.assertEqual(self.b.ler_unidades(), b''.join(us))
        self.assertEqual(self.b.ler_pool(), pool.memoria)
        self.assertEqual((u16(us[1], 0x9a), pool.registro(37)[2]), (0, 1))
        type(self).projectile_dying_stops += 1
