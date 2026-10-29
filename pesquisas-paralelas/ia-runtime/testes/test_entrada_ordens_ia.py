"""M3.1 input path: CPU-free replay of every captured case, the scripted-input reader, and the native differential.

The replay runs ``entrada_ordens_ia`` with the committed owners (``provedores_entrada_ia``) over a sparse memory
holding the case-entry bytes recorded by the native differential (``evidencias/leituras-entrada-ordens-ia.json.xz``:
the bytes the original read and the original value of every byte the translation touched, as the union of all
cases plus each case's own values). Every other address is absent, so a translation that touches an unrecorded
byte fails. Without Core's ``construcao_core`` on the import path, the BatimentPosable cases must stop at that
named dependency. Each case must reproduce the
captured exit registers, changed bytes, sound requests and key answers, or stop at the dependency the native
differential reported.
"""
import json
import os
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
import ambiente_ia_runtime  # noqa: E402,F401
from reinicio_ia import DependenciaIA  # noqa: E402

CAPTURA = OWNED / 'evidencias/captura-entrada-ordens-ia.json'
LEITURAS = OWNED / 'evidencias/leituras-entrada-ordens-ia.json.xz'
RELATORIO = OWNED / 'validacao/entrada-ordens-native.json'


class Ausente(KeyError):
    pass


class MemoriaEsparsa:
    """u8/u16/u32/vista/ler over recorded bytes in 16 MiB chunks (views share storage); an unrecorded address
    raises ``Ausente``."""
    PEDACO = 1 << 24

    def __init__(self, bytes_):
        self.dados, self.conhecidos, self.original = {}, {}, dict(bytes_)
        for a, v in bytes_.items():
            d, k = self._pedaco(a)
            d[a % self.PEDACO], k[a % self.PEDACO] = v, 1
        self.inicial = {c: bytes(d) for c, d in self.dados.items()}

    def _pedaco(self, a):
        c = a // self.PEDACO
        if c not in self.dados:
            self.dados[c], self.conhecidos[c] = bytearray(self.PEDACO), bytearray(self.PEDACO)
        return self.dados[c], self.conhecidos[c]

    def _verificar(self, a, n):
        if a // self.PEDACO != (a + n - 1) // self.PEDACO:
            raise Ausente(f'0x{a:x}+{n} crosses a replay chunk')
        d, k = self._pedaco(a)
        o = a % self.PEDACO
        if not all(k[o:o + n]):
            raise Ausente(hex(a + k[o:o + n].index(0)))
        return d, o

    def _acesso(self, n, a, v):
        if v is None:
            d, o = self._verificar(a, n)
            return int.from_bytes(d[o:o + n], 'little')
        d, k = self._pedaco(a)
        o = a % self.PEDACO
        v &= (1 << 8 * n) - 1
        d[o:o + n] = v.to_bytes(n, 'little')
        k[o:o + n] = b'\x01' * n
        return v

    def u8(self, a, v=None):
        return self._acesso(1, a, v)

    def u16(self, a, v=None):
        return self._acesso(2, a, v)

    def u32(self, a, v=None):
        return self._acesso(4, a, v)

    def vista(self, a, n):
        d, o = self._verificar(a, n)
        return memoryview(d)[o:o + n]

    def ler(self, a, n):
        d, o = self._verificar(a, n)
        return bytes(d[o:o + n])

    def mudancas(self):
        """[address, old, new] of every recorded byte whose value changed (a write to an unrecorded byte is
        reported with old None, so it can never match a native change silently)."""
        saida = []
        for c, d in self.dados.items():
            ini = self.inicial.get(c, bytes(self.PEDACO))
            for b in range(0, self.PEDACO, 4096):
                if d[b:b + 4096] == ini[b:b + 4096] and (c in self.inicial or not any(self.conhecidos[c][b:b + 4096])):
                    continue
                for o in range(b, b + 4096):
                    a = c * self.PEDACO + o
                    if a in self.original:
                        if self.original[a] != d[o]:
                            saida.append([hex(a), self.original[a], d[o]])
                    elif self.conhecidos[c][o]:
                        saida.append([hex(a), None, d[o]])
        return sorted(saida, key=lambda x: int(x[0], 16))


def _bytes(runs, saida=None):
    saida = {} if saida is None else saida
    for inicio, dados in runs:
        base = int(inicio, 16)
        for i in range(len(dados) // 2):
            saida[base + i] = int(dados[2 * i:2 * i + 2], 16)
    return saida


@unittest.skipUnless(LEITURAS.exists() and RELATORIO.exists(), 'native differential not recorded yet')
class ReplayCasos(unittest.TestCase):
    """Every captured case replays from its recorded bytes to the captured result."""

    @classmethod
    def setUpClass(cls):
        from validar_entrada_ordens_ia import comandos_imagem
        cls.captura = json.loads(CAPTURA.read_bytes())
        import lzma
        cls.leituras = json.loads(lzma.decompress(LEITURAS.read_bytes()))
        cls.base = _bytes(cls.leituras['base'])
        cls.relatorio = json.loads(RELATORIO.read_bytes())
        cls.comandos = comandos_imagem()

    def test_every_case(self):
        from validar_entrada_ordens_ia import REGISTROS, comparar_resultado, executar_traducao
        from provedores_entrada_ia import construcao_core
        dependencias = {d['case']: d['dependency'] for d in self.relatorio['dependency_stops']}
        posavel_ausente = construcao_core(None) is None
        posaveis = {c['case'] for c in self.captura['cases'] if any('|BatimentPosable|' in x for x in c['calls'])}
        self.assertEqual(self.relatorio['mismatches'], [])
        self.assertEqual(self.leituras['capture']['sha256'], self.relatorio['capture']['sha256'])
        for caso in self.captura['cases']:
            with self.subTest(caso=caso['case']):
                declarado = dict(caso, keys=[[c[1], c[2]] for c in caso['declared_keys_consumed']],
                                 stack=[int(w, 16) for w in caso['stack_words']])
                m = MemoriaEsparsa(_bytes(self.leituras['cases'][caso['case']], dict(self.base)))
                entrada = {k: int(caso['entry_registers'][k], 16) for k in REGISTROS}
                alocacoes = [int(c.split('|')[4], 16) for c in caso['calls'] if c.split('|')[1] == 'MemAlloc']
                if caso['case'] in dependencias or (posavel_ausente and caso['case'] in posaveis):
                    with self.assertRaises(DependenciaIA) as erro:
                        executar_traducao(m, declarado, entrada, self.leituras['cursor'], alocacoes, self.comandos)
                    esperado = dependencias.get(caso['case']) or 'BatimentPosable required at 0x0042a002; earlier stores retained'
                    self.assertEqual(str(erro.exception), esperado)
                    continue
                saida, pedidos, teclas = executar_traducao(m, declarado, entrada, self.leituras['cursor'], alocacoes,
                                                           self.comandos)
                mudancas = m.mudancas()
                r = comparar_resultado(declarado, caso, saida, pedidos, teclas, mudancas)
                self.assertTrue(r['ok'], {k: v for k, v in r.items() if k not in ('case', 'routine')})


class Roteiro(unittest.TestCase):
    """The scripted-input reader holds the cursor, queues each frame's messages and answers keys by vkey."""

    def test_reader(self):
        from composicao_entrada_ia import RoteiroEntrada
        r = RoteiroEntrada(dict(schema='rising-lands/monde01-scripted-input/1', start=dict(frame=128), stop_frame=140,
                                frames=[dict(frame=130, cursor=[560, 528], messages=[[512, 0, 34603568]]),
                                        dict(frame=131, messages=[[513, 1, 34603568]], keys={'0x26': -32768})]))
        r.iniciar_quadro(129)
        self.assertEqual((r.peek(), r.cursor()), (None, (0, 0)))
        r.iniciar_quadro(130)
        self.assertEqual(r.peek(), (512, 0, 34603568))
        self.assertEqual(r.get(), (512, 0, 34603568))
        self.assertEqual(r.cursor(), (560, 528))
        r.iniciar_quadro(131)
        self.assertEqual((r.tecla(0x26), r.tecla(0x25), r.cursor()), (0x8000, 0, (560, 528)))
        with self.assertRaises(RuntimeError):
            r.iniciar_quadro(132)
        with self.assertRaises(ValueError):
            RoteiroEntrada(dict(schema='x', start=dict(frame=128), stop_frame=129))


def _sonda_disponivel(ref='f058844'):
    import subprocess
    return subprocess.run(['git', '-C', str(OWNED.parents[1]), 'cat-file', '-e', f'{ref}^{{commit}}'],
                          capture_output=True).returncode == 0


@unittest.skipUnless(_sonda_disponivel(), 'Missions probe commit f058844 not fetched')
class CadeiaSondaP1(unittest.TestCase):
    """The chain replays P1's input from frame 128 and equals the probe through the selection click (tag 1 at 133)."""

    def test_p1_first_frames(self):
        import subprocess
        raiz = OWNED.parents[1]
        saida = '.local/entrada/teste-p1.json'
        p = subprocess.run([sys.executable, '-B', str(OWNED / 'provar_entrada_ia.py'), '--sonda', 'P1', '--ref',
                            'f058844', '--quadros', '8', '--saida', saida], cwd=raiz, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr[-2000:])
        r = json.loads((raiz / saida).read_bytes())
        self.assertEqual((r['frames_equal'], r['stop'], r['first_difference']), (8, None, None))
        self.assertEqual([(o['frame'], o['tag'], o.get('word2'), o.get('word4')) for o in r['orders_python']
                          if o.get('event') != 'ProcessInputGame'], [(133, 1, 4113, 4113)])


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'native differential: set RISING_EMULAR=1')
class Nativo(unittest.TestCase):
    def test_native_differential(self):
        import subprocess
        raiz = OWNED.parents[1]
        saida = '.local/entrada/teste-nativo.json'
        argumentos = [sys.executable, '-B', str(OWNED / 'validar_entrada_ordens_ia.py'), '--saida', saida]
        nucleo = os.environ.get('RISING_NUCLEO_REF')
        if nucleo:
            argumentos += ['--nucleo-ref', nucleo]
        p = subprocess.run(argumentos, cwd=raiz, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-2000:] + p.stderr[-2000:])
        r = json.loads((raiz / saida).read_bytes())
        self.assertEqual((r['mismatches'], r['comparisons']), ([], len(json.loads(CAPTURA.read_bytes())['cases'])))


if __name__ == '__main__':
    unittest.main()
