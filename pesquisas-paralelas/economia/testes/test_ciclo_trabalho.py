"""Work cycle, deposit and lodging credit over the original-first multi-frame capture.

- The capture is original-only, reproduces the display reference's frames 0/1, leaves the code unchanged, and
  shows the resource flow natively: the colonist hands the 0xc8 cave to player 0 (cave count 0 -> 1), then a
  lodged carrier and the two Ctrl-depot workers each credit one unit to player 0's totals.
- Every recorded call of a translated routine replays without a CPU from the bytes the original read before
  writing: exit registers, the final value of every changed byte, and each call into another front (name and
  argument bits). Deliberate mutations are caught; named dependencies raise instead of defaulting.
- The committed native differential is bound to the current translation.
- RISING_EMULAR=1 reruns the native differential (about 8 minutes).
"""
import hashlib
import json
import lzma
import os
from pathlib import Path
import struct
import subprocess
import sys
import unittest
from unittest import mock

PASTA = Path(__file__).resolve().parents[1]
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import ciclo_trabalho as ct  # noqa: E402
import replay_ciclo_trabalho as rp  # noqa: E402

RELATORIO = PASTA / 'validacao-ciclo-trabalho-emulada.json'
_CAP = {}


def captura():
    if 'c' not in _CAP:
        _CAP['c'] = json.loads(lzma.decompress(rp.CAPTURA.read_bytes()))
    return _CAP['c']


def totais(quadro):
    r = bytes.fromhex(quadro['resources_p0'])
    return tuple(struct.unpack_from('<H', r, 8 * k + 2)[0] for k in range(3))


class Captura(unittest.TestCase):
    def test_original_only_and_reproduced(self):
        c = captura()
        self.assertFalse(c['translation_executed'])
        self.assertEqual(c['reproduction'], dict(load_tail=True, between_frames=True, frame1=True, code_unchanged=True))
        self.assertEqual(c['original_sha256'], '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')

    def test_listings_are_the_intact_bytes(self):
        from extrair_ordens_economia import ler_pe
        try:
            ler = ler_pe()
        except (OSError, ValueError):
            self.skipTest('original executable not available')
        manifesto = json.loads((PASTA / 'evidencias/ciclo-trabalho/manifesto.json').read_text())
        for t in manifesto['intervals']:
            a, b = int(t['start'], 16), int(t['end_exclusive'], 16)
            self.assertEqual(hashlib.sha256(ler(a, b - a)).hexdigest(), t['sha256'], t['name'])

    def test_resource_flow(self):
        c = captura()
        q = {f['frame']: f for f in c['frames']}
        cave = str(c['cave'])
        primeiro = c['frames'][0]
        self.assertEqual(totais(primeiro), (0, 20, 24))                       # after the cave's 10/6
        self.assertEqual(primeiro['structures'][cave]['owner'], 0xc8)
        self.assertEqual(primeiro['cave_words_p0'][:4], '0000')               # no cave counted
        # The colonist's lodging hands the cave over and counts it: then credits reach the totals.
        dono = next(f for f in c['frames'] if f['structures'][cave]['owner'] == 0)
        self.assertEqual(dono['cave_words_p0'][:4], '0100')
        self.assertEqual(totais(dono), (0, 20, 24))
        creditos = [r for r in c['calls'] if r['routine'] == 'BatimentAjouteMatiere']
        self.assertGreaterEqual(len(creditos), 3)
        for r in creditos:
            self.assertEqual(int(r['entry_registers']['EDX'], 16) & 0xffff, 1)  # one unit per entry
        self.assertEqual(totais(c['frames'][-1])[1] - 20, sum(1 for r in creditos if int(r['entry_registers']['EAX'], 16) & 0xff == 1))
        self.assertEqual(totais(c['frames'][-1])[2] - 24, sum(1 for r in creditos if int(r['entry_registers']['EAX'], 16) & 0xff == 2))
        self.assertTrue(all(f['frame'] in q for f in c['frames']))

    def test_entry_gates(self):
        casos = {a['label']: [None] + [s['exit_registers']['EAX'] for s in a['steps']
                                       if s['label'].startswith('EnginSelectPeutEntrer')]
                 for a in captura()['actions'] if a['kind'] == 'case'}
        cave = captura()['cave']
        col = captura()['colonist']
        self.assertEqual(casos['selection [13] enters structure 0'][1], '0x1')           # troop -> own sanctuary
        self.assertEqual(casos[f'selection [13] enters structure {cave}'][1], '0x0')     # troop -> 0xc8 cave: refused
        self.assertEqual(casos[f'selection [{col}] enters structure {cave}'][1], '0x1')  # colonist -> 0xc8 cave
        self.assertEqual(casos[f'selection [13] enters structure {cave} (owner declared 0)'][1], '0x0')


class Replay(unittest.TestCase):
    def test_every_recorded_call_matches(self):
        contagem, falhas = rp.replay(captura())
        self.assertEqual(falhas, [])
        self.assertGreater(contagem['CalculWorkEngin']['match'], 50)
        self.assertGreaterEqual(contagem['BatimentLogeEngin']['match'], 2)

    def test_mutations_are_caught(self):
        c = captura()
        original = ct.CicloTrabalho._adicionar_bolsa
        try:
            ct.CicloTrabalho._adicionar_bolsa = lambda self, b, v: original(self, b, v + 1)
            _, falhas = rp.replay(c)
            self.assertTrue(any(f['routine'] == 'CalculWorkEngin' for f in falhas))
        finally:
            ct.CicloTrabalho._adicionar_bolsa = original
        with mock.patch.object(ct, 'BUSCA_UNIDADE', 0x496306):
            _, falhas = rp.replay(c)
            self.assertTrue(falhas)
        original_sair = ct.CicloTrabalho._sair_loge
        try:
            ct.CicloTrabalho._sair_loge = staticmethod(lambda regs, u, al: original_sair(regs, u, 1 - (al or 0)))
            _, falhas = rp.replay(c)
            self.assertTrue(any(f['routine'] == 'BatimentLogeEngin' for f in falhas))
        finally:
            ct.CicloTrabalho._sair_loge = original_sair

    def test_named_dependency_raises(self):
        r = next(x for x in captura()['calls'] if x['routine'] == 'CalculWorkEngin'
                 and any(c[1] == 'DeplaceEngin' for c in x['calls']))
        m = rp.MemoriaEsparsa(r['read_before_write'])
        regs = {k: int(v, 16) for k, v in r['entry_registers'].items()}
        with self.assertRaises(ct.DependenciaCicloTrabalho) as e:
            ct.CicloTrabalho(m)._CalculWorkEngin(regs)
        self.assertEqual(e.exception.rotina, 'DeplaceEngin')
        self.assertEqual(m.escritos, {})

    def test_outside_domain_raises_before_storing(self):
        r = next(x for x in captura()['calls'] if x['routine'] == 'CalculWorkEngin')
        m = rp.MemoriaEsparsa(r['read_before_write'])
        regs = {k: int(v, 16) for k, v in r['entry_registers'].items()}
        rec = m.u32(ct.PONTEIRO_UNIDADES) + ct.PASSO * (regs['EAX'] & 0xffff)
        m.u8(rec + 1, 6)
        escritos = dict(m.escritos)
        with self.assertRaises(ct.ForaDoDominioTrabalho):
            ct.CicloTrabalho(m)._CalculWorkEngin(regs)
        self.assertEqual(m.escritos, escritos)


class Nativo(unittest.TestCase):
    def test_report_bound_to_sources(self):
        if not RELATORIO.exists():
            self.skipTest('native report not generated')
        rel = json.loads(RELATORIO.read_text())
        self.assertEqual(rel['translation'], hashlib.sha256((PASTA / 'ciclo_trabalho.py').read_bytes()).hexdigest())
        self.assertEqual(rel['mismatches'], 0)
        self.assertTrue(rel['rerun_equals_capture'])

    @unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'native differential: set RISING_EMULAR=1')
    def test_native_differential(self):
        saida = RAIZ / '.local/validacao-ciclo-trabalho-teste.json'
        saida.parent.mkdir(exist_ok=True)
        p = subprocess.run([sys.executable, '-B', str(PASTA / 'validar_ciclo_trabalho.py'),
                            '--captura', str(rp.CAPTURA.relative_to(RAIZ)), '--saida', str(saida.relative_to(RAIZ))],
                           cwd=RAIZ, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-2000:] + p.stderr[-2000:])
        rel = json.loads(saida.read_text())
        self.assertEqual(rel['mismatches'], 0)
        self.assertTrue(rel['rerun_equals_capture'])


if __name__ == '__main__':
    unittest.main()
