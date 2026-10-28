"""SelectionInit raw-list and live-world retention contract."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'ferramentas'))
from selecao_unidades import inicializar_selecoes_unidades
from ordens_unidades import MundoUnidades


class SelecaoUnidades(unittest.TestCase):
    def test_only_four_count_words_are_cleared(self):
        dados = bytearray((i*53+19) & 255 for i in range(2048))
        antes = bytearray(dados)
        self.assertIsNone(inicializar_selecoes_unidades(dados))
        for offset in (0,512,1024,1536):
            antes[offset:offset+2] = bytes(2)
        self.assertEqual(dados,antes)

    def test_world_method_preserves_every_unit_and_other_shared_buffer(self):
        m = MundoUnidades()
        m.unidades[:] = b'\xa5'*220800
        m.selecoes_unidades[:] = b'\xff'*2048
        unidades,estruturas,grupos = bytes(m.unidades),bytes(m.estruturas),bytes(m.grupos)
        m.inicializar_selecoes_unidades()
        self.assertEqual((bytes(m.unidades),bytes(m.estruturas),bytes(m.grupos)),(unidades,estruturas,grupos))
        self.assertTrue(all(m.unidades[i*276+0xbd] == 0xa5 for i in range(800)))
        self.assertEqual(m.selecoes_unidades[2:512],b'\xff'*510)

    def test_malformed_and_readonly_buffers_are_protected_before_store(self):
        for dados in (bytes(2048),bytearray(2047),bytearray(2049),[1]*2048):
            antes = dados[:]
            with self.assertRaises(ValueError):
                inicializar_selecoes_unidades(dados)
            self.assertEqual(dados,antes)
