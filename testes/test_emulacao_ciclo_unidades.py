"""Original full-reset returns and ordered inline-fragment comparisons."""
import os
import unittest

from test_ciclo_unidades import (preparar,estado,MemoriaRastreada,rastrear_palavras,
                                resetar_bolsa,resetar_todas_unidades)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1','Optional x86: RISING_EMULAR=1')
class DiferencialCicloUnidades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_ciclo_unidades import BancadaCicloUnidades
        cls.bancada=BancadaCicloUnidades()

    def comparar(self,m):
        self.bancada.carregar_mundo(m)
        self.bancada.resetar()
        resetar_todas_unidades(m)
        self.assertEqual(estado(m),self.bancada.estado())

    def test_all_inactive_records_preserved_and_all_owner_type_bags_reset(self):
        for seed in (0,1,31,128,165,255):
            self.comparar(preparar(seed))

    def test_every_state_byte_unknown_types_and_entire_nonzero_pools(self):
        for seed in range(8):
            self.comparar(preparar(seed,estados=lambda i:(i*7+seed) & 255))
        self.comparar(preparar(255,estados=lambda i:4))

    def test_exact_whole_driver_write_order_before_units_and_local_header_order(self):
        m=preparar(estados=lambda i:4 if i in (0,7,799) else 0)
        eventos=[]
        m.unidades=MemoriaRastreada(m.unidades,'units',eventos)
        m.bolsas_tipos_unidades=[MemoriaRastreada(t,f'table{i}',eventos) for i,t in enumerate(m.bolsas_tipos_unidades)]
        self.bancada.carregar_mundo(m)
        self.bancada.rastrear=True
        try:self.bancada.resetar()
        finally:self.bancada.rastrear=False
        with rastrear_palavras(eventos):resetar_todas_unidades(m)
        self.assertEqual(eventos,self.bancada.escritas)
        self.assertEqual(estado(m),self.bancada.estado())
        self.assertEqual(len(eventos),6857)
        type(self).escritas_driver=len(eventos)

    def test_original_inline_bag_contexts_offsets_patterns_and_write_order(self):
        from emulador import UNIDADES
        for ordem in ('tabela','unidade'):
            for offset in (0,1,10,511,1096):
                for seed in (0,165,255):
                    eventos=[]
                    dados=MemoriaRastreada(bytes((i*31+seed) & 255 for i in range(1200)),'units',eventos)
                    self.bancada.rastrear=True
                    try:self.bancada.resetar_bolsa(dados,offset,ordem)
                    finally:self.bancada.rastrear=False
                    with rastrear_palavras(eventos):resetar_bolsa(dados,offset,ordem=ordem)
                    self.assertEqual(bytes(dados),bytes(self.bancada.cpu.mem_read(UNIDADES,1200)))
                    self.assertEqual(eventos,self.bancada.escritas)
