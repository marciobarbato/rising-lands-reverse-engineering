"""M2.3 movement additions without a CPU: the walk animation, CalculNextCase's guards and the small flat routines."""
from pathlib import Path
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
sys.path.insert(0, str(RAIZ / 'testes'))


class AnimacaoMovimento(unittest.TestCase):
    def mundo(self, tipo, a9, a7, a4, a5):
        from navegacao_unidades import MundoNavegacao
        w = MundoNavegacao(64, 64)
        u = w.unidades
        u[1], u[0xa9], u[0xa7], u[0xa4], u[0xa5] = tipo, a9, a7, a4, a5
        return w

    def test_tick_reaching_the_period_advances_the_frame_modulo_count(self):
        w = self.mundo(0, 1, 2, 5, 6)
        w.animar_movimento(0)
        self.assertEqual((w.unidades[0xa9], w.unidades[0xa4]), (0, 0))
        w = self.mundo(0, 0, 2, 3, 6)
        w.animar_movimento(0)
        self.assertEqual((w.unidades[0xa9], w.unidades[0xa4]), (1, 3))

    def test_type_16_and_unknown_types_do_not_animate_type_17_is_a_dependency(self):
        for tipo in (16, 26, 255):
            w = self.mundo(tipo, 1, 2, 5, 6)
            w.animar_movimento(0)
            self.assertEqual((w.unidades[0xa9], w.unidades[0xa4]), (1, 5))
        with self.assertRaises(NotImplementedError):
            self.mundo(17, 1, 2, 5, 6).animar_movimento(0)

    def test_zero_frame_count_is_the_original_divide_fault(self):
        with self.assertRaises(ValueError):
            self.mundo(0, 1, 2, 5, 0).animar_movimento(0)

    def test_default_movement_keeps_the_declared_exclusion(self):
        import inspect
        from navegacao_unidades import MundoNavegacao
        self.assertIs(inspect.signature(MundoNavegacao.atualizar_movimento).parameters['animacao'].default, False)


class RotinasPlanas(unittest.TestCase):
    def memoria(self, atributo):
        from test_chamadas_quadro_core import MemoriaEsparsa
        base = 0x41000000
        bytes_ = {0x507da8 + i: (base >> 8 * i) & 0xff for i in range(4)}
        bytes_[base + 0x3d3d] = atributo
        return MemoriaEsparsa(bytes_)

    def test_terrain_collision_and_reset(self):
        from incursao_core import remover_colisao, terreno_em_colisao
        m = self.memoria(0x03)
        self.assertEqual(terreno_em_colisao(m, 0xabcd3d3d, 0x102), dict(EAX=1))
        self.assertEqual(terreno_em_colisao(m, 0x3d3d, 4), dict(EAX=0))
        self.assertEqual(remover_colisao(m, 0xabcd3d3d, 0x101), dict(EAX=0x3d3d, EDX=0x1fe))
        self.assertEqual(m.u8(0x41003d3d), 0x02)

    def test_memset_reads_the_first_byte_and_returns_the_pattern(self):
        from incursao_core import memset_crt
        from test_chamadas_quadro_core import MemoriaEsparsa
        m = MemoriaEsparsa({0x1000: 9})
        self.assertEqual(memset_crt(m, 0x1000, 0x12345678, 3), dict(EDX=0x78787878))
        self.assertEqual([m.u8(0x1000 + i) for i in range(3)], [0x78] * 3)
        self.assertEqual(memset_crt(MemoriaEsparsa({}), 0x2000, 1, 0), dict(EDX=0x01010101))


if __name__ == '__main__':
    unittest.main()


CAPTURA_MOVIMENTO = RAIZ / 'evidencias/fundacoes-quadro/captura-movimento-incursao-v1.json'


@unittest.skipUnless(CAPTURA_MOVIMENTO.exists(), 'Movement capture not committed')
class ReplayMovimento(unittest.TestCase):
    """Every isolated call of a routine with a flat translation replays exactly from its read-before-write bytes."""
    def test_flat_routines_replay_exactly(self):
        import json
        from compactar_captura_isolada import expandir
        from incursao_core import traducao_core
        from test_chamadas_quadro_core import MemoriaEsparsa, regs, sub_chemin
        registros = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
        vistos = {}
        for c in json.loads(CAPTURA_MOVIMENTO.read_bytes())['calls']:
            traduzir = traducao_core(c['routine'])
            if traduzir is None:
                continue
            c = expandir(c)
            with self.subTest(routine=c['routine'], frame=c['frame'], entry=c['entry_registers']['EAX']):
                m = MemoriaEsparsa({int(a, 16): v for a, v, _ in c['read_before_write']}, 0)
                entrada = regs(c['entry_registers'])
                pilha = [sub_chemin(m, entrada)] if c['routine'] == 'Chemin_ModifieZone' else []
                saida = dict(entrada, **traduzir(m, entrada, pilha, None))
                nativo = regs(c['exit_registers'])
                self.assertEqual({k: hex(saida[k] & 0xffffffff) for k in registros},
                                 {k: hex(nativo[k]) for k in registros})
                m.conferir(self, c['changed_bytes'])
                vistos[c['routine']] = vistos.get(c['routine'], 0) + 1
        self.assertEqual(set(vistos), {'SetEnginCollision', 'SetCollision', 'Chemin_ModifieZone', 'TerrainEnCollision',
                                       'ResetCollision', 'memset'})
