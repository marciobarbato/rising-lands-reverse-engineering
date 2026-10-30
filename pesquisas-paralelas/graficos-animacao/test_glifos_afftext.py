"""Complete native AffText buffers, callback compatibility and addressed unsupported text paths."""
import json,lzma,unittest
from pathlib import Path
from graficos import Catalogo
from texto_afftext_bitmap import TextoAffTextBitmap,planejar_texto_afftext
from texto_bitmap_nativo import DependenciaTextoBitmap
from validar_glifos_afftext import validar
from validar_objetivos_s1 import sha

AQUI=Path(__file__).resolve().parent

class GlifosAffText(unittest.TestCase):
    def test_all_270_native_surfaces_and_7620_raster_arguments(self):
        fresh=validar();saved=json.loads((AQUI/'validacao/glifos-afftext-provider-final.json').read_text())
        self.assertEqual(fresh,saved);self.assertEqual((fresh['equal'],fresh['glyph_calls']),(270,7620))

    def test_callback_matches_a_real_native_case(self):
        d=json.loads(lzma.decompress((AQUI/'evidencias/glifos-afftext-nativos.json.xz').read_bytes()))
        row=next(r for r in d['rows'] if r['request']['font']==1 and r['request']['text_hex']==b'SANTU\xc1RIO'.hex())
        req=dict(row['request']);req['text']=bytes.fromhex(req.pop('text_hex'))
        provider=TextoAffTextBitmap(Catalogo(),recorte=row['clip'],idioma_u32=0,multibyte_u32=0)
        baseline=bytes((x*7+y*11)%256 for y in range(600) for x in range(800))
        self.assertEqual(sha(provider(req,baseline)),row['surface_sha256'])

    def test_unknown_modes_colour_control_and_opaque_pointer_are_not_defaults(self):
        catalog=Catalogo();base=dict(text=b'A',x=12,y=15,right=12,bottom=15,font=1,flags=(0,0))
        for update,mode,address in (({'text':None},(0,0),0x459454),({'text':b'A'*128},(0,0),0x459618),
                ({'text':b'\t'},(0,0),0x459618),({'flags':(1,0)},(0,0),0x459764),({},(0,1),0x459635)):
            with self.assertRaises(DependenciaTextoBitmap) as stop:
                planejar_texto_afftext(catalog,dict(base,**update),idioma_u32=mode[0],multibyte_u32=mode[1])
            self.assertEqual(stop.exception.endereco,address)
        with self.assertRaises(ValueError):
            planejar_texto_afftext(catalog,dict(base,font=True),idioma_u32=0,multibyte_u32=0)
