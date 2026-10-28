"""Fresh unpatched DecouvreTerrain/IllumineTerrain/SetMiniMap beyond vision sum 8."""
import os
import unittest

from test_descoberta_terreno import preparar, executar_python
from colocacao_missao import DependenciaColocacaoMissao
from colocacao_saida import DependenciaColocacaoSaida
from insercao_unidades import (SOMA_VISAO_MAXIMA_INSERCAO, RAIO_DESCOBERTA_MAXIMO_VALIDADO,
                               RAIO_LUZ_MAXIMO_VALIDADO)

PADROES = ('fresh', 'mixed', 'saturated')
GEOMETRIAS = ((1, 1), (1, 256), (256, 1), (3, 5), (16, 16), (32, 16), (64, 64), (128, 64), (256, 256))


def bordas(largura, altura):
    xs, ys = (0, largura//2, largura-1), (0, altura//2, altura-1)
    return sorted({y*256+x for x in xs for y in ys})


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialDescobertaTerreno(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_descoberta_terreno import BancadaDescobertaTerreno
        cls.bancada = BancadaDescobertaTerreno()

    def comparar(self, m, entrada, celula, raio=0, dono=0, parada=None):
        from emulador import RETORNO
        b = self.bancada
        b.carregar_saida(m)
        if entrada == 'mission':
            regs = b.colocar_missao(7, **({'parada': parada} if parada else {}))
        elif entrada == 'exit':
            regs = b.colocar(7, celula, **({'parada': parada} if parada else {}))
        elif entrada == 'discover':
            regs = b.descobrir(celula, raio, dono)
        else:
            regs = b.iluminar(celula, raio, dono)
        self.assertEqual(regs['EIP'], parada or RETORNO)
        if parada:
            erro = DependenciaColocacaoMissao if entrada == 'mission' else DependenciaColocacaoSaida
            with self.assertRaises(erro) as captura:
                executar_python(m, entrada, celula, raio, dono)
            self.assertEqual(captura.exception.checkpoint, parada)
        else:
            executar_python(m, entrada, celula, raio, dono)
        self.assertEqual(b.conferir_saida(m), [])
        self.assertEqual(b.efeitos, m.efeitos)
        self.assertEqual(b.celulas, m.celulas)

    def test_new_sums_both_callers_every_normal_owner_and_camera(self):
        # 64x64 keeps every circle inside the map; 16x16 and the edges are in the next test.
        for entrada, celula in (('mission', 0x2020), ('exit', 0x1f21)):
            for bb, f5 in ((9, 0), (8, 1), (10, 0), (9, 1), (11, 0), (10, 1), (0, 11), (5, 6)):
                for dono in range(4):
                    for camera in range(4):
                        m = preparar(entrada, 64, 64, celula, bb, f5, dono, camera, PADROES[(dono+camera) % 3])
                        self.comparar(m, entrada, celula)

    def test_new_sums_at_map_edges_corners_and_extreme_dimensions(self):
        n = 0
        for largura, altura in GEOMETRIAS:
            for celula in bordas(largura, altura):
                for bb, f5 in ((9, 0), (10, 0), (10, 1)):
                    entrada = ('mission', 'exit')[n % 2]
                    dono, camera = n % 4, (n//4) % 4
                    m = preparar(entrada, largura, altura, celula, bb, f5, dono, camera, PADROES[n % 3])
                    self.comparar(m, entrada, celula)
                    n += 1

    def test_direct_discovery_and_light_radii_through_published_maxima(self):
        posicoes = ((256, 256, 0x8080), (256, 256, 0), (256, 256, 0xffff), (32, 32, 0x1010), (64, 64, 0x2000))
        n = 0
        for entrada, maximo in (('discover', RAIO_DESCOBERTA_MAXIMO_VALIDADO), ('light', RAIO_LUZ_MAXIMO_VALIDADO)):
            for raio in range(maximo+1):
                for largura, altura, celula in posicoes:
                    for dono in range(4):
                        camera = (dono, (dono+1) % 4)[n % 2]
                        m = preparar(entrada, largura, altura, celula, 0, 0, dono, camera, PADROES[n % 3])
                        self.comparar(m, entrada, celula, raio, dono)
                        n += 1

    def test_regression_sums_0_to_8_every_owner_both_callers(self):
        for soma in range(9):
            for dono in range(4):
                for entrada, celula in (('mission', 0x505), ('exit', 0x808)):
                    m = preparar(entrada, celula=celula, bb=soma - (soma > 4), f5=int(soma > 4), dono=dono,
                                 camera=(dono+2) % 4, luz=PADROES[(soma+dono) % 3])
                    self.comparar(m, entrada, celula)

    def test_sums_above_domain_stop_at_each_original_caller(self):
        acima = SOMA_VISAO_MAXIMA_INSERCAO+1
        for indice_bb, f5 in ((acima, 0), (acima-1, 1), (0, acima), (6, 6), (255, 255)):
            for entrada, celula, parada in (('mission', 0x505, 0x457019), ('exit', 0x808, 0x446146)):
                m = preparar(entrada, celula=celula, bb=indice_bb, f5=f5, dono=f5 % 4, luz='mixed')
                self.comparar(m, entrada, celula, parada=parada)

    def test_owners_4_and_200_complete_without_discovery_at_any_sum(self):
        for entrada, celula in (('mission', 0x505), ('exit', 0x808)):
            for dono in (4, 200):
                for bb, f5 in ((255, 255), (SOMA_VISAO_MAXIMA_INSERCAO+1, 0), (10, 1)):
                    self.comparar(preparar(entrada, celula=celula, bb=bb, f5=f5, dono=dono), entrada, celula)


if __name__ == '__main__':
    unittest.main()
