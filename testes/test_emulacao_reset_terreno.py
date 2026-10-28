"""Fresh unpatched TerrainReset, MiniMapReset and BatimentModifyMap comparisons."""
import os
import unittest

from test_reset_terreno import preparar, executar, aplicar_vistas

POSICOES = ((16, 16, 0x0000), (16, 16, 0x0e0d), (64, 64, 0x0b0c), (256, 256, 0x00fe), (256, 256, 0xfe00),
            (256, 256, 0xfffd))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialResetTerreno(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_reset_terreno import BancadaResetTerreno
        cls.bancada = BancadaResetTerreno()

    def comparar(self, entrada, estrutura=None, ativo=1, formato=None, **opcoes):
        from emulador import RETORNO
        m, minas, aleatorio = preparar(entrada, estrutura=estrutura, ativo=ativo, **opcoes)
        if formato is not None:
            minas, aleatorio = aplicar_vistas(m, minas, aleatorio, formato)
        b = self.bancada
        b.carregar_reset(m, minas, aleatorio)
        if entrada == 'terrain':
            regs = b.resetar_terreno()
        elif entrada == 'minimap':
            regs = b.resetar_minimapa()
        else:
            regs = b.modificar_minimapa_estrutura(estrutura[0] | 0xabcd0000, ativo)
        self.assertEqual(regs['EIP'], RETORNO)
        executar(m, minas, aleatorio, entrada, estrutura, ativo)
        self.assertEqual(b.conferir_reset(m, minas, aleatorio), [])
        self.assertEqual(b.efeitos, m.efeitos)
        if entrada == 'terrain':
            self.assertEqual(b.chamadas_aleatorio, 65536)
        elif entrada == 'minimap':
            n = m.tamanho_minimapa[0]*m.tamanho_minimapa[1]
            self.assertEqual(b.memsets, [('mini_final', 2, n), ('mini_unidades', 0, n), ('mini_estruturas', 0, n)])

    def test_terrain_reset_random_state_edges_and_patterns(self):
        for n, semente in enumerate((0, 1, 2, 127772, 127773, 0x7ffffffe, 0x7fffffff, 0x80000000,
                                      0xfffffffe, 0xffffffff, 0x12345678)):
            self.comparar('terrain', semente=semente, padrao=20+n, largura=(16, 64, 256)[n % 3],
                          altura=(16, 64, 256)[n % 3])

    def test_live_unsigned_and_signed_byte_views(self):
        for entrada in ('terrain', 'minimap'):
            for formato in ('B', 'b'):
                self.comparar(entrada, formato=formato)

    def test_minimap_reset_dimensions_including_empty_and_full_layers(self):
        for n, minimapa in enumerate(((128, 128), (64, 32), (1, 1), (0, 0), (0, 128), (128, 0), (256, 256),
                                      (128, 512), (65535, 1), (3, 7))):
            self.comparar('minimap', minimapa=minimapa, padrao=40+n)

    def test_structure_every_type_both_variants_at_corners_and_edges(self):
        n = 0
        for tipo in range(22):
            for largura, altura, origem in POSICOES:
                for ativo in (1, 0, 0x80):
                    self.comparar('structure', (n % 1000, origem, (0, 1, 2, 3, 4, 200)[n % 6], tipo), ativo,
                                  largura=largura, altura=altura, camera=n % 4, padrao=60+n % 7,
                                  visibilidade=(None, 'lit', 'discovered', 'hidden')[n % 4],
                                  unidades_minimapa=(None, 0, 1)[n % 3])
                    n += 1

    def test_structure_owner_camera_visibility_matrix(self):
        n = 0
        for dono in (0, 1, 2, 3, 4, 31, 200):
            for camera in range(4):
                for visibilidade in ('lit', 'discovered', 'hidden'):
                    for unidades in (0, 1):
                        for ativo in (1, 0):
                            self.comparar('structure', (7, 0x0b0c, dono, 2), ativo, camera=camera,
                                          visibilidade=visibilidade, unidades_minimapa=unidades, padrao=n)
                            n += 1

    def test_monde01_dimensions_sanctuary_record(self):
        from formatos import ler_eta
        from analisar import RAIZ
        meta = ler_eta((RAIZ.parent/'source/cd/WORLD/MONDE01.ETA').read_bytes())
        for ativo in (1, 0):
            self.comparar('structure', (0, 0x0b0c, 0, 2), ativo, largura=meta['largura'], altura=meta['altura'],
                          visibilidade='lit', unidades_minimapa=0)


if __name__ == '__main__':
    unittest.main()
