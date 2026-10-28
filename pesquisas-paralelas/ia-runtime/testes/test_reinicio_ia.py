"""IaReset, IaAlloc and IAResetAttaque providers against whole-image native captures."""
import json
import os
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
from ambiente_ia_runtime import EXE, ORIGINAL_SHA256  # noqa: E402


def _documento():
    from capturar_reinicio_ia import ARQUIVO
    return json.loads(ARQUIVO.read_text(encoding='utf-8'))


@unittest.skipUnless(EXE.is_file(), 'intact RISING.EXE is not linked into this worktree (run workstream.py start)')
class CapturedWholeImages(unittest.TestCase):
    """Replay of the committed native observations; no Unicorn needed."""

    @classmethod
    def setUpClass(cls):
        from capturar_reinicio_ia import _expandir, aplicar_delta
        from oraculo_reinicio_ia import imagem_base
        cls.documento = _documento()
        cls.base = imagem_base()
        cls.iniciais = {c['caso']: aplicar_delta(cls.base, _expandir(c['imagem_inicial'])) for c in cls.documento['casos']}

    def caso(self, nome):
        return next(c for c in self.documento['casos'] if c['caso'] == nome)

    def test_identity_and_cases(self):
        self.assertEqual(self.documento['original_sha256'], ORIGINAL_SHA256)
        rotinas = [c['rotina'] for c in self.documento['casos']]
        self.assertEqual((rotinas.count('0x0047f36e'), rotinas.count('0x0047fb15'), rotinas.count('0x0047c162'),
                          len(rotinas)), (11, 3, 1, 19))
        for caso in self.documento['casos']:
            self.assertEqual(self.iniciais[caso['caso']].hashes(), caso['inicial'], caso['caso'])

    def test_every_case_reproduces_the_whole_native_image(self):
        from capturar_reinicio_ia import _expandir, executar_python
        for caso in self.documento['casos']:
            eax, final, mundo = executar_python(int(caso['rotina'], 16), self.iniciais[caso['caso']],
                                                _expandir(caso['observacoes']), caso['registradores'])
            self.assertTrue(mundo.completo(), caso['caso'])
            self.assertEqual(final.hashes(), caso['final'], caso['caso'])
            self.assertEqual(None if eax is None else f'0x{eax & 0xffffffff:08x}', caso['eax'], caso['caso'])

    def test_absent_provider_stops_at_the_original_call_site_with_the_native_state(self):
        from capturar_reinicio_ia import REGIOES_SEGMENTOS, _expandir
        from memoria_ia_runtime import MemoriaDeclarada
        from oraculo_reinicio_ia import MundoRepetido
        from reinicio_ia import REGIOES_REINICIO, DependenciaIA, reiniciar_ia
        contagem = 0
        for caso in self.documento['casos']:
            observacoes = _expandir(caso['observacoes'])
            for ponto in caso['pontos_parada']:
                copia = self.iniciais[caso['caso']].copia()
                memoria = MemoriaDeclarada(copia.segmentos(), REGIOES_REINICIO + REGIOES_SEGMENTOS)
                with self.assertRaises(DependenciaIA) as erro:
                    reiniciar_ia(memoria, MundoRepetido(observacoes, memoria, ate=ponto['chamada']))
                self.assertEqual((erro.exception.rotina, f'0x{erro.exception.sitio:08x}'),
                                 (ponto['rotina'], ponto['sitio']))
                self.assertEqual(copia.hashes(), ponto['imagem'], (caso['caso'], ponto['chamada']))
                contagem += 1
        self.assertEqual(contagem, 9)

    def test_no_world_provider_raises_before_any_store(self):
        from capturar_reinicio_ia import REGIOES_SEGMENTOS
        from memoria_ia_runtime import MemoriaDeclarada
        from reinicio_ia import REGIOES_REINICIO, DependenciaIA, iniciar_ia_programa, reiniciar_ia
        copia = self.iniciais['ia_reset_monde01'].copia()
        memoria = MemoriaDeclarada(copia.segmentos(), REGIOES_REINICIO + REGIOES_SEGMENTOS)
        with self.assertRaises(DependenciaIA) as erro:
            reiniciar_ia(memoria, None)
        self.assertEqual((erro.exception.rotina, erro.exception.sitio), ('PlayerGetType', 0x47f576))
        self.assertEqual(copia.hashes(), self.caso('ia_reset_monde01')['inicial'])
        with self.assertRaises(DependenciaIA) as erro:
            iniciar_ia_programa(memoria, None)
        self.assertEqual((erro.exception.rotina, erro.exception.sitio), ('timeGetTime', 0x489789))

    def test_undeclared_access_is_rejected(self):
        from capturar_reinicio_ia import REGIOES_SEGMENTOS
        from memoria_ia_runtime import AcessoNaoDeclarado, MemoriaDeclarada
        from reinicio_ia import REGIOES_REINICIO
        copia = self.base.copia()
        memoria = MemoriaDeclarada(copia.segmentos(), REGIOES_REINICIO + REGIOES_SEGMENTOS)
        for endereco in (0x49a0c8, 0x5080f4, 0x51b844 - 0x4e0000):
            with self.assertRaises(AcessoNaoDeclarado):
                memoria.u8(endereco)
        self.assertEqual(memoria.u32(0x4e19a0), 0x1000000)

    def test_spec_without_types_is_named_as_original_non_termination(self):
        """Same world calls as the terminating case; only the spec bytes (read after them) differ."""
        from capturar_reinicio_ia import REGIOES_SEGMENTOS, _expandir
        from memoria_ia_runtime import MemoriaDeclarada
        from oraculo_reinicio_ia import DADOS_BASE, MundoRepetido
        from reinicio_ia import REGIOES_REINICIO, NaoTerminaNoOriginal, reiniciar_ia
        caso = self.caso('ia_reset_monster_reserve_emptied')
        copia = self.iniciais[caso['caso']].copia()
        copia.dados[0x50af84 - DADOS_BASE + 4 * 26 + 20] = 0  # group 4 keeps its count but needs no type
        memoria = MemoriaDeclarada(copia.segmentos(), REGIOES_REINICIO + REGIOES_SEGMENTOS)
        with self.assertRaises(NaoTerminaNoOriginal) as erro:
            reiniciar_ia(memoria, MundoRepetido(_expandir(caso['observacoes']), memoria))
        self.assertEqual(erro.exception.sitio, 0x47b1f4)

    def test_monde01_case_facts(self):
        caso = self.caso('ia_reset_monde01')
        self.assertEqual(caso['chamadas_mundo'], {'EnginEstVivant': 800, 'EnginGetType': 16, 'MissionGetNum': 1,
                                                  'PlayerGetType': 13, 'TypeEnginEstMonstre': 16})
        self.assertEqual(caso['bytes_alterados'], {'dados': 2771, 'unidades': 0, 'jogadores': 0})


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'native comparison runs only with RISING_EMULAR=1')
@unittest.skipUnless(EXE.is_file(), 'intact RISING.EXE is not linked into this worktree')
class FreshNativeWholeImages(unittest.TestCase):
    def test_fresh_native_capture_equals_the_committed_document(self):
        from capturar_reinicio_ia import capturar
        fresco = json.loads(json.dumps(capturar()))
        comprometido = _documento()
        for novo, antigo in zip(fresco['casos'], comprometido['casos']):
            self.assertEqual(novo, antigo, novo['caso'])
        self.assertEqual(fresco, comprometido)
        print(f"\nnative whole-image cases: {len(fresco['casos'])}, world calls "
              f"{sum(sum(c['chamadas_mundo'].values()) for c in fresco['casos'])}, bench segments "
              f"{sum(c['segmentos_bancada'] for c in fresco['casos'])}, checkpoints "
              f"{sum(len(c['pontos_parada']) for c in fresco['casos'])}", file=sys.stderr)

    def test_fresh_native_runs_equal_the_python_translation(self):
        from capturar_reinicio_ia import casos, executar_nativo, executar_python
        from inventario_ia_runtime import OriginalImage
        image = OriginalImage()
        for nome, entrada, construir, extra, _ in casos():
            inicial = construir()
            nativo = executar_nativo(image, entrada, inicial, extra)
            eax, final, mundo = executar_python(entrada, inicial, nativo['observacoes'],
                                                extra if isinstance(extra, dict) else None)
            self.assertTrue(mundo.completo(), nome)
            self.assertEqual(final.dados, nativo['imagem'].dados, nome)
            self.assertEqual(final.unidades, nativo['imagem'].unidades, nome)
            self.assertEqual(final.jogadores, nativo['imagem'].jogadores, nome)
            if eax is not None:
                self.assertEqual(eax & 0xffffffff, nativo['eax'], nome)

    def test_original_loops_forever_on_a_spec_without_types(self):
        from capturar_reinicio_ia import executar_nativo
        from inventario_ia_runtime import OriginalImage
        from oraculo_reinicio_ia import DADOS_BASE, fixture_sintetica
        imagem = fixture_sintetica(9, monstros=6, tipos_monstro=(20,), grupos_monstros={4: (2, {})})
        self.assertEqual(imagem.dados[0x50af84 - DADOS_BASE + 4 * 26 + 20], 0)
        with self.assertRaisesRegex(RuntimeError, 'parada dentro do limite'):
            executar_nativo(OriginalImage(), 0x47f36e, imagem, None)


if __name__ == '__main__':
    unittest.main()
