"""CPU-free Stage12 registry guards; no whole-load oracle validation claim."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from estado_herdado_missao import BlocoHerdadoMissao,EstadoHerdadoMissao,DATA_BASE,DATA_SIZE


class EstadoHerdadoMissaoTest(unittest.TestCase):
    def block(self):
        return BlocoHerdadoMissao('data',DATA_BASE,bytearray(DATA_SIZE),
                                 'Explicit structural test bytes; not a game-state fixture')

    def test_live_views_keep_one_backing_without_copy_or_default_pool(self):
        block=self.block()
        state=EstadoHerdadoMissao('test-source','Registry unit test',(block,))
        view=state.vista(0x496fe4,1)
        view[0]=1
        self.assertEqual(block.dados[0x496fe4-DATA_BASE],1)
        self.assertIs(view.obj,block.dados)
        before=bytes(block.dados)
        with self.assertRaises(ValueError):
            state.validar_fechamento_m1()
        self.assertEqual(bytes(block.dados),before)
        for address,size in ((DATA_BASE,-1),(-1,1),(0x1000000,80)):
            with self.assertRaises(ValueError):
                state.vista(address,size)

    def test_overlapping_backings_are_rejected_instead_of_silently_rebound(self):
        block=self.block()
        overlap=BlocoHerdadoMissao('alias',DATA_BASE+1,bytearray(16),'Explicit invalid overlap')
        with self.assertRaises(ValueError):
            EstadoHerdadoMissao('test-source','Invalid independent alias',(block,overlap))
        with self.assertRaises(ValueError):
            EstadoHerdadoMissao('test-source','Duplicate block ID',(block,replace(overlap,nome='data')))


if __name__=='__main__':
    unittest.main()
