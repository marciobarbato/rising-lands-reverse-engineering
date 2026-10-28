"""Original reset captures, live aliases and untouched world state."""
import hashlib
import json
from pathlib import Path
import struct
import unittest

from capturar_remapeamento_mundo import preparar_remapeamento
from remapeamento_mundo import iniciar_remapeamento


def resumo_python(m):
    sha = lambda raw: hashlib.sha256(raw).hexdigest()
    c = m.cores_estruturas
    return dict(search=vars(m.busca).copy(),colors_sha256=sha(c.grade),
                regions_sha256=sha(struct.pack('<65536H',*m.regioes)),
                free_hex=c.livres.hex(),released_hex=c.liberadas.hex(),
                units_sha256=sha(m.unidades),attributes_sha256=sha(m.atributos),
                native_fill_calls=[['colors',0,65536],['released',1,256],['regions',0,131072]])


class RemapeamentoMundo(unittest.TestCase):
    def test_four_independent_original_captures_and_pending_stack_arguments(self):
        arquivo = Path(__file__).resolve().parents[1]/'relatorios/capturas-remapeamento-original.json'
        for caso in json.loads(arquivo.read_text())['cases']:
            m = preparar_remapeamento(**caso['input'])
            pedido = m.iniciar_remapeamento()
            self.assertEqual(resumo_python(m),caso['output'])
            self.assertEqual([pedido.flags,pedido.tamanho],caso['pending_stack_arguments'])
            self.assertEqual((pedido.endereco_dependencia,pedido.importacao),(0x42eebd,0x5231c0))

    def test_all_target_aliases_and_unrelated_state_are_retained(self):
        m = preparar_remapeamento()
        c = m.cores_estruturas
        aliases = (m.busca,m.regioes,c.grade,c.livres,c.liberadas,c.pilha)
        from copy import deepcopy
        retidos = {k:deepcopy(v) for k,v in vars(m).items() if k not in ('busca','regioes','cores_estruturas')}
        pilha = c.pilha[:]
        iniciar_remapeamento(m)
        for antes,depois in zip(aliases,(m.busca,m.regioes,c.grade,c.livres,c.liberadas,c.pilha)):
            self.assertIs(antes,depois)
        self.assertEqual(c.pilha,pilha)
        self.assertEqual({k:v for k,v in vars(m).items() if k in retidos},retidos)
        self.assertEqual(m.busca.concluida,165)

    def test_prefix_has_no_dimension_terrain_or_live_unit_eligibility_guard(self):
        m = preparar_remapeamento(unidade=65535)
        m.largura,m.altura = 0,999
        m.tiles,m.marcadores_obstaculos_tiles = None,None
        m.unidades[:] = b'\xff'*220800
        pedido = iniciar_remapeamento(m)
        self.assertEqual((m.busca.unidade,m.busca.ponteiro_rota,pedido.tamanho),(65535,0,65536))
        self.assertFalse(any(m.regioes))

    def test_all_protected_pool_failures_precede_any_clear(self):
        for alvo in ('regions_size','regions_type','colors','free','released','alias','search'):
            m = preparar_remapeamento()
            c = m.cores_estruturas
            if alvo == 'regions_size': m.regioes.pop()
            if alvo == 'regions_type': m.regioes = tuple(m.regioes)
            if alvo == 'colors': c.grade = bytes(c.grade)
            if alvo == 'free': c.livres.pop()
            if alvo == 'released': c.liberadas = bytes(c.liberadas)
            if alvo == 'alias': c.liberadas = c.livres
            if alvo == 'search': m.busca = object()
            estado = (list(m.regioes),bytes(c.grade),bytes(c.livres),bytes(c.liberadas),
                      vars(m.busca).copy() if hasattr(m.busca,'__dict__') else None)
            with self.assertRaises(ValueError): iniciar_remapeamento(m)
            self.assertEqual((list(m.regioes),bytes(c.grade),bytes(c.livres),bytes(c.liberadas),
                              vars(m.busca).copy() if hasattr(m.busca,'__dict__') else None),estado)
