"""Type-1/type-8 unit bodies (render API 1.3) against the native capture of the M2.2 sequence.

Replays ``evidencias/captura-corpos-tipos1-8-m22-v2.json`` (original only, committed before this translation): every
real-state AffEngin call of units 11 (type 1) and 15 (type 8) in frames 1..6 and the 592-call record-byte matrix.  Each
case runs the frame's own AffEngin handler (``quadro_jogo``) over the native surface crop and compares the crop with
the original's, pixel for pixel (real states) or by SHA-256 (matrix).  No emulation.
"""
import base64, hashlib, json, struct, unittest, zlib
from pathlib import Path

from graficos import Catalogo, localizar
from quadro_jogo import _Composicao, EstadoTela, MundoQuadro, GLOBAIS_QUADRO, DependenciaQuadro
from construcoes import tabelas_jogador
from test_quadro_jogo import tabelas
from corpo_tipos1_8 import consultar_corpo_tipos1_8, CORPOS

AQUI = Path(__file__).resolve().parent
CAPTURA = AQUI/'evidencias/captura-corpos-tipos1-8-m22-v2.json'
CAPTURA_SHA256 = 'fd425b4405391020f6189ceab3263f0b81e4c559c6eaf484eb0b0d0ccc7c466c'   # evidence commit a5011bb (read-only)
LARGURA, ALTURA = 800, 600
sha = lambda d: hashlib.sha256(bytes(d)).hexdigest()
abrir = lambda b64: zlib.decompress(base64.b64decode(b64))
FUNDO = 0xA5   # pixels outside the native crop: must stay untouched


def _tela(globais):
    valores = {n: bytes(w) for n, a, w in GLOBAIS_QUADRO}
    valores['pitch_u32'] = struct.pack('<I', LARGURA); valores['altura_tela_u16'] = struct.pack('<H', ALTURA)
    valores['largura_tela_u16'] = struct.pack('<H', LARGURA)
    valores['camera_u8'] = bytes.fromhex(globais['camera_u8'])
    valores['selecionada_unidade_u16'] = bytes.fromhex(globais['selecionada_unidade_u16'])
    valores['modo_selecao_u8'] = bytes.fromhex(globais['modo_selecao_u8'])
    valores['recorte'] = bytes.fromhex(globais['recorte_u16x4'])
    return EstadoTela(valores)


def _mundo(indice, registro):
    unidades = bytearray(220800); unidades[indice*276:(indice+1)*276] = registro
    z = lambda n: bytes(n)
    return MundoQuadro(terreno=z(131072), objetos=z(65536), auxiliares=z(65536), regioes=z(131072), unidades=bytes(unidades),
                       projeteis=z(5600), descoberta=[z(65536)]*4, iluminacao=[z(65536)]*4)


def _colar(caixa, recorte):
    x0, y0, x1, y1 = caixa; w = x1-x0
    s = bytearray([FUNDO])*(LARGURA*ALTURA)
    for j in range(y1-y0): s[(y0+j)*LARGURA+x0:(y0+j)*LARGURA+x1] = recorte[j*w:(j+1)*w]
    return s


def _recortar(p, caixa):
    x0, y0, x1, y1 = caixa
    return b''.join(bytes(p[y*LARGURA+x0:y*LARGURA+x1]) for y in range(y0, y1))


def _fora_intacto(p, caixa):
    x0, y0, x1, y1 = caixa
    for y in range(ALTURA):
        linha = p[y*LARGURA:(y+1)*LARGURA]
        if y0 <= y < y1: linha = linha[:x0]+linha[x1:]
        if linha.count(FUNDO) != len(linha): return False
    return True


class CorposTipos1e8(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dados = CAPTURA.read_bytes()
        assert sha(dados) == CAPTURA_SHA256, 'native capture changed'
        cls.d = json.loads(dados)
        cls.catalogo = Catalogo(); cls.sombra, cls.ecl = tabelas(); cls.jogador = tabelas_jogador()

    def compor(self, alvo, registro, antes):
        mundo, tela = _mundo(alvo['unit'], registro), _tela(alvo['globals'])
        c = _Composicao(mundo, tela, _colar(alvo['crop_box'], antes), self.catalogo, None, self.sombra, self.ecl)
        c.tabelas_jogador = self.jogador
        c.engin(alvo['x'], alvo['y'], alvo['unit'])
        return c.saida

    def test_identidade_da_captura(self):
        d = self.d
        self.assertEqual(d['executable_sha256'], '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
        self.assertEqual(d['schema'], 'rising-lands/unit-body-types1-8-capture/1')
        self.assertTrue(all(f['end_hash_equals_recorded'] for f in d['rows']))
        self.assertEqual((d['native_calls'], d['matrix_calls']), (12, 592))

    def test_estados_reais_pixel_a_pixel(self):
        n = 0
        for f in self.d['rows']:
            for alvo in f['targets']:
                with self.subTest(frame=f['frame'], unit=alvo['unit']):
                    self.assertTrue(alvo['call']['returned'] and alvo['difference_inside_crop'] and alvo['call']['record_unchanged'])
                    self.assertEqual(alvo['call']['rng_before'], alvo['call']['rng_after'])
                    antes, depois = abrir(alvo['crop_before_zlib_base64']), abrir(alvo['crop_after_zlib_base64'])
                    saida = self.compor(alvo, bytes.fromhex(alvo['call']['record_hex']), antes)
                    self.assertEqual(_recortar(saida, alvo['crop_box']), depois)
                    self.assertTrue(_fora_intacto(saida, alvo['crop_box']))
                    n += 1
        self.assertEqual(n, 12)

    def test_matriz_nativa(self):
        n = 0
        for f in self.d['rows']:
            for alvo in f['targets']:
                if 'matrix' not in alvo: continue
                antes = abrir(alvo['crop_before_zlib_base64'])
                base = bytes.fromhex(alvo['call']['record_hex'])
                for caso in alvo['matrix']:
                    with self.subTest(unit=alvo['unit'], case=caso['name']):
                        self.assertTrue(caso['returned'] and caso['difference_inside_crop'] and caso['record_unchanged'])
                        registro = bytearray(base)
                        for o, v in caso['writes']:
                            o = int(o, 16); registro[o:o+len(bytes.fromhex(v))] = bytes.fromhex(v)
                        saida = self.compor(alvo, bytes(registro), antes)
                        self.assertEqual(sha(_recortar(saida, alvo['crop_box'])), caso['crop_after_sha256'])
                        n += 1
        self.assertEqual(n, 592)

    def test_camadas_iguais_aos_argumentos_nativos(self):
        """Shadow and body arguments equal the native PasteOmbreCmp/PasteBobCmp calls (matrix and real states)."""
        for f in self.d['rows']:
            for alvo in f['targets']:
                base = bytes.fromhex(alvo['call']['record_hex'])
                casos = [dict(writes=[], blits=alvo['call']['blits'])] + alvo.get('matrix', [])
                for caso in casos:
                    registro = bytearray(base)
                    for o, v in caso['writes']:
                        o = int(o, 16); registro[o:o+len(bytes.fromhex(v))] = bytes.fromhex(v)
                    g = alvo['globals']
                    plano = consultar_corpo_tipos1_8(bytes(registro), x=alvo['x'], y=alvo['y'], indice_u16=alvo['unit'],
                        camera_u8=int(g['camera_u8'], 16), indice_selecionado_u16=int.from_bytes(bytes.fromhex(g['selecionada_unidade_u16']), 'little'),
                        modo_selecao_u8=int(g['modo_selecao_u8'], 16))
                    nativo = [(b['routine'], b['x'], b['y'], b['id']) for b in caso['blits'][:2]]
                    meu = [('PasteOmbreCmp' if c['operacao'] == 'remapear_destino' else 'PasteBobCmp', c['x'], c['y'], c['id_motor'])
                           for c in plano['camadas']]
                    self.assertEqual(meu, nativo)

    def test_fora_do_dominio_para_nomeado(self):
        base = bytearray(bytes.fromhex(self.d['rows'][0]['targets'][0]['call']['record_hex']))   # unit 15, type 8
        kw = dict(x=288, y=416, indice_u16=15, camera_u8=0, indice_selecionado_u16=0xffff, modo_selecao_u8=0)
        for o, v in ((2, 14), (2, 1), (0, 1), (0x99, 3), (0xdc, 2), (0xba, 1), (0xbd, 1), (0xa5, 9), (0x91, 0), (0x91, 17), (0xa4, 10)):
            r = bytearray(base); r[o] = v
            with self.subTest(offset=hex(o), value=v), self.assertRaises(NotImplementedError):
                consultar_corpo_tipos1_8(bytes(r), **kw)
        with self.assertRaises(NotImplementedError): consultar_corpo_tipos1_8(bytes(base), **dict(kw, camera_u8=1))
        with self.assertRaises(NotImplementedError): consultar_corpo_tipos1_8(bytes(base), **dict(kw, indice_selecionado_u16=15))
        with self.assertRaises(NotImplementedError): consultar_corpo_tipos1_8(bytes(base), **dict(kw, modo_selecao_u8=1))
        with self.assertRaises(ValueError): consultar_corpo_tipos1_8(bytes(base[:275]), **kw)
        with self.assertRaises(TypeError): consultar_corpo_tipos1_8(bytes(base), x=0, y=0)
        alvo = self.d['rows'][0]['targets'][0]
        r = bytearray(base); r[2] = 14
        with self.assertRaises(DependenciaQuadro) as e:
            self.compor(alvo, bytes(r), abrir(alvo['crop_before_zlib_base64']))
        self.assertEqual(e.exception.endereco, 0x41591F)

    def test_proveniencia(self):
        p = json.loads((AQUI/'evidencias/corpo-tipos1-8.json').read_text())
        self.assertEqual(p['native_capture']['sha256'], CAPTURA_SHA256)
        self.assertEqual(p['executable_sha256'], self.d['executable_sha256'])
        self.assertEqual({k: (v['anchor'], int(v['body_base'].split()[0], 16)) for k, v in p['constants'].items() if k.startswith('type')},
                         {'type1': (list(CORPOS[1]['ancora']), CORPOS[1]['base']), 'type8': (list(CORPOS[8]['ancora']), CORPOS[8]['base'])})

    def test_ids_no_catalogo(self):
        for tipo, t in CORPOS.items():
            for d in range(1, 17):
                for fase in range(t['contagem']):
                    localizar(t['base'] + ((d+1)//2-1)*t['contagem'] + fase)


if __name__ == '__main__':
    unittest.main()
