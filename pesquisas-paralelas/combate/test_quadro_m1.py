"""First-frame combat calls over the M1 post-load input against original captures.

Local tests replay `MaquinaProjeteis.calcular` on the frozen M1 pool and compare
bytes and the ordered store trace with `captura-quadro-m1-original.json`.
With RISING_EMULAR=1 the original-only capture is rerun and must equal the
committed fixture.
"""
import hashlib
import json
import os
import struct
import unittest
from pathlib import Path

from capturar_quadro_m1 import CASOS, PONTEIRO_POOL, blocos_m1
from maquina_projeteis import MaquinaProjeteis
from projeteis import PoolProjeteis

CAPTURA = Path(__file__).resolve().parent / 'evidencias/captura-quadro-m1-original.json'


def sha(dados):
    return hashlib.sha256(bytes(dados)).hexdigest()


class RegistroGravado:
    """Record view that logs every byte store with its pool offset."""
    def __init__(self, memoria, base, stores):
        self.memoria, self.base, self.stores = memoria, base, stores

    def __getitem__(self, k):
        return self.memoria[self.base + k]

    def __setitem__(self, k, v):
        self.stores.append((self.base + k, v))
        self.memoria[self.base + k] = v


class PoolGravado(PoolProjeteis):
    def __post_init__(self):
        super().__post_init__()
        self.stores = []

    def registro(self, indice):
        if not 0 <= indice < 100:
            raise ValueError('Índice de projétil fora de 0..99')
        return RegistroGravado(self.memoria, indice * 56, self.stores)


def pool_m1():
    _sha, blocos = blocos_m1()
    base, dgroup = blocos['dgroup']
    ponteiro = struct.unpack_from('<I', dgroup, PONTEIRO_POOL - base)[0]
    for b, dados in blocos.values():
        if b <= ponteiro and ponteiro + 5600 <= b + len(dados):
            return ponteiro, bytearray(dados[ponteiro - b:ponteiro - b + 5600])
    raise ValueError('Projectile pool is not inside one M1 block')


class QuadroM1Projeteis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.captura = json.loads(CAPTURA.read_text())
        cls.casos = {c['nome']: c for c in cls.captura['capturas']}
        cls.ponteiro, cls.pool = pool_m1()

    def test_fixture_is_the_m1_input(self):
        _sha, blocos = blocos_m1()
        self.assertEqual(self.captura['rotulo'], 'M1 post-load input')
        self.assertEqual(self.captura['entrada']['sha256'], _sha)
        self.assertEqual(self.captura['entrada']['blocos'], len(blocos))
        self.assertEqual([c['nome'] for c in self.captura['capturas']], [c['nome'] for c in CASOS])

    def test_projectile_calcul_matches_original(self):
        for nome in ('projectile-calcul-m1-counter0', 'projectile-calcul-m1-counter1'):
            with self.subTest(nome):
                caso = self.casos[nome]
                self.assertTrue(caso['retornou'])
                self.assertIsNone(caso['parada'])
                self.assertEqual(caso['chamadas_observadas'], {'ProjectileAnim': 100})
                memoria = bytearray(self.pool)
                self.assertEqual(sha(memoria), caso['pool']['entrada_sha256'])
                pool = PoolGravado(memoria)  # no effect callbacks: any effect raises
                MaquinaProjeteis(pool).calcular(caso['contador_entrada'] & 255)
                self.assertEqual(pool.chamadas, [])
                self.assertEqual(sha(memoria), caso['pool']['saida_sha256'])
                self.assertEqual([[hex(self.ponteiro + k), 1, hex(v)] for k, v in pool.stores],
                                 caso['escritas_ordenadas_fora_da_pilha'])
                self.assertEqual(list(caso['alteracoes_por_bloco']), ['alloc00875'])

    def test_non_combat_frame_calls_are_classified(self):
        reset = self.casos['reset-m1']
        self.assertEqual((reset['instrucoes'], reset['escritas_ordenadas_fora_da_pilha']), (1, []))
        sympa = self.casos['sympa-m1-counter1']
        self.assertTrue(sympa['retornou'])
        self.assertEqual((sympa['escritas_ordenadas_fora_da_pilha'], sympa['alteracoes_por_bloco']), ([], {}))
        periodica = self.casos['sympa-m1-counter2000']
        self.assertEqual(periodica['parada'], {'nome': 'MAJSympathie', 'eip': '0x475118'})


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'RISING_EMULAR=1 reruns the original capture')
class QuadroM1Nativo(unittest.TestCase):
    def test_native_rerun_equals_fixture(self):
        from capturar_quadro_m1 import BancadaQuadroM1, capturar
        captura = json.loads(CAPTURA.read_text())
        bancada = BancadaQuadroM1(blocos_m1()[1])
        for caso, salvo in zip(CASOS, captura['capturas']):
            with self.subTest(caso['nome']):
                self.assertEqual(json.loads(json.dumps(capturar(bancada, caso))), salvo)


if __name__ == '__main__':
    unittest.main()
