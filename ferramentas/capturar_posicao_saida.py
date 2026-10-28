"""Capture independent original-only CalculPosition cases before translation."""
import hashlib
import json
from pathlib import Path
import struct
from bancada_posicao_saida import BancadaPosicaoSaida
from emulador import HASH_ORIGINAL

RAIZ = Path(__file__).resolve().parents[1]


def capturar():
    manifesto = json.loads((RAIZ / 'evidencias/posicao-saida/manifesto.json').read_text())
    bancada = BancadaPosicaoSaida()
    casos = []
    for tipo, dimensao in enumerate(manifesto['dimensions']):
        registros = bytearray(b'\xa5') * 276000
        indice = 999 if tipo % 2 else 0
        p = indice * 276
        origem, direcao = (0xff00 + tipo * 37) & 65535, (tipo * 13) & 255
        struct.pack_into('<H', registros, p + 2, origem)
        registros[p + 8] = tipo
        bancada.carregar(registros)
        resultado = bancada.calcular(indice, direcao)
        depois = bancada.registros()
        if depois != registros:
            raise ValueError('Unexpected original pool mutation')
        casos.append(dict(type=tipo, index=indice, direction=direcao,
                           dimensions=[dimensao['width'], dimensao['height']],
                           input_record_hex=bytes(registros[p:p+276]).hex(),
                           return_ax=resultado,
                           output_pool_sha256=hashlib.sha256(depois).hexdigest()))
    report = dict(original_sha256=HASH_ORIGINAL, bounded_x86_executions=bancada.execucoes,
                  synthetic_fixture='0xa5 pool; original dimensions; type/origin set in one record',
                  mutations=False, expected_exceptions=0, expected_limits=0, cases=casos)
    (RAIZ / 'evidencias/posicao-saida/captura-original.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    print('Captured original-only cases:', capturar()['bounded_x86_executions'])
