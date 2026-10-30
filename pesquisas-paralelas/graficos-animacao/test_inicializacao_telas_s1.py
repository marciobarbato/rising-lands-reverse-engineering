"""Native S1 transition dependencies and prepared drawing plans; no implicit text/picture bypass."""
import json,unittest
from pathlib import Path
from validar_objetivos_s1 import CapturaTelaS1
from validar_inicializacao_telas_s1 import validar,FronteirasTelaS1Gravadas
from telas_inicializacao_s1 import compor_inicializacao_s1,DependenciaInicializacaoS1

AQUI=Path(__file__).resolve().parent

class InicializacaoTelasS1(unittest.TestCase):
    def test_two_real_native_transitions_and_all_dependency_sequences(self):
        path=AQUI/'evidencias/s1-dependencias-nativas.json.xz';fresh=validar(path)
        self.assertEqual(fresh,json.loads((AQUI/'validacao/s1-inicializacao-provider-final.json').read_text()))
        cap=CapturaTelaS1(path)
        self.assertEqual(len(cap.d['rows']),20)
        self.assertTrue(all(r['dependency_arguments_equal'] and r['whole_state_equal'] and r['surface_equal'] for r in cap.d['rows']))
        self.assertTrue(all(r['published_phase_and_state_equal'] for r in cap.d['checks']))

    def test_missing_picture_or_text_stops_with_the_exact_partial_surface(self):
        cap=CapturaTelaS1(AQUI/'evidencias/s1-dependencias-nativas.json.xz')
        row=next(r for r in cap.d['rows'] if r['routine']=='MenuInit' and r['frame']==17032)
        m=cap.memory(row);pixels=cap.blob(row['before'])
        with self.assertRaises(DependenciaInicializacaoS1) as stop:
            compor_inicializacao_s1(m,pixels,jogador_u8=0,modo_destino_u8=0x13)
        self.assertEqual((stop.exception.endereco,stop.exception.pixels),(0x4799c4,pixels))
        boundary=FronteirasTelaS1Gravadas(cap,row)
        with self.assertRaises(DependenciaInicializacaoS1) as stop:
            compor_inicializacao_s1(m,pixels,jogador_u8=0,modo_destino_u8=0x13,carregar_pie=boundary.pie,
                mensagem=dict(pointer=0,text=None))
        self.assertEqual((stop.exception.endereco,stop.exception.pixels),(0x459454,pixels))
        self.assertTrue(boundary.pie_checked);self.assertFalse(boundary.text_checked)
