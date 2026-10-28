"""Special-row mode-8 consumers and explicit non-mode-1 death boundary."""
import os
import random
import struct
import unittest

from consumo_dano import ConsumidorDanoUnidade, LimiteMorte
from bonus_combate import ConsultaBonusCombate
from projeteis import por16, u16
import test_consumo_dano as damage_tests
from test_bonus_combate import BonusUnidades


class ContratosDanoModo8(unittest.TestCase):
    def test_special_row_has_no_mode1_bonus_or_message_prefix(self):
        us, rows = damage_tests.fixture(vida=100)
        us[0][0xf7] = 255
        c, calls = damage_tests.local(us, rows+[bytes([20]*26)])
        c.bonus_4965ac = 255
        c.infligir(1, 0x108, 0, 255)
        self.assertEqual(u16(us[1], 0x9a), 80)
        self.assertEqual(calls, [('Modificateur', (0, 6, 0)), ('TerrainEstDecouvert', (0x8080, 0))])

    def test_missing_row_and_unsupported_modes_fail_before_callbacks(self):
        us, rows = damage_tests.fixture()
        c, calls = damage_tests.local(us, rows)
        with self.assertRaisesRegex(ValueError, 'row 26'):
            c.infligir(1, 8, 0)
        for mode in (0, 2, 3, 4, 5, 6, 7, 9, 255):
            with self.assertRaises(NotImplementedError):
                c.infligir(1, mode, 0)
        self.assertEqual(calls, [])
        self.assertEqual(u16(us[1], 0x9a), 100)

    def test_mode8_never_uses_mode1_lethal_handler(self):
        us, rows = damage_tests.fixture(vida=1)
        c, _ = damage_tests.local(us, rows+[bytes([20]*26)])
        c.morte = lambda *a: self.fail('Mode-1 lethal handler must not run for mode 8')
        with self.assertRaises(LimiteMorte) as caught:
            c.infligir(1, 8, 0)
        self.assertEqual((caught.exception.modo, caught.exception.endereco, u16(us[1], 0x9a)),
                         (8, 0x4506a1, 1))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialDanoModo8(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_consumo_dano import BancadaConsumoDano
        cls.b = BancadaConsumoDano()
        cls.complete_returns = cls.death_stops = cls.audio_stops = 0

    def compare(self, us, rows, special, mod6=0, visible=False, victim=1, attacker=0):
        from bancada_consumo_dano import TIPOS, MATRIZES, CONSUMO
        from bancada_combate import RETORNO
        self.b.preparar_consumo(us, rows, mod5=255, mod6=mod6, bonus=255, visivel=visible)
        self.b.cpu.mem_write(TIPOS+26*4, struct.pack('<I', MATRIZES+32*26))
        self.b.cpu.mem_write(MATRIZES+32*26, bytes(special))
        native = self.b.executar(0x4502f0, CONSUMO,
            dict(EAX=victim | 0xabcd0000, EDX=0xface0008,
                 EBX=attacker | 0xbeef0000, ECX=0xcafe00ff),
            parada={RETORNO, 0x4506a1, 0x48aa79}, limite_instrucoes=100000)
        if native['EIP'] == 0x48aa79:
            self.b._observar_consumo(self.b.cpu, 0x48aa79, 0, None)
        events = iter(self.b.eventos_consumo)
        bonus_bytes = bytes(self.b.cpu.mem_read(0x4dfba0, 1872))
        bonus = ConsultaBonusCombate(BonusUnidades(bonus_bytes))
        def check(name, args):
            event = next(events)
            self.assertEqual((name, args), tuple(event[:2]))
            return event
        def query(name, args):
            event = check(name, args)
            if name == 'Modificateur':
                self.assertEqual(args[1], 6)
                result = bonus(name, args)
            elif name == 'TerrainEstDecouvert':
                result = int(visible)
            elif name == 'EnginGetVolume':
                result = event[2]  # Audio geometry provider remains external.
            else:
                self.fail('Unexpected mode-1 prefix query '+name)
            self.assertEqual(result, event[2] if name in ('Modificateur', 'EnginGetVolume') else event[2] & 255)
            return result
        def effect(name, args):
            check(name, args)
            self.assertEqual(name, 'PlaySnd_PostSound')
            raise NotImplementedError('Expected audio stop')
        c = ConsumidorDanoUnidade(us, rows+[special], query, effect, bonus_4965ac=255,
            morte=lambda *args: self.fail('Mode-8 death must not call mode-1 handler'))
        if native['EIP'] == 0x4506a1:
            with self.assertRaises(LimiteMorte) as caught:
                c.infligir(victim, 8, attacker, 255)
            self.assertEqual(caught.exception.modo, 8)
            type(self).death_stops += 1
        elif native['EIP'] == 0x48aa79:
            with self.assertRaisesRegex(NotImplementedError, 'audio'):
                c.infligir(victim, 8, attacker, 255)
            type(self).audio_stops += 1
        else:
            self.assertEqual(native['EIP'], RETORNO)
            c.infligir(victim, 8, attacker, 255)
            type(self).complete_returns += 1
        self.assertEqual(list(events), [])
        self.assertEqual(self.b.ler_unidades(), b''.join(us))
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4dfba0, 1872)), bonus_bytes)

    def test_original_every_source_victim_type_and_loaded_bonus(self):
        rng = random.Random(0x450475)
        for source in range(26):
            for target in range(26):
                us, rows = damage_tests.fixture(tipo_alvo=target, tipo_fonte=source, vida=1000)
                us[0][0xf7], us[1][0xf6] = rng.randrange(256), rng.randrange(256)
                special = rng.randbytes(26)
                self.compare(us, rows, special, mod6=rng.randrange(256))

    def test_original_fixed_width_life_protection_and_reduction_edges(self):
        for life in (0, 1, 127, 128, 255, 65535):
            for raw in (0, 1, 127, 128, 255):
                for reduction in (0, 1, 255):
                    for modifier in (0, 1, 255):
                        for protection in (0, 8):
                            us, rows = damage_tests.fixture(vida=life)
                            us[1][0xf6], us[1][0xdc] = reduction, protection
                            self.compare(us, rows, bytes([raw]*26), modifier)

    def test_original_visible_audio_and_existing_handles(self):
        for kind in (0, 2, 12, 25):
            for handle in (0, 1, 0x80000000, 0xfffffffe, 0xffffffff):
                us, rows = damage_tests.fixture(tipo_alvo=kind)
                us[1][0xf9] = 223
                struct.pack_into('<I', us[1], 0x104, handle)
                self.compare(us, rows, bytes([20]*26), visible=True)

    def test_original_id_edges_and_source_victim_alias(self):
        for victim in (0, 1, 798, 799):
            for attacker in (0, 799):
                us, rows = damage_tests.fixture(vida=1000)
                source, target = bytes(us[0]), bytes(us[1])
                us[attacker][:], us[victim][:] = source, target
                self.compare(us, rows, bytes([20]*26), victim=victim, attacker=attacker)
