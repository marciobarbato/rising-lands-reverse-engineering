"""Combat calls at the exact frame-0/frame-1 inputs of Missions' first-frame path.

Local tests replay the Python entries on the inputs saved in
`captura-isolada-combate-quadro1.json` and compare them with the isolated
native calls. With RISING_EMULAR=1, PlayerEstAllie 0x46d838 is also checked
natively against its full register contract.
"""
import base64
import json
import os
import random
import struct
import unittest
import zlib
from pathlib import Path

import alvos_alcance
from alvos_alcance import aliados, encontrar_alvo
from maquina_projeteis import MaquinaProjeteis
from test_quadro_m1 import PoolGravado, sha

EVID = Path(__file__).resolve().parent / 'evidencias'
CAPTURA = EVID / 'captura-isolada-combate-quadro1.json'
CAPTURA_M1 = EVID / 'captura-quadro-m1-original.json'


def bytes_de(pacote):
    dados = zlib.decompress(base64.b64decode(pacote['zlib_base64']))
    assert len(dados) == pacote['bytes'] and sha(dados) == pacote['sha256']
    return dados


class Grade:
    def __init__(self, dados):
        self.palavras = struct.unpack('<65536H', dados)

    def get(self, celula, padrao=None):
        return self.palavras[celula]


def registros_player_est_allie(eax, edx, mascaras):
    """Register contract of 0x46d838 (AL origin, DL target); ECX is preserved."""
    al, dl = eax & 255, edx & 255
    if al == dl:
        return (eax & ~255) | 1, edx
    if al > 4 or dl > 4:
        return 0, edx
    bit = 1 << dl
    return int(bool(mascaras[al] & bit)), (edx & ~255) | bit


class Quadro1Combate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.captura = json.loads(CAPTURA.read_text())
        cls.chamadas = [(r['routine'], r['frame']) for r in cls.captura['calls']]

    def registros(self, rotina, quadro=None):
        return [r for r in self.captura['calls']
                if r['routine'] == rotina and (quadro is None or r['frame'] == quadro)]

    def test_capture_reproduces_the_committed_frame_path(self):
        self.assertTrue(self.captura['path_reproduction']['passed'])
        self.assertFalse(self.captura['translation_executed'])
        self.assertEqual(self.chamadas, [
            ('PlayerAttaqueReset', 'frame0'), ('ProjectileCalcul', 'frame0'), ('EnginTrouveCible', 'frame0'),
            *[('PlayerEstAllie', 'frame0')] * 7, ('PlayerAttaqueCalculSympa', 'frame0'),
            ('PlayerAttaqueReset', 'frame1'), ('ProjectileCalcul', 'frame1'), ('PlayerAttaqueCalculSympa', 'frame1')])
        self.assertTrue(all(c['reached_return'] for r in self.captura['calls'] for c in r['cases']))

    def test_projectile_calcul_at_exact_inputs(self):
        m1 = {c['nome']: c for c in json.loads(CAPTURA_M1.read_text())['capturas']}
        m1_pool = m1['projectile-calcul-m1-counter0']['pool']
        esperado_entrada = {'frame0': m1_pool['entrada_sha256'], 'frame1': m1_pool['saida_sha256']}
        for r in self.registros('ProjectileCalcul'):
            with self.subTest(r['frame']):
                caso, entradas = r['cases'][0], r['python_inputs']
                memoria = bytearray(bytes_de(entradas['pool']))
                self.assertEqual(sha(memoria), esperado_entrada[r['frame']])
                self.assertEqual(entradas['counter'], {'frame0': 0, 'frame1': 1}[r['frame']])
                ponteiro = int(m1_pool['ponteiro'], 16)
                antes = bytes(memoria)
                pool = PoolGravado(memoria)
                MaquinaProjeteis(pool).calcular(entradas['counter'] & 255)
                self.assertEqual(pool.chamadas, [])
                mudados = [[hex(ponteiro + k), antes[k], memoria[k]] for k in range(5600) if antes[k] != memoria[k]]
                self.assertEqual(mudados, caso['changed_bytes'])
                self.assertEqual(len(pool.stores), {'frame0': 100, 'frame1': 0}[r['frame']])

    def test_engin_trouve_cible_at_frame0_input(self):
        (r,) = self.registros('EnginTrouveCible', 'frame0')
        caso, entradas = r['cases'][0], r['python_inputs']
        dados = bytes_de(entradas['units'])
        unidades = [dados[i * 276:(i + 1) * 276] for i in range(800)]
        mascaras = bytes.fromhex(entradas['masks'])
        consultas = []
        original = alvos_alcance.aliados

        def gravar(origem, destino, m):
            consultas.append((origem & 255, destino & 255))
            return original(origem, destino, m)
        alvos_alcance.aliados = gravar
        try:
            alvo = encontrar_alvo(unidades, int(caso['entry_registers']['EAX'], 16) & 0xffff,
                                  Grade(bytes_de(entradas['grid'])), mascaras)
        finally:
            alvos_alcance.aliados = original
        self.assertEqual(alvo, int(caso['exit_registers']['EAX'], 16) & 0xffff)
        self.assertEqual(caso['changed_bytes'], [])
        nativas = [(int(c['cases'][0]['entry_registers']['EAX'], 16) & 255,
                    int(c['cases'][0]['entry_registers']['EDX'], 16) & 255)
                   for c in self.registros('PlayerEstAllie', 'frame0')]
        self.assertEqual(consultas, nativas)

    def test_player_est_allie_at_frame0_inputs(self):
        for r in self.registros('PlayerEstAllie'):
            caso = r['cases'][0]
            e, x = ({k: int(v, 16) for k, v in caso[n].items()} for n in ('entry_registers', 'exit_registers'))
            mascaras = bytes.fromhex(r['python_inputs']['masks'])
            self.assertEqual(int(aliados(e['EAX'], e['EDX'], mascaras)), x['EAX'] & 255)
            self.assertEqual(registros_player_est_allie(e['EAX'], e['EDX'], mascaras), (x['EAX'], x['EDX']))
            self.assertEqual((x['ECX'], caso['changed_bytes']), (e['ECX'], []))

    def test_non_combat_frame_calls(self):
        for r in self.registros('PlayerAttaqueReset'):
            self.assertEqual((r['cases'][0]['changed_bytes'], r['cases'][0]['read_before_write']), ([], []))
        for r in self.registros('PlayerAttaqueCalculSympa'):
            self.assertEqual(r['cases'][0]['changed_bytes'], [])


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'RISING_EMULAR=1 runs PlayerEstAllie natively')
class PlayerEstAllieNativo(unittest.TestCase):
    def test_register_contract(self):
        from bancada_combate import BancadaCombate, JOGADORES
        b = BancadaCombate()
        rng = random.Random(0x46d838)
        conjuntos = [bytes.fromhex('01020408a7'), bytes(5), b'\xff' * 5,
                     *[rng.randbytes(5) for _ in range(3)]]
        valores = (0, 1, 2, 3, 4, 5, 199, 200, 255)
        for mascaras in conjuntos:
            for i, m in enumerate(mascaras):
                b.cpu.mem_write(JOGADORES + 20 * i + 6, bytes([m]))
            for al in valores:
                for dl in valores:
                    eax = rng.getrandbits(24) << 8 | al
                    edx = rng.getrandbits(24) << 8 | dl
                    ecx = rng.getrandbits(32)
                    r = b.executar(0x46d838, [(0x46d838, 0x46d877)], dict(EAX=eax, EDX=edx, ECX=ecx))
                    self.assertEqual((r['EAX'], r['EDX'], r['ECX']),
                                     (*registros_player_est_allie(eax, edx, mascaras), ecx), (mascaras, al, dl))
                    self.assertEqual(r['EAX'] & 255, int(aliados(al, dl, mascaras)))


if __name__ == '__main__':
    unittest.main()
