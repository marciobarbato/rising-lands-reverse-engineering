"""Frozen original captures and explicit continuation/resource boundaries."""
import hashlib
import json
from pathlib import Path
import struct
import unittest

from cenarios_classificacao_remapeamento import preparar_classificacao, CASOS_CLASSIFICACAO
from classificacao_remapeamento import (retomar_classificacao_remapeamento, ClassificacaoRemapeamento,
                                       DependenciaClassificacaoRemapeamento)
from remapeamento_mundo import iniciar_remapeamento, RemapeamentoPendente
from consultas_unidades import tipo_unidade, tipo_unidade_monstro
from test_remapeamento_mundo import resumo_python

RAIZ = Path(__file__).resolve().parents[1]
HANDLE = 0x1900000


class RecursosClassificacao:
    def __init__(self, nula=False, memoria=None):
        self.nula = nula
        self.memoria = bytearray(b'\xa5'*65536) if memoria is None else memoria
        self.chamadas, self.alocada = [], False

    def alocar(self, flags, tamanho):
        if (flags,tamanho) != (0,65536): raise ValueError('Fixture allocation domain')
        self.alocada = not self.nula
        h = 0 if self.nula else HANDLE
        self.chamadas.append(('GlobalAlloc', (flags,tamanho), h))
        return h

    def fixar(self, handle):
        self.chamadas.append(('GlobalLock', (handle,), 0 if self.nula else HANDLE))
        if handle != (0 if self.nula else HANDLE): raise ValueError('Unknown handle')
        return None if self.nula else self.memoria


def executar_classificacao(m, nula, desconhecido):
    recursos = RecursosClassificacao(nula)
    pedido = iniciar_remapeamento(m)
    if desconhecido:
        try: retomar_classificacao_remapeamento(m, pedido, alocar=recursos.alocar)
        except DependenciaClassificacaoRemapeamento as erro:
            assert (erro.checkpoint,erro.argumentos)==(0x42eec5,(HANDLE,))
            return recursos, erro
        raise AssertionError('Missing lock did not stop')
    return recursos, retomar_classificacao_remapeamento(m, pedido, alocar=recursos.alocar, fixar=recursos.fixar)


def resumo_classificacao_python(m, recursos, resultado):
    r = resumo_python(m)
    dados = bytes(recursos.memoria)
    consultas = list(range(65536)) if isinstance(resultado, ClassificacaoRemapeamento) else []
    r.update(classes_sha256=hashlib.sha256(dados).hexdigest(),
             class_counts={str(v): dados.count(v) for v in set(dados)}, natural_query_count=len(consultas),
             natural_query_order_sha256=hashlib.sha256(struct.pack('<%dH' % len(consultas),*consultas)).hexdigest())
    return r


class ClassificacaoMundo(unittest.TestCase):
    def test_eight_original_first_captures_exact_outputs_and_boundaries(self):
        d = json.loads((RAIZ/'relatorios/capturas-classificacao-remapeamento-original.json').read_text())
        self.assertFalse(d['translation_executed'])
        for c in d['cases']:
            m,nula,desconhecido,_ = preparar_classificacao(c['name'])
            recurso,resultado = executar_classificacao(m,nula,desconhecido)
            self.assertEqual(resumo_classificacao_python(m,recurso,resultado),c['output'])
            if isinstance(resultado,ClassificacaoRemapeamento):
                self.assertIs(resultado.memoria,recurso.memoria)
                self.assertEqual(resultado.endereco_dependencia,0x42ef8b)
            elif nula: self.assertIs(resultado,False)

    def test_first_pass_completes_before_predicate_calls_and_source_order_is_ascending(self):
        import classificacao_remapeamento as modulo
        m,*_ = preparar_classificacao('mixed');m.tiles[:]=list(range(65536))
        recurso=RecursosClassificacao();antes=bytes(x & 1 for x in m.atributos);ordem=[]
        original=modulo.obstaculo_natural
        def observar(tile,objeto,marcadores):
            if not ordem:self.assertEqual(bytes(recurso.memoria),antes)
            ordem.append(tile)
            return original(tile,objeto,marcadores)
        modulo.obstaculo_natural=observar
        try:retomar_classificacao_remapeamento(m,iniciar_remapeamento(m),alocar=recurso.alocar,fixar=recurso.fixar)
        finally:modulo.obstaculo_natural=original
        self.assertEqual(ordem,list(range(65536)))

    def test_null_lock_reads_no_terrain_and_lock_zero_is_still_called(self):
        m,*_=preparar_classificacao('zero');pedido=iniciar_remapeamento(m)
        m.tiles=m.atributos=m.objetos=m.marcadores_obstaculos_tiles=None
        recurso=RecursosClassificacao(True)
        self.assertIs(retomar_classificacao_remapeamento(m,pedido,alocar=recurso.alocar,fixar=recurso.fixar),False)
        self.assertEqual(recurso.chamadas,[('GlobalAlloc',(0,65536),0),('GlobalLock',(0,),0)])

    def test_missing_resource_providers_keep_reset_and_allocation_without_replay(self):
        m,*_=preparar_classificacao('zero');pedido=iniciar_remapeamento(m)
        m.regioes[17]=1234;m.busca.concluida=91
        with self.assertRaises(DependenciaClassificacaoRemapeamento) as c:retomar_classificacao_remapeamento(m,pedido)
        self.assertEqual((c.exception.checkpoint,c.exception.argumentos),(0x42eebd,(0,65536)))
        recurso=RecursosClassificacao()
        with self.assertRaises(DependenciaClassificacaoRemapeamento):retomar_classificacao_remapeamento(m,pedido,alocar=recurso.alocar)
        self.assertTrue(recurso.alocada)
        self.assertEqual((m.regioes[17],m.busca.concluida),(1234,91))
        self.assertEqual(recurso.memoria,bytearray(b'\xa5'*65536))

    def test_invalid_or_overlapping_inputs_precede_class_stores_after_resource_effects(self):
        for caso in ('short','readonly','overlap','tile','markers','shape'):
            m,*_=preparar_classificacao('mixed');pedido=iniciar_remapeamento(m);recurso=RecursosClassificacao()
            if caso=='short':recurso.memoria.pop()
            if caso=='readonly':recurso.memoria=bytes(recurso.memoria)
            if caso=='overlap':recurso.memoria=m.atributos
            if caso=='tile':m.tiles[65535]=65536
            if caso=='markers':m.marcadores_obstaculos_tiles.pop()
            if caso=='shape':recurso.memoria=memoryview(recurso.memoria).cast('B',shape=(256,256))
            antes=bytes(recurso.memoria)
            with self.assertRaises(ValueError):retomar_classificacao_remapeamento(m,pedido,alocar=recurso.alocar,fixar=recurso.fixar)
            self.assertTrue(recurso.alocada);self.assertEqual(bytes(recurso.memoria),antes)
        with self.assertRaises(ValueError):retomar_classificacao_remapeamento(m,RemapeamentoPendente(flags=1),alocar=recurso.alocar)

    def test_nonoverlapping_shared_backing_views_and_signed_destination_are_live(self):
        m,*_=preparar_classificacao('mixed');pedido=iniciar_remapeamento(m)
        arena=bytearray(2*65536+702)
        arena[65536:131072]=m.atributos;arena[131072:]=m.marcadores_obstaculos_tiles
        destino=memoryview(arena)[:65536].cast('b')
        m.atributos=memoryview(arena)[65536:131072]
        m.marcadores_obstaculos_tiles=memoryview(arena)[131072:]
        recurso=RecursosClassificacao(memoria=destino)
        r=retomar_classificacao_remapeamento(m,pedido,alocar=recurso.alocar,fixar=recurso.fixar)
        self.assertIs(r.memoria,destino);self.assertLessEqual(set(bytes(destino)),{0,1})

    def test_direct_initialization_queries_replay_all_original_consumed_al_bytes(self):
        d=json.loads((RAIZ/'relatorios/capturas-consultas-inicializacao-original.json').read_text())
        m,*_=preparar_classificacao('zero')
        for caso in d['getters']:
            indice=caso['index']
            for t,al in enumerate(bytes.fromhex(caso['al_hex'])):
                m.unidades[indice*276+1]=t
                self.assertEqual(m.tipo_unidade(0xabcd0000|indice),al)
        for t,al in enumerate(d['monster_al']):
            self.assertEqual(tipo_unidade_monstro(0xabcd0000|t),bool(al))
        for indice in (800,-1):
            with self.assertRaises(ValueError):tipo_unidade(m,indice)
