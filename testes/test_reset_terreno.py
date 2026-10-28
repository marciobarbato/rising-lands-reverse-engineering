"""TerrainReset, MiniMapReset and BatimentModifyMap: captures, order and protected inputs."""
import json
from pathlib import Path
import struct
import unittest

from test_colocacao_saida import MundoRastreado
from capturar_reset_terreno import preparar_reset, resumo
from candidatos_rota import aleatorio_caminhos
from reset_terreno import resetar_terreno, resetar_minimapa
from minimapa_estruturas import modificar_minimapa_estrutura

RAIZ = Path(__file__).resolve().parents[1]


def preparar(entrada='structure', largura=64, altura=64, minimapa=(128, 128), semente=1, estrutura=None,
             ativo=1, camera=0, padrao=9, **opcoes):
    m, minas, aleatorio = preparar_reset(entrada, largura, altura, minimapa, semente, estrutura, ativo, camera,
                                         padrao, classe=MundoRastreado, **opcoes)
    m.efeitos = []
    return m, minas, aleatorio


def executar(m, minas, aleatorio, entrada, estrutura, ativo):
    if entrada == 'terrain':
        return resetar_terreno(m, minas, aleatorio)
    if entrada == 'minimap':
        return resetar_minimapa(m)
    return modificar_minimapa_estrutura(m, estrutura[0], ativo)


class ResetTerreno(unittest.TestCase):
    def test_eight_original_captures_whole_buffers_mines_seed_and_minimap_calls(self):
        relatorio = json.loads((RAIZ/'relatorios/capturas-reset-terreno-original.json').read_text())
        self.assertFalse(relatorio['translation_executed'])
        for caso in relatorio['cases']:
            a = caso['input']
            estrutura = tuple(a['structure']) if a['structure'] else None
            m, minas, aleatorio = preparar(a['entry'], a['width'], a['height'], tuple(a['minimap']), a['seed'],
                                           estrutura, a['dl'], a['camera'], a['pattern'])
            executar(m, minas, aleatorio, a['entry'], estrutura, a['dl'])
            n = m.tamanho_minimapa[0]*m.tamanho_minimapa[1]
            memsets = ([['mini_final', 2, n], ['mini_unidades', 0, n], ['mini_estruturas', 0, n]]
                       if a['entry'] == 'minimap' else [])
            saida = resumo(m, minas, aleatorio, m.efeitos, 65536 if a['entry'] == 'terrain' else 0, memsets)
            self.assertEqual(saida, caso['output'])

    def test_terrain_reset_draws_one_random_per_cell_and_keeps_other_layers(self):
        m, minas, aleatorio = preparar('terrain', semente=0x12345678)
        antes = (list(m.tiles), list(m.regioes), bytes(m.mini_final), bytes(m.unidades), bytes(m.estruturas))
        reservas = [minas[k*4+2:k*4+4] for k in range(20)]
        resetar_terreno(m, minas, aleatorio)
        semente = 0x12345678
        for celula in range(65536):
            semente = aleatorio_caminhos(semente)
            self.assertEqual(m.donos_objetos[celula], semente & 3)
        self.assertEqual(struct.unpack('<I', aleatorio)[0], semente)
        self.assertEqual((bytes(m.objetos), bytes(m.atributos)), (bytes(65536), bytes(65536)))
        for p in range(4):
            self.assertEqual((bytes(m.contagem_luz[p]), bytes(m.luz_bordas[p]), bytes(m.descoberto[p])),
                             (bytes(65536), b'\x1f'*65536, b'\x1f'*65536))
        self.assertEqual([minas[k*4:k*4+2] for k in range(20)], [b'\0\0']*20)
        self.assertEqual([minas[k*4+2:k*4+4] for k in range(20)], reservas)
        self.assertEqual((list(m.tiles), list(m.regioes), bytes(m.mini_final), bytes(m.unidades),
                          bytes(m.estruturas)), antes)
        self.assertEqual(m.efeitos, [])

    def test_minimap_reset_writes_only_w_times_h_prefix_in_original_order(self):
        for minimapa in ((128, 128), (64, 32), (1, 1), (0, 128), (256, 256)):
            m, _, _ = preparar('minimap', minimapa=minimapa)
            antes = [bytes(getattr(m, n)) for n in ('mini_final', 'mini_unidades', 'mini_estruturas')]
            resetar_minimapa(m)
            n = minimapa[0]*minimapa[1]
            for nome, valor, original in zip(('mini_final', 'mini_unidades', 'mini_estruturas'), (2, 0, 0), antes):
                self.assertEqual(bytes(getattr(m, nome)), bytes([valor])*n + original[n:])

    def test_structure_footprint_row_major_with_256_clipping_and_dl_byte(self):
        m, _, _ = preparar(estrutura=(7, 0x0b0c, 0, 2))
        antes = bytes(m.estruturas)
        modificar_minimapa_estrutura(m, 0xabcd0007, 0x100)  # DL 0x00 after u8 truncation
        self.assertEqual(m.efeitos, [('minimap', 0, (0x0b0c + dy*256 + dx) & 65535, 7)
                                     for dy in range(5) for dx in range(6)])
        self.assertEqual(bytes(m.estruturas), antes)
        m, _, _ = preparar(largura=256, altura=256, estrutura=(999, 0xfefd, 200, 5))
        modificar_minimapa_estrutura(m, 999, 0x80)
        self.assertEqual(m.efeitos, [('minimap', 200, y*256+x, 6) for y in (254, 255) for x in (253, 254, 255)])

    def test_owner_200_structure_color_and_lit_selection(self):
        m, _, _ = preparar(estrutura=(3, 0x0808, 200, 9), visibilidade='lit', unidades_minimapa=0)
        modificar_minimapa_estrutura(m, 3, 1)
        self.assertEqual(len(m.efeitos), 1)
        self.assertIn(0x20, set(m.mini_estruturas))
        self.assertIn(0x20, set(m.mini_final))

    def test_protected_inputs_precede_every_effect(self):
        casos = []
        m, minas, aleatorio = preparar('terrain')
        casos.append((lambda: resetar_terreno(m, minas, aleatorio[:3]), m))
        m2, minas2, aleatorio2 = preparar('terrain')
        m2.luz_bordas[1] = m2.descoberto[1]
        casos.append((lambda: resetar_terreno(m2, minas2, aleatorio2), m2))
        m3, minas3, aleatorio3 = preparar('terrain')
        casos.append((lambda: resetar_terreno(m3, memoryview(bytes(80)), aleatorio3), m3))
        m4, _, _ = preparar('minimap', minimapa=(257, 256))
        casos.append((lambda: resetar_minimapa(m4), m4))
        m5, _, _ = preparar(estrutura=(7, 0x0b0c, 0, 22))
        casos.append((lambda: modificar_minimapa_estrutura(m5, 7, 1), m5))
        m6, _, _ = preparar(estrutura=(7, 0x0b0c, 32, 2))
        casos.append((lambda: modificar_minimapa_estrutura(m6, 7, 1), m6))
        m7, _, _ = preparar(estrutura=(7, 0x0b0c, 0, 2))
        casos.append((lambda: modificar_minimapa_estrutura(m7, 1000, 1), m7))
        for chamada, mundo in casos:
            antes = [bytes(mundo.donos_objetos), bytes(mundo.objetos), bytes(mundo.mini_final),
                     bytes(mundo.mini_estruturas), bytes(mundo.descoberto[1])]
            with self.assertRaises(ValueError):
                chamada()
            self.assertEqual([bytes(mundo.donos_objetos), bytes(mundo.objetos), bytes(mundo.mini_final),
                              bytes(mundo.mini_estruturas), bytes(mundo.descoberto[1])], antes)
            self.assertEqual(mundo.efeitos, [])
        # Owner 32 is colorless only for mode 6; mode 7 does not read the color table.
        modificar_minimapa_estrutura(m6, 7, 0)
        self.assertEqual(len(m6.efeitos), 30)


if __name__ == '__main__':
    unittest.main()
