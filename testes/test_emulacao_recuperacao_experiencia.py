"""Fresh intact native Engin_RetrieveExperimente vs Python differential."""
import os
import random
import unittest

from test_recuperacao_experiencia import captura, PRESERVADOS
from recuperacao_experiencia import recuperar_experiencias, RetornoRecuperacaoExperiencia


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialRecuperacaoExperiencia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_recuperacao_experiencia import BancadaRecuperacaoExperiencia
        cls.bancada = BancadaRecuperacaoExperiencia()
        cls.comparacoes = 0

    def comparar(self, atual, guardada, vizinhanca, regs, produtor=None):
        from bancada_recuperacao_experiencia import ATUAL, GUARDADA, FIM, VIZINHANCA
        b = self.bancada
        b.carregar(atual, guardada, vizinhanca)
        if produtor == 'reset':
            b.resetar({n: v for n, v in regs.items() if n != 'EFLAGS'})
        elif produtor is not None:
            b.carregar_unidades(produtor)
            b.armazenar({n: v for n, v in regs.items() if n != 'EFLAGS'})
        atuais = bytearray(b.ler(ATUAL, GUARDADA))
        guardadas = b.ler(GUARDADA, FIM)
        viz_antes = b.ler(*VIZINHANCA)
        antes = bytes(atuais)
        seg = b.recuperar(regs)
        r = recuperar_experiencias(atuais, guardadas)
        self.assertEqual(b.ler(ATUAL, GUARDADA), bytes(atuais))
        self.assertEqual(b.ler(GUARDADA, FIM), guardadas)
        o = ATUAL-VIZINHANCA[0]
        viz = b.ler(*VIZINHANCA)
        self.assertEqual(viz[:o]+viz[o+40:], viz_antes[:o]+viz_antes[o+40:])
        self.assertEqual(seg['image_changes'],
                         [(ATUAL+i, antes[i], atuais[i]) for i in range(40) if antes[i] != atuais[i]])
        self.assertEqual([w for w in seg['writes'] if w[0] < 0x2000000],
                         [(ATUAL+2*i, 2, guardadas[2*i] | guardadas[2*i+1] << 8) for i in range(20)])
        out = seg['registers']
        self.assertEqual(out['EAX'], r.eax)
        self.assertEqual(out['EFLAGS'], RetornoRecuperacaoExperiencia.eflags(regs.get('EFLAGS', 2)))
        self.assertEqual((out['ESP'], out['EIP']), (0x2008004, 0x3000000))
        for nome in PRESERVADOS:
            self.assertEqual(out[nome], regs.get(nome, 0) & 0xffffffff, nome)
        self.assertEqual([w[2] for w in seg['stack_writes']], [regs.get(n, 0) for n in ('EBX', 'ECX', 'EDX', 'ESI')])
        self.assertEqual(seg['instructions'], 152)
        type(self).comparacoes += 1
        return guardadas

    def test_all_captured_inputs_fresh(self):
        from capturar_recuperacao_experiencia import casos, _vizinhanca, pool_store
        definidos = {x[0]: x for x in casos()}
        for c in captura()['cases']:
            with self.subTest(c['name']):
                _, tipo, atual, guardada, semente, _, _ = definidos[c['name']]
                regs = {k: int(v, 16) for k, v in c['registers_in'].items()}
                produtor = dict(reset_then_retrieve='reset', store_then_retrieve=pool_store()).get(tipo)
                if produtor is None:
                    self.assertEqual((atual.hex(), guardada.hex()), (c['before']['current'], c['before']['saved']))
                produzida = self.comparar(atual, guardada, _vizinhanca(semente), regs, produtor)
                self.assertEqual(produzida.hex(), c['before']['saved'])

    def test_fresh_random_queues_registers_and_flags(self):
        r = random.Random(0xf2e5)
        for i in range(32):
            with self.subTest(i):
                regs = {n: r.getrandbits(32) for n in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')}
                regs['EFLAGS'] = 2 | (r.getrandbits(12) & 0xcd5)
                self.comparar(r.randbytes(40), r.randbytes(40), r.randbytes(0x9c), regs)

    def test_fresh_single_word_differences_at_every_position(self):
        r = random.Random(0x0dd)
        for palavra in range(20):
            with self.subTest(palavra):
                atual = r.randbytes(40)
                guardada = bytearray(atual)
                guardada[2*palavra] ^= 0xa5
                guardada[2*palavra+1] ^= 0x3c
                self.comparar(atual, bytes(guardada), r.randbytes(0x9c), dict(EAX=palavra, EFLAGS=0x402))

    def test_fresh_original_producer_chains(self):
        from capturar_recuperacao_experiencia import pool_store
        r = random.Random(0xc4a1)
        self.comparar(r.randbytes(40), r.randbytes(40), r.randbytes(0x9c), dict(EBX=7, EFLAGS=0x2), 'reset')
        self.comparar(r.randbytes(40), r.randbytes(40), r.randbytes(0x9c), dict(ESI=9, EFLAGS=0x8d7),
                      pool_store(0xbeef))


if __name__ == '__main__':
    unittest.main()
