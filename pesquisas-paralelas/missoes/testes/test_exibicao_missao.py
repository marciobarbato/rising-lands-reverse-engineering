"""Display-executing oracle scenario: CPU-free checks of the committed evidence and reports."""
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ambiente_missoes
import cenarios_oraculo as cen
from oraculo_exibicao_missao import FRONTEIRAS_EXIBICAO, PULOS_EXIBICAO

V = ambiente_missoes.OWNED/'validacao'


def carregar(nome):
    return json.loads((V/nome).read_bytes())


@unittest.skipUnless(cen.caminho('exibicao', 'captura_quadro').exists(), 'Display captures not committed')
class TestEvidenciaExibicao(unittest.TestCase):
    def test_frame_capture_reaches_frame1_and_reproduces_the_display_m1_path(self):
        cap = json.loads(cen.caminho('exibicao', 'captura_quadro').read_bytes())
        self.assertEqual(cap['scenario'], 'exibicao')
        self.assertTrue(cap['frame1_return']['reached'])
        self.assertTrue(cap['m1_path']['entry_equal_committed'])
        self.assertTrue(cap['m1_path']['final_equal_capture_v2'])
        self.assertFalse(cap['translation_executed'])

    def test_display_boundaries_are_only_text_picture_video_credits_and_audio(self):
        self.assertNotIn('AffGame', FRONTEIRAS_EXIBICAO)
        for nome in ('AffInit', 'DDLockSurface', 'DDFlipPage', 'LoadSTRATBank', 'LoadBank', 'SetBank'):
            self.assertNotIn(nome, PULOS_EXIBICAO)
            self.assertNotIn(nome, FRONTEIRAS_EXIBICAO)

    @unittest.skipUnless((V/'m2r3-frame1-v1-vs-exibicao.json').exists(), 'Comparison not committed')
    def test_reports_passed_and_logic_tables_did_not_diverge(self):
        for nome in ('m2r3-missionload-exibicao-x86.json', 'm2r3-frame1-exibicao-x86.json',
                     'm2r3-v1-vs-exibicao-writers.json'):
            self.assertTrue(carregar(nome)['passed'], nome)
        self.assertTrue(carregar('m2r3-m1-composition-strict-exibicao.json')['m1_candidate'])
        comparacao = carregar('m2r3-frame1-v1-vs-exibicao.json')
        self.assertEqual(comparacao['allocation_matching']['matched'], comparacao['allocation_matching']['v1_records'])
        frame1 = comparacao['states']['frame1']['differing']['dgroup']['ranges']
        unidades = [r for r in frame1 if 0x49a0c8 <= int(r['start'], 16) < 0x4de0e8]
        self.assertEqual(unidades, [], 'no structure-pool byte differs')


if __name__ == '__main__':
    unittest.main()
