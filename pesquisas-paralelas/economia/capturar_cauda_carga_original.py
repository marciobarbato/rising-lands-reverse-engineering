"""Original-only Stage 16 captures, recorded before any Python translation.

Runs the MissionLoad tail fragments that economy owns on the intact
executable and stores whole-buffer hashes before and after. Requires Unicorn.
"""
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
sys.dont_write_bytecode = True
for caminho in (RAIZ/'ferramentas', PASTA):
    sys.path.insert(0, str(caminho))
import casos_cauda_carga as casos
from bancada_cauda_carga import BancadaCaudaCarga
from emulador import HASH_ORIGINAL


def _casos():
    for caso in casos.casos_monde01():
        yield 'tail', caso
    yield 'habitation+tail', casos.estender(casos.base.caso_monde01('MONDE01 habitation then tail', padrao='um'),
                                            rede=0, padrao_realizaveis='um')
    for semente, rede in ((1, 0), (2, 1)):
        yield 'tail', casos.caso_pool(f'random pool {semente} network {rede}', semente=semente, rede=rede)


def capturar():
    bancada = BancadaCaudaCarga()
    resultados = []
    for modo, caso in _casos():
        bancada.carregar(caso)
        antes = bancada.resumo()
        paradas = []
        if modo == 'habitation+tail':
            paradas.append(hex(bancada.varrer_estrutura(0)['EIP']))
        for fragmento in (bancada.cauda_tecnologia_cavernas, bancada.cauda_jogadores, bancada.cauda_mercado):
            paradas.append(hex(fragmento()['EIP']))
        resultados.append(dict(name=caso.nome, origin=caso.origem, mode=modo, stops=paradas,
                               input=antes['sha256'], output=bancada.resumo()))
    return dict(sha256_exe=HASH_ORIGINAL, captured_before_translation=True,
                scope='Original-only MissionLoad tail fragments 0x46c5af..0x46c5b9, 0x46c5be..0x46c5c3 and '
                      '0x46c5d1..0x46c5d6 (one case after the Stage 15 caller fragment); whole mapped buffers hashed',
                entries=bancada.entradas, bounded_segments=bancada.execucoes,
                minimap_resumes=bancada.retomadas_minimapa, cases=resultados)


if __name__ == '__main__':
    r = capturar()
    (PASTA/'evidencias/captura-cauda-carga-original.json').write_text(json.dumps(r, indent=2)+'\n')
    print('Original entries:', r['entries'], 'segments:', r['bounded_segments'])
