"""Whole original pre-allocation state and exact ordered reset events."""
import os
import struct
import unittest

from test_remapeamento_mundo import preparar_remapeamento, iniciar_remapeamento


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1','Optional x86: RISING_EMULAR=1')
class DiferencialRemapeamentoMundo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_remapeamento_mundo import BancadaRemapeamentoMundo
        cls.bancada = BancadaRemapeamentoMundo()

    def comparar(self,m):
        self.bancada.carregar_remapeamento(m)
        regs = self.bancada.iniciar()
        pedido = iniciar_remapeamento(m)
        self.assertEqual(self.bancada.conferir_remapeamento(m),[])
        self.assertEqual(self.bancada.preenchimentos,[('colors',0,65536),('released',1,256),('regions',0,131072)])
        self.assertEqual(struct.unpack('<II',self.bancada.cpu.mem_read(regs['ESP'],8)),(pedido.flags,pedido.tamanho))
        self.assertEqual(regs['EIP'],pedido.endereco_dependencia)

    def test_patterns_search_states_and_all_retained_world_buffers(self):
        for seed in (0,1,31,128,165,255):
            for unidade in (0,7,799,65535):
                self.comparar(preparar_remapeamento(seed,unidade))

    def test_no_dimension_or_active_unit_guard_before_allocation(self):
        for largura,altura in ((0,0),(1,256),(256,1),(65535,65535)):
            m = preparar_remapeamento()
            m.largura,m.altura = largura,altura
            m.unidades[:] = b'\xff'*220800
            self.comparar(m)

    def test_search_then_color_fills_free_list_then_region_fill_order(self):
        from ordens_unidades import ContextoBusca
        eventos = []

        class BuscaRastreada(ContextoBusca):
            def __setattr__(self,nome,valor):
                if getattr(self,'rastrear',False) and nome != 'rastrear':
                    eventos.append(('search',nome,valor))
                super().__setattr__(nome,valor)

        class BytesRastreados(bytearray):
            def __setitem__(self,chave,valor):
                if isinstance(chave,slice):
                    eventos.append(('fill',self.nome,valor[0],len(valor)))
                else: eventos.append(('free',chave,valor))
                super().__setitem__(chave,valor)

        class RegioesRastreadas(list):
            def __setitem__(self,chave,valor):
                eventos.append(('fill','regions',0,len(valor)*2))
                super().__setitem__(chave,valor)

        m = preparar_remapeamento()
        self.bancada.carregar_remapeamento(m)
        self.bancada.rastrear = True
        try: self.bancada.iniciar()
        finally: self.bancada.rastrear = False
        m.busca = BuscaRastreada(**vars(m.busca))
        m.busca.rastrear = True
        m.regioes = RegioesRastreadas(m.regioes)
        for nome,rotulo in (('grade','colors'),('liberadas','released'),('livres','free')):
            buf = BytesRastreados(getattr(m.cores_estruturas,nome))
            buf.nome = rotulo
            setattr(m.cores_estruturas,nome,buf)
        iniciar_remapeamento(m)
        self.assertEqual(eventos,self.bancada.escritas)
        self.assertEqual(len(eventos),263)
        self.assertEqual(self.bancada.conferir_remapeamento(m),[])
        type(self).eventos_ordenados = len(eventos)
