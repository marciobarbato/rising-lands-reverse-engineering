"""Mode-3 building-cell/owner requests and prepared type-1 physical arrivals."""
import os
import struct
import unittest

from impacto_unidades import ImpactoUnidades
from fonte_batiment import ConsultaFonteBatiment
import test_consumo_dano as damage_tests
import test_impacto_unidades as impact_tests
import test_impacto_modo4 as pipeline_tests


class ContratosImpactoModo3(unittest.TestCase):
    def test_missing_building_cell_is_distinct_from_unit_step(self):
        us, _ = damage_tests.fixture()
        calls = []
        def query(name, args):
            calls.append((name, args))
            if name in ('ChercheIndiceEnginCible', 'PlayerGetType'):
                return 1
            raise NotImplementedError(name)
        with self.assertRaisesRegex(NotImplementedError, 'BatimentGetCase'):
            ImpactoUnidades(us, None, consulta=query).infligir(0x8080, 3, 0, 255, 1)
        self.assertEqual(calls, [('ChercheIndiceEnginCible', (0x8080, 65535, 1)),
            ('PlayerGetType', (1,)), ('BatimentGetCase', (0,))])

    def test_building_owner_diplomacy_has_no_unit_alert(self):
        us, _ = damage_tests.fixture(tipo_alvo=3)
        calls = []
        def query(name, args):
            calls.append((name, args))
            return {'ChercheIndiceEnginCible': 1, 'PlayerGetType': 0,
                'BatimentGetCase': 0x101, 'CalculDirection': 0,
                'CalculDirCase': 65535, 'BatimentGetPlayer': 3, 'PlayerEstAllie': 0}[name]
        impact = ImpactoUnidades(us, None, lambda *args: calls.append(('consume', args)),
            query, lambda n, a: calls.append((n, a)), contador=1000, jogador_local=1)
        impact.infligir(0x8080, 3, 0, 255, 1)
        self.assertEqual(calls[-3:], [('BatimentGetPlayer', (0,)),
            ('PlayerEstAllie', (3, 1)), ('PlayerAAttaqueSet', (3, 1))])
        self.assertEqual(impact.ultimo_alerta, 0)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialImpactoModo3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_impacto_unidades import BancadaImpactoUnidades
        cls.b = BancadaImpactoUnidades()
        cls.dependency_stops, cls.completed_projectiles, cls.complete_impacts = {}, 0, 0

    def model(self, *args, **kwargs):
        w, events, consumer_events = impact_tests.DiferencialImpactoUnidades.model(self, *args, **kwargs)
        previous = w.consulta
        def query(name, args):
            if name == 'BatimentGetPlayer':
                event = next(events)
                self.assertEqual((name, args), tuple(event[:2]))
                result = self.source_provider(name, args)
                self.assertEqual(result, event[2] & 255)
                return result
            return previous(name, args)
        w.consulta = query
        return w, events, consumer_events

    def compare(self, us, rows, source_kind=10, **kwargs):
        structures = bytearray(276000)
        structures[4], structures[8] = 3, source_kind
        row10, row11 = bytes([127]*26), bytes([124]*26)
        self.source_provider = ConsultaFonteBatiment(structures, row10, row11)
        previous = kwargs.pop('prepare', None)
        def prepare():
            self.b.cpu.mem_write(0x49a0c8, bytes(structures))
            self.b.cpu.mem_write(0x4dfb80, row10)
            self.b.cpu.mem_write(0x4dfb64, row11)
            if previous:
                previous()
        result = impact_tests.DiferencialImpactoUnidades.compare(self, us, rows,
            mode=3, direction=255, prepare=prepare, **kwargs)
        from bancada_combate import RETORNO
        if result['EIP'] == RETORNO:
            type(self).complete_impacts += 1
        self.assertEqual(bytes(self.b.cpu.mem_read(0x49a0c8, 276000)), structures)
        return result

    def test_original_neutral_types_flags_and_building_sources(self):
        for kind in range(26):
            for flag in (0, 255):
                for source_kind in (10, 11):
                    us, rows = damage_tests.fixture(tipo_alvo=kind, vida=1000)
                    us[1][0], us[1][0xab] = 200, int(bool(flag))
                    struct.pack_into('<I', us[1], 0x10c, 0xffffffff)
                    self.compare(us, rows, source_kind=source_kind, flag=flag)

    def test_original_source_cell_and_refuge_stops(self):
        for state in (6, 5, 18):
            us, rows = damage_tests.fixture()
            us[1][0xab], us[1][2] = 0, state
            result = self.compare(us, rows)
            self.assertEqual(result['EIP'], 0x41aee2 if state == 6 else 0x4539f3)
            if state == 6:
                self.assertEqual(self.b.eventos_wrapper[-1][:2], ['BatimentGetCase', (0,)])

    def test_original_building_priority_and_default_death_stop(self):
        from bancada_combate import GRADE
        us, rows = damage_tests.fixture()
        us[1][0xab] = 0
        self.compare(us, rows,
            prepare=lambda: self.b.cpu.mem_write(GRADE+0x8080*2, struct.pack('<H', 0x8000 | 7 << 5)))
        us, rows = damage_tests.fixture(vida=1)
        us[1][0], us[1][0xab] = 200, 0
        struct.pack_into('<I', us[1], 0x10c, 0xffffffff)
        self.compare(us, rows)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialPipelineModo3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_consumo_fisico import BancadaConsumoFisico
        cls.b = BancadaConsumoFisico()
        cls.complete_impacts = cls.complete_projectiles = cls.building_stops = cls.navigation_stops = 0
        cls.projectile_requests = cls.projectile_rng = 0

    def compare(self, **kwargs):
        return pipeline_tests.DiferencialPipelineModo4.compare(self, mode=3, **kwargs)

    def test_original_complete_mode3_cell_impacts(self):
        self.compare(kind=2, life=1000)
        self.compare(kind=1)

    def test_original_prepared_type1_arrivals_and_full_pool(self):
        for kind, life, full, source_kind in ((2, 1, False, 10), (1, 1, False, 11),
                                            (3, 1000, False, 10), (2, 1, True, 11)):
            self.compare(kind=kind, life=life, full=full, source_kind=source_kind, projectile=True)

    def test_original_source_cell_refuge_and_synthetic_owner_reread(self):
        self.compare(human_state=6)
        self.compare(human_state=5)
        self.compare(kind=1, mutate_owner=True)
        self.assertEqual(self.b.eventos_morte[1], ('MAJSympathie', (200, 3, 0)))
        owner = next(e for e in self.b.eventos_wrapper if e[0] == 'BatimentGetPlayer')
        self.assertEqual(owner[2] & 255, 2)
        modifier = next(e for e in self.b.eventos_consumo if e[0] == 'Modificateur')
        self.assertEqual(modifier[1], (0, 6, 0))
