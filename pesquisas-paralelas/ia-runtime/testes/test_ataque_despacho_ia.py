"""State-1/24 table contract and the real S1 parent differential."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
import ambiente_ia_runtime  # noqa: F401
from inventario_ia_runtime import OriginalImage
from proxima_etapa_quadro import _trocar_estado, tabelas_imagem, SAIDA


class AttackDispatch(unittest.TestCase):
    def test_both_original_state_entries_use_the_void_owner_body(self):
        table = tabelas_imagem(OriginalImage())
        for state in (1, 24):
            with self.subTest(state=state):
                self.assertEqual(table['estados'][state], 0x456886)
                class Memory:
                    def u8(self, address):
                        if address != 0x123402:
                            raise AssertionError(hex(address))
                        return state
                calls = []
                p = {'EnginNextEtape:state1': lambda **kw: calls.append(kw)}
                self.assertEqual(_trocar_estado(Memory(), p, 17, 0x123400, table), SAIDA)
                self.assertEqual(calls, [dict(sitio=0x456886, unidade=17)])

    def test_native_parent_effects_and_handoffs_equal(self):
        report = json.loads((OWNED/'validacao/ataque-despacho-native.json').read_text())
        self.assertEqual((report['comparisons'], report['equal']), (1, 1))
        c, = report['cases']
        self.assertTrue(c['native_capture_reproduced'])
        self.assertTrue(c['handoffs_equal'])
        self.assertEqual(c['memory_differences'], [])
        self.assertEqual(c['original_changed_bytes'], 22)
        self.assertEqual(c['game_blocks_compared'], 25197)
        for name, digest in report['source_sha256'].items():
            self.assertEqual(hashlib.sha256((OWNED/name).read_bytes()).hexdigest(), digest)


if __name__ == '__main__':
    unittest.main()
