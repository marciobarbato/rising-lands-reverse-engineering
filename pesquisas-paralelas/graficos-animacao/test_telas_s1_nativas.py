"""Real S1 late-screen native evidence, distinct from an unsupported Python menu renderer."""
import hashlib,json,lzma,subprocess,unittest
from collections import Counter
from pathlib import Path

AQUI=Path(__file__).resolve().parent

class TelasS1Nativas(unittest.TestCase):
    def test_real_native_screen_calls_and_phase_surfaces(self):
        d=json.loads(lzma.decompress((AQUI/'evidencias/s1-telas-finais-nativas.json.xz').read_bytes()))
        self.assertEqual(d['frames'],[17001,17050]);self.assertEqual(len(d['checks']),50);self.assertEqual(len(d['phases']),100)
        self.assertTrue(all(c['published_phase_and_state_equal'] for c in d['checks']))
        self.assertEqual(Counter(r['routine'] for r in d['rows']),dict(MenuInit=2,PartieGetResultat=11,AffObjectif=7))
        for row in d['rows']:
            self.assertEqual(row['declared_writes'],[])
            for key in ('returned','surface_equal','whole_state_equal','raster_arguments_equal','text_arguments_equal'):
                self.assertTrue(row[key],(row['frame'],row['routine'],key))
        self.assertEqual([(r['frame'],r['routine']) for r in d['rows'] if r['routine']=='MenuInit'],[(17032,'MenuInit'),(17043,'MenuInit')])
        frozen=subprocess.check_output(['git','show','24f0ec8:pesquisas-paralelas/graficos-animacao/capturar_telas_finais_s1.py'],cwd=AQUI)
        self.assertEqual(hashlib.sha256(frozen).hexdigest(),d['source_sha256'])
        self.assertEqual(d['input_sha256'],'622a882d5439afc88431102fb98df60dcc44a59714742c9278ba4d7d8413c18c')

    def test_s1_structure_types_and_states_stay_inside_the_proved_matrix(self):
        d=json.loads((AQUI/'evidencias/inventario-estruturas-S1-ledger.json').read_text())
        self.assertEqual(d['frames'],16922)
        self.assertEqual({(r['index'],r['kind'],r['state'],r['owner']) for r in d['structures']},
            {(0,2,4,0),(0,2,5,0),(1,3,2,200),(1,3,5,200),(1,3,5,0)})
        self.assertEqual(len(d['view_origins']),19)

    def test_published_guards_cover_the_two_reported_p6_stops(self):
        d=json.loads((AQUI/'validacao/guardas-p6-publicadas-245-1141.json').read_text())
        self.assertEqual(d['provider_revision'],'3a22f70');self.assertEqual((d['cases'],d['mismatches']),(2,0))
        self.assertEqual([r['projectiles'] for r in d['rows']],[[[0,15,1,0]],[[0,16,1,0]]])
        self.assertTrue(all(r['passed'] and not r['logic_writes'] for r in d['rows']))
