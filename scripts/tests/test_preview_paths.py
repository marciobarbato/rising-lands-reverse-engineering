"""Package containment must compare resolved paths after workspace relocation."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[2] / 'apps/macos-preview/scripts/verificar_pacote.py'
spec = importlib.util.spec_from_file_location('preview_package', MODULE)
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackagePathTests(unittest.TestCase):
    def test_symlink_alias_and_real_path_resolve_inside_same_app(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            app = root / 'local-data/Preview.app'
            (app / 'Contents/Resources/Python').mkdir(parents=True)
            alias = root / 'dist';alias.symlink_to(app.parent, target_is_directory=True)
            runtime = {'prefix': str(app/'Contents/Resources/Python'),
                       'executable': str(alias/'Preview.app/Contents/Resources/Python/bin/python3')}
            self.assertTrue(package.runtime_inside_app(runtime, alias/'Preview.app'))
            runtime['prefix'] = str(root/'local-data/Preview.app-other/Python')
            self.assertFalse(package.runtime_inside_app(runtime, alias/'Preview.app'))
            self.assertFalse(package.runtime_inside_app({}, app))
