"""BatimentEstHabiter/BatimentHabitable against original captures and fresh x86."""
import hashlib
import json
import os
from pathlib import Path
import random
import struct
import sys
import unittest
from unittest import mock

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
sys.path.insert(0, str(PASTA.parents[1]/'ferramentas'))
import casos_habitaveis as casos
import construcoes_habitaveis as ch
from construcoes_habitaveis import DependenciaHabitacao
from navegacao_unidades import MundoNavegacao

CAPTURAS = json.loads((PASTA/'evidencias/captura-habitaveis-original.json').read_text())
RETORNO_CHAMADOR = 0x46c1a7


class MundoRastreado(MundoNavegacao):
    """Diagnostic delegation only; every effect stays in core's methods."""
    def __init__(self, *args):
        self.efeitos = []
        super().__init__(*args)

    def descobrir_area(self, celula, raio, dono):
        self.efeitos.append(('discovery', celula, raio, dono))
        return super().descobrir_area(celula, raio, dono)

    def iluminar_area(self, celula, raio, dono):
        self.efeitos.append(('light', celula, raio, dono))
        return super().iluminar_area(celula, raio, dono)

    def minimapa(self, dono, celula, modo):
        self.efeitos.append(('minimap', dono, celula, modo))
        return super().minimapa(dono, celula, modo)


def parada_esperada(caso, indice=None):
    """Declared boundary from the gates and the record, independent of the API."""
    s = caso.mundo.estruturas
    o = (caso.indice if indice is None else indice)*276
    tipo, dono = s[o+8], s[o+4]
    if tipo in ch.TIPOS_SEM_VISAO:
        return None
    descoberta, luz = ch.limites_visao()
    raio = ch.RAIOS[tipo]
    if dono >= 4 or raio+3 > descoberta:
        return 0x476851
    if raio > luz:
        return 0x476cb3
    return None


def executar_python(h, caso, modo):
    try:
        if modo == 'predicate':
            return h.estrutura_habitada(caso.indice), None
        if modo == 'caller':
            if not h.estrutura_habitada(caso.indice):
                return 0, None
        return h.tornar_habitavel(caso.mundo, caso.indice), None
    except DependenciaHabitacao as e:
        return None, e.endereco
    except ZeroDivisionError:
        return None, 'fault'


def hashes_python(caso):
    m, sha = caso.mundo, lambda b: hashlib.sha256(bytes(b)).hexdigest()
    juntar = lambda grades: b''.join(bytes(g) for g in grades)
    return dict(estruturas=sha(m.estruturas), unidades=sha(m.unidades), pendencias=sha(caso.pendencias),
                capacidades=sha(caso.capacidades.memoria), economia=sha(caso.economia.memoria),
                unidades_realizaveis=sha(caso.unidades_realizaveis), estruturas_realizaveis=sha(caso.estruturas_realizaveis),
                sortilegios=sha(caso.sortilegios), inventados=sha(caso.inventados), mini_final=sha(m.mini_final),
                mini_unidades=sha(m.mini_unidades), descoberto=sha(juntar(m.descoberto)),
                luz_bordas=sha(juntar(m.luz_bordas)), contagem_luz=sha(juntar(m.contagem_luz)))


class CapturasHabitaveis(unittest.TestCase):
    def test_python_matches_every_original_only_capture_or_its_declared_stop(self):
        import capturar_habitaveis_original as cap
        concluidos = paradas = 0
        for (modo, caso), original in zip(cap._casos(), CAPTURAS['cases']):
            self.assertEqual(caso.nome, original['name'])
            # Fixtures are deterministic: the Python input equals the captured input.
            for nome, valor in hashes_python(caso).items():
                self.assertEqual(valor, original['input'][nome], (caso.nome, nome))
            esperado = (None if modo == 'predicate' else
                        0x476851 if modo == 'habitable_owner4_stop' else parada_esperada(caso))
            resultado, parada = executar_python(casos.montar_habitacao(caso), caso, modo)
            atual = hashes_python(caso)
            if modo == 'predicate':
                self.assertEqual(resultado, original['al'], caso.nome)
            if parada is None and modo != 'habitable_owner4_stop':
                self.assertIsNone(esperado, caso.nome)
                concluidos += 1
                for nome, valor in atual.items():
                    self.assertEqual(valor, original['output']['sha256'][nome], (caso.nome, nome))
            else:
                # Before core publishes wider gates: the stop precedes discovery;
                # physical grids keep their captured inputs, earlier Bags changed.
                self.assertEqual(parada, esperado, caso.nome)
                paradas += 1
                for nome in ('descoberto', 'luz_bordas', 'contagem_luz', 'mini_final'):
                    self.assertEqual(atual[nome], original['input'][nome], (caso.nome, nome))
                for nome in ('pendencias', 'capacidades', 'economia'):
                    self.assertEqual(atual[nome], original['output']['sha256'][nome], (caso.nome, nome))
        self.assertEqual(concluidos+paradas, len(CAPTURAS['cases']))

    def test_actual_monde01_is_sanctuary_with_eight_colonists_and_centre_0c0e(self):
        caso = casos.caso_monde01()
        s = caso.mundo.estruturas
        self.assertEqual((s[4], s[5], s[8], struct.unpack_from('<H', s, 2)[0]), (0, 5, 2, 0x0b0c))
        h = casos.montar_habitacao(caso)
        self.assertEqual(h.estrutura_habitada(0), 1)
        self.assertEqual(ch.celula_central_estrutura(s, 0), 0x0c0e)
        evidencia = json.loads((PASTA/'evidencias/habitaveis.json').read_text())
        nomes = [r['name'] for r in evidencia['structure_type_table']['records']]
        self.assertEqual((nomes[2], nomes[3]), ('SANCTUAIRE', 'CAVE'))
        self.assertEqual(evidencia['radius_by_type'], list(ch.RAIOS))


class ExemplosHabitaveis(unittest.TestCase):
    def caso(self, tipo, dono=0, **kw):
        kw.setdefault('padrao', 'um')
        caso = casos.caso_sintetico(f't{tipo}', tipo, dono, 0x4040, indice=7, **kw)
        return caso, casos.montar_habitacao(caso)

    def bag(self, caso, dono, tipo):
        o = dono*2288+tipo*104
        return caso.pendencias[o:o+104]

    def test_technology_branches_reset_and_append_in_original_order(self):
        esperados = {1: [(6, 0), (6, 1), (6, 2), (6, 8)], 2: [(6, 5), (6, 6), (6, 7)], 3: [],
                     5: [(6, u) for u in range(11, 16)], 13: [(6, 3), (6, 25)], 15: [(6, 4), (3, 20)],
                     16: [(6, 10)], 18: [(6, 16)], 20: [(6, 4), (4, 5)]}
        capacidades = {1: 4, 2: 4, 3: 3, 5: 5, 13: 2, 15: 2, 16: 1, 18: 1, 20: 2}
        for tipo, itens in esperados.items():
            caso, h = self.caso(tipo, 2)
            antes = bytes(caso.pendencias)
            h.definir_tecnologia(2, tipo)
            b = self.bag(caso, 2, tipo)
            n = len(itens)
            self.assertEqual(struct.unpack_from('<HHH', b, 0), (n, capacidades[tipo], 0))
            self.assertEqual([(b[0x42+i], struct.unpack_from('<H', b, 6+2*i)[0]) for i in range(n)], itens)
            self.assertEqual(struct.unpack_from('<H', b, 0x66)[0], n)
            self.assertEqual(b[0x60:0x66], antes[2*2288+tipo*104+0x60:2*2288+tipo*104+0x66])
            fora = bytearray(caso.pendencias)
            fora[2*2288+tipo*104:2*2288+tipo*104+104] = antes[2*2288+tipo*104:2*2288+tipo*104+104]
            self.assertEqual(bytes(fora), antes)

    def test_unrealizable_units_skip_and_owner_or_type_without_branch_is_unchanged(self):
        caso, h = self.caso(2, 0, padrao='zero')
        h.definir_tecnologia(0, 15)
        self.assertEqual(self.bag(caso, 0, 15)[0], 0)
        antes = bytes(caso.pendencias)
        for jogador, tipo in ((4, 2), (255, 1), (0, 0), (0, 4), (1, 21), (3, 22), (0, 255)):
            h.definir_tecnologia(jogador, tipo)
        self.assertEqual(bytes(caso.pendencias), antes)

    def test_rejections_happen_before_any_effect(self):
        caso, h = self.caso(2)
        antes = (bytes(caso.pendencias), bytes(caso.mundo.estruturas))
        caso.mundo.estruturas[7*276+8] = 22
        with self.assertRaises(ValueError):
            h.tornar_habitavel(caso.mundo, 7)
        caso.mundo.estruturas[7*276+8] = 2
        with self.assertRaises(ValueError):
            h.tornar_habitavel(caso.mundo, 1000)
        outro = casos.caso_sintetico('outro', 2, 0, 0x4040, indice=7).mundo
        with self.assertRaises(ValueError):
            h.tornar_habitavel(outro, 7)
        self.assertEqual((bytes(caso.pendencias), bytes(caso.mundo.estruturas)), antes)

    def test_owner_four_keeps_type4_store_and_stops_before_discovery(self):
        caso, h = self.caso(4, 4, classe=MundoRastreado)
        struct.pack_into('<HH', caso.mundo.estruturas, 7*276+0x78, 0x1234, 0)
        struct.pack_into('<H', caso.mundo.estruturas, 7*276+0x84, 0x9999)
        with self.assertRaises(DependenciaHabitacao) as erro:
            h.tornar_habitavel(caso.mundo, 7)
        self.assertEqual((erro.exception.endereco, erro.exception.chamada), (0x476851, 0x41cdb9))
        self.assertEqual(struct.unpack_from('<H', caso.mundo.estruturas, 7*276+0x78)[0], 0)
        self.assertEqual(struct.unpack_from('<H', caso.mundo.estruturas, 7*276+0x84)[0], 0x9999)
        self.assertEqual(caso.mundo.efeitos, [])

    def test_light_gate_stops_after_discovery_effects(self):
        caso, h = self.caso(2, 1, classe=MundoRastreado)
        with mock.patch.object(ch, 'limites_visao', return_value=(13, 8)):
            with self.assertRaises(DependenciaHabitacao) as erro:
                h.tornar_habitavel(caso.mundo, 7)
        self.assertEqual((erro.exception.endereco, erro.exception.argumentos), (0x476cb3, (0x4142, 10, 1)))
        self.assertEqual(caso.mundo.efeitos[0], ('discovery', 0x4142, 13, 1))
        self.assertNotIn('light', [e[0] for e in caso.mundo.efeitos])

    def test_type3_division_fault_follows_bag_reset(self):
        caso, h = self.caso(3, 1, armazens=(2, 0))
        with self.assertRaises(ZeroDivisionError):
            h.tornar_habitavel(caso.mundo, 7)
        self.assertEqual(struct.unpack_from('<HH', self.bag(caso, 1, 3), 0), (0, 3))

    def test_vision_gate_reads_core_symbols_when_published(self):
        visao = ch._core('visao_movimento')
        with mock.patch.object(visao, 'RAIO_DESCOBERTA_MAXIMO_VALIDADO', 23, create=True), \
                mock.patch.object(visao, 'RAIO_LUZ_MAXIMO_VALIDADO', 20, create=True):
            self.assertEqual(ch.limites_visao(), (23, 20))

    def test_predicate_branches(self):
        for tipo, tipos_unidades, esperado in ((2, (9,), 1), (2, (4,), 1), (2, (3,), 0), (21, (9,), 1),
                                               (21, (17,), 0), (1, (4,), 0), (1, (9,), 1), (0, (), 0)):
            caso = casos.caso_sintetico(f'p{tipo}', tipo, 0, 0x4040, indice=3,
                                        unidades=tuple(range(20, 20+len(tipos_unidades))), tipos_unidades=tipos_unidades)
            self.assertEqual(casos.montar_habitacao(caso).estrutura_habitada(3), esperado, (tipo, tipos_unidades))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional original x86: RISING_EMULAR=1')
class DiferencialHabitaveis(unittest.TestCase):
    bancadas = []

    @classmethod
    def setUpClass(cls):
        from bancada_habitaveis import BancadaHabitaveis
        cls.b = BancadaHabitaveis()
        cls.bancadas.append(cls.b)

    def comparar(self, caso, modo='habitable', *, limites=None):
        from emulador import RETORNO
        b = self.b
        b.carregar(caso)
        h = casos.montar_habitacao(caso)
        caso.mundo.efeitos = []
        with mock.patch.object(ch, 'limites_visao', return_value=limites or ch.limites_visao()):
            esperado = parada_esperada(caso) if modo != 'predicate' else None
            resultado, parada = executar_python(h, caso, modo)
        if modo == 'predicate':
            regs = b.executar_ou_falhar(b.esta_habitada, caso.indice)
            self.assertEqual(regs['EAX'] & 255, resultado)
        elif modo == 'caller':
            regs = b.executar_ou_falhar(b.varrer_estrutura, caso.indice, paradas=() if esperado is None else (esperado,))
        else:
            regs = b.executar_ou_falhar(b.tornar_habitavel, caso.indice, paradas=() if esperado is None else (esperado,))
        if parada == 'fault':
            self.assertIsNone(regs)  # original #DE after the same earlier effects
        else:
            if modo == 'caller' and resultado == 0:
                alvo = RETORNO_CHAMADOR  # predicate false: BatimentHabitable is not entered
            elif esperado is not None:
                alvo = esperado
            else:
                alvo = RETORNO_CHAMADOR if modo == 'caller' else RETORNO
            self.assertEqual(regs['EIP'], alvo, caso.nome)
            self.assertEqual(parada, alvo if alvo in (0x476851, 0x476cb3) else None, caso.nome)
        estado = b.estado()
        for nome, valor in (('estruturas', caso.mundo.estruturas), ('unidades', caso.mundo.unidades),
                            ('pendencias', caso.pendencias), ('capacidades', caso.capacidades.memoria),
                            ('economia', caso.economia.memoria), ('unidades_realizaveis', caso.unidades_realizaveis),
                            ('estruturas_realizaveis', caso.estruturas_realizaveis), ('sortilegios', caso.sortilegios),
                            ('inventados', caso.inventados)):
            self.assertEqual(estado[nome], bytes(valor), (caso.nome, nome))
        self.assertEqual(b.conferir_saida(caso.mundo), [], caso.nome)
        self.assertEqual(b.guardas(), b.guardas_iniciais, caso.nome)
        self.assertEqual([tuple(e) for e in b.efeitos], caso.mundo.efeitos, caso.nome)
        return regs

    def test_actual_monde01_caller_scan_tables_grids_and_cameras(self):
        for padrao in ('zero', 'um', 'aleatorio'):
            for grades in (False, True):
                for local in (0, 1):
                    self.comparar(casos.caso_monde01(f'MONDE01 {padrao} {grades} {local}', padrao=padrao,
                                                     semear_grades=grades, local=local, classe=MundoRastreado), 'caller')

    def test_all_22_types_for_each_owner_with_edges(self):
        rng = random.Random(0x41cc70)
        origens = (0x0000, 0x00fa, 0xfa00, 0xfafa, 0x8080, 0x0f0f)
        for tipo in range(22):
            for dono in range(4):
                origem = origens[(tipo+dono) % len(origens)] if (tipo+dono) % 3 else rng.randrange(65536)
                self.comparar(casos.caso_sintetico(f'type {tipo} owner {dono}', tipo, dono, origem,
                                                   armazens=(rng.randrange(1, 9), rng.randrange(1, 200)),
                                                   semear_grades=(tipo+dono) % 4 == 0, semente=dono,
                                                   local=dono, classe=MundoRastreado))

    def test_owner_bytes_above_three(self):
        for tipo in (0, 2, 3, 4, 9, 12, 17, 21):
            for dono in (4, 200, 255):
                self.comparar(casos.caso_sintetico(f'type {tipo} owner {dono}', tipo, dono, 0x3040,
                                                   armazens=(2, 9), classe=MundoRastreado))

    def test_small_maps_and_cameras(self):
        for largura, altura in ((40, 40), (64, 32), (256, 20)):
            for tipo, origem in ((0, 0x0000), (2, 0x1010), (4, 0x0505), (21, 0x0101)):
                for local in (0, 3):
                    self.comparar(casos.caso_sintetico(f'{largura}x{altura} type {tipo} cam {local}', tipo, local,
                                                       origem, largura=largura, altura=altura, local=local,
                                                       semear_grades=True, classe=MundoRastreado))

    def test_type3_level_edges_and_division_fault(self):
        for armazens in ((0, 5), (1, 1), (65535, 1), (2, 65535), (3, 0), (1, 7)):
            self.comparar(casos.caso_sintetico(f'cave {armazens}', 3, 1, 0x2020, armazens=armazens,
                                               classe=MundoRastreado))

    def test_light_gate_stop_with_lowered_limits(self):
        for tipo in (2, 1):
            self.comparar(casos.caso_sintetico(f'light gate {tipo}', tipo, 0, 0x3030, classe=MundoRastreado),
                          limites=(13, 7))

    def test_predicate_unit_types_tags_and_capacity(self):
        for tipo in (0, 1, 2, 3, 16, 21):
            for t in list(range(26)) + [26, 200, 255]:
                self.comparar(casos.caso_sintetico(f'pred {tipo} {t}', tipo, 0, 0x4040, unidades=(30, 31),
                                                   tipos_unidades=(t, 3)), 'predicate')
            for etiquetas, capacidade in (((0, 6), None), ((1, 1), 0), ((2, 1), 30)):
                self.comparar(casos.caso_sintetico(f'pred {tipo} tags {etiquetas} cap {capacidade}', tipo, 0, 0x4040,
                                                   unidades=(32, 33), tipos_unidades=(9, 9), etiquetas=etiquetas,
                                                   capacidade=capacidade), 'predicate')

    def test_caller_fragment_with_false_and_true_predicates(self):
        for tipo, tipos_unidades in ((2, (25,)), (21, (17,)), (16, (4,)), (16, (9,)), (21, (9,))):
            self.comparar(casos.caso_sintetico(f'caller {tipo} {tipos_unidades}', tipo, 0, 0x5050, unidades=(40,),
                                               tipos_unidades=tipos_unidades, classe=MundoRastreado), 'caller')

    def test_technology_every_dl_for_four_al_values(self):
        b = self.b
        rng = random.Random(0x41c76c)
        caso = casos.caso_sintetico('technology', 2, 0, 0x4040, padrao='aleatorio')
        h = casos.montar_habitacao(caso)
        b.carregar(caso)
        for jogador in (0, 3, 4, 255):
            for tipo in range(256):
                caso.unidades_realizaveis[:] = bytes(rng.choice((0, 1, 0x80)) for _ in range(104))
                caso.estruturas_realizaveis[:] = bytes(rng.choice((0, 1)) for _ in range(88))
                caso.sortilegios[:] = bytes(rng.choice((0, 1)) for _ in range(20))
                caso.inventados[:] = bytes(rng.choice((0, 1)) for _ in range(20))
                for base, valor in ((0x4e1934, caso.unidades_realizaveis), (0x4dfad4, caso.estruturas_realizaveis),
                                    (0x508f30, caso.sortilegios), (0x508f44, caso.inventados)):
                    b.cpu.mem_write(base, bytes(valor))
                h.definir_tecnologia(jogador | 0x5a00, tipo | 0xa500)
                b.definir_tecnologia(jogador | 0x5a00, tipo | 0xa500)
                self.assertEqual(bytes(b.cpu.mem_read(0x4dd6e8, 9152)), bytes(caso.pendencias), (jogador, tipo))
        self.assertEqual(b.guardas(), b.guardas_iniciais)
        self.assertEqual(bytes(b.cpu.mem_read(0x49a0c8, 276000)), bytes(caso.mundo.estruturas))

    def test_get_case_all_types_and_origins_preserve_edx_ebx(self):
        b = self.b
        caso = casos.caso_sintetico('centre', 0, 0, 0)
        b.carregar(caso)
        for tipo in range(22):
            for origem in (0x0000, 0xffff, 0x80ff, 0xff80, 0x1234, 0xfefe):
                caso.mundo.estruturas[5*276+8] = tipo
                struct.pack_into('<H', caso.mundo.estruturas, 5*276+2, origem)
                b.cpu.mem_write(0x49a0c8+5*276, bytes(caso.mundo.estruturas[5*276:6*276]))
                regs = b.celula_central(5 | 0x770000)
                self.assertEqual(regs['EAX'] & 65535, ch.celula_central_estrutura(caso.mundo.estruturas, 5), (tipo, origem))
                self.assertEqual((regs['EDX'], regs['EBX']), (0x1234abcd, 0x5eed0bb5))
        self.assertEqual(bytes(b.cpu.mem_read(0x49a0c8, 276000)), bytes(caso.mundo.estruturas))
