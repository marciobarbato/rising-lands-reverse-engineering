"""PlayerGetColor (first entered at frame 9000) against its original-only capture.

``capturar_cor_jogador_original`` was committed before this replay. Every AL,
with EAX upper bits 0 and 0xabcd12, from the display post-load state and the
M2.2 frame-128 checkpoint (when that input is present), counter 9000:
``quadro_economia.cor_jogador`` and the ``PlayerGetColor`` provider must return
the original EAX, and the original writes nothing.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import capturar_temporizadores_original as t  # noqa: E402
import quadro_economia as q  # noqa: E402
from test_quadro_economia import Memoria, Provedores  # noqa: E402
from test_quadro1_economia import MemoriaPalavras, base_cenario  # noqa: E402
from test_temporizadores import entrada_quadro128  # noqa: E402

CAPTURA = PASTA / 'evidencias/captura-cor-jogador-original.json'
SHA_CAPTURA = 'de089fd4be163627b18dd689fb6550df6a4e1ceacc129123e570918d10e4aa3b'


def comparar(teste, prefixo, blocos):
    from bonus_unidades import BonusUnidades
    from provedores_economia_quadro import provedores_economia_quadro
    obs = next(c for c in json.loads(CAPTURA.read_text())['captures'] if c['name'] == f'{prefixo}_all_players')
    m = Memoria(blocos)
    teste.assertEqual(m.sha(), obs['initial_state_sha256'])
    m.escrever(t.CONTADOR, struct.pack('<I', 9000))
    prov = provedores_economia_quadro(MemoriaPalavras(m), bonus=BonusUnidades.da_memoria(m),
                                      producao=Provedores(m).producao)
    for c in obs['calls']:
        eax = int(c['regs_in']['EAX'], 16)
        esperado = int(c['regs_out']['EAX'], 16)
        teste.assertEqual((c['outcome'], c['writes']), ('return', []), c['call'])
        teste.assertEqual(q.cor_jogador(m, eax), esperado, c['call'])
        teste.assertEqual(prov['PlayerGetColor'](sitio=0, jogador=eax), esperado, c['call'])
    teste.assertEqual(m.sha(), obs['final_state_sha256'])
    return len(obs['calls'])


class CorJogador(unittest.TestCase):
    def test_frozen_capture_precedes_translation(self):
        r = json.loads(CAPTURA.read_text())
        self.assertFalse(r['translation_executed'])
        self.assertEqual((r['original_entries'], r['returns']), (1024, 1024))
        self.assertEqual(hashlib.sha256(CAPTURA.read_bytes()).hexdigest(), SHA_CAPTURA)

    def test_display_state(self):
        self.assertEqual(comparar(self, 'exibicao_s0', base_cenario('campos')), 512)

    @unittest.skipUnless(entrada_quadro128(), 'frame-128 input (Missions ad50ab2) not present on this checkout')
    def test_frame128_state(self):
        self.assertEqual(comparar(self, 'quadro128', t.blocos_quadro128(entrada_quadro128())[0]), 512)


if __name__ == '__main__':
    unittest.main()
