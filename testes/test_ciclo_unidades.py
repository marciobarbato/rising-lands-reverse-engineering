"""Selective unit/global-Bag reset without invented cleanup effects."""
from contextlib import contextmanager
import struct
import sys
from pathlib import Path
from unittest.mock import patch
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'ferramentas'))
from bolsas_inicializacao import resetar_bolsa
from ciclo_unidades import resetar_todas_unidades
from ordens_unidades import MundoUnidades


def preparar(seed=19, *, estados=None):
    m=MundoUnidades()
    m.unidades[:]=bytes((i*31+seed) & 255 for i in range(220800))
    for i in range(800):
        m.unidades[i*276+2]=0 if estados is None else estados(i)
    for dono,tabela in enumerate(m.bolsas_tipos_unidades):
        tabela[:]=bytes((i*53+seed+dono) & 255 for i in range(2704))
    return m


def estado(m):
    return bytes(m.unidades),tuple(bytes(t) for t in m.bolsas_tipos_unidades)


class MemoriaRastreada(bytearray):
    def __new__(cls,dados,nome,eventos):
        return super().__new__(cls)

    def __init__(self,dados,nome,eventos):
        super().__init__(dados)
        self.nome,self.eventos=nome,eventos

    def __setitem__(self,indice,valor):
        if isinstance(indice,int):
            self.eventos.append((self.nome,indice,1,valor & 255))
        super().__setitem__(indice,valor)


@contextmanager
def rastrear_palavras(eventos):
    original=struct.pack_into
    def guardar(formato,memoria,offset,*valores):
        eventos.append((memoria.nome,offset,struct.calcsize(formato),valores[0]))
        return original(formato,memoria,offset,*valores)
    with patch.object(struct,'pack_into',guardar):
        yield


class CicloUnidades(unittest.TestCase):
    def test_raw_bag_retains_six_reserved_bytes_in_both_contexts(self):
        for ordem in ('tabela','unidade'):
            dados=bytearray(b'\xa5'*104)
            resetar_bolsa(dados,ordem=ordem)
            self.assertEqual(dados[:0x60],bytes(0x60))
            self.assertEqual(dados[0x60:0x66],b'\xa5'*6)
            self.assertEqual(dados[0x66:],bytes(2))

    def test_raw_live_memoryview_unaligned_offsets_and_surroundings(self):
        dados=bytearray(b'\xa5'*200)
        with memoryview(dados)[1:150].cast('b') as vista:
            resetar_bolsa(vista,3,ordem='unidade')
        self.assertEqual(dados[:4],b'\xa5'*4)
        self.assertEqual(dados[4+0x60:4+0x66],b'\xa5'*6)
        self.assertEqual(dados[108:],b'\xa5'*92)
        self.assertEqual(dados[4:4+0x60],bytes(0x60))

    def test_world_state_zero_kept_and_state_four_reset_without_selection_or_sound(self):
        m=preparar(estados=lambda i:4 if i in (0,799) else 0)
        antes=bytes(m.unidades)
        selecoes,busca=bytes(m.selecoes_unidades),vars(m.busca).copy()
        m.resetar_todas_unidades()
        self.assertEqual(m.unidades[276:799*276],antes[276:799*276])
        for i in (0,799):
            p=i*276
            self.assertEqual((m.unidades[p+2],m.palavra(i,0x9a),m.unidades[p+0xaf]),(0,0,0))
            for a,b in ((0x6a,0x70),(0x72,0x74),(0xbd,0xbe),(0x104,0x108)):
                self.assertEqual(m.unidades[p+a:p+b],antes[p+a:p+b])
        self.assertEqual((bytes(m.selecoes_unidades),vars(m.busca)),(selecoes,busca))

    def test_bad_raw_buffers_offsets_and_contexts_fail_before_store(self):
        for dados,offset,ordem in ((bytes(104),0,'tabela'),(bytearray(103),0,'unidade'),
                                   (bytearray(104),-1,'tabela'),(bytearray(104),0,'other'),
                                   (bytearray(104),1,'tabela')):
            antes=dados[:]
            with self.assertRaises(ValueError):
                resetar_bolsa(dados,offset,ordem=ordem)
            self.assertEqual(dados,antes)
        with self.assertRaises(ValueError):
            resetar_bolsa(memoryview(bytearray(208))[::2])

    def test_all_world_allocations_validated_before_any_mutation(self):
        for modo in ('short','alias','readonly'):
            m=preparar(estados=lambda i:255)
            if modo == 'short':m.bolsas_tipos_unidades[-1]=bytearray(2703)
            elif modo == 'alias':m.bolsas_tipos_unidades[-1]=m.bolsas_tipos_unidades[0]
            else:m.bolsas_tipos_unidades[-1]=bytes(2704)
            antes=estado(m)
            with self.assertRaises(ValueError):resetar_todas_unidades(m)
            self.assertEqual(estado(m),antes)
