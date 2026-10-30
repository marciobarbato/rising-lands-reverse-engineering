"""Normal renderer glyphs against original full surfaces, with historical boundaries explicit."""
import json, unittest
from validar_affgame_glifos import validar, AQUI, sha
from validar_objetivos_s1 import validar as objetivos


class AffGameGlifos(unittest.TestCase):
    def test_normal_default_matches_every_native_surface_and_raster_call(self):
        fresh=validar(AQUI/'evidencias/affgame-glifos-nativos.json.xz')
        saved=json.loads((AQUI/'validacao/affgame-glifos-api112-final.json').read_text())
        self.assertEqual(fresh,saved)
        self.assertEqual(fresh['equal'],fresh['expected'])
        p4=next(r for r in fresh['rows'] if r['frame']==484 and 'P4' in r['source'])
        self.assertEqual(p4['text_calls'],1)
        self.assertIsNone(p4['stop'])

    def test_s1_objectives_render_real_loaded_lines(self):
        fresh=objetivos(AQUI/'evidencias/s1-help-glifos-reproduction.json.xz')
        saved=json.loads((AQUI/'validacao/s1-help-glifos-final.json').read_text())
        self.assertEqual(fresh,saved)
        self.assertEqual(fresh['equal'],7)
