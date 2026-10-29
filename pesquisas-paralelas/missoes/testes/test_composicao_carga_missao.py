"""M1 composition of the whole MissionLoad vs the frozen original capture (CPU-free).

The main test runs the strict Python composition (no bridge exists) from the
frozen entry snapshot and compares it with the original capture: whole state,
AL, allocation records and ordered binding requests. A second run checks
determinism. Guards cover snapshot closure, the absence of constructor
defaults, the mandatory Economy per-owner Bag contract and alias identity.
"""
import ctypes
from pathlib import Path
import random
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ambiente_missoes
from mapa_memoria_m1 import MapaMemoriaM1, ErroMapaMemoria, carregar_blocos, carregar_json
from arena_composicao_m1 import ArenaComposicaoM1, ErroArenaM1
from ligacao_provedores_m1 import AtributoNaoMapeadoM1, EXCESSO, montar_provedores, verificar_excessos
from composicao_carga_missao import ComposicaoCargaMissaoM1
from comparacao_carga_missao import comparar_estado, comparar_vinculos

ENTRADA = ambiente_missoes.OWNED / 'evidencias/entrada-carga-missao-original.json'
CAPTURA = ambiente_missoes.OWNED / 'evidencias/captura-carga-missao-original-v2.json'
MIDIA = all((ambiente_missoes.CD / p).is_file() for p in ('WORLD/MONDE01.ETA', 'INSTALHD/MONSTRE.INI'))
TAILS_AFTER_STOP = ['EnginInitTechnologie', 'BatimentInitCave', 'Engin_RetrieveExperimente', 'PlayerRetrieve',
                    'IaReset', 'MarcheResetAll']


def _endereco(buffer):
    view = memoryview(buffer)
    return ctypes.addressof(ctypes.c_ubyte.from_buffer(view)), len(view)


class _Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entrada = carregar_json(ENTRADA)
        cls.blocos = carregar_blocos(cls.entrada['blocks'])

    def novo_mapa(self, blocos=None):
        mapa = MapaMemoriaM1(blocos or self.blocos)
        provedores = montar_provedores(mapa)
        mapa.fechar()
        return mapa, provedores


@unittest.skipUnless(MIDIA, 'original media WORLD/MONDE01.ETA and INSTALHD/MONSTRE.INI are required')
class ComposicaoVsCaptura(_Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.captura = carregar_json(CAPTURA)
        cls.estrita = ComposicaoCargaMissaoM1(cls.entrada)
        cls.resultado = cls.estrita.executar()
        cls.repeticao = ComposicaoCargaMissaoM1(cls.entrada)
        cls.resultado_repeticao = cls.repeticao.executar()

    def test_strict_composition_against_original_capture(self):
        r = self.resultado
        self.assertTrue(r.retornou, r.parada)
        self.assertIsNone(r.parada)
        self.assertEqual(r.al, 1)
        self.assertEqual([p['step'] for p in r.passos[-6:]], TAILS_AFTER_STOP)
        self.assertEqual(len(r.passos), 32)
        vinculos = comparar_vinculos(r.registro, self.captura)
        self.assertTrue(vinculos['equal'], vinculos['first_mismatches'])
        self.assertEqual((vinculos['original_events'], vinculos['composed_requests']), (1400, 1400))
        self.assertEqual(vinculos['original_arguments_not_captured']['count'], 16)
        estado = comparar_estado(self.estrita, self.captura, self.blocos, al=r.al)
        self.assertTrue(estado['equal'], estado['blocks'])
        self.assertEqual((estado['blocks_compared'], estado['bytes_compared']), (881, 2659375))
        self.assertEqual(estado['differing_bytes_or_blocks'], 0)
        self.assertEqual((estado['allocation_records']['original'], estado['allocation_records']['composed'],
                          estado['allocation_records']['differing']), (938, 938, 0))
        self.assertEqual(r.detalhes['excess_changed'], [])

    def test_strict_composition_is_deterministic(self):
        a, b = self.estrita.mapa.serializar(), self.repeticao.mapa.serializar()
        self.assertEqual(a, b)
        self.assertEqual(self.resultado.registro, self.resultado_repeticao.registro)
        self.assertEqual(self.estrita.arena.registros, self.repeticao.arena.registros)

    def test_ia_reset_receives_stack_copy_and_controls(self):
        passo = next(p for p in self.resultado.passos if p['step'] == 'IaReset')
        self.assertEqual(passo['al_argument_unused'], 1)
        self.assertEqual(passo['eax'], 0)
        jogadores = self.estrita.provedores.mercado.jogadores
        self.assertEqual([jogadores[20 * j + 1] for j in range(4)], [1, 2, 2, 2])


class FechamentoESemPadroes(_Base):
    def test_snapshot_closure(self):
        mapa, _ = self.novo_mapa()
        serializado = mapa.serializar()
        self.assertEqual(set(serializado), set(self.blocos))
        for nome, (base, dados) in self.blocos.items():
            self.assertEqual(serializado[nome], (base, dados), nome)
        cobertos = sum(s.fim - s.base for s in mapa.segmentos)
        self.assertEqual(cobertos, sum(len(d) for _, d in self.blocos.values()))

    def test_no_constructor_default_survives(self):
        lidos = set()

        class MapaRegistrado(MapaMemoriaM1):
            def ler_origem(self, endereco, tamanho):
                lidos.update(range(endereco, endereco + tamanho))
                return super().ler_origem(endereco, tamanho)
        mapa0 = MapaRegistrado(self.blocos)
        montar_provedores(mapa0)
        rng = random.Random(0x46c2cf)
        perturbados = {}
        for nome, (base, dados) in self.blocos.items():
            novo = bytearray(rng.randbytes(len(dados)))
            for a in lidos:
                if base <= a < base + len(dados):
                    novo[a - base] = dados[a - base]
            perturbados[nome] = (base, bytes(novo))
        mapa = MapaMemoriaM1(perturbados)
        provedores = montar_provedores(mapa)
        mapa.fechar()
        for nome, (base, dados) in mapa.serializar().items():
            self.assertEqual(dados, perturbados[nome][1], nome)
        w = provedores.mundo
        self.assertEqual(w.largura, struct.unpack_from('<H', mapa.ler(0x497168, 2))[0])
        self.assertEqual(w.semente_caminhos, mapa.u32(0x497164))
        self.assertEqual(w.tiles[0], struct.unpack('<H', mapa.ler(mapa.u32(0x507d70), 2))[0])
        self.assertEqual(verificar_excessos(provedores), [])
        for _, buffer, inicio in provedores.excessos:
            self.assertTrue(all(b == EXCESSO for b in bytes(buffer[inicio:])))

    def test_denied_and_rebinding_guards(self):
        _, provedores = self.novo_mapa()
        w, prop = provedores.mundo, provedores.habitacao.propriedade
        self.assertEqual(len(prop.ordens), 4)
        for a, b in zip(prop.ordens, w.bolsas_tipos_unidades):
            self.assertIs(a, b)
        with self.assertRaises(AtributoNaoMapeadoM1):
            prop.ordens = tuple(w.bolsas_tipos_unidades)
        with self.assertRaises(AtributoNaoMapeadoM1):
            w.solucionador
        with self.assertRaises(AtributoNaoMapeadoM1):
            w.unidades = bytearray(220800)
        with self.assertRaises(AtributoNaoMapeadoM1):
            prop.numeros_unidades = bytearray(208)
        w.largura = w.largura   # declared scalar caches stay assignable

    def test_per_owner_bag_contract_is_mandatory(self):
        import importlib.util
        import types
        caminho = ambiente_missoes.OWNED / 'ligacao_provedores_m1.py'
        real = sys.modules['proprietarios']
        legado = types.ModuleType('proprietarios')
        legado.PropriedadeConstrucoes = real.PropriedadeConstrucoes   # no validar_ordens
        sys.modules['proprietarios'] = legado
        try:
            spec = importlib.util.spec_from_file_location('ligacao_provedores_m1_sem_contrato', caminho)
            with self.assertRaises(ImportError):
                spec.loader.exec_module(importlib.util.module_from_spec(spec))
        finally:
            sys.modules['proprietarios'] = real

    def test_cache_divergence_is_detected(self):
        mapa, provedores = self.novo_mapa()
        w = provedores.mundo
        mapa.puxar()
        w.semente_caminhos ^= 1
        mapa.vista(0x497164, 4)[0] ^= 2
        with self.assertRaises(ErroMapaMemoria):
            mapa.empurrar()


class IdentidadeDeAliases(_Base):
    def test_provider_buffers_are_the_mapped_segments(self):
        mapa, p = self.novo_mapa()
        w = p.mundo
        for endereco, buffer in ((mapa.u32(0x4e19a0), w.unidades), (0x49a0c8, w.estruturas),
                                 (0x51a9e0, w.grupos), (0x4e2ea8, p.economia.memoria),
                                 (mapa.u32(0x5080a8), p.mercado.jogadores), (0x4dfba0, p.bonus.memoria)):
            self.assertIs(mapa._segmento(endereco, len(buffer)).buffer, buffer)
            self.assertEqual(_endereco(mapa.vista(endereco, len(buffer))), _endereco(buffer))
        construcoes = p.habitacao.construcoes
        self.assertIs(construcoes.estruturas, w.estruturas)
        self.assertIs(construcoes.contagens_por_tipo, w.realizaveis_estruturas)
        self.assertIs(construcoes.terreno.tipos, w.objetos)
        self.assertIs(p.habitacao.producao.recrutamento.unidades, w.unidades)
        self.assertIs(p.mercado.economia, p.economia)
        ordenados = sorted(mapa.segmentos, key=lambda s: s.base)
        self.assertTrue(all(a.fim <= b.base for a, b in zip(ordenados, ordenados[1:])))

    def test_ai_adapter_accepts_exact_live_aliasing(self):
        from reinicio_ia import REGIOES_REINICIO
        from reinicio_ia_compartilhado import ReinicioIACompartilhado
        mapa, p = self.novo_mapa()
        u, j = mapa.u32(0x4e19a0), mapa.u32(0x5080a8)
        memoria = mapa.memoria_declarada(REGIOES_REINICIO + ((u, u + 220800, 'units'), (j, j + 80, 'players')))
        ReinicioIACompartilhado(memoria, p.mundo, p.mercado, mapa.vista(0x496fe4, 1),
                                pesquisa64=mapa.vista(0x5080f4, 64))
        with self.assertRaises(ValueError):
            ReinicioIACompartilhado(memoria, p.mundo, p.mercado, bytearray(mapa.ler(0x496fe4, 1)))


class PoliticaArena(_Base):
    def test_page_aligned_bump_from_entry_next_free(self):
        mapa, _ = self.novo_mapa()
        registro = []
        arena = ArenaComposicaoM1(mapa, self.entrada['arena'], self.entrada['allocations'], registro)
        h = arena.alocar(0, 0x10000)
        self.assertEqual(h, 0x418e9000)
        buffer = arena.fixar(h)
        self.assertEqual(bytes(buffer[:4]), b'\xa7' * 4)
        self.assertEqual(arena.obter_handle(buffer), h)
        z = arena.alocar(0x40, 3)
        self.assertEqual(z, 0x418f9000)
        self.assertEqual(bytes(arena.fixar(z)), bytes(3))
        self.assertEqual(arena.alocar(0, 1), 0x418fa000)
        with self.assertRaises(ErroArenaM1):
            arena.liberar(h)              # still locked
        arena.desfixar(h)
        with self.assertRaises(ErroArenaM1):
            arena.desfixar(h)             # unlock without lock
        arena.liberar(h)
        self.assertFalse(arena.registros[881]['active'])
        self.assertIn('freed_sha256', arena.registros[881])
        with self.assertRaises(ErroArenaM1):
            arena.fixar(h)                # stale handle, never reused
        self.assertNotIn('alloc00881', mapa.blocos)
        with self.assertRaises(ErroArenaM1):
            arena.alocar(2, 16)           # GMEM_MOVEABLE outside the policy
        self.assertEqual([e['name'] for e in registro][:3],
                         ['KERNEL32.GlobalAlloc', 'KERNEL32.GlobalLock', 'KERNEL32.GlobalHandle'])


if __name__ == '__main__':
    unittest.main()
