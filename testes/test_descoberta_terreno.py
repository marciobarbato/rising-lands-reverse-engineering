"""Discovery/light beyond vision sum 8: captures, published domain and partial stops."""
import hashlib
import json
from pathlib import Path
import unittest

from test_colocacao_saida import MundoRastreado, resumo_python
from capturar_descoberta_terreno import preparar_caso
import colocacao_missao
import colocacao_saida
import insercao_unidades
import visao_movimento
from colocacao_missao import colocar_unidade_missao, DependenciaColocacaoMissao
from colocacao_saida import colocar_unidade_saida, DependenciaColocacaoSaida
from insercao_unidades import (SOMA_VISAO_MAXIMA_INSERCAO, RAIO_DESCOBERTA_MAXIMO_VALIDADO,
                               RAIO_LUZ_MAXIMO_VALIDADO)

RAIZ = Path(__file__).resolve().parents[1]


class MundoCelulas(MundoRastreado):
    """Adds the per-cell DecouvreCase/IllumineCase entry order to the effect trace."""
    def __init__(self, *args):
        self.celulas = []
        super().__init__(*args)

    def descobrir_celula(self, celula, dono):
        self.celulas.append(('discover_cell', celula, dono))
        return super().descobrir_celula(celula, dono)

    def iluminar_celula(self, celula, dono):
        self.celulas.append(('light_cell', celula, dono))
        return super().iluminar_celula(celula, dono)


def preparar(entrada='mission', largura=16, altura=16, celula=0x505, bb=1, f5=0, dono=0, camera=0,
             luz='fresh'):
    m = preparar_caso(entrada, largura, altura, celula, bb, f5, dono, camera, luz, classe=MundoCelulas)
    m.efeitos, m.celulas = [], []
    return m


def executar_python(m, entrada, celula, raio, dono):
    if entrada == 'mission':
        return colocar_unidade_missao(m, 7)
    if entrada == 'exit':
        return colocar_unidade_saida(m, 7, celula)
    if entrada == 'discover':
        return m.descobrir_area(celula, raio, dono)
    return m.iluminar_area(celula, raio, dono)


def hash_celulas(celulas):
    return hashlib.sha256(json.dumps([list(e) for e in celulas], separators=(',', ':')).encode()).hexdigest()


class DescobertaTerreno(unittest.TestCase):
    def test_seven_original_captures_whole_buffers_effects_and_cell_order(self):
        relatorio = json.loads((RAIZ/'relatorios/capturas-descoberta-terreno-original.json').read_text())
        self.assertFalse(relatorio['translation_executed'])
        self.assertEqual(len(relatorio['cases']), 7)
        for caso in relatorio['cases']:
            a = caso['input']
            m = preparar(a['entry'], a['width'], a['height'], a['cell'], a['bb'], a['f5'], a['owner'],
                         a['camera'], a['light_pattern'])
            executar_python(m, a['entry'], a['cell'], a['bb'], a['owner'])
            saida = resumo_python(m, 7)
            saida['native_cell_trace_count'] = len(m.celulas)
            saida['native_cell_trace_sha256'] = hash_celulas(m.celulas)
            self.assertEqual(saida, caso['output'])

    def test_published_domain_equals_original_byte_inventory(self):
        manifesto = json.loads((RAIZ/'evidencias/descoberta-terreno/manifesto.json').read_text())
        self.assertEqual(manifesto['reachable_vision_sum_max'], SOMA_VISAO_MAXIMA_INSERCAO)
        self.assertEqual(max(manifesto['domain']['type_bb_values'])+max(manifesto['domain']['f5_values']),
                         SOMA_VISAO_MAXIMA_INSERCAO)
        self.assertEqual(manifesto['domain']['map_count'], 38)
        self.assertLessEqual(max(manifesto['domain']['map_sum_values']), SOMA_VISAO_MAXIMA_INSERCAO)
        self.assertEqual(manifesto['direct_radius_max'],
                         dict(discovery=RAIO_DESCOBERTA_MAXIMO_VALIDADO, light=RAIO_LUZ_MAXIMO_VALIDADO))
        self.assertEqual(manifesto['structure_caller']['maximum_discovery_dx'], RAIO_DESCOBERTA_MAXIMO_VALIDADO)
        self.assertLessEqual(SOMA_VISAO_MAXIMA_INSERCAO+2, RAIO_DESCOBERTA_MAXIMO_VALIDADO)
        self.assertLessEqual(SOMA_VISAO_MAXIMA_INSERCAO, RAIO_LUZ_MAXIMO_VALIDADO)
        self.assertEqual(len(manifesto['writers']), 9)
        # Every consumer import path resolves the same published values.
        for modulo in (insercao_unidades, colocacao_missao, colocacao_saida):
            self.assertEqual(modulo.SOMA_VISAO_MAXIMA_INSERCAO, 11)
        for modulo in (visao_movimento, insercao_unidades, colocacao_missao, colocacao_saida):
            self.assertEqual((modulo.RAIO_DESCOBERTA_MAXIMO_VALIDADO, modulo.RAIO_LUZ_MAXIMO_VALIDADO), (23, 20))

    def test_new_sums_complete_both_callers_in_original_call_order(self):
        for entrada, celula in (('mission', 0x505), ('exit', 0x808)):
            for bb, f5 in ((9, 0), (8, 1), (10, 0), (10, 1), (0, 11)):
                m = preparar(entrada, celula=celula, bb=bb, f5=f5, dono=2, camera=2)
                executar_python(m, entrada, celula, 0, 2)
                soma = bb+f5
                visao = [e for e in m.efeitos if e[0] in ('collision', 'discovery', 'light')]
                self.assertEqual(visao, [('collision', 7, celula), ('discovery', celula, soma+2, 2),
                                         ('light', celula, soma, 2)])
                self.assertEqual(m.efeitos[-1], ('minimap', 2, celula, 4))
                self.assertEqual(m.unidades[7*276+0x72], 1)

    def test_sums_above_domain_stop_before_discovery_with_partial_effects(self):
        for entrada, celula, erro, parada in (('mission', 0x505, DependenciaColocacaoMissao, 0x457019),
                                             ('exit', 0x808, DependenciaColocacaoSaida, 0x446146)):
            for bb, f5 in ((12, 0), (11, 1), (0, 12), (255, 255)):
                m = preparar(entrada, celula=celula, bb=bb, f5=f5)
                descoberto, luz = bytes(m.descoberto[0]), bytes(m.contagem_luz[0])
                with self.assertRaises(erro) as captura:
                    executar_python(m, entrada, celula, 0, 0)
                self.assertEqual((captura.exception.checkpoint, captura.exception.endereco), (parada, 0x476851))
                self.assertEqual(m.efeitos, [('collision', 7, celula)])
                self.assertEqual((m.unidades[7*276+0x72], bytes(m.descoberto[0]), bytes(m.contagem_luz[0])),
                                 (1, descoberto, luz))
                self.assertEqual(m.celulas, [])

    def test_owners_4_and_200_never_reach_discovery_at_any_sum(self):
        for entrada, celula in (('mission', 0x505), ('exit', 0x808)):
            for dono in (4, 200):
                m = preparar(entrada, celula=celula, bb=255, f5=255, dono=dono)
                executar_python(m, entrada, celula, 0, dono)
                self.assertEqual(m.efeitos, [('collision', 7, celula), ('minimap', dono, celula, 4)])
                self.assertEqual(m.celulas, [])


if __name__ == '__main__':
    unittest.main()
