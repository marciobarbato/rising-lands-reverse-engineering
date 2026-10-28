"""Native lookup results, immutable unit buffers and callback-connected impacts."""
import os
import random
import unittest

from alvos_impacto import encontrar_vitima_impacto, ConsultaAlvosImpacto
from projeteis import PoolProjeteis, por16, u16
from avanco_projeteis import avancar_linear
import test_alvos_alcance as target_tests
import test_consumo_dano as damage_tests
import test_impacto_unidades as impact_tests


def blank():
    return [bytearray(276) for _ in range(800)]


class ContratosAlvosImpacto(unittest.TestCase):
    def test_last_ground_first_elevated_and_exclusion(self):
        us = blank()
        for index in (7, 15, 799):
            us[index][:] = target_tests.unidade(atual=0x8080)
        before = b''.join(us)
        self.assertEqual(encontrar_vitima_impacto(us, 0x8080), 799)
        self.assertEqual(encontrar_vitima_impacto(us, 0x8080, 799), 15)
        self.assertEqual(encontrar_vitima_impacto(us, 0x8080, flag=1), 65535)
        self.assertEqual(b''.join(us), before)
        us[15][0xab], us[799][0xab] = 50, 255
        self.assertEqual(encontrar_vitima_impacto(us, 0x8080, flag=255), 15)
        self.assertEqual(encontrar_vitima_impacto(us, 0x8080, 15, flag=1), 799)
        self.assertEqual(encontrar_vitima_impacto(us, 0x8080, flag=0), 7)

    def test_widths_missing_provider_and_inactive_unknown_types(self):
        us = blank()
        us[7][:] = target_tests.unidade(atual=0xffff)
        us[799][1] = 255  # inactive bytes are never interpreted as a live type
        q = ConsultaAlvosImpacto(us)
        self.assertEqual(q('ChercheIndiceEnginCible', (0x1234ffff, 0x10007, 0x100)), 65535)
        self.assertEqual(q('ChercheIndiceEnginCible', (0x1234ffff, 0xffff, 0x100)), 7)
        with self.assertRaisesRegex(NotImplementedError, 'ChercheIndiceBatiment'):
            q('ChercheIndiceBatiment', (0,))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialAlvosImpacto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_impacto_unidades import BancadaImpactoUnidades
        cls.b = BancadaImpactoUnidades()
        cls.lookup_returns = 0
        cls.completed_impacts = 0

    def compare_lookup(self, us, cell, excluded=65535, flag=0):
        from bancada_impacto_unidades import WRAPPER
        before = b''.join(us)
        self.b.mundo(us)
        result = self.b.executar(0x4465df, WRAPPER,
            dict(EAX=cell | 0xabcd0000, EDX=excluded | 0xface0000, EBX=flag | 0xbeef0000),
            limite_instrucoes=1000000)
        self.assertEqual(result['EAX'], encontrar_vitima_impacto(us, cell, excluded, flag))
        self.assertEqual(self.b.ler_unidades(), before)
        self.assertEqual(b''.join(us), before)
        type(self).lookup_returns += 1

    def test_original_types_cells_strata_and_exclusion(self):
        for kind in range(26):
            for cell in (0, 0x101, 0xffff):
                for flag in (0, 255):
                    for excluded in (65535, 799):
                        us = blank()
                        for index in (7, 799):
                            us[index][:] = target_tests.unidade(tipo=kind, atual=cell,
                                                               passo=(cell + 257) & 65535)
                            us[index][0xab] = 50 if flag else 0
                        self.compare_lookup(us, cell, excluded, flag)

    def test_original_state_enable_and_random_mixed_tables(self):
        rng = random.Random(0x4465df)
        for case in range(64):
            us = blank()
            for index in (0, 7, 15, 63, 799):
                us[index][:] = target_tests.unidade(tipo=rng.randrange(26), dono=rng.randrange(256),
                    estado=rng.choice((0, 1, 4, 7, 14, 255)), atual=rng.randrange(65536),
                    passo=rng.randrange(65536))
                us[index][0x72], us[index][0xab] = rng.choice((0, 1, 255)), rng.choice((0, 1, 50, 255))
            cell = u16(us[rng.choice((0, 7, 15, 63, 799))], rng.choice((8, 0x7c)))
            self.compare_lookup(us, cell, rng.choice((0, 7, 799, 65535)), rng.choice((0, 1, 2, 255)))

    def test_real_lookup_in_connected_projectile_damage(self):
        for kind in (2, 3, 12, 16, 25):
            us, rows = damage_tests.fixture(tipo_alvo=kind)
            us[1][0xab] = 0
            us[799][:] = us[1]  # last ground match must receive the impact
            pool = PoolProjeteis(bytearray(5600))
            pool.definir(37, 9, 0x8080, 0x8080, 1, 0, 17, 16, 16, 0)
            pool.registro(37)[0x19] = 0
            self.b.preparar_wrapper(us, rows)
            self.b.pool(pool.memoria)
            native = self.b.avancar_ate_fim()
            w, remaining, consumer_remaining = impact_tests.DiferencialImpactoUnidades.model(
                self, us, rows, pool, native)
            delegate = w.consulta
            actual = ConsultaAlvosImpacto(us, delegate)
            def query(n, a):
                if n == 'ChercheIndiceEnginCible':
                    event = next(remaining)
                    self.assertEqual((n, a), (event[0], event[1]))
                    result = actual(n, a)
                    self.assertEqual(result, event[2] & 65535)
                    return result  # computed selection, never replayed native ID
                return actual(n, a)
            w.consulta = query
            pool.efeito_externo = w.receber
            avancar_linear(pool, 37)
            self.assertEqual(list(remaining), [])
            self.assertEqual(list(consumer_remaining), [])
            self.assertEqual(self.b.ler_unidades(), b''.join(us))
            self.assertEqual(self.b.ler_pool(), pool.memoria)
            self.assertEqual((u16(us[1], 0x9a), u16(us[799], 0x9a), pool.registro(37)[2]), (100, 80, 0))
            type(self).completed_impacts += 1
