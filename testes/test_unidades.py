import struct
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from unidades import recompor_memoria, interpretar_unidade, atributos_apos_carga, curar_com_limite
from regras import reconstruir_tipo, ler_ini
from formatos import ler_eta

CD = RAIZ.parent / 'source/cd'


class Instancias(unittest.TestCase):
    def test_remocao_do_intervalo_de_512_bytes(self):
        memoria = bytearray(272)
        memoria[:3] = bytes([3, 8, 7])
        struct.pack_into('<H', memoria, 8, 0x1209)
        struct.pack_into('<H', memoria, 0x9a, 20)
        struct.pack_into('<H', memoria, 0x102, 1234)
        bruto = memoria[:140] + bytes([0xfe]) * 512 + memoria[140:]
        self.assertEqual(recompor_memoria(bruto), memoria)
        unidade = interpretar_unidade(799, bruto)
        self.assertEqual(unidade['posicao'], {'x': 9, 'y': 18})
        self.assertEqual((unidade['vida_no_arquivo'], unidade['recarga_no_arquivo']), (20, 1234))
        self.assertEqual((unidade['proprietario_id'], unidade['tipo']), (3, 8))

    def test_indices_e_tamanho_invalidos(self):
        for indice, bruto in [(-1, bytes(784)), (800, bytes(784)), (0, bytes(783)), (0, bytes(785))]:
            with self.subTest(indice=indice, tamanho=len(bruto)), self.assertRaises(ValueError):
                interpretar_unidade(indice, bruto)

    def test_carga_sobrescreve_vida_e_trunca_alcance(self):
        bruto = bytearray(784)
        bruto[:3] = bytes([2, 16, 7])
        struct.pack_into('<H', bruto, 0x9a + 512, 20)
        unidade = interpretar_unidade(1, bruto)
        tipo = reconstruir_tipo('TESTE', ler_ini(b'[TESTE]\nPORTEE=20\nRAYON=257\n'), bytes(50))
        carregada = atributos_apos_carga(unidade, tipo)
        self.assertEqual(carregada, dict(proprietario_id=0, vida=100, raio_visao=1,
                                        alcance_quadrado_u8=144, recarga=100, grupo=255))
        unidade['tipo'] = 20
        self.assertEqual(atributos_apos_carga(unidade, tipo)['proprietario_id'], 4)
        unidade['ativa_no_predicado_441fff'] = False
        self.assertEqual(atributos_apos_carga(unidade, tipo)['vida'], 20)

    def test_maximo_preservado_da_tabela_original(self):
        registro = bytearray(50)
        struct.pack_into('<H', registro, 8, 125)
        self.assertEqual(reconstruir_tipo('TESTE', ler_ini(b'[TESTE]\n'), registro)['vida_maxima'], 125)

    def test_cura_limite_estrito_e_overflow_x86(self):
        self.assertEqual(curar_com_limite(80, 19, 100), (99, False))
        self.assertEqual(curar_com_limite(80, 20, 100), (100, False))
        self.assertEqual(curar_com_limite(80, 21, 100), (100, True))
        self.assertEqual(curar_com_limite(65535, 1, 100), (0, False))


@unittest.skipUnless((CD / 'WORLD/MONDE01.ETA').exists(), 'CD local não disponível')
class InstanciasDoCorpus(unittest.TestCase):
    def test_todas_as_posicoes_cabem_no_mapa(self):
        quantidade = 0
        feridas = []
        for arquivo in sorted((CD / 'WORLD').glob('*.ETA')):
            mapa = ler_eta(arquivo.read_bytes())
            for unidade in mapa['unidades']:
                quantidade += 1
                with self.subTest(mapa=arquivo.name, unidade=unidade['indice']):
                    self.assertLess(unidade['posicao']['x'], mapa['largura'])
                    self.assertLess(unidade['posicao']['y'], mapa['altura'])
                    self.assertIn(unidade['byte_estado'], (7, 14))
                    self.assertIn(unidade['proprietario_id'], (0, 1, 2, 3, 4, 200))
                if unidade['vida_no_arquivo'] != 100:
                    feridas.append(unidade['vida_no_arquivo'])
        self.assertEqual(quantidade, 2604)
        self.assertEqual(feridas, [20] * 4)

    def test_soldados_e_colonos_da_primeira_missao(self):
        unidades = ler_eta((CD / 'WORLD/MONDE01.ETA').read_bytes())['unidades']
        soldados = [(u['indice'], u['posicao']['x'], u['posicao']['y']) for u in unidades if u['tipo'] == 0]
        self.assertEqual(soldados, [(0, 7, 15), (1, 9, 16), (2, 8, 18)])
        for unidade in unidades:
            self.assertEqual(unidade['proprietario_id'], 0)
            if unidade['tipo'] == 9:
                self.assertEqual(unidade['posicao'], dict(x=14, y=12))
                self.assertEqual(unidade['byte_estado'], 14)


if __name__ == '__main__':
    unittest.main()
