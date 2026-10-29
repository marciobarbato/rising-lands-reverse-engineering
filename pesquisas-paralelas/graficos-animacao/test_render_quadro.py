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
        q, _ = self.renderizar()
        self.assertEqual(q.parada['endereco'], '0x0041591f')            # units with life < 100: overlay not reconstructed
        ref = self.fx.referencia
        dif = [i for i in range(len(ref)) if ref[i] != q.pixels[i]]
        self.assertTrue(dif and min(dif)//800 >= 279, (len(dif), min(dif)//800))   # terrain, vegetation and the facade equal
        self.assertEqual(len(q.rgba), 800*600*4)
        self.assertEqual(self.fx.bruto['habitation'], {'0': 1})

    def test_contract_shape(self):
        q, _ = self.renderizar()
        self.assertEqual((q.versao, q.largura, q.altura), (Q.VERSAO_RENDER_QUADRO, 800, 600))
        self.assertEqual(Q.VERSAO_RENDER_QUADRO, (1, 0))
        pal = Q.Catalogo().paleta()
        self.assertEqual(len(pal), 768)
        for i in (0, 4000, 123456, 479999):    # rgba = palette[index] expanded to RGB, alpha 255, row-major, origin top-left
            p = q.pixels[i]
            self.assertEqual(q.rgba[i*4:i*4+4], pal[p*3:p*3+3]+b'\xff')
        self.assertEqual(sorted(q.parada), ['detalhe', 'endereco'])
        with self.assertRaises(ValueError):
            Q.renderizar_quadro(Memoria(self.fx), superficie_anterior=b'\0'*10)

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

    def test_uninhabited_structure_stops(self):
        mem = Memoria(self.fx)
        q = Q.renderizar_quadro(mem, superficie_anterior=self.fx.antes, habitado=lambda i: False)
        self.assertEqual(q.parada['endereco'], '0x0040892d')

    def test_missing_habitation_provider_stops(self):
        q = Q.renderizar_quadro(Memoria(self.fx), superficie_anterior=self.fx.antes)
        self.assertEqual(q.parada['endereco'], '0x0040f378')   # first footprint cell reaches the tail query


if __name__ == '__main__':
    unittest.main()
