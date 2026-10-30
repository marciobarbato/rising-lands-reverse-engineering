"""Real original S1 objectives pixels and strict text/page dependency behavior."""
import hashlib,json,unittest
from pathlib import Path
from graficos import Catalogo
from validar_objetivos_s1 import CapturaTelaS1,MemoriaTelaS1,validar
from telas_objetivos_s1 import compor_objetivos_s1
from texto_bitmap_nativo import compor_linha_bitmap,DependenciaTextoBitmap

AQUI=Path(__file__).resolve().parent

class ObjetivosS1(unittest.TestCase):
    def test_all_native_objectives_pixels_arguments_and_dgroup(self):
        fresh=validar(AQUI/'evidencias/s1-telas-finais-nativas.json.xz')
        saved=json.loads((AQUI/'validacao/s1-objetivos-provider-final.json').read_text())
        self.assertEqual(fresh,saved);self.assertEqual((fresh['equal'],fresh['cases']),(7,7))
        self.assertEqual(sum(r['drawing_calls'] for r in fresh['rows']),1519)

    def test_missing_text_and_unproved_page_or_font_are_dependencies(self):
        cap=CapturaTelaS1(AQUI/'evidencias/s1-telas-finais-nativas.json.xz')
        row=next(r for r in cap.d['rows'] if r['routine']=='AffObjectif');m=cap.memory(row)
        for a,v in ((0x511ff8,b'\x12\0'),(0x4e1d98,b'\1\0\0\0')):
            dg=bytearray(m.ler_mundo(0x494000,0x8f000));dg[a-0x494000:a-0x494000+len(v)]=v
            with self.assertRaises(DependenciaTextoBitmap):
                compor_objetivos_s1(MemoriaTelaS1([(0x494000,bytes(dg))]),cap.blob(row['before']),catalogo=Catalogo())
        dg=bytearray(m.ler_mundo(0x494000,0x8f000));dg[0x511828-0x494000:0x51182c-0x494000]=b'\0'*4
        with self.assertRaises(KeyError):
            compor_objetivos_s1(MemoriaTelaS1([(0x494000,bytes(dg))]),cap.blob(row['before']),catalogo=Catalogo())
        with self.assertRaises(DependenciaTextoBitmap):
            compor_linha_bitmap(Catalogo(),bytes(480000),texto=b'A',x=0,y=0,fonte_u8=2,
                idioma_u32=0,multibyte_u32=0,recorte=(0,0,799,599))
