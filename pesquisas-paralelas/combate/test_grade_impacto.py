"""Original tagged-grid lookup and computed building-before-unit selection."""
import os
import struct
import unittest

from grade_impacto import encontrar_estrutura_impacto, ConsultaGradeImpacto
from alvos_impacto import ConsultaAlvosImpacto
from impacto_unidades import ImpactoUnidades, LimiteImpactoBatiment
from avanco_projeteis import avancar_linear
from projeteis import PoolProjeteis, u16
import test_consumo_dano as damage_tests
import test_impacto_unidades as impact_tests


class ContratosGradeImpacto(unittest.TestCase):
    def test_tag_widths_no_allocation_clamp_and_live_readonly_view(self):
        grid = bytearray(131072)
        view = memoryview(grid).toreadonly()
        struct.pack_into('<H', grid, 65535*2, 0xffff)
        self.assertEqual(encontrar_estrutura_impacto(view, 0xabcdffff), 1023)
        struct.pack_into('<H', grid, 65535*2, 0x8000 | (999 << 5) | 31)
        self.assertEqual(encontrar_estrutura_impacto(view, -1), 999)
        struct.pack_into('<H', grid, 65535*2, 0x7fff)
        self.assertEqual(encontrar_estrutura_impacto(view, 65535), 65535)
        with self.assertRaisesRegex(ValueError, '65536-word'):
            encontrar_estrutura_impacto(bytes(2), 0)

    def test_adapter_forwards_exact_other_queries_and_errors(self):
        observed = []
        q = ConsultaGradeImpacto(bytes(131072), lambda n, a: observed.append((n, a)) or 123)
        self.assertEqual(q('ChercheIndiceBatiment', (0,)), 65535)
        args = (0xffff, 0xffff, 255)
        self.assertEqual(q('ChercheIndiceEnginCible', args), 123)
        self.assertEqual(observed, [('ChercheIndiceEnginCible', args)])
        with self.assertRaisesRegex(NotImplementedError, 'PlayerGetType'):
            ConsultaGradeImpacto(bytes(131072))('PlayerGetType', (0,))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialGradeImpacto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_impacto_unidades import BancadaImpactoUnidades
        cls.b = BancadaImpactoUnidades()
        cls.lookup_returns = cls.building_stops = cls.complete_projectiles = 0

    def lookups(self, entries):
        from bancada_combate import GRADE
        grid = bytearray(131072)
        for cell, value in entries:
            struct.pack_into('<H', grid, (cell & 65535)*2, value)
        self.b.cpu.mem_write(GRADE, bytes(grid))
        before_units = self.b.ler_unidades()
        for cell, _ in entries:
            r = self.b.executar(0x41b54a, [(0x41b54a, 0x41b579)],
                dict(EAX=(cell & 0xffffffff) | 0xabcd0000, EDX=0xface1234))
            self.assertEqual(r['EAX'], encontrar_estrutura_impacto(grid, cell))
            self.assertEqual(r['EDX'], 0xface1234)
            type(self).lookup_returns += 1
        self.assertEqual(bytes(self.b.cpu.mem_read(GRADE, 131072)), grid)
        self.assertEqual(self.b.ler_unidades(), before_units)

    def test_original_every_ten_bit_id_and_low_subcell_bits(self):
        entries = [(4*index+i, 0x8000 | (index << 5) | sub)
                   for index in range(1024) for i, sub in enumerate((0, 1, 15, 31))]
        self.lookups(entries)

    def test_original_nonbuilding_tags_and_cell_width_edges(self):
        entries = [(i, value) for i, value in enumerate((0, 1, 31, 32, 0x3fff, 0x4000,
            0x4007, 0x58f8, 0x7fe0, 0x7fff))]
        entries += [(0xfffe, 0x8000), (0xffff, 0xffff), (0xabcdffff, 0xffff), (-1, 0xffff)]
        self.lookups(entries)

    def test_original_building_priority_stops_before_unit_consumer(self):
        from bancada_combate import GRADE
        for building in (0, 7, 999, 1000, 1023):
            us, rows = damage_tests.fixture()
            us[1][0xab] = 0
            self.b.preparar_wrapper(us, rows, grade={0x8080: 0x8000 | (building << 5) | 31})
            native = self.b.impacto(0x8080)
            self.assertEqual(native['EIP'], 0x4508af)
            grid = bytes(self.b.cpu.mem_read(GRADE, 131072))
            q = ConsultaAlvosImpacto(us, ConsultaGradeImpacto(grid))
            def forbidden(*args):
                self.fail('Unit consumer must not run before building boundary')
            w = ImpactoUnidades(us, None, consumir=forbidden, consulta=q)
            with self.assertRaises(LimiteImpactoBatiment):
                w.infligir(0x8080, 1, 0, 0, 0)
            self.assertEqual(self.b.ler_unidades(), b''.join(us))
            self.assertEqual([e[0] for e in self.b.eventos_wrapper], ['ChercheIndiceBatiment'])
            self.assertEqual(self.b.eventos_wrapper[0][2], building)
            type(self).building_stops += 1

    def test_computed_both_lookups_in_complete_projectile_returns(self):
        from bancada_combate import GRADE
        for kind in (2, 3, 12, 16, 25):
            us, rows = damage_tests.fixture(tipo_alvo=kind)
            us[1][0xab] = 0
            us[799][:] = us[1]
            pool = PoolProjeteis(bytearray(5600))
            pool.definir(37, 9, 0x8080, 0x8080, 1, 0, 17, 16, 16, 0)
            pool.registro(37)[0x19] = 0
            self.b.preparar_wrapper(us, rows)
            self.b.pool(pool.memoria)
            native = self.b.avancar_ate_fim()
            w, remaining, consumer_remaining = impact_tests.DiferencialImpactoUnidades.model(
                self, us, rows, pool, native)
            grid = bytes(self.b.cpu.mem_read(GRADE, 131072))
            provider = ConsultaAlvosImpacto(us, ConsultaGradeImpacto(grid, w.consulta))
            def query(name, args):
                if name in ('ChercheIndiceBatiment', 'ChercheIndiceEnginCible'):
                    event = next(remaining)
                    result = provider(name, args)
                    self.assertEqual((name, args, result), tuple(event))
                    return result
                return provider(name, args)
            w.consulta = query
            pool.efeito_externo = w.receber
            avancar_linear(pool, 37)
            self.assertEqual(list(remaining), [])
            self.assertEqual(list(consumer_remaining), [])
            self.assertEqual(self.b.ler_unidades(), b''.join(us))
            self.assertEqual(self.b.ler_pool(), pool.memoria)
            self.assertEqual(bytes(self.b.cpu.mem_read(GRADE, 131072)), grid)
            self.assertEqual((u16(us[1], 0x9a), u16(us[799], 0x9a), pool.registro(37)[2]), (100, 80, 0))
            type(self).complete_projectiles += 1
