"""This front's frame-0/1 routines against the committed isolated original captures, without emulation.

Each isolated capture (``captura-isolada-ia-quadro1.json``) lists the bytes the
original read before writing, with their entry values, and every changed byte.
The translation runs on a sparse memory that holds only those bytes. Reading
any other byte fails the test. The written bytes must equal the original's
changes. The full-state native differential is ``comparar_quadro1_ia.py``
(``validacao/m2-quadro1-composicao-ia.json``).
"""
import json
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
import ambiente_ia_runtime  # noqa: E402,F401
from inventario_ia_runtime import OriginalImage  # noqa: E402
from quadro_calcul_game import Quadro  # noqa: E402
from reinicio_ia import DependenciaIA  # noqa: E402
from rotinas_quadro_ia import TABELA_COMANDOS, avancar_monstros, calcular_caixa_mensagens, processar_entrada  # noqa: E402

CAPTURE = json.loads((OWNED / 'evidencias/captura-isolada-ia-quadro1.json').read_text())
VALIDATION = OWNED / 'validacao/m2-quadro1-composicao-ia.json'


class MemoriaEsparsa:
    def __init__(self, caso):
        self.bytes = {int(a, 16): v for a, v, _ in caso['read_before_write']}
        self.escritos = {}

    def _ler(self, a):
        if a in self.escritos:
            return self.escritos[a]
        if a not in self.bytes:
            raise AssertionError(f'read of 0x{a:x}, which the original did not read')
        return self.bytes[a]

    def _acesso(self, largura, a, valor):
        if valor is None:
            return sum(self._ler(a + i) << (8 * i) for i in range(largura))
        for i in range(largura):
            self.escritos[a + i] = (valor >> (8 * i)) & 0xff
        return valor & ((1 << (8 * largura)) - 1)

    def u8(self, a, v=None):
        return self._acesso(1, a, v)

    def u16(self, a, v=None):
        return self._acesso(2, a, v)

    def u32(self, a, v=None):
        return self._acesso(4, a, v)


def casos(rotina):
    for registro in CAPTURE['calls']:
        if registro['routine'] == rotina:
            yield registro['phase'], registro['cases'][0]


def esperado(caso):
    return sorted((int(a, 16), novo) for a, _, novo in caso['changed_bytes'])


def escritos_alterados(memoria, caso):
    """Python writes that change a byte. A byte the original neither read nor changed has an unknown
    entry value in the capture; a Python write there must not appear among the original changes and
    is checked by the full-state native differential instead."""
    antigos = {int(a, 16): velho for a, velho, _ in caso['changed_bytes']}
    antigos.update(memoria.bytes)
    return sorted((a, v) for a, v in memoria.escritos.items() if a in antigos and antigos[a] != v)


class RoutineCaptureTests(unittest.TestCase):
    def test_message_box_calcul(self):
        for fase, caso in casos('MessageBoxCalcul'):
            with self.subTest(fase):
                m = MemoriaEsparsa(caso)
                calcular_caixa_mensagens(m)
                self.assertEqual(escritos_alterados(m, caso), esperado(caso))

    def test_process_input_game_every_player(self):
        comandos = OriginalImage().table(TABELA_COMANDOS, 40)
        vistos = 0
        for fase, caso in casos('ProcessInputGame'):
            with self.subTest(fase=fase, eax=caso['entry_registers']['EAX']):
                m = MemoriaEsparsa(caso)
                eax = processar_entrada(m, int(caso['entry_registers']['EAX'], 16), comandos)
                self.assertEqual(eax, int(caso['exit_registers']['EAX'], 16))
                self.assertEqual(escritos_alterados(m, caso), esperado(caso))
                self.assertEqual(sorted(m.escritos), list(range(eax, eax + 10)))   # the whole record is stored
                vistos += 1
        self.assertEqual(vistos, 8)

    def test_inactive_players_and_monster_advance(self):
        for fase, caso in casos('CalculNextReflect'):
            jogador = int(caso['entry_registers']['EAX'], 16)
            with self.subTest(fase=fase, player=jogador):
                m = MemoriaEsparsa(caso)
                provedores = {'MissionGetNum': lambda sitio: m.u8(0x496fe4)}
                provedores['AvanceMonstre'] = lambda sitio, jogador: avancar_monstros(m, provedores)
                if jogador < 4:
                    self.assertEqual(Quadro(m, provedores).calcul_next_reflect(jogador, 1), 1)
                    self.assertEqual(m.escritos, {})
                    continue
                # iaSolver (Core's task machine over the whole pool) is covered natively;
                # here it is the named stop right after AvanceMonstre's effects.
                with self.assertRaises(DependenciaIA) as parada:
                    Quadro(m, provedores).calcul_next_reflect(jogador, 1)
                self.assertEqual((parada.exception.rotina, parada.exception.sitio), ('iaSolver', 0x47f945))
                self.assertEqual(escritos_alterados(m, caso), esperado(caso))

    def test_native_composition_report(self):
        report = json.loads(VALIDATION.read_text())
        s = report['summary']
        self.assertTrue(report['path_reproduction']['passed'])
        self.assertTrue(s['between_frames_equal'])
        self.assertEqual(s['load_tail'], dict(routine='RestoreAll', site='0x42d27f'))
        self.assertEqual(s['frame1'], dict(routine='InputGame', site='0x42d33b'))
        self.assertEqual(s['stops_equal_original_prefix'], dict(load_tail=True, frame1=True))
        self.assertEqual((s['isolated']['cases'], s['isolated']['equal']), (24, 22))
        self.assertEqual(report['source_dirty_paths'], [])


if __name__ == '__main__':
    unittest.main()
