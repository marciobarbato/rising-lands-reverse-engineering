"""Consumer ABI: no omitted/uncertain recruitment argument becomes an invented zero."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ambiente_ia_runtime  # noqa: F401
from entrada_estruturas import ArgumentoNaoPassado
from provedores_entrada_ia import DonosM3
from recrutamento_core import ARGUMENTOS, ROTINAS, REG7


class SemAcesso:
    def __getattr__(self, nome):
        raise AssertionError(f'Unexpected memory access: {nome}')


class Contrato(unittest.TestCase):
    def test_argumentos_ausentes_ou_incertos_param_antes_de_acessar_memoria(self):
        d = DonosM3(SemAcesso(), som=None)
        for nome, argumentos in ARGUMENTOS.items():
            for k, mask in argumentos.items():
                for entrada in ({r:0 for r in argumentos if r != k},
                                dict({r:0 for r in argumentos}, _incertos={k: mask & -mask})):
                    with self.subTest(nome=nome, register=k, entrada=entrada):
                        with self.assertRaises(ArgumentoNaoPassado) as e:
                            d.externo(nome, 0x420f8c, entrada)
                        self.assertEqual(e.exception.registradores, (k,))
                        self.assertEqual(e.exception.chamada, 0x420f8c)
        self.assertEqual(d.nomes_recrutamento, frozenset(ROTINAS))

    def test_registros_preservados_e_mascaras_na_rota_real(self):
        from memoria_quadro_core import MemoriaQuadro
        u = 0x3000000
        records, globals_ = bytearray(276), bytearray(4)
        m = MemoriaQuadro([(u,records),(0x4e19a0,globals_)])
        m.u32(0x4e19a0,u)
        m.u16(u+0x74,123)
        m.u16(u+0x76,456)
        d = DonosM3(m,som=None)
        out = d.externo('EnginResetFatigue',0x420f7c,dict(EAX=0,EDX=0x12345678, _incertos={'EDX':0xffff0000}))
        self.assertEqual(set(out) - {'_incertos'}, set(REG7))
        self.assertEqual((out['EAX'],out['EDX']), (u,0x12345678))
        self.assertEqual(out['_incertos']['EDX'],0xffff0000)
        self.assertEqual((m.u16(u+0x74),m.u16(u+4)),(0,456))
        self.assertEqual(out['_incertos']['EBX'],0xffffffff)


if __name__ == '__main__':
    unittest.main()
