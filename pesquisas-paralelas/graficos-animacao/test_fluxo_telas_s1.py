"""S1 screen phases, bank identities and explicit unknown-menu dependencies."""
import json,unittest
from pathlib import Path
from graficos import Catalogo
from telas_fluxo_s1 import compor_affgame_s1
from texto_bitmap_nativo import DependenciaTextoBitmap
from validar_fluxo_telas_s1 import validar
from validar_objetivos_s1 import CapturaTelaS1

AQUI=Path(__file__).resolve().parent

class FluxoTelasS1(unittest.TestCase):
    def test_every_native_result_and_objectives_phase(self):
        fresh=validar(AQUI/'evidencias/s1-telas-finais-nativas.json.xz')
        self.assertEqual(fresh,json.loads((AQUI/'validacao/s1-fluxo-telas-provider-final.json').read_text()))
        self.assertEqual(fresh['counts'],dict(result=11,objectives=7))
        self.assertEqual(set(fresh['menu_asset_matches']),{'2','3','4'})

    def test_result_returns_before_display_and_unknown_banks_stop(self):
        class ResultOnly:
            def u8(self,a):
                if a!=0x4e2f78:raise AssertionError('Result branch must not read gameplay state')
                return 0x13
        out=compor_affgame_s1(ResultOnly(),bytes(480000),catalogo=None)
        self.assertEqual((out['pixels'],out['chamadas'],out['efeitos']),(bytes(480000),[],[]))
        cap=CapturaTelaS1(AQUI/'evidencias/s1-telas-finais-nativas.json.xz')
        row=next(r for r in cap.d['phases'] if r['frame']==17044 and r['phase']=='between_frames')
        with self.assertRaises(DependenciaTextoBitmap) as stop:
            compor_affgame_s1(cap.memory(row),cap.blob(row['before']),catalogo=Catalogo())
        self.assertEqual(stop.exception.endereco,0x418590)
