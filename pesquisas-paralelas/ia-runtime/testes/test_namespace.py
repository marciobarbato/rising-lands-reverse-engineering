"""Guard the AI/runtime front against flat-module collisions and silent copies.

Research modules are imported through flat ``sys.path`` entries. The economy and
graphics ``construcoes`` collision showed that two different modules with one
basename corrupt a shared process. Every module published by this front must
therefore carry a basename that no other research module uses, and the front
must consume core's VM/task primitives instead of copying their bodies.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
OWNED = ROOT / 'pesquisas-paralelas/ia-runtime'
SIBLINGS = (ROOT / 'ferramentas', ROOT / 'pesquisas-paralelas/combate',
            ROOT / 'pesquisas-paralelas/economia', ROOT / 'pesquisas-paralelas/graficos-animacao',
            ROOT / 'pesquisas-paralelas/missoes', ROOT / 'apps/macos-preview/src')
# Core-owned primitives the front composes; their bodies must not be duplicated here.
CORE_PRIMITIVES = ('ia.py', 'tarefas_ia.py', 'simbolos_ia.py', 'ordens_unidades.py',
                   'mensagens_chegada.py', 'cadencia.py', 'avanco_unidades.py')


def owned_modules():
    return sorted(path.name for path in OWNED.glob('*.py'))


class NamespaceTests(unittest.TestCase):
    def test_owned_module_names_do_not_collide_with_sibling_fronts(self):
        for name in owned_modules():
            for sibling in SIBLINGS:
                self.assertFalse((sibling / name).exists(),
                                 f'{name} collides with {sibling.relative_to(ROOT)}/{name}; choose a distinct basename')

    def test_core_primitives_are_not_copied(self):
        for name in CORE_PRIMITIVES:
            self.assertTrue((ROOT / 'ferramentas' / name).exists(), name + ' must remain core-owned')
            self.assertFalse((OWNED / name).exists(), name + ' must be consumed from ferramentas, not copied')

    def test_contract_and_handoff_exist(self):
        self.assertTrue((ROOT / 'docs/AI_RUNTIME.md').is_file())
        self.assertTrue((OWNED / 'HANDOFF.md').is_file())


if __name__ == '__main__':
    unittest.main()
