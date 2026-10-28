"""Position query verified by separately captured original-only buffers."""
import hashlib
import json
from pathlib import Path
import struct
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from ordens_unidades import MundoUnidades
from posicao_saida import calcular_posicao_saida
from pegadas_estruturas import tamanho_estrutura


class PosicaoSaida(unittest.TestCase):
    def test_independent_original_captures_all_known_types(self):
        captura = json.loads((RAIZ / 'evidencias/posicao-saida/captura-original.json').read_text())
        self.assertEqual(captura['bounded_x86_executions'], 22)
        for caso in captura['cases']:
            m = MundoUnidades()
            m.estruturas[:] = b'\xa5' * 276000
            p = caso['index'] * 276
            m.estruturas[p:p+276] = bytes.fromhex(caso['input_record_hex'])
            antes = bytes(m.estruturas)
            self.assertEqual(m.calcular_posicao_saida(caso['index'], caso['direction']), caso['return_ax'])
            self.assertEqual(m.estruturas, antes)
            self.assertEqual(hashlib.sha256(m.estruturas).hexdigest(), caso['output_pool_sha256'])

    def test_original_dimensions_match_existing_geometry(self):
        manifesto = json.loads((RAIZ / 'evidencias/posicao-saida/manifesto.json').read_text())
        for caso in manifesto['dimensions']:
            self.assertEqual(tamanho_estrutura(caso['type']), (caso['width'], caso['height']))

    def test_direct_zero_return_is_not_origin_or_failure_sentinel(self):
        m = MundoUnidades()
        struct.pack_into('<H', m.estruturas, 2, 0xffff)
        for tipo in (9, 12, 17):
            m.estruturas[8] = tipo
            self.assertEqual(m.calcular_posicao_saida(0, 255), 0)

    def test_integer_widths_and_explicit_dimensions(self):
        m = MundoUnidades()
        m.estruturas[8] = 18
        struct.pack_into('<H', m.estruturas, 2, 0xffff)
        self.assertEqual(m.calcular_posicao_saida(0xbeef0000, 0xabcd01ff, (0x10004, 0x10005)), 514)
        self.assertEqual(m.calcular_posicao_saida(0, 0, (4, 5)), 514)

    def test_invalid_protected_domain_does_not_mutate(self):
        m = MundoUnidades()
        antes = bytes(m.estruturas)
        for indice in (1000, -1):
            with self.assertRaises(ValueError):
                calcular_posicao_saida(m, indice)
        with self.assertRaises(ValueError):
            calcular_posicao_saida(m, 0, dimensoes=(1,))
        m.estruturas[8] = 22
        with self.assertRaises(ValueError):
            calcular_posicao_saida(m, 0)
        m.estruturas[8] = 0
        self.assertEqual(m.estruturas, antes)

    def test_query_does_not_require_passage_or_place_structure(self):
        from navegacao_unidades import MundoNavegacao
        m = MundoNavegacao()
        m.estruturas[8] = 18
        struct.pack_into('<H', m.estruturas, 2, 0x505)
        m.atributos[:] = b'\xff' * 65536
        antes = bytes(m.atributos), bytes(m.estruturas), list(m.regioes)
        self.assertEqual(m.calcular_posicao_saida(0), 0x708)
        self.assertEqual((bytes(m.atributos), bytes(m.estruturas), m.regioes), antes)
