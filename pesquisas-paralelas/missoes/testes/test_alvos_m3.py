"""M3 Step 0 static targets: the committed JSON is reproduced from the accepted states, and its
translations agree with the bytes and with the committed providers they sit next to.

CPU-free. Needs the committed M1 and frame-128 captures; the code-anchor test also needs the
intact RISING.EXE and skips without it.
"""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'm3'))
import extrair_alvos_m3 as alvos  # noqa: E402

TEM_CAPTURAS = alvos.CAPTURA_128.exists() and alvos.CAPTURA_M1.exists()


def _sem_executavel(resultado):
    r = copy.deepcopy(resultado)
    r['sources'].pop('executable')
    return r


@unittest.skipUnless(TEM_CAPTURAS, 'M1 / frame-128 captures not available')
class TestAlvosM3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resultado = alvos.extrair()
        cls.m, _ = alvos.carregar_quadro128()

    def test_json_publicado_reproduzido(self):
        publicado = json.loads(alvos.SAIDA.read_text())
        self.assertEqual(_sem_executavel(publicado), _sem_executavel(self.resultado))

    def test_ancoras_de_codigo(self):
        ancoras = alvos.verificar_ancoras()
        if ancoras is None:
            self.skipTest('intact RISING.EXE not available')
        self.assertTrue(all(a['verified'] for a in ancoras), [a['name'] for a in ancoras if not a['verified']])
        publicado = json.loads(alvos.SAIDA.read_text())
        self.assertEqual(publicado['sources']['executable']['anchors_status'], 'verified')

    def test_unidades_alvo(self):
        por = {u['unit']: u for u in self.resultado['units']['all']}
        esperado = {12: (7, 4113), 13: (5, 4110), 14: (5, 4108), 11: (1, 5387), 15: (8, 4877)}
        for i, (tipo, c) in esperado.items():
            self.assertEqual((por[i]['owner'], por[i]['type'], por[i]['cell']), (0, tipo, c))
            self.assertEqual(por[i]['cell'], por[i]['cell_plus8'])
        self.assertEqual(por[12]['pixel'], [560, 528])
        self.assertFalse(por[11]['on_screen'])
        self.assertFalse(por[15]['on_screen'])

    def test_mapeamento_pixel_celula(self):
        m = self.m
        self.assertEqual(alvos.vista(m)['origin'], (0, 0))
        for c in range(0x10000):
            px = alvos.pixel_de_celula(m, c)
            if px is not None:
                self.assertEqual(alvos.celula_de_pixel(m, *px), c)
                self.assertEqual(alvos.celula_de_pixel(m, px[0] - 16, px[1] - 16), c)
                self.assertEqual(alvos.celula_de_pixel(m, px[0] + 15, px[1] + 15), c)
        self.assertIsNone(alvos.celula_de_pixel(m, 400, 544))

    def test_zonas_mouse_e_icones(self):
        m = self.m
        self.assertEqual(alvos.zonas_mouse(m)[:2], (1, 31))
        for (px, py), zona in {(0, 0): 1, (64, 64): 10, (400, 560): 11, (400, 300): 0, (799, 300): 4,
                               (180, 573): 11, (2, 300): 8}.items():
            self.assertEqual(alvos.zona_mouse(m, px, py), zona, (px, py))
        for i, (x0, y0, x1, y1) in alvos.retangulos_icones(m).items():
            self.assertEqual(alvos.icone_em(m, (x0 + x1) // 2, (y0 + y1) // 2), i)
            if i < 4:
                self.assertEqual(alvos.icone_em(m, x1 + 1, y0), 0xffff)   # one-pixel gap between action icons
        icone = self.resultado['cave_icon']
        self.assertEqual((icone['slot'], icone['rect_inclusive'], icone['center_pixel']), (2, [151, 548, 209, 598], [180, 573]))

    def test_cave_e_recursos(self):
        r = self.resultado
        self.assertEqual(r['cave']['dims'], [5, 5])
        self.assertEqual(r['cave']['cost'], dict(food=10, stone=6, parts=0))
        self.assertEqual((r['stock']['food'], r['stock']['stone'], r['stock']['parts']), (30, 30, 0))
        self.assertTrue(r['cave_icon_click']['test_ressource_passes'])
        self.assertEqual(r['zone0']['record'], [0, 0, 28, 25])
        self.assertEqual(r['zone0']['cells'], 29 * 26)

    def test_santuario_bate_com_colonos(self):
        # Core BatimentGetCase of structure 0 is the cell the colonists (units 3-10, state 14) hold.
        r = self.resultado
        colonos = {u['cell'] for u in r['units']['all'] if 3 <= u['unit'] <= 10}
        self.assertEqual(colonos, {r['zone0']['sanctuary']['batimentGetCase']})

    def test_local_proposto(self):
        m, sitio = self.m, self.resultado['cave_sites']['proposed']
        self.assertEqual(alvos.batiment_posable(m, alvos.TIPO_CAVE, sitio['cell'], 0)[0], 'valid')
        self.assertEqual(sitio['footprint_origin'], (sitio['cell'] - 0x202) & 0xffff)
        self.assertEqual(sitio['zone'], 0)
        self.assertEqual(alvos.zona_mouse(m, *sitio['pixel']), 0)
        self.assertEqual(alvos.celula_de_pixel(m, *sitio['pixel']), sitio['cell'])
        # The sanctuary's own cells are never a valid site.
        self.assertNotEqual(alvos.batiment_posable(m, alvos.TIPO_CAVE, alvos.celula(14, 13), 0)[0], 'valid')

    def test_comida_e_pedra(self):
        r = self.resultado
        for f in r['food']['nearest_fields']:
            self.assertTrue(0x1d <= f['object'] <= 0x34)
        self.assertEqual([(x['origin_xy'], x['reserve']) for x in r['stone']['mines']], [([43, 8], 50), ([6, 59], 200)])
        self.assertEqual(r['stone']['terrainEstMine_cells'], [2091, 2092, 15110, 15111])
        self.assertEqual(r['food']['field_cells_discovered'], 0)
        self.assertFalse(any(c['caseEstDecouverte'] for x in r['stone']['mines'] for c in x['clickable_cells_terrainEstMine']))

    def test_minimapa(self):
        m = self.m
        for vista in (self.resultado['food']['view_for_nearest_field'], self.resultado['stone']['view_for_first_mine_cell']):
            self.assertEqual(list(alvos.minimapa_centrar(m, *vista['minimap_press_pixel'])), vista['view_origin'])
            self.assertEqual(alvos.zona_mouse(m, *vista['minimap_press_pixel']), 10)
            self.assertEqual(alvos.zona_mouse(m, *vista['minimap_move_press_pixel']), 10)
        campo = self.resultado['food']['nearest_fields'][0]['cell']
        self.assertEqual(alvos.minimapa_celula(m, *self.resultado['food']['view_for_nearest_field']['minimap_move_press_pixel']), campo)
        self.assertEqual(alvos.minimapa_centrar(m, 25, 17), (0, 0))
        self.assertEqual(alvos.minimapa_centrar(m, 128, 128), (39, 47))


if __name__ == '__main__':
    unittest.main()
