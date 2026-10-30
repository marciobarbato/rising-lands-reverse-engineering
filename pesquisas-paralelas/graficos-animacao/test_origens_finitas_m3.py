"""Finite native origin evidence and current guard boundaries, independent of pixel composition."""
import hashlib,json,lzma,struct,unittest
from pathlib import Path
from validar_grade_vistas19 import MemoriaGrade
from efeitos_logicos_exibicao import desenhar_jogo,restaurar_tudo,DependenciaExibicao

AQUI=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()

class OrigensFinitasM3(unittest.TestCase):
    def test_complete_native_matrix_and_current_comparison(self):
        d=json.loads((AQUI/'validacao/grade-vistas19-provider-final.json').read_text())
        self.assertEqual((d['cases'],d['expected_cases'],d['mismatches']),(3840,3840,0))
        self.assertTrue(d['complete'] and d['provider_compared'])
        self.assertEqual(d['provider_sha256'],sha((AQUI/'efeitos_logicos_exibicao.py').read_bytes()))
        self.assertEqual(d['domain_table_sha256'],sha((AQUI/'origens_efeitos_monde01.json').read_bytes()))
        for name,digest in d['native_capture_pins'].items():
            self.assertEqual(digest,sha((AQUI/'evidencias'/name).read_bytes()))
        self.assertTrue(all(r['native_return'] and r['provider_equal'] and not r['additional_logic_writes']
                            and r['crt_changes']==0 and r['cursor_writer_hits']==0 for r in d['rows']))

    def test_new_origins_require_the_captured_camera_map_and_mode(self):
        d=json.loads(lzma.decompress((AQUI/'evidencias/grade-vistas19-0520.json.xz').read_bytes()))
        row=next(r for r in d['rows'] if r['routine']=='AffGame' and r['origin']==[10,15])
        for fn in (desenhar_jogo,restaurar_tudo):
            self.assertEqual(fn(MemoriaGrade(d,row)).escritas,())
            for a,raw in ((0x497168,struct.pack('<H',63)),(0x49716a,struct.pack('<H',65)),
                          (0x508041,b'\1'),(0x4e2f78,b'\x13'),(0x508720,struct.pack('<H',40)),
                          (0x508722,struct.pack('<H',48))):
                m=MemoriaGrade(d,row);m.dg[a-0x494000:a-0x494000+len(raw)]=raw
                with self.assertRaises(DependenciaExibicao) as stop:fn(m)
                self.assertEqual(stop.exception.sitio,0x415b77)

    def test_actual_p7_origins_preserve_ai_flag_and_return(self):
        d=json.loads((AQUI/'validacao/origens-p7-provider-final.json').read_text())
        self.assertEqual((d['cases'],len(d['unique_origins']),d['mismatches']),(7,7,0))
        self.assertEqual(d['graphics_provider_sha256'],sha((AQUI/'efeitos_logicos_exibicao.py').read_bytes()))
        self.assertTrue(all(r['returned'] and r['surface_equal'] and not r['additional_logic_writes'] for r in d['rows']))
