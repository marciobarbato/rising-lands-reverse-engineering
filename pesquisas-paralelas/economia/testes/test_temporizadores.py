"""Economy's periodic branches (M2.3 prep) against the original-only timer capture.

``capturar_temporizadores_original`` was committed before this replay. Python
regenerates each scenario's declared steps over its own copy of the same
state (display post-load, or the M2.2 frame-128 checkpoint when that input is
present), runs the translated routine for every native call and compares, after
every call, every byte the original wrote (a mirror memory replays the native
writes) and, after every scenario, the whole-state hash.

Translated here: GetMeteo, MAJSympathie's event-counter branch (``0x47515d``),
PlayerAttaqueCalculSympa, PlayerInitAllianceCompteur (InitGameZone stays a named
dependency, as the native run stops there) and the market gates as loaded.
The market state-3 branch (``0x466e01``) and the proposition state-4/5 branches
(``0x466ed1``/``0x466fe1``) are still named dependencies: Core's display run
reaches none of them before frame 2,300 (EvalueCoutProposition, ResetMarche,
CalculValeur, ForgetMarche and MessageBoxSet unentered). For those scenarios
the test requires Python to raise at that branch on the call where the
original enters it, and compares everything before. BatimentNextEtape is AI/runtime's loop body; the capture
only records that it writes nothing on MONDE01's structure at any forced counter.
``RISING_EMULAR=1`` reruns the capture natively and requires it to equal the frozen file.
"""
import hashlib
import json
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
import capturar_temporizadores_original as t  # noqa: E402
import quadro_economia as q  # noqa: E402
from test_campos_exibicao import Roteiro  # noqa: E402
from test_quadro_economia import Memoria  # noqa: E402
from test_quadro1_economia import base_cenario  # noqa: E402

CAPTURA = PASTA / 'evidencias/captura-temporizadores-original.json'
COR_JOGADOR = 0x46003b
SHA_CAPTURA = '58349e4fae3892b48474a0eda735b348ac9932fe8ab1e5176b83481014bfe01d'
QUADROS128 = (RAIZ / t.ORIGEM_QUADROS128[1], RAIZ / '.local/m2-3' / Path(t.ORIGEM_QUADROS128[1]).name)


def evidencia():
    return json.loads(CAPTURA.read_text())


def entrada_quadro128():
    return next((p for p in QUADROS128 if p.exists()), None)


def executar(m, c):
    """The translated routine for one native call; returns ('return', None) or ('stop', named address)."""
    regs = {k: int(v, 16) for k, v in c['regs_in'].items()}
    entrada = int(c['entry'], 16)
    try:
        if entrada == t.METEO:
            q.calcular_meteo(m)
        elif entrada == t.MAJ:
            q.atualizar_simpatia(m, regs['EAX'], regs['EDX'], regs['EBX'])
        elif entrada == t.SYMPA:
            q.calcular_simpatia_ataques(m)
        elif entrada == t.ALLIANCE:
            q.contar_aliancas(m)
        elif entrada == t.MARCHE:
            q.calcular_contador_mercado(m, regs['EAX'])
        elif entrada == t.PROPOSITION:
            q.calcular_contador_proposicao(m, regs['EAX'], regs['EDX'])
        else:
            raise AssertionError(c['call'])
    except q.DependenciaQuadro as e:
        return 'stop', e.endereco
    return 'return', None


def comparar(teste, prefixo, blocos):
    original = [c for c in evidencia()['captures'] if c['name'].startswith(prefixo + '_')]
    return reproduzir(teste, blocos, t.cenarios(Roteiro(Memoria(blocos)), prefixo), original)


def reproduzir(teste, blocos, roteiro, original):
    """Replay ``roteiro`` (scenarios) over copies of ``blocos`` against the native ``original`` captures."""
    teste.assertEqual([r[0] for r in roteiro], [c['name'] for c in original])
    total = lacunas = 0
    for (nome, _, overrides, passos), obs in zip(roteiro, original):
        m, espelho = Memoria(blocos), Memoria(blocos)
        for a, dados in overrides:
            m.escrever(a, dados)
            espelho.escrever(a, dados)
        teste.assertEqual(m.sha(), obs['initial_state_sha256'], nome)
        chamadas = iter(obs['calls'])
        lacuna = False
        for passo in passos:
            if passo[0] in ('contador', 'escrever'):
                a, dados = (t.CONTADOR, passo[1].to_bytes(4, 'little')) if passo[0] == 'contador' else passo[1:]
                m.escrever(a, dados)
                espelho.escrever(a, dados)
                continue
            c = next(chamadas)
            rotulo = f'{nome}/{c["call"]}'
            if int(c['entry'], 16) == COR_JOGADOR:
                teste.assertEqual((c['outcome'], c['writes']), ('return', []), rotulo)
                teste.assertEqual(q.cor_jogador(m, int(c['regs_in']['EAX'], 16)), int(c['regs_out']['EAX'], 16), rotulo)
                total += 1
                continue
            if int(c['entry'], 16) == t.BATIMENT:
                teste.assertEqual((c['outcome'], c['writes']), ('return', []), rotulo)
                total += 1
                continue
            resultado, endereco = executar(m, c)
            if resultado == 'stop' and endereco in (0x466e01, 0x466ed1, 0x466fe1):
                # Untranslated market branch: Python stops at the branch the original enters here.
                lacuna = True
                lacunas += 1
                break
            teste.assertEqual((resultado, endereco), (c['outcome'], {'InitGameZone': 0x471830}.get(c['stop'])),
                              rotulo)
            for endereco_w, tamanho, valor in c['writes']:
                espelho.escrever(int(endereco_w, 16), valor.to_bytes(tamanho, 'little'))
            for endereco_w, tamanho, _ in c['writes']:
                a = int(endereco_w, 16)
                teste.assertEqual(m.ler(a, tamanho), espelho.ler(a, tamanho), f'{rotulo} at 0x{a:08x}')
            teste.assertEqual(m.sha(), espelho.sha(), rotulo)
            total += 1
        if not lacuna:
            teste.assertIsNone(next(chamadas, None), nome)
            teste.assertEqual(m.sha(), obs['final_state_sha256'], nome)
    return total, lacunas


class Temporizadores(unittest.TestCase):
    def test_frozen_capture_precedes_translation(self):
        r = evidencia()
        self.assertFalse(r['translation_executed'])
        self.assertEqual((r['returns'], r['dependency_stops']), (420, 14))
        self.assertEqual(hashlib.sha256(CAPTURA.read_bytes()).hexdigest(), SHA_CAPTURA)

    def test_python_reproduces_display_state_timers(self):
        total, lacunas = comparar(self, 'exibicao_s0', base_cenario('campos'))
        self.assertEqual(lacunas, 9)
        self.assertGreater(total, 150)

    @unittest.skipUnless(entrada_quadro128(), 'frame-128 input (Missions ad50ab2) not present on this checkout')
    def test_python_reproduces_frame128_timers(self):
        blocos, _ = t.blocos_quadro128(entrada_quadro128())
        total, lacunas = comparar(self, 'quadro128', blocos)
        self.assertEqual(lacunas, 9)
        self.assertGreater(total, 150)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') and entrada_quadro128(),
                     'set RISING_EMULAR=1 (and provide the frame-128 input) to rerun the original capture')
class DiferencialTemporizadores(unittest.TestCase):
    def test_fresh_capture_equals_frozen(self):
        with tempfile.TemporaryDirectory(dir=RAIZ / '.local') as pasta:
            saida = Path(pasta) / 'captura.json'
            subprocess.run([sys.executable, '-B', str(PASTA / 'capturar_temporizadores_original.py'),
                            '--quadros128', str(entrada_quadro128()), '--output', str(saida)], check=True, cwd=RAIZ,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            self.assertEqual(json.loads(saida.read_text())['captures'], evidencia()['captures'])


if __name__ == '__main__':
    unittest.main()
