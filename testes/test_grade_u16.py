"""Live tile grid [0x507d70]: GradeU16 by identity, and list-equivalent Core world behavior."""
import json
from pathlib import Path
import struct
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
sys.path.insert(0, str(RAIZ / 'testes'))
from grade_u16 import GradeU16


def vivo(lista):
    return bytearray(struct.pack('<65536H', *lista))


class GradeViva(unittest.TestCase):
    def test_identity_and_little_endian_live_access(self):
        buf = bytearray(131072)
        g = GradeU16(buf)
        self.assertIs(g.buffer, buf)
        g[0x505] = 0x2fa
        self.assertEqual(buf[0xa0a:0xa0c], b'\xfa\x02')
        buf[0x1fffe:0x20000] = b'\x34\x12'
        self.assertEqual((g[0xffff], g[-1]), (0x1234, 0x1234))
        vista = memoryview(buf)
        self.assertIs(GradeU16(vista).buffer, vista)

    def test_list_operations_used_by_core(self):
        buf = bytearray(131072)
        g = GradeU16(buf)
        g[:] = [i % 704 for i in range(65536)]
        self.assertEqual(g[:], [i % 704 for i in range(65536)])
        self.assertEqual(list(g), g[:])
        self.assertEqual(g, [i % 704 for i in range(65536)])
        self.assertEqual(len(g), 65536)
        self.assertEqual(g[10:14], [10, 11, 12, 13])
        self.assertEqual(g[0:6:2], [0, 2, 4])
        copia = g[:]
        g[3] = 600
        self.assertEqual((copia[3], g[3]), (3, 600))         # a slice is a copy, like a list
        self.assertEqual(struct.unpack_from('<H', buf, 6)[0], 600)

    def test_refusals_before_any_store(self):
        buf = bytearray(131072)
        g = GradeU16(buf)
        for indice, valor in ((0, 65536), (1, -1), (2, 1.0)):
            with self.assertRaises(ValueError):
                g[indice] = valor
        with self.assertRaises(ValueError):
            g[:] = [0] * 65535
        with self.assertRaises(ValueError):
            g[0:3] = [1, 2, 70000]
        with self.assertRaises(IndexError):
            g[65536]
        self.assertEqual(bytes(buf), bytes(131072))
        for errado in (bytes(131072), bytearray(131070), memoryview(bytearray(131072))[::2]):
            with self.assertRaises(ValueError):
                GradeU16(errado)


class MundoComTilesVivos(unittest.TestCase):
    def test_vincular_tiles_binds_by_identity(self):
        from avanco_unidades import MundoFisico
        m = MundoFisico()
        self.assertIsInstance(m.tiles, list)                  # default unchanged
        buf = bytearray(131072)
        self.assertIs(m.vincular_tiles(buf), m.tiles)
        self.assertIs(m.tiles.buffer, buf)

    def test_structure_terrain_placement_equals_list_mode(self):
        from test_terreno_estruturas import mundo_estrutura
        for tipo, origem, primeiro in ((0, 0x505, 600), (2, 0xfffe, 0xfffe), (5, 0x1210, 0x15d)):
            lista, viva = mundo_estrutura(tipo, 7, origem), mundo_estrutura(tipo, 7, origem)
            buf = vivo(viva.tiles)
            viva.vincular_tiles(buf)
            r1 = lista.aplicar_terreno_estrutura(7, origem, primeiro)
            r2 = viva.aplicar_terreno_estrutura(7, origem, primeiro)
            self.assertEqual(r1, r2)
            self.assertEqual(viva.tiles, lista.tiles)
            self.assertEqual(bytes(buf), struct.pack('<65536H', *lista.tiles))
            self.assertEqual((bytes(lista.atributos), lista.regioes, bytes(lista.objetos)),
                             (bytes(viva.atributos), viva.regioes, bytes(viva.objetos)))

    def test_original_classification_captures_hold_with_a_live_grid(self):
        from test_classificacao_remapeamento import executar_classificacao, resumo_classificacao_python
        from cenarios_classificacao_remapeamento import preparar_classificacao
        d = json.loads((RAIZ / 'relatorios/capturas-classificacao-remapeamento-original.json').read_text())
        for c in d['cases']:
            with self.subTest(c['name']):
                m, nula, desconhecido, _ = preparar_classificacao(c['name'])
                buf = vivo(m.tiles)
                m.vincular_tiles(buf)
                recurso, resultado = executar_classificacao(m, nula, desconhecido)
                self.assertEqual(resumo_classificacao_python(m, recurso, resultado), c['output'])

    def test_region_reconstruction_equals_list_mode(self):
        from regioes_mapa import reconstruir_regioes
        from cenarios_classificacao_remapeamento import preparar_classificacao
        m, *_ = preparar_classificacao('mixed')
        esperado = reconstruir_regioes(m.atributos, m.tiles, m.objetos, m.marcadores_obstaculos_tiles, 64, 64)
        self.assertEqual(reconstruir_regioes(m.atributos, GradeU16(vivo(m.tiles)), m.objetos,
                                             m.marcadores_obstaculos_tiles, 64, 64), esperado)


class GradesVivasMundo(unittest.TestCase):
    def mundo_vivo(self, m):
        buffers = dict(tiles=vivo(m.tiles), regioes=vivo(m.regioes), atributos=bytearray(m.atributos),
                       objetos=bytearray(m.objetos), donos_objetos=bytearray(m.donos_objetos))
        m.vincular_grades(**buffers)
        return buffers

    def test_identity_for_every_grid_and_refusal_before_binding(self):
        from avanco_unidades import MundoFisico
        m = MundoFisico()
        buffers = self.mundo_vivo(m)
        self.assertIs(m.tiles.buffer, buffers['tiles'])
        self.assertIs(m.regioes.buffer, buffers['regioes'])
        for nome in ('atributos', 'objetos', 'donos_objetos'):
            self.assertIs(getattr(m, nome), buffers[nome])
        self.assertEqual(m.grades_vivas, frozenset(buffers))
        outro = MundoFisico()
        antes = (outro.tiles, outro.atributos)
        with self.assertRaises(ValueError):
            outro.vincular_grades(tiles=bytearray(131072), atributos=bytes(65536))
        self.assertIs(outro.tiles, antes[0])
        self.assertIs(outro.atributos, antes[1])

    def test_structure_placement_with_every_grid_live(self):
        from test_terreno_estruturas import mundo_estrutura
        lista, viva = mundo_estrutura(0, 7, 0x505), mundo_estrutura(0, 7, 0x505)
        buffers = self.mundo_vivo(viva)
        self.assertEqual(lista.aplicar_terreno_estrutura(7, 0x505, 600), viva.aplicar_terreno_estrutura(7, 0x505, 600))
        self.assertEqual(bytes(buffers['tiles']), struct.pack('<65536H', *lista.tiles))
        self.assertEqual(bytes(buffers['regioes']), struct.pack('<65536H', *lista.regioes))
        self.assertEqual((bytes(buffers['atributos']), bytes(buffers['objetos'])),
                         (bytes(lista.atributos), bytes(lista.objetos)))

    def test_original_classification_captures_with_every_grid_live(self):
        from test_classificacao_remapeamento import executar_classificacao, resumo_classificacao_python
        from cenarios_classificacao_remapeamento import preparar_classificacao
        d = json.loads((RAIZ / 'relatorios/capturas-classificacao-remapeamento-original.json').read_text())
        for c in d['cases']:
            with self.subTest(c['name']):
                m, nula, desconhecido, _ = preparar_classificacao(c['name'])
                self.mundo_vivo(m)
                recurso, resultado = executar_classificacao(m, nula, desconhecido)
                self.assertEqual(resumo_classificacao_python(m, recurso, resultado), c['output'])

    def test_region_rebuild_keeps_live_identity(self):
        from navegacao_unidades import MundoNavegacao
        lista, viva = MundoNavegacao(32, 24), MundoNavegacao(32, 24)
        for m in (lista, viva):
            m.tiles[:] = [i % 704 for i in range(65536)]
            m.objetos[:] = bytes(i % 13 for i in range(65536))
            m.atributos[:] = bytes(i & 3 for i in range(65536))
        buffers = self.mundo_vivo(viva)
        self.assertEqual(lista.refazer_regioes(), viva.refazer_regioes())
        self.assertIs(viva.regioes.buffer, buffers['regioes'])
        self.assertIs(viva.atributos, buffers['atributos'])
        self.assertEqual((viva.regioes, bytes(viva.atributos)), (lista.regioes, bytes(lista.atributos)))

    def test_economy_field_growth_reads_and_writes_the_core_grids_by_identity(self):
        """ScanNouvellePatate/NouvellePatate (Economy's extracao) over Core's live grids."""
        from integracao.providers import load_economy_resources
        extracao = load_economy_resources()
        from avanco_unidades import MundoFisico
        m = MundoFisico()
        buffers = self.mundo_vivo(m)
        m.tiles[0x1235] = 0x9d                     # a growable tile right of 0x1234
        m.atributos[0x1233] = 1                    # left neighbour blocked by attribute bit 0
        recursos = extracao.RecursosTerreno()
        recursos.mosaicos, recursos.atributos = m.tiles.buffer, m.atributos
        recursos.terreno.tipos, recursos.terreno.quantidades = m.objetos, m.donos_objetos
        recursos.propagar_planta(0x1234)
        self.assertIn(buffers['objetos'][0x1235], (0x1d, 0x29))      # the plant landed in Core's live grid
        self.assertEqual(buffers['objetos'][0x1233], 0)


if __name__ == '__main__':
    unittest.main()
