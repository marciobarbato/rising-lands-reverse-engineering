"""The Python CalculGame frame body against the Stage 1 original frame captures.

Each capture ran the intact CalculGame with every direct callee stubbed to a
declared return (``capturas-originais.json``). The skeleton is given exactly
those declared returns and fixture bytes and must reproduce the original call
order, call sites, argument registers, exit and CalculGame stores. The captures
stub CalculNextReflect and GameNextFrame, which the skeleton reproduces from
their bytes, so iaCalculPlayer's kernel calls (sites outside the frame body) and
the stores to 0x496d40 and the AI contexts are checked separately.
"""
import json
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
import ambiente_ia_runtime  # noqa: E402,F401
from memoria_ia_runtime import MemoriaDeclarada  # noqa: E402
from quadro_calcul_game import REGIOES_QUADRO, SAIDA_LIMPA, SAIDA_MENU_FIM, SAIDA_EPILOGO, calcular_quadro  # noqa: E402
from reinicio_ia import DependenciaIA  # noqa: E402

CAPTURES = json.loads((OWNED / 'evidencias/capturas-originais.json').read_text())
SCENARIOS = {s['scenario']: s for s in CAPTURES['scenarios']}
FRAME = ('frame_single_player', 'frame_music_flag_set_skips_cd_play', 'gate2_event_in_progress',
         'gate3_state_left_during_input', 'end_condition_counting', 'end_condition_mission6_first_frame',
         'end_condition_reached', 'network_frame_state_0x12')
REGISTERS = {'jogador': 'eax', 'faixa': 'eax', 'x': 'eax', 'mensagem': 'eax', 'missao': 'edx', 'edx': 'edx',
             'y': 'edx', 'duracao': 'edx', 'estado': 'edx', 'ecx': 'ecx'}
BODY = range(0x42d2de, 0x42d4f5)
KERNELS = ('iagUnitNoyau', 'iagVilleNoyau', 'iagRessNoyau', 'iagWarNoyau', 'iaSolver', 'AvanceMonstre',
           'iagUnitDeleteAllGroups')
BASE, SIZE = 0x494000, 0x8f000      # DGROUP+.bss: every frame global lies here


class Registro(MemoriaDeclarada):
    def __init__(self, *args):
        super().__init__(*args)
        self.escritas = {}

    def _acesso(self, largura, endereco, valor):
        resultado = super()._acesso(largura, endereco, valor)
        if valor is not None:
            self.escritas[endereco] = (largura, resultado)
        return resultado


def build(scenario):
    fixture = scenario['fixture']
    image = bytearray(SIZE)
    memory = Registro([(BASE, image)], REGIOES_QUADRO)
    for key, value in fixture['memory'].items():
        address = int(key.split()[0], 16)
        width = 4 if address == 0x4e061c else 1
        image[address - BASE:address - BASE + width] = value.to_bytes(width, 'little')
    returns = fixture['declared_returns']
    providers = {}

    def declared(name):
        def call(sitio, **arguments):
            if name == 'PlayerGetType':
                return returns['PlayerGetType'][str(arguments['jogador'])]
            if name == 'ProcessInputGame' and 'ProcessInputGame(3) stores 0x10' in fixture['note'] \
                    and arguments['jogador'] == 3:
                image[0x4e2f78 - BASE] = 0x10
            if name == 'MenuInit' and 'MenuInit effect' in fixture['note'] and arguments['jogador'] == image[0x508041 - BASE]:
                image[0x4e2f78 - BASE] = arguments['estado']
            return returns.get(name, returns['other direct callees'])
        return call

    names = {c[0] for s in FRAME for c in SCENARIOS[s]['calls']} | set(KERNELS)
    for name in names:
        providers[name] = declared(name)
    return memory, image, providers


class FrameSkeletonTests(unittest.TestCase):
    def test_skeleton_reproduces_original_frame_captures(self):
        for name in FRAME:
            with self.subTest(name):
                scenario = SCENARIOS[name]
                memory, image, providers = build(scenario)
                result = calcular_quadro(memory, providers)
                expected = [c for c in scenario['calls'] if int(c[2], 16) != 0x42c89e]   # prologue SetCursorPos
                got = [c for c in result['chamadas'] if c['sitio'] in BODY or c['sitio'] == 0x42c931]
                self.assertEqual([(c['rotina'], c['sitio']) for c in got],
                                 [(c[0], int(c[2], 16)) for c in expected])
                for mine, original in zip(got, expected):
                    registers = dict(zip(('eax', 'edx', 'ebx', 'ecx'), (int(v, 16) for v in original[3:7])))
                    for argument, register in REGISTERS.items():
                        if argument in mine:
                            self.assertEqual(mine[argument], registers[register], (mine, argument))
                stores = {int(a, 16): (w, int(last, 16)) for a, w, _, _, last, _, _ in scenario['stores']
                          if int(a, 16) != 0x49a010}        # prologue store
                mine = {a: v for a, v in memory.escritas.items()
                        if a != 0x496d40 and not 0x51a98c <= a < 0x51a9dc}
                self.assertEqual(mine, stores)
                self.assertEqual(image[0x4e2f78 - BASE], scenario['state_after'])
                self.assertEqual(int.from_bytes(image[0x4e061c - BASE:0x4e061c - BASE + 4], 'little'),
                                 scenario['end_counter_after'])
                self.assertEqual(image[0x5099b0 - BASE], scenario['flag_5099b0_after'])
                exit_ = {'gate2_event_in_progress': SAIDA_EPILOGO, 'end_condition_reached': SAIDA_MENU_FIM}
                self.assertEqual(result['saida'], exit_.get(name, SAIDA_LIMPA))

    def test_game_next_frame_and_ai_contexts_follow_their_bytes(self):
        memory, image, providers = build(SCENARIOS['frame_single_player'])
        image[0x496d40 - BASE:0x496d44 - BASE] = (0xffffffff).to_bytes(4, 'little')
        image[0x51a98c + 16 + 4 - BASE] = 1        # player 1 inactive: iaCalculPlayer returns without a call
        result = calcular_quadro(memory, providers)
        self.assertEqual(image[0x496d40 - BASE:0x496d44 - BASE], bytes(4))   # inc wraps
        inner = [(c['rotina'], c['sitio']) for c in result['chamadas'] if c['sitio'] not in BODY]
        self.assertEqual(inner, [('AvanceMonstre', 0x47f939), ('iaSolver', 0x47f945)])
        self.assertEqual(result['chamadas'][0]['rotina'], 'PlayerAttaqueReset')

    def test_missing_provider_is_a_named_dependency_with_retained_stores(self):
        memory, image, providers = build(SCENARIOS['frame_single_player'])
        del providers['CalculEnginNextEtape']
        with self.assertRaises(DependenciaIA) as raised:
            calcular_quadro(memory, providers)
        self.assertEqual((raised.exception.rotina, raised.exception.sitio), ('CalculEnginNextEtape', 0x42d3f5))
        self.assertEqual(image[0x4e1d18 - BASE], 1)
        self.assertEqual(image[0x496d40 - BASE], 1)

    def test_missing_ai_kernel_retains_the_counter_store(self):
        memory, image, providers = build(SCENARIOS['frame_single_player'])
        del providers['iagUnitNoyau']
        with self.assertRaises(DependenciaIA) as raised:
            calcular_quadro(memory, providers)
        self.assertEqual((raised.exception.rotina, raised.exception.sitio), ('iagUnitNoyau', 0x47f9df))
        self.assertEqual(image[0x51a98c + 16 + 9 - BASE], 1)     # 0x51a995 + 16: empty-cycle counter


if __name__ == '__main__':
    unittest.main()
