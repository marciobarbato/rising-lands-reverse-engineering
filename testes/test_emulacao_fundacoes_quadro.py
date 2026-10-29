"""Fresh intact native vs Python differential of Core frame foundations over M1 state."""
import os
import random
import unittest

from test_fundacoes_quadro import EstadoQuadro, executar_python, conferir_registradores, captura

SENTINELAS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialFundacoesQuadro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_fundacoes_quadro import BancadaFundacoesQuadro, carregar_m1, ROTINAS
        cls.rotinas = ROTINAS
        cls.bancada = BancadaFundacoesQuadro()
        cls.dgroup, cls.thread, _ = carregar_m1()
        cls.comparacoes = 0

    @classmethod
    def tearDownClass(cls):
        if cls.bancada.hash_codigo() != cls.bancada.hash_codigo_inicial:
            raise AssertionError('Original code section changed')

    def caso(self, sobrescritas, passos):
        """Run steps natively and in Python from the same M1 (+derived) state; compare everything."""
        b = self.bancada
        b.carregar_estado(self.dgroup, self.thread, sobrescritas)
        estado = EstadoQuadro(self.dgroup, self.thread, sobrescritas)
        self.assertEqual(b.estado(), estado.bytes())
        for rotina, regs_in, relogio in passos:
            seg = b.chamar(rotina, regs_in, relogio=relogio)
            eax, escritas = executar_python(estado, rotina, regs_in['EAX'], relogio)
            self.assertEqual(b.estado(), estado.bytes(), rotina)
            self.assertEqual(seg['writes'], escritas, rotina)
            conferir_registradores(self, rotina, regs_in, seg['registers'], eax, estado)
            self.assertEqual([int(e['value'], 16) for e in seg['clock']], [] if relogio is None else [relogio])
            parada = self.rotinas[rotina][2]
            self.assertEqual((seg['registers']['ESP'], seg['registers']['EIP']),
                             (0x2008004, 0x3000000) if parada is None else (0x2008000, parada), rotina)
            type(self).comparacoes += 1

    def test_all_captured_cases_fresh(self):
        for c in captura()['cases']:
            with self.subTest(c['name']):
                passos = [(p['routine'], {k: int(v, 16) for k, v in p['registers_in'].items()},
                           None if p['declared_clock'] is None else int(p['declared_clock'], 16))
                          for p in c['steps']]
                self.caso([(int(a, 16), bytes.fromhex(d)) for a, d in c['derived_overrides']], passos)

    def test_fresh_random_seeds_limits_and_clocks(self):
        r = random.Random(0xf4a3e)
        for i in range(24):
            with self.subTest(i):
                regs = lambda eax: dict({n: r.getrandbits(32) for n in SENTINELAS}, EAX=eax,
                                        EFLAGS=2 | (r.getrandbits(12) & 0xcd5))
                sobrescritas = [(0x497164, r.getrandbits(32).to_bytes(4, 'little')),
                                (0x498db4, r.getrandbits(32).to_bytes(4, 'little')),
                                (0x340000c, r.getrandbits(32).to_bytes(4, 'little'))]
                passos = []
                for _ in range(12):
                    escolha = r.randrange(6)
                    if escolha == 0:
                        lim = r.choice((0, r.getrandbits(32), r.randrange(1, 64), 0x80000000 | r.getrandbits(31)))
                        passos.append(('iaRandom', regs(lim), r.getrandbits(32) if lim == 0 else None))
                    else:
                        rotina = ('Random', 'Randomize', 'SetRandomSeed', 'GetRandomSeed', 'LongRand')[escolha-1]
                        passos.append((rotina, regs(r.getrandbits(32)), None))
                self.caso(sobrescritas, passos)

    def test_fresh_counters_frame_counter_and_cursor(self):
        r = random.Random(0xc0de)
        for i in range(16):
            with self.subTest(i):
                c = [r.choice((r.getrandbits(32), 0xffffffff, 0xfffffffe, 0)) for _ in range(4)]
                sobrescritas = [(0x508f7c, b''.join(x.to_bytes(4, 'little') for x in c[:3])),
                                (0x496d40, c[3].to_bytes(4, 'little')), (0x4e1d18, bytes([r.randrange(256)]))]
                regs = lambda: dict({n: r.getrandbits(32) for n in SENTINELAS}, EFLAGS=2 | (r.getrandbits(12) & 0xcd5))
                passos = [(r.choice(('ProgIteration_counter_prefix', 'GameNextFrame', 'CalculGame_cd_permutation_draw',
                                     'ProgIteration_counter_prefix')), regs(), None) for _ in range(10)]
                passos.append(('CalculGame_load_counter_reset', regs(), None))
                self.caso(sobrescritas, passos)


if __name__ == '__main__':
    unittest.main()
