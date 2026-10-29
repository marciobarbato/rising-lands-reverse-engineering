"""ProjectileSet 0x46e208 at MONDE01's raid spawn against the isolated native capture.

`PoolProjeteis.definir` replays both cases of `captura-projectile-set-m2-3-original.json`
(type 0x20 as captured, and DL = 0x1f) on the entry pool with the entry
registers and stack words; its pool bytes must equal the native changed bytes,
and it must request no effect.  Nothing is emulated here.
"""
import json
import unittest
from pathlib import Path

from projeteis import PoolProjeteis
from test_quadro1_combate import bytes_de

CAPTURA = Path(__file__).resolve().parent / 'evidencias/captura-projectile-set-m2-3-original.json'
POOL = 0x418e2000  # [0x5080f0] in this path (M1 allocation 875)


class ProjectileSetIncursao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(CAPTURA.read_text())

    def test_capture_is_the_raid_spawn(self):
        (r,) = self.d['calls']
        self.assertFalse(self.d['translation_executed'])
        self.assertEqual((r['routine'], r['phase'], r['caller']), ('ProjectileSet', 'frame1', 'ProjectileInit+0x76'))
        self.assertEqual([c['case'] for c in r['cases']], ['captured_inputs', 'type-0x1f'])
        self.assertTrue(all(c['reached_return'] and c['counter'] == 9000 for c in r['cases']))

    def test_definir_matches_both_spawn_types(self):
        (r,) = self.d['calls']
        for caso in r['cases']:
            with self.subTest(caso['case']):
                regs = {k: int(v, 16) for k, v in caso['entry_registers'].items()}
                regs.update({k: int(v, 16) for k, v in caso['perturbation']['registers'].items()})
                modo, atacante, direcao, dx, dy, flag = (int(v, 16) for v in caso['stack_words'])
                memoria = bytearray(bytes_de(caso['pool_before']))
                antes = bytes(memoria)
                pool = PoolProjeteis(memoria)
                pool.definir(regs['EAX'] & 0xffff, regs['EDX'] & 255, regs['EBX'] & 0xffff, regs['ECX'] & 0xffff,
                             modo, atacante, direcao, dx, dy, flag)
                self.assertEqual(pool.chamadas, [])
                mudados = [[hex(POOL + k), antes[k], memoria[k]] for k in range(5600) if antes[k] != memoria[k]]
                self.assertEqual(mudados, caso['changed_bytes'])
                self.assertEqual(memoria[0], {'captured_inputs': 0x20, 'type-0x1f': 0x1f}[caso['case']])


if __name__ == '__main__':
    unittest.main()
