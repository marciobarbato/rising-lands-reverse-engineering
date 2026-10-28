"""Shared-pool damage/death composition against intact original whole worlds."""
import os
from pathlib import Path
import struct
import sys
import unittest

from consumo_fisico import criar_consumidor_fisico
from bonus_combate import ConsultaBonusCombate
from proximidade_ataque import ConsultaProximidadeAtaque
from alvos_impacto import ConsultaAlvosImpacto
from impacto_unidades import ImpactoUnidades
from avanco_projeteis import avancar_linear
from projeteis import PoolProjeteis, por16, u16
from navegacao_unidades import MundoNavegacao
from ordens_unidades import ContextoBusca
from morte_unidades import DependenciaMorteUnidade

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'economia'))
from bonus_unidades import BonusUnidades


class SympathyStop(NotImplementedError):
    pass


def fixture(kind=2, victim=1, attacker=0, step=0x506, state=6, full=False):
    world = MundoNavegacao(256, 256)
    world.regioes[:] = [1]*65536
    world.controle_jogadores[:] = [1]*4
    for index, owner, type_, cell in ((attacker, 0, 12, 0x2020), (victim, 1, kind, 0x505)):
        p = index*276
        row = memoryview(world.unidades)[p:p+276]
        row[:] = b'\xa5'*276
        row[0], row[1], row[2], row[0x72], row[0xab] = owner, type_, state, 1, 0
        row[0xbd], row[0xdc], row[0xf6], row[0xf7] = 0, 0, 0, 0
        for offset, value in ((8, cell), (0x7c, step if index == victim else cell),
                              (0xa, 0), (0x9a, 1)):
            por16(row, offset, value)
        struct.pack_into('<I', row, 0x104, 0xffffffff)
        struct.pack_into('<I', row, 0x10c, 0xffffffff)
        struct.pack_into('<I', row, 0x110, 0)
    world.busca = ContextoBusca(victim, 1, 1, 0x12345678, 77)
    world.mini_unidades[0x505] = 42
    world.ocupar(victim, 0x505, True)
    if step != 0x505:
        world.ocupar(victim, step, True)
    pool = PoolProjeteis(bytearray(5600))
    if full:
        for i in range(100):
            pool.registro(i)[2] = 1
    return world, [bytes([20]*26) for _ in range(26)], pool


def queries(world, records):
    def other(name, args):
        if name == 'TerrainEstDecouvert':
            cell, player = args
            return int((world.descoberto[player][cell] & 31) == 0)
        raise NotImplementedError(name)
    return ConsultaBonusCombate(BonusUnidades(bytes(1872)),
        ConsultaProximidadeAtaque(records, struct.pack('<65536H', *world.regioes), other))


def fixture_message(world, name, args):
    """Only the original no-effect guard, not a general message provider."""
    if name != 'iagUnitSendMessage':
        raise NotImplementedError(name)
    index, message, source = args
    p = index*276
    owner = world.unidades[p]
    group = struct.unpack_from('<I', world.unidades, p+0x10c)[0]
    if (owner >= 4 or world.controle_jogadores[owner] == 2) and group != 0xffffffff:
        raise NotImplementedError('Active AI group fixture is unsupported')


class ContratosConsumoFisico(unittest.TestCase):
    def test_shared_records_see_both_world_and_combat_writes(self):
        w, rows, pool = fixture()
        c = criar_consumidor_fisico(w, pool, rows,
            efeito=lambda n, a: fixture_message(w, n, a))
        self.assertTrue(all(isinstance(r, memoryview) and not r.readonly and r.obj is w.unidades
                            for r in c.unidades))
        w.unidades[276+0xf6] = 3
        self.assertEqual(c.unidades[1][0xf6], 3)
        c.unidades[1][0xf6] = 0
        self.assertEqual(w.unidades[276+0xf6], 0)
        c.consulta = queries(w, c.unidades)
        with self.assertRaisesRegex(NotImplementedError, 'MAJSympathie'):
            c.infligir(1, 1, 0)
        self.assertEqual((u16(c.unidades[1], 0x9a), c.unidades[1][2]), (0, 4))
        self.assertEqual((w.regioes[0x505], w.regioes[0x506]), (1, 1))

    def test_physical_exception_identity_and_prior_child_are_retained(self):
        w, rows, pool = fixture(kind=1)
        sentinel = DependenciaMorteUnidade(1, 'test provider', 0x443dfc, 0x443dfc)
        def stop(index):
            self.assertEqual((index, u16(memoryview(w.unidades)[276:552], 0x9a)), (1, 0))
            self.assertEqual((pool.registro(0)[0], pool.registro(0)[2]), (6, 1))
            raise sentinel
        w.iniciar_morte_unidade = stop
        c = criar_consumidor_fisico(w, pool, rows, efeito=lambda n, a: fixture_message(w, n, a))
        c.consulta = queries(w, c.unidades)
        with self.assertRaises(DependenciaMorteUnidade) as caught:
            c.infligir(1, 1, 0)
        self.assertIs(caught.exception, sentinel)
        self.assertEqual((u16(c.unidades[1], 0x9a), c.unidades[1][2]), (0, 6))

    def test_missing_level_still_precedes_life_and_physical_death(self):
        w, rows, pool = fixture()
        w.unidades[1] = 0
        c = criar_consumidor_fisico(w, pool, rows, efeito=lambda n, a: fixture_message(w, n, a))
        c.consulta = queries(w, c.unidades)
        with self.assertRaisesRegex(NotImplementedError, 'EnginSetLevelExperience'):
            c.infligir(1, 1, 0)
        self.assertEqual((u16(c.unidades[1], 0x9a), c.unidades[1][2]), (1, 6))
        self.assertEqual(c.unidades[0][0xaf], 0xa0)

    def test_invalid_backing_pool_fails_before_callbacks(self):
        w, rows, pool = fixture()
        w.unidades = bytes(w.unidades)
        with self.assertRaisesRegex(ValueError, 'writable'):
            criar_consumidor_fisico(w, pool, rows)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialConsumoFisico(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_consumo_fisico import BancadaConsumoFisico
        cls.b = BancadaConsumoFisico()
        cls.complete_consumers = cls.complete_projectiles = cls.sympathy_stops = 0
        cls.physical_stops = {}

    def compare(self, kind=2, victim=1, attacker=0, step=0x506, state=6,
                full=False, sympathy_stop=False, prepare=None, checkpoint=None, projectile=False):
        from emulador import RETORNO
        w, rows, pool = fixture(kind, victim, attacker, step, state, full)
        if prepare:
            prepare(w)
        if projectile:
            pool.definir(37, 9, 0x505, 0x505, 1, attacker, 17, 16, 16, 0)
            pool.registro(37)[0x19] = 0
        self.b.preparar(w, rows, pool)
        native = self.b.consumir(victim, attacker,
            checkpoint=checkpoint or (0x475118 if sympathy_stop else RETORNO), projectile=projectile)
        expected_events = iter(self.b.eventos_consumo)
        external_death = []
        def effect(name, args):
            if name == 'iagUnitSendMessage':
                e = next(expected_events)
                self.assertEqual((name, args), (e[0], e[1]))
                return fixture_message(w, name, args)
            external_death.append((name, args))
            self.assertEqual(name, 'MAJSympathie')
            if sympathy_stop:
                raise SympathyStop(name)
            # All native fixture owners have original inactivity byte 1.
            self.assertEqual(tuple(args[:2]), (1, 0))
        c = criar_consumidor_fisico(w, pool, rows, efeito=effect)
        actual_queries = queries(w, c.unidades)
        def query(name, args):
            event = next(expected_events)
            result = actual_queries(name, args)
            self.assertEqual((name, args), tuple(event[:2]))
            # The native predicates define AL; upper EAX bits may retain cell.
            observed = event[2] if name == 'Modificateur' else event[2] & 255
            self.assertEqual(result, observed)
            return result
        c.consulta = query
        wrapper_events = iter(self.b.eventos_wrapper)
        def wrapper_event(name, args):
            event = next(wrapper_events)
            self.assertEqual((name, args), (event[0], event[1]))
            return event
        if projectile:
            resolver = ConsultaAlvosImpacto(c.unidades)
            def wrapper_query(name, args):
                event = wrapper_event(name, args)
                if name == 'ChercheIndiceEnginCible':
                    result = resolver(name, args)
                    self.assertEqual(result, event[2])
                    return result
                return event[2]  # Other wrapper world queries remain observed fixtures.
            def consume(*args):
                wrapper_event('EnginInfligeDegat', args)
                c.infligir(*args)
            def wrapper_effect(name, args):
                wrapper_event(name, args)
            impact = ImpactoUnidades(c.unidades, pool, consume, wrapper_query, wrapper_effect,
                jogador_local=w.jogador_local, celula_alerta=0x1234)
            pool.efeito_externo = impact.receber
        run = (lambda: avancar_linear(pool, 37)) if projectile else (lambda: c.infligir(victim, 1, attacker, 255))
        if checkpoint:
            with self.assertRaises(DependenciaMorteUnidade) as caught:
                run()
            self.assertEqual(caught.exception.checkpoint, checkpoint)
            type(self).physical_stops[hex(checkpoint)] = type(self).physical_stops.get(hex(checkpoint), 0)+1
        elif sympathy_stop:
            with self.assertRaises(SympathyStop):
                run()
            type(self).sympathy_stops += 1
        else:
            self.assertEqual(native['EIP'], RETORNO)
            run()
            if projectile:
                type(self).complete_projectiles += 1
            else:
                type(self).complete_consumers += 1
        self.assertEqual(native['EIP'], checkpoint or (0x475118 if sympathy_stop else RETORNO))
        self.assertEqual(list(expected_events), [])
        self.assertEqual(list(wrapper_events), [])
        self.assertEqual(self.b.conferir_fisica(w), [])
        self.assertEqual(self.b.ler_pool(), pool.memoria)
        self.assertEqual(self.b.eventos_morte[0], ('SetDyingEngin', (victim,)))
        self.assertEqual(self.b.eventos_morte[1:], external_death)
        if not checkpoint:
            self.assertTrue(self.b.after_dying)
            self.assertEqual(u16(c.unidades[victim], 0x9a), 0)
            self.assertEqual(c.unidades[victim][2], 4 if state not in (0, 4) else state)
        if projectile and not checkpoint and not sympathy_stop:
            self.assertEqual(pool.registro(37)[2], 0)

    def test_original_ordinary_targets_and_current_reserved_cells(self):
        for kind in [*range(11), *range(18, 26)]:
            for step in (0x505, 0x506):
                for stop in (False, True):
                    with self.subTest(kind=kind, step=step, sympathy_stop=stop):
                        self.compare(kind=kind, step=step, sympathy_stop=stop)

    def test_original_child_pool_saturation_and_id_edges(self):
        for victim, attacker in ((1, 0), (799, 798), (0, 799)):
            for full in (False, True):
                self.compare(kind=1, victim=victim, attacker=attacker, full=full)

    def test_original_inactive_guard_preserves_physical_state(self):
        for state in (0, 4):
            self.compare(state=state)

    def test_original_physical_partial_failures_retain_prior_combat_effects(self):
        cases = [
            (2, 0x444c7e, lambda w: w.unidades.__setitem__(276+0xdc, 4)),
            (2, 0x48a446, lambda w: struct.pack_into('<I', w.unidades, 276+0x104, 123)),
            (1, 0x443dfc, lambda w: struct.pack_into('<H', w.unidades, 276+0xa, 1)),
            (1, 0x472683, lambda w: w.unidades.__setitem__(276+0xbd, 1)),
        ]
        cases.extend((kind, 0x46e44c if kind == 16 else 0x4704dc, None) for kind in range(11, 18))
        for kind, checkpoint, prepare in cases:
            with self.subTest(kind=kind, checkpoint=hex(checkpoint)):
                self.compare(kind=kind, checkpoint=checkpoint, prepare=prepare)

    def test_original_projectile_consumer_and_physical_death_return(self):
        for kind in (1, 2, 3, 25):
            for stop in (False, True):
                self.compare(kind=kind, projectile=True, sympathy_stop=stop)
