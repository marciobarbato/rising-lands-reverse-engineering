"""Read-only adapters to unchanged Economy habitation predicates, loaded by path.

Only pure read methods are compiled, avoiding Economy/Graphics flat-name
collisions. There are no constructor defaults, mutable world or callbacks.
"""
import ast
from functools import lru_cache
from pathlib import Path
import struct
from types import SimpleNamespace, MethodType
from macos_state_consumer import StateValidationError


@lru_cache(maxsize=4)
def _read_contract(root):
    folder = Path(root) / 'pesquisas-paralelas/economia'
    namespace = dict(struct=struct)
    selections = {
        'construcoes.py': ('PASSO_CONSTRUCAO',),
        'recrutamento.py': ('_word', '_offset'),
        'limpeza_saida.py': ('bag_vide', '_TIPOS_EXCLUIDOS_BAG_VIDE', 'bag_contient_troupe'),
        'producao.py': ('contar_unidades',),
        'construcoes_habitaveis.py': ('estrutura_habitada',),
    }
    for filename, names in selections.items():
        path = folder / filename
        tree = ast.parse(path.read_text(), filename=str(path))
        nodes = []
        top_names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                nodes.extend(n for n in node.body if isinstance(n, ast.FunctionDef) and n.name in names and n.name not in top_names)
            elif isinstance(node, ast.FunctionDef) and node.name in names: nodes.append(node)
            elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in node.targets): nodes.append(node)
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), namespace)
        if any(name not in namespace for name in names):
            raise StateValidationError('Economy read contract changed: ' + filename)
    return namespace


def habitation_query(root, image):
    namespace = _read_contract(str(Path(root).resolve()))
    recruitment = SimpleNamespace(mundo=SimpleNamespace(estruturas=image.read(0x49a0c8, 276000)),
                                  unidades=image.read(image.u32(0x4e19a0), 220800))
    recruitment._offset = MethodType(namespace['_offset'], recruitment)
    production = SimpleNamespace(recrutamento=recruitment)
    production.contar_unidades = MethodType(namespace['contar_unidades'], production)
    return lambda index: bool(namespace['estrutura_habitada'](production, index))
