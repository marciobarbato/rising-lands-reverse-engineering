"""Late-S1 source-bound full-surface proofs and actual transition regressions."""
import json,unittest
from hud_quadro import _Hud,LeituraHud
from quadro_jogo import DependenciaQuadro
from render_quadro import renderizar_quadro
from validar_affgame_glifos import sha
from validar_colheita_graficos import CapturaLimitada
from validar_entrada_m3 import ArgumentosRasterM3,CatalogoRastreado
from validar_janelas_s1_graficos import AQUI,habitado
from validar_sondas_graficos_m3 import FronteiraTextoGravada
from validar_s1_tardio_graficos import CAPTURES
from efeitos_logicos_exibicao import desenhar_jogo


class S1TardioGraficos(unittest.TestCase):
    def test_complete_prepared_fire_levels_and_allied_soldier_proofs(self):
        for name,count in (('cave-fogo-api112-final.json',141),('s1-soldado-aliado-api112-final.json',2),('s1-raide-multi-api112-final.json',3),('s1-icone-alerta-api112-final.json',32),('s1-fome-fazendeiro-api112-final.json',1)):
            d=json.loads((AQUI/'validacao'/name).read_text())
            self.assertEqual((d['expected'],d['equal']),(count,count))
            for source,digest in d['sources_sha256'].items():self.assertEqual(sha((AQUI/source).read_bytes()),digest,source)
            self.assertTrue(all(r['equal'] and r['stop'] is None for r in d['rows']))

    def test_message_zone_writes_are_logical_outputs_not_masked_display_bytes(self):
        cap=CapturaLimitada(AQUI/'evidencias/s1-render-11751-11900.json.xz')
        row=next(r for r in cap.d['rows'] if r['frame']==11754);m=cap.memory(row)
        before=m.ler_mundo(0x494000,0x8f000)
        effects=desenhar_jogo(m,habitado=lambda i:habitado(m,i))
        writes=[w for w in effects.escritas if 0x5099b4<=w[0]<0x50a9ba]
        self.assertEqual(writes,[(0x509b68,4,512),(0x509b6c,4,45),(0x509b70,4,544)])
        native=cap.blob(row['exit_dgroup'])
        for address,width,value in writes:
            self.assertNotEqual(int.from_bytes(m.ler_mundo(address,width),'little'),value)
            self.assertEqual(native[address-0x494000:address-0x494000+width],value.to_bytes(width,'little'))
        self.assertEqual(m.ler_mundo(0x494000,0x8f000),before)

    def test_complete_native_chained_window_and_normal_glyph_proofs(self):
        report=json.loads((AQUI/'validacao/s1-tardio-api112-final.json').read_text())
        self.assertEqual((report['equal'],report['expected'],report['compared']), (1250,1250,1250))
        self.assertEqual(report['world_unchanged_native_calls'],1250)
        self.assertFalse(report['shared_rng_cursor_changed'])
        for name,digest in report['sources_sha256'].items():self.assertEqual(sha((AQUI/name).read_bytes()),digest,name)
        self.assertTrue(all(c['first_difference'] is None for c in report['captures']))
        self.assertTrue(all(c['continued_from_previous_capture'] for c in report['captures'][1:]))
        for suffix,count in (('11251-11750',500),('11751-12500',750)):
            glyphs=json.loads((AQUI/f'validacao/s1-{suffix}-glifos-api112-final.json').read_text())
            self.assertEqual((glyphs['expected'],glyphs['equal']),(count,count))
            for name,digest in glyphs['sources_sha256'].items():self.assertEqual(sha((AQUI/name).read_bytes()),digest,name)
            self.assertTrue(all(r['equal'] and r['stop'] is None and r['pixel_mismatches']==0
                and r['raster_equal'] and not r['effect_mismatches'] for r in glyphs['rows']))

    def test_actual_alert_combat_death_fatigue_flames_and_recount_frames(self):
        groups={
            's1-render-part-11251-11378.json.xz':(11251,),
            's1-render-11751-11900.json.xz':(11754,11843,11846,11858),
            's1-render-11901-12000.json.xz':(12000,),
            's1-render-12001-12220.json.xz':(12024,12095,12179),
            's1-render-12221-12500.json.xz':(12460,12461,12475,12500)}
        catalog=CatalogoRastreado()
        for name,frames in groups.items():
            cap=CapturaLimitada(AQUI/'evidencias'/name)
            for frame in frames:
                row=next(r for r in cap.d['rows'] if r['frame']==frame);m=cap.memory(row)
                adapter=FronteiraTextoGravada(cap,row)
                with ArgumentosRasterM3(catalog) as raster:
                    result=renderizar_quadro(m,superficie_anterior=cap.blob(row['before']),cache=cap.cache_entry(row),
                        catalogo=catalog,hud=True,texto=adapter,habitado=lambda i:habitado(m,i),
                        relogio=lambda:int.from_bytes(cap.blob(row['exit_dgroup'])[0x4e17b4-0x494000:0x4e17b8-0x494000],'little'))
                self.assertIsNone(result.parada,(frame,result.parada))
                self.assertEqual(result.pixels,cap.blob(row['after']),frame)
                self.assertEqual(raster.calls,row['blits'],frame)
                self.assertFalse(adapter.pending,frame)

    def test_unproved_alert_wrapping_and_action_layout_stop_explicitly(self):
        from alertas_s1_graficos import message_box
        cap=CapturaLimitada(AQUI/'evidencias/s1-render-11751-11900.json.xz')
        row=next(r for r in cap.d['rows'] if r['frame']==11754);m=cap.memory(row)
        base=0x4e7754+518*m.u16(0x507d54)
        for patch,address in (({base+0x102:0,base+0x103:0},0x469d7f),({0x508f90:1},0x471830)):
            h=_Hud(LeituraHud(m,patch),cap.blob(row['before']),CatalogoRastreado(),False)
            with self.assertRaises(DependenciaQuadro) as error:message_box(h)
            self.assertEqual(error.exception.endereco,address)
