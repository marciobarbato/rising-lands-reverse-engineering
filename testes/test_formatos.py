import struct
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from formatos import ErroFormato, ler_cmp, ler_eta, ler_paleta
from regras import ler_ini, reconstruir_tipo, ler_danos

CD = RAIZ.parent / 'source/cd'


class ComandosCMP(unittest.TestCase):
    def montar(self, largura, altura, comandos):
        return struct.pack('<HHHI', 1, largura, altura, len(comandos)) + comandos

    def test_mistura_transparencia_e_literais(self):
        quadro, = ler_cmp(self.montar(4, 2, bytes([2, 253, 9, 8, 7, 3])))
        self.assertEqual(quadro.pixels, bytes([0, 0, 9, 8, 7, 0, 0, 0]))

    def test_literais_extremos_e_comando_zero(self):
        quadro, = ler_cmp(self.montar(127, 1, bytes([0, 129]) + bytes(range(127))))
        self.assertEqual(quadro.pixels, bytes(range(127)))

    def test_nao_presume_semantica_do_comando_0x80(self):
        with self.assertRaises(ErroFormato):
            ler_cmp(self.montar(128, 1, bytes([128]) + bytes(range(128))))

    def test_rejeita_truncamento_excesso_e_dimensao_zero(self):
        casos = [b'', b'\x01', self.montar(0, 4, b''),
                 self.montar(2, 2, bytes([5])), self.montar(2, 2, bytes([3])),
                 self.montar(2, 2, bytes([255])),
                 self.montar(2, 2, bytes([4])) + b'\0']
        for dados in casos:
            with self.subTest(dados=dados), self.assertRaises(ErroFormato):
                ler_cmp(dados)

    def test_paleta_truncada(self):
        for dados in (b'', b'Pie', b'Pie\0\0\0\0\0\x01'):
            with self.assertRaises(ErroFormato):
                ler_paleta(dados)


class Atributos(unittest.TestCase):
    def test_alcance_quadratico_e_truncamento_de_registradores(self):
        ini = ler_ini(b'[TESTE]\nPORTEE=300\nBLINDAGE=257\nTMPSRECRUTE=65537\n')
        tipo = reconstruir_tipo('TESTE', ini, bytes(50))
        memoria = bytes.fromhex(tipo['registro_memoria_hex'])
        self.assertEqual(struct.unpack_from('<H', memoria, 0x2c)[0], 24464)
        self.assertEqual(memoria[0x0b], 1)
        self.assertEqual(struct.unpack_from('<H', memoria)[0], 1)

    def test_valores_padrao_da_api(self):
        tipo = reconstruir_tipo('TESTE', ler_ini(b'[TESTE]\n'), bytes(50))
        self.assertEqual((tipo['tempo_recrutamento'], tipo['fadiga'], tipo['recarga']), (120, 3000, 100))
        self.assertEqual((tipo['blindagem'], tipo['raio_visao'], tipo['alcance_ataque']), (5, 5, 1))

    def test_cp1252_e_tamanho_nome(self):
        nome = 'Á' * 40
        ini = ler_ini(('[TESTE]\nNAME=' + nome).encode('cp1252'))
        memoria = bytes.fromhex(reconstruir_tipo('TESTE', ini, bytes(50))['registro_memoria_hex'])
        self.assertEqual(memoria[12:42], b'\xc1' * 29 + b'\0')

    def test_rejeita_matriz_de_dano_incompleta(self):
        with self.assertRaises(ValueError):
            ler_danos(ler_ini(b'[TESTE]\nDEGAT=1,2,3\n'), 'TESTE')


@unittest.skipUnless((CD / 'WORLD/MONDE01.ETA').exists(), 'CD local não disponível')
class CorpusOriginal(unittest.TestCase):
    def test_38_mapas_fecham_no_mesmo_sufixo(self):
        arquivos = sorted((CD / 'WORLD').glob('*.ETA'))
        self.assertEqual(len(arquivos), 38)
        for arquivo in arquivos:
            with self.subTest(mapa=arquivo.name):
                dados = arquivo.read_bytes()
                mapa = ler_eta(dados)
                self.assertEqual(mapa['fim_carregamento'] + 917504, len(dados))
                self.assertEqual(len(mapa['terreno']), mapa['largura'] * mapa['altura'])
                self.assertTrue(all(1 <= t <= 1345 for t in mapa['terreno']))
                self.assertTrue(all(u['tipo'] < 26 for u in mapa['unidades']))
                indices = [u['indice'] for u in mapa['unidades']]
                self.assertEqual(len(indices), len(set(indices)))
                self.assertTrue(all(0 <= indice < 800 for indice in indices))
                self.assertTrue(all(u['tamanho_memoria_serializada'] == 272 for u in mapa['unidades']))

    def test_primeira_missao_tem_16_unidades_e_origem_da_camera(self):
        mapa = ler_eta((CD / 'WORLD/MONDE01.ETA').read_bytes())
        self.assertEqual((mapa['largura'], mapa['altura']), (64, 64))
        self.assertEqual(mapa['origens_visualizacao'], [[4, 6], [39, 47], [0, 0], [0, 0]])
        self.assertEqual(len(mapa['unidades']), 16)
        self.assertEqual(sum(u['tipo'] == 0 for u in mapa['unidades']), 3)
        self.assertEqual(sum(u['tipo'] == 9 for u in mapa['unidades']), 8)
        self.assertEqual(mapa['fim_carregamento'], 0x539c8)

    def test_eta_rejeita_truncamento_e_versao(self):
        dados = (CD / 'WORLD/MONDE01.ETA').read_bytes()
        for alterado in (b'', b'V0.2' + dados[4:], dados[:0x50031], dados[:-1]):
            with self.assertRaises(ErroFormato):
                ler_eta(alterado)

    def test_oito_cmp_expandem_inteiros(self):
        esperados = {'BLOCS': 1345, 'TROOPS': 2848, 'BUILDING': 611, 'CREATURE': 1920,
                     'INVENTE': 72, 'MENU': 40, 'OTHERS': 4517, 'VEHICULE': 915}
        for nome, quantidade in esperados.items():
            with self.subTest(nome=nome):
                quadros = ler_cmp((CD / f'INSTALHD/GRAPHICS/{nome}.CMP').read_bytes())
                self.assertEqual(len(quadros), quantidade)

    def test_paleta_comparada_com_outro_formato(self):
        jogo = CD / 'INSTALHD'
        paleta = ler_paleta((jogo / 'PLATGAME.PIE').read_bytes())
        referencia = (jogo / 'CHARGE.LZS').read_bytes()[12:780]
        self.assertEqual(paleta[48:765], referencia[48:765])

    def test_valores_reais_soldado_capitao(self):
        ini = ler_ini((CD / 'INSTALHD/RISING.INI').read_bytes())
        soldado = reconstruir_tipo('SOLDAT', ini, bytes(50))
        capitao = reconstruir_tipo('CAPITAINE', ini, bytes(50))
        self.assertEqual((soldado['nome'], soldado['custo_comida'], soldado['tempo_recrutamento']),
                         ('SOLDADO', 6, 800))
        self.assertEqual(capitao['alcance_ataque_quadrado_u16'], 64)
        self.assertEqual(ler_danos(ini, 'SOLDAT')[0], 20)
        self.assertEqual(ler_danos(ini, 'SOLDAT')[26], 2)


if __name__ == '__main__':
    unittest.main()
