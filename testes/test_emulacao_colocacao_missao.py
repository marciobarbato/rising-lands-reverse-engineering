"""Fresh unpatched mission placement, predicates and production regression."""
import os
import unittest

from test_colocacao_saida import preparar, colocar_unidade_saida, DependenciaColocacaoSaida
from colocacao_missao import colocar_unidade_missao, DependenciaColocacaoMissao
from consultas_unidades import existe_unidade, visibilidade_unidade


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1','Optional x86: RISING_EMULAR=1')
class DiferencialColocacaoMissao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_colocacao_missao import BancadaColocacaoMissao
        cls.bancada = BancadaColocacaoMissao(segmentar=True)

    def comparar(self,m,indice,*,saida=False,parada=None):
        self.bancada.carregar_saida(m)
        if saida:
            nativo = lambda: self.bancada.colocar(indice,0x808,**({'parada':parada} if parada else {}))
            python = lambda: colocar_unidade_saida(m,indice,0x808)
            dependencia = DependenciaColocacaoSaida
        else:
            nativo = lambda: self.bancada.colocar_missao(indice,**({'parada':parada} if parada else {}))
            python = lambda: colocar_unidade_missao(m,indice)
            dependencia = DependenciaColocacaoMissao
        nativo()
        if parada:
            with self.assertRaises(dependencia) as captura: python()
            self.assertEqual(captura.exception.checkpoint,parada)
        else: python()
        self.assertEqual(self.bancada.conferir_saida(m),[])
        self.assertEqual(self.bancada.efeitos,m.efeitos)

    def test_predicates_all_bytes_edge_indices_full_pool_and_preserved_edx(self):
        from emulador import UNIDADES
        m = preparar()
        for indice in (0,799):
            p = indice*276
            m.unidades[p:p+2] = b'\xff\xff'
            for valor in range(256):
                m.unidades[p+2],m.unidades[p+0x72] = valor,255-valor
                self.bancada.carregar_consulta(m)
                regs = self.bancada.existe(0xabcd0000 | indice)
                self.assertEqual(regs['EAX'],int(existe_unidade(m,indice)))
                self.assertEqual(regs['EDX'],0xabcd1234)
                self.assertEqual(bytes(self.bancada.cpu.mem_read(UNIDADES,220800)),bytes(m.unidades))
                regs = self.bancada.visibilidade(0xabcd0000 | indice)
                self.assertEqual(regs['EAX'] & 255,visibilidade_unidade(m,indice))
                self.assertEqual(regs['EDX'],0xabcd1234)
                self.assertEqual(bytes(self.bancada.cpu.mem_read(UNIDADES,220800)),bytes(m.unidades))

    def test_mission_all_types_owners_edge_indices_and_every_state(self):
        for tipo in range(26):
            for dono in (0,1,2,3,4,200):
                for indice in (0,799):
                    self.comparar(preparar(tipo,dono,(0,4,14)[tipo % 3],indice),0xabcd0000 | indice)
        for estado in range(256):
            self.comparar(preparar(estado=estado),7)

    def test_geometry_quad_footprints_and_unsaturated_vision_with_native_resumes(self):
        for largura,altura in ((16,16),(32,16),(64,64),(128,64),(256,256)):
            for celula in (0,largura-1,(altura-1)*256,(altura-1)*256+largura-1):
                for tipo in (1,3,16,17):
                    m = preparar(tipo,(0,200)[tipo % 2],largura=largura,altura=altura)
                    m.palavra(7,8,celula)
                    self.comparar(m,7)
        for raio in range(9):
            for dono in (0,3):
                self.comparar(preparar(tipo=3,dono=dono,raio=raio),7)
        self.assertGreater(self.bancada.retomadas_minimapa,0)

    def test_large_vision_keeps_partial_effects_at_each_original_caller(self):
        for indice in (0,799):
            for raio,extra in ((9,0),(8,1),(255,255)):
                self.comparar(preparar(indice=indice,raio=raio,extra=extra),indice,parada=0x457019)
                self.comparar(preparar(indice=indice,raio=raio,extra=extra),indice,saida=True,parada=0x446146)

    def test_factored_production_entry_all_types_owners_and_edge_indices(self):
        for tipo in range(26):
            for dono in (0,1,2,3,4,200):
                for indice in (0,799):
                    self.comparar(preparar(tipo,dono,(0,4,14)[tipo % 3],indice),indice,saida=True)
