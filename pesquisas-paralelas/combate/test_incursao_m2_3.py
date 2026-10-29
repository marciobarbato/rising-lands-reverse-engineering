"""MONDE01's first monster raid (forced counter 9000): combat calls against the native capture.

Replays the Combat-owned calls the forced raid frame reaches, using the inputs
saved in `captura-incursao-m2-3-original.json`: ProjectileInit for the spawn
effect (inside ConstruitGroupeMonstre) and the following ProjectileCalcul.
Nothing here is emulated; the capture itself is the native run.
"""
import json
import struct
import unittest
from pathlib import Path

from maquina_projeteis import MaquinaProjeteis
from projeteis import PoolProjeteis
from test_quadro1_combate import bytes_de
from test_quadro_m1 import PoolGravado

CAPTURA = Path(__file__).resolve().parent / 'evidencias/captura-incursao-m2-3-original.json'
POOL = 0x418e2000  # [0x5080f0] in this path (M1 allocation 875)


def mudancas(antes, depois):
    return [[hex(POOL + k), antes[k], depois[k]] for k in range(5600) if antes[k] != depois[k]]


class IncursaoM23(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d = json.loads(CAPTURA.read_text())
        cls.d = d
        cls.casos = {(r['routine'], c['case']): c for r in d['calls'] for c in r['cases']}
        cls.avance = cls.casos[('AvanceMonstre', 'forced-counter-9000')]
        cls.calcul = cls.casos[('ProjectileCalcul', 'after-forced-avance-monstre')]

    def test_forced_capture_is_complete(self):
        self.assertTrue(self.d['path_reproduction']['passed'])
        self.assertFalse(self.d['translation_executed'])
        self.assertTrue(self.avance['reached_return'] and self.calcul['reached_return'])
        self.assertEqual((self.avance['counter'], self.calcul['counter']), (9000, 9000))
        nomes = [e[0] for e in self.avance['entries']]
        self.assertIn('ConstruitGroupeMonstre', nomes)
        self.assertNotIn('SetAttaqueEngin', nomes)
        self.assertNotIn('InfligeDegat', nomes)

    def test_spawn_effect_projectile_init(self):
        (entrada,) = [e for e in self.avance['entries'] if e[0] == 'ProjectileInit']
        tipo, origem, alvo, modo, *pilha = (int(v, 16) for v in entrada[2:6] + entrada[6:11])
        self.assertEqual(entrada[1], 'ConstruitGroupeMonstre+0xaf')
        antes = bytes_de(self.avance['pool_before'])
        memoria = bytearray(antes)
        pool = PoolProjeteis(memoria)
        indice = pool.iniciar(tipo, origem, alvo, modo, *pilha)
        self.assertEqual((indice, tipo, origem, alvo), (0, 0x20, 0x3e3e, 0x3e3e))
        self.assertEqual(pool.chamadas, [])
        nativas = [c for c in self.avance['changed_bytes'] if POOL <= int(c[0], 16) < POOL + 5600]
        self.assertEqual(mudancas(antes, memoria), nativas)
        self.assertEqual(bytes(memoria), bytes_de(self.calcul['pool_before']))

    def test_projectile_calcul_after_spawn(self):
        memoria = bytearray(bytes_de(self.calcul['pool_before']))
        antes = bytes(memoria)
        avancos = []
        maquina = MaquinaProjeteis(PoolGravado(memoria))
        original = maquina.avancar

        def avancar(i):
            avancos.append(i)
            return original(i)
        maquina.avancar = avancar
        maquina.calcular(self.calcul['counter'] & 255)
        self.assertEqual(maquina.pool.chamadas, [])
        self.assertEqual(mudancas(antes, memoria), self.calcul['changed_bytes'])
        nativos = [(int(e[2], 16) - POOL) // 56 for e in self.calcul['entries'] if e[0] == 'ProjectileAvance']
        self.assertEqual(avancos, nativos)
        self.assertEqual(len(avancos), 29)

    def test_monster_tables_before_raid(self):
        t = self.avance['tables_before']
        registros = bytes.fromhex(t['monster_records'])
        r0 = struct.unpack_from('<HHHBBI', registros, 0)
        self.assertEqual(r0, (0x3f3f, 1, 9000, 0, 0, 0))
        self.assertEqual(struct.unpack_from('<HHHBBI', registros, 12)[:3], (0x3f00, 1, 10800))
        self.assertEqual(bytes.fromhex(t['monster_header'])[:1], b'\x01')


if __name__ == '__main__':
    unittest.main()
