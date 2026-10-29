"""Economy MissionLoad tails against original captures and fresh x86."""
import hashlib
import json
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
sys.path.insert(0, str(PASTA.parents[1]/'ferramentas'))
import casos_cauda_carga as casos
from casos_cauda_carga import MERCADO
from cauda_carga import CaudaCargaEconomia, estrutura_realizavel
from proprietarios import PASSO_ORDENS_JOGADOR, juntar_ordens

CAPTURAS = json.loads((PASTA/'evidencias/captura-cauda-carga-original.json').read_text())


def hashes_python(caso):
    m, sha = caso.mundo, lambda b: hashlib.sha256(bytes(b)).hexdigest()
    r = dict(ordens=sha(caso.ordens), contagens=sha(m.realizaveis_estruturas), contagens_tipo18=sha(caso.contagens_tipo18),
             jogadores=sha(caso.jogadores), jogadores_guardados=sha(caso.jogadores_guardados),
             capacidades=sha(caso.capacidades.memoria), estruturas=sha(m.estruturas), unidades=sha(m.unidades),
             pendencias=sha(caso.pendencias), economia=sha(caso.economia.memoria),
             estruturas_realizaveis=sha(caso.estruturas_realizaveis), mini_final=sha(m.mini_final),
             descoberto=sha(b''.join(bytes(g) for g in m.descoberto)),
             contagem_luz=sha(b''.join(bytes(g) for g in m.contagem_luz)))
    r.update({f'mercado_{n}': sha(caso.mercado[n]) for n in MERCADO})
    return r


def cauda_python(caso, modo='tail', *, bolsas=None):
    h, t = casos.montar_cauda(caso, bolsas=bolsas)
    if modo == 'habitation+tail':
        if h.estrutura_habitada(0):
            h.tornar_habitavel(caso.mundo, 0)
    t.inicializar_tecnologia_unidades()
    t.inicializar_cavernas(caso.mundo)
    t.recuperar_jogadores()
    t.resetar_mercado()
    return t


class CapturasCaudaCarga(unittest.TestCase):
    def test_python_matches_every_original_only_tail_capture(self):
        import capturar_cauda_carga_original as cap
        n = 0
        for (modo, caso), original in zip(cap._casos(), CAPTURAS['cases']):
            self.assertEqual(caso.nome, original['name'])
            for nome, valor in hashes_python(caso).items():
                self.assertEqual(valor, original['input'][nome], (caso.nome, nome))
            cauda_python(caso, modo)
            for nome, valor in hashes_python(caso).items():
                self.assertEqual(valor, original['output']['sha256'][nome], (caso.nome, nome))
            n += 1
        self.assertEqual(n, len(CAPTURAS['cases']))


class ExemplosCaudaCarga(unittest.TestCase):
    def test_monde01_counts_one_sanctuary_and_no_cave(self):
        caso = next(casos.casos_monde01())
        cauda_python(caso)
        contagens = caso.mundo.realizaveis_estruturas
        self.assertEqual(contagens[2], 1)
        self.assertEqual(sum(contagens), 1)
        self.assertEqual([struct.unpack_from('<H', caso.capacidades.memoria, j*6)[0] for j in range(4)], [0]*4)
        self.assertEqual(bytes(caso.contagens_tipo18), bytes(4))

    def test_builder_bag_lists_realizable_types_except_20_and_network_8_12(self):
        for rede, ausentes in ((0, {20}), (1, {8, 12, 20}), (0x80, {8, 12, 20})):
            caso = casos.estender(casos.base.caso_sintetico('bag', 2, 0, 0x4040), rede=rede, padrao_realizaveis='um')
            antes = bytes(caso.ordens)
            _, t = casos.montar_cauda(caso)
            t.definir_tecnologia_unidades(2)
            b = caso.ordens[2*2704+7*104:2*2704+8*104]
            esperado = [x for x in range(22) if x not in ausentes]
            self.assertEqual(struct.unpack_from('<HH', b, 0), (len(esperado), 22))
            self.assertEqual([(b[0x42+i], struct.unpack_from('<H', b, 6+2*i)[0]) for i in range(len(esperado))],
                             [(3, x) for x in esperado])
            self.assertEqual(b[0x60:0x66], antes[2*2704+7*104+0x60:2*2704+7*104+0x66])
            b14 = caso.ordens[2*2704+14*104:2*2704+15*104]
            self.assertEqual((struct.unpack_from('<HH', b14, 0), b14[0x42], struct.unpack_from('<H', b14, 6)[0]),
                             ((1, 1), 7, 6))
            b8 = caso.ordens[2*2704+8*104:2*2704+9*104]
            self.assertEqual([(b8[0x42+i], struct.unpack_from('<H', b8, 6+2*i)[0]) for i in range(4)],
                             [(2, 0), (2, 1), (2, 2), (2, 3)])
            fora = bytearray(caso.ordens)
            for tipo in (7, 8, 14):
                o = 2*2704+tipo*104
                fora[o:o+104] = antes[o:o+104]
            self.assertEqual(bytes(fora), antes)

    def test_player_retrieve_copies_only_alliance_and_sympathies(self):
        caso = next(casos.casos_monde01())
        vivos, guardados = bytes(caso.jogadores), bytes(caso.jogadores_guardados)
        _, t = casos.montar_cauda(caso)
        t.recuperar_jogadores()
        for j in range(4):
            for k in range(20):
                origem = guardados if k == 6 or 12 <= k < 20 else vivos
                self.assertEqual(caso.jogadores[j*20+k], origem[j*20+k], (j, k))

    def test_separate_owner_pools_match_the_legacy_contiguous_fixture(self):
        for semente, rede in ((60, 0), (61, 1), (62, 0x80)):
            legado = casos.caso_pool(f'legacy {semente}', semente=semente, rede=rede)
            separado = casos.caso_pool(f'legacy {semente}', semente=semente, rede=rede)
            bolsas = [bytearray(separado.ordens[j*2704:(j+1)*2704]) for j in range(4)]
            antes_fixture = bytes(separado.ordens)
            t = cauda_python(separado, bolsas=bolsas)
            self.assertTrue(all(a is b for a, b in zip(t.habitacao.propriedade.ordens, bolsas)))
            cauda_python(legado)
            esperado = hashes_python(legado)
            obtido = hashes_python(separado)
            self.assertEqual(obtido.pop('ordens'), hashlib.sha256(antes_fixture).hexdigest())
            self.assertEqual(b''.join(bolsas), bytes(legado.ordens))
            esperado.pop('ordens')
            self.assertEqual(obtido, esperado)

    def test_load_tail_rejects_a_rebound_single_buffer_before_any_store(self):
        caso = next(casos.casos_monde01())
        h, t = casos.montar_cauda(caso)
        originais = h.propriedade.ordens
        antes = hashes_python(caso), [bytes(x) for x in originais]
        for invalido in (bytearray(10816), list(h.propriedade.ordens[:3]),
                         [bytearray(2704), bytearray(2704), bytearray(2704), bytearray(2703)]):
            h.propriedade.ordens = invalido
            with self.assertRaises(ValueError):
                CaudaCargaEconomia(h, t.ciclo, rede=caso.rede_bytes, jogadores_guardados=caso.jogadores_guardados)
            with self.assertRaises(ValueError):
                t.definir_tecnologia_unidades(0)
        self.assertEqual((hashes_python(caso), [bytes(x) for x in originais]), antes)

    def test_protected_domains_and_shared_identity(self):
        caso = next(casos.casos_monde01())
        _, t = casos.montar_cauda(caso)
        for jogador, tipo in ((4, 0), (0, 22)):
            with self.assertRaises(ValueError):
                estrutura_realizavel(caso.estruturas_realizaveis, caso.rede_bytes, jogador, tipo)
        with self.assertRaises(ValueError):
            t.definir_tecnologia_unidades(4)
        outro = casos.base.caso_sintetico('outro', 2, 0, 0x4040).mundo
        antes = bytes(caso.mundo.realizaveis_estruturas)
        with self.assertRaises(ValueError):
            t.inicializar_cavernas(outro)
        self.assertEqual(bytes(caso.mundo.realizaveis_estruturas), antes)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional original x86: RISING_EMULAR=1')
class DiferencialCaudaCarga(unittest.TestCase):
    bancadas = []

    @classmethod
    def setUpClass(cls):
        from bancada_cauda_carga import BancadaCaudaCarga
        cls.b = BancadaCaudaCarga()
        cls.bancadas.append(cls.b)

    def conferir(self, caso):
        b = self.b
        estado = b.estado()
        m = caso.mundo
        for nome, valor in (('estruturas', m.estruturas), ('unidades', m.unidades), ('pendencias', caso.pendencias),
                            ('capacidades', caso.capacidades.memoria), ('economia', caso.economia.memoria),
                            ('estruturas_realizaveis', caso.estruturas_realizaveis), ('ordens', caso.ordens),
                            ('contagens', m.realizaveis_estruturas), ('contagens_tipo18', caso.contagens_tipo18),
                            ('jogadores', caso.jogadores), ('jogadores_guardados', caso.jogadores_guardados),
                            ('rede', bytes([caso.rede]))):
            self.assertEqual(estado[nome], bytes(valor), (caso.nome, nome))
        for nome in MERCADO:
            self.assertEqual(estado[f'mercado_{nome}'], bytes(caso.mercado[nome]), (caso.nome, nome))
        self.assertEqual(b.conferir_saida(m), [], caso.nome)
        self.assertEqual(b.guardas(), b.guardas_iniciais, caso.nome)
        self.assertEqual(b.guardas_extra(), b.guardas_cauda, caso.nome)

    def tail(self, caso, modo='tail', *, nome_loader=False):
        b = self.b
        b.carregar(caso)
        if modo == 'habitation+tail':
            self.assertEqual(b.varrer_estrutura(0)['EIP'], 0x46c1a7)
        par = b.cauda_nome_tecnologia_cavernas if nome_loader else b.cauda_tecnologia_cavernas
        self.assertEqual(par()['EIP'], 0x46c982 if nome_loader else 0x46c5b9)
        self.assertEqual(b.cauda_jogadores()['EIP'], 0x46c5c3)
        self.assertEqual(b.cauda_mercado()['EIP'], 0x46c5d6)
        cauda_python(caso, modo)
        self.conferir(caso)

    def test_actual_monde01_tail_configurations_and_after_habitation(self):
        for caso in casos.casos_monde01():
            self.tail(caso)
        for padrao, rede in (('um', 0), ('aleatorio', 1)):
            caso = casos.estender(casos.base.caso_monde01(f'MONDE01 habitation {padrao} {rede}', padrao=padrao),
                                  rede=rede, padrao_realizaveis='um' if padrao == 'um' else None)
            self.tail(caso, 'habitation+tail')

    def test_random_structure_pools_networks_and_table_patterns(self):
        for semente in range(9):
            rede = (0, 1, 0x80)[semente % 3]
            padrao = ('aleatorio', 'zero', 'um')[semente//3]
            self.tail(casos.caso_pool(f'pool {semente}', semente=semente, rede=rede, padrao=padrao))

    def test_mission_load_name_call_sites(self):
        for semente in (20, 21):
            self.tail(casos.caso_pool(f'name pool {semente}', semente=semente, rede=semente % 2), nome_loader=True)
        self.tail(next(casos.casos_monde01()), nome_loader=True)

    def test_byte_count_wrap_for_caves_and_heliports(self):
        caso = casos.caso_pool('wrap', semente=30, rede=0)
        s = caso.mundo.estruturas
        for i in range(1000):
            s[i*276+4], s[i*276+5], s[i*276+8] = 1, 0, 0
        for i in range(300):
            s[i*276+5], s[i*276+8] = 7, 3
        for i in range(300, 557):
            s[i*276+5], s[i*276+8] = 1, 18
        self.tail(caso)
        self.assertEqual(caso.mundo.realizaveis_estruturas[22+3], 300 & 255)
        self.assertEqual(caso.contagens_tipo18[1], 257 & 255)

    def test_direct_type_realizable_every_owner_type_and_network(self):
        b = self.b
        rng = random.Random(0x418a93)
        caso = casos.caso_pool('realizable', semente=40, rede=0)
        b.carregar(caso)
        for rede in (0, 1, 0x80, 255):
            caso.estruturas_realizaveis[:] = bytes(rng.choice((0, 1, 2, 0x80, 255)) for _ in range(88))
            b.cpu.mem_write(0x4dfad4, bytes(caso.estruturas_realizaveis))
            b.cpu.mem_write(0x4e0730, bytes([rede]))
            for jogador in range(4):
                for tipo in range(22):
                    regs = b.estrutura_realizavel(jogador | 0x7700, tipo | 0x3300)
                    self.assertEqual(regs['EAX'] & 255,
                                     estrutura_realizavel(caso.estruturas_realizaveis, bytes([rede]), jogador, tipo))
                    self.assertEqual(regs['EBX'], 0x13572468)

    def test_engin_init_technologie_through_four_page_aligned_owner_allocations(self):
        """The original shape: [0x4e19b8] -> four separate pages with gaps (MONDE01 0x41781000..)."""
        from bancada_cauda_carga import TABELA_ORDENS
        b = self.b
        base, passo = TABELA_ORDENS + 0x5000, 0x1000
        enderecos = [base + j*passo for j in range(4)]
        antigo = bytes(b.cpu.mem_read(TABELA_ORDENS, 16))
        self.addCleanup(b.cpu.mem_write, TABELA_ORDENS, antigo)
        casos_teste = list(casos.casos_monde01()) + [casos.caso_pool(f'paged {s}', semente=70+s, rede=s % 3)
                                                     for s in range(3)]
        for caso in casos_teste:
            b.carregar(caso)
            rng = random.Random(f'paged:{caso.nome}')
            lacunas = bytes(rng.randbytes(4*passo))
            b.cpu.mem_write(base, lacunas)
            bolsas = [bytearray(rng.randbytes(PASSO_ORDENS_JOGADOR)) for _ in range(4)]
            for endereco, bolsa in zip(enderecos, bolsas):
                b.cpu.mem_write(endereco, bytes(bolsa))
            b.apontar_ordens(enderecos)
            self.assertEqual(b.inicializar_tecnologia_unidades()['EIP'], 0x3000000)
            _, t = casos.montar_cauda(caso, bolsas=bolsas)
            antes = [bytes(x) for x in bolsas]
            t.inicializar_tecnologia_unidades()
            self.assertNotEqual([bytes(x) for x in bolsas], antes, caso.nome)
            for j, (endereco, bolsa) in enumerate(zip(enderecos, bolsas)):
                self.assertEqual(bytes(b.cpu.mem_read(endereco, PASSO_ORDENS_JOGADOR)), bytes(bolsa), (caso.nome, j))
                fim = endereco + PASSO_ORDENS_JOGADOR
                self.assertEqual(bytes(b.cpu.mem_read(fim, passo - PASSO_ORDENS_JOGADOR)),
                                 lacunas[fim-base:(j+1)*passo], (caso.nome, 'gap', j))
            self.conferir(caso)  # contiguous fixture region and all other state untouched on both sides
            b.apontar_ordens(struct.unpack('<4I', antigo))

    def test_direct_engin_set_technologie_with_high_register_bits(self):
        b = self.b
        for semente in range(6):
            caso = casos.caso_pool(f'unit bags {semente}', semente=50+semente, rede=semente % 3)
            b.carregar(caso)
            _, t = casos.montar_cauda(caso)
            for jogador in (3, 0, 2, 1):
                self.assertEqual(b.tecnologia_unidades(jogador | 0xabcd00)['EIP'], 0x3000000)
                t.definir_tecnologia_unidades(jogador)
            self.conferir(caso)
