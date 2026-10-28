"""Fresh native comparison of every audio scenario against the Python reconstruction.

Re-runs the intact routines (``capturar_som``), the Python replays
(``reproduzir_som``) and the committed original-only captures, and requires
all three to be identical. Writes ``validacao/x86-som.json``. Needs Unicorn
in the ordinary execution context; about ten minutes for the three banks.
"""
import json
import sys
import time
from ambiente_audio import LETRAS_BANCO, ORIGINAL_SHA256, OWNED
import capturar_som
import reproduzir_som

CONTADORES = ('instructions', 'segments', 'instructions_file', 'segments_file', 'instructions_memory',
              'segments_memory', 'file_seconds')


def normalizar(valor):
    return json.loads(json.dumps(valor))


def diferencas(a, b, caminho='', saida=None):
    saida = [] if saida is None else saida
    if isinstance(a, dict) and isinstance(b, dict):
        for chave in sorted(set(a) | set(b), key=str):
            if chave not in a or chave not in b:
                saida.append(f'{caminho}.{chave}: missing')
            else:
                diferencas(a[chave], b[chave], f'{caminho}.{chave}', saida)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            diferencas(x, y, f'{caminho}[{i}]', saida)
    elif a != b:
        saida.append(f'{caminho}: {str(a)[:120]} != {str(b)[:120]}')
    return saida


def sem_contadores(registro):
    return {k: v for k, v in registro.items() if k not in CONTADORES}


def comparar(nome, nativo, python, gravado):
    contagem = {k: nativo[k] for k in CONTADORES if k in nativo}
    nativo = normalizar(sem_contadores(nativo))
    return dict(scenario=nome, native_vs_python=diferencas(nativo, normalizar(sem_contadores(python))),
                native_vs_committed=diferencas(nativo, normalizar(sem_contadores(gravado))), **contagem)


def main(letras):
    estrutura = json.loads((OWNED / 'evidencias/captura-som-estrutura.json').read_text())
    resultados, inicio = [], time.time()
    for parte, chave in (('validacao', 'validation'), ('indice', 'index'), ('decodificador', 'decoder')):
        resultados.append(comparar(parte, getattr(capturar_som, 'capturar_' + parte)(),
                                   getattr(reproduzir_som, 'reproduzir_' + parte)(), estrutura[chave]))
        print(parte, len(resultados[-1]['native_vs_python']), 'differences', flush=True)
    sons = {}
    for letra in letras:
        gravado = json.loads((OWNED / f'evidencias/captura-som-banco-{letra}.json').read_text())
        for chave in ('original_sha256', 'created_before_translation', 'fixture'):
            gravado.pop(chave)
        nativo = capturar_som.capturar_banco(letra)
        resultados.append(comparar(f'bank_{letra}', nativo, reproduzir_som.reproduzir_banco(letra), gravado))
        sons[letra] = dict(file=len(nativo['surfaces_from_file']), memory=len(nativo['surfaces_from_memory']),
                           decoded_bytes=sum(sum(s['decoder_returns']) for s in nativo['surfaces_from_file']))
        print('bank', letra, len(resultados[-1]['native_vs_python']), 'differences',
              round(time.time() - inicio, 1), 's', flush=True)
    relatorio = dict(
        original_sha256=ORIGINAL_SHA256, banks=letras, sounds=sons, scenarios=resultados,
        passed=all(not r['native_vs_python'] and not r['native_vs_committed'] for r in resultados),
        instructions=sum(r.get('instructions', 0) + r.get('instructions_file', 0) + r.get('instructions_memory', 0)
                         for r in resultados),
        segments=sum(r.get('segments', 0) + r.get('segments_file', 0) + r.get('segments_memory', 0)
                     for r in resultados),
        seconds=round(time.time() - inicio, 1),
        note='Segments are bounded bench executions (entries, binding resumptions and loop-head checkpoints), '
             'not routine calls. Instruction counts cover bank scenarios and the index bench only.')
    (OWNED / 'validacao').mkdir(exist_ok=True)
    (OWNED / 'validacao/x86-som.json').write_text(json.dumps(relatorio, indent=1) + '\n')
    print('passed' if relatorio['passed'] else 'FAILED', relatorio['instructions'], 'instructions',
          relatorio['segments'], 'segments', relatorio['seconds'], 's')
    return 0 if relatorio['passed'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:] or list(LETRAS_BANCO)))
