"""Fresh intact-x86 runs compared with the Python reconstruction (RISING_EMULAR=1).

Covers every structure scenario, every sound of bank A, and a P subset with
the PCM entry, the byte13=200 headers, a five-variant entry and the largest
sample. ``validar_som.py`` runs the same comparison over all three banks.
"""
import json
import os
from pathlib import Path
import struct
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))

NATIVO = os.environ.get('RISING_EMULAR') == '1'
if NATIVO:
    import capturar_som
    import reproduzir_som
    from bancos_som import entradas_banco
    from cenarios_som import arquivos_originais


def normalizar(valor):
    contadores = ('instructions', 'segments', 'instructions_file', 'segments_file', 'instructions_memory',
                  'segments_memory', 'file_seconds')
    valor = json.loads(json.dumps(valor))
    if isinstance(valor, dict):
        return {k: v for k, v in valor.items() if k not in contadores}
    return valor


@unittest.skipUnless(NATIVO, 'Optional intact-x86: RISING_EMULAR=1')
class Nativo(unittest.TestCase):
    def test_structure_scenarios(self):
        for parte in ('validacao', 'indice', 'decodificador'):
            with self.subTest(parte=parte):
                self.assertEqual(normalizar(getattr(capturar_som, 'capturar_' + parte)()),
                                 normalizar(getattr(reproduzir_som, 'reproduzir_' + parte)()))

    def test_bank_a_every_sound(self):
        self.assertEqual(normalizar(capturar_som.capturar_banco('A')),
                         normalizar(reproduzir_som.reproduzir_banco('A')))

    def test_bank_p_subset(self):
        bancada = capturar_som.nova_bancada(arquivos_originais('P'))
        mundo = reproduzir_som.Mundo(arquivos_originais('P'))
        self.assertEqual(normalizar(capturar_som.abrir(bancada, 'P')), normalizar(reproduzir_som.abrir(mundo, 'P')))
        capturar_som.chamar(bancada, 'InitCompressedBuffer')
        reproduzir_som.iniciar_buffer_comprimido(mundo.sistema, mundo.globais)
        banco = mundo.bancos['P']
        cabecalho = bancada.u32(capturar_som.BANCOS['P'] + 0xc)
        escolhidos, maior = [], None
        for indice, (ident, _, variantes, deslocamento) in enumerate(entradas_banco(banco)):
            for variante in range(max(variantes, 1)):
                dh = banco.cabecalho[deslocamento + 16 * variante:deslocamento + 16 * variante + 16]
                tamanho, formato, byte_0d = struct.unpack_from('<I', dh, 4)[0], dh[12], dh[13]
                if formato == 0 or byte_0d or variantes == 5:
                    escolhidos.append((indice, variante, deslocamento + 16 * variante))
                if maior is None or tamanho > maior[0]:
                    maior = (tamanho, (indice, variante, deslocamento + 16 * variante))
        escolhidos.append(maior[1])
        self.assertGreaterEqual(len(escolhidos), 14)
        for indice, variante, deslocamento in escolhidos:
            with self.subTest(indice=indice, variante=variante):
                chave = dict(index=indice, variant=variante)
                nativo = capturar_som.capturar_superficie(bancada, 'P', cabecalho + deslocamento, dict(chave))
                python = reproduzir_som.superficie(mundo, 'P', deslocamento, dict(chave))
                self.assertEqual(normalizar(nativo), normalizar(python))
                self.assertIsNotNone(nativo['buffer_sha256'])


if __name__ == '__main__':
    unittest.main()
