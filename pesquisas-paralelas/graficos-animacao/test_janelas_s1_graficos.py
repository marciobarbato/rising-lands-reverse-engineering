"""S1 native transport integrity, complete source-bound proof and actual render regressions."""
import hashlib
import json
import re
import subprocess
import unittest

from render_quadro import renderizar_quadro
from validar_colheita_graficos import CapturaLimitada
from validar_entrada_m3 import ArgumentosRasterM3, CatalogoRastreado
from validar_janelas_s1_graficos import AQUI, habitado
from validar_sondas_graficos_m3 import FronteiraTextoGravada


class JanelasS1Graficos(unittest.TestCase):
    def test_active_clock_missing_and_unproved_inputs_have_named_stops(self):
        from hud_quadro import _Hud, LeituraHud
        from quadro_jogo import DependenciaQuadro
        from test_quadro_jogo import tabelas
        cap=CapturaLimitada(AQUI/'evidencias/s1-render-part-1985-2112.json.xz')
        row=next(r for r in cap.d['rows'] if r['frame']==2014)
        m=cap.memory(row);catalog=CatalogoRastreado();shadow=tabelas()[0]
        variations=(
            ({},None,shadow,0x41a5b8),
            ({},lambda i:habitado(m,i),None,0x45b796),
            ({0x49a0c8+0x7b:13},lambda i:habitado(m,i),shadow,0x423f9d),
            ({0x4965ae+50*7:0,0x4965ae+50*7+1:0},lambda i:habitado(m,i),shadow,0x423ec8),
            ({0x49a0c8+0x8c+i:v for i,v in enumerate((101*m.u16(0x4965ae+50*7)).to_bytes(4,'little'))},lambda i:habitado(m,i),shadow,0x401ef1),
            ({0x508f90:1},lambda i:habitado(m,i),shadow,0x401e56),
            ({0x497285:2},lambda i:habitado(m,i),shadow,0x401e11),
        )
        before=m.ler_mundo(0x494000,0x8f000)
        for overrides,query,table,address in variations:
            with self.subTest(address=hex(address)):
                h=_Hud(LeituraHud(m,overrides),cap.blob(row['before']),catalog,0,
                    tabela_sombra=table,habitado=query)
                with self.assertRaises(DependenciaQuadro) as stop:
                    h.cronometro()
                self.assertEqual(stop.exception.endereco,address)
                self.assertEqual(m.ler_mundo(0x494000,0x8f000),before)

    def test_native_transport_preserves_all_original_rows_and_payloads(self):
        total = 275  # The first native capture is below the transport-size threshold.
        first=json.loads((AQUI/'evidencias/s1-render-129-403.json.xz.manifest.json').read_text())
        self.assertEqual(first['status'],'complete')
        self.assertLess(first['invocation_seconds'],1200)
        self.assertEqual(hashlib.sha256((AQUI/'evidencias/s1-render-129-403.json.xz').read_bytes()).hexdigest(),first['compressed_sha256'])
        for parent in ('1729-2383','2251-2878','3001-3508','3251-4000','4001-4750','4751-5090'):
            ledger = json.loads((AQUI / f'evidencias/s1-render-{parent}.json.xz.partitions.json').read_text())
            self.assertTrue(ledger['complete_native_rows_equal'] and ledger['encoded_payloads_unchanged'])
            native = ledger['native_manifest']
            self.assertEqual(native['status'], 'complete')
            self.assertLess(native['invocation_seconds'], 1200)
            self.assertEqual(native['source_sha256'], hashlib.sha256((AQUI/'capturar_janelas_s1_graficos.py').read_bytes()).hexdigest())
            lo, hi = native['frames']
            self.assertEqual(sum(p['frames'][1]-p['frames'][0]+1 for p in ledger['parts']), hi-lo+1)
            total += hi-lo+1
            for part in ledger['parts']:
                raw = (AQUI/'evidencias'/part['path']).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), part['sha256'])
                self.assertLess(len(raw), 100*1024*1024)
        self.assertEqual(total, 3906)

    def test_complete_current_s1_and_prior_probe_proofs(self):
        inventory=json.loads((AQUI/'evidencias/s1-render-window-inventory.json').read_text())
        self.assertEqual(len(inventory['all_s1_view_origins']),19)
        self.assertEqual(inventory['unproved_affgame_origins'],[])
        self.assertEqual(inventory['unproved_restoreall_origins'],[])
        current = json.loads((AQUI/'validacao/s1-render-final.json').read_text())
        self.assertEqual((current['equal_surfaces'], current['expected_surfaces']), (2792,2792))
        self.assertEqual([w['equal'] for w in current['windows']], [274,564,479,399,351,454,271])
        self.assertTrue(all(not w['missing_ranges'] and w['first_difference'] is None for w in current['windows']))
        self.assertEqual(sum(c['equal'] for c in current['captures']),3906)
        self.assertTrue(any(c['continued_from_previous_capture'] for c in current['captures']))
        regression=json.loads((AQUI/'validacao/s1-regression-P3P6P7.json').read_text())
        self.assertEqual({w['probe']:w['equal'] for w in regression['windows']},dict(P3=3001,P6=2272,P7=3572))
        for report in (current,regression):
            for name,digest in report['sources_sha256'].items():
                frozen=subprocess.check_output(['git','show','9b5f449:pesquisas-paralelas/graficos-animacao/'+name],cwd=AQUI)
                self.assertEqual(hashlib.sha256(frozen).hexdigest(),digest,name)
            for capture in report.get('captures',report.get('windows',[])):
                for row in capture['rows']:
                    self.assertTrue(row['equal'])
                    self.assertIsNone(row['stop'])
                    self.assertEqual(row['sha256'],row['native_sha256'])

    def test_real_sanctuary_clock_depot_tasks_and_shifted_tired_icons(self):
        names=json.loads((AQUI/'validacao/s1-render-capture-set.json').read_text())['captures']
        frames=(2014,2549,2561,2670,3001,3177,3251,4100,4788)
        selected={}
        for frame in frames:
            name=next(n for n in names if (lambda v:int(v[0])<=frame<=int(v[1]))(re.findall(r'(\d+)-(\d+)\.json',n)[0]))
            selected.setdefault(name,[]).append(frame)
        catalog=CatalogoRastreado()
        for name, cases in selected.items():
            cap=CapturaLimitada(AQUI/'evidencias'/name)
            for frame in cases:
                row=next(r for r in cap.d['rows'] if r['frame']==frame)
                m=cap.memory(row);adapter=FronteiraTextoGravada(cap,row)
                with ArgumentosRasterM3(catalog) as raster:
                    result=renderizar_quadro(m,superficie_anterior=cap.blob(row['before']),cache=cap.cache_entry(row),
                        catalogo=catalog,habitado=lambda i:habitado(m,i),hud=True,texto=adapter,
                        relogio=lambda:int.from_bytes(cap.blob(row['exit_dgroup'])[0x4e17b4-0x494000:0x4e17b8-0x494000],'little'))
                self.assertIsNone(result.parada,(name,frame,result.parada))
                self.assertEqual(result.pixels,cap.blob(row['after']),(name,frame))
                self.assertEqual(raster.calls,row['blits'],(name,frame))
                self.assertFalse(adapter.pending)
