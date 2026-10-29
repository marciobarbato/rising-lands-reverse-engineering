"""Render API 1.5 against complete original-first native M3 display cases."""
import contextlib, hashlib, io, json, struct, unittest
from pathlib import Path
from graficos import Catalogo
from render_quadro import renderizar_quadro, EstadoCache, regioes_necessarias
from validar_entrada_m3 import CapturaEntradaM3, MemoriaEntradaM3, validar

AQUI=Path(__file__).resolve().parent
CAPTURES=(AQUI/'evidencias/captura-entrada-m3.json',AQUI/'evidencias/captura-entrada-m3-suplementar.json')
HASHES=('58f47c4c7cb1cbbe6cf2264a26f29b7e4bb20e0c96dabc4bbbbd49576b1f0b22',
        '6ecab5a4cafdef5dcd738baaaa75aadad97b08d0afe1620074e71f7c04c0ba43')

class EntradaM3(unittest.TestCase):
    def test_original_identity_and_reproduction(self):
        for path,expected in zip(CAPTURES,HASHES):
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),expected)
            d=json.loads(path.read_text())
            self.assertEqual(d['executable_sha256'],'6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
            self.assertTrue(all(d['reproduction'].values()))
        provenance=json.loads((AQUI/'evidencias/entrada-m3-proveniencia.json').read_text())
        self.assertEqual(provenance['capture_sha256'],HASHES[0])
        report=json.loads((AQUI/'validacao/entrada-m3-api15.json').read_text())
        for name,value in report['sources_sha256'].items():
            self.assertEqual(hashlib.sha256((AQUI/name).read_bytes()).hexdigest(),value,name)

    def test_complete_surfaces_arguments_and_display_effects(self):
        with contextlib.redirect_stdout(io.StringIO()):result=validar(CAPTURES)
        self.assertEqual((result['cases'],result['complete_cases'],result['dependency_stops'],result['mismatches']),(114,113,1,0))
        self.assertTrue(all(r['pixel_mismatches']==0 for r in result['rows'] if not r['expected_stop']))
        self.assertGreater(sum(r['drawing_calls_checked'] for r in result['rows']),2000)

    def test_m22_api15_keeps_all_128_native_frames(self):
        current=json.loads((AQUI/'evidencias/verificacao-cadeia-m22-v2-api15-128.json').read_text())
        previous=json.loads((AQUI/'evidencias/verificacao-cadeia-m22-v2-api14-128.json').read_text())
        self.assertEqual((current['frames'],current['render_api_version'],current['hud'],current['first_stop'],
                          current['first_chained_difference_frame'],current['chained_equals_recorded_count']),
                         (128,[1,5],True,None,None,128))
        for row,old in zip(current['rows'],previous['rows']):
            self.assertTrue(row['chain_cache_equals_native_entry_cache'])
            self.assertEqual(row['chained']['pixels'],0)
            self.assertEqual(row['over_native_previous']['pixels'],0)
            self.assertEqual(row['chained']['sha256'],old['chained']['sha256'])
        for name in ('superficie','cache'):
            new=json.loads((AQUI/f'validacao/{name}-inicial-api15.json').read_text())
            oldpath='cache-terreno-inicial-m22-v2.json' if name=='cache' else 'superficie-inicial-m22-v2.json'
            old=json.loads((AQUI/'evidencias'/oldpath).read_text())
            for key,value in old.items():
                if key not in ('producing_revision','command'):self.assertEqual(new[key],value)

    def test_unsupported_inputs_still_stop_and_memory_is_read_only(self):
        cap=CapturaEntradaM3(CAPTURES[0]);case=next(c for c in cap.d['cases'] if c['name']=='selected_unit_12')
        m=cap.memory(case);base=m.u32(0x4e19a0)+12*276;catalog=Catalogo();cache=case['cache']
        cache=EstadoCache(cap.blob(cache['keys']),cap.blob(cache['payloads']),cache['cursor'])
        cases=((base+0x82,b'\1',0x412923),(base+0xc,b'\2\0',0x410a2c),
               (base+0x9a,b'\x65\0',0x410be4),(base+0x99,b'\1',0x41591f),
               (0x4e2412,b'\3\0',0x417086),(0x4e2412,struct.pack('<HH',2,1000),0x417086),
               (0x4e062c,b'\x11\0',0x417cfc))
        for address,value,stop in cases:
            with self.subTest(address=hex(address),value=value.hex()):
                blocks=[(a,bytearray(d)) for a,d in m.blocks]
                for a,d in blocks:
                    if a<=address and address+len(value)<=a+len(d):d[address-a:address-a+len(value)]=value;break
                memory=MemoriaEntradaM3(blocks);before=[bytes(d) for _,d in blocks]
                result=renderizar_quadro(memory,superficie_anterior=cap.blob(case['before']),cache=cache,catalogo=catalog,
                                         habitado=lambda i:i==0,hud=True)
                self.assertEqual(result.parada['endereco'],f'0x{stop:08x}')
                self.assertEqual([bytes(d) for _,d in blocks],before)
        regions=regioes_necessarias(m,hud=True)
        self.assertIn((m.u32(0x4e24bc),m.u32(0x4e24bc)+256,'noir_blanc'),regions)

if __name__=='__main__':unittest.main()
