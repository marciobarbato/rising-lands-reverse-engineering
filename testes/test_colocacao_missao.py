"""Mission insertion preserves prepared records and search/order state."""
import unittest

from test_colocacao_saida import preparar
from colocacao_missao import colocar_unidade_missao, DependenciaColocacaoMissao
from consultas_unidades import existe_unidade, visibilidade_unidade


class ColocacaoMissao(unittest.TestCase):
    def test_raw_queries_have_no_activity_type_owner_or_visibility_filter(self):
        m = preparar()
        p = 7*276
        m.unidades[p:p+2] = b'\xff\xff'
        for estado in range(256):
            m.unidades[p+2] = estado
            m.unidades[p+0x72] = 255-estado
            antes = bytes(m.unidades)
            self.assertEqual(m.existe_unidade(0xabcd0007), estado != 0)
            self.assertEqual(m.visibilidade_unidade(0xabcd0007), 255-estado)
            self.assertEqual(bytes(m.unidades), antes)

    def test_current_cell_insertion_preserves_record_orders_search_and_old_occupancy(self):
        m = preparar(dono=200, estado=4)
        antes, busca = m.ler_unidade(7), vars(m.busca).copy()
        m.colocar_unidade_missao(0xabcd0007)
        esperado = bytearray(antes)
        esperado[0x72] = 1
        self.assertEqual(m.ler_unidade(7), bytes(esperado))
        self.assertEqual(vars(m.busca), busca)
        self.assertEqual(m.efeitos, [('collision',7,0x505),('minimap',200,0x505,4)])
        self.assertEqual((m.atributos[0x505],m.atributos[0x506]), (1,1))

    def test_large_vision_stops_after_collision_and_flag_with_orders_intact(self):
        m = preparar(raio=9)
        antes, busca = m.ler_unidade(7), vars(m.busca).copy()
        with self.assertRaises(DependenciaColocacaoMissao) as captura:
            colocar_unidade_missao(m,7)
        self.assertEqual((captura.exception.checkpoint,captura.exception.endereco), (0x457019,0x476851))
        self.assertEqual(m.ler_unidade(7)[:0x72], antes[:0x72])
        self.assertEqual(m.ler_unidade(7)[0x73:0xfa], antes[0x73:0xfa])
        self.assertEqual(vars(m.busca), busca)
        self.assertEqual(m.efeitos, [('collision',7,0x505)])

    def test_protected_invalid_inputs_precede_effects(self):
        for cambio in ('index','cell','owner','type','camera','minimap','pool'):
            m = preparar()
            indice = 800 if cambio == 'index' else 7
            if cambio == 'cell': m.palavra(7,8,0x1010)
            if cambio == 'owner': m.unidades[7*276] = 5
            if cambio == 'type': m.unidades[7*276+1] = 26
            if cambio == 'camera': m.jogador_local = 4
            if cambio == 'minimap': m.tamanho_minimapa = (64,64)
            if cambio == 'pool': m.unidades = bytes(m.unidades)
            antes = bytes(m.unidades)
            with self.assertRaises(ValueError): colocar_unidade_missao(m,indice)
            self.assertEqual(bytes(m.unidades), antes)
            self.assertEqual(m.efeitos, [])
        m = preparar()
        for consulta in (existe_unidade,visibilidade_unidade):
            for indice in (800,-1):
                with self.assertRaises(ValueError): consulta(m,indice)
