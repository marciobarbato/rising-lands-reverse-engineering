"""Regressions over the original real-state turret order matrix."""
import json
import os
import unittest

from bancada_ordens_torres_combate import carregar_estados_torres
from ordens_torres_combate import OrdensTorresCombate, REGISTERS
from validar_combate_raid import memory, serialize, write_state
from validar_ordens_torres_combate import CAPTURE, comparar


class TurretInputMatrix(unittest.TestCase):
    def test_every_original_case_whole_state_and_all_registers(self):
        report = comparar()
        self.assertEqual(report['summary'], dict(cases=188, mismatches=0, routines={
            'BatimentPeutAttaquer': 148, 'BatimentInitAttaqueSelect': 40}))

    def test_live_selection_and_reference_before_mode_store(self):
        states, _ = carregar_estados_torres()
        m, blocks = memory(states['P6-frame2020'])
        before = serialize(blocks)
        live = OrdensTorresCombate(m)
        self.assertEqual(serialize(blocks), before)
        # A binding created before a new selection must read that new selection.
        m.u16(0x495be0, 1)
        observed = []
        class Trace:
            def __getattr__(self, name):
                underlying = getattr(m, name)
                if name not in ('u8', 'u16', 'u32'):
                    return underlying
                def access(a, value=None):
                    if value is not None: observed.append((a, value))
                    return underlying(a, value)
                return access
        live.m = Trace()
        regs = dict(zip(REGISTERS, (0, 0xffff, 0x31415926, 1, 4, 5, 6)))
        out = live.provedores()['BatimentInitAttaqueSelect'](regs)
        self.assertEqual(set(out), set(REGISTERS))
        self.assertEqual(observed, [(0x49a1dc + 0x86, 65535), (0x49a1dc + 0x7b, 1)])

    def test_protected_uninitialized_mode_never_manufactures_a_target(self):
        states, _ = carregar_estados_torres()
        m, blocks = memory(write_state(states['P6-frame2020'], [('0x49a0d0', '0a')]))
        live = OrdensTorresCombate(m)
        before = serialize(blocks)
        regs = {k: 0 for k in REGISTERS}
        regs['EDX'] = 2
        with self.assertRaisesRegex(ValueError, 'uninitialized native stack'):
            live.batiment_peut_attaquer(regs)
        self.assertEqual(serialize(blocks), before)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'RISING_EMULAR=1 runs the original turret leaves')
class TurretInputNative(unittest.TestCase):
    def test_all_native_returns_registers_stores_and_whole_state(self):
        report = comparar(native=True)
        self.assertEqual(report['summary']['cases'], 188)
        self.assertEqual(report['summary']['mismatches'], 0)


if __name__ == '__main__':
    unittest.main()
