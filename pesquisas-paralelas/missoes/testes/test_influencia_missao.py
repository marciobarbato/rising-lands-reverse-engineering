"""Influence-zone queries against the original captures at the exact MONDE01 frame-1 inputs.

CPU-free: the captured table bytes are replayed through the translation for
all 65,536 cells, the 256 high-EAX calls and the 400 zone records, and the
results must equal the native EAX arrays.  The native differential over
perturbed tables is the committed report checked at the end.
"""
import base64
import json
from pathlib import Path
import struct
import sys
import unittest
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ambiente_missoes
from influencia_missao import canto_zona_influencia, zona_influencia

CAPTURA = ambiente_missoes.OWNED/'evidencias/captura-influencia-quadro1.json'
DIFERENCIAL = ambiente_missoes.OWNED/'validacao/m2-influencia-differential-x86.json'


def matriz(compacto):
    dados = zlib.decompress(base64.b64decode(compacto['zlib_base64']))
    return list(struct.unpack('<%d%s' % (compacto['count'], compacto['format']), dados))


@unittest.skipUnless(CAPTURA.exists(), 'Influence capture not committed')
class TestCapturaInfluencia(unittest.TestCase):
    def setUp(self):
        self.linha = json.loads(CAPTURA.read_bytes())['injections'][0]
        self.tabela = bytearray(zlib.decompress(base64.b64decode(self.linha['table_zlib_base64'])))

    def test_every_cell_matches(self):
        nativo = matriz(self.linha['case_get_zone_influence'])
        self.assertEqual([zona_influencia(self.tabela, c) for c in range(65536)], nativo)

    def test_high_eax_bits_are_ignored_like_the_original(self):
        for celula, eax in self.linha['high_eax_bits']:
            self.assertEqual(zona_influencia(self.tabela, 0xabcd0000 | int(celula, 16)), int(eax, 16))

    def test_every_zone_corner_matches(self):
        nativo = matriz(self.linha['top_left'])
        self.assertEqual([canto_zona_influencia(self.tabela, z) for z in range(400)], nativo)


class TestContratos(unittest.TestCase):
    def test_view_and_domain_guards(self):
        with self.assertRaises(ValueError):
            zona_influencia(bytearray(3999), 0)
        with self.assertRaises(ValueError):
            canto_zona_influencia(bytearray(4000), 400)

    def test_record_255_is_skipped(self):
        t = bytearray(b'\xff'*4000)
        t[2550:2558] = bytes(8)          # record 255 = (0,0)-(0,0)
        self.assertEqual(zona_influencia(t, 0), 0xff)
        t[2560:2568] = bytes(8)          # record 256
        self.assertEqual(zona_influencia(t, 0), 256)

    @unittest.skipUnless(DIFERENCIAL.exists(), 'Native differential not committed')
    def test_committed_native_differential_passed(self):
        rel = json.loads(DIFERENCIAL.read_bytes())
        self.assertTrue(rel['passed'])
        self.assertEqual(rel['differing'], [])


if __name__ == '__main__':
    unittest.main()
