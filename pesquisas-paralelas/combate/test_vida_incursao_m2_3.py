"""MONDE01 raid unit's first frames (forced counter 9000..): combat calls against the native capture.

Replays the Python entries on the inputs saved in
`captura-vida-incursao-m2-3-original.json` and compares them with the isolated
native calls of every frame: ProjectileCalcul, EnginTrouveCible (with the
PlayerEstAllie queries it makes), PlayerEstAllie's register contract,
PlayerAttaqueReset and PlayerAttaqueCalculSympa.  Nothing is emulated here;
the capture is the native run.
"""
import json
import unittest
from pathlib import Path

import alvos_alcance
from alvos_alcance import aliados, encontrar_alvo
from maquina_projeteis import MaquinaProjeteis
from test_quadro1_combate import Grade, bytes_de, registros_player_est_allie
from test_quadro_m1 import PoolGravado

CAPTURA = Path(__file__).resolve().parent / 'evidencias/captura-vida-incursao-m2-3-original.json'
POOL = 0x418e2000  # [0x5080f0] in this path (M1 allocation 875)
NUNCA = ('SetAttaqueEngin', 'CalculAttaqueEngin', 'InfligeDegat', 'ProjectileInit', 'iagUnitSendMessage')


def inteiros(caso, chave):
    return {k: int(v, 16) for k, v in caso[chave].items()}


class VidaIncursaoM23(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(CAPTURA.read_text())

    def registros(self, rotina):
        return [r for r in self.d['calls'] if r['routine'] == rotina]

    def test_capture_is_complete(self):
        d = self.d
        self.assertFalse(d['translation_executed'])
        n = len(d['frames'])
        self.assertEqual([q['counter'] for q in d['frames']], list(range(9000, 9000 + n)))
        self.assertTrue(all(c['reached_return'] for r in d['calls'] for c in r['cases']))
        # Frame 0 (load_tail, counter 0) is paused too, then one call per forced frame.
        for rotina in ('PlayerAttaqueReset', 'ProjectileCalcul', 'PlayerAttaqueCalculSympa'):
            registros = self.registros(rotina)
            self.assertEqual([r['phase'] for r in registros[:2]], ['load_tail', 'frame1'], rotina)
            self.assertEqual([r['python_inputs']['counter'] for r in registros],
                             [0] + list(range(9000, 9000 + n)), rotina)
        alvos = [(r['python_inputs']['counter'], int(r['cases'][0]['entry_registers']['EAX'], 16) & 0xffff)
                 for r in self.registros('EnginTrouveCible')]
        self.assertIn((9008, 16), alvos)  # the raid unit's first target query: (counter + 16) & 31 == 0
        nomes = {e[0] for r in d['calls'] for e in r['cases'][0]['entries']}
        self.assertFalse(nomes & set(NUNCA))

    def test_projectile_calcul_every_frame(self):
        for r in self.registros('ProjectileCalcul'):
            entradas, caso = r['python_inputs'], r['cases'][0]
            with self.subTest(counter=entradas['counter']):
                memoria = bytearray(bytes_de(entradas['pool']))
                antes = bytes(memoria)
                avancos = []
                maquina = MaquinaProjeteis(PoolGravado(memoria))
                original = maquina.avancar

                def avancar(i, original=original):
                    avancos.append(i)
                    return original(i)
                maquina.avancar = avancar
                maquina.calcular(entradas['counter'] & 255)
                self.assertEqual(maquina.pool.chamadas, [])
                mudados = [[hex(POOL + k), antes[k], memoria[k]] for k in range(5600) if antes[k] != memoria[k]]
                self.assertEqual(mudados, caso['changed_bytes'])
                nativos = [(int(e[2], 16) - POOL) // 56 for e in caso['entries'] if e[0] == 'ProjectileAvance']
                self.assertEqual(avancos, nativos)

    def test_engin_trouve_cible_calls(self):
        registros = self.registros('EnginTrouveCible')
        self.assertTrue(registros)
        for r in registros:
            entradas, caso = r['python_inputs'], r['cases'][0]
            indice = int(caso['entry_registers']['EAX'], 16) & 0xffff
            with self.subTest(counter=entradas['counter'], unit=indice):
                dados = bytes_de(entradas['units'])
                unidades = [dados[i * 276:(i + 1) * 276] for i in range(800)]
                mascaras = bytes.fromhex(entradas['masks'])
                consultas = []
                original = alvos_alcance.aliados

                def gravar(origem, destino, m, original=original):
                    consultas.append((origem & 255, destino & 255))
                    return original(origem, destino, m)
                alvos_alcance.aliados = gravar
                try:
                    alvo = encontrar_alvo(unidades, indice, Grade(bytes_de(entradas['grid'])), mascaras)
                finally:
                    alvos_alcance.aliados = original
                self.assertEqual(alvo, int(caso['exit_registers']['EAX'], 16) & 0xffff)
                self.assertEqual(caso['changed_bytes'], [])
                nativas = [(int(e[2], 16) & 255, int(e[3], 16) & 255)
                           for e in caso['entries'] if e[0] == 'PlayerEstAllie']
                self.assertEqual(consultas, nativas)

    def test_player_est_allie_register_contract(self):
        registros = self.registros('PlayerEstAllie')
        self.assertTrue(registros)
        for r in registros:
            caso = r['cases'][0]
            e, x = inteiros(caso, 'entry_registers'), inteiros(caso, 'exit_registers')
            mascaras = bytes.fromhex(r['python_inputs']['masks'])
            self.assertEqual(int(aliados(e['EAX'], e['EDX'], mascaras)), x['EAX'] & 255)
            self.assertEqual(registros_player_est_allie(e['EAX'], e['EDX'], mascaras), (x['EAX'], x['EDX']))
            self.assertEqual((x['ECX'], caso['changed_bytes']), (e['ECX'], []))

    def test_reset_and_sympathy_store_nothing(self):
        for r in self.registros('PlayerAttaqueReset') + self.registros('PlayerAttaqueCalculSympa'):
            self.assertEqual(r['cases'][0]['changed_bytes'], [], (r['routine'], r['python_inputs']['counter']))


if __name__ == '__main__':
    unittest.main()
