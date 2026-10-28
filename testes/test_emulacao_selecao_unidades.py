"""Whole original selection allocation/unit-pool comparisons."""
import os
import random
import unittest

from test_selecao_unidades import MundoUnidades,inicializar_selecoes_unidades


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1','Optional x86: RISING_EMULAR=1')
class DiferencialSelecaoUnidades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from emulador import BancadaX86
        cls.bancada = BancadaX86()

    def comparar(self,dados,unidades):
        from emulador import UNIDADES
        b=self.bancada
        b.cpu.mem_write(0x508728,bytes(dados))
        b.cpu.mem_write(UNIDADES,bytes(unidades))
        regs=b.executar(0x472555,((0x472555,0x472576),),dict(EAX=0xdeadbeef,EDX=0xabcdef12))
        inicializar_selecoes_unidades(dados)
        self.assertEqual(bytes(b.cpu.mem_read(0x508728,2048)),bytes(dados))
        self.assertEqual(bytes(b.cpu.mem_read(UNIDADES,220800)),bytes(unidades))
        self.assertEqual((regs['EAX'],regs['EDX']),(0xdeadbeef,0xabcdef12))

    def test_every_count_low_byte_and_arbitrary_preserved_list_contents(self):
        rng=random.Random(0x472555)
        unidades=bytes(rng.randrange(256) for _ in range(220800))
        for valor in range(256):
            dados=bytearray((i*31+valor) & 255 for i in range(2048))
            self.comparar(dados,unidades)

    def test_full_word_counts_and_live_selected_flags_are_unconsulted(self):
        m=MundoUnidades()
        for valor in (0,1,255,256,799,65535):
            m.unidades[:]=bytes([valor & 255])*220800
            dados=bytearray(b'\xa5'*2048)
            for offset in (0,512,1024,1536):
                dados[offset:offset+2]=valor.to_bytes(2,'little')
            self.comparar(dados,m.unidades)
