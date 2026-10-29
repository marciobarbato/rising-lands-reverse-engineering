"""Real production delegates and host-alias guards; native comparisons are explicit."""
import json
import os
from pathlib import Path
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
from ambiente_ia_runtime import EXE
from capturar_reinicio_ia import ARQUIVO, _expandir, aplicar_delta
from memoria_ia_runtime import MemoriaDeclarada
from oraculo_reinicio_ia import imagem_base
from reinicio_ia_compartilhado import ReinicioIACompartilhado
from validar_adaptador_reinicio_ia import montar, validar


@unittest.skipUnless(EXE.is_file(), 'intact input not linked')
class SharedProduction(unittest.TestCase):
    def fixture(self):
        capture = next(c for c in json.loads(ARQUIVO.read_text())['casos'] if c['caso']=='ia_reset_monde01')
        image = aplicar_delta(imagem_base(), _expandir(capture['imagem_inicial']))
        return image, montar(image)

    def test_real_delegates_reproduce_or_name_stops_on_all_frozen_reset_inputs(self):
        report = validar()
        self.assertEqual(len(report['cases']), 11)
        self.assertTrue(all(c['production_delegates'] and not c['callback_replay'] for c in report['cases']))

    def test_equal_copies_are_rejected_before_any_store(self):
        for target, field in (('world','unidades'), ('world','grupos'), ('world','estruturas'),
                              ('market','jogadores'), ('economy','memoria')):
            image, provider = self.fixture()
            before = image.hashes()
            obj = {'world':provider.mundo, 'market':provider.mercado,
                   'economy':provider.mercado.economia}[target]
            setattr(obj, field, bytearray(getattr(obj, field)))
            with self.assertRaises(ValueError):
                ReinicioIACompartilhado(provider.memoria, provider.mundo, provider.mercado, provider.missao,
                                       pesquisa64=provider.pesquisa)
            self.assertEqual(image.hashes(), before)

    def test_scalar_disagreement_and_overlap_are_rejected(self):
        image, provider = self.fixture()
        before = image.hashes()
        provider.mundo.grupo_em_iteracao ^= 1
        with self.assertRaises(ValueError):
            ReinicioIACompartilhado(provider.memoria, provider.mundo, provider.mercado, provider.missao)
        provider.mundo.grupo_em_iteracao ^= 1
        segments = [(a, v) for a, _, v in provider.memoria.segmentos]
        segments.append(segments[0])
        overlapping = MemoriaDeclarada(segments, provider.memoria.regioes)
        with self.assertRaises(ValueError):
            ReinicioIACompartilhado(overlapping, provider.mundo, provider.mercado, provider.missao)
        self.assertEqual(image.hashes(), before)

    def test_controls_are_read_from_the_live_table_each_time(self):
        _, provider = self.fixture()
        provider.mercado.jogadores[1] = 2
        self.assertEqual(provider.PlayerGetType(0, sitio=0x47f576), 2)
        provider.mercado.jogadores[1] = 255
        self.assertEqual(provider.PlayerGetType(0, sitio=0x47f576), 255)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1' and EXE.is_file(), 'native comparison opt in')
class SharedProductionNative(unittest.TestCase):
    def test_fresh_whole_or_partial_original_images_equal_actual_delegates(self):
        report = validar(emular=True)
        self.assertTrue(all(c['fresh_native_image_equal'] for c in report['cases']))


if __name__=='__main__':
    unittest.main()
