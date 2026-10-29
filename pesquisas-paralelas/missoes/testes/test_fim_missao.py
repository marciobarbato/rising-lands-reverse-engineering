"""EvenementEnCours/TestFinDeMission translation against the isolated original captures.

CPU-free: each captured call is rebuilt from exactly the bytes the intact
routine read before writing (with their entry values); every other byte is a
poison, and two different poisons must give the native result.  The native
differential over declared perturbations is the committed report checked at
the end.
"""
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ambiente_missoes
from economia import Economia
from fim_missao import (CONDICOES, CONTAGEM_INICIAL, ConsultasFimMissao, DependenciaFimMissao, ESTADO, EVENEMENT,
                        EXERCITOS, EXERCITOS_IA, consultas_publicadas, evento_em_curso, testar_fim_missao)
from oraculo_carga_missao import DGROUP

ISOLADA = ambiente_missoes.OWNED/'evidencias/captura-isolada-missoes-quadro1.json'
DIFERENCIAL = ambiente_missoes.OWNED/'validacao/m2-fim-missao-differential-x86.json'
ESTRUTURAS, RECURSOS, MISSAO, INFLUENCIA = 0x49a0c8, 0x4e2ea8, 0x496fe4, 0x50c614


def memoria_lida(caso, veneno):
    d = bytearray([veneno])*(DGROUP[1]-DGROUP[0])
    for endereco, valor, _ in caso['read_before_write']:
        a = int(endereco, 16)
        if DGROUP[0] <= a < DGROUP[1]:
            d[a-DGROUP[0]] = valor
    return d


def executar(d, jogador):
    f = lambda a, n: bytearray(d[a-DGROUP[0]:a-DGROUP[0]+n])
    estado = f(ESTADO, 14)
    antes = bytes(estado)
    q = consultas_publicadas(memoryview(bytes(f(ESTRUTURAS, 276000))), Economia(memoria=f(RECURSOS, 128)), f(MISSAO, 1),
                             f(INFLUENCIA, 4000))
    al = testar_fim_missao(jogador, f(CONDICOES, 100), estado, f(CONTAGEM_INICIAL, 2), f(EXERCITOS, 8),
                           f(EXERCITOS_IA, 16), q)
    return al, [[hex(ESTADO+i), antes[i], estado[i]] for i in range(14) if estado[i] != antes[i]]


@unittest.skipUnless(ISOLADA.exists(), 'Isolated capture not committed')
class TestCapturasIsoladas(unittest.TestCase):
    def setUp(self):
        self.cap = json.loads(ISOLADA.read_bytes())

    def test_evenement_en_cours_matches_both_frames(self):
        chamadas = [c for c in self.cap['calls'] if c['routine'] == 'EvenementEnCours']
        self.assertEqual([c['phase'] for c in chamadas], ['load_tail', 'frame1'])
        for c in chamadas:
            caso = c['cases'][0]
            self.assertEqual([r[0] for r in caso['read_before_write']], [hex(EVENEMENT)])
            for veneno in (0x00, 0xa5):
                self.assertEqual(evento_em_curso(memoria_lida(caso, veneno)[EVENEMENT-DGROUP[0]:][:1]), caso['al'])
            self.assertEqual(caso['changed_bytes'], [])

    def test_test_fin_de_mission_matches_both_frames_under_two_poisons(self):
        chamadas = [c for c in self.cap['calls'] if c['routine'] == 'TestFinDeMission']
        self.assertEqual([c['phase'] for c in chamadas], ['load_tail', 'frame1'])
        for c in chamadas:
            caso = c['cases'][0]
            jogador = int(caso['entry_registers']['EAX'], 16)
            for veneno in (0x00, 0xa5):
                self.assertEqual(executar(memoria_lida(caso, veneno), jogador), (caso['al'], caso['changed_bytes']))


class TestContratos(unittest.TestCase):
    def consultas(self, **mudar):
        base = dict(existe=lambda j: 0, dono=lambda j: 0, tipo=lambda j: 0, recursos=lambda *a: True,
                    numero_missao=lambda: 1)
        base.update(mudar)
        return ConsultasFimMissao(**base)

    def chamar(self, condicoes, consultas, estado=None, inicial=b'\x01\x00', jogador=0):
        estado = bytearray(14) if estado is None else estado
        return testar_fim_missao(jogador, bytearray(condicoes), estado, bytearray(inicial), bytearray(8),
                                 bytearray(16), consultas), estado

    def test_missing_provider_stops_at_the_original_call(self):
        condicoes = bytearray(b'\xfe'*100)
        condicoes[0] = 3
        with self.assertRaises(DependenciaFimMissao) as erro:
            self.chamar(condicoes, self.consultas())
        self.assertEqual(erro.exception.chamada, 0x45879c)

    def test_victory_sets_latch_and_mission8_needs_the_stack_local(self):
        condicoes = bytes([0, 0, 1, 0]) + b'\xff'*6 + b'\xfe'*90
        al, estado = self.chamar(condicoes, self.consultas())
        self.assertEqual((al, estado[0], estado[4]), (1, 1, 1))
        with self.assertRaises(DependenciaFimMissao) as erro:
            self.chamar(condicoes, self.consultas(numero_missao=lambda: 8))
        self.assertEqual(erro.exception.chamada, 0x4589dc)

    def test_views_have_exact_sizes(self):
        with self.assertRaises(ValueError):
            testar_fim_missao(0, bytearray(99), bytearray(14), bytearray(2), bytearray(8), bytearray(16),
                              self.consultas())
        with self.assertRaises(ValueError):
            testar_fim_missao(0, bytearray(100), bytes(14), bytearray(2), bytearray(8), bytearray(16),
                              self.consultas())

    @unittest.skipUnless(DIFERENCIAL.exists(), 'Native differential not committed')
    def test_committed_native_differential_passed(self):
        rel = json.loads(DIFERENCIAL.read_bytes())
        self.assertTrue(rel['passed'])
        self.assertEqual(rel['differing'], [])
        self.assertTrue(rel['path_reproduction']['passed'])


if __name__ == '__main__':
    unittest.main()
