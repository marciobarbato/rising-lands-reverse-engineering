"""Declared inherited terrain/marker inputs for bounded remap continuation."""
import hashlib
from pathlib import Path
import struct
import sys

from capturar_remapeamento_mundo import preparar_remapeamento

RAIZ = Path(__file__).resolve().parents[1]
CASOS_CLASSIFICACAO = ('null', 'unsupported_lock', 'zero', 'tiles', 'objects', 'mixed', 'MONDE01', 'MONDE01_null')


def preparar_classificacao(nome):
    m = preparar_remapeamento()
    m.atributos[:] = bytes((i*17+0xa5) & 255 for i in range(65536))
    m.tiles[:] = [702]*65536
    m.objetos[:] = bytes(65536)
    marcadores = bytes((i*7) & 255 for i in range(702))
    fonte = dict(kind='synthetic declared layers and markers')
    if nome in ('MONDE01', 'MONDE01_null'):
        # Same-checkout committed mission fixture, not a live peer worktree.
        for p in (RAIZ/'pesquisas-paralelas/missoes',):
            if str(p) not in sys.path: sys.path.insert(0, str(p))
        from capturar_terreno_unidades import preparar_caso
        m, raw, *_ = preparar_caso('MONDE01')
        tabela = (RAIZ.parent/'source/cd/INSTALHD/TABLEAU.COL').read_bytes()
        if len(tabela) != 702: raise ValueError('TerrainLoadObstacle reads exactly 702 explicit bytes')
        marcadores = tabela
        fonte = dict(kind='Actual MONDE01 normalized header layers and shipped TABLEAU.COL; other inherited state synthetic',
                     mission_sha256=hashlib.sha256(raw).hexdigest(), markers_sha256=hashlib.sha256(tabela).hexdigest())
    elif nome == 'zero':
        m.atributos[:] = bytes(65536)
    elif nome == 'tiles':
        m.tiles[:] = [i % 704 for i in range(65536)]
    elif nome == 'objects':
        valores = (0, 1, 11, 12, 29, 255)
        m.objetos[:] = bytes(valores[i % 6] for i in range(65536))
    elif nome == 'mixed':
        tipos = (0, 1, 701, 702, 65535)
        m.tiles[:] = [tipos[i % 5] for i in range(65536)]
        m.objetos[:] = bytes(i % 16 for i in range(65536))
    m.marcadores_obstaculos_tiles[:] = marcadores
    return m, nome in ('null', 'MONDE01_null'), nome == 'unsupported_lock', fonte


def resumo_classificacao(m, memoria):
    sha = lambda x: hashlib.sha256(bytes(x)).hexdigest()
    return dict(classes_sha256=sha(memoria), attributes_sha256=sha(m.atributos),
                regions_sha256=sha(struct.pack('<65536H', *m.regioes)), colors_sha256=sha(m.cores_estruturas.grade),
                free_hex=m.cores_estruturas.livres.hex(), released_hex=m.cores_estruturas.liberadas.hex(),
                search=vars(m.busca).copy(), unit_pool_sha256=sha(m.unidades),
                class_counts={str(v): memoria.count(v) for v in set(memoria)})
