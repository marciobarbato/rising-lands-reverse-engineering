import base64, json, struct, unittest, zlib
from pathlib import Path

import render_quadro as Q
from renderizar_quadro_original import Fixture, renderizar, comparar

EVID = Path(__file__).resolve().parent/'evidencias'
FIXTURE = EVID/'quadro-original-pixels-m1.json'
MODOS = EVID/'quadro-original-pixels-m1-modos.json'


class Memoria:
    """The MemoriaDeclarada read contract over fixture blocks (u8/u16/u32, ler_mundo); counts writes (there must be none)."""
    def __init__(self, fx):
        self.segmentos = [(Fixture.__dict__ and 0x494000, bytearray(fx.dgroup))]
        self.segmentos += [(int(b['base'], 16), bytearray(fx.blocos[n])) for n, b in fx.bruto['blocks'].items() if n != 'dgroup']

    def _seg(self, a, n):
        for base, dados in self.segmentos:
            if base <= a and a+n <= base+len(dados): return dados, a-base
        raise KeyError(hex(a))

    def ler_mundo(self, a, n):
        d, o = self._seg(a, n); return bytes(d[o:o+n])

    def u8(self, a): return self.ler_mundo(a, 1)[0]
    def u16(self, a): return struct.unpack('<H', self.ler_mundo(a, 2))[0]
    def u32(self, a): return struct.unpack('<I', self.ler_mundo(a, 4))[0]

    def definir(self, a, valor):   # test-side perturbation only
        d, o = self._seg(a, 1); d[o] = valor


def recorte(pixels, caixa, ymax=None):
    x0, y0, x1, y1 = caixa
    y1 = min(y1, ymax or y1)
    return b''.join(pixels[y*800+x0:y*800+x1] for y in range(y0, y1))


class QuadroTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fx = Fixture(FIXTURE)
        cls.modos = json.loads(MODOS.read_text())
        cls.habitado = lambda _, i: bool(cls.fx.bruto['habitation'][str(i)])

    def renderizar(self, mem=None):
        mem = mem or Memoria(self.fx)
        return Q.renderizar_quadro(mem, superficie_anterior=self.fx.antes, habitado=lambda i: bool(self.fx.bruto['habitation'][str(i)])), mem

    def test_api_matches_the_native_reference_up_to_the_first_unreconstructed_pass(self):
        # Render API 1.3: types 1 and 8 are composed, so the frame-1 checkpoint is complete and equal pixel for pixel.
        q, _ = self.renderizar()
        self.assertIsNone(q.parada)
        self.assertEqual(q.pixels, self.fx.referencia)
        self.assertEqual(len(q.rgba), 800*600*4)
        self.assertEqual(self.fx.bruto['habitation'], {'0': 1})

    def test_api_1_2_domain_stopped_at_unit_15(self):
        # Historical 1.2 behaviour, kept as a regression: without the type-1/8 bodies the first stop is unit 15 (type 8).
        import quadro_jogo as QJ
        tipos = dict(QJ.CORPOS_TIPOS1_8)
        QJ.CORPOS_TIPOS1_8.clear()
        try:
            q, _ = self.renderizar()
        finally:
            QJ.CORPOS_TIPOS1_8.update(tipos)
        self.assertEqual(q.parada['endereco'], '0x0041591f')
        self.assertIn('unit 15 type 8', q.parada['detalhe'])
        ref = self.fx.referencia
        dif = [i for i in range(len(ref)) if ref[i] != q.pixels[i]]
        self.assertTrue(dif and min(dif)//800 >= 279, (len(dif), min(dif)//800))   # terrain, vegetation and the facade equal

    def test_contract_shape(self):
        q, _ = self.renderizar()
        self.assertEqual((q.versao, q.largura, q.altura), (Q.VERSAO_RENDER_QUADRO, 800, 600))
        self.assertEqual(Q.VERSAO_RENDER_QUADRO, (1, 10))
        pal = Q.Catalogo().paleta()
        self.assertEqual(len(pal), 768)
        for i in (0, 4000, 123456, 479999):    # rgba = palette[index] expanded to RGB, alpha 255, row-major, origin top-left
            p = q.pixels[i]
            self.assertEqual(q.rgba[i*4:i*4+4], pal[p*3:p*3+3]+b'\xff')
        self.assertIsNone(q.parada)
        mem = Memoria(self.fx); mem.definir(0x49a0c8+5, 0)      # a structure mode outside the domain: parada is a dict
        self.assertEqual(sorted(Q.renderizar_quadro(mem, superficie_anterior=self.fx.antes, habitado=lambda i: True).parada), ['detalhe', 'endereco'])
        with self.assertRaises(ValueError):
            Q.renderizar_quadro(Memoria(self.fx), superficie_anterior=b'\0'*10)

    def test_units_with_the_tired_icon_equal_the_original_pixels(self):
        # Types 1 and 8 skipped here (API 1.1 view): every other unit, with its low-life icon, must match.
        import quadro_jogo as QJ
        original = QJ._Composicao.engin
        faltando = []

        def engin(c, x, y, indice):
            tipo = c.mundo.unidades[indice*276+1]
            if tipo in (1, 8):
                faltando.append((indice, tipo, x, y)); return
            return original(c, x, y, indice)
        QJ._Composicao.engin = engin
        try:
            q, _ = self.renderizar()
        finally:
            QJ._Composicao.engin = original
        self.assertIsNone(q.parada)
        self.assertEqual(sorted(faltando), [(11, 1, 224, 480), (15, 8, 288, 416)])
        ref = self.fx.referencia
        dif = [i for i in range(len(ref)) if ref[i] != q.pixels[i]]
        for i in dif:
            x, y = i % 800, i//800
            self.assertTrue(any(fx_-64 <= x < fx_+128 and fy_-128 <= y < fy_+64 for _, _, fx_, fy_ in faltando), (x, y))
        self.assertEqual(len(dif), 2080)
        icones = [c for c in q.chamadas if c[0] == 'EngineIconeFadiga']
        self.assertEqual(len(icones), 6)             # units 0, 1, 2 (type 0), 13, 14 (type 5), 12 (type 7)

    def test_tired_icon_native_capture(self):
        d = json.loads((EVID/'captura-cauda-engin-m1.json').read_text())
        nativos = [e for e in d['events'] if e['at'] == 'player_draw']
        self.assertEqual(len(nativos), 8)            # six drawn types plus types 1 and 8
        self.assertEqual({e['regs']['EBX'] for e in nativos}, {0x1e2f})     # word +4 (= 4) + 0x1E2B
        self.assertTrue(all(e['unit']['life74'] == 1 and e['unit']['w4'] == e['unit']['w76'] for e in nativos))
        self.assertEqual(sorted((e['regs']['EAX'], e['regs']['EDX']) for e in nativos if e['unit']['type'] in (0, 5, 7)),
                         sorted([(88, 277), (152, 309), (248, 309), (312, 309), (408, 309), (120, 373)]))

    def test_api_reads_only(self):
        mem = Memoria(self.fx)
        antes = [bytes(d) for _, d in mem.segmentos]
        self.renderizar(mem)
        self.assertEqual([bytes(d) for _, d in mem.segmentos], antes)

    def test_santuario_modes_3_4_5_equal_the_original_pixels(self):
        caixa = self.modos['box']
        for modo in (3, 4, 5):
            mem = Memoria(self.fx); mem.definir(0x49a0c8+5, modo)
            q, _ = self.renderizar(mem)
            nativo = zlib.decompress(base64.b64decode(self.modos['cases'][f'santuario_mode_{modo}']['crop_zlib_base64']))
            ymax = 279
            self.assertEqual(recorte(q.pixels, caixa, ymax), nativo[:(ymax-caixa[1])*(caixa[2]-caixa[0])], modo)
            self.assertEqual(self.modos['cases'][f'santuario_mode_{modo}']['pixels_changed_vs_base'], 0)

    def test_other_modes_stop_and_the_original_draws_one_common_other_body(self):
        crops = {}
        for modo in (0, 1, 2, 6, 7):
            mem = Memoria(self.fx); mem.definir(0x49a0c8+5, modo)
            q, _ = self.renderizar(mem)
            self.assertEqual(q.parada['endereco'], '0x00408ac8', modo)
            crops[modo] = self.modos['cases'][f'santuario_mode_{modo}']['crop_sha256']
        self.assertEqual(len(set(crops.values())), 1)
        self.assertNotEqual(next(iter(crops.values())), self.modos['cases']['santuario_mode_5']['crop_sha256'])

    def test_uninhabited_structure_requires_its_new_gray_input_region(self):
        mem = Memoria(self.fx)
        # The historical prefix fixture does not include the newly consumed [0x4E24C4] heap table.
        with self.assertRaises(KeyError):
            Q.renderizar_quadro(mem, superficie_anterior=self.fx.antes, habitado=lambda i: False)

    def test_missing_habitation_provider_stops(self):
        q = Q.renderizar_quadro(Memoria(self.fx), superficie_anterior=self.fx.antes)
        self.assertEqual(q.parada['endereco'], '0x0040f378')   # first footprint cell reaches the tail query


class SequenciaTest(unittest.TestCase):
    def test_initial_artifacts_are_bound_to_missions_capture(self):
        sup = json.loads((EVID/'superficie-inicial-m22-v2.json').read_text())
        tabela = json.loads((EVID/'superficies-fase-m22-v2.json').read_text())
        gravado = {p['phase']: p['offscreen'] for p in tabela['phases']}
        pixels = Q.carregar_superficie_inicial(EVID/'superficie-inicial-m22-v2.json')
        self.assertEqual(len(pixels), 480000)
        self.assertEqual(sup['sha256'], gravado['load_tail'])          # equals the capture's recorded load-tail surface hash
        self.assertEqual(sup['source_capture_sha256'], tabela['source_xz_sha256'])
        cache = Q.carregar_cache_inicial(EVID/'cache-terreno-inicial-m22-v2.json')
        self.assertEqual((len(cache.registros), len(cache.blocos_crus), cache.proximo), (1024, 256*1056, 76))

    def test_fixture_frame1_entry_surface_is_the_initial_artifact(self):
        fx = Fixture(FIXTURE)
        self.assertEqual(fx.antes, Q.carregar_superficie_inicial(EVID/'superficie-inicial-m22-v2.json'))

    def test_chain_verification_report(self):
        d = json.loads((EVID/'verificacao-cadeia-m22-v2.json').read_text())
        self.assertEqual(d['frames'], 12)
        self.assertEqual(d['first_stop']['endereco'], '0x0041591f')
        self.assertEqual(d['first_chained_difference_frame'], 1)
        for r in d['rows']:
            self.assertTrue(r['end_hash_equals_recorded'])          # native phase-end surface == Missions' recorded hash
            self.assertTrue(r['chain_cache_equals_native_entry_cache'])   # the carried cache equals the native cache at every frame
        for r in d['rows'][5:]:                                     # view scrolled out: only the bottom strip differs
            self.assertEqual(r['over_native_previous']['pixels'], 0)
            self.assertGreaterEqual(r['chained']['first_row'], 544)

    def test_chain_verification_report_api_1_3(self):
        # Native rerun after the type-1/8 bodies: no stop, every frame equals the original checkpoint over the native surface.
        d = json.loads((EVID/'verificacao-cadeia-m22-v2-api13.json').read_text())
        self.assertEqual((d['frames'], d['render_api_version'], d['first_stop']), (12, [1, 3], None))
        self.assertEqual(d['first_chained_difference_frame'], 2)    # the HUD strip (rows >= 547) of frame 1 onwards
        for r in d['rows']:
            self.assertTrue(r['end_hash_equals_recorded'] and r['chain_cache_equals_native_entry_cache'])
            self.assertTrue(r['over_native_previous']['equals_native_checkpoint'])
            self.assertIsNone(r['over_native_previous']['stop'])
            self.assertIsNone(r['chained']['stop'])
            if r['chained']['pixels']: self.assertGreaterEqual(r['chained']['first_row'], 544)

    def test_chain_verification_report_api_1_3_whole_playback(self):
        d = json.loads((EVID/'verificacao-cadeia-m22-v2-api13-128.json').read_text())
        self.assertEqual((d['frames'], d['render_api_version'], d['first_stop'], len(d['rows'])), (128, [1, 3], None, 128))
        for r in d['rows']:
            self.assertTrue(r['end_hash_equals_recorded'] and r['chain_cache_equals_native_entry_cache'])
            self.assertTrue(r['over_native_previous']['equals_native_checkpoint'])
            self.assertIsNone(r['chained']['stop'])
            if r['chained']['pixels']: self.assertGreaterEqual(r['chained']['first_row'], 544)

    def test_chain_verification_report_api_1_4_full_surface(self):
        # hud=True: the chained render is compared with the original's FULL end-of-phase surface (Missions' recorded hash).
        d = json.loads((EVID/'verificacao-cadeia-m22-v2-api14-128.json').read_text())
        self.assertEqual((d['frames'], d['render_api_version'], d['hud'], d['first_stop'], len(d['rows'])), (128, [1, 4], True, None, 128))
        self.assertIsNone(d['first_chained_difference_frame'])
        self.assertEqual(d['chained_equals_recorded_count'], 128)
        for r in d['rows']:
            self.assertTrue(r['end_hash_equals_recorded'] and r['chain_cache_equals_native_entry_cache'])
            self.assertTrue(r['chained_sha256_equals_recorded'] and r['chain_input_equals_native_previous'])
            self.assertTrue(r['over_native_previous']['equals_native_full_surface'] and r['chained']['equals_native_full_surface'])
            self.assertIsNone(r['chained']['stop'])

    def test_cache_state_is_carried(self):
        fx = Fixture(FIXTURE)
        q1 = Q.renderizar_quadro(Memoria(fx), superficie_anterior=fx.antes, habitado=lambda i: True)
        self.assertEqual(len(q1.cache.registros), 1024)
        q2 = Q.renderizar_quadro(Memoria(fx), superficie_anterior=q1.pixels, habitado=lambda i: True, cache=q1.cache)
        self.assertEqual(q2.cache.proximo, q1.cache.proximo)       # same viewport: every block hits
        with self.assertRaises(ValueError):
            Q.renderizar_quadro(Memoria(fx), superficie_anterior=fx.antes, cache=Q.EstadoCache(b'', b'', 0))


if __name__ == '__main__':
    unittest.main()
