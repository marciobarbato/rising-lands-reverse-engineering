"""AffGame HUD tail (render API 1.4) against the native capture captura-hud-m22-v2.json.

Each captured frame becomes a sparse memory holding exactly the bytes the original read after 0x417B1C (DGROUP and
arena reads-before-write); a read outside it fails.  The surface starts with the native checkpoint values at the
pixels the original wrote and a sentinel elsewhere: the Python tail must write the same pixels with the same values
and leave every other pixel untouched.  Blitter and Box arguments must equal the native ones in every frame.
"""
import base64, hashlib, json, os, struct, unittest, zlib
from pathlib import Path
from graficos import Catalogo
from hud_quadro import compor_hud, LeituraHud, ENDERECOS_PARADA
from quadro_jogo import DependenciaQuadro

AQUI = Path(__file__).resolve().parent
CAPTURA = Path(os.environ.get('HUD_CAPTURA', AQUI/'evidencias/captura-hud-m22-v2.json'))
SHA_CAPTURA = '94086e38b1d6d355b7793817674d2dda93d0ab8918abd82f77e74d370be5fed5'   # evidence commit 6f753ad
SENTINELA = 0xEE
sha = lambda d: hashlib.sha256(bytes(d)).hexdigest()


def _carregar():
    dados = CAPTURA.read_bytes()
    if 'HUD_CAPTURA' not in os.environ and sha(dados) != SHA_CAPTURA: raise ValueError('HUD capture hash mismatch')
    return json.loads(dados)


class MemoriaEsparsa:
    """MemoriaDeclarada over {address: byte}; any other address raises KeyError."""
    def __init__(self, bytes_):
        self.b = bytes_

    def ler_mundo(self, a, n):
        try: return bytes(self.b[a+i] for i in range(n))
        except KeyError as e: raise KeyError(f'HUD read outside the native read set: 0x{e.args[0]:08x}') from None

    def u8(self, a): return self.ler_mundo(a, 1)[0]
    def u16(self, a): return struct.unpack('<H', self.ler_mundo(a, 2))[0]
    def u32(self, a): return struct.unpack('<I', self.ler_mundo(a, 4))[0]


class Captura:
    def __init__(self):
        self.d = _carregar()
        self.blobs = self.d['blobs']

    def blob(self, chave, como_json=False):
        dados = zlib.decompress(base64.b64decode(self.blobs[chave]))
        if sha(dados)[:16] != chave: raise ValueError('blob hash mismatch')
        return json.loads(dados) if como_json else dados

    def memoria(self, linha):
        m = {}
        for ini, hexa, _ in self.blob(linha['dgroup_reads'], True)+self.blob(linha['arena_reads'], True)['values']:
            for i, v in enumerate(bytes.fromhex(hexa)): m[int(ini, 16)+i] = v
        for a, antigo, _ in linha['writes']: m.setdefault(int(a, 16), antigo)   # old values of the effects (not read)
        return MemoriaEsparsa(m)

    def chamadas_nativas(self, linha):
        """Blitter/Box calls of the native tail, in the Python call format."""
        saida = []
        for nome, _, eax, edx, ebx, ecx, pilha in self.blob(linha['routines'], True):
            i16 = lambda v: (v & 0xffff)-0x10000 if v & 0x8000 else v & 0xffff
            if nome == 'PasteBobCmp': saida.append(['PasteBobCmp', i16(eax), i16(edx), ebx & 0xffff, int(bool(ecx & 0xff))])
            elif nome == 'Box': saida.append(['Box', i16(eax), i16(edx), i16(ebx), i16(ecx), pilha[0] & 0xff, int(bool(pilha[1] & 0xff))])
        return saida


def _compor(cap, linha, catalogo, superficie):
    return compor_hud(LeituraHud(cap.memoria(linha)), superficie, catalogo=catalogo, evento=False)


class TestHudQuadro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cap = Captura()
        cls.catalogo = Catalogo()

    def test_capture_is_original_and_complete(self):
        d = self.cap.d
        self.assertEqual(d['executable_sha256'], '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
        self.assertEqual(len(d['rows']), 128)
        self.assertTrue(all(r['end_hash_equals_recorded'] and r['end_of_drawing_equals_end_of_phase'] for r in d['rows']))
        self.assertTrue(all(r['stop'] == '0x417d30' and not r['changed_outside_touched'] for r in d['rows']))

    def test_calls_equal_native_in_every_frame(self):
        for linha in self.cap.d['rows']:
            with self.subTest(frame=linha['frame']):
                mascara = self.cap.blob(linha['touched']['mask'])
                sup = bytes(SENTINELA if not t else 0 for t in mascara)
                r = _compor(self.cap, linha, self.catalogo, sup)
                py = [c for c in r['chamadas'] if c[0] in ('PasteBobCmp', 'Box')]
                self.assertEqual(py, self.cap.chamadas_nativas(linha))
                escritas = {int(a, 16): (v0, v1) for a, v0, v1 in linha['writes']}
                efeitos = {e[1]: e for e in r['efeitos']}
                for a in (0x49a042, 0x49a044):
                    if escritas.get(a, (0, 0))[0] != escritas.get(a, (0, 0))[1] or escritas.get(a+1, (0, 0))[0] != escritas.get(a+1, (0, 0))[1]:
                        novo = bytes([escritas.get(a, (0, 0))[1], escritas.get(a+1, (0, 0))[1]]).hex()
                        self.assertEqual(efeitos[a][3], novo)
                self.assertEqual({a for a, (v0, v1) in escritas.items() if v0 != v1} - {0x49a042, 0x49a043, 0x49a044, 0x49a045}, set())

    def test_pixels_equal_native_in_representative_frames(self):
        n = 0
        for linha in self.cap.d['rows']:
            t = linha['touched']
            if 'end_values' not in t: continue
            with self.subTest(frame=linha['frame']):
                mascara = self.cap.blob(t['mask'])
                idx = [i for i, v in enumerate(mascara) if v]
                antes, depois = self.cap.blob(t['checkpoint_values']), self.cap.blob(t['end_values'])
                sup = bytearray([SENTINELA])*len(mascara)
                for i, v in zip(idx, antes): sup[i] = v
                r = _compor(self.cap, linha, self.catalogo, bytes(sup))['superficie']
                self.assertEqual(bytes(r[i] for i in idx), depois)
                self.assertEqual(sum(1 for i, v in enumerate(mascara) if not v and r[i] != SENTINELA), 0)
                n += 1
        self.assertGreater(n, 0)

    def test_native_matrix(self):
        m = self.cap.d['matrix']
        base = {}
        linha = self.cap.d['rows'][0]
        base = dict(self.cap.memoria(linha).b)
        antes = {k: self.cap.blob(v) for k, v in m['crop_before'].items()}
        for caso in m['cases']:
            with self.subTest(case=caso['name']):
                self.assertIs(caso['returned'], True); self.assertEqual(caso['changed_outside_crop'], 0)
                mem = dict(base)
                for a, hexa in caso['writes']:
                    for i, v in enumerate(bytes.fromhex(hexa)): mem[int(a, 16)+i] = v
                x0, y0, x1, y1 = caso['crop']
                chave = 'counters' if caso['routine'] == 'AffCompteurMatiere' else 'minimap'
                sup = bytearray([SENTINELA])*(800*600)
                for y in range(y0, y1): sup[y*800+x0:y*800+x1] = antes[chave][(y-y0)*(x1-x0):(y-y0+1)*(x1-x0)]
                from hud_quadro import _Hud, CONTADORES
                h = _Hud(LeituraHud(MemoriaEsparsa(mem)), bytes(sup), self.catalogo, False)
                if chave == 'counters':
                    k = int(caso['registers']['EBX'], 16)
                    h.contador(k, *CONTADORES[k])
                else:
                    h.minimapa()
                saida = bytes(h.saida)
                recorte = b''.join(saida[y*800+x0:y*800+x1] for y in range(y0, y1))
                self.assertEqual(sha(recorte)[:16], caso['crop_after'])

    def test_provenance(self):
        p = json.loads((AQUI/'evidencias/hud-quadro.json').read_text())
        self.assertEqual(p['native_capture']['sha256'], SHA_CAPTURA)
        self.assertEqual(p['executable_sha256'], self.cap.d['executable_sha256'])

    def test_out_of_domain_branches_stop(self):
        linha = self.cap.d['rows'][0]
        mascara = self.cap.blob(linha['touched']['mask'])
        sup = bytes(len(mascara))
        casos = ((0x496204, b'\x01\x00', 0x417ba2), (0x4e2e7c, b'\x01', 0x4667a7), (0x507d56, b'\x01\x00', 0x469c5f),
                 (0x4e060c, b'\x01\x00\x00\x00', 0x40f8c0), (0x4e0618, b'\x10\x27', 0x40f77b), (0x496ac4, b'\x00\x00', 0x401d18))
        for endereco, valor, parada in casos:
            with self.subTest(address=hex(endereco)):
                mem = self.cap.memoria(linha)
                for i, v in enumerate(valor): mem.b[endereco+i] = v
                if endereco == 0x496204: mem.b.update({0x4e05ac: 0, 0x4e05ad: 0})  # unsupported marker ID
                if endereco == 0x496ac4: mem.b.update({0x49a0c8+i: 0 for i in range(276)})  # unsupported structure
                with self.assertRaises(DependenciaQuadro) as ctx:
                    compor_hud(LeituraHud(mem), sup, catalogo=self.catalogo, evento=False)
                self.assertEqual(ctx.exception.endereco, parada)
                self.assertIn(parada, ENDERECOS_PARADA)
        with self.assertRaises(DependenciaQuadro) as ctx:
            compor_hud(LeituraHud(self.cap.memoria(linha)), sup, catalogo=self.catalogo, evento=True)
        self.assertEqual(ctx.exception.endereco, 0x417c8a)


if __name__ == '__main__':
    unittest.main()
