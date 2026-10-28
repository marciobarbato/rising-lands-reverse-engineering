"""Guard the audio front against flat-module collisions.

Research modules are imported through flat ``sys.path`` entries, so every module
published by this front needs a basename that no other research module uses.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
OWNED = ROOT / 'pesquisas-paralelas/audio'
SIBLINGS = (ROOT / 'ferramentas', ROOT / 'pesquisas-paralelas/combate',
            ROOT / 'pesquisas-paralelas/economia', ROOT / 'pesquisas-paralelas/graficos-animacao',
            ROOT / 'pesquisas-paralelas/missoes', ROOT / 'pesquisas-paralelas/ia-runtime',
            ROOT / 'apps/macos-preview/src')


class NamespaceTests(unittest.TestCase):
    def test_owned_module_names_do_not_collide_with_sibling_fronts(self):
        for path in sorted(OWNED.glob('*.py')):
            for sibling in SIBLINGS:
                self.assertFalse((sibling / path.name).exists(),
                                 f'{path.name} collides with {sibling.relative_to(ROOT)}/{path.name}; choose a distinct basename')

    def test_contract_and_handoff_exist(self):
        self.assertTrue((ROOT / 'docs/AUDIO.md').is_file())
        self.assertTrue((OWNED / 'HANDOFF.md').is_file())


if __name__ == '__main__':
    unittest.main()
