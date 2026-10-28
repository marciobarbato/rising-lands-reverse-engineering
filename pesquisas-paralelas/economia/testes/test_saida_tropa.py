"""Original-prefix buffer comparisons, including partial credit failures."""
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from construcoes import EconomiaConstrucoes, RetiradaColonoPendente
from recrutamento import Recrutamento
from saida_tropa import SaidaTropa, PreparacaoSaidaTropa


def w(bloco, base, valor):
    struct.pack_into('<H', bloco, base, valor & 65535)


def d(bloco, base, valor):
    struct.pack_into('<I', bloco, base, valor & 0xffffffff)


def bag(bloco, base, entradas, capacidade=30, contador=None):
    w(bloco, base, len(entradas))
    w(bloco, base + 2, capacidade)
    w(bloco, base + 0x66, len(entradas) if contador is None else contador)
    for slot in range(30):
        etiqueta, valor = entradas[slot] if slot < len(entradas) else (0, 0)
        bloco[base + 0x42 + slot] = etiqueta
        w(bloco, base + 6 + slot * 2, valor)


def preparar(indice=0, unidade=799, entradas=((2, 1), (2, 2), (2, 0), (2, 2))):
    r = Recrutamento(EconomiaConstrucoes(estruturas=bytes(1000 * 276)))
    o = indice * 276
    s = r.mundo.estruturas
    s[o + 4], s[o + 8], s[o + 0x7b] = 0, 1, 7
    # SortieTroupe itself does not test +0x74 or +5.
    w(r.tipos_unidades, 7 * 50, 10)
    d(s, o + 0x8c, 1000)
    bag(s, o + 0xc, ((3, 44), (1, unidade), (2, 1)))
    r.unidades[unidade * 276 + 1] = 9
    bag(r.unidades, unidade * 276 + 0xa, entradas)
    r.mundo.capacidades.configurar(0, 1, 100)
    return SaidaTropa(r)


def estado(r):
    m = r.mundo
    e = dict(economia=bytes(m.economia.memoria), capacidades=bytes(m.capacidades.memoria),
             estruturas=bytes(m.estruturas), tipos=bytes(m.terreno.tipos),
             quantidades=bytes(m.terreno.quantidades), semente=m.terreno.semente)
    e.update({k: bytes(getattr(r, k)) for k in ('selecoes', 'tipos_unidades', 'tipos_sortilegios', 'unidades')})
    e['periodo_nova'] = r.periodo_nova
    return e


def observar_depositos(p):
    chamadas = []
    m = p.recrutamento.mundo
    original = m.adicionar
    def adicionar(jogador, recurso, quantidade, indice):
        chamadas.append((jogador, recurso, quantidade, indice))
        return original(jogador, recurso, quantidade, indice)
    m.adicionar = adicionar
    return chamadas


class ExemplosSaidaTropa(unittest.TestCase):
    def test_threshold_no_mutation_then_pending_existing_colonist(self):
        p = preparar()
        r = p.recrutamento
        d(r.mundo.estruturas, 0x8c, 999)
        antes = estado(r)
        self.assertIsNone(p.preparar(0, 4))
        self.assertEqual(estado(r), antes)
        d(r.mundo.estruturas, 0x8c, 1000)
        self.assertEqual(p.preparar(0xface0000, 0xabcd0104), PreparacaoSaidaTropa(0, 4, 799, 7))
        self.assertEqual(r.unidades[799 * 276 + 1], 9)  # Conversion is still pending.
        self.assertEqual(struct.unpack_from('<I', r.mundo.estruturas, 0x8c)[0], 1000)

    def test_cargo_stone_before_food_with_resource_id_as_credit_quantity(self):
        p = preparar()
        chamadas = observar_depositos(p)
        p.preparar(0, 4)
        self.assertEqual(chamadas, [(0, 2, 2, 0), (0, 2, 2, 0), (0, 1, 1, 0)])
        self.assertEqual(p.recrutamento.mundo.economia.consultar(0), (1, 4, 0, 0))
        # Economy query order is food/stone/parts; cargo ID 0 remains untouched.
        r = p.recrutamento
        self.assertEqual(_entries(r.unidades, 799 * 276 + 0xa), [(2, 0)])
        self.assertEqual(_entries(r.mundo.estruturas, 0xc), [(3, 44), (2, 1)])

    def test_first_matching_unit_and_compaction_preserve_unrelated_bytes(self):
        p = preparar(entradas=())
        r = p.recrutamento
        bag(r.mundo.estruturas, 0xc, ((1, 3), (1, 799), (1, 799)), contador=0)
        r.unidades[3 * 276 + 1] = 7
        antes = bytes(r.unidades)
        self.assertEqual(p.preparar(0, 255).unidade, 799)
        self.assertEqual(_entries(r.mundo.estruturas, 0xc), [(1, 3), (1, 799)])
        self.assertEqual(struct.unpack_from('<H', r.mundo.estruturas, 0x72)[0], 65535)
        self.assertEqual(bytes(r.unidades), antes)

    def test_time_zero_progress_zero_and_inactive_still_prepare(self):
        p = preparar(entradas=())
        r = p.recrutamento
        w(r.tipos_unidades, 7 * 50, 0)
        d(r.mundo.estruturas, 0x8c, 0)
        self.assertEqual(p.preparar(0, 0).unidade, 799)

    def test_division_failure_keeps_removed_colonist_cargo_and_credit(self):
        p = preparar(entradas=((2, 1), (2, 2), (2, 2)))
        r = p.recrutamento
        r.mundo.capacidades.configurar(0, 1, 0)
        r.mundo.economia.atribuir(0, 2, 12000)
        with self.assertRaises(ZeroDivisionError):
            p.preparar(0, 4)
        self.assertEqual(_entries(r.mundo.estruturas, 0xc), [(3, 44), (2, 1)])
        self.assertEqual(_entries(r.unidades, 799 * 276 + 0xa), [(2, 1), (2, 2)])
        self.assertEqual(r.mundo.economia.consultar(0).pedra, 9999)

    def test_existing_deposit_dependency_is_not_swallowed(self):
        p = preparar(entradas=((2, 2), (2, 1)))
        r = p.recrutamento
        r.mundo.estruturas[8] = 4
        w(r.mundo.estruturas, 0xe, 0)
        with self.assertRaises(RetiradaColonoPendente):
            p.preparar(0, 4)
        self.assertEqual(_entries(r.unidades, 799 * 276 + 0xa), [(2, 1)])

    def test_missing_colonist_and_invalid_references_are_protected_errors(self):
        for referencia in (3, 800):
            p = preparar()
            r = p.recrutamento
            w(r.mundo.estruturas, 0x14, referencia)
            with self.assertRaises(ValueError):
                p.preparar(0, 4)
        p = preparar()
        with self.assertRaises(ValueError):
            p.preparar(65535, 4)

    def test_invalid_unit_bag_rejected_after_colonist_removal(self):
        p = preparar()
        r = p.recrutamento
        w(r.unidades, 799 * 276 + 0xa + 2, 31)
        with self.assertRaises(ValueError):
            p.preparar(0, 4)
        self.assertEqual(_entries(r.mundo.estruturas, 0xc), [(3, 44), (2, 1)])

    def test_stale_capacity_tag_is_outside_terminating_domain(self):
        p = preparar(entradas=())
        r = p.recrutamento
        base = 799 * 276 + 0xa
        r.unidades[base + 0x42] = 2
        w(r.unidades, base + 6, 2)
        with self.assertRaisesRegex(ValueError, 'terminating domain'):
            p.preparar(0, 4)


def _entries(bloco, base):
    n = struct.unpack_from('<H', bloco, base)[0]
    return [(bloco[base + 0x42 + i], struct.unpack_from('<H', bloco, base + 6 + i * 2)[0]) for i in range(n)]


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional original x86: RISING_EMULAR=1')
class DiferencialSaidaTropa(unittest.TestCase):
    bancadas = []

    def setUp(self):
        self.nova_bancada()
        self.rng = random.Random(0x420e4c)

    def nova_bancada(self):
        from bancada_saida_tropa import BancadaSaidaTropa
        self.b = BancadaSaidaTropa()
        type(self).bancadas.append(self.b)

    def carregar(self, p):
        self.b.carregar_recrutamento(p.recrutamento)
        self.guardas = self.b.guardas_recrutamento(), self.b.guardas(), self.b.outras_guardas()

    def conferir(self, p):
        atual = self.b.estado()
        atual.update(self.b.estado_recrutamento())
        esperado = estado(p.recrutamento)
        for k, v in atual.items():
            self.assertTrue(v == esperado[k], k)
        self.assertEqual((self.b.guardas_recrutamento(), self.b.guardas(), self.b.outras_guardas()), self.guardas)

    def comparar(self, p, indice=0, direcao=4):
        from emulador import RETORNO
        self.carregar(p)
        chamadas = observar_depositos(p)
        esperado = p.preparar(indice, direcao)
        regs = self.b.preparar(indice, direcao)
        self.assertEqual(self.b.depositos_saida, chamadas)
        self.assertEqual(regs['EIP'], RETORNO if esperado is None else 0x420698)
        if esperado is not None:
            self.assertEqual((regs['EAX'], regs['EBX'], regs['ECX'], regs['ESI']),
                             (esperado.indice, esperado.direcao, 0, esperado.unidade))
        self.conferir(p)

    def test_threshold_unsigned_widths_and_no_activity_gate(self):
        for tempo in (0, 1, 65535):
            for valor in sorted({0, 1, max(0, tempo * 100 - 1), tempo * 100, 0x80000000, 0xffffffff}):
                for indice in (0, 999):
                    for flag in (0, 255):
                        p = preparar(indice=indice, entradas=())
                        r = p.recrutamento
                        w(r.tipos_unidades, 7 * 50, tempo)
                        d(r.mundo.estruturas, indice * 276 + 0x8c, valor)
                        r.mundo.estruturas[indice * 276 + 0x74] = flag
                        self.comparar(p, indice | 0xabcd0000, 0xface0104)

    def test_256_mixed_cargo_and_building_bags_whole_buffers(self):
        for n in range(256):
            indice, unidade, jogador = (0, 1, 999)[n % 3], (0, 1, 799)[n % 3], n % 4
            entradas = [(self.rng.choice((2, 3, 4)), self.rng.randrange(5)) for _ in range(n % 31)]
            p = preparar(indice, unidade, entradas)
            r = p.recrutamento
            o = indice * 276
            r.mundo.estruturas[o + 4] = jogador
            r.mundo.estruturas[o + 0x7b] = n % 26
            w(r.tipos_unidades, (n % 26) * 50, 10)
            r.mundo.estruturas[o + 8] = (1, 2, 3, 5, 8, 21)[n % 6]
            r.mundo.capacidades.configurar(jogador, 0 if n % 5 == 0 else 1, 3 + n % 100)
            r.mundo.terreno.semente = 1 + n * 1000
            w(r.unidades, unidade * 276 + 0xa + 0x66, (0, 1, 65535)[n % 3])
            self.comparar(p, indice, n)

    def test_capacity_limits_duplicate_colonists_and_counter_wrap(self):
        for n in range(1, 31):
            p = preparar(entradas=[(2, 2), (2, 1)] * (n // 2))
            r = p.recrutamento
            bag(r.mundo.estruturas, 0xc, [(1, 799)] * n, capacidade=n, contador=0)
            w(r.unidades, 799 * 276 + 0xa + 2, n)
            self.comparar(p)

    def test_full_seeded_buffers_preserve_untouched_bytes(self):
        for n in range(64):
            p = preparar(entradas=())
            r = p.recrutamento
            r.unidades[:] = self.rng.randbytes(len(r.unidades))
            r.mundo.estruturas[:] = self.rng.randbytes(len(r.mundo.estruturas))
            r.mundo.economia.memoria[:] = self.rng.randbytes(128)
            r.mundo.estruturas[4], r.mundo.estruturas[8], r.mundo.estruturas[0x7b] = 0, 8, 7
            d(r.mundo.estruturas, 0x8c, 1000)
            bag(r.mundo.estruturas, 0xc, [(3, 65535), (1, 799)], contador=n)
            r.unidades[799 * 276 + 1] = 9
            bag(r.unidades, 799 * 276 + 0xa, [(2, 2), (2, 0), (2, 1)], contador=0)
            self.comparar(p)

    def test_8_divide_exceptions_after_removal_and_credit(self):
        from emulador import unicorn, x86
        for n in range(8):
            if n:
                self.nova_bancada()  # No stale Unicorn exception state.
            p = preparar(entradas=((2, 1), (2, 2), (2, 2)))
            r = p.recrutamento
            r.mundo.capacidades.configurar(0, 1, 0)
            r.mundo.economia.atribuir(0, 2, 12000 + n)
            self.carregar(p)
            with self.assertRaises(ZeroDivisionError):
                p.preparar(0, n)
            with self.assertRaises(unicorn.UcError) as ctx:
                self.b.preparar(0, n)
            self.assertEqual(ctx.exception.errno, unicorn.UC_ERR_EXCEPTION)
            self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_EIP), 0x423501)
            self.b.excecoes_esperadas += 1
            self.conferir(p)

    def test_4_existing_deposit_dependency_stops_after_cargo_removal(self):
        for jogador in range(4):
            p = preparar(entradas=((2, 2), (2, 1)))
            r = p.recrutamento
            r.mundo.estruturas[4], r.mundo.estruturas[8] = jogador, 4
            w(r.mundo.estruturas, 0xe, 0)
            self.carregar(p)
            with self.assertRaises(RetiradaColonoPendente):
                p.preparar(0, 4)
            regs = self.b.preparar(0, 4)
            self.assertEqual(regs['EIP'], 0x41dde0)
            self.conferir(p)


if __name__ == '__main__':
    unittest.main()
