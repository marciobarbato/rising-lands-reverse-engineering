"""Economy's timer calls from the display run's real frame states (gate probe, frames 50..9000).

``capturar_temporizadores_sondagem_original`` was committed before this replay.
Its 14 inputs are the CalculGame-entry states the Mac mini probe saved
(``evidencias/sondagem-temporizadores-exibicao-9000.json.xz``), each rebuilt
over the display post-load state and checked against its summary. Python
replays every scenario (``test_temporizadores.reproduzir``): writes and
whole-state hash after every call, PlayerGetColor's EAX, and the market
state-3/4/5 branches as named dependencies where the original enters them.

The probe itself also shows, frame by frame, that from frame 1 to 9000 none
of Economy's gate inputs changes except the field-sweep row/flag and the
resource presentation in frames 1..5; that is asserted here too.
``RISING_EMULAR=1`` reruns the capture natively and requires it to equal the frozen file.
"""
import hashlib
import json
import lzma
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PASTA = Path(__file__).resolve().parents[1]
RAIZ = PASTA.parents[1]
sys.path.insert(0, str(PASTA))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import capturar_temporizadores_sondagem_original as ts  # noqa: E402
from test_campos_exibicao import Roteiro  # noqa: E402
from test_quadro_economia import Memoria  # noqa: E402
from test_quadro1_economia import base_cenario  # noqa: E402
from test_temporizadores import reproduzir  # noqa: E402

CAPTURA = PASTA / 'evidencias/captura-temporizadores-sondagem-original.json'
SHA_CAPTURA = '9cc0e7ba10d1b68425f91d3de434cd0b65884231a57e0b69fd6e58ad2c628b27'
SHA_SONDAGEM = '35dd6b014864806c993c34a14f1c36e9051e86fa0b17822002b001fb19337618'


def evidencia():
    return json.loads(CAPTURA.read_text())


class TemporizadoresSondagem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.estados = ts.estados(base_cenario('campos'))

    def test_frozen_capture_precedes_translation(self):
        r = evidencia()
        self.assertFalse(r['translation_executed'])
        self.assertEqual((r['original_entries'], r['returns'], r['dependency_stops']), (2179, 2144, 35))
        self.assertEqual(hashlib.sha256(CAPTURA.read_bytes()).hexdigest(), SHA_CAPTURA)
        self.assertEqual(r['inputs']['probe']['sha256'], SHA_SONDAGEM)
        self.assertEqual(hashlib.sha256(ts.SONDAGEM.read_bytes()).hexdigest(), SHA_SONDAGEM)

    def test_probe_gate_inputs_only_change_in_the_field_sweep_and_early_resources(self):
        r = json.loads(lzma.decompress(ts.SONDAGEM.read_bytes()))
        self.assertEqual((r['reproduction_frames_0_1'], r['code_unchanged'], r['frames_run']),
                         ({'load_tail': True, 'between_frames': True, 'frame1': True}, True, 9000))
        mudancas = {}
        for q in r['frames'][1:]:
            self.assertEqual(q['frame'], q['counter'])
            for n in q['changed']:
                mudancas.setdefault(n, []).append(q['frame'])
        self.assertEqual(set(mudancas), {'field_row_period', 'field_flag', 'resources'})
        self.assertEqual(mudancas['resources'], [1, 2, 3, 4, 5])

    def test_python_reproduces_every_probe_state(self):
        original = evidencia()['captures']
        total = 0
        for k, blocos in self.estados.items():
            roteiro = ts.cenarios(Roteiro(Memoria(blocos)), k)
            obs = [c for c in original if c['name'].startswith(f'sondagem{k}_')]
            n, lacunas = reproduzir(self, blocos, roteiro, obs)
            self.assertEqual(lacunas, 9 if k in ts.COMPLETOS else 0, k)
            total += n
        # 2,179 calls minus those after the 45 market-branch dependency points (9 per full-set state).
        self.assertEqual(total, 1849)


@unittest.skipUnless(os.environ.get('RISING_EMULAR'), 'set RISING_EMULAR=1 to rerun the original capture')
class DiferencialTemporizadoresSondagem(unittest.TestCase):
    def test_fresh_capture_equals_frozen(self):
        with tempfile.TemporaryDirectory(dir=RAIZ / '.local') as pasta:
            saida = Path(pasta) / 'captura.json'
            subprocess.run([sys.executable, '-B', str(PASTA / 'capturar_temporizadores_sondagem_original.py'),
                            '--output', str(saida)], check=True, cwd=RAIZ, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            self.assertEqual(json.loads(saida.read_text())['captures'], evidencia()['captures'])


if __name__ == '__main__':
    unittest.main()
