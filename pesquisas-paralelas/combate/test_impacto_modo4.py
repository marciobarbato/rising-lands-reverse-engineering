"""Mode-4 cell reactions and prepared type-29 shared-world arrivals."""
import os
import struct
import unittest

from impacto_unidades import ImpactoUnidades, LimiteImpactoBatiment
from consumo_fisico import criar_consumidor_fisico
from grade_impacto import encontrar_estrutura_impacto
from alvos_impacto import encontrar_vitima_impacto
from projeteis import u16
from avanco_projeteis import avancar_linear
import test_consumo_dano as damage_tests
import test_impacto_unidades as impact_tests
import test_consumo_fisico as world_tests


class ContratosImpactoModo4(unittest.TestCase):
    def test_mode4_directions_are_explicit_before_queries(self):
        us, _ = damage_tests.fixture()
        w = ImpactoUnidades(us, None)
        for direction in (0, 28, 31, 255):
            with self.assertRaisesRegex(NotImplementedError, '29/30'):
                w.infligir(0, 4, 0, direction, 0)
        for mode in (0, 2, 3, 5, 6, 7, 8, 9, 255):
            with self.assertRaises(NotImplementedError):
                w.infligir(0, mode, 0, 29, 0)

    def test_neutral_victim_forwards_mode4_without_retaliation(self):
        us, _ = damage_tests.fixture()
        us[1][0] = 200
        calls = []
        def query(name, args):
            calls.append((name, args))
            return 1 if name == 'ChercheIndiceEnginCible' else 0
        # Type 3 has no hit child, keeping this local contract focused.
        us[1][1] = 3
        w = ImpactoUnidades(us, None, lambda *a: calls.append(('consume', a)), query,
                            lambda n, a: calls.append((n, a)))
        w.infligir(0, 4, 0, 0x11d, 1)
        self.assertEqual(calls, [('ChercheIndiceEnginCible', (0, 65535, 1)),
            ('consume', (1, 4, 0, 29)), ('PlayerEstAllie', (0, 200)), ('PlayerAAttaqueSet', (0, 200))])


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialImpactoModo4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_impacto_unidades import BancadaImpactoUnidades
        cls.b = BancadaImpactoUnidades()
        cls.dependency_stops, cls.completed_projectiles, cls.complete_impacts = {}, 0, 0

    def model(self, *args, **kwargs):
        return impact_tests.DiferencialImpactoUnidades.model(self, *args, **kwargs)

    def compare(self, us, rows, **kwargs):
        result = impact_tests.DiferencialImpactoUnidades.compare(self, us, rows,
            mode=4, mode4=bytes([127, 124]), **kwargs)
        from bancada_combate import RETORNO
        if result['EIP'] == RETORNO:
            type(self).complete_impacts += 1
        return result

    def test_original_neutral_types_flags_and_directions(self):
        for kind in range(26):
            for flag in (0, 255):
                for direction in (29, 30):
                    us, rows = damage_tests.fixture(tipo_alvo=kind, vida=1000)
                    us[1][0], us[1][0xab] = 200, int(bool(flag))
                    self.compare(us, rows, flag=flag, direction=direction)

    def test_original_zero_origin_evasion_and_refuge_stops(self):
        for state in (6, 5, 18):
            us, rows = damage_tests.fixture()
            us[1][0xab], us[1][2] = 0, state
            r = self.compare(us, rows, direction=29)
            self.assertEqual(r['EIP'], 0x4457d3 if state == 6 else 0x4539f3)
            if state == 6:
                event = next(e for e in self.b.eventos_wrapper if e[0] == 'CalculDirection')
                self.assertEqual(event[1], (0, 0x8080))

    def test_original_building_priority_and_default_death_stop(self):
        from bancada_combate import GRADE
        us, rows = damage_tests.fixture()
        us[1][0xab] = 0
        self.compare(us, rows, direction=29,
            prepare=lambda: self.b.cpu.mem_write(GRADE+0x8080*2, struct.pack('<H', 0x8000 | 7 << 5)))
        us, rows = damage_tests.fixture(vida=1)
        us[1][0], us[1][0xab] = 200, 0
        self.compare(us, rows, direction=29)


class PipelineStop(NotImplementedError):
    pass


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialPipelineModo4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_consumo_fisico import BancadaConsumoFisico
        cls.b = BancadaConsumoFisico()
        cls.complete_impacts = cls.complete_projectiles = cls.building_stops = cls.navigation_stops = 0
        cls.projectile_requests = cls.projectile_rng = 0

    def compare(self, kind=2, life=1, projectile=False, full=False, building=False, human_state=None):
        from bancada_combate import RETORNO
        from bancada_impacto_unidades import QUERIES, EFFECTS
        w, rows, pool = world_tests.fixture(kind=kind, full=full)
        w.unidades[1] = 0
        w.unidades[276] = 200 if human_state is None else 1
        w.palavra(1, 0x9a, life)
        if human_state is not None:
            w.unidades[276+2] = human_state
        if building:
            w.regioes[0x504] = 0x8000 | 7 << 5
        if projectile:
            pool.definir(37, 29, 0x505, 0x505, 4, 0, 29, 16, 16, 0)
            pool.registro(37)[0x18], pool.registro(37)[0x19] = 12, 0
        mode4 = bytes([127, 124])
        self.b.preparar(w, rows, pool, modo4=mode4)
        native = self.b.impacto_modo4(0x505, projectile=projectile)
        stop = QUERIES.get(native['EIP']) or EFFECTS.get(native['EIP'])
        consumer_events, wrapper_events = iter(self.b.eventos_consumo), iter(self.b.eventos_wrapper)
        death_events, random_events = iter(self.b.eventos_morte[1:]), iter(self.b.random_projectile)
        def next_event(events, name, args):
            event = next(events)
            self.assertEqual((name, args), tuple(event[:2]))
            return event
        def consumer_effect(name, args):
            self.assertEqual((name, args), next(death_events))
            self.assertEqual(name, 'MAJSympathie')
            self.assertEqual(args[0], 200)  # original owner>=4 early return, no generic provider
        c = criar_consumidor_fisico(w, pool, rows, efeito=consumer_effect, mortes_sem_experiencia=True)
        c.danos_modo4 = mode4
        actual = world_tests.queries(w, c.unidades)
        def consumer_query(name, args):
            event = next_event(consumer_events, name, args)
            result = actual(name, args)
            self.assertEqual(result, event[2] if name == 'Modificateur' else event[2] & 255)
            return result
        c.consulta = consumer_query
        def wrapper_event(name, args):
            event = next_event(wrapper_events, name, args)
            if name == stop:
                raise PipelineStop(name)
            return event
        def query(name, args):
            event = wrapper_event(name, args)
            if name == 'ChercheIndiceBatiment':
                result = encontrar_estrutura_impacto(struct.pack('<65536H', *w.regioes), *args)
            elif name == 'ChercheIndiceEnginCible':
                result = encontrar_vitima_impacto(c.unidades, *args)
            else:
                result = event[2]  # Declared external world query result; body not implemented here.
            self.assertEqual(result, event[2])
            return result
        def consume(*args):
            wrapper_event('EnginInfligeDegat', args)
            c.infligir(*args)
        impact = ImpactoUnidades(c.unidades, pool, consume, query, wrapper_event, celula_alerta=0x1234)
        def random(marker):
            observed_marker, result = next(random_events)
            self.assertEqual(marker, observed_marker)
            return result
        def run():
            if projectile:
                pool.efeito_externo = impact.receber
                avancar_linear(pool, 37, random)
            else:
                impact.infligir(0x505, 4, 0, 29, 0)
        if native['EIP'] == 0x4508af:
            with self.assertRaises(LimiteImpactoBatiment):
                run()
            type(self).building_stops += 1
        elif native['EIP'] != RETORNO:
            with self.assertRaises(PipelineStop):
                run()
            type(self).navigation_stops += 1
        else:
            run()
            if projectile:
                type(self).complete_projectiles += 1
            else:
                type(self).complete_impacts += 1
        for events in (consumer_events, wrapper_events, death_events, random_events):
            self.assertEqual(list(events), [])
        self.assertEqual(self.b.conferir_fisica(w), [])
        self.assertEqual(self.b.ler_pool(), pool.memoria)
        self.assertEqual(c.unidades[0][0xaf], 0xa5)
        self.assertEqual(bytes(self.b.cpu.mem_read(0x508044, 80)), bytes(80))
        if projectile:
            self.assertEqual(self.b.impactos_projetil, pool.chamadas)
            self.assertEqual(pool.registro(37)[2], int(native['EIP'] != RETORNO))
            type(self).projectile_requests += len(self.b.impactos_projetil)
            type(self).projectile_rng += len(self.b.random_projectile)
        if human_state is None:
            self.assertLess(u16(c.unidades[1], 0x9a), life)
        if building:
            self.assertEqual((u16(c.unidades[1], 0x9a), c.unidades[1][2], len(self.b.random_projectile)), (0, 4, 0))

    def test_original_complete_mode4_cell_impacts(self):
        self.compare(kind=2, life=1000)
        self.compare(kind=1)

    def test_original_prepared_type29_arrivals_and_full_pool(self):
        for kind, life, full in ((2, 1, False), (1, 1, False), (3, 1000, False), (2, 1, True)):
            self.compare(kind=kind, life=life, projectile=True, full=full)

    def test_original_later_building_and_navigation_stops_keep_prior_state(self):
        self.compare(projectile=True, building=True)
        self.compare(human_state=6)
        self.compare(human_state=5)
